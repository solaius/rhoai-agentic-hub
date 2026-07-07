---
title: Agent Memory — Strategy (Phase 2) Overview
description: Index of the Phase 2 strategy documents for RHAISTRAT-1345 and a note on how the strategy was derived from Phase 1 research and the review gate.
source: ai-asset-registry/agent-memory/strategy/README.md (as of 2026-07-05)
timestamp: 2026-07-06
review_after: 2026-08-05
---

# Agent Memory — Strategy (Phase 2)

**Purpose:** Index of the Phase 2 strategy documents for the RHAISTRAT-1345 Outcome, and a note on how the strategy was derived.

**Date:** 2026-06-09 (revised from 2026-05-18)

**Status:** PROPOSED — a PM strategy proposal for leadership review. Items marked DECIDED were settled at the Phase 1 review gate. Updated 2026-06-09 to reflect the 3.6→3.7→3.8+ phasing.

---

## The Documents

| # | Document | What it is |
|---|---|---|
| 01 | [agent-memory-strategy.md](agent-memory-strategy.md) | The core strategy — vision and whitespace, the accepted decomposition, the strategic approach, the **incremental roadmap** (3.6 → 3.7 → 3.8+), the standards workstream (now Phase 0 deliverable), recommendations on the two deferred questions, competitive positioning, risks and dependencies. |
| 02 | [use-cases-and-personas.md](use-cases-and-personas.md) | Who needs the memory substrate (the four RHOAI personas) and the concrete use cases driving scope, tied to roadmap phases. |
| 03 | [recommended-architecture.md](recommended-architecture.md) | High-level architecture — memory substrate + enterprise governance layer + context-engineering capability, RHOAI/OCP integration, deployment model. |
| 04 | [rhaistrat-1345-outcome-update.md](rhaistrat-1345-outcome-update.md) | A proposed paste-ready rewrite of the RHAISTRAT-1345 Outcome. No Jira write. |
| 05 | [rfe-roadmap.md](rfe-roadmap.md) | Outlined RFE breakdown (RFE-M1…M11), sequenced to the roadmap. Includes M10 (adversarial defense) and M11 (benchmarking) from Phase 2 research. Outlines only — not filed. |

**Start with [01 — the core strategy](agent-memory-strategy.md).**

---

## How This Strategy Was Derived

This strategy is **built on the Phase 1 research and the review gate** — it does not re-derive the research's conclusions.

1. **Phase 1 research** (`../research/`, docs 00–08) surveyed the agent-memory landscape, evaluated candidate internal assets and external solutions, analyzed technical patterns and standards, proposed a decomposition (doc 07), and proposed a sourcing direction (doc 08). All Phase 1 recommendations were marked PROPOSED.

1a. **Phase 2 research** (`../research/`, docs 09–15) extended the research with harness memory, adversarial memory, benchmarking, KV-cache optimization, enterprise use cases, and multi-modal memory. Key findings reshape the strategy: adversarial defense and benchmarking become GA acceptance criteria; KV-cache optimization provides research backing for context engineering.

1b. **Platform transition context** (2026-06-10) — the upstream community project currently serving memory primitives is transitioning to gateway-native architecture. The strategy adopts a substrate-agnostic posture: the architecture orients toward the AI Gateway while maintaining delivery-vehicle agnosticism. See [REVIEW-NOTES — Platform Transition Context](/features/agent-memory/research/REVIEW-NOTES.md#ogx-deprecation-context-2026-06-10) and [research 16](/features/agent-memory/research/16-ai-gateway-memory-substrate.md).

2. **The review gate** ([../research/REVIEW-NOTES.md](/features/agent-memory/research/REVIEW-NOTES.md)) accepted the research and made six decisions (D1–D6) selecting among the options the research laid out, deferred two questions to this strategy phase (audit-trail sequencing, the scope-tier model), and named the open cross-team items. **REVIEW-NOTES.md is the contract this strategy conforms to.**

3. **This Phase 2 strategy** turns the review-gate decisions into a release-paced plan:
   - The scope is the **Agent Memory Substrate + Context Engineering** (REVIEW-NOTES D2). **Agent Knowledge is out of scope** — a separate Outcome / separate run — and appears here only as a deferred pointer ([strategy §2.1](agent-memory-strategy.md#21-agent-knowledge--deferred-pointer-only)).
   - The centerpiece is an **incremental roadmap** — RHOAI 3.6 (Nov 2026, standards & upstream foundation) → 3.7 (~Q1-Q2 2027, governed-substrate Dev Preview) → 3.8+ (directional, GA + continued features) — sized to what the org can absorb (REVIEW-NOTES D3/D5). No memory deliverable is targeted for RHOAI 3.5. Timeline set by Peter Double + Sanjeev Rampal (2026-06-09).
   - The two deferred questions are answered with rationale: the **audit trail** is a GA gate (not a 3.6 Dev-Preview gate) with a minimum write-event log at Dev Preview; the **scope-tier model** ships four OpenShift-native tiers (`user`/`project`/`role`/`org`) for the MVP — the tiers with no OpenShift analogue (`campaign`, `organizational`, `enterprise`) are deferred as a design horizon ([strategy §6](agent-memory-strategy.md#6-recommendations-on-the-two-deferred-questions)).
   - The standards workstream runs in parallel from the start (REVIEW-NOTES D6).
   - Open cross-team items (Q-G2/G3/G4/G5/G6, Q-T4, Q-MH-1, Q-G8) are named as required follow-ups, not answered ([strategy §8](agent-memory-strategy.md#8-risks-and-dependencies)).

Every claim in the strategy documents traces to a Phase 1 research doc or a REVIEW-NOTES decision; status markers (PROPOSED / DECIDED / DIRECTIONAL) distinguish PM proposals from review-gate-settled facts from beyond-3.7 direction.

---

## Status Convention

- **DECIDED** — settled at the Phase 1 review gate (REVIEW-NOTES D1–D6). Stated as fact.
- **PROPOSED** — this strategy's recommendation, for leadership review.
- **DIRECTIONAL** — beyond RHOAI 3.7; indicative, not a commitment. RHOAI 3.6 = November 2026 is given; 3.7 (~Q1-Q2 2027) is the base-solution target; 3.8+ contents are not established.
