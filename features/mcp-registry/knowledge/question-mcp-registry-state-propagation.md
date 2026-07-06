---
type: question
title: How registry state should drive gateway and catalog behavior
description: Three open questions on how registry-governed state (lifecycle/approval/verification/certification) should propagate to the Gateway, the Catalog, and the Lifecycle Operator.
status: open
timestamp: 2026-07-06
tags: [mcp-registry, mcp-gateway, mcp-ecosystem]
source: ai-asset-registry/docs/knowledge-registry.md §13 (as of 2026-07-05)
---
1. How should registry-governed state inform Gateway behavior (e.g., should an unapproved/unverified server be routable at all)?
2. How should registry state influence Catalog surfacing (e.g., does "Candidate" show up next to "Published")?
3. How should the MCP Lifecycle Operator interact with the registry — should it create read-only "discovered/managed" entries with restricted mutation, or get full governance write access? (Chris Hambridge / Matt Prahl, Data Model Proposal comments; connects to RHAIRFE-294 per Jon Burdo.)

See [fact-mcp-registry-data-model-proposal.md](/features/mcp-registry/knowledge/fact-mcp-registry-data-model-proposal.md) and [fact-mcp-flow-34-to-35.md](/features/mcp-registry/knowledge/fact-mcp-flow-34-to-35.md).
