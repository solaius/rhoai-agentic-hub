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

detect_platform() {
  case "$OSTYPE" in
    darwin*)  PLATFORM="macos" ;;
    linux*)
      if [ -f /etc/fedora-release ]; then PLATFORM="fedora"
      elif [ -f /etc/redhat-release ]; then PLATFORM="rhel"
      else PLATFORM="linux"
      fi ;;
    msys*|cygwin*|mingw*) PLATFORM="windows" ;;
    *)        PLATFORM="unknown" ;;
  esac
}
detect_platform

echo "[0] venv bootstrap"
SYS_PY=""
# On Windows, `python` is the real binary; `python3` is often the Microsoft
# Store alias stub that prints a "not found" error despite command -v passing.
# On macOS/Linux, `python3` is the standard name. Try the right one first,
# and verify it actually runs (the Store stub passes command -v but fails --version).
if [ "$PLATFORM" = "windows" ]; then
  for _try in python python3; do
    if command -v "$_try" >/dev/null 2>&1 && "$_try" --version >/dev/null 2>&1; then
      SYS_PY="$_try"; break
    fi
  done
else
  for _try in python3 python; do
    if command -v "$_try" >/dev/null 2>&1 && "$_try" --version >/dev/null 2>&1; then
      SYS_PY="$_try"; break
    fi
  done
fi
if [ -z "$SYS_PY" ]; then
  case "$PLATFORM" in
    macos)           fail "python3 not found, install: brew install python3" ;;
    fedora|rhel)     fail "python3 not found, install: sudo dnf install python3" ;;
    windows)         fail "python not found, install: winget install Python.Python.3.12" ;;
    *)               fail "python3/python not found, install python 3.10+" ;;
  esac
else
  if [ ! -d "$ROOT/.venv" ]; then
    "$SYS_PY" -m venv "$ROOT/.venv" && ok "created .venv/ (using $SYS_PY)" || fail "could not create .venv/"
  fi
  case "$PLATFORM" in
    windows) PYTHON="$ROOT/.venv/Scripts/python" ;;
    *)       PYTHON="$ROOT/.venv/bin/python" ;;
  esac
  if ! "$PYTHON" -c "import yaml, pytest, httpx" 2>/dev/null; then
    if "$PYTHON" -m pip install -q -r "$ROOT/scripts/requirements.txt"; then
      ok "venv deps installed"
    else
      fail "pip install into .venv/ failed"
    fi
  else
    ok "venv ready ($PYTHON)"
  fi
fi
# Guard: if SYS_PY was empty we could not create a venv, so PYTHON is unset.
# Sections below reference $PYTHON, so default it to avoid set -u failures.
PYTHON="${PYTHON:-python}"

echo "[1] python + deps"
if "$PYTHON" -c "import yaml, pytest, httpx" 2>/dev/null; then
  ok "python + pyyaml + pytest + httpx"
