---
type: question
title: MCP Registry data model — MVP finalization gaps
description: Six specific decisions still needed to finalize the MCP Registry data model for 3.5 Dev Preview.
status: open
timestamp: 2026-07-06
tags: [mcp-registry, mvp, data-model]
source: ai-asset-registry/docs/knowledge-registry.md §13 (as of 2026-07-05)
---
[fact-mcp-registry-data-model-proposal.md](/features/mcp-registry/knowledge/fact-mcp-registry-data-model-proposal.md) describes the proposed four-track governance model, but these specifics are still undecided for 3.5 Dev Preview:

1. What exact metadata should be mandatory on a registry record?
2. Which of the four tracks' lifecycle states are actually required for the 3.5 DP cut (vs. deferred to a later release)?
3. Should certification programs be backed by an admin-managed allowlist?
4. Should lifecycle history (an audit trail of state transitions) ship in MVP or be deferred?
5. Do approval, verification, and certification transitions need distinct permissions beyond general update permissions?
6. Do MCP registry entities need `EntityAssociationType` support in MVP, or can it wait?
