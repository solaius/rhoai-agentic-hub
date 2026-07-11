# restricted/ git-crypt sync + Cursor validation -- Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make `restricted/` sync automatically between machines via git-crypt (#14), and validate the hub is fully operable from Cursor (#9).

**Architecture:** #14 adds git-crypt encryption to tracked `restricted/` files with linter guards for CI (no key) and a doctor section. #9 adds `.cursor/mcp.json` for Cursor's MCP servers, extends the doctor for Cursor detection, and documents validation results. Both ship with updated docs.

**Tech Stack:** git-crypt (symmetric key), bash (doctor), Python (linter guards + tests), JSON (Cursor MCP config)

## Global Constraints

- This repo is PUBLIC -- every tracked write is world-readable. The git-crypt encryption is what makes tracking `restricted/` safe.
- `restricted/.env.example` MUST stay plaintext (it is a template with no secrets).
- `**/transcripts/` MUST stay gitignored (large, ephemeral -- not worth tracking even encrypted).
- All linter/doctor changes must pass the existing test suite: `python -m pytest scripts/tests -v`.
- Doctor sections are numbered sequentially -- new sections go after the existing ones, before the summary line.
- The hub uses `--` (double hyphen) not em dashes in prose.

---

### Task 1: Linter guards for git-crypt encrypted files

Guard the schema linter and disclosure scanner against `UnicodeDecodeError` when `restricted/` files are encrypted blobs (CI, or a machine without the git-crypt key).

**Files:**
- Modify: `scripts/hublib/schema.py` (the `lint_repo` function, lines 336-353)
- Modify: `scripts/hublib/disclosure.py` (the `load_patterns` function, lines 15-33)
- Modify: `scripts/tests/test_schema.py` (add test)
- Modify: `scripts/tests/test_disclosure.py` (add test)

**Interfaces:**
- Consumes: existing `lint_repo(root)` and `load_patterns(root)` signatures (unchanged)
- Produces: same return types; new behavior: skip gracefully when files are encrypted

- [ ] **Step 1: Write the failing test for schema linter (encrypted restricted/ tree)**

Add to the end of `scripts/tests/test_schema.py`:

```python
def test_restricted_tree_skipped_when_encrypted(tmp_path):
    """git-crypt locked files start with \\x00GITCRYPT -- linter must skip."""
    root = make_repo(tmp_path)
    know = tmp_path / "restricted" / "features" / "x" / "knowledge"
    know.mkdir(parents=True)
    # Simulate a git-crypt encrypted blob: starts with \x00GITCRYPT header
    (know / "fact-a.md").write_bytes(b"\x00GITCRYPT\x00\x00\x02\x00" + b"\xff" * 50)
    errors, warnings = lint_repo(root)
    assert errors == []
    assert not any("restricted" in w for w in warnings)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest scripts/tests/test_schema.py::test_restricted_tree_skipped_when_encrypted -v`
Expected: FAIL with `UnicodeDecodeError` (the linter tries to `read_text()` on the binary blob)

- [ ] **Step 3: Implement the guard in schema.py**

In `scripts/hublib/schema.py`, replace the `lint_repo` function's restricted block (lines 341-343):

```python
    restricted = root / "restricted"
    if restricted.is_dir():
        _lint_tree(root, restricted, errors, warnings, feature_ids)
```

With:

```python
    restricted = root / "restricted"
    if restricted.is_dir() and not _is_git_crypt_locked(restricted):
        _lint_tree(root, restricted, errors, warnings, feature_ids)
```

And add this helper function above `lint_repo` (before line 336):

```python
def _is_git_crypt_locked(restricted):
    """Detect git-crypt locked state by reading the first .md file found."""
    for md in restricted.rglob("*.md"):
        try:
            text = md.read_text(encoding="utf-8")
            return text.startswith("\x00")
        except (UnicodeDecodeError, ValueError):
            return True
    return False
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest scripts/tests/test_schema.py::test_restricted_tree_skipped_when_encrypted -v`
Expected: PASS

- [ ] **Step 5: Write the failing test for disclosure scanner (encrypted patterns file)**

