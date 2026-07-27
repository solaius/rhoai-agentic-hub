---
title: "Competitive landscape analysis (July 2026)"
description: Structured competitive analysis — hyperscaler and OSS memory framework comparison tables, positioning analysis, whitespace update, and series finding impact assessment.
timestamp: 2026-07-27
lens: competitive
review_after: 2026-10-27
---

# Competitive landscape analysis (July 2026)

**Series:** Document 21 of 22 — Agent Memory & Knowledge Research
**Type:** Standard-depth competitive lens
**Triggered by:** Accumulated competitive data across docs 02, 19, 20 now
warrants a consolidated comparison rather than incremental refresh notes.
Adel's positioning doc verification (doc 20) exposed factual errors that
need a clean, verified reference table.

**Methodology:** Web research across official product documentation,
vendor blogs, and secondary analysis sources (July 2026). All data points
carry confidence labels. Benchmark scores are vendor-claimed unless stated
otherwise.

---

## 1. Hyperscaler Platform Memory Comparison

The three major hyperscalers now all ship agent memory as a managed
platform feature. This table captures their state as of late July 2026.

| Dimension | Google Memory Bank | AWS AgentCore Memory | Microsoft Foundry Memory |
|---|---|---|---|
| **Status** | GA (Jan 28, 2026); Memory Revisions in preview [verified — Google Cloud docs] | GA; 15+ regions [verified — AWS docs] | **Public preview** (no GA date) [verified — Microsoft Learn, 2026-06-02] |
| **Memory types** | Sessions, Memory Bank (facts/preferences), Memory Profiles (structured schemas) [verified — Google Cloud docs] | Short-term (session events), long-term (extracted summaries/facts), episodic (outcomes) [verified — AWS docs] | User profile, chat summary, procedural (execution patterns) — all default-on [verified — Microsoft Learn] |
| **Auto-extraction** | Gemini-based async extraction [verified — Google Cloud docs] | Background extraction pipeline with configurable strategies [verified — AWS docs] | LLM-as-a-judge for procedural; standard extraction for user/chat [verified — Microsoft Foundry Blog] |
| **Scope model** | User-scoped with IAM conditions [verified — Google Cloud docs] | Actor/session/strategy; 10 indexed metadata keys [verified — AWS docs] | Up to 100 scopes per store, 10K memories/scope [verified — Microsoft Learn] |
| **Procedural memory** | No [verified] | No (episodic captures outcomes) [verified — AWS docs] | **Yes — first hyperscaler** [verified]. +7–14% Tau-bench [reported — vendor] |
| **Poisoning defense** | Model Armor integration [verified — Google Cloud Security docs] | No memory-specific defense [verified — AWS docs] | MemoryGuard — **guidance pattern, NOT product feature** [verified — MSFT Tech Community, 2026-06-21] |
| **Versioning/rollback** | **Memory Revisions (preview)**: immutable snapshots, 365-day TTL, enabled by default. No rollback [verified — Google Cloud docs, 2026-07-22] | Neither [verified — AWS docs] | Neither [verified — Microsoft Learn]. TTL + CRUD only |
| **Trust-aware retrieval** | No [verified] | Strictly consistent metadata (June 2026): up to 3 deterministic non-LLM keys [verified — AWS what's-new] | No (MemoryGuard is write-side) [reported — MSFT Tech Community] |
| **MCP support** | GA — Agent Platform remote MCP server [verified — Google Cloud docs] | GA — 122 MCP tools incl. memory ops [verified — AWS MCP server docs] | Foundry MCP Server GA (cloud, mcp.ai.azure.com) [verified — Microsoft Learn] |
| **Sandbox integration** | GKE Agent Sandbox (open-source add-on) — not integrated with memory [reported — Google Cloud Next '26] | Code Interpreter + Cloud Browser in Firecracker microVMs — not integrated with memory [verified — AWS docs] | Azure Container Apps sandbox — not integrated with memory [reported — Microsoft Learn] |
| **Storage** | Google-managed (not exposed) [verified] | AWS-managed; KMS with customer keys [verified — AWS docs] | Azure Cosmos DB (vector + full-text + hybrid) [verified — Cosmos DB blog] |
| **Deployment** | Google Cloud only [verified] | AWS only; 15+ regions [verified] | Azure only; 19 regions [verified — Microsoft Learn] |
| **Pricing** | $0.25/1K events; $0.30/GiB-month storage [verified — Google pricing] | $0.25/1K STM; $0.75/1K LTM (default) or $0.25 (custom); $0.50/1K retrievals [verified — AWS pricing] | Free during preview [verified — Microsoft pricing] |

### Key observations

1. **Google leads on inspectability.** Memory Revisions is the only
   hyperscaler feature shipping immutable version history — the property
   the series identifies as compliance-critical (findings 10, 13). Still
   preview, still no rollback.

2. **AWS leads on enterprise metadata.** Strictly consistent metadata is
   the first hyperscaler mechanism for deterministic (non-LLM) memory
   attributes — maps directly to compliance requirements (audit keys,
   tenant IDs, classification labels that must not be rewritten by
   extraction models).

3. **Microsoft leads on procedural memory.** First hyperscaler shipping
   learned execution patterns. Tau-bench gains are modest (+7–14%) but
   the capability category is new. MemoryGuard, while only guidance, is
   the most explicit memory-security framing from any hyperscaler.

4. **All three are cloud-only.** None offer self-hosted, on-premise, or
   air-gapped deployment. RHOAI's primary structural differentiation.

5. **No hyperscaler integrates memory with sandboxed execution.** AWS has
   the closest components (Code Interpreter + Memory) but they are not
   architecturally integrated.

---

## 2. OSS Memory Framework Comparison

| Dimension | Mem0 (post-v2.0) | Zep / Graphiti (post-SOC 2) | Letta (post-$10M) | Cognee (post-1.0) | MemPalace |
|---|---|---|---|---|---|
| **Architecture** | Single-pass extraction, hybrid retrieval (semantic + BM25 + entity linking) [verified — Mem0 docs] | Temporal knowledge graph (Graphiti); bi-temporal tracking (4 timestamps/fact) [verified — Zep docs] | OS-inspired: core/recall/archival. Sleep-time compute [reported — Letta blog] | ECL pipeline (Extract-Cognify-Load); self-improving graph [verified — Cognee docs] | Verbatim storage; spatial metaphor (wings/rooms/halls) [verified — MemPalace GitHub] |
| **License** | Apache 2.0 (OSS) + cloud + enterprise [verified] | Graphiti: Apache 2.0. Zep Cloud: proprietary. CE deprecated [verified] | Apache 2.0 [verified] | Apache 2.0 [verified] | MIT [verified] |
| **Self-hosted** | Yes — Docker + 20 backends; local OpenMemory MCP [verified — Mem0 docs] | Graphiti only — requires manual Neo4j/FalkorDB + LLM assembly. No turnkey [verified — Zep docs] | Yes — Letta Server (Apache 2.0) [verified] | Yes — Docker, Ollama, air-gap capable [verified — Cognee docs] | Yes — local-first (ChromaDB + SQLite) [verified] |
| **Graph memory** | Entity linking (v2.0, replaces Neo4j) [verified — Mem0 docs] | Core — bi-temporal graph, three subgraphs [verified — Zep docs] | Archival supports graph backends [reported — Letta docs] | Core — relational + vector + graph (Kuzu + LanceDB) [verified — Cognee docs] | Temporal entity graph in SQLite [verified — MemPalace GitHub] |
| **MCP support** | Yes — Plugin for AI Editors, 9 tools [verified — Mem0 docs] | No first-class MCP server [reported] | No first-class MCP server [reported] | Yes — cognee-mcp Docker image [verified — Cognee GitHub] | Yes — 36 MCP tools [verified — MemPalace GitHub] |
| **Governance** | Metadata filtering. No audit/erasure/retention in OSS [verified] | **SOC 2 Type 2, HIPAA, GDPR** (cloud only) [verified — Zep site] | Thin — sunsetting constraints for "frontier capabilities" [reported] | Ontology-based permissions, per-(user,dataset) isolation, OTEL [verified — Cognee docs] | None — filesystem trust boundary [verified] |
| **Benchmarks** | LongMemEval 93.4%, LoCoMo 91.6%, BEAM-10M 48.6% (vendor-claimed) | LongMemEval 71.2% (peer-reviewed, arXiv:2501.13956) | #1 Terminal-Bench (vendor-claimed) | BEAM-100K SOTA +6.5% (vendor-claimed) | LongMemEval 96.6% R@5 (vendor-claimed; verbatim attribution) |
| **Funding** | $24M Series A; 59K+ stars; AWS partnership [reported] | $500K YC; 28K+ stars; SOC 2 implies revenue [reported] | $10M seed (Felicis); 16K+ stars [reported] | EUR 7.5M seed (Pebblebed); 28.5K+ stars; 70+ deployments [reported] | No funding; 55K+ stars (celebrity-driven) [reported] |
| **Lock-in risk** | Low — swappable ~2 person-days [reported — secondary] | Medium-High — full platform SaaS-only; CE deprecated [verified] | **High** — agents run inside Letta; 2–6 week migration [reported — secondary] | Low — Apache 2.0, pluggable backends [verified] | Low — MIT, no cloud dependency [verified] |
| **RHOAI relevance** | **High** — deployment-flexible, MCP, 21 frameworks. Governance gap needs Red Hat layer | **Medium** — Graphiti temporal model distinctive; SOC 2 milestone; cloud-only platform | **Medium** — architecture reference value; product diverging from enterprise platform | **Medium-High** — graph-first, air-gap, MCP, ontology permissions. Closest self-hosted governance to MemoryHub | **Low** — no governance, pattern value only |

### Key observations

1. **Zep is the compliance leader** — SOC 2 + HIPAA + GDPR is a real
   barrier no other OSS framework has crossed. But the certified
   platform is cloud-only; self-hosted Graphiti carries no certifications.

2. **Cognee is the governance dark horse.** Apache 2.0, self-hosted,
   air-gap capable, ontology-based permissions, and MCP server. If its
   governance matures to include audit trails and retention policies, it
   becomes the most RHOAI-aligned OSS option after MemoryHub.

3. **Mem0 remains the deployment-flexible leader.** SDK v2.0 dropping
   Neo4j was significant. 59K+ stars, AWS partnership, and 21-framework
   compatibility give it the widest adoption surface.

4. **Letta is diverging.** The pivot to Letta Code (coding agent, not
   memory platform) means the memory layer is becoming an implementation
   detail. The 2–6 week migration estimate is a lock-in red flag.

5. **MemPalace is a benchmark artifact.** The 96.6% is attributable to
   verbatim storage + ChromaDB, not the spatial metaphor. 55K stars are
   attention, not enterprise adoption.

---

## 3. Competitive Positioning Analysis

### 3.1 Whitespace shift since May 2026

The whitespace (finding 4) has **narrowed but not closed**.

**What changed:**
- Google shipped Memory Revisions (preview) — first hyperscaler with
  immutable version history
- AWS shipped strictly consistent metadata — first deterministic
  (non-LLM) memory attributes
- Microsoft shipped procedural memory — first hyperscaler with learned
  execution patterns
- Zep earned SOC 2 + HIPAA + GDPR — first OSS framework with
  compliance certs
- Cognee 1.0 shipped with ontology permissions and air-gap deployment

**What has NOT changed:**
- No hyperscaler offers self-hosted or air-gapped deployment
- No OSS framework combines compliance certifications with self-hosted
- No solution ships rollback (Google has versioning, not rollback)
- No solution integrates memory governance with sandboxed execution

The whitespace is now more precisely: **governed, versioned,
rollback-capable memory + Kubernetes-native self-hosted + air-gappable +
open standard interface + sandbox-aware write governance**. Each
competitor has chipped at one or two requirements; the full combination
remains unserved.

### 3.2 The lock-in vector thesis

Adel's framing: hyperscalers use memory as invisible lock-in —
enterprises accumulate switching costs with every interaction.

Evidence supporting the thesis:
- **Google's Memory Revisions** create durable version history with no
  documented export mechanism
- **AWS's strictly consistent metadata** embeds enterprise taxonomy into
  memory records — harder to replicate elsewhere as they accumulate
- **Microsoft's procedural memory** captures institutional knowledge of
  how workflows operate in a proprietary format — no documented export
- **Anthropic's Dreaming** creates a self-improving layer only on
  Managed Agents — value compounds with sessions

RHOAI positioning response: **memory portability as a platform
primitive** — open storage format, export/import APIs,
backend-agnostic abstraction, no proprietary extraction format.

### 3.3 What "governance" means now

| Governance capability | Who has it (July 2026) | Status |
|---|---|---|
| Access controls / RBAC | Most solutions (platform-level) | Table stakes |
| Compliance certs (SOC 2, HIPAA) | Zep Cloud, hyperscaler platforms (inherited) | Differentiator for cloud; absent for self-hosted |
| Memory versioning / inspection | Google (Memory Revisions, preview) | Emerging — one provider |
| Deterministic metadata (non-LLM) | AWS (strictly consistent metadata) | Emerging — one provider |
| Write-path validation | Microsoft (MemoryGuard, guidance), Google (Model Armor) | Emerging — guidance/tooling, not built-in |
| Rollback | **Nobody** | Unserved |
| Audit trail (per-memory provenance) | MemoryHub (stub), Oracle (per-record) | Prototype/proprietary only |
| Retention/erasure (GDPR Art. 17) | Oracle (per-record erasure) | Proprietary only |
| Trust-aware retrieval | Academic research only | Not shipped by any vendor |
| Sandbox-aware write governance | **Nobody** | Unserved |

"Governance" is no longer binary. It is a ladder, and the competitive
question is who climbs it fastest. RHOAI's opportunity is to define the
full ladder and ship the top rungs first.

### 3.4 The procedural memory frontier

Microsoft's procedural memory (Build 2026) shifts memory from "what was
said" to "how to do the work."

- No other hyperscaler ships procedural memory
- OGX (RHOAI's substrate) has procedural primitives via the Prompts API
  (pre-authored procedures, not learned-from-trajectories)
- The governance risk is highest for procedural memory — Microsoft's
  MemoryGuard explicitly notes procedural candidates "can influence how
  the agent performs future work" and should require human review
- Aligns with finding 18 (memory security) — a poisoned procedural
  memory is a persistent backdoor into agent behavior

RHOAI implication: procedural memory is high-value, high-risk. Must ship
with the strongest write-path governance of any memory type.

### 3.5 The sandbox gap

No platform integrates memory with ephemeral execution in a governed way:

1. Sandboxed agents generate high-value episodic memories that should be
   captured
2. Sandbox environments are high-risk for memory poisoning — memories
   from untrusted execution should carry lower trust and require stronger
   validation
3. No platform makes this distinction — AWS, Google, Microsoft all treat
   sandbox-sourced and human-supervised memories identically

RHOAI's OpenShell integration creates a structural opportunity: if memory
writes from OpenShell sessions carry sandbox-provenance metadata and pass
through a validation gate before promotion, RHOAI would be the first
platform to integrate memory governance with sandbox execution.

---

## 4. What No Competitor Does (updated)

### 4.1 Governed, versioned, rollback-capable memory on self-hosted K8s

Google shipped versioning (preview, cloud-only, no rollback). Zep earned
SOC 2 (cloud-only). Cognee ships air-gap + ontology permissions (no
certs, no versioning). MemoryHub is the only OpenShift-native prototype
with governance + versioning intent, but its audit trail is a stub.

**Gap persists.** [verified across all vendor docs, July 2026]

### 4.2 Memory portability across frameworks and providers

MCP is the de facto transport (Mem0, Cognee, MemPalace, Google, AWS,
Microsoft all ship MCP surfaces). But MCP is a tool protocol, not a
memory schema. No standardized memory operations schema exists. AAIF is
the venue; no memory working group exists. Opportunity window (finding 9)
remains open.

**Gap persists.** [verified — MCP 2026-07-28 spec, AAIF governance]

### 4.3 Sandbox-integrated memory governance

Newly identified gap (not in doc 02). No platform distinguishes memory
writes by execution context (sandboxed vs. normal), attaches
sandbox-provenance metadata, or applies differential validation gates
based on memory source. RHOAI's OpenShell creates the structural
opportunity.

**Gap persists — not addressed by any competitor.** [verified across all
vendor docs, July 2026]

---

## 5. What This Changes in the Series

| Finding | # | Status | Evidence |
|---|---|---|---|
| Governance + K8s + air-gap + open standard | 4 | **Strengthened** | Google versioning is cloud-only preview; Zep SOC 2 is cloud-only; Cognee air-gap has no certs; full combination still unserved |
| Market fragmenting, consolidation likely | 5 | **Evolving — leaders stabilizing** | Mem0 ($24M, AWS), Zep (SOC 2), Letta ($10M, pivoting), Cognee (EUR 7.5M). Leaders emerging, no consolidation yet |
| Inspectable compaction is compliance-critical | 10 | **Strengthened** | Google Memory Revisions validates inspectability as platform feature; MemoryGuard validates write-path inspection |
| Audit trail is GA-gating | 13 | **Unchanged** | No competitor ships complete audit trail. Google Memory Revisions closest (version history, no provenance metadata per write) |
| Memory-as-MCP | 16 | **Sharpened** | MCP statelessness removes protocol-level session identity. Mem0, Cognee, MemPalace all ship MCP servers, validating the surface |
| Dream consolidation | 17 | **Confirmed shipped** | Anthropic Dreaming research preview (May 2026). Perplexity Brain is second production implementation |
| Memory security is existential | 18 | **Strengthened** | Microsoft MemoryGuard validates threat model. OWASP ASI06 recognizes memory poisoning. Google recommends Model Armor for Memory Bank |
| Benchmark reliability | 12 | **Weakened as differentiator** | Vendor-claimed benchmarks proliferating; only Zep's arXiv result is peer-reviewed. Benchmark wars becoming marketing, not engineering signals |

---

## Sources

### Hyperscaler (verified)
- Google Memory Bank: cloud.google.com/gemini-enterprise-agent-platform/scale/memory-bank
- Google Memory Revisions: cloud.google.com/agent-builder/agent-engine/memory-bank/revisions
- AWS AgentCore Memory: docs.aws.amazon.com/bedrock-agentcore/latest/devguide/memory.html
- AWS strictly consistent metadata: aws.amazon.com/about-aws/whats-new/2026/05/agentcore-memory-scmetadata/
- AWS AgentCore MCP: awslabs.github.io/mcp/servers/amazon-bedrock-agentcore-mcp-server
- Microsoft Foundry Memory: learn.microsoft.com/en-us/azure/foundry/agents/concepts/what-is-memory
- Microsoft Foundry Build 2026: devblogs.microsoft.com/foundry/memory-build2026/
- Microsoft MemoryGuard: techcommunity.microsoft.com (2026-06-21)

### OSS (verified where noted)
- Mem0: docs.mem0.ai, github.com/mem0ai/mem0
- Zep / Graphiti: getzep.com, arXiv:2501.13956
- Letta: letta.com, github.com/cpacker/letta
- Cognee: cognee.ai, github.com/topoteretes/cognee
- MemPalace: github.com/mempalace/mempalace

### Series
- Doc 02 (Solution Survey), 19 (Market refresh July 10), 20 (Market
  refresh July 27), 10 (Dreaming), 11 (Adversarial), 12 (Benchmarking)
