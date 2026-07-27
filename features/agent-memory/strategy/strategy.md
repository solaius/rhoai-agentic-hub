---
title: "Agent Memory — strategy"
description: Living strategy for RHAISTRAT-1345 — governed agent memory substrate, "alongside harness not instead of" positioning, three-phase roadmap (3.6 DP → 3.7 TP → 3.8 GA), fourteen filed RFEs, sandbox-integrated memory governance as differentiation frontier.
timestamp: 2026-07-27
status: current
review_after: 2026-09-27
source: hub.strategy — synthesized from research 00-21 (22-doc series), strategy/agent-memory-strategy.md (pre-convention), knowledge entries, Adel positioning doc, roadmap + strategy profiles
---

## The brief

Agent memory is a funded, contested platform layer — ~$62M in startup
investment, GA features at every hyperscaler, and no solution combining
enterprise governance + Kubernetes-native self-hosted + air-gappable +
open standard interface. That whitespace has narrowed (Google shipped
versioning, Zep earned SOC 2) but not closed. The bet: a governed,
portable, self-hosted memory substrate that runs **alongside** harness-native
memory, not instead of it — "your harness handles memory for one session
on one machine; the platform handles memory for your fleet, your team,
and your compliance requirements." Three phases: 3.6 DP (standards +
upstream), 3.7 TP (governed substrate + governance layer), 3.8+ GA.
Fourteen RFEs filed under RHAISTRAT-1345. Next milestone: 3.6 EA2
standards deliverables.

## What

### Product shape by release train

| Release | Scope | Status |
|---|---|---|
| 3.5 (current) | No memory deliverable; OGX memory primitives ride passively in Responses bridge | Shipping |
| 3.6 DP (Nov 2026) | Standards & upstream foundation (MCP Memory Convention, MLflow memory, A2A AgentCard binding); architecture validated | PROPOSED — 6 RFEs filed (RHAIRFE-2630..2635) |
| 3.7 TP (~Q1-Q2 2027) | Governed memory substrate + enterprise governance layer + context engineering — all Dev Preview | PROPOSED — 8 RFEs filed (RHAIRFE-2636..2643) |
| 3.8+ GA (directional) | Audit trail, operator, observability, FIPS, adversarial defense, benchmarking, gateway re-home, client-side hybrid | DIRECTIONAL — RFEs unfiled |

### Boundaries

| This feature IS | This feature is NOT |
|---|---|
| Subsystem 1 (Agent Memory Substrate) + Context Engineering as a capability | Agent Knowledge (Subsystem 3) — enterprise-RAG-shaped, separate Outcome |
| A governed platform service alongside harness memory | A replacement for MEMORY.md, .cursorrules, or harness-native memory |
| Server-side default with client-side hybrid path | Client-side only |
| RHAISTRAT-1345 scope | Skills registry, agent registry, or MCP catalog work |

Related siblings: none declared in features.yaml. Cross-references:
agent-interop (OpenShell sandbox integration for memory lifecycle
hooks), platform (AI Gateway, AI Hub surfaces).

## Why

### The problem

Every harness manages memory as local files on one machine. This breaks
in three places enterprises care about: **no governance** (no versioning,
no audit, no rollback — stale memories compound errors per Databricks),
**no sharing** (each agent's knowledge is siloed — Itaú built shared
memory across agents because silos blocked their 4M sessions/month
platform), **no durability** (switch laptops, switch harnesses, run in a
sandbox — memory is gone).

### The bet

A governed, portable, self-hosted memory substrate that:
1. **Runs alongside harness memory** — both systems operate during a
   session; the harness writes to its native store, the model calls
   `memorize` on the platform; redundancy is harmless, the platform
   deduplicates
   ([fact-adel-positioning-alongside-harness](/features/agent-memory/knowledge/fact-adel-positioning-alongside-harness.md))
2. **Fills the governance gap no harness fills** — versioning, rollback,
   audit trail, scope isolation, poisoning defense
