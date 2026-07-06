---
title: Agent memory — landscape research, benchmarks, and Feast's strategic options
description: Deep-research extraction on the agent-memory competitive landscape (Mem0, Zep, OpenViking, Letta, Feast), published benchmarks, protocol standards, and Feast's four strategic options for agentic positioning — background research behind the Feast + OGX proposal, not an approved design.
source: ai-asset-registry/docs/knowledge-review/assets/agent-memory-knowledge.md (as of 2026-07-05)
timestamp: 2026-07-06
review_after: 2026-08-05
---

> **Status**: Background research, not an approved design. Nothing here is scoped or decided — it's the research base several PROPOSAL-stage documents (Feast + OGX, "Feast in the Agentic AI Era") drew on. The RHAISTRAT-1345 outcome this feeds has no child Features yet; see [ref-rhaistrat-1345-outcome.md](/features/agent-memory/knowledge/ref-rhaistrat-1345-outcome.md).

## Why this document exists

This is the extracted research base behind two proposal documents already in the knowledge store — [ref-feast-in-agentic-ai-era.md](/features/agent-memory/knowledge/ref-feast-in-agentic-ai-era.md) and [ref-feast-ogx-agent-memory-proposal.md](/features/agent-memory/knowledge/ref-feast-ogx-agent-memory-proposal.md) — plus cross-source observations spanning MemoryHub, Oracle, Meta, and Wes Jackson's platform-concern argument. Those source documents and their competitive positions are each already captured as their own knowledge entries (see the Quick Map below); this document holds the sourced tables, benchmarks, and analysis too dense for a short reference entry, per the hub's "link out, don't copy in" rule for `knowledge/` entries.

## Quick map to existing knowledge entries

Rather than re-summarizing what's already indexed, here's where each source's short form lives:

- **RHAISTRAT-1345** (the internal Jira Outcome) → [ref-rhaistrat-1345-outcome.md](/features/agent-memory/knowledge/ref-rhaistrat-1345-outcome.md); scope-expansion question → [question-rhaistrat-1345-scope-expansion.md](/features/agent-memory/knowledge/question-rhaistrat-1345-scope-expansion.md)
- **MemoryHub** (Red Hat AI Americas prototype) → [ref-memory-hub-repo.md](/features/agent-memory/knowledge/ref-memory-hub-repo.md)
- **Oracle AI Agent Memory** (competitive blog) → [ref-oracle-ai-agent-memory-blog.md](/features/agent-memory/knowledge/ref-oracle-ai-agent-memory-blog.md) (now includes benchmark numbers)
- **Meta's "AI Second Brain"** (org-scale case study) → [ref-meta-ai-second-brain-blog.md](/features/agent-memory/knowledge/ref-meta-ai-second-brain-blog.md)
- **Wes Jackson, "When Agent Memory Becomes a Platform Concern"** → [ref-wes-jackson-agent-memory-platform-blog.md](/features/agent-memory/knowledge/ref-wes-jackson-agent-memory-platform-blog.md)
- **Feast + OGX Agent Memory: Proposal** (Zarecki) → [ref-feast-ogx-agent-memory-proposal.md](/features/agent-memory/knowledge/ref-feast-ogx-agent-memory-proposal.md) (now includes the MemoryFeatureView/L0-L1-L2 model and the three-deltas table)
- **OGX Memory Alpha Architecture** (Francisco Arceo) → [ref-ogx-memory-alpha-architecture.md](/features/agent-memory/knowledge/ref-ogx-memory-alpha-architecture.md)
- **Agent Memory Team Sync, 2026-06-23** → [fact-agent-memory-team-sync-20260623-transcript.md](/features/agent-memory/knowledge/fact-agent-memory-team-sync-20260623-transcript.md)
- **"Data guardrails" positioning** → [fact-data-guardrails-positioning.md](/features/agent-memory/knowledge/fact-data-guardrails-positioning.md)
- **Protocol standardization gap** → [question-agent-memory-protocol-standardization.md](/features/agent-memory/knowledge/question-agent-memory-protocol-standardization.md)

