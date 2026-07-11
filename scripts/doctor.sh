#!/usr/bin/env bash
# hub.doctor — idempotent environment check/setup for rhoai-agentic-hub.
# Usage: bash scripts/doctor.sh [check|setup]   (default: check)
set -u
MODE="${1:-check}"
# pwd -W yields a Windows-style path (C:/...) under Git Bash so values passed
# to Windows-native python/JSON are correct; plain pwd elsewhere.
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && (pwd -W 2>/dev/null || pwd))"
PASS=0; WARN=0; FAIL=0
ok()   { echo "  OK    $1"; PASS=$((PASS+1)); }
warn() { echo "  WARN  $1"; WARN=$((WARN+1)); }
fail() { echo "  FAIL  $1"; FAIL=$((FAIL+1)); }
note() { echo "        $1"; }   # follow-on detail; no counter

echo "== hub.doctor ($MODE) — $ROOT"

echo "[1] python + deps"
if python -c "import yaml, pytest, httpx" 2>/dev/null; then
  ok "python + pyyaml + pytest + httpx"
elif [ "$MODE" = "setup" ]; then
  pip install -r "$ROOT/scripts/requirements.txt" && ok "deps installed" || fail "pip install failed"
else
  fail "missing python deps — run: pip install -r scripts/requirements.txt (or doctor setup)"
fi

echo "[2] marketplace wiring + plugin installs"
SETTINGS="$ROOT/.claude/settings.json"
if [ -f "$SETTINGS" ] && grep -q "opendatahub-skills" "$SETTINGS"; then
  ok "settings.json declares ODH marketplace"
else
  fail ".claude/settings.json missing ODH marketplace block"
fi
# Enablement (settings.json enabledPlugins) is NOT installation (the plugin
# cache): /plugin clones each plugin into the profile's plugins dir. Enabled
# but not installed means /rfe.create, /assess-rfe etc. silently don't exist
# as skills (hit on 2026-07-10). There is no non-interactive install
# (`claude plugin` has enable/disable but no install), so setup cannot do it;
# what setup CAN fix is the known install blocker: the plugin installer
# clones github-source plugins over SSH (git@github.com:), which dies with
# "Permission denied (publickey)" on machines without a GitHub SSH key
# unless the https insteadOf rewrite is present (see
# memory/.scratch or fact-hub-build-operational-gotchas for lineage).
PLUGROOT="${CLAUDE_CONFIG_DIR:-$HOME/.claude}/plugins"
INSTALLED_JSON="$PLUGROOT/installed_plugins.json"
MISSING_PLUGINS=""
if [ -f "$SETTINGS" ]; then
  while IFS= read -r plug; do
    plug="${plug%$'\r'}"   # Windows python prints \r\n; a kept \r breaks the grep
    [ -z "$plug" ] && continue
    if [ -f "$INSTALLED_JSON" ] && grep -qF "\"$plug\"" "$INSTALLED_JSON"; then
      ok "plugin installed: $plug"
    else
      MISSING_PLUGINS="$MISSING_PLUGINS $plug"
      fail "plugin enabled but NOT installed: $plug (its skills won't exist in Claude Code)"
    fi
  done < <(python - "$SETTINGS" <<'PY'
import json, sys
try:
    d = json.load(open(sys.argv[1]))
except Exception:
    sys.exit(0)
for name, enabled in (d.get("enabledPlugins") or {}).items():
    if enabled:
        print(name)
PY
)
fi
if [ -n "$MISSING_PLUGINS" ]; then
  # Precondition for the interactive install: can this machine clone from
  # github at all the way the installer will try to?
  if git config --global --get "url.https://github.com/.insteadof" >/dev/null 2>&1; then
    ok "github ssh->https rewrite present (plugin clones will work)"
  elif GIT_SSH_COMMAND="ssh -o BatchMode=yes -o ConnectTimeout=5" \
       git ls-remote git@github.com:opendatahub-io/skills-registry.git HEAD >/dev/null 2>&1; then
    ok "github ssh access works (plugin clones will work)"
  elif [ "$MODE" = "setup" ]; then
    if git config --global url."https://github.com/".insteadOf "git@github.com:"; then
      ok "applied github ssh->https rewrite (installer clones over ssh; no key on this machine)"
    else
      fail "could not set the git insteadOf rewrite"
    fi
  else
    fail "plugin install would fail: no github ssh key and no https rewrite - run: bash scripts/doctor.sh setup"
    note "(setup applies: git config --global url.\"https://github.com/\".insteadOf \"git@github.com:\")"
  fi
  note "then install inside Claude Code: /plugin -> marketplace opendatahub-skills ->$MISSING_PLUGINS"
  note "accept the workspace trust prompt if asked; finish with /reload-plugins (or restart)"
