---
title: Agent Memory — RFE Roadmap (Outlines)
description: Outlined RFE breakdown for RHAISTRAT-1345, one outline per proposed RFE, sequenced to the incremental release roadmap.
source: ai-asset-registry/agent-memory/strategy/rfe-roadmap.md (as of 2026-07-05)
timestamp: 2026-07-06
review_after: 2026-08-05
---

# Agent Memory — RFE Roadmap (Outlines)

**Purpose:** An outlined RFE breakdown for the RHAISTRAT-1345 Outcome — one outline per proposed RFE, sequenced to the incremental release roadmap. Ready to feed `/rfe.create` later.

**Date:** 2026-06-09 (revised from 2026-05-18)

**Author:** Peter Double (Principal PM — MCP & AI Asset Registries)

**Status:** PROPOSED — RFE **outlines**, not full RFEs, and **not filed**. They are ready to feed `/rfe.create` once the [Outcome rewrite](rhaistrat-1345-outcome-update.md) is approved. Sizes (S/M/L) and sequence are PROPOSED estimates; 3.8+ items are DIRECTIONAL. Updated 2026-06-09 to reflect 3.6→3.7→3.8+ phasing, reframed M1, and two new RFEs (M10, M11) from Phase 2 research. No Jira keys are assigned — RHAISTRAT-1345 is the only existing key.

**Strategy series:** [README](strategy-overview.md) · [Strategy](agent-memory-strategy.md) · [Use Cases & Personas](use-cases-and-personas.md) · [Architecture](recommended-architecture.md) · [Outcome Update](rhaistrat-1345-outcome-update.md) · RFE Roadmap (this doc)

---

## 1. How This Maps to the Roadmap

