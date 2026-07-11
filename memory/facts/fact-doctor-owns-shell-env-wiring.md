---
type: fact
description: "The rfe.* marketplace skills silently depended on the retired ai-asset-registry clone; hub.doctor now owns the ~/.bashrc wiring and probes Slack auth"
timestamp: 2026-07-11
status: current
---
Discovered while scoping R5 (backlog #6) on 2026-07-11, then fixed the same
day.

## The bug

Machine A's `~/.bashrc` sourced the **retired** repo's env file
(`ai-asset-registry/rhoai-restricted/.env`), not the hub's
`restricted/.env`. The `rfe.*` pipeline (RHAIRFE filing, `assess-rfe`)
therefore worked on A only because that old clone still happened to sit on
disk carrying valid Jira credentials. Delete or move it and `/rfe.submit`
breaks on A for no visible reason. On machine B the path never existed, so
those skills were **already broken there** and it went unnoticed because all
RFE filing happens from A.

## Why the wiring is needed at all

The split matters, and the backlog (#19) had it wrong:

- **Hub tooling does NOT need it.** `scripts/hub_jira.py` self-loads
  `restricted/.env` (now via `hublib.shellenv.load_env`), and doctor
  section 4 sources the file directly. `hub.jira-sweep`, `hub.jira-sync`
  and the doctor Jira probe all work in a bare shell.
- **The marketplace `rfe.*` skills DO need it.** `preflight.py`,
  `fetch_single.py`, `dump_jira.py` and `rfe.submit` read `os.environ` with
  no `.env` fallback. They are a third-party ODH plugin, so the hub cannot
  add one. Their own SKILL.md tells the user to `! export JIRA_SERVER=...`
  by hand.

## The fix (shipped 2026-07-11)

`hub.doctor` now OWNS the shell wiring. `scripts/hub_env.py` (section 4)
removes the retired marked block and writes a marked block sourcing the
hub's own `restricted/.env`, backing up to `~/.bashrc.bak` first. Removing
the retired block also retired the old `unset CLAUDE_CODE_USE_VERTEX ...`
machinery, which the 2026-07-08 no-LLM-credential ruling had banned anyway.

Both `.env` files carried the same 14 keys with hash-matching `JIRA_*`
values, so repointing was lossless.

Two hard-won properties, both learned by breaking them first:

- `apply()` REFUSES to edit a profile whose hub markers are malformed
  (`MalformedProfile`) rather than guessing. An earlier version left an
  orphan marker and silently ate user lines on the NEXT setup run, and
  `~/.bashrc.bak` did not protect against it because the second run
  overwrote the backup with the already-corrupted file.
- The doctor must not report health it did not verify. Section 4 originally
  sourced `restricted/.env` into its own process BEFORE asking whether
  `JIRA_*` reached the shell, so it printed `ok` on a machine with no wiring
  at all. The check now runs before the sourcing.

## Slack: registration is not validity

`scripts/hub_slack.py` (section 9) probes `slack.com/api/auth.test` with the
xoxc bearer and xoxd cookie. Doctor already proved the MCP server was
registered, which says nothing about whether the tokens work. They are
per-login session tokens. On A the probe returns
`slack auth ok: pedouble @ Red Hat`.

**Open question:** whether xoxc/xoxd copied from A authenticate on machine B
is still UNTESTED. The probe is what will answer it. See
[[fact-slack-mcp-podman-engine-old-repo]].

Related: [[fact-rfe-creator-windows-quirks]],
[[fact-repo-doctor-llm-cred-exclusion-old-repo]].
