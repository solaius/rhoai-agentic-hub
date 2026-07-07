---
title: Agent Memory — Recommended Architecture
description: High-level architecture for the RHOAI agent memory substrate -- substrate, governance layer, context-engineering capability, RHOAI/OCP integration, deployment model.
source: ai-asset-registry/agent-memory/strategy/recommended-architecture.md (as of 2026-07-05)
timestamp: 2026-07-06
review_after: 2026-08-05
---

# Agent Memory — Recommended Architecture

**Purpose:** A high-level architecture for the RHOAI agent memory substrate — the substrate, the governance layer, the context-engineering capability, how it slots into RHOAI/OCP, and the deployment model. Strategy-level, not detailed design.

**Date:** 2026-06-09 (revised from 2026-05-18)

**Author:** Peter Double (Principal PM — MCP & AI Asset Registries)

**Status:** PROPOSED — a PM strategy proposal for leadership and architecture review. The memory-primitives-as-substrate / governance-prototype-as-governance-layer pairing is DECIDED at the review gate (REVIEW-NOTES D5); the integration details below are PROPOSED, traced to [research 08](/features/agent-memory/research/08-rhoai-ocp-alignment.md). Several integration points carry open cross-team questions, flagged inline. Updated 2026-06-09 to reflect the 3.6→3.7→3.8+ phasing and Phase 2 research integration.

**Strategy series:** [README](strategy-overview.md) · [Strategy](agent-memory-strategy.md) · [Use Cases & Personas](use-cases-and-personas.md) · Architecture (this doc) · [Outcome Update](rhaistrat-1345-outcome-update.md) · [RFE Roadmap](rfe-roadmap.md)

---

## 1. Scope of This Document

This is a *strategy-level* architecture — enough to show the shape, the component boundaries, and the RHOAI integration points so leadership can assess feasibility. It is not a design spec; the detailed API surface, schema, and operator design are deferred to the RFE/design phase. It covers **Subsystem 1 (Agent Memory Substrate) + Context Engineering** only — Agent Knowledge architecture is deferred (see §6).

---

## 2. The Three Architectural Pieces

The architecture has three pieces, matching the in-scope decomposition (REVIEW-NOTES D1):

```
                  ┌──────────────────────────────────────────────┐
                  │  ENTERPRISE GOVERNANCE LAYER                   │
                  │  scope tiers (user/project/role/org) · RBAC ·  │
                  │  curation · contradiction detection ·         │
                  │  provenance · audit (write-log → full at GA)  │
                  └──────────────────────────────────────────────┘
                                governs ↓
   ┌──────────────────────────────┐   ┌──────────────────────────────┐
   │  MEMORY SUBSTRATE            │   │  CONTEXT ENGINEERING          │
   │  working · episodic ·        │◀──│  (capability layer over the   │
   │  semantic · procedural       │   │   substrate)                  │
   │  4 CoALA access patterns,    │   │  inspectable compaction ·     │
   │  one PostgreSQL+pgvector     │   │  retrieval assembly ·         │
   │  store                       │   │  progressive disclosure ·     │
   │                              │   │  KV-cache-aware ordering      │
   └──────────────────────────────┘   └──────────────────────────────┘
            append-heavy datastore           operates on the substrate
```

### 2.1 The Memory Substrate

**One governed store exposing the four CoALA access patterns** — working, episodic, semantic, procedural — not four systems ([research 07](/features/agent-memory/research/07-taxonomy-and-decomposition.md) §4.1; REVIEW-NOTES D4). It is append-heavy and agent-written.

- **Foundation:** The memory primitives — Conversations API (episodic/working), Vector Stores + Files (semantic), Prompts API (procedural), `previous_response_id` chaining — already ship internally ([research 06](/features/agent-memory/research/06-ogx-memory-primitives.md); [research 16](/features/agent-memory/research/16-ai-gateway-memory-substrate.md)). The memory API surface is substrate-agnostic — it works regardless of delivery vehicle. Identity and scope isolation are provided by the AI Gateway's Authorino-based model (header injection → row-level scoping). The memory strategy builds on these primitives starting in Phase 1 (RHOAI 3.7).
- **Storage:** PostgreSQL + pgvector — relational, vector, and (where validated) graph queries in one engine. The OpenShift-native path is the out-of-the-box PostgreSQL operator ([research 08](/features/agent-memory/research/08-rhoai-ocp-alignment.md) §2.7). One substrate minimizes FIPS surface and operational sprawl, valid up to an estimated ~50M-vector threshold (practitioner estimate, not an RHOAI measurement — see Q-G4); the empirical workload profile (Q-G4) confirms whether RHOAI stays under it.
- **Interface:** a framework-agnostic, substrate-agnostic memory API, exposed over MCP so it routes through the MCP Gateway for per-tool authz and audit ([research 08](/features/agent-memory/research/08-rhoai-ocp-alignment.md) §2.4).

