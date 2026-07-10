---
title: "Agent Memory & Knowledge: OGX Memory Primitives"
description: Deep research into OGX (formerly Llama Stack) memory-related primitives and what the OGX trajectory means for RHOAI's agent memory strategy.
source: ai-asset-registry/agent-memory/research/06-ogx-memory-primitives.md (as of 2026-07-05)
timestamp: 2026-07-06
review_after: 2026-08-05
---

# Agent Memory & Knowledge: OGX Memory Primitives

**Purpose:** Deep research into OGX (formerly Llama Stack) memory-related primitives — what exists, what Francisco Arceo has contributed, and what the OGX trajectory means for RHOAI's agent memory strategy.

**Date:** 2026-05-17

**Status:** EXPLORATORY — OGX is an active open-source project. Memory primitives in OGX are in production (Conversations, Vector Stores, Responses compaction) but multi-tenancy and governance features are newly landed (May 2026) and not yet validated in RHOAI context. Nothing in this document represents a decided RHOAI design.

**Series:** Document 06 of 17 — Agent Memory & Knowledge Research
**Phase 1:** [00](00-executive-summary.md) · [01](01-landscape-and-definitions.md) · [02](02-solution-survey.md) · [03](03-memoryhub-deep-dive.md) · [04](04-technical-patterns.md) · [05](05-standards-and-protocols.md) · 06 OGX Memory Primitives (this doc) · [07](07-taxonomy-and-decomposition.md) · [08](08-rhoai-ocp-alignment.md)
**Phase 2:** [09](09-agent-harness-memory.md) · [10](10-claude-memory-dreaming.md) · [11](11-adversarial-memory.md) · [12](12-benchmarking-evaluation.md) · [13](13-kv-cache-optimization.md) · [14](14-enterprise-use-cases.md) · [15](15-multi-modal-memory.md) · [16](16-ai-gateway-memory-substrate.md) · [REVIEW-NOTES](REVIEW-NOTES.md)

**Repo access:** The `ogx-ai/ogx` repository is publicly accessible on GitHub. All code-level claims in this document were verified from repository files, GitHub API responses, and PR bodies as of 2026-05-17. No claims about commits, PR numbers, file paths, or API signatures were invented.

**IMPORTANT VERIFICATION NOTE — Llama Stack Relationship:** The OGX README includes the following statement at the top of the repository: *"Llama Stack is now OGX. The name changed, and so did the mission — model-agnostic, multi-SDK, production-grade."* This was verified by direct GitHub API query on 2026-05-17. The relationship is confirmed.

---

## Contents

