---
title: Agent Memory Strategy — RHOAI Agent Memory Substrate & Context Engineering
description: The Phase 2 strategy for RHAISTRAT-1345 -- an incrementally-absorbable path to a governed agent memory substrate and context-engineering capability.
source: ai-asset-registry/agent-memory/strategy/agent-memory-strategy.md (as of 2026-07-05)
timestamp: 2026-07-06
review_after: 2026-08-05
---

# Agent Memory Strategy — RHOAI Agent Memory Substrate & Context Engineering

**Purpose:** The Phase 2 strategy for the RHAISTRAT-1345 Outcome — a recommended, incrementally-absorbable path to a governed agent memory substrate and context-engineering capability for RHOAI, built on the Phase 1 research and the review-gate decisions.

**Date:** 2026-06-09 (revised from 2026-05-18)

**Author:** Peter Double (Principal PM — MCP & AI Asset Registries)

**Status:** PROPOSED — a PM strategy proposal for leadership review. Items marked DECIDED were settled at the Phase 1 review gate (see [REVIEW-NOTES](/features/agent-memory/research/REVIEW-NOTES.md)); everything else is a recommendation for leadership to confirm. RHOAI 3.6 = November 2026 is given; RHOAI 3.7 (~Q1-Q2 2027) is the base-solution target; anything past 3.7 is directional and marked as such. Updated 2026-06-09 to reflect the timeline shift (Peter Double + Sanjeev Rampal) and Phase 2 research integration.

**Strategy series — Agent Memory (Phase 2):**
- 00 [README](strategy-overview.md) — index and derivation note
- 01 Agent Memory Strategy (this document)
- 02 [Use Cases & Personas](use-cases-and-personas.md)
- 03 [Recommended Architecture](recommended-architecture.md)
- 04 [RHAISTRAT-1345 Outcome Update](rhaistrat-1345-outcome-update.md)
- 05 [RFE Roadmap](rfe-roadmap.md)

---

## Contents