Add to the end of `scripts/tests/test_disclosure.py`:

```python
def test_encrypted_patterns_file_returns_empty(tmp_path):
    """git-crypt locked lint-patterns.txt is a binary blob -- load_patterns
    must return empty, not crash."""
    p = tmp_path / "restricted" / "lint-patterns.txt"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(b"\x00GITCRYPT\x00\x00\x02\x00" + b"\xff" * 50)
    patterns, warnings = load_patterns(tmp_path)
    assert patterns == []
    assert warnings == []
```

- [ ] **Step 6: Run test to verify it fails**

Run: `python -m pytest scripts/tests/test_disclosure.py::test_encrypted_patterns_file_returns_empty -v`
Expected: FAIL with `UnicodeDecodeError`

- [ ] **Step 7: Implement the guard in disclosure.py**

In `scripts/hublib/disclosure.py`, wrap the `read_text` call in `load_patterns` (line 23) with a try/except. Replace:

```python
    if not path.is_file():
        return patterns, warnings
    for lineno, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
```

With:

```python
    if not path.is_file():
        return patterns, warnings
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (UnicodeDecodeError, ValueError):
        return patterns, warnings
    for lineno, raw in enumerate(lines, 1):
```

- [ ] **Step 8: Run test to verify it passes**

Run: `python -m pytest scripts/tests/test_disclosure.py::test_encrypted_patterns_file_returns_empty -v`
Expected: PASS

- [ ] **Step 9: Run the full test suite**

Run: `python -m pytest scripts/tests -v`
Expected: all tests PASS (222+ existing + 2 new)

- [ ] **Step 10: Commit**

```bash
git add scripts/hublib/schema.py scripts/hublib/disclosure.py scripts/tests/test_schema.py scripts/tests/test_disclosure.py
git commit -m "feat(lint): guard schema linter and disclosure scanner against git-crypt locked files (#14)"
```

---

### Task 2: Doctor git-crypt section

Add a new doctor section that checks whether git-crypt is installed and whether the repo is unlocked.

**Files:**
- Modify: `scripts/doctor.sh` (add section 11 between the pre-commit hook section and the summary)

**Interfaces:**
- Consumes: the `ok`, `warn`, `fail`, `note` helper functions already defined in doctor.sh
- Produces: doctor output lines for git-crypt status; on `setup`, attempts to unlock if key file exists

- [ ] **Step 1: Add doctor section 11 for git-crypt**

In `scripts/doctor.sh`, insert the following block BEFORE the final summary line (`echo "== result: $PASS ok, $WARN warn, $FAIL fail"`):

```bash
echo "[11] git-crypt (restricted/ encryption)"
KEYFILE="$HOME/.git-crypt-keys/rhoai-agentic-hub.key"
if command -v git-crypt >/dev/null 2>&1; then
  ok "git-crypt installed ($(git-crypt version 2>/dev/null || echo 'unknown version'))"
  # Check locked/unlocked state: read the first .md under restricted/ --
  # if it starts with a NUL byte, it is a git-crypt encrypted blob.
  LOCKED=0
  FIRST_MD="$(find "$ROOT/restricted" -name '*.md' -type f 2>/dev/null | head -1)"
  if [ -n "$FIRST_MD" ]; then
    if head -c 1 "$FIRST_MD" 2>/dev/null | od -An -tx1 | grep -q '00'; then
      LOCKED=1
    fi
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
      fail "restricted/ is locked — copy the key file to $KEYFILE, then re-run setup"
      note "get the key from your other machine: scp machine-a:~/.git-crypt-keys/rhoai-agentic-hub.key $KEYFILE"
    fi
  else
    fail "restricted/ is locked — run: bash scripts/doctor.sh setup (needs key at $KEYFILE)"
  fi
else
  warn "git-crypt not installed — restricted/ files cannot be decrypted on this machine"
  note "install: choco install git-crypt (or scoop install git-crypt)"
fi
```

- [ ] **Step 2: Verify doctor check runs cleanly**

