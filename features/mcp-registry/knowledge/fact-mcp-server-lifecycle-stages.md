---
type: fact
title: MCP server lifecycle — pipeline stages & status states (as documented)
description: The as-documented MCP server pipeline stages, the older linear 7-state governance model, and MLflow's native model-registry states — the baseline the proposed 4-track model (see fact-mcp-registry-data-model-proposal.md) supersedes.
timestamp: 2026-07-06
tags: [mcp-registry, lifecycle, states]
source: ai-asset-registry/docs/knowledge-registry.md §4 (as of 2026-07-05)
review_after: 2026-08-05
---
**Pipeline stages** (6): Sources → Quarantine → Registry → Catalog → Deployments → Consumable.

**Current documented lifecycle-state flow** (7 states, linear — superseded by the proposed 4-track model): Draft → Candidate → Verified → Approved → Published → Deprecated → Retired.

**MLflow native model-registry states**: None, Staging, Production, Archived — flagged as possibly needing expansion to fit MCP governance needs (Dan Kuc comment, source undated).

See [fact-mcp-registry-data-model-proposal.md](/features/mcp-registry/knowledge/fact-mcp-registry-data-model-proposal.md) for the proposed replacement — four independent status tracks instead of one linear flow.
