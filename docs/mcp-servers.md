# MCP servers

The hub's skills lean on four MCP servers. Three are **user-scoped** — they
live in your Claude config and follow the profile, not the repo; one is
**project-scoped** — registered in this repo's gitignored `.mcp.json`:

| server | scope | gives you | needed by |
|---|---|---|---|
| `google-workspace` | Claude config | Gmail, Drive, Calendar, Docs, Sheets, Slides | `hub.file` GDoc intake, `presentation-create` / `blog-create` source material, calendar/mail lookups |
| `slack` | Claude config | read/search/post across the Red Hat workspace | research sweeps, channel context for knowledge entries |
| `patternfly-docs` | Claude config | PatternFly v6 component docs, design guidelines, accessibility, AI prompt guidance | `hub.prototype` |
| `rhai-tracker` | repo `.mcp.json` | the shared customer-interest Google Sheet | `customer-feedback-sync` |

`rhai-tracker` is fully handled by doctor section 7 — see
[/docs/tooling.md](/docs/tooling.md). This page covers the three user-scoped
servers: the secrets they need, how they get configured (by `hub.doctor` or
by hand), and the traps.

## Secrets — `restricted/.env`

All values live in `restricted/.env` (tracked but encrypted via git-crypt;
syncs automatically on `git pull` once the key is unlocked --
see [/docs/setup.md](/docs/setup.md)). Keys the two
servers use:

| key | for | notes |
|---|---|---|
| `GOOGLE_OAUTH_CLIENT_ID` / `GOOGLE_OAUTH_CLIENT_SECRET` | google-workspace | one OAuth desktop client, reused across machines |
| `USER_GOOGLE_EMAIL` | google-workspace | your `@redhat.com` address |
| `OAUTHLIB_INSECURE_TRANSPORT` | google-workspace | `1` — the local OAuth callback is `http://` |
| `SLACK_XOXC_TOKEN` / `SLACK_XOXD_TOKEN` | slack | **session** tokens; they expire (see below) |
| `SLACK_MCP_TRANSPORT` / `SLACK_LOGS_CHANNEL_ID` | slack | optional; default `stdio` / empty |

That (plus `JIRA_*` and the `CTRACK_*` overrides) is the complete set. In
particular, **LLM-provider credentials never belong in `restricted/.env`** —
anyone using this repo already has Claude Code or Cursor set up with working
LLM access, and nothing in the hub configures, checks, or touches that auth.

With those in place, `bash scripts/doctor.sh setup` (doctor sections 8–9)
writes both server definitions — secrets included — into your Claude config
(backed up to `*.bak` first) and prepares the Slack runtime. **Restart
Claude Code afterwards** — MCP servers load at startup. The rest of this
page is the manual path and the reference for what the doctor does.

## Which Claude config? (the profile trap)

The servers are written to `$CLAUDE_CONFIG_DIR/.claude.json` when
`CLAUDE_CONFIG_DIR` is set, else `~/.claude.json`. If you run separate
work/personal Claude profiles, run the doctor — and Claude Code — under the
profile that should own the servers. A "not configured" report on a machine
that used to work usually means the wrong profile, not a lost setup; the
doctor prints which config file it inspected.

## Google Workspace MCP

