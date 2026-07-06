---
type: question
title: Agent registry runtime lifecycle vs. Red Hat's multi-track governance model
description: How ACTIVE/UNHEALTHY/STALE/REMOVED runtime states should map onto Red Hat's approval/verification/certification governance tracks, if at all.
status: open
timestamp: 2026-07-06
tags: [agent-registry, mcp-registry, governance]
source: ai-asset-registry/docs/knowledge-registry.md §13 (as of 2026-07-05)
---
[fact-agent-registry.md](/features/agent-registry/knowledge/fact-agent-registry.md) frames the agent registry's runtime lifecycle as "simpler... since it's runtime-focused" and "complementary, not overlapping" with the MCP Registry's multi-track governance ([fact-mcp-registry-data-model-proposal.md](/features/mcp-registry/knowledge/fact-mcp-registry-data-model-proposal.md)). The monolith still lists the mapping as an open question as of 2026-07-05 — treat "complementary, not overlapping" as the working assumption, not a settled answer.

Related, and already framed (not re-opened here): whether the post-deployment agent registry should relate formally to a pre-deployment agent-artifacts registry — [fact-agent-registry.md](/features/agent-registry/knowledge/fact-agent-registry.md) already notes the pre-deployment case is "a separate, deferred proposal."
