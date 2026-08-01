---
title: "Agent Memory & Knowledge: Landscape and Definitions"
description: Shared vocabulary and definitions for agent memory, agent knowledge, and context engineering, and why precise scoping matters for RHOAI.
source: ai-asset-registry/agent-memory/research/01-landscape-and-definitions.md (as of 2026-07-05)
timestamp: 2026-07-06
review_after: 2026-08-05
---

# Agent Memory & Knowledge: Landscape and Definitions

**Purpose:** Establish shared vocabulary and definitions for "agent memory," "agent knowledge," and "context engineering," map where the industry disagrees, and explain why precise scoping matters for RHOAI's platform decisions.

**Date:** 2026-05-17

**Status:** EXPLORATORY — foundational research, no features scoped. See [RHAISTRAT-1345](https://redhat.atlassian.net/browse/RHAISTRAT-1345).

**Series:** Document 01 of 17 — Agent Memory & Knowledge Research
**Phase 1:** [00](00-executive-summary.md) · 01 Landscape & Definitions (this doc) · [02](02-solution-survey.md) · [03](03-memoryhub-deep-dive.md) · [04](04-technical-patterns.md) · [05](05-standards-and-protocols.md) · [06](06-ogx-memory-primitives.md) · [07](07-taxonomy-and-decomposition.md) · [08](08-rhoai-ocp-alignment.md)
**Phase 2:** [09](09-agent-harness-memory.md) · [10](10-claude-memory-dreaming.md) · [11](11-adversarial-memory.md) · [12](12-benchmarking-evaluation.md) · [13](13-kv-cache-optimization.md) · [14](14-enterprise-use-cases.md) · [15](15-multi-modal-memory.md) · [16](16-ai-gateway-memory-substrate.md) · [REVIEW-NOTES](REVIEW-NOTES.md)

---

## 1. The Definitional Landscape: Where Terms Agree and Where They Diverge

### 1.1 "Agent Memory" — Converging Definition

**REFERENCE** — Most practitioners and researchers converge on this core formulation: agent memory is the mechanism by which an AI agent stores and retrieves information across more than one inference call, enabling behavioral continuity and learning over time. The definitive academic framing comes from the CoALA paper (Sumers et al., arXiv:2309.02427, Princeton, 2023), which established the canonical four-type taxonomy now cited across industry and academia: working, episodic, semantic, and procedural. Subsequent surveys (Du, arXiv:2603.07670, March 2026; Jiang et al., arXiv:2602.19320, 2026) refine but do not displace this structure.

The key property distinguishing agent memory from a simple cache is the **write path**: memory systems allow agents to record new information during interactions and retrieve it in future sessions. This is not retrieval over a fixed corpus — it is a living, append-heavy, and frequently updated state store.

**Tension on scope:** Where practitioners diverge is on what counts as *memory* versus *external knowledge*. Oracle (Alake, 2026) defines memory broadly as four access patterns over a single unified state, explicitly including both a user's stated preferences (semantic) and an agent's past session history (episodic) in the same governed substrate. Mem0 (State of AI Agent Memory 2026) uses a three-type model (episodic, semantic, procedural), folding working memory into the context management concern separately. Wes Jackson explicitly distinguishes memory from RAG-served external corpora, classifying only the agent's *internally learned state* — preferences, observations, decisions, provenance chains — as true memory. IBM arrives at the same four types as CoALA, but introduces a fifth "organisational context memory" for enterprise data agents requiring certified assets and runtime governance enforcement.

**Practical implication:** There is no single authoritative definition of where the boundary sits between "agent memory" and "external knowledge base." This document adopts the CoALA four-type model as the reference taxonomy (Section 4) and treats the boundary question as an open research issue for RHOAI (see Section 5, Q40–41).

### 1.2 "Agent Knowledge" — Least Settled Term

**EXPLORATORY** — "Agent knowledge" is the least consistently used term in this space. Peter Double's initial framing (see `docs/knowledge-review/assets/agent-memory-knowledge.md`) defines it as a *graph knowledge layer organizing everything related to an organization*: regulations, policies, product knowledge, code, processes, scoped from a single team to the whole company. This closely resembles what practitioners call *enterprise RAG* or a *knowledge graph*, but frames it as a first-class platform primitive rather than a retrieval augmentation.

Oracle (Alake, 2026) does not use "agent knowledge" as a distinct term — Oracle folds the concept into *semantic memory* (durable facts and structured reference data). Meta's AI Second Brain (Analytics at Meta, 2026) uses Tiago Forte's PARA framework (Projects/Areas/Resources/Archives) as an organizational layer that serves a similar function: progressive disclosure of org-wide context. Neither of these treats "agent knowledge" as requiring a separate system from memory.

**Contradiction to flag:** Peter's framing separates "Agent Knowledge" (area 1) from "Agentic Memory" (area 2), implying they are distinct platform concerns. The Oracle, MemoryHub, and academic evidence argues these can and should live on a single governed substrate distinguished only by their access pattern, not their storage layer. Resolution is a key research question (Q41 in `docs/knowledge-registry.md`).

### 1.3 "Context Engineering" — Contested Scope

**REFERENCE** — Context engineering has emerged in 2025–2026 as a term covering a broader design discipline than prompt engineering. Weaviate (blog, 2026) defines it as "the discipline of designing the architecture that feeds an LLM the right information at the right time" — treating the context window as a scarce resource and orchestrating retrieval, memory, tool integrations, and prompts around it. The distinction from prompt engineering: prompt engineering specifies *how to phrase instructions*; context engineering specifies *what information the model can access* across the full inference-time context window.

Mem0 (blog, 2026) goes further, explicitly positioning memory management as "one of the core pillars of context engineering" — memory determines what information persists across interactions and how it gets retrieved. Under this framing, context engineering subsumes memory.

The New Stack (article, 2026) frames memory as "a new paradigm of context engineering," positioning the two as tightly coupled rather than separate concerns.

**Where it diverges:** Peter's initial framing treats context engineering as a distinct third area alongside Agent Knowledge and Agentic Memory. The emerging industry usage collapses context engineering into memory management: they are the same problem domain, not parallel tracks. Meta's "progressive disclosure" and Oracle's "summarization-threshold tuning" are both context engineering techniques implemented as part of their memory architectures.

**Tension to flag:** If context engineering is a sub-discipline of memory management rather than a parallel concern, RHAISTRAT-1345's scope (conversation state, long-term persistence, context compaction) may already encompass all three of Peter's initial areas rather than only areas 2 and 3. This has direct implications for scope definition and Outcome boundaries (Q42 in `docs/knowledge-registry.md`).

---

## 2. Memory vs. RAG

**REFERENCE** — The distinction between agent memory and RAG is one of the most practically important — and most frequently blurred — in the agent architecture space. Wes Jackson, a Red Hat Solutions Architect, offers the sharpest available formulation:

> RAG retrieves external information — it answers *"What does the manual say?"* Agent memory tracks internal system knowledge — it answers *"What have agents learned?"*

The structural distinction is the **write path**. RAG operates as a read-only, stateless retrieval mechanism: documents are indexed in a batch pipeline and queried at inference time, with the session context discarded after each exchange. Agent memory operates as a stateful, append-heavy store where agents *write* to the store during interactions and retrieve that written state in future sessions.

A research citation formalizes this: "RAG targets large heterogeneous corpora; agent memory involves bounded, coherent dialogue streams with highly correlated spans" (arXiv:2602.02007, 2026). These are not the same data shape, and optimizing for one does not optimize for the other.

The key architectural differences:

| Dimension | RAG | Agent Memory |
|---|---|---|
| **Write path** | Offline ingestion only; agents cannot write | Dynamic writes from agent interactions during inference |
| **Persistence** | Session-independent (corpus is stable) | Cross-session accumulation; memories evolve |
| **Data shape** | Large, diverse, heterogeneous document corpora | Bounded, coherent interaction streams |
| **Freshness model** | Batch-dependent lag | Continuously updated |
| **Retrieval model** | One-shot at query time | Dynamic, context-aware, multi-signal |
| **Primary cost driver** | Token injection per query | Storage + retrieval overhead; can be mitigated by prompt caching |
| **Error semantics** | Errors reset each session | Errors persist and resurface indefinitely if written to memory |

**Agentic RAG as a bridge concept:** A middle-ground pattern has emerged called *agentic RAG*, where an agent dynamically decides *whether* and *where* to retrieve external knowledge, using retrieval as a tool call rather than a fixed preprocessing step. This is still read-only retrieval against an external corpus, but it introduces LLM-driven retrieval strategy. It is not the same as agent memory (Monigatti, 2026).

**The combination pattern:** For production enterprise agents, RAG and agent memory are not alternatives — they are complementary. The standard recommendation (Atlan, Memorilabs, 2026) is: use RAG for breadth (knowledge-intensive Q&A, large static corpora), use memory for continuity (multi-turn workflows, personalization, cross-session learning). Systems requiring both deploy them in parallel. *(Note: Atlan is a data-catalog vendor; this recommendation reflects their marketing blog, corroborated here by Memorilabs — treat as practitioner guidance, not independent research.)*

**Important caveat for RHOAI:** Peter's area 1 (Agent Knowledge — the org-wide graph layer) looks architecturally closer to enterprise RAG than to agent memory as defined above. If this mapping holds, "Agent Knowledge" and "Agentic Memory" are not two subtypes of the same thing — they are fundamentally different data architectures (search vs. database). However, Oracle argues they can be access patterns over one governed substrate, collapsing this distinction. See Section 5 for implications.

---

## 3. Client-Side vs. Server-Side Memory

**REFERENCE** — One of the most practically significant architectural forks in the current landscape is where memory physically lives: in the agent's local execution environment (client-side) or on a remote, centrally managed service (server-side). Francisco Arceo's comment on RHAISTRAT-1345 (March 2026) first surfaced this distinction as a RHOAI-relevant concern.

### 3.1 Client-Side Memory

Client-side memory lives in the agent's own execution environment. The agent controls all reads and writes; no separate memory service is required. Examples:

- **Anthropic Memory Tool** (beta, 2025): The memory tool is explicitly client-side. Claude makes tool calls to perform operations (view, create, str_replace, insert, delete, rename) on files in a `/memories` directory. The application developer controls where and how data is stored — file-based, database, cloud storage, or encrypted files are all valid backends. The documentation states: "The memory tool operates client-side: you control where and how the data is stored through your own infrastructure." (platform.claude.com/docs)

- **OpenClaw**: Client-side exclusively. Memory is stored as plain Markdown files in the agent's workspace (`~/.openclaw/workspace`). Retrieval uses hybrid search (vector similarity 70% + BM25 keyword 30%) when an embedding provider is configured. The documentation explicitly states there is no hidden remote state: "The agent remembers only what persists to disk in its workspace." This is the "client-side hybrid search" pattern Francisco Arceo referenced.

- **OpenAI Agents SDK (Sessions)**: The SDK offers both modes. Sessions (client-side) have the SDK manage conversation history locally, with multiple backend options: SQLite (default), Redis, MongoDB, PostgreSQL via SQLAlchemy, Dapr state stores. This is the "client-managed history" pattern.

### 3.2 Server-Side Memory

Server-side memory is managed by a remote service — the agent calls APIs to read and write memories; the storage and retrieval logic is fully abstracted from the agent.

- **OpenAI server-managed memory**: The Conversations API offers `conversation_id` and `previousResponseId` parameters that instruct OpenAI's infrastructure to manage state server-side. The Responses API launched server-side compaction in February 2026, automatically summarizing older context on OpenAI's servers. From the agent's perspective, state is opaque — OpenAI carries it forward between calls.

- **OpenAI's user-facing memory feature** (available to free and paid users as of March 2026): Automatically summarizes conversations and carries context across sessions for the consumer product. This is entirely server-side; users cannot inspect raw stored memories in the same way a developer can inspect files.

- **MemoryHub** (Red Hat AI Americas prototype): A server-side memory service accessed via MCP (streamable HTTP), Python SDK, or CLI. All memory operations — search, read, write, curation, contradiction detection — go to a centralized PostgreSQL+pgvector backend. Agents are clients of the memory service; they do not manage storage themselves.

### 3.3 Hybrid Approaches

Several patterns blend both sides:

- **Anthropic Claude Managed Agents + Dreaming** (May 2026): Agent execution is server-hosted, but the memory consolidation ("dreaming") runs as a scheduled background process on Anthropic's infrastructure, reviewing past sessions and rewriting the memory store. This is server-side in operation but developer-controlled in scope (up to 100 past sessions).

- **OpenClaw with cloud backends** (e.g., Honcho, LanceDB): The agent architecture is client-side, but the persistence backend is a remote service. The agent authors memory locally, which is synced to a remote store.

### 3.4 Implications of the Split

The client/server divide has direct consequences for platform design:

| Concern | Client-Side | Server-Side |
|---|---|---|
| **Data sovereignty** | Organization controls storage location and format | Data leaves the organization's environment |
| **Multi-agent sharing** | Hard — each agent has its own store; synchronization is manual | Native — all agents share one service |
| **Framework lock-in** | Low — standard file I/O or generic APIs | Varies — may depend on provider's SDK |
| **Governance** | Organization's responsibility | Service provider's responsibility (with API controls) |
| **Air-gap deployability** | Yes — works without network | Requires self-hosting or on-premise deployment |
| **Observability** | Application-layer; no built-in audit | Centralized logs, audit trails possible |

Wes Jackson's platform-tier argument is essentially a case that server-side (or self-hosted server-side) is the correct model for enterprise agents: client-side memory cannot meet multi-agent sharing, governance, and data-residency requirements at scale. Harrison Chase (LangChain) and Sarah Wooders represent the opposing single-agent perspective: agents should own their memory within their harness for portability and autonomy. The RHOAI context is unambiguously the platform tier, which gives weight to the server-side/self-hosted approach — but the client-side hybrid search pattern (OpenClaw, MemoryHub's MCP surface) remains relevant for individual-developer and IDE-embedded agents in the developer workflow.