RFEs are sequenced to the three roadmap phases ([strategy §4](agent-memory-strategy.md#4-the-incremental-roadmap)): Phase 0 = RHOAI 3.6 (Nov 2026), Phase 1 = RHOAI 3.7 (~Q1-Q2 2027), Phase 2 = RHOAI 3.8+ (directional). The timeline was set by Peter Double + Sanjeev Rampal (2026-06-09): base solution targets 3.7 Dev Preview; no memory deliverable in 3.5; 3.6 is standards/upstream only. Each RFE builds on the prior phase with no thrown-away work (the D3 incremental-path requirement). Size key: **S** ≈ enablement/docs or a contained change; **M** ≈ a feature on existing foundations; **L** ≈ a substantial new capability or productization effort.

| RFE | Title | Size | Phase / Release |
|---|---|---|---|
| RFE-M1 | Standards & upstream foundation | S | 0 — 3.6 |
| RFE-M2 | Framework-agnostic governed memory API | L | 1 — 3.7 |
| RFE-M3 | Enterprise governance & scope layer | L | 1 — 3.7 |
| RFE-M4 | Inspectable context-engineering capability | M | 1 — 3.7 |
| RFE-M5 | Memory-over-MCP exposure & AI Asset Registry integration | M | 1 — 3.7 |
| RFE-M6 | Append-only memory audit trail | L | 2 — 3.8+ (directional) |
| RFE-M7 | Memory service operator & observability | M | 2 — 3.8+ (directional) |
| RFE-M8 | Complete gateway-native transition & FIPS validation | L | 2 — 3.8+ (directional) |
| RFE-M9 | Client-side memory hybrid path | M | 2 — 3.8+ (directional) |
| RFE-M10 | Adversarial memory defense | M | 2 — 3.8+ (directional) |
| RFE-M11 | Memory quality benchmarking | M | 2 — 3.8+ (directional) |

The standards workstream (previously a parallel background effort) is now the Phase 0 (3.6) deliverable — absorbed into M1's scope.

---

## 2. RFE Outlines

### RFE-M1 — Standards & upstream foundation
- **Problem:** No agent-memory standard exists; shipping a proprietary RHOAI memory API before standards converge would inherit a migration cost. The 3.5 and 3.6 release windows carry heavy competing priorities, but the standards groundwork that de-risks the 3.7 substrate build can happen now.
- **Scope:** Standards and upstream contributions: (1) **MCP Memory Convention SEP** — a Standards Enhancement Proposal formalizing the de facto memory-tool naming convention into a reference convention (canonical tool set, minimal record format, scope model). (2) **Upstream MLflow collaboration** on memory abstractions. (3) **A2A AgentCard memory binding** — an optional extension declaring an agent's memory services (transport, scope, access model). Architecture validated against upstream consensus. The standards workstream (previously tracked as a parallel background effort per [strategy §5](agent-memory-strategy.md#5-the-parallel-standards-workstream)) is the primary Phase 0 deliverable.
- **Out of scope:** Any deployed substrate or governance code; Agent Knowledge.
- **Size:** S — contributor effort: specification drafting, upstream engagement, architecture validation.
- **Sequence:** Phase 0, RHOAI 3.6. Foundation for RFE-M2/M3/M4/M5.
- **Depends on:** No hard dependencies. Existing upstream contributor channels and AAIF Gold membership are existing assets.
- **Personas / use cases:** AI Engineer, Platform Engineer (indirect — standards alignment benefits all).

### RFE-M2 — Framework-agnostic governed memory API
- **Problem:** Every agent team reinvents memory plumbing; memory is not portable across frameworks.
- **Scope:** A stable, framework-agnostic RHOAI memory API exposing the four CoALA access patterns (working/episodic/semantic/procedural) over the governed substrate; works across LangGraph, CrewAI, OpenClaw; scope-aware, consuming RHOAI platform identity. This is the substrate workstream — mostly governance-wrapping of existing internal memory primitives.
- **Out of scope:** The governance-layer internals (RFE-M3); audit trail (RFE-M6); Agent Knowledge.
- **Size:** L — the core substrate deliverable, Dev Preview.
- **Sequence:** Phase 1, RHOAI 3.7 (Dev Preview).
- **Depends on:** RFE-M1 (standards foundation); Q-G2 (directionally answered — AI Gateway is the replacement); Q-G6 (platform identity).
- **Personas / use cases:** AI Engineer, Platform Engineer; UC-1, UC-2, UC-4.

### RFE-M3 — Enterprise governance & scope layer
- **Problem:** The memory substrate has no enterprise governance — no multi-tier scope, no curation, no contradiction detection, no provenance.
- **Scope:** A governance service alongside the memory substrate: four OpenShift-native scope tiers (`user`/`project`/`role`/`org`, modeled as an extensible enumeration — per [strategy §6.2](agent-memory-strategy.md#62-scope-tier-model--recommendation-ship-four-openshift-native-tiers-for-the-mvp-keep-the-remaining-tiers-as-a-design-horizon)); RBAC; inline curation (PII/secrets scanning); contradiction detection; provenance metadata. This is the governance workstream — productization of the internal governance prototype.
- **Out of scope:** The full audit trail (RFE-M6 — minimum write-event log only here); scope tiers with no OpenShift-native analogue (campaign/organizational/enterprise — design horizon); Agent Knowledge.
- **Size:** L — productization of a prototype, Dev Preview.
- **Sequence:** Phase 1, RHOAI 3.7 (Dev Preview).
- **Depends on:** RFE-M2; Q-MH-1 (governance prototype IP transfer — administrative prerequisite); Q-G5 (actor-chain RBAC).
- **Personas / use cases:** AgentOps Admin; UC-5, UC-7.

### RFE-M4 — Inspectable context-engineering capability
- **Problem:** Long-running agents overflow their context windows; opaque compaction is not compliance-inspectable.
- **Scope:** A context-engineering capability over the substrate — inspectable compaction (human-readable summaries), retrieval assembly, progressive disclosure, KV-cache-aware ordering — now backed by Phase 2 research ([research 13](/features/agent-memory/research/13-kv-cache-optimization.md)). Built on existing compaction primitives (`/responses/compact` and `context_management`). Carries its own quality metric (token efficiency at a quality threshold).
- **Out of scope:** Substrate storage (RFE-M2); Agent Knowledge.
- **Size:** M — a capability on existing compaction foundations.
- **Sequence:** Phase 1, RHOAI 3.7 (Dev Preview).
- **Depends on:** RFE-M2.
- **Personas / use cases:** AI Engineer; UC-3.

### RFE-M5 — Memory-over-MCP exposure & AI Asset Registry integration
- **Problem:** A governed memory service must be discoverable, per-tool-authorized, audited, and registered as a governed asset.
- **Scope:** Expose the memory API as MCP tools routed through the MCP Gateway (per-tool authz, metrics, audit logging, content guardrails on writes); register the memory *service* as a governed asset in the AI Asset Registry (two-tier model, like an MCP Server); record agent→memory bindings.
- **Out of scope:** Whether individual memory *records* are registry-governed (Q-G3 — open cross-team item); Agent Knowledge.
- **Size:** M — integration on existing gateway/registry patterns.
- **Sequence:** Phase 1, RHOAI 3.7 (Dev Preview).
- **Depends on:** RFE-M2, RFE-M3; Q-G3 (memory-as-registry-asset boundary — joint with AI Asset Registry team).
- **Personas / use cases:** Platform Engineer, AgentOps Admin; UC-6.

### RFE-M6 — Append-only memory audit trail *(directional)*
- **Problem:** No internal candidate ships a working audit trail; an inspectable append-only memory audit log is a hard EU AI Act / GDPR / HIPAA requirement and is GA-blocking.
- **Scope:** A complete inspectable, immutable, append-only audit trail of memory reads and writes; erasure primitives. Per [strategy §6.1](agent-memory-strategy.md#61-audit-trail-sequencing--recommendation-ga-gate-with-a-dev-preview-disclosure-obligation): a minimum write-event log ships in RFE-M3 at 3.7 Dev Preview; this RFE delivers the full trail as a **GA gate**.
- **Out of scope:** Agent Knowledge audit.
- **Size:** L — the highest-severity gap; schedule-consuming.
- **Sequence:** Phase 2, RHOAI 3.8+ (directional). GA-gating.
- **Depends on:** RFE-M3.
- **Personas / use cases:** AgentOps Admin; UC-6.

### RFE-M7 — Memory service operator & observability *(directional)*
- **Problem:** The governance prototype's Kubernetes operator is a skeleton and observability is TBD; a Red Hat product cannot ship as plain manifests.
- **Scope:** An OLM-integrated Kubernetes operator for the memory service; Prometheus metrics and Grafana dashboards for SRE/support.
- **Size:** M — productization work.
- **Sequence:** Phase 2, RHOAI 3.8+ (directional). GA-gating.
- **Depends on:** RFE-M2, RFE-M3.
- **Personas / use cases:** Platform Engineer.

### RFE-M8 — Complete gateway-native transition & FIPS validation *(directional)*
- **Problem:** Phase 1 (3.7) designs for the gateway architecture but may use a transitional fallback where gateway primitive parity is incomplete ([research 16](/features/agent-memory/research/16-ai-gateway-memory-substrate.md) §3); FIPS is delegated but not validated end-to-end.
- **Scope:** Complete the gateway-native transition — close any remaining primitive parity gaps (Files API, compaction), migrate any transitional dependencies, harden the gateway-routed deployment model; complete end-to-end FIPS validation.
- **Size:** L — depends on the gateway-native replacement existing.
- **Sequence:** Phase 2, RHOAI 3.8+ (directional). GA-gating.
- **Depends on:** Q-G2 (the gateway-native replacement plan must resolve); RFE-M2.
- **Personas / use cases:** Platform Engineer.

### RFE-M9 — Client-side memory hybrid path *(directional)*
- **Problem:** IDE / dev-workflow agents (the harness tier) need a client-side memory path; the substrate defaults to server-side only.
- **Scope:** A client-side memory deployment mode with hybrid search, portable to/from the server-side substrate, so an agent's memory moves between modes. Phase 2 research on harness memory patterns ([research 09](/features/agent-memory/research/09-agent-harness-memory.md)) informs the design. *Note: this is the least-researched element of the deployment model — carried as directional until further validation.*
- **Size:** M.
- **Sequence:** Phase 2, RHOAI 3.8+ (directional).
- **Depends on:** RFE-M2.
- **Personas / use cases:** AI Engineer; UC-8.

### RFE-M10 — Adversarial memory defense *(directional)*
- **Problem:** Agent memory is an attack surface: prompt injection via memory writes, memory poisoning across shared scopes, and gradual belief manipulation are identified threats ([research 11](/features/agent-memory/research/11-adversarial-memory.md)). PII/secrets scanning (RFE-M3) is necessary but not sufficient — adversarial patterns require dedicated detection.
- **Scope:** Adversarial injection pattern detection on memory writes; memory quarantine for flagged records; poisoning prevention across shared scope tiers. Defense-in-depth layered on top of RFE-M3's curation (PII/secrets scanning). GA-gating — adversarial defense is security-critical.
- **Out of scope:** General model security; prompt-injection defense at the inference layer (IPP/guardrails concern); Agent Knowledge.
- **Size:** M — detection patterns + quarantine workflow.
- **Sequence:** Phase 2, RHOAI 3.8+ (directional). GA-gating.
- **Depends on:** RFE-M3 (governance layer provides the write-path hooks).
- **Personas / use cases:** AgentOps Admin; UC-9.

### RFE-M11 — Memory quality benchmarking *(directional)*
- **Problem:** No existing memory system ships with built-in quality measurement ([research 12](/features/agent-memory/research/12-benchmarking-evaluation.md)). Operators cannot validate that the substrate meets quality thresholds before production deployment. Without benchmarks, memory degradation is invisible until agents produce poor results.
- **Scope:** Standardized recall/precision benchmarks for the memory substrate; quality threshold validation tooling; metrics covering recall accuracy, multi-session persistence, and contradiction rates. Can be phased: basic recall metrics first, comprehensive quality dashboards later.
- **Out of scope:** Inference-quality benchmarking (model concern); Agent Knowledge quality.
- **Size:** M — benchmarking framework + integration with observability (RFE-M7).
- **Sequence:** Phase 2, RHOAI 3.8+ (directional).
- **Depends on:** RFE-M2 (substrate API to benchmark against); RFE-M7 (observability integration).
- **Personas / use cases:** Platform Engineer; UC-10.

---

## 3. Parallel — Standards Workstream (not a release-committed RFE)

The standards workstream is now **absorbed into RFE-M1 as the Phase 0 (3.6) deliverable** (see [strategy §5](agent-memory-strategy.md#5-the-parallel-standards-workstream)). The three opportunities are:

- **MCP Memory Convention SEP** — **Phase 0 (3.6) deliverable**; the 3.7 substrate's MCP surface tracks it.
- **A2A AgentCard memory binding** — **Phase 0 (3.6) deliverable**; propose alongside RFE-M5's registry integration at 3.7.
- **AAIF memory project** — socialize from Phase 0 (3.6); formal proposal as the substrate matures post-3.7.

The named follow-up is to resource the standards effort and assign an owner (open item Q-G8, settled by REVIEW-NOTES D6 as parallel-from-the-start).

---

## 4. Out of Scope — Agent Knowledge RFEs

No RFEs for **Agent Knowledge** appear here. Agent Knowledge is a separate Outcome / separate run (REVIEW-NOTES D2; [strategy §2.1](agent-memory-strategy.md#21-agent-knowledge--deferred-pointer-only)); its RFE breakdown is produced when that run begins.

---

## 5. Sources

| Source | Used for |
|---|---|
| [REVIEW-NOTES.md](/features/agent-memory/research/REVIEW-NOTES.md) | D2/D3/D5/D6 — scope, incremental path, standards |
| [agent-memory-strategy.md](agent-memory-strategy.md) | The roadmap phases, audit-trail and scope-tier recommendations |
| [rhaistrat-1345-outcome-update.md](rhaistrat-1345-outcome-update.md) | The Outcome these RFEs are children of |
| [use-cases-and-personas.md](use-cases-and-personas.md) | Persona / use-case mapping per RFE |
| [research 08](/features/agent-memory/research/08-rhoai-ocp-alignment.md) | Productization gaps (D-5/D-6/D-7/D-8/D-9), the Q-G* dependencies |
| [research 09](/features/agent-memory/research/09-agent-harness-memory.md) | Harness memory patterns (RFE-M9 design input) |
| [research 11](/features/agent-memory/research/11-adversarial-memory.md) | Adversarial memory attack surface (RFE-M10) |
| [research 12](/features/agent-memory/research/12-benchmarking-evaluation.md) | Memory quality benchmarking gap (RFE-M11) |
| [research 13](/features/agent-memory/research/13-kv-cache-optimization.md) | KV-cache research backing (RFE-M4) |
| [research 16](/features/agent-memory/research/16-ai-gateway-memory-substrate.md) | Gateway-native transition, primitive mapping, parity gaps (M2, M8) |
