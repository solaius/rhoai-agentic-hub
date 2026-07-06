---
type: fact
title: MCP Registry proposed data model (MCPServer / MCPServerVersion)
description: Proposed entity model, the four independent governance status tracks (with their state enumerations), and governance invariants for the MCP Registry — not finalized, a brain-dump-stage proposal.
timestamp: 2026-07-06
tags: [mcp-registry, data-model, mlflow, proposal]
review_after: 2026-08-05
source: ai-asset-registry/docs/knowledge-registry.md §3, §4 (as of 2026-07-05)
---
From the MLflow MCP Registry Data Model Proposal (brain dump, not finalized — see [ref-mlflow-mcp-registry-data-model-proposal.md](/features/mcp-registry/knowledge/ref-mlflow-mcp-registry-data-model-proposal.md)):

- **MCPServer**: logical governed asset scoped to a workspace — name, description, status, tags, aliases, audit fields.
- **MCPServerVersion**: immutable MCP payload (`server_json`) plus mutable governance metadata; each version tracks lifecycle_state, approval_status, verification_status, and certification_status independently.
- Design principles: `server_json` is the canonical immutable payload; governance metadata is first-class (separate from tags); workspace is the MVP visibility boundary; deployment visibility is minimal (`is_deployed` boolean only).
- Governance invariant: `lifecycle_state=PUBLISHED` implies `approval_status=APPROVED`; `REJECTED`/`REVOKED` approval cannot coexist with `PUBLISHED`.
- Key distinction from the older linear 7-state lifecycle doc: governance splits into four independent status tracks instead of one line.

**The four tracks' state enumerations**:
- **Lifecycle State** (5): Draft → Candidate → Published → Deprecated → Retired
- **Approval Status** (5): Draft → Pending → Approved → Rejected → Revoked
- **Verification Status** (2): Unverified → Verified
- **Certification Status** (5): None → Candidate → Certified → Expired → Revoked

This lets a version, e.g., be verified but not yet approved, or approved but not yet certified — independent progression per track, constrained only by the invariant above. Compare the older, pre-proposal linear flow and MLflow's native (non-MCP) registry states in [fact-mcp-server-lifecycle-stages.md](/features/mcp-registry/knowledge/fact-mcp-server-lifecycle-stages.md).