else
  fail "python deps not importable (venv bootstrap may have failed above)"
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
  PLUGIN_LIST=$("$PYTHON" - "$SETTINGS" <<'PY'
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
  while IFS= read -r plug; do
    plug="${plug%$'\r'}"   # Windows python prints \r\n; a kept \r breaks the grep
    [ -z "$plug" ] && continue
    if [ -f "$INSTALLED_JSON" ] && grep -qF "\"$plug\"" "$INSTALLED_JSON"; then
      ok "plugin installed: $plug"
    else
      MISSING_PLUGINS="$MISSING_PLUGINS $plug"
      fail "plugin enabled but NOT installed: $plug (its skills won't exist in Claude Code)"
    fi
  done <<< "$PLUGIN_LIST"
fi
# Prototype dependencies: user-scoped plugins not in settings.json
for PROTO_PLUG in "playwright@claude-plugins-official"; do
  if [ -f "$INSTALLED_JSON" ] && grep -qF "\"$PROTO_PLUG\"" "$INSTALLED_JSON"; then
    ok "plugin installed: $PROTO_PLUG"
  else
    warn "$PROTO_PLUG not installed — needed for hub.prototype visual verification. Install: /plugin in Claude Code"
  fi
done
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
if [ -f "$LOCAL" ] && "$PYTHON" - "$LOCAL" "$SCRATCH" <<'PY'
import json, sys, pathlib
data = json.load(open(sys.argv[1]))
cur = data.get("autoMemoryDirectory", "")
sys.exit(0 if cur and pathlib.Path(cur).as_posix() == pathlib.Path(sys.argv[2]).as_posix() else 1)
PY
then
  ok "autoMemoryDirectory -> memory/.scratch"
elif [ "$MODE" = "setup" ]; then
  mkdir -p "$SCRATCH"
  if "$PYTHON" - "$LOCAL" "$SCRATCH" <<'PY'
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
if [ -f "$ENV_FILE" ] && [ "$(head -c 9 "$ENV_FILE" | tr -d '\0')" = "GITCRYPT" ]; then
  # A ciphertext .env means the checkout was never git-crypt-unlocked (or
  # the file was copied from a locked checkout). Every consumer then breaks
  # with misleading "missing var" warnings and ~/.bashrc spews parse errors
  # on every shell (seen 2026-07-16). Do not source it; fail loud with the
  # real fix instead of the per-var noise.
  fail "restricted/.env is git-crypt CIPHERTEXT — the checkout is locked; run: git-crypt unlock ${GIT_CRYPT_KEY:-$HOME/.git-crypt-keys/rhoai-agentic-hub.key} (or: bash scripts/doctor.sh setup)"
elif [ -f "$ENV_FILE" ]; then
  # Shell wiring (backlog #19), run BEFORE this process sources $ENV_FILE
  # below: hub_env.py inspects the AMBIENT environment on purpose (it reads
  # restricted/.env itself via --root), and if it ran after the sourcing it
  # would always see JIRA_* in ITS OWN process and report "ok" even on a
  # shell with no wiring at all - health the doctor never actually verified.
  # Hub tooling self-loads restricted/.env, but the marketplace rfe.* scripts
  # read os.environ with no fallback, so JIRA_* must reach every shell.
  # hub_env.py owns the ~/.bashrc block and removes the retired
  # ai-asset-registry one. Logic lives in python because it is tested;
  # idempotent profile editing is where bash quietly gets it wrong.
  if [ "$MODE" = "setup" ]; then ENV_MODE="--setup"; else ENV_MODE="--check"; fi
  # Capture output + exit status (stderr merged in) instead of streaming a
  # discarded-stderr process substitution: a crashing CLI must WARN, not
  # silently move zero counters while doctor still prints 0 fail.
  ENV_OUT="$("$PYTHON" "$ROOT/scripts/hub_env.py" $ENV_MODE 2>&1)"
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
  # not FAIL - offline machines must still pass the doctor.
  if [ -n "${JIRA_SERVER:-}" ] && [ -n "${JIRA_TOKEN:-}" ]; then
    if "$PYTHON" "$ROOT/scripts/hub_jira.py" --check >/dev/null 2>&1; then
      ok "jira reachable (hub_jira --check)"
    else
      warn "jira unreachable or auth failed - run: python scripts/hub_jira.py --check (expired JIRA_TOKEN? offline?)"
    fi
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
if "$PYTHON" "$ROOT/scripts/hub_lint.py" >/dev/null; then ok "hub_lint: 0 errors"; else fail "hub_lint errors — run: python scripts/hub_lint.py"; fi
if "$PYTHON" "$ROOT/scripts/hub_index.py" --check >/dev/null; then ok "indexes fresh"; else warn "indexes stale — run: python scripts/hub_index.py"; fi

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

# 7a. clone / presence. WARN, not FAIL (owner ruling 2026-07-11, surfaced by
# R5 on machine B): the tracker is optional, only the customer-feedback skills
# need it, and restricted/.env is copied between machines wholesale so its
# CTRACK_* keys cannot signal intent. Hard-failing here made "0 fail"
# unreachable on any machine that does not do customer-feedback work, which
# trains people to skim past FAILs. The skills themselves fail loudly when
# invoked without the tracker, so nothing is silently hidden. Severity is
# intent-aware here for the same reason section 8 is.
if [ -f "$SERVER_JS" ]; then
  ok "rhai-customer-tracker present ($ABS_CTRACK)"
else
  warn "rhai-customer-tracker not cloned at $ABS_CTRACK (only the customer-feedback skills need it; clone ${CTRACK_REPO_URL:-git@gitlab.cee.redhat.com:rh-ai-pm/rhai-customer-tracker.git}, or set CTRACK_DIR/CTRACK_REPO_URL in restricted/.env)"
fi

# 7b. register in .mcp.json — creates the file if absent (gitignored; see
# the .mcp.json line in .gitignore). Idempotent: an unchanged path is a
# no-op OK, never a rewrite.
if [ -f "$SERVER_JS" ]; then
  RESULT=$("$PYTHON" - "$ROOT/.mcp.json" "$SERVER_JS" "$MODE" <<'PY'
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
  # Also register in Cursor's project-scoped config if .cursor/ exists
  if [ -d "$ROOT/.cursor" ]; then
    CURSOR_RESULT=$("$PYTHON" - "$ROOT/.cursor/mcp.json" "$SERVER_JS" "$MODE" <<'PY'
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
else:
    print("skip")
PY
)
    case "$CURSOR_RESULT" in
      ok)    ok ".cursor/mcp.json rhai-tracker registered" ;;
      wrote) ok ".cursor/mcp.json rhai-tracker registered (restart Cursor)" ;;
      skip)  : ;;
    esac
  fi
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

