---
type: reference
title: Unified Platform Agentic Memory Infrastructure
description: A 3-phase Feast-based agent memory architecture (Discovery -> Retrieval -> Write loops) spanning 3.5 and 3.6.
resource: https://docs.google.com/document/d/1Oae8Ie6aoQRcwQ0SEt24yGkLCviWOuLBrzrJgOec0qM
tags: [agent-memory, feast, proposal, architecture]
timestamp: 2026-07-06
source: ai-asset-registry/docs/knowledge-registry.md §12 (as of 2026-07-05)
review_after: 2026-08-05
---
Author: Umberto Manganiello (May 2026). Phase A (Discovery, 3.5): Feast MCP server for agent-assisted feature engineering. Phase B (Retrieval, 3.5): `MemoryFeatureView` with L0/L1/L2 tiers (Redis KV → Parquet summaries → pgvector). Phase C (Write, 3.6): Feast as a pluggable storage backend for Mem0/Zep ("Mem0 owns the cognitive logic; Feast owns the data boundary"). Identifies 5 platform gaps (episodic-memory absence, token-bloat efficiency, personalization, write bottleneck, state contradiction) and evaluates 3 alternatives (pure app-layer, raw infra, framework-native) as insufficient alone. Overlaps significantly with [ref-feast-ogx-agent-memory-proposal.md](/features/agent-memory/knowledge/ref-feast-ogx-agent-memory-proposal.md) — see [question-feast-proposals-vs-memoryhub-overlap.md](/features/agent-memory/knowledge/question-feast-proposals-vs-memoryhub-overlap.md) for the open question on whether these (plus MemoryHub) should merge.