3. **Breaks the cloud lock-in vector** — memory portability as a platform
   primitive; open storage format, export/import APIs, no proprietary
   extraction format

### Market position

The whitespace has **narrowed but not closed**
([research 21](/features/agent-memory/research/21-competitive-landscape-2026-07.md) §3.1):
- Google shipped Memory Revisions (versioning, preview) — cloud-only, no
  rollback
- AWS shipped strictly consistent metadata (deterministic non-LLM keys)
  — cloud-only
- Microsoft shipped procedural memory (first hyperscaler) + MemoryGuard
  (guidance, not product) — cloud-only, preview
- Zep earned SOC 2 + HIPAA + GDPR — cloud-only certified platform
- **Nobody** ships rollback, per-memory audit trails, sandbox-aware write
  governance, or self-hosted + governed + air-gappable

Governance is now a ladder, not binary
([research 21](/features/agent-memory/research/21-competitive-landscape-2026-07.md) §3.3).
Access controls are table stakes. Versioning is emerging (Google only).
Rollback, audit, retention/erasure, trust-aware retrieval, and
sandbox-aware governance remain unserved. RHOAI's opportunity: define
the full ladder and ship the top rungs first.

### Why now

- 88% of agent pilots fail to graduate to production (Forrester/Anaconda
  2026) — governance and reliability are the top blockers
- EU AI Act GPAI enforcement 2026-08-02; Annex III high-risk deferral
  provisionally to 2027-12-02 (adoption pending)
- Sandbox adoption accelerating (OpenShell, Agent Sandbox k-sigs, Google
  Agent Substrate) — harness memory dies with the sandbox
- Memory is the new lock-in vector — hyperscalers lock memory to their
  cloud; switching costs compound with every interaction

## Where we stand

### Decisions to date

| Date | Decision | Source |
|---|---|---|
| 2026-05-17 | Decomposition: 3 subsystems + 2 cross-cutting dimensions (D1) | [REVIEW-NOTES](/features/agent-memory/research/REVIEW-NOTES.md) |
| 2026-05-17 | RHAISTRAT-1345 scoped to Substrate + Context Eng; Knowledge deferred (D2) | [REVIEW-NOTES](/features/agent-memory/research/REVIEW-NOTES.md) |
| 2026-05-17 | Phased sourcing: OGX substrate + MemoryHub governance + build-fresh for Knowledge (D3/D5) | [REVIEW-NOTES](/features/agent-memory/research/REVIEW-NOTES.md) |
| 2026-05-17 | Standards workstream runs in parallel from day one (D6) | [REVIEW-NOTES](/features/agent-memory/research/REVIEW-NOTES.md) |
| 2026-06-30 | Standalone service (decoupled from OGX AND AI Gateway) | [fact-1on1](/features/agent-memory/knowledge/fact-agent-memory-1on1-paths-forward-20260630.md) |
| 2026-06-30 | Phasing: 3.6 DP → 3.7 TP → 3.8 GA | [fact-1on1](/features/agent-memory/knowledge/fact-agent-memory-1on1-paths-forward-20260630.md) |
| 2026-07-07 | Feast ruled out as interim memory; OGX memory tool + MemoryHub pair | [fact-sync-0707](/features/agent-memory/knowledge/fact-agent-memory-team-sync-20260707-transcript.md) |
| 2026-07-10 | Fourteen RFEs filed (RHAIRFE-2630..2643) | [fact-rfes-filed](/features/agent-memory/knowledge/fact-rhaistrat-1345-rfes-filed-20260710.md) |

### Delivery state

- **Research**: 22-doc series complete (Phase 1 DECIDED, Phase 2
  EXPLORATORY, 3 refreshes including competitive lens)
- **Strategy**: this document (conventions-format); pre-convention
  strategy docs in strategy/ for reference
- **RFEs**: 14 filed — 6 targeting 3.6 EA2, 8 targeting 3.7 (no version
  until 3.7 exists in Jira). 3.8 GA wave unfiled.
