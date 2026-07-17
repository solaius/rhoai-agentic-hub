---
title: Agent Registry Research - RHOAI Patterns, Decisions & Internal Context
description: Transferable patterns from MCP and skills registry work, internal decisions, and the ownership landscape for the agent registry.
source: ai-asset-registry/agents/agent-registry/research/06-rhoai-context.md (as of 2026-07-05)
timestamp: 2026-07-06
review_after: 2026-08-05
---

# Agent Registry Research - RHOAI Patterns, Decisions & Internal Context

> Superseded 2026-07-16 in part by [09-architecture](09-architecture.md) and [10-requirements](10-requirements.md) — kagenti-as-deployment-primitive and the 3.5 co-priority are overtaken (OpenShell, 3.6); the dual-state-machine analysis stands and is extended (four join points, SUSPENDED state, verified-naming hazard).

**Date**: 2026-04-24
**Author**: Peter Double (Principal PM - MCP & AI Asset Registries)
**Purpose**: Extract transferable patterns from MCP and skills registry work, document internal decisions, and map the ownership landscape.

---

## 1. Transferable Patterns from MCP Registry

The MCP Registry, designed for RHOAI 3.5 Dev Preview, establishes foundational patterns for AI asset governance in MLflow. The MCP Registry design doc itself anticipated this reuse: *"This data model is MCP-specific, but the pattern (logical asset + versioned record, separated governance tracks, workspace scoping) could inform future data models for agents, skills, and other AI assets."* (Source: MCP Registry design doc, cited in [skills research](/features/skills-registry/research/04-rhoai-patterns-and-meetings.md))

The following table assesses each MCP pattern against agent registry requirements.

