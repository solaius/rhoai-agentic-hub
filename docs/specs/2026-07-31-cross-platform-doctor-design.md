# Cross-platform doctor.sh and setup improvements

**Date:** 2026-07-31
**Triggered by:** Bek Komilov's macOS setup experience (9 issues reported)
**Approach:** Script-first (Approach A) -- make doctor.sh the single
cross-platform entry point with surgical fixes.

## Problem

The hub's setup (doctor.sh, docs/setup.md, docs/mcp-servers.md) was built on
a Windows machine with Git Bash. Contributors on macOS and Fedora hit
multiple failures:

1. `python` not on PATH (macOS ships `python3` only)
2. Missing Python dependencies (`httpx` etc.)
3. pip blocked by PEP 668 (macOS "externally-managed-environment")
4. autoMemoryDirectory not set (cascading failure from #1)
5. Bash syntax error in section 8 (process substitution incompatible with
   macOS bash 3.2, shipped due to GPLv3 licensing)
6. Google Workspace MCP GCP permission issues (org-specific, not fixable in
   code, but docs should guide better)
7. git-crypt install instructions are Windows-only (`choco install`)
8. Marketplace plugins interactive-only (working as intended)
9. preferences.md references Windows (owner profile, not a setup issue)

Issues 1-5 and 7 are code/script fixes. Issue 6 is a docs improvement.
Issues 8 and 9 require no changes (8 is by design, 9 is the owner's personal
profile).

## Design

### 1. Venv bootstrap (new section 0 in doctor.sh)

Before any existing section runs:

1. Detect the python binary: try `python3` first (macOS/Fedora convention),
   fall back to `python`. Fail with a clear message if neither exists.
2. Create `.venv/` in the repo root if it doesn't exist.
3. Install deps from `scripts/requirements.txt` into the venv (pip inside a
   venv is never blocked by PEP 668).
4. Set `PYTHON` to the venv's python for all subsequent sections:
   `.venv/bin/python` on Unix, `.venv/Scripts/python` on Windows.
5. Every `python` call in the rest of the script becomes `$PYTHON`.

The venv is gitignored. Idempotent: existing venv + installed deps = fast
no-op.

Solves issues #1, #2, #3, #4 in one stroke.

### 2. Bash compatibility fixes

Rewrite the two process-substitution patterns that use
`< <(python - ... <<'PY' ... PY)` (sections 2 and 8) to the
variable-capture pattern `RESULT=$(python - ... <<'PY' ... PY)` followed by
parsing `$RESULT`. This pattern already works in sections 7b, 4, and 9 of
the same script.

The `< <(...)` construct requires bash 4+ or a non-ancient bash. macOS ships
bash 3.2 (2007) due to GPLv3 licensing. The variable-capture pattern works
on bash 3.2, bash 4+, bash 5, and zsh.

Solves issue #5.

### 3. Platform-detect helper

A function at the top of doctor.sh:

```bash
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
```

Used by:

- **Section 11 (git-crypt):** platform-aware install instructions
  (`brew install git-crypt` on macOS, `sudo dnf install git-crypt` on
  Fedora, `choco install git-crypt` on Windows).
- **Section 9 (podman/Slack runtime):** platform-aware install commands and
  path probing. macOS: `brew install podman`, no Desktop/Engine distinction.
  Fedora: `sudo dnf install podman`. Windows: existing `winget` path stays.
  Path probing on macOS/Fedora uses standard PATH only (no
  `C:/Program Files` scanning).

Solves issue #7 and extends issue #5's platform coverage.

### 4. Platform-aware podman section (section 9)

The current section 9 is entirely Windows-specific. Changes:

- **Engine detection:** on macOS/Fedora, `command -v podman` is sufficient
  (no Windows install-path fallback needed). The Desktop-vs-Engine trap is
  Windows-specific.
- **Machine state:** macOS uses `podman machine` (same as Windows); Fedora
  runs podman rootless natively (no machine needed). Branch on `$PLATFORM`.
- **Install instructions:** platform-specific remediation messages.
- **Image pull:** same logic across platforms (podman CLI is identical once
  installed).

### 5. Documentation updates

**docs/setup.md:**
- Add macOS/Fedora prerequisites section (Homebrew, python3, brew/dnf
  commands for git-crypt and podman).
- Note that the venv is created automatically by doctor.sh.
- Add a brief GCP OAuth setup note for Google Workspace MCP with a link to
  the detailed instructions (already exist in the predecessor repo's docs
  and in Bek's document).

**docs/mcp-servers.md:**
- Add macOS/Fedora podman install commands alongside the Windows ones.
- Add a "GCP OAuth setup from scratch" subsection (for contributors who
  don't have access to the existing OAuth client) referencing the steps
  from Bek's document.

### 6. .gitignore update

Add `.venv/` to `.gitignore` (not currently present).

### 7. Enhancement note for future Python-based doctor (Approach C)

Add an item to `docs/enhancements.md` noting the long-term option of
rewriting doctor.sh in Python, eliminating bash compatibility issues entirely.

## Decisions

| # | Decision | Rationale |
|---|---|---|
| D1 | Venv in repo root (`.venv/`), not system python | Solves PEP 668, python/python3, and missing deps in one pattern |
| D2 | Variable-capture over process-substitution | Works on bash 3.2 (macOS default), already proven in the same script |
| D3 | `$OSTYPE` for platform detection | Reliable in bash on all three target platforms, no external deps |
| D4 | Leave preferences.md unchanged | It's the owner's personal profile, not setup guidance |
| D5 | Leave marketplace plugin install interactive | Working as intended, no automated path exists |
| D6 | GCP OAuth setup in docs, not automated | Org-specific permissions vary; guidance beats automation here |

## Files changed

| file | change |
|---|---|
| `scripts/doctor.sh` | Venv bootstrap (section 0), platform detection, bash compat rewrites, platform-aware remediation messages |
| `.gitignore` | Add `.venv/` |
| `docs/setup.md` | Cross-platform prerequisites, venv note, GCP OAuth pointer |
| `docs/mcp-servers.md` | macOS/Fedora podman install, GCP OAuth from-scratch guidance |
| `docs/enhancements.md` | Enhancement note for Python-based doctor (Approach C) |

## Non-goals

- Rewriting doctor.sh in Python (deferred, enhancement backlog)
- Automating GCP OAuth client creation
- Automating marketplace plugin installation
- Changing the owner's preferences profile
- Supporting platforms beyond macOS, Fedora, and Windows
