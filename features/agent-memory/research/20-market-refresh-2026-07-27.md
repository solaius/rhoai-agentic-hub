---
title: "Market refresh (late July 2026)"
description: Quick-depth refresh — Microsoft Foundry Memory (new entry, preview not GA), AWS AgentCore metadata advances, Mem0 SDK v2.0 restructuring + MCP pivot, Zep SOC 2 certification, Letta $10M seed, Anthropic Dreaming shipped as research preview; Adel positioning doc verification.
timestamp: 2026-07-27
lens: landscape
review_after: 2026-09-27
---

# Market refresh (late July 2026)

Quick-depth refresh (`hub.research agent-memory refresh quick landscape`,
2026-07-27): one inline pass, ~10 sources, no fan-out. Triggered by
Adel Zaalouk's positioning musings GDoc
([ref](/features/agent-memory/knowledge/ref-adel-agent-memory-positioning-musings.md))
which claims Microsoft Foundry Memory is "GA (Jul 2026)" — verification
was the primary driver. Confidence labels inline.

## 1. Microsoft Foundry Memory (new series entry)

Doc 19 had no Microsoft entry. Corrected here.

- **Status: PUBLIC PREVIEW** [verified — Microsoft Learn docs,
  `ms.date: 2026-06-02`, explicit "Memory (preview)" banner]. Adel's
  GDoc claims "GA (Jul 2026)" — this is **incorrect**. The Foundry Agent
  Service hosted runtime was expected to GA by early July 2026, but
  Memory itself remains in public preview with no confirmed GA date.
- **Three memory types** [verified — Microsoft Learn]: user profile
  (durable preferences), chat summary (distilled conversation history),
  procedural (reusable execution patterns). All enabled by default.
- **Procedural memory** [verified — Microsoft Foundry Blog, 2026-06-03]:
  the first hyperscaler shipping procedural memory. Uses
  LLM-as-a-judge to extract structured procedures from agent
  trajectories, then retrieves and injects them at runtime. Benchmarks:
  +7–14% absolute on Tau-bench, ~5% on STATE-Bench [reported — vendor].
- **MemoryGuard** [verified — Microsoft Tech Community blog,
  2026-06-21]: **NOT a product feature** — an application-level guidance
  pattern. A reference architecture for write-path validation: inspect
  every candidate memory before persistence, route (not just block),
  scope-based isolation, procedural candidates require strongest
  validation and often human review. Cites OWASP Top 10 for Agentic
  Applications 2026. Adel's GDoc treats MemoryGuard as a product
  capability — this overstates it.
- **No versioning/rollback** [verified — neither the concept docs nor
  the blog mention versioning or rollback]. Unlike Google's Memory
  Revisions, Microsoft has TTL and CRUD management only.
- **Scope model**: up to 100 scopes per store, 10,000 memories per scope.
  Scope set explicitly per request; automatic scope resolution only via
  the memory search tool with `{{$userId}}`.
- **Quotas**: 1,000 req/min for search and update. 19 Azure regions.

**Series impact**: Microsoft fills the third hyperscaler column. Their
investment in procedural memory and MemoryGuard (even as guidance, not
product) validates two series positions — finding 18 (memory security is
existential) and the strategy's procedural-memory inclusion. Their lack
of versioning/rollback keeps finding 4 (the governance whitespace)
intact.

## 2. AWS AgentCore Memory — metadata capabilities advancing

Doc 19 didn't cover AWS in detail. Three updates since March:

