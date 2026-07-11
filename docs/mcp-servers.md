# MCP servers

The hub's skills lean on three MCP servers. Two are **user-scoped** — they
live in your Claude config and follow the profile, not the repo; one is
**project-scoped** — registered in this repo's gitignored `.mcp.json`:

| server | scope | gives you | needed by |
|---|---|---|---|
| `google-workspace` | Claude config | Gmail, Drive, Calendar, Docs, Sheets, Slides | `hub.file` GDoc intake, `presentation-create` / `blog-create` source material, calendar/mail lookups |
| `slack` | Claude config | read/search/post across the Red Hat workspace | research sweeps, channel context for knowledge entries |
| `rhai-tracker` | repo `.mcp.json` | the shared customer-interest Google Sheet | `customer-feedback-sync` |

`rhai-tracker` is fully handled by doctor section 7 — see
[/docs/tooling.md](/docs/tooling.md). This page covers the two user-scoped
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

### 2. Podman engine (Desktop is not enough)

Podman **Desktop** (the GUI) does not ship `podman.exe` — with only the
Desktop app installed, the config looks fine and the MCP silently never
loads. Install the **engine** from an **Administrator** terminal (the UAC
prompt fails silently from a non-elevated shell):

```powershell
winget install --id RedHat.Podman -e --accept-source-agreements --accept-package-agreements
podman machine start                              # a podman-machine-default WSL VM usually already exists
podman pull quay.io/redhat-ai-tools/slack-mcp     # optional: pre-pull so first use is fast
```

Doctor section 9 checks all three states (engine vs Desktop-only, machine
running, image pulled), and `setup` starts the machine and pre-pulls the
image; only the engine install itself stays manual (needs the admin shell).
After installing the engine, restart Claude Code — it lands on the
*persisted* PATH, which running sessions don't see.

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

## Verify

Restart Claude Code, run `/mcp` — `google-workspace` and `slack` (plus
`rhai-tracker` if set up) should show connected — then try one tool from
each (list calendar events; list joined Slack channels).
`bash scripts/doctor.sh check` should report sections 8–9 green.
