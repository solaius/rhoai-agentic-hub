---
title: KV-Cache Memory Optimization
description: How KV-cache optimization in vLLM and llm-d relates to agent memory, establishing cache efficiency as a platform differentiator for RHOAI.
source: ai-asset-registry/agent-memory/research/13-kv-cache-optimization.md (as of 2026-07-05)
timestamp: 2026-07-06
review_after: 2026-08-05
---

# KV-Cache Memory Optimization

**Purpose:** Analyze how KV-cache optimization in vLLM and llm-d relates to agent memory, establishing the tight coupling between memory-service context ordering and inference-engine cache efficiency as a platform differentiator for RHOAI.

**Date:** 2026-06-09

**Status:** EXPLORATORY — Phase 2 research. See [RHAISTRAT-1345](https://redhat.atlassian.net/browse/RHAISTRAT-1345).

**Series:** Document 13 of 17 — Agent Memory & Knowledge Research
**Phase 1:** [00](00-executive-summary.md) · [01](01-landscape-and-definitions.md) · [02](02-solution-survey.md) · [03](03-memoryhub-deep-dive.md) · [04](04-technical-patterns.md) · [05](05-standards-and-protocols.md) · [06](06-ogx-memory-primitives.md) · [07](07-taxonomy-and-decomposition.md) · [08](08-rhoai-ocp-alignment.md)
**Phase 2:** [09](09-agent-harness-memory.md) · [10](10-claude-memory-dreaming.md) · [11](11-adversarial-memory.md) · [12](12-benchmarking-evaluation.md) · 13 KV-Cache Optimization (this doc) · [14](14-enterprise-use-cases.md) · [15](15-multi-modal-memory.md) · [16](16-ai-gateway-memory-substrate.md) · [REVIEW-NOTES](REVIEW-NOTES.md)

---

## Contents

1. [KV-Cache Fundamentals](#1-kv-cache-fundamentals)
2. [Prefix Caching: The Highest-Leverage Optimization](#2-prefix-caching-the-highest-leverage-optimization)
3. [vLLM KV-Cache Features](#3-vllm-kv-cache-features)
4. [llm-d: Distributed Cache-Aware Inference](#4-llm-d-distributed-cache-aware-inference)
5. [Memory-Ordering Impact on Cache Hit Rates](#5-memory-ordering-impact-on-cache-hit-rates)
6. [Quantitative Studies and Benchmark Data](#6-quantitative-studies-and-benchmark-data)
7. [Red Hat Differentiator Analysis](#7-red-hat-differentiator-analysis)
8. [Connection to the RFE Roadmap](#8-connection-to-the-rfe-roadmap)
9. [Open Questions](#9-open-questions)
10. [Sources](#10-sources)

---

## 1. KV-Cache Fundamentals

**REFERENCE** — established inference-engine mechanics, not novel claims.

### 1.1 What the KV-cache is

During autoregressive inference, a Transformer model computes Key (K) and Value (V) matrices for every token at every attention layer. These KV pairs encode the model's "understanding" of each token in context. Without caching, the model recomputes all prior KV pairs for every new token generated — a cost that grows quadratically with sequence length. The KV-cache stores previously computed pairs so that each decode step only processes the new token against the cached history.

The memory footprint is significant. For a Llama 70B model at FP16 precision with a 1M-token context, the KV-cache consumes approximately 135 GB — nearly matching the 140 GB of model weights themselves. Above 128K context tokens, KV-cache memory consistently exceeds parameter memory. At 32K+ tokens, the KV-cache accounts for 60-85% of wall-clock time and 70-90% of GPU memory consumption.

This makes the KV-cache the dominant cost variable for any deployment serving long-context or multi-turn workloads — which is exactly the workload profile of persistent agent conversations.

### 1.2 Why it matters for agent memory

Agent memory creates a specific and favorable pattern for KV-cache optimization. Persistent agent conversations produce repeated context prefixes: the system prompt, tool definitions, role instructions, organizational policies, and accumulated conversation history are prepended to every inference call within a session, and much of this content is shared across sessions for the same agent type.

The economics are stark:

| Scenario | Cost per M tokens (Anthropic) | Ratio |
|----------|-------------------------------|-------|
| Uncached input tokens | $3.00 | 1.0x |
| Cached input tokens | $0.30 | 0.1x |
| **Savings on cache hit** | **$2.70** | **10x** |

For a multi-turn agent session with a 20,000-token system prompt (common in complex agent architectures with large tool schemas), every subsequent inference call after the first can skip recomputation of that prefix — if the cache is warm. Over a 10-step agent task, this turns a 10x system-prompt cost into roughly 1x.

### 1.3 Cache hits vs. misses: the cost/latency fork

A cache hit means the inference engine loads pre-computed KV pairs from memory rather than recomputing them from scratch. The impact is two-dimensional:

- **Latency.** Cache hits reduce time-to-first-token (TTFT) by 50-85% depending on prefix length, because the prefill phase (processing the prompt) is the dominant latency contributor for long-context requests.
- **Cost.** Skipping prefill computation directly reduces GPU-hours consumed per request. At provider scale, this compounds: Anthropic charges 10x less for cached tokens; OpenAI offers 50% discounts; Amazon Bedrock reports up to 90% input-cost reduction.

A cache miss means full recomputation — every KV pair regenerated from scratch. In a distributed deployment, misses are the default when load balancers scatter requests across replicas without visibility into cache state. This is the central problem llm-d solves (Section 4).

---

## 2. Prefix Caching: The Highest-Leverage Optimization

**REFERENCE** — widely deployed; quantitative claims cite published benchmarks.

### 2.1 How prefix caching works

Prefix caching operates at the KV-cache block level. When a request arrives, the inference engine divides the prompt into fixed-size blocks (typically 16 tokens each in vLLM) and computes a hash for each block based on the token IDs within that block and the token IDs of the prefix preceding it. If a block with the same hash exists in cache, the engine reuses it directly, skipping the prefill computation for that block.

The critical insight: cache recognition depends on prefix byte sequences. Because autoregressive models process tokens sequentially from front to back, any token change in the prefix causes all KV pairs from the change point onward to invalidate. The cache "breaks" at the first point of divergence. This means two requests sharing a 15,000-token system prompt but differing at token 15,001 will cache-hit on 15,000 tokens and recompute only the remainder. Two requests with identical content but a single differing token at position 100 will cache-miss on everything after position 100.

### 2.2 Cost savings potential

Published benchmarks and production deployments show consistent savings in the 50-90% range:

| Deployment pattern | Achievable hit rate | Cost reduction |
|-------------------|---------------------|----------------|
| Multi-tenant SaaS (shared system prompts) | 60-85% | 5-12x per-call |
| Agent loops (stable tool schemas) | 70-87% | 4-8x per-call |
| Long-document Q&A (stable reference docs) | 75-90% | 6-10x per-call |
| Repository-grounded coding assistants | 60-80% | 3-7x per-call |

Prefix caching is described in the 2026 literature as "almost a free lunch" — it does not change model outputs, adds negligible overhead, and is already deployed by default at OpenAI, Anthropic, Google, and Amazon Bedrock. Every major open-source inference framework (vLLM, SGLang, TensorRT-LLM) ships it.

### 2.3 The distributed scaling problem

In a single-instance deployment, prefix caching works automatically. The challenge emerges at scale: when multiple vLLM replicas serve behind a load balancer, each pod manages its own cache in complete isolation. Standard load balancers — round-robin, least-connections, random — distribute traffic using cache-blind metrics. Related requests scatter across different pods, and the carefully built cache locality disintegrates.

This is not a marginal problem. In a multi-replica deployment with naive load balancing, cache hit rates drop from 80%+ (single instance) to near-zero (distributed), because the probability of a request landing on the same pod that served its prefix predecessor falls to 1/N for N replicas. The cost savings evaporate precisely when they matter most — at scale.

---

## 3. vLLM KV-Cache Features

**REFERENCE** — vLLM is Red Hat's inference engine, shipped in RHOAI via Red Hat AI Inference Server.

### 3.1 PagedAttention

PagedAttention, introduced in the original vLLM paper (Kwon et al., SOSP 2023), is the foundational memory-management technique. It treats GPU memory for the KV-cache like an operating system's virtual memory: fixed-size blocks allocated on demand, freed immediately upon request completion, and mapped through an indirection table that eliminates fragmentation.

Quantitative impact:

- **Memory waste:** Reduced from 60-80% (pre-vLLM systems) to under 4%.
- **Throughput:** 2-4x improvement over FasterTransformer and Orca at the same latency level.
- **Real-world deployment:** LMSYS (Chatbot Arena) cut GPU count by 50% while serving 2-3x more requests per second.
- **Beam search:** Up to 55-66% KV-cache sharing across beams, achieving 2.3x speedup.

PagedAttention is now the substrate for all other KV-cache optimizations. Every production inference stack in 2026 ships it by default.

### 3.2 Automatic Prefix Caching (APC)

vLLM implements prefix caching through a hash-based approach at the block-allocator layer. When a new request arrives, vLLM computes hashes for each KV-cache block based on token IDs, looks up existing blocks with matching hashes, and reuses them directly. APC accelerates the prefill phase specifically — it does not reduce decode time, since decode generates new tokens rather than reprocessing existing ones.

Key design choices:

- **Hash-based lookup** — O(1) block matching, deterministic behavior.
- **Eviction via LRU** — least-recently-used blocks are evicted when GPU memory is full.
- **Cache isolation via `cache_salt`** — optional per-request salting prevents timing-based side-channel attacks in multi-tenant environments. The salt is injected into the hash of the first block, ensuring only requests with the same salt can reuse cached blocks. This is a security primitive relevant to governed multi-tenant agent deployments.

### 3.3 Multi-tier memory hierarchy

vLLM supports hierarchical KV-cache storage across three tiers:

1. **GPU memory** — fastest access, limited capacity.
2. **CPU memory** — larger capacity, higher latency. LMCache integration achieves 3-10x latency reduction versus full recomputation by caching in CPU RAM rather than regenerating from scratch.
3. **Disk / filesystem** — largest capacity, highest latency. The `llmd-fs-connector` (now upstreamed into vLLM as of v0.22) enables filesystem-tier offloading.

This multi-tier architecture is directly analogous to the memory hierarchy in operating systems (L1/L2/L3 cache, RAM, disk) and enables KV-cache capacity to exceed GPU memory bounds. For long-context agent sessions that accumulate significant conversation history, this means the cache can persist across the full session rather than being evicted when GPU memory fills.

### 3.4 KV-cache quantization

vLLM supports quantizing the KV-cache to reduce its memory footprint:

| Format | Memory savings vs. FP16 | Quality impact | Hardware requirement |
|--------|------------------------|----------------|---------------------|
| FP8 (E4M3) | 50% (2x compression) | Minimal for most workloads | Hopper+ (H100) |
| FP8 (E5M2) | 50% (2x compression) | Slightly lower precision | Hopper+ |
| NVFP4 | 75% (4x compression) | Moderate; under evaluation | Blackwell (B200+) |

FP8 quantization is compatible with automatic prefix caching — switching to FP8 changes the values inside the blocks but does not change the hash key computation.

**Accuracy caveat.** Stress tests on Hopper GPUs revealed that the FP8 Flash Attention 3 kernel suffered from accumulation precision loss at long contexts: on a 128K-token needle-in-a-haystack task, FP8 accuracy dropped from 91% (BF16 baseline) to 13%. An accumulation fix in later vLLM releases restores long-context accuracy near the BF16 baseline while preserving the decode-speed advantage. This is a relevant caveat for agent memory workloads that routinely operate at long context lengths.

### 3.5 Combined optimization stack

The 2026 production optimization stack for KV-cache combines five technique families:

| Technique | Function | Impact |
|-----------|----------|--------|
| PagedAttention | Memory management substrate | 2-4x throughput, <4% waste |
| Prefix caching | Reuse KV blocks across requests | 85-95% cost savings on hits |
| GQA / MLA | Attention-layer compression | 7-14x KV compression (MLA) |
| FP8 quantization | Reduce per-block memory | 50% memory reduction |
| Continuous batching | Schedule new requests into running batches | Higher GPU utilization |

These compound multiplicatively. DeepSeek's MLA + FP8 together reduce KV-cache from 135 GB to approximately 8 GB for a 70B model at 1M context — a 17x reduction that makes previously unservable context lengths economically viable.

---

## 4. llm-d: Distributed Cache-Aware Inference

**REFERENCE** — llm-d is a CNCF Sandbox project led by Red Hat.

### 4.1 The problem llm-d solves

As established in Section 2.3, distributed vLLM deployments with naive load balancing destroy cache locality. llm-d solves this by providing cache-aware routing: it creates a global view of the cluster's KV-cache state and routes each request to the pod that already has the most relevant prefix cached.

llm-d was accepted as a CNCF Sandbox project in March 2026. It was co-founded by Red Hat, Google Cloud, IBM Research, CoreWeave, and NVIDIA, with contributions from AMD, Cisco, Hugging Face, Intel, Lambda, Mistral AI, UC Berkeley, and University of Chicago.

### 4.2 Architecture

llm-d is organized around four capabilities:

1. **Intelligent routing** — The Endpoint Picker (EPP), a sidecar component that intercepts every inference request via Envoy's ext-proc callback, scores available pods, and selects the optimal target. The EPP implements the Kubernetes Gateway API Inference Extension (GAIE).

2. **Prefill/decode disaggregation** — Independent scaling of prompt-processing and token-generation phases, addressing the resource-utilization asymmetry between these workload types.

3. **Hierarchical KV-cache offloading** — Multi-tier cache across GPU, TPU, CPU, and storage tiers, extending the single-node vLLM hierarchy to a cluster-wide resource.

4. **Native Kubernetes orchestration** — LeaderWorkerSet (LWS) primitives for multi-node replicas and expert parallelism.

### 4.3 The KV-Cache Indexer and KV-Events

The architectural core of llm-d's cache awareness is the KV-Cache Indexer — a Go library (llm-d-kv-cache) that maintains a near-real-time, globally consistent index of KV-cache block residency across the entire pod fleet.

The data flow:

1. **KV-Events emission** — Each vLLM pod emits structured events (`BlockStored`, `BlockRemoved`) as KV-cache blocks are created or evicted.
2. **Indexer ingestion** — The KV-Cache Indexer subscribes to these events, computes request-space hashes from the token chunks in `BlockStored` events, and maintains a mapping from request keys to pod locations.
3. **Scoring API** — When a new request arrives, the EPP queries the indexer to determine what percentage of the incoming prompt's prefix is cached on each pod.

The scoring pipeline uses multiple weighted signals:

| Scorer | Weight | Function |
|--------|--------|----------|
| `prefix-cache-scorer` | 3 (dominant) | % of prompt prefix already cached on each pod |
| `kv-cache-utilization-scorer` | 2 | GPU VRAM KV-cache utilization per pod |
| `load-aware-scorer` | 1 | Queue depth and active requests |

The prefix-cache-scorer is deliberately weighted highest — eliminating redundant prefill is the single highest-value optimization for tail latency.

**Dual hash-space design.** The indexer handles a subtle architectural challenge: vLLM's internal content-addressing hashes (engine keys) and the indexer's token-derived hashes (request keys) are independent hash spaces. The bridge is built on ingestion — `BlockStored` events carry the token chunk, allowing the indexer to compute the request key and record an engine-key-to-request-key mapping. This enables the eviction path (`BlockRemoved` events carry only the engine key) to look up the corresponding request key for index removal.

Memory overhead for this global index is negligible: the scaling analysis shows a 1,000,000:1 data-to-metadata ratio.

### 4.4 The 57x TTFT improvement

llm-d's precise prefix-cache-aware scheduling mode delivered the headline benchmark result:

| Scheduling mode | P90 TTFT | Throughput (tok/s) |
|----------------|----------|-------------------|
| Random (cache-blind) | >90 seconds | ~4,365 |
| Round-robin (cache-blind) | >90 seconds | ~4,365 |
| Approximate (traffic-pattern prediction) | 31 seconds | ~6,984 |
| **Precise (actual KV block state)** | **0.542 seconds** | **8,730** |

The precise scheduler is:
- **57x faster** than approximate scheduling on P90 TTFT.
- **170x faster** than random scheduling on P90 TTFT.
- **25% higher throughput** than approximate scheduling.
- **2x higher throughput** than cache-blind configurations.

These benchmarks were conducted on 8 pods / 16 H100 GPUs.

The distinction between approximate and precise scheduling is significant. The approximate mode predicts cache state from traffic patterns; the precise mode reads actual KV block residency from vLLM via KV-Events in near-real-time. The 57x gap between them demonstrates that prediction alone is insufficient — actual cache-state visibility is necessary for order-of-magnitude gains.

### 4.5 Production validation

Google's Vertex AI team validated llm-d's cache-aware routing in production:

- For context-heavy coding tasks (Qwen Coder): **TTFT latency reduced by 35%+**.
- For bursty chat workloads (DeepSeek): **P95 tail latency improved by 52%**.
- Prefix cache hit rate: **doubled from 35% to 70%**.

Alibaba Cloud has integrated precise routing into its ACK Gateway with Inference Extension (GIE). DaoCloud adopted llm-d for disaggregated inference with P/D disaggregation and advanced KV-cache architectures for DeepSeek serving.

---

## 5. Memory-Ordering Impact on Cache Hit Rates

**EXPLORATORY** — this section draws a product-design insight from inference-engine mechanics.

### 5.1 The ordering principle

The most important context-engineering insight for agent memory is that **the ordering of content in the context window directly determines KV-cache hit rates**. This is not a vague performance guideline — it is a deterministic consequence of how prefix caching works.

Because prefix caching matches from the first token forward, and any divergence breaks the cache from that point onward:

- **Static content (system prompt, role instructions, tool definitions, organizational policies) must be placed at the beginning of the context window.** This creates a long, stable prefix that caches across all requests for the same agent type.
- **Dynamic content (user queries, session-specific metadata, timestamps, tool results) must be placed at the end.** This confines cache invalidation to the variable tail, preserving the cached prefix.

This ordering is not merely an optimization suggestion — it is a structural requirement for cost-effective inference at scale.

### 5.2 What breaks the cache in production

Published case studies document specific patterns that destroy cache hit rates:

| Anti-pattern | Impact | Fix |
|-------------|--------|-----|
| Timestamp injected into system prompt | Every request creates a unique hash; 0% hit rate | Move timestamps to end of prompt or out of prompt entirely |
| JSON serializer with non-deterministic key ordering | Different key order between requests invalidates prefix | Enforce stable serialization order for tool schemas |
| Tool definitions modified mid-session | Adding/removing a tool invalidates everything downstream | Freeze tool definitions for the session duration |
| Variable metadata at prompt start | Cache breaks at the first token of metadata | Move variable metadata to end of prompt |
| Rewriting historical messages | Prefix changes from the edit point onward | Append new messages; never mutate prior ones |

The OpenAI Codex team explicitly treats prompt structure as "a first-class performance surface": system instructions, tool definitions, sandbox configuration, and environment context are kept identical and consistently ordered between requests to preserve long, stable prompt prefixes. The agent loop appends new messages rather than modifying earlier ones when runtime configurations change mid-conversation.

### 5.3 Quantitative impact of ordering

Published data on the cost impact of prompt ordering:

- One production team reported a **74% cache hit rate and 59% monthly cost reduction** from a single change: moving dynamic content out of the prompt prefix.
- For agent architectures where the system prompt represents 40-60% of total input tokens per session (common with large tool schemas), proper ordering translates to a **30-45% reduction in total inference cost** purely from token layout changes.
- OpenAI's `prompt_cache_key` parameter, which increases routing stickiness for requests with the same prefix, improved one customer's hit rate from **60% to 87%**.

### 5.4 The product design implication

**PROPOSED** — This ordering principle has a direct product implication for RHOAI's memory service: **the context-engineering capability (RFE-M4) must be aware of KV-cache prefix structure and order the assembled context window accordingly.**

The memory service assembles the context window from multiple sources: system prompt, tool definitions, retrieved episodic memories, semantic knowledge, conversation history, and the current user message. The order in which it places these components determines whether the inference engine can reuse its cache. A memory service that naively interleaves dynamic and static content — or that non-deterministically serializes tool schemas — will produce cache miss rates that negate any savings from the underlying inference optimization.

The recommended ordering for an agent memory context window:

```
[1] System prompt (static per agent type)          ← CACHED PREFIX
[2] Tool/skill definitions (stable per session)    ← CACHED PREFIX
[3] Organizational policies (stable per tenant)    ← CACHED PREFIX
[4] Retrieved knowledge (semi-stable per query)    ← PARTIAL CACHE
[5] Episodic memory (session-specific)             ← PARTIAL CACHE
[6] Conversation history (growing per turn)        ← PARTIAL CACHE
[7] Current user message (unique per request)      ← UNCACHED
```

Items 1-3 form the stable prefix that should cache across all requests for the same agent-tenant pair. Items 4-6 grow per session but share a prefix from prior turns. Item 7 is always unique.

### 5.5 The "Don't Break the Cache" study

Lumer et al. (2026, arXiv:2601.06007) provide the first rigorous cross-provider evaluation of prompt caching for agentic workloads. Their findings on the DeepResearch Bench (multi-turn agentic tasks with extensive tool calling):

- Prompt caching reduces API costs by **41-80%** and TTFT by **13-31%** across OpenAI, Anthropic, and Google.
- Strategic cache block control — placing dynamic content at the end, avoiding dynamic function calling, excluding dynamic tool results from the cached prefix — provides **more consistent benefits** than naive full-context caching.
- Naive full-context caching can **paradoxically increase latency** when dynamic tool results invalidate the cache on every call.
- Benefits are universal and linear after the provider caching token minimum (typically 1,024-4,096 tokens), with provider-specific strategy discrepancies.

This study validates the ordering principle: cache-aware prompt engineering is not optional for cost-effective agentic workloads. It is a first-class design concern.

---

## 6. Quantitative Studies and Benchmark Data

**REFERENCE** — published numbers from vendor documentation, academic papers, and production reports.

### 6.1 Inference cost benchmarks (2025-2026)

| Metric | Value | Source |
|--------|-------|--------|
| LLM API price drop (2025-2026) | ~80% (GPT-4-level: $30/M tokens in 2023 to $0.40/M in 2026) | Morph LLM Inference Guide |
| Inference share of total ML cost | 90%+ | IDC / industry estimates |
| Global enterprise AI investment (2025) | $307 billion | IDC |

### 6.2 KV-cache optimization impact

| Optimization | Metric | Improvement | Source |
|-------------|--------|-------------|--------|
| PagedAttention | Memory waste | 60-80% reduced to <4% | vLLM (Kwon et al., 2023) |
| PagedAttention | Throughput | 2-4x vs. FasterTransformer/Orca | vLLM benchmarks |
| Prefix caching (single node) | Cost per request | 85-95% savings on cache hits | vLLM docs, production reports |
| FP8 KV quantization | Memory footprint | 50% reduction vs. FP16 | vLLM FP8 blog (April 2026) |
| MLA (DeepSeek) | KV compression | 7-14x vs. standard attention | DeepSeek papers |
| MLA + FP8 combined | KV memory (70B @ 1M ctx) | 135 GB to ~8 GB (17x) | Engineering analyses |
| LMCache + vLLM | TTFT (128K system prompt, H100) | 11s to 1.5s (7.3x) | LMCache benchmarks |

### 6.3 llm-d distributed scheduling benchmarks

| Configuration | Metric | Value | Source |
|--------------|--------|-------|--------|
| Precise scheduling (8 pods / 16xH100) | P90 TTFT | 0.542s (vs. 31s approximate, >90s random) | llm-d blog |
| Precise scheduling | TTFT mean reduction | 99.5% | llm-d benchmarks |
| Precise scheduling | E2E request latency mean reduction | 39.9% | llm-d benchmarks |
| Precise scheduling | Inter-token latency mean improvement | 10.4% | llm-d benchmarks |
| Precise scheduling | Throughput | 8,730 tok/s (2x vs. cache-blind) | llm-d benchmarks |
| Precise scheduling | Cache hit rate (prefix-heavy workloads) | 87% | llm-d benchmarks |
| Vertex AI production (Qwen Coder) | TTFT | 35%+ reduction | Google Cloud blog |
| Vertex AI production (DeepSeek) | P95 tail latency | 52% improvement | Google Cloud blog |
| Vertex AI production | Cache hit rate | 35% to 70% (doubled) | Google Cloud blog |

### 6.4 Agentic workload caching benchmarks

| Study | Metric | Value | Source |
|-------|--------|-------|--------|
| "Don't Break the Cache" (Lumer et al.) | API cost reduction | 41-80% | arXiv:2601.06007 |
| "Don't Break the Cache" | TTFT improvement | 13-31% | arXiv:2601.06007 |
| ProjectDiscovery (Neo security platform) | Cost reduction | 59% | ProjectDiscovery blog |
| Production team (prompt reordering only) | Cache hit rate | 74% (from near-zero) | AgentMarketCap |
| TensorMesh CacheBlend (non-prefix) | Cache hit rate on agent skills | 63.6-85.0% | TensorMesh blog |
| LMSYS Chatbot Arena | GPU reduction | 50% fewer GPUs, 2-3x more req/s | vLLM paper |

---

## 7. Red Hat Differentiator Analysis

**PROPOSED** — this section argues that the memory-inference coupling is a platform-level differentiator.

### 7.1 The integration gap that only a platform vendor can close

The central thesis: **the tight coupling between the memory service (what goes in the context window) and the inference engine (how the cache handles it) is a cross-layer optimization that only a platform vendor can deliver end-to-end.**

Consider the optimization stack:

1. **Memory service** — decides what memories, knowledge, and context to include, and in what order.
2. **Context engineering** — compacts, retrieves, and assembles the context window.
3. **Inference routing** — selects the vLLM pod with the warmest cache for this prefix.
4. **Inference engine** — processes the request, leveraging cached KV blocks.

In the current industry landscape, these layers are typically built and operated independently:

- Memory startups (Mem0, Zep, Letta) build layers 1-2 but have no control over layers 3-4.
- Inference providers (cloud LLM APIs) optimize layers 3-4 but treat the prompt as an opaque input.
- Agent frameworks (LangGraph, CrewAI) orchestrate the agent loop but delegate both memory and inference.

No single vendor today optimizes across all four layers. A memory service that formats its context window with awareness of the inference engine's cache structure — and an inference router that understands the memory service's context-assembly patterns — can achieve cache hit rates that are structurally unreachable by solutions that treat these as independent concerns.

### 7.2 RHOAI's position

Red Hat is uniquely positioned to close this gap because RHOAI already ships or is actively building every layer:

| Layer | RHOAI component | Status |
|-------|----------------|--------|
| Memory service | OGX memory primitives (Conversations, Vector Stores, Prompts) | RHOAI 3.5 GA (Responses bridge) |
| Context engineering | OGX `/responses/compact`, `context_management` | RHOAI 3.5 GA |
| Inference routing | llm-d EPP with prefix-cache-aware scoring | llm-d 0.6+ (CNCF Sandbox) |
| Inference engine | vLLM with APC, PagedAttention, FP8 | Red Hat AI Inference Server (RHOAI GA) |

The integration path: the memory service (RFE-M2, RFE-M4) orders the context window with awareness of the prefix-caching behavior of the underlying vLLM engine. llm-d's EPP routes the assembled request to the pod with the warmest cache for that prefix. The result is a closed optimization loop:

```
Memory service orders context → stable prefix formed
    → llm-d routes to warm pod → high cache hit rate
        → lower TTFT, lower cost → more agent calls per budget
            → richer agent behavior → better memory utilization
```

This loop does not require any change to the LLM itself — it is pure infrastructure optimization. And it is invisible to the agent developer: the platform handles ordering, routing, and caching automatically. This is the definition of a platform differentiator.

### 7.3 Competitive positioning

No hyperscaler currently offers this integrated optimization:

| Vendor | Memory | Inference routing | Cache-aware ordering? |
|--------|--------|-------------------|----------------------|
| AWS (Bedrock) | Bedrock Memory | Not exposed | No |
| Google (Vertex) | Vertex AI Memory | llm-d-based (via GAIE) | No |
| Azure (OpenAI) | Prompt caching (automatic) | Internal routing | No |
| Anthropic | API-level caching | Internal routing | No |
| RHOAI | OGX memory + MemoryHub governance | llm-d EPP (precise) | **Possible with RFE-M4** |

Google uses llm-d for routing (and validated the 35-70% cache hit rate improvement), but does not expose a governed memory service that optimizes context ordering for cache efficiency. AWS and Azure offer memory features and prompt caching independently but do not integrate them.

The "context-ordering-aware memory service" is greenfield. No one has built it yet. This is RHOAI's whitespace.

### 7.4 The self-hosted advantage

The KV-cache optimization story reinforces the self-hosted value proposition. In a managed API model (OpenAI, Anthropic), the customer has limited control over:

- How the context window is assembled (they can order their prompt, but the provider's system wraps it).
- How inference is routed (the provider's internal routing is opaque).
- What cache state exists (the provider's cache is shared across all customers, with privacy implications).

In a self-hosted RHOAI deployment:

- The memory service controls context assembly end-to-end.
- llm-d's EPP routing is configurable and observable.
- KV-cache state is per-cluster, per-tenant, or per-namespace — with `cache_salt` for additional isolation.
- Cache eviction policies can be tuned for the specific workload.

For enterprises with compliance requirements (HIPAA, GDPR, EU AI Act), the ability to govern the entire memory-to-inference pipeline — including what is cached, where, and for how long — is not a luxury. vLLM's `cache_salt` isolation, combined with RHOAI's namespace-scoped deployment model, provides a privacy-preserving caching architecture that managed APIs cannot match.

---

## 8. Connection to the RFE Roadmap

**PROPOSED** — mapping KV-cache optimization to the memory RFE roadmap defined in [rfe-roadmap.md](/features/agent-memory/strategy/rfe-roadmap.md).

### 8.1 RFE-M4 — Inspectable context-engineering capability

RFE-M4's scope includes "KV-cache-aware ordering" as an explicit capability. This document provides the technical foundation:

- **What "KV-cache-aware ordering" means:** The context-engineering capability must order the assembled context window so that static content forms a stable prefix (Section 5.4). This is not a vague aspiration — it is a specific algorithm: sort context items by volatility (system prompt first, user message last), enforce deterministic serialization of tool schemas, and append rather than mutate prior turns.
- **Why it is a quality metric:** The token efficiency metric proposed for RFE-M4 should include cache hit rate as a component. A context-engineering capability that produces efficient token usage but breaks the cache is not actually efficient — it has shifted cost from token count to recomputation.
- **What "inspectable" means for caching:** The inspectable dimension of RFE-M4 should expose the prefix boundary — the point in the assembled context window where the stable prefix ends and the dynamic tail begins. This enables operators to understand and tune cache behavior.

### 8.2 Cross-RFE implications

| RFE | KV-cache connection |
|-----|-------------------|
| RFE-M1 (OGX memory primitives) | The substrate that produces the memories fed into the context window. OGX's `previous_response_id` chaining naturally creates append-only conversation history, which is prefix-cache-friendly by design. |
| RFE-M2 (Framework-agnostic memory API) | The API must support ordered retrieval — returning memories in a cache-friendly sequence rather than relevance-only ranking. |
| RFE-M3 (Governance & scope layer) | Scope-tier isolation maps to `cache_salt` isolation in vLLM — each scope tier can have its own cache partition, preventing cross-tenant cache inference. |
| RFE-M4 (Context engineering) | Primary RFE for this work. KV-cache-aware ordering is a core capability. |
| RFE-M5 (Memory-over-MCP) | MCP tool definitions are part of the cached prefix. Stable tool schemas are a caching prerequisite. |

### 8.3 Implementation considerations

The KV-cache-aware ordering capability in RFE-M4 should be implemented as a policy-driven ordering layer in the context-engineering subsystem, not hardcoded into the memory substrate. This allows:

- **Configuration per agent type** — different agents may have different ordering requirements based on their tool schemas and memory patterns.
- **Observability** — exposing prefix length, cache hit rate predictions, and ordering decisions as metrics, connecting to the inspectable dimension of RFE-M4.
- **Evolution** — as inference engines add new caching techniques (e.g., SGLang's RadixAttention for branching prompt patterns, or CacheBlend for non-prefix caching), the ordering policy can adapt without changing the memory substrate.

---

## 9. Open Questions

| ID | Question | Dependency |
|----|----------|------------|
| Q-KV-1 | Should the context-engineering capability (RFE-M4) expose prefix-boundary metadata to operators, or should it be fully opaque? | RFE-M4 scope decision |
| Q-KV-2 | How should scope-tier isolation (RFE-M3) map to `cache_salt` partitioning in vLLM? One salt per scope tier? Per agent? Per tenant? | RFE-M3, RHOAI namespace model |
| Q-KV-3 | Should the memory service predict cache hit rates based on ordering decisions and expose them as an observability metric? | RFE-M4, RHOAI monitoring stack |
| Q-KV-4 | Should RHOAI enforce deterministic tool-schema serialization at the platform level (gateway or memory service), or leave it to agent frameworks? | MCP Gateway, RFE-M5 |
| Q-KV-5 | How does multi-tier KV offloading (GPU-CPU-disk) interact with memory retention policies? Should long-term episodic memory map to lower cache tiers? | RFE-M4, llm-d offloading roadmap |
| Q-KV-6 | What is the interaction between compaction (OGX `/responses/compact`) and cache invalidation? Compacting conversation history changes the prefix, but the compacted version should be more cache-friendly for subsequent requests. | RFE-M4, OGX compaction design |

---

## 10. Sources

| # | Source | Type | Date | Key contribution |
|---|--------|------|------|-----------------|
| S1 | [KV-Cache Wins You Can See: From Prefix Caching in vLLM to Distributed Scheduling with llm-d](https://llm-d.ai/blog/kvcache-wins-you-can-see) | Blog (llm-d) | 2026 | End-to-end analysis of prefix caching through distributed scheduling; 87% hit rate, 88% faster TTFT |
| S2 | [Welcome llm-d to the CNCF](https://www.cncf.io/blog/2026/03/24/welcome-llm-d-to-the-cncf-evolving-kubernetes-into-sota-ai-infrastructure/) | Blog (CNCF) | 2026-03-24 | CNCF Sandbox acceptance, founding members, architectural overview |
| S3 | [llm-d: Intelligent Inference at Scale](https://medium.com/@yakovbeder/llm-d-the-inference-scheduler-that-fixes-what-more-gpus-cant-03644ac55504) | Blog (Medium) | 2026 | 57x TTFT improvement, precise vs. approximate scheduling analysis |
| S4 | [Precise Prefix Cache Aware Routing](https://github.com/llm-d/llm-d/blob/main/guides/precise-prefix-cache-aware/README.md) | Docs (GitHub) | 2026 | Benchmark methodology, P90 TTFT 0.542s, throughput 8,730 tok/s |
| S5 | [llm-d officially a CNCF Sandbox project](https://cloud.google.com/blog/products/containers-kubernetes/llm-d-officially-a-cncf-sandbox-project) | Blog (Google Cloud) | 2026 | Vertex AI production validation: 35%+ TTFT reduction, cache hit rate doubled 35% to 70% |
| S6 | [Automatic Prefix Caching — vLLM Documentation](https://docs.vllm.ai/en/stable/design/prefix_caching/) | Docs (vLLM) | 2025-2026 | Hash-based APC design, cache_salt isolation, block-allocator integration |
| S7 | [Quantized KV Cache — vLLM Documentation](https://docs.vllm.ai/en/latest/features/quantization/quantized_kvcache/) | Docs (vLLM) | 2025-2026 | FP8 E4M3/E5M2 quantization, per-attention-head calibration |
| S8 | [The State of FP8 KV-Cache and Attention Quantization in vLLM](https://vllm.ai/blog/2026-04-22-fp8-kvcache) | Blog (vLLM) | 2026-04-22 | FP8 accuracy regression analysis (91% to 13% at 128K), accumulation fix, NVFP4 preview |
| S9 | [KV-Cache Optimization: Memory Efficiency for Production LLMs](https://introl.com/blog/kv-cache-optimization-memory-efficiency-production-llms-guide) | Blog (Introl) | 2026 | Production stack overview: five technique families, 4-40x cost reduction |
| S10 | [KV Cache Optimization for LLMs 2026: Engineering Guide](https://www.digitalapplied.com/blog/kv-cache-optimization-techniques-2026-engineering-guide) | Blog (DigitalApplied) | 2026 | Recommended order of operations, combined optimization impact |
| S11 | [Efficient Memory Management for Large Language Model Serving with PagedAttention](https://arxiv.org/abs/2309.06180) | Paper (arXiv) | 2023 | Original PagedAttention paper; 2-4x throughput, <4% memory waste |
| S12 | [llm-d-kv-cache architecture](https://github.com/llm-d/llm-d-kv-cache/blob/main/docs/architecture.md) | Docs (GitHub) | 2026 | Dual hash-space design, read/write paths, 1M:1 metadata ratio |
| S13 | [Master KV cache aware routing with llm-d](https://developers.redhat.com/articles/2025/10/07/master-kv-cache-aware-routing-llm-d-efficient-ai-inference) | Blog (Red Hat Developer) | 2025-10-07 | Red Hat perspective on llm-d cache-aware routing |
| S14 | [Don't Break the Cache: An Evaluation of Prompt Caching for Long-Horizon Agentic Tasks](https://arxiv.org/abs/2601.06007) | Paper (arXiv) | 2026-01 | First rigorous cross-provider caching evaluation for agentic workloads; 41-80% cost reduction, 13-31% TTFT improvement |
| S15 | [Context Engineering for Complex Agent Systems](https://medium.com/@joycebirkins/context-engineering-for-complex-agent-systems-kv-cache-file-management-prefill-prompts-and-rag-c7e0f3ba2cd3) | Blog (Medium) | 2026 | Context ordering for cache hits, agent cadence mismatch analysis |
| S16 | [Prompt Cache Hit Rate Engineering](https://agentmarketcap.ai/blog/2026/04/11/prompt-cache-hit-rate-engineering-2026) | Blog (AgentMarketCap) | 2026-04-11 | 74% hit rate from prompt reordering; 30-45% cost reduction for agent architectures |
| S17 | [The Inference Tax: How Prefix-Aware Routing Eliminates the Hidden Cost of LLMs at Scale](https://www.digitalocean.com/blog/reduce-llm-inference-costs-prefix-caching) | Blog (DigitalOcean) | 2026 | EPP-based routing at cloud scale, Endpoint Picker architecture |
| S18 | [How We Cut LLM Costs by 59% With Prompt Caching](https://projectdiscovery.io/blog/how-we-cut-llm-cost-with-prompt-caching) | Blog (ProjectDiscovery) | 2025-2026 | Real-world agentic workload (20-40 LLM steps/task): 59% cost reduction |
| S19 | [Achieving 85% Cache Hit Rates for LLM Agents](https://www.tensormesh.ai/blog-posts/agent-skills-caching-cacheblend-llm-cache-hit-rates) | Blog (TensorMesh) | 2026 | CacheBlend non-prefix caching: 63.6-85.0% hit rates on agent skill content |
| S20 | [What is vLLM?](https://www.redhat.com/en/topics/ai/what-is-vllm) | Docs (Red Hat) | 2025-2026 | Red Hat's vLLM strategy, AI Inference Server positioning |
| S21 | [Introducing Red Hat AI Inference Server](https://www.redhat.com/en/blog/red-hat-ai-inference-server-technical-deep-dive) | Blog (Red Hat) | 2025-2026 | Enterprise-ready vLLM, hardened and supported distribution |
| S22 | [What is llm-d?](https://www.redhat.com/en/topics/ai/what-is-llm-d) | Docs (Red Hat) | 2026 | Red Hat perspective on llm-d, "any model, any accelerator, any cloud" |
| S23 | [KV Cache Management and Prefix Caching — DeepWiki](https://deepwiki.com/vllm-project/vllm/3.4-kv-cache-management-and-prefix-caching) | Docs (DeepWiki) | 2026 | vLLM internals: block allocator, evictor, hash computation |
| S24 | [Ceph.io — KV Caching with vLLM, LMCache, and Ceph](https://ceph.io/en/news/blog/2025/vllm-kv-caching/) | Blog (Ceph) | 2025 | Multi-tier caching with distributed storage backend |
| S25 | [llm-d v0.5: Sustaining Performance at Scale](https://llm-d.ai/blog/llm-d-v0.5-sustaining-performance-at-scale) | Blog (llm-d) | 2026 | Hierarchical KV offloading, KV Connector upstream into vLLM, resilient networking |
| S26 | [Prompt Caching 201](https://developers.openai.com/cookbook/examples/prompt_caching_201) | Docs (OpenAI) | 2025-2026 | prompt_cache_key for routing stickiness; 60% to 87% hit rate improvement |
| S27 | [KV Cache Optimization Strategies for Scalable and Efficient LLM Inference](https://arxiv.org/html/2603.20397v1) | Paper (arXiv) | 2026-03 | Survey of five principal optimization directions: eviction, compression, hybrid memory, novel attention, combination strategies |
| S28 | [Predicted-Latency Based Scheduling for LLMs](https://llm-d.ai/blog/predicted-latency-based-scheduling-for-llms) | Blog (llm-d) | 2026 | XGBoost-based latency prediction, real-time retraining on sliding window |
| S29 | [KV Cache Explained: Why It's the Most Important Optimization](https://www.morphllm.com/kv-cache-explained) | Blog (Morph) | 2026 | KV cache as primary cost variable above 128K context |
| S30 | [Agentic Plan Caching: Test-Time Memory for Fast and Cost-Efficient LLM Agents](https://arxiv.org/abs/2506.14852) | Paper (arXiv) | 2026-06 | Plan-level caching for agent workflows, complementary to KV-level caching |

---

*This document is research input for the agent memory strategy. It does not commit RHOAI to any implementation. The connection between memory-service context ordering and inference-engine cache efficiency is a product-design insight that should inform RFE-M4 scope and the broader RHOAI platform strategy.*
