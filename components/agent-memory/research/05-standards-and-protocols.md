---
title: "Agent Memory & Knowledge: Standards and Protocols"
description: Standards and protocols landscape for agent memory and knowledge, and the open-standards/portability argument for Red Hat.
source: ai-asset-registry/agent-memory/research/05-standards-and-protocols.md (as of 2026-07-05)
timestamp: 2026-07-06
review_after: 2026-08-05
---

# Agent Memory & Knowledge: Standards and Protocols

**Purpose:** Map the standards and protocols landscape for agent memory and knowledge — what exists, what is emerging, what is absent — and make the open-standards / portability argument for why this gap matters strategically to Red Hat.

**Date:** 2026-05-17

**Status:** EXPLORATORY — research phase, no features scoped. See [RHAISTRAT-1345](https://redhat.atlassian.net/browse/RHAISTRAT-1345).

**Series:** Document 05 of 17 — Agent Memory & Knowledge Research
**Phase 1:** [00](00-executive-summary.md) · [01](01-landscape-and-definitions.md) · [02](02-solution-survey.md) · [03](03-memoryhub-deep-dive.md) · [04](04-technical-patterns.md) · 05 Standards & Protocols (this doc) · [06](06-ogx-memory-primitives.md) · [07](07-taxonomy-and-decomposition.md) · [08](08-rhoai-ocp-alignment.md)
**Phase 2:** [09](09-agent-harness-memory.md) · [10](10-claude-memory-dreaming.md) · [11](11-adversarial-memory.md) · [12](12-benchmarking-evaluation.md) · [13](13-kv-cache-optimization.md) · [14](14-enterprise-use-cases.md) · [15](15-multi-modal-memory.md) · [16](16-ai-gateway-memory-substrate.md) · [REVIEW-NOTES](REVIEW-NOTES.md)

---

## Contents

1. [Standards Landscape: Summary Verdict](#1-standards-landscape-summary-verdict)
2. [MCP as Memory Transport](#2-mcp-as-memory-transport)
3. [Adjacent Standards](#3-adjacent-standards)
4. [Governance Bodies and Memory Coverage](#4-governance-bodies-and-memory-coverage)
5. [The Portability and Open-Standards Argument](#5-the-portability-and-open-standards-argument)
6. [Gaps and the Standards Opportunity for Red Hat](#6-gaps-and-the-standards-opportunity-for-red-hat)
7. [Standards Coverage Matrix](#7-standards-coverage-matrix)
8. [Sources](#8-sources)

---

## 1. Standards Landscape: Summary Verdict

**REFERENCE** — There is no mature, ratified standard for agent memory interoperability as of May 2026. This is the single most important finding in this document.

The adjacent infrastructure layers are well-standardized: MCP (agent-to-tool; released Nov 2024 by Anthropic; AAIF/Linux Foundation project Dec 2025) and A2A (agent-to-agent; released Apr 2025 by Google; Linux Foundation project Jun 2025; v1.0 early 2026) provide a two-layer interoperability stack for how agents connect to external services and how agents coordinate with each other. But neither standard defines:

- A portable schema for agent memory records
- A standard wire format for transferring memory state between systems
- A protocol for reading or writing to a memory service
- A standard API surface for a memory backend

The memory layer sits between the transport standards (MCP, A2A) and the storage substrate (PostgreSQL, Redis, vector databases) — and it has no standards coverage. Teams building agent memory today are writing bespoke APIs, proprietary schemas, and vendor-specific SDK integrations.

**What exists in the memory standards space:**

| Category | Status | Description |
|---|---|---|
| **MCP as memory transport** | De facto pattern, no memory-specific convention | MCP is widely used to expose memory services to agents; no standard schema for memory tools |
| **Tool-based memory naming** | Weak de facto convention | Multiple implementations converge on similar verb patterns (`add_memory`, `search_memories`); not formalized |
| **AGENTS.md / CLAUDE.md context files** | De facto pattern, now under AAIF governance (AGENTS.md) | File-based procedural memory for coding agents; convergence in progress |
| **Open Responses specification** | Emerging specification, conversation-state focused | Standardizes agentic loop items and conversation continuation; not a memory format |
| **Portable Agent Memory (PAM)** | Academic research paper (arXiv:2605.11032, May 2026) | Full portability protocol proposal; not yet adopted by any product or governance body |
| **A2A contextId** | Specified in A2A v1.0 | Groups related tasks into a conversational context; does not define memory storage or schema |
| **NIST AI Agent Standards Initiative** | Early stage (Feb 2026) | Covers identity, security, interoperability; memory not explicitly addressed |
| **AAIF** | Governs MCP, goose, AGENTS.md (A2A is a separate Linux Foundation project, not AAIF) | No memory-specific working group or project as of May 2026 |

The absence of a memory standard is not a gap left by accident. It reflects the immaturity of the space: vendors are competing on memory as a differentiation layer, and no single actor has sufficient cross-industry trust to propose a standard that others would adopt. The conditions for standardization — market consolidation, clear abstraction boundaries, and shared pain from fragmentation — are not yet fully present.

**Why this finding matters for RHOAI:** A platform that ships memory primitives before standards converge gets to shape those standards. A platform that waits for standards to converge will inherit them. Red Hat's history with OpenShift, Kubernetes, and RHEL is the former pattern. See Section 6.

---

## 2. MCP as Memory Transport

**REFERENCE** — The most significant de facto standard in the memory space is the use of MCP as the transport layer for memory services. This pattern did not originate from an explicit standard; it emerged from the practical reality that MCP is the only widely-adopted protocol for exposing AI services to agents, and memory is a service.

### 2.1 The Pattern

The MCP-as-memory-transport pattern works as follows: a memory backend (typically PostgreSQL+pgvector, a vector store, or a key-value store) is wrapped in a FastMCP server that exposes memory operations as typed MCP tools. Any MCP-compatible agent framework — LangGraph, Claude Code, CrewAI, AG2 — can call these tools to read and write memories. The memory backend is decoupled from the agent framework.

**Examples of this pattern in production:**

- **MemoryHub (Red Hat AI Americas):** FastMCP 3 server exposing memory operations through configurable tool profiles (compact: 2 tools / 19 actions; full: 10 tools; minimal: 4 tools) over streamable HTTP, delegating to a PostgreSQL+pgvector backend with OAuth 2.1 auth. ([github.com/redhat-ai-americas/memory-hub](https://github.com/redhat-ai-americas/memory-hub))
- **Mem0 MCP Server:** Cloud-hosted MCP server with 9 tools (`add_memory`, `search_memories`, `get_memories`, `update_memory`, `delete_memory`, `delete_all_memories`, `get_all_memories`, and lifecycle hooks). Available as `mem0-mcp-server` on PyPI. ([docs.mem0.ai/platform/mem0-mcp](https://docs.mem0.ai/platform/mem0-mcp))
- **OpenMemory (Mem0):** Local-first MCP-compatible memory server; runs on-device and is compatible with Claude Desktop, Cursor, Windsurf, and VS Code. ([mem0.ai/openmemory](https://mem0.ai/openmemory))
- **Anthropic Reference Memory Server:** The official `modelcontextprotocol/servers` repository includes a `memory` reference server — a TypeScript implementation using a local knowledge graph (entities, relations, observations) persisted to JSONL. Licensed MIT. ([github.com/modelcontextprotocol/servers/tree/main/src/memory](https://github.com/modelcontextprotocol/servers/tree/main/src/memory))
- **Letta (formerly MemGPT):** MCP integration for its server-side persistent memory service, now supporting client-side MCP skills alongside server-side memory. ([letta.com](https://www.letta.com))

### 2.2 What MCP Provides — and What It Does Not

MCP provides the **transport and tool-invocation contract**, not the **memory schema**. When a memory service exposes itself via MCP:

- **Provided:** A standard way for agents to discover available tools (`tools/list`), invoke them (`tools/call`) with typed JSON Schema inputs, and receive structured outputs. Authentication, streaming, and session lifecycle are handled by the MCP protocol layer.
- **Not provided:** The names of memory tools, the schema of memory records, the semantics of what "adding a memory" means, the format of retrieved memories, or any contract about how memories relate to each other across providers.

This means that two MCP memory servers may both expose `search_memories` tools, but an agent designed against one cannot be pointed at the other without integration work — because the input schema, output format, and semantics differ.

### 2.3 The Emerging (Informal) Tool-Naming Convention

**EXPLORATORY** — Multiple independent implementations have converged on a loose naming convention for MCP memory tools. This convergence is informal — it has not been ratified by MCP's governance body (AAIF), is not in the MCP specification, and exists only as observed practice.

Commonly observed patterns:
- `add_memory` / `store_memory` / `create_memory` — write a new memory record
- `search_memories` / `search_memory` — semantic search over stored memories
- `get_memories` / `get_memory` / `read_memory` — retrieve specific or recent memories
- `update_memory` — modify an existing memory record
- `delete_memory` / `delete_memories` — remove memory records

This convergence is useful evidence that the abstraction is real — agents and memory systems independently arrived at similar verbs. But without a schema definition (what fields does a memory record have? what is the output format of `search_memories`?), this informal convention does not provide portability.

**The MemoryHub divergence:** MemoryHub's full profile exposes 10 tools — significantly more than the ~5-verb informal convention above — because it includes governance-specific operations (curation, contradiction detection, provenance, session management). (See doc 03 for full profile breakdown.) This reflects an enterprise-grade memory service design rather than a minimal memory primitive. Neither shape is wrong; they serve different audiences. But the divergence illustrates that the convention has not converged on scope.

### 2.4 MCP 2026 Roadmap: No Dedicated Memory Features

**REFERENCE** — The official 2026 MCP roadmap (published by the MCP blog) identifies four priority areas: transport evolution and scalability, agent communication (Tasks primitive), governance maturation, and enterprise readiness (audit, auth, config). There is no dedicated memory primitive, memory schema, or memory-specific working group in the 2026 MCP roadmap.

The roadmap does address **session state** as a transport concern — specifically how MCP sessions are created, resumed, and migrated during scale-out events (Transports Working Group, tentatively targeting a June 2026 specification cycle). This is infrastructure session management, not agent memory. The session ID becomes a routing key; it does not define a schema for what agents remember.

This is an important null result: the MCP specification body is not currently planning to standardize memory as part of the MCP protocol. Memory-via-MCP will remain a convention of tool-naming and informal practice unless an explicit memory-focused project is proposed to AAIF.

---

## 3. Adjacent Standards

### 3.1 A2A Protocol: Context Groups, Not Memory

**REFERENCE** — The A2A (Agent-to-Agent) protocol v1.0 introduced `contextId` as a first-class concept. A `contextId` logically groups multiple Task objects and Message objects that are part of the same conversational context. Tasks and messages with the same `contextId` are treated as part of the same conversational session. ([a2a-protocol.org/latest/specification](https://a2a-protocol.org/latest/specification/))

This provides **session-scoped task grouping**, not memory. The key distinctions:

- A `contextId` groups tasks happening *now*, in an ongoing interaction. It does not define how the agent remembers *past* interactions.
- A2A does not define a schema for what agents carry between contextId groups (i.e., cross-session memory).
- A2A does not specify any mechanism for reading or writing to a persistent memory store.
- When two agents communicate via A2A, there is no standard field in the AgentCard or the Task message for declaring the memory backend the agent uses, the schema of its memory records, or the scope of what it remembers.

**Relevant A2A fields for context:**
- `contextId`: Session grouping identifier (string)
- `history`: Optional task history within a context
- `metadata`: Arbitrary key-value pairs that clients and servers can use to pass custom information

The `metadata` field is the closest thing A2A has to an extensible context-passing mechanism — but it is untyped and not standardized for memory.

**Contradiction to flag:** Some sources describe A2A as enabling agents to "pass along relevant context (like memory, user preferences, or goals) when collaborating." This overstates what A2A specifies. A2A defines that agents *can* pass messages to each other; it does not define *what* those messages contain when memory is involved. The passing of memory *content* via A2A `metadata` or message payloads is an application-layer decision, not a protocol specification.

**Registry implication:** The Agent Registry (see `agents/agent-registry/research/02-standards-and-protocols.md`) stores A2A AgentCards. A memory-aware AgentCard extension — analogous to how the registry extended AgentSkill with parameter schemas — could declare a memory service binding, but this would be a registry-level extension, not A2A itself.

### 3.2 Open Responses Specification: Conversation State, Not Memory

**REFERENCE** — Open Responses is an open-source specification (and ecosystem) inspired by the OpenAI Responses API, enabling unified interfaces across multiple LLM providers (OpenAI, Anthropic, Gemini, local models via vLLM, Ollama, LM Studio). Partners include Hugging Face, Vercel, and local inference providers. ([openresponses.org/specification](https://www.openresponses.org/specification))

What Open Responses standardizes for state:

- **`previous_response_id`**: Clients can resume or extend an existing response without resending the full transcript. The server loads prior input and output as context.
- **WebSocket-persistent state**: Servers MAY maintain connection-local state for recent responses, enabling low-latency continuation.
- **`/responses/compact` endpoint**: Returns a condensed input window for context compression.
- **Item types**: Formalizes `message`, `function_call`, `reasoning`, and other atomic context units with round-trippable data structures.

What Open Responses does **not** address:
- Long-term cross-session memory persistence
- Memory schemas or memory record formats
- Cross-provider memory portability (its vendor-prefixed extension mechanism intentionally allows providers to differentiate)
- The semantic meaning of what an agent "knows" across sessions

**Assessment:** Open Responses is a step toward standardizing the conversational context window format — how in-flight inference state is represented and resumed. It is not a memory standard. It addresses working memory (what is in the context window right now) rather than episodic or semantic memory (what agents have learned across sessions). The two are complementary problems, not the same problem.

### 3.3 AGENTS.md and CLAUDE.md: De Facto Context File Convention

**REFERENCE** — AGENTS.md is a de facto convention for providing AI coding agents with persistent, project-specific operational guidance in a Markdown file placed at the root of a repository: build commands, coding conventions, testing rules, and behavioral constraints. It was contributed to AAIF (Linux Foundation) as a founding project in December 2025, by OpenAI. ([linuxfoundation.org/press](https://www.linuxfoundation.org/press/linux-foundation-announces-the-formation-of-the-agentic-ai-foundation))

**CLAUDE.md** serves the same function for Claude Code specifically. Meta's AI Second Brain (Analytics at Meta, 2026) built their entire context architecture on a hierarchy of `CLAUDE.md` files — root context for user identity, project-level files for specifics, enabling progressive disclosure (lean context first, deeper detail loaded on demand). *(See `docs/knowledge-review/assets/agent-memory-knowledge.md`, Section 5.)*

**What these conventions address:** Procedural memory — how agents behave on a project — and semantic memory about a project's context. They are read at session start and effectively act as a durable, human-curated memory injection.

**What they do not address:**
- Episodic memory (past events in prior sessions)
- Dynamic writes from agent interactions (these files are human-authored)
- Multi-agent sharing or cross-project memory

**Contradiction to flag:** The AGENTS.md specification is under AAIF governance, giving it the most formal standards backing of any memory-adjacent convention. But it is the *least* automated of all memory patterns — it requires human curation. The "behavioral context file" pattern addresses procedural memory for coding agents but does not generalize to the full memory taxonomy ([01 Landscape & Definitions](01-landscape-and-definitions.md), Section 4).

**Research note on name consistency:** The broader ecosystem has produced multiple variants — `MEMORY.md`, `SKILLS.md`, `CONTEXT.md`, `CONTEXT7.md` — each with informal conventions. This proliferation is evidence of unmet standardization needs rather than convergence. The AGENTS.md AAIF project specifically targets coding agent context rather than the broader memory problem.

### 3.4 Portable Agent Memory (PAM): Academic Research Protocol

**EXPLORATORY** — A May 2026 arXiv paper (arXiv:2605.11032), titled "Portable Agent Memory: A Protocol for Provenance-Verified Memory Transfer Across Heterogeneous LLM Agents," proposes Portable Agent Memory (PAM), the first full specification for cryptographically-verified, cross-provider agent memory transfer. This is academic research, not an adopted standard. It is included here because it is the most complete technical proposal yet for what a memory portability protocol would look like.

**PAM protocol components:**

| Component | Description |
|---|---|
| **Memory model** | Five types: Episodic (E), Semantic (S), Procedural (P), Working (W), Identity (I) — extending the CoALA four-type model with an Identity type for persistent persona attributes |
| **Merkle-DAG provenance** | Content-addressable entries using BLAKE3 hashing with parent references; tamper-evident derivation chains |
| **Capability-based access control** | Scoped authorization tokens supporting read, write, derive, and export permissions |
| **Injection-resistant re-hydration** | Seven-stage pipeline with structural framing, content escaping, and type enforcement against memory-mediated prompt injection |
| **Serialization** | JSON-first with optional CBOR binary; designed for universal language/framework compatibility |

**Reported evaluation results:**
- Transfer Continuity Score: 0.83–0.92 vs. 0.28–0.45 baseline (no-memory) across Claude, GPT-4, Gemini
- Re-Hydration Fidelity: semantic similarity ≥ 0.71 at 25% token compression
- Security: 100% tamper detection across 1,000 mutations; zero successful injections from 200 attack patterns
- Efficiency: 69% storage reduction vs. raw conversation logs; full pipeline < 13ms
- Tooling: Python SDK with 54 passing tests released alongside the paper

**Assessment:** PAM is the most technically complete proposal for a memory portability standard in the space. Its explicit addressing of prompt injection in memory transfer is particularly important for enterprise contexts. However, it is a research paper; it has not been proposed to AAIF, NIST, or any governance body. Its adoption depends on whether the authors or others pursue standardization, or whether a vendor implements it and drives de facto convergence. The five-type model (adding Identity to the CoALA four) and the Merkle-DAG provenance chain are notable design choices that extend beyond current industry practice.

**Contradiction to note:** PAM's academic framing uses "Identity memory" (persistent persona attributes and preferences) as a fifth type distinct from semantic memory. This is not the same as the Identity concept in A2A (agent authentication identity). The vocabulary overlap could cause confusion in implementation.

---

## 4. Governance Bodies and Memory Coverage

### 4.1 Agentic AI Foundation (AAIF) — Memory Not in Scope

**REFERENCE** — AAIF was formed December 9, 2025, as a directed fund under the Linux Foundation. It governs three projects: MCP (donated by Anthropic), goose (donated by Block), and AGENTS.md (donated by OpenAI). Red Hat joined as a Gold Member in February 2026. ([aaif.io](https://aaif.io/), [linuxfoundation.org/press/agentic-ai-foundation-welcomes-97-new-members](https://www.linuxfoundation.org/press/agentic-ai-foundation-welcomes-97-new-members))

A2A (Agent-to-Agent) is a separate Linux Foundation project, governed independently of AAIF. Google donated A2A to the Linux Foundation in June 2025, where it became the Agent2Agent Protocol Project. IBM's Agent Communication Protocol (ACP) merged into A2A in August 2025 under LF AI & Data governance, not AAIF. A2A reached v1.0 in early 2026. AAIF's three founding projects are MCP, goose, and AGENTS.md; A2A is not an AAIF project.

**On memory specifically:** The AAIF website highlights "AgentMemory" as a recent development in the ecosystem — an open-source project bringing persistent memory to Claude Code, Cursor, and Gemini CLI — but this is a third-party project leveraging AAIF-governed standards, not an AAIF project. There is no memory standards working group, no memory-specific SEP (Standards Enhancement Proposal) in the MCP roadmap, and no proposed memory project in the AAIF project lifecycle.

**AAIF's project submission process is open.** Organizations can submit project proposals via GitHub. This is the mechanism by which a Red Hat or community-sponsored memory standards project could enter AAIF governance.

### 4.2 NIST AI Agent Standards Initiative — Memory Not Explicitly Addressed

**REFERENCE** — NIST's Center for AI Standards and Innovation (CAISI) announced the AI Agent Standards Initiative on February 17, 2026. The initiative has three pillars: facilitating industry-led standards development, fostering community-led open-source protocol development, and advancing research in agent security and identity. ([nist.gov/artificial-intelligence/ai-agent-standards-initiative](https://www.nist.gov/artificial-intelligence/ai-agent-standards-initiative))

**What NIST covers that is adjacent to memory:**
- Agent identity and authorization — the NCC0E concept paper on "identity standards to enterprise agent use cases" (comment period closed April 2, 2026) asks whether existing standards (OAuth, SPIFFE, OIDC) suffice for AI agents. Memory access control is identity-adjacent.
- Agent audit trails — NIST's broader governance framework requires "records of what agents were allowed to do, what context they received, what decision they made." A memory audit trail is directly relevant.
- MCP security — NIST has indicated interest in MCP as a candidate for integrating security and identity controls; since MCP is increasingly used as a memory transport, NIST MCP security work is indirectly relevant.

**What NIST does not cover:**
- Memory schemas or formats
- Memory portability requirements
- Guidance on what a memory service should provide

**Assessment:** NIST's role is that of convener and facilitator — it does not create data-format standards. Even if NIST acknowledged memory as a concern, the output would be guidance and evaluation criteria, not a wire format or API contract. The gap NIST is most likely to fill is auditing and access-control requirements for memory systems — which aligns with the governance requirements in MemoryHub.

### 4.3 IEEE 2894-2024 — Not Applicable to Memory or Agent Capability Descriptions

**REFERENCE** — IEEE 2894-2024 (formerly project P2894) is the "Guide for an Architectural Framework for Explainable Artificial Intelligence (XAI)." It covers XAI requirements, XAI method types, and performance evaluation of AI systems for transparency and trustworthiness. It is NOT a standard for agent capability descriptions, agent memory storage, memory schema, or agent interoperability. Any prior reference to IEEE P2894 as a "semantic interoperability standard for agent capability descriptions" is incorrect. This standard has no relevance to the memory portability gap and is included here only to prevent misattribution. There is no ratified standard for agent capability descriptions as of May 2026.

### 4.4 Oasis Security Agentic Access Management (AAM) Framework — Memory-Adjacent

**REFERENCE** — Oasis Security (a cybersecurity vendor, unrelated to the OASIS Open standards body) AAM Framework (November 2025, updated March 2026) addresses security governance for autonomous agents but approaches memory indirectly: the principle "monitor actions" requires capturing every session (intent, policy, identity, activity, expiration). This is equivalent to requiring an episodic memory audit trail. The principle "retire fast" requires decommissioning agent access when agents are no longer active — which implies a defined lifecycle for agent memory records as well.

The AAM Framework does not define a memory schema or standard, but its principles have direct implications for what a memory service must support in a governed enterprise context. *(See `agents/agent-registry/research/02-standards-and-protocols.md`, Section 5.4 for full AAM details.)*

### 4.5 EU AI Act — Compliance Implications for Memory

**REFERENCE** — The EU AI Act transparency requirements (enforcement August 2026) are not a memory standard, but they create compliance requirements that memory systems must satisfy for high-risk AI applications: transparency about what data was used, audit trails, human oversight mechanisms, and data accuracy requirements. A memory service serving EU-deployed agents must support erasure, audit, and provenance. MemoryHub explicitly targets EU AI Act compliance. This compliance pressure may accelerate the adoption of memory governance conventions even before formal standards emerge.

---

## 5. The Portability and Open-Standards Argument

### 5.1 The Core Problem: Memory as a Vendor Moat

**REFERENCE** — Wes Jackson (Red Hat SSA, "When Agent Memory Becomes a Platform Concern," 2026-05-01) makes the most direct available formulation of this argument for the Red Hat audience:

> "An open-source, platform-level memory layer built on open standards (MCP for transport, standard database primitives for governance) gives organizations the flexibility to avoid lock-in."

The article explicitly argues that teams should "build bridges instead of moats" — that the platform vendors who treat memory as a shared infrastructure concern rather than a proprietary differentiation layer will win long-term enterprise trust.

The specific enterprise risk Jackson identifies: *"Switching models is cheap; switching memory is not."* An agent that has accumulated preferences, decisions, and operational context in a vendor's proprietary memory system is effectively locked into that vendor. The lock-in is not contractual (as with legacy software) but behavioral — the agent's accumulated knowledge is in a format only that vendor's system understands.

This is the "behavioral lock-in" problem documented by MindStudio (2026): "the agent has built up an operational model of your organization — your terminology, your preferences, your decision patterns, your exceptions — and that model exists only inside the vendor's system." A JSON dump of conversation logs does not capture what the agent *learned* from those conversations.

### 5.2 Why Data Portability Regulations Fall Short

**REFERENCE** — Existing data portability frameworks (GDPR Article 20, CCPA) were designed for structured personal data held in defined formats. They are insufficient for agent memory for three reasons:

1. **Behavioral understanding is not a data export.** GDPR can require a vendor to export conversation logs. It cannot require them to export the semantic understanding the model developed from those conversations. The embeddings, weight updates, and contextual representations encoding what an agent learned are proprietary model internals.

2. **Consent was designed for app-specific data silos.** When a single agent prompt triggers cascading memory writes across a dozen integrated services (as the New America brief documents), the consent model breaks down — "consent becomes diffuse and even more hollow." There is no regulatory standard for what disclosures are required when an agent updates persistent memory.

3. **There is no standard format to export to.** For GDPR data portability to work, there must be a receiving format. For model weights or embeddings, no such standard format exists for memory exports.

**The IAPP analysis** (2026) frames this as "behavioral lock-in as the next labor mobility issue" — professionals who build deeply integrated AI agent workflows at one organization cannot easily take those workflows to another, because the agent's behavioral memory lives in the employer's system.

### 5.3 The Enterprise Case for Platform-Level Memory

**REFERENCE** — New America's technology policy brief (2026) on MCP and agent memory makes a parallel institutional argument: standardization could lower switching costs and prevent AI monopolies — but "only if enforcement mechanisms prevent platforms from restricting API access or giving their own agents privileged integrations." They recommend memory portability requirements preventing lock-in as a long-term fairness intervention.

The $60M+ investment signal (documented in `docs/knowledge-review/assets/agent-memory-knowledge.md`, Section 6) — Mem0 ($24M), Letta ($10M), Interloom ($16.5M) — shows the market expects memory to become a value-capture layer. Bessemer Venture Partners flagged memory as a 2026 differentiation frontier. From Red Hat's perspective, this is the same dynamic that played out with container registries, service mesh, and MLOps platforms: a capability that vendors want to own as a proprietary moat, which is precisely when a neutral, enterprise-grade, open-source platform alternative creates the most value.

### 5.4 The RHOAI Context: On-Premise, Air-Gap, Data Sovereignty

**EXPLORATORY** — The portability argument lands differently for Red Hat than for SaaS providers. RHOAI's value proposition includes:

- **On-premise deployment:** Memory cannot leave the customer's data center. Proprietary cloud memory services (OpenAI server-side memory, Oracle AI Database) are not viable for air-gapped or data-sovereign deployments.
- **Data residency:** Healthcare (HIPAA), financial services (SOC2, PCI), and government (FedRAMP) customers require that accumulated agent knowledge be stored in systems the customer controls — not vendor-managed infrastructure.
- **Migration freedom:** Enterprise customers using Red Hat expect to be able to swap inference providers (from OpenAI to a self-hosted Llama model, for example) without losing their agents' accumulated operational knowledge.
- **Multi-vendor frameworks:** RHOAI supports LangGraph, CrewAI, AG2, LlamaStack, and other frameworks. A memory service that only works with one framework is not a platform primitive.

The MemoryHub prototype articulates this directly: "The same rigor you apply to API governance and data residency should apply to agent memory." The MCP transport layer is necessary but not sufficient — the governance, access control, and portability layer above it is the differentiated platform concern.

### 5.5 "Bridges Not Moats": The Standards Strategy

**EXPLORATORY** — Jackson's article uses a "bridges not moats" framing as an organizing concept (this is a characterization of the article's argument, not a verbatim quote from it). The strategic implication: the way to build an enterprise memory platform that customers trust is to build it on and toward open standards, so customers know they can always migrate. This is different from "wait for standards to exist" — it means:

1. **Build on the de facto standard (MCP transport)** where it exists
2. **Contribute to conventions becoming standards** — naming conventions, schema proposals, semantic definitions
3. **Participate in governance bodies** — Red Hat is already an AAIF Gold Member; the memory gap in AAIF is an opportunity
4. **Publish internal designs as open proposals** — MemoryHub's five-tier scope model and governance layer are potential contributions to an emerging standard

The alternative — building a proprietary memory format and API — produces short-term differentiation and long-term customer skepticism.

---

## 6. Gaps and the Standards Opportunity for Red Hat

### 6.1 The Four Unstandardized Layers

Applying the analysis above, four specific layers lack standards coverage:

| Layer | What Is Missing | Who Could Fill It |
|---|---|---|
| **Memory record schema** | No standard format for what a memory record contains (fields, types, metadata). No schema covering the four memory types (working/episodic/semantic/procedural) in a portable format. | AAIF (as a new project), arXiv PAM as a starting point |
| **Memory API surface** | No standard API contract for a memory service: what operations it exposes, what their inputs/outputs look like, what error semantics apply. The informal MCP tool-naming convention is the closest thing. | AAIF (as a MCP extension or new project) |
| **Memory scope / tenancy** | No standard for how memory is scoped: user-level, agent-level, project-level, organizational-level. MemoryHub's five-tier model is the most articulated proposal, but it is one implementation's design, not a cross-industry convention. | Community proposal |
| **Memory portability / migration** | No standard format for exporting and importing agent memory across providers. PAM (arXiv:2605.11032) is the only full technical proposal, and it is a research paper not yet submitted to any governance body. | Red Hat + AAIF, building on PAM |

### 6.2 The Three Most Actionable Standards Opportunities

**EXPLORATORY** — Based on the gap analysis and Red Hat's existing participation in the ecosystem (AAIF Gold Member, MemoryHub prototype, active in MLflow upstream, Wes Jackson's public positioning), three specific standards opportunities stand out:

**Opportunity 1: MCP Memory Convention SEP**

Submit a Standards Enhancement Proposal (SEP) to MCP's governance process proposing a minimal, opinionated convention for memory-as-MCP-service: a canonical tool set (names + JSON Schema definitions), a minimal memory record format, and a scope model. This would not require building a new protocol — it would formalize the de facto practice into a reference convention. The MemoryHub tool set and schema are a strong starting point.

**Opportunity 2: Memory Binding for A2A AgentCard**

Propose an optional extension to A2A's AgentCard schema declaring the memory services an agent uses: transport (MCP endpoint URL), scope (user/project/organizational), and access control model. This would make memory services discoverable in the agent registry and enable governance tooling to enforce memory access policies. Red Hat's agent registry work provides the governance context for why this matters.

**Opportunity 3: AAIF Memory Project**

Propose an AAIF project specifically for agent memory interoperability — a neutral governance home for a memory schema standard, memory API contract, and portability specification. This would follow the same model as MCP (Anthropic donated) and AGENTS.md (OpenAI donated): an implementation-backed contribution to a neutral foundation. MemoryHub (under Apache 2.0) is a credible contribution candidate.

### 6.3 Near-Term vs. Long-Term Positioning

**EXPLORATORY** — The absence of a memory standard is an opportunity, but the timeline is uncertain:

- **Near-term (12 months):** The MCP memory-transport pattern will continue as the de facto approach. Informal naming conventions may strengthen. No formal standard will be ratified in this window. Red Hat should build against MCP transport and contribute to the naming convention.
- **Medium-term (12–24 months):** Either AAIF or NIST will likely convene memory-specific work — NIST through audit/identity requirements, AAIF through a community project. Red Hat should be a contributor at the table, not a recipient of whatever standard others define.
- **Long-term (24+ months):** A memory standard — likely covering schema, API surface, and portability format — will likely exist and be referenced in compliance frameworks. Red Hat's RHOAI memory primitives should be positioned to comply or lead that standard.

**The risk of waiting:** If Red Hat ships a proprietary memory API for RHOAI and a standard emerges two years later, the migration cost to align with the standard falls on Red Hat engineering and on customers. The RHOAI team's existing pattern (MLflow Registry, A2A AgentCard, MCP spec) is to align with open standards early — the same discipline applied to memory avoids that migration cost.

---

## 7. Standards Coverage Matrix

The following matrix maps each standard or convention to its coverage of agent memory concerns:

| Concern | MCP | A2A | AGENTS.md | Open Responses | PAM (research) | NIST AASI | AAIF |
|---|---|---|---|---|---|---|---|
| **Memory transport / tool invocation** | Primary transport layer | None | None | None | None | None | Via MCP |
| **Memory tool naming convention** | Informal (no spec) | None | None | None | None | None | None |
| **Memory record schema / format** | None | None | None | None | Full proposal | None | None |
| **Memory API contract** | None | None | None | None | Partial | None | None |
| **Cross-session continuity** | None | contextId (in-session only) | None | previous_response_id (limited) | Full | None | None |
| **Procedural memory (coding agents)** | Via tools | None | Primary | None | Procedural type | None | Via AGENTS.md |
| **Memory portability / migration** | None | None | None | None | Full protocol | None | None |
| **Access control for memory** | Via MCP auth | securitySchemes | None | None | Capability tokens | Identity pillar | Via MCP auth |
| **Memory audit / provenance** | None | None | None | None | Merkle-DAG | Audit focus | None |
| **Memory scope / tenancy** | None | tenant field (agent scope) | Project scope | None | None | None | None |
| **Compliance (EU AI Act, HIPAA)** | None | None | None | None | None | Guidance | None |

**Reading the matrix:** The PAM research paper has the broadest *intended* coverage, but zero *adopted* coverage — it is a proposal, not a standard. MCP has the narrowest intended coverage (transport only) but the *highest* adoption coverage — it is the most real thing in the table. Every other row is either absent or nascent.

---

## 8. Sources

### Internal (Repository)

| Source | Path / Reference |
|---|---|
| Agent Memory & Knowledge working doc | `docs/knowledge-review/assets/agent-memory-knowledge.md` |
| Agent Registry: Standards & Protocols (sibling doc) | `agents/agent-registry/research/02-standards-and-protocols.md` |
| Agent Memory: Landscape & Definitions | `agent-memory/research/01-landscape-and-definitions.md` |
| Agent Memory: Technical Patterns | `agent-memory/research/04-technical-patterns.md` |
| RHAISTRAT-1345 (Outcome: Agent Memory Primitives) | https://redhat.atlassian.net/browse/RHAISTRAT-1345 |
| MemoryHub prototype (Red Hat AI Americas) | https://github.com/redhat-ai-americas/memory-hub |
| Wes Jackson: When Agent Memory Becomes a Platform Concern (2026-05-01) | https://medium.com/@wjackson_63436/when-agent-memory-becomes-a-platform-concern-4b6cd23af47f |
| Knowledge Registry (MCP / standards references) | `docs/knowledge-registry.md` |

### External — Protocols and Specifications

| Source | URL |
|---|---|
| MCP Specification (2025-11-25) | https://modelcontextprotocol.io/specification/2025-11-25 |
| MCP 2026 Roadmap (official blog) | https://blog.modelcontextprotocol.io/posts/2026-mcp-roadmap/ |
| MCP Reference Memory Server (Anthropic, MIT) | https://github.com/modelcontextprotocol/servers/tree/main/src/memory |
| A2A Protocol Specification v1.0 | https://a2a-protocol.org/latest/specification/ |
| A2A What's New in v1.0 | https://a2a-protocol.org/latest/whats-new-v1/ |
| Open Responses Specification | https://www.openresponses.org/specification |
| Open Responses — InfoQ announcement (2026-02-02) | https://www.infoq.com/news/2026/02/openai-open-responses/ |
| AAIF Home and Projects | https://aaif.io/ |
| AAIF Formation Announcement (Linux Foundation, Dec 2025) | https://www.linuxfoundation.org/press/linux-foundation-announces-the-formation-of-the-agentic-ai-foundation |
| AAIF 97 New Members (Red Hat joins, Feb 2026) | https://www.linuxfoundation.org/press/agentic-ai-foundation-welcomes-97-new-members |
| AGENTS.md Repository (AAIF project) | https://github.com/agentsmd/agents.md |
| Linux Foundation: A2A Protocol Project Launch (Jun 23, 2025) | https://www.linuxfoundation.org/press/linux-foundation-launches-the-agent2agent-protocol-project-to-enable-secure-intelligent-communication-between-ai-agents |
| ACP Joins Forces with A2A (LF AI & Data, Aug 2025) | https://lfaidata.foundation/communityblog/2025/08/29/acp-joins-forces-with-a2a-under-the-linux-foundations-lf-ai-data/ |
| IEEE 2894-2024: Guide for an Architectural Framework for Explainable AI (XAI) | https://standards.ieee.org/ieee/2894/11296/ |
| NIST AI Agent Standards Initiative | https://www.nist.gov/artificial-intelligence/ai-agent-standards-initiative |
| NIST AASI Announcement (Feb 17, 2026) | https://www.nist.gov/news-events/news/2026/02/announcing-ai-agent-standards-initiative-interoperable-and-secure |

### External — Research and Analysis

| Source | URL |
|---|---|
| Portable Agent Memory (PAM) — arXiv:2605.11032 (May 2026) | https://arxiv.org/html/2605.11032v1 |
| State of AI Agent Memory 2026 (Mem0) | https://mem0.ai/blog/state-of-ai-agent-memory-2026 |
| AI Agents and Memory: Privacy and Power in the MCP Era (New America OTI, 2026) | https://www.newamerica.org/oti/briefs/ai-agents-and-memory/ |
| AI Agents in 2026: MCP, Memory Limits, and the Interoperability Wall (Conectia) | https://conectia.pro/en/blog/ai-agents-mcp-interoperability-wall-2026 |
| What Is Behavioral Lock-In? (MindStudio, 2026) | https://www.mindstudio.ai/blog/what-is-behavioral-lock-in-persistent-ai-agents-switching-costs |
| The Enterprise Agent Portability Problem Is Coming (IAPP, 2026) | https://iapp.org/news/a/the-enterprise-agent-portability-problem-is-coming |
| Enterprise Agentic AI Landscape 2026: Trust, Flexibility, Vendor Lock-In (Kai Waehner) | https://www.kai-waehner.de/blog/2026/04/06/enterprise-agentic-ai-landscape-2026-trust-flexibility-and-vendor-lock-in/ |
| Mem0 MCP Server documentation | https://docs.mem0.ai/platform/mem0-mcp |
| OpenMemory (Mem0 local MCP server) | https://mem0.ai/openmemory |
| Memory in AI: MCP, A2A & Agent Context Protocols (Orca Security) | https://orca.security/resources/blog/bringing-memory-to-ai-mcp-a2a-agent-context-protocols/ |
| Tool-based Agent Memory: Why 2026 Benchmarks Favor It (Wire Blog) | https://usewire.io/blog/memory-as-tools-2026-agent-memory-pattern/ |
| Oasis Security AAM Framework (Nov 2025, updated Mar 2026) | https://www.oasis.security/blog/agentic-access-management-framework |

### Access Notes

- The Wes Jackson Medium article was successfully fetched and directly quoted. The exact phrase "bridges instead of moats" does not appear to be a verbatim quote from the article; the section heading in the article uses this framing as a structural organizing concept, not a named thesis. The direct quotes in Section 5 are verified from the fetched content.
- The Oracle AI Agent Memory blog (`blogs.oracle.com/developers/oracle-ai-agent-memory-a-governed-unified-memory-core-for-enterprise-ai-agents`) returned HTTP 403 on direct fetch; content cited via the seed document (`docs/knowledge-review/assets/agent-memory-knowledge.md`).
- PAM paper (arXiv:2605.11032) was successfully fetched and directly summarized.
- New America OTI brief was successfully fetched.
- Open Responses specification was successfully fetched.
- AAIF website was successfully fetched.
- NIST AASI page was successfully fetched.
- **Quality review correction (2026-05-17):** IEEE 2894-2024 (formerly P2894) was previously misidentified in Section 4.3 as a "semantic interoperability standard for agent capability descriptions." It is confirmed via the IEEE Standards website to be the "Guide for an Architectural Framework for Explainable Artificial Intelligence (XAI)." The section has been corrected to accurately describe the standard and note it has no relevance to agent memory.
- **Quality review correction (2026-05-17):** The claim "A2A is also governed under AAIF" in Section 4.1 was incorrect. Verified via Linux Foundation press releases: A2A was donated to the Linux Foundation in June 2025 as its own independent project; IBM's ACP merged into A2A in August 2025 under LF AI & Data. AAIF (formed December 2025) governs MCP, goose, and AGENTS.md only. Sections 4.1 and the summary table have been corrected.
