---
title: Agent Memory & Knowledge: Taxonomy and Decomposition
description: Synthesis of wave-1 research answering how the agent memory/knowledge problem space should be decomposed for RHOAI.
source: ai-asset-registry/agent-memory/research/07-taxonomy-and-decomposition.md (as of 2026-07-05)
timestamp: 2026-07-06
review_after: 2026-08-05
---

# Agent Memory & Knowledge: Taxonomy and Decomposition

**Purpose:** Synthesize wave-1 research (docs 01–06) to answer the central question of this research series — how the agent memory and knowledge problem space should be decomposed for RHOAI — by evaluating Peter Double's initial 3-area framing against competing taxonomies and recommending a decomposition.

**Date:** 2026-05-17

**Status:** EXPLORATORY for the analysis; the recommended decomposition in Section 4 is **PROPOSED** — a research recommendation for the review gate, not a decided RHOAI design. See [RHAISTRAT-1345](https://redhat.atlassian.net/browse/RHAISTRAT-1345).

**Series:** Document 07 of 17 — Agent Memory & Knowledge Research
**Phase 1:** [00](00-executive-summary.md) · [01](01-landscape-and-definitions.md) · [02](02-solution-survey.md) · [03](03-memoryhub-deep-dive.md) · [04](04-technical-patterns.md) · [05](05-standards-and-protocols.md) · [06](06-ogx-memory-primitives.md) · 07 Taxonomy & Decomposition (this doc) · [08](08-rhoai-ocp-alignment.md)
**Phase 2:** [09](09-agent-harness-memory.md) · [10](10-claude-memory-dreaming.md) · [11](11-adversarial-memory.md) · [12](12-benchmarking-evaluation.md) · [13](13-kv-cache-optimization.md) · [14](14-enterprise-use-cases.md) · [15](15-multi-modal-memory.md) · [16](16-ai-gateway-memory-substrate.md) · [REVIEW-NOTES](REVIEW-NOTES.md)

---

## Contents

1. [The Central Question](#1-the-central-question)
2. [Candidate Taxonomies, Side by Side](#2-candidate-taxonomies-side-by-side)
3. [Evaluation Criteria and Comparative Assessment](#3-evaluation-criteria-and-comparative-assessment)
4. [Recommended Decomposition for RHOAI (PROPOSED)](#4-recommended-decomposition-for-rhoai-proposed)
5. [Verdict on Peter's Three Areas](#5-verdict-on-peters-three-areas)
6. [Mapping onto RHAISTRAT-1345 and the AI Asset Registry](#6-mapping-onto-rhaistrat-1345-and-the-ai-asset-registry)
7. [Open Questions for the Review Gate](#7-open-questions-for-the-review-gate)
8. [Sources](#8-sources)

---

## 1. The Central Question

**EXPLORATORY** — RHAISTRAT-1345 ("Agent Memory Primitives") is an Outcome with no child Features. Before Features can be authored, the problem space must be decomposed correctly: a wrong decomposition produces wrong Outcome boundaries, wrong API surfaces, and wrong cross-team handoffs ([01 Landscape & Definitions](01-landscape-and-definitions.md) §5).

The project owner, Peter Double, proposed an initial decomposition into three areas ([agent-memory-knowledge seed doc](/features/agent-memory/research/agent-memory-landscape-research.md) §1):

| # | Area | Working definition |
|---|---|---|
| 1 | **Agent Knowledge** | A graph knowledge layer organizing/accessing everything related to the org — regulations, policies, rules, product knowledge, code, processes — scoped from a team to the whole company. |
| 2 | **Agentic Memory** | Short-term conversational memory and long-term context persistence. |
| 3 | **Context Engineering / Management** | How to gather, construct, and compact session context for agents. |

Peter explicitly flagged this framing as a hypothesis to validate, not a decision. This document's job is to confirm, refine, or restructure it. Two specific tensions were surfaced in wave-1 research and **must** be adjudicated here, not deferred:

- **Tension A — Context engineering's status.** [01 Landscape & Definitions](01-landscape-and-definitions.md) §1.3 found that the industry (Mem0, The New Stack, Weaviate) treats "context engineering" as a *sub-discipline of memory management*, not a third peer area. Mem0 calls memory "one of the core pillars of context engineering"; The New Stack calls memory "a new paradigm of context engineering." The two are tightly coupled, not parallel tracks.
- **Tension B — "Agent Knowledge" maps to two different things.** [01 Landscape & Definitions](01-landscape-and-definitions.md) §1.2 and §2 found that Peter's "Agent Knowledge" maps to *either* semantic-memory-in-a-unified-substrate (the Oracle/CoALA reading) *or* enterprise-RAG-with-governance (the Wes Jackson / memory-vs-RAG reading) — two fundamentally different data architectures (database vs. search). This ambiguity cannot survive into Feature scoping.

This document resolves both.

---

## 2. Candidate Taxonomies, Side by Side

Wave-1 research surfaced four distinct decompositions of the space. They are not all answers to the same question — and recognizing that is the key to the synthesis (see Section 3.2).

### 2.1 Taxonomy A — Peter's 3-Area Split (functional/scoping)

Knowledge / Memory / Context Engineering. Organizes the space by **what platform concern is being addressed**: an org-knowledge layer, a learned-state store, and a context-construction discipline. It is a *product decomposition* — it answers "what subsystems or Outcomes should we build." Source: [agent-memory-knowledge seed doc](/features/agent-memory/research/agent-memory-landscape-research.md) §1.

### 2.2 Taxonomy B — CoALA / Oracle 4-Type Model (functional/cognitive)

Working / Semantic / Episodic / Procedural memory. Derived from cognitive science (Soar, ACT-R) and formalized for LLM agents by the CoALA paper (arXiv:2309.02427), it is the dominant academic and vendor taxonomy — used by Oracle, IBM, Atlan, Mem0 (minus working memory), and most frameworks ([01 Landscape & Definitions](01-landscape-and-definitions.md) §4). It organizes the space by **what kind of information is stored and how it is accessed**.

Critically, Oracle attaches an architectural claim to this taxonomy: the four types are **not four systems but four access patterns over one governed substrate** ([01](01-landscape-and-definitions.md) §4.5; [04 Technical Patterns](04-technical-patterns.md) §2.4; [seed doc](/features/agent-memory/research/agent-memory-landscape-research.md) §4). This is the single most important architectural signal in the external survey ([02 Solution Survey](02-solution-survey.md) §3.1).

### 2.3 Taxonomy C — MemoryHub Scope-Tier Model (governance/access)

user / project / campaign / role / organizational / enterprise. This is **orthogonal** to Taxonomies A and B: it does not classify *kinds* of memory, it classifies *who can read/write a memory record and what governance applies* ([03 MemoryHub Deep-Dive](03-memoryhub-deep-dive.md) §3.1; [04 Technical Patterns](04-technical-patterns.md) §7.1). Any memory of any CoALA type can sit at any scope tier. The seed doc itself observes this tier model "closely parallels Peter's area-1 framing of team→company knowledge scoping" ([seed doc](/features/agent-memory/research/agent-memory-landscape-research.md) §3).

The deployed model has six tiers, not the five named in MemoryHub's README — `campaign` was added April 2026 ([03](03-memoryhub-deep-dive.md) §3.1). The wave-1 research flags this six-tier model as possibly over-complex for a product ([03](03-memoryhub-deep-dive.md) §5.3 Gap 7, Q-MH-2).

### 2.4 Taxonomy D — Memory vs. RAG Architectural Divide

A two-way split by **data architecture and write path** ([01 Landscape & Definitions](01-landscape-and-definitions.md) §2; [seed doc](/features/agent-memory/research/agent-memory-landscape-research.md) §6). RAG = read-only retrieval over a stable, batch-indexed external corpus ("what does the manual say?"); agent memory = a stateful, append-heavy store agents *write to* during interaction ("what have agents learned?"). Wes Jackson's formulation: memory is a database concern (consistency, audit, retention), RAG is a search concern. A research citation formalizes the data-shape difference: "RAG targets large heterogeneous corpora; agent memory involves bounded, coherent dialogue streams" (arXiv:2602.02007, via [01](01-landscape-and-definitions.md) §2).

### 2.5 Two more decompositions surfaced in docs 01–06

- **The "fifth type" — organizational context memory.** Atlan proposes a fifth memory type beyond CoALA's four: certified assets, data-event history, versioned access policies, cross-system entity identity — requiring *runtime governance enforcement*, not just fact retrieval ([01](01-landscape-and-definitions.md) §4.5, Contradiction 3). If adopted, "the AI Asset Registry itself becomes a memory subsystem." (Caveat: this originates from a data-catalog vendor's marketing blog and is not academically corroborated — treat as practitioner opinion.) PAM (arXiv:2605.11032) independently adds a fifth type — *Identity memory* — to the CoALA four ([05 Standards & Protocols](05-standards-and-protocols.md) §3.4).
- **Client-side vs. server-side memory.** A deployment-model fork, not a content taxonomy: where memory physically lives ([01](01-landscape-and-definitions.md) §3; Francisco Arceo's RHAISTRAT-1345 comment). Like Taxonomy C, this is orthogonal to A/B and a separable design axis.

### 2.6 Side-by-side summary

| Taxonomy | Organizing axis | Question it answers | Type | Primary sources |
|---|---|---|---|---|
| **A — Peter's 3 areas** | Platform concern | What subsystems/Outcomes to build | Product decomposition | [seed doc](/features/agent-memory/research/agent-memory-landscape-research.md) §1 |
| **B — CoALA/Oracle 4 types** | Information kind / access pattern | What is stored and how it is read | Functional/cognitive taxonomy | [01](01-landscape-and-definitions.md) §4; arXiv:2309.02427 |
| **C — MemoryHub scope tiers** | Access control / governance | Who can read/write; what governance applies | Governance taxonomy (orthogonal) | [03](03-memoryhub-deep-dive.md) §3.1 |
| **D — Memory vs. RAG** | Data architecture / write path | Search corpus vs. append-heavy database | Architectural divide | [01](01-landscape-and-definitions.md) §2 |

The four are **not competitors for the same slot.** A and D are product/architecture decompositions; B is a functional taxonomy; C is a governance overlay. The synthesis error to avoid is treating "should we use Peter's 3 areas or CoALA's 4 types" as an either/or — they answer different questions. The real question is: *which product decomposition (A-shaped) best fits RHOAI, and how do B, C, and D inform it.*

---

## 3. Evaluation Criteria and Comparative Assessment

### 3.1 Criteria

Five criteria, derived from the scoping concerns in [01 Landscape & Definitions](01-landscape-and-definitions.md) §5 and the RHOAI platform profile in [02 Solution Survey](02-solution-survey.md) and [05 Standards & Protocols](05-standards-and-protocols.md) §5.4:

1. **Clarity** — Are the boundaries unambiguous? Can a Feature be assigned to exactly one area without overlap?
2. **Completeness** — Does it cover the whole space (working/episodic/semantic/procedural memory, context construction, org knowledge, governance) with no gaps?
3. **Fit to "Registry = Governance"** — RHOAI's organizing principle is Registry = Governance, Catalog = Discovery (project `CLAUDE.md`). Governance recurs as the consistent enterprise differentiator across MemoryHub and Oracle ([seed doc](/features/agent-memory/research/agent-memory-landscape-research.md) §7). Does the decomposition put governance in the right place?
4. **Implementation tractability** — Does it map onto buildable subsystems with clean API surfaces and clear cross-team handoffs (notably to the skills registry and the OGX bridge)?
5. **Substrate question** — Does it correctly treat "are memory and knowledge one substrate or two systems" — the central design problem ([02](02-solution-survey.md) §8 Gap 5)?

### 3.2 Comparative assessment

**Taxonomy A — Peter's 3 areas.**
- *Clarity:* Mixed. Areas 2 and 3 overlap badly — context engineering (gather/construct/compact session context) is operationally inseparable from memory (what persists and how it is retrieved). [01](01-landscape-and-definitions.md) §1.3 documents the industry collapsing the two. Area 1 vs. area 2 is the Tension-B ambiguity.
- *Completeness:* Good at the headline level — it does name org-knowledge, learned state, and context construction. It under-specifies procedural memory (skills/behavioral rules), which is a real cross-domain concern ([01](01-landscape-and-definitions.md) §4.4) and a live overlap with the skills registry.
- *Fit to Registry = Governance:* Neutral. Governance is implicit, not a first-class dimension. The decomposition does not itself surface scope/audit/erasure.
- *Tractability:* Weak as-is. A 3-Outcome split with overlapping areas 2/3 would produce two teams building the same compaction primitive ([01](01-landscape-and-definitions.md) §5.5).
- *Substrate question:* Area 1 vs. area 2 *presupposes* an answer (two systems) that the strongest evidence contradicts (Oracle's one-substrate argument).

**Taxonomy B — CoALA/Oracle 4 types.**
- *Clarity:* High as a vocabulary; the four types are well-defined and near-universally cited.
- *Completeness:* High for memory *content*; it does not, by itself, name context construction as a concern (Mem0's 3-type variant explicitly folds working memory into "context management" separately — [01](01-landscape-and-definitions.md) §4.5). It also does not name governance.
- *Fit to Registry = Governance:* Neutral — it is a content taxonomy. But Oracle's *architectural* claim (one substrate) is exactly what makes uniform governance possible ([04](04-technical-patterns.md) §2.4): you cannot govern four bolted-together stores uniformly.
- *Tractability:* The one-substrate reading is the most tractable architecture in the survey — single PostgreSQL+pgvector backend, one interface to secure and audit ([03](03-memoryhub-deep-dive.md) §2.1, §5.5; [04](04-technical-patterns.md) §2.1). But "4 types" is a poor *product* decomposition: you would not ship four Outcomes named Working/Episodic/Semantic/Procedural — they are access patterns, not subsystems.
- *Substrate question:* This is its central strength. Oracle's "four access patterns over one substrate" is corroborated by MemoryHub (all types through one pgvector backend) and is the recommended answer ([02](02-solution-survey.md) §8 Gap 5; [04](04-technical-patterns.md) §2.4).

**Taxonomy C — MemoryHub scope tiers.**
- *Clarity:* High within its axis.
- *Completeness:* Not a complete decomposition on its own — it says nothing about *what kind* of memory or about context construction. It is an overlay.
- *Fit to Registry = Governance:* Highest of all four. Scope tiers + SQL-level RBAC + audit + erasure are governance made concrete ([03](03-memoryhub-deep-dive.md) §3; [04](04-technical-patterns.md) §7). This is the dimension that turns a memory store into a *governed* memory store.
- *Tractability:* The six-tier model is buildable but flagged as possibly over-complex ([03](03-memoryhub-deep-dive.md) §5.3 Gap 7). A product likely needs fewer tiers.
- *Substrate question:* Indirectly supportive — a scope hierarchy is far simpler to enforce over one substrate than across many.

**Taxonomy D — Memory vs. RAG.**
- *Clarity:* High and operationally important — write-path presence is a crisp test ([01](01-landscape-and-definitions.md) §2).
- *Completeness:* Two-way only; it does not subdivide memory.
- *Fit to Registry = Governance:* High — it correctly predicts that memory and RAG need *different governance models* (memory: append-heavy, retention, erasure; RAG: batch-indexed, document-level provenance — [01](01-landscape-and-definitions.md) §5.2).
- *Tractability:* High — it tells you not to conflate a memory service and a RAG service in one feature.
- *Substrate question:* This is the *counterweight* to Oracle's one-substrate argument. Oracle says four memory types unify; the Memory-vs-RAG divide says memory and large-corpus knowledge retrieval do *not* unify well — different data shapes, different cost drivers. The honest synthesis (Section 4) must hold both.

### 3.3 The adjudication of the substrate question

Two evidence streams point in apparently opposite directions and must be reconciled:

- **One substrate:** Oracle and MemoryHub both argue/implement a single governed backend for the four memory types ([04](04-technical-patterns.md) §2.4; [02](02-solution-survey.md) §3.1).
- **Not one substrate:** Memory ≠ RAG; org-wide knowledge at 50M–100M+ entities (a practitioner estimate, not a formal benchmark) has a different data shape and cost profile than bounded per-user/per-project memory streams ([01](01-landscape-and-definitions.md) §2; [04](04-technical-patterns.md) §2.2, §6.4).

These are reconcilable because they are claims about *different boundaries*:

- The four CoALA memory **types** genuinely *can and should* unify on one substrate — they are all bounded, append-heavy, agent-written, governance-identical. The evidence (MemoryHub pgvector consolidation, [04](04-technical-patterns.md) §2.1 scale thresholds showing pgvector competitive under ~50M vectors) supports this; Oracle's 93.8% LongMemEval result is evidence of memory-system quality, not of substrate unification specifically. **Verdict: unify.**
- Org-wide enterprise **knowledge** (Peter's area 1) is *not* a fifth CoALA memory type — it is a different architecture: large, batch-indexed, read-mostly, with document-level provenance, that approaches the scale (50M–100M+ entities — a practitioner estimate, not a formal benchmark) where dedicated stores become defensible ([04](04-technical-patterns.md) §2.2, §6.4). It is closer to enterprise RAG / GraphRAG ([02](02-solution-survey.md) §4.4 — "GraphRAG is most relevant to Peter's area 1… not operational agent memory"). **Verdict: do not force into the memory substrate; treat as a distinct, adjacent, governed knowledge subsystem.**

So the substrate question has a *two-part* answer: **one substrate for memory, a separate (governed, federated) subsystem for org-wide knowledge** — joined by a governance model and a retrieval interface, not by a shared storage engine. This directly resolves Tension B.

---

## 4. Recommended Decomposition for RHOAI (PROPOSED)

**PROPOSED** — This is a research recommendation for the review gate. It is not a decided RHOAI architecture. It restructures Peter's 3 areas into **three subsystems plus two cross-cutting dimensions**, using Taxonomy A as the product spine, B as the internal model, C and D as the resolving evidence.

### 4.1 The recommended decomposition

```
                     ┌─────────────────────────────────────────────┐
   CROSS-CUTTING  ──▶ │  Governance & Scope (Taxonomy C overlay)     │
   (apply to all)     │  Deployment model: client-side / server-side │
                     └─────────────────────────────────────────────┘
                                       applies to ↓
   ┌────────────────────┐  ┌────────────────────┐  ┌────────────────────┐
   │ 1. AGENT MEMORY     │  │ 2. CONTEXT          │  │ 3. AGENT KNOWLEDGE  │
   │    SUBSTRATE         │  │    ENGINEERING      │  │    (org knowledge)  │
   │                     │  │   (capability layer │  │                     │
   │ ONE governed store; │  │    over the         │  │ Distinct, adjacent  │
   │ 4 CoALA access      │  │    substrate)       │  │ governed/federated  │
   │ patterns: working/  │  │                     │  │ knowledge layer;    │
   │ episodic/semantic/  │  │ compaction, retrieval│  │ enterprise-RAG /    │
   │ procedural          │  │ assembly, progressive│  │ knowledge-graph     │
   │                     │  │ disclosure, KV-cache │  │ shape               │
   └────────────────────┘  └────────────────────┘  └────────────────────┘
        append-heavy DB         tuneable discipline       batch-indexed search
```

**Subsystem 1 — Agent Memory Substrate.** A single governed memory store exposing the four CoALA access patterns (working, episodic, semantic, procedural). This is Peter's area 2, but reframed: not "short-term + long-term" as two things, but *one substrate, multiple access patterns* per Oracle's argument ([01](01-landscape-and-definitions.md) §4.5; [04](04-technical-patterns.md) §2.4). It is append-heavy, agent-written, governed (Taxonomy D's "memory" side). This is where MemoryHub and OGX's Conversations/Vector Stores/Prompts primitives sit ([03](03-memoryhub-deep-dive.md); [06 OGX Memory Primitives](06-ogx-memory-primitives.md) §5.1).

**Subsystem 2 — Context Engineering.** *A subsystem tightly coupled to the Memory Substrate — a capability layer over it, not a fully independent peer.* It covers compaction, retrieval assembly, progressive disclosure, and KV-cache-aware ordering — operations that act on what the substrate stores and on the inference-time context window. It is named as the third-of-three subsystems for counting and tracking purposes, but architecturally it operates *on* Subsystem 1 rather than standing alongside it. **Rationale:** [01](01-landscape-and-definitions.md) §1.3 documents the industry treating context engineering as a sub-discipline of memory; OGX implements compaction *inside* the Responses API, not as a separate service ([06](06-ogx-memory-primitives.md) §3.3). It retains its own quality metrics (token efficiency at a quality threshold — [01](01-landscape-and-definitions.md) §5.5; [02](02-solution-survey.md) §8 Gap 6) so it remains a *tracked, measurable* subsystem — but it does not warrant a separate Outcome independent of the Memory Substrate.

**Subsystem 3 — Agent Knowledge.** Peter's area 1, *kept as a distinct subsystem but explicitly re-typed*: it is **not** semantic memory and **not** a fifth CoALA memory type. It is a governed, federated enterprise-knowledge layer (regulations, policies, product knowledge, code, processes) with an enterprise-RAG / knowledge-graph data architecture — batch-indexed, read-mostly, document-provenance ([02](02-solution-survey.md) §4.4; [04](04-technical-patterns.md) §6). It is adjacent to the memory substrate, not inside it. It naturally extends the existing AI Asset Registry **Knowledge Sources** asset type (Section 6).

**Cross-cutting dimension 1 — Governance & Scope (Taxonomy C).** Scope tiers, RBAC, audit, erasure, contradiction detection, provenance, compliance. Applies uniformly to all three subsystems. It is *not* a subsystem — it is the dimension that makes each subsystem a *governed* subsystem, and it is where "Registry = Governance" lands ([04](04-technical-patterns.md) §7; [03](03-memoryhub-deep-dive.md) §3).

**Cross-cutting dimension 2 — Deployment model.** Client-side vs. server-side ([01](01-landscape-and-definitions.md) §3). RHOAI's platform tier points to self-hosted server-side as the default, with a client-side hybrid-search path for IDE/dev-workflow agents. Orthogonal to all three subsystems.

### 4.2 Why this is the right decomposition

- **It resolves both flagged tensions.** Tension A: Context Engineering is kept as a named subsystem (Subsystem 2) but characterized as a capability layer tightly coupled to / operating over the Memory Substrate, not a fully independent peer (Section 4.1, Subsystem 2). Tension B: "Agent Knowledge" is explicitly re-typed as enterprise-RAG-shaped, not semantic-memory-shaped, and kept as a separate subsystem (Section 3.3 adjudication).
- **It is honest about the substrate question.** One substrate for the four memory types; a separate subsystem for org knowledge. It holds both the Oracle one-substrate evidence and the Memory-vs-RAG divide without contradiction.
- **It is buildable and matches what exists.** Subsystem 1 ≈ OGX memory primitives + MemoryHub-style governance ([06](06-ogx-memory-primitives.md) §6 "OGX and MemoryHub are complementary"). Subsystem 3 ≈ AI Asset Registry Knowledge Sources + GraphRAG-style construction. The handoffs are clean.
- **It uses each taxonomy for what it is good at.** Product spine from A; internal model from B; governance overlay from C; the architectural guardrail from D. No taxonomy is forced to do a job it cannot.

### 4.3 What this decomposition deliberately does *not* do

- It does not adopt Atlan's "fifth type" (organizational context memory) as a memory type. The org-knowledge concern is real, but it belongs in Subsystem 3 as a *knowledge* concern, not as a memory type — the Atlan claim is uncorroborated vendor opinion ([01](01-landscape-and-definitions.md) §4.5). The grain of truth — that the AI Asset Registry itself is a governed organizational store — is captured in Section 6.
- It does not ship "4 types" as four Outcomes. The CoALA types are the *internal* model of Subsystem 1, not its decomposition.
- It does not pre-decide the six-tier scope model. Governance & Scope is a cross-cutting dimension; the *number* of tiers is an open design question ([03](03-memoryhub-deep-dive.md) Q-MH-2; Section 7 Q-T3).

---

## 5. Verdict on Peter's Three Areas

**Direct verdict: the 3-area framing is mostly sound as a starting point but needs one demotion and one re-typing. It does not hold as-is.**

| Area | Verdict | Action |
|---|---|---|
| **1 — Agent Knowledge** | **REFINE (re-type).** The area is real and worth keeping as a distinct subsystem. But its *type* must be pinned down: it is enterprise-RAG / knowledge-graph-shaped, **not** semantic memory and **not** a fifth memory type. As written, the seed doc's "graph knowledge layer" wording is right; the risk is that it gets implemented as semantic memory inside the memory substrate. It must be re-typed explicitly. | Keep as Subsystem 3; re-type as governed/federated enterprise-knowledge layer; extend the Knowledge Sources asset type. Resolves Tension B. |
| **2 — Agentic Memory** | **REFINE (reframe).** The area survives and is the core. But "short-term conversational memory and long-term context persistence" frames it as *two things bolted together*. The stronger framing — backed by Oracle, MemoryHub, and the academic taxonomy — is **one governed substrate exposing four access patterns** (working/episodic/semantic/procedural). Same scope, better architecture. | Keep as Subsystem 1; reframe as one-substrate / four-access-patterns. Also: surface procedural memory explicitly because it overlaps the skills registry. |
| **3 — Context Engineering** | **RESTRUCTURE (re-couple).** This is the one area that does **not** hold as an independent peer. The wave-1 evidence is consistent: the industry treats context engineering as a sub-discipline of memory management ([01](01-landscape-and-definitions.md) §1.3), and OGX implements compaction inside the memory/Responses layer, not as a separate service ([06](06-ogx-memory-primitives.md) §3.3). Keeping it as a fully independent peer area would risk two teams building the same compaction primitive. | Keep as Subsystem 2 (a named, measurable subsystem) but characterize it as a capability layer tightly coupled to / operating over the Memory Substrate, not an independent peer. It keeps its own quality metric; it does not keep its own Outcome. Resolves Tension A. |

**Net:** Peter's instinct to separate org-knowledge from learned-agent-state (areas 1 vs. 2) is correct and is *vindicated* by the Memory-vs-RAG divide — they are genuinely different data architectures. His instinct to call out context engineering as important is also correct — but it is a capability tightly coupled to the Memory Substrate, not an independent peer. The decomposition goes from **3 peer areas** to **3 subsystems — Agent Memory Substrate, Context Engineering, and Agent Knowledge** — plus **2 cross-cutting dimensions (Governance & Scope, Deployment model)**. Context Engineering is retained as the third named subsystem for counting purposes, but it is a capability layer tightly coupled to / operating over the Memory Substrate rather than a fully independent peer. The AI Asset Registry is the cross-cutting governance framework these subsystems are governed by — it is **not** itself a subsystem.

---

## 6. Mapping onto RHAISTRAT-1345 and the AI Asset Registry

### 6.1 RHAISTRAT-1345 scope coverage

RHAISTRAT-1345's scope is: short-term conversation state, long-term knowledge persistence, context compaction, cross-framework memory abstractions ([seed doc](/features/agent-memory/research/agent-memory-landscape-research.md) §2).

| Recommended subsystem | In RHAISTRAT-1345 scope today? |
|---|---|
| **Subsystem 1 — Agent Memory Substrate** (incl. context engineering capability) | **Yes, fully.** Conversation state, long-term persistence, compaction, cross-framework abstractions all map here. RHAISTRAT-1345 *is* the Outcome for Subsystem 1. |
| **Subsystem 3 — Agent Knowledge** | **No — not clearly in scope.** RHAISTRAT-1345 maps cleanly onto Peter's areas 2 and 3 but not area 1 ([seed doc](/features/agent-memory/research/agent-memory-landscape-research.md) §2 note; [01](01-landscape-and-definitions.md) §5.1). |
| **Cross-cutting governance & deployment** | Partially — acceptance criteria imply cross-framework and platform-managed primitives but do not name scope/audit/erasure explicitly. |

**Recommendation (PROPOSED):** RHAISTRAT-1345 should be scoped as the Outcome for **Subsystem 1 only** (the Agent Memory Substrate, with context engineering as an in-scope capability). **Agent Knowledge (Subsystem 3) should be a separate Outcome**, because forcing an enterprise-RAG/knowledge-graph subsystem into a memory-primitives Outcome would repeat the exact conflation [01](01-landscape-and-definitions.md) §5.2 warns against ("conflating them in a single platform feature will produce an architecture that serves neither well"). This answers open question Q42.

### 6.2 Mapping onto AI Asset Registry asset types

The AI Asset Registry already defines asset types including MCP Servers, Agents, Models, Prompts, Skills, Guardrails, and **Knowledge Sources** (`docs/knowledge-registry.md` §2; project `CLAUDE.md`). The recommended decomposition maps onto them as follows:

- **Subsystem 3 (Agent Knowledge) extends the Knowledge Sources asset type.** Knowledge Sources is described as "governed info sources for RAG, agents, retrieval workflows" — exactly Subsystem 3's shape. Agent Knowledge should be built as the governed, federated realization of Knowledge Sources, not as a new parallel concept. This answers Q44's "how does it relate to the Knowledge Sources asset type."
- **Procedural memory overlaps the Skills asset type.** Procedural memory (behavioral rules, skills, workflow templates) is partly addressed by the MLflow skills registry (versioned skill artifacts) and partly by the memory substrate (dynamically learned behavioral rules) ([01](01-landscape-and-definitions.md) §4.4, §5.4; [06](06-ogx-memory-primitives.md) Q11). The decomposition must define a clean handoff: **skills-as-registry-artifacts** (versioned, governed, in the Skills asset type) vs. **procedural-memory-in-the-substrate** (dynamic, agent-learned). This is a hard cross-domain boundary, not a detail.
- **A memory record is itself a governed AI asset.** [04](04-technical-patterns.md) §7.2 notes the memory provenance model (identity, version, owner, source, lineage, relationships) directly parallels the AI Asset Registry metadata model. This is the defensible grain of truth in Atlan's "fifth type": the AI Asset Registry is the governed organizational store; the memory substrate and Knowledge Sources are governed asset types within the same governance framework. This is how "Registry = Governance" extends to memory — not by making memory a registry, but by governing it with the same model.
- **The OGX Prompts API vs. the Prompts asset type** is a known reconciliation point ([06](06-ogx-memory-primitives.md) Q11) — versioned procedural memory exists in two places and the boundary must be drawn.

---

## 7. Open Questions for the Review Gate

These are forwarded to the review gate (Task 11) and to [08 RHOAI & OCP Alignment](08-rhoai-ocp-alignment.md). They are the decisions this decomposition *raises* and cannot itself settle.

**Q-T1 (REVIEW GATE — blocks Feature scoping).** Accept the recommended decomposition — 3 subsystems (Agent Memory Substrate, Context Engineering, Agent Knowledge) + 2 cross-cutting dimensions (Governance & Scope, Deployment model), with Context Engineering as a capability tightly coupled to the Memory Substrate and the AI Asset Registry as the cross-cutting governance framework rather than a subsystem? Or retain Peter's 3 peer areas? This is the decomposition decision; everything downstream depends on it. (Resolves Q40.)

**Q-T2 (REVIEW GATE).** Should RHAISTRAT-1345 be scoped to Subsystem 1 only, with Agent Knowledge spun out as a separate Outcome — as Section 6.1 recommends? Or should the Outcome be expanded to cover all three subsystems? (Resolves Q42.)

**Q-T3.** How many scope tiers should the productized Governance & Scope dimension have? MemoryHub's six (user/project/campaign/role/organizational/enterprise) is flagged as possibly over-complex ([03](03-memoryhub-deep-dive.md) Q-MH-2). Is `campaign` a necessary tier or replaceable by project-level group tagging?

**Q-T4.** Where exactly is the boundary between **procedural-memory-in-the-substrate** and **skills-as-registry-artifacts**? Both the skills registry and the memory substrate (and OGX's Prompts API) can hold behavioral rules. A clean handoff must be specified before either team builds ([01](01-landscape-and-definitions.md) §5.4; [06](06-ogx-memory-primitives.md) Q11).

**Q-T5.** Confirm the substrate verdict: one substrate for the four memory types, a separate subsystem for org knowledge (Section 3.3). Does RHOAI's actual workload profile (memory volume per user, org-knowledge entity count) support the ~50M-vector pgvector threshold that underpins the "one substrate for memory" half of this verdict ([04](04-technical-patterns.md) §2.1, §2.2)? (Relates to Q41, Q44.)

**Q-T6.** Is Agent Knowledge (Subsystem 3) the governed realization of the existing **Knowledge Sources** asset type, or a new asset type? Section 6.2 recommends extending Knowledge Sources; this needs an explicit decision with the AI Asset Registry owners.

**Q-T7.** Does the recommended decomposition need an explicit "Identity memory" element (PAM's fifth type — persistent persona attributes), or is that adequately covered as a slice of semantic memory within Subsystem 1 ([05](05-standards-and-protocols.md) §3.4)?

---

## 8. Sources

### Internal (Repository)

| Source | Type | Path / Reference |
|---|---|---|
| Agent Memory & Knowledge seed doc | Internal seed document | `docs/knowledge-review/assets/agent-memory-knowledge.md` |
| Knowledge Registry (asset types §2; open questions Q40–Q44 §13) | Internal reference | `docs/knowledge-registry.md` |
| 01 Landscape & Definitions | Sibling research doc | `agent-memory/research/01-landscape-and-definitions.md` |
| 02 Solution Survey | Sibling research doc | `agent-memory/research/02-solution-survey.md` |
| 03 MemoryHub Deep-Dive | Sibling research doc | `agent-memory/research/03-memoryhub-deep-dive.md` |
| 04 Technical Patterns | Sibling research doc | `agent-memory/research/04-technical-patterns.md` |
| 05 Standards & Protocols | Sibling research doc | `agent-memory/research/05-standards-and-protocols.md` |
| 06 OGX Memory Primitives | Sibling research doc | `agent-memory/research/06-ogx-memory-primitives.md` |
| Agent Registry Research Executive Summary | Analytical-rigor calibration reference | `agents/agent-registry/research/00-executive-summary.md` |
| Project guidance — Registry = Governance principle, asset types | Internal reference | `CLAUDE.md` |
| RHAISTRAT-1345 | Jira Outcome | https://redhat.atlassian.net/browse/RHAISTRAT-1345 |

### External — cited via sibling docs (not independently re-fetched for this synthesis)

| Source | Cited for | Via |
|---|---|---|
| CoALA: Cognitive Architectures for Language Agents (arXiv:2309.02427) | Four-type memory taxonomy | [01](01-landscape-and-definitions.md) §4 |
| Oracle AI Agent Memory (Richmond Alake, 2026-05-01) | "Four access patterns over one substrate" argument; LongMemEval 93.8% | [01](01-landscape-and-definitions.md) §4, [02](02-solution-survey.md) §3.1, [seed doc](/features/agent-memory/research/agent-memory-landscape-research.md) §4 |
| When Agent Memory Becomes a Platform Concern (Wes Jackson, 2026-05-01) | Memory ≠ RAG; database-not-search; platform-tier framing | [01](01-landscape-and-definitions.md) §2, [seed doc](/features/agent-memory/research/agent-memory-landscape-research.md) §6 |
| arXiv:2602.02007 (2026) | RAG vs. memory data-shape distinction | [01](01-landscape-and-definitions.md) §2 |
| Atlan — types of AI agent memory; "organisational context memory" fifth type | Fifth-type proposal (flagged as vendor opinion) | [01](01-landscape-and-definitions.md) §4.5 |
| Portable Agent Memory / PAM (arXiv:2605.11032, May 2026) | Five-type model adding "Identity memory" | [05](05-standards-and-protocols.md) §3.4 |
| Mem0 — State of AI Agent Memory 2026; The New Stack; Weaviate | Context engineering as sub-discipline of memory management | [01](01-landscape-and-definitions.md) §1.3 |
| Microsoft GraphRAG / LazyGraphRAG | Org-knowledge / area-1 as enterprise-RAG-shaped | [02](02-solution-survey.md) §4.4, [04](04-technical-patterns.md) §6 |
| MemoryHub (redhat-ai-americas/memory-hub) | Six-tier scope model; single pgvector substrate; governance | [03](03-memoryhub-deep-dive.md) §2–3 |
| OGX (ogx-ai/ogx) | Memory primitives; compaction inside Responses API | [06](06-ogx-memory-primitives.md) §3, §5–6 |

### Notes

This is a synthesis document. It introduces no new external research; every substantive claim traces to a wave-1 sibling document (01–06) or the internal seed/registry documents, which carry their own primary-source attribution and access notes. Where wave-1 docs flagged a source as vendor-claimed, uncorroborated, or behind an HTTP error, those caveats are preserved here (notably: Oracle blog 403, Atlan "fifth type" as marketing-blog opinion, MemoryHub cache-optimization figures not independently benchmarked).
