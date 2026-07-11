# Cursor notes

The hub is designed for harness independence (D2). This page covers
Cursor-specific setup and behavioral differences from Claude Code.

## Setup

1. Open the repo in Cursor. AGENTS.md loads natively -- verify the session
   reads `memory/index.md` on start (the session-start rule from AGENTS.md).
2. Run `bash scripts/doctor.sh setup` -- section 8 writes `.cursor/mcp.json`
   alongside the Claude config when `.cursor/` exists. Restart Cursor after.
3. Verify MCP servers: list calendar events (google-workspace), list joined
   Slack channels (slack), query the tracker (rhai-tracker if configured).

## Skills

Cursor v2.4+ supports the SKILL.md open standard. The hub's skills live under
`.claude/skills/<name>/SKILL.md`.

<!-- R6 VALIDATION: update this section with actual findings -->
**Status:** Pending R6 validation. Expected behavior: Cursor discovers skills
in `.claude/skills/` and surfaces them via `/` slash menu. If Cursor only
looks in `.cursor/skills/`, a symlink bridges the gap.

Marketplace plugins (`rfe-creator`, `assess-rfe`) are Claude Code-specific
(installed via `/plugin` from the ODH skills-registry). In Cursor, the
underlying scripts work from any terminal (`python scripts/hub_jira.py`,
`python scripts/hub_triage.py`), but the conversational skill wrappers are
unavailable.

## Memory tier

Cursor has no `autoMemoryDirectory` equivalent. The scratch tier
(`memory/.scratch/`) will not receive automatic writes.

This is graceful degradation:
- `hub.capture` and `hub.consolidate` write the tracked store directly via the
  gate -- they do not depend on scratch
- In Cursor, skip `hub.consolidate`'s scratch sweep (nothing to sweep) and use
  `hub.capture` for all durable items
- Cursor's built-in memories (Settings > Rules > Generate Memories) complement
  the hub's memory system for quick per-session preferences

## MCP servers

`.cursor/mcp.json` (project-scoped) is written by `doctor.sh setup` with the
same servers as the Claude config. Format is identical (`mcpServers` root key).
Cursor also supports `envFile` for `.env` loading, but the doctor writes
secrets inline for consistency with the Claude path.

See [/docs/mcp-servers.md](/docs/mcp-servers.md) for server details and
troubleshooting (server packages are interchangeable between harnesses).

## Known differences

<!-- R6 VALIDATION: update with actual findings from the validation runbook -->

| area | Claude Code | Cursor | impact |
|---|---|---|---|
| Skills | `.claude/skills/` + marketplace plugins | SKILL.md standard + skills.sh | TBD -- pending validation |
| Auto-memory | `autoMemoryDirectory` -> `memory/.scratch/` | built-in per-project memories (not files) | graceful -- use hub.capture directly |
| MCP config | `.mcp.json` (project) + `~/.claude.json` (user) | `.cursor/mcp.json` (project) + `~/.cursor/mcp.json` (user) | doctor handles both |
| Hooks | `.claude/settings.json` hooks | `.cursor/rules/*.mdc` auto-attach | superpowers hooks are Claude-specific |

## R6 validation outcome

<!-- Fill this in after executing the R6 validation runbook from the spec -->
**Status:** Not yet executed.
