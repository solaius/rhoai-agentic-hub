---
type: question
title: How does the agent registry interact with Red Hat's multi-track governance model?
description: Open question on reconciling the agent registry's simple runtime lifecycle with MCP Registry's four-track approval/verification/certification governance model.
status: open
timestamp: 2026-07-06
tags: [agent-registry, governance, mcp-registry]
source: ai-asset-registry/docs/knowledge-registry.md §7 (as of 2026-07-05)
---
The agent registry proposal's runtime lifecycle (ACTIVE/UNHEALTHY/STALE/REMOVED) has no approval, certification, or verification tracks — unlike the MCP Registry's four independent governance tracks (see [fact-mcp-registry-data-model-proposal.md](/features/mcp-registry/knowledge/fact-mcp-registry-data-model-proposal.md)). Open question: how should the agent registry interact with Red Hat's multi-track governance model — bolt the same four tracks on top of the runtime lifecycle, or define a different governance shape suited to live services? Identified as Red Hat's main opportunity to add value on top of the upstream proposal (see [fact-agent-registry.md](/features/agent-registry/knowledge/fact-agent-registry.md)).
