---
title: Agent Memory & Knowledge — Review Gate Notes
description: Decisions and direction from the Phase 1 research review gate (D1-D6) -- the contract the Phase 2 strategy is built on.
source: ai-asset-registry/agent-memory/research/REVIEW-NOTES.md (as of 2026-07-05)
timestamp: 2026-07-06
review_after: 2026-08-05
---

# Agent Memory & Knowledge — Review Gate Notes

**Date:** 2026-05-18
**Participants:** Peter Double (Principal PM — MCP & AI Asset Registries)
**Purpose:** Record the decisions and direction from the Phase 1 research review gate. This file is the contract the Phase 2 strategy is built on. It supersedes the PROPOSED markers in docs 07, 08, and 00 for the items decided below.

---

## Status

Phase 1 research (docs 00–08) reviewed and **accepted**. No factual corrections to the research documents were requested at the gate — the research stands as written; the decisions below select among the options the research laid out as PROPOSED. Phase 2 (strategy) is cleared to begin.

---

## Decisions

### D1 — Decomposition: ACCEPTED as proposed
Adopt the doc-07 model: **3 subsystems** — (1) Agent Memory Substrate, (2) Context Engineering, (3) Agent Knowledge — **+ 2 cross-cutting dimensions** — Governance & Scope, Deployment model. Context Engineering is a capability layer over the substrate, not a peer area. The AI Asset Registry is the cross-cutting governance framework, not a memory subsystem. Peter's original 3 peer areas are restructured accordingly (Agent Knowledge re-typed, Agentic Memory reframed, Context Engineering re-coupled).

### D2 — RHAISTRAT-1345 scope: Memory Substrate only; Agent Knowledge spun out
RHAISTRAT-1345 ("Agent Memory Primitives") is scoped to **Subsystem 1 (Agent Memory Substrate) + Context Engineering as an in-scope capability**. **Agent Knowledge (Subsystem 3) is explicitly OUT of scope for this run** — it is enterprise-RAG / knowledge-graph-shaped, a different architecture with a different team/timeline. It becomes a **separate Outcome, attacked in a different run.** This strategy effort does not produce Agent Knowledge strategy beyond a brief pointer noting the deferral.

### D3 — Sourcing: phased combination ACCEPTED, with an explicit MVP→full path required
Accept the phased combination — OGX as memory substrate, MemoryHub-derived layer for governance, build-fresh reserved for Agent Knowledge (deferred), upstream contribution as standards posture, partner products only as pluggable backends. **Requirement from Peter:** the strategy must show a clear, step-by-step path from MVP to full solution — "making sure there is a path to get there."

### D4 — Substrate verdict: CONFIRMED
One governed substrate for the four memory types (working/episodic/semantic/procedural); a separate subsystem for org-wide Agent Knowledge. Memory (append-heavy datastore) and knowledge (enterprise RAG / knowledge graph) are different data architectures. The empirical workload-profile measurement (Q-G4) is commissioned as a design-time task, not a blocker.

### D5 — MVP anchor: OGX-primitives-first, then governance
The MVP leads with **(C+D) exposing OGX's existing memory primitives as governed, first-class RHOAI features**; the MemoryHub-derived governance layer (Track B) follows. Rationale (Peter): RHOAI **3.5 ships August 2026** — the goal is to "sneak some memory in" by building on the OGX Responses bridge already GA'ing there. **3.6 ships November 2026** — the window to push a larger solution. Releases are every ~3 months; the org has competing priorities. The strategy must therefore be a **step-by-step, incrementally absorbable roadmap**, delivering the best customer solution as fast as the org can absorb it.

### D6 — Standards work: parallel from the start
Open-standards work (MCP Memory Convention proposal, AAIF memory project, A2A memory binding — per doc 05 §6.2) runs **in parallel with product work from day one** — build toward open standards from the start, using Red Hat's OGX contributor channel and AAIF Gold membership.

---

## Deferred to the strategy phase (Peter: "let the strategy recommend")

These were not decided at the gate; the strategy phase should analyze and recommend, with rationale:

- **Audit trail sequencing (Q-G7)** — whether a complete append-only audit trail gates a 3.6 Dev Preview or is a GA gate only. Hard constraint context: EU AI Act enforcement August 2026; neither OGX nor MemoryHub ships a working audit trail today.
- **Scope-tier model (Q-T3 / Q-MH-2)** — whether to carry MemoryHub's full six-tier scope model or simplify to OpenShift-native tiers (user/project/org) for the MVP. Three of MemoryHub's tiers (campaign/organizational/enterprise) have no native OpenShift analogue.

---

## Open items carried into the strategy (not Peter-decisions — factual unknowns / cross-team)

- **Q-G2 / doc-06 Q1–Q3** — exact OGX API surface exposed in RHOAI 3.5, whether the 3.5 deployment includes the May-2026 multi-tenancy work, and the OGX/Llama-Stack gateway-native replacement plan. To be confirmed with the OGX/AI-Gateway team; the strategy should flag where its roadmap depends on the answer.
- **Q-G4** — RHOAI memory workload profile (volume/concurrency/entity counts). Commissioned as a design-time measurement task.
- **Q-G3 / Q-G5 / Q-G6** — memory-as-registry-asset boundary, actor-chain RBAC for shared memory, and platform identity vs. MemoryHub's standalone OAuth. Cross-team decisions with AI Asset Registry / AI Gateway owners; the strategy should name them as required follow-ups.
- **Q-T4** — procedural memory vs. skills registry vs. OGX Prompts boundary. Cross-team design question; the strategy should carry the proposed three-layer model as a position to socialize.
- **Q-MH-1** — MemoryHub IP/copyright transfer (currently held by an individual). Administrative prerequisite for any productization of MemoryHub-derived code.

