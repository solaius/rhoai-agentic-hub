---
title: Agent Memory & Knowledge Research — Executive Summary
description: Living synthesis of the agent-memory research series (Phase 1, Phase 2, later additions, and the 2026-07-10 refresh) -- findings, decomposition, sourcing direction, and open questions.
source: ai-asset-registry/agent-memory/research/00-executive-summary.md (as of 2026-07-05); refreshed in-hub 2026-07-10
timestamp: 2026-07-10
review_after: 2026-09-10
---

# Agent Memory & Knowledge Research — Executive Summary

**Purpose:** Synthesize the eight research documents (01–08) in the Phase 1 research set on agent memory and knowledge into a single, decision-ready overview — the findings, the proposed decomposition, the proposed sourcing direction, and the open questions — to tee up the human review gate (Task 11) before any strategy or Feature work begins.

**Date:** 2026-05-17

**Author:** Peter Double (Principal PM — MCP & AI Asset Registries)

**Status:** SYNTHESIS — this document summarizes both research phases. Phase 1 findings (docs 01–08) are DECIDED per [REVIEW-NOTES](REVIEW-NOTES.md). Phase 2 findings (docs 09–15) are EXPLORATORY — deep dives commissioned at the first Agent Memory Team Sync (2026-06-09). See [RHAISTRAT-1345](https://redhat.atlassian.net/browse/RHAISTRAT-1345). Refreshed 2026-07-10 — see the refresh note below and [doc 19](19-market-direction-refresh-2026-07.md).

## Refresh note — 2026-07-10

The quick refresh ([19 — Market & direction refresh](19-market-direction-refresh-2026-07.md)) records four changes against this synthesis; the decided Phase-1 baseline (D1–D6) is unchanged:

1. **Delivery phasing superseded**: 3.6 = DP (deliberately) → 3.7 = TP (Feb 2027) → 3.8 = GA — replaces §5's "3.7+ (GA)" sketch (owner 1:1, 2026-06-30).
2. **Delivery vehicle superseded**: agent memory is a **standalone service**, decoupled from OGX *and* the AI Gateway — doc 16's gateway-absorption premise carries a supersede note; the substrate-agnostic API posture stands.
3. **Compliance timing nuanced**: GPAI enforcement starts 2026-08-02 as expected, but the Annex III high-risk deadline is provisionally deferred to 2027-12-02 (Digital Omnibus, adoption pending) — Q-G7's audit-trail urgency is now customer-driven more than date-driven.
4. **Interim landscape settled for now**: Feast out as interim memory; OGX memory tool (interim DP) + MemoryHub (governance leader) are the candidate pair; official workstream repo is opendatahub-io/agent-memory.

**Series — Agent Memory & Knowledge Research (20 documents + review notes):**
**Phase 1 (completed 2026-05-17):**
- 00 Executive Summary (this document)
- [01 Landscape & Definitions](01-landscape-and-definitions.md)
- [02 Solution Survey](02-solution-survey.md)
- [03 MemoryHub Deep-Dive](03-memoryhub-deep-dive.md)
- [04 Technical Patterns](04-technical-patterns.md)
- [05 Standards & Protocols](05-standards-and-protocols.md)
- [06 OGX Memory Primitives](06-ogx-memory-primitives.md)
- [07 Taxonomy & Decomposition](07-taxonomy-and-decomposition.md)
- [08 RHOAI & OCP Alignment](08-rhoai-ocp-alignment.md)
**Phase 2 (2026-06-09):**
- [09 Agent Harness Memory Mechanisms](09-agent-harness-memory.md)
- [10 Claude Memory & Dreaming](10-claude-memory-dreaming.md)
- [11 Adversarial Memory & Context Integrity](11-adversarial-memory.md)
- [12 Benchmarking & Evaluation](12-benchmarking-evaluation.md)
- [13 KV-Cache Memory Optimization](13-kv-cache-optimization.md)
- [14 Enterprise Use Case Patterns](14-enterprise-use-cases.md)
- [15 Multi-Modal Memory](15-multi-modal-memory.md)
- [16 AI Gateway Memory Substrate](16-ai-gateway-memory-substrate.md) *(superseded 2026-07-10 — see doc 19)*
**Later additions (post-2026-06-10):**
- [17 Open Knowledge Format](17-open-knowledge-format.md)
- [18 Filesystem Knowledge & Project Memory](18-filesystem-knowledge-and-project-memory.md)
**Refresh (2026-07-10):**
- [19 Market & Direction Refresh](19-market-direction-refresh-2026-07.md)
- [REVIEW-NOTES](REVIEW-NOTES.md)

---

## 1. The Bottom Line

Agent memory has crossed from a research curiosity into a funded, contested platform layer: ~$62M of venture investment into pure-play memory startups in 18 months (analyst Wes Jackson pegs the figure at $60M+), GA memory features at every hyperscaler, and a clear analyst consensus (Bessemer) that memory is a 2026 differentiation frontier. Yet there is **no mature standard** for agent memory, and — critically — **no existing solution combines enterprise governance with Kubernetes-native, self-hosted, air-gappable deployment behind an open interface**. That gap is RHOAI's whitespace. Red Hat already holds two unusually strong assets in this space: MemoryHub, an OpenShift-native governed-memory prototype with the most mature scope/RBAC governance model of any candidate surveyed; and OGX (the renamed Llama Stack), which RHOAI 3.5 is GA'ing as the Responses bridge and which *already ships* production working/episodic/semantic/procedural memory primitives plus compaction. On the research taken together, this synthesis concludes that RHOAI is better positioned than the framing in RHAISTRAT-1345 alone would suggest — but the Outcome is not yet scopeable, because the problem space has not been decomposed and the sourcing path has not been chosen.

The research therefore makes two **PROPOSED** recommendations for the review gate. First, on decomposition (doc 07): Peter's original 3-area framing (Agent Knowledge / Agentic Memory / Context Engineering) is mostly sound but does not hold as-is — it should be restructured into **3 subsystems plus 2 cross-cutting dimensions**, with Agent Knowledge re-typed as enterprise-RAG-shaped (not memory), Agentic Memory reframed as one governed substrate with four access patterns, and Context Engineering demoted from a peer area to a capability layer over the substrate. Second, on sourcing (doc 08): no single option wins — the analysis points to a **phased combination**, with OGX as the memory substrate, a MemoryHub-derived governance layer on top, build-fresh reserved for Agent Knowledge, upstream contribution as the standards posture, and partner products only as pluggable-backend compatibility. Both recommendations, and a focused set of decisions only Peter can make, are the agenda for the review session.

## 2. Research Document Index

| # | Document | What It Covers |
|---|----------|----------------|
| 01 | [Landscape & Definitions](01-landscape-and-definitions.md) | Definitions of memory/knowledge/context engineering; memory-vs-RAG distinction; client- vs. server-side fork; the CoALA four-type taxonomy; why definitions drive scoping (Q40–44). |
| 02 | [Solution Survey](02-solution-survey.md) | Survey of 16 solutions — memory startups, hyperscaler features, frameworks, MemoryHub — scored on governance maturity and RHOAI relevance; investment signal; 7 cross-solution gaps. |
| 03 | [MemoryHub Deep-Dive](03-memoryhub-deep-dive.md) | Technical analysis of Red Hat's MemoryHub prototype — architecture, six-tier scope governance, notable ideas, and a subsystem-by-subsystem productization gap assessment. |
| 04 | [Technical Patterns](04-technical-patterns.md) | The recurring architecture patterns — storage substrates, retrieval, writing/extraction, compaction, knowledge graphs, scope/governance, cache optimization, multi-agent coordination. |
| 05 | [Standards & Protocols](05-standards-and-protocols.md) | The standards landscape: no memory standard exists; MCP as de facto transport; adjacent standards (A2A, AGENTS.md, PAM); the open-standards / portability argument for Red Hat. |
| 06 | [OGX Memory Primitives](06-ogx-memory-primitives.md) | Deep research into OGX (formerly Llama Stack) — its production memory primitives, Francisco Arceo's contributions, governance gaps, and how it contrasts with MemoryHub. |
| 07 | [Taxonomy & Decomposition](07-taxonomy-and-decomposition.md) | Synthesis of docs 01–06: evaluates four candidate taxonomies, recommends a 3-subsystem + 2-cross-cutting-dimension decomposition, gives a verdict on Peter's 3 areas. |
| 08 | [RHOAI & OCP Alignment](08-rhoai-ocp-alignment.md) | Maps the decomposition onto RHOAI/OCP component by component; lays out 5 sourcing options with trade-offs and release feasibility; resolves doc-07 questions; raises Q-G* questions. |

## 3. Key Findings

1. **There is no single authoritative boundary between "agent memory" and "agent knowledge."** Practitioners diverge; this is a real scoping ambiguity, not a vocabulary nitpick — and it must be resolved before Features can be authored. See [01] §1–2.

2. **The structural test that separates memory from RAG is the write path.** Memory is a stateful, append-heavy store agents *write to* during interaction ("what have agents learned?"); RAG is read-only retrieval over a stable, batch-indexed corpus ("what does the manual say?"). They are different data architectures — a database concern vs. a search concern — and conflating them produces an architecture that serves neither. See [01] §2.

3. **The CoALA four-type taxonomy (working/episodic/semantic/procedural) is the dominant model, and Oracle's key architectural claim is that the four types are four access patterns over one governed substrate** — not four systems. This is the strongest external design signal for a unified memory substrate — but [07] §3.3 holds it against a counterweight: the Memory-vs-RAG divide asserts that semantic memory and enterprise RAG are *different* data architectures even if the type taxonomy overlaps, and Oracle's 93.8% LongMemEval result is evidence of memory-system quality, not of substrate unification specifically. The substrate unification claim is thus a strong design signal, not a settled conclusion. See [01] §4, [04] §2, and [07] §3.3.

4. **No solution combines enterprise governance + Kubernetes-native self-hosted + open standard interface.** Oracle has the best governance but requires Oracle Database; AWS/Google are cloud-only; Mem0 is deployment-flexible but governance-thin; Zep deprecated its self-hosted edition. This unmet combination is RHOAI's whitespace. See [02] §8 Gap 1.

5. **Memory has become a funded value-capture layer, and the market is fragmenting.** ~$62M into pure-play memory startups in 18 months, GA features at every hyperscaler — but five-plus startups converging on near-identical technical approaches means consolidation is likely. Adopting any single startup product risks picking a non-survivor; this argues for a standards-based, backend-agnostic platform primitive. See [02] §6, §8 Gap 7.

6. **MemoryHub is Red Hat's strongest internal artifact for the governance layer.** Its six-tier scope model with SQL-level RBAC, inline curation, contradiction detection, and cache-optimized assembly are production-capable and OpenShift-native by design — but the audit trail is a stub, the Kubernetes operator is a skeleton, observability is TBD, FIPS is delegated-not-validated, and copyright is held by an individual (CLA/IP transfer needed). It is the best governance foundation and a genuine prototype, not a near-shippable product. See [03] §3, §5.

7. **OGX (formerly Llama Stack) already ships production memory primitives, and RHOAI 3.5 is GA'ing it as the Responses bridge.** Conversations (episodic/working), Vector Stores + Files (semantic), Prompts (procedural), `previous_response_id` chaining, `/responses/compact` compaction, and `AuthorizedSqlStore` ABAC tenant isolation are all in the production path *today*. The RHOAI 3.5 Responses bridge is, in effect, already a partial agent-memory substrate. See [06] §3, §5.1 and [08] §2.3.

8. **OGX's gaps are exactly the enterprise-governance dimension:** no multi-tier scope isolation (per-principal only), no knowledge graph, no curation/provenance/contradiction detection, no cross-agent shared memory, no audit trail, no retention/erasure, no inspectable compaction, no FIPS. These are precisely what a MemoryHub-derived layer addresses — OGX and MemoryHub are **complementary, not competing**. See [06] §5.2, §6.

9. **There is no memory standard, and that absence is an opportunity, not a permanent gap.** MCP is the de facto memory transport but defines no memory schema; A2A, AGENTS.md, and Open Responses each cover adjacent concerns only; PAM (arXiv) is the most complete proposal but is an unadopted research paper. A platform that ships memory primitives before standards converge gets to shape them — Red Hat's OpenShift/Kubernetes/RHEL pattern. See [05] §1, §6.

10. **Context compaction must be inspectable to be compliant.** OpenAI's compaction is opaque-optimized; Anthropic's Dreaming and MemoryHub's design are human-readable. For EU AI Act (enforcement August 2026), GDPR, and HIPAA, opaque compaction is not compliant — this is one of the most concrete near-term architectural constraints. See [02] §8 Gap 3 and [03] §4.2.

11. **Multi-session and multi-agent memory is the unsolved hard problem.** Every benchmark shows multi-session as the lowest-scoring category (Oracle 88% on LongMemEval multi-session; Mem0 48.6% overall on BEAM-10M — note these are different benchmarks and not directly comparable). This is where well-targeted RHOAI investment has the most differentiation potential — and the hardest to deliver. See [02] §7, §8 Gap 4.

12. **Memory is the first AI asset type that is itself a live, append-heavy datastore** rather than a metadata record pointing at one. This breaks the "Registry = Governance, registry does not store payload" model cleanly: Knowledge Sources resolves fine (registry points at an external source), but the memory substrate *is* the payload. The resolution: the registry governs the memory *service* as an asset and governs records with the same model — it does not become a memory store. See [08] §2.1.

13. **The single highest-severity gap for either sourcing candidate is the audit trail.** MemoryHub's is a stub (issue #67); OGX has none. An inspectable, append-only memory audit log is a hard EU AI Act / GDPR / HIPAA requirement and is GA-blocking for any compliance-facing memory feature. See [08] §3.2 D-6, §6 Q-G7.

14. **Red Hat already has an alignment channel into OGX upstream.** Francisco Arceo (an RHAISTRAT-1345 stakeholder) and Sébastien Han are core OGX contributors — Arceo drove OGX's multi-tenancy, compaction, and vector-store tenant-isolation work. Decisions in this research can directly inform what gets prioritized upstream, making the upstream-contribution posture credible rather than aspirational. See [06] §4, §5.4.

## 4. The Recommended Decomposition (PROPOSED — doc 07)

Doc 07 evaluates four candidate taxonomies — Peter's 3 areas (a product decomposition), the CoALA/Oracle 4 types (a functional taxonomy), MemoryHub's scope tiers (a governance overlay), and the Memory-vs-RAG divide (an architectural guardrail) — and finds they answer *different questions* and should not be treated as either/or. The synthesis uses each for what it is good at and proposes:

**Three subsystems:**
- **Subsystem 1 — Agent Memory Substrate.** One governed store exposing the four CoALA access patterns (working/episodic/semantic/procedural). Append-heavy, agent-written. (Peter's area 2, reframed.)
- **Subsystem 2 — Context Engineering.** A capability layer *tightly coupled to and operating over* Subsystem 1 — compaction, retrieval assembly, progressive disclosure, KV-cache-aware ordering. Named and measurable, but not an independent peer. (Peter's area 3, demoted.)
- **Subsystem 3 — Agent Knowledge.** A distinct, adjacent governed/federated enterprise-knowledge layer — enterprise-RAG / knowledge-graph-shaped, **not** semantic memory and **not** a fifth memory type. (Peter's area 1, re-typed.)

**Two cross-cutting dimensions** (apply to all three subsystems, are not subsystems themselves):
- **Governance & Scope** — scope tiers, RBAC, audit, erasure, contradiction detection, provenance, compliance. This is where "Registry = Governance" lands.
- **Deployment model** — client-side vs. server-side; RHOAI's platform tier points to server-side as default with a client-side hybrid-search path for IDE/dev-workflow agents.

The AI Asset Registry is the cross-cutting governance *framework* these subsystems are governed by — it is **not** itself a memory subsystem.

**Verdict on Peter's three original areas:**

| Area | Verdict | Why |
|------|---------|-----|
| 1 — Agent Knowledge | **REFINE (re-type)** | Real and worth keeping as a distinct subsystem, but its *type* must be pinned: it is enterprise-RAG / knowledge-graph-shaped, not semantic memory. Keep as Subsystem 3; extend the Knowledge Sources asset type. |
| 2 — Agentic Memory | **REFINE (reframe)** | The core, survives — but "short-term + long-term" frames it as two bolted-together things. Reframe as one governed substrate with four access patterns. Surface procedural memory explicitly (it overlaps the skills registry). |
| 3 — Context Engineering | **RESTRUCTURE (re-couple)** | The one area that does not hold as an independent peer. The industry treats it as a sub-discipline of memory; OGX implements compaction *inside* the Responses layer. Keep as a named, measurable subsystem but characterize it as a capability layer over the substrate, not a peer. |

## 5. The Recommended Solution Direction (PROPOSED — doc 08)

> Phasing note (2026-07-10): the release mapping below is superseded by
> the revised plan — 3.6 = DP, 3.7 = TP (Summit 2027 setup), 3.8 = GA —
> and the delivery vehicle is now a standalone memory service (see the
> refresh note above and [doc 19](19-market-direction-refresh-2026-07.md)).
> The option structure (C+D substrate, B governance, A for Agent
> Knowledge, E as backends) remains the decided baseline per REVIEW-NOTES.

Doc 08 maps the decomposition onto RHOAI/OCP component by component and evaluates five sourcing options (A — build fresh; B — productize MemoryHub; C — consume/extend OGX; D — upstream-contribute; E — partner with a memory vendor). No single option wins. The proposed direction is a **phased combination**:

- **3.5 (now):** OGX memory primitives ride along passively in the Responses bridge (Option C, passive). No new memory deliverable — but the Conversations / Vector Stores / compaction primitives *exist* and should be acknowledged in scoping. This is a fact, not a choice.
- **3.6 (target):** Two parallel tracks. **(C + D)** Expose OGX's memory primitives as governed, first-class RHOAI features *and* upstream the governance primitives (audit hooks, scope attributes) where they fit OGX's charter. **(B, Dev Preview)** Stand up a MemoryHub-derived governance layer — six-tier scope model, inline curation, contradiction detection — as the Governance & Scope service alongside the OGX substrate.
- **3.7+ (GA):** The gateway-native Responses replacement absorbs the working/episodic substrate as its "conversation state microservice"; the MemoryHub-derived governance layer reaches GA with the audit / operator / observability / FIPS gaps closed. Subsystem 3 (Agent Knowledge) is built fresh as a Knowledge Sources extension, since neither candidate has a real org-knowledge-graph implementation.
- **Throughout:** Partner products (Option E) only as pluggable-backend *compatibility*, never as the primary substrate. Upstream contribution (Option D) is the standards posture layered across all of it.

**The clearest single leaning:** OGX is the substrate, a MemoryHub-derived layer is the governance, and they are complementary — not competing. Build-fresh is reserved for Agent Knowledge; partner is reserved for backend-compatibility. The honest caveat: this phasing assumes the doc-07 decomposition is accepted at the review gate and assumes the OGX replacement plan resolves without stranding 3.6 work on the bridge.

## 6. Competitive Positioning

The field divides into three camps, none of which occupies RHOAI's target position (from [02]):

| Camp | Examples | Strength | Disqualifier for RHOAI's profile |
|------|----------|----------|----------------------------------|
| Hyperscaler managed memory | AWS AgentCore, Google Memory Bank, OpenAI server-side | GA, validated as a product feature | Cloud-only — no on-premise/air-gap path |
| Enterprise database-native | Oracle AI Agent Memory | Highest external governance maturity; per-record audit/erasure | Hard Oracle Database lock-in; not portable to OpenShift |
| OSS memory startups / frameworks | Mem0, Letta, Zep/Graphiti, Cognee; LangGraph, CrewAI, OpenClaw | Deployment-flexible, open-source, fast-moving | Governance thin or absent; market-consolidation risk; no governed enterprise tier |

**RHOAI's whitespace:** enterprise governance + Kubernetes-native self-hosted + air-gappable + open standard interface. No competitor offers all four ([02] §8 Gap 1). Red Hat's differentiators are the open-source foundation (OGX, Apache-2.0 MemoryHub), OpenShift-native deployment (UBI9, FIPS delegation, on-cluster vLLM embeddings), governance depth (MemoryHub's scope/RBAC/curation model), and a credible standards posture (AAIF Gold Member, existing OGX contributor channel). The strategic risk is timing: the hyperscalers and Oracle ship today, and a proprietary RHOAI memory API built before standards converge would inherit a migration cost — which is why doc 05 argues for building *toward* open standards from the start.

## 7. Open Questions for the Review Gate

This is the agenda for the Task 11 review session — the decisions only Peter can make. Questions are grouped; **[BLOCKS]** marks those that block Feature scoping for RHAISTRAT-1345 and must be answered before any strategy/Feature work proceeds. **[GATE — commissions a measurement task]** marks questions the gate should initiate (not answer) — the work is commissioned at the review gate and runs in parallel with early Feature scoping.

### Group A — Decomposition and Outcome scoping (the foundational decisions)

- **Q-T1 [BLOCKS] — Accept the decomposition?** Adopt the doc-07 model — 3 subsystems (Agent Memory Substrate, Context Engineering, Agent Knowledge) + 2 cross-cutting dimensions (Governance & Scope, Deployment model), with Context Engineering as a capability over the substrate and the AI Asset Registry as the governance framework — or retain Peter's 3 peer areas? Everything downstream depends on this. (Resolves Q40.) See [07] §7.
- **Q-T2 [BLOCKS] — Scope of RHAISTRAT-1345?** Scope the Outcome to Subsystem 1 only (Agent Memory Substrate + Context Engineering as an in-scope capability), and spin Agent Knowledge out as a separate Outcome — as docs 07 and 08 both recommend? Or expand the Outcome to cover all three subsystems? (Resolves Q42.) See [07] §6.1, [08] §5.
- **Q42 (registry) — Outcome boundary** is the knowledge-registry framing of Q-T2; resolving Q-T2 resolves it.

### Group B — Substrate and architecture

- **Q-T5 / Q41 / Q44 [BLOCKS] — Confirm the substrate verdict.** One substrate for the four memory types, a separate subsystem for org-wide knowledge ([07] §3.3)? Doc 08 confirms this architecturally (OGX and MemoryHub both already do it) but flags the empirical half as open — see Q-G4. This is the knowledge-registry Q41 (memory vs. RAG: distinct subsystems or one substrate?) and Q44 (RHOAI's unified-substrate equivalent and its relation to Knowledge Sources).
- **Q-G4 [GATE — commissions a measurement task] — RHOAI's actual memory workload profile.** Memory volume per user, concurrent-agent count, org-knowledge entity count. No internal source supplies these; they determine whether the single PostgreSQL+pgvector substrate holds (~50M-vector threshold) or whether Subsystem 3 needs a dedicated store. Doc 08 §5–6 frames the substrate verdict as confirmed architecturally — Q-G4 is a design-time measurement task the review gate should *commission*, not a question that must be answered *before* Feature work can proceed. See [08] §5–6.
- **Q-G2 — The OGX/Llama Stack replacement plan.** Does the gateway-native Responses replacement reimplement the memory primitives or delegate to OGX? If it reimplements conversation state / vector stores / compaction, that team owns Subsystem 1's working/episodic slice and the memory-team boundary moves. (Knowledge-registry Q38.) See [08] §6.
- **Q-T3 / Q-MH-2 — Scope-tier count.** Is MemoryHub's six tiers (user/project/campaign/role/organizational/enterprise) the right abstraction, or is it over-complex? `campaign`, `organizational`, and `enterprise` have no native OpenShift analogue. See [07] §7, [03] §6.
- **Q-T7 — Identity memory?** Does the decomposition need an explicit "Identity memory" element (PAM's fifth type — persistent persona attributes), or is that adequately a slice of semantic memory? See [07] §7.

### Group C — Sourcing and delivery

- **Q-G1 [BLOCKS] — Accept the phased sourcing recommendation?** OGX as substrate (C) + MemoryHub-derived governance layer (B) as a 3.6 Dev Preview + build-fresh (A) for Agent Knowledge + upstream-contribute (D) as standards posture + partner (E) only as pluggable-backend compatibility? Or commit to a single option? See [08] §4.7, §6.
- **Q1 / Q2 / Q3 (doc 06) — RHOAI 3.5 OGX bridge scope.** Which OGX APIs are actually exposed in 3.5 (only Responses, or also Conversations / Vector Stores / Prompts / Files)? Does the 3.5 deployment include Arceo's May-2026 multi-tenancy work or a pre-multi-tenancy pin? What is the concrete replacement plan? The memory-primitive strategy changes materially with each answer. See [06] §7.
- **Q4 / Q-G1-adjacent — Red Hat's posture toward OGX:** consume, extend-with-contributions, or fork/embed? Arceo's contributions imply "extend," but there is no documented decision. See [06] §7.

### Group D — Governance, compliance, and identity

- **Q-G7 [BLOCKS, highest severity] — Audit-trail delivery plan.** Neither candidate ships a working audit trail (MemoryHub stub, OGX none) and EU AI Act enforcement is August 2026. What is the delivery plan, and does it gate a 3.6 memory Dev Preview? Cannot be deferred past the review gate. See [08] §6.
- **Q-G3 / Q-A1 — Memory as a registry asset.** Is a productized memory service a governed asset in the AI Asset Registry, and are *individual memory records* also registry-governed, or only the service? Resolving the payload-vs-metadata tension. Needs an explicit decision with AI Asset Registry owners. See [08] §2.1, §6.
- **Q-G5 / Q-A2 — Actor-chain RBAC for shared memory.** How does a memory service enforce the AI Gateway's lowest-permission rule when agent B reads org-scoped memory on behalf of agent A's user? Neither MemoryHub nor OGX documents a multi-actor-chain RBAC model — a privilege-escalation risk if unaddressed. See [08] §6.
- **Q-G6 / Q-MH-3 — Platform identity vs. standalone auth.** Should a productized memory service consume RHOAI platform identity (Spire/Authbridge, RFC 8693 token exchange) and drop MemoryHub's standalone OAuth 2.1 server? Doc 08 recommends yes; it is a cross-team integration decision. See [08] §6.
- **Q43 (registry) — Client-side vs. server-side.** Which side should memory primitives live on; should the platform support both? Doc 07 makes this a cross-cutting dimension (server-side default, client-side hybrid path for IDE agents) — the review gate should confirm. See [01] §3.

### Group E — Cross-domain boundaries and standards

- **Q-T4 / Q11 (doc 06) — Procedural memory vs. skills registry vs. OGX Prompts.** Where exactly is the boundary between skills-as-registry-artifacts, OGX's runtime Prompts API, and dynamically agent-learned procedural memory in the substrate? Doc 08 §5 proposes a three-layer model with a promotion-with-HITL handoff, but it remains a cross-team design question to be agreed before either the skills team or the memory team builds. See [07] §7, [08] §5.
- **Q-T6 — Agent Knowledge as a Knowledge Sources extension?** Is Subsystem 3 the governed realization of the existing Knowledge Sources asset type (doc 08's recommendation), or a new asset type? A registry-framework change requiring a decision with AI Asset Registry owners. See [08] §5.
- **Q-G8 — Standards program.** Should Red Hat pursue the doc-05 §6.2 opportunities — an MCP Memory Convention SEP, an A2A AgentCard memory binding, and/or an AAIF memory project — as part of the agent-memory program, and on what timeline relative to 3.6/3.7 product work? See [08] §6.

### Question-source cross-reference

| Source | Questions |
|--------|-----------|
| Knowledge registry Q40–Q44 | Q40→Q-T1; Q41→Q-T5 group; Q42→Q-T2; Q43→Group D; Q44→Q-T5 group |
| Doc 07 §7 (Q-T1…Q-T7) | All carried forward; Q-T1/T2/T5 block Feature scoping |
| Doc 08 §6 (Q-G1…Q-G8) | All carried forward; Q-G1/G7 block Feature scoping; Q-G4 is a gate-commissioned measurement task |
| Doc 06 §7 (Q1…Q12) | Q1–Q4, Q11 surfaced above; remainder are design-shaping, not gate-blocking |
| Doc 03 §6 (Q-MH-1…Q-MH-5) | Q-MH-1 (IP transfer, administrative), Q-MH-2→Q-T3, Q-MH-3→Q-G6 |

---

## 8. Phase 2 Research Document Index (2026-06-09)

Phase 2 research was commissioned at the first Agent Memory Team Sync (2026-06-09) to address 13 gaps identified by cross-referencing Phase 1 research against team sync discussions, workstream tasks, and the RFE roadmap. Approach: breadth-first with living plans. See [Phase 2 Research Design Spec](https://github.com/solaius/ai-asset-registry/blob/main/docs/superpowers/specs/2026-06-09-agent-memory-phase2-research-design.md).

### New Documents (09–15)

| # | Document | What It Covers |
|---|----------|----------------|
| 09 | [Agent Harness Memory](09-agent-harness-memory.md) | Comparative analysis of 5 agent harnesses (OpenClaw, Hermes, Claude Code, Codex CLI, Gemini CLI) — memory architectures, 7 cross-harness patterns (filesystem-native, layered override, memory-as-MCP, dream consolidation, git-native), RHOAI platform capability recommendations. |
| 10 | [Claude Memory & Dreaming](10-claude-memory-dreaming.md) | Deep dive into Anthropic's 4-layer memory system and Auto Dream consolidation mechanism; Harvey 6x case study; pluggability analysis and "Open Dreaming" CRD architecture sketch; comparison with Mem0/Zep/Letta consolidation approaches. |
| 11 | [Adversarial Memory](11-adversarial-memory.md) | Security threat model: OWASP ASI06 classification, 6 attack vectors (SpAIware, PoisonedRAG, MINJA >95% success, MemoryGraft, MemMorph, sleeper poisoning), real-world incidents, defense taxonomy by memory lifecycle phase, mnemonic sovereignty framework, RHOAI security architecture recommendations. |
| 12 | [Benchmarking & Evaluation](12-benchmarking-evaluation.md) | Survey of 7 academic benchmarks (LongMemEval, BEAM, LoCoMo, MemoryArena, MemoryAgentBench, AMA-Bench, Memora); competitive leaderboard data; enterprise evaluation gaps (compliance, multi-tenant, security); Red Hat benchmarking harness design (5-phase pipeline, pluggable backends, OpenShift-native execution). |
| 13 | [KV-Cache Optimization](13-kv-cache-optimization.md) | How KV-cache optimization relates to agent memory; vLLM PagedAttention and prefix caching; llm-d 57x TTFT improvement via cache-aware routing; memory-ordering impact on cache hit rates; Red Hat differentiator analysis (cross-layer memory-inference coupling); connection to RFE-M4. |
| 14 | [Enterprise Use Cases](14-enterprise-use-cases.md) | Agent memory use cases across 6 verticals (healthcare, financial services, ITOps/SRE, legal, manufacturing, defense); benchmark-to-production gap (91.6% benchmark vs ~49% at scale); cross-vertical convergence on platform requirements; RFE roadmap validation; 3 roadmap gaps identified. |
| 15 | [Multi-Modal Memory](15-multi-modal-memory.md) | Forward-looking horizon assessment (12-24 months): multi-modal memory concepts, 7 implementations (MemVerse, M3-Agent, OmniMem +411% F1, Supermemory, Reminisce), technical challenges (storage asymmetry, cross-modal retrieval), three-phase RHOAI plan (convert-to-text bridge → multi-modal embeddings → full providers). |

### Existing Documents Updated

| Doc | Addition | Phase 2 Gap Addressed |
|-----|----------|-----------------------|
| [02 Solution Survey](02-solution-survey.md) | §2.7 OpenViking/ByteDance analysis — AGPL-3.0 license (hard productization blocker), filesystem-paradigm architecture, tiered context loading, pattern-extraction value | #8 — OpenViking assessment |
| [03 MemoryHub Deep-Dive](03-memoryhub-deep-dive.md) | §7 Adoption Decision Assessment — current status, IP transfer analysis, architecture fit (5 strong/2 partial/1 partial alignment), 3-option decision framework, hybrid path recommendation | #12 — MemoryHub adoption decision |
| [04 Technical Patterns](04-technical-patterns.md) | §9 expanded from ~700 to ~3,400 words — 5 multi-agent architectures, scope isolation (actor chain problem, IETF drafts), coordination/consistency models, anti-patterns (87% contamination cascade, MINJA), enterprise regulatory requirements, 6-framework implementation survey | #9 — Multi-agent memory patterns |
| [08 RHOAI & OCP Alignment](08-rhoai-ocp-alignment.md) | §7 Kagenti Integration (AgentRuntime/AgentCard CRDs, SPIFFE identity, agent-sandbox, gap analysis) + §8 Storage Backend Trade-offs (PostgreSQL+pgvector recommended, Redis hot cache, no vector DB has Red Hat OCP certification, decision framework) | #7, #13 — Kagenti and storage |

## 9. Phase 2 Key Findings

Building on the 14 Phase 1 key findings above, Phase 2 research surfaces these additional insights:

15. **Filesystem-native Markdown memory is the universal harness pattern.** All 5 surveyed agent harnesses (OpenClaw, Hermes, Claude Code, Codex CLI, Gemini CLI) use Markdown files as their primary memory format with layered override semantics. RHOAI must support this pattern as a first-class memory surface — not just API-based memory. See [09] §6.

16. **Memory-as-MCP is the most strategically important emerging pattern.** OpenClaw and Hermes already expose memory through MCP servers. This aligns directly with RHOAI's MCP Gateway strategy — memory becomes a governed MCP tool with per-tool authorization, metrics, and audit logging via the gateway. See [09] §6, [RFE-M5].

17. **Dream consolidation is a validated production pattern, not a research curiosity.** Claude's Auto Dream mechanism (4-phase: orient→gather→consolidate→prune) and Codex CLI's async Memories pipeline both demonstrate scheduled memory consolidation at scale. Harvey reports 6x task completion improvement. An "Open Dreaming" equivalent on RHOAI is a feasible medium-term capability. See [10] §3–4.

18. **Memory security is an existential concern, not a feature.** MINJA achieves >95% injection success via query-only interaction (no elevated privileges needed). SpAIware persists across sessions through document injection. Memory contamination in one agent propagates to 87% of downstream agents within 4 hours. OWASP's ASI06 classification and the mnemonic sovereignty framework establish the minimum security architecture. See [11] §2–5.

19. **The benchmark-to-production gap is severe and under-measured.** Mem0 scores 91.6% on LoCoMo but drops to ~49% at 50,000 production sessions (BEAM-10M). No existing benchmark tests enterprise requirements (compliance, multi-tenant isolation, security, governance). The proposed Red Hat benchmarking harness fills this gap with a 5-phase pipeline and enterprise evaluation modules. See [12] §2, §6.

20. **KV-cache optimization is a platform differentiator only RHOAI can deliver.** The ordering of memory items in the context window directly determines KV-cache hit rates — static prefixes before dynamic content yields 74% hit rates and 59% cost reduction. llm-d's prefix-cache-aware routing achieves 57x TTFT improvement. The memory→cache→inference coupling is a cross-layer optimization only a platform vendor with control over all three layers can optimize end-to-end. See [13] §5, §7.

21. **All six enterprise verticals independently converge on the same platform requirements.** Healthcare, financial services, ITOps, legal, manufacturing, and defense all require scope isolation, audit trails, inspectable compaction, and write-path governance — the mechanism is the same, the policy differs. This validates RFE-M3 (governance) and RFE-M6 (audit trail) as the enterprise linchpin RFEs. See [14] §9.

22. **No dedicated vector database has achieved Red Hat OpenShift Operator Certification.** PostgreSQL+pgvector (via Crunchy PGO or EDB, both Red Hat Certified) and Redis Enterprise (Red Hat Certified) are the only certified storage options. This confirms the recommended hybrid architecture: PostgreSQL+pgvector as unified MVP store + Redis as hot cache. See [08] §8.

23. **OpenViking (ByteDance) is architecturally interesting but AGPL-3.0 licensed — a hard productization blocker.** The license changed from Apache 2.0 to AGPL-3.0 in v0.2.15 (~March 2026). The filesystem-paradigm and tiered context loading patterns are extractable value; the code itself cannot be used. See [02] §2.7.

24. **Multi-modal memory is a medium-term horizon (12-24 months), not a 3.5 requirement.** The near-term pragmatic path is convert-to-text (caption images, transcribe audio). Schema extensibility (`source_modality`, `source_reference` fields) should be baked in now as a low-cost future-proofing measure. See [15] §8.

## 10. Self-Check and Reconciliation Note

**Document set reconciliation (Phase 1):** The eight research documents (01–08), plus this executive summary (00), were checked for structural consistency. Filenames and titles align with the planned scaffold. No renumbering, splitting, or merging was needed — the set is consistent. No research content was modified.

**Phase 2 reconciliation (2026-06-09):** Seven new documents (09–15) and four existing-document updates (02, 03, 04, 08) were added per the [Phase 2 Research Design Spec](https://github.com/solaius/ai-asset-registry/blob/main/docs/superpowers/specs/2026-06-09-agent-memory-phase2-research-design.md). All new documents follow the Phase 1 series format. Series navigation links across all documents have been updated to include the full 16-document set.

**This document:** synthesizes; it does not decide. Phase 1 recommendations relayed from docs 07 and 08 were PROPOSED at Phase 1 and are now DECIDED per [REVIEW-NOTES](REVIEW-NOTES.md). Phase 2 findings (docs 09–15) are EXPLORATORY. Every key finding traces to a source document.

## 11. Sources

| Source | Path / Reference |
|--------|------------------|
| Agent Memory & Knowledge seed doc | `docs/knowledge-review/assets/agent-memory-knowledge.md` |
| Knowledge Registry — §13 Open Questions Q40–Q44 | `docs/knowledge-registry.md` |
| Research documents 01–08 | `agent-memory/research/01-…` through `08-…` |
| Agent Registry Research Executive Summary (structure/rigor calibration) | `agents/agent-registry/research/00-executive-summary.md` |
| RHAISTRAT-1345 (Outcome: Agent Memory Primitives) | https://redhat.atlassian.net/browse/RHAISTRAT-1345 |

This is a synthesis document. It introduces no new external research; every substantive claim traces to one of the eight research documents (01–08) — plus this executive summary (00) making nine documents in the series total — which carry their own primary-source attribution and access notes.