What follows is the research this document adds beyond those entries: the competitive framework landscape, published benchmarks, protocol-standards survey, Feast's four strategic options, experimentation results, and the cross-source synthesis.

## Agent memory framework landscape (verified April 2026)

From "Feast in the Agentic AI Era" (Aniket Paluskar, research Apr 28 2026; Jonathan Zarecki, PM position May 15 2026) — see [ref-feast-in-agentic-ai-era.md](/features/agent-memory/knowledge/ref-feast-in-agentic-ai-era.md) for the source doc.

| Framework | GitHub stars | Architecture | License | Funding | Status |
|---|---|---|---|---|---|
| Mem0 | 54,299 | Hybrid: vector + graph + KV store | Apache 2.0 (OSS); graph behind $249/mo paywall | $24M ($20M Series A + $3.9M seed), Oct 2025 | Production. SOC 2 Type II. |
| Zep / Graphiti | 25,488 | Temporal knowledge graph | MIT (Graphiti OSS) | Not publicly disclosed | Production. |
| OpenViking | 23,189 | Filesystem paradigm, tiered L0/L1/L2 loading | AGPL-3.0 (main); Apache 2.0 (CLI/examples) | ByteDance / Volcengine backed | Early-stage. v0.3.10. |
| Letta / MemGPT | 22,351 | OS-inspired 3-tier: core/recall/archival | Apache 2.0 | Not publicly disclosed | Production. |
| Feast | 6,987 | Entity-keyed feature store + vector search | Apache 2.0 | Red Hat / community-supported | Production. |

Sources: GitHub live counts (Apr 28, 2026); Mem0 funding via TechCrunch (Oct 2025).

## Published benchmarks (not directly comparable to each other)

**LOCOMO (short-term conversational recall)**:

| Approach | Accuracy | Median latency | Tokens/conversation |
|---|---|---|---|
| Full-context (ceiling) | 72.9% | 9.87s (p95: 17.12s) | ~26,000 |
| Mem0g (graph) | 68.4% | 1.09s | ~1,800 |
| Mem0 | 66.9% | 0.71s | ~1,800 |
| RAG | 61.0% | 0.70s | — |
| OpenAI Memory | 52.9% | — | — |

Source: Mem0 paper, ECAI 2025 (arXiv:2504.19413).