fi

echo "[3] auto-memory scratch redirect"
SCRATCH="$ROOT/memory/.scratch"
LOCAL="$ROOT/.claude/settings.local.json"
if [ -f "$LOCAL" ] && python - "$LOCAL" "$SCRATCH" <<'PY'
import json, sys, pathlib
data = json.load(open(sys.argv[1]))
cur = data.get("autoMemoryDirectory", "")
sys.exit(0 if cur and pathlib.Path(cur).as_posix() == pathlib.Path(sys.argv[2]).as_posix() else 1)
PY
then
  ok "autoMemoryDirectory -> memory/.scratch"
elif [ "$MODE" = "setup" ]; then
  mkdir -p "$SCRATCH"
  if python - "$LOCAL" "$SCRATCH" <<'PY'
import json, os, sys
path, want = sys.argv[1], sys.argv[2]
data = {}
if os.path.exists(path):
    data = json.load(open(path))
data["autoMemoryDirectory"] = want
os.makedirs(os.path.dirname(path), exist_ok=True)
with open(path, "w") as fh:
    json.dump(data, fh, indent=2)
print("  wrote", path)
PY
  then
    ok "autoMemoryDirectory written (restart Claude Code to take effect)"
  else
    fail "could not write $LOCAL (pre-existing invalid JSON? permissions?)"
  fi
else
  fail "autoMemoryDirectory not set — run: bash scripts/doctor.sh setup"
fi

echo "[4] restricted/.env + shell wiring"
# The .env carries repo tooling secrets only (Jira, MCP servers, tracker
# overrides) — never LLM-provider credentials; Claude Code/Cursor is set up
# before this repo and the hub never configures or touches that auth.
ENV_FILE="$ROOT/restricted/.env"
if [ -f "$ENV_FILE" ]; then
  # Source it (values never printed) so later sections can use it: section
  # 7's CTRACK_* overrides, sections 8-9's MCP secrets. Handles both KEY=
  # and 'export KEY=' line forms, which a plain grep for ^KEY= would not.
  set -a
  # shellcheck disable=SC1090
  . "$ENV_FILE"
  set +a
  for k in JIRA_SERVER JIRA_USER JIRA_TOKEN; do
    if [ -n "${!k:-}" ]; then ok "$k present"; else warn "$k missing in restricted/.env"; fi
  done
  # Live probe (backlog #19's Jira slice): presence is not validity. WARN,
  # not FAIL — offline machines must still pass the doctor.
  if [ -n "${JIRA_SERVER:-}" ] && [ -n "${JIRA_TOKEN:-}" ]; then
    if python "$ROOT/scripts/hub_jira.py" --check >/dev/null 2>&1; then
      ok "jira reachable (hub_jira --check)"
    else
      warn "jira unreachable or auth failed — run: python scripts/hub_jira.py --check (expired JIRA_TOKEN? offline?)"
    fi
  fi
  # Shell wiring (backlog #19). Hub tooling self-loads restricted/.env, but the
  # marketplace rfe.* scripts read os.environ with no fallback, so JIRA_* must
  # reach every shell. hub_env.py owns the ~/.bashrc block and removes the
  # retired ai-asset-registry one. Logic lives in python because it is tested;
  # idempotent profile editing is where bash quietly gets it wrong.
  if [ "$MODE" = "setup" ]; then ENV_MODE="--setup"; else ENV_MODE="--check"; fi
  # Capture output + exit status (stderr merged in) instead of streaming a
  # discarded-stderr process substitution: a crashing CLI must WARN, not
  # silently move zero counters while doctor still prints 0 fail.
  ENV_OUT="$(python "$ROOT/scripts/hub_env.py" $ENV_MODE 2>&1)"
  ENV_STATUS=$?
  if [ $ENV_STATUS -ne 0 ] || [ -z "$ENV_OUT" ]; then
    warn "hub_env.py $ENV_MODE did not run (exit $ENV_STATUS) - run by hand to diagnose: python scripts/hub_env.py $ENV_MODE"
  else
    # Here-string, not a pipe: a pipe would put this loop in a subshell and
    # lose the ok/warn counter increments.
    while IFS=$'\t' read -r kind msg; do
      case "$kind" in
        ok)    ok "$msg" ;;
        wrote) ok "$msg (open a new shell for it to take effect)" ;;
        warn)  warn "$msg" ;;
        *)     [ -n "${kind:-}" ] && warn "hub_env.py produced unexpected output: $kind" ;;
      esac
    done <<< "$ENV_OUT"
  fi
