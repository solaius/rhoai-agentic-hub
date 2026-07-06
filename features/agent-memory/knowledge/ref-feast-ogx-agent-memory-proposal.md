---
type: reference
title: "Feast + OGX Agent Memory: Proposal"
description: Feast team's pitch to replace MemoryHub as the RHAISTRAT-1345 governance layer — not the current direction.
resource: https://docs.google.com/document/d/1NE6aefxMKvyTfceDt9evdnteHd7R9ED0UOpcoTbFVEA
tags: [agent-memory, feast, proposal]
timestamp: 2026-07-06
source: ai-asset-registry/docs/knowledge-registry.md §12 (as of 2026-07-05); MemoryFeatureView/deltas/subsystem-mapping detail from ai-asset-registry/docs/knowledge-review/assets/agent-memory-knowledge.md §7 (as of 2026-07-05)
review_after: 2026-08-05
---
Author: Jonathan Zarecki (Jun 23, 2026). Proposes Feast (GA in 3.4, Apache 2.0, ships RBAC/lineage/PIT-correctness) as a MemoryHub governance-layer replacement, via a `MemoryFeatureView` primitive (L0/L1/L2 tiered memory) plus three deltas: record-level scope tiers, write-event audit log, provenance fields. Explicitly marked not the current direction in the old registry — evaluate alongside [ref-memory-hub-repo.md](/features/agent-memory/knowledge/ref-memory-hub-repo.md) rather than treat as settled.

**`MemoryFeatureView` tiered model (L0/L1/L2)**: L0 (short-term episodic) — last N turns, Redis KV, sub-ms retrieval, maps to the Conversations API. L1 (mid-term summarized) — async batch LLM summaries, Parquet offline + Redis online, maps to `/responses/compact`. L2 (long-term behavioral) — float-array embeddings, pgvector semantic search, maps to Vector Stores + Files. Claimed token savings: ~76% vs. full content loading (said to match the OpenViking benchmark cited in the wider research — see the research doc below).

**Three deltas to close** (additive to what Feast ships today, not architectural rethinks):

| Delta | Requirement | Feast today | Work needed |
|---|---|---|---|
| Record-level scope tiers | `user`/`project`/`role`/`org` scope per memory record | Feature-view-level RBAC only | Add `scope_tier` metadata field + query-layer filter |
| Write-event audit log | Append-only log per memory write (EU AI Act/GDPR/HIPAA gate) | PIT correctness, no per-write event log | Audit hook on `write_to_online_store` path |
| Provenance fields | `identity`/`source_agent`/`lineage` per record | Lineage at feature-view level only | Add optional fields to entity schema |

**Proposed subsystem mapping to RHAISTRAT-1345**: OGX/AI Gateway keeps the Agent Memory Substrate and Context Engineering subsystems unchanged; Feast is proposed for the cross-cutting Governance & Scope layer (replacing MemoryHub) and is positioned as the natural landing zone for the Agent Knowledge (enterprise-RAG/knowledge-graph) subsystem. Contradiction detection stays external to Feast in this proposal (Mem0/Zep handle semantic conflict resolution at the application layer). Proposed timeline: MemoryFeatureView + the scope-tier delta land in RHOAI 3.6.

Full competitive landscape, benchmarks, and RFE roadmap this proposal draws on: [agent-memory-landscape-research.md](/features/agent-memory/research/agent-memory-landscape-research.md).
