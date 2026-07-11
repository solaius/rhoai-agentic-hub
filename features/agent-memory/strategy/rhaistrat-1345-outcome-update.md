---
title: RHAISTRAT-1345 — Proposed Outcome Rewrite
description: Outcome rewrite lineage for RHAISTRAT-1345 - a revised version (standalone service, 3.6 DP / 3.7 TP / 3.8 GA, six child RFEs) was applied to Jira 2026-07-10; the section 2 draft below is the superseded June-9 version.
source: ai-asset-registry/agent-memory/strategy/rhaistrat-1345-outcome-update.md (as of 2026-07-05)
timestamp: 2026-07-10
review_after: 2026-08-05
---

# RHAISTRAT-1345 — Proposed Outcome Rewrite

**Purpose:** A proposed rewrite of the RHAISTRAT-1345 Outcome ("Agent Memory Primitives"), reflecting the review-gate decisions — to be reviewed and, once approved, pasted into Jira.

**Date:** 2026-06-09 (revised from 2026-05-18)

**Author:** Peter Double (Principal PM — MCP & AI Asset Registries)

**Status:** APPLIED (superseded draft below). On 2026-07-10 a revised version of this rewrite was written to the RHAISTRAT-1345 Jira description, updated beyond the section 2 text to reflect the 2026-06-30 direction: standalone service decoupled from OGX and AI Gateway, three-layer framing (substrate / memory intelligence / governance and scope), multi-backend storage requirement, revised phasing (3.6 DP deliberately not TP, 3.7 TP Feb 2027 for Summit setup, 3.8 GA at the Summit drop), EU AI Act Annex III deferral nuance, and the six child RFEs RHAIRFE-2630..2635 (see [fact-rhaistrat-1345-rfes-filed-20260710](/features/agent-memory/knowledge/fact-rhaistrat-1345-rfes-filed-20260710.md)). The section 2 draft below is retained as lineage; the Jira description is now authoritative. Original 2026-06-09 rewrite reflected REVIEW-NOTES D1-D5.

**Strategy series:** [README](strategy-overview.md) · [Strategy](agent-memory-strategy.md) · [Use Cases & Personas](use-cases-and-personas.md) · [Architecture](recommended-architecture.md) · Outcome Update (this doc) · [RFE Roadmap](rfe-roadmap.md)

---

## 1. Why a Rewrite

RHAISTRAT-1345's current scope ("short-term conversation state, long-term knowledge persistence, context compaction, cross-framework memory abstractions" — [seed doc](/features/agent-memory/research/agent-memory-landscape-research.md) §2) was authored before the Phase 1 research. The review gate (REVIEW-NOTES) made four changes the Outcome text should now reflect:

1. **D1** — the problem space is a 3-subsystem + 2-cross-cutting-dimension decomposition, not three peer areas.
2. **D2** — the Outcome is scoped to the **Agent Memory Substrate + Context Engineering**; **Agent Knowledge is spun out as a separate Outcome**. The current text's "long-term knowledge persistence" is ambiguous between memory and org-knowledge — that ambiguity must be removed.
3. **D4** — one governed substrate for the four memory types, framed as four access patterns over one store, not "short-term + long-term" as two things.
4. **D5** — delivery is incremental: 3.6 upstream foundation → 3.7 Dev Preview → 3.8+ GA.

Everything below is **plain markdown ready to paste into Jira**. It is not a Jira write.

---

## 2. Proposed Outcome Text (paste-ready)

