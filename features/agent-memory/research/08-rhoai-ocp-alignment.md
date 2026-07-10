---
title: "Agent Memory & Knowledge: RHOAI & OCP Alignment"
description: Maps agent memory and knowledge onto RHOAI/OpenShift architecture, sourcing options with trade-offs, and open questions for the review gate.
source: ai-asset-registry/agent-memory/research/08-rhoai-ocp-alignment.md (as of 2026-07-05)
timestamp: 2026-07-06
review_after: 2026-08-05
---

# Agent Memory & Knowledge: RHOAI & OCP Alignment

**Purpose:** Map agent memory and knowledge onto Red Hat's existing RHOAI / OpenShift architecture — component by component — establish the integration points and dependencies, lay out the sourcing options (build / productize MemoryHub / OGX-based / upstream-contribute / partner) with trade-offs and RHOAI release feasibility, and surface the open architectural questions for the review gate.

**Date:** 2026-05-17 (original); 2026-06-09 (§7–8, series navigation update)

**Status:** EXPLORATORY for the analysis; the sourcing options and the alignment recommendations in Sections 3–4 are **PROPOSED** — research recommendations for the review gate, not decided RHOAI design. Established RHOAI architecture facts (OGX/Llama Stack as the 3.5 Responses bridge; AI Gateway IPP framework; kagenti as the agent deployment primitive) are marked **DECIDED** or **REFERENCE**. Nothing here invents an RHOAI component, release date, or Jira key. See [RHAISTRAT-1345](https://redhat.atlassian.net/browse/RHAISTRAT-1345).

**Series:** Document 08 of 17 — Agent Memory & Knowledge Research
**Phase 1:** [00](00-executive-summary.md) · [01](01-landscape-and-definitions.md) · [02](02-solution-survey.md) · [03](03-memoryhub-deep-dive.md) · [04](04-technical-patterns.md) · [05](05-standards-and-protocols.md) · [06](06-ogx-memory-primitives.md) · [07](07-taxonomy-and-decomposition.md) · 08 RHOAI & OCP Alignment (this doc)
**Phase 2:** [09](09-agent-harness-memory.md) · [10](10-claude-memory-dreaming.md) · [11](11-adversarial-memory.md) · [12](12-benchmarking-evaluation.md) · [13](13-kv-cache-optimization.md) · [14](14-enterprise-use-cases.md) · [15](15-multi-modal-memory.md) · [16](16-ai-gateway-memory-substrate.md) · [REVIEW-NOTES](REVIEW-NOTES.md)
**Strategy:** [README](/features/agent-memory/strategy/strategy-overview.md) · [01 Agent Memory Strategy](/features/agent-memory/strategy/agent-memory-strategy.md) · [02 Use Cases & Personas](/features/agent-memory/strategy/use-cases-and-personas.md) · [03 Recommended Architecture](/features/agent-memory/strategy/recommended-architecture.md) · [04 RHAISTRAT-1345 Outcome Update](/features/agent-memory/strategy/rhaistrat-1345-outcome-update.md) · [05 RFE Roadmap](/features/agent-memory/strategy/rfe-roadmap.md)

---

## Contents

1. [Scope and Method](#1-scope-and-method)
2. [Where Agent Memory & Knowledge Fits the RHOAI/OCP Architecture](#2-where-agent-memory--knowledge-fits-the-rhoaiocp-architecture)
3. [Integration Points and Dependencies](#3-integration-points-and-dependencies)
4. [The Sourcing Options Matrix](#4-the-sourcing-options-matrix)
5. [Resolving the Doc-07 Forwarded Questions](#5-resolving-the-doc-07-forwarded-questions)
6. [Open Architectural Questions for the Review Gate](#6-open-architectural-questions-for-the-review-gate)
7. [Kagenti Integration](#7-kagenti-integration)
8. [Storage Backend Trade-offs](#8-storage-backend-trade-offs)
9. [Sources](#9-sources)

---

## 1. Scope and Method

**EXPLORATORY** — This document is the bridge between research and design. Documents 01–07 established *what* agent memory and knowledge is, *how* the industry builds it, *what* the candidate internal artifacts (MemoryHub, OGX) provide, and *how* the problem space should be decomposed. This document answers the platform question: **given RHOAI and OpenShift as they actually are in mid-2026, where does each piece of agent memory & knowledge land, what does it depend on, and how should Red Hat source it?**

The recommended decomposition from [07 Taxonomy & Decomposition](07-taxonomy-and-decomposition.md) §4 is the spine of this document. That decomposition is **PROPOSED**, not decided — but to map memory onto RHOAI at all, this document adopts it provisionally and flags where the mapping would change if the review gate rejects it. The decomposition (doc 07 §4.1):

- **Subsystem 1 — Agent Memory Substrate.** One governed store exposing the four CoALA access patterns (working, episodic, semantic, procedural). Append-heavy, agent-written.
- **Subsystem 2 — Context Engineering.** A capability layer tightly coupled to / operating over Subsystem 1: compaction, retrieval assembly, progressive disclosure, KV-cache-aware ordering.
- **Subsystem 3 — Agent Knowledge.** A distinct, adjacent governed/federated enterprise-knowledge layer (regulations, policies, product knowledge, code, processes) — enterprise-RAG / knowledge-graph-shaped, **not** semantic memory and **not** a fifth memory type.
- **Cross-cutting dimension 1 — Governance & Scope.** Scope tiers, RBAC, audit, erasure, contradiction detection, provenance, compliance.
- **Cross-cutting dimension 2 — Deployment model.** Client-side vs. server-side.

A constraint that governs everything below: the AI Asset Registry's organizing principle is **Registry = Governance, Catalog = Discovery** (`CLAUDE.md`; [core-concepts.md](https://github.com/solaius/ai-asset-registry/blob/main/docs/knowledge-review/architecture/core-concepts.md)). The registry holds metadata and policy linkage; it does not store the asset payload, and it does not enforce — gateways and controllers enforce ([core-concepts.md](https://github.com/solaius/ai-asset-registry/blob/main/docs/knowledge-review/architecture/core-concepts.md), "Gateway Enforcement"). Memory is the first AI asset type that is *itself a live, append-heavy datastore* rather than a metadata record pointing at one — this asymmetry is the central architectural tension of this document and is flagged explicitly throughout.

**Accuracy note.** Several RHOAI facts that bear on memory are still partially open in the internal docs themselves — the AI Gateway architecture is "~60% detailed" ([ai-gateway.md](https://github.com/solaius/ai-asset-registry/blob/main/docs/knowledge-review/components/ai-gateway.md)), the OGX/Llama Stack replacement has a decided *direction* but no execution plan ([ai-gateway.md](https://github.com/solaius/ai-asset-registry/blob/main/docs/knowledge-review/components/ai-gateway.md); `docs/knowledge-registry.md` Q38), and the MLflow plugin architecture is "proposed to Databricks; revisions requested" ([06-rhoai-context.md](/features/agent-registry/research/06-rhoai-context.md) §7.2). Where an RHOAI fact is genuinely unknown, this document marks it as a review-gate question rather than inventing an answer.

---

## 2. Where Agent Memory & Knowledge Fits the RHOAI/OCP Architecture

This section walks the RHOAI/OCP stack component by component and places each subsystem of the doc-07 decomposition against it.

### 2.1 The AI Asset Registry and the Knowledge Sources asset type

**REFERENCE** — The AI Asset Registry already defines a fixed set of asset types: MCP Servers, Agents, Models, Prompts, Skills, Guardrails, and **Knowledge Sources** ([asset-types.md](https://github.com/solaius/ai-asset-registry/blob/main/docs/knowledge-review/assets/asset-types.md); `CLAUDE.md`). Knowledge Sources is described as *"Governed information sources for RAG, agents, retrieval workflows. May include documents, repositories, connectors, structured systems,"* with registry needs of *"Identity, version, source reference, access model, trust/governance context, refresh schedule"* ([asset-types.md](https://github.com/solaius/ai-asset-registry/blob/main/docs/knowledge-review/assets/asset-types.md)).

**PROPOSED — Subsystem 3 (Agent Knowledge) extends the Knowledge Sources asset type; it is not a new asset type.** Doc 07 §6.2 makes this recommendation directly: Knowledge Sources *"is described as 'governed info sources for RAG, agents, retrieval workflows' — exactly Subsystem 3's shape. Agent Knowledge should be built as the governed, federated realization of Knowledge Sources, not as a new parallel concept."* The fit is strong on three counts:

1. **Data shape match.** Knowledge Sources is read-mostly, batch-indexed, document-provenance-carrying — the same enterprise-RAG / knowledge-graph shape doc 07 §3.3 assigns to Agent Knowledge ([07](07-taxonomy-and-decomposition.md) §3.3; [01](01-landscape-and-definitions.md) §2).
2. **Registry-need match.** The Knowledge Sources registry-need list (`source reference`, `access model`, `trust/governance context`, `refresh schedule`) already covers what a governed org-knowledge layer needs; "refresh schedule" in particular is the batch-reindex cadence that distinguishes a knowledge source from an append-heavy memory store.
3. **Federation match.** The registry is explicitly a **federated** model ([core-concepts.md](https://github.com/solaius/ai-asset-registry/blob/main/docs/knowledge-review/architecture/core-concepts.md), "Federated Registry Model") — multiple backends under one governance framework — which is exactly what an org-wide knowledge layer spanning teams and source systems needs.

**The Agent Memory Substrate (Subsystem 1), by contrast, does not cleanly map to an existing asset type.** It is a live datastore, not a metadata record. Doc 07 §6.2 resolves this carefully: *"A memory record is itself a governed AI asset… the AI Asset Registry is the governed organizational store; the memory substrate and Knowledge Sources are governed asset types within the same governance framework. This is how 'Registry = Governance' extends to memory — not by making memory a registry, but by governing it with the same model."* In RHOAI terms: the memory **service** (the running PostgreSQL+pgvector-backed store) is a deployed workload; the memory service **instance** could be a registered asset (identity, version, endpoint, policy linkage, owning workspace) the same way an MCP server is — a metadata record pointing at a separately deployed service ([asset-types.md](https://github.com/solaius/ai-asset-registry/blob/main/docs/knowledge-review/assets/asset-types.md), MCP Server pattern). Whether *individual memory records* are also registry-governed assets, or only the service, is **Q-A1** (Section 6).

**Contradiction to flag.** There is a real tension between "Registry = Governance, registry does not store payload" ([core-concepts.md](https://github.com/solaius/ai-asset-registry/blob/main/docs/knowledge-review/architecture/core-concepts.md)) and the memory substrate, which *is* the payload. Knowledge Sources resolves cleanly (the registry points at the source; the source lives elsewhere — same as a model or MCP server). The Agent Memory Substrate does not: the governed thing and the live datastore are the same thing. This is why doc 07 §5 is emphatic that the AI Asset Registry is the *governance framework* memory is governed *by*, **not itself a memory subsystem** ([07](07-taxonomy-and-decomposition.md) §5). The substrate is a governed *workload*; the registry governs its identity, policy linkage, and lifecycle — but the substrate enforces its own row-level RBAC internally, as MemoryHub and OGX both already do ([03](03-memoryhub-deep-dive.md) §3.5; [06](06-ogx-memory-primitives.md) §2.3).

### 2.2 MCP Registry and the Agent Registry — pattern reuse

**REFERENCE** — The MCP Registry (RHOAI 3.5 Dev Preview target) establishes the governance pattern: a two-tier entity model (logical `MCPServer` asset + immutable `MCPServerVersion`), four independent governance tracks (lifecycle, approval, verification, certification), workspace-scoped RBAC, and metadata-first records ([mcp-registry.md](https://github.com/solaius/ai-asset-registry/blob/main/docs/knowledge-review/components/mcp-registry.md); [06-rhoai-context.md](/features/agent-registry/research/06-rhoai-context.md) §1). The Agent Registry reuses this pattern with a dual-state addition (governance state + runtime state) ([06-rhoai-context.md](/features/agent-registry/research/06-rhoai-context.md) §3.2, §6).

**PROPOSED** — A productized memory service should be a *governed asset* in this framework, registered the way an MCP server is:

- **Agent Memory Substrate** → the memory **service instance** is registered as an asset (analogous to the MCP Server two-tier model: a logical `MemoryService` asset + a versioned record carrying the deployment reference and governance metadata). The four governance tracks transfer: a memory service can be `Draft → Candidate → Published`, can require approval, can be verified and certified. This is the "store governed state first, automate behavior later" pattern doc [06-rhoai-context.md](/features/agent-registry/research/06-rhoai-context.md) §1 lists as transferring directly.
- **Agent Knowledge** → registered as a Knowledge Source asset (Section 2.1).
- **Relationship model.** [core-concepts.md](https://github.com/solaius/ai-asset-registry/blob/main/docs/knowledge-review/architecture/core-concepts.md) defines a relationship model where an agent references its component assets (model, prompt, MCP server, guardrail, knowledge source). A memory binding is a natural addition: an Agent asset should be able to declare *which memory service and which knowledge sources it uses* — the same way [05 Standards & Protocols](05-standards-and-protocols.md) §6.2 proposes a "Memory Binding for A2A AgentCard." This makes memory dependencies visible to governance tooling and enables impact analysis ("if this memory service is deprecated, which agents are affected?").

The MLflow **plugin architecture** ([06-rhoai-context.md](/features/agent-registry/research/06-rhoai-context.md) §4.6, §7.2) is the mechanism by which a memory-service asset type (or a Knowledge Source extension) would enter MLflow without building a bespoke vertical. Its approval status — "proposed to Databricks; revisions requested" — is a dependency, not a blocker, but it gates the *registry-side* of memory work.

### 2.3 OGX — the RHOAI 3.5 Responses bridge and its memory primitives

**DECIDED** — RHOAI 3.5 will GA the current Llama Stack implementation as a **bridge** for the Responses API; the architecture allows replacement within ~6 months ([ai-gateway.md](https://github.com/solaius/ai-asset-registry/blob/main/docs/knowledge-review/components/ai-gateway.md), "Responses API Re-Architected for Multi-Tenancy"; `docs/knowledge-registry.md` Q38). Llama Stack is now OGX ([06 OGX Memory Primitives](06-ogx-memory-primitives.md) §1.1) — the rename and mission expansion are confirmed by the OGX project, but the *internal RHOAI docs refer to the bridge as "Llama Stack"*; this document treats OGX and "the Llama Stack bridge" as the same codebase, as doc 06 establishes.

**REFERENCE** — OGX already ships production memory primitives that map to the CoALA four types ([06](06-ogx-memory-primitives.md) §5.1): Conversations API (episodic/working), Vector Stores + Files (semantic), Prompts API (procedural), `previous_response_id` chaining and background tasks (working), `POST /v1/responses/compact` and `context_management` (context compaction), and `AuthorizedSqlStore` ABAC row-level tenant isolation across all of them. This is the single most important alignment fact in this document: **the RHOAI 3.5 Responses bridge is, today, also a partial agent-memory substrate.** Subsystem 1 (working, episodic, procedural) and a meaningful slice of Subsystem 2 (compaction) already exist inside a component RHOAI is shipping in 3.5.

What OGX does *not* provide ([06](06-ogx-memory-primitives.md) §5.2): multi-tier scope isolation (it isolates per principal, not user/project/org), a knowledge graph, memory curation/provenance/contradiction detection, cross-session shared memory, an audit trail, retention/erasure policies, inspectable compaction, and FIPS/compliance certification. These gaps are precisely the **Governance & Scope** cross-cutting dimension of the doc-07 decomposition — and precisely what MemoryHub's design addresses ([03](03-memoryhub-deep-dive.md) §3; [06](06-ogx-memory-primitives.md) §6).

**The architectural placement.** OGX sits behind the AI Gateway as the Responses API implementation. Its memory primitives are therefore *gateway-adjacent session memory* — working/episodic memory bound to the agentic loop. The doc-07 decomposition's Subsystem 2 (Context Engineering) is "implemented inside the Responses API, not as a separate service" in OGX ([07](07-taxonomy-and-decomposition.md) §4.1; [06](06-ogx-memory-primitives.md) §3.3). This is a genuine constraint: if RHOAI adopts OGX primitives, context engineering is *coupled to the Responses API surface* by construction — which is consistent with doc 07's verdict that Context Engineering is a capability layer over the substrate, not an independent peer.

### 2.4 AI Gateway and MCP Gateway — the enforcement points

**DECIDED** — The AI Gateway is the unified gateway for all AI traffic, built on the **IPP (Inference Payload Processor)** plugin framework within Envoy; it serves four traffic types — model inference, tool calling/MCP, A2A, and external egress ([ai-gateway.md](https://github.com/solaius/ai-asset-registry/blob/main/docs/knowledge-review/components/ai-gateway.md); [system-boundaries.md](https://github.com/solaius/ai-asset-registry/blob/main/docs/knowledge-review/architecture/system-boundaries.md)). The MCP Gateway (Kuadrant) handles MCP protocol traffic specifically; the two are complementary, sharing Envoy/RHCL infrastructure ([mcp-gateway.md](https://github.com/solaius/ai-asset-registry/blob/main/docs/knowledge-review/components/mcp-gateway.md); [system-boundaries.md](https://github.com/solaius/ai-asset-registry/blob/main/docs/knowledge-review/architecture/system-boundaries.md)).

Two gateway facts place memory directly in the gateway's path:

1. **Group-based tenancy already extends to "vector stores" and "files."** The F2F DECIDED that the MaaS group-based subscription model is generalized across vector stores, file storage, MCP tool catalogs, guardrails, and evaluations ([ai-gateway.md](https://github.com/solaius/ai-asset-registry/blob/main/docs/knowledge-review/components/ai-gateway.md), "Group-Based Tenancy Extended Across the Stack"). Vector stores and files *are* OGX's semantic-memory substrate ([06](06-ogx-memory-primitives.md) §3.4). So the gateway's tenancy model already nominally covers part of the memory layer — but the gateway "establishes identity; each downstream microservice performs its own authorization" ([system-boundaries.md](https://github.com/solaius/ai-asset-registry/blob/main/docs/knowledge-review/architecture/system-boundaries.md)). The memory service is one of those downstream microservices: it receives an identity-bearing request from the gateway and must enforce its own scope-level RBAC. This is exactly MemoryHub's and OGX's model ([03](03-memoryhub-deep-dive.md) §3.5; [06](06-ogx-memory-primitives.md) §2.3) — the gateway is *not* the memory access-control point; it is the identity-establishment point.

2. **Conversation state, files, and vector stores become "independent microservices."** The gateway-native Responses replacement decomposes conversation state, files, vector stores, and tool catalogs into independent microservices for horizontal scaling ([ai-gateway.md](https://github.com/solaius/ai-asset-registry/blob/main/docs/knowledge-review/components/ai-gateway.md), decision 2). This is the post-3.5 architecture, and it is where a productized RHOAI memory substrate naturally lands: **the "conversation state microservice" of the gateway-native Responses implementation is the working/episodic slice of the Agent Memory Substrate.** Whoever owns that microservice owns part of Subsystem 1.

**Memory exposed via MCP — the gateway as enforcement point.** [05 Standards & Protocols](05-standards-and-protocols.md) §2 establishes MCP-as-memory-transport as the dominant de facto pattern; MemoryHub *is* an MCP server ([03](03-memoryhub-deep-dive.md) §2.1). A memory service exposed over MCP routes through the **MCP Gateway**, which provides identity-aware tool filtering, per-tool auth/authz via Authorino/RHCL, per-tool metrics, and audit logging ([mcp-gateway.md](https://github.com/solaius/ai-asset-registry/blob/main/docs/knowledge-review/components/mcp-gateway.md)). This is a clean fit: a memory MCP server's `memory(action="write")` and `memory(action="search")` tools become governed, audited, per-tool-authorized gateway tools. The MCP Gateway's planned **Content Guardrails** (TP, Apr 2026) and **MCP Registry integration** (GA, Q4 2026) extend directly to a memory MCP server — guardrails can scan memory writes at the gateway, and the registry can drive memory-server gateway configuration automatically ([mcp-gateway.md](https://github.com/solaius/ai-asset-registry/blob/main/docs/knowledge-review/components/mcp-gateway.md)).

**Compaction at the gateway.** The F2F flagged that "OpenAI auto-compaction cannot be reproduced exactly by the gateway" — the agreed approach is to detect compaction via a `response.compaction` flag and approximate via summarization ([ai-gateway.md](https://github.com/solaius/ai-asset-registry/blob/main/docs/knowledge-review/components/ai-gateway.md), "Conversation State Management"; `docs/knowledge-registry.md` Q35). OGX's `CompactionConfig` and `POST /v1/responses/compact` are the concrete implementation of this pattern in the bridge ([06](06-ogx-memory-primitives.md) §3.3). Context Engineering (Subsystem 2) therefore has a *named open design item inside the AI Gateway* — this is the most concrete near-term integration surface for memory work.

### 2.5 kagenti — the agent runtime

**REFERENCE** — kagenti is the Kubernetes-native agent lifecycle operator — the deployment primitive for agents on K8s, analogous to the MCP Lifecycle Operator for MCP servers ([06-rhoai-context.md](/features/agent-registry/research/06-rhoai-context.md) §6.5; `docs/knowledge-registry.md` "Kagenti"). It manages `AgentRuntime` and `AgentCard` CRDs and injects **SPIFFE identity** into agent workloads ([06-rhoai-context.md](/features/agent-registry/research/06-rhoai-context.md) §3.5, §6.5). RHOAI 3.5 status: Tech Preview ([06-rhoai-context.md](/features/agent-registry/research/06-rhoai-context.md) §6.5; `docs/knowledge-registry.md`).

kagenti is where agent *workloads* run, so it is where memory is *consumed*. Three integration facts:

1. **MemoryHub already has a kagenti integration design.** MemoryHub's three-phase kagenti plan — Phase 1 MCP connector registration, Phase 2 OAuth token exchange, Phase 3 ContextStore replacement — is documented but at "Design" status ([03](03-memoryhub-deep-dive.md) §1, §5.1, §5.5). There is also an early external consumer: `kagenti/adk` PR #231 consumes MemoryHub's `MemoryHubClient` ([03](03-memoryhub-deep-dive.md) §1). This is the first thin ecosystem-adoption signal — a single PR consuming a client library — not strong productization validation, but it confirms the IBM Python Agent Development Kit, used in kagenti, is an early MemoryHub SDK consumer.
2. **SPIFFE identity is the memory-access identity.** kagenti injects SPIFFE SVIDs into agent workloads ([06-rhoai-context.md](/features/agent-registry/research/06-rhoai-context.md) §3.5). The AI Gateway's Tier-2 agent identity is Spire/Authbridge with actor-chain tracking ([ai-gateway.md](https://github.com/solaius/ai-asset-registry/blob/main/docs/knowledge-review/components/ai-gateway.md), decision 4). A memory service should consume *that* identity — the agent's SPIFFE workload identity, carried through the gateway — as the principal for its scope-level RBAC. MemoryHub's standalone OAuth 2.1 server ([03](03-memoryhub-deep-dive.md) §3.5) is the productization gap here: it issues its own JWTs rather than consuming platform identity. Token exchange (RFC 8693) "for platform-integrated agents on RHOAI/kagenti is designed but not yet wired" ([03](03-memoryhub-deep-dive.md) §3.5) — this is the bridge between kagenti SPIFFE identity and a memory service's RBAC.
3. **The `AgentCard` is the discovery and binding surface.** The Agent Registry reads kagenti `AgentCard` CRDs as a discovery source ([06-rhoai-context.md](/features/agent-registry/research/06-rhoai-context.md) §6.5; `docs/knowledge-registry.md`). A memory binding declared on the AgentCard (per [05](05-standards-and-protocols.md) §6.2) would flow into the Agent Registry automatically and make agent→memory dependencies governable.

### 2.6 MLflow — the registry/governance backbone

**REFERENCE** — MLflow is the registry backend for MCP Servers, Agents, Prompts, and Skills; Kubeflow Hub is the catalog backend ([system-boundaries.md](https://github.com/solaius/ai-asset-registry/blob/main/docs/knowledge-review/architecture/system-boundaries.md), "Backend Registry Mapping"). MLflow already has a Prompt Registry ([asset-types.md](https://github.com/solaius/ai-asset-registry/blob/main/docs/knowledge-review/assets/asset-types.md); [platform-integration.md](https://github.com/solaius/ai-asset-registry/blob/main/docs/knowledge-review/integration/platform-integration.md)).

MLflow's role for memory is **governance metadata, not memory storage**. MLflow registers the memory *service* and the *knowledge sources*; it does not hold conversation state or memory records. This is consistent with "Registry = Governance" and with MLflow's existing role (it stores model/agent metadata, not the running model).

**One concrete reconciliation point — the Prompts overlap.** OGX has a Prompts API providing versioned, tenant-isolated procedural memory ([06](06-ogx-memory-primitives.md) §3.5); MLflow has a Prompt Registry asset type ([asset-types.md](https://github.com/solaius/ai-asset-registry/blob/main/docs/knowledge-review/assets/asset-types.md)). These are *two prompt-management surfaces at different layers* — OGX's is a runtime store an agent reads/writes at inference time; MLflow's is a governance registry. Doc 06 Q11 and doc 07 Q-T4 both forward this as an open question. **PROPOSED** — A proposed boundary (developed in Section 5, Q-T4 below; still an open question requiring agreement between the MLflow/skills team and the OGX/memory team): **MLflow Prompt Registry = governed, versioned, approved prompt artifacts; OGX Prompts API = runtime procedural-memory store; the substrate's procedural memory = dynamically agent-learned behavioral rules.** Three layers, one governance model — but where the handoff lines fall is a cross-team design question forwarded by doc 07 Q-T4, not a settled agreement.

### 2.7 Identity / SPIFFE and storage on OpenShift

**REFERENCE** — Agent identity in RHOAI is tiered: Tier 1 OpenShell token masking, Tier 2 Spire/Authbridge with actor-chain tracking and OPA policy enforcement ([ai-gateway.md](https://github.com/solaius/ai-asset-registry/blob/main/docs/knowledge-review/components/ai-gateway.md), decision 4). The Agentic Strategy's Govern & Secure pillar calls for agents to have verifiable identities (SPIFFE/SPIRE), fine-grained dynamic access control, on-behalf-of token exchange, and IdP integration (Keycloak/EntraID) ([governance-and-security.md](https://github.com/solaius/ai-asset-registry/blob/main/docs/knowledge-review/security/governance-and-security.md), "Agent Security (Zero-Trust)").

For memory, the actor-chain property matters: when agent A calls agent B, OPA enforces the **lowest permission level** across the chain ([ai-gateway.md](https://github.com/solaius/ai-asset-registry/blob/main/docs/knowledge-review/components/ai-gateway.md), decision 4). A memory service must respect this — a memory read performed by agent B *on behalf of* agent A's user must be scoped to the *intersection* of both actors' entitlements, or shared/organizational memory becomes a privilege-escalation vector. MemoryHub's scope model ([03](03-memoryhub-deep-dive.md) §3.1) and its explicit "cross-user writes are blocked as a security property" handle the single-actor case; the multi-actor chain case is a productization design item (**Q-A2**, Section 6).

**Storage on OpenShift.** Both candidate substrates are PostgreSQL-based. MemoryHub uses PostgreSQL + pgvector for relational, vector, and graph queries in one engine ([03](03-memoryhub-deep-dive.md) §2.3; [04](04-technical-patterns.md) §2.1). OGX's Vector I/O supports pgvector among nine backends, and its SQL stores run on SQLite or Postgres ([06](06-ogx-memory-primitives.md) §3.4). The OpenShift-native path is the **out-of-the-box PostgreSQL operator**; MemoryHub explicitly defers Apache AGE (openCypher) "pending validation with OpenShift's OOTB PostgreSQL operator" ([03](03-memoryhub-deep-dive.md) §2.3). The single-substrate pattern is the right default for an enterprise Kubernetes platform — it minimizes FIPS surface and operational sprawl ([04](04-technical-patterns.md) §2.1) — but only up to the ~50M-vector threshold ([04](04-technical-patterns.md) §2.1); above that, or for org-wide knowledge at 50–100M+ entities, the dedicated-store case strengthens ([04](04-technical-patterns.md) §2.2). This is why Subsystem 1 (bounded memory) and Subsystem 3 (org-wide knowledge) should *not* share a storage engine even though they share a governance model (doc 07 §3.3; addressed as Q-T5 in Section 5).

**FIPS and air-gap.** RHOAI's enterprise profile requires FIPS, air-gap, and data-residency support ([01](01-landscape-and-definitions.md) §5.3; [05](05-standards-and-protocols.md) §5.4). MemoryHub is designed for this — UBI9 base images, FIPS delegated to cluster OpenSSL, air-gap deployable with on-cluster embedding models on RHOAI vLLM ([03](03-memoryhub-deep-dive.md) §2.3) — but FIPS is *delegated, not validated end-to-end* ([03](03-memoryhub-deep-dive.md) §5.3 Gap 5). OGX has *no evidence of FIPS validation* in the repo ([06](06-ogx-memory-primitives.md) §5.2). FIPS is a productization gap for both candidates.

### 2.8 Component-by-component summary

| RHOAI/OCP component | Memory & Knowledge placement | Status of the fit |
|---|---|---|
| **AI Asset Registry — Knowledge Sources** | Subsystem 3 (Agent Knowledge) extends it directly | PROPOSED — strong fit ([07](07-taxonomy-and-decomposition.md) §6.2) |
| **AI Asset Registry — asset framework** | Memory *service* registered as a governed asset; memory *records* governed by the same model, not the registry | PROPOSED — fit, with the payload-vs-metadata tension flagged (§2.1) |
| **MLflow** | Registers the memory service + knowledge sources; does not store memory | REFERENCE fit; depends on plugin architecture (§2.6) |
| **OGX / Llama Stack bridge** (internal RHOAI docs call it "Llama Stack"; "OGX" is the upstream project's new name per doc 06) | Already ships working/episodic/procedural memory + compaction; the 3.5 substrate by default | DECIDED that OGX / Llama Stack is the 3.5 bridge; memory-primitive *exposure as governed RHOAI feature* is the gap (§2.3) |
| **AI Gateway (IPP)** | Identity-establishment point; "conversation state microservice" is Subsystem 1's working/episodic slice post-3.5 | DECIDED architecture; ~60% detailed (§2.4) |
| **MCP Gateway** | Enforcement point for memory exposed via MCP — per-tool authz, guardrails, audit, registry-driven config | REFERENCE fit; MCP-as-memory-transport is the de facto pattern (§2.4) |
| **kagenti** | Agent runtime — where memory is consumed; SPIFFE identity is the memory-access principal | REFERENCE; MemoryHub kagenti integration at "Design" status; `kagenti/adk` already consumes MemoryHub SDK (§2.5) |
| **Identity / SPIFFE / OPA** | Memory RBAC consumes platform identity; actor-chain lowest-permission rule applies to shared memory | REFERENCE; token exchange to a memory service not yet wired (§2.7) |
| **PostgreSQL on OpenShift** | Storage substrate for Subsystem 1 (pgvector single-substrate); Subsystem 3 may need a dedicated store at scale | REFERENCE; OOTB Postgres operator is the target; FIPS validation pending (§2.7) |

---

## 3. Integration Points and Dependencies

This section enumerates the concrete integration points and the dependencies each carries. Dependencies are the gating items for any sourcing path (Section 4).

### 3.1 The integration points

| # | Integration point | What flows | Direction |
|---|---|---|---|
| IP-1 | Memory service ↔ **MCP Gateway** | Memory tools (`write`/`search`/`curate`) exposed as governed, audited, per-tool-authorized MCP tools | Memory → gateway (registered backend) |
| IP-2 | Memory service ↔ **AI Gateway** | Identity-bearing requests; the "conversation state microservice" of the gateway-native Responses implementation | Gateway → memory (downstream microservice) |
| IP-3 | Memory service ↔ **OGX/Responses bridge** | Working/episodic memory via Conversations API; compaction via `/responses/compact`; `file_search` into vector stores | Bidirectional; OGX *is* part of Subsystem 1 in 3.5 |
| IP-4 | Memory service ↔ **kagenti** | Agent workloads consume memory; SPIFFE identity injected by kagenti is the RBAC principal; AgentCard carries the memory binding | kagenti → memory (consumer); memory binding → AgentCard |
| IP-5 | Memory service ↔ **MLflow / AI Asset Registry** | The memory service registered as a governed asset; agent→memory relationships recorded; Knowledge Sources extended for Subsystem 3 | Memory metadata → registry |
| IP-6 | Memory service ↔ **Identity (Spire/Authbridge/OPA)** | Token exchange (RFC 8693); actor-chain claims; lowest-permission enforcement for shared memory | Identity → memory |
| IP-7 | Memory service ↔ **vLLM serving on RHOAI** | Embedding model (e.g., `all-MiniLM-L6-v2`) and cross-encoder reranker served on RHOAI vLLM | Memory → vLLM (inference dependency) |
| IP-8 | Memory service ↔ **Guardrails / IPP plugins** | PII / prompt-injection scanning on memory writes; defense-in-depth at write path | Guardrails → memory write path |
| IP-9 | Knowledge layer ↔ **Catalog (Kubeflow Hub)** | Approved knowledge sources surfaced for discovery; consistent with registry→catalog pattern | Registry → catalog |

### 3.2 The dependencies, and their status

**EXPLORATORY** — Each integration point carries a dependency; several are not yet satisfied.

- **D-1 — MLflow plugin architecture (gates IP-5).** A memory-service asset type or a Knowledge Sources extension needs the generic asset-plugin framework, which is "proposed to Databricks; revisions requested" ([06-rhoai-context.md](/features/agent-registry/research/06-rhoai-context.md) §7.2). Without it, memory governance is a bespoke MLflow vertical — slower, but not blocked.
- **D-2 — OGX/Llama Stack replacement plan (gates IP-2, IP-3).** The replacement *direction* is DECIDED; the *execution plan* is not (`docs/knowledge-registry.md` Q38; [06](06-ogx-memory-primitives.md) §7 Q3). Whether the gateway-native Responses replacement reimplements memory primitives or delegates to OGX changes Subsystem 1's home.
- **D-3 — Token exchange to a memory service (gates IP-4, IP-6).** RFC 8693 token exchange "for platform-integrated agents on RHOAI/kagenti is designed but not yet wired" in MemoryHub ([03](03-memoryhub-deep-dive.md) §3.5). OGX's `AuthorizedSqlStore` consumes JWT claims and supports escaped-dot `claims_mapping` for K8s service-account tokens ([06](06-ogx-memory-primitives.md) §4.1) — OGX is closer here.
- **D-4 — MCP Registry → gateway automation (gates IP-1).** Automatic registry-driven gateway configuration is an MCP Gateway *GA Q4 2026* feature ([mcp-gateway.md](https://github.com/solaius/ai-asset-registry/blob/main/docs/knowledge-review/components/mcp-gateway.md)). Before GA, a memory MCP server is registered in the gateway manually.
- **D-5 — Kubernetes operator for the memory service.** MemoryHub's operator is a *skeleton* — current deployment is plain manifests + scripts ([03](03-memoryhub-deep-dive.md) §1, §5.3 Gap 1). OGX has no operator ([06](06-ogx-memory-primitives.md) §6). A Red Hat product cannot ship as manifests; an operator integrated with OLM is mandatory.
- **D-6 — Audit trail.** MemoryHub's audit log is a *stub interface* (issue #67), not wired through ([03](03-memoryhub-deep-dive.md) §3.4, §5.3 Gap 2). OGX has *no audit trail* — `AuthorizedSqlStore` enforces access control but produces no immutable log of reads/writes ([06](06-ogx-memory-primitives.md) §5.2). For EU AI Act (enforcement Aug 2026), GDPR, HIPAA, an audit trail is not optional ([05](05-standards-and-protocols.md) §4.5; [03](03-memoryhub-deep-dive.md) §5.3 Gap 2). **This is the single highest-severity gap for either candidate.**
- **D-7 — Observability.** MemoryHub observability is TBD — no Prometheus metrics, no Grafana dashboards ([03](03-memoryhub-deep-dive.md) §5.3 Gap 3). A product must be observable for SRE/support.
- **D-8 — FIPS end-to-end validation.** Delegated but not validated for MemoryHub; absent for OGX (§2.7).
- **D-9 — IP ownership.** MemoryHub copyright is held by Wes Jackson individually, not Red Hat ([03](03-memoryhub-deep-dive.md) §5.4). Productizing MemoryHub code requires a CLA or IP transfer — administrative, not a blocker, but a required step ([03](03-memoryhub-deep-dive.md) Q-MH-1).

### 3.3 Dependency-to-sourcing-path mapping

The dependencies do not weigh equally across sourcing paths. D-1/D-2/D-4 are *platform-readiness* dependencies that apply regardless of path. D-5/D-6/D-7/D-8/D-9 are *productization* dependencies that apply heavily to the "productize MemoryHub" path and lightly to the "OGX-based" path (because OGX is already in the production stack and Red Hat already contributes to it). This asymmetry is the core of the trade-off analysis in Section 4.

---

## 4. The Sourcing Options Matrix

**PROPOSED** — Five sourcing options for RHOAI agent memory & knowledge. They are *not mutually exclusive* — doc 06 §5.3 explicitly notes a likely path combines them across releases. The matrix evaluates each on its own, then Section 4.7 gives the synthesis.

### 4.1 Option A — Build fresh (RHOAI-native memory primitive)

Design and build a new RHOAI memory substrate from scratch, taking the *ideas* from MemoryHub and OGX but writing new, Red-Hat-owned code.

| Dimension | Assessment |
|---|---|
| **Trade-off — for** | Clean ownership; no IP transfer (D-9 moot); design exactly to the doc-07 decomposition and RHOAI's gateway/registry/kagenti architecture; no inherited prototype debt. |
| **Trade-off — against** | Slowest path. Discards working code: MemoryHub's six-tier scope model + SQL-level RBAC, cache-optimized assembly, inline curation are all production-capable today ([03](03-memoryhub-deep-dive.md) §5.2); OGX's compaction and multi-tenancy are in the production path already. Rebuilding from zero is the highest-cost, highest-schedule-risk choice. |
| **RHOAI release feasibility** | Not 3.5. Realistically 3.7+ for anything substantial; a thin working-memory primitive maybe 3.6 if scoped hard. |
| **Risk** | Schedule risk; rebuilding-the-wheel risk; market-timing risk — competitors (Mem0, Oracle, the hyperscalers) ship now ([02](02-solution-survey.md) §6). |

**Verdict:** Weakest standalone option. Build-fresh makes sense only for *components* with no existing artifact (e.g., the Subsystem-3 knowledge-graph layer, where neither MemoryHub nor OGX has a real implementation), not for the memory substrate as a whole.

### 4.2 Option B — Productize MemoryHub

Take the MemoryHub prototype, transfer IP to Red Hat, close the productization gaps, and ship it as the RHOAI memory primitive.

| Dimension | Assessment |
|---|---|
| **Trade-off — for** | Most architecturally complete *governance* model of any candidate — six-tier scope + SQL-level RBAC, contradiction detection, inline curation, version/provenance, cache-optimized assembly ([03](03-memoryhub-deep-dive.md) §3, §5.5). OpenShift-native by design (UBI9, FIPS delegation, air-gap). Apache 2.0, RHOAI vLLM integration, MCP-native. Already has a kagenti integration design and an early-ecosystem SDK consumer (`kagenti/adk` PR #231 — one PR, an early/thin signal per doc 03, not broad adoption validation). Directly realizes the doc-07 Governance & Scope dimension. |
| **Trade-off — against** | Heaviest productization burden: operator is a skeleton (D-5), audit trail is a stub (D-6), observability is TBD (D-7), FIPS unvalidated (D-8), IP held by an individual (D-9). Standalone OAuth server needs replacing with platform identity ([03](03-memoryhub-deep-dive.md) §5.3 Gap 4). Single-author prototype with no documented product engineering team ([03](03-memoryhub-deep-dive.md) §5.4). Six-tier scope model flagged as possibly over-complex ([03](03-memoryhub-deep-dive.md) §5.3 Gap 7). |
| **RHOAI release feasibility** | A *Dev Preview* of a MemoryHub-derived memory primitive could plausibly target **3.6**, given the core (CRUD + scope RBAC + curation) is already production-capable. **GA realistically 3.7+** — the audit trail and operator gaps are GA-blocking and cannot be hand-waved for a compliance-facing feature. |
| **Risk** | Productization-effort risk (six high-severity gaps); single-maintainer / bus-factor risk; the gaps that remain — audit, operator, observability — are exactly the unglamorous, schedule-consuming ones. |

**Verdict:** The strongest *governance* foundation, and the right source for the Governance & Scope dimension. But it is a prototype, and treating it as near-shippable would be a mistake — the gaps are real and GA-blocking.

### 4.3 Option C — Consume / extend OGX

Use OGX's memory primitives (Conversations, Vector Stores, Files, Prompts, compaction, `AuthorizedSqlStore`) as the RHOAI memory substrate, and add RHOAI governance on top.

| Dimension | Assessment |
|---|---|
| **Trade-off — for** | OGX is *already the RHOAI 3.5 Responses bridge* ([ai-gateway.md](https://github.com/solaius/ai-asset-registry/blob/main/docs/knowledge-review/components/ai-gateway.md)) — its memory primitives are in the production path with zero additional adoption decision. Production-grade primitives covering working/episodic/semantic/procedural memory + compaction + tenant isolation ([06](06-ogx-memory-primitives.md) §5.1). Large community (8,377 stars, Meta + Red Hat + community). Red Hat engineers (Francisco Arceo, Sébastien Han) are already core contributors ([06](06-ogx-memory-primitives.md) §4). OpenAI-API-conformant — interoperable. |
| **Trade-off — against** | OGX's memory model is *OpenAI-API-centric and per-principal* — no multi-tier scope, no knowledge graph, no curation/provenance/contradiction detection, no cross-agent shared memory, no audit trail, no retention/erasure, opaque-ish compaction, no FIPS ([06](06-ogx-memory-primitives.md) §5.2). These are exactly the enterprise-governance gaps. Adding multi-scope isolation may break OpenAI-API conformance ([06](06-ogx-memory-primitives.md) §5.3 Option A). The 6-month replacement clock means whatever is built on the *bridge* may need re-homing onto the gateway-native replacement. |
| **RHOAI release feasibility** | OGX memory primitives are *available in 3.5* as a side-effect of the bridge — but "available in the bridge" ≠ "a governed RHOAI memory feature." Exposing them as first-class, governed RHOAI memory features: **3.6**. The gateway-native re-home: post-3.5 / 3.6–3.7 ([ai-gateway.md](https://github.com/solaius/ai-asset-registry/blob/main/docs/knowledge-review/components/ai-gateway.md) roadmap). |
| **Risk** | Bridge-replacement risk (`docs/knowledge-registry.md` Q38, Risk 7 — dual-track maintenance); governance-gap risk (the hard enterprise requirements are the missing ones); API-conformance risk if governance is bolted on. |

**Verdict:** The fastest path to *some* memory capability and the lowest-friction technically — but it ships the *easy* half of memory (storage/retrieval/compaction) and leaves the *hard* half (governance) unsolved. OGX is a substrate, not a governed memory platform.

### 4.4 Option D — Upstream-contribute (governance primitives into OGX)

Continue the pattern Francisco Arceo's multi-tenancy work already established: contribute multi-scope isolation, audit logging, retention/erasure, and inspectable compaction *into OGX upstream* rather than building them separately ([06](06-ogx-memory-primitives.md) §5.3 Option C).

| Dimension | Assessment |
|---|---|
| **Trade-off — for** | Governance features land in the community project and Red Hat sets the de-facto standard — consistent with Red Hat's OpenShift/Kubernetes/RHEL pattern and with [05](05-standards-and-protocols.md) §5–6's "bridges not moats" argument. Builds on an *existing* Red Hat contribution channel (Arceo is already a core OGX contributor — [06](06-ogx-memory-primitives.md) §4, §5.4). No separate component to operate. Avoids fragmentation. |
| **Trade-off — against** | Upstream community consensus is *slower* than internal delivery ([06](06-ogx-memory-primitives.md) §5.3 Option C). OGX's charter is OpenAI-API conformance — multi-tier governance may be *out of scope* for OGX upstream, and the community may reject it. Red Hat does not control the schedule. Some enterprise features (FIPS, air-gap validation) are inherently downstream-RHOAI concerns that do not belong upstream. |
| **RHOAI release feasibility** | Cannot be schedule-committed to a specific release — upstream timelines are not Red-Hat-controlled. Realistically a 3.6→3.7 *contribution stream*, not a release deliverable. |
| **Risk** | Schedule-uncontrollability risk; upstream-rejection risk (governance may not fit OGX's charter); the features customers most need on a deadline are the ones least controllable upstream. |

**Verdict:** The right *strategic* posture for the standards layer and for the primitives that genuinely belong in a shared project — but it cannot be the *only* path, because the enterprise-governance and compliance features are exactly the schedule-critical, RHOAI-downstream-specific ones.

### 4.5 Option E — Partner with a memory vendor

License or integrate a third-party memory product (Mem0, Letta, Zep/Graphiti, Cognee) as the RHOAI memory backend.

| Dimension | Assessment |
|---|---|
| **Trade-off — for** | Fastest *feature* delivery — these products exist and ship today. Mem0 is the most deployment-flexible (self-hosted Docker, MCP surface, 21-framework support — [02](02-solution-survey.md) §2.1); Graphiti is the best open temporal-knowledge-graph engine ([02](02-solution-survey.md) §2.3). |
| **Trade-off — against** | *No external solution combines enterprise governance + Kubernetes-native self-hosted + open standard interface* — this is RHOAI's whitespace ([02](02-solution-survey.md) §8 Gap 1). Mem0's governance is thin; Letta is deprioritizing enterprise governance; Zep's self-hosted Community Edition is deprecated; Oracle requires Oracle Database lock-in ([02](02-solution-survey.md) §2–3). Market-consolidation risk: 5+ venture-backed startups converging — adopting one risks picking a non-survivor ([02](02-solution-survey.md) §6, §8 Gap 7). Partnering on a core platform primitive contradicts Red Hat's open-source platform value proposition ([05](05-standards-and-protocols.md) §5). |
| **RHOAI release feasibility** | Integration could be fast (3.6) — but as a *pluggable backend behind an RHOAI memory API*, not as the RHOAI memory platform itself. |
| **Risk** | Vendor-survival risk; governance-gap risk; lock-in / strategic-misalignment risk. |

**Verdict:** Weakest as a primary strategy. The defensible use of Option E is *backend-agnosticism* — [02](02-solution-survey.md) §8 Gap 7 recommends architecting the RHOAI memory layer to support pluggable backends (Mem0-compatible, LangGraph-Store-compatible, MemoryHub-native). Partner *compatibility*, not partner *dependency*.

### 4.6 The matrix

| Option | Speed to capability | Governance completeness | RHOAI-arch fit | IP / control | Earliest realistic GA | Primary risk |
|---|---|---|---|---|---|---|
| **A — Build fresh** | Slowest | Designed-in (none built) | Highest (designed to fit) | Full Red Hat ownership | 3.7+ | Schedule / rebuild-the-wheel |
| **B — Productize MemoryHub** | Medium (core done, gaps remain) | Highest of any candidate | High (OpenShift-native by design) | Needs IP transfer | 3.7+ (DP 3.6) | Six high-severity productization gaps |
| **C — Consume/extend OGX** ("OGX" = the codebase internal RHOAI docs call "Llama Stack"; see §2.3) | Fastest (already in 3.5 bridge) | Lowest (per-principal only) | High (already in the stack) | Community-owned | 3.6 (as governed feature) | Bridge-replacement; governance gaps |
| **D — Upstream-contribute** | Slow (consensus-bound) | Strategic (lands upstream) | High (via OGX) | Shared / community | Not release-committable | Schedule uncontrollable upstream |
| **E — Partner** | Fast (as pluggable backend) | Vendor-dependent (thin) | Low–medium | Vendor-owned | 3.6 (as backend) | Vendor survival; strategic misalignment |

### 4.7 Synthesis — the leaning the analysis surfaces

**PROPOSED** — The analysis does not point to one option; it points to a **phased combination**, which is what doc 06 §5.3 anticipated (*"short-term bridge via OGX primitives as-is (3.5), medium-term contribution of governance primitives upstream (3.6), long-term gateway-native implementation"*). The recommendation this document surfaces for the review gate:

- **3.5 (now):** OGX memory primitives ride along in the Responses bridge (Option C, passive). No new RHOAI memory deliverable — but the Conversations/Vector Stores/compaction primitives *exist* and should be acknowledged in scoping. This is a fact, not a choice.
- **3.6 (target):** Two parallel tracks. **(C+D)** Expose OGX's memory primitives as governed, first-class RHOAI memory features *and* upstream the governance primitives (audit hooks, scope attributes) where they fit OGX's charter. **(B, Dev Preview)** Stand up a MemoryHub-derived governance layer — the six-tier scope model, inline curation, contradiction detection — as the *governance service* that the doc-07 Governance & Scope dimension calls for, deployed as a Dev Preview alongside the OGX substrate. This is the doc-06 §6 synthesis made concrete: *OGX as the session-level working/episodic substrate; a MemoryHub-derived governance service as the organizational/long-term governed layer.*
- **3.7+ (GA):** The gateway-native Responses replacement absorbs the working/episodic substrate as its "conversation state microservice"; the MemoryHub-derived governance layer reaches GA with the D-5/D-6/D-7/D-8 gaps closed (operator, audit, observability, FIPS). Subsystem 3 (Agent Knowledge) is built fresh (Option A) as a Knowledge Sources extension, since neither candidate has a real org-knowledge-graph implementation.
- **Throughout:** Option E only as **pluggable-backend compatibility**, never as the primary substrate ([02](02-solution-survey.md) §8 Gap 7).

The single clearest leaning: **OGX is the substrate, a MemoryHub-derived layer is the governance, and they are complementary — not competing — exactly as doc 06 §6 concluded.** Build-fresh is reserved for Agent Knowledge; partner is reserved for backend-compatibility; upstream-contribute is the standards posture layered across all of it. The honest caveat: this phasing assumes the doc-07 decomposition is accepted at the review gate (Q-T1) and assumes the OGX replacement plan resolves in a way that does not strand 3.6 work on the bridge (D-2 / Q-G2).

---

## 5. Resolving the Doc-07 Forwarded Questions

Doc 07 §7 forwarded several open questions explicitly to this document. Each is addressed here with what the RHOAI/OCP alignment analysis can now say — recognizing that final resolution is a review-gate decision, not a research call.

**Q-T2 (forwarded — should RHAISTRAT-1345 be scoped to Subsystem 1 only, with Agent Knowledge spun out as a separate Outcome?).** The RHOAI alignment analysis *strengthens* doc 07 §6.1's recommendation. Agent Knowledge maps to a *different RHOAI component* than the memory substrate: it extends the **Knowledge Sources asset type** in the AI Asset Registry (§2.1), with a batch-indexed / read-mostly data shape and a likely *separate storage engine* (§2.7). The Agent Memory Substrate maps to the **OGX/gateway-native conversation-state microservice** plus a governance service (§2.3–2.4). These are different teams, different backends, different release vehicles. Forcing both under one Outcome would couple a registry-asset-type extension to a gateway-microservice deliverable. **The alignment analysis supports scoping RHAISTRAT-1345 to Subsystem 1 (+ Context Engineering as an in-scope capability) and spinning Agent Knowledge out as a separate Outcome.** Final call: review gate.

**Q-T5 (forwarded — confirm the substrate verdict: one substrate for the four memory types, a separate subsystem for org knowledge; does RHOAI's workload profile support the ~50M-vector pgvector threshold?).** The alignment analysis confirms the *architectural* half and leaves the *empirical* half open. Architecturally: OGX and MemoryHub both already consolidate the memory types onto PostgreSQL-class backends ([06](06-ogx-memory-primitives.md) §3.4; [03](03-memoryhub-deep-dive.md) §2.3), and both treat org-knowledge as out of their scope — so "one substrate for memory, separate for knowledge" matches what the candidate artifacts *already do*. Empirically: this document cannot supply RHOAI's actual memory-volume-per-user or org-knowledge-entity-count figures — those are not in any internal source read. The ~50M-vector pgvector threshold ([04](04-technical-patterns.md) §2.1) is a practitioner estimate, not an RHOAI measurement. **The substrate verdict is confirmed architecturally; the workload-profile validation is a review-gate / design-time measurement task — see Q-G4 below.**

**Q-T6 (forwarded — is Agent Knowledge the governed realization of the Knowledge Sources asset type, or a new asset type?).** §2.1 develops this in full. The alignment analysis comes down clearly: **extend Knowledge Sources, do not create a new asset type.** The Knowledge Sources definition ("governed information sources for RAG, agents, retrieval workflows… documents, repositories, connectors, structured systems") and its registry-need list (`source reference`, `access model`, `trust/governance context`, `refresh schedule`) already describe Subsystem 3's shape; the registry is already federated. Creating a parallel "Agent Knowledge" asset type would duplicate governance machinery and split the org-knowledge concern across two asset types. This needs an explicit decision *with the AI Asset Registry owners* — it is a registry-framework change, not a memory-team-internal call.

**Q-T4 (forwarded implicitly via doc 07 §7 and doc 06 Q11 — the procedural-memory vs. skills-registry vs. OGX-Prompts boundary).** §2.6 establishes a three-layer boundary the alignment analysis supports: **(1) MLflow Prompt Registry / Skills asset type** = governed, versioned, *approved* prompt and skill artifacts — the registry-governed, human-curated layer; **(2) OGX Prompts API** = the runtime procedural-memory *store* an agent reads/pins at inference time ([06](06-ogx-memory-primitives.md) §3.5); **(3) the memory substrate's procedural memory** = *dynamically agent-learned* behavioral rules, never human-authored. The clean handoff: an artifact is *promoted* from layer 3 (learned) → layer 2 (runtime) → layer 1 (governed) via the same kind of promotion-with-HITL gate MemoryHub's promotion pipeline and Anthropic Dreaming both use ([03](03-memoryhub-deep-dive.md) §4.3; [04](04-technical-patterns.md) §5.4). This is a hard cross-domain boundary and must be specified before either the skills team or the memory team builds.

**Q-T3 and Q-T7 (forwarded — scope-tier count; whether an explicit Identity-memory element is needed)** are *internal-design* questions that the RHOAI/OCP alignment does not materially change. They are carried forward to the review gate unchanged. The one alignment-relevant observation: MemoryHub's six-tier scope model maps onto OpenShift constructs unevenly — `user` and `role` align with OpenShift OAuth RBAC, `project` aligns with OpenShift namespaces / MLflow workspaces, but `campaign`, `organizational`, and `enterprise` have no native OpenShift analogue and would be memory-service-internal constructs. This *mild* misalignment is a small additional argument for doc 07 §5.3 Gap 7's concern that six tiers may be too many — but it is not decisive.

---

## 6. Open Architectural Questions for the Review Gate

These are the questions this alignment analysis *raises* and cannot itself settle. They are flagged **REVIEW GATE** and carried into Task 11. They are in addition to the doc-07 §7 questions (Q-T1…Q-T7), which remain open; Section 5 above gives this document's input to Q-T2/T3/T4/T5/T6/T7.

**Q-G1 (REVIEW GATE — blocks Subsystem-1 sourcing).** Adopt the phased sourcing recommendation of Section 4.7 — OGX as substrate (C), MemoryHub-derived governance layer (B) as a 3.6 Dev Preview, build-fresh (A) reserved for Agent Knowledge, upstream-contribute (D) as the standards posture, partner (E) only as pluggable-backend compatibility? Or commit to a single option?

**Q-G2 (REVIEW GATE — depends on D-2).** What is the concrete OGX/Llama Stack replacement plan, and does it reimplement the memory primitives or delegate to OGX? If the gateway-native Responses replacement reimplements conversation state, vector stores, and compaction, then *that* team owns Subsystem 1's working/episodic slice and the memory-team boundary moves. This is `docs/knowledge-registry.md` Q38 and doc 06 §7 Q3, restated as a memory-ownership question.

**Q-G3 (REVIEW GATE).** Is a productized memory service registered as a *governed asset* in the AI Asset Registry (§2.2), and are *individual memory records* also registry-governed assets, or only the service? §2.1 flags the unresolved payload-vs-metadata tension: the registry "does not store the asset payload," but the memory substrate *is* the payload. The likely answer (the service is an asset; records are governed by the same model but not registry rows) needs an explicit decision with the AI Asset Registry owners. (This is Q-A1 in §2.1.)

**Q-G4 (REVIEW GATE — empirical, supports Q-T5).** What is RHOAI's actual agent-memory workload profile — memory volume per user, concurrent-agent count, org-knowledge entity count? No internal source read for this document supplies these figures. They determine whether the single PostgreSQL+pgvector substrate holds (the ~50M-vector threshold — [04](04-technical-patterns.md) §2.1) or whether Subsystem 3 needs a dedicated store. This is a design-time measurement task, not a research call.

**Q-G5 (REVIEW GATE).** How does a memory service enforce the AI Gateway's actor-chain *lowest-permission* rule for shared/organizational memory (§2.7)? When agent B reads project- or org-scoped memory on behalf of agent A's user, the read must be scoped to the *intersection* of both actors' entitlements, or shared memory becomes a privilege-escalation path. Neither MemoryHub nor OGX documents a multi-actor-chain RBAC model. (This is Q-A2 in §2.7.)

**Q-G6 (REVIEW GATE — identity).** Should a productized memory service consume RHOAI platform identity directly (Spire/Authbridge, RFC 8693 token exchange — D-3) and *drop* MemoryHub's standalone OAuth 2.1 server? §2.5 and [03](03-memoryhub-deep-dive.md) §5.3 Gap 4 both point to "yes," but it is an integration-architecture decision with cross-team (AI Gateway, kagenti) dependencies. (This restates doc 03's Q-MH-3, now answerable with RHOAI context: the alignment analysis recommends platform identity, not a standalone auth server.)

**Q-G7 (REVIEW GATE — compliance, highest severity).** Given that *neither* candidate substrate ships a working audit trail (D-6 — MemoryHub stub, OGX absent) and EU AI Act enforcement is August 2026, what is the audit-trail delivery plan, and does it block any 3.6 memory Dev Preview? An inspectable, append-only memory audit log is a hard compliance requirement ([05](05-standards-and-protocols.md) §4.5; [03](03-memoryhub-deep-dive.md) §5.3 Gap 2) — this question cannot be deferred past the review gate.

**Q-G8 (REVIEW GATE — standards).** Should Red Hat pursue the [05 Standards & Protocols](05-standards-and-protocols.md) §6.2 opportunities — an MCP Memory Convention SEP, an A2A AgentCard memory binding, and/or an AAIF memory project — as part of the agent-memory program, and on what timeline relative to the 3.6/3.7 product work? Option D (upstream-contribute) and the standards strategy are linked but not identical; the review gate should decide whether standards work is in-program or parallel.

---

## 7. Kagenti Integration

**REFERENCE / PROPOSED** — This section deepens the kagenti integration analysis from §2.5 with concrete architecture, the ADK memory implementation, the `agent-sandbox` project, integration points with a productized RHOAI memory service, and a gap analysis of what kagenti does *not* provide.

### 7.1 Kagenti architecture

kagenti is a Red Hat incubation project for Kubernetes-native agent orchestration. It provides the deployment and lifecycle management primitives for agents on OpenShift, analogous to how the MCP Lifecycle Operator manages MCP server workloads ([06-rhoai-context.md](/features/agent-registry/research/06-rhoai-context.md) §6.5; `docs/knowledge-registry.md`). The core architecture comprises four components:

1. **AgentRuntime CRD.** The primary deployment primitive. An `AgentRuntime` defines an agent workload's container image, resource requirements, environment bindings, and lifecycle policy. The kagenti controller reconciles `AgentRuntime` resources into running pods with the correct identity, networking, and configuration. This is where memory *consumption* originates — every agent workload that needs persistent memory runs as an `AgentRuntime`.

2. **AgentCard CRD.** The discovery and capability-advertisement primitive. An `AgentCard` declares an agent's name, description, supported protocols (A2A, MCP), input/output schemas, and — critically for memory — its dependency bindings. §2.5 and [05 Standards & Protocols](05-standards-and-protocols.md) §6.2 propose a **memory binding** on the AgentCard: a declaration of which memory service the agent uses, what scope tier it operates at, and what memory capabilities it requires. The AgentCard is the surface the Agent Registry reads for discovery ([06-rhoai-context.md](/features/agent-registry/research/06-rhoai-context.md) §6.5), so a memory binding on the AgentCard flows into the registry automatically and makes agent-to-memory dependencies visible to governance tooling.

3. **Auth Bridge with SPIFFE identity injection.** kagenti injects SPIFFE SVIDs (Secure Verifiable Identity Documents) into every agent workload via the Spire agent running on each node. The Auth Bridge component handles the SPIFFE-to-platform-identity translation — bridging between the workload's SPIFFE identity and the platform's OIDC/OAuth identity providers (Keycloak, EntraID). For memory, this is the **identity chain**: the agent workload presents its SPIFFE SVID to the memory service, which validates it against the Spire trust bundle and extracts the agent's identity claims for scope-level RBAC. The AI Gateway's Tier-2 agent identity (Spire/Authbridge with actor-chain tracking — [ai-gateway.md](https://github.com/solaius/ai-asset-registry/blob/main/docs/knowledge-review/components/ai-gateway.md), decision 4) is the same identity kagenti injects, ensuring a single identity model from agent workload through gateway to memory service.

4. **ADK (Agent Development Kit).** The Python SDK for building agents that run on kagenti. The ADK provides the programming model — tool registration, conversation management, state persistence, and memory access. As detailed in §7.2, the ADK is where the most concrete agent-memory implementation in the Red Hat ecosystem exists today.

### 7.2 Memory in Kagenti — the ADK implementation

The ADK (Agent Development Kit), used within kagenti, provides the most concrete implementation of agent memory in the Red Hat ecosystem. The ADK uses **PostgreSQL for session persistence** with **pgvector for semantic search** — the same storage-substrate pattern this research series identifies as the convergent industry choice ([04](04-technical-patterns.md) §2.1; [03](03-memoryhub-deep-dive.md) §2.3).

Key implementation details:

- **Session persistence.** The ADK stores agent session state (conversation history, tool call results, intermediate reasoning) in PostgreSQL tables. Sessions are keyed by agent identity and user identity, providing per-agent, per-user isolation by default. This is *working memory* and *episodic memory* in the CoALA taxonomy ([01](01-landscape-and-definitions.md) §4) — the agent's short-term context and its record of past interactions.

- **pgvector semantic search.** The ADK uses the pgvector extension to store and query embedding vectors alongside session data. This enables semantic retrieval over past interactions — an agent can search its own history for relevant context using vector similarity, not just sequential lookup. The embedding model is configurable; the default path uses the same model-serving infrastructure (vLLM on RHOAI) that the memory service would consume (IP-7, §3.1).

- **MemoryHub SDK consumption.** As noted in §2.5, `kagenti/adk` PR #231 consumes MemoryHub's `MemoryHubClient` — an early signal that the ADK is designed to work with an external governed memory service, not only its built-in PostgreSQL persistence. This is the thin ecosystem-adoption signal noted in doc 03 §1: one PR consuming a client library, not broad adoption validation, but architecturally meaningful because it confirms the ADK's memory interface is pluggable.

- **Scope limitation.** The ADK's built-in persistence is *per-agent, per-session*. There is no concept of shared memory, project-scoped memory, or organizational memory in the ADK itself. Cross-agent memory sharing, scope tiers, and governed multi-tenant access are all outside the ADK's current implementation — these are the responsibilities of the proposed RHOAI memory service (Subsystem 1 with the Governance & Scope cross-cutting dimension from doc 07 §4.1).

### 7.3 kubernetes-sigs/agent-sandbox

The **Agent Sandbox** project (`kubernetes-sigs/agent-sandbox`) defines a `Sandbox` CRD for isolated, stateful, singleton agent workloads on Kubernetes. While kagenti manages the agent lifecycle and identity, agent-sandbox addresses a complementary concern: providing agents with a controlled execution environment that includes persistent state.

Key properties relevant to memory:

- **Stateful singleton workloads.** A Sandbox is a single-instance, long-lived workload with attached persistent storage (PVCs). This is the natural deployment model for an agent that maintains long-term memory — the Sandbox's persistent volume is where memory state survives pod restarts and rescheduling. For agents that use local SQLite or file-based memory stores (as several OGX backends support — [06](06-ogx-memory-primitives.md) §3.4), the Sandbox's PVC provides the durability guarantee.

- **Isolation boundary.** Each Sandbox runs in its own namespace or with its own security context, providing network and filesystem isolation between agent workloads. This maps to the *per-agent isolation* tier of the memory scope model — each agent's working memory is contained within its Sandbox boundary. The isolation is infrastructure-level (namespace, network policy, seccomp profile), not application-level (RBAC within a shared memory service).

- **Relationship to kagenti.** agent-sandbox and kagenti are complementary, not competing. kagenti manages agent identity, lifecycle, and orchestration; agent-sandbox provides the execution environment. A kagenti-managed `AgentRuntime` could run *inside* an agent-sandbox `Sandbox`, combining kagenti's identity injection with agent-sandbox's stateful isolation. The memory integration point is clear: the Sandbox provides the infrastructure-level memory isolation (persistent storage, network boundary); the RHOAI memory service provides the application-level memory governance (scope tiers, RBAC, audit, cross-agent sharing).

### 7.4 Integration points with RHOAI memory

A productized RHOAI memory service would integrate with kagenti's agent lifecycle at four points:

1. **Memory scope bound to AgentRuntime identity.** Each `AgentRuntime` has a SPIFFE identity injected by kagenti. The memory service should bind memory scopes to this identity: the agent's SPIFFE SVID determines *which* memory scopes the agent can access (its own working memory, the project-scoped shared memory for its namespace, the org-scoped memory for its tenant). The scope binding is declarative — specified on the `AgentCard` as a memory-capability annotation — and enforced at the memory service's RBAC layer, not at the Kubernetes level. This maps to the proposed four-tier scope model from the Phase 2 strategy (`user`/`project`/`role`/`org` — [strategy §6](/features/agent-memory/strategy/agent-memory-strategy.md)).

2. **SPIFFE-based RBAC for memory access.** The memory service validates the agent's SPIFFE SVID on every request. The SVID's SPIFFE ID encodes the agent's trust domain, namespace, and service account — sufficient to derive the `user` and `project` scope tiers directly from Kubernetes-native constructs. The `role` and `org` tiers require additional claims, either from the Auth Bridge's OIDC token exchange (RFC 8693) or from the AgentCard's memory-binding annotations. This is the same identity chain described in §2.7 and §3.1 (IP-6), now made concrete: `kagenti Auth Bridge → SPIFFE SVID → memory service RBAC → scope-tier enforcement`.

3. **Memory as a platform service consumed by kagenti-managed agents.** The memory service is *not* deployed by kagenti — it is an RHOAI platform service, deployed and managed by its own operator (the operator gap flagged as D-5 in §3.2), with its own lifecycle independent of any single agent workload. kagenti-managed agents *consume* the memory service the same way they consume model serving (vLLM) or tool execution (MCP Gateway) — as a platform dependency declared in the AgentCard and accessed via the agent's SPIFFE identity. This is the correct boundary: kagenti manages *agent workloads*; the memory service manages *memory state*. The two are coupled by identity and protocol, not by deployment.

4. **Lifecycle events.** When kagenti scales down, updates, or deletes an `AgentRuntime`, the memory service should receive lifecycle signals (or the agent should perform cleanup). Working memory for a deleted agent can be garbage-collected; episodic and semantic memory should persist (the agent may be redeployed). This lifecycle coupling is not yet designed in either kagenti or the memory-service proposal — it is a design-time integration item for the 3.6 Dev Preview.

### 7.5 Gap analysis — what kagenti does not provide

kagenti provides the agent *lifecycle and identity* layer. It does *not* provide a governed memory platform. The gaps, mapped to the doc-07 decomposition:

| Memory concern | kagenti provides | kagenti does not provide |
|---|---|---|
| **Working memory (per-session state)** | ADK PostgreSQL session persistence — functional, per-agent scoped | No governed multi-tenant store; no scope tiers beyond per-agent isolation; no RBAC model beyond "agent owns its own sessions" |
| **Episodic memory (interaction history)** | ADK stores conversation history in PostgreSQL | No cross-session consolidation; no memory curation, contradiction detection, or provenance tracking; no retention/erasure policies |
| **Semantic memory (learned facts)** | ADK pgvector for vector search over session data | No governed semantic store; no cross-agent shared semantic memory; no version control on learned facts |
| **Procedural memory (behavioral rules)** | Not implemented in ADK; agents use static prompt templates | No dynamic procedural memory; no learned-behavior extraction or promotion pipeline |
| **Scope tiers** | Per-agent isolation (via SPIFFE identity + PostgreSQL row-level access) | No project-scoped, role-scoped, or org-scoped memory; no shared memory between agents; no scope-tier RBAC model |
| **Audit trail** | No memory-specific audit logging | No append-only audit log of memory reads/writes; no compliance-facing immutable record |
| **Context engineering** | Not implemented; agents manage their own context window | No compaction, retrieval assembly, progressive disclosure, or KV-cache-aware ordering |
| **Knowledge (Subsystem 3)** | Not in scope for kagenti | No enterprise knowledge layer; no RAG integration; no knowledge-graph support |

**The summary gap:** kagenti provides *per-agent memory isolation as a side effect of Kubernetes-native identity and deployment* — the infrastructure layer. The RHOAI memory service provides the *application layer*: governed multi-tenant storage, scope tiers, audit, curation, and the context-engineering capabilities that turn raw memory into useful agent context. The two are complementary by design. The ADK's MemoryHub SDK integration (§7.2) is the early signal that this complementarity is already recognized in the kagenti codebase.

---

## 8. Storage Backend Trade-offs

**REFERENCE / PROPOSED** — This section evaluates storage backend options for the RHOAI memory service against the constraints established throughout this research series: OpenShift certification requirements, FIPS compliance, operational complexity for enterprise SREs, and the performance profiles the memory workload demands.

### 8.1 PostgreSQL + pgvector (recommended primary)

PostgreSQL with the pgvector extension is the convergent storage choice across the agent-memory ecosystem. MemoryHub uses it as its sole backend ([03](03-memoryhub-deep-dive.md) §2.3); OGX supports it as one of nine Vector I/O backends ([06](06-ogx-memory-primitives.md) §3.4); Mem0, Zep, and Letta all support or default to PostgreSQL+pgvector ([02](02-solution-survey.md) §2). Doc 04 §2.1 identifies the "unified relational + vector store" as the dominant production pattern.

**Indexing strategies and performance characteristics:**

- **HNSW (Hierarchical Navigable Small World).** The recommended indexing strategy for production memory workloads. HNSW provides approximate nearest-neighbor search with tunable recall-speed trade-offs. Published benchmarks show approximately 40 queries per second at 99% recall for 1 million 768-dimensional vectors (the dimension of common embedding models like `all-MiniLM-L6-v2` and `text-embedding-3-small`). HNSW indexes are more expensive to build (hours for large datasets) but provide consistent, fast query performance at runtime. For agent memory, where the query workload (read-before-reasoning) is latency-sensitive and the write workload (write-after-acting) is append-heavy, HNSW is the correct default.

- **IVFFlat (Inverted File with Flat Compression).** An alternative indexing strategy with faster index builds but lower recall at equivalent query speeds. IVFFlat is suitable for prototyping and development environments where rebuild speed matters more than production recall. For the RHOAI 3.6 Dev Preview, IVFFlat may be the pragmatic default (faster iteration during development); HNSW should be the GA default.

- **pgvectorscale (StreamingDiskANN).** The Timescale extension for PostgreSQL that extends pgvector's effective range from approximately 10-50 million vectors to 50-300 million vectors using the StreamingDiskANN algorithm. StreamingDiskANN stores the vector index partially on disk rather than entirely in memory, trading some query latency for dramatically reduced memory requirements at scale. This is relevant for the transition point between Subsystem 1 (agent memory, bounded per-agent) and Subsystem 3 (org-wide knowledge, potentially 50-100M+ entities) — pgvectorscale extends the "single PostgreSQL substrate" story to cover a larger portion of the workload spectrum before a dedicated vector database becomes necessary. pgvectorscale is open source (Apache 2.0) and compatible with the standard pgvector extension.

**Operator support on OpenShift:**

Two PostgreSQL operators have achieved **Red Hat OpenShift Operator Certification** and are available on OperatorHub:

- **Crunchy Data PostgreSQL Operator (PGO).** Mature, widely deployed on OpenShift. Provides automated backups, high availability (Patroni-based), connection pooling (PgBouncer), monitoring, and pgvector extension support. Crunchy Data is a Red Hat technology partner with a long history of OpenShift collaboration.
- **EDB (EnterpriseDB) Operator.** Enterprise PostgreSQL on OpenShift with similar operational features. EDB provides commercial support and adds enterprise features (Oracle compatibility, advanced security).

Both operators support the pgvector extension, handle the operational lifecycle (backup, restore, failover, scaling), and are certified for FIPS-validated OpenShift clusters. This is a decisive advantage: PostgreSQL+pgvector on OpenShift is a *supported, certified, operationally mature* deployment, not a bring-your-own-database exercise.

**Advantage summary:** Unified relational + vector store reduces operational complexity — one database engine for session state, conversation history, vector embeddings, and metadata. The enterprise operations team manages one backup strategy, one monitoring stack, one security posture, one FIPS validation. Doc 04 §2.1 calls this the "single-substrate pattern" and identifies it as the right default for enterprise Kubernetes platforms.

### 8.2 Redis (recommended hot cache)

Redis provides sub-millisecond latency key-value access, making it the natural choice for the hot-cache layer of the memory architecture — the frequently-accessed working memory and active session context that agents read on every reasoning step.

**Use cases in the memory architecture:**

- **Session state.** The agent's current conversation context, tool-call history, and intermediate reasoning state. This data is read on every request and updated on every response — the highest-frequency access pattern in the memory system. PostgreSQL can serve this workload, but Redis's sub-millisecond reads reduce the critical-path latency for agent responses.
- **Active context cache.** The assembled context window (the output of context engineering / Subsystem 2) — the compacted, ordered, relevance-ranked memory slice that the agent sends to the LLM. Caching the assembled context avoids re-running the retrieval + compaction + ordering pipeline on every request when the underlying memory has not changed.
- **Frequently-accessed memories.** Hot semantic memories (recently written, frequently retrieved) can be cached in Redis with a TTL-based eviction policy, with PostgreSQL+pgvector as the durable backing store.

**Operator support on OpenShift:**

The **Redis Enterprise Operator** is Red Hat Certified on OperatorHub. It provides clustered Redis with automatic sharding, persistence (RDB + AOF), high availability, and monitoring. Redis Enterprise supports the full Redis data-structure set (strings, hashes, sorted sets, streams) and Redis Search (for secondary indexing), though for the memory use case, the primary value is low-latency key-value access, not Redis's richer data structures.

**Architecture pattern:** Redis as a write-through or write-behind cache in front of PostgreSQL+pgvector. Writes go to both Redis (for immediate availability) and PostgreSQL (for durability and vector indexing). Reads check Redis first; cache misses fall through to PostgreSQL. This is the **hybrid pattern** used by most production agent memory systems — Mem0, Zep, and Letta all converge on a "hot cache + durable store" architecture ([02](02-solution-survey.md) §2; [04](04-technical-patterns.md) §2.1).

### 8.3 Dedicated vector databases (evaluated, not recommended for MVP)

Several dedicated vector databases were evaluated during the doc-02 solution survey and doc-04 technical patterns analysis. While all offer strong vector-search performance, none meets the OpenShift certification requirement for an RHOAI-shipped component.

| Vector Database | Strengths | OpenShift Operator Certification | Assessment |
|---|---|---|---|
| **Qdrant** | Rust-based, strong single-node performance, rich filtering, gRPC + REST APIs, active community (20K+ GitHub stars) | **No** — no Red Hat OpenShift Operator Certification | Strong technology; deployment on OpenShift requires customer-managed Helm charts or manual manifests. Cannot be shipped as a supported RHOAI component without certification. |
| **Milvus** | Distributed architecture, horizontal scaling, GPU-accelerated indexing, strong at 100M+ vector scale | **No** — no Red Hat OpenShift Operator Certification | Best-in-class for very large scale; complex operational footprint (etcd, MinIO, Pulsar dependencies). Operational complexity is the opposite of the single-substrate pattern. |
| **Weaviate** | GraphQL interface, hybrid search (vector + keyword), multi-tenancy, module ecosystem | **No** — no Red Hat OpenShift Operator Certification | Good developer experience; GraphQL interface is non-standard in the agent-memory ecosystem (MCP and Responses API are the de facto transports — [05](05-standards-and-protocols.md) §2). |
| **Chroma** | Lightweight, developer-friendly, Python-native, popular for prototyping | **No** — no Red Hat OpenShift Operator Certification | Prototyping tool, not production-grade for enterprise multi-tenant workloads. |
| **Pinecone** | Fully managed SaaS, strong performance, simple API | **N/A** — SaaS only, no self-hosted option | Incompatible with air-gap, data-residency, and self-hosted enterprise requirements. |

**Key finding:** No dedicated vector database has achieved Red Hat OpenShift Operator Certification as of mid-2026. This is not a quality judgment — Qdrant and Milvus are strong technologies — but a practical constraint: RHOAI cannot ship an uncertified operator as a supported component. Customers can deploy these databases independently alongside RHOAI, and the memory service should support pluggable backends ([02](02-solution-survey.md) §8 Gap 7) to accommodate this, but the *default, supported, shipped-with-RHOAI* backend must be a certified operator. PostgreSQL+pgvector meets this requirement; no dedicated vector database does.

### 8.4 Graph databases (evaluated, archived for future consideration)

Graph databases address the *relationship-heavy* memory patterns that arise in organizational knowledge (Subsystem 3) and in complex multi-agent coordination — scenarios where "agent A learned fact X from agent B, which contradicts fact Y from source Z" is the query shape, not "find the 10 most similar vectors."

| Graph Database | Strengths | Assessment for RHOAI memory |
|---|---|---|
| **Neo4j** | Most mature graph database; Cypher query language is well-known; strong for relationship traversal and pattern matching | Adds a second database engine to the operational footprint; no Red Hat Operator Certification; commercial license for enterprise features. Good technology, wrong phase — operational complexity outweighs benefit for MVP. |
| **FalkorDB** | Redis-based graph database; sub-millisecond graph queries; Cypher-compatible | Interesting hybrid (graph on Redis), but nascent and no OpenShift certification. Worth monitoring for future phases. |
| **KuzuDB** | Embedded graph database; strong for analytical graph queries; no server overhead | Embedded-only — not a fit for a shared, multi-tenant platform service. Could be useful for agent-local graph reasoning within a Sandbox. |
| **Apache AGE** | **PostgreSQL extension** for openCypher graph queries; runs inside the existing PostgreSQL instance | **Best fit for the "unified PostgreSQL" architecture.** AGE adds graph query capability without adding a separate database engine. MemoryHub explicitly targets AGE "pending validation with OpenShift's OOTB PostgreSQL operator" ([03](03-memoryhub-deep-dive.md) §2.3). If graph queries are needed, AGE preserves the single-substrate pattern. |

**Recommendation:** Archive graph database evaluation for Phase 2+. The MVP memory service (Subsystem 1) does not require graph queries — the four CoALA access patterns (working, episodic, semantic, procedural) are served by relational + vector queries. If graph queries become necessary — for contradiction detection, provenance tracking, or the Subsystem-3 knowledge layer — **Apache AGE is the recommended path** because it keeps graph capability within the existing PostgreSQL instance, preserving the operational simplicity of the single-substrate pattern. This aligns with MemoryHub's architectural direction ([03](03-memoryhub-deep-dive.md) §2.3) and avoids introducing a second database engine.

### 8.5 Recommended architecture

**PROPOSED** — The recommended storage architecture for the RHOAI memory service MVP is a two-tier hybrid:

```
┌─────────────────────────────────────────────────────────────┐
│                     RHOAI Memory Service                     │
│                                                              │
│  ┌──────────────────┐     ┌──────────────────────────────┐  │
│  │   Redis (hot)     │     │   PostgreSQL + pgvector       │  │
│  │                   │     │   (source of truth)           │  │
│  │  - Session state  │◄───►│  - Conversation history       │  │
│  │  - Active context │     │  - Vector embeddings          │  │
│  │  - Hot memories   │     │  - Memory metadata + RBAC     │  │
│  │                   │     │  - Audit log (append-only)    │  │
│  │  Sub-ms reads     │     │  - Scope-tier enforcement     │  │
│  │  TTL eviction     │     │                               │  │
│  └──────────────────┘     │  + Apache AGE (Phase 2+)      │  │
│                            │    for graph queries           │  │
│                            └──────────────────────────────┘  │
│                                                              │
│  Operators: Crunchy PGO or EDB (PostgreSQL)                  │
│             Redis Enterprise Operator (Redis)                │
│  Both: Red Hat OpenShift Operator Certified                  │
└─────────────────────────────────────────────────────────────┘
```

- **PostgreSQL+pgvector** is the durable source of truth for all memory types (working, episodic, semantic, procedural), metadata, scope-tier RBAC enforcement, and the append-only audit log. HNSW indexing for production vector search; IVFFlat for development. pgvectorscale available for high-scale deployments (50-300M vectors).
- **Redis** is the hot cache for session state, active context, and frequently-accessed memories. Write-through to PostgreSQL ensures durability; Redis provides sub-millisecond read latency for the agent's critical reasoning path.
- **Apache AGE** (PostgreSQL extension) is the deferred graph-query path — available when graph-shaped queries (contradiction detection, provenance traversal, knowledge-graph reasoning) become necessary, without adding a separate database engine.

This architecture is the same hybrid pattern used by Mem0 (PostgreSQL+pgvector + Redis/DragonflyDB), Zep (PostgreSQL+pgvector + graph layer), and Letta (PostgreSQL+pgvector) — the industry has converged on this shape ([02](02-solution-survey.md) §2; [04](04-technical-patterns.md) §2.1). RHOAI's advantage is that both required operators (Crunchy PGO / EDB for PostgreSQL, Redis Enterprise for Redis) are already Red Hat OpenShift Operator Certified — the operational foundation is production-ready.

### 8.6 Decision framework

The following table compares storage options across the dimensions that matter for an RHOAI-shipped component. This is the decision framework the review gate should use when evaluating backend choices.

| Dimension | PostgreSQL + pgvector | Redis | Qdrant | Milvus | Weaviate | Neo4j |
|---|---|---|---|---|---|---|
| **OpenShift Operator Certified** | Yes (Crunchy PGO, EDB) | Yes (Redis Enterprise) | No | No | No | No |
| **FIPS compatibility** | Yes (via certified operator + cluster OpenSSL) | Yes (via certified operator) | Unknown | Unknown | Unknown | Unknown |
| **Operational complexity** | Low (single engine for relational + vector) | Low (well-understood caching layer) | Medium (dedicated vector engine) | High (etcd, MinIO, Pulsar dependencies) | Medium (module ecosystem) | Medium-High (separate engine + Cypher learning curve) |
| **Vector search performance (1M 768-dim)** | Good (~40 QPS at 99% recall with HNSW) | N/A (not a vector database) | Excellent (~100+ QPS) | Excellent (distributed, GPU-capable) | Good (~50 QPS) | N/A (graph, not vector) |
| **Scalability ceiling** | 10-50M vectors (native pgvector); 50-300M (pgvectorscale) | N/A (cache, not primary vector store) | 100M+ vectors (single node) | Billions (distributed) | 100M+ (sharded) | N/A (graph scale, not vector scale) |
| **Relational data support** | Native (full SQL) | Limited (key-value + data structures) | No (vector-only with payload metadata) | No (vector-only with scalar filtering) | Limited (property filtering) | Yes (property graph with Cypher) |
| **Ecosystem maturity (agent memory)** | High (default for Mem0, Zep, Letta, MemoryHub, ADK) | High (universal caching layer) | Medium (growing adoption) | Medium (ML-focused, less agent-memory) | Medium (developer-friendly) | Low (few agent-memory integrations) |
| **Air-gap deployable** | Yes | Yes | Yes (self-hosted) | Yes (self-hosted, complex) | Yes (self-hosted) | Yes (self-hosted) |
| **Cost (OpenShift deployment)** | Included with operator subscription | Included with operator subscription | No supported operator; manual deployment | No supported operator; complex infra | No supported operator | No supported operator; commercial license |
| **Unified store benefit** | Yes — one engine for all data shapes | No — cache only, needs a backing store | No — vector only, needs relational store | No — vector only, needs relational store | Partial — hybrid search, but not full relational | Partial — graph + properties, but not vector |

**Reading the table:** The first two columns (PostgreSQL+pgvector, Redis) are the recommended MVP components — they score "Yes" or "High" on every dimension that is a hard RHOAI requirement (certification, FIPS, air-gap, operational complexity). The remaining columns show why dedicated vector and graph databases, while technically strong, do not meet the certification and operational-simplicity requirements for an RHOAI-shipped default. They remain valid as customer-deployed pluggable backends behind the memory service's backend-agnostic interface ([02](02-solution-survey.md) §8 Gap 7).

---

## 9. Sources

### Internal (Repository)

| Source | Type | Path / Reference |
|---|---|---|
| Agent Memory & Knowledge seed doc | Internal seed document | `docs/knowledge-review/assets/agent-memory-knowledge.md` |
| Knowledge Registry (components §3; platform integration §6; open questions Q35–Q44) | Internal reference | `docs/knowledge-registry.md` |
| Core Concepts (Registry/Catalog/Plugin/Federation/Gateway Enforcement) | Architecture reference | `docs/knowledge-review/architecture/core-concepts.md` |
| System Boundaries (component responsibilities; backend registry mapping) | Architecture reference | `docs/knowledge-review/architecture/system-boundaries.md` |
| AI Gateway (IPP framework; Responses re-architecture; group-based tenancy; agent identity; roadmap) | Component reference | `docs/knowledge-review/components/ai-gateway.md` |
| MCP Gateway (Envoy/Kuadrant; per-tool authz; guardrails; registry integration roadmap) | Component reference | `docs/knowledge-review/components/mcp-gateway.md` |
| MCP Registry (two-tier model; four governance tracks; workspace scoping) | Component reference | `docs/knowledge-review/components/mcp-registry.md` |
| Platform Integration (deployment architecture; MLflow/Databricks upstream process) | Integration reference | `docs/knowledge-review/integration/platform-integration.md` |
| Governance & Security (RBAC; trust tiers; agent zero-trust; SPIFFE/SPIRE) | Security reference | `docs/knowledge-review/security/governance-and-security.md` |
| AI Asset Types (Knowledge Sources; Agents; the agent dual-entity challenge) | Asset reference | `docs/knowledge-review/assets/asset-types.md` |
| Agent Registry Research — RHOAI Patterns, Decisions & Internal Context | Sibling research / depth calibration | `agents/agent-registry/research/06-rhoai-context.md` |
| 01 Landscape & Definitions | Sibling research doc | `agent-memory/research/01-landscape-and-definitions.md` |
| 02 Solution Survey | Sibling research doc | `agent-memory/research/02-solution-survey.md` |
| 03 MemoryHub Deep-Dive | Sibling research doc | `agent-memory/research/03-memoryhub-deep-dive.md` |
| 04 Technical Patterns | Sibling research doc | `agent-memory/research/04-technical-patterns.md` |
| 05 Standards & Protocols | Sibling research doc | `agent-memory/research/05-standards-and-protocols.md` |
| 06 OGX Memory Primitives | Sibling research doc | `agent-memory/research/06-ogx-memory-primitives.md` |
| 07 Taxonomy & Decomposition | Sibling research doc | `agent-memory/research/07-taxonomy-and-decomposition.md` |
| RHAISTRAT-1345 (Outcome: Agent Memory Primitives) | Jira Outcome | https://redhat.atlassian.net/browse/RHAISTRAT-1345 |
| Project guidance — Registry = Governance principle; asset types; component context | Internal reference | `CLAUDE.md` |
| Phase 2 Strategy — Agent Memory Strategy | Strategy doc | `agent-memory/strategy/agent-memory-strategy.md` |
| Phase 2 Strategy — Recommended Architecture | Strategy doc | `agent-memory/strategy/recommended-architecture.md` |
| Phase 2 Strategy — RFE Roadmap | Strategy doc | `agent-memory/strategy/rfe-roadmap.md` |

### External — cited via sibling docs (not independently re-fetched for this alignment synthesis)

| Source | Cited for | Via |
|---|---|---|
| MemoryHub (`redhat-ai-americas/memory-hub`) | Six-tier scope model; PostgreSQL+pgvector substrate; operator skeleton; audit stub; FIPS delegation; kagenti integration design; cache-optimized assembly | [03](03-memoryhub-deep-dive.md) |
| OGX (`ogx-ai/ogx`) | Conversations / Vector Stores / Files / Prompts APIs; compaction; `AuthorizedSqlStore` ABAC; Llama Stack rename; Arceo / Han contributions | [06](06-ogx-memory-primitives.md) |
| AI Gateway F2F — Agenda & Outcomes (April 21–23, 2026) | Llama Stack bridge decision; gateway-native Responses replacement; IPP; group-based tenancy; agent identity tiers | [ai-gateway.md](https://github.com/solaius/ai-asset-registry/blob/main/docs/knowledge-review/components/ai-gateway.md); [06](06-ogx-memory-primitives.md) §1.2 |
| Varsha Prasad Narsing — agent registry upstream proposal (`varshaprasad96/mlflow`, branch `spike/gateway`) | Agent Registry post-deployment model; runtime states; kagenti discovery | [06-rhoai-context.md](/features/agent-registry/research/06-rhoai-context.md); [asset-types.md](https://github.com/solaius/ai-asset-registry/blob/main/docs/knowledge-review/assets/asset-types.md) |
| When Agent Memory Becomes a Platform Concern (Wes Jackson, Red Hat SSA, 2026-05-01) | Memory ≠ RAG; platform-tier framing; portability / open-standards argument | [01](01-landscape-and-definitions.md) §2; [05](05-standards-and-protocols.md) §5 |
| Oracle AI Agent Memory (Richmond Alake, Oracle, 2026-05-01) | "Four access patterns over one substrate"; per-record audit/erasure governance model | [01](01-landscape-and-definitions.md) §4; [02](02-solution-survey.md) §3.1 |
| Mem0 / Letta / Zep-Graphiti / Cognee | Partner-option assessment; market-consolidation risk; backend-compatibility argument | [02](02-solution-survey.md) §2, §6, §8 |
| CoALA (arXiv:2309.02427) | Four-type memory taxonomy used as the Subsystem-1 internal model | [01](01-landscape-and-definitions.md) §4; [07](07-taxonomy-and-decomposition.md) §2.2 |
| EU AI Act transparency requirements (enforcement August 2026) | Compliance driver for the audit-trail and inspectable-compaction requirements | [05](05-standards-and-protocols.md) §4.5; [03](03-memoryhub-deep-dive.md) §5.3 |
| MCP-as-memory-transport; AAIF / A2A AgentCard standards opportunities | Memory exposed via MCP; standards-posture options (Q-G8) | [05](05-standards-and-protocols.md) §2, §6 |
| kagenti ADK (`kagenti/adk`) | PostgreSQL session persistence; pgvector semantic search; MemoryHub SDK consumption (PR #231) | [03](03-memoryhub-deep-dive.md) §1; §7.2 of this document |
| kubernetes-sigs/agent-sandbox | Sandbox CRD for isolated, stateful, singleton agent workloads | §7.3 of this document; Kubernetes SIG documentation |
| pgvector (`pgvector/pgvector`) | HNSW and IVFFlat indexing for PostgreSQL vector search | [04](04-technical-patterns.md) §2.1; §8.1 of this document |
| pgvectorscale (Timescale) | StreamingDiskANN algorithm for 50-300M vector scale on PostgreSQL | §8.1 of this document; Timescale public documentation |
| Apache AGE | PostgreSQL extension for openCypher graph queries | [03](03-memoryhub-deep-dive.md) §2.3; §8.4 of this document |
| Crunchy Data PostgreSQL Operator (PGO) | Red Hat OpenShift Operator Certified PostgreSQL operator | §8.1 of this document; OperatorHub certification listing |
| EDB (EnterpriseDB) Operator | Red Hat OpenShift Operator Certified PostgreSQL operator | §8.1 of this document; OperatorHub certification listing |
| Redis Enterprise Operator | Red Hat OpenShift Operator Certified Redis operator | §8.2 of this document; OperatorHub certification listing |
| Qdrant, Milvus, Weaviate, Chroma, Pinecone | Dedicated vector database evaluation — none OpenShift Operator Certified | §8.3 of this document; [02](02-solution-survey.md) §2; [04](04-technical-patterns.md) §2 |

### Notes

Sections 1–6 are the original wave-1/2 research synthesis document. It introduces no new external research; every external claim traces to a wave-1 sibling document (01–06), which carries its own primary-source attribution and access notes (including the preserved caveats: Oracle blog 403, MemoryHub cache-optimization figures not independently benchmarked, OpenClaw star count not independently verified). All RHOAI/OCP architecture claims trace to internal `docs/knowledge-review/` component documents or `docs/knowledge-registry.md`. Where an RHOAI fact is genuinely unresolved in the internal sources themselves — the OGX replacement execution plan, the MLflow plugin-architecture approval, RHOAI's empirical memory workload profile — this document marks it as a review-gate question (Q-G2, D-1, Q-G4) rather than inventing an answer. No RHOAI component, release date, or Jira key has been invented; RHAISTRAT-1345 is the only memory-related Jira key, and it is an Outcome with no child Features ([agent-memory-knowledge seed doc](/features/agent-memory/research/agent-memory-landscape-research.md) §2).

Sections 7–8 were added after the Phase 2 strategy phase to deepen two areas identified as needing further analysis: the kagenti integration model (§7) and the storage backend trade-offs (§8). These sections draw on the same sibling research documents (particularly [03](03-memoryhub-deep-dive.md), [04](04-technical-patterns.md), and [06](06-ogx-memory-primitives.md)) and on the Phase 2 strategy documents for the scope-tier model and roadmap phasing. External sources added for §7–8 (pgvectorscale, Apache AGE, OperatorHub certification listings, kubernetes-sigs/agent-sandbox) are public documentation, not independently benchmarked — performance figures cited are published benchmarks, not RHOAI-specific measurements.
