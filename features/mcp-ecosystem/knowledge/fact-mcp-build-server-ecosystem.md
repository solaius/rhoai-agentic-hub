---
type: fact
title: MCP build server ecosystem landscape
description: Survey of tools for building MCP servers (gen-mcp, kmcp, FastMCP, fips-agents) — a growing customer/field need with no single tool covering all cases.
timestamp: 2026-07-06
tags: [mcp-ecosystem, build-tools, research]
review_after: 2026-08-05
source: ai-asset-registry/docs/knowledge-registry.md §3 (as of 2026-07-05)
---
Customers increasingly ask "how do I build an MCP server?" — no single tool spans the full spectrum from declarative/no-code (gen-mcp) through scaffolding + composition (kmcp from Solo.io/K Agents, fips-agents/mcp-server-template from Wes Jackson) to full pro-code (FastMCP from PrefectHQ). Key gap identified: business-layer composition — chaining multiple API calls behind one tool with custom logic. Strategic timing: pipeline phase, research targeted for the RHOAI 3.6 timeframe.

Full detail out of scope for this batch — see `mcps/mcp-build-server/knowledge-registry.md` and `mcps/mcp-build-server/research/` in the old repo.