else
  warn "restricted/.env not found (Jira-facing skills and MCP setup won't work; copy it from your other machine)"
fi

echo "[5] pages repo clone (optional convenience)"
if [ -d "$ROOT/../rhoai-agentic-hub-pages/.git" ]; then
  ok "pages repo cloned alongside"
else
  warn "pages repo not cloned at ../rhoai-agentic-hub-pages (CI publishes regardless)"
fi

echo "[6] structure"
if python "$ROOT/scripts/hub_lint.py" >/dev/null; then ok "hub_lint: 0 errors"; else fail "hub_lint errors — run: python scripts/hub_lint.py"; fi
if python "$ROOT/scripts/hub_index.py" --check >/dev/null; then ok "indexes fresh"; else warn "indexes stale — run: python scripts/hub_index.py"; fi

echo "[7] customer tracker (rhai-tracker MCP)"
# Ported/adapted from ai-asset-registry's repo-doctor bootstrap.sh section 5
# (C:/Users/peter/code/rh/ai-asset-registry/.claude/skills/repo-doctor/bootstrap.sh).
# Being on disk is NOT enough for the MCP to work — four separate states,
# each reported separately so "cloned" can't masquerade as "functional":
# (a) clone present, (b) registered in .mcp.json, (c) node deps installed,
# (d) server/.env present.
# Override keys (set in restricted/.env): CTRACK_DIR (where the clone lives)
# and CTRACK_REPO_URL (where to clone it from — surfaced in the remediation
# message below; this section does not auto-clone).
CTRACK_DIR="${CTRACK_DIR:-../rhai-customer-tracker}"
# Default assumes a sibling clone named rhai-customer-tracker, matching the
# upstream repo name. Override
# CTRACK_DIR in restricted/.env if your clone lives elsewhere or under a
# different name.
case "$CTRACK_DIR" in /*|?:*) ABS_CTRACK="$CTRACK_DIR" ;; *) ABS_CTRACK="$ROOT/$CTRACK_DIR" ;; esac
SERVER_JS="$ABS_CTRACK/server/mcp-server.js"
SERVER_DIR="$ABS_CTRACK/server"

# 7a. clone / presence
if [ -f "$SERVER_JS" ]; then
  ok "rhai-customer-tracker present ($ABS_CTRACK)"
else
  fail "rhai-customer-tracker missing at $ABS_CTRACK (clone ${CTRACK_REPO_URL:-git@gitlab.cee.redhat.com:rh-ai-pm/rhai-customer-tracker.git}, or set CTRACK_DIR/CTRACK_REPO_URL in restricted/.env)"
fi

# 7b. register in .mcp.json — creates the file if absent (gitignored; see
# the .mcp.json line in .gitignore). Idempotent: an unchanged path is a
# no-op OK, never a rewrite.
if [ -f "$SERVER_JS" ]; then
  RESULT=$(python - "$ROOT/.mcp.json" "$SERVER_JS" "$MODE" <<'PY'
import json, os, shutil, sys
p, server, mode = sys.argv[1], sys.argv[2], sys.argv[3]
try:
    d = json.load(open(p))
    if not isinstance(d, dict): d = {}
except Exception:
    d = {}
srv = d.setdefault("mcpServers", {})
cur = (srv.get("rhai-tracker", {}).get("args", [None]) or [None])[-1] or ""
if cur.lower() == server.lower():
    print("ok")
elif mode == "setup":
    if os.path.exists(p): shutil.copy(p, p + ".bak")
    srv["rhai-tracker"] = {"command": "node", "args": [server]}
    json.dump(d, open(p, "w"), indent=2)
    open(p, "a").write("\n")
    print("wrote")
elif cur:
    print("warn:" + cur)
else:
    print("fail")
PY
)
  case "$RESULT" in
    ok)     ok ".mcp.json rhai-tracker registered" ;;
    wrote)  ok ".mcp.json rhai-tracker registered -> $SERVER_JS (restart Claude Code)" ;;
    warn:*) warn ".mcp.json path (${RESULT#warn:}) != $SERVER_JS — run: bash scripts/doctor.sh setup" ;;
    fail)   fail "rhai-tracker not registered in .mcp.json — run: bash scripts/doctor.sh setup" ;;
    *)      warn "could not evaluate .mcp.json (python error?)" ;;
  esac
fi

# 7c. node deps — the server won't start without them
if [ -f "$SERVER_JS" ]; then
  if [ -d "$SERVER_DIR/node_modules" ]; then
    ok "tracker server deps installed"
  elif [ "$MODE" = "setup" ]; then
    if command -v npm >/dev/null; then
      ( cd "$SERVER_DIR" && npm install >/dev/null 2>&1 ) && ok "tracker server deps installed" || fail "npm install failed in $SERVER_DIR (run it by hand to see why)"
    else
      fail "npm not found — cannot install tracker server deps"
    fi
  else
    warn "tracker server deps not installed — run: bash scripts/doctor.sh setup (needs npm)"
  fi
fi

# 7d. server/.env — Google Sheets + AI-provider secrets, NOT in restricted/.env.
# setup only scaffolds the template; it never invents secret values.
if [ -f "$SERVER_JS" ]; then
  SENV="$SERVER_DIR/.env"
  if [ -f "$SENV" ]; then
    ok "tracker server/.env present"
  elif [ "$MODE" = "setup" ] && [ -f "$ABS_CTRACK/.env.example" ]; then
    cp "$ABS_CTRACK/.env.example" "$SENV"
    warn "scaffolded tracker server/.env from .env.example — fill GOOGLE_SPREADSHEET_ID, Google OAuth client ID/secret, and an AI_PROVIDER (see rhai-customer-tracker README)"
  else
    warn "tracker server/.env missing (needs GOOGLE_SPREADSHEET_ID + Google OAuth + AI provider)"
  fi
fi

echo "[8] Claude MCP servers (slack + google-workspace)"
# Ported/adapted from ai-asset-registry's repo-doctor bootstrap.sh section 6
# (C:/Users/peter/code/rh/ai-asset-registry/.claude/skills/repo-doctor/).
# These two servers are USER-scoped — they live in the Claude config and
# follow the profile, not the repo — so "not configured" can simply mean the
# wrong profile is active. Full guide + traps: docs/mcp-servers.md.
# setup writes each missing server (definition + secrets from restricted/
# .env, sourced in section 4) into the config, backing it up to *.bak first.
# Severity is intent-aware: missing server + secrets available = FAIL (setup
# can fix it); missing server + no secrets = WARN (optional, nothing to do).
CFG="${CLAUDE_CONFIG_DIR:+$CLAUDE_CONFIG_DIR/}"; CFG="${CFG:-$HOME/}.claude.json"
[ -f "$CFG" ] || CFG="$HOME/.claude.json"
note "target config: $CFG (profile-dependent — see docs/mcp-servers.md)"
while IFS=$'\t' read -r kind msg; do
  case "$kind" in
    ok)    ok "$msg" ;;
    wrote) ok "$msg (restart Claude Code)" ;;
    warn)  warn "$msg" ;;
    fail)  fail "$msg" ;;
    *)     [ -n "${kind:-}" ] && warn "could not evaluate Claude config (python error?)" ;;
  esac
done < <(python - "$CFG" "$MODE" <<'PY'
import json, os, shutil, sys
cfg, mode = sys.argv[1], sys.argv[2]
try:
    d = json.load(open(cfg))
    if not isinstance(d, dict): d = {}
except Exception:
    d = {}
srv = d.setdefault("mcpServers", {})
def want_slack():
    return {"command": "podman", "args": ["run", "-i", "--rm",
        "-e", "SLACK_XOXC_TOKEN", "-e", "SLACK_XOXD_TOKEN",
        "-e", "MCP_TRANSPORT", "-e", "LOGS_CHANNEL_ID",
        "quay.io/redhat-ai-tools/slack-mcp"],
        "env": {"SLACK_XOXC_TOKEN": os.environ.get("SLACK_XOXC_TOKEN", ""),
                "SLACK_XOXD_TOKEN": os.environ.get("SLACK_XOXD_TOKEN", ""),
                "MCP_TRANSPORT": os.environ.get("SLACK_MCP_TRANSPORT", "stdio"),
                "LOGS_CHANNEL_ID": os.environ.get("SLACK_LOGS_CHANNEL_ID", "")}}
def want_google():
    return {"type": "stdio", "command": "uvx", "args": ["workspace-mcp"],
        "env": {"GOOGLE_OAUTH_CLIENT_ID": os.environ.get("GOOGLE_OAUTH_CLIENT_ID", ""),
                "GOOGLE_OAUTH_CLIENT_SECRET": os.environ.get("GOOGLE_OAUTH_CLIENT_SECRET", ""),
                "USER_GOOGLE_EMAIL": os.environ.get("USER_GOOGLE_EMAIL", ""),
                "OAUTHLIB_INSECURE_TRANSPORT": os.environ.get("OAUTHLIB_INSECURE_TRANSPORT", "1")}}
report = []; changed = False
for name, builder, tok in (("slack", want_slack, "SLACK_XOXC_TOKEN"),
                           ("google-workspace", want_google, "GOOGLE_OAUTH_CLIENT_ID")):
    have_secret = bool(os.environ.get(tok))
    if name in srv and srv[name].get("env", {}).get(tok):
        report.append(("ok", f"{name} configured")); continue
    if mode == "setup":
        if have_secret:
            srv[name] = builder(); changed = True
            report.append(("wrote", f"{name} written to {cfg}"))
        else:
            report.append(("warn", f"{name}: {tok} not in restricted/.env - skipped (docs/mcp-servers.md)"))
    elif have_secret:
        report.append(("fail", f"{name} not configured - run: bash scripts/doctor.sh setup (or wrong profile? docs/mcp-servers.md)"))
    else:
        report.append(("warn", f"{name} not configured and no {tok} in restricted/.env - optional (docs/mcp-servers.md)"))
if changed:
    if os.path.exists(cfg): shutil.copy(cfg, cfg + ".bak")
    json.dump(d, open(cfg, "w"), indent=2)
for kind, msg in report: print(f"{kind}\t{msg}")
PY
)

echo "[9] slack MCP runtime (podman) + auth probe"
# Ported/adapted from ai-asset-registry's repo-doctor bootstrap.sh section 7.
# Section 8 can write the slack config while the thing that RUNS it is
# missing — "slack configured" does NOT mean slack will load. Its command is
# 'podman run … slack-mcp', so verify that runtime. Two traps this catches:
#   1. Podman DESKTOP (the GUI) installed but the podman ENGINE (CLI) not —
#      the GUI ships no podman.exe; the MCP silently never loads.
#   2. Engine installed but absent from THIS shell's PATH (session predates
#      the install) — a restarted Claude Code would find it, so the known
#      Windows install path is checked too before calling it missing.
# The engine install itself needs an ADMIN shell (winget's UAC prompt fails
# silently otherwise), so it stays manual; setup starts the machine and
# pre-pulls the image.
IMG="quay.io/redhat-ai-tools/slack-mcp"
SLACK_WANTED=0
[ -n "${SLACK_XOXC_TOKEN:-}" ] && SLACK_WANTED=1
if [ "$SLACK_WANTED" = 0 ] && [ -f "$CFG" ]; then
  python -c 'import json,sys;d=json.load(open(sys.argv[1]));sys.exit(0 if "slack" in d.get("mcpServers",{}) else 1)' "$CFG" 2>/dev/null && SLACK_WANTED=1
fi
if [ "$SLACK_WANTED" = 0 ]; then
  note "slack MCP not configured and no SLACK_XOXC_TOKEN — skipping podman checks"
else
  # Tokens are short-lived SESSION tokens (xoxc/xoxd) — presence is not
  # validity. The extractor names them SLACK_MCP_XOXC_TOKEN/XOXD; rename to
  # SLACK_XOXC_TOKEN/XOXD when pasting into restricted/.env.
  if [ -n "${SLACK_XOXC_TOKEN:-}" ]; then
    ok "slack tokens present (they EXPIRE — 'invalid_auth' means re-extract; docs/mcp-servers.md)"
  else
    warn "no SLACK_XOXC_TOKEN in this shell/restricted/.env — slack needs fresh session tokens (docs/mcp-servers.md)"
  fi

  # Locate the engine CLI: PATH first, then the known Windows install path
  # so a stale shell PATH doesn't masquerade as "not installed".
  PODMAN=""; PODMAN_ONPATH=0
  if command -v podman >/dev/null 2>&1; then PODMAN="podman"; PODMAN_ONPATH=1
  else
    for cand in "/c/Program Files/RedHat/Podman/podman.exe" \
                "${PROGRAMFILES:-/c/Program Files}/RedHat/Podman/podman.exe" \
                "${ProgramW6432:-}/RedHat/Podman/podman.exe"; do
      [ -n "$cand" ] && [ -x "$cand" ] && { PODMAN="$cand"; break; }
    done
  fi

  if [ -z "$PODMAN" ]; then
    DESKTOP=""
    for dsk in "/c/Program Files/Podman Desktop/Podman Desktop.exe" \
               "${PROGRAMFILES:-/c/Program Files}/Podman Desktop/Podman Desktop.exe"; do
      [ -f "$dsk" ] && { DESKTOP="$dsk"; break; }
    done
    if [ -n "$DESKTOP" ]; then
      fail "Podman Desktop is installed but the podman ENGINE (CLI) is not — the GUI alone can't run the slack MCP"
    else
      fail "podman not installed (the slack MCP runs 'podman run … $IMG')"
    fi
    note "install the engine in an ADMIN shell (winget's UAC prompt fails silently from here):"
    note "  winget install --id RedHat.Podman -e --accept-source-agreements --accept-package-agreements"
    note "then re-run 'bash scripts/doctor.sh setup' to start the machine and pre-pull the image"
  else
    if [ "$PODMAN_ONPATH" = 1 ]; then
      ok "podman engine on PATH ($("$PODMAN" --version 2>/dev/null))"
    else
      ok "podman engine installed ($("$PODMAN" --version 2>/dev/null)) — not on THIS shell's PATH yet (a restarted Claude Code will resolve it)"
    fi

    # Machine state: running is ideal; stopped -> start it in setup; none ->
    # 'machine init' is interactive/heavy (downloads a WSL VM image), manual.
    MACHINE_UP=0
    RUNNING=$("$PODMAN" machine list --format '{{.Running}}' 2>/dev/null | grep -ci true || true)
    HAVE_MACHINE=$("$PODMAN" machine list --format '{{.Name}}' 2>/dev/null | grep -c . || true)
    if [ "${RUNNING:-0}" -ge 1 ]; then
      ok "podman machine running"; MACHINE_UP=1
    elif [ "${HAVE_MACHINE:-0}" -ge 1 ]; then
      if [ "$MODE" = "setup" ]; then
        if "$PODMAN" machine start >/dev/null 2>&1; then
          ok "podman machine started (restart Claude Code)"; MACHINE_UP=1
        else
          fail "podman machine start failed (run '$PODMAN machine start' by hand to see why)"
        fi
      else
        fail "podman machine is stopped — run: bash scripts/doctor.sh setup (or: podman machine start)"
      fi
    else
      fail "no podman machine exists — run interactively: podman machine init && podman machine start"
    fi

    # Image: pre-pull in setup so the first Slack call isn't a slow pull.
    if "$PODMAN" image exists "$IMG" 2>/dev/null; then
      ok "slack-mcp image present ($IMG)"
    elif [ "$MODE" = "setup" ] && [ "$MACHINE_UP" = 1 ]; then
      if "$PODMAN" pull "$IMG" >/dev/null 2>&1; then
        ok "slack-mcp image pulled"
      else
        warn "could not pull $IMG (needs a running machine + network)"
      fi
    else
      warn "slack-mcp image not pulled yet (setup pre-pulls it; first use would pull on demand, slowly)"
    fi
  fi
fi

# Auth probe (backlog #19). Section 8 proves the server is REGISTERED;
# registration is not validity. xoxc/xoxd are per-login session tokens that do
# not travel between machines, the exact gap R5 predicted for machine B.
# WARN only, so an offline machine still reaches 0 fail.
# Capture output + exit status (stderr merged in) instead of streaming a
# discarded-stderr process substitution: a crashing CLI must WARN, not
# silently move zero counters while doctor still prints 0 fail.
SLACK_OUT="$(python "$ROOT/scripts/hub_slack.py" --check 2>&1)"
SLACK_STATUS=$?
if [ $SLACK_STATUS -ne 0 ] || [ -z "$SLACK_OUT" ]; then
  warn "hub_slack.py --check did not run (exit $SLACK_STATUS) - run by hand to diagnose: python scripts/hub_slack.py --check"
else
  # Here-string, not a pipe: a pipe would put this loop in a subshell and
  # lose the ok/warn counter increments.
  while IFS=$'\t' read -r kind msg; do
    case "$kind" in
      ok)   ok "$msg" ;;
      warn) warn "$msg" ;;
      *)    [ -n "${kind:-}" ] && warn "hub_slack.py produced unexpected output: $kind" ;;
    esac
  done <<< "$SLACK_OUT"
fi

echo "[10] git pre-commit hook"
# Kills the #1 CI failure (edit -> forget reindex -> red) and runs the
# disclosure lint at the earliest possible moment. In a worktree .git is a
# FILE, so resolve the hooks dir via git, never hardcode .git/hooks.
HOOKS_DIR="$(cd "$ROOT" 2>/dev/null && git rev-parse --git-path hooks 2>/dev/null)"
case "$HOOKS_DIR" in
  "") : ;;
  /*|?:*) : ;;
  *) HOOKS_DIR="$ROOT/$HOOKS_DIR" ;;
esac
HOOK="${HOOKS_DIR:+$HOOKS_DIR/pre-commit}"
HOOK_MARKER="# hub-doctor pre-commit v1"
write_hook() {
  mkdir -p "$HOOKS_DIR" && cat > "$HOOK" <<'HOOKEOF' && chmod +x "$HOOK"
#!/bin/sh
# hub-doctor pre-commit v1 — installed by scripts/doctor.sh setup
python scripts/hub_lint.py && python scripts/hub_index.py --check
status=$?
if [ $status -ne 0 ]; then
  echo ""
  echo "pre-commit: hub gate failed."
  echo "  stale indexes     -> python scripts/hub_index.py"
  echo "  deliberate bypass -> git commit --no-verify"
fi
exit $status
HOOKEOF
}
if [ -z "$HOOKS_DIR" ]; then
  warn "not a git repo? could not resolve the hooks dir — skipping hook check"
elif [ -f "$HOOK" ] && grep -qF "$HOOK_MARKER" "$HOOK"; then
  ok "pre-commit hook installed (current version)"
elif [ -f "$HOOK" ] && grep -q "hub-doctor pre-commit" "$HOOK"; then
  if [ "$MODE" = "setup" ]; then
    cp "$HOOK" "$HOOK.bak" && write_hook && ok "pre-commit hook updated (old version -> pre-commit.bak)" || fail "could not write pre-commit hook"
  else
    warn "pre-commit hook is an outdated hub-doctor version — run: bash scripts/doctor.sh setup"
  fi
elif [ -f "$HOOK" ]; then
  if [ "$MODE" = "setup" ]; then
    cp "$HOOK" "$HOOK.bak" && write_hook && ok "pre-commit hook installed (foreign hook -> pre-commit.bak)" || fail "could not write pre-commit hook"
  else
    warn "a non-hub pre-commit hook exists — setup will back it up to pre-commit.bak and replace it"
  fi
else
  if [ "$MODE" = "setup" ]; then
    write_hook && ok "pre-commit hook installed" || fail "could not write pre-commit hook"
  else
    fail "pre-commit hook not installed — run: bash scripts/doctor.sh setup"
  fi
fi

echo "== result: $PASS ok, $WARN warn, $FAIL fail"
[ "$FAIL" -eq 0 ]