---

## Implications for Phase 2 (strategy/)

1. Strategy scope = **Agent Memory Substrate + Context Engineering + the Governance & Scope and Deployment cross-cutting dimensions.** Agent Knowledge gets only a short "deferred to a separate Outcome/run" pointer.
2. The centerpiece is an **incremental roadmap**: 3.5 (Aug 2026, OGX-primitives "sneak-in"), 3.6 (Nov 2026, larger governed solution / Dev Preview), 3.7+ (GA), each release ~3 months apart and sized to what the org can absorb.
3. The proposed RHAISTRAT-1345 Outcome rewrite reflects D1–D5 — substrate + context-engineering scope, restructured framing.
4. The RFE roadmap outline is sequenced to the incremental release plan.
5. Standards work appears as a parallel workstream in the roadmap.

---

## Phase 2 Research Commission (2026-06-09)

**Trigger:** First Agent Memory Team Sync meeting (2026-06-09).

**Approach:** Breadth-first — research plans created for all gaps simultaneously, with plans re-evaluated as findings emerge. Hybrid document strategy: new topics get new docs numbered 09+; updates to existing topics go as new sections within existing docs.

**Gaps addressed (13 total):**

1. Agent harness memory mechanisms (OpenClaw, Hermes, Claude Code, Codex CLI, Gemini CLI)
2. Claude memory & dreaming architecture
3. Adversarial memory & context integrity (OWASP ASI06, context rot, injection)
4. Benchmarking landscape (LongMemEval, BEAM, LoCoMo, MemoryArena)
5. Benchmark-to-production gap analysis
6. Multi-modal memory (12–24 month horizon)
7. Kagenti integration (AgentRuntime/AgentCard CRDs, SPIFFE identity)
8. OpenViking/ByteDance evaluation (AGPL-3.0 license — hard productization blocker)
9. Multi-agent memory design patterns (shared pools, blackboard, message-passing, hierarchical)
10. KV-cache optimization as Red Hat differentiator (vLLM, llm-d, 57× TTFT)
11. Enterprise use cases beyond coding (healthcare, finance, ITOps, defense)
12. MemoryHub adoption decision assessment (fork vs. extract vs. hybrid)
13. Storage backend trade-offs (PostgreSQL+pgvector, Redis, vector DB certification gap)

**Documents produced:**

| Type | Doc | Title |
|---|---|---|
| New | 09 | Agent Harness Memory Mechanisms |
| New | 10 | Claude Memory & Dreaming Deep Dive |
| New | 11 | Adversarial Memory & Context Integrity |
| New | 12 | Benchmarking & Evaluation Framework Design |
| New | 13 | KV-Cache Memory Optimization |
| New | 14 | Enterprise Use Case Patterns Beyond Coding |
| New | 15 | Multi-Modal Memory |
| Update | 02 | Solution Survey — §2.7 OpenViking/ByteDance |
| Update | 03 | MemoryHub Deep Dive — §7 Adoption Decision Assessment |
| Update | 04 | Technical Patterns — §9 expanded (multi-agent patterns) |
| Update | 08 | RHOAI & OCP Alignment — §7 Kagenti, §8 Storage Backends |

**Design spec:** [Phase 2 Research Design Spec](https://github.com/solaius/ai-asset-registry/blob/main/docs/superpowers/specs/2026-06-09-agent-memory-phase2-research-design.md)

**Key findings (added to doc 00 §9 as findings 15–24):** Cross-harness memory patterns converging on 7 architectural archetypes; memory-as-MCP emerging as the portable interface; dream consolidation viable as an OpenShift CRD; OWASP ASI06 establishing the security framework; benchmark-to-production gap (~91% → ~49% at scale); KV-cache optimization as a Red Hat differentiator; enterprise verticals converging on 4 common primitives; no dedicated vector DB has Red Hat OpenShift Operator Certification; OpenViking AGPL-3.0 is a hard productization blocker; multi-modal memory is a 12–24 month horizon.

---

## OGX Deprecation Context (2026-06-10)

**Signal:** OGX is likely being deprecated over time, replaced by AI Gateway components. Evidence: the AI Gateway F2F (April 2026) decided to re-architect the Responses API from single-tenant Llama Stack to gateway-native multi-tenant implementation; Playground OGX decoupling is targeting 3.7 as the earliest; the AI Gateway is architecturally positioned to absorb all stateful API surfaces currently provided by OGX. This is **DIRECTIONAL** — no formal deprecation announcement has been made.

**What it means for D3/D5:** D3 named "OGX as memory substrate" and D5 named "OGX-primitives-first" as the MVP anchor. These decisions remain valid for the *primitives* they describe (Conversations, Vector Stores, Files, Prompts, Compaction, `AuthorizedSqlStore` ABAC), but the *delivery vehicle* is transitioning from OGX to the AI Gateway Responses API. The strategy should be substrate-agnostic at the API surface.

**Q-G2 status update:** Q-G2 ("exact OGX API surface and the gateway-native replacement plan") is directionally answered — the AI Gateway IS the replacement. Parity timeline aligns with 3.7.

**Research response:** [Doc 16](16-ai-gateway-memory-substrate.md) analyzes the AI Gateway Responses API as the memory substrate replacement.

**Strategy response:** Strategy docs updated to use "Responses API primitives" as the substrate-agnostic term and adopt a hybrid posture — substrate-agnostic API surface, architecturally gateway-bound.