1. [What OGX Is and Its Relationship to Llama Stack and RHOAI](#1-what-ogx-is-and-its-relationship-to-llama-stack-and-rhoai)
2. [OGX Architecture Overview](#2-ogx-architecture-overview)
3. [Memory Primitives — What OGX Provides Today](#3-memory-primitives--what-ogx-provides-today)
4. [Francisco Arceo's Contributions](#4-francisco-arceos-contributions)
5. [OGX Memory Direction and RHOAI Agent Memory Strategy](#5-ogx-memory-direction-and-rhoai-agent-memory-strategy)
6. [Contrast with MemoryHub](#6-contrast-with-memoryhub)
7. [Open Questions and Review Gate Items](#7-open-questions-and-review-gate-items)

---

## 1. What OGX Is and Its Relationship to Llama Stack and RHOAI

### 1.1 Confirmed Relationship: Llama Stack is Now OGX

**DECIDED (by OGX project)** — The OGX repository (`ogx-ai/ogx`) is the direct continuation and rename of Llama Stack. The OGX README states explicitly:

> "Llama Stack is now OGX. The name changed, and so did the mission — model-agnostic, multi-SDK, production-grade."

The `ogx-ai/ogx` repository was created on 2024-06-25 and has accumulated 8,377 stars and 1,309 forks as of 2026-05-17. (Note: the GitHub `created_at` date reflects the original Llama Stack repository transferred into the `ogx-ai` org — `gh api repos/ogx-ai/ogx` returns `"created_at":"2024-06-25T22:32:26Z"`, confirmed 2026-05-17.) The codebase is the same codebase under a new name. The Python SDK remains `ogx-client`, which wraps `LlamaStackClient` by name (visible in notebooks and the VectorIO tutorial). The description on GitHub is "Open GenAI Stack."

The name change reflects a deliberate repositioning: from Meta's model-specific Llama server to a **model-agnostic, multi-SDK, production-grade agentic API server**. This is more than a rename — it is a mission expansion (see Section 2).

Source: `gh repo view ogx-ai/ogx` (verified 2026-05-17); `ogx-ai/ogx` README content.

### 1.2 Why This Matters Directly for RHOAI

**DECIDED (AI Gateway F2F, April 21-23, 2026)** — RHOAI 3.5 is GA'ing the current Llama Stack implementation as a **bridge** for the Responses API. The architectural decision from the AI Gateway F2F is:

> "GA current Llama Stack as a bridge in 3.5; architecture allows replacement within ~6 months."

Since Llama Stack is now OGX, this means:
1. RHOAI 3.5 will GA OGX (the Llama Stack codebase) as a bridge for the Responses API.
2. Red Hat engineers, including Francisco Arceo, are already contributing to OGX upstream.
3. The ~6-month replacement clock creates a window where OGX's own direction (especially multi-tenancy, memory primitives) directly affects what Red Hat inherits and builds on top of.
4. The planned "gateway-native, multi-tenant Responses implementation" (the eventual RHOAI replacement for the OGX bridge) will need to replicate or delegate to the memory primitives OGX has defined.

Source: `docs/knowledge-review/components/ai-gateway.md` (RHOAI internal); AI Gateway F2F notes (April 2026).

### 1.3 Mission Expansion: From Llama Server to Protocol Hub

**REFERENCE** — The OGX blog post "Every Protocol. Every Framework. Zero Code Changes." (2026-05-11, author: leseb / Sébastien Han, Red Hat) articulates the expanded mission:

> "OGX exists to break that coupling. It's a server that speaks every major agentic protocol natively, translating them to any model running on any infrastructure."

("That coupling" in context refers to vendor lock-in caused by tight SDK-to-model dependencies — the blog post precedes this line with a description of how each AI vendor SDK is coupled to its own model, forcing teams to rewrite code when switching providers.)

OGX now supports three API surfaces simultaneously on a single server:
- **OpenAI API** — Chat Completions, Responses API, Embeddings, Vector Stores, Files, Batches, Eval
- **Anthropic Messages API** — `/v1/messages` endpoint via Anthropic SDK
- **Google Interactions API** — `/v1alpha/interactions` endpoint via Google GenAI SDK

This is significant for RHOAI: if OGX is the bridge, it means the Responses API bridge is on a server that also speaks Anthropic and Google protocols. When Red Hat builds the gateway-native replacement, it will need to match this multi-protocol surface.

Source: `docs/blog/2026-05-11-consistent-agentic-api-layer.md` in the OGX repo.

---

## 2. OGX Architecture Overview

**REFERENCE** — Understanding OGX's architecture is prerequisite to understanding its memory primitives.

### 2.1 Core Architecture

OGX is structured as a FastAPI server with a pluggable provider architecture:

```
src/ogx/              # Server implementation
  core/                  # Request routing, server, storage, access control
  providers/
    inline/              # Built-in providers (responses, eval, vector_io, etc.)
    remote/              # Remote provider adapters (OpenAI, Azure, vLLM, Ollama, etc.)
    registry/            # Provider registration specs
    utils/               # Shared provider utilities (OpenAI mixin, MCP, etc.)
src/ogx_api/          # API definitions, Pydantic models, FastAPI routes
```

The server supports multiple inference backends via a pluggable `providers/` architecture: OpenAI, Azure, AWS Bedrock, vLLM, Ollama, WatsonX, Vertex AI, and others. The provider architecture means memory primitives (Vector I/O, Conversations, Responses storage) are also provider-pluggable.

Source: `AGENTS.md` in OGX repo.

### 2.2 Key APIs Relevant to Memory

| API Surface | OGX Endpoint Prefix | Description |
|---|---|---|
| **Responses API** | `/v1/responses` | Stateful agentic orchestration — inference + tool calling + conversation persistence |
| **Conversations API** | `/v1/conversations` | OpenAI-compatible conversation thread management with ordered item storage |
| **Vector Stores** | `/v1/vector_stores` | Managed document storage and semantic search (backed by pluggable Vector I/O) |
| **Files** | `/v1/files` | File upload/management for RAG ingestion into vector stores |
| **Prompts API** | `/v1/prompts` | Versioned prompt management with tenant isolation |
| **Vector I/O** | internal routing | Provider-pluggable vector database backend (FAISS, Chroma, Qdrant, Milvus, pgvector, Weaviate, Elasticsearch, Infinispan, sqlite-vec) |

Source: `AGENTS.md`; `src/ogx_api/` directory listing; `docs/docs/providers/vector_io/` (OGX repo).

### 2.3 Governance Architecture: AuthorizedSqlStore

**EXPLORATORY (newly landed)** — A cross-cutting governance primitive was added in May 2026: `AuthorizedSqlStore` (`src/ogx/core/storage/sqlstore/authorized_sqlstore.py`). This is an ABAC-based (Attribute-Based Access Control) SQL store wrapper that enforces row-level tenant isolation across multiple OGX subsystems. Its design:

- Every record in an `AuthorizedSqlStore`-backed table carries `owner_principal` and `access_attributes` columns.
- Access policies are defined as `AccessRule` objects evaluating claims from JWT tokens.
- Public records (no `access_attributes`) are universally accessible; records with attributes require the requesting user to match at least one attribute category.
- Cross-tenant access returns `404` (not `403`) to prevent resource enumeration.
- A `SQL_OPTIMIZED_POLICY` constant implements the default policy directly in SQL WHERE clauses to avoid Python-level O(n) filtering.

This store is the governance backbone for the memory primitives described in Section 3.

Source: `src/ogx/core/storage/sqlstore/authorized_sqlstore.py` (OGX repo, read 2026-05-17).

---

## 3. Memory Primitives — What OGX Provides Today

OGX's memory-relevant primitives fall into four distinct layers: (1) working/session memory via Conversations, (2) context compaction for long-running agents, (3) semantic/episodic memory via Vector Stores and Files, and (4) procedural memory via Prompts. Each is described below.

### 3.1 Conversations API — Working/Session Memory

**REFERENCE (production)** — The Conversations API provides per-turn item storage for multi-turn agent sessions. It is an OpenAI-compatible `/v1/conversations` API backed by `AuthorizedSqlStore`.

**Schema:**

```python
class Conversation(BaseModel):
    id: str            # "conv_<48-hex-chars>"
    object: "conversation"
    created_at: int    # Unix epoch
    metadata: dict     # Up to 16 key-value pairs

ConversationItem = Union[
    OpenAIResponseMessage,
    OpenAIResponseOutputMessageFileSearchToolCall,
    OpenAIResponseOutputMessageFunctionToolCall,
    OpenAIResponseInputFunctionToolCallOutput,
    OpenAIResponseMCPApprovalRequest | Response,
    OpenAIResponseOutputMessageMCPCall | MCPListTools,
    OpenAIResponseOutputMessageReasoningItem,
    OpenAIResponseCompaction,   # ← compaction items are first-class
]
```

> **Note:** The `ConversationItem` union above is a simplified/representative rendering. The actual type union in `src/ogx_api/conversations/models.py` includes additional members (e.g., `OpenAIResponseOutputMessageWebSearchToolCall`) and may use slightly different type names from those shown. Refer to the source file for the verbatim definition.

**Implementation details:**

- Two SQL tables: `openai_conversations` (metadata, one row per conversation) and `conversation_items` (items, one row per turn item, with a `sort_order` INTEGER column for deterministic ordering).
- The `sort_order` column was added in PR #5850 (Derek Higgins, merged 2026-05-15, SHA `791a0484`) to fix non-deterministic ordering when multiple `add_items` calls land within the same second. The fix replaces `created_at`-based ordering with a monotonically increasing per-conversation counter.
- Compaction items (`OpenAIResponseCompaction`) are a first-class `ConversationItem` type — the conversation history can include compaction summaries as items.
- The API supports `create`, `retrieve`, `update`, `delete` on conversations, and `add_items`, `list_items`, `retrieve_item`, `delete_item` on items.

Source: `src/ogx/core/conversations/conversations.py`; `src/ogx_api/conversations/models.py`; PR #5850 body (OGX repo, 2026-05-17).

### 3.2 Responses API — The Agentic Loop with Integrated Memory

**REFERENCE (production)** — The Responses API (`/v1/responses`) is OGX's stateful agentic orchestration surface. It is the API Llama Stack originally implemented for RHOAI 3.5, and it is the most memory-relevant API in the stack.

**Memory mechanics within the Responses API:**

1. **`previous_response_id` chaining** — Multi-turn conversations are stored incrementally. When `previous_response_id` is set, only the new input items for the current turn are stored (not the full accumulated history). The full chain is reconstructed on read by walking the `previous_response_id` ancestry chain. This reduces storage from O(n²) to O(n) for multi-turn conversations (PR #5804, Sébastien Han / leseb, Red Hat, merged 2026-05-15, SHA `cdb4f29a`).

2. **Auto-compaction via `context_management`** — The `responses.create` call accepts a `context_management` parameter. When the token count exceeds `compact_threshold`, the server automatically compacts the conversation history into a summarized form before the next inference call. This is server-side working-memory management.

3. **`POST /v1/responses/compact`** — A standalone endpoint for explicit compaction requests. Takes the current conversation state, calls the configured `summarization_model` (defaulting to the conversation model), and produces a `response.compaction` object. The summary framing uses two configurable prompts (see Section 3.3).

4. **Background response processing** — Long-running agent loops can run as background tasks, decoupled from the client connection. A `BACKGROUND_RESPONSE_TIMEOUT_SECONDS = 300` (5 minutes) governs background task lifetime.

5. **Integrated file_search** — The Responses API natively supports `file_search` as a server-side tool, automatically invoking vector store retrieval without client-side code.

6. **Integrated MCP tools** — The agentic loop includes direct MCP server integration (`src/ogx/providers/remote/tool_runtime/model_context_protocol/`), making OGX a hub for MCP-connected memory systems.

Source: `src/ogx/providers/inline/responses/builtin/responses/openai_responses.py`; `src/ogx/providers/inline/responses/builtin/config.py`; PR #5804 (Sébastien Han / leseb, OGX repo, 2026-05-17).

### 3.3 Context Compaction — CompactionConfig

**REFERENCE (production)** — Compaction configuration is a first-class server-side primitive, not a client-side concern.

**`CompactionConfig` fields** (from `src/ogx/providers/inline/responses/builtin/config.py`):

> **Note:** The default values in the table below are abbreviated for readability. The actual defaults are multi-sentence strings. For example, the real `summarization_prompt` default begins `"You are performing a CONTEXT CHECKPOINT COMPACTION..."` (not `"CONTEXT CHECKPOINT COMPACTION..."`). Refer to `config.py` in the OGX repo for the verbatim text.

| Field | Default (abbreviated) | Purpose |
|---|---|---|
| `summarization_prompt` | "You are performing a CONTEXT CHECKPOINT COMPACTION. Create a handoff summary for another LLM that will resume the task." (abbreviated) | Instructs the model to produce a structured handoff |
| `summary_prefix` | "Another language model started to solve this problem and produced a summary of its thinking process..." | Frames the summary as a prior-LLM handoff for the receiving model |
| `summarization_model` | None (uses conversation model) | Separate model for generating summaries |
| `default_compact_threshold` | None | Per-server default token threshold for auto-compaction |
| `tokenizer_encoding` | None | Admin-level default tiktoken encoding |
| `model_tokenizer_mappings` | `{llama, mistral, claude, gemma, qwen, phi, deepseek: cl100k_base}` | Model-family prefix → tiktoken encoding heuristic |

**5-step tokenizer resolution chain** (PR #5791, Francisco Arceo, May 2026): Compaction requires token counting. OGX resolves the tokenizer via a 5-step chain: (1) per-request `extra_body` override, (2) admin `CompactionConfig.tokenizer_encoding`, (3) tiktoken built-in model lookup, (4) model-family prefix mapping (the `model_tokenizer_mappings` dict), (5) character-based fallback (`max(1, len(text) // 4)`). This means compaction never fails on non-OpenAI models — it degrades gracefully.

**RHOAI relevance:** The AI Gateway F2F identified "OpenAI auto-compaction behavior" as an open item — "OpenAI auto-compaction (summarizing conversation history) cannot be reproduced exactly by the gateway." OGX's `CompactionConfig` is the concrete implementation of this pattern in the Llama Stack bridge, and represents one approach Red Hat can study when designing the gateway-native replacement.

Source: `src/ogx/providers/inline/responses/builtin/config.py` (OGX repo); `docs/knowledge-review/components/ai-gateway.md` (RHOAI internal).

### 3.4 Vector Stores and Files — Semantic/Episodic Memory

**REFERENCE (production)** — OGX implements the OpenAI Vector Stores and Files APIs (`/v1/vector_stores`, `/v1/files`). These provide long-term document storage with semantic search — functioning as a managed semantic/episodic memory substrate.

**Provider matrix** (from `docs/docs/providers/vector_io/`):

| Provider Type | Backends |
|---|---|
| Inline (bundled) | FAISS, Chroma, Qdrant, Milvus, sqlite-vec |
| Remote (external service) | Chroma, Elasticsearch, Infinispan, Milvus, OCI, pgvector, Qdrant, Weaviate |

**Retrieval configuration** (from `VectorStoresConfig` in `inline_builtin` provider docs):

| Parameter | Default | Purpose |
|---|---|---|
| `default_search_mode` | `vector` | Search mode: `vector`, `keyword`, or `hybrid` |
| `default_reranker_strategy` | `rrf` | Reranker: `rrf` (Reciprocal Rank Fusion), `weighted`, `normalized` |
| `rrf_impact_factor` | 60.0 | RRF impact parameter |
| `chunk_multiplier` | 5 | Over-retrieval factor for OpenAI API compatibility |
| `max_tokens_in_context` | 4000 | Token budget for RAG context before truncation |
| `default_chunk_size_tokens` | 512 | Default ingestion chunk size |
| `default_chunk_overlap_tokens` | 128 | Chunk overlap for context continuity |

**Contextual retrieval** — OGX supports contextual retrieval during file ingestion: an LLM call contextualizes each chunk before embedding, improving retrieval quality. This mirrors Anthropic's "contextual embeddings" pattern from the technical patterns survey.

**Query rewriting** — A `rewrite_query_params` config enables LLM-based query expansion: the query is paraphrased with synonyms before searching, improving recall.

**Tenant isolation for vector store metadata** — Prior to May 2026, vector store metadata was stored in KVStore with no tenant isolation. PR #5782 (Francisco Arceo, May 2026) migrated all 9 vector_io providers to `AuthorizedSqlStore` for row-level tenant isolation (see Section 4.2 for full context). An automatic migration path converts existing KVStore records on first startup.

Source: `docs/docs/providers/responses/inline_builtin.mdx`; `src/ogx/providers/utils/memory/vector_store.py`; `src/ogx/providers/utils/memory/openai_vector_store_mixin.py` (OGX repo).

### 3.5 Prompts API — Versioned Procedural Memory

**REFERENCE (production)** — The Prompts API (`/v1/prompts`) provides versioned, tenant-isolated storage for system prompts and prompt templates. It maps onto what Oracle's four-type taxonomy calls "procedural memory" — durable behavioral rules the agent consults on each invocation.

**Key properties:**
- `prompts` SQL table via `AuthorizedSqlStore` with `owner_principal` and `access_attributes` for tenant isolation.
- Schema: `id`, `prompt_id`, `version` (integer), `is_default` (boolean), `created_at`, `prompt_data` (JSON).
- Operations: `create_prompt`, `get_prompt`, `list_prompts`, `list_prompt_versions`, `update_prompt`, `delete_prompt`, `set_default_version`.
- Agents can read their own current prompt at runtime (`GET /v1/prompts/{prompt_id}`), update it programmatically, and pin specific versions.

**Self-improving agent pattern** — The OGX blog post "Building a Self-Improving Agent with OGX" (2026-03-01) demonstrates an agent that reads, evaluates, and rewrites its own system prompt via the Prompts API. This is a working example of procedural memory as a first-class runtime primitive.

Source: `src/ogx/core/prompts/prompts.py`; `docs/blog/2026-03-01-building-agentic-flows.md` (OGX repo).

---

## 4. Francisco Arceo's Contributions

Francisco Arceo (`farceo@redhat.com` / GitHub: `franciscojavierarceo`) is a Red Hat engineer who is already a stakeholder in the knowledge registry (cited in RHAISTRAT-1345 as a subject-matter expert on client-side vs. server-side memory). He has a significant and ongoing contribution record in the OGX repository. All contributions below were verified from the GitHub API (`gh api repos/ogx-ai/ogx/commits?author=franciscojavierarceo`) as of 2026-05-17.

**IMPORTANT ACCURACY NOTE:** The claims below are sourced from PR bodies and commit messages verified via the GitHub API. PR numbers, commit SHAs, and titles are confirmed. Contributor names are confirmed via the `Signed-off-by` trailers in commit bodies.

### 4.1 Multi-Tenancy Core for MaaS Deployments (PR #5756, May 7, 2026)

The foundational multi-tenancy contribution. PR title: "feat!: multi-tenancy core for MaaS deployments." SHA: `dafb79e3`.

**What it adds:**
- `AuthorizedSqlStore` — the ABAC-based row-level tenant isolation store now used across all memory-related subsystems.
- `owner_principal` tracking wired through prompts and inference stores.
- `fairness_header_attribute` config for extracting user identity from JWT claims.
- `set_default_version` atomicity fix in prompts to prevent race conditions.
- Escaped-dot support (`\.`) in `claims_mapping` for Kubernetes service account tokens.
- Integration tests for prompts tenant isolation using an Alice/Bob two-user pattern.

**Why this is significant for RHOAI:** Multi-tenancy is the first enterprise requirement for any shared memory system. Without it, all agents in a cluster share memory state. PR #5756 is the foundational primitive that makes per-user, per-team memory isolation possible in OGX. Given that RHOAI 3.5 is GA'ing OGX as the Responses API bridge, this multi-tenancy work is directly in the RHOAI production path.

### 4.2 Vector I/O Tenant Isolation (PR #5782, May 12, 2026)

PR title: "feat(vector_io): add tenant isolation for vector store metadata." SHA: `ef8cf459`.

**What it adds:**
- Migrates `OpenAIVectorStoreMixin` metadata storage from KVStore to `AuthorizedSqlStore`.
- Covers all 9 vector_io providers: faiss, sqlite-vec, chroma, qdrant, milvus, pgvector, weaviate, elasticsearch, infinispan.
- Adds `vector_stores` SqlStoreReference to `ServerStoresConfig`.
- Adds `metadata_store` config field to each provider for SQL-backed metadata.
- Automatic KVStore-to-SQL migration on first startup after upgrade (idempotent, SQLite and Postgres).
- Integration tests using Alice/Bob pattern in the auth CI workflow.
- Backward compatibility: providers without `metadata_store` configured continue using KVStore.

**Significance:** Vector Stores are OGX's semantic/episodic memory substrate. This PR makes vector store ownership tenant-scoped: Alice's vector stores are invisible to Bob even on the same OGX deployment. This is necessary for any multi-tenant deployment, including RHOAI.

### 4.3 Conversation Compaction for Responses API (PR #5327, April 8, 2026)

PR title: "feat: add conversation compaction support to Responses API." SHA: `462d4051`.

**What it adds:**
- `POST /v1/responses/compact` endpoint — standalone compaction call.
- `context_management` parameter on `responses.create` — auto-compaction when token count exceeds `compact_threshold`.
- LLM-based summarization producing a `compaction` item (type: `OpenAIResponseCompaction`).
- Compaction items round-trip as assistant context and are filtered from `input_items` API (matching OpenAI behavior).
- zstd request body decompression for Codex CLI compatibility.
- End-to-end tested with OpenAI Codex CLI v0.118.0 connecting through OGX as a proxy to OpenAI.

**Significance:** This is the first implementation of context compaction in the Llama Stack/OGX codebase. The RHOAI AI Gateway F2F identified conversation compaction as an open item for the gateway-native Responses implementation. Arceo's PR is the reference implementation that the gateway team will need to study or replicate.

### 4.4 O(n) Storage Optimization for Multi-Turn Conversations (PR #5804, May 2026)

> **Note:** PR #5804 was authored by **Sébastien Han** (GitHub: `leseb`, Red Hat) — *not* Francisco Arceo. It is included here because it is a closely related peer-contributor PR that complements Arceo's work in this area. Authorship confirmed via `gh api repos/ogx-ai/ogx/pulls/5804 --jq .user.login` (returns `leseb`).

PR title: "feat(responses): optimize storage from O(n²) to O(n) for multi-turn conversations." Merge SHA: `cdb4f29a`. Merged 2026-05-15. Author: Sébastien Han (`leseb`).

**What it addresses:** Multi-turn conversations with `previous_response_id` previously stored the full accumulated input from all prior turns per response — O(n²) total storage. This PR implements incremental storage (only new input items per turn) with chain reconstruction on read.

**Technical design:**
- `input_storage_mode=incremental` marker on non-compaction responses.
- Compaction snapshots bypass incremental mode (full content preserved at compaction boundaries).
- Delete safety: before deleting a response, incremental direct children are materialized.
- Backward compatibility: mixed old/new chains handled by stopping reconstruction at the first non-incremental ancestor.

**Significance:** This is foundational storage engineering for long-running agent sessions. Without it, a 100-turn agent session produces 100× more storage than necessary, making persistent multi-session agents impractical at scale.

### 4.5 Connectors and Batches Migration (PR #5757, May 8, 2026)

PR title: "feat(connectors,batches)!: migrate KVStore to AuthorizedSqlStore." SHA: `d30a6030`.

Completes the migration of connector and batch storage to `AuthorizedSqlStore`, extending the tenant isolation model to these subsystems.

### 4.6 5-Step Tokenizer Resolution for Compaction (PR #5791, May 12, 2026)

PR title: "feat(compaction): add 5-step tokenizer resolution chain for non-OpenAI models." SHA: `bcc25660`.

Makes compaction work for any model, not just OpenAI-named models. Particularly important for RHOAI deployments where models are Llama, Mistral, Phi, or other open-weight models on vLLM. The `model_tokenizer_mappings` dict covers 7 model families by default and is admin-configurable.

### 4.7 Earlier Foundational Contributions

The GitHub commit history shows Arceo has been contributing to OGX since before the rename. Earlier verified contributions include:

- **PR #3743** — "feat: Add support for Conversations in Responses API" — the initial Conversations API integration into the Responses API flow.
- **PR #4471** — "feat: Enable Filters in OpenAI Search API" — filter support for vector search, enabling metadata-scoped retrieval.
- **PR #3803** / **#3818** — Default embedding model configuration in the stack.
- **PR #3774** — Breaking change removing VectorDB APIs in favor of the Vector Stores API.
- **PR #3698** — Enabling annotations in Responses (source citations in RAG results).

### 4.8 Summary Assessment of Arceo's Memory-Related Contributions

Francisco Arceo has been the primary driver of three distinct memory-related capability areas in OGX:

| Area | Contribution | RHOAI Relevance |
|---|---|---|
| **Context compaction** | `POST /v1/responses/compact`, `context_management` parameter, tokenizer resolution chain | Direct — the AI Gateway F2F named this as an open item for gateway-native Responses |
| **Multi-tenancy** | `AuthorizedSqlStore`, ABAC row-level isolation for prompts, vector stores, conversations, connectors, batches | Direct — required for any shared RHOAI memory deployment |
| **Semantic memory storage** | Tenant-isolated vector stores (PR #5782), conversation item ordering (PR #5850 / Derek Higgins) | Direct — these are the building blocks for persistent agent sessions |
| **Storage optimization** (peer contributor) | O(n) multi-turn storage (PR #5804, **Sébastien Han / leseb**, not Arceo) | Direct — reduces storage cost for long-running agent sessions |

This is not "starting to add memory primitives" in an exploratory sense — Arceo has shipped production-grade memory primitives into the codebase that are active in the RHOAI 3.5 bridge. The gap is that these primitives are in OGX upstream but not yet exposed as governed, first-class RHOAI platform features.

---

## 5. OGX Memory Direction and RHOAI Agent Memory Strategy

### 5.1 What OGX Already Provides as Memory Primitives

Mapping OGX's existing primitives to the Oracle four-type taxonomy (see [doc 01](01-landscape-and-definitions.md)):

| Oracle Memory Type | OGX Implementation | Status |
|---|---|---|
| **Working memory** | Responses API in-flight state; `previous_response_id` chain; background task queue | Production |
| **Semantic memory** | Vector Stores API (`/v1/vector_stores`) with 9 pluggable backends | Production |
| **Episodic memory** | Conversations API (`/v1/conversations`) — ordered turn history | Production |
| **Procedural memory** | Prompts API (`/v1/prompts`) — versioned, tenant-isolated system prompts | Production |
| **Context compaction** | `POST /v1/responses/compact`; `context_management` parameter | Production (PR #5327) |
| **Tenant isolation** | `AuthorizedSqlStore` ABAC across all memory subsystems | Production (PR #5756+) |

This is a more complete memory primitive coverage than any single memory startup offers — OGX ships working, semantic, episodic, and procedural memory in one server.

### 5.2 What OGX Does Not Provide (Gaps vs. Full Enterprise Memory)

Relative to what MemoryHub (doc 03) and the requirements in RHAISTRAT-1345 call for:

| Gap | Description |
|---|---|
| **No multi-tier scope isolation** | OGX isolates per user/principal (row-level). MemoryHub implements 5-tier hierarchy: user / project / role / organizational / enterprise. OGX has no concept of "organizational" or "campaign" scoping. |
| **No knowledge graph** | OGX has no graph-based relational memory. All retrieval is vector similarity or keyword BM25. No entity relationship modeling, no contradiction detection. |
| **No memory curation / provenance** | OGX stores items but has no automated extraction, no version history with provenance branches, no contradiction detection, no memory promotion pipeline. |
| **No cross-session shared memory** | Vector stores and conversations are per-principal. There is no native mechanism for multiple agents to share a common memory pool (e.g., MemoryHub's "swarm coherence" / project-scoped memory). |
| **No audit trail** | The `AuthorizedSqlStore` enforces access control but does not produce an immutable audit log of who read or wrote what memory. |
| **No retention / erasure policies** | OGX has no TTL, retention, or erasure primitives. Records exist until explicitly deleted. |
| **Compaction is not inspectable** | Compaction summaries are LLM-generated plaintext marked `encrypted_content` in the schema (the field name is an OpenAI spec artifact; the content is actually plaintext in OGX). They are not structured or human-readable in any governed sense — the content depends entirely on the `summarization_prompt` config. |
| **No FIPS / compliance certification** | No evidence of FIPS validation, HIPAA controls, or EU AI Act compliance tooling in the repo. |

### 5.3 Strategic Position: OGX as the Foundation Layer

**EXPLORATORY** — There are three postures Red Hat could take toward OGX's memory primitives:

**Option A: Extend OGX as the memory platform.** Use OGX's Conversations, Vector Stores, Compaction, and Prompts APIs as the RHOAI memory foundation. Build governance, multi-scope isolation, and knowledge graph as additional microservices or OGX plugins on top. Benefit: OGX is already the RHOAI 3.5 bridge — this is a natural extension. Risk: OGX's memory model is OpenAI-API-centric; deviating may break conformance.

**Option B: Use OGX as transport, build RHOAI memory as a separate service.** The Responses API agentic loop delegates to external tools (file_search, MCP). A RHOAI-native memory service could be an MCP server (or vector store endpoint) that OGX calls. This decouples RHOAI memory governance from the OGX API surface. MemoryHub is architecturally closer to this model.

**Option C: Contribute governance primitives to OGX upstream.** Francisco Arceo's multi-tenancy work shows Red Hat is already contributing foundational governance to OGX. Red Hat could continue this pattern — contributing multi-scope isolation, audit logging, and retention APIs to OGX upstream rather than building them separately. Benefit: these features land in the community project and Red Hat sets the standard. Risk: upstream community consensus is slower than internal delivery.

The three options are not mutually exclusive. A likely path is: short-term bridge via OGX primitives as-is (3.5), medium-term contribution of governance primitives upstream (3.6), long-term gateway-native implementation that abstracts OGX vs. native behind a platform API.

### 5.4 Alignment Signal: Francisco Arceo as Bridge Between OGX and RHOAI Strategy

Francisco Arceo is a Red Hat engineer contributing to both the RHOAI strategy (RHAISTRAT-1345 stakeholder) and the OGX upstream. This creates a natural alignment channel: decisions made in RHAISTRAT-1345 research can directly inform what features get prioritized and contributed in OGX, and vice versa. His comment on RHAISTRAT-1345 (2026-03-23) flagging client-side vs. server-side memory as the key architectural choice is directly addressed by OGX's current design — OGX is explicitly server-side memory, and Arceo's compaction work makes that concrete.

---

## 6. Contrast with MemoryHub

Both OGX and MemoryHub address agent memory for RHOAI, but from different angles. See [doc 03](03-memoryhub-deep-dive.md) for MemoryHub's full technical analysis.

| Dimension | OGX | MemoryHub |
|---|---|---|
| **Origin** | Meta Llama Stack, now Open GenAI Stack | Red Hat AI Americas prototype (Wes Jackson) |
| **Primary interface** | OpenAI-compatible REST APIs (Responses, Conversations, Vector Stores) | MCP server (FastMCP 3, streamable HTTP) |
| **Memory model** | Per-principal, per-API-surface (no cross-agent sharing out of box) | Project/campaign/org-scoped sharing; "swarm coherence" |
| **Governance model** | ABAC row-level isolation (AuthorizedSqlStore) | 5-tier scope hierarchy + RBAC + OAuth 2.1 |
| **Storage substrate** | Pluggable: 9 vector backends + SQL (SQLite or Postgres) | PostgreSQL + pgvector (fixed) |
| **Compaction** | LLM-based summarization via Responses API; configurable prompt templates | LLM-based summarization; "human-readable for compliance inspection" |
| **Contradiction detection** | None | Implemented (Phase 2a) |
| **Knowledge graph** | None | Partial — PostgreSQL graph queries (not a native graph DB) |
| **Audit trail** | None (access control without audit log) | Stub interface (wired but not production-grade) |
| **Self-improving agents** | First-class via Prompts API + Responses loop (blog post demo) | Not a stated pattern |
| **Kubernetes operator** | Not present | Skeleton (CRDs defined, not feature-complete) |
| **Community** | 8,377 stars, 1,309 forks; Meta + Red Hat + community contributors | 6 forks; 0 stars; Red Hat AI Americas only |
| **SDK** | `ogx-client` on PyPI (wraps `LlamaStackClient`) | `memoryhub` on PyPI (v0.7.0); external SDK consumer: `kagenti/adk` PR #231 |
| **RHOAI integration path** | Direct — already the RHOAI 3.5 Responses API bridge | Requires explicit integration work; Kubernetes operator needed |
| **Maturity for production RHOAI** | Higher — in the production path | Lower — prototype; audit log stub, operator skeleton |

**Key synthesis:** OGX and MemoryHub are complementary, not competing. OGX is the agentic API server with integrated memory primitives (storage, retrieval, compaction) that RHOAI is already shipping. MemoryHub is a governed organizational memory layer that addresses the governance, cross-agent sharing, and curation concerns that OGX does not (and may not want to, given its OpenAI-API-conformance charter). A full RHOAI memory platform likely needs both: OGX as the session-level working/episodic memory layer, and a governance service (whether MemoryHub-inspired or purpose-built) as the organizational/long-term memory layer.

---

## 7. Open Questions and Review Gate Items

The following questions must be answered before RHOAI memory features can be scoped. They are flagged as **REVIEW GATE** items — the research team and Peter Double should address them before design work begins.

### High Priority (Block Design)

**Q1 (REVIEW GATE).** What is the exact scope of the RHOAI 3.5 OGX bridge deployment? Specifically: which OGX APIs are exposed in 3.5 — only the Responses API, or also Conversations, Vector Stores, Prompts, and Files? The memory primitive analysis changes significantly depending on the answer.

**Q2 (REVIEW GATE).** Does the RHOAI 3.5 deployment of OGX include Arceo's multi-tenancy work (PRs #5756, #5782) or a pre-multi-tenancy version? If the bridge is pinned to a version before May 2026, the tenant isolation model described in this document is not in the production deployment.

**Q3 (REVIEW GATE).** The AI Gateway F2F decision says "GA current Llama Stack as bridge in 3.5; architecture allows replacement within ~6 months." What is the concrete replacement plan — is it a full reimplementation of the Responses API or a delegation to OGX via MCP/vector stores? The memory primitive strategy differs for each.

**Q4 (REVIEW GATE).** Is Red Hat's intended posture toward OGX to (a) consume upstream, (b) extend upstream with contributions, or (c) fork/embed as a private component? Francisco Arceo's contributions suggest (b), but there is no documented decision.

### Medium Priority (Shape Architecture)

**Q5.** The Conversations API provides per-principal session memory. The gateway-native Responses implementation (planned post-3.5) is described as having "conversation state, files, vector stores, and tool catalogs become independent microservices for horizontal scaling." How does this relate to OGX's Conversations API — is RHOAI replacing it with a custom implementation?

**Q6.** OGX's `compaction_config.summarization_model` allows a separate model for compaction summarization. In a RHOAI deployment, should this be a dedicated small model (e.g., Llama-3.2-3B) to avoid consuming expensive GPU capacity, or should it use the conversation model? This is a cost and performance architecture question.

**Q7.** MemoryHub's "cache-optimized assembly" (deterministic, epoch-locked memory ordering for KV-cache prefix hits) provides ~2× vLLM throughput gains. OGX has no equivalent optimization. If RHOAI adopts OGX as the memory substrate, this optimization opportunity is foregone. Is there a path to contributing cache-optimized retrieval ordering to OGX?

**Q8.** OGX's Vector Stores API supports query rewriting (`rewrite_query_params`) and contextual retrieval at ingestion time. Are these features exposed/configurable in the RHOAI OGX bridge, or are they available only in OGX standalone deployments?

**Q9.** Francisco Arceo flagged in RHAISTRAT-1345 (2026-03-23) that "frameworks (e.g., OpenClaw) have client-side memory, where client-side behavior ends up using a flavor of hybrid search." OGX is server-side memory. How should RHOAI handle frameworks that implement their own client-side memory — bypass OGX, delegate to OGX, or provide a hybrid path?

### Lower Priority (Inform Product Decisions)

**Q10.** The OGX rename from Llama Stack to "Open GenAI Stack" reflects a mission expansion to multi-SDK support (OpenAI, Anthropic, Google). Is Red Hat's Responses API bridge expected to expose only the OpenAI protocol, or also Anthropic and Google surfaces via OGX's multi-SDK layer?

**Q11.** OGX's Prompts API provides versioned procedural memory. The current RHOAI platform already has a prompt registry concept via the AI Asset Registry. How should these two prompt management surfaces be reconciled — are they complementary, overlapping, or the same thing at different layers?

**Q12.** OGX has no native long-term knowledge graph (no entity resolution, no contradiction detection, no relationship modeling). If Peter's area-1 framing ("org-wide knowledge graph") is in scope for RHOAI, OGX alone is insufficient. What is the right boundary between OGX's vector-search-based semantic memory and a hypothetical RHOAI knowledge graph service?

---

## Sources

### Internal (Red Hat / RHOAI Project)

| Source | Path | Notes |
|---|---|---|
| Agent Memory & Knowledge seed doc | `docs/knowledge-review/assets/agent-memory-knowledge.md` | Contains RHAISTRAT-1345 details, Francisco Arceo's comment, MemoryHub overview |
| AI Gateway F2F decisions | `docs/knowledge-review/components/ai-gateway.md` | Llama Stack bridge decision; gateway-native replacement plan; conversation state management status |
| Knowledge registry | `docs/knowledge-registry.md` | Llama Stack as Responses API bridge; Open Responses Specification; stakeholder list |
| MemoryHub deep-dive | `agent-memory/research/03-memoryhub-deep-dive.md` | MemoryHub comparison basis |
| Technical patterns | `agent-memory/research/04-technical-patterns.md` | Pattern taxonomy used in Sections 3 and 6 |
| Landscape and definitions | `agent-memory/research/01-landscape-and-definitions.md` | Oracle four-type taxonomy applied in Section 3.5 |

### External (OGX Repository, Verified 2026-05-17)

| Source | URL / Reference | Notes |
|---|---|---|
| OGX repo root | `https://github.com/ogx-ai/ogx` | Confirms Llama Stack rename; repo metadata |
| OGX README | `ogx-ai/ogx` README (via `gh repo view`) | "Llama Stack is now OGX" statement |
| AGENTS.md | `ogx-ai/ogx` / `AGENTS.md` | Project overview; repo layout; Python tooling |
| Responses API config | `src/ogx/providers/inline/responses/builtin/config.py` | `CompactionConfig` schema |
| Responses API impl | `src/ogx/providers/inline/responses/builtin/responses/openai_responses.py` | Agentic loop; background tasks; compaction integration |
| Conversations impl | `src/ogx/core/conversations/conversations.py` | `ConversationServiceImpl`; `AuthorizedSqlStore` usage; schema |
| Conversations models | `src/ogx_api/conversations/models.py` | `Conversation`, `ConversationItem` types |
| AuthorizedSqlStore | `src/ogx/core/storage/sqlstore/authorized_sqlstore.py` | ABAC governance primitive |
| Prompts impl | `src/ogx/core/prompts/prompts.py` | `PromptServiceImpl`; `AuthorizedSqlStore` usage |
| Vector store mixin | `src/ogx/providers/utils/memory/openai_vector_store_mixin.py` | Vector Stores API provider implementation |
| Vector store util | `src/ogx/providers/utils/memory/vector_store.py` | Chunking; tiktoken; reranking utils |
| inline_builtin docs | `docs/docs/providers/responses/inline_builtin.mdx` | Full config reference for Responses provider |
| Memory101 notebook | `docs/zero_to_hero_guide/05_Memory101.ipynb` | Vector I/O tutorial |
| Agentic flows blog | `docs/blog/2026-03-01-building-agentic-flows.md` | Self-improving agent pattern via Prompts API |
| Multi-SDK blog | `docs/blog/2026-05-11-consistent-agentic-api-layer.md` | OGX multi-protocol posture |
| PR #5756 (Arceo) | `gh api repos/ogx-ai/ogx/pulls/5756` | Multi-tenancy core; ABAC; `AuthorizedSqlStore` |
| PR #5782 (Arceo) | `gh api repos/ogx-ai/ogx/pulls/5782` | Vector I/O tenant isolation; all 9 providers |
| PR #5327 (Arceo) | `gh api repos/ogx-ai/ogx/pulls/5327` | Conversation compaction; `POST /v1/responses/compact` |
| PR #5804 (Sébastien Han / leseb) | SHA `cdb4f29a`, merged 2026-05-15 | O(n) multi-turn storage optimization |
| PR #5791 (Arceo) | SHA `bcc25660` | 5-step tokenizer resolution chain |
| PR #5757 (Arceo) | SHA `d30a6030` | Connectors/batches KVStore → AuthorizedSqlStore |
| PR #5850 (Higgins) | SHA `791a0484`, merged 2026-05-15 | sort_order column for deterministic conversation ordering |
| Commit history (Arceo) | `gh api repos/ogx-ai/ogx/commits?author=franciscojavierarceo` | Full contribution record verified 2026-05-17 |
| Vector I/O provider docs | `docs/docs/providers/vector_io/` directory | 9 vector backends documented |