[google_workspace_mcp](https://github.com/taylorwilsdon/google_workspace_mcp)
runs locally via `uvx` (`pip install uv` if you don't have it) and
authenticates with your own Google Cloud OAuth client.

**OAuth client:** reuse the existing one — its ID/secret are already in
`restricted/.env` on any set-up machine, and one desktop client serves every
machine. Only if starting from zero: create a Google Cloud project → APIs &
Services → Credentials → OAuth Client ID, type **Desktop Application**;
enable the APIs you'll use (Calendar, Drive, Gmail, Docs, Sheets, Slides,
Forms, Tasks, People); configure the consent screen (Internal for a
Workspace org). Step-by-step with per-API links: the predecessor repo's
[google-workspace-install-guide.md](https://github.com/solaius/ai-asset-registry/blob/main/docs/google-workspace-install-guide.md).

Config block (under `mcpServers` in the Claude config — exactly what doctor
`setup` writes):

```json
"google-workspace": {
  "type": "stdio",
  "command": "uvx",
  "args": ["workspace-mcp"],
  "env": {
    "GOOGLE_OAUTH_CLIENT_ID": "<from restricted/.env>",
    "GOOGLE_OAUTH_CLIENT_SECRET": "<from restricted/.env>",
    "USER_GOOGLE_EMAIL": "<you>@redhat.com",
    "OAUTHLIB_INSECURE_TRANSPORT": "1"
  }
}
```

First use triggers a browser OAuth flow; credentials cache under
`~/.google_workspace_mcp/credentials/` with automatic refresh, so you
authenticate once per machine. Persistent auth errors → delete that
directory and re-authenticate. "API not enabled" / "forbidden" on one tool →
enable the corresponding API in the Google Cloud console.

### GCP OAuth setup from scratch

If you do not have access to the existing shared OAuth client (its
credentials live in `restricted/.env` on any set-up machine), create your
own:

1. Go to [console.cloud.google.com](https://console.cloud.google.com) and
   create a new project (or reuse an existing one).
2. Navigate to **APIs & Services > Credentials** and create an **OAuth
   Client ID** with application type **Desktop Application**.
3. Enable the following APIs for your project (APIs & Services > Library):
   - [Calendar API](https://console.cloud.google.com/apis/library/calendar-json.googleapis.com)
   - [Drive API](https://console.cloud.google.com/apis/library/drive.googleapis.com)
   - [Gmail API](https://console.cloud.google.com/apis/library/gmail.googleapis.com)
   - [Docs API](https://console.cloud.google.com/apis/library/docs.googleapis.com)
   - [Sheets API](https://console.cloud.google.com/apis/library/sheets.googleapis.com)
   - [Slides API](https://console.cloud.google.com/apis/library/slides.googleapis.com)
   - [Forms API](https://console.cloud.google.com/apis/library/forms.googleapis.com)
   - [Tasks API](https://console.cloud.google.com/apis/library/tasks.googleapis.com)
   - [People API](https://console.cloud.google.com/apis/library/people.googleapis.com) (used for Chat/Contacts)
   - [Apps Script API](https://console.cloud.google.com/apis/library/script.googleapis.com)
4. Configure the **OAuth consent screen** (APIs & Services > OAuth consent
   screen):
   - **Internal** if your Google account belongs to a Workspace organization
     (e.g. `@redhat.com`). This skips the verification requirement.
   - **External** if using a personal Gmail account. You will need to add
     your email as a test user until the app is verified.
5. Copy the **Client ID** and **Client Secret** from the Credentials page,
   then add them to `restricted/.env`:
   ```
   GOOGLE_OAUTH_CLIENT_ID=<your client id>
   GOOGLE_OAUTH_CLIENT_SECRET=<your client secret>
   ```
6. Re-run `bash scripts/doctor.sh setup` to write the updated credentials
   into the Claude config, then restart Claude Code.

## Slack MCP

[slack-mcp](https://github.com/redhat-ai-tools/slack-mcp) runs as a
container — the server's command is literally `podman run … slack-mcp` — so
it needs two things a fresh machine won't have: session tokens and the
podman **engine**.

### 1. Tokens (they expire)

`xoxc`/`xoxd` are browser **session** tokens, not OAuth — they die on Slack
logout or session invalidation. Symptom: Slack tools return `invalid_auth`
→ re-extract:

```bash
git clone https://github.com/maorfr/slack-token-extractor
cd slack-token-extractor && pip install -r requirements.txt && python main.py
```

A Playwright browser opens; log in to the Red Hat workspace. Tokens land in
`.slack_tokens.env` — **rename on paste**: the extractor writes them as
`SLACK_MCP_XOXC_TOKEN` / `SLACK_MCP_XOXD_TOKEN`, but `restricted/.env` and
the Claude config use the `SLACK_MCP_`-less names `SLACK_XOXC_TOKEN` /
`SLACK_XOXD_TOKEN`. Paste the new values into `restricted/.env`, then re-run
`bash scripts/doctor.sh setup` (or edit the Claude config by hand) and
restart Claude Code.

### 2. Podman engine

The Slack MCP container needs the podman **engine** (the CLI), not just
Podman Desktop. Install per platform:

**macOS (Homebrew):**

```bash
brew install podman
podman machine init && podman machine start
podman pull quay.io/redhat-ai-tools/slack-mcp     # optional: pre-pull so first use is fast
```

**Fedora/RHEL:**

Podman is usually pre-installed. No `podman machine` is needed (podman runs
rootless natively on Linux).

```bash
sudo dnf install podman                           # only if not already present
podman pull quay.io/redhat-ai-tools/slack-mcp     # optional: pre-pull so first use is fast
```

**Windows:**

Podman **Desktop** (the GUI) does not ship `podman.exe`. With only Desktop
installed, the config looks fine and the MCP silently never loads. Install the
**engine** from an **Administrator** terminal (the UAC prompt fails silently
from a non-elevated shell):

```powershell
winget install --id RedHat.Podman -e --accept-source-agreements --accept-package-agreements
podman machine start                              # a podman-machine-default WSL VM usually already exists
podman pull quay.io/redhat-ai-tools/slack-mcp     # optional: pre-pull so first use is fast
```

Doctor section 9 checks all three states (engine vs Desktop-only, machine
running, image pulled), and `setup` starts the machine and pre-pulls the
image; only the engine install itself stays manual (needs the admin shell on
Windows). After installing the engine, restart Claude Code, as it lands on
the *persisted* PATH, which running sessions don't see.

### 3. Config

```json
"slack": {
  "command": "podman",
  "args": ["run", "-i", "--rm",
           "-e", "SLACK_XOXC_TOKEN", "-e", "SLACK_XOXD_TOKEN",
           "-e", "MCP_TRANSPORT", "-e", "LOGS_CHANNEL_ID",
           "quay.io/redhat-ai-tools/slack-mcp"],
  "env": {
    "SLACK_XOXC_TOKEN": "<from restricted/.env>",
    "SLACK_XOXD_TOKEN": "<from restricted/.env>",
    "MCP_TRANSPORT": "stdio",
    "LOGS_CHANNEL_ID": ""
  }
}
```

`LOGS_CHANNEL_ID` must be present (empty is fine) — the container errors
without it.

### Still not loading?

Config green + engine green but no Slack tools after a restart — run the
container by hand to separate a runtime problem from a token problem in one
shot:

```bash
printf '%s\n' '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"smoke","version":"1"}}}' \
  | SLACK_XOXC_TOKEN=… SLACK_XOXD_TOKEN=… MCP_TRANSPORT=stdio LOGS_CHANNEL_ID= \
    podman run -i --rm -e SLACK_XOXC_TOKEN -e SLACK_XOXD_TOKEN -e MCP_TRANSPORT -e LOGS_CHANNEL_ID quay.io/redhat-ai-tools/slack-mcp
```

A `jsonrpc` result line means the plumbing works (wrong profile, or a
restart is still needed); an auth error means expired tokens.

## PatternFly MCP

[@patternfly/patternfly-mcp](https://www.npmjs.com/package/@patternfly/patternfly-mcp)
runs locally via `npx` and provides PatternFly v6 component documentation,
design guidelines, accessibility docs, AI prompt guidance (from the
`patternfly/ai-helpers` repo), and JSON schemas. `hub.prototype` queries it
before generating any HTML to ensure correct component selection, CSS class
names, HTML structure, and design token usage.

**Prerequisite:** Node.js (provides `npx`). Install via your package
manager (`brew install node`, `dnf install nodejs`, `winget install
OpenJS.NodeJS`).

Config block (under `mcpServers` in the Claude config — exactly what doctor
`setup` writes):

```json
"patternfly-docs": {
  "type": "stdio",
  "command": "npx",
  "args": ["-y", "@patternfly/patternfly-mcp@latest"],
  "env": {}
}
```

On Windows the command is `npx.cmd` (doctor handles this automatically).

No secrets, no OAuth, no tokens. First invocation downloads the package
via npm; subsequent calls use the npx cache.

**Troubleshooting:**
- "PatternFly MCP not responding" in `hub.prototype` → check
  `bash scripts/doctor.sh check` section 8 for `patternfly-docs configured`.
  If not configured, run `bash scripts/doctor.sh setup` and restart Claude
  Code.
- "npx not found" → install Node.js.
- "npm ERR!" or timeout on first use → network/proxy issue; `npx` needs to
  download `@patternfly/patternfly-mcp` from the npm registry.

## Verify

Restart Claude Code, run `/mcp` — `google-workspace`, `slack`, and
`patternfly-docs` (plus `rhai-tracker` if set up) should show connected —
then try one tool from each (list calendar events; list joined Slack
channels; search PatternFly docs for "button").
`bash scripts/doctor.sh check` should report sections 8–9 green.

## Cursor

Cursor uses two config locations:

- **`~/.cursor/mcp.json`** (user-level) -- servers here are auto-approved and
  appear in Settings > Tools & MCP. **This is the recommended location** for
  servers that must work reliably in Cursor.
- **`.cursor/mcp.json`** (project-level) -- `bash scripts/doctor.sh setup`
  writes this alongside the Claude config when `.cursor/` exists. However,
  project servers may stay disconnected and not appear in Settings (R6
  validated 2026-07-11). Keep as a parity record; do not rely on it alone.

**Setup:** after running `doctor.sh setup`, copy the server blocks from
`.cursor/mcp.json` into `~/.cursor/mcp.json` (create it if it does not
exist). The format is identical -- a `"mcpServers"` root key with the same
server definitions shown above. Restart Cursor after editing.

The project config is gitignored (secrets in env values).
