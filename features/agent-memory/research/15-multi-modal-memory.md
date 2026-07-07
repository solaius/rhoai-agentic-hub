---
title: Multi-Modal Memory
description: How agent memory extends beyond text to images, audio, video, and sensor data, and implications for RHOAI's architecture on a 12-24 month horizon.
source: ai-asset-registry/agent-memory/research/15-multi-modal-memory.md (as of 2026-07-05)
timestamp: 2026-07-06
review_after: 2026-08-05
---

# Multi-Modal Memory

**Purpose:** Assess how agent memory extends beyond text to encompass images, audio, video, and sensor data — distinguishing multi-modal memory (persistent recall) from multi-modal input processing (transient inference), mapping the emerging research landscape, and identifying the implications for RHOAI's agent memory architecture on a 12-24 month horizon.

**Date:** 2026-06-09

**Status:** EXPLORATORY — Phase 2 research, forward-looking horizon assessment. Multi-modal memory is a medium-term capability (2027+), not a near-term requirement for RHOAI 3.5 Dev Preview. See [RHAISTRAT-1345](https://redhat.atlassian.net/browse/RHAISTRAT-1345).

**Series:** Document 15 of 17 — Agent Memory & Knowledge Research
**Phase 1:** [00](00-executive-summary.md) · [01](01-landscape-and-definitions.md) · [02](02-solution-survey.md) · [03](03-memoryhub-deep-dive.md) · [04](04-technical-patterns.md) · [05](05-standards-and-protocols.md) · [06](06-ogx-memory-primitives.md) · [07](07-taxonomy-and-decomposition.md) · [08](08-rhoai-ocp-alignment.md)
**Phase 2:** [09](09-agent-harness-memory.md) · [10](10-claude-memory-dreaming.md) · [11](11-adversarial-memory.md) · [12](12-benchmarking-evaluation.md) · [13](13-kv-cache-optimization.md) · [14](14-enterprise-use-cases.md) · 15 Multi-Modal Memory (this doc) · [16](16-ai-gateway-memory-substrate.md) · [REVIEW-NOTES](REVIEW-NOTES.md)

---

## Contents

1. [The Core Distinction: Processing vs. Remembering](#1-the-core-distinction-processing-vs-remembering)
2. [Multi-Modal Embeddings: The Foundation Layer](#2-multi-modal-embeddings-the-foundation-layer)
3. [Current Implementations](#3-current-implementations)
4. [Technical Challenges](#4-technical-challenges)
5. [Benchmarks and Evaluation](#5-benchmarks-and-evaluation)
6. [Enterprise Use Cases](#6-enterprise-use-cases)
7. [Architecture Considerations](#7-architecture-considerations)
8. [RHOAI Implications and Phasing](#8-rhoai-implications-and-phasing)
9. [Sources](#9-sources)

---

## 1. The Core Distinction: Processing vs. Remembering

**EXPLORATORY** — The terms "multi-modal AI" and "multi-modal memory" are frequently conflated. This section establishes the distinction that governs the rest of the document.

### 1.1 Multi-modal input processing

A model that accepts an image and answers a question about it is performing **multi-modal inference** — the image is consumed within the context window, reasoning occurs, and the output is generated. The image is not retained after the session ends. This is the dominant mode of multi-modal AI today: Gemini, GPT-4o, and Claude all process images, audio, and video as *transient inputs*. The model "sees" the image but does not "remember" it.

### 1.2 Multi-modal memory

Multi-modal memory is the capacity to **persist, organize, and retrieve non-text experiences across sessions**. An agent with multi-modal memory can recall what it saw in a previous interaction — a specific chart from a meeting, the tone of a customer's voice, a frame from a surveillance feed — without the original artifact being re-presented in the context window. This requires:

- **Encoding:** Converting raw multi-modal inputs into storable representations (embeddings, captions, structured metadata).
- **Storage:** Persisting those representations with their provenance, temporal context, and cross-modal relationships.
- **Retrieval:** Finding relevant past multi-modal experiences in response to queries that may be in a different modality (e.g., text query retrieving a remembered image).
- **Consolidation:** Compacting, merging, and abstracting multi-modal memories over time to manage storage growth.

### 1.3 Multi-modal RAG vs. multi-modal memory

Multi-modal RAG and multi-modal memory are related but distinct:

| Dimension | Multi-Modal RAG | Multi-Modal Memory |
|---|---|---|
| **Data source** | Pre-existing document corpus (PDFs with images, video archives) | Agent's own experiences and observations |
| **Write pattern** | Batch-indexed at ingest time | Append-heavy, continuous during agent operation |
| **Ownership** | Organization owns the corpus | Agent (or agent-user pair) owns the memories |
| **Temporal context** | Documents have publication dates | Memories have *experienced* timestamps with causal ordering |
| **Scope** | Shared across users/agents | Scoped to agent, user, session, or workspace |

Multi-modal RAG is a **retrieval** capability over a pre-existing multi-modal corpus. Multi-modal memory is an **experiential** capability — the agent builds its own multi-modal knowledge over time. In CoALA terms ([07 Taxonomy & Decomposition](07-taxonomy-and-decomposition.md) §2.2), multi-modal RAG maps to **semantic memory** (world knowledge), while multi-modal memory spans **episodic memory** (past experiences) and **semantic memory** (derived facts). The RHOAI decomposition from [08](08-rhoai-ocp-alignment.md) positions multi-modal RAG as part of Subsystem 3 (Agent Knowledge / Knowledge Sources) and multi-modal memory as part of Subsystem 1 (Agent Memory Substrate).

---

## 2. Multi-Modal Embeddings: The Foundation Layer

**REFERENCE** — Multi-modal embeddings are the enabling technology for both multi-modal RAG and multi-modal memory. They map heterogeneous data types — text, images, audio, video — into a shared vector space where cross-modal similarity search becomes possible.

### 2.1 Foundational models

**CLIP (OpenAI, 2021).** The first model to demonstrate contrastive learning at scale for image-text alignment. Trained on 400M image-text pairs, CLIP produces aligned embeddings for images and text in a shared 512-dimensional space. Zero-shot classification accuracy is competitive with task-specific supervised models. CLIP remains the backbone for over 80% of subsequent multi-modal embedding work, but is limited to two modalities (image + text).

**ImageBind (Meta, 2023).** Extended contrastive alignment to six modalities: images/video, text, audio, depth, thermal, and IMU (inertial measurement unit) data. The key architectural insight is that images serve as a "binding" modality — by pairing images with each other modality and leveraging existing vision-language alignment from CLIP, ImageBind creates a unified six-modality space without requiring all possible modality pairs during training. ImageBind is the foundation model used by Reminisce (Section 3.6) and the default embedding backbone in MemVerse (Section 3.1).

**Amazon Nova Multimodal Embeddings (October 2025).** The first unified commercial embedding model supporting five modalities — text, documents, images, video, and audio — through a single API endpoint. Key capabilities include: Matryoshka representation learning (supporting dimensions of 3072, 1024, 384, and 256 for storage/latency trade-offs), purpose-optimized embeddings (`embeddingPurpose` parameter for retrieval vs. classification), support for video+audio simultaneous embedding, batch inference, and context lengths up to 8,192 tokens with video/audio segments up to 30 seconds. Available via Amazon Bedrock.

**Gemini Embedding 2 (Google, March 2026).** Google's first natively multi-modal embedding model, mapping text, images, video, audio, and documents into a single embedding space. Defaults to 3,072 dimensions with efficient truncation to 1,536 or 768 via Matryoshka representation learning. Supports 200 languages. Represents the shift from "stitching together CLIP for images, Whisper for audio, and a text embedding model" to a single unified encoder.

### 2.2 The three pipeline architectures

The Weaviate multimodal guide and the 2026 state-of-the-art pipeline design literature identify three main approaches for multi-modal retrieval:

1. **Unified embedding space.** Encode all modalities with a single model (CLIP, ImageBind, Nova, Gemini Embedding 2) into one vector space. Simplest to operate; accuracy depends on how well the model aligns modalities. The dominant approach for new systems in 2026.

2. **Bridge to primary modality.** Convert all non-text inputs to text (caption images, transcribe audio, describe video frames), then use a text embedding model. Loses modality-specific nuance but is the most practical and compatible with existing text-only memory infrastructure. This is MemVerse's actual approach for multi-modal input handling (Section 3.1).

3. **Separate stores with cross-modal re-ranking.** Maintain modality-specific embedding stores and use a multi-modal re-ranker at query time to fuse results. Most flexible but operationally complex; suitable for large-scale production systems with heterogeneous data.

### 2.3 Storage implications

Embedding storage scales with dimensionality and vector count:

| Configuration | Storage per 1M vectors | Notes |
|---|---|---|
| 768 dimensions, float32 | ~3 GB | Google-recommended production tier |
| 1,536 dimensions, float32 | ~6 GB | Balance of quality and cost |
| 3,072 dimensions, float32 | ~12 GB | Maximum precision |
| 768 dimensions, int8 quantized | ~0.75 GB | 75% reduction, ~97% of float32 quality |
| Binary quantization (Cohere) | ~0.09 GB | 32x reduction, suitable for coarse filtering |

These are **embedding** storage costs only. Raw multi-modal content — the original images, audio clips, and video segments that the embeddings represent — require separate object storage and introduce dramatically larger footprints (Section 4.1).

---

## 3. Current Implementations

**EXPLORATORY** — The research landscape for multi-modal agent memory has accelerated sharply since late 2025. This section surveys the most significant systems, ordered by publication date.

### 3.1 MemVerse (Shanghai AI Lab, December 2025)

**Architecture.** MemVerse is a model-agnostic, plug-and-play memory framework that integrates three memory components inspired by the human hippocampus:

- **Short-term memory:** Caches recent interaction states to avoid redundant retrieval and continuous long-term storage updates.
- **Long-term memory:** Structured as a multi-modal knowledge graph — heterogeneous signals organized into entity nodes and semantic relationship edges, supporting cross-modal reasoning and retrieval.
- **Parametric memory:** A lightweight neural model periodically distilled from long-term memory, enabling fast, differentiable recall while preserving interpretability.

**Multi-modal approach.** Despite the "multi-modal" label, MemVerse's actual approach to non-text inputs is pragmatic: it employs pre-trained MLLMs to **convert raw data (images, videos, audio) into textual representations** before storage. This is the "bridge to primary modality" pattern (Section 2.2) — multi-modal input, text-only storage. The knowledge graph and retrieval operate over text; the multi-modal capability is in the ingestion pipeline, not the storage layer.

**Performance.** MemVerse-enhanced models achieve 85.48% average accuracy on ScienceQA (GPT-4o-mini + MemVerse), with the highest per-subject scores in natural science (85.26%), social science (81.55%), and language (89.09%).

**Cost.** Requires three LLM calls per ingested item (caption/convert, structure, embed), which is computationally expensive for high-throughput multi-modal streams. Open-source; widely cited as a baseline in subsequent work.

**Source:** [Liu et al. (2025). "MemVerse: Multimodal Memory for Lifelong Learning Agents." arXiv:2512.03627](https://arxiv.org/abs/2512.03627)

### 3.2 TeleMem (China Telecom TeleAI, December 2025)

**Architecture.** TeleMem is a unified long-term and multi-modal memory system that organizes memory as structured, evolvable semantic trajectories. It maintains three types of long-term memory: user profile memory, bot profile memory, and event memory. The writing pipeline batches summaries, retrieves related memories, clusters semantically aligned entries, and performs LLM-based consolidation before persistent storage — assigning each memory item an action (add, delete, update, no-op).

**Multi-modal capabilities.** TeleMem implements a ReAct-style reasoning pipeline for video understanding: video frame extraction, caption generation, vector database construction, and structured storage/retrieval. The system can store, retrieve, and reason over video content using the same memory interface as text memories.

**Performance.** Outperforms the Mem0 baseline by 19% in accuracy on the ZH-4O benchmark while significantly reducing token usage. Positioned as a "high-performance drop-in replacement for Mem0."

**Limitation.** Weaker performance on multi-hop questions, indicating remaining challenges in complex relational reasoning over stored multi-modal memories.

**Source:** [Chen et al. (2025). "TeleMem: Building Long-Term and Multimodal Memory for Agentic AI." arXiv:2601.06037](https://arxiv.org/abs/2601.06037)

### 3.3 M3-Agent (ByteDance Seed, August 2025)

**Architecture.** M3-Agent is the most ambitious multi-modal memory system in the current literature, built around an **entity-centric multi-modal graph** where nodes encapsulate entity attributes acquired through diverse modalities (faces, voices, textual utterances) and edges encode temporal, relational, and semantic connections.

The system operates two parallel processes:

- **Memorization:** Processes video and audio streams online, clip by clip, generating episodic memory for raw content and semantic memory for abstract knowledge (identities, relationships).
- **Control:** Executes instructions by iteratively thinking and retrieving from long-term memory across multiple reasoning rounds.

**Training.** Unlike MemVerse and TeleMem (prompt-engineered), M3-Agent uses **reinforcement learning** to optimize both memorization and control, with separate models trained for each process.

**Benchmark.** M3-Agent introduced **M3-Bench**, comprising 100 real-world robot-perspective videos and 929 web-sourced videos, with question-answer pairs testing human understanding, general knowledge extraction, and cross-modal reasoning. M3-Agent outperforms prompting agents using Gemini-1.5-pro and GPT-4o by 6.7%, 7.7%, and 5.3% on M3-Bench-robot, M3-Bench-web, and Video-MME-long respectively.

**Hardware.** Runs on a single 80 GB A100 or 4x RTX 3090; inference fits in 16 GB VRAM. Apache-2.0 licensed code, CC-BY-4.0 data.

**Source:** [ByteDance Seed et al. (2025). "Seeing, Listening, Remembering, and Reasoning: A Multimodal Agent with Long-Term Memory." arXiv:2508.09736](https://arxiv.org/abs/2508.09736)

### 3.4 Omni-SimpleMem / OmniMem (April 2026)

**Architecture.** OmniMem is the product of an **autonomous research pipeline** (AutoResearchClaw) that started from a text-only memory baseline (SimpleMem, F1=0.117 on LoCoMo) and autonomously executed approximately 50 experiments to discover a multi-modal memory architecture — without human intervention in the inner loop.

The discovered architecture is organized around three principles:

- **Selective ingestion:** Entropy-driven filtering per modality — modality-specific novelty detectors create Memory Atomic Units (MAUs) with LLM-generated summaries and embeddings.
- **Progressive retrieval:** Hybrid FAISS + BM25 search with pyramid token-budget expansion.
- **Knowledge graph augmentation:** Multi-hop cross-modal reasoning via entity extraction with typed entities and relations.

Storage uses a hot/cold split: hot storage for summaries, embeddings, and metadata; cold storage for raw multi-modal content.

**Performance.** State-of-the-art on both benchmarks: **+411% F1 on LoCoMo** (0.117 to 0.598) and **+214% on Mem-Gallery** (0.254 to 0.797). The most impactful discoveries were not hyperparameter adjustments: bug fixes (+175%), architectural changes (+44%), and prompt engineering (+188% on specific categories) each individually exceeded the cumulative contribution of all hyperparameter tuning.

**Significance for RHOAI.** OmniMem's autonomous discovery pipeline demonstrates that multi-modal memory architecture design is itself automatable — the design space is too large and interconnected for manual exploration. This has implications for how Red Hat might approach memory system configuration and optimization at scale.

**Source:** [Liu et al. (2026). "Omni-SimpleMem: Autoresearch-Guided Discovery of Lifelong Multimodal Agent Memory." arXiv:2604.01007](https://arxiv.org/abs/2604.01007)

### 3.5 Supermemory (Commercial, 2025-present)

**Architecture.** Supermemory is the leading commercial multi-modal memory platform, offering a universal memory API built around a custom knowledge graph engine. Key differentiators:

- **Multi-modal extractors:** Supports PDFs, web pages, images, audio, and raw files with automatic extraction pipelines.
- **Dynamic memory:** Unlike static vector databases, memories can merge, contradict, and evolve across sessions. The system handles knowledge updates, contradictions, and expiration automatically.
- **Sub-300ms retrieval** across the full memory graph.
- **Connectors:** Real-time synchronization with Slack, Notion, Drive, Gmail, GitHub, and S3.

**Market position.** Raised $29M across 2 rounds. Claims #1 on LongMemEval, LoCoMo, and ConvoMem benchmarks (self-reported, not independently verified as of late 2025). MCP server and plugins for Claude Code and OpenCode. Pricing from $19/month; self-hosted and air-gapped deployments available for enterprise.

**Relevance.** Supermemory's architecture validates the commercial viability of multi-modal memory as an API service, and its MCP integration model is directly relevant to RHOAI's MCP Registry work.

**Source:** [Supermemory.ai](https://supermemory.ai/) | [GitHub](https://github.com/supermemoryai/supermemory)

### 3.6 Reminisce (Nature Communications, 2025)

**Architecture.** Reminisce is an on-device multi-modal embedding system designed for **resource-constrained mobile devices**. It addresses the fundamental challenge that continuous multi-modal embedding on mobile drains the battery faster than gaming — even when quantized to INT4, ImageBind consumes 1.8x more energy than gaming workloads.

The core design uses **coarse-grained embeddings** built on an early-exit mechanism: embeddings generated by early-exited models (using only the first N transformer layers) serve as coarse filters during storage, while the remaining layers are computed only at query time for candidate refinement. This offloads the expensive computation from the continuous ingestion phase to the less frequent, intent-specific query phase.

**Foundation model.** Built on ImageBind (huge version) as the default multi-modal embedding model, with evaluation also on CLIP.

**Evaluation.** Tested on NVIDIA ORIN, Jetson TX2, Raspberry Pi 4B, and Qualcomm Snapdragon 8Gen3. Achieves high-quality embedding with high throughput while operating silently in the background with negligible memory usage and reduced energy consumption.

**Significance for RHOAI.** Reminisce's coarse-to-fine retrieval pattern and energy-aware design are directly relevant to edge/disconnected agent scenarios on OpenShift at the edge. The early-exit embedding strategy could be adapted for KServe-served embedding models to balance throughput and accuracy.

**Source:** [Cai et al. (2025). "Ubiquitous memory augmentation via mobile multimodal embedding system." Nature Communications, 10.1038/s41467-025-60802-5](https://www.nature.com/articles/s41467-025-60802-5)

### 3.7 Gemini's context-window approach

**Architecture.** Rather than building an explicit multi-modal memory system, Google's approach with Gemini 3.1 Ultra is to extend the context window to **2 million tokens** — approximately 1.5 million words of text, two hours of video, or 22 hours of audio. All modalities share a single attention mechanism; images are tiled into visual tokens, audio is segmented at ~25 frames per second, and video frames are sampled and encoded into the same token stream.

**Trade-offs.** The 2M context window is powerful for single-session, large-scale ingestion tasks (legal review, codebase audits, multi-modal analysis), but it functions as **session-bound short-term memory** — it does not persist across sessions. Explicit memory architectures remain necessary for long-running, multi-session agent workflows. In CoALA terms, Gemini's context window is working memory, not long-term memory.

**Cost.** At Gemini 3.1 Pro pricing ($2 input / $12 output per million tokens), processing 2M tokens of multi-modal context per session creates significant per-interaction costs that scale poorly for continuous agent operation.

**Relevance.** Gemini's approach represents the "just make the context window big enough" alternative to explicit memory. It is effective for bounded tasks but does not solve the persistent, cross-session, scope-governed memory requirements identified in [07 Taxonomy & Decomposition](07-taxonomy-and-decomposition.md) and [08 RHOAI Alignment](08-rhoai-ocp-alignment.md).

---

## 4. Technical Challenges

**EXPLORATORY** — Multi-modal memory introduces challenges that do not exist in text-only memory systems. These challenges are the primary reason multi-modal memory is a medium-term horizon rather than a near-term requirement.

### 4.1 Storage asymmetry

The most fundamental challenge is the dramatic difference in storage requirements across modalities:

| Content Type | Raw Size (typical) | Embedding Size (768d, float32) | Ratio (raw:embedding) |
|---|---|---|---|
| Text snippet (100 words) | ~0.5 KB | 3 KB | 1:6 |
| Image (1080p JPEG) | ~500 KB | 3 KB | 167:1 |
| Audio clip (30 seconds) | ~500 KB (compressed) | 3 KB | 167:1 |
| Video segment (1 minute, 720p) | ~50 MB | 3 KB per frame, ~5,400 KB at 30fps sampling | 9,260:1 |
| 3D scan / point cloud | ~50-500 MB | 3 KB | 16,000:1+ |

For text-only memory, the embedding is often larger than the source text. For video, the raw content is **four orders of magnitude** larger than its embedding. This creates a forced choice:

- **Store embeddings only:** Cross-modal retrieval works, but the original content is lost — the agent "remembers" that it saw something relevant but cannot re-examine the original.
- **Store embeddings + raw content:** Full recall capability, but storage costs escalate rapidly. One hour of video memory at 720p requires approximately 3 GB of raw storage per hour of experience.
- **Store embeddings + compressed summaries:** A middle path — keep the embedding for retrieval and a captioned/transcribed summary for reconstruction, discard the raw content. This is what OmniMem's hot/cold architecture implements.

For enterprise deployments, the hot/cold storage split (embeddings and metadata in vector DB; raw content in object storage) is the pragmatic path. In Kubernetes terms, this maps to vector DB (Milvus/Qdrant) + S3-compatible object storage (MinIO, ODF) — both of which are already available on OpenShift.

### 4.2 Cross-modal retrieval accuracy

Retrieving relevant memories across modalities is harder than within a single modality. A text query like "the chart showing revenue decline" must match an image embedding of a specific chart from a past interaction. Current cross-modal retrieval accuracy depends heavily on:

- **Embedding model quality:** Unified models (Nova, Gemini Embedding 2) outperform bridge-based approaches (caption + text embed) for cross-modal queries, but may underperform modality-specific models for within-modality queries.
- **Modality bias:** CLIP and early models show systematic bias — when text and image documents are in the same index, retrieval skews toward one modality. Newer natively multi-modal models (Gemini Embedding 2, SigLIP-2) train all modalities jointly to reduce this bias.
- **Query-document asymmetry:** The user queries in text; the memories may be images, audio, or video. The embedding model must bridge this asymmetry reliably.

Production recommendations from the 2026 literature: use tiered encoding (full resolution for complex diagrams, thumbnails for decorative images), lazy loading (store references, load raw content only when a chunk makes it into top-k results), and SigLIP-2 for the visual path aligned with a strong text encoder (BGE or E5) through a lightweight projection layer.

### 4.3 Memory compression and compaction

Text memories compact well — multiple text snippets about the same topic can be summarized into a single, shorter text. Multi-modal memories are harder to compact:

- **Image memories:** Multiple images of the same subject can be consolidated if the agent can identify they depict the same entity, but the resulting "summary" is either a new generated image (expensive, lossy) or a text description (loses visual detail).
- **Audio memories:** Temporal alignment matters — the *sequence* of sounds, pauses, and tone shifts carries meaning that a transcript does not capture. Compacting audio memories into text transcripts loses paralinguistic information.
- **Video memories:** The highest compaction challenge. A video memory contains synchronized visual, audio, and temporal streams. OmniMem's approach (selective ingestion with entropy-driven filtering) discards low-novelty frames at ingest time rather than trying to compact after storage.

MemVerse's approach — periodic distillation of long-term memory into a parametric model — is a radical compaction strategy that works for text but has not been demonstrated for raw multi-modal content. M3-Agent's entity-centric graph compacts by extracting structured entity knowledge from multi-modal streams and discarding raw content once entities and relationships are encoded.

### 4.4 Temporal alignment

Multi-modal experiences are temporally synchronized — in a video call, the visual stream (facial expressions), audio stream (words and tone), and text stream (chat messages) all carry meaning in relation to each other's timing. Storing these as independent modality-specific memories loses the temporal alignment that makes them meaningful.

M3-Agent addresses this through its entity-centric graph, where temporal edges connect nodes across modalities. TeleMem uses semantic trajectories to preserve causal ordering. Both approaches add significant complexity to the memory graph compared to text-only episodic memory.

For enterprise use cases (Section 6), temporal alignment is critical in manufacturing (correlating visual defects with sensor readings at the same moment) and healthcare (correlating radiology images with clinical notes from the same examination).

---

## 5. Benchmarks and Evaluation

**REFERENCE** — The multi-modal memory benchmarking landscape has matured rapidly in 2025-2026, moving from ad-hoc evaluation to purpose-built benchmark suites.

### 5.1 M3-Bench (ByteDance, August 2025)

Introduced alongside M3-Agent. Comprises 100 real-world robot-perspective videos (M3-Bench-robot) and 929 web-sourced videos (M3-Bench-web). Tests human understanding, general knowledge extraction, and cross-modal reasoning. The first benchmark specifically designed for multi-modal agent memory rather than multi-modal perception.

### 5.2 Mem-Gallery (January 2026)

Benchmarks multi-modal long-term conversational memory in MLLM agents. Features high-quality multi-session conversations grounded in both visual and textual information, with long interaction horizons and rich multi-modal dependencies. Used as one of OmniMem's two primary evaluation benchmarks (F1: 0.254 baseline to 0.797 with OmniMem).

### 5.3 Video-MME / Video-MME v2 (CVPR 2025 / April 2026)

The industry-standard benchmark for multi-modal video understanding, used by OpenAI (GPT-4.1, GPT-5), Google (Gemini 2.5 Pro, Gemini 3), and others. Covers short (<2 min), medium (4-15 min), and long (30-60 min) videos across 6 visual domains and 30 subfields.

**Video-MME v2** (April 2026) introduces three-level progressive evaluation: Level 1 (multi-point information aggregation), Level 2 (temporal understanding and causal relations), Level 3 (temporal complex reasoning with external priors). Uses a grouped non-linear scoring mechanism — 4 interrelated questions per group testing capability consistency and reasoning coherence. Even the state-of-the-art Gemini-3-Pro shows significant room for improvement across all dimensions.

### 5.4 M3Eval (June 2026)

The first comprehensive evaluation framework specifically for probing **memory dimensions** in multi-modal models, grounded in cognitive psychology. Key findings:

- Models struggle to maintain disentangled representations when processing parallel video streams.
- Interference patterns differ substantially from human memory interference.
- Models ground memory sources more reliably in the spatial domain than the temporal domain.
- Symbolic memory remains limited.

**Source:** [arXiv:2606.05008](https://arxiv.org/abs/2606.05008)

### 5.5 MemEye (May 2026)

A visual-centric evaluation framework noting that long-term agent memory evaluations rarely test whether agents preserve the visual evidence needed for later reasoning. MemEye evaluates memory from two dimensions: the granularity of decisive visual evidence and how retrieved evidence must be used.

### 5.6 Benchmark landscape summary

| Benchmark | Focus | Modalities | Memory-Specific? | Status |
|---|---|---|---|---|
| M3-Bench | Agent memory in real-world video | Video + Audio + Text | Yes | Aug 2025 |
| Mem-Gallery | Long-term conversational memory | Image + Text | Yes | Jan 2026 |
| Video-MME v2 | Video understanding | Video + Audio + Subtitles | Partial (temporal reasoning) | Apr 2026 |
| M3Eval | Cognitive memory dimensions | Video | Yes (first cognitive grounding) | Jun 2026 |
| MemEye | Visual evidence preservation | Image + Text | Yes (visual-centric) | May 2026 |
| BEAM | Ultra-long context | Text (10M tokens) | Yes (scale) | ICLR 2026 |
| LoCoMo | Long conversational memory | Text (+ multi-modal extensions) | Yes | Ongoing |

The trend is clear: memory is now a **first-class evaluation dimension** with its own benchmark suite, distinct from perception and reasoning benchmarks. Multi-modal memory benchmarks specifically are proliferating, reflecting the field's recognition that processing and remembering are fundamentally different capabilities.

---

## 6. Enterprise Use Cases

**EXPLORATORY** — Multi-modal memory enables enterprise use cases that text-only memory cannot address. These are forward-looking — none are in production with full multi-modal memory systems today — but they represent the demand signal that will drive adoption.

### 6.1 Manufacturing visual inspection memory

**Scenario.** A quality inspection agent processes camera feeds from production lines, remembering visual defect patterns across shifts and production runs. When a new defect appears, the agent can recall: "I saw a similar surface irregularity on Line 3 two weeks ago — that batch was later traced to supplier A's material lot #4721."

**Memory requirements.** Episodic memory of visual defect observations, with entity-centric indexing (by part type, defect category, production line, supplier lot). Temporal alignment with sensor data (temperature, pressure, vibration readings at the moment of the defect). Multi-modal retrieval: text query ("surface irregularity similar to last month") returning relevant image memories.

**Current state.** Multi-modal AI is already used for real-time defect detection (perception), but **memory** of past defects for pattern recognition across time remains largely manual (quality engineers maintaining spreadsheets and photo archives). AI-enhanced inspection systems in Industry 4.0 environments are moving toward this capability, particularly with advances in OCT (optical coherence tomography) and AI-driven imaging platforms.

### 6.2 Healthcare radiology with prior scan memory

**Scenario.** A radiology AI assistant examines a chest CT and recalls prior scans of the same patient — not just the radiologist's text report, but the actual imaging features. "Compared to the scan from March 2025, the left lower lobe nodule has increased from 6mm to 9mm. The growth rate is consistent with the pattern I observed in similar cases where follow-up biopsy confirmed malignancy."

**Memory requirements.** Semantic memory of imaging features (nodule size, density, location) extracted from prior scans. Episodic memory of specific patient encounters. Cross-modal retrieval between text (clinical notes) and images (CT/MRI slices). Strict governance: HIPAA/GDPR compliance, patient-scoped access control, audit trails.

**Current state.** Multi-modal AI models that combine radiology images with clinical notes and lab results are improving diagnostic accuracy. AI does not just "see" the image — it reads the doctor's notes and correlates both. MedMemoryBench (2026) benchmarks agent memory in personalized healthcare. CT-Agent, MedRAX, and TheraAgent demonstrate specialized multi-modal reasoning in radiology, but persistent cross-session memory of prior imaging remains a research frontier. The EU AI Act (effective January 2026) classifies medical AI as high-risk, requiring rigorous evaluation of accuracy, explainability, and bias.

### 6.3 Security surveillance pattern memory

**Scenario.** A monitoring agent processes video feeds across a facility, building memory of normal patterns and flagging anomalies: "Vehicle with license plate XYZ-123 has appeared in the loading dock area at 2 AM on three of the last five nights — this is outside normal delivery hours."

**Memory requirements.** Continuous video stream processing with selective ingestion (only novel/anomalous events stored). Entity tracking across sessions (vehicle, person, object identities maintained over time). Temporal pattern detection across days and weeks. Audio correlation (unusual sounds linked to visual events).

### 6.4 Customer support with visual context

**Scenario.** A support agent helping a customer troubleshoot a product remembers: "You sent a photo of the error screen last Tuesday — based on that specific error code and the hardware model visible in your photo, here is the resolution that worked for the three similar cases I have handled this month."

**Memory requirements.** Episodic memory of customer interactions including shared images and screenshots. Cross-customer semantic memory of resolution patterns indexed by visual error signatures. Scope governance: customer-specific memories (private) vs. resolution patterns (shared across the support team).

### 6.5 Common enterprise requirements

Across all four use cases, the common enterprise requirements for multi-modal memory are:

- **Governance.** Scope-tiered access control (who can see which memories), audit trails, data retention/erasure policies, compliance with industry regulations.
- **Provenance.** Every memory must carry its source — when was the original observation made, by which agent, from which sensor/camera/document.
- **Reliability.** Memory retrieval must be deterministic and auditable — "why did the agent recall this particular memory?" must be answerable.
- **Scale.** Enterprise multi-modal memory accumulates rapidly — a single camera feed can generate gigabytes per day of potential memory content, requiring aggressive selective ingestion.

These requirements align directly with the governance and scope framework established in [07 Taxonomy & Decomposition](07-taxonomy-and-decomposition.md) §4 and the AI Asset Registry's "Registry = Governance" principle from [08 RHOAI Alignment](08-rhoai-ocp-alignment.md) §2.1.

---

## 7. Architecture Considerations

**EXPLORATORY** — This section maps multi-modal memory onto the architectural frameworks established in the Phase 1 research.

### 7.1 CoALA taxonomy applied to multi-modal memory

The CoALA framework ([07 Taxonomy & Decomposition](07-taxonomy-and-decomposition.md) §2.2) defines four memory types. Multi-modal memory extends each:

| CoALA Type | Text-Only | Multi-Modal Extension |
|---|---|---|
| **Working memory** | Current conversation context | Current context + active visual/audio/video inputs (Gemini's 2M window) |
| **Episodic memory** | Past interaction transcripts | Past interactions with images, audio recordings, video segments |
| **Semantic memory** | Factual knowledge as text | Factual knowledge including visual references, diagrams, charts, audio examples |
| **Procedural memory** | Code snippets, tool definitions | Demonstrated procedures (video tutorials), physical manipulation sequences |

CoALA explicitly addresses the multi-modal question: "LLMs vs VLMs — should reasoning be language-only or multimodal?" Most current agents use language-only reasoning with a separate captioning model to convert observations to text. Multi-modal models allow interleaved image and text reasoning natively. CoALA's position is that the basic architectural principles — internal memories, structured action space, generalized decision-making — hold regardless of whether the agent reasons in text or multi-modally.

The practical implication for RHOAI: the **memory substrate API** (Subsystem 1 from [08](08-rhoai-ocp-alignment.md)) should be modality-agnostic. Memory operations (store, retrieve, update, delete) should accept any representable content type. The modality-specific complexity belongs in the **ingestion pipeline** (converting raw multi-modal inputs into storable representations) and the **embedding generation service** (computing cross-modal embeddings), not in the memory substrate itself.

### 7.2 Storage backend requirements

Multi-modal memory requires three storage tiers, each with different access patterns:

| Tier | Content | Technology | Access Pattern |
|---|---|---|---|
| **Vector store** | Multi-modal embeddings + metadata | Milvus, Qdrant, pgvector | High-frequency similarity search, sub-100ms latency |
| **Object store** | Raw multi-modal content (images, audio, video) | S3-compatible (MinIO, ODF) | Infrequent access, bulk storage, lifecycle management |
| **Graph store** | Entity relationships, temporal connections, cross-modal links | Neo4j, or embedded in vector store metadata | Graph traversal, multi-hop reasoning, relationship queries |

**Kubernetes-native deployment.** Both Milvus and Qdrant have Kubernetes operators:

- **Milvus Operator:** Manages the full Milvus service stack (Milvus components + etcd, Pulsar, MinIO) via CRDs. Recommended for production at billion-vector scale. Microservices architecture in Go/C++.
- **Qdrant Operator:** Single-binary deployment in Rust. Simpler to operate, faster on filtered queries. API key management, TLS, backup scheduling. Better default for most production RAG pipelines in 2026; reach for Milvus only at very large scale.

The 2026 production guidance: pgvector if you already have PostgreSQL (RHOAI already uses PostgreSQL); Qdrant for dedicated vector workloads at moderate scale; Milvus for billion-vector, distributed deployments. Multi-modal workloads generate vectors fast — indexing a million 15-second video chunks at 3,072 dimensions each produces multi-gigabyte vector indexes.

### 7.3 Embedding generation as a serving workload

Multi-modal embedding generation is a GPU-intensive inference task. In RHOAI terms, it maps to a **KServe InferenceService** — a served model that accepts multi-modal inputs and returns embedding vectors. This is not a new concept; RHOAI already serves models via KServe/vLLM for text generation. Multi-modal embedding models (ImageBind, Nova, Gemini Embedding 2) can be served through the same infrastructure with appropriate model containers.

The key difference from text generation serving: embedding requests are typically **high-throughput, low-latency** (hundreds or thousands of embeddings per second for continuous ingestion) rather than **low-throughput, variable-latency** (conversational interactions). This affects autoscaling configuration, batching strategies, and GPU utilization targets.

Reminisce's early-exit embedding strategy (Section 3.6) is particularly relevant here: a two-tier serving architecture where a smaller model produces coarse embeddings for ingestion (high throughput, low GPU cost) and the full model is invoked only for query-time refinement (lower throughput, higher accuracy). This could be implemented as two KServe InferenceServices with different scaling profiles.

### 7.4 The convert-to-text bridge

Every multi-modal memory system surveyed in Section 3 uses some form of text conversion as part of its pipeline — even systems that store multi-modal embeddings also generate text captions, transcriptions, and descriptions. This is not a limitation to be overcome; it is a pragmatic architectural layer that:

1. **Enables text-only agents** to benefit from multi-modal memories (the agent retrieves a text description of a remembered image).
2. **Provides human-readable audit trails** (governance requires that memories be inspectable by humans, who read text more readily than they interpret embedding vectors).
3. **Supports memory compaction** (text summaries compress multi-modal content by orders of magnitude).
4. **Bridges the gap** between current text-only memory systems and future natively multi-modal systems.

For RHOAI, the convert-to-text bridge is the pragmatic near-term path (Section 8.1). It requires only: (a) multi-modal models served via KServe that can caption images, transcribe audio, and describe video, and (b) the existing text-only memory substrate to store the results. No new memory infrastructure is needed.

---

## 8. RHOAI Implications and Phasing

**PROPOSED** — This section translates the research findings into RHOAI planning guidance. All recommendations are subject to the review gate for agent memory architecture decisions.

### 8.1 Near-term (RHOAI 3.5, 2026): Convert-to-text bridge

**No multi-modal memory infrastructure is needed for 3.5 Dev Preview.** The pragmatic interim path is:

- **Caption images** using served vision-language models (already supported via KServe/vLLM).
- **Transcribe audio** using served speech-to-text models (Whisper variants via KServe).
- **Describe video** using frame-sampling + captioning pipelines.
- **Store the resulting text** in the text-only memory substrate (Subsystem 1 from [08](08-rhoai-ocp-alignment.md)).

This approach matches what MemVerse actually does — "employs pretrained MLLMs to convert raw data into textual representations." It is the dominant approach in production multi-modal memory systems today. The memory substrate API should accept a `content_type` field in memory write operations to record that a memory originated from a non-text source, even though the stored representation is text. This is a low-cost extensibility point.

**Concrete action for 3.5:** Ensure the memory substrate schema includes a `source_modality` metadata field (enum: `text`, `image`, `audio`, `video`, `sensor`, `mixed`) and a `source_reference` field (URI to the original multi-modal content in object storage, if retained). No new infrastructure; just schema foresight.

### 8.2 Medium-term (RHOAI 3.6-4.0, 2027): Multi-modal embedding generation

When the demand signal from enterprise customers justifies native multi-modal memory (rather than the convert-to-text bridge), the key enabler is:

- **Multi-modal embedding models served via KServe.** ImageBind (open-source, six modalities) and open alternatives to Nova/Gemini Embedding 2 can be served as InferenceServices alongside existing text generation models.
- **Vector database integration.** The vector DB backing the memory substrate (pgvector, Qdrant, or Milvus, per [08](08-rhoai-ocp-alignment.md) §2.5) already supports the vector dimensions and index types needed for multi-modal embeddings. No new vector DB infrastructure is required — the same instance stores text embeddings and multi-modal embeddings.
- **Object storage for raw content.** Multi-modal memories that retain raw content (images, audio clips) need S3-compatible object storage alongside the vector DB. OpenShift Data Foundation (ODF) or standalone MinIO provides this. The memory substrate API needs a `raw_content_ref` field linking the embedding record to the object storage location.

**Architecture decision to make before 3.6:** Whether multi-modal embeddings live in the same vector collection as text embeddings (simpler, enables cross-modal search natively) or in separate modality-specific collections with a cross-modal re-ranker (more flexible, avoids modality bias issues). The 2026 literature favors unified collections with natively multi-modal embedding models.

### 8.3 Strategic (2027+): Extensibility for multi-modal memory providers

The AI Asset Registry and MCP Registry architectures should be **extensible** for multi-modal memory providers without requiring redesign:

- **Memory service registration.** The memory service asset type proposed in [08](08-rhoai-ocp-alignment.md) §2.2 should include a `supported_modalities` field in its registry metadata, declaring which modalities the service can store and retrieve. This enables governance tooling to match agents' multi-modal memory requirements with available memory services.
- **MCP tool definitions.** If multi-modal memory is exposed via MCP tools (the memory-as-MCP-tool pattern from [05 Standards & Protocols](05-standards-and-protocols.md) §6), the tool schemas should support multi-modal content parameters. The MCP specification already supports binary content in tool inputs/outputs; memory tools should leverage this.
- **Agent-memory binding.** The agent-memory binding proposed in [08](08-rhoai-ocp-alignment.md) §2.2 (an agent declares which memory service it uses) should include modality requirements: "This agent requires a memory service that supports image and audio modalities." The registry can then validate that the bound memory service satisfies the requirement.

**What this means concretely:** No multi-modal memory service needs to exist in RHOAI 3.5. But the registry schemas, memory substrate API, and agent binding model should include the metadata fields that will be needed when multi-modal memory arrives. The cost of adding these fields now is near-zero; the cost of retrofitting them later is a schema migration across all registered memory services.

### 8.4 Phasing summary

| Phase | Timeframe | Capability | Infrastructure Required | Risk |
|---|---|---|---|---|
| **Convert-to-text** | RHOAI 3.5 (2026) | Multi-modal inputs captioned/transcribed to text, stored in text memory | None new — KServe + existing memory substrate | Low — proven approach, MemVerse baseline |
| **Multi-modal embeddings** | RHOAI 3.6-4.0 (2027) | Native multi-modal embedding storage and cross-modal retrieval | Multi-modal embedding model on KServe + object storage for raw content | Medium — embedding model maturity, storage cost |
| **Full multi-modal memory** | 2027+ | Entity-centric multi-modal graphs, temporal alignment, cross-modal reasoning | Graph database or graph-enhanced vector DB + multi-modal embedding serving + object storage | High — research frontier, no production-proven stack |

---

## 9. Sources

| # | Source | Type | Date | Relevance |
|---|---|---|---|---|
| S1 | [Liu et al. "MemVerse: Multimodal Memory for Lifelong Learning Agents." arXiv:2512.03627](https://arxiv.org/abs/2512.03627) | Research paper | Dec 2025 | Dual-path architecture, text-bridge approach, ScienceQA results |
| S2 | [Chen et al. "TeleMem: Building Long-Term and Multimodal Memory for Agentic AI." arXiv:2601.06037](https://arxiv.org/abs/2601.06037) | Research paper | Dec 2025 | Video memory pipeline, Mem0 drop-in replacement, semantic trajectories |
| S3 | [ByteDance Seed. "Seeing, Listening, Remembering, and Reasoning: A Multimodal Agent with Long-Term Memory." arXiv:2508.09736](https://arxiv.org/abs/2508.09736) | Research paper | Aug 2025 | Entity-centric multi-modal graph, RL-trained, M3-Bench |
| S4 | [Liu et al. "Omni-SimpleMem: Autoresearch-Guided Discovery of Lifelong Multimodal Agent Memory." arXiv:2604.01007](https://arxiv.org/abs/2604.01007) | Research paper | Apr 2026 | Autonomous discovery pipeline, +411% F1 on LoCoMo, hot/cold storage |
| S5 | [Supermemory](https://supermemory.ai/) | Commercial platform | 2025-present | Commercial multi-modal memory API, MCP integration, $29M raised |
| S6 | [Cai et al. "Ubiquitous memory augmentation via mobile multimodal embedding system." Nature Communications](https://www.nature.com/articles/s41467-025-60802-5) | Peer-reviewed journal | 2025 | On-device multi-modal memory, ImageBind, early-exit embeddings, energy-aware |
| S7 | [Amazon Nova Multimodal Embeddings](https://aws.amazon.com/blogs/aws/amazon-nova-multimodal-embeddings-now-available-in-amazon-bedrock/) | Product announcement | Oct 2025 | Five-modality unified embeddings, Matryoshka dimensions, enterprise API |
| S8 | [Google Gemini Embedding 2](https://blog.google/innovation-and-ai/models-and-research/gemini-embedding-2/) | Product announcement | Mar 2026 | Natively multi-modal, 200 languages, 3072/1536/768 dimensions |
| S9 | [Gemini 3.1 Ultra 2M context window](https://codelucky.com/google-gemini-3-1-ultra-2m-token-context-multimodal/) | Technical analysis | 2026 | 2M token multi-modal context, session-bound, pricing implications |
| S10 | [M3Eval. arXiv:2606.05008](https://arxiv.org/abs/2606.05008) | Benchmark paper | Jun 2026 | First cognitive-grounded multi-modal memory benchmark |
| S11 | [Mem-Gallery. arXiv:2601.03515](https://arxiv.org/abs/2601.03515) | Benchmark paper | Jan 2026 | Multi-modal long-term conversational memory benchmark |
| S12 | [Video-MME v2](https://github.com/MME-Benchmarks/Video-MME-v2) | Benchmark | Apr 2026 | Three-level progressive evaluation, industry-standard video benchmark |
| S13 | [Weaviate Multimodal Embeddings and RAG Guide](https://weaviate.io/blog/multimodal-guide) | Technical guide | 2026 | Three pipeline architectures, practical implementation guidance |
| S14 | [Sumers et al. "Cognitive Architectures for Language Agents." arXiv:2309.02427](https://arxiv.org/abs/2309.02427) | Framework paper | 2023 | CoALA taxonomy, memory types, multi-modal reasoning considerations |
| S15 | [Milvus Operator](https://github.com/zilliztech/milvus-operator) | Open-source tool | Ongoing | Kubernetes-native Milvus lifecycle management |
| S16 | [Qdrant on Kubernetes](https://docs.cloud.google.com/kubernetes-engine/docs/tutorials/deploy-qdrant) | Deployment guide | 2026 | StatefulHA operator, multi-AZ deployment, TLS/backup |
| S17 | [Mem0 "State of AI Agent Memory 2026"](https://mem0.ai/blog/state-of-ai-agent-memory-2026) | Industry report | 2026 | Memory as first-class architectural component, benchmark ecosystem |
| S18 | [IBM "What is Multimodal RAG?"](https://www.ibm.com/think/topics/multimodal-rag) | Reference | 2026 | Multi-modal RAG definition and pipeline patterns |
| S19 | [NVIDIA Multimodal RAG Introduction](https://developer.nvidia.com/blog/an-easy-introduction-to-multimodal-retrieval-augmented-generation/) | Technical blog | 2025 | Cross-modal fusion architectures, production patterns |
| S20 | [Pandaily "Shanghai AI Lab Open-Sources MemVerse"](https://pandaily.com/shanghai-ai-lab-open-sources-mem-verse-giving-agents-a-hippocampus-for-multimodal-memory) | News coverage | Dec 2025 | MemVerse context and impact assessment |

---

*This document is a horizon assessment. Multi-modal memory is a research frontier with no production-proven enterprise stack. The recommendations in Section 8 are designed to position RHOAI for multi-modal memory readiness without committing infrastructure investment to unproven technology. The convert-to-text bridge (Section 8.1) is the pragmatic near-term path; native multi-modal memory (Sections 8.2-8.3) should be gated on enterprise customer demand signals and the maturation of multi-modal embedding serving at production scale.*
