---
type: fact
title: "R6 Cursor validation (2026-07-11)"
description: "R6 Cursor e2e: AGENTS.md + .claude/skills discovery PASS; scratch empty; project MCP servers stay disconnected until enabled in Settings; Google worked via user-level mcp.json; rhai-tracker missing from .cursor/mcp.json"
timestamp: 2026-07-11
tags: [r6, cursor, harness, mcp]
status: current
---
R6 (enhancement #9) validation runbook executed in Cursor on 2026-07-11.
Full write-up: [/docs/cursor.md](/docs/cursor.md); outcome note in
[/docs/enhancements.md](/docs/enhancements.md).

**PASS**
- AGENTS.md session-start rule (agent read `memory/index.md` first).
- Skill discovery: all 20 hub skills under `.claude/skills/` appear in the
  agent skill list. No `.cursor/skills` symlink needed (Cursor loads Claude
  skill dirs for compatibility).
- Memory scratch tier: `memory/.scratch/` exists with 0 files; capture does
  not depend on it.

**PARTIAL / gaps**
- Project MCP from `.cursor/mcp.json` is discovered
  (`project-0-rhoai-agentic-hub-google-workspace`,
  `project-0-rhoai-agentic-hub-slack`) but stays **disconnected** until the
  human enables them in Settings → MCP. Cursor April 2026+: user-level
  servers auto-approve; project servers do not.
- Google tool call succeeded only via pre-existing user-level
  `google_workspace` in `~/.cursor/mcp.json`.
- Slack: doctor config + podman + image OK; tools unavailable until project
  enable.
- `rhai-tracker` registered for Claude but absent from `.cursor/mcp.json`
  (doctor section 7 mirror gap).
- ODH marketplace skill wrappers remain Claude-only; underlying CLIs work.
