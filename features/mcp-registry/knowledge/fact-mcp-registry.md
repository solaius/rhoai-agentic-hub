---
type: fact
title: MCP Registry (3.5 Dev Preview target)
description: The system-of-record / governance backbone for MCP servers — identity, version, lifecycle, certification, trust, auditability.
timestamp: 2026-07-06
tags: [mcp-registry, governance, 3.5-dp]
review_after: 2026-08-05
source: ai-asset-registry/docs/knowledge-registry.md §3, §8 (as of 2026-07-05)
---
New component targeting RHOAI 3.5 Dev Preview. Fills the gap between catalog, deployment (Lifecycle Operator), gateway, and Studio by governing identity, version, metadata, lifecycle state, certification/approval, trust, and auditability for MCP servers. Conceptually integrates with: Catalog (surfacing), Lifecycle Operator (deployment), Gateway (runtime), AAA/Studio (consumption). It is explicitly NOT a replacement for any of those — it's the governance layer underneath them.

**Governance model**: RBAC-aware visibility and management; policy linkage (associating assets with policies/controls); approval workflows kept separate from runtime enforcement (the registry governs what's approved, the gateway enforces at request time — two distinct concerns); auditability and controlled change tracking throughout.

See [fact-mcp-registry-data-model-proposal.md](/features/mcp-registry/knowledge/fact-mcp-registry-data-model-proposal.md) for the proposed data model.