---

## 4. The Four-Type Memory Taxonomy

**REFERENCE** — The dominant taxonomy in current agent memory literature is the four-type model derived from cognitive science and formalized for LLM agents by the CoALA paper (Sumers et al., arXiv:2309.02427, 2023). It is used — with minor variations in labeling and scope — by Oracle, IBM, Atlan, academic surveys (Du 2026, Jiang et al. 2026), and most major agent frameworks. The CoALA paper explicitly builds on classical cognitive architectures: Soar (production rules) and ACT-R (declarative/procedural memory distinction).

### 4.1 Working Memory (In-Context Memory)

Working memory is everything the agent actively reasons over during a single inference call: the system prompt, current conversation history, tool outputs, retrieved documents, and any intermediate scratchpad content. It is bounded by the context window. It is temporary and session-bound — nothing persists across inference calls without an explicit write action.

**Practical significance:** Working memory is the only memory the model directly reasons over. All other memory types are external to the model's computation and must be explicitly retrieved into working memory before they can influence reasoning. The design question for context engineering is: what goes in, in what order, and at what cost?

Oracle's finding *(Oracle blog returned HTTP 403; figures via search summaries — see Sources)*: an 80-turn conversation held flat at ~1,300 tokens per request by using memory-augmented retrieval, versus ~13,900 tokens growing unboundedly with a flat transcript — a 9.5x context efficiency difference. The quality judgment also favored the retrieved approach: a retrieved context card focuses the model; a sprawling transcript dilutes attention.