echo "[8] Claude MCP servers (slack + google-workspace + patternfly-docs)"
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
MCP_RESULT=$(ROOT="$ROOT" "$PYTHON" - "$CFG" "$MODE" <<'PY'
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
# patternfly-docs: no secrets, needs npx (Node.js)
npx_cmd = "npx.cmd" if sys.platform == "win32" else "npx"
have_npx = shutil.which(npx_cmd) is not None
if "patternfly-docs" in srv:
    report.append(("ok", "patternfly-docs configured"))
elif mode == "setup":
    if have_npx:
        srv["patternfly-docs"] = {"type": "stdio", "command": npx_cmd,
            "args": ["-y", "@patternfly/patternfly-mcp@latest"], "env": {}}
        changed = True
        report.append(("wrote", f"patternfly-docs written to {cfg}"))
    else:
        report.append(("warn", "patternfly-docs: npx not found — install Node.js first (docs/mcp-servers.md)"))
else:
    if have_npx:
        report.append(("warn", "patternfly-docs not configured — needed for hub.prototype. Run: bash scripts/doctor.sh setup"))
    else:
        report.append(("warn", "patternfly-docs not configured and npx not found — install Node.js + run setup (docs/mcp-servers.md)"))
if changed:
    if os.path.exists(cfg): shutil.copy(cfg, cfg + ".bak")
    json.dump(d, open(cfg, "w"), indent=2)
# Cursor config: .cursor/mcp.json (project-scoped, same format)
cursor_dir = os.path.join(os.environ.get("ROOT", "."), ".cursor")
cursor_cfg = os.path.join(cursor_dir, "mcp.json")
if os.path.isdir(cursor_dir):
    try:
        cd = json.load(open(cursor_cfg)) if os.path.exists(cursor_cfg) else {}
    except Exception:
        cd = {}
    csrv = cd.setdefault("mcpServers", {})
    cursor_changed = False
    for name in ("slack", "google-workspace", "patternfly-docs"):
        if name in srv and name not in csrv:
            csrv[name] = srv[name]; cursor_changed = True
        elif name in srv and csrv.get(name) != srv[name]:
            csrv[name] = srv[name]; cursor_changed = True
    if cursor_changed:
        if os.path.exists(cursor_cfg): shutil.copy(cursor_cfg, cursor_cfg + ".bak")
        os.makedirs(cursor_dir, exist_ok=True)
        json.dump(cd, open(cursor_cfg, "w"), indent=2)
        report.append(("wrote", f"Cursor MCP config written to {cursor_cfg}"))
    elif csrv:
        report.append(("ok", f"Cursor MCP config present ({cursor_cfg})"))
for kind, msg in report: print(f"{kind}\t{msg}")
PY
)
while IFS=$'\t' read -r kind msg; do
  case "$kind" in
    ok)    ok "$msg" ;;
    wrote) ok "$msg (restart Claude Code)" ;;
    warn)  warn "$msg" ;;
    fail)  fail "$msg" ;;
    *)     [ -n "${kind:-}" ] && warn "could not evaluate Claude config (python error?)" ;;
  esac
