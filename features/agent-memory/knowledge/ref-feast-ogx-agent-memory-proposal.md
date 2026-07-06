---
type: reference
title: "Feast + OGX Agent Memory: Proposal"
description: Feast team's pitch to replace MemoryHub as the RHAISTRAT-1345 governance layer — not the current direction.
resource: https://docs.google.com/document/d/1NE6aefxMKvyTfceDt9evdnteHd7R9ED0UOpcoTbFVEA
tags: [agent-memory, feast, proposal]
timestamp: 2026-07-06
source: ai-asset-registry/docs/knowledge-registry.md §12 (as of 2026-07-05)
review_after: 2026-08-05
---
Author: Jonathan Zarecki (Jun 23, 2026). Proposes Feast (GA in 3.4, Apache 2.0, ships RBAC/lineage/PIT-correctness) as a MemoryHub governance-layer replacement, via a `MemoryFeatureView` primitive (L0/L1/L2 tiered memory) plus three deltas: record-level scope tiers, write-event audit log, provenance fields. Explicitly marked not the current direction in the old registry — evaluate alongside [ref-memory-hub-repo.md](/features/agent-memory/knowledge/ref-memory-hub-repo.md) rather than treat as settled.