**Note on terminology:** Oracle calls this "working memory" in their taxonomy. Weaviate and some practitioners distinguish *working memory* (task-specific intermediate state for multi-step processes) from *short-term memory* (the immediate conversation context). IBM and most frameworks collapse these. The distinction is not settled.

### 4.2 Semantic Memory

Semantic memory stores durable, de-contextualized facts and knowledge: user preferences, entity properties, domain terminology, canonical definitions, structured reference data, and accumulated world knowledge. It is independent of any specific interaction — it stores *what is true* rather than *what happened*.

Examples: "The user prefers Python over Java," "Project X uses PostgreSQL 15," "The FIPS 140-3 standard requires encrypted connections."

**Storage patterns:** vector stores (for similarity search over unstructured facts), relational databases (for structured reference data), knowledge graphs (for entity relationships). Most production systems use more than one.

**Relation to Peter's area 1 (Agent Knowledge):** Semantic memory is the closest match to Peter's org-wide knowledge layer — it covers policies, product knowledge, regulations, and structured reference information. However, the CoALA and Oracle framing treats this as one type within a unified memory model, not a separate "knowledge" system. Whether org-level knowledge warrants its own governed system (closer to enterprise RAG) or can be addressed by a promoted tier within a memory substrate is one of the core open questions for RHOAI (Q40, Q41).

