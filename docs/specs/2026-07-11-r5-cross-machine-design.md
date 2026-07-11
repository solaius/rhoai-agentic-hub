# R5 cross-machine continuity: doctor-owned env wiring + Slack probe, then measure on B - design spec

- **Date:** 2026-07-11 · **Owner:** Peter Double · **Status:** approved design,
  pre-implementation
- **Closes:** enhancements backlog #19 (fully: the env-wiring and Slack-probe
  slices; the Jira probe shipped 2026-07-10 with #2) and #6 (R5) in its
  measurable half. Unblocks #14 (`restricted/` sync) by replacing its
  guesswork with evidence.
- **Does not close:** R5 step 1 (cold path). See Non-goals.

## Problem

Backlog #6 (R5) is filed as pure execution: run a checklist on machine B,
record the friction. Two things break that framing on contact.

**1. B is warm, so the cold path cannot be honestly re-run.** R5 step 1
(clone, trust prompt, `doctor.sh setup`, restart, copy `restricted/`,
re-run setup, `check` = 0 fail) assumes a virgin machine. B already runs
the hub. Worse, most of what step 1 exercises is not per-clone at all
(Claude Code marketplace trust, plugin installs, podman engine, MCP entries
in the user-level config), so cloning into a second directory on B would
skip exactly the steps most likely to break for a real newcomer. Simulating
a cold run would produce a green result that means nothing.

**2. A one-shot runbook is not reusable, but machine onboarding recurs.**
Machine C will happen; B will be reloaded. The reusable artifacts for that
already exist: `docs/setup.md` (human path) and `scripts/doctor.sh`
(machine-checked path). A standalone "R5 run sheet" document would be a
second description of onboarding that drifts from those two and rots.

Investigating #19 to see whether its remaining slice was even needed
surfaced a live bug on machine A, which settles both points.

### The latent bug on machine A

`~/.bashrc` on A sources a `.env`, but it is the **retired repo's**:

```
C:/Users/peter/Code/rh/ai-asset-registry/rhoai-restricted/.env
```

not the hub's `restricted/.env`. The `rfe.*` pipeline (the RHAIRFE-2630..2643
wave, among others) has worked on A only because that old `ai-asset-registry`
clone still sits on disk carrying valid Jira credentials. CLAUDE.md states the
hub replaced that repo for daily work. The day it is deleted or moved,
`/rfe.submit` and the `assess-rfe` REST fallback break on A with no obvious
cause. On B the path does not exist, so those skills are **already broken
there** and it went unnoticed because all RFE filing happens from A.

Verified during brainstorming: both files carry the same 14 keys, and
`JIRA_SERVER` / `JIRA_USER` / `JIRA_TOKEN` hash-match between them. Repointing
is therefore safe and severs the last daily-work dependency on the retired repo.

### Who actually needs the env wiring

The backlog justifies #19's env slice as "so `JIRA_*` reaches every shell".
That is half wrong, and the correct half is the load-bearing one:

- **Hub tooling does not need it.** `scripts/hub_jira.py` carries a
  `_load_env()` that reads `restricted/.env` when the shell never sourced it,
  and doctor section 4 sources the file directly. `hub.jira-sweep`,
  `hub.jira-sync` and the doctor Jira probe all work in a bare shell.
- **The marketplace `rfe.*` skills do need it.** `preflight.py`,
  `fetch_single.py`, `dump_jira.py` and `rfe.submit` read `os.environ` with
  no `.env` fallback. They are a third-party ODH plugin, so the hub cannot
  add one. Their own SKILL.md instructs the user to `! export JIRA_SERVER=...`
  by hand, or to add the keys to a shell profile.

So the wiring is genuinely required, but it belongs to the doctor (which
every machine runs) rather than to a checklist step a human is asked to
remember.

## Decisions made during brainstorming

1. **R5 splits into a durable half and a measured half.** The durable half is
   #19, shipped as doctor coverage so that machine C verifies itself via
   `doctor.sh check` instead of needing a hand-run checklist. The measured
   half is R5 steps 2-4 on B, which produce the #14 evidence. Every R5 finding
   lands as a doctor check or a `docs/setup.md` step. No parallel runbook
   document is created.

2. **Logic goes in `hublib`, not in `doctor.sh`.** `doctor.sh` is 476 lines of
   bash with zero tests; `hublib/` has 12 pytest files. The Jira probe from #2
   already set the precedent: logic in `hublib/jira.py` plus a thin
   `scripts/hub_jira.py --check`, with doctor shelling out to it. Idempotent
   profile editing and token probing are precisely where bash fails quietly,
   so they get the same treatment.

3. **The retired `.bashrc` line is removed, not tolerated** (owner ruling,
   2026-07-11). `setup` deletes the `ai-asset-registry` sourcing line and
   writes the hub's marked block. The `.env` files are key-identical, so
   nothing is lost.

