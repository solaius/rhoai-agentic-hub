---
type: reference
title: "Cursor MCP documentation"
description: "Cursor MCP docs — project .cursor/mcp.json servers require enable; user-level ~/.cursor/mcp.json auto-approves (April 2026+)."
resource: https://cursor.com/docs/context/mcp
timestamp: 2026-07-11
tags: [cursor, mcp, harness]
---
Canonical docs for how Cursor loads MCP servers (project vs user).

Why it matters for this hub: `doctor.sh` writes project
`.cursor/mcp.json`, but Cursor leaves those servers disconnected until
enabled in Settings → MCP. User-level servers in `~/.cursor/mcp.json` are
auto-approved. Surfaced during R6 validation
([fact-r6-cursor-validation](/memory/facts/fact-r6-cursor-validation.md)).

What's inside: MCP config locations, enable/approve behavior, CLI/editor
parity notes.

Read first: project vs global approval difference (changelog note April
2026).
