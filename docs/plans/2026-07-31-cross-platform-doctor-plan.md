# Cross-platform doctor.sh and setup -- implementation plan

**Spec:** [/docs/specs/2026-07-31-cross-platform-doctor-design.md](/docs/specs/2026-07-31-cross-platform-doctor-design.md)
**Date:** 2026-07-31

## Task breakdown

### Task 1: doctor.sh -- venv bootstrap + platform detection + $PYTHON everywhere

**Files:** `scripts/doctor.sh`, `.gitignore`

1. Add `.venv/` to `.gitignore`.
2. Add `detect_platform()` function near the top (after the helper functions,
   before section 1), setting `PLATFORM` to `macos|fedora|rhel|linux|windows|unknown`.
3. Add new section `[0] python + venv` BEFORE the current section 1:
   - Detect system python: try `python3 --version`, fall back to `python --version`.
     Fail with a clear per-platform install message if neither exists.
   - If `.venv/` does not exist, create it: `$SYS_PYTHON -m venv .venv`.
   - Set `PYTHON` based on platform: `.venv/bin/python` (Unix) or
     `.venv/Scripts/python` (Windows via MSYS/Git Bash -- use forward slashes).
   - If deps not installed (`$PYTHON -c "import yaml, pytest, httpx"` fails),
     run `$PYTHON -m pip install -r scripts/requirements.txt`.
   - Report OK/FAIL.
4. Replace the current section `[1] python + deps` with a simple verification
   that `$PYTHON -c "import yaml, pytest, httpx"` passes (the heavy lifting
   moved to section 0). Keep the section number for continuity or renumber --
   the existing section's pip-install-from-system logic is fully replaced by
   the venv.
5. Replace every bare `python` call in the rest of the script with `$PYTHON`.
   Grep for all occurrences: the inline `python -` heredocs in sections 2, 3,
   7, 8, 9, 11 and the `python "$ROOT/scripts/..."` calls in sections 4, 6, 9.

**Verification:** `bash scripts/doctor.sh check` runs without error on the
current (Windows) machine. All `python` references replaced with `$PYTHON`.

### Task 2: doctor.sh -- bash compatibility (process substitution rewrites)

**Files:** `scripts/doctor.sh`

Two constructs to rewrite:

1. **Section 2** (marketplace wiring): the `while ... done < <(python - ... <<'PY' ... PY)` loop.
   Rewrite to:
   ```bash
   PLUGIN_LIST=$($PYTHON - "$SETTINGS" <<'PY'
   ...
   PY
   )
   while IFS= read -r plug; do
     ...
   done <<< "$PLUGIN_LIST"
   ```

2. **Section 8** (Claude MCP servers): the `while ... done < <(ROOT="$ROOT" python - ... <<'PY' ... PY)` loop.
   Rewrite to:
   ```bash
   MCP_RESULT=$(ROOT="$ROOT" $PYTHON - "$CFG" "$MODE" <<'PY'
   ...
   PY
   )
   while IFS=$'\t' read -r kind msg; do
     ...
   done <<< "$MCP_RESULT"
   ```

Both patterns already have working precedent in the script (sections 4 and 9
use the same `RESULT=$(...)` + `<<< "$RESULT"` approach).

**Verification:** sections 2 and 8 produce the same output as before on the
current machine.

### Task 3: doctor.sh -- platform-aware remediation messages

**Files:** `scripts/doctor.sh`

1. **Section 11 (git-crypt):** Replace the hardcoded
   `note "install: choco install git-crypt (or scoop install git-crypt)"`
   with a platform-branching block:
   ```bash
   case "$PLATFORM" in
     macos)   note "install: brew install git-crypt" ;;
     fedora|rhel|linux) note "install: sudo dnf install git-crypt" ;;
     *)       note "install: choco install git-crypt (or scoop install git-crypt)" ;;
   esac
   ```

2. **Section 9 (podman/Slack runtime):** Make the entire section
   platform-aware:
   - **Engine detection:** on macOS/Fedora/Linux, only check `command -v podman`.
     Remove the Windows-specific `C:/Program Files` path probing into a
     `windows)` case branch.
   - **Desktop-vs-Engine trap:** wrap in `if [ "$PLATFORM" = "windows" ]`.
   - **Machine state:** on Fedora/RHEL/Linux, podman runs rootless natively,
     no `podman machine` needed. On macOS, `podman machine` is needed (same
     as Windows). Branch accordingly.
   - **Install instructions:** platform-specific remediation:
     - macOS: `brew install podman`
     - Fedora: `sudo dnf install podman`
     - Windows: existing `winget` instructions

**Verification:** section 9 and 11 produce correct platform-specific messages
on the current machine (Windows path still works).

### Task 4: docs updates

**Files:** `docs/setup.md`, `docs/mcp-servers.md`, `docs/enhancements.md`

1. **docs/setup.md:**
   - Add a "Prerequisites by platform" section near the top:
     - macOS: Homebrew, `python3` (via `brew install python`), `brew install git-crypt`
     - Fedora: `python3` (pre-installed), `sudo dnf install git-crypt podman`
     - Windows: Python from python.org, `choco install git-crypt`
   - Note that `doctor.sh` creates a `.venv/` automatically (no manual pip).
   - In the git-crypt section (step 6), add `brew install git-crypt` for macOS.
   - Add a brief note about GCP OAuth setup for Google Workspace MCP,
     linking to docs/mcp-servers.md.

2. **docs/mcp-servers.md:**
   - In the Slack MCP "Podman engine" subsection, add macOS/Fedora install
     commands alongside the existing Windows `winget` block. Note that on
     Fedora, podman is often pre-installed and no `podman machine` is needed.
   - Add a "GCP OAuth setup from scratch" subsection under Google Workspace
     MCP, distilled from Bek's document: create GCP project, create OAuth
     Desktop client, enable the ~11 APIs, configure consent screen. Link to
     the predecessor repo's detailed guide.

3. **docs/enhancements.md:**
   - Add an enhancement item: "Python-based doctor rewrite (Approach C)" --
     rewrite doctor.sh in Python to eliminate bash compatibility issues
     entirely. Low priority while the bash fixes cover the three target
     platforms.

**Verification:** docs render correctly, links resolve.

## Execution order

Tasks 1 and 4 can run in parallel (doctor.sh changes and docs changes are
independent files). Task 2 depends on Task 1 (needs `$PYTHON` defined).
Task 3 depends on Task 1 (needs `detect_platform`).

```
Task 1 (venv + platform detect + $PYTHON) ──┬──> Task 2 (bash compat)
                                             └──> Task 3 (platform messages)
Task 4 (docs)  ─────────────────────────────────> (parallel with all)
```

## Final verification

After all tasks: `bash scripts/doctor.sh check` on the current (Windows)
machine must produce the same results as before (or better). The script
must not contain any bare `python` calls outside the section 0 bootstrap.