4. **Probes WARN, never FAIL.** Consistent with the Jira probe: an offline
   machine must still reach `0 fail`.

5. **B is Windows + Git Bash**, same as A. R5 therefore yields no cross-OS
   signal, and the outcome note must not claim one.

## Architecture

Two new testable units plus two thin doctor sections that call them.

### `hublib/shellenv.py` + `scripts/hub_env.py`

Owns the shell-profile wiring.

- `--check`: reports three facts. Are `JIRA_*` present in the environment? Does
  the active profile source the hub's `restricted/.env`? Does it still source
  the retired `ai-asset-registry` path?
- `--setup`: backs up `~/.bashrc` to `~/.bashrc.bak`, removes any
  `ai-asset-registry` `.env` sourcing line, and writes an idempotent marked
  block:

```
# >>> rhoai-agentic-hub env >>>
if [ -f "<repo>/restricted/.env" ]; then
  set -a; . "<repo>/restricted/.env"; set +a
fi
# <<< rhoai-agentic-hub env <<<
```

Re-running is a no-op. A moved repo path is repaired in place (the block is
rewritten, not duplicated). The repo path is absolute and machine-specific,
which is why the doctor writes it rather than the repo tracking it.

### `hublib/slack.py` + `scripts/hub_slack.py --check`

The connectivity probe R5's own "known gaps" section calls for. Slack's
`xoxc`/`xoxd` are per-login session tokens; whether A's copies work on B has
never been tested. The probe answers it in one line instead of leaving the
user to discover it mid-task.

- Calls `slack.com/api/auth.test` with the `xoxc` bearer token and the `xoxd`
  cookie from `restricted/.env`.
- `ok:true`: report the authenticated user and workspace.
- `ok:false` with `invalid_auth`: WARN, pointing at the token re-extraction
  procedure in `docs/mcp-servers.md`.
- Network failure: WARN (offline machines still pass).

### Doctor sections

Two new sections calling the CLIs above, following section 4's shape. Section
numbering shifts; `docs/tooling.md`'s section-by-section reference is updated
to match.

## Data flow

`restricted/.env` (untracked, per machine) is the single source. The doctor
sources it for its own sections, `hub_env.py --setup` wires it into the shell
profile for the `rfe.*` plugin, and `hub_slack.py --check` reads the Slack
tokens from it to probe. Nothing else changes about how credentials are held:
they stay untracked, out of git, and never printed.

## Error handling

Probe failures are WARN with a remediation command on the same line, matching
the existing doctor contract ("every FAIL line includes its own remediation").
`hub_env.py --setup` refuses to write if `restricted/.env` is absent, backs up
before every mutation, and never edits a line it did not write except the one
explicitly-matched retired-repo line.

## Testing

`hublib/shellenv.py`: pytest against a temporary `HOME` and synthetic profile
contents. Cases: no profile, profile with no wiring, profile carrying the
retired `ai-asset-registry` line (removed), profile already carrying the hub
block (no-op), profile carrying a stale hub block with a moved repo path
(repaired in place, not duplicated), backup written.

`hublib/slack.py`: pytest with a mocked HTTP layer, following `test_jira.py`.
Cases: `ok:true`, `invalid_auth`, missing tokens, network error. Each asserts
severity is WARN, never FAIL.

CI already runs `pytest scripts/tests`, `hub_lint.py` and
`hub_index.py --check`.

## Sequencing

The order is what makes R5 honest: B is a machine where the wiring genuinely
does not exist, so B's run is a real test of what we build, not a simulation.

1. Build #19 on A with tests. A's stale wiring is fixed as a side effect.
2. Commit and push.
3. On B: `git pull`, `doctor.sh setup`, `doctor.sh check`. This exercises the
   new env wiring and Slack probe on a machine that has neither.
4. R5 steps 2-4 on B: round-trip `hub.capture` (B to A and back, indexes clean
   both ways), restricted-tier reality check (which restricted files B actually
   needs day to day, how far A and B have drifted, whether manual copying is
   tolerable), and the deliberate push race.
5. Record: `## R5 outcome` appended to the R5 section of
   `docs/enhancements.md`, a `memory/log.md` line, #19 moved to Done, #14
   annotated with the evidence it was waiting for.

## Non-goals

- **R5 step 1 (cold path) is not executed.** B is warm and we do not fake it.
  It is recorded as untested by design; machine C will verify itself through
  `doctor.sh check`, which is the entire point of shipping #19.
- **No cross-OS signal.** B is Windows + Git Bash like A, so the doctor's shell
  assumptions stay unproven on Linux and macOS.
- **`~/.bashrc` reaches Claude Code's Bash tool, not its PowerShell tool.**
  Documented in `docs/setup.md`, not solved.
- **#14 is not decided here.** R5 produces the evidence; the private-mirror vs
  git-crypt vs stay-manual call is a separate ruling afterwards.
- **No LLM-provider credentials**, per the standing 2026-07-08 owner ruling.
