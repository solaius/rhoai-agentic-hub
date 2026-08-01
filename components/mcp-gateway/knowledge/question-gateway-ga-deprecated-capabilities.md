---
type: question
title: Which Gateway GA line items need re-scoping after MCP 2026-07-28?
description: Three Gateway GA roadmap items reference capabilities that are deprecated or removed in MCP 2026-07-28 -- resumable session management (sessions removed), sampling (deprecated, 12-month window), and elicitation (replaced by MRTR). Decisions D1-D3 needed by Aug 2026.
status: open
timestamp: 2026-07-29
tags: [mcp-gateway, roadmap, mcp-spec, deprecation]
components: [mcp-ecosystem]
source: hub.research mcp-ecosystem architecture+requirements 2026-07-29
---

The MCP 2026-07-28 spec invalidates three Gateway GA roadmap items
(from [fact-mcp-gateway-roadmap.md](/components/mcp-gateway/knowledge/fact-mcp-gateway-roadmap.md)):

1. **"resumable session management"** -- Sessions removed from protocol.
   Rename to optional HTTP affinity routing, or drop.
2. **"extended capabilities (sampling)"** -- Sampling deprecated with
   12-month window (earliest removal July 2027). Ship as deprecated,
   skip, or document migration?
3. **"MCP elicitation support"** (TP, shipped) -- `elicitation/create`
   replaced by MRTR. TP may only work with 2025-11-25 servers; GA
   needs MRTR support.

See research docs
[01-architecture](/components/mcp-ecosystem/research/01-architecture-mcp-2026-07-28-impact.md)
and
[02-requirements](/components/mcp-ecosystem/research/02-requirements-mcp-2026-07-28-impact.md)
for full analysis.

Decisions D1-D3 needed before GA planning (target Aug 2026).
