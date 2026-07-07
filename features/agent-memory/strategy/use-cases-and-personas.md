---
title: Agent Memory — Use Cases and Personas
description: Who needs the RHOAI agent memory substrate, the concrete use cases driving its scope, and how each ties to a roadmap phase.
source: ai-asset-registry/agent-memory/strategy/use-cases-and-personas.md (as of 2026-07-05)
timestamp: 2026-07-06
review_after: 2026-08-05
---

# Agent Memory — Use Cases and Personas

**Purpose:** Identify who needs the RHOAI agent memory substrate and the concrete use cases driving its scope, and tie each use case to a roadmap phase.

**Date:** 2026-06-09 (revised from 2026-05-18)

**Author:** Peter Double (Principal PM — MCP & AI Asset Registries)

**Status:** PROPOSED — a PM strategy proposal for leadership review. Personas are drawn from the established RHOAI persona set ([target-users.md](https://github.com/solaius/ai-asset-registry/blob/main/docs/knowledge-review/personas/target-users.md)); use cases trace to the Phase 1 research and conform to the review-gate scope (REVIEW-NOTES D2 — Agent Memory Substrate + Context Engineering only). Updated 2026-06-09 to reflect the 3.6→3.7→3.8+ phasing, Phase 2 research integration, and two new use cases (UC-9, UC-10).

**Strategy series:** [README](strategy-overview.md) · [Strategy](agent-memory-strategy.md) · Use Cases & Personas (this doc) · [Architecture](recommended-architecture.md) · [Outcome Update](rhaistrat-1345-outcome-update.md) · [RFE Roadmap](rfe-roadmap.md)

---

## 1. Why Personas Matter Here

The memory substrate is a *platform primitive*, not an end-user application. Its users are the people who build, govern, and operate agents on RHOAI — not the business consumers who eventually interact with those agents. Getting the persona set right keeps the scope honest: the substrate exists to serve the four personas below, and a proposed capability that does not clearly serve one of them is out of scope.

Personas are taken verbatim from the RHOAI persona set ([target-users.md](https://github.com/solaius/ai-asset-registry/blob/main/docs/knowledge-review/personas/target-users.md)); the memory-specific framing is this document's.

---

## 2. The Personas and Their Memory Needs

### 2.1 AI Engineers — *primary users*

The primary users of the registry ecosystem: they build AI applications, consume governed assets, and create new ones ([target-users.md](https://github.com/solaius/ai-asset-registry/blob/main/docs/knowledge-review/personas/target-users.md)).

**Memory pain today.** Every agent team reinvents memory handling — conversation state, long-term persistence, context compaction — as custom plumbing ([seed doc](/features/agent-memory/research/agent-memory-landscape-research.md) §2). An AI Engineer who switches frameworks (LangGraph → CrewAI → OpenClaw) loses or has to re-port their memory layer. "Switching models is cheap; switching memory is not" ([seed doc](/features/agent-memory/research/agent-memory-landscape-research.md) §6).

**What the substrate gives them.** A framework-agnostic memory API they call without custom plumbing; conversation state and long-term persistence as a primitive; context compaction for long-running agents. Their work stops including a memory subsystem.

### 2.2 Platform Engineers

Responsible for setting up, integrating, and maintaining the AI platform; care about tenancy, access control, operational consistency, and a scalable foundation for current and future asset types ([target-users.md](https://github.com/solaius/ai-asset-registry/blob/main/docs/knowledge-review/personas/target-users.md)).

**Memory pain today.** A memory store is a stateful, append-heavy datastore — the first AI asset type that is *itself* a live datastore rather than a metadata record ([research 00](/features/agent-memory/research/00-executive-summary.md) §3 finding 12). Without a platform primitive, every agent team's bespoke memory store is an un-operated, un-monitored, un-secured liability the Platform Engineer inherits.

**What the substrate gives them.** One governed, OpenShift-native memory service to deploy and operate — UBI9, FIPS-delegated, air-gappable, OLM-managed (at GA), Prometheus-observable (at GA). One thing to secure and scale instead of N bespoke stores.

### 2.3 AgentOps Admins

Responsible for governance, approval, enablement, and operational oversight; review and approve assets, control what is enabled, manage governance state, associate assets with policies, and understand lineage and ownership ([target-users.md](https://github.com/solaius/ai-asset-registry/blob/main/docs/knowledge-review/personas/target-users.md)).

**Memory pain today.** Ungoverned memory is an audit and compliance gap: no scope isolation, no audit trail, no erasure, no provenance, no contradiction detection. For EU AI Act (enforcement August 2026), GDPR, and HIPAA this is disqualifying ([research 00](/features/agent-memory/research/00-executive-summary.md) §3 finding 13).

**What the substrate gives them.** The Governance & Scope dimension: scope tiers (`user`/`project`/`role`/`org`), RBAC, curation, contradiction detection, provenance, and — at GA — an inspectable append-only audit trail and erasure. The memory service is a governed asset in the AI Asset Registry, with the same lifecycle/approval/verification model as any other asset.

### 2.4 Business Consumers — *indirect beneficiaries*

Indirect users who benefit from governed assets through the applications and assistants they use; want trusted, reliable AI capabilities and lower risk from ungoverned assets ([target-users.md](https://github.com/solaius/ai-asset-registry/blob/main/docs/knowledge-review/personas/target-users.md)).

**Memory relevance.** Business Consumers never touch the substrate directly. They benefit because agents backed by a governed memory substrate are more consistent (memory-aware agents focus better than memory-augmented ones) and lower-risk (governed, audited memory rather than a bespoke store). The substrate is plumbing they should never have to think about.

### 2.5 Customer insight signals

The Agentic Strategy customer insights ([target-users.md](https://github.com/solaius/ai-asset-registry/blob/main/docs/knowledge-review/personas/target-users.md) §"Key Customer Insights") corroborate the memory need:

- **SAS** — "can't move agents to production without an audit trail." Directly the Q-G7 / §6.1 audit-trail concern: memory without an audit trail blocks production.
- **Infineon** — multiple frameworks (AutoGen, LangChain, LangGraph). Directly the framework-agnostic-substrate requirement.
- **Florida Blue** — "DIY proliferation, need centralized control." Directly the "every team reinvents memory" pain — the substrate is the control plane.
- **Turkcell** — project-level chargeback. The `project` scope tier and per-tenant accounting depend on a governed substrate.

---

## 3. Use Cases Driving Scope

Each use case is tied to the persona it serves and the roadmap phase that delivers it ([strategy §4](agent-memory-strategy.md#4-the-incremental-roadmap)).

### UC-1 — Conversation state without custom plumbing
**Persona:** AI Engineer. **Memory type:** working / episodic.
An agent maintains multi-turn conversation state across a session via a platform API instead of hand-rolled history management. Existing memory primitives (Conversations API, `previous_response_id` chaining) already provide this ([research 06](/features/agent-memory/research/06-ogx-memory-primitives.md)); the use case is *surfacing it as a governed RHOAI feature*.
**Roadmap:** governed API in **Phase 1 (3.7)**.

### UC-2 — Long-term knowledge persistence across sessions
**Persona:** AI Engineer. **Memory type:** semantic / episodic.
An agent recalls facts, preferences, and prior-session experiences durably — the multi-session recall that every benchmark shows is the hardest category ([research 00](/features/agent-memory/research/00-executive-summary.md) §3 finding 11). Backed by existing vector store and file storage primitives.
**Roadmap:** **Phase 1 (3.7)** governed substrate.

### UC-3 — Context compaction for long-running agents
**Persona:** AI Engineer. **Memory type:** context engineering (Subsystem 2).
A long-running multi-turn agent's context window is kept bounded by inspectable compaction — human-readable summaries, not opaque tokens, so compaction is compliance-inspectable ([research 00](/features/agent-memory/research/00-executive-summary.md) §3 finding 10). Existing compaction primitives (`/responses/compact`) are the substrate.
**Roadmap:** inspectable governed compaction in **Phase 1 (3.7)**.

### UC-4 — Framework-agnostic memory across LangGraph / CrewAI / OpenClaw
**Persona:** AI Engineer, Platform Engineer.
One memory abstraction works across frameworks, so an agent's memory survives a framework switch (the Infineon signal). The RHAISTRAT-1345 acceptance criterion "memory primitives work across frameworks."
**Roadmap:** **Phase 1 (3.7)** — the framework-agnostic governed API is the core of the substrate workstream.

### UC-5 — Scoped, shared memory for multi-agent teams
**Persona:** AI Engineer, AgentOps Admin. **Cross-cutting:** Governance & Scope.
Memory is scoped — `user` / `project` / `role` / `org` ([strategy §6.2](agent-memory-strategy.md#62-scope-tier-model--recommendation-ship-four-openshift-native-tiers-for-the-mvp-keep-the-remaining-tiers-as-a-design-horizon)) — so a team of agents can share project-scoped or role-scoped memory while user-private memory stays isolated. Depends on actor-chain RBAC (Q-G5, an open cross-team item).
**Roadmap:** **Phase 1 (3.7)** for the four-tier model; actor-chain RBAC hardening into **Phase 2 (3.8+)**.

### UC-6 — Governed, audited memory for regulated production
**Persona:** AgentOps Admin, Platform Engineer. **Cross-cutting:** Governance & Scope.
Memory writes/reads are auditable; memory records have provenance and can be erased; the memory service is a governed registry asset. This is the SAS "can't go to production without an audit trail" signal and the EU AI Act constraint.
**Roadmap:** minimum write-event log at **Phase 1 (3.7) Dev Preview**; full inspectable append-only audit trail and erasure are a **Phase 2 (3.8+) GA** gate (per [strategy §6.1](agent-memory-strategy.md#61-audit-trail-sequencing--recommendation-ga-gate-with-a-dev-preview-disclosure-obligation)).

### UC-7 — Memory curation and contradiction detection
**Persona:** AgentOps Admin. **Cross-cutting:** Governance & Scope.
Memory writes pass PII/secrets scanning; contradictory memories are flagged rather than silently coexisting — the governance layer's curation and contradiction-detection capability ([research 03](/features/agent-memory/research/03-memoryhub-deep-dive.md)).
**Roadmap:** **Phase 1 (3.7)** governance workstream (Dev Preview).

### UC-8 — Client-side memory for IDE / dev-workflow agents
**Persona:** AI Engineer. **Cross-cutting:** Deployment model.
IDE and dev-workflow agents (the "harness tier") use a client-side memory path with hybrid search, while platform-tier agents default to the server-side substrate ([seed doc](/features/agent-memory/research/agent-memory-landscape-research.md) §6; Francisco Arceo's RHAISTRAT-1345 comment). Server-side is the default; client-side is the hybrid path. *Note: this is the least-researched element of the deployment model — carried as directional until further validation.*
**Roadmap:** server-side substrate is **Phase 1 (3.7)**; the client-side hybrid path is directional, **Phase 2 (3.8+)**, informed by harness memory research ([research 09](/features/agent-memory/research/09-agent-harness-memory.md)).

### UC-9 — Adversarial memory defense
**Persona:** AgentOps Admin. **Cross-cutting:** Governance & Scope.
Memory writes are validated against adversarial injection patterns; poisoned memories are quarantined rather than silently persisted. This addresses the adversarial memory attack surface identified in Phase 2 research ([research 11](/features/agent-memory/research/11-adversarial-memory.md)) — prompt injection via memory, memory poisoning across shared scopes, and gradual belief manipulation. Defense-in-depth: PII/secrets scanning (UC-7) plus adversarial pattern detection.
**Roadmap:** **Phase 2 (3.8+)** — GA gate. Adversarial defense is security-critical and gates production readiness alongside the audit trail.

### UC-10 — Memory quality benchmarking
**Persona:** Platform Engineer. **Cross-cutting:** Governance & Scope.
Memory recall quality is measurable via standardized benchmarks — operators validate that the substrate meets quality thresholds before production deployment. Phase 2 research ([research 12](/features/agent-memory/research/12-benchmarking-evaluation.md)) identified that no existing memory system ships with built-in quality measurement, making this a differentiation opportunity. Benchmarks cover recall accuracy, multi-session persistence, and contradiction rates.
**Roadmap:** **Phase 2 (3.8+)**. Can be phased incrementally — basic recall metrics first, then comprehensive quality dashboards.

### Use-case-to-phase summary

| Use case | Primary persona | Phase 0 (3.6) | Phase 1 (3.7) | Phase 2 (3.8+) |
|---|---|---|---|---|
| UC-1 Conversation state | AI Engineer | — | governed API | — |
| UC-2 Long-term persistence | AI Engineer | — | core | — |
| UC-3 Context compaction | AI Engineer | — | inspectable | — |
| UC-4 Framework-agnostic memory | AI/Platform Eng | — | core | — |
| UC-5 Scoped shared memory | AI Eng / AgentOps | — | 4-tier model | actor-chain RBAC |
| UC-6 Governed/audited memory | AgentOps / Platform | — | write-event log (DP) | full audit (GA) |
| UC-7 Curation / contradiction | AgentOps Admin | — | governance (DP) | hardened |
| UC-8 Client-side memory | AI Engineer | — | server-side default | client-side hybrid |
| UC-9 Adversarial defense | AgentOps Admin | — | — | GA gate |
| UC-10 Quality benchmarking | Platform Engineer | — | — | phased |

---

## 4. Out of Scope for This Run

Use cases for **Agent Knowledge** — org-wide regulations/policies/product-knowledge graphs, enterprise-RAG-shaped retrieval — are **not** in this set. Agent Knowledge is a separate Outcome / separate run (REVIEW-NOTES D2; [strategy §2.1](agent-memory-strategy.md#21-agent-knowledge--deferred-pointer-only)). The personas above will also be the users of Agent Knowledge when that run begins, but its use cases are deferred.

---

## 5. Sources

| Source | Used for |
|---|---|
| [target-users.md](https://github.com/solaius/ai-asset-registry/blob/main/docs/knowledge-review/personas/target-users.md) | The four personas and the customer-insight signals |
| [REVIEW-NOTES.md](/features/agent-memory/research/REVIEW-NOTES.md) | Scope boundary (D2) — Agent Knowledge out of scope |
| [research 00](/features/agent-memory/research/00-executive-summary.md) | Key findings on memory pain, audit, multi-session |
| [research 06](/features/agent-memory/research/06-ogx-memory-primitives.md) | Memory primitives underlying UC-1/UC-2/UC-3 |
| [research 03](/features/agent-memory/research/03-memoryhub-deep-dive.md) | Governance prototype curation / contradiction detection (UC-7) |
| [seed doc](/features/agent-memory/research/agent-memory-landscape-research.md) | RHAISTRAT-1345 problem framing; client/server-side memory |
| [agent-memory-strategy.md](agent-memory-strategy.md) | Roadmap phases the use cases map to |
| [research 11](/features/agent-memory/research/11-adversarial-memory.md) | Adversarial memory attack surface (UC-9) |
| [research 12](/features/agent-memory/research/12-benchmarking-evaluation.md) | Memory quality benchmarking gap (UC-10) |
