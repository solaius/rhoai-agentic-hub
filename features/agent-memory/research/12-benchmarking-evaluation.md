---
title: Benchmarking & Evaluation Framework Design
description: Survey of memory benchmarks, evaluation frameworks, and competitive results, with a proposed Red Hat benchmarking harness design for OpenShift.
source: ai-asset-registry/agent-memory/research/12-benchmarking-evaluation.md (as of 2026-07-05)
timestamp: 2026-07-06
review_after: 2026-08-05
---

# Benchmarking & Evaluation Framework Design

**Purpose:** Comprehensive survey of memory benchmarks, evaluation frameworks, and competitive results, with a proposed Red Hat benchmarking harness design for enterprise-grade agent memory evaluation on OpenShift.

**Date:** 2026-06-09

**Status:** EXPLORATORY — Phase 2 research. See [RHAISTRAT-1345](https://redhat.atlassian.net/browse/RHAISTRAT-1345).

**Series:** Document 12 of 17 — Agent Memory & Knowledge Research
**Phase 1:** [00](00-executive-summary.md) · [01](01-landscape-and-definitions.md) · [02](02-solution-survey.md) · [03](03-memoryhub-deep-dive.md) · [04](04-technical-patterns.md) · [05](05-standards-and-protocols.md) · [06](06-ogx-memory-primitives.md) · [07](07-taxonomy-and-decomposition.md) · [08](08-rhoai-ocp-alignment.md)
**Phase 2:** [09](09-agent-harness-memory.md) · [10](10-claude-memory-dreaming.md) · [11](11-adversarial-memory.md) · 12 Benchmarking & Evaluation (this doc) · [13](13-kv-cache-optimization.md) · [14](14-enterprise-use-cases.md) · [15](15-multi-modal-memory.md) · [16](16-ai-gateway-memory-substrate.md) · [REVIEW-NOTES](REVIEW-NOTES.md)

---

## Contents

1. [Why This Document](#1-why-this-document)
2. [The Academic Benchmark Landscape](#2-the-academic-benchmark-landscape)
3. [Benchmark Dimensions: What Gets Measured](#3-benchmark-dimensions-what-gets-measured)
4. [Competitive Leaderboard Analysis](#4-competitive-leaderboard-analysis)
5. [Evaluation Frameworks (Distinct from Benchmarks)](#5-evaluation-frameworks-distinct-from-benchmarks)
6. [Enterprise-Specific Evaluation Needs](#6-enterprise-specific-evaluation-needs)
7. [Red Hat Benchmarking Harness Design](#7-red-hat-benchmarking-harness-design)
8. [Key Gaps: What No Benchmark Currently Tests](#8-key-gaps-what-no-benchmark-currently-tests)
9. [Recommendations](#9-recommendations)
10. [Sources](#10-sources)

---

## 1. Why This Document

**EXPLORATORY** — Two gaps motivate this research.

**Gap 1 — Benchmarking literacy.** The agent memory benchmarking landscape has exploded since mid-2025. Six major benchmarks were published between ICLR 2025 and ICML 2026, each measuring different abilities at different scales. Vendors cite whichever benchmark favors their architecture, making cross-system comparison unreliable. RHOAI cannot evaluate memory backends — whether OGX-native, MemoryHub-derived, or partner-contributed — without understanding what each benchmark actually measures and where the measurement gaps lie.

**Gap 2 — Enterprise evaluation void.** Every published benchmark evaluates conversational recall accuracy. None evaluates compliance operations (GDPR erasure, HIPAA isolation), governance enforcement (scope boundary violations), multi-tenant isolation, security (memory injection resistance), or production reliability under scale degradation. These are the dimensions that matter most for an enterprise platform. RHOAI needs a benchmarking harness that tests what the academic benchmarks do not.

This document surveys the landscape (Gap 1) and proposes a harness design (Gap 2). It does not commit RHOAI to building a benchmark — the harness design is **PROPOSED** for the review gate. The academic survey sections are **REFERENCE**.

**Relationship to other documents.** The adversarial taxonomy in [11 Adversarial Memory](11-adversarial-memory.md) identifies the threat classes that the security evaluation dimension (Section 6.4) must test. The OGX memory primitives in [06](06-ogx-memory-primitives.md) and the RHOAI alignment in [08](08-rhoai-ocp-alignment.md) establish the backend interfaces that the pluggable backend abstraction (Section 7.2) must wrap. The taxonomy in [07](07-taxonomy-and-decomposition.md) — working/episodic/semantic/procedural memory — defines the capability axes the harness must cover.

---

## 2. The Academic Benchmark Landscape

**REFERENCE** — This section catalogs the seven major benchmarks and one standardization framework published between 2024 and 2026. Each is evaluated on: what it measures, at what scale, with what methodology, and what it misses.

### 2.1 LongMemEval (ICLR 2025) — The De Facto Industry Standard

LongMemEval was the first rigorous, large-scale benchmark purpose-built for long-term interactive memory in chat assistants. Published at ICLR 2025 by Wu et al. (University of Wisconsin-Madison), it established the evaluation methodology that every subsequent benchmark either builds on or responds to.

| Dimension | Detail |
|---|---|
| **Questions** | 500 manually curated |
| **Memory abilities** | 5: information extraction, multi-session reasoning, temporal reasoning, knowledge updates, abstention |
| **Scale variants** | Oracle (gold retrieval), S (~115K tokens), M (~1.5M tokens, 500 sessions) |
| **Evaluation** | Task-averaged accuracy; LLM-judge + exact match |
| **Question types** | single-session-user, single-session-assistant, single-session-preference, temporal-reasoning, knowledge-update, multi-session |

**Design philosophy.** Inspired by needle-in-a-haystack testing, LongMemEval compiles a coherent, length-scalable chat history and embeds evaluation questions that require recalling information hidden across one or more task-oriented dialogues. The pipeline generates increasingly long histories while maintaining narrative coherence — a property that separates it from synthetic concatenation approaches.

**Retrieval baselines.** The benchmark ships with multiple retrieval baselines (BM25, Contriever, Stella V5 1.5B, GTE-Qwen2-7B) supporting turn- and session-level granularity. The authors propose a unified three-stage framework (indexing, retrieval, reading) with optimizations including session decomposition, fact-augmented key expansion, and time-aware query expansion.

**Key findings.** Four long-context LLMs evaluated on LongMemEval-S showed a 30--60% performance decline when reading the full history versus oracle retrieval. Commercial chat assistants achieved only 30--70% accuracy in a simplified setting. This gap established the research agenda for 2025--2026: memory systems are not an optional enhancement but a requirement for sustained interaction.

**Industry adoption.** LongMemEval-S (500 questions, ~115K tokens) has become the primary public leaderboard. Every major memory vendor reports scores on it, making it the closest thing the field has to a standard. Its limitations — moderate scale, conversational-only, no multi-modal elements — drove the creation of BEAM and the domain-specific benchmarks that followed.

### 2.2 BEAM (ICLR 2026) — Production-Scale Evaluation

BEAM ("Beyond a Million Tokens") was published at ICLR 2026 by Tavakoli et al. It is the first and only benchmark that evaluates memory at production-relevant scale (up to 10M tokens), directly testing whether context windows can substitute for memory systems.

| Dimension | Detail |
|---|---|
| **Conversations** | 100 coherent, multi-domain |
| **Questions** | 2,000 human-validated |
| **Memory abilities** | 10: information extraction, multi-hop reasoning, knowledge update, temporal reasoning, summarization, preference following, abstention, contradiction resolution, event ordering, instruction following |
| **Scale tiers** | 128K, 500K, 1M, 10M tokens |
| **Evaluation** | Nugget-based decomposition (fine-grained, not binary correct/incorrect) |

**Novel contributions.** BEAM adds three abilities not tested by LongMemEval: contradiction resolution, event ordering, and instruction following. The nugget-based evaluation decomposes each reference answer into atomic information units, enabling partial credit and more diagnostic failure analysis. For 10M-token conversations, ten interlocking narrative plans form a coherent longer story — a substantial engineering effort to maintain coherence at scale.

**The context-window verdict.** BEAM's central finding is that context windows are not a substitute for memory, even at 1M+ tokens. GPT-4o's 128K window holds ~1.3% of a 10M-token history; Gemini 1.5 Pro's 2M window holds 20%. Models lose coherence and miss information buried in the middle starting at 128K tokens. At 10M tokens — where no baseline natively supports the full context — memory-augmented systems like LIGHT achieve +155.7% accuracy over vanilla Llama-4-Maverick.

**The LIGHT framework.** Alongside the benchmark, the paper proposes LIGHT, a cognitive-inspired framework combining three complementary memory systems: episodic memory (retrieval over conversation), working memory (recent turns), and a scratchpad that accumulates salient facts over time. LIGHT achieves 3.5--12.7% accuracy improvement over strongest baselines across all models.

**Enterprise relevance.** BEAM-10M is the only benchmark that tests memory at enterprise-realistic scale. A production agent deployed for months across thousands of interactions easily accumulates 10M+ tokens. Any RHOAI memory evaluation must include a BEAM-scale tier.

### 2.3 LoCoMo (ACL 2024) — Long-Term Conversational Memory

Published at ACL 2024 by Maharana et al. (UNC Chapel Hill, Snap Research), LoCoMo was the first benchmark targeting very long-term conversational memory specifically. It predates LongMemEval and focuses on a different failure mode: consistency across sessions spanning weeks to months.

| Dimension | Detail |
|---|---|
| **Conversations** | Multi-persona, grounded in temporal event graphs |
| **Turns** | ~600 turns, ~16K tokens per conversation, up to 32 sessions |
| **Tasks** | 3: question answering (5 subtypes), event summarization, multi-modal dialogue generation |
| **QA subtypes** | Single-hop, multi-hop, temporal, open-domain, adversarial (unanswerable) |
| **Construction** | Machine-human pipeline with LLM-based agent architectures + human verification |

**Multi-modal elements.** LoCoMo equips each agent with the capability of sharing and reacting to images within conversations — a unique property among memory benchmarks, though the multi-modal evaluation remains limited.

**The human-LLM gap.** GPT-4 scored 32.1 F1 on LoCoMo's QA task with a 4K context window; humans scored 87.9 F1 — a 56-point gap. Even GPT-3.5 with 16K context reached only 37.8 F1. This gap has narrowed with memory-augmented systems, but LoCoMo remains one of the hardest evaluation sets for temporal and multi-hop reasoning.

**Legacy and influence.** LoCoMo's 1,540 questions across five QA categories have become a second standard evaluation set alongside LongMemEval. It directly prompted innovations in memory-augmented LLMs, retrieval architectures, and neuro-symbolic reasoning. Extensions like TReMu (temporal reasoning) and LoCoMo-V (visual) reflect continuing research interest.

### 2.4 MemoryArena (ICML 2026) — Interdependent Multi-Session Tasks

Published at ICML 2026 by He et al. (Stanford), MemoryArena addresses a fundamental gap in all prior benchmarks: they test memorization and action in isolation. MemoryArena tests them together — agents must learn from earlier actions, distill experiences into memory, and use that memory to guide later actions.

| Dimension | Detail |
|---|---|
| **Task types** | Web navigation, preference-constrained planning, progressive search, sequential formal reasoning |
| **Subtasks** | 4,850 (compositional multi-session design) |
| **Key property** | Causal dependencies across sessions — earlier results determine later task parameters |
| **Construction cost** | ~$60K; 8--10 hours per math/physics task by senior PhDs |

**Why it matters.** MemoryArena is the first benchmark to evaluate whether memory improves downstream task execution, not just recall accuracy. This is the dimension that matters most for production agents: a customer support agent that recalls a previous conversation but fails to apply that context to the current interaction has accurate memory and broken behavior.

**Key findings.** All state-of-the-art methods achieve low Task Success Rates. Agents show clear performance decay as subtask interdependencies span more sessions, suggesting "belief drift" and error accumulation. Critically, augmenting strong long-context models with external memory or RAG does not consistently improve performance — attributed to representation and training mismatches.

**Enterprise relevance.** MemoryArena's interdependent-task design maps directly to enterprise workflows: multi-step approval processes, progressive document assembly, iterative design reviews. Its findings that RAG augmentation does not automatically help are a caution flag for the "just add a vector store" approach.

### 2.5 MemoryAgentBench (ICLR 2026) — Four Competencies Including Selective Forgetting

Published at ICLR 2026 by Hu et al. (UC San Diego), MemoryAgentBench introduces a critical evaluation dimension missing from all prior work: selective forgetting — the ability to recognize when previously stored information has been superseded and to stop using it.

| Dimension | Detail |
|---|---|
| **Competencies** | 4: accurate retrieval, test-time learning, long-range understanding, selective forgetting |
| **Novel datasets** | EventQA (accurate retrieval), FactConsolidation (selective forgetting) |
| **Design** | Incremental multi-turn interactions; existing long-context datasets restructured as dialogue chunks |

**The selective forgetting gap.** All existing methods show significant limitations in selective forgetting, particularly in multi-hop scenarios where accuracy drops to as low as 7%. While long-context agents show reasonable performance on single-hop forgetting (recognizing that a single fact has changed), the challenge of dynamically updating and resolving contradictory information over long sequences remains largely unsolved.

**Architecture-specific insights.** RAG methods dominate accurate retrieval but fail at test-time learning and long-range understanding. Long-context models excel at learning and understanding but struggle with forgetting. No method masters all four competencies — the benchmark reveals a fundamental tension in memory architecture design.

**Enterprise relevance.** Selective forgetting is a compliance requirement, not just a capability gap. GDPR Article 17 (right to erasure) and HIPAA minimum necessary rules both require that outdated or deleted information stops influencing agent behavior. MemoryAgentBench's FactConsolidation dataset is the closest any benchmark comes to testing this, though it tests information supersession rather than commanded deletion.

### 2.6 AMA-Bench (ICLR 2026 Workshop) — Long-Horizon Agentic Memory

Published at the ICLR 2026 Memory Agent Workshop by Zhao et al., AMA-Bench ("Agent Memory with Any length") fills a specific gap: it evaluates memory over real agentic trajectories — agent-environment interaction streams — rather than human-agent conversations.

| Dimension | Detail |
|---|---|
| **Trajectory types** | Real-world (6 domains: web navigation, software engineering, etc.) + synthetic (arbitrary length) |
| **QA pairs** | Expert-curated (real) + rule-based (synthetic) |
| **Key differentiator** | Machine-generated representation streams, not human conversation |

**Why conversations are not enough.** Prior benchmarks assume memory content is human-authored dialogue. In production, agent memory is overwhelmingly machine-generated: tool call results, API responses, environment observations, execution traces. AMA-Bench's real-world trajectories come from actual agent runs, testing whether memory systems can handle the format, density, and causal structure of machine-generated data.

**The causality finding.** Existing memory systems underperform on AMA-Bench primarily because they lack causality and objective information and are constrained by lossy similarity-based retrieval. The proposed AMA-Agent solution builds a Causality Graph — parsing actions and observations into nodes and edges representing causal links — achieving 57.22% average accuracy versus 46.06% for the next-best baseline.

### 2.7 Memora — Forgetting-Aware Memory Accuracy

Published April 2026 (arXiv:2604.20006), Memora introduces the FAMA (Forgetting-Aware Memory Accuracy) metric — the first evaluation metric that explicitly accounts for invalid memories.

| Dimension | Detail |
|---|---|
| **Conversations** | Multi-session spanning weeks to months |
| **Tasks** | 3: remembering, reasoning, recommending |
| **Scale variants** | Weekly, monthly, quarterly durations |
| **Novel metric** | FAMA: penalizes reliance on obsolete/deleted memory |

**Why FAMA matters.** Existing evaluations reward memory inclusion — measuring whether relevant information appears in a model's response. This overlooks memory misuse, where obsolete information is retrieved and used. As long as the final answer appears correct, reliance on invalidated memory is not penalized. FAMA closes this gap by rewarding correct use of valid memory and penalizing reliance on obsolete or deleted memory.

**Key finding.** Evaluations of four LLMs and six memory agents reveal frequent reuse of invalid memories and failures to reconcile evolving memories — a finding that aligns with MemoryAgentBench's selective forgetting results and reinforces the concern that current memory systems lack first-class mutation and consolidation.

**Enterprise relevance.** FAMA is the metric closest to what an enterprise compliance evaluation needs. If an employee's access is revoked, a customer relationship changes, or a policy is updated, the agent must not only stop retrieving the old fact but must not use it even if it appears in retrieved context. FAMA measures exactly this failure mode.

### 2.8 MemEval (Prosus) — Standardized Cross-System Comparison

Published March 2026 by Prosus AI, MemEval is not a benchmark in the traditional sense — it is a standardization framework that enables fair comparison across memory systems.

**The comparability problem.** On the LoCoMo dataset, judge accuracy ranges from 58% to 92% across different evaluations. The variation is not purely because some systems are better — each evaluation uses different LLMs, different embedding models, different token budgets, and different scoring methods. The numbers are not measuring the same thing.

**What MemEval standardizes.** Same LLM, same embedding model, same scoring method across every system. The framework evaluated 9 memory systems across two benchmark datasets (LoCoMo and LongMemEval) under identical conditions, also tracking token efficiency.

**PropMem.** While benchmarking, the Prosus team identified recurring failure modes across all tested systems, leading them to build PropMem — a factual memory system designed around those failure modes. This exemplifies the virtuous cycle between evaluation and architecture improvement.

**Practical value.** MemEval is open source (ProsusAI/MemEval on GitHub). Adding a new memory system requires one adapter function. For RHOAI, MemEval's standardization approach is directly applicable to the pluggable backend abstraction proposed in Section 7.2.

---

## 3. Benchmark Dimensions: What Gets Measured

**REFERENCE** — The seven benchmarks collectively cover twelve distinct memory dimensions. No single benchmark tests all of them. Understanding the coverage matrix is essential for designing an enterprise evaluation framework.

### 3.1 Coverage Matrix

| Dimension | LongMemEval | BEAM | LoCoMo | MemoryArena | MemAgentBench | AMA-Bench | Memora |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| Single-session recall | X | X | X | | X | | X |
| Multi-session recall | X | X | X | X | | X | X |
| Temporal reasoning | X | X | X | | | | |
| Knowledge update / supersession | X | X | | | X | | X |
| Multi-hop retrieval | | X | X | | | X | |
| Contradiction detection | | X | | | | | |
| Scale degradation | | X | | | | X | |
| Abstention (knowing what you don't know) | X | X | X | | | | |
| Task-action coupling | | | | X | | X | |
| Selective forgetting | | | | | X | | X |
| Event ordering | | X | | | | | |
| Preference following | | X | X | X | | | X |

### 3.2 Dimension Definitions

**Single-session recall.** Retrieving a specific fact stated in a single conversation turn. The baseline capability — every system must pass this.

**Multi-session recall.** Composing information across multiple separate conversation sessions. Tests whether the memory index maintains cross-session connections. Performance typically degrades as session count increases.

**Temporal reasoning.** Answering questions that require understanding when events occurred, their relative ordering, or computing time intervals. This is where most systems fail first — embedding-based retrieval strips temporal context.

**Knowledge update / fact supersession.** When a fact changes (user moves to a new city, policy is revised, preference is updated), the memory system must surface the current fact and suppress the outdated one. Distinct from selective forgetting in that the new fact is explicitly provided.

**Multi-hop retrieval.** Answering questions that require chaining two or more retrieved facts, where no single retrieval would suffice. Tests the memory system's ability to perform iterative or compositional retrieval.

**Contradiction detection.** Identifying when retrieved facts contradict each other and either resolving the contradiction or flagging it. A prerequisite for knowledge update but also independently important for data quality.

**Scale degradation.** How performance changes as the memory store grows from 128K to 500K to 1M to 10M tokens. Only BEAM and AMA-Bench (synthetic) test this at production scale.

**Abstention.** Correctly refusing to answer when the required information is not present in memory. Tests whether the system hallucinates plausible-but-ungrounded answers rather than admitting uncertainty.

**Task-action coupling.** Whether memory improves actual task execution, not just answer accuracy. Only MemoryArena and AMA-Bench test this — every other benchmark treats memory as a retrieval problem.

**Selective forgetting.** The ability to stop using information that has been explicitly invalidated — whether by supersession, deletion, or access revocation. Only MemoryAgentBench and Memora test this, and performance drops to 7% in multi-hop scenarios.

**Event ordering.** Correctly sequencing events in chronological order from memory. Requires temporal metadata preservation in the index.

**Preference following.** Applying learned user preferences to constrain future responses or actions. Tests personalization, not just recall.

### 3.3 The Missing Dimensions

No benchmark currently tests:

- **Compliance operations** — commanded deletion (GDPR Article 17), access revocation, retention enforcement
- **Multi-tenant isolation** — whether one tenant's memory leaks into another tenant's retrieval
- **Security** — resistance to memory injection (InjecMEM, MINJA), poisoned retrieval, adversarial write
- **Governance** — scope boundary enforcement, audit trail completeness, provenance preservation
- **Production reliability** — behavior under concurrent writes, partial failures, backend degradation
- **Multi-modal memory** — recall across text, image, audio, and structured data modalities

These dimensions are the subject of Section 6.

---

## 4. Competitive Leaderboard Analysis

**REFERENCE** — This section reports published benchmark scores from vendors and researchers. All scores are as of June 2026. Scores are vendor-reported unless otherwise noted; MemEval standardized comparisons are noted where available.

### 4.1 LongMemEval-S Leaderboard (Task-Averaged Accuracy, ~115K tokens)

| Rank | System | Score | Model | Architecture | Notes |
|---:|---|---:|---|---|---|
| 1 | Supermemory (ASMR) | ~99% | Multi-agent | Agent-swarm, no embeddings | Experimental; not in production |
| 2 | MemPalace | 96.6% | Local-only | Verbatim storage, ChromaDB + SQLite | Local-only; no cloud |
| 3 | OMEGA | 95.4% | GPT-4.1 | Local-first, multi-signal retrieval | Solo developer, zero funding |
| 4 | Mastra (Observational) | 94.87% | GPT-5-mini | Observation-based memory | Highest with GPT-5-mini |
| 5 | Hindsight | 91.4% | Gemini-3 Pro | Four memory networks | Most architecturally ambitious |
| 6 | RetainDB | 88% | — | Preference recall focus | 88% preference recall (SOTA sub-category) |
| 7 | Emergence | 86% | — | — | — |
| 8 | Supermemory (prod) | 85.2% | Gemini-3 Pro | Production engine | ~85.4% with GPT-4o |
| 9 | Mastra OM | 84.23% | GPT-4o | Observation-based | — |
| 10 | Letta | ~83.2% | — | MemGPT-derived | Third-party testing |
| 11 | Zep / Graphiti | 71.2% | — | Neo4j knowledge graph | 63.8% on temporal sub-task |
| 12 | Full-context GPT-4o | 60.2% | GPT-4o | No memory system | Baseline |
| 13 | Mem0 | ~49% | — | Token-efficient | Temporal sub-task score |

**Comparability warning.** These scores are often incomparable. Different vendors benchmark with different LLM backends, different retrieval parameters, and sometimes different LongMemEval variants. A "95%" from one system does not necessarily mean the same thing as "95%" from another. MemEval (Section 2.8) exists specifically to address this problem.

**Key observations:**

1. **Architecture diversity at the top.** The top-5 systems span agent-swarm (Supermemory ASMR), verbatim storage (MemPalace), multi-signal retrieval (OMEGA), observation-based (Mastra), and multi-network graph (Hindsight). No single architectural pattern dominates.

2. **The experimental-production gap.** Supermemory's ASMR approach scores ~99% experimentally but only ~85% in production. This ~14-point gap is the norm, not the exception — benchmark scores overstate production-achievable accuracy.

3. **The model matters more than the architecture.** Mastra's score jumps from 84.23% (GPT-4o) to 94.87% (GPT-5-mini) with the same architecture — a 10.6-point improvement from the model upgrade alone. This suggests that memory system improvements and LLM improvements are partially substitutable.

4. **Graph-based systems underperform on this benchmark.** Zep/Graphiti (Neo4j-backed) scores 71.2%, significantly below embedding-based systems. Knowledge graph construction overhead may not justify itself for conversational recall specifically — though graph-based approaches may have advantages on reasoning tasks that LongMemEval does not test.

5. **Full-context is not competitive.** GPT-4o with full context scores 60.2% — memory systems improve this by 25--39 points. The case for dedicated memory systems over raw context windows is settled.

### 4.2 BEAM-10M Leaderboard (10M Token Tier)

| Rank | System | Score | Notes |
|---:|---|---:|---|
| 1 | Hindsight | 64.1% | Multi-strategy retrieval; reciprocal rank fusion |
| 2 | Honcho | 40.6% | — |
| 3 | RAG baseline | 24.9% | Standard RAG pipeline |

At 10M tokens, the field narrows dramatically. Hindsight leads by 58% over the next-best result. The 64.1% absolute score — while leading — reveals that even the best system fails on more than a third of questions at production scale.

**Scale behavior.** Hindsight's 1M score (73.9%) is higher than its 500K score (71.1%). Performance does not degrade as token volume increases; it slightly improves. Most systems show the opposite. This suggests that Hindsight's multi-strategy retrieval (semantic search, keyword matching, graph traversal, temporal filtering, fused via reciprocal rank fusion) becomes more effective as the retrieval space grows — likely because the fusion mechanism has more signal to work with.

### 4.3 LoCoMo Leaderboard (Selective)

| System | F1 | Notes |
|---|---:|---|
| ByteRover 2.0 | 92.2% | — |
| Mem0 (token-efficient) | 91.6% | 90% lower token consumption vs full-context |
| Human baseline | 87.9% | — |
| GPT-4 (4K context) | 32.1% | No memory system |

Mem0's 91.6% on LoCoMo is notable not for the accuracy score alone but for the operational efficiency: 1.8K tokens per query versus 26K for full-context (90% reduction), with p95 latency of 1.44s versus 17.12s (91% reduction). In production, cost and latency matter as much as accuracy.

### 4.4 What the Leaderboards Tell Us

**For RHOAI product decisions:**

1. **There is no single best architecture.** The top system on LongMemEval-S (OMEGA) uses a completely different approach than the top system on BEAM-10M (Hindsight). Selection must be benchmark-specific and workload-specific.

2. **Production-readiness is orthogonal to benchmark score.** Supermemory ASMR scores ~99% but is not in production. Mem0 scores lower but demonstrates production-viable cost and latency. The benchmarking harness must measure operational metrics alongside accuracy.

3. **Scale is the differentiator.** At 115K tokens, many systems score above 85%. At 10M tokens, only one scores above 60%. RHOAI's enterprise positioning means the 10M+ tier is the evaluation that matters.

4. **The 2026 state of the art still fails frequently.** Even the best systems fail on 5--36% of questions depending on benchmark and scale. Memory is not a solved problem; it is an advancing frontier.

---

## 5. Evaluation Frameworks (Distinct from Benchmarks)

**REFERENCE** — Benchmarks define the *what* (test cases and scoring). Evaluation frameworks define the *how* (methodology, tooling, integration). This section surveys the evaluation approaches that can be applied to any benchmark.

### 5.1 LLM-as-Judge for Memory Quality

LLM-as-Judge is the dominant evaluation methodology for memory systems in 2026. An LLM judge agrees with human reviewers approximately 85% of the time — higher than two humans agree with each other on the same task. The approach has matured from a research technique to production infrastructure.

**Key techniques:**

- **G-Eval.** Uses chain-of-thought to generate evaluation steps from a criterion, then scores via form-filling. Suitable for nuanced memory quality assessment (relevance, freshness, coherence).
- **DAGMetric.** Breaks evaluation into a decision tree, with each node handling a smaller judgment. Produces controlled, deterministic scores. Suitable for compliance-oriented evaluation where scoring must be auditable.
- **Nugget-based decomposition.** Used by BEAM. Decomposes reference answers into atomic information units, enabling partial credit. More diagnostic than binary correct/incorrect but more expensive to construct.

**Bias mitigations required:**
- **Position bias.** Judge models favor the response placed first. Mitigation: randomly swap positions and average judgments.
- **Verbosity bias.** Judges give higher scores to longer responses regardless of content quality. Mitigation: length-normalized scoring or penalizing unnecessary verbosity.
- **Self-enhancement bias.** GPT-4 as judge favors GPT-4 outputs. Mitigation: use a different model family for judging than for generation, or use the open-source Prometheus model (13B parameters, 0.897 Pearson correlation with human evaluators — on par with GPT-4's 0.882 and far exceeding ChatGPT's 0.392).

**Enterprise consideration.** For RHOAI, the Prometheus model's comparable-to-GPT-4 correlation combined with self-hosted execution is significant. An evaluation pipeline that does not require sending production data to external APIs is a compliance requirement for many enterprise deployments. The harness design in Section 7 assumes self-hosted LLM-as-Judge as the default.

### 5.2 Human Evaluation Protocols

Human evaluation remains the ground truth calibration for LLM-as-Judge. In the memory domain specifically:

- **Factual accuracy verification.** Does the retrieved memory match the ground truth? Binary annotation, high inter-annotator agreement (>0.9 Cohen's kappa on well-defined tasks).
- **Temporal consistency judgment.** Is the most recent version of a fact used? Requires annotators to understand the full conversation history — expensive but essential for knowledge-update evaluation.
- **Relevance rating.** Is the retrieved memory relevant to the query? 1--5 Likert scale; lower inter-annotator agreement (~0.7 kappa), requiring more annotators.
- **Hallucination detection.** Does the response contain information not grounded in any memory? Binary annotation with rationale capture.

**Cost model.** MemoryArena reports 8--10 hours per formal reasoning task by senior PhDs and ~$60K total construction cost. LoCoMo used LLM-generated conversations verified by human annotators. A mixed approach — LLM-generated test cases with human verification of a calibration subset — is the pragmatic path for enterprise evaluation.

### 5.3 Production Metrics

Beyond benchmark accuracy, production memory systems must be evaluated on operational metrics:

| Metric | Definition | Target (2026 norms) |
|---|---|---|
| **Precision** | Fraction of retrieved memories that are relevant | >0.90 |
| **Recall** | Fraction of relevant memories that are retrieved | >0.85 |
| **F1** | Harmonic mean of precision and recall | >0.87 |
| **Token efficiency** | Tokens consumed per retrieval query | <7,000 (Mem0 standard) |
| **p50 latency** | Median retrieval time | <100ms (voice), <200ms (chat), <400ms (copilot) |
| **p95 latency** | 95th percentile retrieval time | <500ms for all modalities |
| **Freshness** | Time from memory write to retrievability | <5s for working memory, <60s for long-term |
| **FAMA** | Forgetting-Aware Memory Accuracy (Memora) | No established target; >0.80 proposed |
| **Write throughput** | Memory writes per second sustained | Workload-dependent; minimum 100 writes/s per agent |
| **Storage efficiency** | Bytes per memory fact stored | Architecture-dependent |

**Latency budgets (2026 industry standards):**
- Voice AI agents: sub-100ms retrieval to hit <800ms total response time
- Conversational chat agents: 200ms retrieval budget within 1-second window
- Enterprise copilots: 400ms retrieval budget within 3-second window
- Reranking adds 50--150ms on top of vector search
- Redis achieves 5ms p50 for in-memory workloads; Qdrant delivers 4ms for vector operations

### 5.4 CI/CD Integration Patterns

The modern LLM evaluation pipeline follows a four-stage model that applies directly to memory evaluation:

**Stage 1 — Local development.** Rapid iteration against a curated golden dataset (200--500 examples). Tools: DeepEval, Promptfoo. Run per-commit or on-demand.

**Stage 2 — Pull request gate.** Automated LLM-judge run against the full golden dataset. The judge must be calibrated to achieve 85--90% agreement with a human-annotated reference set. Regressions below the established baseline block the merge.

**Stage 3 — Deployment gate.** Threshold-based blocking on accuracy, FAMA, latency, and token efficiency. This is where the harness proposed in Section 7 integrates — any regression from the production baseline halts deployment.

**Stage 4 — Production monitoring.** Live traffic sampling feeding back into the golden dataset. Each production failure becomes a new test case, creating a virtuous cycle where the evaluation suite becomes permanently more robust.

**The feedback loop.** Production monitoring discovers new failure modes. Those failures become golden dataset entries. The updated golden dataset catches regressions in CI/CD. CI/CD prevents those failures from reaching production. Over months, this builds an evaluation suite deeply tailored to the specific deployment.

**Key tools (2026):** DeepEval (pytest integration via `assert_test()`, agent-level metrics including tool correctness and trajectory evaluation), Promptfoo (quality gates + red teaming + compliance reporting), Langfuse (self-hosted evaluation infrastructure), Braintrust (benchmark curation + regression testing).

---

## 6. Enterprise-Specific Evaluation Needs

**PROPOSED** — The dimensions in this section are not covered by any existing benchmark. They represent the evaluation gap between academic memory benchmarks and enterprise production requirements. Each dimension is a proposed component of the RHOAI benchmarking harness (Section 7).

### 6.1 Compliance Evaluation

**GDPR Article 17 — Right to Erasure.** No commercially available vector database currently provides a provable deletion mechanism for embedded personal data. A compliance evaluation must test:

- **Erasure completeness.** After a deletion request, is the target data absent from all retrieval paths — vector similarity, keyword search, graph traversal, metadata queries?
- **Erasure verifiability.** Can the system produce an audit trail proving that deletion occurred and that the data is no longer retrievable?
- **Cascade deletion.** If a memory fact was used to derive other facts (through consolidation, summarization, or inference), are the derived facts also purged or flagged?
- **Erasure latency.** How long between a deletion request and guaranteed non-retrievability? The gap is a compliance exposure window.

**HIPAA ePHI Isolation.** Healthcare deployments require that electronic Protected Health Information (ePHI) in memory is isolated, encrypted at rest and in transit, and accessible only to authorized roles. The evaluation must test:

- **Cross-patient isolation.** Agent A's patient memory must never appear in Agent B's patient retrieval, even under semantic similarity.
- **Minimum necessary.** Memory retrieval must return only the facts necessary for the current task, not the full patient history.
- **Audit completeness.** Every memory read and write must produce an audit event traceable to the requesting user, agent, and purpose.

**EU AI Act (enforceable August 2, 2026).** Article 12 requires automatic event logging throughout the lifetime of any high-risk AI system, with traceability to source data and decision rationale. Memory systems must:

- **Log all writes with provenance.** Every memory write must record: source (user, tool, environment), timestamp, agent identity, and the raw input that produced the write.
- **Log all reads with purpose.** Every memory retrieval must record: query, results returned, downstream usage (which response or action consumed the memory).
- **Support lineage queries.** Given a decision, trace backward to the specific memory facts, their sources, and their write timestamps that contributed to it.

### 6.2 Multi-Tenant Isolation Testing

In a multi-tenant RHOAI deployment, memory isolation between tenants is a hard security boundary, not a soft preference. The evaluation must test:

- **Cross-tenant retrieval.** Given Tenant A's memory store and Tenant B's queries, does any of Tenant A's data appear in Tenant B's results? Test with semantically similar content across tenants.
- **Shared infrastructure leakage.** If tenants share a vector store backend (e.g., shared Elasticsearch or Qdrant cluster), does embedding proximity cause cross-tenant retrieval?
- **Metadata leakage.** Can Tenant B discover Tenant A's memory key names, session counts, or usage patterns through side-channel queries?
- **Tenant deletion.** When a tenant is deprovisioned, is their entire memory store verifiably purged?

### 6.3 Scope Boundary Enforcement

The doc-07 taxonomy defines memory scope tiers (session, user, team, org, platform). The evaluation must verify that scope boundaries are enforced:

- **Upward leakage.** Does session-scoped memory appear in org-scoped queries?
- **Downward leakage.** Does org-scoped confidential memory appear in individual user queries when the user lacks access?
- **Cross-scope reasoning.** When a query requires combining facts from different scope tiers, are the access controls on each fact individually verified before composition?
- **Scope transition.** When a memory fact's scope changes (e.g., user-scoped memory promoted to team-scoped), are the access controls updated atomically?

### 6.4 Security Evaluation (Memory Injection Resistance)

Doc 11 (Adversarial Memory) catalogs the threat taxonomy. The benchmarking harness must include a red-team evaluation layer:

- **InjecMEM resistance.** Does a single adversarial interaction succeed in poisoning the memory store such that future queries on the target topic return attacker-controlled output? The published attack achieves 76.6% success rate with Multi-GCG optimization — a passing system must reduce this to <5%.
- **MINJA resistance.** Does an indirect injection through a document processed into memory succeed in altering retrieval results? Published defenses (LlamaGuard, embedding-level sanitization, prompt-based detection) have proven ineffective.
- **Provenance-aware retrieval.** Does the system distinguish between user-authored memory and tool/environment-derived memory, applying different trust levels to each?
- **Memory integrity verification.** Can the system detect that a memory record has been tampered with post-write?

### 6.5 Scale Degradation Testing

Enterprise memory stores grow continuously. The evaluation must test behavior at:

| Scale Tier | Token Count | Equivalent | What It Tests |
|---|---:|---|---|
| T1 | 1M | ~3 months of single-agent interaction | Baseline operation |
| T2 | 10M | ~2.5 years single-agent or 1 month 100-agent team | BEAM-equivalent scale |
| T3 | 100M | Enterprise-wide deployment, 1 year | Beyond any published benchmark |
| T4 | 1B | Enterprise-wide deployment, multi-year | Aspirational; tests index architecture limits |

At each tier, measure: accuracy (all benchmark dimensions), latency (p50, p95, p99), token efficiency, write throughput, and storage footprint. The degradation curve across tiers is the key output — a system that scores 95% at 1M but 40% at 100M has a hidden cliff.

---

## 7. Red Hat Benchmarking Harness Design

**PROPOSED** — This section proposes the architecture of an internal benchmarking harness for evaluating agent memory backends on OpenShift. The design is not committed — it is a research recommendation for the review gate. The harness serves two audiences: (1) RHOAI engineering, selecting and validating memory backends for productization, and (2) RHOAI customers, evaluating memory configurations for their workloads.

### 7.1 Pipeline Phases

The harness operates as a five-phase pipeline. Each phase is a discrete container image with defined inputs and outputs, composable via Kubernetes Jobs or Tekton Pipelines.

```
INGEST --> INDEX --> QUERY --> ANSWER --> EVALUATE

Phase 1: INGEST
  Input:  Benchmark dataset (LongMemEval, BEAM, LoCoMo, custom)
  Output: Normalized conversation stream in OpenTelemetry-compatible format
  Action: Parse benchmark format, inject temporal metadata, apply scope annotations

Phase 2: INDEX
  Input:  Normalized conversation stream
  Output: Populated memory backend (the system under test)
  Action: Feed conversations to the memory system as if they were live interactions
  Metric: Write throughput, storage footprint, indexing latency

Phase 3: QUERY
  Input:  Benchmark question set + populated memory backend
  Output: Raw retrieval results (memories retrieved per question)
  Action: Issue each question as a retrieval query to the memory system
  Metric: Retrieval latency (p50, p95, p99), token count per retrieval

Phase 4: ANSWER
  Input:  Retrieved memories + original questions
  Output: Generated answers (using a fixed LLM to control for model variation)
  Action: Prompt the LLM with retrieved context and the question
  Metric: Tokens consumed, generation latency

Phase 5: EVALUATE
  Input:  Generated answers + ground-truth answers + FAMA annotations
  Output: Scored results across all dimensions
  Action: LLM-as-Judge scoring (self-hosted Prometheus or equivalent)
  Metric: Accuracy, FAMA, precision, recall, F1, per-dimension breakdowns
```

**Isolation principle.** Each phase runs in its own container with its own resource quotas. Phase 2 (INDEX) is the only phase that touches the memory backend. Phase 4 (ANSWER) is the only phase that touches the LLM. This separation ensures that benchmark results are attributable: a latency regression can be traced to the memory system (Phase 2/3) or the LLM (Phase 4), not conflated.

### 7.2 Pluggable Backend Abstraction

The harness must evaluate multiple memory backends without modification to the pipeline. The abstraction layer defines a minimal interface:

```
MemoryBackend:
  write(session_id, turn_id, content, metadata) -> write_ack
  query(query_text, scope, filters) -> list[MemoryResult]
  delete(memory_id) -> delete_ack
  delete_by_scope(scope, filters) -> delete_count
  stats() -> BackendStats (count, storage, index_size)
```

**Planned adapters:**
- OGX memory primitives (doc 06) — the MVP path
- MemoryHub-derived store (doc 03) — the governance layer
- Mem0 — token-efficient baseline
- Zep/Graphiti — knowledge graph baseline
- Raw vector store (Qdrant, pgvector) — minimal baseline
- Full-context (no memory system) — lower-bound baseline

The adapter contract is inspired by MemEval's one-function adapter approach: adding a new backend requires implementing the five interface methods and providing a Dockerfile.

### 7.3 OpenShift-Native Benchmark Execution

The harness leverages existing OpenShift and RHOAI benchmarking patterns:

**GuideLLM integration.** GuideLLM is already the standard tool for LLM inference benchmarking on OpenShift. The Phase 4 (ANSWER) stage uses GuideLLM's scheduling strategies to simulate realistic inference load patterns:
- Constant rate for steady-state evaluation
- Poisson distribution for production-realistic arrival patterns
- Sweep mode for finding throughput limits
- The harness adds a "memory-bound" mode that sequences queries based on temporal dependencies in the benchmark

**Kube-burner patterns.** For scale-degradation testing (Section 6.5), the harness adopts kube-burner's approach to stress testing:
- Configurable job iterations (number of conversations to ingest)
- Namespace-per-tier isolation (T1/T2/T3/T4 run in separate namespaces)
- Prometheus metric scraping and indexing throughout the benchmark run
- Grafana dashboards for real-time observation during benchmark execution

**Resource specification.** Each benchmark run specifies its resource requirements as a Kubernetes resource quota:

```yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: memory-benchmark-t2
spec:
  hard:
    requests.cpu: "16"
    requests.memory: 64Gi
    requests.nvidia.com/gpu: "1"  # For LLM-as-Judge
    persistentvolumeclaims: "4"   # Memory backend, benchmark data, results, judge model
```

### 7.4 Reproducibility Requirements

Every benchmark run must produce a manifest that enables exact reproduction:

```yaml
benchmark_manifest:
  harness_version: "1.2.0"
  benchmark_dataset: "longmemeval-s-v2"
  dataset_hash: "sha256:abc123..."
  memory_backend:
    type: "ogx-memory"
    version: "0.4.1"
    config_hash: "sha256:def456..."
  llm_judge:
    model: "prometheus-13b-v2"
    model_hash: "sha256:ghi789..."
    temperature: 0.0
  llm_answer:
    model: "llama-3.3-70b-instruct"
    model_hash: "sha256:jkl012..."
    temperature: 0.0
  infrastructure:
    ocp_version: "4.17"
    rhoai_version: "3.6"
    node_type: "m5.4xlarge"
    gpu_type: "A10G"
  results:
    accuracy: 0.874
    fama: 0.821
    p95_latency_ms: 312
    tokens_per_query: 4200
    timestamp: "2026-09-15T14:30:00Z"
```

**Determinism.** Temperature 0.0 for both the answer LLM and the judge LLM. Fixed random seeds for any sampling operations. Pinned model versions (not "latest"). Network-isolated execution (no external API calls during the benchmark).

### 7.5 CI/CD Integration

The harness integrates into the RHOAI CI/CD pipeline at two points:

**Nightly regression.** A reduced benchmark suite (100 questions, T1 scale) runs nightly against the current development branch. Regressions >2% from the established baseline trigger alerts and block promotion to the next release gate.

**Release qualification.** The full benchmark suite (500+ questions across all academic benchmarks, T1--T3 scale, all enterprise evaluation dimensions) runs as part of release qualification. Results are compared against the previous release baseline and against a fixed competitive reference set.

**Dashboard.** Results are indexed to Elasticsearch and visualized in Grafana dashboards showing:
- Accuracy trend over time (per dimension, per backend)
- Latency distribution (p50/p95/p99) over time
- Scale degradation curves (accuracy vs. token count)
- FAMA score trend (memory freshness health)
- Competitive comparison (RHOAI backend vs. published vendor scores on same benchmark)

### 7.6 Enterprise Evaluation Module

In addition to the academic benchmark pipeline, the harness includes an enterprise evaluation module that tests the dimensions from Section 6. This module uses synthetic test scenarios rather than academic datasets:

**Compliance test suite:**
- `compliance/gdpr-erasure`: Write N memories, issue deletion for specific records, verify non-retrievability across all retrieval paths, verify audit trail
- `compliance/hipaa-isolation`: Create two patient contexts, verify zero cross-patient retrieval, verify audit events
- `compliance/eu-ai-act-lineage`: Write memories, generate answers, trace lineage backward from answer to source memory to original input

**Security test suite:**
- `security/injecmem`: Execute the published InjecMEM attack across 10 topic domains, measure attack success rate, target <5%
- `security/scope-boundary`: Attempt cross-scope retrieval at every boundary pair (session/user, user/team, team/org), measure leakage rate, target 0%
- `security/concurrent-write`: Issue concurrent writes from multiple agents, verify memory consistency and no corruption

**Scale test suite:**
- `scale/degradation-curve`: Ingest at T1/T2/T3 scales, measure accuracy and latency at each tier, produce degradation curve
- `scale/concurrent-agents`: Simulate 10/100/1000 concurrent agents accessing the same memory backend, measure throughput and isolation

---

## 8. Key Gaps: What No Benchmark Currently Tests

**EXPLORATORY** — Synthesizing the survey in Sections 2--6, the following gaps represent capabilities that matter for enterprise deployment but have no published evaluation methodology.

### 8.1 Enterprise Governance

No benchmark tests whether a memory system enforces organizational governance policies. Scope boundaries (doc 07), access control, retention policies, and audit completeness are untested. The closest proxy is Memora's FAMA metric for obsolete memory, but FAMA tests information supersession, not policy-driven access control.

### 8.2 Compliance Operations

GDPR right-to-erasure, HIPAA minimum necessary, and EU AI Act lineage requirements have no evaluation methodology in the academic literature. The Memora and MemoryAgentBench work on selective forgetting tests a related capability (information supersession) but not commanded deletion or access revocation. Given that EU AI Act Article 12 becomes enforceable August 2, 2026, this gap is urgent.

### 8.3 Production Reliability

No benchmark tests memory system behavior under partial failure (backend degradation, network partition, concurrent-write conflicts), recovery from corruption, or graceful degradation. Academic benchmarks assume perfect infrastructure. Production does not provide perfect infrastructure.

### 8.4 Multi-Modal Memory

LoCoMo includes image-sharing elements, but no benchmark rigorously tests recall across text, image, audio, and structured data modalities. Enterprise agents increasingly operate across modalities — a customer support agent may need to recall a screenshot shared in a previous session alongside the text of the conversation.

### 8.5 Security (Memory Injection)

The InjecMEM and MINJA attacks demonstrate that memory systems are vulnerable to persistent poisoning. No benchmark includes adversarial injection as a standard evaluation dimension. Published defenses (LlamaGuard, embedding sanitization, prompt-based detection) have proven ineffective. Red-team evaluation of memory injection resistance is necessary for any system handling sensitive enterprise data.

### 8.6 Cost-Accuracy Tradeoff at Scale

Benchmarks report accuracy. Production deployments optimize for cost-adjusted accuracy. A system that achieves 95% accuracy at $0.10/query and a system that achieves 92% at $0.002/query are not comparable on accuracy alone. No benchmark provides a cost-normalized scoring methodology. Mem0's published efficiency data (91.6% accuracy at 90% lower token consumption) points toward this dimension but does not standardize the measurement.

### 8.7 Cross-System Memory Migration

Enterprise deployments change memory backends over time — from a prototype vector store to a production knowledge graph, or from one vendor to another. No benchmark tests whether memories can be migrated between systems without information loss, and no benchmark tests whether a system can operate on a memory store originally populated by a different system.

---

## 9. Recommendations

**PROPOSED** — For the review gate.

### R1. Adopt the Three-Benchmark Standard for RHOAI Memory Evaluation

Use LongMemEval-S (conversational recall), BEAM-10M (production-scale stress), and MemoryArena (task-action coupling) as the three mandatory academic benchmarks for any memory backend considered for RHOAI productization. These three collectively cover 11 of the 12 dimensions in Section 3.1 (missing only selective forgetting, which MemoryAgentBench adds as a supplementary benchmark).

### R2. Build the Enterprise Evaluation Module Before Productizing Any Memory Backend

The compliance, security, and scale-degradation test suites described in Section 7.6 must be built and passing before any memory backend is shipped as a supported RHOAI feature. Academic benchmark scores are necessary but not sufficient — they test recall accuracy, not enterprise governance.

### R3. Adopt FAMA as a First-Class Metric

Memora's Forgetting-Aware Memory Accuracy should be tracked alongside standard accuracy for every benchmark run. FAMA is the only metric that penalizes reliance on obsolete memory — a compliance-relevant failure mode that standard accuracy scores hide.

### R4. Use Self-Hosted LLM-as-Judge

All evaluation should use a self-hosted judge model (Prometheus-13B or successor). The harness must not depend on external API calls for evaluation. This satisfies enterprise data residency requirements and ensures evaluation infrastructure is available in air-gapped deployments.

### R5. Establish a Competitive Reference Set

Maintain a fixed set of published vendor scores (from the leaderboards in Section 4) and compare RHOAI backend results against them in every release qualification. The reference set should be updated quarterly as new vendor results are published.

### R6. Start with MemEval's Standardization Approach

MemEval's one-adapter-per-backend model should inform the pluggable backend abstraction (Section 7.2). Rather than building a custom framework from scratch, extend MemEval with the enterprise evaluation module. MemEval is open source and already supports LoCoMo and LongMemEval.

### R7. Align Benchmark Execution with Existing OpenShift Tooling

Use GuideLLM for LLM inference characterization, kube-burner patterns for scale stress testing, and Tekton Pipelines for pipeline orchestration. Do not introduce new execution frameworks when existing Red Hat tooling serves the purpose.

---

## 10. Sources

| # | Source | Type | Date | Used In |
|---|---|---|---|---|
| S1 | [LongMemEval: Benchmarking Chat Assistants on Long-Term Interactive Memory](https://arxiv.org/abs/2410.10813) — Wu et al., ICLR 2025 | Paper | 2025-01 | SS 2.1, 3, 4.1 |
| S2 | [BEAM: Beyond a Million Tokens — Benchmarking and Enhancing Long-Term Memory in LLMs](https://arxiv.org/abs/2510.27246) — Tavakoli et al., ICLR 2026 | Paper | 2026-01 | SS 2.2, 3, 4.2 |
| S3 | [LoCoMo: Evaluating Very Long-Term Conversational Memory of LLM Agents](https://aclanthology.org/2024.acl-long.747/) — Maharana et al., ACL 2024 | Paper | 2024-08 | SS 2.3, 3, 4.3 |
| S4 | [MemoryArena: Benchmarking Agent Memory in Interdependent Multi-Session Agentic Tasks](https://arxiv.org/abs/2602.16313) — He et al., ICML 2026 | Paper | 2026-02 | SS 2.4, 3, R1 |
| S5 | [MemoryAgentBench: Evaluating Memory in LLM Agents via Incremental Multi-Turn Interactions](https://arxiv.org/abs/2507.05257) — Hu et al., ICLR 2026 | Paper | 2026-01 | SS 2.5, 3 |
| S6 | [AMA-Bench: Evaluating Long-Horizon Memory for Agentic Applications](https://arxiv.org/abs/2602.22769) — Zhao et al., ICLR 2026 Workshop | Paper | 2026-02 | SS 2.6 |
| S7 | [Memora: From Recall to Forgetting — Benchmarking Long-Term Memory for Personalized Agents](https://arxiv.org/abs/2604.20006) | Paper | 2026-04 | SS 2.7, R3 |
| S8 | [MemEval: Benchmarking Memory for AI Agents](https://medium.com/prosus-ai-tech-blog/memeval-benchmarking-memory-for-ai-agents-932d3fd9f3b4) — Prosus AI | Blog | 2026-03 | SS 2.8, R6 |
| S9 | [OMEGA LongMemEval Benchmark Leaderboard](https://omegamax.co/benchmarks) | Leaderboard | 2026 | SS 4.1 |
| S10 | [Hindsight BEAM SOTA](https://hindsight.vectorize.io/blog/2026/04/02/beam-sota) — Vectorize | Blog | 2026-04 | SS 4.2 |
| S11 | [Supermemory ASMR: 99% on LongMemEval](https://aihola.com/article/supermemory-99-longmemeval-agentic-memory) | Article | 2026 | SS 4.1 |
| S12 | [Mastra Observational Memory: 95% on LongMemEval](https://mastra.ai/research/observational-memory) | Research | 2026 | SS 4.1 |
| S13 | [Mem0 Research Paper: Token-Efficient Memory Algorithm](https://mem0.ai/research) | Paper | 2026 | SS 4.3, 5.3 |
| S14 | [State of AI Agent Memory 2026](https://mem0.ai/blog/state-of-ai-agent-memory-2026) — Mem0 | Blog | 2026 | SS 3, 4 |
| S15 | [AI Memory Benchmarks in 2026](https://mem0.ai/blog/ai-memory-benchmarks-in-2026) — Mem0 | Blog | 2026 | SS 2, 3 |
| S16 | [InjecMEM: Memory Injection Attack on LLM Agent Memory Systems](https://openreview.net/forum?id=QVX6hcJ2um) | Paper | 2026 | SS 6.4 |
| S17 | [A Survey on the Security of Long-Term Memory in LLM Agents](https://arxiv.org/html/2604.16548v1) | Survey | 2026-04 | SS 6.4 |
| S18 | [When Memory Became the Attack Surface](https://llms3.com/blog/when-memory-became-the-attack-surface-may-2026) — LLMS3 | Blog | 2026-05 | SS 6.4 |
| S19 | [GuideLLM: Evaluate LLM Deployments for Real-World Inference](https://developers.redhat.com/articles/2025/06/20/guidellm-evaluate-llm-deployments-real-world-inference) — Red Hat Developer | Article | 2025-06 | SS 7.3 |
| S20 | [Benchmarking with GuideLLM in Air-Gapped OpenShift Clusters](https://developers.redhat.com/articles/2025/09/15/benchmarking-guidellm-air-gapped-openshift-clusters) — Red Hat Developer | Article | 2025-09 | SS 7.3 |
| S21 | [Kube-burner: A Tool to Burn Down Kubernetes and OpenShift](https://www.redhat.com/en/blog/introducing-kube-burner-a-tool-to-burn-down-kubernetes-and-openshift) — Red Hat | Blog | — | SS 7.3 |
| S22 | [AI Agent Memory Governance: 6 Enterprise Risks Explained](https://atlan.com/know/ai-agent-memory-governance/) — Atlan | Article | 2026 | SS 6.1 |
| S23 | [Engineering GDPR Compliance in the Age of Agentic AI](https://iapp.org/news/a/engineering-gdpr-compliance-in-the-age-of-agentic-ai) — IAPP | Article | 2026 | SS 6.1 |
| S24 | [DeepEval: The LLM Evaluation Framework](https://deepeval.com/docs/evaluation-unit-testing-in-ci-cd) | Docs | 2026 | SS 5.4 |
| S25 | [Promptfoo CI/CD Integration](https://www.promptfoo.dev/docs/integrations/ci-cd/) | Docs | 2026 | SS 5.4 |
| S26 | [LLM-as-a-Judge: Complete Guide](https://www.confident-ai.com/blog/why-llm-as-a-judge-is-the-best-llm-evaluation-method) — Confident AI | Guide | 2026 | SS 5.1 |
| S27 | [Memory Retrieval Latency Budgets (May 2026)](https://blog.supermemory.ai/latency-budgets-memory-retrieval/) — Supermemory | Blog | 2026-05 | SS 5.3 |
| S28 | [Hindsight Benchmark Results](https://benchmarks.hindsight.vectorize.io/) — Vectorize | Dashboard | 2026 | SS 4.2 |
| S29 | [Agent Memory Benchmark Comparison: Hindsight vs Alternatives](https://hindsight.vectorize.io/guides/2026/04/21/comparison-agent-memory-benchmark-hindsight-vs-alternatives) — Vectorize | Guide | 2026-04 | SS 4 |
| S30 | [MemPalace: 100% LongMemEval Benchmark](https://gamgee.ai/blogs/mempalace-verbatim-memory-benchmark/) — Gamgee | Blog | 2026 | SS 4.1 |
| S31 | [AI Memory Systems Statistics 2026 (60+ Sourced Stats)](https://preuve.ai/blog/ai-memory-systems-statistics-2026) — Preuve | Blog | 2026 | SS 5.3 |
| S32 | [Best AI Agent Memory Systems in 2026: 8 Frameworks Compared](https://vectorize.io/articles/best-ai-agent-memory-systems) — Vectorize | Article | 2026 | SS 4 |
| S33 | [LLM Evaluation in 2026](https://medium.com/@nairmilind3/llm-evaluation-in-2026-e631a78c67dc) — Nair | Blog | 2026 | SS 5.4 |

---

*Document 12 of 15 — Agent Memory & Knowledge Research, Phase 2. Last updated 2026-06-09.*