Run: `bash scripts/doctor.sh check`
Expected: the new section 11 prints; git-crypt installed status depends on whether it is installed on this machine. The overall result should still be 0 fail (the section uses `warn` when git-crypt is not installed, not `fail`).

- [ ] **Step 3: Commit**

```bash
git add scripts/doctor.sh
git commit -m "feat(doctor): add section 11 for git-crypt status (#14)"
```

---

### Task 3: Git-crypt migration files + docs

Update `.gitignore`, create `.gitattributes`, and update `docs/setup.md` and `docs/enhancements.md`. The actual git-crypt init/add/push is a human-interactive step documented at the end.

**Files:**
- Modify: `.gitignore` (remove restricted/* lines)
- Create: `.gitattributes` (encryption patterns)
- Modify: `docs/setup.md` (update step 6 for git-crypt workflow)
- Modify: `docs/enhancements.md` (update #14 entry, add to Done)
- Modify: `docs/architecture.md` (update trust model section -- restricted/ is now encrypted-in-repo, not gitignored)
- Modify: `docs/mcp-servers.md` (minor: restricted/.env is now tracked-encrypted, not "copied between machines by hand")

**Interfaces:**
- Consumes: Task 1 (linter guards) and Task 2 (doctor section) must be committed first
- Produces: repo ready for `git-crypt init && git-crypt add ...`

- [ ] **Step 1: Create .gitattributes**

Create a new file `.gitattributes` at the repo root:

```
restricted/** filter=git-crypt diff=git-crypt
restricted/.env.example !filter !diff !merge
```

- [ ] **Step 2: Update .gitignore**

In `.gitignore`, remove the two `restricted/` lines. Replace:

```
# NDA / local-only content — never tracked
restricted/*
!restricted/.env.example
```

With:

```
# NDA content — tracked but encrypted via git-crypt (see docs/setup.md)
# restricted/.env.example stays plaintext (.gitattributes exclusion)
```

- [ ] **Step 3: Update docs/setup.md**

Replace the current step 6 content. Find:

```
6. Copy restricted content from an existing machine (none of it is ever in
   git). For almost every machine, **`restricted/.env` alone is enough**:
   keys `JIRA_SERVER`, `JIRA_USER`, `JIRA_TOKEN`, plus the Slack/Google MCP
   secrets listed in [/docs/mcp-servers.md](/docs/mcp-servers.md). The Slack
   `xoxc`/`xoxd` tokens travel with that file and authenticate on the new
   machine (R5 verified this; they are session tokens, so when they do expire
   the doctor's section 9 probe tells you).
   Copy the rest of the `restricted/` tree (`restricted/features/`,
   `restricted/memory/`) **only if you will run the customer-feedback
   workflows on this machine**. R5 measured a second machine doing normal
   hub work and it never needed them, so do not spread NDA content to a
   machine with no use for it.
```

Replace with:

```
6. Unlock the encrypted `restricted/` tree. All restricted content is tracked
   in git, encrypted via git-crypt -- it syncs automatically on `git pull`,
   but needs a one-time key unlock per machine.
   - Install git-crypt: `choco install git-crypt` (or `scoop install git-crypt`)
   - Copy the key file from an existing machine to
     `~/.git-crypt-keys/rhoai-agentic-hub.key`
   - Run `git-crypt unlock ~/.git-crypt-keys/rhoai-agentic-hub.key`
   - Or let the doctor handle it: `bash scripts/doctor.sh setup` (section 11
     unlocks automatically when the key file is in place)
   After unlocking, `restricted/` files are plaintext locally and stay
   encrypted on GitHub. The Slack `xoxc`/`xoxd` tokens in `restricted/.env`
   travel with the repo and authenticate on the new machine (R5 verified
   this; they are session tokens, so when they expire the doctor's section 9
   probe tells you).
```

- [ ] **Step 4: Update docs/architecture.md trust model**

In `docs/architecture.md`, find the trust model section's restricted layer description:

```
2. **`restricted/`** — a gitignored local mirror (`restricted/features/…`,
   `restricted/memory/…`) with the same shapes and conventions. The
   restricted bar (what must go there) is codified in
   [/conventions/memory.md](/conventions/memory.md). The linter also runs a
   restricted-content heuristic over tracked files and warns on matches.
```

Replace with:

```
2. **`restricted/`** — tracked but encrypted via git-crypt
   (`restricted/features/…`, `restricted/memory/…`, `restricted/.env`) with
   the same shapes and conventions. Files are plaintext locally when
   unlocked, opaque blobs on GitHub and in CI. The restricted bar (what must
   go there) is codified in [/conventions/memory.md](/conventions/memory.md).
   The linter also runs a restricted-content heuristic over tracked files and
   warns on matches; when git-crypt is locked (CI), the linter skips the
   restricted tree gracefully.
```

- [ ] **Step 5: Update docs/mcp-servers.md secrets section**

In `docs/mcp-servers.md`, find:

```
All values live in `restricted/.env` (gitignored; copied between machines by
hand, never generated — see [/docs/setup.md](/docs/setup.md)).
```

Replace with:

```
All values live in `restricted/.env` (tracked but encrypted via git-crypt;
syncs automatically on `git pull` once the key is unlocked --
see [/docs/setup.md](/docs/setup.md)).
```

- [ ] **Step 6: Update the information flow diagram in docs/architecture.md**

In `docs/architecture.md`, find the line in the mermaid diagram:

```
    R["restricted/ (gitignored mirror)"] -. "same shapes, local only" .- F
```

Replace with:

```
    R["restricted/ (git-crypt encrypted)"] -. "same shapes, encrypted at rest" .- F
```

- [ ] **Step 7: Commit the migration prep files**

```bash
git add .gitattributes .gitignore docs/setup.md docs/architecture.md docs/mcp-servers.md
git commit -m "feat: prepare git-crypt migration for restricted/ (#14)

.gitattributes encrypts restricted/** except .env.example.
.gitignore no longer ignores restricted/.
Docs updated: setup.md, architecture.md, mcp-servers.md."
```

- [ ] **Step 8: HUMAN -- git-crypt init, add, and push**

These steps require the human because git-crypt must be installed and the commands change the repo's encryption state:

```bash
# 1. Install git-crypt if not already
choco install git-crypt
# or: scoop install git-crypt

# 2. Initialize git-crypt in the repo
git-crypt init

# 3. Export the key for machine B
mkdir -p ~/.git-crypt-keys
git-crypt export-key ~/.git-crypt-keys/rhoai-agentic-hub.key

# 4. Add the restricted/ files (now encrypted on commit)
git add restricted/

# 5. Commit and push
git commit -m "feat: encrypt and track restricted/ via git-crypt (#14)"
git push

# 6. Verify on GitHub: browse to restricted/features/ -- files should show
#    as binary/encrypted content
```

- [ ] **Step 9: Verify**

```bash
# Verify encryption status
git-crypt status | head -20
# Expected: restricted/** files listed as "encrypted", restricted/.env.example as "not encrypted"

# Verify linter still passes
python scripts/hub_lint.py
# Expected: 0 errors

# Verify tests pass
python -m pytest scripts/tests -v
# Expected: all pass

# Verify doctor
bash scripts/doctor.sh check
# Expected: section 11 reports "restricted/ is unlocked (plaintext)"
```

---

### Task 4: Cursor MCP config + doctor extension

Create `.cursor/mcp.json` for Cursor's MCP servers and extend the doctor to detect and configure Cursor.

**Files:**
- Create: `.cursor/mcp.json` (MCP server definitions for Cursor)
- Modify: `scripts/doctor.sh` (extend section 8 to also write `.cursor/mcp.json`)
- Modify: `.gitignore` (add `.cursor/mcp.json` -- secrets in env values, same as `.mcp.json`)

**Interfaces:**
- Consumes: `restricted/.env` secrets (same as Claude Code MCP config)
- Produces: working Cursor MCP configuration; doctor manages it alongside the Claude config

- [ ] **Step 1: Add .cursor/mcp.json to .gitignore**

In `.gitignore`, after the existing `.mcp.json` line, add:

```
# Cursor MCP config (secrets in env values, same as .mcp.json; regenerated
# by hub.doctor / scripts/doctor.sh)
.cursor/mcp.json
```

- [ ] **Step 2: Create the initial .cursor/mcp.json template**

Create `.cursor/mcp.json` (this is a working template; doctor setup will overwrite with real values):

```json
{
  "mcpServers": {
    "google-workspace": {
      "type": "stdio",
      "command": "uvx",
      "args": ["workspace-mcp"],
      "env": {
        "GOOGLE_OAUTH_CLIENT_ID": "",
        "GOOGLE_OAUTH_CLIENT_SECRET": "",
        "USER_GOOGLE_EMAIL": "",
        "OAUTHLIB_INSECURE_TRANSPORT": "1"
      }
    },
    "slack": {
      "command": "podman",
      "args": ["run", "-i", "--rm",
               "-e", "SLACK_XOXC_TOKEN", "-e", "SLACK_XOXD_TOKEN",
               "-e", "MCP_TRANSPORT", "-e", "LOGS_CHANNEL_ID",
               "quay.io/redhat-ai-tools/slack-mcp"],
      "env": {
        "SLACK_XOXC_TOKEN": "",
        "SLACK_XOXD_TOKEN": "",
        "MCP_TRANSPORT": "stdio",
        "LOGS_CHANNEL_ID": ""
      }
    }
  }
}
```

Note: `rhai-tracker` is project-scoped in `.mcp.json` for Claude Code; Cursor uses `.cursor/mcp.json` for the same purpose. The doctor's existing section 7 tracker config writes `.mcp.json` -- extend it to also write the tracker entry into `.cursor/mcp.json` if the `.cursor/` directory exists.

- [ ] **Step 3: Extend doctor section 8 to write Cursor MCP config**

In `scripts/doctor.sh`, in the section 8 Python block (the inline `python -` that writes Claude MCP config), add Cursor config writing. After the existing block that writes the Claude config (line ~356 `json.dump(d, open(cfg, "w"), indent=2)`), add a second pass:

Find the end of the section 8 Python script (the line `for kind, msg in report: print(f"{kind}\t{msg}")`), and insert before it:

```python
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
    for name in ("slack", "google-workspace"):
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
```

Also pass `ROOT` to the Python script's environment by adding to the section 8 header, before the Python heredoc. Find:

```bash
done < <(python - "$CFG" "$MODE" <<'PY'
```

The ROOT variable is already available in the bash scope. Pass it by adding `ROOT="$ROOT"` as an environment prefix:

```bash
done < <(ROOT="$ROOT" python - "$CFG" "$MODE" <<'PY'
```

- [ ] **Step 4: Extend doctor section 7b (tracker .mcp.json) to also write Cursor config**

In `scripts/doctor.sh`, section 7b writes the tracker to `.mcp.json` (lines 230-261). After the `case "$RESULT"` block ends (line 261: `esac`), and still inside the `if [ -f "$SERVER_JS" ]; then` guard, add:

```bash
  # Also register in Cursor's project-scoped config if .cursor/ exists
  if [ -d "$ROOT/.cursor" ]; then
    CURSOR_RESULT=$(python - "$ROOT/.cursor/mcp.json" "$SERVER_JS" "$MODE" <<'PY'
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
```

- [ ] **Step 5: Run doctor check to verify**

Run: `bash scripts/doctor.sh check`
Expected: no new failures; if `.cursor/` directory exists, section 8 reports Cursor MCP config status

- [ ] **Step 6: Run doctor setup to verify write path**

Run: `bash scripts/doctor.sh setup`
Expected: if `.cursor/` directory exists and secrets are available, `.cursor/mcp.json` is written with real values

- [ ] **Step 7: Commit**

```bash
git add .gitignore scripts/doctor.sh
git commit -m "feat(doctor): extend MCP config for Cursor (.cursor/mcp.json) (#9)"
```

Note: do NOT `git add .cursor/mcp.json` -- it is gitignored (contains secrets).

---

### Task 5: Cursor documentation + validation prep

Write the Cursor notes documentation and update enhancements.md. The R6 outcome section is a template that the human fills in after the Cursor validation runbook.

**Files:**
- Create: `docs/cursor.md` (Cursor-specific setup and behavioral differences)
- Modify: `docs/working-here.md` (add pointer to cursor.md)
- Modify: `docs/enhancements.md` (move #9 and #14 to Done, add R6 outcome template)
- Modify: `docs/mcp-servers.md` (add Cursor appendix)

**Interfaces:**
- Consumes: Task 4 (Cursor MCP config exists)
- Produces: documentation ready for validation findings to be filled in

- [ ] **Step 1: Create docs/cursor.md**

```markdown
# Cursor notes

The hub is designed for harness independence (D2). This page covers
Cursor-specific setup and behavioral differences from Claude Code.

## Setup

1. Open the repo in Cursor. AGENTS.md loads natively -- verify the session
   reads `memory/index.md` on start (the session-start rule from AGENTS.md).
2. Run `bash scripts/doctor.sh setup` -- section 8 writes `.cursor/mcp.json`
   alongside the Claude config when `.cursor/` exists. Restart Cursor after.
3. Verify MCP servers: list calendar events (google-workspace), list joined
   Slack channels (slack), query the tracker (rhai-tracker if configured).

## Skills

Cursor v2.4+ supports the SKILL.md open standard. The hub's skills live under
`.claude/skills/<name>/SKILL.md`.

<!-- R6 VALIDATION: update this section with actual findings -->
**Status:** Pending R6 validation. Expected behavior: Cursor discovers skills
in `.claude/skills/` and surfaces them via `/` slash menu. If Cursor only
looks in `.cursor/skills/`, a symlink bridges the gap.

Marketplace plugins (`rfe-creator`, `assess-rfe`) are Claude Code-specific
(installed via `/plugin` from the ODH skills-registry). In Cursor, the
underlying scripts work from any terminal (`python scripts/hub_jira.py`,
`python scripts/hub_triage.py`), but the conversational skill wrappers are
unavailable.

## Memory tier

Cursor has no `autoMemoryDirectory` equivalent. The scratch tier
(`memory/.scratch/`) will not receive automatic writes.

This is graceful degradation:
- `hub.capture` and `hub.consolidate` write the tracked store directly via the
  gate -- they do not depend on scratch
- In Cursor, skip `hub.consolidate`'s scratch sweep (nothing to sweep) and use
  `hub.capture` for all durable items
- Cursor's built-in memories (Settings > Rules > Generate Memories) complement
  the hub's memory system for quick per-session preferences

## MCP servers

`.cursor/mcp.json` (project-scoped) is written by `doctor.sh setup` with the
same servers as the Claude config. Format is identical (`mcpServers` root key).
Cursor also supports `envFile` for `.env` loading, but the doctor writes
secrets inline for consistency with the Claude path.

See [/docs/mcp-servers.md](/docs/mcp-servers.md) for server details and
troubleshooting (server packages are interchangeable between harnesses).

## Known differences

<!-- R6 VALIDATION: update with actual findings from the validation runbook -->

| area | Claude Code | Cursor | impact |
|---|---|---|---|
| Skills | `.claude/skills/` + marketplace plugins | SKILL.md standard + skills.sh | TBD -- pending validation |
| Auto-memory | `autoMemoryDirectory` -> `memory/.scratch/` | built-in per-project memories (not files) | graceful -- use hub.capture directly |
| MCP config | `.mcp.json` (project) + `~/.claude.json` (user) | `.cursor/mcp.json` (project) + `~/.cursor/mcp.json` (user) | doctor handles both |
| Hooks | `.claude/settings.json` hooks | `.cursor/rules/*.mdc` auto-attach | superpowers hooks are Claude-specific |

## R6 validation outcome

<!-- Fill this in after executing the R6 validation runbook from the spec -->
**Status:** Not yet executed.
```

- [ ] **Step 2: Add pointer in docs/working-here.md**

In `docs/working-here.md`, in the "Further reading" section at the bottom, add after the lineage link:

```
Cursor setup: [/docs/cursor.md](/docs/cursor.md)
```

So the line becomes:

```
[/docs/tooling.md](/docs/tooling.md) · lineage: [/docs/history.md](/docs/history.md) ·
Cursor: [/docs/cursor.md](/docs/cursor.md).
```

- [ ] **Step 3: Add Cursor appendix to docs/mcp-servers.md**

At the end of `docs/mcp-servers.md`, after the "Verify" section, add:

```markdown

## Cursor

Cursor uses `.cursor/mcp.json` (project-scoped) with the same `mcpServers`
format. `bash scripts/doctor.sh setup` writes it alongside the Claude config
when `.cursor/` exists (section 8). Restart Cursor after setup.

The config is gitignored (secrets in env values). If you need to recreate it
manually, the server definitions are identical to the Claude config blocks
shown above -- copy them into `.cursor/mcp.json` under a `"mcpServers"` root
key.
```

- [ ] **Step 4: Update docs/enhancements.md -- move #14 to Done**

In `docs/enhancements.md`, in the priority table, remove the #14 row and add to the Done section:

```markdown
- **#14 restricted/ cross-machine sync** -- shipped 2026-07-11: git-crypt
  encrypts `restricted/` in-repo (`.gitattributes` patterns, `.env.example`
  stays plaintext). Linter guards skip encrypted files gracefully on CI.
  Doctor section 11 checks git-crypt install + lock state. Manual `.env` copy
  replaced by one-time key file copy + `git pull`.
  Spec: [/docs/specs/2026-07-11-restricted-sync-cursor-validation-design.md](/docs/specs/2026-07-11-restricted-sync-cursor-validation-design.md).
  Plan: [/docs/plans/2026-07-11-restricted-sync-cursor-validation-plan.md](/docs/plans/2026-07-11-restricted-sync-cursor-validation-plan.md).
```

- [ ] **Step 5: Update docs/enhancements.md -- update #9 status**

In the priority table, update #9's When column to "In progress" and add a note that the code is ready, validation runbook pending.

In the R6 section, add an outcome template:

```markdown
### R6 outcome (2026-07-11)

**Status:** Code/config shipped. Validation runbook not yet executed.

**Shipped:**
- `.cursor/mcp.json` config (doctor-managed, section 8)
- `docs/cursor.md` with setup, known differences, and gap table
- Linter guards for git-crypt (Task 1, benefits both enhancements)
- Doctor section 11 (git-crypt)

**Validation runbook (execute in Cursor, record everything):**
1. [ ] Open repo in Cursor, confirm AGENTS.md loads, verify session-start rule
2. [ ] Test skill discovery -- `/hub.capture` or equivalent
3. [ ] MCP servers -- test one tool from each
4. [ ] Full gated capture -> reindex -> commit -> push
5. [ ] Multi-step skill: `hub.file`
6. [ ] Record gaps in `docs/cursor.md`

<!-- Fill in after running the validation -->
```

- [ ] **Step 6: Commit**

```bash
git add docs/cursor.md docs/working-here.md docs/mcp-servers.md docs/enhancements.md
git commit -m "docs: Cursor setup guide + enhancements #14/#9 status (#9, #14)"
```

---

## Acceptance checklist

After all tasks complete:

**#14 (git-crypt):**
- [ ] `restricted/` files tracked and encrypted on GitHub
- [ ] `git-crypt status` shows `restricted/**` encrypted, `.env.example` not encrypted
- [ ] CI passes (linter skips locked tree)
- [ ] Doctor section 11 reports green
- [ ] `docs/setup.md` reflects git-crypt workflow

**#9 (Cursor -- code/config only; validation is a separate human-driven step):**
- [ ] `.cursor/mcp.json` written by doctor setup
- [ ] `docs/cursor.md` exists with setup, differences, gap table
- [ ] `docs/mcp-servers.md` has Cursor appendix
- [ ] R6 validation runbook ready to execute in Cursor