1. [Vision and the Whitespace](#1-vision-and-the-whitespace)
2. [The Accepted Decomposition (Scoped to This Run)](#2-the-accepted-decomposition-scoped-to-this-run)
3. [Strategic Approach](#3-strategic-approach)
4. [The Incremental Roadmap](#4-the-incremental-roadmap)
5. [The Parallel Standards Workstream](#5-the-parallel-standards-workstream)
6. [Recommendations on the Two Deferred Questions](#6-recommendations-on-the-two-deferred-questions)
7. [Differentiation and Competitive Positioning](#7-differentiation-and-competitive-positioning)
8. [Risks and Dependencies](#8-risks-and-dependencies)
9. [Basis and Sources](#9-basis-and-sources)

---

## 1. Vision and the Whitespace

**Vision (PROPOSED).** RHOAI should provide agent memory as a *governed platform primitive* — a self-hosted, Kubernetes-native, air-gappable substrate that agents of any framework can write to and read from, governed by the same model the AI Asset Registry applies to every other AI asset type. The goal is not to ship a memory feature; it is to make memory a platform tier — the way OpenShift made container orchestration a platform tier — so that every agent team stops reinventing conversation state, long-term persistence, and context compaction ([seed doc](/features/agent-memory/research/agent-memory-landscape-research.md) §2; [research 00](/features/agent-memory/research/00-executive-summary.md) §3 finding 1).

**The whitespace is real and specific.** The research is unambiguous on this: no existing solution combines *enterprise governance + Kubernetes-native self-hosted + air-gappable + an open standard interface* ([research 00](/features/agent-memory/research/00-executive-summary.md) §1, §6; [research 02] §8 Gap 1, via [research 08](/features/agent-memory/research/08-rhoai-ocp-alignment.md) §4.5). The market divides into three camps and none occupies RHOAI's target position:

- **Hyperscaler managed memory** (AWS AgentCore, Google Memory Bank, OpenAI server-side) — GA and validated, but cloud-only, no air-gap path.
- **Enterprise database-native** (Oracle AI Agent Memory) — the highest external governance maturity, but hard Oracle Database lock-in, not portable to OpenShift.
- **OSS memory startups / frameworks** (Mem0, Letta, Zep/Graphiti, Cognee) — deployment-flexible, but governance is thin or absent, and the field is consolidating (~$60M+ of venture funding into pure-play memory startups in 18 months, per analyst estimates — adopting one risks picking a non-survivor).

**Red Hat's structural advantage.** Two unusually strong internal assets already exist ([research 00](/features/agent-memory/research/00-executive-summary.md) §1):

- **Production-ready memory primitives** — working/episodic/semantic/procedural memory primitives plus compaction are already shipping internally ([research 06](/features/agent-memory/research/06-ogx-memory-primitives.md); [research 16](/features/agent-memory/research/16-ai-gateway-memory-substrate.md)). The primitives themselves — Conversations, Vector Stores, Files, Prompts, Compaction — are architecturally preserved across delivery vehicles; the memory strategy builds on these primitives starting in Phase 1 (RHOAI 3.7), with a substrate-agnostic API surface that works regardless of delivery vehicle.
- **An OpenShift-native governance prototype** — the most mature scope/RBAC/curation governance model of any candidate the research surveyed ([research 03] deep-dive; [research 08](/features/agent-memory/research/08-rhoai-ocp-alignment.md) §4.2).

The two are **complementary, not competing**: the memory primitives are the substrate, the governance prototype provides the enterprise governance layer (per REVIEW-NOTES D5; [research 08](/features/agent-memory/research/08-rhoai-ocp-alignment.md) §4.7). The strategy below converts that pairing into a release-paced plan.

**The strategic risk is timing, not capability.** The hyperscalers and Oracle ship today. A proprietary RHOAI memory API built before standards converge would inherit a migration cost. This is why the standards workstream (§5) runs in parallel from day one, and why the roadmap (§4) leads with the lowest-cost, fastest-to-customer step.

---

## 2. The Accepted Decomposition (Scoped to This Run)

**DECIDED (REVIEW-NOTES D1).** The Phase 1 decomposition is accepted: **3 subsystems + 2 cross-cutting dimensions** ([research 07](/features/agent-memory/research/07-taxonomy-and-decomposition.md) §4).

| Element | What it is | In scope this run? |
|---|---|---|
| **Subsystem 1 — Agent Memory Substrate** | One governed store exposing the four CoALA access patterns (working / episodic / semantic / procedural). Append-heavy, agent-written. | **Yes** |
| **Subsystem 2 — Context Engineering** | A capability layer *over* the substrate — compaction, retrieval assembly, progressive disclosure, KV-cache-aware ordering. Named and measurable, not an independent peer. | **Yes** (as an in-scope capability) |
| **Subsystem 3 — Agent Knowledge** | A distinct, adjacent governed/federated enterprise-knowledge layer — enterprise-RAG / knowledge-graph-shaped, **not** semantic memory. | **No — deferred** (see below) |
| **Cross-cutting 1 — Governance & Scope** | Scope tiers, RBAC, audit, erasure, contradiction detection, provenance, compliance. Where "Registry = Governance" lands. | **Yes** |
| **Cross-cutting 2 — Deployment model** | Client-side vs. server-side. Server-side default; client-side hybrid path for IDE/dev-workflow agents. | **Yes** |

**Scope of this strategy (DECIDED — REVIEW-NOTES D2).** RHAISTRAT-1345 is scoped to **Subsystem 1 (Agent Memory Substrate) + Context Engineering as an in-scope capability**, with the Governance & Scope and Deployment cross-cutting dimensions applied throughout. The substrate verdict is confirmed (REVIEW-NOTES D4): one governed substrate for the four memory types; a separate subsystem for org-wide knowledge.

### 2.1 Agent Knowledge — deferred (pointer only)

**Agent Knowledge (Subsystem 3) is explicitly OUT of scope for this run** (REVIEW-NOTES D2). It is enterprise-RAG / knowledge-graph-shaped — a different data architecture, with a different team and timeline — and becomes a **separate Outcome attacked in a separate run**. This strategy does not produce Agent Knowledge strategy. The research position to carry forward when that run begins: Agent Knowledge should be built as the governed, federated realization of the existing AI Asset Registry **Knowledge Sources** asset type, not as a new asset type ([research 08](/features/agent-memory/research/08-rhoai-ocp-alignment.md) §2.1, §5 Q-T6) — and `build-fresh` is the reserved sourcing option for it, since no internal candidate has a real org-knowledge-graph implementation ([research 08](/features/agent-memory/research/08-rhoai-ocp-alignment.md) §4.7). That is the extent of the Agent Knowledge treatment here.

---

## 3. Strategic Approach

**DECIDED (REVIEW-NOTES D3, D5).** The sourcing approach is a **phased combination**, not a single-vendor or single-build bet ([research 08](/features/agent-memory/research/08-rhoai-ocp-alignment.md) §4.7):

- **Existing internal memory primitives are the substrate.** Working/episodic/semantic/procedural primitives and compaction already ship internally ([research 06](/features/agent-memory/research/06-ogx-memory-primitives.md); [research 16](/features/agent-memory/research/16-ai-gateway-memory-substrate.md)). The memory API surface is designed to be substrate-agnostic — it works regardless of the underlying delivery vehicle. Adopting these primitives is the lowest-friction technical path.
- **The internal governance prototype provides the governance layer.** Scope tiers (four OpenShift-native tiers for the MVP — see §6.2), inline curation, contradiction detection, provenance — exactly the enterprise-governance dimension the memory primitives lack on their own ([research 08](/features/agent-memory/research/08-rhoai-ocp-alignment.md) §2.3, §4.2). The primitives and the governance prototype are complementary.
- **Build-fresh is reserved for Agent Knowledge** (deferred — §2.1).
- **Partner products (Mem0, etc.) only as pluggable-backend compatibility**, never as the primary substrate ([research 08](/features/agent-memory/research/08-rhoai-ocp-alignment.md) §4.5).
- **Upstream contribution is the standards posture** layered across all of it (§5; REVIEW-NOTES D6).

**The MVP anchor (DECIDED — REVIEW-NOTES D5): memory primitives first, then governance.** The MVP leads by exposing the *existing* internal memory primitives as governed, first-class RHOAI features, with the enterprise governance layer as a concurrent track. The memory API surface is substrate-agnostic — it works regardless of delivery vehicle ([REVIEW-NOTES — Platform Transition Context](/features/agent-memory/research/REVIEW-NOTES.md#ogx-deprecation-context-2026-06-10)). Phase 0 (RHOAI 3.6) establishes Red Hat's upstream position through standards and specification work; Phase 1 (RHOAI 3.7) delivers the governed substrate and governance layer together as a Dev Preview. The rationale is delivery economics: the 3.5 and 3.6 release windows carry heavy competing priorities, and the substrate work — though mostly *governance-wrapping* of code that already ships — needs the upstream foundation that Phase 0 standards work provides.

**The path from MVP to full solution (the D3 requirement).** Each release builds directly on the last with no thrown-away work:

```
 3.6 (Nov 2026)         3.7 (~Q1-Q2 2027)         3.8+ (GA — directional)
 Standards &       →    Governed substrate    →   Productized substrate
 upstream                (Dev Preview) +           at GA: audit/operator/
 foundation:             enterprise governance     observability/FIPS/
 MCP Memory Conv,        layer (Dev Preview) +     adversarial defense/
 MLflow memory,          context engineering       benchmarking gaps
 A2A AgentCard                                     closed; gateway-native
                                                   re-home complete
        │                      │                          │
        └── standards workstream is Phase 0 deliverable ──┘
```

The 3.6 step establishes Red Hat's upstream position and de-risks the 3.7 build. The 3.7 step delivers the governed substrate, governance layer, and context-engineering capability as a Dev Preview. The 3.8+ step hardens what 3.7 previewed, closes the GA gaps (audit trail, operator, FIPS, adversarial defense, benchmarking), and absorbs the substrate into the gateway-native Responses replacement. Nothing in 3.6 is discarded at 3.7; nothing in 3.7 is discarded at 3.8. That is the "path to get there" the review gate required.

---

## 4. The Incremental Roadmap

**This section is the centerpiece of the strategy (per REVIEW-NOTES D3/D5).** It is release-paced and sized to what the org can absorb. RHOAI ships roughly every ~3 months; 3.6 = November 2026 is given; 3.7 (~Q1-Q2 2027) is the base-solution target; 3.8+ is directional. The timeline was set by Peter Double + Sanjeev Rampal (2026-06-09): the base solution targets RHOAI 3.7 as a Dev Preview; 3.6 delivers standards and upstream foundation work only, given the heavy 3.5/3.6 workload. No memory deliverable is targeted for RHOAI 3.5.

Status legend: **DECIDED** = settled at the review gate; **PROPOSED** = this strategy's recommendation for leadership; **DIRECTIONAL** = beyond 3.7, indicative only.

### Phase 0 — RHOAI 3.6 (November 2026): Standards & upstream foundation

**Theme:** Establish Red Hat's upstream position and de-risk the 3.7 build. No product feature delivery — the 3.5 and 3.6 release windows are committed to other priorities. Phase 0 is a standards and specification sprint.

| | |
|---|---|
| **Deliverable** | Standards and upstream contributions: (1) MCP Memory Convention SEP — a Standards Enhancement Proposal formalizing the de facto memory-tool naming convention into a reference convention (canonical tool set, minimal record format, scope model); (2) upstream MLflow collaboration on memory abstractions; (3) A2A AgentCard memory binding — an optional extension declaring an agent's memory services. Architecture validated against upstream consensus. |
| **Sizing** | Contributor effort — specification drafting, upstream engagement, architecture validation. Absorbable alongside a committed release. |
| **Status** | PROPOSED |
| **Why standards first** | The 3.5 and 3.6 workload is already heavy. Rather than delivering a half-built substrate, Phase 0 invests in the upstream consensus that makes the 3.7 substrate standards-aligned from day one. This avoids the proprietary-API lock-in risk (§8) by establishing the standard before shipping the product. |

### Phase 1 — RHOAI 3.7 (~Q1-Q2 2027): The governed substrate, Dev Preview

**Theme:** Push the governed solution. Two parallel workstreams ([research 08](/features/agent-memory/research/08-rhoai-ocp-alignment.md) §4.7).

**Substrate workstream — Governed memory substrate (Dev Preview).** Expose the existing memory primitives as governed, first-class RHOAI memory features: a stable memory API agents call without custom plumbing, framework-agnostic, with scope-aware RBAC consuming platform identity. This is the Subsystem-1 MVP — the substrate, governed.

**Governance workstream — Enterprise governance layer (Dev Preview).** Stand up the Governance & Scope service alongside the memory substrate: scope tiers (simplified — see §6.2), inline curation, contradiction detection, provenance. This is the cross-cutting Governance & Scope dimension made concrete.

| | |
|---|---|
| **Deliverable** | A **Dev Preview** of a governed agent memory substrate: framework-agnostic memory API (substrate workstream) + governance layer with scope tiers, curation, contradiction detection, provenance (governance workstream) + a context-engineering capability (inspectable compaction, retrieval assembly, KV-cache-aware ordering — now backed by Phase 2 research [doc 13](/features/agent-memory/research/13-kv-cache-optimization.md)). Memory exposed via MCP through the MCP Gateway for per-tool authz and audit. Memory service registered as a governed asset in the AI Asset Registry. |
| **Sizing** | The single largest phase. The substrate workstream is mostly governance-wrapping of existing internal memory primitives; the governance workstream is productization of the internal governance prototype. Both are Dev Preview — explicitly *not* GA — which is what makes the 3.7 window realistic. The Phase 0 standards work de-risks the API surface design. |
| **Status** | PROPOSED |
| **Gating dependencies** | Q-G7 (audit trail — see §6.1 recommendation), Q-MH-1 (governance prototype IP/copyright transfer — administrative prerequisite for the governance workstream), Q-G2 (directionally answered — AI Gateway is the replacement), Q-G6 (platform identity vs. the governance prototype's standalone OAuth), Q-G3/Q-G5 (memory-as-registry-asset boundary, actor-chain RBAC). See §8. |

**Why Dev Preview, not GA:** GA carries hard compliance and operability bars — audit trail, OLM operator, observability, FIPS validation, adversarial memory defense — that cannot be cleared in one release on top of two prototypes ([research 08](/features/agent-memory/research/08-rhoai-ocp-alignment.md) §4.2). Dev Preview lets 3.7 deliver a real, customer-testable governed substrate while those gaps are closed for 3.8+.

### Phase 2 — RHOAI 3.8+ (directional): Productization to GA, then continued features

**Theme:** Harden the 3.7 Dev Preview to GA, then continue adding features. **DIRECTIONAL — beyond 3.7; indicative, not a commitment.** RHOAI 3.8+ release contents are not established by the research; this phase is named to show the path, not to commit dates.

| | |
|---|---|
| **Deliverable (directional)** | GA of the governed memory substrate: append-only audit trail wired through (the highest-severity gap — [research 08](/features/agent-memory/research/08-rhoai-ocp-alignment.md) §3.2 D-6); OLM-integrated Kubernetes operator (replacing the current skeleton operator); Prometheus/Grafana observability; end-to-end FIPS validation; **adversarial memory defense** — memory writes validated against injection patterns, poisoned memories quarantined ([research 11](/features/agent-memory/research/11-adversarial-memory.md)); **memory quality benchmarking** — standardized recall/precision metrics for substrate validation ([research 12](/features/agent-memory/research/12-benchmarking-evaluation.md)). The substrate's working/episodic slice re-homes onto the gateway-native architecture. Client-side memory hybrid path for IDE/dev-workflow agents, informed by harness memory patterns ([research 09](/features/agent-memory/research/09-agent-harness-memory.md)). |
| **Sizing** | Productization-heavy — operator, audit, observability, FIPS, adversarial defense, and benchmarking are the schedule-consuming gaps ([research 08](/features/agent-memory/research/08-rhoai-ocp-alignment.md) §4.2). Likely more than one release. Features continue in subsequent releases after the GA bar is cleared. |
| **Status** | DIRECTIONAL |
| **Gating dependencies** | Q-G2 (the gateway-native transition target must exist); Q-G4 (workload-profile measurement — commissioned as a design-time task, informs whether the single pgvector substrate holds). |

### Roadmap summary

| Phase | Release | Deliverable | Maturity | Org-absorption sizing |
|---|---|---|---|---|
| 0 | 3.6 — Nov 2026 | Standards & upstream foundation (MCP Memory Conv, MLflow, A2A AgentCard) | Upstream / specs | Contributor effort — fits alongside a committed release |
| 1 | 3.7 — ~Q1-Q2 2027 | Governed memory substrate + governance layer + context engineering | **Dev Preview** | Largest phase; Dev Preview keeps it realistic |
| 2 | 3.8+ — directional | Audit / operator / observability / FIPS / adversarial defense / benchmarking; gateway-native re-home; client-side hybrid | GA + features (directional) | Productization-heavy; likely multi-release |

---

## 5. The Parallel Standards Workstream

**DECIDED (REVIEW-NOTES D6).** Open-standards work runs **in parallel with product work from day one** — building toward open standards from the start, using Red Hat's existing upstream contributor channels and AAIF Gold membership. With the timeline update (2026-06-09), **the standards workstream is the Phase 0 (3.6) deliverable** — rather than running as background effort, it is the primary memory contribution to the 3.6 release, establishing Red Hat's upstream position before the 3.7 substrate build. Upstream timelines beyond Phase 0 are not Red-Hat-controlled, so ongoing standards work remains tracked but not schedule-committed to a specific RHOAI release ([research 08](/features/agent-memory/research/08-rhoai-ocp-alignment.md) §4.4).

There is no agent-memory standard today, and that absence is an opportunity: a platform that ships memory primitives before standards converge gets to shape them ([research 05](/features/agent-memory/research/05-standards-and-protocols.md) §1, §6.3). The three actionable opportunities from the research ([research 05](/features/agent-memory/research/05-standards-and-protocols.md) §6.2):

| Opportunity | What it is | Sequencing |
|---|---|---|
| **MCP Memory Convention SEP** | A Standards Enhancement Proposal to MCP formalizing the de facto memory-tool naming convention into a reference convention — canonical tool set, minimal record format, scope model. The governance prototype's MCP tool set is a strong starting point ([research 03]). | **Phase 0 (3.6) deliverable**; the 3.7 substrate's MCP surface tracks it. |
| **A2A AgentCard memory binding** | An optional A2A AgentCard extension declaring an agent's memory services (transport, scope, access model) — makes memory bindings discoverable and governable. | **Phase 0 (3.6) deliverable**; propose alongside RFE-M5's registry integration at 3.7. |
| **AAIF memory project** | Propose an AAIF project as a neutral governance home for a memory schema, API contract, and portability spec — the MCP/AGENTS.md donation model. The governance prototype (Apache 2.0 licensed) is a credible contribution candidate. | Longer horizon; socialize from Phase 0 (3.6), formal proposal as the substrate matures post-3.7. |

**Posture:** Contribute governance primitives (audit hooks, scope attributes) upstream where they fit the community project's charter (Option D); contribute the substrate's standardizable surfaces toward AAIF. Build *against* MCP transport from the start so the substrate is standards-aligned rather than proprietary ([research 05](/features/agent-memory/research/05-standards-and-protocols.md) §6.3).

**Open cross-team item:** Q-G8 — whether standards work is run as in-program or as a parallel-but-separate workstream — is named in the research as a review-gate question; REVIEW-NOTES D6 settles it as *parallel from the start*. The named follow-up is to formally resource the standards effort and assign an owner.

---

## 6. Recommendations on the Two Deferred Questions

The review gate deferred two questions to this strategy phase, to be analyzed and recommended with rationale (REVIEW-NOTES "Deferred to the strategy phase").

### 6.1 Audit-trail sequencing — Recommendation: GA gate, with a Dev-Preview disclosure obligation

**The question (Q-G7).** Does a complete append-only audit trail gate the 3.7 Dev Preview, or is it a GA-only gate? Hard constraint: EU AI Act enforcement is August 2026; no internal candidate ships a working audit trail today — the governance prototype's is a stub, and the memory primitives have none ([research 08](/features/agent-memory/research/08-rhoai-ocp-alignment.md) §3.2 D-6, §6 Q-G7).

**Recommendation (PROPOSED): The complete append-only audit trail is a GA gate, not a 3.7 Dev-Preview gate — but the 3.7 Dev Preview must ship with an explicit non-production disclosure and a minimum write-event log.**

**Rationale:**

1. **Dev Preview is, by definition, not for production or regulated workloads.** The EU AI Act enforcement obligation attaches to *production* deployments processing real data. A Dev Preview that is clearly labeled non-production, and that customers are contractually told not to use for regulated workloads, does not trigger the August 2026 enforcement bar. Gating the Dev Preview on a complete audit trail would push the *entire* 3.7 governed-substrate deliverable out — the audit trail is one of the heaviest gaps ([research 08](/features/agent-memory/research/08-rhoai-ocp-alignment.md) §4.2) — and that would extend the timeline further.

2. **GA is where the obligation genuinely lands.** An inspectable, append-only memory audit log is a hard EU AI Act / GDPR / HIPAA requirement and is correctly identified as GA-blocking for any compliance-facing memory feature ([research 00](/features/agent-memory/research/00-executive-summary.md) §3 finding 13; [research 08](/features/agent-memory/research/08-rhoai-ocp-alignment.md) §3.2 D-6). Holding the *GA* gate firm is non-negotiable. The audit trail is therefore a named, must-close gap for Phase 2 (§4).

3. **A Dev Preview that ships zero audit capability is still the wrong call.** To de-risk the GA gate and to give 3.6 customers something testable, the 3.7 Dev Preview should ship a *minimum* write-event log (who/what/when/scope on every memory write) even though the full inspectable, immutable, read-and-write audit trail is deferred to GA. This makes the audit trail an *increment* across 3.7→3.8 rather than a single cliff, consistent with the incremental-roadmap principle (D3).

**Net:** Do not gate 3.7 Dev Preview on the complete audit trail (it would cost the November window); do gate GA on it firmly (compliance is non-negotiable); ship a minimum write-event log at Dev Preview plus a clear non-production disclosure. The audit trail is a Phase-2 must-close item in the roadmap (§4).

### 6.2 Scope-tier model — Recommendation: ship four OpenShift-native tiers for the MVP; keep the remaining tiers as a design horizon

**The question (Q-T3 / Q-MH-2).** Carry the governance prototype's full six-tier scope model (user / project / campaign / role / organizational / enterprise), or simplify to OpenShift-native tiers for the MVP? Three tiers — `campaign`, `organizational`, `enterprise` — have no native OpenShift analogue ([research 08](/features/agent-memory/research/08-rhoai-ocp-alignment.md) §5; [research 07](/features/agent-memory/research/07-taxonomy-and-decomposition.md) §7 Q-T3). `user` and `role` align with OpenShift OAuth RBAC; `project` aligns with OpenShift namespaces / MLflow workspaces; `campaign`, `organizational`, and `enterprise` have no native analogue and would be memory-service-internal constructs.

**Recommendation (PROPOSED): Ship four OpenShift-native scope tiers — `user`, `project`, `role`, `org` — in the 3.7 MVP. Keep the remaining tiers (`campaign`, `organizational`, `enterprise`) as a documented design horizon, addable later without an API break.**

**Rationale:**

1. **The MVP should map to constructs the platform already enforces.** `user` aligns with OpenShift OAuth identity; `project` aligns with OpenShift namespaces / MLflow workspaces; `role` aligns with OpenShift OAuth RBAC groups (e.g., a team role within a project); `org` is the cluster/tenant boundary. These four are directly enforceable with platform identity and existing RBAC ([research 08](/features/agent-memory/research/08-rhoai-ocp-alignment.md) §5 Q-T3/Q-T7 note). The remaining `campaign`, `organizational`, and `enterprise` tiers "have no native OpenShift analogue and would be memory-service-internal constructs" — extra surface to build, test, and govern for value the MVP cannot yet prove it needs.

2. **The research itself flags six tiers as possibly over-complex.** This is not a new concern — [research 03] §5.3 Gap 7 and [research 07](/features/agent-memory/research/07-taxonomy-and-decomposition.md) §4.3 both flag the six-tier model as possibly over-engineered for a product. Simplifying to the four platform-anchored tiers is the conservative, research-aligned choice.

3. **Four tiers do not foreclose six.** Scope is an attribute on a memory record. A four-tier MVP that models scope as an extensible enumeration can add `campaign` or `organizational` later as new values without breaking the API or migrating data. Shipping fewer tiers first is reversible; shipping six and discovering three are unused is not cleanly reversible.

4. **It de-risks the actor-chain RBAC problem.** The hardest unsolved governance problem — actor-chain lowest-permission enforcement for shared memory (Q-G5) — gets combinatorially harder with more tiers. Four platform-anchored tiers make the 3.7 RBAC model tractable; the no-analogue tiers can be added once the actor-chain model is proven.

**Net:** Four OpenShift-native tiers (`user` / `project` / `role` / `org`) for the 3.7 MVP, modeled as an extensible enumeration; the remaining `campaign`, `organizational`, and `enterprise` tiers are documented as a design horizon for post-GA. The deferred tiers are precisely those with no native OpenShift analogue. This is reversible-by-design and research-aligned. The empirical workload-profile measurement (Q-G4) should inform whether and when the remaining tiers are warranted.

---

## 7. Differentiation and Competitive Positioning

**RHOAI's whitespace (from [research 00](/features/agent-memory/research/00-executive-summary.md) §6):** enterprise governance + Kubernetes-native self-hosted + air-gappable + open standard interface. No competitor offers all four.

| Competitor camp | Their strength | Why they cannot occupy RHOAI's position |
|---|---|---|
| Hyperscaler managed memory | GA, product-validated | Cloud-only — no on-premise / air-gap path |
| Enterprise database-native (Oracle) | Highest external governance maturity | Oracle Database lock-in; not portable to OpenShift |
| OSS memory startups / frameworks | Deployment-flexible, open-source | Governance thin/absent; market-consolidation risk |

**Red Hat's differentiators:**

- **Open-source foundation** — built on upstream community projects (Red Hat is already a core contributor) and Apache-2.0-licensed prototypes. No proprietary lock-in.
- **OpenShift-native deployment** — UBI9, FIPS delegation, air-gap, on-cluster vLLM embeddings. The only camp that can serve regulated, sovereign, and disconnected customers.
- **Governance depth** — the scope/RBAC/curation/provenance governance model is deeper than any OSS competitor and not locked to a proprietary database the way Oracle's is.
- **Credible standards posture** — AAIF Gold membership and existing upstream contributor channels make the upstream-contribution posture real, not aspirational ([research 00](/features/agent-memory/research/00-executive-summary.md) §3 finding 14).

**Positioning statement (PROPOSED):** *RHOAI agent memory is the governed memory substrate for enterprises that cannot send their agents' memory to a hyperscaler and will not lock it into a proprietary database — self-hosted, air-gappable, framework-agnostic, and built toward open standards.*

---

## 8. Risks and Dependencies

**Risks (PROPOSED assessment):**

| Risk | Description | Mitigation |
|---|---|---|
| Gateway-native transition strands substrate work | The gateway-native replacement could re-home conversation state in a way that orphans substrate work built on the current delivery vehicle ([research 08](/features/agent-memory/research/08-rhoai-ocp-alignment.md) §4.7 caveat). | Resolve Q-G2 with the AI Gateway team before committing the substrate design; design the substrate workstream to the *governed-API* surface, not delivery-vehicle internals. |
| Phase 0 upstream consensus insufficient | 3.6 standards work doesn't land enough upstream consensus to de-risk the 3.7 build — API surface designed without standards alignment. | Scope Phase 0 to achievable milestones (draft SEPs, not ratified standards); design the 3.7 API surface to be standards-*aligned*, not standards-*dependent*. |
| Phase 2 research expands GA scope | Adversarial memory defense and benchmarking (Phase 2 research findings) add new GA acceptance criteria, expanding the scope of 3.8+ work. | Size M10/M11 RFEs early; prioritize adversarial defense as security-critical; benchmarking can be phased incrementally. |
| Gateway-native parity gap | The gateway-native architecture may not have full primitive parity at Phase 1 (3.7) — Files API frontend requirements are OPEN, compaction detailed design is DISCUSSED ([research 16](/features/agent-memory/research/16-ai-gateway-memory-substrate.md) §3). | Substrate-agnostic API surface allows a transitional fallback. Track parity gaps as design-time validation items, not blockers. Per-namespace deployment provides Phase 1 isolation. |
| Org cannot absorb the roadmap | Competing priorities; ~3-month release cadence. | Phase 0 is near-zero cost; Phase 1 is Dev Preview; sizing is explicit per phase (§4). |
| Audit trail under-delivered for GA | EU AI Act August 2026; neither candidate ships one. | GA gate held firm (§6.1); minimum write-event log at Dev Preview; audit treated as a Phase-2 must-close item. |
| Market consolidation / picking a non-survivor | 5+ memory startups converging. | Partner products only as pluggable backends, never the substrate ([research 08](/features/agent-memory/research/08-rhoai-ocp-alignment.md) §4.5). |
| Proprietary-API lock-in | A bespoke RHOAI memory API would inherit a migration cost when a standard emerges. | Standards workstream from day one (§5); build against MCP transport. |

**Dependencies and required cross-team follow-ups (named, not invented — per REVIEW-NOTES "Open items"):**

- **Q-G2** — exact memory API surface and the gateway-native transition plan. *Owner: AI Gateway team.* **Directionally answered:** the AI Gateway is the platform delivery vehicle; parity timeline aligns with 3.7 ([REVIEW-NOTES — Platform Transition Context](/features/agent-memory/research/REVIEW-NOTES.md#ogx-deprecation-context-2026-06-10)). Remaining: validate specific primitive parity (Files API, compaction design) before Phase 1 design lock.
- **Q-G4** — RHOAI memory workload profile (volume / concurrency / entity counts). *Commissioned as a design-time measurement task.* Informs the substrate-scaling and scope-tier decisions.
- **Q-G3** — memory-as-registry-asset boundary (is the service an asset; are individual records registry-governed?). *Owner: AI Asset Registry team (joint).*
- **Q-G5** — actor-chain RBAC for shared memory (lowest-permission enforcement across an agent call chain). *Owner: AI Gateway team (joint).* Privilege-escalation risk if unaddressed.
- **Q-G6** — platform identity vs. the governance prototype's standalone OAuth (recommendation: consume Spire/Authbridge, RFC 8693 token exchange). *Owner: AI Gateway / kagenti teams (joint).*
- **Q-T4** — procedural memory vs. skills registry vs. prompts-primitive boundary. The research's three-layer model (governed artifacts / runtime store / agent-learned) is a *position to socialize*, not a settled answer. *Owner: skills/MLflow team + memory team (joint).*
- **Q-MH-1** — governance prototype IP/copyright transfer (currently held by an individual). *Administrative prerequisite for productization of the governance layer.*

None of these are invented answers; they are flagged as required follow-ups, with the roadmap phases that depend on them noted in §4.

---

## 9. Basis and Sources

This strategy is built on the Phase 1 research (docs 00–08), the Phase 2 research (docs 09–15), and the review gate; it does not re-derive the research's conclusions. Phase 2 research findings have been integrated where they reshape scope (adversarial defense, benchmarking) or strengthen existing positions (KV-cache optimization, enterprise use cases, harness memory patterns).

**The contract:** [REVIEW-NOTES.md](/features/agent-memory/research/REVIEW-NOTES.md) — decisions D1–D6 and the deferred/open items. Every DECIDED marker in this document traces to a REVIEW-NOTES decision.

| Source | Used for |
|---|---|
| [REVIEW-NOTES.md](/features/agent-memory/research/REVIEW-NOTES.md) | D1–D6, the two deferred questions, the open cross-team items |
| [research 00 — Executive Summary](/features/agent-memory/research/00-executive-summary.md) | The whitespace, competitive camps, key findings |
| [research 07 — Taxonomy & Decomposition](/features/agent-memory/research/07-taxonomy-and-decomposition.md) | The accepted decomposition |
| [research 08 — RHOAI & OCP Alignment](/features/agent-memory/research/08-rhoai-ocp-alignment.md) | Sourcing options, the phased combination, RHOAI integration, the Q-G* questions |
| [research 03 — Governance Prototype Deep-Dive](/features/agent-memory/research/03-memoryhub-deep-dive.md) | Governance model, productization gaps, scope tiers |
| [research 06 — Memory Primitives](/features/agent-memory/research/06-ogx-memory-primitives.md) | Internal memory primitives and gaps |
| [research 05 — Standards & Protocols](/features/agent-memory/research/05-standards-and-protocols.md) | The standards workstream and its three opportunities |
| [seed doc — agent-memory-knowledge.md](/features/agent-memory/research/agent-memory-landscape-research.md) | RHAISTRAT-1345 framing |
| [research 09 — Agent Harness Memory](/features/agent-memory/research/09-agent-harness-memory.md) | Harness-tier memory patterns informing client-side hybrid path |
| [research 11 — Adversarial Memory](/features/agent-memory/research/11-adversarial-memory.md) | Adversarial defense — new GA acceptance criterion |
| [research 12 — Benchmarking & Evaluation](/features/agent-memory/research/12-benchmarking-evaluation.md) | Memory quality benchmarking — new GA acceptance criterion |
| [research 13 — KV-Cache Optimization](/features/agent-memory/research/13-kv-cache-optimization.md) | KV-cache-aware ordering research backing for context engineering |
| [research 14 — Enterprise Use Cases](/features/agent-memory/research/14-enterprise-use-cases.md) | Enterprise use-case validation |
| [research 16 — AI Gateway Memory Substrate](/features/agent-memory/research/16-ai-gateway-memory-substrate.md) | Gateway-native transition analysis, primitive mapping, parity gaps |

**Implementation context:** This strategy is deliberately capability-framed — it describes WHAT the business needs and WHY, not which specific codebases or technologies deliver it. The research documents (00–16) contain the solution-specific evaluations, including deep-dives on individual internal and external candidates. Sourcing decisions reference those evaluations; readers seeking implementation-level specifics should consult the research series.

**Status discipline:** This is a PM proposal — PROPOSED unless marked DECIDED (review-gate settled) or DIRECTIONAL (beyond 3.6). No RHOAI release contents, Jira keys, or dates are invented beyond what the research and REVIEW-NOTES establish: RHOAI 3.6 = November 2026 is given; 3.7 (~Q1-Q2 2027) is the base-solution target; 3.8+ is directional.