### 4.3 Episodic Memory

Episodic memory stores specific past experiences: what happened in a prior session, which decisions were made and when, which errors were encountered, what feedback was received. It is *event-indexed* — timestamped records of agent activity across sessions.

Examples: "On 2026-04-15, the agent attempted to deploy to production cluster X and encountered RBAC permission error Y," "In session 3 of project Z, the user asked to change the code style from tabs to spaces."

**Why it matters:** Without episodic memory, long-running agents restart their understanding of the project at every session. With it, agents can pick up where they left off, avoid repeating past mistakes, and demonstrate continuity that builds user trust. This is the capability Anthropic's "Claude Dreaming" feature is designed to improve — consolidating episodic records across up to 100 past sessions into a structured, current memory store.

**Hard benchmark results *(Oracle figures via search summaries — blog returned HTTP 403; see Sources)*:** Oracle reported an overall LongMemEval score of 93.8% (469/500), with per-category figures of 96% on temporal reasoning and 88% on multi-session tasks (those two are subcategory results, not the headline). Mem0's 2026 algorithm scored 93.4 overall on the same benchmark — essentially tied with Oracle — with the largest improvements on temporal reasoning (+29.6 points) and multi-hop recall (+23.1 points). RHOAI should expect multi-session performance to be the hardest category.

