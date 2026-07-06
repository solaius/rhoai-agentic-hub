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
  python - "$LOCAL" "$SCRATCH" <<'PY'
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
  ok "autoMemoryDirectory written (restart Claude Code to take effect)"
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

echo "== result: $PASS ok, $WARN warn, $FAIL fail"
[ "$FAIL" -eq 0 ]