**LongMemEval (long-horizon, 1.5M tokens)**: Zep 63.8% vs. Mem0 49.0%. Source: Zep paper (arXiv:2501.13956). (Compare Oracle's own 93.8% LongMemEval claim in [ref-oracle-ai-agent-memory-blog.md](/features/agent-memory/knowledge/ref-oracle-ai-agent-memory-blog.md) — different system, not a head-to-head result.)

**OpenViking + OpenClaw (LoCoMo10, 1,540 cases)**: 52.08% task completion with only 4.3M input tokens vs. 24.6M baseline — but see known issues below.

Different datasets test different things: LOCOMO tests short recall, LongMemEval tests temporal reasoning, LoCoMo10 tests task completion with token efficiency. Don't rank frameworks across benchmarks they weren't both run on.

### OpenViking known issues (competitive intelligence)

| Issue | Severity | Source |
|---|---|---|
| Single repo import consumed ~35.96M LLM tokens unexpectedly | High (cost) | GitHub Issue #1595 |
| Directory overview generation created 117K+ token prompts, crashed VLM | High (stability) | Issue #529 |
| Every memory write triggers full parent-directory recomputation | High (cost scaling) | Issue #769 |
| Path traversal vulnerability in `.ovpack` imports | High (security) | Issue #342 |
| Non-localhost trusted mode without API key | High (security) | Issue #1234 |
| AGPL-3.0 license on main project | Adoption barrier | License file |

## Protocol standards — the memory gap

| Protocol | Purpose | Version | Adoption |
|---|---|---|---|
| MCP | Agent ↔ Tool | Latest (2024-11-05 base) | De-facto standard (OpenAI, Google, GitHub, Slack, Notion) |
| A2A | Agent ↔ Agent | 1.0.0 (March 2026) | 150+ orgs in production (Linux Foundation governed) |
| A2M | Agent ↔ Memory | Draft v0.1 | None — single author, MIT license |
| Engram (PLUR) | YAML memory unit format | v2.1 (March 2026) | Minimal (~1.4K npm weekly downloads) |

MCP standardized tools, A2A standardized agent-to-agent — no adopted standard exists for agent memory. See [question-agent-memory-protocol-standardization.md](/features/agent-memory/knowledge/question-agent-memory-protocol-standardization.md) for the open question this creates.

## Feast's four strategic options

PM recommendation (Zarecki): A+B in RHOAI 3.5, C in 3.6, D watch-only.

| Option | What | Timeline | Risk |
|---|---|---|---|
| A: Agent-Assisted Feature Engineering | LLM helps data scientists discover, analyze, and create features through natural language, inside Feast's governance perimeter | 2 weeks (demo), 6 weeks (product) | Low |
| B: ODFV as Memory Engine | Use Feast's ODFV materialization to implement OpenViking-like L0/L1/L2 tiered memory | 1-2 weeks (PoC) | Low |
| C: Feast + External Memory Frameworks | Integrate with Mem0/Zep so Feast provides governed persistence underneath app-layer memory engines | Months | Medium |
| D: Feast Defines the Memory Protocol | Publish an open memory interface spec; standardize how memory systems talk to data infrastructure | 6-12 months | High (adoption dependent) |

## Customer evidence

Named-account evidence for this research is restricted (customer-named requirements) — see the agent-memory section of [fact-agentic-ai-customer-pain-points.md](/restricted/features/platform/knowledge/fact-agentic-ai-customer-pain-points.md) (restricted) for the specific accounts and signals. In aggregate: the evidence spans governance/audit requirements, zero-trust data-access parity with human users, cost chargeback for agent workloads, framework-agnostic governance across multi-framework shops, data-sovereignty/disconnected-deployment needs, multi-tenant isolation between teams' agents, and MCP-based governed data access.

## Experimentation results

**Experiment 1 — OGX + Ollama EDA** (May 13, 2026, Chaitany Patel): Llama Stack with local Ollama (llama3.2:3b) for EDA on sample data — ~10 seconds, ~1,141 tokens. Proves local LLM EDA is feasible.

**Experiment 2 — Schema Discovery + Native SQL Statistics** (May 26, 2026, Chaitany Patel): standalone tool ([patelchaitany/schema-discovery-eda](https://github.com/patelchaitany/schema-discovery-eda)) scans PostgreSQL/MongoDB, computes native SQL statistics, sends to LLM for EDA — ~23 seconds, ~350 lines of code. Gaps vs. the Feast vision: no Feast integration, no feature suggestion or code generation, no `feast plan` validation, no RBAC, no session memory.

## Production agent-memory lessons (sourced findings)

| Finding | Source |
|---|---|
| 65% of enterprise AI failures trace to context drift or memory loss | tianpan.co |
| GPT-4 accuracy drops from 98.1% to 64.1% based on information position in context | tianpan.co |
| Working memory should be 800-2,000 tokens; >8,000 tokens increases latency 40-60% | mindra.co |
| Vector databases alone fail — no understanding of importance vs. recency | violaris.org |
| Unoptimized agent costs $250K+/year; 60% compression reduces to $102K | tianpan.co |

Treat these as sourced but not independently verified by Red Hat.

## Zarecki's PM position — release schedule & RFEs

**Already filed**: [RHAIRFE-1916](https://redhat.atlassian.net/browse/RHAIRFE-1916) — Feast MCP Server: Governed Feature Access for AI Agents (3.5-candidate, but Feast team capacity pushed it to 3.6 per a Gaurav Kamathe comment).

**Proposed, not yet filed**: RFE-A (Governed Feature Engineering via Feast MCP + self-hosted LLM, TP, 3.5-candidate); RFE-B (Feast Agent Memory — MemoryFeatureView + template, TP, 3.6-candidate); RFE-C (Feast as pluggable memory backend for Mem0/Zep, TP, 3.6-candidate — see [question-feast-mem0-pluggable-storage.md](/features/agent-memory/knowledge/question-feast-mem0-pluggable-storage.md)); RFE-D (Agent Memory Observability in RHOAI Dashboard, TP, 3.6-candidate).

Filing dependency: RFE-A first (smallest scope), then RFE-B (foundation for C and D). Coordinate with Adel Zaalouk's team before filing — the agentic strategy doc has "Agentic Memory [WIP] — Jiras missing." Loop in Ecosystem Engineering (Swati Kale) for RFE-C.

## Key commenters and debates (from the source doc's review comments)

- **Jitendra Yejare**: recommended a standard orchestrated context manager rather than a raw ODFV pattern — "without the standard pattern each customer/project would have to implement the same repeatable pattern." This influenced the `MemoryFeatureView` abstraction.
- **Nikhil Kathole**: suggested a `feast init -t agent` template for automatic scaffolding; noted Option D (memory protocol) feels out of scope, Option C (Feast + Mem0/Zep) is better positioned.
- **Gaurav Kamathe**: suggested a Feast + Mem0 blog for positioning; flagged that Feast team capacity blocks RHAIRFE-1916 to 3.6; identified trusted agents / red-teaming as an exploration area.
- **Umberto Manganiello**: asked for success metrics and decision criteria for PoCs before committing.
- **Jonathan Zarecki**: coined the "data guardrails" framing (see [fact-data-guardrails-positioning.md](/features/agent-memory/knowledge/fact-data-guardrails-positioning.md)); "memory as git" handles point-in-time correctness to some extent.

## Cross-source observations

- **Funding signal**: >$60M into pure-play agent-memory startups in 18 months (Mem0 $24M, Letta $10M, Interloom $16.5M, plus Cognee, Supermemory). Bessemer Venture Partners flagged the memory layer as a 2026 differentiation frontier. Feature-store acquisitions for agentic use: Databricks acquired Tecton, Redis acquired Featureform (both 2025). The market is consolidating around agent memory as infrastructure, not application logic.
- **Protocol standardization gap**: real but premature to fill — see [question-agent-memory-protocol-standardization.md](/features/agent-memory/knowledge/question-agent-memory-protocol-standardization.md).
- **"Data guardrails" as a positioning concept**: source-side enforcement (before data reaches the LLM) vs. output-side enforcement (after the LLM generates a response) — see [fact-data-guardrails-positioning.md](/features/agent-memory/knowledge/fact-data-guardrails-positioning.md).
- **Taxonomy mismatch to resolve**: Peter's 3 areas (Knowledge / Memory / Context Engineering) vs. Oracle's 4 types (Working / Semantic / Episodic / Procedural) vs. MemoryHub's scope-tier model vs. Feast's L0/L1/L2 tiers — see [question-agent-memory-taxonomy.md](/features/agent-memory/knowledge/question-agent-memory-taxonomy.md). Oracle's "four access patterns over one substrate" argument is worth testing against Peter's separation of concerns; Feast's L0/L1/L2 model adds yet another lens, mapped to specific API primitives (Conversations, `/responses/compact`, Vector Stores).
- **Memory ≠ RAG** (Wes Jackson): Peter's "Agent Knowledge" (area 1) looks closer to enterprise RAG / a knowledge graph, while "Agentic Memory" (area 2) is the append-heavy, learned-state database — see [question-agent-memory-vs-rag-distinction.md](/features/agent-memory/knowledge/question-agent-memory-vs-rag-distinction.md).
- **Unified substrate vs. separate services**: Oracle and MemoryHub both argue for a single governed backend (Oracle AI Database; PostgreSQL+pgvector). The Feast proposal introduces a third approach: separate substrate (OGX) from governance (Feast), with clean boundaries. Open question for RHOAI: which pattern fits the platform better — see [question-agent-memory-unified-substrate.md](/features/agent-memory/knowledge/question-agent-memory-unified-substrate.md).
- **Client-side vs. server-side memory** (Francisco Arceo): see [question-agent-memory-client-vs-server-side.md](/features/agent-memory/knowledge/question-agent-memory-client-vs-server-side.md).
- **Session memory vs. long-term memory** (June 23 team-sync consensus): session memory (conversation state) and long-term memory should be separate, though "they come together at the time of prompt assembly" — aligns with Peter's area 2 (Agentic Memory) covering both as distinct concerns. See [fact-agent-memory-team-sync-20260623-transcript.md](/features/agent-memory/knowledge/fact-agent-memory-team-sync-20260623-transcript.md).
- **Context engineering (area 3) is corroborated** by Meta's progressive disclosure, Oracle's summarization-threshold tuning, and the OGX Memory Alpha's token-bounded context injection (1,200-token default) — all treat context construction/compaction as a first-class, measurable concern.
- **Governance is the consistent differentiator**: scope tiers, audit, erasure, contradiction detection, provenance, compliance (EU AI Act, GDPR, HIPAA) recur across MemoryHub, Oracle, and the Feast proposal — aligning with this hub's "Registry = Governance" principle (see [decision-registry-vs-catalog.md](/features/platform/knowledge/decision-registry-vs-catalog.md)). Feast's argument is that it already ships most of these primitives (GA in 3.4), needing only the three bounded deltas above.
- **MemoryHub vs. Feast as governance layer**: the Feast proposal explicitly positions itself as a MemoryHub alternative for governance, citing MemoryHub's IP/copyright blocker and prototype status. Neither proposal is the current direction — research must evaluate both independently. See [question-feast-proposals-vs-memoryhub-overlap.md](/features/agent-memory/knowledge/question-feast-proposals-vs-memoryhub-overlap.md).
- **Memory creation intelligence**: brute-force capture (save everything, curate later) vs. intelligent extraction (agent/rules decide what to save) — most projects favor intelligent extraction to avoid memory bloat. See [question-agent-memory-creation-intelligence.md](/features/agent-memory/knowledge/question-agent-memory-creation-intelligence.md).
- **"Ship something fast" pressure**: both the OGX MVP and the Feast proposal are pushing to get something into product quickly; the team's view is that short-term deliverables can align with long-term architecture rather than trading one off against the other.

## Source documents

| Source | Type | Status |
|---|---|---|
| Feast in the Agentic AI Era | Google Doc (Doc ID `114HxY58rqRFa_GMb9zRR_ScFurn8gbUZCTHNyjzRUYA`) | PROPOSAL / research — see [ref-feast-in-agentic-ai-era.md](/features/agent-memory/knowledge/ref-feast-in-agentic-ai-era.md) |
| Feast + OGX Agent Memory: Proposal | Google Doc (Doc ID `1NE6aefxMKvyTfceDt9evdnteHd7R9ED0UOpcoTbFVEA`) | PROPOSAL — see [ref-feast-ogx-agent-memory-proposal.md](/features/agent-memory/knowledge/ref-feast-ogx-agent-memory-proposal.md) |
| Unified Platform Agentic Memory Infrastructure | Google Doc (Doc ID `1Oae8Ie6aoQRcwQ0SEt24yGkLCviWOuLBrzrJgOec0qM`, Umberto Manganiello, May 2026) | Referenced PROPOSAL — see [ref-unified-platform-agentic-memory-infrastructure.md](/features/agent-memory/knowledge/ref-unified-platform-agentic-memory-infrastructure.md) |

This document itself is sourced from `ai-asset-registry/docs/knowledge-review/assets/agent-memory-knowledge.md` in the old repo (as of 2026-07-05), which consolidated all of the above plus the MemoryHub/Oracle/Meta/Wes-Jackson/OGX-Alpha/team-sync material already captured as individual knowledge entries (see the Quick Map above).
