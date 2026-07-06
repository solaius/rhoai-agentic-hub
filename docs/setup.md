# Machine setup

Target: a working machine in ≤30 minutes with no help. Prereqs: git, GitHub
CLI (`gh auth status` must pass), Python 3.11+, Claude Code.

1. Clone:
   `git clone https://github.com/solaius/rhoai-agentic-hub.git` (put it under
   `code/rh/` next to your other repos).
2. Open the folder in Claude Code and **accept the workspace trust prompt** —
   it enables the ODH skills marketplace declared in `.claude/settings.json`.
3. In Claude Code run `/plugin` — confirm `rfe-creator` is installed (accept
   the install prompt if offered).
4. Run the doctor's fix mode: `bash scripts/doctor.sh setup`
   (installs Python deps, creates `memory/.scratch/`, writes
   `.claude/settings.local.json` with the auto-memory redirect).
5. **Restart Claude Code** so the auto-memory redirect takes effect.
6. Copy `restricted/.env` from an existing machine (it is never in git).
   Minimum keys: `JIRA_SERVER`, `JIRA_USER`, `JIRA_TOKEN`.
7. Verify: `bash scripts/doctor.sh check` → `0 fail`. You're done.

Optional: clone the pages repo alongside for inspecting published output:
`git clone https://github.com/solaius/rhoai-agentic-hub-pages.git`

Troubleshooting: every FAIL line the doctor prints includes its own
remediation command. Marketplace plugins missing → the trust prompt was
declined; close and reopen the repo in Claude Code.