done <<< "$MCP_RESULT"

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
  "$PYTHON" -c 'import json,sys;d=json.load(open(sys.argv[1]));sys.exit(0 if "slack" in d.get("mcpServers",{}) else 1)' "$CFG" 2>/dev/null && SLACK_WANTED=1
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

  # Locate the engine CLI: PATH first, then (on Windows only) the known
  # install path so a stale shell PATH doesn't masquerade as "not installed".
  PODMAN=""; PODMAN_ONPATH=0
  if command -v podman >/dev/null 2>&1; then PODMAN="podman"; PODMAN_ONPATH=1
  elif [ "$PLATFORM" = "windows" ]; then
    for cand in "/c/Program Files/RedHat/Podman/podman.exe" \
                "${PROGRAMFILES:-/c/Program Files}/RedHat/Podman/podman.exe" \
                "${ProgramW6432:-}/RedHat/Podman/podman.exe"; do
      [ -n "$cand" ] && [ -x "$cand" ] && { PODMAN="$cand"; break; }
    done
  fi

  if [ -z "$PODMAN" ]; then
    # On Windows, check for Podman Desktop without the engine (common trap).
    if [ "$PLATFORM" = "windows" ]; then
      DESKTOP=""
      for dsk in "/c/Program Files/Podman Desktop/Podman Desktop.exe" \
                 "${PROGRAMFILES:-/c/Program Files}/Podman Desktop/Podman Desktop.exe"; do
        [ -f "$dsk" ] && { DESKTOP="$dsk"; break; }
      done
      if [ -n "$DESKTOP" ]; then
        fail "Podman Desktop is installed but the podman ENGINE (CLI) is not, the GUI alone can't run the slack MCP"
      else
        fail "podman not installed (the slack MCP runs 'podman run ... $IMG')"
      fi
    else
      fail "podman not installed (the slack MCP runs 'podman run ... $IMG')"
    fi
    case "$PLATFORM" in
      macos)
        note "install: brew install podman && podman machine init && podman machine start" ;;
      fedora|rhel|linux)
        note "install: sudo dnf install podman (runs rootless, no machine needed)" ;;
      *)
        note "install the engine in an ADMIN shell (winget's UAC prompt fails silently from here):"
        note "  winget install --id RedHat.Podman -e --accept-source-agreements --accept-package-agreements"
        note "then re-run 'bash scripts/doctor.sh setup' to start the machine and pre-pull the image" ;;
    esac
  else
    if [ "$PODMAN_ONPATH" = 1 ]; then
      ok "podman engine on PATH ($("$PODMAN" --version 2>/dev/null))"
    else
      ok "podman engine installed ($("$PODMAN" --version 2>/dev/null)), not on THIS shell's PATH yet (a restarted Claude Code will resolve it)"
    fi

    # Machine state: on Linux (fedora/rhel/linux), podman runs rootless
    # natively with no machine needed, so skip straight to the image check.
    # On macOS and Windows, a VM-backed machine is required.
    MACHINE_UP=0
    case "$PLATFORM" in
      fedora|rhel|linux)
        ok "podman runs rootless natively (no machine needed)"; MACHINE_UP=1 ;;
      *)
        # Machine state: running is ideal; stopped -> start it in setup; none ->
        # 'machine init' is interactive/heavy (downloads a VM image), manual.
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
            fail "podman machine is stopped, run: bash scripts/doctor.sh setup (or: podman machine start)"
          fi
        else
          fail "no podman machine exists, run interactively: podman machine init && podman machine start"
        fi ;;
    esac

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
# WARN only, so an offline machine still reaches 0 fail. Gated on
# SLACK_WANTED like the podman checks above it: a machine that never
# configured slack should not get a permanent token-missing warn every run,
# and a machine that DID configure it but is missing tokens should get this
# warn once, not twice (the "no SLACK_XOXC_TOKEN" warn above already covers
# it inside the SLACK_WANTED branch).
if [ "$SLACK_WANTED" = 1 ]; then
  # Capture output + exit status (stderr merged in) instead of streaming a
  # discarded-stderr process substitution: a crashing CLI must WARN, not
  # silently move zero counters while doctor still prints 0 fail.
  SLACK_OUT="$("$PYTHON" "$ROOT/scripts/hub_slack.py" --check 2>&1)"
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
HOOK_MARKER="# hub-doctor pre-commit v2"
write_hook() {
  mkdir -p "$HOOKS_DIR" && cat > "$HOOK" <<'HOOKEOF' && chmod +x "$HOOK"
#!/bin/sh
# hub-doctor pre-commit v2 — installed by scripts/doctor.sh setup
# Use the venv python if available (cross-platform), fall back to python3/python.
if [ -x .venv/bin/python ]; then PY=.venv/bin/python
elif [ -x .venv/Scripts/python ]; then PY=.venv/Scripts/python
elif command -v python3 >/dev/null 2>&1; then PY=python3
else PY=python
fi
$PY scripts/hub_lint.py && $PY scripts/hub_index.py --check
status=$?
if [ $status -ne 0 ]; then
  echo ""
  echo "pre-commit: hub gate failed."
  echo "  stale indexes     -> $PY scripts/hub_index.py"
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

echo "[11] git-crypt (restricted/ encryption)"
KEYFILE="${GIT_CRYPT_KEY:-$HOME/.git-crypt-keys/rhoai-agentic-hub.key}"
if command -v git-crypt >/dev/null 2>&1; then
  ok "git-crypt installed ($(git-crypt version 2>/dev/null || echo 'unknown version'))"
  # Check locked/unlocked state on a TRACKED restricted file — a find over
  # the working tree can hit untracked hand-copied plaintext and report
  # "unlocked" on a fully locked checkout (exactly what happened
  # 2026-07-16). Only files git checked out prove the smudge state.
  LOCKED=0
  FIRST_MD="$(git -C "$ROOT" ls-files -- restricted/ | grep '\.md$' | grep -v '\.env\.example' | head -1)"
  if [ -n "$FIRST_MD" ]; then
    if head -c 1 "$ROOT/$FIRST_MD" 2>/dev/null | od -An -tx1 | grep -q '00'; then
      LOCKED=1
    fi
  fi
  # The smudge/clean filters live in LOCAL git config, written by unlock.
  # Without them, even a plaintext worktree would commit restricted files
  # raw (public repo!) — treat a missing filter as locked.
  if ! git -C "$ROOT" config --get filter.git-crypt.clean >/dev/null 2>&1; then
    LOCKED=1
  fi
  if [ "$LOCKED" = 0 ]; then
    ok "restricted/ is unlocked (plaintext)"
  elif [ "$MODE" = "setup" ]; then
    if [ -f "$KEYFILE" ]; then
      if (cd "$ROOT" && git-crypt unlock "$KEYFILE" 2>/dev/null); then
        ok "restricted/ unlocked with $KEYFILE"
      else
        fail "git-crypt unlock failed with $KEYFILE — try manually: cd $ROOT && git-crypt unlock $KEYFILE"
      fi
    else
      warn "restricted/ is locked — copy the key file to $KEYFILE, then re-run setup"
      note "get the key from your other machine: scp machine-a:~/.git-crypt-keys/rhoai-agentic-hub.key $KEYFILE"
    fi
  else
    warn "restricted/ is locked — run: bash scripts/doctor.sh setup (needs key at $KEYFILE)"
  fi
else
  warn "git-crypt not installed, restricted/ files cannot be decrypted on this machine"
  case "$PLATFORM" in
    macos)   note "install: brew install git-crypt" ;;
    fedora|rhel|linux) note "install: sudo dnf install git-crypt" ;;
    *)       note "install: choco install git-crypt (or scoop install git-crypt)" ;;
  esac
fi