### 2.2 The Enterprise Governance Layer

The Governance & Scope cross-cutting dimension, made concrete — exactly the enterprise-governance dimension the memory primitives lack on their own ([research 08](/features/agent-memory/research/08-rhoai-ocp-alignment.md) §2.3):

- **Scope tiers:** `user` / `project` / `role` / `org` for the MVP — four OpenShift-native tiers, modeled as an extensible enumeration so the remaining tiers (`campaign`, `organizational`, `enterprise`) can be added later without an API break (per [strategy §6.2](agent-memory-strategy.md#62-scope-tier-model--recommendation-ship-four-openshift-native-tiers-for-the-mvp-keep-the-remaining-tiers-as-a-design-horizon)).
- **RBAC:** the substrate enforces its own row-level scope RBAC internally — the gateway establishes identity, the memory service authorizes ([research 08](/features/agent-memory/research/08-rhoai-ocp-alignment.md) §2.4). Actor-chain lowest-permission enforcement for shared memory is an open cross-team item (Q-G5).
- **Curation & contradiction detection:** PII/secrets scanning on memory writes; contradictory memories flagged ([research 03](/features/agent-memory/research/03-memoryhub-deep-dive.md)).
- **Provenance:** every memory record carries identity, version, owner, source, lineage — paralleling the AI Asset Registry metadata model.
- **Audit:** a minimum write-event log at 3.6 Dev Preview; a full inspectable, append-only audit trail (reads and writes) is a GA gate ([strategy §6.1](agent-memory-strategy.md#61-audit-trail-sequencing--recommendation-ga-gate-with-a-dev-preview-disclosure-obligation)).

### 2.3 Context Engineering (capability over the substrate)

A capability layer tightly coupled to the substrate, not an independent peer ([research 07](/features/agent-memory/research/07-taxonomy-and-decomposition.md) §4.1):

- **Inspectable compaction** — human-readable summaries, not opaque tokens, so compaction is compliance-inspectable ([research 00](/features/agent-memory/research/00-executive-summary.md) §3 finding 10). Built on existing compaction primitives (`/responses/compact` and `context_management`).
- **Retrieval assembly, progressive disclosure, KV-cache-aware ordering** — assembling the right context into the window, tiered loading (lean first, deeper on demand), deterministic ordering for KV-cache prefix hits. KV-cache-aware ordering is now backed by Phase 2 research ([research 13](/features/agent-memory/research/13-kv-cache-optimization.md)) demonstrating measurable latency and cost improvements from deterministic token ordering.
- It keeps its own quality metric — token efficiency at a quality threshold — so it remains tracked and measurable, but it does not warrant a separate Outcome.

---

## 3. How It Slots Into RHOAI / OCP

The substrate is not a standalone product; it is a governed workload inside the RHOAI/OCP stack. The integration points ([research 08](/features/agent-memory/research/08-rhoai-ocp-alignment.md) §2–3):

| RHOAI/OCP component | Role for the memory substrate |
|---|---|
| **Memory primitives** | The substrate's foundation — working/episodic/semantic/procedural primitives + compaction. Already shipping internally; transitioning to gateway-routed microservice architecture ([research 16](/features/agent-memory/research/16-ai-gateway-memory-substrate.md)). *Q-G2 directionally answered — AI Gateway is the delivery vehicle.* |
| **AI Gateway (IPP)** | Identity-establishment point. The gateway-native architecture hosts the substrate's working/episodic slice as a "conversation state microservice." The gateway establishes identity; the memory service authorizes. |
| **MCP Gateway** | Enforcement point for memory exposed via MCP — per-tool authz (Authorino/RHCL), per-tool metrics, audit logging, content guardrails on memory writes. |
| **kagenti** | Agent runtime — where memory is *consumed*. kagenti injects SPIFFE identity into agent workloads; that identity is the substrate's RBAC principal. The AgentCard carries the agent→memory binding. |
| **MLflow / AI Asset Registry** | Registers the memory *service* as a governed asset (identity, version, endpoint, policy linkage, lifecycle) — the same two-tier model as an MCP Server. MLflow does **not** store memory records. *Open: Q-G3 — whether individual records are also registry-governed.* |
| **Identity (Spire/Authbridge/OPA)** | The substrate consumes RHOAI platform identity via RFC 8693 token exchange — recommendation is to drop the governance prototype's standalone OAuth server in favor of platform identity (Q-G6). Actor-chain lowest-permission rule applies to shared memory (Q-G5). |
| **vLLM on RHOAI** | Serves the embedding model and cross-encoder reranker the substrate depends on — on-cluster, air-gap-compatible. |
| **Guardrails / IPP plugins** | PII / prompt-injection scanning on the memory write path — defense-in-depth. |

**The "Registry = Governance" boundary.** Memory is the first AI asset type that is *itself* a live, append-heavy datastore rather than a metadata record pointing at one ([research 00](/features/agent-memory/research/00-executive-summary.md) §3 finding 12). The resolution: the AI Asset Registry governs the memory *service* as an asset and governs records with the same metadata model — it does **not** become a memory store. The registry holds metadata and policy linkage; the substrate enforces its own row-level RBAC ([research 08](/features/agent-memory/research/08-rhoai-ocp-alignment.md) §2.1).

---

## 4. Deployment Model

**Server-side is the default; a client-side hybrid path is the secondary mode** — the Deployment cross-cutting dimension ([research 07](/features/agent-memory/research/07-taxonomy-and-decomposition.md) §4.1; REVIEW-NOTES D1).

- **Server-side (default).** The substrate runs as a governed OpenShift workload — UBI9 images, FIPS delegated to cluster OpenSSL, air-gap deployable, on-cluster vLLM embeddings, OLM-managed operator (at GA). This is the platform-tier model: multi-agent coordination, governance, multi-tenancy. It serves the AI Engineer / Platform Engineer / AgentOps personas and the regulated-production use cases (UC-5/6/7).
- **Client-side (hybrid path).** IDE and dev-workflow agents — the "harness tier" — use a client-side memory path with hybrid search ([seed doc](/features/agent-memory/research/agent-memory-landscape-research.md) §6; Francisco Arceo's RHAISTRAT-1345 comment). This is directional, **Phase 2 (3.8+)**; the server-side substrate ships first in Phase 1 (3.7). Phase 2 research on harness memory patterns ([research 09](/features/agent-memory/research/09-agent-harness-memory.md)) informs the client-side design.

The two are not separate products — they are two deployment modes of one governed memory abstraction, so an agent's memory remains portable between them.

---

## 5. Architecture by Roadmap Phase

| Phase | What exists architecturally |
|---|---|
| **0 — 3.6 (Nov 2026)** | Standards & upstream foundation — MCP Memory Convention SEP, upstream MLflow memory abstractions, A2A AgentCard memory binding. Architecture validated against upstream consensus. No deployed substrate. |
| **1 — 3.7 (~Q1-Q2 2027)** | Governed substrate (substrate workstream) + enterprise governance layer (governance workstream) + context-engineering capability — all Dev Preview. Four scope tiers (`user`/`project`/`role`/`org`); minimum write-event log; MCP-exposed; registered as a governed asset. KV-cache-aware ordering backed by Phase 2 research. |
| **2 — 3.8+ (directional)** | Full audit trail, OLM operator, observability, FIPS validation, adversarial memory defense, memory quality benchmarking; substrate re-homed onto gateway-native architecture; client-side hybrid path informed by harness memory research. |

---

## 6. Agent Knowledge — Architecture Deferred

The architecture of **Agent Knowledge (Subsystem 3)** — the org-wide enterprise-RAG / knowledge-graph layer — is **not covered here**. It is a different data architecture (batch-indexed, read-mostly, document-provenance, potentially a dedicated store at 50–100M+ entities) and a separate Outcome / separate run (REVIEW-NOTES D2; [strategy §2.1](agent-memory-strategy.md#21-agent-knowledge--deferred-pointer-only)). The research position to carry forward: it should extend the AI Asset Registry **Knowledge Sources** asset type, and it should **not** share a storage engine with the memory substrate even though it shares a governance model ([research 08](/features/agent-memory/research/08-rhoai-ocp-alignment.md) §2.7, §5). That is the extent of the Agent Knowledge note.

---

## 7. Sources

| Source | Used for |
|---|---|
| [REVIEW-NOTES.md](/features/agent-memory/research/REVIEW-NOTES.md) | D1/D4/D5 — decomposition, substrate verdict, substrate + governance pairing |
| [research 08](/features/agent-memory/research/08-rhoai-ocp-alignment.md) | RHOAI/OCP component mapping, integration points, the Q-G* open items |
| [research 07](/features/agent-memory/research/07-taxonomy-and-decomposition.md) | The three-piece decomposition; context engineering as a capability layer |
| [research 06](/features/agent-memory/research/06-ogx-memory-primitives.md) | Internal memory primitives and gaps |
| [research 03](/features/agent-memory/research/03-memoryhub-deep-dive.md) | Governance model, curation, contradiction detection |
| [research 00](/features/agent-memory/research/00-executive-summary.md) | The payload-vs-metadata boundary; inspectable compaction |
| [seed doc](/features/agent-memory/research/agent-memory-landscape-research.md) | Client/server-side deployment fork |
| [agent-memory-strategy.md](agent-memory-strategy.md) | Roadmap phases, the two deferred-question recommendations |