- **Streaming notifications** (March 2026) [reported — AWS what's-new]:
  push notifications via Amazon Kinesis when LTM records are
  created/modified. Eliminates polling. 15 regions.
- **Metadata for LTM** (May 2026) [reported — AWS what's-new]: up to
  10 indexed keys per memory resource (STRING, NUMBER, STRING_LIST),
  operator-based filtering alongside semantic search. Metadata can be
  attached at ingestion or inferred by the LLM.
- **Strictly consistent metadata** (June 2026) [reported — AWS
  what's-new]: application-controlled metadata values that bypass LLM
  inference entirely — pass through extraction and consolidation
  unchanged. Up to 3 strictly consistent keys per strategy. Events
  sharing the same values are extracted and consolidated together;
  different values are never merged, even if semantically similar.

**Series impact**: AWS is building the enterprise-metadata story the
others lack. Strictly consistent metadata is architecturally notable —
it's the first hyperscaler mechanism for deterministic (non-LLM) memory
attributes, which maps directly to compliance requirements (audit keys,
tenant IDs, classification labels).

## 3. Google Memory Bank — steady state

Doc 19 already recorded GA + Memory Revisions (preview). Since then:

- **Rebranding**: now "Agent Platform Memory Bank" under the Gemini
  Enterprise Agent Platform (Google Cloud Next 2026) [reported — Google
  Cloud docs + SolidAITech overview]. Features unchanged.
- **Memory Revisions**: still in preview, enabled by default, 365-day
  TTL [verified — Google Cloud docs, updated 2026-07-22].
- **ADK Go support**: Memory Bank implementation for ADK Go's
  memory.Service interface proposed (May 2026, issue #791) [reported —
  GitHub].
- No new capabilities since doc 19.

## 4. Anthropic Dreaming — shipped as research preview

Doc 10 covered the mechanism deeply. Status update:

- **Shipped May 6, 2026** at Code with Claude conference (San Francisco),
  as a **research preview** gated behind a request form [verified —
  multiple outlets]. Only on Claude Managed Agents API — NOT on
  Claude.ai consumer apps.
- **Non-destructive by design** [verified — Foundry Blog, felloai]:
  produces a new memory store alongside the original. Developer
  inspects, accepts, or discards before applying. Original never
  modified during dreaming.
- **Specs**: up to 100 past sessions per dream. Supported models: Opus
  4.7 and Sonnet 4.6.
- **Results**: Harvey reports ~6x task completion improvement
  (legal-drafting jobs). Anthropic internal benchmark: 10.1%
  improvement on PowerPoint generation quality [reported — vendor
  announcements].
- **Not yet expanded** beyond research preview. Billed at standard API
  token rates.

**Series impact**: finding 17 (dream consolidation validated at
production scale) confirmed — now shipping, not just theorized.
Perplexity Brain (doc 19) and Anthropic Dreaming are the two production
implementations of async memory consolidation.

## 5. OSS memory — Mem0 restructuring, Zep compliance, Letta funding

### Mem0

Doc 19 recorded the April 2026 token-efficient algorithm. Since then:

- **SDK v2.0.0** (April 16, 2026) [reported — mem0.ai, callsphere.ai]:
  single-pass extraction (~50% latency reduction), hybrid retrieval
  (semantic + BM25 + entity-graph boosting), and — notably — **entity
  linking replaces Neo4j/Memgraph dependency**. Graph memory no longer
  requires a separate graph database. This changes the series' Mem0
  profile: the "$249/mo Pro" graph lock-in (doc 02, finding 5) is
  partially addressed by built-in entity linking, though the commercial
  cloud graph offering persists.
- **MCP strategy shift** (March–April 2026) [reported — mem0.ai]:
  standalone `mem0-mcp-server` repo removed/consolidated; replaced by
  "Mem0 Plugin for AI Editors" — 9 MCP tools with lifecycle hooks,
  cloud MCP server, integrated into Claude Code/Cursor/Codex workflows.
  OpenMemory consolidated into main repo.
- **Version updates**: v1.0.3 (Jan 2026) added per-project config;
  v1.0.4 (Feb 2026) added timestamp parameter on `update()` for
  backfilling.

### Zep

- **SOC 2 Type 2, HIPAA, GDPR certification** [reported — innobu,
  hermesos.cloud]: the only memory framework with enterprise compliance
  certifications. This directly addresses finding 4's governance gap for
  the OSS camp.
- **Benchmark rebuttal** [reported — rohitraj.tech]: Zep published a
  rebuttal to Mem0's benchmark paper claiming a corrected 75.14% on
  LOCOMO (vs Mem0's reported 65.99% for Zep). The benchmark dispute is
  ongoing.
- **Self-hosting stepped back**: Graphiti engine remains open source;
  the full platform is SaaS from ~$25/mo.

### Letta

- **$10M seed** led by Felicis, backed by Jeff Dean (Google DeepMind),
  Clem Delangue (Hugging Face), Cristobal Valenzuela (Runway) [reported
  — multiple outlets]. Positions Letta as the best-funded pure-play
  after Mem0 ($24M).
- **#1 on Terminal-Bench** (model-agnostic open-source agent category)
  [reported — Letta].
- **Lock-in concern documented**: migration from Letta typically takes
  2–6 weeks (Vectorize, TokenMix analysis) because agents run inside
  Letta's runtime, not with it. Mem0 is swappable within 2 person-days
  by comparison [reported — rohitraj.tech].

### MemPalace

Doc 19 had it as watch-list. Now at ~54.1k GitHub stars, v3.4.0
(June 6, 2026). Still unverified by independent benchmarks.

## 6. Adel positioning doc — verification summary

| Claim in Adel's GDoc | Status |
|---|---|
| Microsoft Foundry Memory "GA (Jul 2026)" | **Incorrect** — public preview, no GA date confirmed |
| MemoryGuard as a product capability | **Overstated** — application-level guidance pattern, not a built-in feature |
| Procedural memory (+7-14% Tau-bench) | **Confirmed** — vendor benchmarks |
| "No competitor ships versioning/rollback" | **Partially outdated** — Google Memory Revisions ships versioning (preview, doc 19); no competitor ships rollback |
| Three scopes (session/user/project/team/org) | Conceptual — Microsoft has user/session; AWS has actor/session/strategy; Google has user-scoped |
| Mem0 graph locked behind $249/mo Pro | **Partially addressed** — SDK v2.0 entity linking replaces Neo4j dependency; cloud graph offering persists |
| "No OSS framework offers enterprise governance" | **Evolving** — Zep now has SOC 2 + HIPAA + GDPR |
| Anthropic Dreaming "most interesting development" | **Confirmed shipped** — research preview, non-destructive, production results |

## 7. What this changes in the series

| Series item | Status after this refresh |
|---|---|
| Doc 02 §2 solution survey rows | Microsoft Foundry Memory is the missing hyperscaler entry — fold into doc 02 at the next standard-depth refresh |
| Doc 19 §3 hyperscaler comparison | Microsoft fills the third column; AWS metadata capabilities should join |
| Finding 4 (governance + K8s + air-gap + open standard whitespace) | **Strengthened** — Microsoft has procedural memory + MemoryGuard guidance but no versioning/rollback, cloud-only; Google has versioning but no rollback, cloud-only; AWS has metadata but no versioning; nobody checks all four boxes |
| Finding 5 (consolidation risk) | **Evolving** — Mem0 SDK v2.0 dropping Neo4j dependency, Zep earning SOC 2, Letta raising $10M; leaders stabilizing but market still fragmented |
| Finding 17 (dream consolidation) | **Confirmed shipped** — Anthropic Dreaming is a production research preview |
| Finding 18 (memory security) | **Strengthened** — Microsoft MemoryGuard guidance validates the threat model as an industry concern |
| Adel's competitive table (doc intake fact) | Mostly accurate on capabilities; wrong on Microsoft GA status; overstates MemoryGuard; Zep SOC 2 changes the governance column for OSS |

## Sources

Web (this pass): learn.microsoft.com Memory concept docs [fetched,
2026-06-02], devblogs.microsoft.com/foundry/memory-build2026 [fetched],
techcommunity.microsoft.com MemoryGuard blog [search summary, paywall
blocked full fetch, 2026-06-21], aws.amazon.com what's-new
(AgentCore Memory streaming/metadata/sc-metadata, Mar-Jun 2026),
cloud.google.com Memory Bank + Memory Revisions docs [fetched,
2026-07-22], docs.cloud.google.com release notes, mem0.ai blog +
callsphere.ai + rohitraj.tech + innobu.com + hermesos.cloud (Mem0/Zep/
Letta comparisons), claudefa.st + letsdatascience.com + felloai.com +
softpagecms.com + faq.com.tw (Anthropic Dreaming coverage). Internal:
[fact-adel-positioning-alongside-harness](/features/agent-memory/knowledge/fact-adel-positioning-alongside-harness.md)
(intake `0743f33`).
