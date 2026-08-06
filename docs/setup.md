# Machine setup

Target: a working machine in ≤30 minutes with no help.

## Prerequisites by platform

**All platforms:** Git, GitHub CLI (`gh auth status` must pass), Python 3.11+,
Claude Code.

- **macOS:** Homebrew is the easiest path.
  `brew install python git-crypt podman`
- **Fedora/RHEL:** `python3` is pre-installed.
  `sudo dnf install git-crypt podman`
- **Windows:** Python from [python.org](https://python.org) or
  `winget install Python.Python.3`; `choco install git-crypt`
  (or `scoop install git-crypt`).

Google Workspace MCP requires a GCP OAuth client for Calendar, Drive, Gmail,
Docs, Sheets, Slides, Forms, and Tasks access. If you do not have access to
the shared OAuth credentials in `restricted/.env`, see
[/docs/mcp-servers.md](/docs/mcp-servers.md) for setup-from-scratch
instructions.

1. Clone:
   `git clone https://github.com/solaius/rhoai-agentic-hub.git` (put it under
   `code/rh/` next to your other repos).
2. Open the folder in Claude Code and **accept the workspace trust prompt** —
   it enables the ODH skills marketplace declared in `.claude/settings.json`.
3. In Claude Code run `/plugin` — confirm `rfe-creator` is installed (accept
   the install prompt if offered).

Optional (content skills like presentation-create): the superpowers plugin —
install per its own docs if you'll build decks/blogs. Optional
(hub.prototype): Node.js for the PatternFly MCP server —
`bash scripts/doctor.sh setup` configures it; see
[/docs/mcp-servers.md](/docs/mcp-servers.md). The Google Workspace
and Slack MCP servers are covered by steps 6–7 below plus
[/docs/mcp-servers.md](/docs/mcp-servers.md).

Optional (hub.prototype): the UXD RHOAI fork clone + Red Hat VPN --
`bash scripts/doctor.sh setup` (section 12) clones it, wires the
`upstream` remote, installs deps, and grants it as a working directory;
set `UXD_FORK_DIR` in `restricted/.env` if the clone lives somewhere
custom, and `GITLAB_CEE_TOKEN` (GitLab CEE personal token, api scope)
to let setup verify Pages and set the fork's `PAGES_URL` CI variable.

Optional (hub.prototype, mlflow target): the MLflow fork clone —
`bash scripts/doctor.sh setup` clones and prepares it (uv sync + yarn
install) as a sibling of this repo; set MLFLOW_DIR / MLFLOW_SOURCE_REPO /
MLFLOW_SOURCE_BRANCH / MLFLOW_PUSH_REPO in `restricted/.env` to override
(see restricted/.env.example). Building the frontend needs Node.js +
corepack (yarn 4); the Python side needs uv >= 0.10.12.

4. Run the doctor's fix mode: `bash scripts/doctor.sh setup`
   (creates a `.venv/`, installs Python deps, creates `memory/.scratch/`,
   writes `.claude/settings.local.json` with the auto-memory redirect).
   No manual `pip install` is needed; the doctor handles it.
5. **Restart Claude Code** so the auto-memory redirect takes effect.
6. Unlock the encrypted `restricted/` tree. All restricted content is tracked
   in git, encrypted via git-crypt -- it syncs automatically on `git pull`,
   but needs a one-time key unlock per machine.
   - Install git-crypt:
     - macOS: `brew install git-crypt`
     - Fedora/RHEL: `sudo dnf install git-crypt`
     - Windows: `choco install git-crypt` (or `scoop install git-crypt`)
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
8. **Cursor users only:** copy the MCP server blocks from `.cursor/mcp.json`
   into `~/.cursor/mcp.json` (user-level). Project-level servers may not
   appear in Cursor's Settings -- user-level is reliable. See
   [/docs/mcp-servers.md](/docs/mcp-servers.md) Cursor section for details.
9. Verify: `bash scripts/doctor.sh check` -> `0 fail`. You're done.

Note: the `~/.bashrc` wiring reaches Claude Code's Bash tool, not its
PowerShell tool. If a skill runs Jira scripts through PowerShell it will not
see `JIRA_*`; hub scripts self-load `restricted/.env` and are unaffected.

Optional: clone the pages repo alongside for inspecting published output:
`git clone https://github.com/solaius/rhoai-agentic-hub-pages.git`

Troubleshooting: every FAIL line the doctor prints includes its own
remediation command. Marketplace plugins missing → the trust prompt was
declined; close and reopen the repo in Claude Code. Doctor section-by-section
reference: [/docs/tooling.md](/docs/tooling.md).