echo "[12] UXD fork prototyping (hub.prototype)"
# Silent VPN probe -- gitlab.cee.redhat.com is VPN-only. Failure is the
# ONLY thing surfaced; success prints nothing extra (owner ruling
# 2026-08-04: automatic, never a question).
GITLAB_CEE="https://gitlab.cee.redhat.com"
HTTP=$(curl -sk --connect-timeout 5 -o /dev/null -w '%{http_code}' \
  "$GITLAB_CEE/api/v4/projects/155361" 2>/dev/null || echo 000)
if [ "$HTTP" != "200" ]; then
  warn "cannot reach gitlab.cee.redhat.com — connect to the Red Hat VPN (fork checks skipped: VPN)"
else
  # 12a. clone. UXD_FORK_DIR (restricted/.env) overrides; default probe.
  FORK=""
  for CAND in "${UXD_FORK_DIR:-}" "/f/code/rh/rhoai" "$HOME/code/rh/rhoai"; do
    [ -n "$CAND" ] && [ -d "$CAND/.git" ] && FORK="$CAND" && break
  done
  if [ -z "$FORK" ]; then
    if [ "$MODE" = "setup" ]; then
      FORK="${UXD_FORK_DIR:-/f/code/rh/rhoai}"
      if git clone git@gitlab.cee.redhat.com:pedouble/rhoai.git "$FORK" 2>/dev/null; then
        ok "fork cloned to $FORK"
      else
        fail "could not clone the fork — check SSH access to gitlab.cee.redhat.com"
        FORK=""
      fi
    else
      fail "fork clone not found — set UXD_FORK_DIR in restricted/.env or run: bash scripts/doctor.sh setup"
    fi
  else
    ok "fork clone at $FORK"
  fi
  if [ -n "$FORK" ]; then
    # 12b. remotes: origin must be the personal fork; upstream must exist.
    ORIGIN_URL=$(git -C "$FORK" remote get-url origin 2>/dev/null || echo "")
    case "$ORIGIN_URL" in
      *pedouble/rhoai*) ok "origin -> pedouble/rhoai" ;;
      *) warn "origin is '$ORIGIN_URL' (expected pedouble/rhoai)" ;;
    esac
    if git -C "$FORK" remote get-url upstream >/dev/null 2>&1; then
      ok "upstream remote configured"
    elif [ "$MODE" = "setup" ]; then
      git -C "$FORK" remote add upstream "$GITLAB_CEE/uxd/prototypes/rhoai.git" \
        && git -C "$FORK" config http."$GITLAB_CEE".sslVerify false \
        && ok "upstream remote added (uxd/prototypes/rhoai, sslVerify off for cee)" \
        || fail "could not add upstream remote"
    else
      fail "no 'upstream' remote — run: bash scripts/doctor.sh setup"
    fi
    if git -C "$FORK" remote get-url upstream >/dev/null 2>&1; then
      if git -C "$FORK" ls-remote upstream HEAD >/dev/null 2>&1; then
        ok "upstream reachable"
      else
        warn "upstream not reachable — check VPN/certs (git config http.$GITLAB_CEE.sslVerify false)"
      fi
    fi
    # 12c. toolchain: node >= 18, npm, node_modules.
    if command -v node >/dev/null 2>&1 && node -e 'process.exit(parseInt(process.versions.node)>=18?0:1)'; then
      ok "node $(node --version)"
    else
      fail "node >= 18 required for the fork build — install Node.js"
    fi
    if [ -d "$FORK/node_modules" ]; then
      ok "fork node_modules installed"
    elif [ "$MODE" = "setup" ]; then
      note "running npm install in the fork (takes a few minutes)..."
      (cd "$FORK" && npm install --no-audit --no-fund >/dev/null 2>&1) \
        && ok "npm install done (submodules init via postinstall)" \
        || fail "npm install failed — run it manually in $FORK"
    else
      fail "fork node_modules missing — run: bash scripts/doctor.sh setup"
    fi
    # 12d. session wiring: the fork as an additional working directory so
    # hub sessions can write there (same local-settings pattern as
    # autoMemoryDirectory in section 3).
    AD_RESULT=$(FORK="$FORK" "$PYTHON" - "$ROOT/.claude/settings.local.json" "$MODE" <<'PY'
import json, os, sys
path, mode = sys.argv[1], sys.argv[2]
fork = os.environ["FORK"].replace("\\", "/")
try:
    data = json.load(open(path, encoding="utf-8"))
except (OSError, ValueError):
    data = {}
dirs = data.setdefault("permissions", {}).setdefault("additionalDirectories", [])
if fork in dirs:
    print("ok")
elif mode == "setup":
    dirs.append(fork)
    json.dump(data, open(path, "w", encoding="utf-8"), indent=2)
    print("written")
else:
    print("missing")
PY
)
    case "$AD_RESULT" in
      ok) ok "fork granted as additional working directory" ;;
      written) ok "fork added to additionalDirectories (restart Claude Code to take effect)" ;;
      *) fail "fork not in .claude/settings.local.json additionalDirectories — run: bash scripts/doctor.sh setup" ;;
    esac
    # 12e. Pages + PAGES_URL CI variable. With GITLAB_CEE_TOKEN (api scope,
    # restricted/.env): discover the fork's Pages URL and set the variable
    # via the API. NEVER edit .gitlab-ci.yml (mr-scope-check exists to
    # catch exactly that). Without the token: manual instructions.
    PROJ="$GITLAB_CEE/api/v4/projects/pedouble%2Frhoai"
    if [ -n "${GITLAB_CEE_TOKEN:-}" ]; then
      PAGES_JSON=$(curl -sk --connect-timeout 5 -H "PRIVATE-TOKEN: $GITLAB_CEE_TOKEN" "$PROJ/pages" 2>/dev/null || echo "")
      PAGES_LIVE=$(printf '%s' "$PAGES_JSON" | "$PYTHON" -c 'import json,sys
try: print(json.load(sys.stdin).get("url",""))
except Exception: print("")')
      if [ -n "$PAGES_LIVE" ]; then
        ok "fork Pages enabled: $PAGES_LIVE"
        VAR_CODE=$(curl -sk --connect-timeout 5 -o /dev/null -w '%{http_code}' -H "PRIVATE-TOKEN: $GITLAB_CEE_TOKEN" "$PROJ/variables/PAGES_URL")
        if [ "$VAR_CODE" = "200" ]; then
          ok "PAGES_URL CI variable set"
        elif [ "$MODE" = "setup" ]; then
          curl -sk --connect-timeout 5 -o /dev/null -X POST -H "PRIVATE-TOKEN: $GITLAB_CEE_TOKEN" \
            "$PROJ/variables" --data-urlencode "key=PAGES_URL" --data-urlencode "value=$PAGES_LIVE" \
            && ok "PAGES_URL CI variable created ($PAGES_LIVE)" \
            || fail "could not create PAGES_URL variable (token needs api scope + Maintainer)"
        else
          warn "PAGES_URL CI variable not set — run: bash scripts/doctor.sh setup"
        fi
        # keep conventions/prototype-targets.yaml in sync (tracked -- commit it).
        SYNC=$(PAGES_LIVE="$PAGES_LIVE" "$PYTHON" - "$ROOT/conventions/prototype-targets.yaml" "$MODE" uxd-rhoai <<'PY'
import os, re, sys
path, mode, target = sys.argv[1], sys.argv[2], sys.argv[3]
url = os.environ["PAGES_LIVE"].rstrip("/")
text = open(path, encoding="utf-8").read()
block = re.search(r'(?ms)^  ' + re.escape(target) + r':\n.*?(?=^  \S|\Z)', text)
if not block:
    print("stale"); sys.exit()
m = re.search(r'(?m)^    pages_base_url:\s*"?([^"\n]*)"?\s*$', block.group(0))
if not m:
    print("stale"); sys.exit()
cur = m.group(1)
if cur == url:
    print("ok")
elif mode == "setup":
    s = block.start() + m.start()
    e = block.start() + m.end()
    open(path, "w", encoding="utf-8").write(
        text[:s] + f'    pages_base_url: "{url}"' + text[e:])
    print("written")
else:
    print("stale")
PY
)
        case "$SYNC" in
          ok) ok "prototype-targets.yaml pages_base_url in sync" ;;
          written) ok "prototype-targets.yaml pages_base_url written — commit the change" ;;
          *) warn "prototype-targets.yaml pages_base_url is stale/empty — run: bash scripts/doctor.sh setup" ;;
        esac
      else
        warn "fork Pages not reachable via API — check token scope, or enable Pages by pushing a branch once"
      fi
    else
      PB=$("$PYTHON" -c "import yaml; d=yaml.safe_load(open(r'$ROOT/conventions/prototype-targets.yaml', encoding='utf-8')); print(d['targets']['uxd-rhoai'].get('pages_base_url') or '')" 2>/dev/null)
      if [ -n "$PB" ]; then
        ok "pages_base_url configured: $PB (no GITLAB_CEE_TOKEN — API checks skipped)"
      else
        warn "no GITLAB_CEE_TOKEN in restricted/.env — set PAGES_URL by hand: fork Settings > CI/CD > Variables (key PAGES_URL, value from Deploy > Pages), then put the same URL in conventions/prototype-targets.yaml (targets.uxd-rhoai.pages_base_url)"
      fi
      note "optional: GITLAB_API_TOKEN as a fork CI variable enables MR-comment previews (fork CI feature)"
    fi
  fi
