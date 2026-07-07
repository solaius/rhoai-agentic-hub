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

Optional (content skills like presentation-create): the superpowers plugin
and the Google Workspace MCP — install per their own docs if you'll build
decks/blogs.

4. Run the doctor's fix mode: `bash scripts/doctor.sh setup`
   (installs Python deps, creates `memory/.scratch/`, writes
   `.claude/settings.local.json` with the auto-memory redirect).
5. **Restart Claude Code** so the auto-memory redirect takes effect.
6. Copy restricted content from an existing machine (none of it is ever in
   git): at minimum `restricted/.env` (keys: `JIRA_SERVER`, `JIRA_USER`,
   `JIRA_TOKEN`); if the other machine has `restricted/features/` or
   `restricted/memory/` content, copy the whole `restricted/` tree.
7. Verify: `bash scripts/doctor.sh check` → `0 fail`. You're done.

Optional: clone the pages repo alongside for inspecting published output:
`git clone https://github.com/solaius/rhoai-agentic-hub-pages.git`

Troubleshooting: every FAIL line the doctor prints includes its own
remediation command. Marketplace plugins missing → the trust prompt was
declined; close and reopen the repo in Claude Code. Doctor section-by-section
reference: [/docs/tooling.md](/docs/tooling.md).
