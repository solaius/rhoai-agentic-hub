---
title: Agent Registry Research - MLflow Agent Support & Registry Patterns
description: Analysis of MLflow's current agent capabilities and existing registry patterns to identify the RFC insertion point.
source: ai-asset-registry/agents/agent-registry/research/05-mlflow-upstream.md (as of 2026-07-05)
timestamp: 2026-07-06
review_after: 2026-08-05
---

# Agent Registry Research - MLflow Agent Support & Registry Patterns

**Date**: 2026-04-24
**Author**: Peter Double (Principal PM - MCP & AI Asset Registries)
**Purpose**: Analyze MLflow's current agent capabilities and existing registry patterns to identify the RFC insertion point.

---

## 1. Executive Summary

MLflow has a Model Registry (GA, mature), a Prompt Registry (GA since MLflow 3.0), and an emerging Skills Registry (Databricks MVP at [B-Step62/mlflow](https://github.com/B-Step62/mlflow/tree/skill-registry-mvp)). It has **no Agent Registry**. This is the gap the upstream RFC must fill.

MLflow now provides agent authoring (ResponsesAgent), FastAPI-based Agent Server, tracing with 60+ framework integrations, and an AI Gateway. What it lacks is a registry primitive -- a governed, versioned way to register, alias, tag, and discover agent definitions before deployment. The `mlflow.agents` namespace handles runtime concerns; it has no registry counterpart.

The existing registries follow a consistent entity + version pattern: `RegisteredModel`/`ModelVersion`, `Prompt`/`PromptVersion`, `Skill`/`SkillVersion`. The Agent Registry RFC should follow this pattern exactly with `RegisteredAgent`/`AgentVersion`, addressing agents' unique characteristics: multi-component composition, protocol metadata, and runtime discovery extensions.

Red Hat's position is strong. Matt Prahl has 20+ merged MLflow PRs. The Skills Registry MVP validated our preferred architecture (dedicated entity types). No one has proposed an Agent Registry design upstream. The window is open.

---

## 2. MLflow 3 Agent Capabilities

MLflow 3.0 (June 2025) redesigned the platform around GenAI and agent workflows. Releases through MLflow 3.11 (April 2026) have deepened agent support across authoring, serving, tracing, evaluation, and gateway routing.

### 2.1 ResponsesAgent / ChatAgent Interfaces

`ResponsesAgent` is MLflow's recommended agent interface since MLflow 3.0, superseding both `ChatModel` and `ChatAgent`. It is framework-agnostic: subclass `mlflow.pyfunc.ResponsesAgent`, implement `predict` (and optionally `predict_stream`), and wrap any agent framework (LangGraph, CrewAI, OpenAI Agents SDK, custom). Inputs and outputs follow the OpenAI Responses API schema. The legacy `ChatAgent` (ChatCompletion schema) remains functional but is deprecated.

The critical architectural fact: agents in MLflow are treated as **deployable model artifacts**. They are logged, versioned, and served through Model Registry infrastructure. An agent today is a `RegisteredModel` with a `pyfunc` flavor -- there is no separate agent entity type.

([MLflow ResponsesAgent docs](https://mlflow.org/docs/latest/genai/flavors/responses-agent-intro/), April 2026; [MLflow ChatModel guide](https://mlflow.org/docs/latest/genai/flavors/chat-model-guide/), April 2026)

### 2.3 Agent Server

The MLflow Agent Server (experimental, MLflow 3.6.0+) provides a **FastAPI-based hosting solution** for ResponsesAgent-wrapped agents. It serves agents at `/invocations` with decorator-based registration (`@invoke`, `@stream`), automatic request/response validation, built-in tracing, and async streaming. It is distinct from the general `mlflow models serve` command -- the Agent Server adds agent-specific validation and tracing.

([MLflow Agent Server docs](https://mlflow.org/docs/latest/genai/serving/agent-server/), April 2026)

### 2.4 LoggedModel Entity

MLflow 3 introduced `LoggedModel` as a **first-class entity**, created when you call `log_model()`. It carries its own metadata (parameters, metrics), provides lineage between models, runs, traces, prompts, and evaluation metrics, and serves as a metadata hub linking to external code and configuration. For agents, LoggedModel is the bridge between development and registry -- the proposed Agent Registry would provide an alternative promotion target alongside RegisteredModel.

([MLflow 3 release notes](https://mlflow.org/releases/3), June 2025; [MLflow LoggedModel API](https://mlflow.org/docs/latest/api_reference/python_api/mlflow.client.html))

### 2.5 Tracing & Observability

MLflow Tracing is the platform's most mature agent capability, providing OpenTelemetry-compatible observability across the entire agent execution lifecycle.

**Current state (MLflow 3.11, April 2026):** 60+ framework integrations, production-ready async logging, lightweight `mlflow-tracing` package (95% smaller footprint), native OpenTelemetry GenAI Semantic Conventions, distributed tracing for multi-agent systems, trace-aware evaluation via TruLens Agent GPA scorers, automatic AI-powered issue detection, interactive trace graph visualization, and per-model cost tracking.

The tracing infrastructure is significant for the Agent Registry RFC because it provides the **observability backbone** that a registry can reference. An AgentVersion could link to trace experiments, evaluation results, and quality metrics -- connecting the governance plane (registry) to the operational plane (tracing).

([MLflow Tracing docs](https://mlflow.org/docs/latest/genai/tracing/), April 2026; [MLflow 3.11.1 release](https://mlflow.org/releases/3.11.1/), April 2026)

### 2.6 The mlflow.agents Namespace

The `mlflow.agents` namespace today is thin. It primarily provides:
- `mlflow.agents.invoke()` -- invoke a deployed agent
- Integration with the Deployments API (`mlflow.deployments`) for managing agent endpoints
- The `ResponsesAgent` base class (under `mlflow.pyfunc`)
- Agent Server utilities (under `mlflow.genai.agent_server`)

What `mlflow.agents` does **not** provide:
- `register_agent()` -- no agent registration function
- `load_agent()` -- no agent loading from a registry
- `search_agents()` -- no agent discovery
- `set_agent_alias()` -- no alias management
- No `agents:/name/version` URI scheme

This is the empty namespace the RFC fills. The pattern established by the Prompt Registry (`mlflow.genai.register_prompt()`, `mlflow.genai.load_prompt()`) and the Skills Registry MVP (`mlflow.genai.register_skill()`, `mlflow.genai.load_skill()`) directly predicts what `mlflow.agents` (or `mlflow.genai`) should gain.

---

## 3. Registry Architecture Pattern Analysis

MLflow's registries follow a consistent pattern. Analyzing this pattern is essential for predicting what Databricks will accept in an Agent Registry RFC.

### 3.1 Model Registry (Mature, GA)

The Model Registry is the original and most mature registry in MLflow. It established the architectural patterns all subsequent registries follow.

| Aspect | Detail |
|--------|--------|
| **Top-level entity** | `RegisteredModel` (name, description, creation_timestamp, last_updated_timestamp, tags, aliases, latest_versions) |
| **Version entity** | `ModelVersion` (name, version, source, run_id, status, description, creation_timestamp, last_updated_timestamp, tags, aliases, run_link, current_stage) |
| **Versioning** | Auto-incrementing integers starting from 1, immutable snapshots |
| **Lifecycle** | MLflow 3 deprecated stage transitions (None/Staging/Production/Archived) in favor of aliases |
| **Aliases** | Mutable named references (e.g., "champion", "production", "challenger") pointing to specific versions |
| **Tags** | Key-value metadata on both model and version levels |
| **REST API** | Full CRUD at `2.0/mlflow/registered-models/` and `2.0/mlflow/model-versions/` |
| **Python API** | `mlflow.register_model()`, `mlflow.client.MlflowClient.create_registered_model()`, `get_registered_model()`, `search_registered_models()`, `set_registered_model_alias()`, etc. |
| **URI scheme** | `models:/name/version` or `models:/name@alias` |
| **Store pattern** | Abstract store with SqlAlchemy, file-based, and REST implementations |
| **Unity Catalog** | In Databricks, models register in Unity Catalog with workspace-scoped governance |

([MLflow Model Registry docs](https://mlflow.org/docs/latest/ml/model-registry), April 2026; [RegisteredModel source](https://mlflow.org/docs/latest/_modules/mlflow/entities/model_registry/registered_model.html))

### 3.2 Prompt Registry (GA, MLflow 3.0+)

The Prompt Registry was introduced as GA in MLflow 3.0. It follows the Model Registry pattern but with prompt-specific features.

| Aspect | Detail |
|--------|--------|
| **Top-level entity** | `Prompt` (name, description, tags, latest_version, creation_timestamp, last_updated_timestamp) |
| **Version entity** | `PromptVersion` (name, version, template, commit_message, creation_timestamp, tags, aliases, user_id, response_format, model_config) |
| **Versioning** | Auto-incrementing integers, immutable versions |
| **Template format** | String with `{{variable}}` placeholders, or list of chat messages with role/content |
| **Lifecycle** | No publish state -- versions are immediately available |
| **Aliases** | Mutable named references (e.g., "production", "staging") |
| **Tags** | Key-value on both prompt and version levels |
| **Python API** | `mlflow.genai.register_prompt()`, `load_prompt()`, `search_prompts()`, `set_prompt_alias()`, `set_prompt_tag()` |
| **URI scheme** | `prompts:/name/version` or `prompts:/name@alias` |
| **Caching** | In-memory with configurable TTL (infinite for version-based, 60s for alias-based) |
| **Lineage** | Links to LoggedModel via `mlflow.set_active_model()` -- tracks which prompts an application version uses |
| **Model config** | Model-specific configuration (model name, parameters) stored alongside the prompt version |
| **Implementation note** | Prompts are internally stored as a specialized type of ModelVersion with special tags (`IS_PROMPT_TAG_KEY`, `PROMPT_TEXT_TAG_KEY`, `PROMPT_TYPE_TAG_KEY`). Edson Tirelli noted there is "tech debt" in this approach. |

([MLflow Prompt Registry docs](https://mlflow.org/docs/latest/genai/prompt-registry/), April 2026; [PromptVersion source](https://mlflow.org/docs/latest/api_reference/_modules/mlflow/entities/model_registry/prompt_version.html); [Prompt entity source](https://mlflow.org/docs/latest/api_reference/_modules/mlflow/entities/model_registry/prompt.html))

### 3.3 Skills Registry (Databricks MVP, Not Yet Merged)

The Skills Registry MVP (discovered April 2026 at [B-Step62/mlflow](https://github.com/B-Step62/mlflow/tree/skill-registry-mvp)) is documented extensively in the Skills research series (see [skills/skills-registry/research/02-mlflow-upstream.md](/features/skills-registry/research/02-mlflow-upstream.md)). Key architectural decisions relevant to the Agent Registry:

| Aspect | Detail |
|--------|--------|
| **Top-level entity** | `Skill` (name, description, creation_timestamp, last_updated_timestamp, latest_version, aliases) |
| **Version entity** | `SkillVersion` (name, version, source, description, manifest_content, artifact_location, creation_timestamp, tags, aliases, created_by) |
| **Implementation** | **Dedicated entity type** -- 5 new database tables (`registered_skills`, `skill_versions`, `skill_version_tags`, `skill_tags`, `skill_aliases`), NOT tag-based ModelVersion specialization |
| **REST API** | `ajax-api/3.0/mlflow/skills/` (newer API version than Model Registry's `2.0/`) |
| **Python API** | `mlflow.genai.register_skill()`, `load_skill()`, `preview_skills()`, `search_skills()`, `install_skill()` |
| **Source provenance** | GitHub URL with automatic commit hash extraction, or local directory path |
| **What it lacks** | No lifecycle states, no approval workflows, no URI scheme, no workspace-scoped RBAC |

The Skills Registry MVP's choice of dedicated entity types validates that Databricks will create new tables for each registry type, rather than forcing everything into ModelVersion.

### 3.4 Predicted Agent Registry Pattern

| Aspect | Predicted Pattern | Agent-Specific Considerations |
|--------|-------------------|-------------------------------|
| **Top-level entity** | `RegisteredAgent` (name, description, tags, aliases, latest_version) | Needs protocol field (A2A, OpenAI-compatible, custom), agent_type (single, multi-agent, orchestrator) |
| **Version entity** | `AgentVersion` (name, version, source, description, tags, aliases, created_by, artifact_location) | Needs composition metadata: model references, tool/MCP server references, prompt references, skill references |
| **Database** | Dedicated tables: `registered_agents`, `agent_versions`, `agent_version_tags`, `agent_tags`, `agent_aliases` | Likely adds `agent_version_dependencies` for composition tracking |
| **Versioning** | Auto-incrementing integers, immutable snapshots | Same pattern |
| **Aliases** | Mutable named references | Same pattern |
| **REST API** | `ajax-api/3.0/mlflow/agents/` or `2.0/mlflow/agents/` | Same pattern |
| **Python API** | `mlflow.genai.register_agent()`, `load_agent()`, `search_agents()` | Same pattern, extends `mlflow.agents` namespace |
| **URI scheme** | `agents:/name/version` or `agents:/name@alias` | Same pattern |
| **Governance** | None upstream (downstream RHOAI concern) | Lifecycle states, approval workflows, certification -- all downstream |

### 3.5 Cross-Registry Comparison Table

| Dimension | Model Registry | Prompt Registry | Skills Registry (MVP) | Agent Registry (Predicted) |
|-----------|---------------|-----------------|----------------------|---------------------------|
| Entity pair | RegisteredModel / ModelVersion | Prompt / PromptVersion | Skill / SkillVersion | RegisteredAgent / AgentVersion |
| Storage approach | Dedicated tables | Tag-based ModelVersion specialization (tech debt) | Dedicated tables | Dedicated tables (should follow Skills precedent) |
| Versioning | Auto-increment integer | Auto-increment integer | Auto-increment integer | Auto-increment integer |
| Aliases | Yes (champion, production) | Yes (production, staging) | Yes (champion, prod) | Yes |
| Tags | Model-level + version-level | Prompt-level + version-level | Skill-level + version-level | Agent-level + version-level |
| URI scheme | `models:/name/version` | `prompts:/name/version` | Not implemented (gap) | `agents:/name/version` |
| Artifact storage | Model artifacts in artifact store | Template text in tags | SKILL.md files in artifact store | Agent definition artifacts in artifact store |
| Source provenance | Run ID + artifact path | N/A (inline template) | GitHub URL + commit hash | Framework source + dependency manifest |
| Lifecycle/publish state | Deprecated stages, now aliases only | None | None | None upstream (downstream extension) |
| Composition tracking | None | model_config (model reference) | None | Model refs, tool refs, prompt refs, skill refs |
| REST API base | `2.0/mlflow/` | `2.0/mlflow/` | `ajax-api/3.0/mlflow/` | TBD |

---

## 4. Databricks Agent Framework Context

Databricks is both the primary maintainer of MLflow and the largest consumer of its agent capabilities. Understanding their internal patterns is essential for framing an acceptable RFC.

### 4.1 Mosaic AI Agent Framework

The Mosaic AI Agent Framework is Databricks' production agent platform, built on top of MLflow. It provides:

- **Agent authoring**: Build agents using any framework (LangGraph, OpenAI Agents SDK, custom), wrapped in MLflow's ResponsesAgent interface
- **Agent evaluation**: Automated evaluation of agent quality using LLM judges, with multi-turn conversation simulation
- **Agent deployment**: One-click deployment to Databricks Model Serving endpoints or Databricks Apps
- **Agent tracing**: Full MLflow tracing integration for observability
- **Tool integration**: Unity Catalog Functions as governed tools, MCP servers for external tool access

The Agent Framework uses MLflow's **Model Registry** for agent governance today. Agents are logged as pyfunc models, registered as RegisteredModels, and versioned as ModelVersions. There is no separate agent registry in Databricks' current product.

([Mosaic AI Agent Framework](https://www.databricks.com/product/machine-learning/retrieval-augmented-generation), April 2026; [Databricks agent authoring docs](https://docs.databricks.com/aws/en/generative-ai/agent-framework/author-agent), April 2026)

### 4.2 Agent Bricks

Agent Bricks (announced Data + AI Summit 2025) automates agent optimization: auto-generates task-specific evaluations and LLM judges, creates domain-specific synthetic data, searches across optimization techniques, and delivers production agents in minutes. Ships with pre-built types (Information Extraction, Knowledge Assistant, Supervisor/multi-agent). Early adopters include AstraZeneca and Hawaiian Electric.

**Registry implication**: Each Agent Bricks optimization iteration produces a new agent variant currently managed through the Model Registry. A dedicated Agent Registry could provide richer metadata -- tracking optimization techniques, synthetic data, evaluation benchmarks, and composition differences between iterations.

([Databricks launches Agent Bricks](https://www.databricks.com/company/newsroom/press-releases/databricks-launches-agent-bricks-new-approach-building-ai-agents), June 2025; [Mosaic AI Summit announcements](https://www.databricks.com/blog/mosaic-ai-announcements-data-ai-summit-2025), June 2025)

### 4.3 Unity Catalog for Governance

Unity Catalog is Databricks' unified governance layer. In 2026 it covers models (workspace-scoped permissions, lineage, audit trails), UC Functions (governed agent tools), AI Gateway (now **Unity AI Gateway**, Beta April 2026 -- extends UC governance to LLM endpoints, MCP servers, and coding agents), MCP governance (on-behalf-of user execution), and cost attribution (every request logged with dollar costs).

Unity Catalog does **not** have a dedicated "Agent" asset type -- agents are governed as models. This mirrors the MLflow OSS gap and suggests a well-designed MLflow Agent Registry could eventually map to a Unity Catalog Agent asset type.

([Unity AI Gateway blog](https://www.databricks.com/blog/ai-gateway-governance-layer-agentic-ai), April 2026; [Unity AI Gateway docs](https://docs.databricks.com/aws/en/ai-gateway/), April 2026)

### 4.4 AI Gateway (Unity AI Gateway)

The AI Gateway (now Unity AI Gateway, Beta April 2026) provides routing (fallbacks, rate limits, load balancing), guardrails (PII, content safety, prompt injection, custom), MCP governance, full observability, cost tracking, and coding agent governance.

The AI Gateway handles **post-deployment routing and governance**; the Agent Registry handles **pre-deployment definition and versioning**. These are complementary and the RFC should acknowledge this boundary clearly.

([MLflow AI Gateway guardrails blog](https://mlflow.org/blog/gateway-guardrails), March 2026; [Databricks AI Gateway docs](https://docs.databricks.com/aws/en/ai-gateway/overview-beta), April 2026)

### 4.5 How Databricks Might Use an Agent Registry

A Databricks-accepted Agent Registry would: (1) complement the Model Registry with richer agent-specific metadata; (2) store tool bindings, prompt references, framework type, and protocol capabilities that ModelVersion cannot capture cleanly; (3) version Agent Bricks optimization iterations; (4) map to a Unity Catalog Agent asset type; and (5) feed the AI Gateway with routing/governance metadata.

---

## 5. Key GitHub Issues & PRs

No existing agent registry proposals exist in the MLflow GitHub repository, but several adjacent discussions inform the RFC.

### 5.1 No Agent Registry Proposals Exist

As of April 24, 2026, there are **no open issues, PRs, or discussions** in [mlflow/mlflow](https://github.com/mlflow/mlflow) proposing an agent registry, a `RegisteredAgent` entity, or an `agents:/` URI scheme. The namespace is unoccupied. This is unlike the Skills Registry space, where Issue [#20435](https://github.com/mlflow/mlflow/issues/20435) explicitly requested skills version management and received maintainer encouragement.

### 5.2 MLflow 2026 Roadmap (Discussion #19855)

The [MLflow OSS Roadmap for 2026](https://github.com/mlflow/mlflow/discussions/19855) identifies four priorities: tracing observability, evaluation (multi-turn, tool-calling), prompt management, and platform foundations. Agent registry is not listed, but the roadmap invites contributors to open issues for aligned features. An Agent Registry framed as extending prompt management patterns to agent definitions aligns with all four areas.

### 5.3 Skills Version Management (Issue #20435)

The most relevant precedent. Community member KMichan requested "version control for Agent Skills similar to the Prompt Registry." Databricks maintainer Corey Zumar responded: *"I think this would be a nice extension to our Prompt Registry. Is this something you'd be able to share a brief design for? We'd love to support you in the process of delivering this."* This response pattern -- maintainer inviting a community design proposal -- is exactly what the Agent Registry RFC should target.

### 5.4 Adjacent Signals

- **EU AI Act compliance (Issue [#21022](https://github.com/mlflow/mlflow/issues/21022))**: Proposes governance metadata (risk classification, conformity) in the Model Registry -- demonstrates community appetite for structured governance fields, though these are downstream RHOAI concerns for agents.
- **mlflow.agents module**: No PRs in 2026 have attempted to add registry functionality. Activity has focused on ResponsesAgent improvements, Agent Server, tracing integrations, and evaluation.
- **Model Registry Webhooks (MLflow 3.3.0)**: Webhooks on registry events (registration, version creation, alias changes) landed in January 2026. An Agent Registry should include the same capability from day one.

---

## 6. What Upstream Will Accept

Every decision in the RFC must pass the Databricks acceptance filter. Based on MLflow registry evolution and the Skills Registry MVP precedent, these are the constraints.

### 6.1 Must Follow Existing Registry Patterns

The RFC must propose: `RegisteredAgent` (top-level entity) and `AgentVersion` (immutable snapshot) with auto-incrementing integer versions, mutable aliases, key-value tags at both levels, REST API, Python SDK under `mlflow.genai` or `mlflow.agents`, and URI scheme `agents:/name/version` or `agents:/name@alias`. Deviations will be rejected.

### 6.2 Must Be Plugin-Agnostic

The RFC **cannot depend on kagenti**, A2A, or any specific agent framework. Protocol metadata (A2A, OpenAI-compatible, custom) should be optional tags, not required fields. Varsha's pluggable discovery provider system (`mlflow.agent_discovery` entry points) follows MLflow conventions and would be accepted -- but belongs in the **post-deployment discovery extension**, not the core registry.

### 6.3 Must Be Opt-In

No breaking changes. New additive subsystem, new Alembic migration adding tables (never modifying existing ones), new API endpoints only, no impact on existing registries.

### 6.4 Governance, Approval, and Certification Are Downstream

Critical framing principle. The upstream MLflow Agent Registry provides **primitives**: register, version, alias, tag, search, load. Lifecycle states, approval workflows, certification, trust tiers, and RBAC are all **RHOAI downstream extensions** -- the same pattern as Model Registry (MLflow primitives; Unity Catalog governance in Databricks; RHOAI enterprise governance in OpenShift AI).

### 6.5 Discovery Providers as Entry-Point Plugins

MLflow's established plugin mechanism uses Python entry points for extensibility (precedent: `mlflow.deployments`, `mlflow.tracking_store`, `mlflow.artifact_repository`). The Agent Registry should define an `mlflow.agent_discovery` entry point group for pluggable discovery backends (Kubernetes/kagenti, Docker, Consul, static files). Varsha's `AgentDiscoveryProvider` interface (`discover()` + optional `watch()`) follows this convention and should be included as the runtime discovery extension.

### 6.6 Pre-Deployment = Primary Upstream Value

The core upstream value proposition is **pre-deployment agent governance**: register agent definitions with their composition metadata (which model, which tools, which prompts, which skills), version them, alias them for deployment targeting, and search/discover them within the registry.

Post-deployment concerns -- runtime discovery of live agents, health checking, lifecycle state management (ACTIVE/UNHEALTHY/STALE/REMOVED) -- are valuable but should be positioned as an **extension layer**, not the core registry. This is a deliberate scope boundary:

| Concern | Upstream (MLflow OSS) | Downstream (RHOAI) |
|---------|----------------------|---------------------|
| Agent definition versioning | Core registry | Inherited |
| Aliases and tags | Core registry | Extended with governance tags |
| Composition metadata | Core registry | Extended with dependency validation |
| Runtime discovery | Plugin extension (`mlflow.agent_discovery`) | kagenti integration |
| Lifecycle states | Not included | Draft/Published/Deprecated/Archived |
| Approval workflows | Not included | Review gates, certification |
| Runtime health monitoring | Plugin extension | Integrated with OpenShift monitoring |

---

## 7. Red Hat Contributors & Relationships

### 7.1 Matt Prahl (GitHub: [mprahl](https://github.com/mprahl))

Matt is Red Hat's most active MLflow contributor with 20+ merged PRs since February 2026. His work focuses on infrastructure that directly enables registry functionality:

- **Workspace support**: Multi-workspace environments for logical isolation of experiments, models, and prompts
- **Trace archival**: Lifecycle management for traces
- **Labeling**: Metadata tagging and organization
- **UI improvements**: Execution recovery, workspace navigation

Matt has been providing Red Hat requirements to Databricks for the Skills Registry via Slack (per the 2026-04-07 AI Asset Registries Sync meeting). His workspace support work is foundational -- workspaces provide the scoping boundary that any new registry type (including agents) operates within.

### 7.2 Dan Kuc (GitHub: [dkuc](https://github.com/dkuc))

Dan is positioned on MLflow/registry work at Red Hat. He has forked both `mlflow/mlflow` and `kubeflow/model-registry`. No public commits, issues, PRs, or comments in mlflow/mlflow are visible as of April 2026. His engagement is likely through internal channels and design discussions rather than public GitHub contributions.

### 7.3 Edson Tirelli

Edson is Red Hat's primary liaison with Databricks. He maintains the relationship with the MLflow maintainers (including Corey Zumar / dbczumar and Yuki Watanabe / B-Step62) and coordinates on upstream strategy. Key context from meeting transcripts:

- Reported that Databricks/MLflow maintainers are building a skills catalog/registry experience in MLflow (confirmed by the B-Step62 MVP)
- Noted the Prompt Registry's "tech debt" (prompts as "models with a special flag") -- advocacy for dedicated entity types in new registries
- Qualified Databricks timelines: *"I don't know if that is going to happen"* -- indicating uncertainty in Databricks delivery schedules
- Coordinates Red Hat's upstream strategy with Matt Prahl and Dan Kuc

### 7.4 Varsha Prasad Narsing

Varsha authored the post-deployment agent registry proposal (see [agent-registry-upstream-proposal.md](/features/agent-registry/strategy/upstream-proposal.md)) covering runtime discovery with pluggable providers, kagenti integration, and Gateway bridging. Peter Double has taken over the agent registry initiative, building the research and RFC foundation documented in this series.

### 7.5 Key Databricks Contacts

- **Corey Zumar (dbczumar)**: MLflow maintainer, key decision-maker for registry features, invited community design proposals on Issue #20435.
- **Yuki Watanabe (B-Step62)**: Building both Skills Evaluation (PR #21725) and Skills Registry MVP. Primary implementation contact.
- **Daniel Lok (daniellok-db)**: Skills Evaluation PR co-author.

---

## 8. Strategic Implications

### 8.1 Timing

The Agent Registry RFC window is **open but time-sensitive**.

**In our favor:** No one has proposed an Agent Registry upstream -- the namespace is unoccupied. The Skills Registry MVP validated our preferred architecture (dedicated entity types). Red Hat has active contributors (Matt Prahl, 20+ PRs) and Databricks relationships (Edson Tirelli). Corey Zumar has demonstrated willingness to accept community-driven registry designs. AWS launching Agent Registry (April 2026) creates external market pressure.

**Against us:** Databricks could build an agent registry internally (as they did with Skills). The ~1 month design approval process means the RFC must be submitted soon. Agent registry is not on the 2026 MLflow roadmap. Agent scope complexity (multi-component composition, protocol diversity, framework diversity) exceeds skills or prompts.

### 8.2 Risks

1. **Databricks builds it first**: The Skills Registry MVP appeared without warning. Databricks could build an agent registry MVP internally. Mitigation: submit the RFC early, align with Edson/Matt on Databricks' internal plans.
2. **Scope creep**: Agents reference models, tools, prompts, skills, and each other. Mitigation: propose a minimal core (RegisteredAgent + AgentVersion) and define extension points for composition tracking and discovery.
3. **Framework fragmentation**: Agents have no standard definition format (Python graphs, YAML configs, Python classes). Mitigation: store agents as opaque artifacts with structured metadata in tags and fields.
4. **Pre/post-deployment confusion**: Varsha's proposal covers runtime discovery; the RFC covers pre-deployment registration. Mitigation: present as two clean layers with an explicit interface.

### 8.3 Opportunities

1. **Define the standard first**: No open-source AI platform has an agent registry integrated with tracing, evaluation, and model serving. MLflow has the infrastructure; it needs the registry primitive.
2. **Clear Red Hat value-add**: Enterprise governance on top of MLflow primitives -- same proven pattern as MCP Registry and Model Registry. RHOAI adds what MLflow won't.
3. **Cross-registry composition**: An Agent Registry referencing Model, Prompt, and Skills registries creates a dependency graph unique to agents. Red Hat can lead cross-registry lineage design.
4. **kagenti as Kubernetes discovery provider**: The plugin system positions kagenti as the reference K8s implementation without creating MLflow dependency -- clean separation of concerns.
5. **A2A AgentCard alignment**: The registry metadata model should align with AgentCard fields (see [02-standards-and-protocols.md](./02-standards-and-protocols.md)) without requiring A2A compliance, positioning for future integration.

---

## 9. References

### MLflow Documentation
- [MLflow 3 Release Notes](https://mlflow.org/releases/3) | [3.11.1](https://mlflow.org/releases/3.11.1/) | [3.10.0](https://mlflow.org/releases/3.10.0/) | [3.9.0](https://mlflow.org/releases/)
- [Model Registry Docs](https://mlflow.org/docs/latest/ml/model-registry) | [Prompt Registry Docs](https://mlflow.org/docs/latest/genai/prompt-registry/)
- [ResponsesAgent Docs](https://mlflow.org/docs/latest/genai/flavors/responses-agent-intro/) | [Agent Server Docs](https://mlflow.org/docs/latest/genai/serving/agent-server/)
- [Tracing Docs](https://mlflow.org/docs/latest/genai/tracing/) | [Model Serving Docs](https://mlflow.org/docs/latest/genai/serving/)
- [RegisteredModel Source](https://mlflow.org/docs/latest/_modules/mlflow/entities/model_registry/registered_model.html) | [PromptVersion Source](https://mlflow.org/docs/latest/api_reference/_modules/mlflow/entities/model_registry/prompt_version.html)
- [AI Gateway Guardrails Blog](https://mlflow.org/blog/gateway-guardrails)

### MLflow GitHub
- [mlflow/mlflow Repository](https://github.com/mlflow/mlflow) | [Releases](https://github.com/mlflow/mlflow/releases) | [Changelog](https://github.com/mlflow/mlflow/blob/master/CHANGELOG.md)
- [2026 Roadmap Discussion #19855](https://github.com/mlflow/mlflow/discussions/19855)
- [Skills Version Management Issue #20435](https://github.com/mlflow/mlflow/issues/20435) | [Skills Evaluation Issue #21255](https://github.com/mlflow/mlflow/issues/21255) | [Skills Evaluation PR #21725](https://github.com/mlflow/mlflow/pull/21725)
- [EU AI Act Compliance Issue #21022](https://github.com/mlflow/mlflow/issues/21022)
- [B-Step62 Skills Registry MVP](https://github.com/B-Step62/mlflow/tree/skill-registry-mvp)

### Databricks
- [Mosaic AI Agent Framework](https://www.databricks.com/product/machine-learning/retrieval-augmented-generation) | [Agent Authoring Docs](https://docs.databricks.com/aws/en/generative-ai/agent-framework/author-agent)
- [Agent Bricks Announcement](https://www.databricks.com/company/newsroom/press-releases/databricks-launches-agent-bricks-new-approach-building-ai-agents) | [Summit 2025 Announcements](https://www.databricks.com/blog/mosaic-ai-announcements-data-ai-summit-2025)
- [Unity AI Gateway Blog](https://www.databricks.com/blog/ai-gateway-governance-layer-agentic-ai) | [Unity AI Gateway Docs](https://docs.databricks.com/aws/en/ai-gateway/)
- [Coding Agent Governance](https://www.databricks.com/blog/governing-coding-agent-sprawl-unity-ai-gateway)

### Red Hat Contributors
- Matt Prahl: [github.com/mprahl](https://github.com/mprahl) -- 20+ MLflow PRs
- Dan Kuc: [github.com/dkuc](https://github.com/dkuc) -- MLflow/registry contributor

### Prior Research (This Series)
- [01-agent-ecosystem.md](./01-agent-ecosystem.md) -- Terminology map, three-layer abstraction model
- [02-standards-and-protocols.md](./02-standards-and-protocols.md) -- A2A, MCP, Oracle Agent Spec analysis
- [03-kagenti-and-kubernetes.md](./03-kagenti-and-kubernetes.md) -- kagenti architecture, CRD design, discovery
- [04-agent-management-landscape.md](./04-agent-management-landscape.md) -- AWS, IBM, Google competitive landscape
- [Skills Registry MLflow Research](/features/skills-registry/research/02-mlflow-upstream.md) -- Skills Registry MVP, Red Hat contributor activity
- [Agent Registry Proposal](/features/agent-registry/strategy/upstream-proposal.md) -- Varsha's post-deployment discovery, plugin system
