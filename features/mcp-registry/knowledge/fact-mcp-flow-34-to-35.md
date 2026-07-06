---
type: fact
title: MCP flow — 3.4 (fragmented/manual) vs. 3.5 (registry-governed) target
description: How MCP server flow changes from RHOAI 3.4's manual, fragmented steps to the 3.5 registry-governed target.
timestamp: 2026-07-06
tags: [mcp-registry, lifecycle, 3.4, 3.5]
source: ai-asset-registry/docs/knowledge-registry.md §4 (as of 2026-07-05)
review_after: 2026-08-05
---
**Current flow (3.4 — fragmented/manual)**:
1. Discover in catalog
2. Deploy through lifecycle operator
3. Manually register in MCP Gateway
4. Manually update ConfigMap
5. Consume through Gen AI Studio

**Target flow (3.5 — registry-governed)**:
1. MCPs discovered and evaluated
2. Governed in the registry (system of record)
3. Surfaced through catalog when approved
4. Associated with deployment/runtime state
5. Made consumable through registry-governed platform paths

The 3.5 target replaces steps 3–4 of the manual flow (register in Gateway, update ConfigMap by hand) with registry governance as the source of truth — see [fact-mcp-registry.md](/features/mcp-registry/knowledge/fact-mcp-registry.md).
