# Cursor notes

The hub is designed for harness independence (D2). This page covers
Cursor-specific setup and behavioral differences from Claude Code.

Validated 2026-07-11 (R6 runbook). See `## R6 validation outcome` below.

## Setup

1. Open the repo in Cursor. AGENTS.md loads natively -- verify the session
   reads `memory/index.md` on start (the session-start rule from AGENTS.md).
2. Run `bash scripts/doctor.sh setup` -- section 8 writes `.cursor/mcp.json`
   alongside the Claude config when `.cursor/` exists. Restart Cursor after.
3. Hub MCP servers that must work in Cursor belong in
   `~/.cursor/mcp.json` (user-level) — that is what Settings → Tools & MCP
   lists and auto-approves. Doctor still writes project `.cursor/mcp.json`,
   but on this machine project servers did not appear in Settings.
4. Verify MCP servers: list calendar events (google-workspace), list joined
   Slack channels (slack), query the tracker (rhai-tracker if configured).
   After editing user mcp.json, restart Cursor or reload MCP.

## Skills

Cursor discovers hub skills under `.claude/skills/<name>/SKILL.md`
automatically — no symlink and no `.cursor/skills/` bridge needed. Cursor
docs confirm Claude/Codex skill directories are loaded for compatibility.
This session's agent skill list included all 20 hub skills from that tree.

**How to invoke:** ask the agent to follow a skill ("run hub.capture",
"follow `.claude/skills/hub.capture/SKILL.md`"), or pick from the `/`
skills menu if your Cursor build surfaces project skills there. Pointing
the agent at the SKILL.md file reproduces the gated behavior (one-line
confirm → write → reindex → lint → pathspec commit).

Marketplace plugins (`rfe-creator`, `assess-rfe`) are Claude Code-specific
(installed via `/plugin` from the ODH skills-registry). In Cursor, the
underlying scripts work from any terminal (`python scripts/hub_jira.py`,
`python scripts/hub_triage.py`), but the conversational skill wrappers are
unavailable. Severity: nice-to-have (CLI covers daily Jira work).

## Memory tier

Cursor has no `autoMemoryDirectory` equivalent. The scratch tier
(`memory/.scratch/`) will not receive automatic writes.

Confirmed 2026-07-11: `memory/.scratch/` exists and is empty (0 files)
during a Cursor session that had already done durable work — nothing
writes there from this harness.

This is graceful degradation:
- `hub.capture` and `hub.consolidate` write the tracked store directly via the
  gate -- they do not depend on scratch
- In Cursor, skip `hub.consolidate`'s scratch sweep (nothing to sweep) and use
  `hub.capture` for all durable items
- Cursor's built-in memories (Settings → Rules → Generate Memories) complement
  the hub's memory system for quick per-session preferences

## MCP servers

`.cursor/mcp.json` (project-scoped) is written by `doctor.sh setup` with the
same servers as the Claude config. Format is identical (`mcpServers` root key).
Cursor also supports `envFile` for `.env` loading, but the doctor writes
secrets inline for consistency with the Claude path.

**Critical Cursor behavior (April 2026+):** global servers in
`~/.cursor/mcp.json` are auto-approved and appear in Settings → Tools &
MCP. Project-level servers in `.cursor/mcp.json` are discovered by the
runtime (logs show `project-0-<repo>-<name>`) but on this machine they
stayed **disconnected** and **did not appear in the Settings UI** — so
"enable in Settings" is not a workable path for project Slack.

R6 evidence (this machine):
- Doctor-written project servers: `google-workspace`, `slack` present in
  `.cursor/mcp.json`. Cursor log entries briefly listed
  `project-0-rhoai-agentic-hub-google-workspace` and
  `project-0-rhoai-agentic-hub-slack` as disconnected; neither showed up
  as a toggleable row in Settings → MCP for the owner.
- Working Google access came from the **user-level** server
  `google_workspace` in `~/.cursor/mcp.json` (`user-google_workspace`) —
  list_calendars succeeded (11 calendars). That is what Settings shows as
  enabled "Google Workspace".
- `slack`: config + podman engine + image OK in the project file, but
  invisible from Settings. **Working fix:** mirror the same `slack` block
  into `~/.cursor/mcp.json` (done 2026-07-11 during R6 follow-up) so it
  follows the Google pattern. Restart Cursor / reload MCP after.
- `rhai-tracker`: registered in Claude `.mcp.json` and `server.js` exists
  on disk, but **absent from `.cursor/mcp.json`**. Doctor section 7 is
  supposed to mirror it when `.cursor/` exists — gap to fix on next
  `doctor.sh setup` pass / doctor tweak. Tracker clone path in
  `restricted/.env` (`CTRACK_DIR`) may also be stale relative to the
  live `rhai-customer-tracker` checkout the Claude config points at.

Recommended SoT for Cursor day-to-day: put hub MCP servers that must
work in Cursor into `~/.cursor/mcp.json` (user-level), matching how
Google already worked here. Keep doctor writing `.cursor/mcp.json` for
parity/docs, but do not rely on the project file alone until Cursor
surfaces project servers reliably in Settings.

## Known differences

| area | Claude Code | Cursor | impact |
|---|---|---|---|
| Skills | `.claude/skills/` + marketplace plugins | Discovers `.claude/skills/` natively (compat); no marketplace `/plugin` | Core hub skills work; ODH plugin wrappers Claude-only |
| Auto-memory | `autoMemoryDirectory` → `memory/.scratch/` | built-in per-project memories (not files); scratch stays empty | graceful — use hub.capture directly |
| MCP config | `.mcp.json` (project) + `~/.claude.json` (user) | `.cursor/mcp.json` (project, **needs enable**) + `~/.cursor/mcp.json` (user, auto) | doctor writes project file; human must enable |
| Hooks | `.claude/settings.json` hooks | `.cursor/rules/*.mdc` auto-attach | superpowers hooks are Claude-specific |

## Gap table (R6)

| gap | severity | workaround |
|---|---|---|
| Project MCP from `.cursor/mcp.json` not listed in Settings → MCP (stays disconnected in logs) | **Blocks** Slack if only project-configured | Mirror into `~/.cursor/mcp.json` (same path Google already used) |
| `rhai-tracker` missing from `.cursor/mcp.json` | **Blocks** tracker sync from Cursor | Re-run `doctor.sh setup` after confirming tracker path; also add to user mcp.json for Cursor |
| ODH marketplace skill wrappers (`rfe-creator`, `assess-rfe`) | Nice-to-have | Run underlying `python scripts/hub_*.py` CLIs |
| No scratch auto-memory | None (by design) | `hub.capture` for every durable item |
| Superpowers / Claude hooks | Nice-to-have | Not required for hub daily loop |

## R6 validation outcome

**Status:** Executed 2026-07-11 in Cursor (this session).

| # | check | result |
|---|---|---|
| 1 | AGENTS.md + session-start (`memory/index.md` first) | **PASS** — followed |
| 2 | Skill discovery (`hub.capture` / `.claude/skills/`) | **PASS** — 20 hub skills discovered; no `.cursor/skills` symlink needed |
| 3 | MCP — one tool from each of google / slack / rhai-tracker | **PARTIAL** — Google OK via user-level server; project google+slack disconnected pending enable; rhai-tracker not in project mcp.json |
| 4 | Memory tier (scratch empty, capture still works) | **PASS** — scratch 0 files; capture path does not depend on it |
| 5 | Full gated capture → reindex → commit → push | **PASS** — `fact-r6-cursor-validation` |
| 6 | Multi-step skill `hub.file` | **PASS** — `ref-cursor-mcp-docs` |