fi

echo "[13] MLflow prototyping (hub.prototype)"
# Spec: docs/superpowers/specs/2026-08-05-mlflow-prototype-target-design.md
# 13a-13f. GitHub-side checks always run; gitlab-side checks (13b push
# remote reachability, 13f Pages) are VPN/token gated like section 12.
MLF_SRC="${MLFLOW_SOURCE_REPO:-https://github.com/mlflow/mlflow}"
MLF_BR="${MLFLOW_SOURCE_BRANCH:-master}"
# 13a. clone. MLFLOW_DIR overrides; default sibling of the hub repo.
MLF=""
SIBLING="$(dirname "$ROOT")/mlflow"
for CAND in "${MLFLOW_DIR:-}" "$SIBLING" "$HOME/code/rh/mlflow"; do
  [ -n "$CAND" ] && [ -d "$CAND/.git" ] && MLF="$CAND" && break
done
if [ -z "$MLF" ]; then
  if [ "$MODE" = "setup" ]; then
    MLF="${MLFLOW_DIR:-$SIBLING}"
    note "cloning $MLF_SRC (branch $MLF_BR) to $MLF (large repo, takes a while)..."
    if git clone --branch "$MLF_BR" "$MLF_SRC" "$MLF" >/dev/null 2>&1; then
      ok "mlflow clone created at $MLF"
    else
      fail "could not clone $MLF_SRC — check the URL/branch (MLFLOW_SOURCE_REPO/MLFLOW_SOURCE_BRANCH in restricted/.env)"
      MLF=""
    fi
  else
    fail "mlflow clone not found — set MLFLOW_DIR in restricted/.env or run: bash scripts/doctor.sh setup"
  fi
