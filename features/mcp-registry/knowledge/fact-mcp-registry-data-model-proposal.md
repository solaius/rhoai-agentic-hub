---
type: fact
title: MCP Registry proposed data model (MCPServer / MCPServerVersion)
description: Proposed entity model and governance invariants for the MCP Registry — not finalized, a brain-dump-stage proposal.
timestamp: 2026-07-06
tags: [mcp-registry, data-model, mlflow, proposal]
review_after: 2026-08-05
source: ai-asset-registry/docs/knowledge-registry.md §3 (as of 2026-07-05)
---
From the MLflow MCP Registry Data Model Proposal (brain dump, not finalized — see [ref-mlflow-mcp-registry-data-model-proposal.md](/features/mcp-registry/knowledge/ref-mlflow-mcp-registry-data-model-proposal.md)):

- **MCPServer**: logical governed asset scoped to a workspace — name, description, status, tags, aliases, audit fields.
- **MCPServerVersion**: immutable MCP payload (`server_json`) plus mutable governance metadata; each version tracks lifecycle_state, approval_status, verification_status, and certification_status independently.
- Design principles: `server_json` is the canonical immutable payload; governance metadata is first-class (separate from tags); workspace is the MVP visibility boundary; deployment visibility is minimal (`is_deployed` boolean only).
- Governance invariant: `lifecycle_state=PUBLISHED` implies `approval_status=APPROVED`; `REJECTED`/`REVOKED` approval cannot coexist with `PUBLISHED`.
- Key distinction from the older linear 7-state lifecycle doc: governance splits into four independent status tracks instead of one line.