### 4.4 Procedural Memory

Procedural memory stores behavioral rules, guidelines, executable skills, and learned procedures: how to perform recurring tasks, which tools to use in which sequences, business process rules, workflow templates.

Examples: system prompts encoding behavioral constraints, tool-routing logic, reusable skill definitions (Meta's "Skills as Markdown"), decision trees for common scenarios.

**Key tension — where procedural memory lives:** Procedural memory is often encoded directly in the agent's system prompt or harness configuration (static), rather than in an external queryable store (dynamic). The CoALA framing and Oracle include it in the memory taxonomy explicitly; the MemoryHub architecture stores it separately from the PostgreSQL+pgvector operational memory. MLflow's nascent skills registry (github.com/B-Step62/mlflow, branch skill-registry-mvp — an unmerged prototype fork, per `docs/knowledge-registry.md`) addresses procedural memory as version-controlled skill artifacts. How RHOAI draws the line between *skills-as-registry-artifacts* and *procedural-memory-in-a-memory-service* is a design decision with direct cross-domain implications.

Atlan notes: procedural memory "is the least discussed memory type because it is often built directly into agent architecture." This may understate its importance: as agents gain long-running autonomy, dynamically querying and updating procedural memory (e.g., learning more efficient workflows, updating business rules) becomes a platform capability rather than a startup configuration step.

### 4.5 Taxonomy Variants and Contradictions

**Contradiction 1 — Three vs. four types:** Mem0's production implementation uses three types (episodic, semantic, procedural), folding working memory into the session/context management concern. This is a practical simplification that decouples memory management from inference-time context assembly — but it means Mem0's architecture does not directly manage what the model sees in the context window, only what is stored outside it.

**Contradiction 2 — Four types vs. one substrate:** Oracle's central argument is that the four types are not four systems but four *access patterns* over one governed database. MemoryHub is architecturally similar: all memory types flow through one PostgreSQL+pgvector backend. This contrasts with architectures that bolt together a vector store (semantic), a document log (episodic), and a key-value cache (working), which can create consistency problems across stores.

**Contradiction 3 — Emerging fifth type:** Atlan (2026) identifies "organisational context memory" as a distinct category that the standard four-type taxonomy omits — covering certified assets, data-event history, versioned access policies, and cross-system entity identity resolution. *(Caveat: Atlan is a data-catalog vendor and this claim originates from their marketing blog; it is not corroborated by an academic or independent source — treat as practitioner opinion.)* This is not the same as semantic memory because it requires runtime governance enforcement (not just fact retrieval) and lineage tracking. If RHOAI adopts this framing, the AI Asset Registry itself becomes a memory subsystem — specifically, the governed organisational context store. This would significantly expand the scope of what the AI Asset Registry does.

**Contradiction 4 — CoALA as ground truth:** Academic surveys and vendor implementations all cite CoALA, but CoALA was published in 2023 against a landscape of much smaller context windows (4k–32k tokens). With 128k+ context windows now standard, some CoALA-designed patterns (especially for working memory management) are less critical for single-session tasks. The Jiang et al. arXiv paper (2026) explicitly notes "benchmark saturation risk" — datasets under 1M tokens may no longer require external memory given modern context window sizes. The hard memory problems are multi-session, multi-agent, and governance, not single-session recall.

---

## 5. Why Definitions Matter for RHOAI Scoping

**EXPLORATORY** — The definitional questions above are not academic. Each unresolved term ambiguity maps directly to a platform scoping decision:

### 5.1 Scope of RHAISTRAT-1345

The Outcome as currently scoped covers: short-term conversation state, long-term knowledge persistence, context compaction, and memory abstractions across frameworks. This maps cleanly to the four-type model (working + episodic + semantic + some procedural) and to the server-side memory-service pattern.

What is **not** clearly in scope: the org-wide graph knowledge layer (Peter's area 1). If this is treated as semantic memory in a unified substrate, it belongs in this Outcome. If it is treated as enterprise RAG — external knowledge retrieval with governance — it may warrant a separate Outcome or extend the existing Knowledge Sources asset type in the AI Asset Registry.

**Recommendation for research:** Phase 2 of this research series should evaluate whether MemoryHub's five-tier scope model (user/project/role/organizational/enterprise) can serve both purposes — making the "one substrate vs. two systems" question an architecture question, not a scope question.

### 5.2 Memory Service vs. RAG Service

If RHOAI provides both a memory primitive and a knowledge retrieval (RAG) capability, their APIs, storage backends, and governance models will differ. The memory service is append-heavy, governed, with audit and retention. The RAG service is batch-indexed, read-optimized, with document-level provenance. Conflating them in a single platform feature will produce an architecture that serves neither well.

Wes Jackson's formulation is actionable: "Memory needs dynamic, append-heavy architectures with consistency semantics, access controls, audit trails, retention policies — database concerns, not search concerns." If RHOAI ships a "knowledge layer" that is implemented as a search index, it will not meet the memory requirements. If it ships a "memory service" that is optimized for search over large corpora, it will not perform well as a knowledge retrieval layer.

### 5.3 Client-Side vs. Server-Side Determines Feature Shape

The client/server divide is not primarily a technical decision — it is a governance and deployment model decision. An RHOAI memory service:
- Must be **self-hosted on OpenShift** to meet Red Hat's on-premise, air-gapped, and data-sovereignty requirements.
- Should expose a **standard interface** (MCP is the natural choice given the platform direction) so that both client-side agent tools (IDE agents, dev-workflow agents) and server-side platform agents can access the same memory store.
- Should support **multi-agent sharing** as a first-class feature, not an afterthought — the platform tier use case requires it.

The MemoryHub architecture (MCP access surface + PostgreSQL+pgvector backend + RHOAI vLLM embedding) is the closest existing Red Hat artifact for this pattern.

### 5.4 Procedural Memory and the Skills Registry

The overlap between procedural memory and the skills registry requires an explicit design decision. If RHOAI ships a skills registry (via MLflow upstream, per github.com/B-Step62/mlflow branch skill-registry-mvp — an unmerged prototype) and a memory service, some procedural memory will be addressed by the skills registry (versioned, governed skill artifacts) and some by the memory service (dynamic behavioral rules learned through agent operation). These must be designed with clear handoff points — otherwise teams will implement the same capability in two places.

### 5.5 Context Engineering as a First-Class Feature

Meta's progressive disclosure, Oracle's summarization threshold, Anthropic's compaction + memory combination, and OpenAI's server-side compaction all implement context engineering as a measurable, tuneable feature — not as a byproduct of memory management. RHOAI should treat context compaction (RHAISTRAT-1345 acceptance criterion) as a distinct platform primitive with its own quality metric (token efficiency, quality retention) rather than as an incidental benefit of memory persistence.

---

## 6. Open Questions (Forwarded to Research Series)

These questions are registered in `docs/knowledge-registry.md` (Q40–Q44) and remain unresolved pending the full research series:

**Q40 — Taxonomy validation:** Is Peter's 3-area split (Agent Knowledge / Agentic Memory / Context Engineering) the right decomposition, or should it be replaced by the CoALA four-type model? *(See [07 Taxonomy & Decomposition](07-taxonomy-and-decomposition.md))*

**Q41 — Memory vs. RAG boundary:** Are "Agent Knowledge" (org graph layer) and "Agentic Memory" (learned agent state) genuinely distinct subsystems requiring different architectures, or can they be addressed by one governed substrate? *(See [04 Technical Patterns](04-technical-patterns.md))*

**Q42 — Outcome scope:** Should RHAISTRAT-1345 be expanded to cover the org-wide knowledge layer, or should that be a separate Outcome? *(See [08 RHOAI & OCP Alignment](08-rhoai-ocp-alignment.md))*

**Q43 — Client vs. server-side:** Which side should RHOAI's memory primitives live on, and should the platform support both? *(See [04 Technical Patterns](04-technical-patterns.md))*

**Q44 — Unified substrate:** What is RHOAI's equivalent of Oracle AI Database or PostgreSQL+pgvector as a memory backend, and how does it relate to the existing AI Asset Registry Knowledge Sources asset type? *(See [08 RHOAI & OCP Alignment](08-rhoai-ocp-alignment.md))*

---

## Sources

### Internal (Repository)

| Source | Type | Path/Reference |
|---|---|---|
| Agent Memory & Knowledge working doc | Internal seed document | `docs/knowledge-review/assets/agent-memory-knowledge.md` |
| Knowledge Registry — Section 13, Q40–Q44 | Open questions | `docs/knowledge-registry.md` |
| RHAISTRAT-1345 | Jira Outcome | https://redhat.atlassian.net/browse/RHAISTRAT-1345 |
| When Agent Memory Becomes a Platform Concern | Wes Jackson (Red Hat SSA), 2026-05-01 | https://medium.com/@wjackson_63436/when-agent-memory-becomes-a-platform-concern-4b6cd23af47f |
| MemoryHub prototype | Red Hat AI Americas, Apache 2.0 | https://github.com/redhat-ai-americas/memory-hub |
| Oracle AI Agent Memory blog (seed) | Richmond Alake, Oracle, 2026-05-01 | https://blogs.oracle.com/developers/oracle-ai-agent-memory-a-governed-unified-memory-core-for-enterprise-ai-agents *(403 on fetch — summary from seed doc)* |

### External — Academic and Technical References

| Source | Type | URL |
|---|---|---|
| CoALA: Cognitive Architectures for Language Agents | Academic paper (canonical taxonomy) | https://arxiv.org/abs/2309.02427 |
| Anatomy of Agentic Memory (Jiang et al., arXiv:2602.19320) | Academic survey, 2026 | https://arxiv.org/html/2602.19320v1 |
| Memory for Autonomous LLM Agents (Du, arXiv:2603.07670) | Academic survey, March 2026 | https://arxiv.org/html/2603.07670v1 |
| State of AI Agent Memory 2026 (Mem0) | Industry benchmark report | https://mem0.ai/blog/state-of-ai-agent-memory-2026 |
| Types of AI Agent Memory: Episodic, Semantic, Procedural and More (Atlan) | Reference article | https://atlan.com/know/types-of-ai-agent-memory/ |
| AI Memory System vs RAG (Atlan) | Reference article | https://atlan.com/know/ai-memory-system-vs-rag/ |
| The Evolution from RAG to Agentic RAG to Agent Memory (Monigatti) | Reference article | https://www.leoniemonigatti.com/blog/from-rag-to-agent-memory.html |
| RAG vs Memory for AI Agents (Memorilabs) | Reference article | https://memorilabs.ai/blog/rag-vs-memory-for-ai-agents/ |
| Context Engineering — LLM Memory and Retrieval for AI Agents (Weaviate) | Reference article | https://weaviate.io/blog/context-engineering |
| Anthropic Memory Tool documentation | Provider documentation | https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool |
| OpenAI Agents SDK — Sessions (client/server memory) | Provider documentation | https://openai.github.io/openai-agents-python/sessions/ |
| OpenClaw Memory documentation | Framework documentation | https://docs.openclaw.ai/concepts/memory |
| How We Built an AI Second Brain for 60K Knowledge Workers (Meta) | Case study | https://medium.com/@AnalyticsAtMeta/how-we-built-an-ai-second-brain-for-60k-knowledge-workers-78c507dd795b |
| Agent Memory — Why Your AI Has Amnesia (Oracle/Casius Lee) | Vendor blog | https://blogs.oracle.com/developers/agent-memory-why-your-ai-has-amnesia-and-how-to-fix-it *(403 on fetch — used search summary)* |
| IBM — What Is AI Agent Memory | Vendor reference | https://www.ibm.com/think/topics/ai-agent-memory *(403 on fetch — used search summary)* |
| OpenAI Responses API — Server-Side Compaction (2026-02-11) | News summary | https://aitoolly.com/ai-news/article/2026-02-11-openai-enhances-responses-api-with-server-side-compaction-hosted-shell-and-agent-skills-for-long-ter |
| Anthropic Claude Dreaming — Memory Consolidation Feature | News coverage | https://www.mindstudio.ai/blog/what-is-claude-dreaming-anthropic-managed-agents |
| Wes Jackson — Platform Concern article (fetched) | Industry opinion, 2026-05-01 | https://medium.com/@wjackson_63436/when-agent-memory-becomes-a-platform-concern-4b6cd23af47f |

### Access Notes

The following sources returned HTTP 403 on direct fetch; content was obtained via web search summaries and internal seed documents:
- `blogs.oracle.com/developers/oracle-ai-agent-memory-a-governed-unified-memory-core-for-enterprise-ai-agents` (Oracle, Richmond Alake)
- `blogs.oracle.com/developers/agent-memory-why-your-ai-has-amnesia-and-how-to-fix-it` (Oracle, Casius Lee)
- `www.ibm.com/think/topics/ai-agent-memory` (IBM)

The Wes Jackson Medium article was successfully fetched and directly excerpted. Academic arXiv papers were successfully fetched. Provider documentation (Anthropic, OpenAI, OpenClaw) was successfully fetched.
