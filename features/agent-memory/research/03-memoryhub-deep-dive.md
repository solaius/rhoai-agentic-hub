---
title: "Agent Memory & Knowledge: MemoryHub Deep-Dive"
description: Deep technical analysis of the MemoryHub prototype -- architecture, governance model, and productization assessment as the leading internal Red Hat candidate for an RHOAI memory primitive.
source: ai-asset-registry/agent-memory/research/03-memoryhub-deep-dive.md (as of 2026-07-05)
timestamp: 2026-07-06
review_after: 2026-08-05
---

# Agent Memory & Knowledge: MemoryHub Deep-Dive

**Purpose:** Deep technical analysis of the MemoryHub prototype — architecture, governance model, notable design ideas, and productization assessment — as the leading internal Red Hat candidate for an RHOAI agent memory primitive.

**Date:** 2026-05-17

**Status:** EXPLORATORY — MemoryHub is a prototype. Nothing in this document describes a shipped RHOAI feature. All MemoryHub capabilities described here are from a Red Hat AI Americas internal prototype, not an RHOAI product.

**Series:** Document 03 of 17 — Agent Memory & Knowledge Research
**Phase 1:** [00](00-executive-summary.md) · [01](01-landscape-and-definitions.md) · [02](02-solution-survey.md) · 03 MemoryHub Deep-Dive (this doc) · [04](04-technical-patterns.md) · [05](05-standards-and-protocols.md) · [06](06-ogx-memory-primitives.md) · [07](07-taxonomy-and-decomposition.md) · [08](08-rhoai-ocp-alignment.md)
**Phase 2:** [09](09-agent-harness-memory.md) · [10](10-claude-memory-dreaming.md) · [11](11-adversarial-memory.md) · [12](12-benchmarking-evaluation.md) · [13](13-kv-cache-optimization.md) · [14](14-enterprise-use-cases.md) · [15](15-multi-modal-memory.md) · [16](16-ai-gateway-memory-substrate.md) · [REVIEW-NOTES](REVIEW-NOTES.md)
**Strategy:** [README](/features/agent-memory/strategy/strategy-overview.md) · [Agent Memory Strategy](/features/agent-memory/strategy/agent-memory-strategy.md)
- [Use Cases & Personas](/features/agent-memory/strategy/use-cases-and-personas.md)
- [Recommended Architecture](/features/agent-memory/strategy/recommended-architecture.md)
- [RHAISTRAT-1345 Outcome Update](/features/agent-memory/strategy/rhaistrat-1345-outcome-update.md)
- [RFE Roadmap](/features/agent-memory/strategy/rfe-roadmap.md)

**Repo access status:** Fully accessible. The `redhat-ai-americas/memory-hub` repository is public on GitHub and was read directly for this document. All code-level claims are sourced from files in that repository as of the last commit (`2026-05-07`). No claims were invented from the internal seed document alone; each claim has a corresponding repo file citation.

---

## 1. What MemoryHub Is and Current Status