> ### Outcome: Governed Agent Memory Substrate
>
> #### Problem
>
> There is no convergence on what good agent memory looks like on RHOAI (discovery signal, Feb–Mar 2026). Every agent team reinvents memory handling — conversation state, long-term persistence, context compaction — as custom, per-framework plumbing. The result is duplicated effort, no portability when an agent's framework changes ("switching models is cheap; switching memory is not"), and — most seriously — ungoverned memory: no scope isolation, no audit trail, no erasure, no provenance. For regulated customers this is disqualifying (EU AI Act enforcement August 2026; GDPR; HIPAA). RHOAI should provide agent memory as a governed platform primitive.
>
> RHOAI is well-positioned: production-ready memory primitives (Conversations, Vector Stores, Files, Prompts, Compaction) already ship internally, and Red Hat holds an OpenShift-native governed-memory prototype with a mature governance model. The two are complementary — the memory primitives are the substrate, the governance prototype provides the enterprise governance layer. The gap is exposing them as a single governed, framework-agnostic RHOAI feature.
>
> #### Scope
>
> This Outcome covers the **Agent Memory Substrate** and **Context Engineering**:
>
> - **Agent Memory Substrate** — one governed memory store exposing the four memory access patterns (working, episodic, semantic, procedural), append-heavy and agent-written, with a framework-agnostic API.
> - **Context Engineering** — an in-scope capability over the substrate: inspectable context compaction, retrieval assembly, progressive disclosure, KV-cache-aware ordering.
> - **Governance & Scope** (cross-cutting) — scope tiers (`user`/`project`/`role`/`org`), RBAC, curation, contradiction detection, provenance, and an audit trail.
> - **Deployment model** (cross-cutting) — server-side as the default, with a client-side hybrid path for IDE/dev-workflow agents.
>
> **Explicitly out of scope:** **Agent Knowledge** — the org-wide enterprise-knowledge layer (regulations, policies, product knowledge, code, processes). It is an enterprise-RAG / knowledge-graph architecture, distinct from agent memory, and is **spun out as a separate Outcome** with its own team and timeline. It is expected to extend the AI Asset Registry Knowledge Sources asset type.
>
> #### Acceptance Criteria
>
> **Dev Preview (RHOAI 3.7)**
>
> - The platform provides a governed memory API that agents call without custom plumbing.
> - The memory API is framework-agnostic — it works across LangGraph, CrewAI, OpenClaw, and other frameworks; an agent's memory survives a framework switch.
> - The substrate exposes all four memory access patterns (working, episodic, semantic, procedural) over one governed store.
> - Inspectable context compaction is available for long-running multi-turn agents (human-readable summaries, not opaque tokens).
> - Memory is scope-isolated across `user` / `project` / `role` / `org` tiers, with RBAC consuming RHOAI platform identity.
> - Memory writes pass curation (PII/secrets scanning); contradictory memories are flagged.
> - The memory service is registered as a governed asset in the AI Asset Registry.
> - A minimum write-event log (who/what/when/scope on every memory write) is available; the substrate carries an explicit non-production disclosure.
>
> **GA (RHOAI 3.8+) — directional**
>
> - An append-only, inspectable audit trail of all memory reads and writes is available; erasure primitives are present.
> - The substrate is OpenShift-native and production-ready: self-hosted, air-gap-deployable, FIPS-compliant, OLM-managed, Prometheus-observable.
> - Adversarial memory defense is in place — memory writes are validated against injection patterns; poisoned memories are quarantined.
> - Memory recall quality is measurable via standardized benchmarks; operators can validate quality thresholds before production deployment.
>
> #### Delivery (incremental)
>
> - **RHOAI 3.6 (Nov 2026)** — Standards & upstream foundation: MCP Memory Convention, upstream MLflow memory abstractions, A2A AgentCard memory binding. No product feature delivery.
> - **RHOAI 3.7 (~Q1-Q2 2027)** — Dev Preview of the governed memory substrate + governance layer + context engineering.
> - **RHOAI 3.8+ (directional)** — GA: audit trail, operator, observability, FIPS validation, adversarial memory defense, memory quality benchmarking; re-home onto the gateway-native Responses replacement. Continued feature additions in subsequent releases.
>
> #### Proposed child Features
>
> See the RFE roadmap. Child Features are sequenced to the incremental delivery plan above; they will be authored via the RFE pipeline after this Outcome rewrite is approved.

---

## 3. Note on the Proposed Child Features

RHAISTRAT-1345 currently has **no child Features** — Peter authors them after research ([seed doc](/features/agent-memory/research/agent-memory-landscape-research.md) §2). The Phase 2 [RFE roadmap](rfe-roadmap.md) outlines the proposed Features, sequenced to the 3.6 / 3.7 / 3.8+ delivery plan. In summary:

- **3.6-phase:** one standards/upstream Feature (MCP Memory Convention, MLflow memory abstractions, A2A AgentCard).
- **3.7-phase:** the core cluster — governed memory API, enterprise governance layer, context-engineering capability, MCP exposure + registry integration.
- **3.8+-phase (directional):** productization and research-driven Features — audit trail, operator, observability/FIPS, gateway-native re-home, client-side hybrid path, adversarial memory defense, memory quality benchmarking.

These are **outlines**, not filed Features. They are ready to feed `/rfe.create` once this Outcome rewrite is approved. A separate Outcome will be created for **Agent Knowledge** — it is not a child of RHAISTRAT-1345.

---

## 4. What Changed vs. the Current Ticket

| Current ticket ([seed doc](/features/agent-memory/research/agent-memory-landscape-research.md) §2) | Proposed rewrite | Basis |
|---|---|---|
| Title: "Agent Memory Primitives" | "Governed Agent Memory Substrate" — names the governance and the unified-substrate framing | REVIEW-NOTES D4 |
| Scope: "long-term knowledge persistence" (ambiguous) | Split: long-term *memory* persistence is in; org *knowledge* is explicitly out | REVIEW-NOTES D2 |
| "Short-term conversation state + long-term persistence" as two things | One substrate, four access patterns | REVIEW-NOTES D1/D4 |
| No governance language | Governance & Scope made a first-class scope item | REVIEW-NOTES D1 |
| No delivery phasing | Incremental 3.5 → 3.6 → 3.7+ delivery plan | REVIEW-NOTES D3/D5 |
| No deployment-model language | Server-side default + client-side hybrid path | REVIEW-NOTES D1 |
| Delivery: 3.5 → 3.6 → 3.7+ | Delivery: 3.6 → 3.7 → 3.8+. No 3.5 memory work; 3.6 = standards/upstream only; base solution targets 3.7 Dev Preview. Adversarial defense and benchmarking added as GA criteria from Phase 2 research. | Timeline direction (Peter Double + Sanjeev Rampal, 2026-06-09); Phase 2 research (docs 09–15) |

---

## 5. Sources

| Source | Used for |
|---|---|
| [REVIEW-NOTES.md](/features/agent-memory/research/REVIEW-NOTES.md) | D1–D5 — the decisions the rewrite reflects |
| [agent-memory-knowledge.md](/features/agent-memory/research/agent-memory-landscape-research.md) §2 | The current RHAISTRAT-1345 ticket text |
| [agent-memory-strategy.md](agent-memory-strategy.md) | Scope, roadmap, the audit-trail and scope-tier recommendations |
| [rfe-roadmap.md](rfe-roadmap.md) | The proposed child Features |
| [Phase 2 research (docs 09–15)](/features/agent-memory/research/) | Timeline shift context and scope-reshaping findings |