else
  ok "mlflow clone at $MLF"
fi
if [ -n "$MLF" ]; then
  # 13b. remotes: origin = source repo; gitlab = push repo (if configured).
  ORIGIN_URL=$(git -C "$MLF" remote get-url origin 2>/dev/null || echo "")
  # compare ignoring a trailing .git / trailing slash
  NORM_SRC=$(printf '%s' "$MLF_SRC" | sed 's|/$||;s|\.git$||')
  NORM_ORI=$(printf '%s' "$ORIGIN_URL" | sed 's|/$||;s|\.git$||')
  if [ "$NORM_ORI" = "$NORM_SRC" ]; then
    ok "origin -> $MLF_SRC"
  else
    warn "origin is '$ORIGIN_URL' (expected $MLF_SRC from MLFLOW_SOURCE_REPO)"
  fi
  if [ -n "${MLFLOW_PUSH_REPO:-}" ]; then
    PUSH_URL=$(git -C "$MLF" remote get-url gitlab 2>/dev/null || echo "")
    NORM_PUSH_WANT=$(printf '%s' "$MLFLOW_PUSH_REPO" | sed 's|/$||;s|\.git$||')
    NORM_PUSH_HAVE=$(printf '%s' "$PUSH_URL" | sed 's|/$||;s|\.git$||')
    if [ "$NORM_PUSH_HAVE" = "$NORM_PUSH_WANT" ]; then
      ok "gitlab remote -> $MLFLOW_PUSH_REPO"
    elif [ -z "$PUSH_URL" ] && [ "$MODE" = "setup" ]; then
      git -C "$MLF" remote add gitlab "$MLFLOW_PUSH_REPO" \
        && ok "gitlab remote added ($MLFLOW_PUSH_REPO)" \
        || fail "could not add gitlab remote"
    elif [ -z "$PUSH_URL" ]; then
      fail "no 'gitlab' remote — run: bash scripts/doctor.sh setup"
    else
      warn "gitlab remote is '$PUSH_URL' (expected $MLFLOW_PUSH_REPO from MLFLOW_PUSH_REPO)"
    fi
  else
    note "MLFLOW_PUSH_REPO not set — push/Pages checks skipped (local-only prototyping)"
  fi
  # 13c. toolchain + prepare. uv >= 0.10.12 (older uv fails on uv.lock).
  if command -v uv >/dev/null 2>&1; then
    UV_V=$(uv --version 2>/dev/null | sed 's/^uv //;s/ .*//')
    UV_OK=$("$PYTHON" -c "import sys;v='$UV_V'.split('.');print('yes' if tuple(map(int,v[:3]))>=(0,10,12) else 'no')" 2>/dev/null || echo no)
    if [ "$UV_OK" = "yes" ]; then
      ok "uv $UV_V"
    else
      warn "uv $UV_V < 0.10.12 (fails to parse uv.lock) — run: uv self update"
    fi
  else
    fail "uv not installed — https://docs.astral.sh/uv/getting-started/installation/"
  fi
  if command -v yarn >/dev/null 2>&1 || [ -x "$HOME/.local/bin/yarn" ]; then
    ok "yarn available"
  elif [ "$MODE" = "setup" ] && command -v corepack >/dev/null 2>&1; then
    corepack enable --install-directory "$HOME/.local/bin" >/dev/null 2>&1 \
      && ok "yarn enabled via corepack (~/.local/bin)" \
      || fail "corepack enable failed — run: corepack enable --install-directory ~/.local/bin"
  else
    fail "yarn missing — run: corepack enable --install-directory ~/.local/bin (then re-run doctor)"
  fi
  if [ "$MODE" = "setup" ]; then
    if [ ! -d "$MLF/.venv" ] && ! (cd "$MLF" && uv sync >/dev/null 2>&1); then
      warn "uv sync failed in $MLF — run it manually"
    else
      ok "python env ready (uv sync)"
    fi
    if [ -d "$MLF/mlflow/server/js/node_modules" ]; then
      ok "frontend node_modules installed"
    else
      note "running yarn install in mlflow/server/js (~580 MB, takes a while)..."
      (cd "$MLF/mlflow/server/js" && yarn install >/dev/null 2>&1) \
        && ok "yarn install done" \
        || fail "yarn install failed — run it manually in $MLF/mlflow/server/js"
    fi
  else
    [ -d "$MLF/mlflow/server/js/node_modules" ] \
      && ok "frontend node_modules installed" \
      || fail "frontend node_modules missing — run: bash scripts/doctor.sh setup"
  fi
  # 13d. ready probe (non-blocking; does NOT boot the dev servers —
  # that's the clone's own dev-server skill at prototype time). --no-sync
  # keeps check mode read-only: plain `uv run` can trigger uv's auto env
  # sync (a write) even when we only want a version probe.
  if (cd "$MLF" && uv run --no-sync mlflow --version >/dev/null 2>&1); then
    ok "mlflow importable — clone ready for use"
  else
    warn "uv run --no-sync mlflow --version failed — run: bash scripts/doctor.sh setup (uv sync)"
  fi
  # 13e. session wiring: additional working directory (same as 12d).
  AD13=$(FORK="$MLF" "$PYTHON" - "$ROOT/.claude/settings.local.json" "$MODE" <<'PY'
import json, os, sys
path, mode = sys.argv[1], sys.argv[2]
fork = os.environ["FORK"].replace("\\", "/")
try:
    data = json.load(open(path, encoding="utf-8"))
except (OSError, ValueError):
    data = {}
dirs = data.setdefault("permissions", {}).setdefault("additionalDirectories", [])
if fork in dirs:
    print("ok")
elif mode == "setup":
    dirs.append(fork)
    json.dump(data, open(path, "w", encoding="utf-8"), indent=2)
    print("written")
else:
    print("missing")
PY
)
  case "$AD13" in
    ok) ok "mlflow clone granted as additional working directory" ;;
    written) ok "mlflow clone added to additionalDirectories (restart Claude Code to take effect)" ;;
    *) fail "mlflow clone not in .claude/settings.local.json additionalDirectories — run: bash scripts/doctor.sh setup" ;;
  esac
  # 13f. Pages base URL discovery (pedouble/mlflow), token + VPN gated.
  if [ -n "${MLFLOW_PUSH_REPO:-}" ]; then
    HTTP13=$(curl -sk --connect-timeout 10 -o /dev/null -w '%{http_code}' \
      "$GITLAB_CEE/api/v4/projects/pedouble%2Fmlflow" 2>/dev/null)
    # pedouble/mlflow is a private project: unauthenticated requests get a
    # 404 (not 200) even when reachable, so only "000" (no connection)
    # means unreachable/VPN-down. Any other code means the API answered.
    # NOTE: no `|| echo 000` fallback here — curl's own -w write-out
    # already prints "000" on connection failure; appending another
    # "000" on top of it would yield "000000" and the check below would
    # never match.
    if [ "$HTTP13" = "000" ]; then
      warn "cannot reach gitlab.cee.redhat.com — connect to the Red Hat VPN (mlflow Pages checks skipped)"
    elif [ -n "${GITLAB_CEE_TOKEN:-}" ]; then
      MPROJ="$GITLAB_CEE/api/v4/projects/pedouble%2Fmlflow"
      MPAGES_JSON=$(curl -sk --connect-timeout 5 -H "PRIVATE-TOKEN: $GITLAB_CEE_TOKEN" "$MPROJ/pages" 2>/dev/null || echo "")
      MPAGES_LIVE=$(printf '%s' "$MPAGES_JSON" | "$PYTHON" -c 'import json,sys
try: print(json.load(sys.stdin).get("url",""))
except Exception: print("")')
      if [ -n "$MPAGES_LIVE" ]; then
        ok "mlflow fork Pages enabled: $MPAGES_LIVE"
        SYNC13=$(PAGES_LIVE="$MPAGES_LIVE" "$PYTHON" - "$ROOT/conventions/prototype-targets.yaml" "$MODE" mlflow <<'PY'
import os, re, sys
path, mode, target = sys.argv[1], sys.argv[2], sys.argv[3]
url = os.environ["PAGES_LIVE"].rstrip("/")
text = open(path, encoding="utf-8").read()
block = re.search(r'(?ms)^  ' + re.escape(target) + r':\n.*?(?=^  \S|\Z)', text)
if not block:
    print("stale"); sys.exit()
m = re.search(r'(?m)^    pages_base_url:\s*"?([^"\n]*)"?\s*$', block.group(0))
if not m:
    print("stale"); sys.exit()
cur = m.group(1)
if cur == url:
    print("ok")
elif mode == "setup":
    s = block.start() + m.start()
    e = block.start() + m.end()
    open(path, "w", encoding="utf-8").write(
        text[:s] + f'    pages_base_url: "{url}"' + text[e:])
    print("written")
else:
    print("stale")
PY
)
        case "$SYNC13" in
          ok) ok "prototype-targets.yaml mlflow pages_base_url in sync" ;;
          written) ok "prototype-targets.yaml mlflow pages_base_url written — commit the change" ;;
          *) warn "prototype-targets.yaml mlflow pages_base_url is stale/empty — run: bash scripts/doctor.sh setup" ;;
        esac
      else
        warn "mlflow fork Pages not reachable via API — push a branch with the Pages CI once, then re-run"
      fi
    else
      note "no GITLAB_CEE_TOKEN — mlflow Pages URL discovery skipped (fill targets.mlflow.pages_base_url by hand from the fork's Deploy > Pages settings)"
    fi
  fi
fi

echo "== result: $PASS ok, $WARN warn, $FAIL fail"
[ "$FAIL" -eq 0 ]
