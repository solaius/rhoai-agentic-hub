---
title: Agent Memory & Knowledge: Solution Survey
description: Survey of agent memory/knowledge solutions -- startups, enterprise platform features, framework-native implementations, server-side offerings -- against RHOAI enterprise requirements.
source: ai-asset-registry/agent-memory/research/02-solution-survey.md (as of 2026-07-05)
timestamp: 2026-07-06
review_after: 2026-08-05
---

# Agent Memory & Knowledge: Solution Survey

**Purpose:** Survey the current landscape of agent memory and knowledge solutions — dedicated startups, enterprise platform features, framework-native implementations, and server-side offerings — and assess each against Red Hat's RHOAI enterprise requirements.

**Date:** 2026-05-17

**Status:** EXPLORATORY — research phase, no features scoped. See [RHAISTRAT-1345](https://redhat.atlassian.net/browse/RHAISTRAT-1345).

**Series:** Document 02 of 17 — Agent Memory & Knowledge Research
**Phase 1 (completed 2026-05-17):** [00 Executive Summary](00-executive-summary.md) · [01 Landscape & Definitions](01-landscape-and-definitions.md) · 02 Solution Survey (this doc) · [03 MemoryHub Deep-Dive](03-memoryhub-deep-dive.md) · [04 Technical Patterns](04-technical-patterns.md) · [05 Standards & Protocols](05-standards-and-protocols.md) · [06 OGX Memory Primitives](06-ogx-memory-primitives.md) · [07 Taxonomy & Decomposition](07-taxonomy-and-decomposition.md) · [08 RHOAI & OCP Alignment](08-rhoai-ocp-alignment.md)
**Phase 2 (2026-06-09):** [09 Agent Harness Memory](09-agent-harness-memory.md) · [10 Claude Memory & Dreaming](10-claude-memory-dreaming.md) · [11 Adversarial Memory](11-adversarial-memory.md) · [12 Benchmarking & Evaluation](12-benchmarking-evaluation.md) · [13 KV-Cache Optimization](13-kv-cache-optimization.md) · [14 Enterprise Use Cases](14-enterprise-use-cases.md) · [15 Multi-Modal Memory](15-multi-modal-memory.md) · [16 AI Gateway Memory Substrate](16-ai-gateway-memory-substrate.md) · [REVIEW-NOTES](REVIEW-NOTES.md)

---

## 1. Comparison Table

The table below covers every solution examined in this survey. "Governance Maturity" is rated on a four-point scale: **None / Emerging / Moderate / Enterprise** — based on the presence of audit trails, access controls, multi-tenancy, compliance certifications, retention/erasure controls, and operational oversight features. "RHOAI Relevance" is rated **High / Medium / Low** based on alignment with the on-premise, Kubernetes-native, air-gappable, governance-first profile of RHOAI.

**REFERENCE** — all vendor data below is drawn from public sources as of May 2026; see the Sources section.

| Solution | Category | Openness / License | Governance Maturity | Deployment Model | RHOAI Relevance |
|---|---|---|---|---|---|
| **Mem0** | Dedicated memory startup | Open core; Apache 2.0 OSS tier + managed cloud + enterprise | Emerging (multi-scope isolation, metadata filtering; no audit/erasure primitives in OSS tier) | Managed cloud, self-hosted Docker, local MCP (OpenMemory) | **High** — self-hosted option, MCP surface, 21 framework integrations, active benchmark research |
| **Letta (MemGPT)** | Dedicated memory + agent platform | Apache 2.0 (OSS framework + server); commercial API tier | Emerging (agent-level memory isolation; no documented enterprise governance) | Self-hosted (Letta Server), cloud API, local desktop app | **Medium** — strong architecture innovation (OS-inspired hierarchy, sleep-time compute); enterprise governance thin |
| **Zep / Graphiti** | Temporal knowledge graph | Graphiti: Apache 2.0 (open source engine only); Zep Cloud: proprietary; Community Edition deprecated | Moderate for cloud (SOC2 Type 2, HIPAA); None for self-hosted (CE deprecated) | Cloud-only managed service; Graphiti engine self-hostable with manual stack assembly | **Medium** — Graphiti's bi-temporal graph is technically distinctive; cloud-only managed product is a data-residency concern |
| **Cognee** | Knowledge graph / memory control plane | Apache 2.0 core; commercial cloud | Emerging (ECL pipeline provenance; 70+ enterprise deployments; no documented audit/erasure) | Cloud SaaS, OSS self-hosted, edge Rust engine (in development) | **Medium** — graph-first architecture with self-hosted option; enterprise governance nascent |
| **OpenViking (ByteDance/Volcengine)** | Context database / memory infrastructure | **AGPL-3.0** (main project; CLI and examples Apache 2.0); changed from Apache 2.0 in v0.2.15 (March 2026) | None (no audit trail, RBAC, retention/erasure primitives; self-evolution raises governance questions) | Self-hosted (pip/Docker), OpenShift AI (community manifests), Volcengine cloud ("OpenViking Personal") | **Low for adoption (AGPL-3.0 is a productization blocker); Medium as pattern** — filesystem-paradigm context organization and tiered L0/L1/L2 loading are architecturally novel; AGPL-3.0 copyleft requirements conflict with Red Hat's typical licensing approach for productized components |
| **Supermemory** | Memory API / developer tooling | Open source (license not verified in primary sources; see Sources note); commercial API | None documented | Cloud API, MCP server | **Low** — early-stage, small team (8 employees), no enterprise governance; useful reference for MCP-native memory API design |
| **Interloom** | Enterprise tacit knowledge / context graph | Proprietary | Emerging (expert oversight governance model; no technical audit primitives documented) | Cloud SaaS for enterprise; current deployments in European enterprises | **Low** — problem framing (undocumented tacit knowledge) is relevant; proprietary and non-Kubernetes-native |
| **Oracle AI Agent Memory** (`oracleagentmemory`) | Enterprise database-native memory | Proprietary Python SDK; requires Oracle AI Database | Enterprise (per-record audit/erasure, multi-tenant isolation, four memory types over one governed substrate, GDPR/HIPAA-aligned scoping) | Oracle Database (cloud or on-premise) | **Medium** — highest governance maturity of any external solution; requires Oracle Database lock-in; the "four access patterns over one substrate" architecture is the strongest external design signal for RHOAI |
| **AWS Bedrock AgentCore Memory** | Hyperscaler managed memory | Proprietary; AWS-managed | Moderate (KMS encryption, episodic learning, streaming notifications; lacks on-premise option) | AWS cloud-only managed service | **Low for adoption; High as signal** — validates managed memory as a product feature; cloud-only is disqualifying for on-premise RHOAI deployments |
| **Google Vertex AI Memory Bank** | Hyperscaler managed memory | Proprietary; Google-managed | Moderate (IAM, VPC, audit logs via Cloud Audit; GA Jan 2026) | Google Cloud-only managed service | **Low for adoption; Medium as signal** — similar to AWS; Memory Profiles feature is architecturally notable |
| **OpenAI server-side memory** | Provider-managed memory | Proprietary; OpenAI-managed | Low (opaque server-side compaction; not inspectable; server-managed state) | OpenAI cloud-only | **Low** — useful context for context engineering study; architecture is opposite of RHOAI's governance and data-residency requirements |
| **Anthropic Claude Dreaming** | Provider-managed memory consolidation | Proprietary; Claude Managed Agents only | Emerging (human approval gate before deployment; source sessions preserved; currently research preview) | Anthropic Managed Agents cloud only | **Low for adoption; Medium as signal** — sleep-time consolidation pattern is relevant; enterprise nervousness about Anthropic owning memory is a validated concern |
| **LangGraph / LangMem** | Framework-native memory | Apache 2.0 (LangGraph, LangMem); LangSmith cloud proprietary | Emerging (LangSmith RBAC on enterprise tier; storage layer is developer-managed) | Self-hosted or LangSmith cloud; pluggable backends (Postgres, Redis, MongoDB) | **High** — RHOAI's LangGraph integration requirement means LangGraph's memory primitives define the baseline developer expectation; LangMem adds long-term extraction on top |
| **CrewAI memory** | Framework-native memory | Apache 2.0 (framework); CrewAI Enterprise proprietary | None in OSS tier (LanceDB + SQLite; local only); Moderate in CrewAI Enterprise (SOC2, HIPAA) | Local (OSS); managed cloud (Enterprise) | **Medium** — CrewAI is one of the framework targets in RHAISTRAT-1345; cognitive memory model (selective encoding, contradiction resolution, purposeful forgetting) is architecturally notable |
| **OpenClaw** | Framework-native memory | MIT License (fully open source) | None documented in OSS release (filesystem trust boundary; channel-level access policies; no audit trail, RBAC, or retention primitives in core) | Client-side local (default; `~/.openclaw/workspace`); self-hosted Kubernetes via community operator; Docker; OpenShift documented | **Medium as pattern** — MIT, 370K+ GitHub stars, Kubernetes/OpenShift deployment documented; client-side hybrid memory model (70% vector / 30% BM25) is the canonical example of the client-side memory pattern for developer-workflow agents; no enterprise governance in OSS core |
| **Microsoft GraphRAG** | Knowledge graph / RAG framework | MIT license | None (research/tooling; no governance features) | Self-hosted (open source) | **Medium as pattern** — 26% comprehensiveness improvement over vector RAG documented; full GraphRAG indexing cost ($50–200 per corpus for moderate corpora) largely resolved at moderate scale by LazyGraphRAG (0.1% of full cost, late 2024); more relevant to "Agent Knowledge" (area 1) than operational memory |
| **MemPalace** | Dedicated memory / developer tool | MIT License (fully open source) | None (local-first; namespace isolation available on Qdrant/pgvector backends; no audit trail, RBAC, retention/erasure, or compliance features) | Local-first (ChromaDB + SQLite default); Docker; optional Qdrant/pgvector remote backends; MCP server mode | **Low for adoption; Medium as pattern** — verbatim storage philosophy with 96.6% LongMemEval is the strongest local-only benchmark result; no enterprise governance; celebrity-driven growth (55K+ GitHub stars) reflects attention not enterprise adoption |
| **MemoryHub (Red Hat AI Americas)** | Internal Red Hat prototype | Apache 2.0 | Enterprise-oriented (five-tier scope isolation, contradiction detection, PII scanning, immutable audit trail on roadmap, EU AI Act / GDPR / HIPAA compliance posture) | OpenShift-native (UBI images, FIPS delegation, air-gap deployable) | **Very High** — see [MemoryHub Deep-Dive](03-memoryhub-deep-dive.md) |

---

## 2. Dedicated Memory Startups

### 2.1 Mem0

**REFERENCE** — Mem0 is the highest-traction dedicated memory startup as of May 2026. Founded by Taranjeet Singh (CEO) and Deshraj Yadav (CTO); YC-backed; raised $24M Series A (Basis Set Ventures lead, Peak XV, GitHub Fund, YC). GitHub: 48,000+ stars on the `mem0` repository.

**Architecture:** Mem0 operates as a dedicated memory layer separate from the LLM context window, using a multi-signal retrieval approach that combines semantic similarity (vector), BM25 keyword matching, and entity matching into a fused scoring mechanism. In the April 2026 v2.0.0 release, the architecture shifted to single-pass hierarchical extraction (one LLM call per `add()`), built-in entity linking replacing external graph stores, and hybrid retrieval combining semantic + BM25 + entity-graph boosting. This shift traded graph traversal depth for deployment simplicity and p95 latency improvement.

**Memory types:** Three types — episodic (interaction history), semantic (learned facts and knowledge), procedural (workflows and patterns; documented as early-stage).

**Memory scoping:** Four dimensions — `user_id`, `agent_id`, `run_id`, `app_id` — with an optional `org_id`. This is a reasonable multi-tenancy model but stops short of MemoryHub's five-tier scope (user/project/role/organizational/enterprise) or the enforcement guarantees of Oracle's per-record scoping fields.

**Benchmarks (from Mem0's own published report — treat as vendor-claimed):**

| Benchmark | Mem0 Score | Token/Query |
|---|---|---|
| LongMemEval | 93.4% | 6,787 |
| LoCoMo | 91.6% | 6,956 |
| BEAM (1M tokens) | 64.1% | 6,719 |
| BEAM (10M tokens) | 48.6% | 6,914 |

Key gains over prior version: +29.6 points on temporal reasoning, +23.1 on multi-hop recall. The sharp drop from 64.1% at 1M tokens to 48.6% at 10M tokens is an important signal: temporal abstraction degrades significantly at enterprise scale. These figures are self-reported by Mem0; independent third-party validation is not available in public sources.

**Deployment:** Three tiers — managed cloud (2-min setup), self-hosted Docker + Qdrant (20 min), local-first OpenMemory MCP (for dev tools like Claude Desktop, Cursor, Windsurf). The OpenMemory MCP option keeps data on-device with no cloud sync. Self-hosted option supports 20 vector store backends and 21 agent frameworks.

**Governance posture:** Metadata filtering, structured error handling, and async writes are production-grade. Audit trails, erasure primitives, retention policies, and multi-tenant enforcement are not documented in public OSS tier. The enterprise tier likely adds governance features, but these are not publicly documented. For RHOAI, the governance surface needs significant augmentation.

**Enterprise signal:** Exclusive memory provider for AWS's Agent SDK — gives Mem0 enterprise distribution most open-source projects lack. The AWS partnership is a validation signal but also creates a dependency question for non-AWS deployments.

**Hype-vs-reality note:** Mem0's benchmark scores are vendor-published and not yet independently reproduced. The 10M-token BEAM result (48.6%) is a direct contradiction to the headline precision narrative — RHOAI workloads involving large-scale enterprise knowledge could hit this degradation ceiling.

**RHOAI relevance:** High. Self-hosted Docker deployment, MCP surface (OpenMemory), and 21-framework compatibility make Mem0 the most deployment-flexible of the startups. Governance gap requires Red Hat to add the enterprise layer. Mem0 could serve as a reference implementation or integration target for a platform-managed memory service.

---

### 2.2 Letta (formerly MemGPT)

**REFERENCE** — Letta is the commercial product and framework descending from the MemGPT research project (UC Berkeley Sky Computing Lab; Sumers, Weng, et al., 2023). Founded by Charles Packer (CEO) and Sarah Wooders (CTO). Raised $10M seed round (Felicis Ventures, Sept 2024). No Series A disclosed as of May 2026. GitHub: ~19,000 stars on the Letta repo (MemGPT repo accumulated the historical star count separately).

**Architecture — OS-inspired memory hierarchy:** Letta's defining contribution is treating the LLM context window as constrained RAM, with an explicit hierarchy of three memory tiers:

1. **Core memory** — in-context memory blocks pinned to the context window, editable by the agent in real time (analogous to RAM). Supports labeled blocks (e.g., `human`, `persona`, `project`) with explicit character limits.
2. **Recall memory** — complete interaction history persisted to disk/database, searchable on demand (analogous to a paging file).
3. **Archival memory** — externalized knowledge in vector or graph databases, accessed via tool calls (analogous to a hard drive).

This is the most explicit OS analogy in the memory space and provides the clearest conceptual model for platform memory primitives. The CoALA taxonomy (doc 01) independently arrived at a similar hierarchy; Letta is its most fully realized implementation.

**Sleep-time compute:** A 2026 addition — asynchronous memory agents that run between active sessions to refine, prune, and reorganize memory without blocking inference. This mirrors Anthropic's Dreaming feature architecturally but is developer-controlled and framework-agnostic.

**Conversations API (Jan 2026):** Enables shared agent memory across parallel agent instances — the first sign of Letta moving toward multi-agent shared state.

**Letta Code (April 2026):** The current product direction is a local-first, model-agnostic agent harness with git-backed memory and subagents. This is a pivot away from hosted infrastructure toward developer tooling. Enterprise governance features are explicitly being deprioritized in favor of "frontier capabilities."

**Deployment:** Self-hosted (Letta Server, Apache 2.0), cloud API, local desktop app. Open source.

**Governance posture:** Thin. Letta is actively sunsetting constraint-based governance (tool rules, specialized memory tools). For RHOAI, Letta is most useful as an architectural reference — the core/archival/recall model and sleep-time compute patterns are worth incorporating — rather than as a platform component.

**Contradiction:** Letta's pivot to Letta Code (local, git-backed, individual developer) moves away from the multi-agent platform tier that RHOAI targets. The architecture is sound but the product direction is diverging from enterprise requirements.

**RHOAI relevance:** Medium. The OS-inspired memory hierarchy is the best conceptual model for explaining memory tiers to platform engineers. Sleep-time compute is a pattern worth considering for the RHOAI memory primitives roadmap. The enterprise product gap limits direct integration value.

---

### 2.3 Zep and Graphiti

**REFERENCE** — Zep is a context engineering and memory platform built by Daniel Chalef and team. YC-backed ($500K, April 2024 — confirmed from Tracxn; no further rounds publicly confirmed). The Zep Community Edition was deprecated in 2025; Zep Cloud is the commercial managed service. Graphiti (the temporal knowledge graph engine) was open-sourced under Apache 2.0 as Zep's open-source strategy pivot.

**Architecture — temporal knowledge graph:** Zep's defining technical contribution is Graphiti's bi-temporal tracking model. For every fact in the knowledge graph, the system maintains four timestamps:
- `t'created` and `t'expired` (transactional timeline — when the fact entered/left the database)
- `t_valid` and `t_invalid` (event timeline — when the fact was actually true in the world)

This enables accurate reasoning about temporal relationships, relative references ("two weeks ago"), and fact supersession — a capability that purely vector-based systems lack. The graph is structured as three hierarchical subgraphs: Episode (raw data), Semantic Entity (extracted entities and relationships), and Community (clustered summaries via label propagation).

**Retrieval:** Multi-faceted search combining cosine similarity, BM25 full-text, and breadth-first graph traversal. This is the same retrieval stack that MemoryHub, Mem0, and Cognee all converge on.

**Benchmarks:**

*From arXiv:2501.13956 (peer-reviewed paper):*
- LongMemEval: Zep + gpt-4o: 71.2% (+18.5% vs baseline), with 90% latency reduction (approximately 2.6s vs 28.9s)
- Context tokens reduced from ~115K to ~1.6K per query

*From Zep vendor documentation (not from arXiv:2501.13956 — treat as vendor-claimed):*
- Deep Memory Retrieval: 94.8% (gpt-4-turbo), 98.2% (gpt-4o-mini)

Note: The LongMemEval score of 71.2% is lower than Oracle (93.8%) and Mem0 (93.4%) in their published benchmarks. These runs used different model configurations and test conditions — direct comparison is not valid without controlled conditions.

**Open source status:** Zep Community Edition deprecated — no longer maintained or updated, though the Apache 2.0 licensed repository remains. Graphiti (the graph engine) is the active open-source component. A full self-hosted Zep-equivalent requires assembling: Graphiti + a graph database (Neo4j, FalkorDB, or Kuzu) + embedding models + LLM infrastructure. There is no turnkey self-hosted option.

**Deployment:** Cloud-only for managed Zep; Graphiti engine self-hostable with manual stack assembly. SOC2 Type 2 certified, HIPAA compliant for cloud tier.

**RHOAI relevance:** Medium. Graphiti's bi-temporal model is the best available open-source implementation of temporal fact tracking — directly relevant to the multi-session and knowledge-update requirements that all enterprise memory systems face. The abandonment of Community Edition is a risk signal: vendors in this space are finding sustainable open-source memory service operation difficult. Red Hat should not plan to use Zep Cloud (data residency concern) but should evaluate Graphiti as a component for an RHOAI-native memory substrate.

---

### 2.4 Cognee

**REFERENCE** — Cognee (Berlin-based, founded by Vasilije Markovic and team) raised €7.5M seed (Pebblebed lead — Pamela Vagata, founding member of OpenAI, and Keith Adams, who founded Facebook AI Research (FAIR); 42CAP, Vermilion Ventures, Google DeepMind angels; announced Feb 19, 2026). Apache 2.0 open source core; commercial cloud SaaS. 12,000+ GitHub stars, 80+ contributors, operating in 70+ companies, pipeline volume 500x growth in 2025 (2,000 to 1M+ monthly runs).

**Architecture — ECL pipeline:** Cognee's core concept is the Extract-Cognify-Load (ECL) pipeline:
1. **Extract** — ingests data from 38+ sources in any format or structure
2. **Cognify** — builds a structured knowledge graph with embeddings and relationships; prunes stale nodes, strengthens frequent connections, reweights edges based on usage signals, adds derived facts
3. **Load** — makes the structured knowledge searchable

The "Cognify" step is what distinguishes Cognee from RAG: it continuously rewrites graph structure based on usage patterns rather than storing static chunks. This is a form of self-improving memory — the graph adapts as agents interact with it.

**Use case fit:** Bayer used Cognee for scientific research workflows; University of Wyoming for evidence graph construction from scattered policy documents with page-level provenance. These are "Agent Knowledge" (Peter's area 1) use cases — org-wide structured knowledge rather than operational episodic/semantic memory.

**Deployment:** Cloud SaaS (primary), OSS self-hosted option, edge Rust engine in development (adds air-gap potential). Neo4j, Amazon Neptune, n8n, Claude, OpenAI, LangGraph integrations documented.

**Governance posture:** ECL pipeline provides data provenance (source tracking per node); no documented audit trail, retention policies, or RBAC beyond what the hosting layer provides. Self-hosted option gives data sovereignty; cloud tier requires trust in Cognee's cloud.

**RHOAI relevance:** Medium. Cognee's ECL architecture and the self-improving graph model are worth studying for the "Agent Knowledge" layer design (Peter's area 1). The edge Rust engine roadmap item is interesting for air-gap scenarios. Enterprise governance is nascent. Cognee occupies a different niche than operational memory (Mem0, Letta) — it is closer to a governed knowledge graph engine than a session-state store.

---

### 2.5 Supermemory

**REFERENCE** — Supermemory is an early-stage startup (founded 2024 by Dhravya Shah, San Francisco). Raised $2.6M seed (Oct 2025; co-led by Susa Ventures, Browder Capital, and SF1.vc; individual investors include Google AI chief Jeff Dean, Cloudflare's Knecht, Logan Kilpatrick, Sentry's David Cramer, executives from OpenAI/Meta/Google). 8 total employees as of May 2026.

**Architecture:** Five-layer stack: connectors (Slack, Notion, Gmail auto-sync), extractors (multi-modal chunking), Super-RAG (hybrid vector + keyword with reranking), memory graphs (ontology-aware edges), and user profiles (static preferences + real-time session data). Publishes sub-300ms p95 recall latency and 85.4% LongMemEval-S accuracy — but these figures are vendor-claimed (LongMemEval-S is a variant, not the full LongMemEval). Open source licensing status was not confirmed from primary sources (Supermemory's GitHub was referenced but license was not verified — do not assume Apache 2.0).

**Notable:** MCP-native memory API for coding agent workflows (Claude Code, OpenCode integrations). This is the most coding-agent-focused memory API in the survey.

**Governance:** No documented governance, compliance certifications, or enterprise access controls. Very early stage.

**RHOAI relevance:** Low. Supermemory is too early-stage and governance-thin for enterprise consideration. Useful as a reference for MCP-native memory API design patterns, and the coding-agent focus is relevant to RHOAI's developer workflow positioning.

---

### 2.6 Interloom

**REFERENCE** — Interloom (Berlin-based, German/European enterprise focus) raised $16.5M seed (March 2026; DN Capital lead, Bek Ventures, Air Street Capital). Previously raised $3M in March 2024. Live with several large European enterprises including Commerzbank and Zurich Insurance/Fiege.

**Problem framing:** Interloom frames their target as "tacit knowledge" — the ~70% of operational decisions that exist only in employee heads, emails, tickets, and transcripts but are never formally documented. This directly maps to Peter's "Agent Knowledge" area 1.

**Architecture — context graph:** Ingests millions of operational records (support emails, service tickets, call transcripts, work orders) and constructs a continuously updated "context graph" of how problems get resolved within an organization. Analogized to Google Maps for expert decision-making: captures the routes experts take, not just the documented processes.

**Enterprise deployment:** SaaS, deployed at large European enterprises. Current use case: Commerzbank analyzed millions of customer support emails and found existing documentation was "conflicting or incomplete" — Interloom's context graph surfaces the actual resolution patterns.

**Governance:** Expert oversight model (expert teams co-resolve cases with AI agents; resolutions automatically enter institutional memory). No technical audit primitives or RBAC details in public sources. Proprietary.

**RHOAI relevance:** Low for adoption (proprietary, SaaS-only, European enterprise focus, no Kubernetes-native path). High as a problem-framing signal: the tacit knowledge problem ($16.5M funded, enterprise traction) validates that org-level "Agent Knowledge" (area 1) is a real, funded market need. The context graph approach — continuously learning from real operational resolutions — is a pattern RHOAI's eventual knowledge layer should consider.

---

### 2.7 OpenViking (ByteDance / Volcengine)

**REFERENCE** — OpenViking is an open-source context database designed for AI agents, initiated and maintained by ByteDance's Volcengine Viking team. Open-sourced in January 2026. GitHub: 25,000+ stars, 1,900+ forks (as of June 2026). The project open-sources a subset of the capabilities described in the VikingMem paper (arXiv:2605.29640, accepted by VLDB 2026). No venture funding (ByteDance subsidiary, not a startup). Stack: Python (~76%), Rust (~11%), TypeScript (~7%), C++ (~3%).

**CRITICAL — License: AGPL-3.0.** The main OpenViking project is licensed under **AGPL-3.0** (changed from Apache 2.0 in v0.2.15, approximately March 30, 2026). The CLI (`crates/ov_cli`) and examples remain Apache 2.0. The AGPL-3.0 network interaction clause (Section 13) requires that any organization that modifies OpenViking's server code and provides that functionality to users over a network must release all modifications under AGPL-3.0. This triggers even for internal deployments accessed by other teams within the same organization. **This is the most significant licensing concern in this survey for RHOAI productization** — AGPL-3.0 copyleft requirements are incompatible with Red Hat's typical approach for components that ship as part of a commercial product offering. Volcengine has not publicly offered a commercial/dual license alternative.

Note: Several third-party sources (including the Red Hat Developer article on OpenShift AI deployment) still reference "Apache 2.0" — these were written before the v0.2.15 license change. The GitHub repository badge now reads "AGPL-3.0." Any RHOAI evaluation must use the current license, not the historical one.

**Architecture — filesystem-paradigm context database:** OpenViking's defining contribution is treating agent context not as flat vector chunks but as a hierarchical virtual filesystem addressed via a `viking://` protocol. Every piece of context — memories, resources, skills — is mapped to a virtual directory with a unique URI:

```
viking://
├── resources/    (project docs, repos, web pages)
├── user/         (preferences, habits, memories)
│   └── memories/
└── agent/        (skills, instructions, task memories)
    ├── skills/
    └── memories/
```

Agents interact with context using filesystem-like operations (`ls`, `find`, `grep`, `tree`) rather than opaque semantic search. This makes retrieval trajectories fully observable and debuggable — a direct contrast to the black-box retrieval patterns of traditional RAG systems.

**Tiered context loading (L0/L1/L2):** Every piece of context is automatically processed into three levels of detail on write:

| Tier | Token Budget | Purpose |
|---|---|---|
| **L0 (Abstract)** | ~100 tokens | One-sentence summary; enough to decide relevance without loading content |
| **L1 (Overview)** | ~2,000 tokens | Core information for planning and decision-making; equivalent to a README |
| **L2 (Detail)** | Full content | Complete original data; loaded on-demand only when deep detail is needed |

This tiered approach achieves up to 96% token savings (vendor-claimed) by defaulting to L0/L1 summaries and fetching L2 content only when explicitly needed. The approach is conceptually aligned with Letta's core/archival hierarchy but implemented as a content-level abstraction rather than a memory-tier abstraction.

**Directory Recursive Retrieval:** OpenViking's retrieval strategy integrates multiple methods in a hierarchical traversal:
1. Intent analysis generates multiple retrieval conditions from the query
2. Vector search locates the highest-scoring directories
3. Secondary retrieval refines results within those directories
4. Recursive drill-down through subdirectories if they exist
5. Result aggregation returns the most relevant context with full traversal trajectory preserved

This "lock directory first, then refine content" approach is structurally different from the flat hybrid retrieval (vector + BM25 + entity) used by Mem0, Zep/Graphiti, and MemoryHub. The traversal trajectory is fully preserved and visualizable — useful for debugging retrieval quality.

**Self-evolution:** At the end of each agent session, OpenViking automatically extracts long-term memories from conversations and updates `viking://user/memories/` and `viking://agent/memories/`. The agent writes to its own skills directory based on experience — effectively reprogramming its own capabilities over time. This is architecturally similar to CrewAI's cognitive memory (selective encoding, contradiction resolution) but operates at the filesystem level rather than the embedding level.

**Governance concern with self-evolution:** Agents that can rewrite their own skills directory are self-modifying — a powerful mechanism that creates governance challenges in enterprise settings. No guardrails, approval gates, or audit trails for self-evolution are documented. Contrast with Anthropic's Dreaming, which requires human approval before memory updates take effect. For RHOAI, any adoption of the self-evolution pattern would require adding an approval gate analogous to Dreaming's governance model.

**Memory types:** OpenViking does not use the traditional cognitive science labels (episodic, semantic, procedural). Instead, it organizes context into three functional categories:
- **Resources** — documents, repos, web pages (closest to "semantic" / area 1 Agent Knowledge)
- **User memories** — preferences, habits, learned facts (closest to "episodic" + "semantic")
- **Agent skills/memories** — reusable tool definitions, task execution insights (closest to "procedural")

These categories are unified under the filesystem abstraction rather than implemented as separate storage systems — conceptually aligned with Oracle's "four access patterns over one substrate" argument, though with a filesystem metaphor rather than a relational database metaphor.

**Benchmarks (from vendor documentation and the VikingMem paper — treat as vendor-claimed unless from the VLDB-accepted paper):**

| Benchmark | Result | Comparison |
|---|---|---|
| LoCoMo10 (1,540 cases) | Accuracy: up to 82.08% (OpenClaw + OpenViking) | vs. 24.20% baseline OpenClaw; 49% improvement with 83% token reduction |
| HotpotQA | 91% accuracy, 0.23s retrieval latency | Top-20 retrieval |
| OpenClaw integration | +43% task completion, -91% input tokens | vs. native OpenClaw |
| OpenClaw + LanceDB | +17% task completion, -92% input tokens | vs. OpenClaw with LanceDB backend |
| VikingMem paper (VLDB) | Storage cost reduction up to 83.2%, P95 latency improvement of 900ms | vs. naive RAG/raw-log approaches |

Note: The VLDB-accepted VikingMem paper is the most methodologically rigorous benchmark source for OpenViking. The LoCoMo/HotpotQA figures are from vendor documentation. No independent third-party benchmarks have been published. The LoCoMo figures are not directly comparable to the LongMemEval scores reported for Mem0 (93.4%), Oracle (93.8%), or Zep (71.2%) — different benchmarks, different evaluation methodology.

**Deployment:** Four options:
- **Local:** `pip install openviking`, configure `ov.conf`, run `openviking-server` (REST API on port 1933)
- **Docker:** Official image bundles server, VikingBot agent, and console UI
- **OpenShift AI:** Community-maintained deployment manifests (`aicatalyst-team/openviking-openshift`) using Kustomize; two-namespace architecture with KServe InferenceServices for models (Qwen3-Embedding-0.6B + Qwen3-32B) and OpenViking server; runs entirely in-cluster with no external API calls
- **Volcengine cloud:** "OpenViking Personal" managed service with VikingDB backend (proprietary infrastructure)

The OpenShift AI deployment was documented in a Red Hat Developer article (April 2026), which explicitly advised: "Treat it as an experiment worth running, not a production dependency." The article referenced the pre-AGPL Apache 2.0 license; the current AGPL-3.0 license adds significant constraints for enterprise deployment.

**Integration patterns:**
- **MCP integration:** Provides MCP tools for Claude Desktop, Claude CLI, and other MCP-compatible clients
- **OpenAI-compatible API:** REST API compatible with OpenAI-style `file_search` and `vectorstore` APIs
- **OpenClaw ecosystem:** Native integration with OpenClaw; adopted by Chinese tech giants (Tencent QClaw, ByteDance ArkClaw, Alibaba JVS Claw)
- **Python SDK:** `SyncHTTPClient` / `AsyncHTTPClient` with minimal API surface: `add_resource()`, `search()`, `read()`, `ls()`
- **CLI:** `ov` command with filesystem-like operations

**Governance posture:** None. No documented audit trail, access controls, RBAC, retention/erasure primitives, or multi-tenancy features. The self-evolution capability (agents rewriting their own memory and skills) operates without governance controls. The filesystem is the trust boundary — same limitation as OpenClaw's client-side model. For RHOAI enterprise requirements, the governance surface is entirely absent and would need to be built from scratch.

**Comparison with other solutions in this survey:**

| Dimension | OpenViking | Mem0 | Letta | Zep/Graphiti |
|---|---|---|---|---|
| **Context organization** | Hierarchical filesystem (`viking://`) | Flat multi-signal retrieval | OS-inspired hierarchy (core/recall/archival) | Bi-temporal knowledge graph |
| **Token optimization** | L0/L1/L2 tiered loading (up to 96% savings) | Single-pass extraction (~7K tokens/query) | Core memory in-context, archival on-demand | Graph-based context reduction (~1.6K tokens) |
| **Retrieval** | Directory recursive traversal | Semantic + BM25 + entity fusion | Tool-call-based archival access | Cosine + BM25 + graph BFS |
| **Self-evolution** | Native (agents rewrite skills/memories) | Not documented | Sleep-time compute (async reorganization) | Not documented |
| **License** | **AGPL-3.0** | Apache 2.0 (OSS tier) | Apache 2.0 | Apache 2.0 (Graphiti) |
| **Governance** | None | Emerging | Thin | Moderate (cloud only) |
| **RHOAI adoptability** | **Blocked by AGPL-3.0** | High (self-hosted option) | Medium (architecture reference) | Medium (Graphiti as component) |

**Key differentiators from other solutions:**
1. **Filesystem paradigm** — Unique in this survey. Every other solution uses flat storage (vector, graph, or relational). OpenViking's `viking://` protocol treats context as navigable directories, making retrieval observable and debuggable.
2. **Tiered loading** — The L0/L1/L2 approach is the most aggressive token optimization strategy surveyed. Rather than retrieving and truncating, it generates pre-computed summaries at different granularities.
3. **Self-evolution** — The only solution where agents actively rewrite their own skill definitions based on experience, creating a feedback loop between execution and capability.
4. **Research backing** — VLDB 2026-accepted paper (VikingMem) provides academic validation that other memory startups lack. Only Zep (arXiv:2501.13956) has comparable peer-reviewed backing.

**RHOAI implications — the AGPL-3.0 problem:**

The AGPL-3.0 license is the decisive factor for RHOAI evaluation. Specifically:

1. **Network copyleft trigger:** AGPL Section 13 requires that modified server code providing functionality over a network must be released under AGPL-3.0. Any RHOAI modifications to OpenViking's server — customization, governance additions, platform integration — would trigger this clause and require open-sourcing all modifications under AGPL-3.0. This is fundamentally incompatible with shipping OpenViking as part of a proprietary product offering.

2. **No dual license available:** Unlike MongoDB (which offers a commercial alternative to its SSPL license) or similar projects, Volcengine has not publicly offered a commercial/dual license for OpenViking. There is no obvious path to negotiate AGPL-3.0 away.

3. **ByteDance governance risk:** The project is governed entirely by Volcengine (ByteDance) with no independent foundation. Licensing, roadmap, and contributor terms are controlled by a single corporate entity. The license change from Apache 2.0 to AGPL-3.0 mid-project (v0.2.15) demonstrates this governance risk in practice — downstream adopters who relied on the Apache 2.0 license were surprised by the change.

4. **Pattern extraction is the viable path:** RHOAI can study and adopt OpenViking's architectural patterns (filesystem paradigm, L0/L1/L2 tiered loading, directory recursive retrieval, self-evolution with governance gates) without adopting the AGPL-3.0 codebase. These patterns are ideas, not copyrightable implementations. MemoryHub or a future RHOAI memory service could implement similar concepts under Apache 2.0 without AGPL contamination.

5. **Red Hat's AGPL track record:** Red Hat accepts AGPL for Fedora and internal infrastructure (with compliance processes), but AGPL components in productized RHEL/RHOAI offerings face significantly higher legal review barriers. Running unmodified AGPL software is generally permissible; modifying AGPL server components that serve network users triggers copyleft obligations that conflict with commercial product distribution models.

**RHOAI relevance:** Low for adoption; Medium as pattern. OpenViking's filesystem-paradigm context organization, L0/L1/L2 tiered loading, and directory recursive retrieval are the most architecturally novel contributions in this survey update. The self-evolution mechanism (agents rewriting their own skills) is technically impressive but governance-uncontrolled. **The AGPL-3.0 license is a hard blocker for productization** — RHOAI cannot ship or modify OpenViking as part of a commercial product without triggering copyleft obligations. The viable path is pattern extraction: study the architecture, implement similar concepts under Apache 2.0 in MemoryHub or a future RHOAI-native memory service.

---

### 2.8 MemPalace

**REFERENCE** — MemPalace is an open-source long-term memory system for AI agents, released April 5, 2026 by Milla Jovovich and developer Ben Sigman. MIT License. GitHub: 55,400+ stars and 7,200+ forks as of June 2026 — among the fastest-growing AI developer tools on GitHub (~36K stars in the first 5 days). No venture funding publicly disclosed; celebrity-driven growth trajectory (stars measure attention, not enterprise adoption). Built on the ancient "Method of Loci" (memory palace) metaphor.

**Architecture — verbatim storage with spatial metaphor:** MemPalace's core design principle is contrarian: store all conversations verbatim and permanently, never summarize or delete originals, invest in retrieval quality rather than extraction intelligence. The founding insight: "Why should AI decide what I need to remember?"

The spatial hierarchy has six levels:
- **Wings** (top) — major containers for people/projects
- **Rooms** (mid) — topic-specific categories
- **Halls** (mid) — memory type classification (facts, events, preferences)
- **Closets** (bottom) — compressed summaries
- **Drawers** (bottom) — verbatim originals, permanently stored and never modified
- **Tunnels** (cross-link) — references connecting rooms

**Tiered retrieval (similar to OpenViking's L0/L1/L2):** Four retrieval layers minimize token usage at session start:

| Layer | Token Cost | Behavior |
|---|---|---|
| **L0** | ~50 | Core identity, always loaded |
| **L1** | ~120 | Critical facts, always loaded |
| **L2** | Variable | Room-specific, loaded on topic detection |
| **L3** | Variable | Full semantic search, on-demand |

Startup cost is approximately 170 tokens — significantly lower than systems that front-load context.

**Tech stack:** ChromaDB (default vector store), SQLite (metadata + knowledge graph with temporal entity tracking), Python 3.9+. Alternative backends: `sqlite_exact` (local), Qdrant REST (remote), pgvector/PostgreSQL (remote). Embedding models: `embeddinggemma-300m` (multilingual, recommended) or `all-MiniLM-L6-v2` (English-only).

**Benchmarks:**

| Mode | LongMemEval Score | Notes |
|---|---|---|
| Raw (no API) | **96.6%** | Local-only, verbatim retrieval — highest local-only result on LongMemEval |
| Hybrid (Claude Haiku reranking) | 100% (claimed) | **Overfitting concern:** targeted fixes for 3 specific failing questions, retested on same dataset. Held-out score: 98.4%. The 96.6% raw score is the credible metric. |
| With AAAK compression | 84.2% | 12.4-point regression; "lossless" compression claim contradicted by benchmark data |

**Independent analysis (arXiv:2604.21284; Gamgee blog):** The headline retrieval performance is attributable primarily to the verbatim storage philosophy combined with ChromaDB's default embedding model, rather than the spatial organizational metaphor. The palace structure (wings, rooms, halls) is not involved in the benchmark scoring path. As the Gamgee analysis notes: "The headline number measures how well ChromaDB's default embedding model performs on verbatim text retrieval."

**Framework integrations:** 29 MCP tools (compatible with any MCP client); Claude Code (auto-save hooks, `.claude-plugin`); OpenAI Codex; Gemini CLI; Ollama Cloud. MCP server mode runs over stdio.

**Deployment:** Local-first by default ("nothing leaves your machine unless you opt in"). Docker containers (CPU and GPU variants). Optional remote backends (Qdrant, pgvector) require explicit opt-in. Namespace isolation available on Qdrant and pgvector backends for multi-tenant deployments.

**Governance posture:** None. No audit trail, RBAC, retention/erasure primitives, or compliance features documented. Local filesystem is the trust boundary. Namespace isolation on remote backends is the only multi-tenancy mechanism. Security policy published (SECURITY.md) but no enterprise governance features.

**Limitations for enterprise consideration:**
- **Linear storage scaling** — every conversation stored permanently; heavy users generate gigabytes
- **No semantic consolidation** — redundant mentions (e.g., 50 references to the same preference) remain as separate chunks rather than being merged
- **Phrasing-dependent retrieval** — vector similarity must bridge vocabulary gaps between queries and stored text
- **Weak structured query support** — aggregation queries (e.g., "list all preferences") require searching across many documents rather than querying structured data
- **Celebrity-driven adoption signal** — 55K+ GitHub stars partly reflect distribution reach; no verified enterprise production deployments documented

**Comparison with other verbatim/tiered approaches in this survey:**

| Dimension | MemPalace | OpenViking | Letta |
|---|---|---|---|
| **Storage philosophy** | Verbatim-first: store everything, never delete | Filesystem-paradigm: hierarchical directories | OS-inspired: core/recall/archival tiers |
| **Token optimization** | L0/L1/L2/L3 tiered retrieval (~170 token startup) | L0/L1/L2 tiered loading (up to 96% savings) | Core memory in-context, archival on-demand |
| **Retrieval** | ChromaDB vector search + knowledge graph | Directory recursive traversal | Tool-call-based archival access |
| **License** | MIT | **AGPL-3.0** | Apache 2.0 |
| **Governance** | None | None | Thin |

**RHOAI relevance:** Low for adoption; Medium as pattern. MemPalace's verbatim storage philosophy — "store everything, invest in retrieval" — is a counterpoint to the extraction-based approaches (Mem0, CrewAI cognitive memory) that dominate the field. The 96.6% LongMemEval result demonstrates that simple verbatim storage with good embeddings can outperform more sophisticated architectures on recall benchmarks. The tiered retrieval model (170-token startup) is worth studying alongside OpenViking's L0/L1/L2 approach. However, MemPalace has no enterprise governance, no multi-tenant support beyond namespace isolation, and its linear storage scaling makes it unsuitable for enterprise multi-agent deployments. The spatial metaphor (wings/rooms/halls) is a UX innovation but is not involved in the retrieval scoring path — the benchmark performance comes from ChromaDB + verbatim storage, not the palace structure.

---

## 3. Enterprise Platform Memory Features

### 3.1 Oracle AI Agent Memory

**REFERENCE** — Oracle AI Agent Memory (`oracleagentmemory`, PyPI) is an enterprise Python SDK providing a governed memory substrate on top of Oracle AI Database. Announced May 1, 2026 (Richmond Alake blog post). Oracle AI Database combines relational, vector, and graph access in a single engine. The SDK is available publicly; the database backend requires Oracle AI Database (Oracle 23ai).

**Architecture:** Oracle's central argument — detailed in doc 01 — is that the four memory types (working, semantic, episodic, procedural) are not four systems but four access patterns over one governed substrate. Key implementation details:

- **Short-term threads** with automatic summarization and "context cards"
- **Long-term durable memories** with vector search and LLM-based extraction
- **Per-record scoping fields:** user, agent, thread, timestamp — enabling per-record audit and erasure
- **Multi-tenant isolation** enforced at the store layer, not the application layer
- **Framework-agnostic client:** same `OracleAgentMemory` instance used across LangGraph, Claude Agent SDK, OpenAI Agents SDK, WayFlow

**Benchmarks (from Oracle blog, which returned HTTP 403; figures via search summaries — see Sources):**
- LongMemEval: 93.8% overall (469/500); 100% single-session recall; 96% temporal reasoning; 95% knowledge-update; 88% multi-session
- Token efficiency: 80-turn conversation held at ~1,300 tokens/request vs ~13,900 for flat history (9.5x)
- Quality: judged winner 48:13 over flat-history baseline (19 ties)

These are the strongest governance-oriented benchmark results in this survey. Caveats: vendor-published, Oracle blog was not fetchable (403), figures are from web search summaries and the internal seed document (`docs/knowledge-review/assets/agent-memory-knowledge.md`). Independent validation not found in public sources.

**Governance posture:** The most mature of any external solution surveyed — per-record audit/erasure, multi-tenant isolation enforced at the database layer, thread/user/agent scoping on every record. Directly addresses GDPR and HIPAA erasure requirements.

**Lock-in concern:** Requires Oracle AI Database (Oracle 23ai). This is a hard dependency on proprietary Oracle infrastructure. For RHOAI, which targets OpenShift on any hardware and air-gapped deployments, Oracle Database is not a viable backend. The architectural pattern is the value; the implementation is not portable.

**RHOAI relevance:** Medium for architecture learning; Not adoptable as-is. Oracle's "four access patterns over one substrate" argument is the strongest external validation for a unified memory substrate approach on RHOAI. The per-record governance model should be studied for RHOAI's memory primitive design. The database backend should be replaced with PostgreSQL + pgvector (as MemoryHub already does).

---

### 3.2 AWS Bedrock AgentCore Memory

**REFERENCE** — AWS launched AgentCore Memory as a fully managed service within the Bedrock AgentCore suite. The Memory type definitions became publicly documented in late 2025; episodic memory functionality reached GA in early 2026; streaming notifications for long-term memory added March 2026.

**Architecture:** Two primary memory types:
- **Short-term memory (sessions):** Stores raw interaction events via `CreateEvent` API; supports metadata filters on events; sessions identified by `sessionId`. Provides continuity across service restarts.
- **Long-term memory (records):** Asynchronous extraction pipeline runs in the background after events are stored; extracts summaries, facts, preferences into durable memory records; semantic search via `RetrieveMemoryRecords`.

**Episodic memory (GA 2026):** Structured episodes capturing context, reasoning, actions, outcomes; a secondary agent analyzes episode patterns to improve future decision-making. This is the most explicit episodic learning feature of any hyperscaler offering.

**Governance:** KMS encryption at rest and in transit; customer-managed KMS keys supported; streaming notifications for change events. No documented audit trail, retention policies, or erasure primitives in public documentation as of survey date.

**Cloud-only:** No on-premises option. AgentCore runs in AWS regions only (preview limited to five regions as of April 2026 documentation). This is disqualifying for RHOAI's on-premise and air-gapped deployment targets.

**Signal value:** AWS's investment validates that managed memory is a product feature — not an infrastructure concern for individual application teams. The two-tier model (raw sessions + extracted long-term records) maps cleanly to the working/episodic split in the CoALA taxonomy and is a simple, deployable reference architecture.

**RHOAI relevance:** Low for adoption; High as signal. The two-tier managed memory model is a straightforward reference for RHOAI's own memory primitive design.

---

### 3.3 Google Vertex AI Memory Bank

**REFERENCE** — Google's Memory Bank (part of Vertex AI Agent Engine / Gemini Enterprise Agent Platform) reached GA for sessions and memory on January 28, 2026 (memory events charged at $0.25 per 1,000 at that point). "Memory Profiles" feature added in 2026 for high-accuracy, low-latency recall.

**Architecture:** Memory Bank integrates with Agent Engine Sessions. During active sessions, conversation history is stored via Agent Engine. After sessions, Gemini models asynchronously extract key facts, preferences, and context to generate structured memories. Memory Profiles enable agents to recall high-accuracy details quickly.

**Integration:** Designed around Google's Agent Development Kit (ADK). Framework agnostic in principle; practically tightest integration with ADK/Google ecosystem.

**Governance:** Google Cloud IAM, VPC Service Controls, Cloud Audit Logs, Threat Detection via Security Command Center. These are platform-level governance features, not memory-specific ones — they apply to all Vertex AI services.

**Cloud-only:** Google Cloud only, same disqualification as AWS for RHOAI on-premise requirements.

**RHOAI relevance:** Low for adoption; Medium as signal. Memory Profiles (high-accuracy, low-latency retrieval from structured memory) is a feature pattern worth noting. The Google offering demonstrates that memory is now a GA platform feature at all major hyperscalers, validating the market timing for RHOAI.

---

### 3.4 OpenAI Server-Side Memory and Compaction

**REFERENCE** — OpenAI has two distinct memory mechanisms, both server-side:

**User-facing memory** (available to free/paid users): Automatic conversation summarization carried across sessions. Opaque to users; raw stored memories are not accessible for inspection. This is the consumer product, not relevant to RHOAI.

**Responses API compaction (launched Feb 11, 2026):** Server-side compaction triggered when context crosses a configured `compact_threshold`. Two modes:
- Inline compaction: runs automatically in-stream when threshold is crossed; returns a compressed, encrypted state artifact
- Standalone `/responses/compact`: explicit developer-controlled trigger

The key technical claim: GPT-4.1 and above are specifically fine-tuned to produce and consume these compressed state artifacts — making it trained behavior, not just truncation. Triple Whale reported handling a 5 million token session over 150 tool calls without accuracy degradation after enabling compaction.

**Governance:** The compaction artifact is opaque and not human-interpretable. This is by design (efficient, model-internal representation) but is the opposite of RHOAI's governance requirement that compacted memory be inspectable (MemoryHub uses human-readable summaries explicitly for compliance inspection). **Contradiction with RHOAI direction:** OpenAI's opaque compaction is optimal for performance but cannot satisfy compliance inspection requirements.

**RHOAI relevance:** Low for adoption. The compaction trigger threshold model is relevant to context engineering design. The inspectability tradeoff is a direct design constraint RHOAI must decide on: optimized-opaque vs. compliant-readable.

---

### 3.5 Anthropic Claude Dreaming

**REFERENCE** — Anthropic shipped "dreaming," outcomes, and multiagent orchestration for Claude Managed Agents on May 6, 2026 (Code with Claude event). Currently a research preview.

**How it works:** A scheduled background process (configurable interval: hourly, nightly, custom) that:
1. Reviews recent session transcripts and event logs
2. Compares against existing memory store
3. Prunes stale entries, merges duplicates, resolves contradictions
4. Writes a reorganized memory layer
5. Presents the updated memory for human review (approve/reject/modify) before agents adopt it

Source sessions are preserved untouched during consolidation. The output is CLAUDE.md-style structured files, not opaque artifacts.

**Governance gate:** The human approval gate before memory deployment is a meaningful governance control — it is what distinguishes Dreaming from OpenAI's opaque compaction architecturally. Teams can review, reject, or modify memory updates before they take effect.

**Vendor concern (VentureBeat analysis, URL returned 429):** Multiple analysts have noted that Anthropic's move to own memory, evals, and orchestration simultaneously creates a strong lock-in vector. Claude Managed Agents is Anthropic infrastructure only; the Dreaming feature is not available for self-hosted or third-party deployments.

**Enterprise signal from Harvey (legal AI):** Task completion rates increased roughly 6x after implementing Dreaming — the most concrete ROI signal for sleep-time memory consolidation in this survey. (Source: Anthropic's Code with Claude launch announcement, May 6, 2026; this is Anthropic's own published figure, not an independent Harvey publication or third-party benchmark.)

**RHOAI relevance:** Low for adoption (Anthropic Managed Agents cloud only). High as pattern signal: the sleep-time consolidation pattern (off-line memory reorganization with human governance gate) is directly relevant to RHOAI's memory primitive design. MemoryHub's planned "promotion pipeline" serves a similar function. The governance gate model (approve/reject before deployment) is worth incorporating into RHOAI's memory primitive design.

---

## 4. Framework-Native Memory

### 4.1 LangGraph / LangMem

**REFERENCE** — LangGraph (Apache 2.0; LangChain ecosystem) is the most widely adopted open-source agent framework (97K+ stars on the `langchain-ai/langchain` repo; the `langchain-ai/langgraph` repo carries its own separate star count — the 97K figure reflects ecosystem breadth, not the LangGraph repo specifically). LangMem is LangChain's dedicated long-term memory SDK layered on top of LangGraph's storage infrastructure.

**LangGraph memory model:**
- **Short-term (thread-scoped):** Conversation state managed within a thread via LangGraph's state machine; handled automatically by the graph execution engine
- **Long-term (cross-thread):** LangGraph Stores — JSON documents organized by namespace and key, persistent across threads via pluggable backends (InMemoryStore for development; PostgresStore, Redis, MongoDB for production)

**LangMem (launched as SDK, current status beta-adjacent):**
- Hot-path memory: `create_manage_memory_tool` and `create_search_memory_tool` — agents actively manage memory during conversations
- Background processing: Memory manager that automatically extracts, consolidates, and updates knowledge between sessions
- Storage-backend agnostic: functional primitives work with any storage system

**Performance note:** LangMem p95 latency is 59.82 seconds (background processing) — suitable only for batch/async workloads, not interactive agents. For interactive production agents, the recommendation is to use a dedicated memory service (Mem0 at 0.200s p95) rather than LangMem's inline extraction. This is a significant operational limitation for production deployments.

**Governance:** LangSmith Enterprise tier adds RBAC and workspaces; LangSmith is the deployment and observability platform (formerly LangGraph Platform). The underlying LangGraph storage is developer-managed — governance is the application team's responsibility.

**RHOAI relevance:** High. LangGraph is a target framework in RHAISTRAT-1345. LangGraph's memory model (thread-scoped short-term + cross-thread long-term via Stores) defines the memory abstraction that LangGraph-using teams on RHOAI will expect. RHOAI's memory primitive must be compatible with — or superior to — LangGraph's native Store interface. LangMem's hot-path/background split is a useful model for RHOAI's memory architecture planning. The 59-second p95 latency for background extraction reinforces the need for dedicated memory infrastructure rather than inline framework-based extraction.

---

### 4.2 CrewAI Memory

**REFERENCE** — CrewAI (Apache 2.0; 44,600+ GitHub stars, 450M+ monthly workflows) redesigned its memory system from scratch in 2025, focusing on what they describe as a "cognitive process" rather than a database with a search layer.

**Architecture:** CrewAI's unified Memory class replaced separate short-term, long-term, entity, and external memory types. Key features:
- **LanceDB** as the embedding/vector database backend
- **SQLite3** for long-term structured persistence across runs
- **Cognitive consolidation:** When saving new content, the encoding pipeline checks for similar existing records (similarity threshold 0.85 default); LLM decides whether to keep/update/delete/merge
- **Purposeful forgetting:** Memory is designed to forget on purpose — not just accumulate
- Storage configurable via `CREWAI_STORAGE_DIR`

The consolidation model (selective encoding, contradiction resolution, purposeful forgetting) is conceptually aligned with how human memory works and is more sophisticated than simple append-write approaches.

**Governance:** OSS tier: local only (SQLite + LanceDB); no access controls, audit, or multi-tenancy. CrewAI Enterprise tier: SOC2 Type 2, HIPAA compliance — but these are platform-level credentials, not memory-specific governance features.

**RHOAI relevance:** Medium. CrewAI is one of the target frameworks in RHAISTRAT-1345. The cognitive consolidation model (selective encoding, contradiction resolution, purposeful forgetting) is an architectural pattern RHOAI's memory primitives should evaluate. The OSS tier's local-only SQLite storage is incompatible with enterprise multi-agent sharing requirements — reinforcing the need for a server-side, shared memory service.

---

### 4.3 OpenClaw

**REFERENCE** — OpenClaw (MIT License; github.com/openclaw/openclaw) is an open-source, personal AI assistant framework. Launched in late January 2026; crossed 250,000 GitHub stars within 60 days of launch (surpassing React and Linux as of March 3, 2026); 370,000+ stars and 500+ contributors as of survey date. Growth was extraordinary — 9,000 stars on launch day, 60,000 within three days, 190,000 within two weeks. Chinese technology companies including Tencent and Z.ai have announced OpenClaw-based services. No venture funding publicly disclosed; MIT-licensed and community-driven with no single commercial owner. Adoption signals are primarily in the individual developer and small-team market; no documented enterprise deployments of the memory subsystem specifically.

**Note on star count:** The growth trajectory and absolute star count are based on multiple web sources referencing a March 2026 data point; they have not been independently verified against the live GitHub counter. Star inflation from bots or campaigns cannot be ruled out for a project with this unusual growth curve. The figures are cited as reported, not as independently confirmed.

**Architecture — client-side, file-based memory:** OpenClaw's memory model is explicitly client-side. The agent stores state as plain Markdown files in its local workspace (`~/.openclaw/workspace`). There is no hidden remote state; the documentation states: *"The model only 'remembers' what gets saved to disk — there is no hidden state."* This makes memory human-readable, directly editable, and trivially auditable by a developer — but it is not a server-side governed store.

The three-tier file structure is:
1. **`MEMORY.md`** — Durable, curated long-term facts and preferences; loaded at the start of every private session
2. **`memory/YYYY-MM-DD.md`** — Daily working notes, session context, and raw observations (append-only; today's and yesterday's logs auto-loaded)
3. **`DREAMS.md`** — Optional consolidation diary written during background dreaming passes

This is consistent with doc 01's description: "Memory is stored as plain Markdown files in the agent's workspace. The documentation explicitly states there is no hidden remote state: 'The agent remembers only what persists to disk in its workspace.'"

**Hybrid retrieval — 70% vector / 30% BM25:** When an embedding provider is configured, `memory_search` applies hybrid search combining two retrieval signals:
- **Vector similarity (70% weight):** Semantic search via chunk embeddings stored in a per-agent SQLite file (`~/.openclaw/memory/<agentId>.sqlite`); optional `sqlite-vec` extension for in-database vector distance; fallback to in-process JavaScript cosine similarity
- **BM25 keyword search (30% weight):** Lexical matching for exact tokens — IDs, environment variable names, error strings, code symbols — where semantic similarity fails

Scoring formula: `finalScore = 0.7 * vectorScore + 0.3 * (1 / (1 + max(0, bm25Rank)))`. Files are chunked at ~400 tokens with 80-token overlap; a file watcher marks the index dirty and sync runs asynchronously on session start, search calls, or at intervals.

Post-processing includes MMR re-ranking (balances relevance with diversity, λ default 0.7) and temporal decay (exponential score decay, configurable half-life defaulting to 30 days; `MEMORY.md` and non-dated files never decay — they are treated as evergreen).

**Embedding backends:** Auto-selection hierarchy: local GGUF model (default `ggml-org/embeddinggemma-300m-qat-q8_0`, ~0.6 GB, auto-downloaded) → OpenAI → Gemini → Voyage → Mistral. Custom OpenAI-compatible endpoints supported. When no embedding provider is configured, memory search falls back to BM25 keyword-only.

**Alternative backends:** Four backend options — builtin SQLite (default, no extra dependencies), QMD (local-first sidecar with BM25 + reranking + query expansion, macOS/Linux/WSL2), Honcho (cross-session AI-native server with user modeling), LanceDB (bundled plugin with auto-recall). The Honcho and LanceDB backends shift parts of the memory layer server-side; the core architecture remains client-driven.

**Context compaction integration:** OpenClaw triggers an automatic memory flush before context compaction, prompting the agent to write durable memories before the context window is compacted. This is the same sleep-time consolidation pattern as Anthropic's Dreaming and Letta's sleep-time compute — implemented inline within the client-side framework.

**Deployment:** Primarily local. Official Kubernetes documentation exists (`docs.openclaw.ai/install/kubernetes`); community Kubernetes operator (`openclaw-rocks/k8s-operator`) provides production-grade deployment with network isolation, secret management, persistent storage, and health monitoring. Red Hat Developer content documents deploying OpenClaw on OpenShift with SPIFFE/SPIRE identity injection, OpenTelemetry tracing, MCP Gateway tool governance, and container-level sandboxing — without modifying agent code.

**Governance posture:** None in the OSS core. The filesystem is the trust boundary; whoever has filesystem access can read, edit, or delete all memory. Channel-level access policies control which sessions can access QMD search. No audit trail, retention/erasure primitives, RBAC, or multi-tenancy in the core framework. An enterprise deployment pattern documented in third-party guides implements a three-role RBAC model (Admin/Developer/Auditor) with 90-day audit log retention meeting ISO 27001 requirements — but this is a community integration pattern, not a built-in framework capability.

**Contradiction to flag — adoption signal vs. governance maturity:** OpenClaw's GitHub growth rate is anomalous. The project accumulated more stars in 60 days than React did in 10 years, per multiple sources. However, star counts do not translate directly to enterprise adoption, and no verified enterprise production deployments of the memory subsystem are documented in primary sources. The signal value for RHOAI is architectural (client-side hybrid search pattern) rather than market (adoption volume).

**RHOAI relevance:** Medium as pattern. OpenClaw is the canonical reference for the client-side hybrid memory model (70% vector / 30% BM25) that doc 01 uses as a named example of the client-side memory pattern. This pattern is relevant to RHOAI for developer-workflow and IDE-embedded agents — contexts where a lightweight, self-contained memory layer is more appropriate than a full server-side memory service. The community OpenShift deployment pattern demonstrates that OpenClaw can run on RHOAI's platform; however, the OSS core has no enterprise governance, no multi-tenant isolation, and no audit primitives. For platform-tier enterprise use cases, the client-side model is insufficient; OpenClaw reinforces rather than challenges the case for a server-side governed memory service.

---

### 4.4 Microsoft GraphRAG

**REFERENCE** — Microsoft GraphRAG (MIT license; github.com/microsoft/graphrag) is a framework for knowledge graph construction from document corpora, designed to improve RAG performance on complex sensemaking tasks.

**How it works:** At index time, GraphRAG reads all documents and builds a knowledge graph of entities, relationships, and community clusters. Cross-document reasoning happens during indexing rather than at query time. At query time, the graph structure enables multi-hop retrieval that pure vector search cannot support.

**Performance (from Microsoft Research and practitioner analysis):**
- 26% improvement in answer comprehensiveness vs. standard vector RAG
- 57% improvement in response diversity
- GraphRAG wins 70-80% of complex sensemaking tasks vs. baseline RAG

**Cost concern (updated for LazyGraphRAG):** Full GraphRAG's indexing cost — entity extraction, relationship mapping, and community summarization — was historically $50–200 for moderate corpora and up to $33K for very large datasets (2024), a prohibitive 10–40x premium vs. standard vector RAG. Microsoft's **LazyGraphRAG** (released late 2024, production-ready June 2025) removes this barrier at moderate scale: it defers all pre-summarization, using NLP noun-phrase extraction instead, bringing indexing costs to **0.1% of full GraphRAG** and to parity with vector RAG (~$20–50 for corpora that previously cost $50–200). The prohibitive indexing cost framing now applies only to full GraphRAG on *large* enterprise corpora; LazyGraphRAG has largely resolved the cost objection at moderate scale.

**2026 practitioner consensus (from community analysis):** "vectors for semantic entry-point retrieval, graphs for relational depth." The question is no longer "GraphRAG or vector RAG?" but query routing — which method does this specific query need?

**RHOAI positioning:** GraphRAG is most relevant to Peter's area 1 (Agent Knowledge — org-wide knowledge graph) rather than operational agent memory (area 2). It is a document-corpus-level technology (large-scale, batch-indexed) not a session-state technology (append-heavy, dynamic). MemoryHub uses PostgreSQL + pgvector for both vector and graph queries rather than a standalone GraphRAG pipeline — a simpler operational model.

**RHOAI relevance:** Medium as pattern. Microsoft GraphRAG's entity-relationship extraction approach informs knowledge graph construction for the "Agent Knowledge" layer. The indexing cost must be factored into any production design. Neo4j's Graphiti integration with GraphRAG (documented separately) is a more recent and more agentic-memory-focused implementation.

---

## 5. Red Hat MemoryHub

**REFERENCE** — MemoryHub is an Apache 2.0 prototype built by the Red Hat AI Americas team (associated with Wes Jackson, Red Hat SSA). Status as of April 2026: core operations, auth, dashboard, SDK, and cache-optimized assembly are production-capable; Kubernetes operator and curator background agent are on roadmap.

MemoryHub receives the highest RHOAI relevance rating in this survey because it is the only solution that combines:
- OpenShift-native deployment (UBI images, FIPS delegation, air-gap deployable)
- Enterprise governance posture (five-tier scope isolation, contradiction detection, PII scanning, EU AI Act / GDPR / HIPAA compliance design)
- Standard interface (MCP streamable HTTP — compatible with any MCP client)
- Unified backend (PostgreSQL + pgvector for relational, vector, and graph queries)

MemoryHub's detailed architecture and governance model are covered in [MemoryHub Deep-Dive](03-memoryhub-deep-dive.md). This survey registers MemoryHub as the strongest available Red Hat reference design without repeating its full analysis here.

---

## 6. Investment and Market Signal

**REFERENCE** — The following funding figures are sourced from news coverage and press releases; see Sources section.

| Company | Amount | Round | Date | Lead Investor |
|---|---|---|---|---|
| **Mem0** | $24M | Series A | 2025 | Basis Set Ventures |
| **Interloom** | $16.5M | Seed | March 2026 | DN Capital |
| **Cognee** | €7.5M (~$8M) | Seed | Feb 2026 | Pebblebed |
| **Supermemory** | $2.6M | Seed | Oct 2025 | Susa Ventures, Browder Capital, SF1.vc (co-led) |
| **Letta** | $10M | Seed | Sept 2024 | Felicis Ventures |
| **Zep** | $500K | YC batch | April 2024 | Y Combinator |

Total confirmed investment in pure-play agent memory startups: approximately $62M, aligned with Wes Jackson's "$60M+ in 18 months" estimate from May 2026 (the slight variation reflects rounding and conversion). Bessemer Venture Partners' identification of the memory layer as a 2026 differentiation frontier is corroborated by this funding concentration.

**Contradiction to flag — market fragmentation risk:** With five or more venture-backed startups competing on similar technical approaches (vector + graph + BM25 hybrid retrieval, temporal tracking, multi-scope isolation), consolidation is likely. Platforms adopting any single startup's memory service risk picking a non-survivor. This strengthens the case for RHOAI to build a standards-based, infrastructure-level memory primitive rather than integrating a specific startup product.

---

## 7. Benchmark Summary and Caveats

**REFERENCE** — The following benchmark data is compiled from vendor-published and peer-reviewed sources. Not all figures are directly comparable (different test configurations, model versions, evaluation sets).

| Solution | LongMemEval | Notes / Caveats |
|---|---|---|
| **Oracle AI Agent Memory** | 93.8% | Vendor-published; Oracle blog 403; figures from seed doc and search summaries. Multi-session 88% is the weak category. |
| **Mem0 (v2 algorithm)** | 93.4% | Vendor-published (Mem0 blog, April 2026). BEAM 10M = 48.6% — significant degradation at scale. |
| **Zep (gpt-4o)** | 71.2% | Peer-reviewed paper (arXiv:2501.13956). Different model config than Oracle/Mem0 — not directly comparable. |
| **MemPalace** | 96.6% | Vendor-published; highest local-only result. 100% hybrid claim has overfitting concerns (held-out: 98.4%). Performance attributable to verbatim storage + ChromaDB embeddings, not spatial metaphor. |
| **Supermemory** | 85.4% (LongMemEval-S) | Vendor-claimed; LongMemEval-S is a variant, not the full benchmark. |

**Structural caution:** Mem0 and Oracle publish their own benchmark results on their own infrastructure with their chosen model configurations. Until a neutral third party publishes a controlled comparison, treat all benchmark comparisons as directional, not definitive. The Zep result is from a peer-reviewed arXiv paper (the only peer-reviewed benchmark in this list) and is therefore the most methodologically reliable — but it is also the oldest configuration.

The most important benchmark signal for RHOAI is the multi-session degradation pattern: Oracle 88%, Mem0 10M-scale BEAM 48.6%. Multi-session, multi-agent, and large-corpus scenarios — the exact scenarios that matter for enterprise RHOAI workloads — are consistently the hardest category across all solutions.

---

## 8. Gaps and Implications for RHOAI

**EXPLORATORY** — The following gap analysis synthesizes cross-solution findings. These are research observations, not design decisions.

### Gap 1: No solution combines enterprise governance with Kubernetes-native deployment

Oracle has the best governance posture but requires Oracle Database (proprietary, no Kubernetes-native path). AWS and Google have managed memory as a GA product but are cloud-only. Mem0 has the best open-source deployment flexibility but thin governance. Zep has the best temporal knowledge graph but deprecated its self-hosted offering. **No existing solution provides enterprise governance + self-hosted Kubernetes-native + open standard interface.** This is RHOAI's whitespace.

### Gap 2: No standard memory interface or protocol exists

MCP serves as a transport layer (MemoryHub, Mem0 OpenMemory, Supermemory all expose MCP servers) but there is no standardized MCP schema for memory operations (read, write, search, delete, manage, audit). Every solution implements its own API. A standard memory schema — even an informal one — would reduce integration friction for framework authors. RHOAI could propose one through the MCP ecosystem, aligned with RHAISTRAT-1345's acceptance criterion for cross-framework memory abstractions. (See [05 Standards & Protocols](05-standards-and-protocols.md).)

### Gap 3: Opaque vs. inspectable compaction is a design fork

OpenAI's compaction is opaque and optimized; Anthropic's Dreaming is inspectable and governed; MemoryHub's compaction uses human-readable summaries explicitly for compliance. This is not a matter of preference — it is a regulatory requirement gap. For RHOAI (EU AI Act enforcement August 2026, GDPR, HIPAA), opaque compaction is not compliant. RHOAI must adopt the inspectable compaction model. **This is the most concrete near-term architectural requirement that emerges from this survey.**

### Gap 4: Multi-session and multi-agent memory is the unsolved hard problem

Every benchmark shows multi-session performance as the lowest-scoring category. No solution has solved multi-session, multi-agent memory to enterprise reliability standards. This is where RHOAI's investment — if well-targeted — has the most differentiation potential.

### Gap 5: Agent Knowledge (org-wide graph) vs. operational memory (session state) remain architecturally unresolved

Oracle argues for one governed substrate; practitioners build vector stores (semantic search) + graph stores (entity relationships) + relational stores (structured facts) + session logs (episodic events) as four separate systems. No one has shipped a production system that unifies all four under a single governance model that also performs well. MemoryHub comes closest (PostgreSQL + pgvector enabling both vector and graph queries) but at smaller scale than enterprise-wide knowledge requirements. This unresolved question is the central design problem for RHOAI. (See [07 Taxonomy & Decomposition](07-taxonomy-and-decomposition.md) and [08 RHOAI & OCP Alignment](08-rhoai-ocp-alignment.md).)

### Gap 6: Context engineering as a measurable, tuneable platform primitive

Meta (progressive disclosure), Oracle (summarization threshold), Anthropic (compaction + Dreaming), and AWS (episode-based learning) all implement context engineering as a first-class measurable feature. RHOAI should treat context compaction not as a byproduct of memory but as a distinct platform primitive with defined quality metrics (token efficiency at quality threshold). This is already in RHAISTRAT-1345's acceptance criteria; the gap is that no current open-source tooling provides this as a measurable, platform-managed service.

### Gap 7: Market consolidation risk

Five or more venture-backed startups are converging on similar technical approaches. Enterprise teams that adopt specific startup products risk dependency on a potential non-survivor. RHOAI should architect its memory primitive layer to be backend-agnostic — supporting pluggable memory backends (Mem0-compatible, LangGraph Store-compatible, MemoryHub-native) rather than coupling to any single vendor.

---

## Sources

### Internal (Repository)

| Source | Type | Path / Reference |
|---|---|---|
| Agent Memory & Knowledge working doc | Internal seed document | `docs/knowledge-review/assets/agent-memory-knowledge.md` |
| Agent Memory & Knowledge: Landscape and Definitions | Sibling research document | `agent-memory/research/01-landscape-and-definitions.md` |
| Agent Registry Research: Agent Management Landscape | Style and depth reference | `agents/agent-registry/research/04-agent-management-landscape.md` |
| Competitive Landscape | Internal reference | `docs/knowledge-review/competitive/landscape.md` |
| RHAISTRAT-1345 | Jira Outcome | https://redhat.atlassian.net/browse/RHAISTRAT-1345 |
| MemoryHub prototype | Red Hat AI Americas, Apache 2.0 | https://github.com/redhat-ai-americas/memory-hub |
| Oracle AI Agent Memory (seed) | Richmond Alake, Oracle, 2026-05-01; blog returned 403 | blogs.oracle.com/developers/oracle-ai-agent-memory-a-governed-unified-memory-core-for-enterprise-ai-agents |
| When Agent Memory Becomes a Platform Concern | Wes Jackson (Red Hat SSA), 2026-05-01 | https://medium.com/@wjackson_63436/when-agent-memory-becomes-a-platform-concern-4b6cd23af47f |
| How We Built an AI Second Brain for 60K Knowledge Workers | Analytics at Meta, 2026-04-29 | https://medium.com/@AnalyticsAtMeta/how-we-built-an-ai-second-brain-for-60k-knowledge-workers-78c507dd795b |

### External — Vendor and Product Documentation

| Source | URL | Access Status |
|---|---|---|
| OpenViking GitHub repository (AGPL-3.0) | https://github.com/volcengine/OpenViking | Fetched successfully; license confirmed AGPL-3.0 (badge and LICENSE file) |
| OpenViking official site | https://openviking.ai/ | Search summary |
| OpenViking: ByteDance's Context Database for AI Agents | https://emelia.io/hub/openviking-context-database-ai-agents | Fetched successfully |
| ByteDance Volcengine Open-Sources OpenViking | https://www.toolmesh.ai/news/bytedance-volcengine-open-sources-openviking-ai-agents | Search summary |
| OpenViking: Context Database (a2a-mcp.org) | https://a2a-mcp.org/entry/openviking | Fetched successfully |
| OpenViking: The Context Database That Gives AI Agents a Real Brain | https://www.marcinsalata.com/en/2026/03/17/openviking-the-context-database-that-gives-ai-agents-a-real-brain/ | Search summary |
| Deploy OpenViking on OpenShift AI (Red Hat Developer) | https://developers.redhat.com/articles/2026/04/23/deploy-openviking-openshift-ai-improve-ai-agent-memory | Fetched successfully; note: references pre-AGPL Apache 2.0 license |
| OpenViking: Strategic Alternative to Pinecone | https://www.opentechhub.io/openviking/ | Search summary; includes AGPL license change details |
| OpenViking v0.2.15 release (license change) | https://newreleases.io/project/github/volcengine/OpenViking/release/v0.2.15 | Search summary; confirms AGPL-3.0 change |
| OpenViking PyPI package | https://pypi.org/project/openviking/ | Search summary |
| MemPalace GitHub repository (MIT) | https://github.com/MemPalace/mempalace | Fetched successfully; license confirmed MIT |
| MemPalace: 100% LongMemEval Benchmark (Gamgee blog) | https://gamgee.ai/blogs/mempalace-verbatim-memory-benchmark/ | Fetched successfully |
| MemPalace benchmarks (GitHub) | https://github.com/MemPalace/mempalace/blob/develop/benchmarks/BENCHMARKS.md | Search summary |
| Spatial Metaphors for LLM Memory: Critical Analysis (arXiv:2604.21284) | https://arxiv.org/html/2604.21284v1 | Search summary |
| MemPalace Review: Benchmark Claims vs Reality (Vectorize) | https://vectorize.io/articles/mempalace-review | Search summary |
| Mem0: State of AI Agent Memory 2026 | https://mem0.ai/blog/state-of-ai-agent-memory-2026 | Fetched successfully |
| Mem0 Series A announcement | https://mem0.ai/series-a | Search summary |
| Mem0 OpenMemory MCP | https://mem0.ai/blog/introducing-openmemory-mcp | Search summary |
| Letta: Agent Memory blog | https://www.letta.com/blog/agent-memory | Fetched successfully |
| Letta: Next Phase | https://www.letta.com/blog/our-next-phase | Fetched successfully |
| Letta: Announcing Letta | https://www.letta.com/blog/announcing-letta | Search summary |
| Zep: Agent Memory product page | https://www.getzep.com/product/agent-memory/ | Fetched successfully |
| Zep: Open Source Strategy announcement | https://blog.getzep.com/announcing-a-new-direction-for-zeps-open-source-strategy/ | Fetched successfully |
| Graphiti GitHub (Apache 2.0) | https://github.com/getzep/graphiti | Search summary |
| Cognee: Seed round announcement | https://www.cognee.ai/blog/cognee-news/cognee-raises-seven-million-five-hundred-thousand-dollars-seed | Fetched successfully |
| Cognee: AI Memory Architecture | https://www.cognee.ai/blog/fundamentals/how-cognee-builds-ai-memory | Search summary |
| Interloom: Seed announcement | https://interloom.com/en/blog/seed-announcement/ | Fetched successfully |
| Interloom: Fortune coverage | https://fortune.com/2026/03/23/interloom-ai-agents-raises-16-million-venture-funding/ | Search summary |
| Oracle AI Agent Memory: Detailed engineering post | https://vinish.dev/oracle-ai-agent-memory | 403 Forbidden |
| AWS AgentCore Memory types | https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/memory-types.html | Fetched successfully |
| AWS AgentCore Memory overview | https://aws.amazon.com/blogs/machine-learning/amazon-bedrock-agentcore-memory-building-context-aware-agents/ | Search summary |
| AWS AgentCore Memory streaming (March 2026) | https://aws.amazon.com/about-aws/whats-new/2026/03/agentcore-memory-streaming-ltm/ | Search summary |
| Google Vertex AI Memory Bank overview | https://docs.cloud.google.com/agent-builder/agent-engine/memory-bank/overview | Search summary |
| Google Memory Bank public preview | https://cloud.google.com/blog/products/ai-machine-learning/vertex-ai-memory-bank-in-public-preview | Search summary |
| OpenAI Responses API compaction | https://developers.openai.com/api/docs/guides/compaction | Search summary |
| OpenAI compaction launch coverage | https://aitoolly.com/ai-news/article/2026-02-11-openai-enhances-responses-api-with-server-side-compaction-hosted-shell-and-agent-skills-for-long-ter | Search summary |
| Anthropic Claude Dreaming (MindStudio) | https://www.mindstudio.ai/blog/what-is-claude-dreaming-anthropic-managed-agents | Fetched successfully |
| Anthropic Dreaming launch (Code with Claude 2026) | https://letsdatascience.com/blog/anthropic-dreaming-claude-managed-agents-self-improving-may-6 | Search summary |
| Anthropic: Dreaming introduces governed self-improvement | https://startupfortune.com/anthropics-dreaming-agents-introduce-governed-self-improvement-as-the-next-enterprise-battleground/ | Search summary |
| VentureBeat: Anthropic wants to own your agent's memory | https://venturebeat.com/orchestration/anthropic-wants-to-own-your-agents-memory-evals-and-orchestration-and-that-should-make-enterprises-nervous/ | 429 Too Many Requests |
| LangMem documentation | https://langchain-ai.github.io/langmem/ | Fetched successfully |
| LangChain long-term memory docs | https://docs.langchain.com/oss/python/langchain/long-term-memory | Search summary |
| CrewAI Memory documentation | https://docs.crewai.com/en/concepts/memory | Search summary |
| CrewAI: How we built Cognitive Memory | https://crewai.com/blog/how-we-built-cognitive-memory-for-agentic-systems | Search summary |
| OpenClaw GitHub repository (MIT License) | https://github.com/openclaw/openclaw | Fetched successfully |
| OpenClaw Memory documentation | https://docs.openclaw.ai/concepts/memory | Fetched successfully |
| OpenClaw Memory documentation (mirror) | https://openclaw-ai.com/en/docs/concepts/memory | Fetched successfully — source of 70%/30% weights and scoring formula |
| OpenClaw Kubernetes install docs | https://docs.openclaw.ai/install/kubernetes | Search summary |
| Red Hat Developer: Deploying OpenClaw on OpenShift | https://developers.redhat.com/videos/deploying-open-source-ai-agents-openshift-using-openclaw | Search summary |
| Red Hat blog: Operationalizing OpenClaw on Red Hat AI | https://www.redhat.com/en/blog/operationalizing-bring-your-own-agent-red-hat-ai-openclaw-edition | Search summary |
| OpenClaw enterprise deployment guide (community) | https://eastondev.com/blog/en/posts/ai/20260205-openclaw-enterprise-deploy/ | Search summary |
| OpenClaw Kubernetes operator (community) | https://github.com/openclaw-rocks/k8s-operator | Search summary |
| Medium: OpenClaw beats React GitHub record | https://medium.com/@aftab001x/openclaw-just-beat-reacts-10-year-github-record-in-60-days-now-nobody-knows-what-to-do-with-it-937b8f370507 | Search summary — star count figures sourced here; not independently verified against live GitHub counter |
| Microsoft GraphRAG GitHub | https://github.com/microsoft/graphrag | Search summary |
| Microsoft LazyGraphRAG announcement | https://www.microsoft.com/en-us/research/blog/lazygraphrag-setting-a-new-standard-for-quality-and-cost/ | Search summary — 0.1% indexing cost vs. full GraphRAG; production-ready June 2025 |
| Neo4j: Graphiti knowledge graph memory | https://neo4j.com/blog/developer/graphiti-knowledge-graph-memory/ | Search summary |

### External — Academic and Analysis

| Source | URL | Access Status |
|---|---|---|
| VikingMem: A Memory Base Management System for Stateful LLM-based Applications (arXiv:2605.29640; VLDB 2026) | https://arxiv.org/html/2605.29640v1 | Search summary; accepted by VLDB 2026 |
| Zep: Temporal Knowledge Graph Architecture (arXiv:2501.13956) | https://arxiv.org/html/2501.13956v1 | Fetched successfully |
| Supermemory TechCrunch funding coverage | https://techcrunch.com/2025/10/06/a-19-year-old-nabs-backing-from-google-execs-for-his-ai-memory-startup-supermemory/ | Search summary |
| Atlan: Best AI Agent Memory Frameworks 2026 | https://atlan.com/know/best-ai-agent-memory-frameworks-2026/ | Search summary |
| OSS Insight: Agent Memory Race 2026 | https://ossinsight.io/blog/agent-memory-race-2026 | Fetched successfully |
| newclawtimes: The Agent Memory Problem | https://newclawtimes.com/articles/agent-memory-problem-microsoft-oracle-mem0-persistent-state-enterprise/ | Search summary |

### Access Notes

The following sources returned HTTP errors; content was obtained via web search summaries:
- `blogs.oracle.com/developers/oracle-ai-agent-memory-...` — HTTP 403 (vendor blog)
- `vinish.dev/oracle-ai-agent-memory` — HTTP 403
- `venturebeat.com/orchestration/anthropic-wants-to-own-your-agents-memory...` — HTTP 429
