---
title: AI Gateway Responses API as Memory Substrate
description: Whether the AI Gateway's Responses API can replace OGX as the memory substrate foundation, mapping 7 OGX primitives to gateway equivalents.
source: ai-asset-registry/agent-memory/research/16-ai-gateway-memory-substrate.md (as of 2026-07-05)
timestamp: 2026-07-06
review_after: 2026-08-05
---

# AI Gateway Responses API as Memory Substrate

> Superseded 2026-07-10 by [19-market-direction-refresh-2026-07](19-market-direction-refresh-2026-07.md) — the architecture direction moved to a standalone memory service decoupled from the gateway (2026-06-30/07-07 syncs); this doc stands as the record of the gateway-absorption option and its parity analysis.

**Purpose:** Analyze whether the AI Gateway's Responses API implementation can replace OGX as the memory substrate foundation for the RHOAI agent memory strategy, map the 7 OGX primitives the strategy depends on to their gateway equivalents, and identify parity gaps.

**Date:** 2026-06-10

**Author:** Peter Double (Principal PM — MCP & AI Asset Registries)

**Status:** PROPOSED — an analysis responding to the directional OGX deprecation signal. See [REVIEW-NOTES — OGX Deprecation Context](REVIEW-NOTES.md#ogx-deprecation-context-2026-06-10).

**Research series — Agent Memory:**
- Document 16 of 17
- **Phase 1 (landscape):** [00](00-executive-summary.md) · [01](01-landscape-and-definitions.md) · [02](02-solution-survey.md) · [03](03-memoryhub-deep-dive.md) · [04](04-technical-patterns.md) · [05](05-standards-and-protocols.md) · [06](06-ogx-memory-primitives.md) · [07](07-taxonomy-and-decomposition.md) · [08](08-rhoai-ocp-alignment.md)
- **Phase 2 (deep dives):** [09](09-agent-harness-memory.md) · [10](10-claude-memory-dreaming.md) · [11](11-adversarial-memory.md) · [12](12-benchmarking-evaluation.md) · [13](13-kv-cache-optimization.md) · [14](14-enterprise-use-cases.md) · [15](15-multi-modal-memory.md) · 16 (this doc)
- **Strategy:** [README](/features/agent-memory/strategy/strategy-overview.md) · [Strategy](/features/agent-memory/strategy/agent-memory-strategy.md) · [Use Cases](/features/agent-memory/strategy/use-cases-and-personas.md) · [Architecture](/features/agent-memory/strategy/recommended-architecture.md) · [Outcome](/features/agent-memory/strategy/rhaistrat-1345-outcome-update.md) · [RFE Roadmap](/features/agent-memory/strategy/rfe-roadmap.md)

---

## 1. Context and Trigger

OGX (the renamed Llama Stack) is likely being deprecated over time, replaced by AI Gateway components. The AI Gateway F2F (April 2026) decided to re-architect the Responses API from single-tenant Llama Stack to a gateway-native multi-tenant implementation. Playground OGX decoupling targets RHOAI 3.7 as the earliest milestone.

The agent memory strategy ([agent-memory-strategy.md](/features/agent-memory/strategy/agent-memory-strategy.md)) was built on OGX as the substrate foundation (REVIEW-NOTES D3/D5). This document assesses whether the AI Gateway's Responses API architecture can serve as the replacement substrate, maps the 7 primitives the strategy depends on, and identifies parity gaps.

**Key architectural finding:** "AI Gateway Responses API" does not mean the gateway *reimplements* the memory primitives — the [Llama Stack RFC](https://docs.google.com/document/d/1uiVoYqh8FftqcHyzQmuedFfAoXur_lT52HHuwNFMfqU) shows that Llama Stack continues as the stateful orchestration layer *behind* the gateway. The gateway (Envoy + IPP framework) handles routing, auth, rate limiting, and policy; Llama Stack (on CPU pods) handles stateful APIs: Responses, Files, Vector Stores, Conversations, Compaction. OGX deprecation means the *deployment model* changes (standalone bridge → microservice behind gateway), not necessarily a reimplementation of the primitives themselves.

---

## 2. The 7 Primitives Mapping

The agent memory strategy depends on 7 OGX primitives ([research 06](06-ogx-memory-primitives.md); [research 08](08-rhoai-ocp-alignment.md) §2.3). This table maps each to the AI Gateway architecture:

| # | OGX Primitive | Memory Role | AI Gateway Equivalent | Parity Status |
|---|---|---|---|---|
| 1 | **Conversations API** | Episodic/working memory | Gateway routes `/v1/conversations` to stateful layer (RFC §4.1 HTTPRoute definition). Conversation state becomes an independent microservice for horizontal scaling. | **DESIGNED** — architecture decided, route defined |
| 2 | **Vector Stores** | Semantic memory | Gateway routes `/v1/vector_stores` to stateful layer. Vector store becomes an independent microservice (RFC §4.1). Milvus/pgvector backend preserved. | **DESIGNED** — architecture decided, route defined |
| 3 | **Files API** | Semantic memory (document storage) | Gateway routes `/v1/files` to stateful layer (RFC §4.1). | **OPEN** — gateway frontend requirements not substantively addressed at F2F. Request body size (100MB+) and streaming constraints identified but not resolved. |
| 4 | **Prompts API** | Procedural memory | Gateway routes `/v1/prompts` to stateful layer (RFC §4.1 HTTPRoute definition). | **DESIGNED** — route defined, implementation TBD |
| 5 | **`/responses/compact` + `context_management`** | Inspectable compaction | Gateway routes `/v1/compaction` to stateful layer. The Open Responses Spec defines `/responses/compact` minimally ("returns a compacted input window, not a response ID"). OpenAI auto-compaction approximation approach agreed at F2F (detect via response.compaction flag, use summarization). | **DISCUSSED** — approach agreed, detailed design needed. The Open Responses Spec deliberately underspecifies compaction. |
| 6 | **`previous_response_id` chaining** | Conversation state continuity | Preserved in the RFC architecture (§4.2 step 3a): stateful layer resolves `previous_response_id` chain from PostgreSQL, reconstructs full input array. The Open Responses Spec defines this as the sole stateful mechanism — servers "MUST load both the input and output associated with that prior response." | **DESIGNED** — core to the Responses API flow, well-specified in both Open Responses Spec and the RFC |
| 7 | **`AuthorizedSqlStore` ABAC** | Row-level scope isolation (RBAC foundation) | Replaced by the gateway identity model: Authorino validates API key → resolves user identity → injects `x-llama-user-id` header → stateful layer scopes all data access by header value. Existing `AccessRule` / `AuthorizedSqlStore` plumbing in Llama Stack is reused — middleware reads the header and creates the `AccessRule` (RFC §6.4). | **DESIGNED** — middleware needed (header → AccessRule). Simpler than standalone ABAC. RFC notes this is "only safe when [the stateful layer] is unreachable except through the gateway." |

**Summary:** 5 of 7 primitives are DESIGNED (architecture decided, implementation planned), 1 is DISCUSSED (compaction — approach agreed, needs design), and 1 is OPEN (Files API frontend requirements). No primitives are architecturally missing — all 7 have a defined path in the gateway model.

---

## 3. Gap Analysis

### 3.1 Files API (OPEN)

The Files API gateway frontend requirements were not substantively addressed at the F2F (listed as an open item). The memory substrate's semantic memory depends on Vector Stores + Files; Files is the less mature of the two. Specific concerns:

- Envoy's default `max_request_bytes` (1MB) is too small for document uploads; the RFC recommends 100MB+ for stateful routes
- File upload is a gateway-routed operation, not a direct Llama Stack call — gateway buffering and timeout behavior must be configured
- **Risk level for memory strategy:** MEDIUM. Vector Stores (the primary semantic memory interface) are DESIGNED; Files is the secondary interface used for document ingestion. The memory substrate can function without Files in Phase 1 if needed.

### 3.2 Compaction (DISCUSSED)

The compaction strategy (automatic vs. user-controlled, same model vs. cheaper model) is discussed but not decided. The memory strategy's context engineering layer depends on *inspectable* compaction — human-readable summaries, not opaque tokens ([research 00](00-executive-summary.md) §3 finding 10). Specific concerns:

- The Open Responses Spec defines `/responses/compact` minimally — it "returns a compacted input window, not a response ID" with no schema detail. This is deliberately underspecified.
- The F2F agreed to approximate OpenAI's auto-compaction (detect via `response.compaction` flag, use summarization) but this is a *detection* mechanism, not an *inspectable compaction* implementation.
- **Risk level for memory strategy:** MEDIUM. The context engineering capability (RFE-M4) can build inspectable compaction as a layer *on top of* the basic `/responses/compact` primitive, regardless of how the gateway implements it. The primitive existing is sufficient; the inspectability is added by the memory substrate, not expected from the gateway.

### 3.3 Multi-Tenancy

Llama Stack does not have built-in multi-tenancy today (RFC §6.3, Appendix B). The RFC's Phase 1 mitigation is per-namespace deployment (one Llama Stack instance per tenant — strong isolation, no code changes, higher operational overhead). Full multi-tenancy requires adding `tenant_id` scoping to all storage operations (ResponsesStore, Files, VectorIO, Conversations, KV Store).

- The AI Gateway's group-based tenancy model is designed to extend across vector stores, file storage, MCP tool catalogs, and guardrails — this is the eventual platform-provided solution.
- **Risk level for memory strategy:** LOW for Phase 1 (3.7 Dev Preview). Per-namespace deployment provides strong isolation. The four-tier scope model (`user`/`project`/`role`/`org`) maps onto the gateway's group-based tenancy as it matures. The MemoryHub-derived governance layer (RFE-M3) adds the memory-specific scope enforcement on top.

### 3.4 `/v1/memories` Route

The `/v1/memories` route appears in the RFC's HTTPRoute definition (§4.1) but with no implementation detail — it is listed alongside other routes but not discussed in the architecture or phasing sections. This is the most directly relevant route for the memory substrate's API surface.

- **Risk level for memory strategy:** LOW. The memory substrate will define its own API surface (RFE-M2) — the `/v1/memories` route being present in the RFC's route definition is a positive signal that the gateway architecture anticipates memory as a routed service. The memory API design is driven by the strategy, not by the gateway's route definition.

### 3.5 Identity Model Delta

The gateway's Authorino-based identity model (header injection) is architecturally simpler than `AuthorizedSqlStore`'s standalone ABAC, but may need extension:

- The four-tier scope model (`user`/`project`/`role`/`org`) requires scope attributes beyond a single `x-llama-user-id` header. The gateway may need to inject additional scope headers (project, role, org).
- Actor-chain RBAC (Q-G5) — when agent A calls agent B, the gateway tracks all actors' SPIFFE IDs in the token's claims and enforces lowest-permission. This is the AI Gateway's Tier 2 identity model (Spire/Authbridge integration, decided at F2F). It aligns with the memory strategy's actor-chain requirement.
- **Risk level for memory strategy:** LOW. The gateway's identity model is more capable than OGX's standalone ABAC for the memory strategy's needs — it provides actor-chain tracking that OGX lacks. The extension needed (scope headers) is a configuration concern, not an architectural gap.

---

## 4. What Changes for the Memory Strategy

### 4.1 Responses API Primitives Are Architecturally Preserved

All 7 primitives the memory strategy depends on have a defined path in the AI Gateway architecture. The delivery vehicle changes (standalone OGX bridge → Llama Stack microservice behind gateway), but the capabilities themselves are preserved. The Llama Stack codebase — where these primitives are implemented — continues to exist as the stateful layer behind the gateway.

### 4.2 Identity/RBAC Is Simplified

The gateway establishes identity (Authorino validates, injects headers); the memory substrate consumes identity headers. This is simpler than OGX's standalone `AuthorizedSqlStore` ABAC and more capable — the gateway's Tier 2 identity model provides actor-chain SPIFFE tracking that the memory strategy's Q-G5 requires. The recommendation to drop MemoryHub's standalone OAuth (Q-G6) is reinforced.

### 4.3 Multi-Tenancy Improves Over Time

OGX is single-tenant-per-namespace. The AI Gateway's group-based tenancy model is designed to be multi-tenant. For Phase 1 (3.7 Dev Preview), per-namespace deployment provides strong isolation. As the gateway's multi-tenancy matures, the memory substrate benefits without additional work.

### 4.4 RFE-M8 Shifts From "Re-Home" to "Design-For"

The current strategy positions RFE-M8 as a Phase 2 (3.8+) "re-home" — migrate the substrate from OGX onto the gateway-native replacement. With OGX likely deprecated, the memory substrate should design for the gateway architecture from day one (Phase 1 / 3.7). RFE-M8 shifts from "re-home onto gateway" to "complete gateway-native transition" — closing any remaining parity gaps and hardening the deployment model.

### 4.5 The Substrate-Agnostic API Surface Protects the Strategy

The hybrid posture — substrate-agnostic API surface, architecturally gateway-bound — means the memory strategy works regardless of the OGX/gateway parity timeline. The memory API is designed against "Responses API primitives" (Conversations, Vector Stores, Files, Prompts, Compaction), not a specific delivery vehicle. If the gateway isn't at full parity at 3.7, the same primitives can be consumed from OGX as a transitional fallback.

---

## 5. Source Research Findings

### 5.1 Open Responses Specification (openresponses.org/specification)

The Open Responses Spec is deliberately a **stateless-first protocol**. It defines:
- **`previous_response_id` chaining** — the sole stateful mechanism. Servers MUST load prior response input/output and treat them as context.
- **`store` flag** — controls whether response state is persisted. `store=false` means state exists only in connection-local memory (WebSocket).
- **`/responses/compact`** — returns a compacted input window, not a response ID. Minimally specified.
- **Truncation** — `auto` or `disabled`, governing whether servers may shorten context exceeding the model window.

The spec does NOT define: Conversations API, Vector Stores, Files API, Prompts API, memory endpoints, embeddings, identity/tenancy, or any multi-turn container abstraction. These are all provider extensions.

**Implication for memory strategy:** The Open Responses Spec provides the foundational chaining mechanism (`previous_response_id`) that the memory substrate builds on, but the memory-specific primitives (conversations, vector stores, files, prompts, compaction, scope-isolated RBAC) are — and will remain — extensions above the spec. The Phase 0 (3.6) MCP Memory Convention SEP work is the right venue for standardizing these extensions, not the Open Responses Spec itself.

### 5.2 AI Gateway Payload Processing Repo (opendatahub-io/ai-gateway-payload-processing)

The repo implements the IPP (Inference Payload Processor) plugin framework — the gateway's processing layer. Current plugins:
- `api-translation` — translates between OpenAI, Anthropic, Azure, Bedrock, Vertex API formats
- `apikey-injection` — injects API keys for external provider calls
- `model-provider-resolver` — resolves model references to backend providers
- `nemo` — NeMo guardrails integration (request/response guards)

The repo contains **zero stateful API code** — no Responses API implementation, no conversation state, no vector stores, no files, no memory primitives. This confirms the RFC's architecture: the IPP framework handles the inference/routing layer; stateful APIs live in Llama Stack behind the gateway.

**Implication for memory strategy:** The gateway repo is not where the memory primitives will live. The memory substrate's code will either (a) extend Llama Stack's existing primitives behind the gateway, or (b) be implemented as independent microservices routed through the gateway — both paths are consistent with the RFC architecture and the strategy's substrate-agnostic posture.

---

## 6. Recommendation

1. **Design the memory substrate API against "Responses API primitives"** — substrate-agnostic terminology that decouples from the OGX/gateway delivery vehicle transition.
2. **Architecturally orient toward the AI Gateway** — Phase 1 (3.7) designs for the gateway-routed model from day one, not as a retrofit.
3. **Track parity gaps as design-time validation items**, not blockers:
   - Files API gateway frontend (OPEN) — validate before Phase 1 design lock
   - Compaction detailed design (DISCUSSED) — inform RFE-M4 context engineering design
   - `/v1/memories` route implementation — coordinate with gateway team
   - Multi-tenancy maturity — per-namespace in Phase 1, platform-provided over time
4. **Preserve the research historical record** — docs 00–15 stay as-is with OGX terminology. Doc 16 and the REVIEW-NOTES deprecation note provide the forward-looking context.
5. **Update strategy docs** with substrate-agnostic terminology and hybrid posture framing.

---

## 7. Sources

| Source | Used for |
|---|---|
| [REVIEW-NOTES — OGX Deprecation Context](REVIEW-NOTES.md#ogx-deprecation-context-2026-06-10) | The deprecation signal and its implications for D3/D5 |
| [Llama Stack RFC](https://docs.google.com/document/d/1uiVoYqh8FftqcHyzQmuedFfAoXur_lT52HHuwNFMfqU) | Architecture for Llama Stack behind the AI Gateway; HTTPRoute definitions; identity model; multi-tenancy |
| [AI Gateway F2F — Agenda & Outcomes](https://docs.google.com/document/d/1-WGqvk5Ehn5ocyMON0QNkMDeQyiFzbsAMmIXuyzqrBU) | F2F decisions: unified IPP, Responses re-architecture, group-based tenancy, agent identity tiers |
| [Open Responses Specification](https://www.openresponses.org/specification) | Stateless-first protocol; `previous_response_id`, `store`, `/responses/compact`, truncation |
| [AI Gateway Payload Processing repo](https://github.com/opendatahub-io/ai-gateway-payload-processing) | IPP plugin framework — confirms no stateful API code in gateway layer |
| [research 06 — OGX Memory Primitives](06-ogx-memory-primitives.md) | The 7 primitives the memory strategy depends on |
| [research 08 — RHOAI & OCP Alignment](08-rhoai-ocp-alignment.md) | OGX as substrate (D3/D5), RHOAI integration points |
| [AI Gateway component doc](https://github.com/solaius/ai-asset-registry/blob/main/docs/knowledge-review/components/ai-gateway.md) | F2F decisions summary, traffic types, roadmap alignment |
