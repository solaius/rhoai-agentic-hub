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

echo "== hub.doctor ($MODE) — $ROOT"

echo "[1] python + deps"
if python -c "import yaml, pytest" 2>/dev/null; then
  ok "python + pyyaml + pytest"
elif [ "$MODE" = "setup" ]; then
  pip install -r "$ROOT/scripts/requirements.txt" && ok "deps installed" || fail "pip install failed"
else
  fail "missing python deps — run: pip install -r scripts/requirements.txt (or doctor setup)"
fi

echo "[2] marketplace wiring"
if [ -f "$ROOT/.claude/settings.json" ] && grep -q "opendatahub-skills" "$ROOT/.claude/settings.json"; then
  ok "settings.json declares ODH marketplace (confirm installs with /plugin inside Claude Code)"
else
  fail ".claude/settings.json missing ODH marketplace block"
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

echo "[4] restricted/.env"
if [ -f "$ROOT/restricted/.env" ]; then
  for k in JIRA_SERVER JIRA_USER JIRA_TOKEN; do
    if grep -q "^$k=" "$ROOT/restricted/.env"; then ok "$k present"; else warn "$k missing in restricted/.env"; fi
  done
else
  warn "restricted/.env not found (Jira-facing skills won't work; copy it from your other machine)"
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
CTRACK_DIR="${CTRACK_DIR:-../c-tracker}"
# Default assumes a sibling clone named c-tracker, matching the
# ai-asset-registry .env convention (CTRACK_DIR=.../c-tracker). Override
# CTRACK_DIR in restricted/.env if your clone lives elsewhere or under a
# different name.
case "$CTRACK_DIR" in /*|?:*) ABS_CTRACK="$CTRACK_DIR" ;; *) ABS_CTRACK="$ROOT/$CTRACK_DIR" ;; esac
SERVER_JS="$ABS_CTRACK/server/mcp-server.js"
SERVER_DIR="$ABS_CTRACK/server"

# 7a. clone / presence
if [ -f "$SERVER_JS" ]; then
  ok "c-tracker present ($ABS_CTRACK)"
else
  fail "c-tracker missing at $ABS_CTRACK (clone ${CTRACK_REPO_URL:-git@gitlab.cee.redhat.com:rh-ai-pm/rhai-customer-tracker.git}, or set CTRACK_DIR/CTRACK_REPO_URL in restricted/.env)"
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
    warn "scaffolded tracker server/.env from .env.example — fill GOOGLE_SPREADSHEET_ID, Google OAuth client ID/secret, and an AI_PROVIDER (see c-tracker README)"
  else
    warn "tracker server/.env missing (needs GOOGLE_SPREADSHEET_ID + Google OAuth + AI provider)"
  fi
fi

echo "== result: $PASS ok, $WARN warn, $FAIL fail"
[ "$FAIL" -eq 0 ]