**REFERENCE** — MemoryHub is a Kubernetes-native agent memory component for OpenShift AI, developed as an internal Red Hat AI Americas prototype. It provides centralized, governed shared memory for AI agents on OpenShift AI: persistent across sessions, shared across agent frameworks, with multi-tiered access control, version tracking, and semantic search. ([`README.md`](https://github.com/redhat-ai-americas/memory-hub/blob/main/README.md), 2026)

**Author and ownership:** Wes Jackson, Red Hat Solutions Architect (AI Americas). The NOTICE file lists sole copyright: "Copyright 2026 Wes Jackson." The repository is hosted under the `redhat-ai-americas` GitHub organization, indicating AI Americas team stewardship. ([`NOTICE`](https://github.com/redhat-ai-americas/memory-hub/blob/main/NOTICE); [`pyproject.toml`](https://github.com/redhat-ai-americas/memory-hub/blob/main/pyproject.toml))

**License:** Apache 2.0. ([`LICENSE`](https://github.com/redhat-ai-americas/memory-hub/blob/main/LICENSE))

**Repository visibility and activity:** Public repository. Last push: 2026-05-13. Forks: 6. Stars: 0 (the star count reflects that this is an internal prototype, not a promoted public project). The most recent substantive commit (2026-05-07) moved positioning content and competitive analyses to a private peer repo (`rdwj/memory-hub-research`), making the public repo contributor-focused. ([`gh repo view`](https://github.com/redhat-ai-americas/memory-hub))

**Current status table** (from [`docs/SYSTEMS.md`](https://github.com/redhat-ai-americas/memory-hub/blob/main/docs/SYSTEMS.md), as of 2026-04-15 update):

| Subsystem | Status |
|---|---|
| memory-tree (core data model) | **Implemented** |
| storage-layer (PostgreSQL + pgvector) | **Implemented** |
| curator-agent (inline curation pipeline, Phase 2a) | **Implemented (Phase 2a)** |
| governance (RBAC + JWT; campaign RBAC; project auto-enrollment) | **Implemented** (audit log + FIPS pending) |
| mcp-server (compact profile: 2 tools with 19 actions; full: 10 tools; minimal: 4 tools) | **Implemented** |
| memoryhub-auth (OAuth 2.1 authorization server) | **Implemented** |
| sdk (`memoryhub` on PyPI, v0.7.0) | **Implemented** |
| memoryhub-cli | **Implemented** |
| memoryhub-ui (React + PatternFly 6 dashboard) | **Implemented** |
| agent-memory-ergonomics (Layers 1–3) | **Implemented** (Phase 2 open) |
| operator (Kubernetes CRDs for lifecycle management) | **Skeleton** |
| observability (Prometheus + Grafana) | **TBD** |
| org-ingestion (external source pipeline) | **TBD** |
| kagenti-integration | **Design** |
| llamastack-integration | **Design** |

**Key gap from the status table:** The Kubernetes operator is a skeleton — the current deployment is plain manifests and scripts, not operator-managed. Audit logging is a stub interface (not yet wired through). FIPS compliance is inherited from the cluster but not validated end-to-end. These three gaps are directly relevant to the productization assessment in Section 5.

**SDK published:** The Python SDK `memoryhub` is published to PyPI and has an external downstream consumer: `kagenti/adk` PR #231 (IBM Python Agent Development Kit) consumes `MemoryHubClient`. This is the first confirmed external SDK consumer and a meaningful signal that the prototype has crossed from internal experiment to early ecosystem adoption. ([`docs/SYSTEMS.md`](https://github.com/redhat-ai-americas/memory-hub/blob/main/docs/SYSTEMS.md))

**Correction to internal seed document:** The seed document (`docs/knowledge-review/assets/agent-memory-knowledge.md`) describes the MCP server as "exposing 14 tools." This is outdated. The repo's own README component table is also stale at "14 tools." The authoritative sources are SYSTEMS.md and mcp-server.md. The current deployed tool surface is a **compact profile** with 2 tools (`register_session` + `memory` with an `action` parameter dispatching 19 actions). The older 10 flat-parameter tools are retained as deprecated aliases during a migration period. Three tool profiles are available via `MEMORYHUB_TOOL_PROFILE`: **compact** (default, 2 tools), **full** (10 tools — the pre-consolidation flat surface retained for backward compatibility), and **minimal** (4 tools — a reduced surface for constrained agents or token-budget environments). The "14 tools" figure likely reflected a transient state during consolidation (#201/#202). ([`docs/SYSTEMS.md`](https://github.com/redhat-ai-americas/memory-hub/blob/main/docs/SYSTEMS.md); [`docs/mcp-server.md`](https://github.com/redhat-ai-americas/memory-hub/blob/main/docs/mcp-server.md))

---

## 2. Architecture

### 2.1 Consumer Surfaces

**REFERENCE** — MemoryHub exposes four consumer surfaces, all routing through a single MCP server as the sole entry point. ([`docs/ARCHITECTURE.md`](https://github.com/redhat-ai-americas/memory-hub/blob/main/docs/ARCHITECTURE.md))

| Surface | Technology | Notes |
|---|---|---|
| **Agents over MCP** | FastMCP 3, streamable-HTTP transport | Primary agent surface. Compatible with any MCP-capable framework: Claude Code, kagenti-deployed LangGraph/CrewAI/AG2 agents, LlamaStack workflows, custom Python. |
| **Python SDK** | `memoryhub` on PyPI (v0.7.0) | Typed async client. OAuth 2.1 token management is automatic. Auto-discovers `.memoryhub.yaml` project config and applies retrieval defaults. Note: v0.6.0 cannot operate against the current deployment (wire format changed; see SYSTEMS.md). |
| **CLI** | `memoryhub-cli` on PyPI (v0.3.0) | Terminal client with full tool surface parity. `memoryhub config init` generates project-level config and agent rule files. `--output json` flag on all commands for agent consumption. |
| **Dashboard UI** | React + PatternFly 6 frontend, FastAPI BFF, OAuth-proxy sidecar | Six panels: Memory Graph, Status Overview, Users & Agents, Client Management, Curation Rules, Contradiction Log. |

No direct REST API is exposed. No direct database access path exists for external consumers. The MCP server is intentionally the single chokepoint — "one interface to secure and one interface to audit." ([`docs/ARCHITECTURE.md`](https://github.com/redhat-ai-americas/memory-hub/blob/main/docs/ARCHITECTURE.md))

### 2.2 Service Layer

**REFERENCE** — The service layer is the `memoryhub_core` package (distribution name `memoryhub-core`; import name `memoryhub_core`). It contains SQLAlchemy models, business logic services, embedding integration, and RBAC enforcement (`core/authz.py`). The MCP server, BFF, Alembic migrations, and the seed-OAuth-clients script all import from here. ([`pyproject.toml`](https://github.com/redhat-ai-americas/memory-hub/blob/main/pyproject.toml); [`docs/ARCHITECTURE.md`](https://github.com/redhat-ai-americas/memory-hub/blob/main/docs/ARCHITECTURE.md))

**Data flow for a memory write:**
1. Agent calls `memory(action="write", ...)` via MCP (or the deprecated `write_memory` alias).
2. FastMCP 3's `JWTVerifier` validates the JWT at the transport layer before any tool code executes.
3. `core/authz.py`'s `authorize_write(claims, scope, owner_id)` enforces RBAC.
4. The write-time curation pipeline runs inline (Tier 1: regex secrets/PII scan; Tier 2: embedding similarity dedup check).
5. The embedding model (`all-MiniLM-L6-v2`) generates a 384-dimensional vector.
6. PostgreSQL stores the memory node, embedding, and metadata.
7. The response includes the created memory plus curation feedback (`similar_count`, `nearest_id`, `nearest_score`, `flags`, `blocked`).

**Data flow for a memory search (with session focus):**
1. Agent calls `memory(action="search", focus="OpenShift", session_focus_weight=0.4, ...)`.
2. Auth and RBAC enforcement as above; the authorized-scopes filter is built as a SQL clause.
3. Query and focus strings are independently embedded.
4. pgvector cosine top-K=32 recall by query embedding.
5. Optional cross-encoder rerank (`ms-marco-MiniLM-L12-v2`); if reranker is unreachable, graceful fallback to cosine with `focus_fallback_reason` in response.
6. Reciprocal-rank fusion (RRF) blends reranker ranks with focus cosine ranks at `session_focus_weight`.
7. Weight-based stub/full injection and token-budget packing (`max_response_tokens`).
8. Response includes `pivot_suggested` and `pivot_reason` when topic distance from focus exceeds threshold.

([`docs/ARCHITECTURE.md`](https://github.com/redhat-ai-americas/memory-hub/blob/main/docs/ARCHITECTURE.md); [`docs/mcp-server.md`](https://github.com/redhat-ai-americas/memory-hub/blob/main/docs/mcp-server.md))

### 2.3 Infrastructure

**REFERENCE** — The infrastructure layer uses PostgreSQL with the pgvector extension as the single backend for all relational, vector, and graph queries. ([`docs/storage-layer.md`](https://github.com/redhat-ai-americas/memory-hub/blob/main/docs/storage-layer.md))

**Single-database design (current deployed state):** The Phase 1 retrospective documents an explicit pivot from a multi-store architecture (Milvus + Neo4j + MinIO) to PostgreSQL-only after FIPS research. In the *current deployed state*, a single PostgreSQL+pgvector instance handles all three responsibilities with no separate vector store, no separate graph database, and no separate key-value cache:
- **Vector similarity search** — pgvector extension, `all-MiniLM-L6-v2` embeddings (384-dim), cosine/L2/inner-product operators.
- **Relational data** — memory nodes, version chains, user/agent identities, campaign memberships, contradiction reports.
- **Graph relationships** — `memory_relationships` table with typed edges (`derived_from`, `supersedes`, `conflicts_with`, `related_to`). Adjacency lists with recursive CTEs for traversal. Apache AGE (openCypher) considered but deferred pending validation with OpenShift's OOTB PostgreSQL operator.

**However, MinIO and Valkey/Redis are coded dependencies, not removed ones.** `pyproject.toml` lists `minio` and `redis>=5.0` as hard dependencies, and `docs/storage-layer.md` describes MinIO for document/blob storage. ARCHITECTURE.md also mentions a Valkey-backed session vector store (Pattern E, issue #62) deferred to Phase 2. These components are designed and wired as dependencies but not yet active in the deployed configuration. Their FIPS implications differ from PostgreSQL: MinIO's FIPS posture on OpenShift requires separate validation, and Valkey/Redis FIPS compliance is cluster-configuration-dependent. The "PostgreSQL-only" characterization accurately describes what is *deployed today* but should not be read as "MinIO and Valkey are out of scope forever."

**External model dependencies:**
- `all-MiniLM-L6-v2` — embedding model deployed on RHOAI vLLM serving; URL configured via `MEMORYHUB_EMBEDDING_URL`.
- `ms-marco-MiniLM-L12-v2` — cross-encoder reranker, also on RHOAI vLLM; URL configured via `MEMORYHUB_RERANKER_URL`. Optional; system is designed to degrade gracefully when this is unavailable.

**Deployment topology — three OpenShift namespaces:**

| Namespace | Pods | Purpose |
|---|---|---|
| `memory-hub-mcp` | `memory-hub-mcp` (FastMCP server), `memoryhub-ui` (BFF + oauth-proxy sidecar) | Agent-facing MCP server and dashboard. |
| `memoryhub-auth` | `auth-server` | Standalone OAuth 2.1 authorization server. |
| `memoryhub-db` | `memoryhub-pg-0` | PostgreSQL + pgvector. |

([`docs/SYSTEMS.md`](https://github.com/redhat-ai-americas/memory-hub/blob/main/docs/SYSTEMS.md); [`docs/ARCHITECTURE.md`](https://github.com/redhat-ai-americas/memory-hub/blob/main/docs/ARCHITECTURE.md))

**Install mechanism:** `make install` deploys the full stack to an existing OpenShift/RHOAI cluster. The Makefile triggers OpenShift BuildConfigs (binary strategy) for the MCP server, auth service, and UI, then rolls out deployments. Estimated first-install time: 10–15 minutes. ([`README.md`](https://github.com/redhat-ai-americas/memory-hub/blob/main/README.md))

**Container posture:** Red Hat UBI9 base images. FIPS delegated to the cluster's OS-level OpenSSL (no components implement their own cryptography). Air-gap deployable with on-cluster embedding models. ([`docs/governance.md`](https://github.com/redhat-ai-americas/memory-hub/blob/main/docs/governance.md))

---

## 3. Governance Model

### 3.1 Five-Tier Scope Model

**REFERENCE** — MemoryHub's central governance primitive is a five-tier scope hierarchy. Every memory node carries a scope field that determines both who can access it and what governance rules apply to writes. ([`docs/governance.md`](https://github.com/redhat-ai-americas/memory-hub/blob/main/docs/governance.md); [`docs/memory-tree.md`](https://github.com/redhat-ai-americas/memory-hub/blob/main/docs/memory-tree.md))

| Scope | Access: Read | Access: Write | Governance |
|---|---|---|---|
| **user** | Owning user's agents only | Agent acting on behalf of owning user only | Fully automatic; no approval. Cross-user writes explicitly blocked as a security property: "if someone else could modify your memories, they could change how your agent behaves and make you appear responsible for the outcome." |
| **project** | All agents with project context | All agents with project context | Automatic; auditable. Project owners can review and modify. Project auto-enrollment: agents writing to open projects are auto-enrolled on first project-scoped write (#188). |
| **campaign** | All agents whose project is enrolled in the campaign | All agents whose project is enrolled | Campaign as a bounded cross-project scope — a modernization campaign or compliance rollout. Enrollment checked via `campaign_memberships` table at RBAC time. Shipped as of 2026-04-09 (#164). |
| **role** | All agents whose users hold the specified role | Curator agent only (pattern promotion) | Readable by role; writable only by curator after pattern detection. Role assignment from OpenShift OAuth RBAC. |
| **organizational** | All agents in the organization | Curator agent only, with optional human approval | Collective patterns. Requires provenance tracking. All operations auditable. |
| **enterprise/policy** | All agents | Human-in-the-loop approval required | Mandated rules. "These always require human-in-the-loop for creation and modification." The governance engine blocks any attempt to write enterprise memories without the approval workflow completing. |

The scope enforcement is SQL-level, not application-level. `search_memory` builds the authorized-scopes filter at the SQL level so "RBAC violations are impossible by construction." ([`docs/mcp-server.md`](https://github.com/redhat-ai-americas/memory-hub/blob/main/docs/mcp-server.md))

**Note on scope count:** The internal seed document and the README describe "five-tier scope isolation" using the terms `user / project / role / organizational / enterprise`. The code and governance doc reveal a sixth scope in active use: `campaign` (between `project` and `role`), shipped in April 2026. The "five-tier" description in the README predates this addition. The actual deployed model has six scopes.

### 3.2 Versioning and Contradiction Detection

**REFERENCE** — Every memory node carries version metadata: an `isCurrent` boolean (only one version current at any time), creation and last-modified timestamps, and a reference to the previous version. All versions are preserved — none are deleted. ([`docs/memory-tree.md`](https://github.com/redhat-ai-americas/memory-hub/blob/main/docs/memory-tree.md))

This version model supports two capabilities:
- **Forensics:** Reconstructing exactly what an agent knew at any point in time. "What memories were in agent X's context during conversation Y on March 15th?" is answered by correlating the audit trail's read entries with the version history of each memory read at that timestamp.
- **Staleness detection:** When an agent observes behavior contradicting a stored memory, it calls `manage_curation(action="report_contradiction", memory_id=..., observed_behavior=..., confidence=...)`. Reports accumulate in a `contradiction_reports` table. When the unresolved count crosses a threshold (currently 5), the curator surfaces the memory for review.

The `contradiction_reports` table captures: `memory_id`, `observed_behavior` (text — agents are instructed to be specific, not vague), `confidence` (float 0.0–1.0), `reporter` (agent/user identity), timestamps, and a `resolved` boolean. ([`docs/storage-layer.md`](https://github.com/redhat-ai-americas/memory-hub/blob/main/docs/storage-layer.md))

### 3.3 Three-Layer Curation Rules Engine

**REFERENCE** — Curation runs as an inline pipeline within every `write_memory` / `memory(action="write", ...)` call — not as a separate service. The pipeline is entirely deterministic (regex and embedding checks, no LLM calls at write time). ([`docs/curator-agent.md`](https://github.com/redhat-ai-americas/memory-hub/blob/main/docs/curator-agent.md))

**Write-time pipeline (three tiers):**

| Tier | Mechanism | Latency | Action on match |
|---|---|---|---|
| **Tier 0: Schema validation** | Pydantic | ~0ms | Reject with validation error |
| **Tier 1: Regex scanning** | Pattern matching | ~microseconds | Block or quarantine (configurable) |
| **Tier 2: Embedding similarity** | pgvector cosine against existing memories for same `(owner_id, scope, is_current=true)` | ~milliseconds | >0.95: reject with pointer; 0.80–0.95: flag in metadata, allow write; <0.80: allow |

Secrets detection categories (Tier 1): AWS/GCP/Azure/GitHub API keys and tokens, passwords and connection strings, private key headers (`-----BEGIN`). PII categories: SSNs, email addresses, phone numbers, credit card numbers.

**No inline LLM sampling:** Earlier designs included LLM sampling at write time for ambiguous cases. This was removed because the MCP specification requires human-in-the-loop for sampling, creating unacceptable write-path friction. Instead, `write_memory` returns similarity feedback (`similar_count`, `nearest_id`, `nearest_score`) and the calling agent's own LLM handles the judgment call as part of its normal flow. ([`docs/curator-agent.md`](https://github.com/redhat-ai-americas/memory-hub/blob/main/docs/curator-agent.md))

**Three-layer rules hierarchy:** Rules are layered as system > organizational > user. System rules (secrets scanning) are marked `override=true` and cannot be weakened by user rules. Users tune their own dedup thresholds via `manage_curation(action="set_rule", ...)`.

**Future curator-as-background-agent (EXPLORATORY):** The roadmap includes a background curator agent for cross-user pattern detection and promotion from lower scopes to higher scopes (user → organizational, organizational → enterprise). This is currently on the roadmap as Phase 2 of the curator subsystem; it is not shipped. ([`docs/SYSTEMS.md`](https://github.com/redhat-ai-americas/memory-hub/blob/main/docs/SYSTEMS.md))

### 3.4 Audit Trail

**EXPLORATORY** — The governance documentation describes a comprehensive immutable audit trail ("append-only: entries cannot be modified or deleted, even by administrators"). Each entry would include: operation type, target memory ID, actor identity (user + agent), timestamp, before-state, after-state, and governance decision. ([`docs/governance.md`](https://github.com/redhat-ai-americas/memory-hub/blob/main/docs/governance.md))

**However, the SYSTEMS.md status table explicitly states:** "audit log + FIPS pending" — the audit log is a "stub interface (#67), not yet wired through." ([`docs/SYSTEMS.md`](https://github.com/redhat-ai-americas/memory-hub/blob/main/docs/SYSTEMS.md))

**Contradiction to flag:** The README and governance.md describe the audit trail as a feature of MemoryHub's compliance posture. The SYSTEMS.md status table and issue #67 make clear the audit log is not yet implemented — it is a stub interface. For RHOAI productization assessment, the audit trail must be treated as designed-but-not-shipped.

### 3.5 Authentication and Authorization Architecture

**REFERENCE** — Two cooperating layers handle auth:

**Authentication (`memoryhub-auth`):** A standalone OAuth 2.1 authorization server. FastAPI, `client_credentials` and `refresh_token` grants, RSA-2048 JWT signing, JWKS endpoint, admin client management API, DB-backed refresh token rotation. Token claims include `sub`, `client_id`, operational scopes (`memory:read`, `memory:write`, `memory:admin`), access-tier scopes (`user`, `project`, `campaign`, `role`, `organizational`, `enterprise`), and `tenant_id` for future multi-tenant isolation. JWTs are short-lived (5–15 min) and refreshed automatically by the SDK. ([`docs/ARCHITECTURE.md`](https://github.com/redhat-ai-americas/memory-hub/blob/main/docs/ARCHITECTURE.md))

Token exchange (RFC 8693) for platform-integrated agents on RHOAI/kagenti is designed but not yet wired. ([`docs/mcp-server.md`](https://github.com/redhat-ai-americas/memory-hub/blob/main/docs/mcp-server.md))

**Authorization (`core/authz.py`):** JWT-first validation with a dev-path API key shim fallback. `build_authorized_scopes(claims)` maps token scopes to a SQL filter clause. `authorize_read()` and `authorize_write()` called by every tool before any service-layer call. SQL-level scope filtering makes RBAC violations impossible by construction. ([`docs/governance.md`](https://github.com/redhat-ai-americas/memory-hub/blob/main/docs/governance.md))

---

## 4. Notable Ideas

### 4.1 Cache-Optimized Memory Assembly

**EXPLORATORY** — MemoryHub's most distinctive performance idea is the design of memory retrieval order as a vLLM KV-cache optimization.

**Background:** vLLM's Automatic Prefix Caching (APC) stores computed KV tensors for token prefix blocks. Cache matching is strictly block-aligned and prefix-contiguous — a single different token within a block invalidates that block and all subsequent blocks. If 100 concurrent agents receive memories in a deterministic, stable order, they share a common token prefix; only the first agent pays the full prefill cost and subsequent agents get the cached prefix nearly free. ([`research/vllm-cache-optimization.md`](https://github.com/redhat-ai-americas/memory-hub/blob/main/research/vllm-cache-optimization.md))

**MemoryHub's approach:** SDK v0.5.0 (shipped 2026-04-12) added cache-optimized assembly: `search()` returns results in a stable, deterministic order designed for KV-cache prefix hits. The approach uses "epoch locking" — the sort order for a given memory set is locked at a compile time and does not change unless the memory set itself changes. High-stability, high-weight memories (enterprise/organizational scope) appear first; they are the most likely to be shared across agent sessions and thus the most valuable to cache. ([`CHANGELOG.md`](https://github.com/redhat-ai-americas/memory-hub/blob/main/CHANGELOG.md); [`research/vllm-cache-optimization.md`](https://github.com/redhat-ai-americas/memory-hub/blob/main/research/vllm-cache-optimization.md))

**Published performance claims** (from README.md — internal research, not independently benchmarked):

| Model/Provider | Claimed benefit |
|---|---|
| vLLM | 2x throughput, 152x TTFT improvement (llm-d precise routing with 8 pods, H100) |
| Anthropic | ~90% cost reduction |
| OpenAI | ~50% cost reduction |
| Gemini | 75–90% cost reduction |

**Caveat:** These figures are from the MemoryHub README and the research document, not from independently published benchmarks. The vLLM figures cite llm-d's own published benchmarks for its cache-aware routing, not a MemoryHub-specific benchmark. The Anthropic/OpenAI/Gemini figures are stated as design targets without a controlled benchmark. These are directionally plausible given how KV-cache prefix hits work in theory; independent validation is not available.

**Why this matters for RHOAI:** The insight that memory retrieval order is a performance variable — not merely a relevance variable — is a genuinely novel design idea. If RHOAI builds a memory primitive, cache-optimized assembly is a differentiating feature worth validating rigorously.

### 4.2 Human-Readable Compaction (Designed, Not Shipped)

**EXPLORATORY** — MemoryHub's roadmap explicitly positions its context compaction approach as the compliance-compliant alternative to OpenAI's opaque compaction:

> "Compaction will use readable summaries — not opaque tokens — so the compliance team can inspect what was kept." ([`README.md`](https://github.com/redhat-ai-americas/memory-hub/blob/main/README.md))

This directly addresses Gap 3 identified in [02 Solution Survey](02-solution-survey.md): the regulatory requirement that compressed memory remain inspectable under EU AI Act, GDPR, and HIPAA. OpenAI's compaction artifact is optimized for performance but is non-human-readable; Anthropic's Dreaming produces CLAUDE.md-style structured files that are human-readable; MemoryHub's roadmap targets the same inspectable model.

**Status: not yet shipped.** Governed context compaction is listed as a roadmap item in the README but does not appear in the SYSTEMS.md subsystem table as a designed or implemented feature. There are no implementation artifacts for the compaction pipeline in the public repo as of 2026-05-07.

### 4.3 Promotion Pipeline (Designed, Not Shipped)

**EXPLORATORY** — MemoryHub describes a planned "promotion pipeline" that lifts patterns discovered by individual agents into organizational knowledge:

> "A planned promotion pipeline will lift patterns discovered by individual agents into organizational knowledge." ([`README.md`](https://github.com/redhat-ai-americas/memory-hub/blob/main/README.md))

The mechanism is the curator-as-background-agent layer (roadmap Phase 2): a background process that runs cross-user analysis, detects convergent patterns across user-scope memories (e.g., 30+ engineers all independently noting "scan for secrets before commits"), and promotes them to organizational scope — adding provenance branches traceback to source user memories. ([`docs/memory-tree.md`](https://github.com/redhat-ai-americas/memory-hub/blob/main/docs/memory-tree.md) — note: the org memory example in memory-tree.md illustrates this pattern with `source: user memories u47, u102, u203...`)

This is the same "sleep-time compute" pattern that Letta and Anthropic's Dreaming implement — off-line memory reorganization without blocking inference. MemoryHub adds a human governance gate for enterprise-scope promotion.

**Status: not yet shipped.** The promotion pipeline is a roadmap item, not an implemented feature.

### 4.4 Project Config Wizard and Agent Rule Generation

**REFERENCE** — The `.memoryhub.yaml` config file and the `memoryhub config init` CLI command form a configuration layer that sits between the memory service and the agent's instruction files.

**`.memoryhub.yaml` schema** (from the live config in the repo root):

```yaml
memory_loading:
  mode: focused                    # focused | broad
  pattern: lazy_with_rebias        # loading pattern
  focus_source: declared           # declared | inferred
  session_focus_weight: 0.4
  on_topic_shift: rebias
  cross_domain_contradiction_detection: false
  campaigns: []                    # enrolled campaign slugs
  live_subscription: false
  push_payload: uri_only
  push_filter_weight: 0.6
  push_transport: queue
retrieval_defaults:
  max_results: 10
  max_response_tokens: 4000
  default_mode: full               # full | index | full_only
```

`memoryhub config init` generates both the `.memoryhub.yaml` config and a `.claude/rules/memoryhub-loading.md` rule file — meaning it generates the instructions that tell an agent *when and how* to call the memory service, not just the service configuration parameters. The SDK auto-discovers `.memoryhub.yaml` and applies `retrieval_defaults` to all outbound calls. ([`.memoryhub.yaml`](https://github.com/redhat-ai-americas/memory-hub/blob/main/.memoryhub.yaml); [`docs/SYSTEMS.md`](https://github.com/redhat-ai-americas/memory-hub/blob/main/docs/SYSTEMS.md))

This is the most developer-experience-focused feature in the prototype: rather than requiring developers to hand-write memory loading instructions for every project, the CLI generates the correct rule file from the project's declared memory shape. The pattern aligns with the "low friction accelerates adoption" lesson from Meta's AI Second Brain (referenced in [01 Landscape & Definitions](01-landscape-and-definitions.md)).

### 4.5 Two-Vector Retrieval with Session Focus

**REFERENCE** — The session focus feature (Layer 2 of agent-memory-ergonomics, shipped 2026-04-07, issue #58) implements a stateless two-vector retrieval pattern: the agent passes a `focus` string per search call; the system embeds both the query and the focus independently, runs cross-encoder reranking, and blends results via Reciprocal-Rank Fusion (RRF) weighted by `session_focus_weight`. ([`docs/agent-memory-ergonomics/design.md`](https://github.com/redhat-ai-americas/memory-hub/blob/main/docs/agent-memory-ergonomics/design.md); [`docs/mcp-server.md`](https://github.com/redhat-ai-americas/memory-hub/blob/main/docs/mcp-server.md))

**Key design decision:** The focus is **stateless** — passed per call, not stored server-side. This avoids all coordination requirements for session state, enables horizontal scaling without coordination, and adds only ~50ms per call for focus re-embedding (warm vLLM). The cost-benefit comparison with a stateful session focus was documented in the retrospectives and the design doc; stateless won on simplicity and operability.

A `pivot_suggested` signal in the response tells the agent when the query topic has drifted far from the session focus (cosine distance > 0.55 threshold), enabling the agent to proactively rebias its loading pattern.

### 4.6 Shared Agent Memory and Campaign Scoping

**REFERENCE** — MemoryHub provides a "shared agent memory" capability that distinguishes it from per-agent memory stores:

- **Project-scoped memories auto-surface** for all agents working in that project context with auto-enrollment on first write to open projects.
- **Campaign scoping** enables bounded cross-project knowledge sharing: a modernization campaign or compliance rollout can share memories across multiple enrolled projects without making them globally organizational.
- **Domain tags** enable crosscutting retrieval across scope boundaries: a memory tagged `FIPS` surfaces in any project's search even if not explicitly scoped to that project.
- **Real-time push notifications** (Pattern E, issue #62) — **EXPLORATORY / NOT SHIPPED.** The SDK client method `on_memory_updated()` was added in v0.3.0, but the backend Valkey store that actually delivers push events is deferred to Phase 2 (issue #62, "not yet started" per SYSTEMS.md). The "shipped 2026-04-08" claim in a prior draft was incorrect; only the client-side API surface exists today. ([`README.md`](https://github.com/redhat-ai-americas/memory-hub/blob/main/README.md); [`docs/mcp-server.md`](https://github.com/redhat-ai-americas/memory-hub/blob/main/docs/mcp-server.md); [`docs/SYSTEMS.md`](https://github.com/redhat-ai-americas/memory-hub/blob/main/docs/SYSTEMS.md))

---

## 5. What Transfers to a RHOAI Product, and What Gaps Remain

**EXPLORATORY** — This section is a productization assessment. All judgments are research observations. No RHOAI architecture has been decided.

### 5.1 Maturity Assessment by Subsystem

| Subsystem | Prototype Status | Productization Gap |
|---|---|---|
| Five-tier scope model + SQL-level RBAC | Implemented, tested | Low: the model is sound and the enforcement is correct. Primary gap: multi-tenant `tenant_id` isolation is designed but not wired (tracked as #46). |
| OAuth 2.1 authorization server | Implemented, shipped | Medium: token exchange (RFC 8693) for platform-integrated agents is designed but not wired. Integration with OpenShift OAuth (not standalone auth service) would be required for a productized deployment. |
| MCP server (compact profile) | Implemented, deployed on OpenShift | Low: the MCP interface is clean and tested. Deprecation of legacy tool aliases needs to complete before a stable API contract can be published. |
| PostgreSQL + pgvector storage | Implemented, tested | Low: the storage model is sound. The OOTB PostgreSQL operator on OpenShift needs FIPS validation end-to-end (currently delegated but not validated). |
| Python SDK + CLI | Implemented, on PyPI | Low-medium: SDK v0.7.0 required for current MCP wire format (v0.6.0 cannot operate against the current deployment). External consumer (kagenti-adk) is present. |
| Inline curation pipeline | Implemented (Phase 2a) | Medium: the deterministic pipeline is production-quality. The background curator-as-agent for promotion is not yet designed as an implementation artifact. |
| Governance/audit trail | DESIGNED, not shipped | High: the audit log is a stub interface (#67). This is a hard gap for enterprise compliance — an audit trail is not optional for regulated environments. |
| Kubernetes operator | Skeleton | High: current deployment is plain manifests + scripts. A product requires an operator for lifecycle management, upgrades, and configuration via CRDs. |
| Observability | TBD | High: no Prometheus metrics or Grafana dashboards. No product ships without observable services. |
| Dashboard UI | Implemented | Medium: PatternFly 6 is correct for RHOAI. Observability panel intentionally disabled (#10). |
| FIPS compliance | Delegated, not validated | Medium: the delegation strategy (UBI9 + cluster FIPS mode) is sound in principle. End-to-end validation is not complete. |
| Cache-optimized assembly | Implemented (SDK v0.5.0) | Low: sound design, shipped. Needs independent benchmark validation rather than internal research-document figures. |
| Context compaction | Roadmap only | High: governed context compaction is a stated roadmap item. No implementation artifacts exist in the public repo. |
| Promotion pipeline | Roadmap only | High: the cross-user pattern detection and promotion pipeline is a roadmap item. No implementation artifacts. |
| kagenti integration | Design | Medium: three-phase integration plan is documented. Phase 1 (MCP connector registration) could be shipped soon. Token exchange integration (Phase 2) and ContextStore replacement (Phase 3) require more work. |
| LlamaStack integration | Design | Similar to kagenti. |

### 5.2 What Is Production-Ready vs. Prototype

**Production-capable (as assessed from the repo):**
- Core memory CRUD (write, read, update, delete, search) with SQL-level RBAC
- Five/six-tier scope model with SQL-level enforcement
- OAuth 2.1 machine-to-machine flow (`client_credentials`)
- Inline curation (Tier 1 regex, Tier 2 embedding dedup)
- Python SDK published to PyPI with an external downstream consumer
- Single-command `make install` deployment on OpenShift
- Session focus retrieval with RRF blending and cross-encoder reranking
- Cache-optimized assembly (SDK v0.5.0+)
- Dashboard UI (PatternFly 6, six panels)
- Project scoping with auto-enrollment, campaign scoping

**Designed but not yet shipped:**
- Immutable audit trail (stub interface, issue #67)
- FIPS end-to-end validation
- OAuth token exchange (RFC 8693) for platform agents
- Multi-tenant `tenant_id` isolation wiring (issue #46)
- Real-time push notification (Pattern E) Phase 2 backend (Valkey-backed session focus vectors)

**Roadmap / skeleton only:**
- Kubernetes operator (CRDs designed but not implemented)
- Observability (Prometheus + Grafana, TBD)
- Org-ingestion pipeline (external source scanning, TBD)
- Background curator agent (promotion pipeline)
- Governed context compaction

### 5.3 What Would Need to Change to Productize

**Gap 1 — Kubernetes operator is mandatory.** A Red Hat product cannot ship as plain manifests + scripts. The operator skeleton exists; this requires significant design and implementation work. The CRD concepts in `planning/operator.md` are a reasonable starting point. The operator would need to coordinate with the OOTB PostgreSQL operator (already planned) and integrate with OLM. ([`planning/operator.md`](https://github.com/redhat-ai-americas/memory-hub/blob/main/planning/operator.md))

**Gap 2 — Audit trail must ship, not be a stub.** Enterprise compliance (EU AI Act enforcement August 2026, GDPR, HIPAA) requires an audit trail. The governance design is thorough; the implementation gap is issue #67. A productized memory primitive cannot meet compliance requirements without this. ([`docs/governance.md`](https://github.com/redhat-ai-americas/memory-hub/blob/main/docs/governance.md))

**Gap 3 — Observability must be TBD-to-done.** No metrics, no dashboards, no alerting. A product must be observable. The SRE and support organizations cannot operate an unobservable service.

**Gap 4 — Standalone OAuth 2.1 service needs RHOAI identity integration.** The current architecture has a standalone `memoryhub-auth` service issuing JWTs. A productized deployment would integrate with OpenShift's platform identity (OIDC/OAuth2 via Red Hat SSO or OpenShift Auth). The OAuth 2.1 foundation is solid; this is an integration architecture question, not a design flaw.

**Gap 5 — FIPS end-to-end validation.** The delegation strategy is sound; the validation is not done. Required for FedRAMP and regulated-industry customers.

**Gap 6 — Scale testing and multi-tenancy.** The prototype has been tested at "hundreds of agents, thousands of memories per user" scale. Enterprise RHOAI deployments may require multiple organizations on one cluster (`tenant_id` isolation, issue #46). Horizontal scaling of the MCP server (currently single-replica) and PostgreSQL read replicas for high-throughput search are not addressed.

**Gap 7 — Scope creep risk on the six-scope model.** The current scope model has six levels (user/project/campaign/role/organizational/enterprise). This is more complex than most comparable systems. The campaign scope is newer and less tested than the original five. A productized version should validate whether campaign scoping is the right abstraction or whether project-level tagging with group enrollment serves the same purpose with less model complexity.

### 5.4 Licensing, Ownership, and Team

**Licensing:** Apache 2.0. This is compatible with Red Hat product inclusion. No known patent or CLA issues identified in the public repo.

**Ownership:** Copyright is held by Wes Jackson individually (per NOTICE file). The repo is under the `redhat-ai-americas` organization. For product inclusion, Red Hat would need to establish a formal IP transfer or contribution agreement to bring the code into a Red Hat-owned project. This is a standard process (similar to other field-originated prototypes) but must be initiated explicitly.

**Team:** Primary author is Wes Jackson (Red Hat SSA). The AI Americas team is the steward. The prototype was built using Claude Code as a development assistant (per commit messages). There is no documented product team or engineering owner for a productization effort.

**Contradiction to flag:** The NOTICE file says "Copyright 2026 Wes Jackson" — not "Copyright 2026 Red Hat, Inc." This means Red Hat does not hold the copyright on this code today. For any product usage, this requires either a CLA (Contributor License Agreement) or IP transfer. This is not a blocker, but it is a required administrative step before product engineering can proceed.

### 5.5 What Transfers Most Directly

Even if MemoryHub is not adopted as-is, the following ideas transfer directly to a RHOAI memory primitive design:

1. **Five/six-tier scope model with SQL-level RBAC enforcement.** The scope model is the strongest governance idea in the prototype and has no direct equivalent in any external solution surveyed in [02 Solution Survey](02-solution-survey.md). Enterprise/policy scope with HITL approval is the right model for the highest-authority memories.

2. **Single PostgreSQL + pgvector backend.** The consolidation of relational, vector, and graph queries into one database (no separate vector store, no separate graph database) reduces operational complexity and FIPS surface area. This is confirmed as the right choice by the Phase 1 retrospective (which explicitly pivoted away from Milvus + Neo4j + MinIO to PostgreSQL-only after FIPS research).

3. **Cache-optimized memory assembly.** The insight that memory retrieval order is a performance variable for KV-cache prefix hits is novel and validated in principle by vLLM APC research. Worth productizing with rigorous benchmarking.

4. **Stateless session focus with graceful degradation.** The two-vector retrieval design with stateless focus (no server-side session state required) is a clean architecture that avoids coordination complexity. The graceful fallback when the reranker is unavailable is production-quality defensive design.

5. **Inline deterministic curation (no inline LLM sampling).** The decision to remove LLM sampling from the write path (documented in the curator retrospective and design doc) is a defensible architectural choice that avoids MCP HITL friction on every write. The curation feedback loop (returning `similar_count` etc. to the calling agent's LLM) is the right division of responsibilities.

6. **Project config wizard generating agent rule files.** The pattern of generating `.claude/rules/memoryhub-loading.md` from `.memoryhub.yaml` is a developer experience pattern that could transfer to any RHOAI memory primitive — reducing the barrier to correct memory integration from "write custom harness instructions" to "run `config init`."

7. **Kagenti integration design.** The three-phase kagenti integration plan (MCP connector → token exchange → ContextStore replacement) is directly applicable to RHOAI's own kagenti integration requirements. This design work does not need to be repeated from scratch.

---

## 6. Open Questions Forwarded to Later Documents

These questions arise from this deep-dive and are not resolved here:

**Q-MH-1 — IP transfer:** What is the process and timeline for establishing IP ownership or a CLA for MemoryHub code if a productization path is chosen? *(administrative, not research)*

**Q-MH-2 — Scope model simplification:** Is the six-scope model (user/project/campaign/role/organizational/enterprise) the right abstraction for a product, or should campaign scope be replaced by project-level group enrollment with tagging? *(See [07 Taxonomy & Decomposition](07-taxonomy-and-decomposition.md))*

**Q-MH-3 — Standalone auth vs. platform identity:** Should a productized memory service have its own OAuth 2.1 authorization server, or integrate directly with Red Hat SSO / OpenShift Auth? *(See [08 RHOAI & OCP Alignment](08-rhoai-ocp-alignment.md))*

**Q-MH-4 — Scale boundaries:** What is the memory-per-user and concurrent-agent ceiling for the current PostgreSQL + pgvector single-backend design? What triggers the need for read replicas, horizontal MCP server scaling, or an in-memory graph layer? *(See [04 Technical Patterns](04-technical-patterns.md))*

**Q-MH-5 — Cache-optimization validation:** Can the cache-optimized assembly claims (2x vLLM throughput, 90% Anthropic cost reduction) be independently reproduced on RHOAI infrastructure with real workloads? *(See [04 Technical Patterns](04-technical-patterns.md))*

---

## 7. Adoption Decision Assessment

**EXPLORATORY** — This section evaluates whether and how MemoryHub should be adopted for RHOAI productization. It synthesizes the productization assessment (Section 5), the strategy decisions (REVIEW-NOTES D3/D5), and the recommended architecture ([Recommended Architecture](/features/agent-memory/strategy/recommended-architecture.md)) into a structured adoption framework. All judgments are research-informed recommendations, not commitments.

### 7.1 Current MemoryHub Status Assessment

**What MemoryHub is today:** A functional prototype — a Kubernetes-deployed, PostgreSQL+pgvector-backed agent memory service with a FastMCP 3 interface, six-scope RBAC model, inline curation pipeline, and a published Python SDK (v0.7.0 on PyPI). It is deployed on OpenShift and has one confirmed external SDK consumer (kagenti/adk PR #231).

**What MemoryHub is not:** A production-ready product. The maturity assessment in Section 5.1 identifies three high-severity gaps (audit trail is a stub, Kubernetes operator is a skeleton, observability is TBD) and three medium-severity gaps (OAuth token exchange not wired, FIPS not end-to-end validated, multi-tenant isolation designed but not wired). The core memory operations, scope model, and curation pipeline are functionally solid; the operational infrastructure around them is incomplete.

**Production readiness summary:**

| Dimension | Assessment |
|---|---|
| Core functionality (CRUD, search, scope RBAC) | Production-capable — the data model, business logic, and SQL-level scope enforcement are tested and deployed |
| Governance model (scope tiers, curation, contradiction detection) | Production-capable in design; the inline curation pipeline is deterministic and production-quality. The governance *design* is the strongest of any candidate surveyed ([02 Solution Survey](02-solution-survey.md) §8). The audit trail gap (stub interface, issue #67) is the critical shortfall |
| Operational readiness (operator, observability, FIPS) | Not production-ready — all three are skeleton/TBD/unvalidated |
| External integration (platform identity, token exchange) | Not production-ready — standalone OAuth 2.1 works, but integration with OpenShift platform identity is designed-only |

**Net assessment:** MemoryHub is a *well-designed prototype with production-capable core logic and incomplete operational infrastructure*. The code quality is high for a prototype; the architecture is sound; the governance model is differentiated. But no Red Hat product ships without an operator, audit trail, and observability — these are hard gaps, not optional polish.

### 7.2 IP Transfer Analysis

**The dependency (Q-MH-1).** The `NOTICE` file states "Copyright 2026 Wes Jackson" — not "Copyright 2026 Red Hat, Inc." The code is Apache 2.0 licensed, which permits Red Hat to use, modify, and distribute it. However, for *product inclusion* — where Red Hat ships, supports, and takes liability for the code — a formal IP transfer or Contributor License Agreement (CLA) is a standard prerequisite.

**What IP transfer involves:**

1. **CLA or copyright assignment.** Either Wes Jackson signs a CLA granting Red Hat sufficient rights to productize the code, or copyright is transferred to Red Hat, Inc. Red Hat has established processes for both paths (similar to other field-originated prototypes that became product features).
2. **Repository transfer.** The code would move from `redhat-ai-americas/memory-hub` (an AI Americas team org) to an RHOAI-engineering-owned organization or repository, with appropriate CI/CD, review processes, and support ownership.
3. **Dependency audit.** The `pyproject.toml` dependencies (SQLAlchemy, asyncpg, pgvector, pydantic, minio, redis, etc.) need license-compatibility verification for product distribution. All listed dependencies are OSS-licensed; no known blockers, but the formal audit is a required step.

**Risks:**

| Risk | Severity | Notes |
|---|---|---|
| Administrative delay | Medium | CLA/IP transfer processes can take weeks to months depending on legal review cycles. This is a *schedule* risk, not a technical risk |
| Single-author bus factor | Medium | Primary author is Wes Jackson. IP transfer must be completed while the author is engaged and available. Product engineering needs knowledge transfer regardless of the IP path |
| Private peer repo (`rdwj/memory-hub-research`) | Low | Competitive analyses and positioning content were moved to a private repo in May 2026. This content is not needed for productization (it is strategy/marketing material, not code), but its existence should be noted in any IP transfer agreement |

**Timeline implication:** Q-MH-1 is an *administrative prerequisite* for Track B of the Phase 1 roadmap (RHOAI 3.6, November 2026). If IP transfer is not initiated early, it becomes a schedule-critical-path item. The recommendation from the [strategy](/features/agent-memory/strategy/agent-memory-strategy.md) §8 is to initiate it as soon as the adoption decision is confirmed.

### 7.3 Architecture Fit Assessment

**How well does MemoryHub's architecture align with the [recommended architecture](/features/agent-memory/strategy/recommended-architecture.md)?** The alignment is strong in the governance dimension and partial in the substrate dimension.

**Alignment points:**

| MemoryHub Feature | Recommended Architecture | Alignment |
|---|---|---|
| **PostgreSQL + pgvector storage** | Single PostgreSQL+pgvector backend for relational, vector, and graph queries | **Strong** — identical technology choice, same consolidation rationale (minimize FIPS surface, reduce operational sprawl) |
| **FastMCP 3 interface** | Framework-agnostic memory API exposed over MCP through MCP Gateway | **Strong** — MemoryHub's MCP-first architecture directly maps to the recommended MCP-through-gateway model |
| **Scope tiers** | 4 OpenShift-native tiers for MVP (user/project/role/org) | **Partial** — MemoryHub has 6 tiers (user/project/campaign/role/organizational/enterprise); the strategy recommends shipping 4 and keeping the rest as design horizon. MemoryHub's scope model is *richer* than the MVP needs, which is a simplification task, not a gap |
| **SQL-level RBAC enforcement** | Row-level scope RBAC internally enforced | **Strong** — MemoryHub's `core/authz.py` SQL-level enforcement is exactly the pattern the architecture recommends |
| **Inline curation pipeline** | PII/secrets scanning on memory writes; contradictory memories flagged | **Strong** — MemoryHub's three-tier deterministic curation pipeline (schema validation, regex scanning, embedding similarity) is the reference implementation |
| **Contradiction detection** | Contradictory memories flagged | **Strong** — MemoryHub's `contradiction_reports` table and threshold-based surfacing is the reference design |
| **OAuth 2.1 auth** | Platform identity integration (Spire/Authbridge, RFC 8693 token exchange) | **Partial** — MemoryHub has a standalone OAuth 2.1 server. The recommended architecture consumes *platform* identity, not a standalone service. The OAuth 2.1 foundation is solid; the integration target is different |
| **Cache-optimized assembly** | KV-cache-aware ordering | **Strong** — MemoryHub's cache-optimized assembly (SDK v0.5.0) is the direct implementation of this recommended capability |

**Gap analysis:**

| Gap | Severity | Notes |
|---|---|---|
| **No audit trail** | High | Stub interface only (issue #67). The recommended architecture requires a minimum write-event log at Dev Preview and a full append-only audit trail at GA ([strategy](/features/agent-memory/strategy/agent-memory-strategy.md) §6.1) |
| **Skeleton Kubernetes operator** | High | The recommended architecture requires an OLM-integrated operator for lifecycle management. MemoryHub's `planning/operator.md` has CRD concepts but no implementation |
| **Limited observability** | High | No Prometheus metrics, no Grafana dashboards. The recommended architecture requires observable services |
| **Standalone auth (not platform-integrated)** | Medium | MemoryHub's `memoryhub-auth` service issues its own JWTs. The recommended path is platform identity consumption (Q-G6) |
| **8 scope tiers vs. 4** | Low | A simplification task — removing tiers from a working model is easier than adding governance to a model without them |
| **MinIO/Valkey dependencies coded but not active** | Low | These are wired as Python dependencies but not deployed. A productized version would either activate or explicitly remove them based on the deployment model |

**Net architecture-fit assessment:** MemoryHub's governance layer is a strong architectural match for the recommended architecture. The governance model (scope tiers, RBAC, curation, contradiction detection, provenance) maps directly. The substrate layer (PostgreSQL+pgvector, MCP interface) also aligns. The primary gaps are *operational infrastructure* (audit, operator, observability), not *architectural design*. The scope-tier simplification (8 to 4) is a narrowing task, not a redesign.

### 7.4 Adoption Decision Framework

Three adoption paths are evaluated below. Each is assessed against four criteria: engineering effort, IP risk, time-to-market, and architectural alignment with the [recommended architecture](/features/agent-memory/strategy/recommended-architecture.md).

#### Option A: Fork and Productize

**Description:** Take the MemoryHub codebase, fork it into an RHOAI-owned repository, strip to MVP scope (4 scope tiers, remove unused dependencies), and productize — building the operator, audit trail, observability, and platform identity integration on top of the existing code.

| Criterion | Assessment |
|---|---|
| **Engineering effort** | Medium-high. The core code is functional and tested, reducing greenfield work. But the productization gaps (operator, audit, observability, FIPS validation) are significant regardless of starting point. Scope-tier simplification and dependency cleanup add effort. The standalone OAuth server needs to be replaced with platform identity integration |
| **IP risk** | Medium. Requires Q-MH-1 IP transfer. Fork creates a maintenance boundary — upstream MemoryHub changes would not automatically flow into the product fork. Risk of the prototype and product diverging |
| **Time-to-market** | Fastest for the governance layer. The governance model code (scope tiers, RBAC, curation) is the most mature part of MemoryHub and would not need to be reimplemented |
| **Architectural alignment** | High for governance; medium for substrate. The governance layer aligns well. But the recommended architecture uses OGX as the memory substrate (REVIEW-NOTES D5), and MemoryHub's substrate layer is its own PostgreSQL-backed service, not OGX. A fork-and-productize path would need to either (a) replace MemoryHub's substrate with OGX or (b) abandon the OGX-as-substrate decision |

**Verdict:** Option A is the fastest path to a governance layer but creates tension with the OGX-as-substrate decision. It works if the goal is to ship MemoryHub as a standalone service, but the strategy explicitly decided against that (REVIEW-NOTES D3/D5: OGX is the substrate, MemoryHub is the governance layer, not a standalone product).

#### Option B: Extract Patterns Only

**Description:** Use MemoryHub as a *design reference* only — extract the governance patterns (scope model, RBAC enforcement, curation pipeline design) and reimplement them from scratch on top of the OGX substrate.

| Criterion | Assessment |
|---|---|
| **Engineering effort** | High. Reimplementing the scope model, SQL-level RBAC, curation pipeline, and contradiction detection from scratch is significant work even with MemoryHub as a design reference. The research and design work transfers; the implementation does not |
| **IP risk** | Lowest. No MemoryHub code is used in the product. Q-MH-1 becomes irrelevant for the code (though the design patterns may still benefit from a CLA for IP clarity on the design ideas) |
| **Time-to-market** | Slowest. A ground-up reimplementation of the governance layer delays the 3.6 Dev Preview window |
| **Architectural alignment** | Highest. A clean-sheet implementation can be built directly on the OGX substrate from day one, with no legacy integration baggage |

**Verdict:** Option B maximizes architectural purity but sacrifices time-to-market. It is the right choice only if the IP transfer (Q-MH-1) proves infeasible or if the MemoryHub code is assessed as too far from production quality to be worth adapting. The research assessment is that the code quality is adequate for adaptation (Section 5.2) — making Option B a fallback, not the preferred path.

#### Option C: Hybrid (Recommended)

**Description:** Use MemoryHub's governance layer (scope model, RBAC enforcement, curation engine, contradiction detection, provenance tracking) on top of the OGX memory substrate. MemoryHub-derived code handles *governance* — scope tiers, inline curation, contradiction detection, provenance — while OGX handles *memory storage and retrieval* — the four CoALA access patterns (working/episodic/semantic/procedural), compaction, and vector search. This corresponds to Track A (governed OGX substrate) + Track B (MemoryHub-derived governance layer) from the [strategy](/features/agent-memory/strategy/agent-memory-strategy.md) §4.

| Criterion | Assessment |
|---|---|
| **Engineering effort** | Medium. The governance layer code from MemoryHub (scope model, `core/authz.py`, curation pipeline, contradiction detection) is the most reusable part and the part that has no equivalent in OGX. The substrate code (MemoryHub's own memory CRUD, search, embedding) is *replaced* by OGX primitives rather than adapted. The integration work is a bounded interface between the governance layer and the OGX substrate |
| **IP risk** | Medium. Q-MH-1 IP transfer is still required for the governance-layer code. The scope is narrower than Option A (governance code only, not the full codebase), which may simplify the IP conversation |
| **Time-to-market** | Best balance. Track A (governed OGX substrate) is mostly governance-wrapping of existing code. Track B (MemoryHub-derived governance layer) reuses the governance code that is the most production-capable part of MemoryHub. Both tracks run in parallel. This is the approach the strategy sizes as realistic for the November 2026 Dev Preview window |
| **Architectural alignment** | Highest practical. The OGX-as-substrate decision (REVIEW-NOTES D5) is preserved. The governance layer draws from MemoryHub's differentiated strengths. The recommended architecture's diagram (§2) literally shows "Governance Layer (MemoryHub-derived)" on top of "Memory Substrate (OGX-based)" — this option is the direct implementation of that diagram |

**Verdict:** Option C (the hybrid path) is the recommended adoption approach. It is the direct implementation of the Track A + Track B roadmap from the [strategy](/features/agent-memory/strategy/agent-memory-strategy.md) §4. It preserves the OGX-as-substrate decision, reuses MemoryHub's strongest asset (the governance model), avoids reimplementing proven patterns, and fits the 3.6 Dev Preview timeline.

#### Summary Comparison

| Criterion | Option A (Fork) | Option B (Extract) | Option C (Hybrid) |
|---|---|---|---|
| Engineering effort | Medium-high | High | Medium |
| IP risk | Medium | Low | Medium (narrower scope) |
| Time-to-market | Fastest (governance only) | Slowest | Best balance |
| Architectural alignment | Medium (tension with OGX-as-substrate) | Highest (clean-sheet) | Highest practical |
| **Strategy alignment** | **Low** (contradicts D5) | **Medium** (fallback) | **High** (implements Track A+B) |

### 7.5 Recommendation

**The recommended adoption path is Option C — the hybrid approach (Track A + Track B from the strategy).** This is not a new recommendation; it is the formalization of the decision already made at the review gate (REVIEW-NOTES D3/D5) and articulated in the [Agent Memory Strategy](/features/agent-memory/strategy/agent-memory-strategy.md) §3 and [Recommended Architecture](/features/agent-memory/strategy/recommended-architecture.md) §2.

**Why this is the right path:**

1. **It plays to each asset's strength.** OGX already ships production memory primitives (Conversations, Vector Stores, Files, Prompts, compaction) and is GA'ing in RHOAI 3.5 via the Responses bridge. MemoryHub's governance model (scope tiers, RBAC, curation, contradiction detection) is the most mature of any candidate surveyed. The hybrid lets each asset do what it does best — OGX for storage and retrieval, MemoryHub-derived code for governance — without forcing either to do what it does poorly.

2. **It avoids the OGX-vs-MemoryHub false choice.** The research is explicit that OGX and MemoryHub are complementary, not competing ([00 Executive Summary](00-executive-summary.md) §1; [08 RHOAI & OCP Alignment](08-rhoai-ocp-alignment.md) §4.7). A fork-and-productize path (Option A) would effectively abandon OGX-as-substrate; an extract-patterns-only path (Option B) would discard MemoryHub's working governance code. Neither serves the strategy.

3. **It fits the release cadence.** The 3.5 (August 2026) to 3.6 (November 2026) window is approximately three months. The hybrid approach sizes realistically for this: Track A is governance-wrapping of existing OGX code (not new substrate construction), and Track B reuses MemoryHub's governance code (not a greenfield reimplementation). Dev Preview maturity (not GA) makes the window achievable.

4. **The scope-tier simplification is straightforward.** MemoryHub ships 6 (arguably 8, counting `system` and `session` from the SDK's internal documentation) scope tiers. The strategy recommends 4 OpenShift-native tiers for the MVP (user/project/role/org). Narrowing from a working 6-tier model to a 4-tier model — by making the scope field an extensible enumeration and simply not activating the deferred tiers — is a simplification task, not an architectural redesign. The deferred tiers remain available as a design horizon.

5. **The governance layer is MemoryHub's most transferable asset.** Section 5.5 identifies seven ideas that transfer directly from MemoryHub regardless of the adoption path. All seven are governance-layer concerns: scope model, SQL-level RBAC, cache-optimized assembly, session focus, inline curation, project config wizard, and kagenti integration design. The hybrid approach reuses exactly the code that implements these transferable ideas.

### 7.6 Open Questions for MemoryHub Adoption

The following questions must be resolved before or during the adoption process. Several are inherited from Section 6 and the strategy's §8; they are consolidated here with adoption-specific context.

| Question | Origin | Description | Dependency |
|---|---|---|---|
| **Q-MH-1** | §5.4, strategy §8 | IP/copyright transfer for MemoryHub code. Currently held by Wes Jackson individually. CLA or copyright assignment required before Track B code can be productized. | **Administrative prerequisite for Track B.** Must be initiated before engineering begins on MemoryHub-derived governance code. Schedule risk if delayed. |
| **Q-G2** | strategy §8 | OGX substrate target — the exact OGX API surface in RHOAI 3.5, the May-2026 multi-tenancy work, and the gateway-native Responses replacement plan. | **Gates Track A design.** The governance layer wraps OGX primitives; Track A's design depends on knowing which primitives are available. |
| **Q-G6** | strategy §8 | Platform identity vs. MemoryHub's standalone OAuth. Should the memory service consume Spire/Authbridge/RFC 8693 token exchange, or retain a standalone auth service? | **Determines auth integration architecture.** The recommendation is to consume platform identity; the standalone `memoryhub-auth` service would be retired in a productized deployment. |
| **Q-MH-2** | §6, strategy §6.2 | Scope-tier model — whether MemoryHub's `campaign`, `organizational`, and `enterprise` tiers should be carried as active (but dormant) tiers or removed from the 3.6 codebase entirely. | **Design decision for Track B.** The strategy recommends 4 tiers for the MVP with an extensible enumeration; the implementation question is whether deferred tiers exist as inactive code or are absent entirely. |
| **Q-MH-3** | §6 | Standalone auth vs. platform identity — resolved in principle by Q-G6 but implementation details remain open (how does token exchange work? what identity claims does the governance layer consume?). | **Track B auth integration.** |
| **Q-MH-4** | §6 | Scale boundaries — the memory-per-user and concurrent-agent ceiling. The hybrid approach inherits OGX's scale characteristics for the substrate and MemoryHub's for the governance layer. | **Design-time measurement task (Q-G4).** Not a blocker; informs scaling decisions. |
| **Knowledge transfer** | New | Single-author bus factor. Regardless of the IP transfer path, product engineering needs a knowledge transfer from the MemoryHub author (Wes Jackson) covering architecture decisions, design rationale, and known limitations not captured in documentation. | **Should be initiated concurrently with Q-MH-1.** |
| **Dependency audit** | New | Formal license-compatibility verification of MemoryHub's Python dependencies for Red Hat product distribution. All known dependencies are OSS-licensed; no anticipated blockers, but the formal audit is a standard product prerequisite. | **Required before product inclusion; can run in parallel with engineering work.** |

---

## Sources

### Internal (Repository)

| Source | Type | Path |
|---|---|---|
| Agent Memory & Knowledge working doc | Internal seed document | `docs/knowledge-review/assets/agent-memory-knowledge.md` |
| Knowledge Registry — MemoryHub entry | Registry row | `docs/knowledge-registry.md` (line 869) |
| Agent Memory Landscape & Definitions | Sibling research doc | `agent-memory/research/01-landscape-and-definitions.md` |
| Agent Memory Solution Survey | Sibling research doc | `agent-memory/research/02-solution-survey.md` |
| RHAISTRAT-1345 | Jira Outcome | https://redhat.atlassian.net/browse/RHAISTRAT-1345 |
| Kagenti & Kubernetes Deep-Dive | Style/depth reference | `agents/agent-registry/research/03-kagenti-and-kubernetes.md` |
| Agent Memory Strategy (Phase 2) | Strategy doc | `agent-memory/strategy/agent-memory-strategy.md` |
| Recommended Architecture (Phase 2) | Architecture doc | `agent-memory/strategy/recommended-architecture.md` |
| REVIEW-NOTES | Review gate decisions | `agent-memory/research/REVIEW-NOTES.md` |

### External — MemoryHub Repository Files

All files below are from `https://github.com/redhat-ai-americas/memory-hub` (main branch, as of 2026-05-07). Access was via `gh repo view`, `gh api`, and direct `curl` to `raw.githubusercontent.com`.

| File | Key content used |
|---|---|
| `README.md` | Project overview, status claim (2026-04-15), architecture summary, install instructions, roadmap |
| `NOTICE` | Copyright holder (Wes Jackson), Apache 2.0 |
| `pyproject.toml` | Dependencies (SQLAlchemy, asyncpg, pgvector, pydantic, minio, alembic, redis), Python ≥3.11 requirement, author field |
| `CHANGELOG.md` | SDK version history (v0.1.0–v0.7.0), key feature additions by release |
| `.memoryhub.yaml` | Live config schema: `memory_loading` and `retrieval_defaults` fields |
| `docs/ARCHITECTURE.md` | System diagram, data flow sequences (write path, search-without-focus, search-with-focus), auth model, deployment topology |
| `docs/SYSTEMS.md` | Subsystem inventory and status table (Implemented/Design/Skeleton/TBD), dependency graph, "What's not yet shipped" section |
| `docs/governance.md` | Five/six-tier scope access rules, immutable audit trail design, FIPS delegation strategy, secrets/PII detection categories, EU AI Act alignment, attribution problem defense |
| `docs/memory-tree.md` | Tree-based data model, node properties (content/weight/scope/branches/version metadata/embedding), scope hierarchy, versioning model, rationale branches |
| `docs/mcp-server.md` | Tool surface (compact/full/minimal profiles), search response shape (mode/max_response_tokens/include_branches), session focus retrieval pipeline, campaign scope and domain tagging, authentication model |
| `docs/curator-agent.md` | Write-time curation pipeline (Tier 0/1/2), no-inline-sampling design decision, similarity feedback on write, response shape |
| `docs/storage-layer.md` | PostgreSQL responsibilities, pgvector, graph relationships table schema, contradiction_reports table schema, adjacency lists vs. AGE decision |
| `research/vllm-cache-optimization.md` | vLLM APC mechanics, block-level granularity, llm-d cache-aware routing, cache-optimized assembly design implications |
| `docs/agent-memory-ergonomics/design.md` | Session focus design rationale, two-vector retrieval candidates and benchmark, stub policy, `.memoryhub.yaml` schema and loading patterns |
| `planning/operator.md` | Kubernetes operator design: CRD concepts (MemoryHub, MemoryTier), operator responsibilities, skeleton status |
| `planning/kagenti-integration/overview.md` | Kagenti capability delta table, three-phase integration approach |
| `retrospectives/2026-04-03_phase-1-foundation/RETRO.md` | Milvus+Neo4j → PostgreSQL pivot rationale, FastMCP 2 → 3 migration, key design pivots, gaps identified |

### External — Third-Party References

| Source | URL | Used for |
|---|---|---|
| vLLM APC research (cited in memory-hub research doc) | https://docs.vllm.ai (general reference) | Cache hit rate mechanics corroboration |
| llm-d CNCF Sandbox project | https://github.com/llm-d/llm-d | Cache-aware routing performance figures |
| Wes Jackson: "When Agent Memory Becomes a Platform Concern" | https://medium.com/@wjackson_63436/when-agent-memory-becomes-a-platform-concern-4b6cd23af47f | Author background, platform-tier framing |

### Access Notes

The `redhat-ai-americas/memory-hub` repository is public and was read directly via `gh api` and `curl` to `raw.githubusercontent.com`. All file citations were verified against live content. The most recent commit examined was `ec2bed28` (2026-05-07, Wes Jackson). No content was fabricated from the internal seed document; every claim is cross-referenced against the repo files listed above.

A private peer repository (`rdwj/memory-hub-research`) was created in the 2026-05-07 commit to hold competitive comparisons, blog drafts, and positioning material. Content from that private repo is not available and was not used in this document.
