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

Optional (content skills like presentation-create): the superpowers plugin —
install per its own docs if you'll build decks/blogs. The Google Workspace
and Slack MCP servers are covered by steps 6–7 below plus
[/docs/mcp-servers.md](/docs/mcp-servers.md).

4. Run the doctor's fix mode: `bash scripts/doctor.sh setup`
   (installs Python deps, creates `memory/.scratch/`, writes
   `.claude/settings.local.json` with the auto-memory redirect).
5. **Restart Claude Code** so the auto-memory redirect takes effect.
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
7. Re-run `bash scripts/doctor.sh setup` - with `.env` in place it also
   writes the Slack + Google Workspace MCP servers into your Claude config,
   prepares the Slack podman runtime (traps and manual steps, e.g. the
   podman engine install: [/docs/mcp-servers.md](/docs/mcp-servers.md)), and wires
   `restricted/.env` into `~/.bashrc` so `JIRA_*` reaches every shell (the
   marketplace `rfe.*` skills read the environment directly and have no
   fallback). Then **open a new shell** and restart Claude Code once more.
8. Verify: `bash scripts/doctor.sh check` -> `0 fail`. You're done.

Note: the `~/.bashrc` wiring reaches Claude Code's Bash tool, not its
PowerShell tool. If a skill runs Jira scripts through PowerShell it will not
see `JIRA_*`; hub scripts self-load `restricted/.env` and are unaffected.

Optional: clone the pages repo alongside for inspecting published output:
`git clone https://github.com/solaius/rhoai-agentic-hub-pages.git`

Troubleshooting: every FAIL line the doctor prints includes its own
remediation command. Marketplace plugins missing → the trust prompt was
declined; close and reopen the repo in Claude Code. Doctor section-by-section
reference: [/docs/tooling.md](/docs/tooling.md).
