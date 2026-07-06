---
title: Gen AI Studio — architecture & feature inventory
description: System architecture, tech stack, deployment topology, and feature roadmap for Gen AI Studio (prompt engineering, playground, AI Assets, observability) as of 2026-06-23 — Tech Preview in RHOAI 3.5 EA, targeting GA in 3.6.
source: ai-asset-registry/docs/knowledge-review/components/gen-ai-studio-architecture.md (as of 2026-07-05), itself last updated 2026-06-23
timestamp: 2026-07-06
review_after: 2026-08-05
---

> Owner: Peter Double (Principal PM — MCP & Gen AI Studio). Engineering: Team Crimson (BFF & Frontend). Repo: [opendatahub-io/odh-dashboard](https://github.com/opendatahub-io/odh-dashboard) (`packages/gen-ai/`). Slack: `#team-dashboard-crimson`, `#wg-dashboard-crimson`.
>
> This is the first substantive knowledge-hub content for the `gen-ai-studio` partition — the monolith (`docs/knowledge-registry.md`) that fed R2 batches 1-4 had almost nothing on Gen AI Studio specifically. See [fact-gen-ai-studio-overview.md](/features/gen-ai-studio/knowledge/fact-gen-ai-studio-overview.md) for the short version of this document, and the partition's other new entries for extracted facts/questions/decisions.

## What is Gen AI Studio?

The prompt engineering, model interaction, and AI asset management surface within RHOAI. Evolved from the original "Prompt Lab" concept (watsonx.ai parity target) into four capability areas:

- **Playground** — interactive chat-based model interaction with multi-model comparison
- **AI Available Assets (AAE)** — unified view of models, prompts, MCP endpoints, guardrails, and vector stores
- **Observability** — chat metrics and distributed tracing for debugging/optimization
- **Configuration Persistence** — save, load, and share complete AI agent configurations

Current maturity: Tech Preview in RHOAI 3.5 EA, targeting GA in RHOAI 3.6.

## System architecture

Gen AI Studio is **not a standalone component** — it's a federated module (micro-frontend + Go BFF sidecar) within the ODH Dashboard pod, which runs 9+ containers total: the main dashboard (Node.js/Fastify + React/PatternFly 6), a kube-rbac-proxy authn/authz sidecar, and one BFF per module (gen-ai-ui at port 8143, plus model-registry, maas-ui, mlflow, eval-hub, automl, autorag, agent-ops BFFs on their own ports).

**Module Federation**: the main dashboard loads `gen-ai` as a remote entry at runtime via Webpack Module Federation (`/_mf/gen-ai/*`). Extensions register routes, nav items, and feature-area flags. Feature flag: `genAiStudio: true` on the `OdhDashboardConfig` CRD, requiring `llamastampoperator: Managed` in the DataScienceCluster (Gen AI Studio's own name for its Llama Stack Distribution dependency is "OGX" throughout this doc).

**Technology stack**: React 18 + TypeScript + PatternFly (frontend); Go/Fastify-reverse-proxy (BFF, `packages/gen-ai/bff/`); OGX — Red Hat's Llama Stack Distribution — as the AI runtime (OpenAI-compatible API managing models, RAG, shields, agents); vLLM/llm-d/MaaS for inference backends; MLflow Prompt Registry for prompts; NeMo Guardrails via the TrustyAI Operator (migrating off Llama-Stack-mediated guardrails); pgvector as the default vector store (moving off inline Milvus); MCP Gateway (Envoy-based) for tools, ConfigMap-based today with registry discovery planned; OpenTelemetry + MLflow Traces for observability; Kubernetes ConfigMaps for config storage (AgentProfile CRs planned).

**Request flow (inference)**: Browser → HAProxy (OpenShift Router) → Envoy Gateway (HTTPRoute) → kube-rbac-proxy (authn/authz) → Gen AI BFF (Go, SSE streaming) → OGX Server (Llama Stack) → model serving runtime (vLLM/llm-d/MaaS). Non-streamed requests (CPU models, guardrails, tool calls) can exceed 30s; timeouts are extended to 5 minutes across the proxy chain ([RHOAIENG-63831](https://redhat.atlassian.net/browse/RHOAIENG-63831)). ASR (audio transcription) bypasses OGX entirely — the BFF calls the user's ASR model directly. Guardrails calls also bypass OGX — the BFF calls NeMo Guardrails' `/v1/guardrail/checks` directly.

**OGX auto-setup flow**: the BFF manages the OGX server lifecycle — user selects models/vector stores in the UI, the BFF's `lsd_install_handler.go` creates/updates the OGX CR + `config.yaml`, the OGX Operator reconciles and deploys the Llama Stack server, and user changes trigger reconfiguration. Known limitation (targeting 3.6): config changes currently require an OGX restart ([RHAISTRAT-1921](https://redhat.atlassian.net/browse/RHAISTRAT-1921)).

**Nav visibility logic**: Gen AI Studio, AAE, and Playground visibility are decoupled by feature flag × OGX state ([RHOAIENG-64596](https://redhat.atlassian.net/browse/RHOAIENG-64596)) — when OGX is removed but the studio flag is on, AAE and prompts still work (no playground actions); this lets AAE/prompts/AutoRAG function independently of OGX.

## Repository structure (odh-dashboard monorepo)

`packages/gen-ai/` holds the federated module: `bff/` (Go 1.26 — handlers per domain: `lsd_install_handler.go`, `lsd_responses_handler.go`, `mcp_handler.go`, `mlflow_handler.go`, `guardrails_handler.go`, `agent_profile_handler.go`, `maas_handler.go`, plus client factories, repositories, config, middleware, k8s ops, and 14 internal ADRs under `docs/adr/`) and `frontend/src/app/` (React — `Chatbot/` is the main playground with sub-components for configuration, guardrails UI, prompt management, MCP tools panel, RAG file upload, and chat state; `AIAssets/`, `agentProfile/`, shared `context/` and `hooks/`).

Sibling packages in the same monorepo: `maas/`, `autorag/` (consumes an `EmbeddableChatbotPlayground` exported by gen-ai), `eval-hub/`, `mlflow/`, `agent-ops/`, `plugin-core/`, `ui-core/`, `distributions/core-bff/`.

**BFF design patterns** (from the 14 internal ADRs): Factory pattern for all external clients (LlamaStack, MaaS, MCP, Kubernetes, MLflow, NeMo — Real/Mock implementations); Repository pattern for business logic between handlers and clients; a CORS → Auth (OAuth/OIDC) → Logging → Panic-Recovery → Telemetry → Namespace-Injection → Client-Attachment middleware chain; a consistent `{data, metadata}` envelope response shape; an in-memory `MemoryStore` for MaaS tokens (15-minute TTL).

**Deployment modes**: federated (production — Module Federation sidecar sharing TLS certs/ConfigMaps with the dashboard pod), standalone (development — `make dev-start` / `make dev-start-mock`), OpenShift Build (`build.openshift.sh` for `oc new-app`).

## Feature roadmap (by theme, condensed)

The full per-ticket status/target breakdown lives in Jira and will drift fast — this is the shape as of 2026-06-23, not a live status board. Two Outcomes anchor almost all of it: [RHAISTRAT-1312](https://redhat.atlassian.net/browse/RHAISTRAT-1312) (Playground, Observability, AI Assets, Model Specialization — 42 child features across 3.5/3.6/future) and [RHAISTRAT-1743](https://redhat.atlassian.net/browse/RHAISTRAT-1743) (Future Enhancements, 3.Next — 8 child features); [RHAISTRAT-1067](https://redhat.atlassian.net/browse/RHAISTRAT-1067) tracks watsonx.ai Prompt Lab feature parity specifically.

- **Prompt engineering & model specialization**: MLflow prompt template integration (text + chat, `{{variable}}` substitution), model-prompt pairing in Playground, loading starter prompts from a global registry namespace, eventual consolidation of prompts into AI Assets (3.6).
- **Playground experience**: multimodal support (image vision + audio/ASR), configuration persistence (save/load/compare agent configs), chat persistence, multi-language "View Code," a context-aware model selector with capability filtering, and — further out — ExternalModel CR support and deployment of playground configs as callable API services.
- **Observability & tracing**: chat metrics and tracing in Playground, backed by engineering epics for an OTel instrumentation toggle, embedded MLflow trace/call-tree view, multi-tenant trace routing, inline per-chat metrics, and trace export/persistence.
- **AI asset management**: surfacing MCP endpoints, guardrails, and guardrail templates in the unified AI Assets view; consolidating prompts into AI Assets; a still-unfiled RFE for knowledge-source listing/selection.
- **Vector store & RAG**: a default pgvector vector store for Gen AI Studio and AutoRAG (in progress), registration of existing vector stores, multi-vector-store selection, and in-line RAG source viewing (all pushed to 3.7).
- **Guardrails**: surfacing basic Llama Stack guardrails in Playground (`llm_input`/`llm_output` only for MVP — tool-level guardrails wait on LlamaFirewall or MCP Gateway ToolGuard) and migrating the integration to call NeMo Guardrails directly via the TrustyAI Operator, decoupling guardrails from the inference path.
- **MCP & agentic**: see the dedicated MCP Gateway Integration section below.
- **Model serving integration**: AI Gateway as an alternative to OGX (3.7), ExternalModel CR support and a re-evaluation of custom endpoints against it (3.6), and Gen AI Studio GA itself ([RHAISTRAT-1939](https://redhat.atlassian.net/browse/RHAISTRAT-1939) / [RHAIRFE-2375](https://redhat.atlassian.net/browse/RHAIRFE-2375)).
- **Future (3.Next)**: user-level secrets management, a pluggable agent runtime in Playground, integrating an OpenClaw installer into the dashboard, full chat transcript download.

## Configuration persistence (AgentProfile)

The foundational layer for reproducibility and future deployment ([RHAISTRAT-1534](https://redhat.atlassian.net/browse/RHAISTRAT-1534)). A saved `AgentProfile` captures: selected model + inference parameters, system prompt/template reference, RAG configuration (vector store, connections, search params), enabled MCP servers, and guardrail policies/settings. Storage today is Kubernetes ConfigMaps (namespaced), via BFF CRUD endpoints.

## Multimodal architecture

Adds image/vision and audio/ASR to the Playground ([RHAISTRAT-1527](https://redhat.atlassian.net/browse/RHAISTRAT-1527)). Image flow: user uploads JPG/PNG (≤10MB) → BFF encodes and sends to OGX → OGX forwards to a vision-capable model (e.g., Qwen3-VL-4B) → text response via the standard chat path. Audio flow bypasses OGX: user uploads WAV/MP3 (≤10MB) → BFF sends directly to the user's ASR model (e.g., Whisper) → transcribed text returns to the message input for the user to edit/send.

Design decisions: one image per conversation (simplicity + predictable inference); one audio file per message (multiple across messages allowed); no microphone capture, file upload only (security simplicity); "View Code" snippets only appear when multimodal features are actively configured; fully stateless backend, no new infrastructure.

## Guardrails architecture

Two parallel features ship in 3.5: surfacing Llama Stack guardrails as toggleable Playground options (MVP scope `llm_input`/`llm_output` only — [RHAISTRAT-313](https://redhat.atlassian.net/browse/RHAISTRAT-313)), and migrating from Llama-Stack-mediated to direct NeMo Guardrails calls at `/v1/guardrail/checks` via the TrustyAI Operator ([RHAISTRAT-1299](https://redhat.atlassian.net/browse/RHAISTRAT-1299)) — this removes Llama Stack as an intermediary for guardrail checks and simplifies token/auth handling. Future: surface guardrails and guardrail templates in the AI Assets view (3.7, [RHAISTRAT-1560](https://redhat.atlassian.net/browse/RHAISTRAT-1560)).

## MCP Gateway integration architecture

Today, MCP servers are configured via hand-authored Kubernetes ConfigMaps — no browse-and-select experience in the UI. Planned evolution in three phases:

1. **MCP Discovery from Registry** ([RHAISTRAT-1678](https://redhat.atlassian.net/browse/RHAISTRAT-1678)) — browse MCP servers from the registry directly in the Gen AI Studio UI, eliminating manual ConfigMap authoring. Enterprise-customer demand signal behind this phase is restricted — see [fact-mcp-discovery-customer-demand.md](/restricted/features/gen-ai-studio/knowledge/fact-mcp-discovery-customer-demand.md) (restricted).
2. **MCP Gateway integration** (3.6 features) — OAuth authentication for MCP Gateway endpoints, identity delegation so user identity flows through to MCP servers, multi-server tool aggregation behind a single gateway endpoint, virtual MCP server selection (curated tool collections), and token lifecycle management for gateway connections.
3. **AI Assets integration** ([RHAISTRAT-1576](https://redhat.atlassian.net/browse/RHAISTRAT-1576)) — surface MCP endpoints in the AI Asset Endpoints view alongside model-serving endpoints, for unified discovery of all AI assets.

See [fact-gen-ai-studio-mcp-integration-roadmap.md](/features/gen-ai-studio/knowledge/fact-gen-ai-studio-mcp-integration-roadmap.md) for the short version, and [question-gen-ai-studio-mcp-gateway-authn.md](/features/gen-ai-studio/knowledge/question-gen-ai-studio-mcp-gateway-authn.md) for the open identity-flow-through question this creates.

## Architecture Decision Records (ADRs)

Two approved ODH ADRs directly shape Gen AI Studio:

- **ODH-ADR-ML-0001** — "Consolidate AI Asset Registries on MLflow" (approved 2026-05-24, author Edson Tirelli): MLflow is the unified registry backend for all AI asset types (models, prompts, skills, MCP servers, agents, guardrails, knowledge sources); registry-catalog separation (MLflow = registry, AI Hub = catalog); federated plugin model per asset type; upstream-first development. This formally ratifies, via an approved architecture-decision-record process, the same registry-vs-catalog split already captured informally in [decision-registry-vs-catalog.md](/features/platform/knowledge/decision-registry-vs-catalog.md) (sourced from an April 2026 sync quote) — see [decision-odh-adr-consolidate-registries-mlflow.md](/features/platform/knowledge/decision-odh-adr-consolidate-registries-mlflow.md) for this as its own decision entry. Impact on Gen AI Studio: the AI Assets view will consolidate all asset types through MLflow APIs.
- **ODH-ADR-ML-0002** — "Shared Workspace for Cross-Namespace Resource Sharing" (approved 2026-05-24): a shared global MLflow workspace enables cross-namespace prompt sharing into Gen AI Studio — enables "load starter prompts from global registry" ([RHAISTRAT-1750](https://redhat.atlassian.net/browse/RHAISTRAT-1750)).

Both live in [opendatahub-io/architecture-decision-records](https://github.com/opendatahub-io/architecture-decision-records/tree/main/architecture-decision-records/mlflow).

## Architecture context repository

[opendatahub-io/architecture-context](https://github.com/opendatahub-io/architecture-context) (already indexed at [ref-opendatahub-architecture-context-repo.md](/features/platform/knowledge/ref-opendatahub-architecture-context-repo.md)) carries per-RHOAI-version architecture summaries and C4 diagrams for `odh-dashboard`, including a `rhoai.next` (latest/upcoming) snapshot and per-EA-milestone snapshots (3.5-ea.1, 3.5-ea.2) plus the `OdhDashboardConfig` CRD schema.

## E2E usability research (RHOAI 3.4 GA)

Already fully captured — see [ref-e2e-usability-findings-deployment-playground.md](/features/gen-ai-studio/knowledge/ref-e2e-usability-findings-deployment-playground.md) and [person-yingzhao-zhou.md](/features/gen-ai-studio/knowledge/person-yingzhao-zhou.md). Three implications from that study feed directly into this architecture: tool-execution transparency needs the BFF to surface tool-call traces inline in the chat stream (ties to the tracing epics above); MCP tool use is being adopted as a RAG alternative in regulated environments, so Gen AI Studio should position both as peer context strategies, not RAG-primary; and the "try model before infra investment" user need supports both the AI-Gateway-as-OGX-alternative work and ExternalModel CR support.

## Open architectural questions

Three of these are extracted as standalone questions (see the partition's `knowledge/`); the rest are noted here for completeness:

1. **OGX vs. AI Gateway** — will Gen AI Studio eventually need a pluggable runtime layer abstracting both, or will they coexist as alternative backends indefinitely? → [question-gen-ai-studio-ogx-vs-ai-gateway-runtime.md](/features/gen-ai-studio/knowledge/question-gen-ai-studio-ogx-vs-ai-gateway-runtime.md)
2. **Configuration persistence → deployment** — what's the path from a saved AgentProfile (ConfigMap-backed) to a deployed, callable API service? May need CRDs.
3. **MCP Gateway AuthN** — how does OAuth token exchange work when the Playground user's identity needs to flow through to MCP servers behind the gateway? → [question-gen-ai-studio-mcp-gateway-authn.md](/features/gen-ai-studio/knowledge/question-gen-ai-studio-mcp-gateway-authn.md)
4. **AI Assets convergence** — as prompts, MCP endpoints, guardrails, and vector stores all surface in AI Assets, what's the unified data model? Each asset type currently has its own storage and API path.
5. **Tracing multi-tenancy** — how are OTel traces routed and namespace-isolated in multi-tenant environments?
6. **ExternalModel CR vs. custom endpoints** — if ExternalModel CR satisfies the same use case, does the custom-endpoints feature get deprecated? → [question-gen-ai-studio-externalmodel-vs-custom-endpoints.md](/features/gen-ai-studio/knowledge/question-gen-ai-studio-externalmodel-vs-custom-endpoints.md)

## Key people & teams

Peter Double (Principal PM — MCP, Gen AI Studio, AI Assets); Nick Gagan (Staff Engineer/Tech Lead — frontend & architecture); Andrew Ballantyne (Architecture Lead — dashboard-wide, MaaS, Catalog/Registry); Eder Ignatowicz (Engineering Manager — Team Crimson); Darach Cawley (Engineering Manager — broader team); Jenny Yi (PM — dashboard experience); Ying[zhao Zhou] (UX Researcher — E2E usability studies, see [person-yingzhao-zhou.md](/features/gen-ai-studio/knowledge/person-yingzhao-zhou.md)); plus engineers Chris Jones (tracing/OTel), Avik (multimodal), Gaizka Menendez (BFF/SSE, AgentOps), Danny Pierce (vector stores/AAE), Dana Gutride (scrum/delivery), Griffin Sullivan (MaaS integration). Related teams: Team Purple, Team Monarch (cross-team architecture WG), Team Onyx (MaaS/model-serving dashboard), AgentOps, `#forum-agentic-api` (OGX/Llama Stack API discussions).

## Key references

Source repo: [opendatahub-io/odh-dashboard](https://github.com/opendatahub-io/odh-dashboard). Architecture context: [opendatahub-io/architecture-context](https://github.com/opendatahub-io/architecture-context). ADRs: [opendatahub-io/architecture-decision-records](https://github.com/opendatahub-io/architecture-decision-records). BFF OGX-install entry point: [`lsd_install_handler.go`](https://github.com/opendatahub-io/odh-dashboard/blob/main/packages/gen-ai/bff/internal/api/lsd_install_handler.go). Jira Outcomes: [RHAISTRAT-1312](https://redhat.atlassian.net/browse/RHAISTRAT-1312), [RHAISTRAT-1743](https://redhat.atlassian.net/browse/RHAISTRAT-1743), [RHAISTRAT-1067](https://redhat.atlassian.net/browse/RHAISTRAT-1067).