| Pattern | Transfers? | What Changes for Agents |
|---|---|---|
| **Two-tier entity model** | Yes | Agent + AgentVersion follows the same structure. Agent entity holds stable identity; AgentVersion holds immutable definition snapshot plus mutable governance metadata. |
| **Four governance tracks** | Yes | All four tracks (lifecycle, approval, verification, certification) transfer unchanged, including the invariant that `lifecycle_state=PUBLISHED` requires `approval_status=APPROVED`. |
| **Workspace-scoped RBAC** | Yes | Agent records scoped to workspaces for multi-tenant visibility. Aligns with Matt Prahl's workspace support work in MLflow. |
| **Metadata-first records** | Yes | Transfers with richer metadata. Agents carry additional fields: protocol type (A2A, OpenAI-compatible, custom), skills/capabilities, identity claims, and trust domain. |
| **Gateway integration** | Partially | MCP Gateway provides tool-level mediation. Agent routing operates higher -- request routing, traffic splitting, fallbacks based on capabilities and health. Agents may also route *through* MCP Gateway when invoking tools, creating a layered integration. |
| **Deployment/runtime lifecycle** | Partially | MCP Registry records deployment references ([Story 6](https://github.com/solaius/ai-asset-registry/blob/main/mcps/mcp-registry/mcp-registry-3.5-user-stories.md)). Agents have a richer runtime lifecycle with four runtime states (ACTIVE, UNHEALTHY, STALE, REMOVED) from Varsha's proposal. The agent registry must track both governance state and runtime state -- a dual-state model absent from MCP. |
| **Ingestion pipeline** | Partially | The MCP pipeline pattern (validate -> scan -> containerize -> register) partially transfers. Agents need endpoint validation and protocol compliance checks rather than containerization. Pre-deployment definitions need code scanning; post-deployment agents need health checking and identity verification. |
| **Downstream read surfaces** | Yes | Stories 5 and 8 (surface to catalog, surface to AAA/Studio) transfer directly. The pattern -- registry as governance truth, catalog as discovery surface -- is identical. |
| **Version history and deprecation** | Yes | Transfers directly. Even more important for agents since deployed instances reference specific versions. |
| **"Store state vs. automate behavior"** | Yes | The phased approach transfers: store governed state first, automate handoffs later. |

**Summary**: 7 patterns transfer directly, 3 transfer partially. The partial transfers all relate to the same root cause: agents are running services with runtime state, whereas MCP servers in the registry are governed metadata records that point to separately deployed services. This runtime dimension is what makes the agent registry distinct.

---

## 2. Transferable Patterns from Skills Registry

The skills registry research, completed two weeks prior to this document, applied the same transferability analysis from MCP to skills. Several of those patterns cascade further to agents.

| Pattern | Transfers? | What Changes for Agents |
|---|---|---|
| **Upstream/downstream story split** | Yes | The skills [user stories](/features/skills-registry/strategy/user-stories.md) cleanly separate upstream MLflow stories (U1-U7) from RHOAI-specific stories (R1-R8). This template directly informs agent registry story structure. |
| **User story format** | Yes | Format (actor, action, outcome, acceptance notes) reusable as-is. Actor set adjusted: "Skill Author" becomes "Agent Developer"; "MCP Gateway" becomes "AI Gateway"; "Kagenti Operator" added. |
| **Packaging analysis** | No | Skills packaging (SKILL.md, OCI artifacts) does not transfer. Agents are services, not files. The equivalent analysis covers deployment models (container image, Helm chart, CRD) and protocol compliance. |
| **Data model (entity + version + governance)** | Yes | Three-layer model transfers cleanly: Agent entity, AgentVersion with immutable snapshot, governance extensions with four independent tracks. Same pattern across all asset types. |
| **Trust tiers** | Yes | Four tiers (Red Hat certified, Partner, Community, Unverified) apply with same semantics. Agents may additionally reflect SPIFFE/SPIRE identity verification status. |
| **Dependency tracking via tags** | Yes | Tag-based loose references (Phase 1) followed by formal associations (Phase 2) is the right phasing. Agents have richer graphs -- dependencies on MCP servers, skills, models, prompts, guardrails, and other agents. |
| **Registry vs. catalog** | Yes (resolved) | Both needed. December 17 decision (MLflow for registries, Kubeflow for catalogs) applies uniformly across all AI asset types. |

**Summary**: 5 of 7 patterns transfer, 1 partially, 1 does not. The skills work provides the template for agent registry story structure. Packaging analysis does not transfer because agents are services, not files.

---

## 3. What's Different About Agents

While the governance framework (data model, lifecycle tracks, workspace scoping) transfers cleanly from MCP and skills, agents introduce several capabilities and complexities that are genuinely new.

### 3.1 Running Services with Endpoints

MCP servers are referenced by endpoint metadata but deployed separately. Skills are files with no runtime presence. Agents are more complex: running services with network endpoints where the registry must govern both the *definition* (pre-deployment) and the *instance* (post-deployment).

This **dual-entity challenge** was identified in the [asset types documentation](https://github.com/solaius/ai-asset-registry/blob/main/docs/knowledge-review/assets/asset-types.md): "The proposal covers post-deployment (live agent discovery and monitoring) but not pre-deployment (agent definition versioning, governance, approval). Red Hat needs both." Varsha's upstream proposal explicitly scoped to post-deployment only.

### 3.2 Runtime State

MCP and skills registries track governance state only. Agent registries must additionally track **runtime state** (ACTIVE, UNHEALTHY, STALE, REMOVED from Varsha's proposal), creating two independent state machines:

- **Governance state**: Controlled by Platform Engineers. Determines whether an agent *should* be available.
- **Runtime state**: Determined by discovery plugins and health checks. Describes whether an agent *is* available.

These state machines are independent. A governance-deprecated agent can still be ACTIVE (deprecation is a signal, not enforcement). An UNHEALTHY agent can be governance-published (the registry records reality).

### 3.3 Protocol Diversity

MCP servers use one protocol (MCP with SSE or Streamable HTTP). Skills have no protocol. Agents communicate via multiple protocols:

- **A2A (Agent-to-Agent)**: AgentCard discovery, task lifecycle, streaming. Adopted by kagenti.
- **OpenAI-compatible**: De facto standard for chat-based interaction. MLflow ResponsesAgent supports this.
- **Custom**: Framework-specific protocols.

Protocol metadata is registry-critical -- it determines consumer interaction, gateway routing, and agent-to-agent communication feasibility.

### 3.4 Capability-Based Discovery

Agents expose structured **skills** (capability declarations) aligned with A2A's AgentCard format (`id`, `name`, `description`, `tags`, `examples`). The registry must index these to enable capability-based discovery ("Find agents that can process invoices"). This discovery dimension is absent from MCP and skills registries.

### 3.5 Cryptographic Identity

Agents in multi-agent architectures require **cryptographic identity verification** beyond standard Kubernetes RBAC:

- **SPIFFE/SPIRE**: Workload identity via SVIDs. Kagenti injects SPIFFE identity into agent workloads.
- **JWS signatures**: Agent identity attestation and verification via kagenti.
- **Trust domains**: Organizational boundaries determining which agents can interact.

The registry stores verification status and trust domain membership (`verified`, `identity`, `trust_domain` fields), aligning with the [agentic strategy](https://github.com/solaius/ai-asset-registry/blob/main/docs/knowledge-review/strategy/agentic-strategy.md) Govern & Secure pillar.

### 3.6 Pre-Deployment vs. Post-Deployment

The most structurally significant difference. The agent registry serves two use cases:

1. **Pre-deployment (governance)**: Register agent definitions, manage versions, apply governance tracks, track deployment eligibility. Mirrors the MCP Registry model.
2. **Post-deployment (runtime)**: Discovery plugins detect running instances across environments (kagenti, Docker, Consul, static), register runtime metadata (URL, health, protocol, skills). This is Varsha's proposal.

The relationship is one-to-many: a governed AgentVersion may have zero or more running instances. The registry must link them to answer: "Which definition is this instance based on?" and "How many healthy instances of this approved agent exist?"

---

## 4. Meeting Insights & Decisions

The following decisions and insights are extracted from meeting transcripts spanning March-April 2026.

### 4.1 Agent Registry Ownership Transfer

Varsha Prasad Narsing authored the original post-deployment agent registry proposal (2026-02-16) on her `varshaprasad96/mlflow` branch `spike/gateway`. In the AI asset registries sync (2026-04-07) (transcript was local-only in the old repo; not retained), Varsha raised the agent registry status directly:

> "A few months back, we also had a conversation with databricks on the agent registries pre and post deployment. And then there was a strat created for it, we started working on it, but since we are working towards Summit and that was not slated for Summit, we stopped working."

Peter Double is now taking over agent registry PM ownership, as documented in the [agentic strategy context](https://github.com/solaius/ai-asset-registry/blob/main/docs/knowledge-review/strategy/agentic-strategy.md). The immediate task is to develop Varsha's proposal into a full upstream MLflow RFC, extending it with pre-deployment governance tracks.

### 4.2 Priority and Timeline

Adam Bellusci set clear priority ordering in the Registry Proposal Discussion (2026-03-19) (transcript was local-only in the old repo; not retained):

> "MCP needs to go first because we're going to have the catalog. We need a registry to go along with that. And I think agencies has to be super fast follow."

And in the AI asset registries sync (2026-04-07) (transcript was local-only in the old repo; not retained):

> "My priority is to try to get MCP and Agent registry out concurrently... the 3.5 release sounds like with MLflow doing the skills piece, we might be able to get all three out."

Peter reinforced this in the same meeting: "Agent Registry and MCP registry will be the two top big rocks that would be working on for three five. Jeff has agreed that those will be very, very high priority."

**Decision**: MCP and Agent registry are co-priority for RHOAI 3.5. Skills registry is third, potentially covered by Databricks/MLflow upstream work.

### 4.3 Kagenti Relationship

Varsha noted the kagenti relationship in the 2026-04-07 meeting: "There had been talks with kagenti which is another project... I took a quick look at that, kind of didn't fit much on our pre-deployment part of it."

Peter responded: "I think those people need to be heavily involved to light speed us forward with what they've ran into, and how we might be able to bring in their functionality with this. But... we should be using their knowledge to get what we need in MLflow."

Kagenti is being productized for RHOAI 3.5 Tech Preview. The agent registry must integrate with kagenti's AgentCard and AgentRuntime CRDs as a discovery source, while kagenti's runtime lifecycle management complements the registry's governance lifecycle.

### 4.4 Databricks Collaboration Process

Edson Tirelli provided critical context on the upstream development process in the Registry Proposal Discussion (2026-03-19) (transcript was local-only in the old repo; not retained):

> "Features and development there is quite a bit of analysis and back and forth... it's not a bad thing... but at the same time it takes time to get there."

Key process constraints:
- Design approval takes approximately one month of back-and-forth with Databricks
- Everything must be broken into small, reviewable PRs
- Design documents require detailed requirement lists, API specifications, database changes, and decision matrices
- Databricks is "very interested" in agents and "willing to collaborate" -- the bottleneck is Red Hat's readiness with clear requirements

Edson's characterization of the Databricks collaboration: "The faster we get started the better. And by the way, the only reason we haven't started is because we told them we are not ready for it. So it's on us as soon as we are ready."

### 4.5 IBM/Red Hat Positioning

The Agentic AI pod v2 (2026-04-14) (transcript was local-only in the old repo; not retained) meeting established positioning for joint IBM/Red Hat customer conversations:

- **Red Hat focus**: Agent runtime, lifecycle management, Agent Ops (observability, evaluations, security), MCP Gateway
- **IBM focus**: Agent building, control plane, Watsonx Orchestrate (no-code, business user GUI)

Tushar Katarki emphasized this is strictly for joint customer conversations: "This doesn't mean that we are going to change any of what we are doing with regards to our product roadmap."

**Relevance to agent registry**: The agent registry falls squarely in Red Hat's domain (Deploy & Manage pillar). There is no conflict with IBM positioning here -- IBM is not building an agent registry for Kubernetes/hybrid cloud environments.

### 4.6 Plugin Architecture for MLflow

Peter Double proposed a plugin architecture for MLflow that would allow rapid addition of new AI asset types. In the Sharon/Peter 1:1 (2026-04-13) (transcript was local-only in the old repo; not retained):

> "I've proposed a plugin architecture that will allow for you to rapidly create new AI asset types in MLflow, instead of having to build the whole vertical... Databricks, they're open to it, they want me to rewrite a couple things."

The plugin architecture is essential for the agent registry because it determines how the Agent entity type is introduced into MLflow. Rather than building a bespoke agent registry, the approach is to create a generic asset plugin framework with MCPs, agents, and skills as the first three plugins.

---

## 5. Key People & Ownership

| Person | Agent Registry Role | Notes |
|---|---|---|
| **Peter Double** | Agent registry PM (current owner) | Taking over from Varsha. Responsible for upstream MLflow RFC, RHOAI user stories, and cross-component coordination. |
| **Varsha Prasad Narsing** | Original proposal author | Authored the post-deployment agent registry proposal (2026-02-16). Kagenti contributor. Paused agent registry work during Summit push. |
| **Adam Bellusci** | Leadership, strategic direction | Set the MLflow-for-registries / Kubeflow-for-catalogs decision (2025-12-17). Prioritized MCP + Agent as co-priority for 3.5. |
| **Adel Zaalouk** | Agentic strategy lead | Owns the four-pillar agentic strategy. Agent registry maps to Pillar 3 (Deploy & Manage). Oversees kagenti direction. |
| **Edson Tirelli** | Upstream MLflow liaison | Primary engineering contact with Databricks. Manages design approval process. Confirmed Databricks interest in agent registry. |
| **Matt Prahl** | MLflow engineering, upstream collaboration | Workspace support in MLflow. Provides Red Hat requirements to Databricks via Slack. Will be key for agent registry implementation. |
| **Dan Kuc** | MLflow/Registry engineering | Part of the upstream engineering team. Working on MLflow features with Edson. |
| **Chris Hambridge** | Architecture, downstream engineering | Leading downstream engineering for registry features. Raised need for early architect (Jason, Jessica) engagement. |
| **Emilio Garcia** | Agent relationships and telemetry | Articulated the need for registering agent-component relationships for observability: "How can we differentiate between an agent that you're developing versus the different instances that you've deployed?" (2026-04-07) |
| **Jason / Jessica** | Chief Architects | Decision authority on architectural direction. Chris Hambridge flagged the need for early engagement to avoid late-stage rework. |
| **Jeff Martin Demoss** | Engineering leadership | Agreed that agent registry is "very, very high priority" for 3.5 (per Peter, 2026-04-07). |

---

## 6. Component Boundaries

The agent registry exists within a broader ecosystem of components. Clear boundaries prevent scope creep and ensure each component has a single responsibility.

### 6.1 Agent Registry (MLflow)

**Scope**: Governed identity, versioning, lifecycle management, metadata storage for agent definitions. Stores protocol, skills/capabilities, dependency references, governance state, trust tier, workspace scope. Does not run agents, route requests, or manage workloads.

**Pre-deployment**: The "should" side -- Platform Engineers register definitions, manage versions, apply governance, mark eligible for deployment.

### 6.2 Agent Discovery (MLflow + Plugins)

**Scope**: Runtime discovery of live agent instances. Sources: kagenti (K8s AgentCard CRDs), Docker, Consul, static configs, webhooks. Stores URL, health, runtime state (ACTIVE/UNHEALTHY/STALE/REMOVED), identity claims, timestamps.

**Post-deployment**: The "is" side -- discovery plugins detect running agents and track availability. Discovery results should link to governed registry records, though this linkage requires explicit design.

### 6.3 Agent Catalog (Kubeflow Hub)

**Scope**: Read-only discovery surface for published agents. Reads from registry, displays name, capabilities, protocol, trust tier, version history. Does not store governance state -- consistent with MCP catalog pattern.

### 6.4 MCP Gateway (Envoy-based)

**Scope**: Tool-level routing for MCP servers. Agents invoking MCP tools route through the gateway. Does not route agent-to-agent communication. Registry metadata enables impact analysis ("If I deprecate this MCP server, which agents are affected?").

### 6.5 Kagenti Operator

**Scope**: Kubernetes-native agent lifecycle management via AgentRuntime and AgentCard CRDs, SPIFFE identity injection. Kagenti is the deployment primitive for agents on K8s (analogous to Lifecycle Operator for MCP servers). The kagenti discovery plugin bridges runtime state into MLflow agent discovery.

**RHOAI 3.5 status**: Tech Preview target (Source: [agentic strategy context](https://github.com/solaius/ai-asset-registry/blob/main/docs/knowledge-review/strategy/agentic-strategy.md)).

### 6.6 AAA/Studio (AI Available Assets)

**Scope**: Consumption surface for AI engineers. Queries registry for published, workspace-visible agents. Enables capability browsing and workflow integration -- analogous to MCP server tool selection (MCP Story 8).

### Component Interaction Summary

```
Platform Engineer
    |
    v
[Agent Registry (MLflow)] -- governance truth, pre-deployment
    |           |           |
    v           v           v
[Catalog]   [AAA/Studio]  [AI Gateway]
(Kubeflow)  (consumption)  (routing)
                              |
                              v
                    [Running Agent Instances]
                              ^
                              |
[Agent Discovery (MLflow)] -- runtime truth, post-deployment
    ^           ^           ^
    |           |           |
[kagenti]   [Docker]    [Static]
(K8s)       (plugin)    (plugin)
```

---

## 7. Open Questions

The following items require stakeholder input or further research before the upstream MLflow RFC can be finalized.

### 7.1 Pre-Deployment + Post-Deployment Unification

How should the governance registry and runtime discovery registry relate within MLflow? Options: (a) single `agent_registry` table with both governance and runtime fields, (b) two linked tables (`agent_registry` + `agent_discovery`), (c) extend Varsha's proposal with governance tracks. **Stakeholder needed**: Edson Tirelli, Chris Hambridge, Databricks engineering.

### 7.2 Plugin Architecture Dependency

Agent registry implementation depends on whether the generic asset plugin architecture is approved by Databricks. If not, it must be built as a dedicated feature (like prompts-as-models). **Status**: Proposed to Databricks; revisions requested. Timeline uncertain.

### 7.3 Kagenti Integration Depth

Options: (a) loose coupling -- kagenti as one discovery plugin, no kagenti-specific logic in core, (b) tight coupling -- AgentCard CRD schema informs registry metadata model, (c) downstream-only -- upstream MLflow knows nothing about kagenti, RHOAI adds extensions. **Stakeholder needed**: Adel Zaalouk, Varsha Prasad Narsing.

### 7.4 Agent-to-Agent Relationship Tracking

Should the registry track agent-to-agent dependencies (orchestration, delegation, handoffs)? More complex than skill/MCP dependencies because agents are dynamically discovered and relationships change at runtime. Emilio Garcia raised this (2026-04-07): "How can we differentiate between an agent that you're developing versus the different instances that you've deployed?"

### 7.5 Scope for 3.5 Dev Preview

- **Minimum**: Registration with metadata, version history, publish state, workspace scoping. No runtime discovery.
- **Target**: Minimum plus kagenti discovery source, linking governed records to running instances.
- **Stretch**: Target plus AI Gateway integration for registry-based agent routing.

**Stakeholder needed**: Adam Bellusci, Jeff Martin Demoss.

### 7.6 Agent Definition Format

MCP servers have registry schema. Skills have SKILL.md. What is the canonical agent definition? Options: ResponsesAgent class, A2A AgentCard JSON, new `agent.yaml` schema, framework-specific configs. Registry should be format-agnostic but needs to know what fields to extract for governance and discovery.

### 7.7 IBM Overlap Monitoring

2026-04-14 positioning clarified Red Hat owns agent runtime/lifecycle (including registry), but this is for joint customer conversations only. Monitor whether IBM's Watsonx.governance introduces overlapping agent registry capabilities.

---

## 8. References

### Internal Documents

- [MCP Registry 3.5 DP User Stories](https://github.com/solaius/ai-asset-registry/blob/main/mcps/mcp-registry/mcp-registry-3.5-user-stories.md) -- MCP user stories informing agent story structure
- [Skills Registry User Stories](/features/skills-registry/strategy/user-stories.md) -- upstream/downstream split template
- [Skills RHOAI Patterns and Meetings](/features/skills-registry/research/04-rhoai-patterns-and-meetings.md) -- transferability analysis pattern
- [Agentic Strategy Context](https://github.com/solaius/ai-asset-registry/blob/main/docs/knowledge-review/strategy/agentic-strategy.md) -- four pillars, IBM positioning
- [AI Asset Types](https://github.com/solaius/ai-asset-registry/blob/main/docs/knowledge-review/assets/asset-types.md) -- agent asset type definition, dual-entity challenge
- [Agent Registry Upstream Proposal](/features/agent-registry/strategy/upstream-proposal.md) -- Varsha's post-deployment proposal (local copy)

### Prior Research (This Series)

- [01 - Agent Ecosystem & Terminology](./01-agent-ecosystem.md)
- [02 - Standards and Protocols](./02-standards-and-protocols.md)
- [03 - Kagenti and Kubernetes](./03-kagenti-and-kubernetes.md)
- [04 - Agent Management Landscape](./04-agent-management-landscape.md)

### Meeting Transcripts

- AI Asset Registries Sync (2026-04-07) (transcript was local-only in the old repo; not retained) -- agent registry priority, ownership, Databricks collaboration
- Registry Proposal Discussion (2026-03-19) (transcript was local-only in the old repo; not retained) -- upstream process, priority setting, plugin architecture
- Agentic AI Pod v2 (2026-04-14) (transcript was local-only in the old repo; not retained) -- IBM/Red Hat positioning
- Sharon/Peter 1:1 (2026-04-13) (transcript was local-only in the old repo; not retained) -- plugin architecture proposal to Databricks
- MCP Pipeline w/ gen-mcp (2026-04-10) (transcript was local-only in the old repo; not retained) -- ingestion pipeline pattern

### External Sources

- [Varsha's MLflow Fork (agent-registry proposal)](https://github.com/varshaprasad96/mlflow/blob/spike/gateway/proposals/agent-registry-discovery.md)
- [kagenti](https://kagenti.github.io/.github/) -- Kubernetes agent lifecycle operator
- [A2A Protocol](https://a2a-protocol.org/latest/specification/) -- Agent-to-Agent protocol specification
- [MLflow ResponsesAgent](https://mlflow.org/docs/latest/genai/flavors/responses-agent-intro/) -- MLflow agent abstraction
- [AWS Agent Registry](https://aws.amazon.com/blogs/machine-learning/the-future-of-managing-agents-at-scale-aws-agent-registry-now-in-preview/) -- competitive reference