- **Workstream**: opendatahub-io/agent-memory repo, evaluation-criteria
  PR, team meeting cadence established
- **Positioning**: Adel Zaalouk's positioning musings ingested
  ([ref](/features/agent-memory/knowledge/ref-adel-agent-memory-positioning-musings.md))
  — "alongside harness" stance adopted as framing

### In-flight

- Standards workstream: MCP Memory Convention SEP, MLflow memory
  abstractions, A2A AgentCard memory binding (Phase 0 / 3.6)
- MemoryHub IP transfer: Wes is willing; formal transfer required before
  productization (Q-MH-1)
- Engineering sponsor: needed for the work to land — Adel connecting
  Peter with counterparts

## Gaps & risks

### Open questions (from research series)

| Question | Why it matters | Status |
|---|---|---|
| Q-G7 — Audit-trail delivery plan | Neither candidate ships a working audit trail; GPAI enforcement 2026-08-02 | Highest severity; minimum write-event log at DP, full trail at GA |
| Q-G2 — OGX replacement plan | Does the gateway reimpl memory primitives or delegate? Boundary moves | Directionally answered (AI Gateway is replacement) |
| Q-G5 — Actor-chain RBAC | Privilege-escalation risk in shared memory | Design-time |
| Q-G6 — Platform identity vs standalone auth | MemoryHub's OAuth 2.1 vs RHOAI SPIFFE/Authbridge | Cross-team integration |
| Q-MH-1 — MemoryHub IP transfer | Copyright held by individual; CLA needed | Administrative prerequisite |
| Q-T3 — Scope-tier count | Six tiers vs four OpenShift-native tiers for MVP | Recommendation: four for MVP ([strategy §6.2](/features/agent-memory/strategy/agent-memory-strategy.md#62-scope-tier-model--recommendation-ship-four-openshift-native-tiers-for-the-mvp-keep-the-remaining-tiers-as-a-design-horizon)) |

### Competitive risks

| Risk | If it fires → what changes |
|---|---|
| Google ships Memory Revisions GA + rollback | Closes the versioning gap; RHOAI must ship rollback at DP, not GA |
| Microsoft ships MemoryGuard as a product feature | Closes the poisoning-defense gap; accelerates RFE-M10 (adversarial defense) |
| Zep ships SOC 2 for self-hosted Graphiti | Closes the governance+self-hosted gap for the OSS camp; RHOAI loses the "only governed self-hosted" claim |
| A memory standard emerges from AAIF | Phase 0 standards work must track/align; proprietary API risk if we miss it |
| Cognee matures governance + earns certifications | Strongest RHOAI-aligned OSS option becomes a credible alternative |

### Tensions

- **Org priority**: agent memory is not on leadership's 12-month list ("a
  2027 topic"); scoped RFEs are the response, but engineering sponsorship
  is the bottleneck
- **Procedural memory**: Microsoft shipped it; our RFE roadmap defers it
  to 3.8+ (DIRECTIONAL). If customer demand surfaces, it pulls forward
  — but procedural memory carries the highest poisoning risk
  ([research 21](/features/agent-memory/research/21-competitive-landscape-2026-07.md) §3.4)
- **Benchmark reliability weakening**: vendor-claimed benchmarks
  proliferating; only Zep's arXiv result is peer-reviewed. Benchmark
  wars becoming marketing, not engineering signals
  ([research 21](/features/agent-memory/research/21-competitive-landscape-2026-07.md) §5)

## Jira map

### Coverage table

| Strategy element | Key(s) | Status |
|---|---|---|
| Outcome | RHAISTRAT-1345 | New (rewritten 2026-07-10) |
| Framework-agnostic memory API | RHAIRFE-2630 | Filed, 3.6 EA2 target |
| Memory as governed MCP tools | RHAIRFE-2631 | Filed, 3.6 EA2 target |
| Built-in memory in AI Hub (interim DP) | RHAIRFE-2632 | Filed, 3.6 EA2 target |
| Record-level scope isolation | RHAIRFE-2633 | Filed, 3.6 EA2 target |
| Sensitive-data screening on write path | RHAIRFE-2634 | Filed, 3.6 EA2 target |
| Write auditability | RHAIRFE-2635 | Filed, 3.6 EA2 target |
| Auto memory creation & curation | RHAIRFE-2636 | Filed, 3.7 candidate |
| Org-wide shared memory: tiers + conflict | RHAIRFE-2637 | Filed, 3.7 candidate |
| Inspectable context engineering | RHAIRFE-2638 | Filed, 3.7 candidate |
| Memory as governed AI Asset Registry asset | RHAIRFE-2639 | Filed, 3.7 candidate |
| Memory visibility in Gen AI Studio | RHAIRFE-2640 | Filed, 3.7 candidate |
| Memory governance console in AI Hub | RHAIRFE-2641 | Filed, 3.7 candidate |
| Harness/framework integration packs | RHAIRFE-2642 | Filed, 3.7 candidate |
| Memory effectiveness on smaller models | RHAIRFE-2643 | Filed, 3.7 candidate |
| Full audit trail + erasure (3.8 GA) | — | **Unfiled** |
| Operator + observability (3.8 GA) | — | **Unfiled** |
| Adversarial memory defense (3.8 GA) | — | **Unfiled** |
| Memory benchmarking (3.8 GA) | — | **Unfiled** |

### Candidate jiras (new — from competitive lens)

| Gap | Problem statement | Suggested project |
|---|---|---|
| Sandbox-integrated memory governance | No platform distinguishes memory writes by execution context; sandbox-generated memories carry different trust than supervised sessions; OpenShell integration creates a first-mover opportunity | RHAIRFE — child of RHAISTRAT-1345 |
| Memory portability (export/import) | No standard memory format exists; hyperscaler lock-in compounds with every interaction; enterprises need export/import to avoid switching costs | RHAIRFE — child of RHAISTRAT-1345 |
| Procedural memory with governance | Microsoft shipped learned execution patterns; the capability is high-value but highest-risk for poisoning; RHOAI should ship it with the strongest write-path governance | RHAIRFE — child of RHAISTRAT-1345, 3.8+ |

## Watchlist

| Date / trigger | What | If it fires → what changes |
|---|---|---|
| 2026-08-02 | EU AI Act GPAI enforcement | Audit-trail pressure becomes regulatory, not just customer-driven |
| 2026-07-28 | MCP spec largest revision (statelessness) | Memory-as-MCP session identity must live in the memory service, not the protocol ([research 19](/features/agent-memory/research/19-market-direction-refresh-2026-07.md) §4) |
| Q3-Q4 2026 | Google Memory Revisions GA decision | If GA + rollback, RHOAI must match at DP |
| Q3-Q4 2026 | Microsoft Foundry Memory GA | If GA, the "preview" qualifier in our competitive positioning disappears |
| Q3-Q4 2026 | AAIF memory working group formation | Phase 0 standards work must engage; opportunity to shape vs. follow |
| Ongoing | Anthropic Dreaming expands beyond research preview | Validates async consolidation as production-grade; aligns with RFE-M4 pattern |
| Ongoing | Mem0 Series B / acquisition | Consolidation risk (finding 5); if acquired by a hyperscaler, OSS tier may degrade |

## History

- 2026-07-27 — **Creation** — first hub-convention strategy.md for
  agent-memory. Synthesized from: pre-convention strategy docs
  (strategy/agent-memory-strategy.md, 5 docs), research series (22
  docs, including competitive lens doc 21), 14 filed RFEs, Adel
  positioning doc, roadmap + strategy profiles. New elements vs
  pre-convention docs: sandbox-integrated memory governance as unserved
  gap (doc 21 §3.5), governance ladder framing (doc 21 §3.3),
  lock-in vector positioning (Adel), "alongside harness" stance (Adel),
  procedural memory frontier (doc 21 §3.4), 3 candidate jiras from
  competitive lens.
