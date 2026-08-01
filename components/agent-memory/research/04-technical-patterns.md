---
title: "Agent Memory & Knowledge: Technical Patterns"
description: Catalog of recurring technical/architecture patterns across agent memory and knowledge systems, independent of specific products or RHOAI integration.
source: ai-asset-registry/agent-memory/research/04-technical-patterns.md (as of 2026-07-05)
timestamp: 2026-07-06
review_after: 2026-08-05
---

# Agent Memory & Knowledge: Technical Patterns

**Purpose:** Catalog and analyze the recurring technical/architecture patterns across agent memory and knowledge systems — how these systems are built, not which specific products implement them (see [02 Solution Survey](02-solution-survey.md)) and not how to integrate them into RHOAI (see [08 RHOAI & OCP Alignment](08-rhoai-ocp-alignment.md)).

**Date:** 2026-05-17

**Status:** REFERENCE — industry patterns synthesized from public technical literature, production system documentation, and academic surveys. Nothing here is a decided RHOAI design. See [RHAISTRAT-1345](https://redhat.atlassian.net/browse/RHAISTRAT-1345).

**Series:** Document 04 of 17 — Agent Memory & Knowledge Research
**Phase 1:** [00](00-executive-summary.md) · [01](01-landscape-and-definitions.md) · [02](02-solution-survey.md) · [03](03-memoryhub-deep-dive.md) · 04 Technical Patterns (this doc) · [05](05-standards-and-protocols.md) · [06](06-ogx-memory-primitives.md) · [07](07-taxonomy-and-decomposition.md) · [08](08-rhoai-ocp-alignment.md)
**Phase 2:** [09](09-agent-harness-memory.md) · [10](10-claude-memory-dreaming.md) · [11](11-adversarial-memory.md) · [12](12-benchmarking-evaluation.md) · [13](13-kv-cache-optimization.md) · [14](14-enterprise-use-cases.md) · [15](15-multi-modal-memory.md) · [16](16-ai-gateway-memory-substrate.md) · [REVIEW-NOTES](REVIEW-NOTES.md)

---

## Contents

1. [Pattern Families Overview](#1-pattern-families-overview)
2. [Storage Substrates](#2-storage-substrates)
3. [Retrieval Patterns](#3-retrieval-patterns)
4. [Memory Writing and Extraction](#4-memory-writing-and-extraction)
5. [Context Compaction and Summarization](#5-context-compaction-and-summarization)
6. [Knowledge Graphs for Organizational Memory](#6-knowledge-graphs-for-organizational-memory)
7. [Scope, Tenancy, and Governance Patterns](#7-scope-tenancy-and-governance-patterns)
8. [Cache Optimization Patterns](#8-cache-optimization-patterns)
9. [Multi-Agent Memory Coordination](#9-multi-agent-memory-coordination)
   - 9.1 [Multi-Agent Memory Architectures](#91-multi-agent-memory-architectures)
   - 9.2 [Write Conflict Resolution](#92-write-conflict-resolution)
   - 9.3 [Shared vs. Private Memory for Swarm Coherence](#93-shared-vs-private-memory-for-swarm-coherence)
   - 9.4 [Scope Isolation and Access Control](#94-scope-isolation-and-access-control)
   - 9.5 [Coordination and Consistency](#95-coordination-and-consistency)
   - 9.6 [Anti-Patterns and Failure Modes](#96-anti-patterns-and-failure-modes)
   - 9.7 [Enterprise Regulatory Requirements](#97-enterprise-regulatory-requirements)
   - 9.8 [Implementation Survey](#98-implementation-survey)
10. [Synthesis: Maturity and Trajectory](#10-synthesis-maturity-and-trajectory)

---

## 1. Pattern Families Overview

**REFERENCE** — Agent memory systems are built from a small set of recurring pattern families that recombine across products. This document organizes them into seven families based on what problem they address in the memory lifecycle.

The agent memory lifecycle follows a standard loop (Redis, 2026; arXiv:2603.07670):

```
read-before-reasoning → reason-and-plan → act → observe → write-after-acting → loop
```

Each pattern family addresses one or more phases of this loop:

| Pattern Family | Phase | Core Problem Addressed |
|---|---|---|
| **Storage substrates** | Read + Write | What technology holds memory state |
| **Retrieval** | Read | How agents find relevant memory |
| **Writing and extraction** | Write | How durable memories are created from raw interaction |
| **Compaction and summarization** | Read + Write | How context windows are kept bounded over time |
| **Knowledge graphs** | Read + Write | How relational and temporal knowledge is organized |
| **Scope, tenancy, governance** | All | Who can read/write what; audit; compliance |
| **Cache optimization** | Read | How retrieval order reduces inference cost |

These families are not mutually exclusive — production systems compose multiple patterns. The LOCOMO benchmark study (referenced in Redis, 2026) showed that selective external memory (using patterns 2–7) achieves 66.9% accuracy at 1.44s p95 vs. full-context in-memory at 72.9% accuracy at 17.12s p95 — a 91% speed gain and 90% token reduction at a 6-point accuracy cost. This accuracy/latency tradeoff is the central engineering tension that all the patterns below navigate.

---

## 2. Storage Substrates

### 2.1 The Single-Substrate Pattern

**REFERENCE** — The single-substrate pattern consolidates relational data, vector embeddings, and graph relationships into one database engine. The primary example is **PostgreSQL + pgvector**: agents store conversation records, user preferences, entity relationships, and vector embeddings in one PostgreSQL instance. Relational data and vectors are queryable together in the same transaction.

**Technical advantages:**
- ACID consistency: updating a document and its embedding happen atomically — no dual-write synchronization lag (MarkTechPost, 2026)
- Unified operations: backups, migrations, schema changes, monitoring cover one system
- Transactional integrity: no window where relational and vector representations are out of sync
- Reduced FIPS/security surface: one system to validate rather than three

**Scale thresholds (REFERENCE — from practitioner analysis, not formal benchmarks):**
- Under 10M vectors: pgvector matches or exceeds dedicated vector databases on most workloads (MarkTechPost, 2026)
- Under 50M vectors at 99% recall: pgvector with HNSW indexes is competitive with Qdrant on equivalent compute (Supabase benchmarks, cited in MarkTechPost, 2026)
- With pgvectorscale (Timescale extension): 471 QPS at 99% recall on 50M vectors — claimed 11.4x better than Qdrant on their benchmarks (MarkTechPost, 2026; note: vendor benchmark, not independently reproduced)
- Above ~50–100M vectors or sub-10ms p99 latency requirements: dedicated vector databases become defensible

**Who uses this:** MemoryHub (PostgreSQL + pgvector for all relational, vector, and graph queries — explicitly chose this after pivoting away from Milvus + Neo4j + MinIO for FIPS reasons, per `retrospectives/2026-04-03_phase-1-foundation/RETRO.md`); Oracle AI Agent Memory (Oracle 23ai combining relational + vector + graph); Redis (single platform covering short-term in-memory state, vector ANN search, operational state, and coordination via Streams).

**RHOAI relevance:** The single-substrate pattern reduces operational complexity and FIPS/security surface area — both high priorities for an enterprise Kubernetes platform. MemoryHub's Phase 1 retrospective documents the concrete tradeoffs that led to this choice.

---

### 2.2 Multi-Store Architectures

**REFERENCE / CONTESTED** — Multi-store architectures separate concerns into specialized databases: a vector store (Qdrant, Pinecone, Milvus) for semantic search; a relational database for structured records; a graph database (Neo4j, FalkorDB) for entity relationships; sometimes a key-value cache (Redis, Valkey) for hot-path session data.

**Technical advantages:**
- Each store optimized for its specific access pattern
- Horizontal scaling per tier based on actual load
- Best-of-breed tooling for each data type
- At 100M+ vectors, dedicated systems provide better throughput guarantees

**Technical disadvantages:**
- Cross-store queries require application-layer joins — complex and error-prone
- Dual-write paths (same data to vector store AND relational store) create consistency windows
- Four failure modes instead of one
- FIPS/security surface multiplied across every system
- Operational sprawl: separate monitoring, backup, upgrade cycles for each store

**Contradiction to flag — this is a genuinely contested pattern.** The multi-store approach was the default in 2022–2024 as purpose-built vector databases gained adoption. The 2025–2026 trend has shifted toward reconsidering it. The 2026 consensus from practitioner literature (MarkTechPost, 2026; ZenML; SingleStore) is that most agent memory workloads — typically bounded, coherent per-user or per-project stores rather than large heterogeneous corpora — do not require dedicated vector databases. The convergence is: "if you're under ~10–50M vectors, start with pgvector before adding new infrastructure." However, for large-scale organizational knowledge (Peter's area 1 use case), approaching 50M–100M+ entities, the dedicated-database case becomes stronger.

**Who uses multi-store:** Microsoft GraphRAG (separate graph construction + vector retrieval); Cognee ECL pipeline (graph store + embedding index); Letta's archival memory tier (external vector store as the "hard drive" in the OS analogy); early-stage startups that adopted purpose-built vector databases before pgvector matured.

---

### 2.3 Tiered Memory Architecture

**REFERENCE** — The tiered memory pattern (pioneered by Letta/MemGPT, 2023) models the LLM context window as constrained RAM and organizes memory across three explicit tiers:

| Tier | Analogy | Technology | Access Speed |
|---|---|---|---|
| **Core memory** (in-context) | RAM | Context window tokens, directly editable | Instantaneous (already in prompt) |
| **Recall memory** (warm) | Paging file | Relational/vector store, searchable on demand | Milliseconds (vector query) |
| **Archival memory** (cold) | Hard drive | Externalized vector/graph store | Seconds (retrieval + injection) |

**How it works:** Agents actively manage tier promotion/demotion via function calls. Core memory has explicit character limits per labeled block (e.g., `human` block, `persona` block, `project` block). When core memory fills, the agent summarizes and pages content down to recall. Archival memory is accessed via explicit tool calls.

**Technical significance:** This is the most explicit OS-inspired memory model and the clearest conceptual framework for explaining memory tiers to platform engineers. The CoALA taxonomy (arXiv:2309.02427, 2023) independently maps to this hierarchy: working memory = core tier, episodic memory = recall tier, semantic + procedural memory = archival tier.

**Who uses this:** Letta (the originating implementation, though note Letta has since pivoted toward local-first developer tooling per [02 Solution Survey](02-solution-survey.md)); AWS Bedrock AgentCore Memory (two-tier: sessions = recall, extracted records = archival); Google Vertex AI Memory Bank (sessions + Memory Profiles); LangGraph (thread-scoped state = core/recall, LangGraph Stores = archival).

**RHOAI relevance:** The tiered model provides the vocabulary for platform engineers and the conceptual basis for designing memory primitives. The specific tier boundaries and promotion logic are implementation decisions; the three-tier model itself is the useful abstraction.

---

### 2.4 The OS-Analogy vs. One-Substrate Tension

**CONTESTED** — A key architectural tension: Letta's tiered model (tiers = separate systems with explicit promotion) vs. Oracle/MemoryHub's unified substrate model (one database with access-pattern differentiation). 

Letta: different tiers require different optimizations; separating them lets each scale independently.

Oracle: the four memory types are not four systems but four access patterns over one governed substrate; unifying them eliminates consistency problems between stores and allows governance to be applied uniformly.

The evidence favors the Oracle/MemoryHub model for enterprise governance use cases — consistency, ACID semantics, and unified audit are easier to implement on one system. The tiered-system model is better for architectures with radically different scale requirements per tier (e.g., millions of episodic events but only thousands of curated semantic facts). RHOAI should evaluate its workload profile before deciding.

---

## 3. Retrieval Patterns

### 3.1 Vector/Semantic Search

**REFERENCE** — Vector search is the baseline retrieval pattern: text chunks are embedded into dense vectors at write time; at query time the query string is embedded and Approximate Nearest Neighbor (ANN) search retrieves top-k semantically similar entries. HNSW (Hierarchical Navigable Small World) is the dominant ANN index for production systems — it trades a small accuracy loss for dramatically faster lookups at scale (Redis, 2026; arXiv:2603.07670).

**Limitation:** Dense embeddings average token representations, which destroys exact string matching. They fail silently on:
- Error codes and identifiers (e.g., `ERR_SSL_VERSION_OR_CIPHER_MISMATCH`, `0x80070005`)
- SKUs and model numbers (e.g., `RTX-4090` vs `RTX-4070` appear near-identical in embedding space)
- Exact function signatures and rare named entities
- Domain jargon with controlled vocabulary (tianpan.co, 2026)

This limitation is the primary motivation for hybrid search (Section 3.2).

---

### 3.2 Hybrid Search (Vector + BM25)

**REFERENCE** — Hybrid search combines dense vector search with BM25 keyword matching. BM25 uses an inverted index to match exact tokens; its relevance score incorporates term frequency, inverse document frequency, and document length normalization. The combination addresses the failure modes of each method independently.

**The 2026 practitioner consensus** is that hybrid retrieval outperforms single-method approaches across the board for agent memory workloads. A benchmark across ~25,000 QA pairs (4 datasets) and 8 conversational datasets showed hybrid retrieval superior to single-method approaches in all tested conditions (Redis, 2026 — vendor-curated evaluation).

**Weighting strategies:**

- **Reciprocal Rank Fusion (RRF):** Score = `1 / (k + rank)` where k=60. Score-scale agnostic; requires no labeled data; standard in Elasticsearch, Weaviate, Qdrant, OpenSearch 2.19. Limitation: discards score magnitude information. A Wands/Elasticsearch study found properly tuned alpha weighting outperformed RRF by a meaningful margin (7.5% vs 1.3% NDCG improvement), but alpha tuning requires labeled data (reported by tianpan.co, 2026 — practitioner/secondary source, not the primary study).

- **Convex combination (tuned alpha):** `score = α × score_dense + (1-α) × score_sparse`. With ~40 labeled examples per domain, consistently outperforms RRF. Recommended values: technical documentation α ≈ 0.3, conversational content α ≈ 0.7–0.8, mixed content α ≈ 0.6 (tianpan.co, 2026).

- **Dynamic alpha (emerging):** Detecting whether an incoming query is keyword-heavy or semantic, adjusting α at query time rather than per-collection. Described as the 2025–2026 frontier in practitioner literature; not yet a standard feature in open-source systems (tianpan.co, 2026).

**Production architecture:** Hybrid retrieval produces a candidate pool (top-100); cross-encoder reranking is applied to reduce to the final 5–30 for context injection (Section 3.3). MMR de-duplication is optionally applied between retrieval and reranking to remove near-identical chunks.

**Specific implementations:**
- **OpenClaw:** Fixed 70% vector / 30% BM25, RRF blending, with MMR re-ranking (λ=0.7 default) and temporal decay — the canonical client-side hybrid memory implementation per [01 Landscape & Definitions](01-landscape-and-definitions.md)
- **Mem0 v2.0.0:** Hybrid semantic + BM25 + entity-graph boosting (April 2026), replacing a multi-system approach with single-pass extraction
- **MemoryHub:** Two-vector retrieval via RRF (Section 3.4) — query vector + session focus vector blended at configurable weight
- **Zep/Graphiti:** Cosine similarity + BM25 full-text + breadth-first graph traversal in a multi-signal retrieval stack

---

### 3.3 Cross-Encoder Reranking

**REFERENCE** — Cross-encoder reranking is a two-stage retrieval pattern that separates high-recall candidate retrieval from high-precision final selection.

**Stage 1 (recall):** Hybrid retrieval (or pure vector) produces 50–200 candidates cheaply — ANN search is fast even at scale.

**Stage 2 (precision):** A cross-encoder model evaluates each candidate pair (query, candidate) jointly using full attention. This is computationally expensive (O(n) full model passes) but produces significantly better relevance ranking than the dual-encoder models used in stage 1. Target latency for stage 2: 100–200ms on 30–50 candidates (tianpan.co, 2026).

**Standard models:** `ms-marco-MiniLM-L12-v2` (used by MemoryHub), `ms-marco-MiniLM-L6-v2`, and other cross-encoders trained on MS MARCO passage retrieval. These are small but effective for reranking.

**RHOAI relevance:** MemoryHub uses `ms-marco-MiniLM-L12-v2` on RHOAI vLLM serving, with graceful fallback when the reranker is unreachable. This is a production-quality pattern for RHOAI: deploy the cross-encoder as a secondary vLLM endpoint; treat it as optional but recommended.

---

### 3.4 Two-Vector Retrieval with Session Focus

**REFERENCE** — A distinctive retrieval pattern developed for session-aware memory: the retrieval call includes both a semantic *query* vector and a separate *session focus* vector, with the two signals blended via RRF.

**How it works (MemoryHub implementation, per `docs/agent-memory-ergonomics/design.md`):**
1. Agent passes `query="what is the FIPS posture"` AND `focus="OpenShift deployment"` with a `session_focus_weight=0.4` parameter
2. System embeds query and focus independently
3. pgvector cosine retrieves top-K=32 by query embedding
4. Cross-encoder reranker runs on those candidates
5. RRF blends reranker ranks with focus-vector cosine ranks at `session_focus_weight`
6. Response includes `pivot_suggested` signal when query-to-focus distance exceeds a threshold (cosine > 0.55), indicating the agent's session has shifted topics

**Why stateless focus:** The focus string is passed per-call, not stored server-side. This eliminates server-side session state, enables horizontal scaling without coordination, and adds only ~50ms per call for focus re-embedding on a warm vLLM instance. The design retrospective in MemoryHub explicitly evaluated stateful vs. stateless session focus and chose stateless on simplicity and operability grounds.

**Who uses this:** MemoryHub (shipped as Layer 2 of agent-memory-ergonomics, 2026-04-07); the pattern is not documented as a named standard elsewhere in the literature — it is a distinctive architectural choice.

---

### 3.5 Temporal and Graph-Aware Retrieval

**REFERENCE** — Standard vector search is temporally blind: it retrieves by semantic similarity without regard to when facts were true or whether they have been superseded. Temporal and graph-aware retrieval corrects this.

**Temporal retrieval operators** (from graph-based memory taxonomy, arXiv:2602.05665):
- **Recency scoring:** Exponential decay applied to embedding similarity scores — a fact noted three months ago scores lower than one noted last week, unless marked evergreen. OpenClaw implements configurable half-life (default 30 days); MEMORY.md files are marked evergreen and never decay.
- **Bi-temporal tracking:** Zep/Graphiti maintains four timestamps per edge: `t'created` (database insert time), `t'expired` (database removal time), `t_valid` (when the fact became true in the world), `t_invalid` (when the fact ceased to be true). This enables accurate resolution of relative temporal references ("two weeks ago") and fact supersession — capabilities that vector-only systems cannot provide.
- **Timeline indexing:** Systems that parse temporal expressions and index them as inferred absolute timestamps rather than relative strings, enabling timeline-based filtering and reconstruction.

**Graph traversal retrieval:** Breadth-first or depth-first traversal across entity-relationship edges, enabling multi-hop retrieval that vector similarity alone cannot perform. Example: "What projects does the team that worked on Project X also work on?" requires graph traversal, not semantic similarity. HopRAG (arXiv:2502.12442) showed graph-structured retrieval with logical traversal achieves **76.78% higher answer accuracy and 65.07% improved retrieval F1 vs. the BGE dense retriever** on multi-hop reasoning benchmarks (MuSiQue, 2WikiMultiHopQA, HotpotQA) — though these are research-benchmark figures, not production deployments.

**Multi-signal scoring (Generative Agents pattern, arXiv:2603.07670):** Combines recency (exponential decay), relevance (embedding similarity), and importance (LLM self-assessed importance score) rather than pure similarity. This tripartite scoring is directly cited in the academic survey as a production-relevant pattern for episodic memory retrieval.

**RHOAI relevance:** Temporal retrieval is directly relevant to the hardest benchmark category for all agent memory systems: multi-session recall, where facts get stale, updated, or contradicted across sessions. Bi-temporal tracking (Graphiti/Zep) is the most technically mature open-source implementation; PostgreSQL can approximate this via versioned records (MemoryHub's `isCurrent` + version chain pattern), though without the full bi-temporal query expressiveness of a native graph database.

---

### 3.6 Selective Retrieval (Retrieval as a Tool Call)

**REFERENCE** — Rather than unconditionally retrieving memory before every inference call, selective retrieval treats retrieval as a conditional tool call: the agent (via LLM reasoning) decides whether memory retrieval is needed for the current task.

**Self-RAG pattern:** Demonstrated by arXiv:2603.07670 as a technique that cuts unnecessary retrieval latency for tasks that do not require long-term context. The agent generates a retrieval relevance score before executing the retrieval call.

**Agentic RAG bridge:** Described in [01 Landscape & Definitions](01-landscape-and-definitions.md) — the agent dynamically decides whether and where to retrieve external knowledge. This is the same principle applied to memory: retrieval-on-demand rather than retrieval-on-every-turn.

**Tradeoff:** Selective retrieval reduces token consumption and latency for tasks that don't need context, at the cost of requiring accurate self-assessment from the LLM about when context is needed. Over-conservative self-assessment leads to missing relevant history; over-liberal self-assessment recreates the full-context latency penalty.

---

## 4. Memory Writing and Extraction

### 4.1 The Write Path

**REFERENCE** — The write path is the most complex and differentiated part of memory system architecture. The standard multi-stage write pipeline (arXiv:2603.07670; Redis, 2026) includes:

1. **Filtering:** Removing low-signal noise — small talk, redundant confirmations, near-duplicate content
2. **Canonicalization:** Normalizing dates, names, quantities, entity references
3. **Deduplication:** Merging overlapping entries (via embedding similarity threshold)
4. **Priority scoring:** Ranking by task relevance and novelty
5. **Metadata tagging:** Timestamps, source attribution, task labels, confidence scores
6. **Embedding generation:** Computing vector representations for retrieval
7. **Write to store:** Persisting with metadata and embedding

The write path is where most systems differ in sophistication. Simple systems (OpenClaw, early Letta) append every turn; sophisticated systems (Mem0, MemoryHub, CrewAI) apply multi-stage filtering before any write.

---

### 4.2 LLM-Based Memory Extraction

**REFERENCE** — In LLM-based extraction, the agent's LLM (or a dedicated smaller extraction model) processes raw conversation turns and extracts durable facts to write to the memory store. This is how episodic events become semantic memories.

**The core operation:** The system passes recent turns (or a windowed batch) to an LLM with a prompt like "extract any facts worth remembering in the long term from this conversation" and writes the output as memory records. Oracle AI Agent Memory, LangMem, Mem0 v2, and AWS AgentCore Memory (background extraction pipeline) all implement this.

**Extraction triggers:**
- **Hot-path (inline):** Extraction runs on every turn or every N turns. LangMem provides `create_manage_memory_tool` for inline extraction. Cost: adds LLM call latency to every write. LangMem's p95 extraction latency is 59.82 seconds for background processing (as of the version tested in [02 Solution Survey](02-solution-survey.md)) — unsuitable for interactive agents at that latency level; treat as a version-specific measurement, not a permanent characteristic.
- **Background (async):** Extraction runs out-of-band after turns complete, without blocking inference. AWS AgentCore Memory (asynchronous extraction pipeline), LangMem background memory manager, Mem0 (async writes) all use this pattern.
- **Sleep-time / consolidation (off-session):** Extraction runs between sessions, processing accumulated episodic records into semantic facts. See Section 5.3.

**Single-pass vs. multi-pass extraction:** Mem0 v2.0.0 (April 2026) introduced single-pass hierarchical extraction — one LLM call per `add()` — replacing an earlier multi-pass approach. This shifted graph traversal depth for deployment simplicity and reduced latency.

**Episodic-to-semantic consolidation:** The cognitive science insight (arXiv:2603.07670) is that semantic memory consolidation from episodic is rarely automatic — e.g., the episodic records "user corrected date format on Jan 5, Jan 12, and Feb 1" should consolidate into the semantic fact "user prefers DD/MM/YYYY," but this requires either explicit prompting or heuristic triggers. Systems that manage this transition explicitly have better long-term memory quality than those that treat semantic and episodic as separate append-only stores.

---

### 4.3 Append vs. Update vs. Selective Encoding

**REFERENCE** — Three distinct approaches to how new information is written relative to existing memories:

**Append-only:** Every new memory creates a new record; existing records are never modified. Simple, auditable, and consistent. Limitation: store grows indefinitely; stale facts co-exist with current facts; retrieval degrades as noise accumulates. OpenClaw's daily log files (`memory/YYYY-MM-DD.md`) are append-only; only `MEMORY.md` is curated.

**Update-in-place:** New information overwrites existing records when a newer version of the same fact arrives. Simpler retrieval (only current facts stored) but loses version history needed for forensics and contradiction debugging.

**Selective encoding with contradiction resolution (CrewAI Cognitive Memory pattern):** When saving new content, the system checks for similar existing records (similarity threshold 0.85 in CrewAI's implementation); an LLM decides whether to keep, update, delete, or merge the conflicting records. This is the most sophisticated pattern — it implements "purposeful forgetting" alongside "purposeful remembering." The cognitive analogy is how human semantic memory consolidates and updates rather than simply accumulating.

**Contradiction detection as a distinct step:** MemoryHub implements a separate contradiction detection path: agents call `manage_curation(action="report_contradiction", memory_id=..., observed_behavior=..., confidence=...)`. Reports accumulate in a `contradiction_reports` table. When unresolved count crosses threshold (currently 5), the curator surfaces the memory for review. This decouples detection from resolution, which is the right separation for a governed system — agents detect, humans (or a background process) resolve.

---

### 4.4 Write-Time Deterministic Curation vs. Inline LLM Sampling

**REFERENCE** — An important design decision in the write path: whether LLM inference is used at write time for content decisions, or whether write-time checks are deterministic (regex, embedding similarity) with LLM judgment deferred to the calling agent.

**MemoryHub's decision (REFERENCE — from `docs/curator-agent.md`):** Earlier designs included LLM sampling at write time for ambiguous cases. This was removed because the MCP specification requires human-in-the-loop for sampling, creating unacceptable write-path friction. The adopted design: write-time pipeline is entirely deterministic (Tier 0: Pydantic schema validation; Tier 1: regex PII/secrets scanning; Tier 2: pgvector embedding similarity dedup check at 0.95 cosine threshold). The calling agent's own LLM handles judgment calls using the similarity feedback returned in the write response (`similar_count`, `nearest_id`, `nearest_score`, `flags`, `blocked`).

**Implication:** Deterministic write-time curation keeps write latency predictable and avoids MCP HITL friction. It shifts ambiguity resolution to the calling agent, which already has an LLM context and can make the judgment inline. This is the right architectural division for an MCP-native memory service.

---

## 5. Context Compaction and Summarization

### 5.1 The Compaction Problem

**REFERENCE** — As an agent's conversation history grows, injecting the full transcript into the context window becomes expensive and counterproductive. Oracle's measurements (via internal seed document, `docs/knowledge-review/assets/agent-memory-knowledge.md`; Oracle blog returned HTTP 403 — not directly verified): an 80-turn conversation held flat at ~1,300 tokens/request with memory-augmented retrieval vs. ~13,900 tokens for a flat history — approximately 9.5x context efficiency difference. Quality also favored retrieved context: "a retrieved context card focuses the model; a sprawling transcript dilutes attention."

**Compaction** is the process of reducing context size by summarizing, truncating, or compressing older turns while preserving the information needed for task continuity. It is a distinct problem from memory extraction: compaction is about managing working memory; extraction is about promoting episodic events to long-term semantic store.

---

### 5.2 Threshold-Based Trigger Strategies

**REFERENCE** — Compaction is triggered when working memory approaches a threshold. Practitioner guidance (Zylos Research, 2026; Google ADK) recommends proactive triggering at 60–70% context window utilization — before performance degrades, not after errors appear.

**Compaction trigger models:**
- **Token-count threshold:** Simple and deterministic. Google ADK configures compaction to run when a configured number of workflow events or invocations is reached.
- **Percentage threshold:** Compact when context reaches N% of context window limit. More model-agnostic than absolute token counts.
- **Turn-count threshold:** Compact every N turns. Predictable but ignores actual content density.
- **Manual / developer-controlled:** Explicit API call. OpenAI's `/responses/compact` endpoint supports this (standalone trigger for developer-controlled compaction).

The threshold value is itself a tunable quality parameter: lower thresholds (compact earlier) reduce context noise but may discard relevant recent turns; higher thresholds (compact later) preserve more context but increase token costs and latency.

---

### 5.3 Human-Readable vs. Opaque Compaction

**CONTESTED — this is the most significant design fork in context compaction.** Two fundamentally different approaches exist, with direct regulatory implications:

**Opaque compaction:** OpenAI's `/responses/compact` produces an opaque, encrypted state artifact — GPT-4.1 and above are fine-tuned to produce and consume these compressed state artifacts. The output is not human-readable and is optimized for reconstruction quality. Triple Whale reported handling a 5M token session over 150 tool calls without accuracy degradation (Triple Whale's own assessment, not independently benchmarked; from [02 Solution Survey](02-solution-survey.md)). Factory.ai's evaluation found OpenAI achieved 3.35/5.0 overall quality score — lowest of the three methods tested — despite highest compression ratio (99.3%). The "tokens per task" metric (accounting for re-fetch costs when detail is lost) matters more than raw compression ratio.

**Structured/readable compaction:** Factory.ai's own method ("anchored iterative summarization") uses explicit sections for intent, file modifications, decisions, and next steps — producing 4.04/5.0 on accuracy and 4.44/5.0 on completeness, outperforming OpenAI by 0.35 points overall (Factory.ai, 2026; evaluation across 36,611 production messages). Anthropic's SDK compression produces 7,000–12,000-character structured summaries. Anthropic's Claude Dreaming (sleep-time) produces CLAUDE.md-style structured files.

**The regulatory constraint:** For RHOAI deployments subject to EU AI Act transparency requirements (enforcement August 2026), GDPR, or HIPAA, the compaction artifact must be inspectable. Opaque compaction — even if superior in pure accuracy metrics — cannot satisfy compliance inspection requirements. MemoryHub's roadmap explicitly commits to human-readable summaries "so the compliance team can inspect what was kept" (README.md).

**Remaining challenge:** Artifact tracking (file/state awareness across compression cycles) remains unsolved across all approaches. Factory.ai's evaluation found artifact trail scores in the 2.19–2.45/5.0 range — weak across all tested methods. This suggests compaction alone is insufficient for stateful agents tracking complex file or system state; supplementary state tracking is needed.

---

### 5.4 Sleep-Time Consolidation

**REFERENCE** — Sleep-time consolidation (also called "background consolidation" or "dreaming") runs memory reorganization asynchronously between active sessions, without blocking inference.

**How it works:** After sessions complete, a scheduled background process reviews accumulated episodic records, compares against existing memory, prunes stale entries, merges duplicates, resolves contradictions, and writes a reorganized memory layer. The output is available for the agent's next session.

**Implementations:**
- **Anthropic Claude Dreaming** (May 2026, research preview): Reviews up to 100 past sessions; presents updated memory for human approval before agents adopt it. Source sessions preserved untouched. Output is CLAUDE.md-style structured files. Human approval gate is a governance control that distinguishes this from autonomous self-modification. Harvey (legal AI) reported approximately 6x task completion rate improvement after enabling Dreaming — this figure is from Anthropic's own launch announcement, not an independent publication.
- **Letta sleep-time compute** (2026): Asynchronous memory agents running between sessions. Developer-controlled, framework-agnostic. Mirrors Anthropic Dreaming architecturally; no equivalent governance gate in the open-source version.
- **OpenClaw dreaming pass:** The `DREAMS.md` file captures optional consolidation output from background dreaming passes. Lightweight, no governance gate.
- **MemoryHub promotion pipeline** (EXPLORATORY — roadmap, not shipped): Background curator agent for cross-user pattern detection and scope promotion (user → organizational, with HITL approval for enterprise scope). This adds the governance gate that the Letta/OpenClaw implementations lack.

**The human governance gate (EXPLORATORY):** Anthropic's Dreaming and MemoryHub's planned promotion pipeline both include a human approval step before reorganized memory is deployed. This is not present in Letta's or OpenClaw's implementations. For enterprise governance contexts, the governance gate is the differentiating feature — it prevents autonomous self-modification of organizational memory without oversight. The pattern: propose → review → approve/reject → deploy.

**Performance signal:** The academic survey (arXiv:2603.07670, citing the original Generative Agents paper, Park et al., arXiv:2304.03442) cites: "Generative Agents without reflection degenerated within 48 simulated hours to repetitive responses" — the strongest direct evidence that sleep-time consolidation is functionally necessary, not merely an optimization, for long-running agents. Without periodic memory reorganization, quality degrades.

---

## 6. Knowledge Graphs for Organizational Memory

### 6.1 Why Graphs for Knowledge

**REFERENCE** — Flat vector stores are semantically powerful but relationally blind. They cannot efficiently answer queries like "what projects does the person who approved policy X also oversee?" or "what facts has this user's preference changed to since last month?" Graph-structured memory addresses these limitations by representing entities, relationships, and temporal facts as an interconnected network rather than a flat index.

The 2026 practitioner consensus (AgentMarketCap, 2026; neo4j/Graphiti, 2026): **vectors for semantic entry-point retrieval, graphs for relational depth.** This is not a binary choice — production systems use both. The vector index provides fast semantic access; the graph provides relational traversal once an entry-point entity is found.

---

### 6.2 Knowledge Graph Construction (GraphRAG-Style)

**REFERENCE** — GraphRAG-style construction (Microsoft GraphRAG, MIT license) builds a knowledge graph at index time by:
1. Reading all documents
2. Extracting entities and relationships via LLM prompting (producing entity-relation-entity triples)
3. Grouping entities into thematic clusters/communities via label propagation
4. Generating community summaries

Cross-document reasoning happens during indexing rather than at query time. Multi-hop retrieval at query time leverages the pre-built community structure.

**Performance figures (Microsoft Research and practitioner analysis, from [02 Solution Survey](02-solution-survey.md)):**
- 26% improvement in answer comprehensiveness vs. standard vector RAG
- 57% improvement in response diversity
- GraphRAG wins 70–80% of complex sensemaking tasks vs. baseline RAG (Microsoft self-evaluation — win-rate judgments on their own corpora)

**Indexing cost evolution (REFERENCE):** Full GraphRAG's indexing cost was historically $50–200 for moderate corpora, creating a prohibitive barrier. Microsoft's **LazyGraphRAG** (released late 2024, production-ready June 2025) reduces indexing cost to approximately 0.1% of full GraphRAG at moderate scale, by deferring all pre-summarization and using NLP noun-phrase extraction instead. The prohibitive cost framing now applies only to full GraphRAG on very large corpora; LazyGraphRAG has substantially resolved the cost objection for moderate-scale deployments. *(Caveat: the 0.1% figure is from Microsoft's own research announcement — treat as vendor-claimed until independently reproduced.)*

**LLM-based entity extraction vs. NLP pipelines:** The academic survey (arXiv:2602.05665) documents that LLM-based extraction of entity-relation triples outperforms traditional NLP pipelines by leveraging contextual understanding of implicit relations. The tradeoff is cost (LLM calls at index time) vs. quality. LazyGraphRAG addresses this by deferring LLM extraction to query time, combining NLP-based indexing with LLM-assisted retrieval.

---

### 6.3 Temporal Knowledge Graphs

**REFERENCE** — Standard knowledge graphs record static triples (entity, relation, entity). Temporal knowledge graphs extend this to quadruples or quintuples including time validity information, enabling accurate reasoning about how facts change over time.

**Zep/Graphiti bi-temporal model (REFERENCE — from arXiv:2501.13956 and Zep documentation):**
Four timestamps per edge:
- `t'created`: When the record entered the database (transaction time)
- `t'expired`: When the record was removed from the database (transaction time)
- `t_valid`: When the fact became true in the world (event time)
- `t_invalid`: When the fact ceased to be true in the world (event time)

This separation of transaction time from event time allows the system to:
- Answer "what was true at time T?" (point-in-time queries)
- Resolve relative temporal expressions ("two weeks ago" → inferred absolute timestamp)
- Track fact supersession without deletion (old version is `t_invalid`-bounded, new version has open `t_invalid`)
- Enable forensic reconstruction of what an agent believed at any past point

**Three-level graph structure (Graphiti/Zep):**
1. **Episode subgraph:** Raw data nodes (ingestion events)
2. **Semantic entity subgraph:** Extracted entities and typed relationships
3. **Community subgraph:** Clustered summaries via label propagation

**Benchmark results (from arXiv:2501.13956, peer-reviewed — the most methodologically reliable benchmark in this area):**
- LongMemEval with Zep + gpt-4o: 71.2% (+18.5% improvement over baseline)
- Latency reduction: approximately 90% (2.6s vs 28.9s at baseline)
- Context tokens reduced from ~115K to ~1.6K per query

Note: This 71.2% is lower than Oracle's (93.8%) and Mem0's (93.4%) published figures, but uses different model configurations and test conditions — direct comparison is not methodologically valid.

**RHOAI relevance:** Temporal knowledge graph capabilities are relevant primarily to Peter's area 1 (Agent Knowledge — org-wide knowledge layer) and to the hardest memory benchmark category: multi-session temporal reasoning. PostgreSQL + adjacency-list graph queries (MemoryHub's current approach) can approximate bi-temporal semantics via versioned records, but without the full expressive power of a native graph database. Whether the expressiveness gap justifies adding a graph database dependency is a design decision for RHOAI — see [Q44 in `docs/knowledge-registry.md`].

---

### 6.4 Incremental vs. Batch Graph Construction

**CONTESTED** — Two graph construction strategies for evolving organizational knowledge:

**Batch/index-time construction (Microsoft GraphRAG, Cognee ECL pipeline):** Graph is built offline over a full document corpus. High quality from global entity resolution and community summarization. Latency-free at query time. Cost: rebuilding the graph after every new document is expensive (mitigated by LazyGraphRAG).

**Incremental/online construction (Graphiti/Zep, Cognee continuous updates):** Graph is updated incrementally as new documents or interactions arrive, "instantly updating entities, relationships, and communities without batch recomputation" (neo4j/Graphiti blog, 2026). Lower rebuild cost; potential for stale community summaries if batching is deferred; more complex conflict detection when entities arrive in arbitrary order.

**Cognee "Cognify" step:** A middle approach — continuously rewriting graph structure based on usage patterns: pruning stale nodes, strengthening frequent connections, reweighting edges based on usage signals, adding derived facts. This is a form of self-improving memory. The tradeoff: non-deterministic graph evolution is harder to audit and debug than batch construction.

**Production recommendation (REFERENCE — from practitioner literature, not formal study):** For organizational knowledge that changes infrequently (policies, product documentation, regulations), batch construction with incremental updates on change events. For episodic agent memory that updates per-session, incremental construction.

---

## 7. Scope, Tenancy, and Governance Patterns

### 7.1 Scope Hierarchies

**REFERENCE** — A scope hierarchy defines who owns and who can access each memory record. It is the fundamental multi-tenancy primitive for a memory service. The pattern recurs across all enterprise memory systems; they differ in the number of tiers and the enforcement mechanism.

**Common scope tiers (from survey of implementations):**

| Tier | Description | Examples |
|---|---|---|
| **User** | Private to a single user | All systems support this |
| **Agent** | Private to a specific agent instance | Mem0 (`agent_id`), LangGraph (thread-scoped state) |
| **Session/Run** | Private to a single conversation run | OpenAI Sessions (`sessionId`), Mem0 (`run_id`) |
| **Project/Team** | Shared within a bounded team/project | MemoryHub project scope, Mem0 (`app_id`) |
| **Campaign** | Bounded cross-project sharing for a defined initiative | MemoryHub campaign scope (added April 2026) |
| **Role** | Shared across users holding a platform role | MemoryHub role scope |
| **Organizational** | All agents in an organization | MemoryHub organizational scope, Oracle tenant-scoped isolation |
| **Enterprise/Policy** | Organization-wide mandated rules with HITL enforcement | MemoryHub enterprise scope |

**MemoryHub's six-tier model** (user/project/campaign/role/organizational/enterprise) is the most detailed in the surveyed implementations. The scope hierarchy is enforced at the SQL level — authorized-scopes filter built as a SQL clause — making RBAC violations impossible by construction (per `docs/governance.md`).

**Oracle's per-record model:** Every memory record carries user, agent, thread, and timestamp scoping fields. Multi-tenant isolation enforced at the database layer, not the application layer. This is equivalent to row-level security but more granular — every record carries its own access context.

**The key principle (from MemoryHub governance doc):** Cross-user writes are explicitly blocked as a security property: "if someone else could modify your memories, they could change how your agent behaves and make you appear responsible for the outcome." This is an important threat model for AI agents that agents-as-service architectures must enforce.

---

### 7.2 Versioning and Provenance

**REFERENCE** — Versioning tracks how memory records change over time. Provenance tracks where memory records came from.

**Versioning patterns:**
- **Immutable append (MVCC-style):** Each update creates a new version; old versions are preserved with `isCurrent=false`. Enables forensic reconstruction: "what did this agent believe on March 15th?" MemoryHub uses this pattern (per `docs/memory-tree.md`): `isCurrent` boolean + `previous_version` pointer + creation/modification timestamps.
- **Overwrite:** Current state only; no version history. Simple but loses auditability.
- **Soft delete + archive:** Records are never deleted, only marked expired. Bi-temporal tracking (Graphiti) is a generalization of this.

**Provenance:**
- **Source attribution:** Which user, session, or external document originated this memory. MemoryHub's organizational memories carry `source: user memories u47, u102, u203...` provenance branches (per `docs/memory-tree.md`).
- **Confidence scores:** Mem0 and MemoryHub both store confidence floats on records. A memory derived from strong evidence (user explicitly stated something) has a higher confidence than one inferred from weak signal.
- **Rationale branches:** MemoryHub's memory tree stores not just the fact but the reasoning chain that produced it — important for audit ("why did the agent believe this?").

**Relation to the AI Asset Registry:** The provenance model for memory records directly parallels the `docs/knowledge-registry.md` project's metadata model: identity, version, owner, source, lineage, relationships. A memory record in a governed memory service is a specialized AI asset.

---

### 7.3 Audit Trails

**REFERENCE** — Enterprise memory systems require an immutable audit trail: a log of every read, write, update, and delete, with actor identity, timestamp, before-state, and after-state.

**Requirements in regulated environments:**
- EU AI Act (enforcement August 2026): Transparency obligations for high-risk AI systems require documented explanations of AI behavior — audit trails on what information the agent used and when are directly relevant.
- GDPR Article 17 (right to erasure): To fulfill an erasure request, the system must know which memory records contain the requesting user's personal data — requiring provenance + audit trail.
- HIPAA: Audit controls (45 CFR §164.312(b)) require hardware, software, and procedural mechanisms that record and examine activity in information systems containing protected health information.

**MemoryHub status:** Audit trail is designed but not shipped (issue #67, "stub interface" per `docs/SYSTEMS.md`). This is a hard gap for production enterprise use.

**Oracle model:** Per-record scoping fields (user/agent/thread/timestamp) on every record enable per-record erasure and auditing. This is GDPR Article 17 compliant by design.

**SuperLocalMemory (arXiv:2603.02240):** Introduces per-agent provenance and behavioral data isolation in a separate database with GDPR Article 17 erasure support — a research prototype showing the pattern.

**MemOS:** Includes operation auditing for memory access — memory units tagged with access roles and every read/write logged (cited in Acuvity/Gleecus, 2026). Note: MemOS documentation quality varies across cited sources; treat as corroborating evidence, not primary reference.

---

### 7.4 Erasure Primitives

**REFERENCE** — The ability to delete all memory records associated with a specific user, agent, session, or data subject is required for GDPR Article 17 compliance and for operational hygiene (removing stale agents, off-boarded employees, etc.).

**Implementation patterns:**
- **Cascading delete by scope field:** `DELETE WHERE user_id = X` removes all records for a user. Simple but requires the data model to carry user identity on every record.
- **Soft delete + anonymization:** Records are not physically deleted but user identity fields are nulled/anonymized ("right to be forgotten" without losing the fact that something happened). Useful for audit log preservation.
- **Per-record erasure vs. bulk erasure:** Oracle's model supports per-record erasure (any record with a matching scoping field can be individually erased); MemoryHub's model supports scope-level bulk operations.

**SuperLocalMemory's isolated behavioral store pattern:** Stores behavioral data (what actions an agent took) in a separate database from the memory content, enabling erasure of behavioral data without disrupting factual memory. This is an interesting pattern for compliance architectures where action logs (higher privacy sensitivity) and knowledge facts (lower privacy sensitivity) have different retention requirements.

---

### 7.5 Memory Governance vs. Content Safety

**REFERENCE** — A distinct concern from multi-tenancy: preventing dangerous or sensitive information from being stored in memory at all.

**Write-time content filtering (MemoryHub pattern):** Regex scanning for secrets (API keys, passwords, connection strings, private key headers), PII (SSNs, emails, phone numbers, credit card numbers) at write time. Violations result in blocked writes or quarantine depending on configuration. This is a preventive control — it stops sensitive data from entering the memory store in the first place.

**Memory poisoning (adversarial concern, arXiv:2603.02240):** An active research area: agents whose memories can be manipulated by adversarial inputs to alter their behavior. SuperLocalMemory introduces Bayesian trust defense against memory poisoning. This is not yet standard in any production system surveyed, but represents an emerging security concern for multi-agent platforms where agents share memory across trust boundaries.

---

## 8. Cache Optimization Patterns

### 8.1 KV-Cache Prefix Hits

**REFERENCE** — LLM inference using vLLM's Automatic Prefix Caching (APC) stores computed KV (key-value attention) tensors for token prefix blocks in GPU memory. If a new request's prompt starts with the same token prefix as a cached request, those blocks are reused without recomputation — eliminating prefill cost for the shared prefix.

**Block granularity (REFERENCE — from vLLM documentation):** vLLM partitions prompts into fixed-size token blocks (16 tokens by default in most configurations, configurable). KV blocks are indexed by their content hash. Cache matching is strictly prefix-contiguous: a single token difference within a block invalidates that block and all subsequent blocks. The architecturally important constraint is this strict prefix-contiguity requirement, not the specific block size.

**Performance (from llm-d production telemetry, Red Hat Developer, 2025):**
- 87.4% overall cache hit rate on a representative inference workload
- 88% TTFT improvement: 2,850ms cold vs. 340ms warm cache hit (8.4x)
- 70% compute reduction for repeated prompts at 87.4% hit rate
- $336 daily savings per 10-GPU cluster at that hit rate (llm-d benchmark, cited in Red Hat Developer, 2025 — vendor-measured, not independently reproduced)

**Why this is a memory concern:** If 100 concurrent agents receive memory context in a different order every request, each agent pays full prefill cost for its memory block. If memory is returned in a **deterministic, stable order**, all agents sharing the same memory tier pay the prefill cost only once; subsequent agents get the cached prefix nearly free.

---

### 8.2 Deterministic/Epoch-Locked Memory Assembly

**REFERENCE** — MemoryHub SDK v0.5.0 (shipped 2026-04-12) introduced "cache-optimized assembly": memory search results are returned in a stable, deterministic order designed for KV-cache prefix hits, using "epoch locking" — the sort order for a given memory set is locked until the memory set itself changes.

**Sort order design principle (from `research/vllm-cache-optimization.md`):** High-stability, high-weight memories (enterprise/organizational scope — the most likely to be shared across agent sessions) appear first in the assembled context. These are the most valuable to cache because:
1. They are shared by the most agents (maximum cache reuse)
2. They change infrequently (maximum cache hit duration)
3. They represent the highest governance tier (appropriate to front-load for compliance inspection)

**Deterministic hashing in cache-aware systems:** Best practice (ankitbko.github.io, 2025) is to use SHA256 hash or CBOR serialization of the exact prompt prefix for deterministic cache recognition — arbitrary serialization order prevents cache hits. Any variable content (current time, session-specific data) should be placed at the end of the assembled context, not the beginning.

**MemoryHub's published claims** (from README.md — internal research, not independently benchmarked):
- vLLM: 2x throughput, 152x TTFT improvement (derived from llm-d benchmarks, not a controlled MemoryHub end-to-end test; claimed via llm-d precise routing with 8 pods, H100)
- Anthropic: ~90% cost reduction
- OpenAI: ~50% cost reduction
- Gemini: 75–90% cost reduction

**Caveat:** The vLLM throughput and TTFT figures cite llm-d's own published cache-aware routing benchmarks, not a MemoryHub-specific benchmark. The Anthropic/OpenAI/Gemini figures are design targets without a controlled benchmark. These figures are directionally plausible given vLLM APC theory and the llm-d production telemetry above; independent validation against a real RHOAI workload has not been performed and is recommended before productizing this feature with these numbers. (See also open question Q-MH-5 in [03 MemoryHub Deep-Dive](03-memoryhub-deep-dive.md).)

**RHOAI relevance:** This is a novel and potentially high-value pattern for RHOAI specifically — because RHOAI runs vLLM on-cluster and llm-d is a Red Hat-originated project in active development. The combination of memory-layer deterministic assembly + llm-d cache-aware routing is a differentiated performance story that no other memory solution in the survey has implemented end-to-end.

---

## 9. Multi-Agent Memory Coordination

### 9.1 Multi-Agent Memory Architectures

**REFERENCE** — As agents proliferate, the question of how memory is shared, isolated, and coordinated among them becomes the central design problem. The academic taxonomy (TechRxiv: "Memory in LLM-based Multi-agent Systems," December 2025) identifies three placement categories — per-agent hosting, centralized shared memory, and external hosting — but production systems compose across five distinct architectural patterns.

**Pattern 1 — Shared memory pool:** All agents read/write a common store. Strong consistency; simple to reason about; bottlenecks emerge beyond ~5 agents; effective for shared state that all agents need (Mem0 multi-agent blog, 2026). MemoryHub's project-scope and organizational-scope memory are a centralized model with scope-bounded sharing. CrewAI's `memory=True` flag creates a default shared `Memory()` instance that all agents in a crew access — the simplest form of this pattern. The limitation is contention: as agent count grows, concurrent writes to the same scope create conflicts, and retrieval noise accumulates as every agent's output enters the shared pool.

**Pattern 2 — Blackboard architecture:** A central knowledge store ("blackboard") with specialist agents that observe the blackboard state, contribute their expertise, and write results back. Unlike shared memory pools, agents are not assigned tasks by a coordinator — they retain full autonomy and self-select based on the blackboard state. The blackboard pattern has seen a major resurgence for LLM multi-agent systems: a February 2026 arXiv study (arXiv:2510.01285) on LLM-based blackboard systems demonstrated **13–57% relative improvement in end-to-end success** on complex data science tasks and up to a 9% gain on data tasks vs. strong baselines. The pattern excels at problems requiring heterogeneous expertise (e.g., code generation + analysis + verification) where no single agent has full domain coverage. A June 2026 proposal for "Stateful Swarms" (Devansh, Medium) adapts the blackboard pattern specifically for agent memory: specialized agents write provenance-tracked entries to an append-only, typed knowledge base instead of passing volatile conversational context.

**Pattern 3 — Message-passing:** Agents communicate via explicit messages; no shared mutable state. Each agent maintains its own memory; coordination happens through structured message exchanges. This is the A2A protocol's fundamental model — agents discover capabilities via AgentCards and exchange tasks/artifacts without exposing internal memory, prompts, or tools. Clean isolation and clear trust boundaries, but higher coordination overhead: every piece of shared context requires an explicit send/receive cycle. The message-passing pattern is also the natural fit for cross-organizational agent interactions where shared memory would create unacceptable security boundaries.

**Pattern 4 — Hierarchical memory:** Manager agents curate and distribute memory to worker agents. CrewAI's hierarchical process introduces a manager agent that dispatches tasks to subordinates, maintaining the high-level "team memory" while workers record task-specific details. Anthropic's multi-agent research system uses a similar pattern: the orchestrator's memory holds high-level team state; specialist agents record execution details. The manager serves as a memory gateway — filtering, summarizing, and distributing relevant context downward while aggregating results upward. This reduces cross-talk and limits the blast radius of bad memory writes, but creates a single point of failure at the manager layer.

**Pattern 5 — Federated memory:** Distributed memory across multiple autonomous stores with eventual consistency. Each team or deployment maintains its own memory substrate; selected facts are synchronized across stores via replication or event streaming. This is the most complex pattern but scales best for multi-team, multi-region, or multi-cluster deployments. The "Collaborative Memory" framework (Rezazadeh et al., arXiv:2505.18279, May 2025) provides the most rigorous formalization: a two-tier architecture (private + shared memory) with access control encoded as dynamic bipartite graphs linking users, agents, and resources. Federated memory is an emerging pattern in enterprise multi-team deployments; no production-grade implementation was found in the survey, but the MaaS (Memory as a Service) follow-up paper (arXiv:2506.22815, June 2025) proposes service-oriented modules designed explicitly for this use case.

**Hybrid (production standard):** Most production systems compose multiple patterns. A typical enterprise architecture uses hierarchical memory for team coordination (pattern 4), shared memory within teams (pattern 1), and message-passing for cross-team interactions (pattern 3). The academic position paper "Multi-Agent Memory from a Computer Architecture Perspective" (arXiv:2603.10062, March 2026) frames this as a computer architecture problem — analogous to cache hierarchies with L1 (agent-private), L2 (team-shared), and L3 (organizational) tiers.

---

### 9.2 Write Conflict Resolution

**REFERENCE** — When multiple agents write to the same memory scope concurrently, conflicts arise: two agents may update the same fact to different values within a short time window.

**Database-level serialization:** The standard approach is to rely on the underlying database's transaction isolation guarantees. PostgreSQL MVCC handles concurrent writes without corruption; the application layer must decide how to merge conflicting versions.

**Contradiction detection as an alternative to locking:** MemoryHub's `contradiction_reports` pattern decouples conflict detection from conflict resolution. Rather than preventing concurrent writes (which would require distributed locking and hurt throughput), agents independently report contradictions after the fact. A threshold-based curator process resolves them asynchronously. This is a write-optimistic pattern appropriate for an append-heavy memory store.

**The academic survey's recommendation (arXiv:2603.07670):** "Database-style access control lists...are a natural but unexplored solution" for multi-agent write conflict. As of the survey's writing, this remains an open problem without a standardized production solution.

---

### 9.3 Shared vs. Private Memory for Swarm Coherence

**REFERENCE** — For multi-agent systems where agents coordinate toward a common goal (Wes Jackson's "organizational hive-mind" framing), shared memory serves as the implicit coordination mechanism: Agent A writes a decision; Agent B retrieves it without an explicit message.

**Push notification pattern (EXPLORATORY):** MemoryHub includes a planned Pattern E (issue #62) — real-time push notifications to agents when relevant organizational memories are updated. The client-side API exists (`on_memory_updated()`) but the Valkey-backed backend is not yet shipped. AWS AgentCore Memory added streaming notifications for long-term memory updates in March 2026 (managed service only). This pattern enables reactive coordination without polling: agents are notified of relevant memory changes rather than retrieving on a fixed interval.

**Swarm coherence risk:** In large multi-agent deployments, a bad memory write at organizational scope propagates to all agents. The governance gate (enterprise scope requires HITL approval) mitigates the highest-risk case. For organizational scope, MemoryHub relies on the contradiction detection threshold before curator review. Neither is sufficient for adversarial inputs (see Section 7.5).

---

### 9.4 Scope Isolation and Access Control

**REFERENCE** — When Agent A delegates to Agent B, what memory scope does Agent B inherit? This is the "actor chain problem" — the multi-agent equivalent of privilege escalation. The 2025–2026 period has produced multiple competing approaches, none yet standardized.

**The IETF agent authorization landscape (2025–2026):** Multiple IETF drafts address this problem from different angles. **AAuth** (Agentic Authorization, draft-rosenberg-oauth-aauth-00) defines an OAuth 2.1 extension allowing AI agents to obtain access tokens on behalf of users — directly relevant to MCP server authorization. **OIDC-A** (OpenID Connect for Agents, arXiv:2509.25974, September 2025) introduces standardized claims for agent identity, capabilities, trust levels, and delegation chains. OIDC-A tokens carry `agent_capabilities` claims (e.g., `["email:read", "calendar:view"]`), enabling capability-based access control at the token level. **draft-klrc-aiagent-auth** maps existing WIMSE (Workload Identity in Multi-System Environments) and OAuth mechanisms to agent use cases rather than defining new protocols. A separate draft on **Transaction Tokens for Agents** extends the Txn-Token spec to carry actor (agent) and principal (human) context through the service graph. None of these drafts has reached RFC status; the landscape remains fragmented.

**Collaborative Memory framework (arXiv:2505.18279, May 2025):** The most rigorous academic treatment of scope isolation for multi-agent memory. Introduces explicit scope isolation primitives: access control is encoded as bipartite graphs linking users, agents, and resources, with time-varying permissions. Memory fragments carry immutable provenance attributes (contributing agents, accessed resources, timestamps). Read policies project existing memory into filtered views based on current permissions; write policies determine fragment retention and sharing with context-aware transformations. The evaluation across asymmetric collaboration scenarios (e.g., hierarchical business roles where only the Strategy Director can consult all agents) confirmed strict policy adherence — users only accessed agents and resources explicitly permitted.

**CrewAI's hierarchical scope model:** CrewAI provides hierarchical memory isolation with automatic root scoping. When `memory=True`, the crew creates a shared `Memory()` that all agents access by default. Agents can receive a scoped view for private context. The cognitive memory system's five operations (encode, consolidate, recall, extract, forget) respect the scope hierarchy. However, CrewAI's scope model is per-crew, not cross-crew — it does not address the problem of memory sharing between separate crews or teams, which requires the federated pattern (Section 9.1, Pattern 5).

**Kagenti's approach (Red Hat incubation project):** Kagenti addresses the identity dimension of scope isolation via **SPIFFE identity injection**. Each agent pod receives a cryptographic workload identity (e.g., `spiffe://localtest.me/ns/beeai-team/sa/beeai-coordinator`). The SPIFFE identity feeds into Keycloak via RFC 8693 token exchange, producing short-lived JWTs that attest to the workload's identity. Agent Cards are bound to Kubernetes workloads using SPIFFE-derived identity conventions, preventing look-alike agents from impersonating legitimate ones. Mismatches trigger either audit-mode warnings or strict-mode traffic isolation via NetworkPolicy. This approach solves the identity problem at the infrastructure layer — but the memory scope problem (what memory does a SPIFFE-authenticated agent get access to?) remains an application-layer concern that Kagenti does not prescribe (Red Hat Emerging Technologies blog, March 2026; May 2026).

---

### 9.5 Coordination and Consistency

**REFERENCE** — Multi-agent memory coordination requires consistency models borrowed from distributed systems, adapted for the specific characteristics of LLM agent workloads.

**Consistency models applied to agent memory:**
- **Eventual consistency:** Agents tolerate reading stale memory; updates propagate asynchronously. Appropriate for organizational knowledge that changes infrequently (policy documents, product facts). Most current systems operate here implicitly — there is no coordination protocol ensuring agents see the latest memory state.
- **Causal consistency:** If Agent A's memory write causally depends on Agent B's write, all agents see them in that order. Relevant for task chains where output ordering matters. No production agent memory system implements causal consistency explicitly; the concept is from distributed database literature (Lamport clocks, vector clocks).
- **Strong consistency:** All agents see the same memory state at the same logical time. Achievable via database-level serialization (PostgreSQL MVCC) for co-located agents, but prohibitively expensive for distributed or federated memory.

**Conflict resolution strategies:**
- **Last-write-wins (LWW):** Simplest strategy; the most recent timestamp wins. Adequate for low-contention workloads. Risk: silent data loss when concurrent writes are semantically meaningful.
- **Merge:** LLM-mediated merge where a curator agent synthesizes conflicting memory entries. MemoryHub's contradiction detection + curator review is an asynchronous variant of this pattern.
- **Human-in-the-loop:** Conflicts at high-governance scopes (enterprise, organizational) are escalated to human review. MemoryHub's enterprise scope requires HITL approval; Anthropic Dreaming requires human approval before memory reorganization is deployed.

**Pub/sub for memory change notification:** The emerging pattern for reactive coordination. MemoryHub's planned Pattern E (Valkey-backed push notifications, issue #62) and AWS AgentCore Memory's streaming notifications (March 2026) both implement this: agents subscribe to memory scope changes and are notified asynchronously rather than polling. This enables event-driven coordination without shared mutable state.

**Key finding — interagent misalignment:** The MAST failure taxonomy (Cemri et al., "Why Do Multi-Agent LLM Systems Fail?", NeurIPS 2025 Datasets & Benchmarks Track, spotlight paper) analyzed 1,600+ execution traces across seven multi-agent frameworks and found that **36.9% of all multi-agent failures are attributable to inter-agent misalignment** — communication breakdowns, context loss during handoffs, conflicting outputs, and format mismatches. The full breakdown: specification and system design issues account for 41.8%, inter-agent misalignment for 36.9%, and task verification/termination failures for 21.3%. The implication: roughly 79% of multi-agent failures originate in coordination and specification problems, not model capability limitations. Better memory coordination directly addresses the second-largest failure category.

---

### 9.6 Anti-Patterns and Failure Modes

**REFERENCE / ADVERSARIAL** — Multi-agent memory introduces failure modes that do not exist in single-agent systems. These range from emergent coordination failures to active adversarial attacks.

**Memory contamination and cascade propagation:** In multi-agent systems, one agent's outputs become another agent's inputs. If Agent A's memory is poisoned, its outputs may poison Agent B's memory, creating a cascade. A December 2025 simulation by Galileo AI demonstrated that compromising a single agent's memory led to **87% of downstream decision-making being poisoned within 4 hours** (Galileo AI, 2025 — simulation, not a controlled academic study). The cascade occurs because agents trust their own retrieved memories implicitly — there is no external validation mechanism. Men et al. (2025) independently demonstrate contagious jailbreak attacks where malicious instructions spread through shared memory structures.

**MINJA (Memory INJection Attack):** Published at NeurIPS 2025 (Dong et al., arXiv:2503.03704), MINJA demonstrates that attackers can inject malicious records into an agent's memory through query-only interaction — without any direct access to the memory store. The attack uses "bridging steps" (intermediate reasoning that appears benign individually but leads to malicious outcomes) and temporal decoupling (injection in February, damage in April). Across GPT-4 and GPT-4o agents, MINJA achieves an **injection success rate exceeding 95%** and an end-to-end attack success rate above 70%. A follow-on study confirmed these rates generalize to GPT-4o-mini, Gemini-2.0-Flash, and Llama-3.1-8B. Existing defenses (tool contracts, circuit breakers, I/O moderation) fail because they detect malicious actions, not corrupted beliefs. OWASP recognized this threat class by listing "Memory and Context Poisoning" as ASI06 in the 2026 Agentic AI Top 10.

**MemoryGraft (December 2025):** A related attack vector — indirect injection that implants malicious "successful experiences" into an agent's long-term memory. Unlike MINJA's reasoning-chain approach, MemoryGraft exploits the agent's semantic imitation heuristic: the tendency to replicate patterns from retrieved successful tasks. The poisoned memories are indistinguishable from legitimate context because they are structurally valid task completions.

**Groupthink and echo chambers:** Shared memory creates echo chambers when agents reinforce each other's outputs without external validation. If Agent A writes a conclusion to shared memory and Agent B retrieves and cites it as evidence, the conclusion gains unearned credibility. This is the LLM equivalent of circular sourcing. The risk is highest in blackboard architectures (Pattern 2) where agents self-select contributions based on the current blackboard state.

**Information cascading:** Unverified information is amplified through agent chains. An agent's speculative inference, stored as a memory record, is retrieved by downstream agents who treat it as established fact. Without confidence scoring and provenance tracking, the system cannot distinguish between high-confidence observations and low-confidence inferences.

**Context degradation taxonomy:** The State Contamination paper (arXiv:2605.16746, NeurIPS 2026 submission) identifies a distinct failure mode: harmful influence compressed into external agent state (summaries, transcripts) that passes standard toxicity checks while conditioning downstream agents toward unsafe behavior. This "memory laundering" is harder to detect than direct content poisoning because the toxic signal is distributed across otherwise-benign state artifacts.

**Statelessness as an anti-pattern:** OpenAI Swarm (October 2024) is stateless by design — each `run()` call is independent with no built-in memory persistence. While this simplifies debugging and testing, Stanford research (Tran & Kiela, 2026) found that passing information through natural language summaries (the only coordination mechanism available without persistent state) causes **single agents to outperform multi-agent systems under equal token budgets**. The OpenAI Agents SDK (March 2025) is the production successor that adds session memory as a first-class feature, implicitly acknowledging that pure statelessness is not viable for production multi-agent coordination.

---

### 9.7 Enterprise Regulatory Requirements

**REFERENCE** — Multi-agent memory systems operating in regulated environments face specific compliance obligations that constrain architectural choices.

**EU AI Act (enforcement August 2, 2026):** Article 26 imposes deployer obligations for high-risk AI systems including: automatic log retention for at least six months, human oversight mechanisms, and Fundamental Rights Impact Assessments. Article 12 mandates that logging be integrated into core system design — not bolted on after the fact. Audit trails must be structured, tamper-evident (cryptographic measures required), retained, exportable for regulator review, and independently verifiable. Recitals 99 and 100 address multi-agent architectures explicitly: the compliance boundary extends to every agent that performs a high-risk function in a chain. Penalties for non-compliance cap at up to 15M EUR or 3% of worldwide annual turnover for obligation violations. *(Note: a May 2026 provisional Omnibus VII agreement between the Council presidency and Parliament may extend high-risk deadlines to December 2027 for standalone systems, but this has not been formally adopted into law as of June 2026 — enterprises should treat August 2026 as the operative deadline.)*

**NIST AI RMF:** The AI Risk Management Framework 1.0 (January 2023) is voluntary but increasingly referenced in FTC, SEC, and other US agency enforcement guidance. NIST is developing RMF 1.1 addenda and expanded profiles through 2026, including the Cybersecurity Framework Profile for AI (NIST IR 8596, December 2025 preliminary draft) and SP 800-53 Control Overlays for Securing AI Systems (COSAiS). The framework crosswalks to ISO/IEC 42001, meaning NIST-aligned AI governance supports international certification. For multi-agent memory, the relevant NIST guidance centers on the GOVERN and MAP functions: understanding AI context, defining risk tolerances, and establishing governance structures.

**ISO/IEC 42001:** The AI management system standard establishes requirements for responsible AI development and deployment. For memory systems, the standard's requirements on data governance, lifecycle management, and documentation of AI system behavior translate into specific memory architecture constraints: provenance tracking, scope-bounded access control, and auditable memory operations.

**RHOAI implication:** Any RHOAI memory service targeting enterprise customers must treat audit trail infrastructure as a first-class architectural requirement, not an optional add-on. The EU AI Act's August 2026 enforcement date (even if extended by Omnibus VII) makes this the highest-priority regulatory constraint. MemoryHub's audit trail is designed but not shipped (issue #67, "stub interface"); closing this gap is prerequisite for production enterprise use.

---

### 9.8 Implementation Survey

**REFERENCE** — How current frameworks implement multi-agent memory coordination, organized by approach.

| Framework | Memory Architecture | Multi-Agent Pattern | Key Characteristic |
|---|---|---|---|
| **CrewAI** | Cognitive memory with five operations (encode, consolidate, recall, extract, forget). Unified `Memory` class with LLM-driven analysis. Qdrant Edge storage backend. | Shared pool (Pattern 1) within crews; hierarchical (Pattern 4) with manager agents. Per-crew scope isolation. | Most sophisticated write-time intelligence: each `remember()` call runs encoding analysis (scope, categories, importance, contradiction detection). Adds 1–2 LLM calls and ~200–500ms per write. Agents in the same crew share memory but recall differently — a planning agent weights importance while an execution agent weights recency. |
| **LangGraph** | State-based with checkpointing. `Checkpointer` saves graph state snapshots at every super-step. Separate `Store` for cross-thread long-term memory. PostgresSaver for production. | State graph (explicit state machine). Thread-scoped isolation via `thread_id`. | Strongest fault tolerance: if nodes fail mid-step, graph resumes from last checkpoint without re-running successful nodes. The Checkpointer vs. Store distinction is architecturally important — checkpointer state is thread-scoped (vanishes on new thread), Store state persists across threads. |
| **AutoGen/AG2** | GroupChat with shared message history. In-memory by default; no built-in persistence between runs. | Message-passing (Pattern 3) via structured conversation. GroupChatManager selects speakers. | Emergent coordination through multi-agent dialogue — agents negotiate, debate, and self-correct conversationally. Limitation: no state persistence; if the process crashes, all state is lost. Production deployments require external state management. |
| **OpenAI Swarm** | Stateless by design. Context variables exist only within a single `run()` call. No built-in memory, no conversation store, no RAG integration. | Message-passing with handoffs. | Deliberately minimal — an educational framework, not production-grade. The Agents SDK (March 2025) is the supported successor with session memory. Swarm's statelessness is now recognized as an anti-pattern for production multi-agent coordination (see Section 9.6). |
| **A2A v1.0** | No memory specification. Agents are opaque — internal memory, prompts, and tools are not exposed through the protocol. | Message-passing (Pattern 3) via structured task/artifact exchange. AgentCards declare capabilities. | A2A's design philosophy explicitly keeps memory internal to each agent. The protocol supports `extensions` for additional capabilities, but no memory binding extension has been proposed as of v1.0. The gap is recognized by the community. |
| **Kagenti** | No memory abstraction. Focuses on agent deployment, identity, and security. | Infrastructure-layer orchestration. SPIFFE identity injection, Istio Ambient mesh mTLS, A2A discovery. | Solves the identity and network isolation problems that are prerequisites for secure multi-agent memory sharing, but does not prescribe a memory architecture. Works with any A2A-compatible framework (LangGraph, CrewAI, AG2). |

**Key observation:** No current framework provides a complete multi-agent memory solution. CrewAI has the most sophisticated per-crew memory but lacks cross-crew coordination. LangGraph has the strongest persistence and fault tolerance but treats memory as agent-local state, not shared infrastructure. A2A provides the interoperability protocol but explicitly excludes memory. Kagenti provides the identity and security layer but not the memory layer. A production enterprise multi-agent memory architecture requires composing capabilities across multiple layers — which is the opportunity space for a platform-level memory service.

---

## 10. Synthesis: Maturity and Trajectory

**REFERENCE** — The following assessment synthesizes the patterns above into a maturity/trajectory view for RHOAI planning purposes.

### 10.1 Mature and Proven Patterns

These patterns have multiple production implementations, peer-reviewed or independent benchmark validation, and industry convergence. Adopting them carries low technical risk.

| Pattern | Evidence of Maturity |
|---|---|
| **Hybrid search (BM25 + vector + RRF)** | Multiple production implementations (OpenClaw, Mem0, Zep, MemoryHub, Elasticsearch, Weaviate); benchmark across 25K+ QA pairs shows superiority over single-method retrieval (Redis, 2026 — vendor-curated evaluation) |
| **Cross-encoder two-stage reranking** | Production-standard architecture across enterprise search and memory systems; multiple open models (`ms-marco-MiniLM` family) with established quality benchmarks |
| **Threshold-based compaction triggers** | Implemented by Google ADK, OpenAI Responses API, Anthropic SDK; practitioner consensus on 60–70% utilization trigger (Zylos, 2026) |
| **Three-tier memory hierarchy (core/recall/archival)** | Letta/MemGPT since 2023; directly maps to CoALA academic taxonomy; AWS/Google managed memory services both implement two-tier or three-tier variants |
| **Scope-based multi-tenancy (user/project/org)** | Oracle, MemoryHub, Mem0, LangGraph Stores all implement multi-scope isolation; key design elements (scope field on every record, scope-level enforcement) are consistent across implementations |
| **Single-substrate (PostgreSQL + pgvector) for bounded memory** | Multiple production deployments under 50M vectors; pgvector HNSW now competitive with dedicated vector DBs at this scale (MarkTechPost, 2026) |

### 10.2 Emerging and Contested Patterns

These patterns show strong signals but have fewer independent validations, contested tradeoffs, or significant open engineering challenges.

| Pattern | Maturity Status | Key Uncertainty |
|---|---|---|
| **Bi-temporal knowledge graphs (Graphiti-style)** | arXiv paper (2501.13956, peer-reviewed); production in Zep Cloud; OSS Graphiti engine | Self-hosted stack assembly is complex; no turnkey Kubernetes-native deployment |
| **Readable compaction (structured summaries)** | Anthropic Dreaming, Factory.ai, MemoryHub roadmap; Factory.ai evaluation (36K+ messages) | No large-scale independent comparison; artifact tracking remains weak across all methods |
| **Sleep-time consolidation with governance gate** | Anthropic Dreaming (cloud only); MemoryHub roadmap; Letta (no governance gate) | The governance gate model itself is not standardized; human review bottleneck at scale |
| **LLM-based extraction (single-pass)** | Mem0 v2 (April 2026) introduced single-pass; LangMem p95 59s latency indicates async-only | Episodic-to-semantic consolidation quality varies; no standardized quality metric for extraction accuracy |
| **Cache-optimized deterministic assembly** | MemoryHub SDK v0.5.0 (shipped); llm-d APC telemetry (Red Hat, 2025) | No controlled end-to-end benchmark for memory-specific prefix caching; directional but not validated for RHOAI workloads |
| **Dynamic alpha hybrid search** | Described as 2025–2026 frontier in practitioner literature | Not yet a standard feature in open-source retrieval systems; requires labeled data to tune |
| **Memory poisoning defenses** | arXiv:2603.02240 (SuperLocalMemory, research prototype only); MINJA (NeurIPS 2025) demonstrates >95% injection success; OWASP ASI06 (2026) | No production defenses proven effective; existing I/O moderation fails against belief-level attacks; active research area without settled designs |
| **Multi-agent scope isolation** | Collaborative Memory (arXiv:2505.18279, May 2025) with bipartite-graph access control; IETF AAuth/OIDC-A drafts; Kagenti SPIFFE identity injection | No RFC-status standard for agent authorization; IETF landscape fragmented across 4+ competing drafts; scope isolation and memory access remain separate concerns |
| **Blackboard architecture for LLM agents** | arXiv:2510.01285 (February 2026): 13–57% improvement in complex tasks; Stateful Swarms proposal (June 2026) | Limited to research benchmarks; no production-grade open-source blackboard for LLM agent memory |

### 10.3 The Central Design Fork for RHOAI

The most consequential unresolved pattern question for RHOAI is the one flagged as contested in Section 2: **single unified substrate vs. multi-store architecture.** All of the governance patterns in Section 7 are substantially easier to implement on a single substrate (uniform schema, one enforcement layer, one audit sink). All of the graph knowledge patterns in Section 6 are substantially more expressive on a dedicated graph database. The current evidence (MemoryHub Phase 1 retrospective; Oracle's "four access patterns over one substrate" framing; Wes Jackson's FIPS/governance argument) favors a unified substrate for RHOAI at MVP scale, with the understanding that a graph database layer may be warranted if the Agent Knowledge use case (area 1 from `docs/knowledge-review/assets/agent-memory-knowledge.md`) becomes a first-class RHOAI product requirement.

The inspectability of compaction output is the most near-term architectural requirement from regulatory constraints: the EU AI Act enforcement deadline (August 2026) is imminent, GDPR is in effect, and multiple documented customer environments require HIPAA. Opaque compaction is not a viable option for these deployments regardless of its performance advantages.

---

## Sources

### Internal (Repository)

| Source | Type | Path |
|---|---|---|
| Agent Memory & Knowledge working doc | Internal seed document | `docs/knowledge-review/assets/agent-memory-knowledge.md` |
| AI Asset Registry — Core Concepts | Architecture reference | `docs/knowledge-review/architecture/core-concepts.md` |
| Agent Memory Landscape & Definitions | Sibling research doc | `agent-memory/research/01-landscape-and-definitions.md` |
| Agent Memory Solution Survey | Sibling research doc | `agent-memory/research/02-solution-survey.md` |
| MemoryHub Deep-Dive | Sibling research doc | `agent-memory/research/03-memoryhub-deep-dive.md` |
| RHAISTRAT-1345 | Jira Outcome | https://redhat.atlassian.net/browse/RHAISTRAT-1345 |
| MemoryHub repository | Red Hat AI Americas prototype | https://github.com/redhat-ai-americas/memory-hub |
| When Agent Memory Becomes a Platform Concern | Wes Jackson (Red Hat SSA), 2026-05-01 | https://medium.com/@wjackson_63436/when-agent-memory-becomes-a-platform-concern-4b6cd23af47f |

### External — Academic

| Source | URL | Access |
|---|---|---|
| CoALA: Cognitive Architectures for Language Agents (Sumers et al., arXiv:2309.02427) | https://arxiv.org/abs/2309.02427 | Available |
| Generative Agents: Interactive Simulacra of Human Behavior (Park et al., arXiv:2304.03442) | https://arxiv.org/abs/2304.03442 | Available |
| HopRAG: Multi-Hop Reasoning for Logic-Aware Retrieval-Augmented Generation (arXiv:2502.12442) | https://arxiv.org/abs/2502.12442 | Available |
| Memory for Autonomous LLM Agents (Du, arXiv:2603.07670, March 2026) | https://arxiv.org/html/2603.07670v1 | Fetched directly |
| Why Do Multi-Agent LLM Systems Fail? (Cemri et al., NeurIPS 2025 Datasets & Benchmarks, Spotlight) | https://openreview.net/forum?id=wM521FqPvI | Available |
| MINJA: Memory Injection Attacks on LLM Agents via Query-Only Interaction (Dong et al., NeurIPS 2025) | https://arxiv.org/abs/2503.03704 | Available |
| Collaborative Memory: Multi-User Memory Sharing with Dynamic Access Control (Rezazadeh et al., arXiv:2505.18279, May 2025) | https://arxiv.org/abs/2505.18279 | Available |
| Memory as a Service: Rethinking Contextual Memory as Service-Oriented Modules (arXiv:2506.22815, June 2025) | https://arxiv.org/html/2506.22815v1 | Search summary |
| LLM-based Multi-Agent Blackboard System (arXiv:2510.01285, February 2026) | https://arxiv.org/pdf/2510.01285 | Search summary |
| Multi-Agent Memory from a Computer Architecture Perspective (arXiv:2603.10062, March 2026) | https://arxiv.org/abs/2603.10062 | Search summary |
| Memory in LLM-based Multi-agent Systems: Mechanisms, Challenges, and Collective Intelligence (TechRxiv, December 2025) | https://www.researchgate.net/publication/398392208 | Search summary |
| OpenID Connect for Agents (OIDC-A) 1.0 (Nagabhushanaradhya, arXiv:2509.25974, September 2025) | https://arxiv.org/abs/2509.25974 | Available |
| MemoryGraft: Persistent Compromise of LLM Agents via Poisoned Experience Retrieval (arXiv:2512.16962, December 2025) | https://arxiv.org/html/2512.16962v1 | Search summary |
| State Contamination in Memory-Augmented LLM Agents (Wang & Goyal, arXiv:2605.16746, 2026) | https://arxiv.org/pdf/2605.16746 | Search summary |
| Memory Poisoning Attack and Defense on Memory Based LLM-Agents (Sunil et al., arXiv:2601.05504, January 2026) | https://arxiv.org/abs/2601.05504 | Search summary |
| A Survey on the Security of Long-Term Memory in LLM Agents: Toward Mnemonic Sovereignty (arXiv:2604.16548, April 2026) | https://arxiv.org/html/2604.16548v1 | Search summary |
| Graph-Based Agent Memory: Taxonomy, Techniques, Applications (arXiv:2602.05665) | https://arxiv.org/html/2602.05665v1 | Fetched directly |
| Zep: Temporal Knowledge Graph Architecture for Agent Memory (arXiv:2501.13956) | https://arxiv.org/html/2501.13956v1 | Available (fetched in doc 02) |
| SuperLocalMemory: Privacy-Preserving Multi-Agent Memory (arXiv:2603.02240) | https://arxiv.org/abs/2603.02240 | Search summary |
| Externalization in LLM Agents (arXiv:2604.08224) | https://arxiv.org/html/2604.08224v1 | Search result reference |
| Agent Memory Below the Prompt: Persistent Q4 KV Cache (arXiv:2603.04428) | https://arxiv.org/html/2603.04428v1 | Search result reference |

### External — Vendor and Practitioner Technical References

| Source | URL | Access |
|---|---|---|
| Atlan: Agent Memory Architecture Patterns (2026) | https://atlan.com/know/agent-memory-architectures/ | Fetched directly |
| Redis: Long-Term Memory Architectures for AI Agents | https://redis.io/blog/long-term-memory-architectures-ai-agents/ | Fetched directly |
| Factory.ai: Evaluating Context Compression | https://factory.ai/news/evaluating-compression | Fetched directly |
| Mem0: Multi-Agent Memory Systems Design | https://mem0.ai/blog/multi-agent-memory-systems | Fetched directly |
| MarkTechPost: Best Vector Databases in 2026 | https://www.marktechpost.com/2026/05/10/best-vector-databases-in-2026-pricing-scale-limits-and-architecture-tradeoffs-across-nine-leading-systems/ | Fetched directly |
| Neo4j/Graphiti: Knowledge Graph Memory for an Agentic World | https://neo4j.com/blog/developer/graphiti-knowledge-graph-memory/ | Search summary |
| AgentMarketCap: Graph RAG vs Vector RAG for Agent Memory (2026) | https://agentmarketcap.ai/blog/2026/04/07/graph-rag-vs-vector-rag-agent-memory-neo4j-pgvector | Search result reference |
| TianPan.co: Hybrid Search in Production — BM25 Wins on Queries That Matter (2026) | https://tianpan.co/blog/2026-04-12-hybrid-search-production-bm25-dense-embeddings | Fetched directly |
| Red Hat Developer: KV-Cache Aware Routing with llm-d | https://developers.redhat.com/articles/2025/10/07/master-kv-cache-aware-routing-llm-d-efficient-ai-inference | Fetched directly |
| Zylos Research: AI Agent Context Compression Strategies (2026) | https://zylos.ai/research/2026-02-28-ai-agent-context-compression-strategies | Search summary |
| Google ADK: Context Compaction | https://google.github.io/adk-docs/context/compaction/ | Search result reference |
| Microsoft LazyGraphRAG announcement | https://www.microsoft.com/en-us/research/blog/lazygraphrag-setting-a-new-standard-for-quality-and-cost/ | Search summary (cited in doc 02) |
| vLLM Automatic Prefix Caching documentation | https://docs.vllm.ai/en/stable/design/prefix_caching/ | Search result reference |
| Ankitbko: KV-Cache Aware Prompt Engineering (2025) | https://ankitbko.github.io/blog/2025/08/prompt-engineering-kv-cache/ | Search result reference |
| Acuvity: Memory Governance and AI Security | https://acuvity.ai/what-is-memory-governance-why-important-for-ai-security/ | Search result reference |
| CrewAI: How We Built Cognitive Memory for Agentic Systems (2026) | https://blog.crewai.com/how-we-built-cognitive-memory-for-agentic-systems/ | Search summary |
| CrewAI: Memory Concepts Documentation | https://docs.crewai.com/en/concepts/memory | Search summary |
| Kagenti: Zero Trust AI Agents on Kubernetes (Red Hat Emerging Technologies, March 2026) | https://next.redhat.com/2026/03/05/zero-trust-ai-agents-on-kubernetes-what-i-learned-deploying-multi-agent-systems-on-kagenti/ | Search summary |
| Kagenti: Securing Agent-to-Agent Communication (Red Hat Emerging Technologies, May 2026) | https://next.redhat.com/2026/05/13/securing-agent-to-agent-communication/ | Search summary |
| AAuth: Agentic Authorization OAuth 2.1 Extension (IETF draft-rosenberg-oauth-aauth-00) | https://www.ietf.org/archive/id/draft-rosenberg-oauth-aauth-00.html | Search summary |
| AI Agent Authentication and Authorization (IETF draft-klrc-aiagent-auth-01) | https://datatracker.ietf.org/doc/draft-klrc-aiagent-auth/ | Search summary |
| Galileo AI: Memory Poisoning Cascade Simulation (December 2025) | https://dev.to/mkdelta221/87-compromised-in-4-hours-the-memory-poisoning-stat-that-should-terrify-ai-developers-58oc | Secondary source (DEV.to) |
| Stateful Swarms Will Revolutionize Agentic AI (Devansh, Medium, June 2026) | https://machine-learning-made-simple.medium.com/stateful-swarms-will-revolutionize-agentic-ai-3315f7ec2a5c | Search summary |
| EU AI Act: Article 26 Deployer Obligations | https://artificialintelligenceact.eu/article/26/ | Search summary |
| EU AI Act Audit Trail Requirements (Asqav, 2026) | https://www.asqav.com/blog/posts/eu-ai-act-audit-trail-requirements | Search summary |
| NIST AI RMF 2025–2026 Updates (IS Partners, 2026) | https://www.ispartnersllc.com/blog/nist-ai-rmf-2025-2026-updates-what-you-need-to-know-about-the-latest-framework-changes/ | Search summary |
| LangGraph: Persistence Documentation | https://docs.langchain.com/oss/python/langgraph/persistence | Search summary |
| OWASP Agentic Security Initiative Top 10 (2026) | Referenced via arXiv:2604.16548 | Cross-reference |
| O'Reilly Radar: Why Multi-Agent Systems Need Memory Engineering | https://www.oreilly.com/radar/why-multi-agent-systems-need-memory-engineering/ | Search summary |

### Access Notes

The following sources returned HTTP errors; content was obtained via web search summaries:
- `blogs.oracle.com/developers/oracle-ai-agent-memory-a-governed-unified-memory-core-for-enterprise-ai-agents` — HTTP 403. Oracle figures (80-turn token efficiency, LongMemEval 93.8%, quality judgment results) are from the internal seed document `docs/knowledge-review/assets/agent-memory-knowledge.md` and web search summaries. Not directly verified.
- `blogs.oracle.com/developers/comparing-file-systems-and-databases-for-effective-ai-agent-memory-management` — HTTP 403 (search result reference only; not cited for specific claims in this document).
- `zylos.ai/research/2026-02-28-ai-agent-context-compression-strategies` — Search summary; not directly fetched.
- `google.github.io/adk-docs/context/compaction/` — Search result reference only; cited for the compaction trigger model, not specific numbers.
