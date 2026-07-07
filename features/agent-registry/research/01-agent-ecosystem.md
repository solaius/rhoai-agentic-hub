---
title: Agent Registry Research - Agent Ecosystem & Terminology
description: Defines what "agent" means across the ecosystem and maps the abstraction landscape, building shared vocabulary for the upstream MLflow Agent Registry RFC.
source: ai-asset-registry/agents/agent-registry/research/01-agent-ecosystem.md (as of 2026-07-05)
timestamp: 2026-07-06
review_after: 2026-08-05
---

# Agent Registry Research - Agent Ecosystem & Terminology

**Date**: 2026-04-24
**Author**: Peter Double (Principal PM - MCP & AI Asset Registries)
**Purpose**: Define what "agent" means across the ecosystem, establish terminology, and map the abstraction landscape. This document builds the shared vocabulary for the upstream MLflow Agent Registry RFC and informs the metadata model, lifecycle design, and integration points covered in upcoming documents.

---

## 1. Terminology Map

The term "agent" suffers from even more definitional fragmentation than "skill" or "tool." Every framework, protocol, and platform defines agents differently -- ranging from a Python class with a system prompt to a running Kubernetes workload with cryptographic identity. Before proposing an Agent Registry schema, we must map how each major player uses the term.

| Framework / Protocol | Primary Term | What It Means | Granularity Level | Key Metadata |
|---|---|---|---|---|
| **LangChain / LangGraph** | Agent (graph node) | An LLM wrapped in a stateful directed graph with nodes (agents/tools), edges (transitions), and persistent state. Agents reason, plan, and invoke tools in cycles. | Single LLM + tool loop within a graph | name, model, tools, state schema, graph topology |
| **CrewAI** | Agent (role-based) | An autonomous entity with a role, goal, backstory, and tool access, organized into crews with a process (sequential or hierarchical). Emphasis on team collaboration. | Single autonomous persona | role, goal, backstory, tools, allow_delegation, memory |
| **Microsoft Agent Framework 1.0** | Agent (unified) | The converged abstraction from Semantic Kernel + AutoGen. An agent is an LLM-powered entity with instructions, tools, middleware pipeline, and orchestration capabilities. Ships .NET and Python with native MCP + A2A support. | Single agent or agent team | name, instructions, model, tools, middleware, protocols |
| **OpenAI Agents SDK** | Agent | An LLM equipped with instructions, tools, and optional output_type. Supports agents-as-tools, handoffs between agents, guardrails, and sandbox environments. | Single LLM + tools | name, instructions, model, tools, output_type, handoffs, guardrails |
| **Google ADK** | Agent (3 types) | A self-contained execution unit: LlmAgent (LLM-powered), Workflow Agents (SequentialAgent, ParallelAgent, LoopAgent), or Custom Agents (BaseAgent subclass). Multi-agent by design. | Single agent or agent team | name, description, model, tools, sub_agents, artifacts |
| **IBM BeeAI** | Agent (ACP-based) | A containerized autonomous entity communicating via the Agent Communication Protocol (ACP). Originally BeeAgent, renamed to ReActAgent to acknowledge no single agent design is definitive. | Single containerized agent | name, framework, container image, ACP endpoint, tools |
| **AutoGen / AG2** | ConversableAgent | An agent that participates in structured conversations (group chats, swarms, nested chats). The fundamental building block is message exchange between agents. AG2 is the community fork; Microsoft AutoGen v0.4+ merged into Agent Framework 1.0. | Single conversational agent | name, system_message, llm_config, tools, code_execution |
| **A2A Protocol** | Agent (via AgentCard) | A deployed service described by an AgentCard -- a JSON metadata document listing capabilities (skills), supported protocols, security schemes, and provider information. Discovered at `/.well-known/agent-card.json`. | Running service with capabilities | name, description, version, skills, capabilities, security, provider, interfaces |
| **AWS Agent Registry** | Agent (registry record) | A registered resource in a governed catalog. Agents are metadata records validated against protocol schemas (A2A, MCP), with approval workflows and semantic search. | Registry record (any environment) | name, description, protocol, metadata, approval_status, publisher |
| **MLflow** | ChatAgent / ResponsesAgent | A Python class subclassing `ResponsesAgent` (or legacy `ChatAgent`) with a `predict` method. Framework-agnostic wrapper that integrates with MLflow logging, tracing, and serving. No dedicated agent registry exists yet. | Deployable model artifact | name, model_signature, task, custom_inputs, tracing |
| **Anthropic / MCP** | (no agent abstraction) | MCP defines the protocol between hosts and servers for tool/resource/prompt access. MCP does not define agents -- it provides the plumbing agents use to access tools. Anthropic's Claude Managed Agents is a separate hosted runtime. | Protocol layer (below agents) | server capabilities, tools, resources, prompts, transport |
| **kagenti (Red Hat)** | AgentRuntime + AgentCard | A Kubernetes workload (Deployment/StatefulSet) declared as an agent via the AgentRuntime CRD, with capabilities described in an AgentCard CRD. SPIFFE identity injection, A2A protocol support, zero-trust networking via Istio Ambient. | Kubernetes workload + metadata CRD | AgentRuntime (workload binding, phase, config), AgentCard (capabilities, endpoints, identity) |

**Sources**: LangGraph docs ([langchain.com/langgraph](https://www.langchain.com/langgraph), April 2026); CrewAI docs ([docs.crewai.com](https://docs.crewai.com/en/introduction), April 2026); Microsoft Agent Framework 1.0 announcement ([devblogs.microsoft.com](https://devblogs.microsoft.com/agent-framework/microsoft-agent-framework-version-1-0/), April 3, 2026); OpenAI Agents SDK ([openai.github.io/openai-agents-python](https://openai.github.io/openai-agents-python/agents/), April 2026); Google ADK ([adk.dev/agents](https://adk.dev/agents/), April 2026); IBM BeeAI ([github.com/i-am-bee/beeai-framework](https://github.com/i-am-bee/beeai-framework), April 2026); AG2 ([github.com/ag2ai/ag2](https://github.com/ag2ai/ag2), April 2026); A2A Protocol ([a2a-protocol.org/latest/specification](https://a2a-protocol.org/latest/specification/), April 2026); AWS Agent Registry ([aws.amazon.com/blogs/machine-learning](https://aws.amazon.com/blogs/machine-learning/the-future-of-managing-agents-at-scale-aws-agent-registry-now-in-preview/), April 2026); MLflow ResponsesAgent ([mlflow.org/docs/latest/genai/flavors/responses-agent-intro](https://mlflow.org/docs/latest/genai/flavors/responses-agent-intro/), April 2026); MCP Specification ([modelcontextprotocol.io/specification](https://modelcontextprotocol.io/specification/2025-11-25), 2025-11-25); kagenti ([kagenti.github.io](https://kagenti.github.io/.github/), March 2026).

### Key Insight: "Agent" Spans Three Distinct Meanings

The table above reveals that "agent" is used at three fundamentally different levels:

1. **Agent-as-code**: A Python/C# class with a system prompt, tools, and a predict/run method (LangGraph, CrewAI, OpenAI Agents SDK, MLflow). This is a development artifact -- source code that can be versioned, tested, and packaged.

2. **Agent-as-service**: A deployed, running process reachable via a network URL, described by an AgentCard or equivalent metadata (A2A, kagenti, AWS Agent Registry). This is a runtime entity with lifecycle state.

3. **Agent-as-record**: A metadata entry in a governed catalog with approval workflows, compliance status, and discovery capabilities (AWS Agent Registry, IBM watsonx.governance). This is a governance artifact.

An Agent Registry must accommodate all three meanings, or clearly scope which it addresses. The upstream MLflow proposal from Varsha Prasad Narsing explicitly chose meaning #2 (post-deployment services). The full registry needs all three.

---

## 2. The Agent Abstraction Ladder

Building on the [Skills Ecosystem Research](/features/skills-registry/research/01-skills-ecosystem.md) abstraction ladder for tools and skills, agents sit at the top of a broader hierarchy:

```
Agent (autonomous system with goals, reasoning, and tool use)
  |
  |-- Skills / Capabilities (what the agent can do -- A2A AgentSkill level)
  |     |
  |     |-- Plugins / Tool Groups (named collections of related functions)
  |     |     |
  |     |     |-- Tools / Functions (atomic callable units)
  |     |     |     |
  |     |     |     |-- MCP Tools (protocol-level tool definitions)
  |     |     |
  |     |     |-- Prompts (reusable prompt templates)
  |     |
  |     |-- Models (LLMs the agent uses for reasoning)
  |     |
  |     |-- Knowledge Sources (RAG, documents, databases)
  |
  |-- Guardrails (safety boundaries, input/output validation)
  |
  |-- Identity & Trust (SPIFFE, JWS signatures, trust domains)
```

### How Frameworks Map to This Ladder

Different frameworks enter the ladder at different levels and decompose it differently:

| Framework | Top-Level Unit | Decomposes Into | Missing Layers |
|---|---|---|---|
| **LangGraph** | Agent (graph) | Nodes (tools, LLM calls), Edges (transitions), State | No formal skill/capability abstraction |
| **CrewAI** | Crew (team) | Agents (roles) -> Tools | No formal skill abstraction; tools are flat |
| **OpenAI Agents SDK** | Agent | Tools (5 types), Handoffs, Guardrails | No plugin/skill grouping |
| **Google ADK** | Agent (LlmAgent) | Sub-agents, Tools, Plugins, Artifacts | Rich hierarchy but Google-specific |
| **A2A Protocol** | AgentCard | Skills (structured metadata) | Skills lack parameter schemas |
| **Microsoft Agent Framework 1.0** | Agent | Tools (MCP), Plugins (SK), Middleware | Inherits Semantic Kernel plugin model |
| **MCP** | Server | Tools, Resources, Prompts | Below agent level entirely |
| **kagenti** | AgentRuntime | AgentCard (capabilities), MCP servers (tools) | Clear separation of runtime vs. metadata |

### The Composition Gap

No framework provides a complete, standardized way to describe the full agent composition hierarchy. An AgentCard lists skills but not the tools within each skill. MCP describes tools but not which agent uses them. MLflow tracks model artifacts but not agent topology. This is the gap an Agent Registry must fill -- linking the agent to its constituent skills, tools, models, and guardrails as governed, versioned relationships.

---

## 3. Pre-Deployment vs. Post-Deployment Agents

The most fundamental design question for an Agent Registry is whether it governs agent *definitions* (pre-deployment), agent *instances* (post-deployment), or both. The answer shapes every subsequent design decision -- data model, lifecycle states, discovery mechanisms, and integration points.

### The Container Analogy

| Concept | Container World | Agent World (Pre-Deployment) | Agent World (Post-Deployment) |
|---|---|---|---|
| **Definition** | Dockerfile | Agent code + config (LangGraph graph, CrewAI crew YAML, ResponsesAgent class) | -- |
| **Packaged artifact** | Container image (OCI) | Agent artifact (MLflow model, OCI image, Python package) | -- |
| **Registry** | Container registry (Quay, ECR) | Agent artifact registry (MLflow Model Registry, OCI registry) | Agent service registry (A2A discovery, kagenti AgentCard CRD) |
| **Running instance** | Container (pod) | -- | Agent service (A2A endpoint, K8s workload) |
| **Lifecycle states** | image: tagged, signed, scanned / container: running, stopped, crashed | draft, approved, certified, deprecated, archived | ACTIVE, UNHEALTHY, STALE, REMOVED |
| **Discovery** | Image tags, labels, vulnerability scans | Version history, approval status, certification tier | Health checks, `.well-known/agent-card.json`, watch/poll |
| **Identity** | Image digest, signature (cosign) | Version hash, provenance attestation | SPIFFE ID, JWS-signed AgentCard |

### The Model Analogy

MLflow's existing Model Registry already handles this duality for models:

- **Pre-deployment**: Model versions with stages (None -> Staging -> Production -> Archived), lineage tracking, evaluation metrics, artifact storage
- **Post-deployment**: Model serving endpoints with health monitoring, traffic splitting, A/B testing

The Agent Registry needs the same two-track approach, but agents are more complex than models because they compose multiple assets (models, tools, prompts, guardrails, knowledge sources) and have richer runtime behavior (multi-turn state, tool calling, agent-to-agent delegation).

### Where Each Player Focuses

| Platform / Framework | Pre-Deployment | Post-Deployment | Both |
|---|---|---|---|
| **MLflow (current)** | Model Registry, Prompt Registry | Model Serving | Models only, no agent-specific support |
| **MLflow (proposed)** | -- | Agent Registry (Varsha's proposal) | Agent definitions deferred |
| **AWS Agent Registry** | -- | -- | Metadata records spanning both |
| **IBM watsonx.governance** | Factsheets, approval workflows | Agent Monitoring & Insights (Q1 2026) | Unified governance |
| **kagenti** | -- | AgentRuntime + AgentCard CRDs | Runtime-focused |
| **A2A Protocol** | -- | AgentCard discovery | Runtime discovery only |
| **LangGraph / CrewAI / etc.** | Code-level definitions | -- | Development-focused |

### What the MLflow RFC Needs

The upstream MLflow Agent Registry RFC should address both tracks:

1. **Pre-deployment**: Agent definitions as versioned artifacts with governance metadata (approval, certification, trust tier), composition tracking (which models, tools, prompts, guardrails does this agent use?), and evaluation results.

2. **Post-deployment**: Live agent discovery via pluggable providers (the core of Varsha's proposal), health monitoring, runtime state tracking, and identity verification.

The two tracks connect through a *deployment link* -- an agent definition (pre-deployment artifact) is deployed to become an agent service (post-deployment instance), and the registry maintains this relationship.

---

## 4. Agent Composition Patterns

Agents in production rarely operate in isolation. Understanding composition patterns is essential because the Agent Registry must model not just individual agents but how they relate to each other.

### 4.1 Single Agent

The simplest pattern: one agent with tools, a model, and instructions.

```
[User] --> [Agent] --> [Tools/MCP Servers]
                  --> [Model (LLM)]
```

**Used by**: All frameworks for simple use cases. MLflow's ResponsesAgent wraps a single agent.

**Registry implication**: One agent record with references to its tools, model, and configuration.

### 4.2 Multi-Agent Teams (Peer Collaboration)

Multiple agents collaborate as peers, coordinating through shared state or message passing.

```
[User] --> [Agent A (Researcher)] <--> [Agent B (Writer)]
                                  <--> [Agent C (Reviewer)]
```

**Used by**: CrewAI (crews with sequential/hierarchical processes), AG2 (group chats), Google ADK (SequentialAgent, ParallelAgent).

**Registry implication**: Each agent registered individually, plus a "team" or "crew" record describing the composition and orchestration pattern.

### 4.3 Hierarchical Delegation (Manager Pattern)

A manager agent delegates subtasks to specialist agents, which report results back.

```
[User] --> [Manager Agent]
              |-- delegates to --> [Specialist A]
              |-- delegates to --> [Specialist B]
              |-- delegates to --> [Specialist C]
```

**Used by**: OpenAI Agents SDK (agents-as-tools), CrewAI (hierarchical process with Manager Agent), Anthropic (Agent Teams with lead agent).

**Registry implication**: Parent-child relationships between agent records. The manager agent's metadata references its delegate agents.

### 4.4 Agent-as-Tool

An agent is exposed as a callable tool to another agent, flattening the hierarchy.

```python
# OpenAI Agents SDK pattern
research_agent = Agent(name="researcher", tools=[web_search])
main_agent = Agent(
    name="coordinator",
    tools=[research_agent.as_tool()]
)
```

**Used by**: OpenAI Agents SDK (agent.as_tool()), LangGraph (nested graph nodes), Microsoft Agent Framework 1.0.

**Registry implication**: Cross-referencing between agent records and tool records. An agent can appear as both an agent and a tool in the registry.

### 4.5 A2A Delegation (Protocol-Based)

Agents discover and invoke each other via the A2A protocol, using AgentCards for capability discovery and JSON-RPC for task execution.

```
[Agent A] --discovers--> /.well-known/agent-card.json
          --delegates--> [Agent B via A2A]
          <--results---- [Agent B]
```

**Used by**: A2A-compatible frameworks (kagenti, Google ADK, Microsoft Agent Framework 1.0, BeeAI). Framework-agnostic -- agents can be built with different frameworks.

**Registry implication**: The registry becomes the discovery layer. Agents query the registry to find other agents by skill, protocol, trust domain, or metadata instead of relying on `.well-known` URLs.

### 4.6 Handoff Chains

An agent explicitly transfers control to another agent mid-conversation, passing along conversation context.

```
[User] --> [Triage Agent] --handoff--> [Billing Agent]
                          --handoff--> [Technical Agent]
```

**Used by**: OpenAI Agents SDK (handoffs), Google ADK (agent transfer).

**Registry implication**: Handoff relationships are runtime-determined but can be pre-configured. The registry should capture which agents are eligible handoff targets for a given agent.

### 4.7 Summary: Composition Pattern Requirements

| Pattern | Relationship Type | Registry Must Track |
|---|---|---|
| Single agent | Agent -> Tools, Model | Asset references |
| Multi-agent team | Agent <-> Agent (peer) | Team membership, orchestration pattern |
| Hierarchical delegation | Agent -> Agent (parent-child) | Delegation hierarchy |
| Agent-as-tool | Agent = Tool | Dual registration (agent + tool) |
| A2A delegation | Agent -> Agent (protocol) | Protocol, endpoint, skills |
| Handoff chains | Agent -> Agent (transfer) | Handoff eligibility, context sharing |

---

## 5. Agent Metadata Comparison

To design the Agent Registry schema, we must compare how existing platforms describe agents. The following matrix compares metadata fields across the most relevant systems.

### 5.1 Field-by-Field Comparison

| Metadata Field | A2A AgentCard | kagenti CRD | AWS Agent Registry | IBM watsonx | MLflow ResponsesAgent | Varsha's Proposal |
|---|---|---|---|---|---|---|
| **Name** | name (required) | metadata.name | record name | asset name | model name | name (required) |
| **Description** | description (required) | spec.description | record description | factsheet description | -- | description |
| **Version** | version (required) | metadata.resourceVersion | -- | factsheet version | model version | version |
| **Endpoint URL** | url (required) | status.endpoint | discovery URL | -- | serving endpoint | url (required) |
| **External URL** | -- | -- | -- | -- | -- | external_url |
| **Protocol** | supportedInterfaces | A2A (implicit) | MCP, A2A, custom | -- | Responses API | protocol (enum) |
| **Skills/Capabilities** | skills[] (required) | spec.capabilities | resource capabilities | -- | -- | skills[] (AgentSkill) |
| **Provider** | provider (org, URL) | -- | publisher | -- | -- | -- |
| **Documentation** | documentationUrl | -- | -- | documentation link | -- | -- |
| **Security Schemes** | securitySchemes | SPIFFE identity | IAM, JWT | IAM integration | -- | -- |
| **Security Requirements** | securityRequirements | -- | authorization config | compliance metadata | -- | -- |
| **Identity (crypto)** | signatures (JWS) | SPIFFE ID via AuthBridge | -- | -- | -- | verified, identity |
| **Trust Domain** | -- | spec.trustDomain | -- | -- | -- | trust_domain |
| **Input/Output Modes** | defaultInputModes, defaultOutputModes | -- | -- | -- | ResponsesAgentRequest/Response schemas | -- |
| **Health Status** | -- | status.phase | -- | monitoring alerts | serving endpoint health | status (ACTIVE/UNHEALTHY/STALE/REMOVED) |
| **Health Check Path** | -- | -- | -- | -- | -- | health_check_path |
| **Lifecycle State** | -- | status.conditions | approval status (DRAFT/APPROVED/DEPRECATED) | lifecycle stage | model stage | status |
| **Source/Discovery Plugin** | -- | -- | -- | -- | -- | source_plugin |
| **Framework** | -- | framework-neutral | framework-neutral | -- | framework-agnostic | -- |
| **Tags/Labels** | skills[].tags | metadata.labels | custom metadata | tags | tags | metadata (dict) |
| **Icon** | iconUrl | -- | -- | -- | -- | -- |
| **Timestamps** | -- | K8s timestamps | record timestamps | factsheet dates | model timestamps | last_seen_at, created_at, updated_at |
| **Custom Metadata** | extensions | metadata.annotations | custom schemas | custom attributes | custom_inputs | metadata (dict) |

**Sources**: A2A AgentCard specification ([a2a-protocol.org/latest/specification](https://a2a-protocol.org/latest/specification/)); kagenti CRDs ([next.redhat.com](https://next.redhat.com/2026/03/05/zero-trust-ai-agents-on-kubernetes-what-i-learned-deploying-multi-agent-systems-on-kagenti/), March 2026); AWS Agent Registry ([docs.aws.amazon.com](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/registry.html), April 2026); IBM watsonx.governance ([ibm.com/products/watsonx-governance](https://www.ibm.com/products/watsonx-governance), 2026); MLflow ResponsesAgent ([mlflow.org/docs/latest](https://mlflow.org/docs/latest/genai/flavors/responses-agent-intro/)); Varsha's proposal ([agents/agent-registry-upstream-proposal.md](/features/agent-registry/strategy/upstream-proposal.md)).

### 5.2 Coverage Analysis

**Well-covered fields** (4+ systems agree):
- Name, description, version -- universal identity fields
- Endpoint URL -- required for post-deployment discovery
- Skills/capabilities -- present in A2A, kagenti, AWS, and Varsha's proposal

**Partially covered fields** (2-3 systems):
- Protocol (A2A, Varsha's proposal, AWS)
- Security/identity (A2A, kagenti, Varsha's proposal)
- Lifecycle state (AWS, Varsha's proposal, IBM)
- Provider/publisher (A2A, AWS)

**Unique to specific systems**:
- Trust domain (kagenti, Varsha's proposal) -- important for enterprise multi-tenancy
- Source plugin (Varsha's proposal) -- supports pluggable discovery
- External URL (Varsha's proposal) -- separates internal and external endpoints
- JWS signatures (A2A) -- cryptographic integrity for AgentCards
- Factsheets (IBM) -- rich governance metadata capture

### 5.3 The A2A AgentCard as De Facto Standard

The A2A AgentCard is emerging as the de facto standard for agent metadata. Key indicators:

- **AWS Agent Registry** validates agent records against the A2A schema ([AWS announcement](https://aws.amazon.com/about-aws/whats-new/2026/04/aws-agent-registry-in-agentcore-preview/), April 2026)
- **kagenti** uses A2A AgentCard as the source of truth for agent capabilities ([kagenti docs](https://kagenti.github.io/.github/), 2026)
- **Microsoft Agent Framework 1.0** ships with native A2A support ([devblogs.microsoft.com](https://devblogs.microsoft.com/agent-framework/microsoft-agent-framework-version-1-0/), April 2026)
- **Google ADK** is the reference A2A implementation ([adk.dev](https://adk.dev/agents/), 2026)
- **IBM BeeAI** supports A2A interoperability ([github.com/i-am-bee/beeai-framework](https://github.com/i-am-bee/beeai-framework), 2026)
- Both MCP and A2A are now governed by the **Agentic AI Foundation (AAIF)** under the Linux Foundation ([anthropic.com](https://www.anthropic.com/news/donating-the-model-context-protocol-and-establishing-of-the-agentic-ai-foundation), December 2025)

The MLflow Agent Registry should align with the AgentCard schema where possible, extending it for governance fields (lifecycle state, approval, certification, trust tier) that A2A does not cover.

---

## 6. Implications for the Agent Registry

Synthesizing the analysis above, the following requirements emerge for the upstream MLflow Agent Registry.

### 6.1 The Registry Must Support Three Agent Representations

1. **Agent Definition** (pre-deployment): A versioned, governed artifact describing what the agent is, what it composes (models, tools, prompts, guardrails), and how it should be configured. Analogous to a container image in a container registry.

2. **Agent Instance** (post-deployment): A live, running agent service with a network endpoint, health state, and runtime metadata. Analogous to a running container discovered by a service mesh.

3. **Agent Record** (governance): A metadata entry linking definitions to instances with approval status, certification tier, compliance information, and audit trail. Analogous to a governed entry in a software catalog.

Varsha's proposal addresses #2 (post-deployment). The full registry needs all three, connected through deployment relationships.

### 6.2 Agent Metadata Schema Must Be A2A-Aligned

The AgentCard schema from the A2A protocol is the strongest candidate for the base metadata model. The MLflow Agent Registry should:

- Use A2A AgentCard fields as the core schema (name, description, version, skills, capabilities, provider, interfaces, security)
- Extend with governance fields (lifecycle_state, approval_status, certification_tier, trust_domain, evaluation_results)
- Extend with composition fields (referenced_models, referenced_tools, referenced_prompts, referenced_guardrails)
- Extend with deployment fields (source_plugin, health_status, last_seen_at, deployment_link)
- Support custom metadata via an extensible key-value mechanism

### 6.3 Composition Tracking Is Essential

Unlike models or prompts, agents are inherently composite. The registry must track:

- Which models an agent uses (and which versions)
- Which tools/MCP servers an agent has access to
- Which prompts are embedded in the agent's configuration
- Which guardrails are applied to the agent's inputs and outputs
- Which other agents this agent can delegate to or hand off to
- Which knowledge sources the agent can access

This composition graph is the unique value proposition of an Agent Registry versus a simple service directory.

### 6.4 Lifecycle Must Span Both Pre-Deployment and Post-Deployment

**Pre-deployment lifecycle** (governance track):
```
DRAFT -> REVIEW -> APPROVED -> CERTIFIED -> DEPRECATED -> ARCHIVED
```

**Post-deployment lifecycle** (runtime track):
```
DISCOVERED -> ACTIVE -> UNHEALTHY -> STALE -> REMOVED
```

The two tracks are connected: only APPROVED or CERTIFIED agent definitions should be deployable (policy-enforced), and DEPRECATED definitions should trigger alerts on their running instances.

### 6.5 Discovery Must Be Pluggable and Protocol-Aware

Following Varsha's proposal, the registry should support pluggable discovery providers:

- **Kubernetes** (via kagenti AgentCard CRDs)
- **A2A well-known** (via `/.well-known/agent-card.json` endpoint discovery)
- **Static configuration** (for manually registered agents)
- **Cloud-specific** (AWS, Azure, GCP agent services)

Discovery should be protocol-aware, supporting at minimum:
- **A2A** (agent-to-agent communication)
- **OpenAI-compatible** (chat completions / responses API)
- **Custom** (extensible for framework-specific protocols)

### 6.6 Identity and Trust Are First-Class Concerns

Enterprise agent deployments require:

- **Cryptographic identity**: SPIFFE IDs (kagenti), JWS-signed AgentCards (A2A), or equivalent
- **Trust domains**: Organizational boundaries for filtering agent visibility
- **Verification status**: Whether an agent's identity has been cryptographically verified
- **Certification tiers**: Red Hat certified, partner, community, untrusted (mirroring the MCP Registry trust model)

### 6.7 The Registry Must Be Framework-Agnostic

The terminology map in Section 1 shows that agents are built with LangGraph, CrewAI, OpenAI Agents SDK, Google ADK, Microsoft Agent Framework, BeeAI, and many other tools. The registry must not favor any specific framework. The MLflow ResponsesAgent wrapper pattern is instructive here -- it provides a framework-agnostic interface that any agent framework can implement.

### 6.8 Relationship to Existing MLflow Registries

The Agent Registry should complement, not replace, existing MLflow registries:

| Registry | What It Stores | Relationship to Agent Registry |
|---|---|---|
| **Model Registry** | Model versions, stages, metrics | Agent records reference model versions |
| **Prompt Registry** | Prompt templates, versions | Agent records reference prompt versions |
| **Agent Registry** (new) | Agent definitions + live agents | Composes models, prompts, tools, guardrails |

This aligns with the broader AI Asset Registry vision where each asset type has its own registry but cross-references are maintained.

---

## 7. References

### Standards & Protocols

- A2A Protocol Specification: [a2a-protocol.org/latest/specification](https://a2a-protocol.org/latest/specification/)
- A2A Protocol GitHub: [github.com/a2aproject/A2A](https://github.com/a2aproject/A2A)
- AgentCard Concepts: [agent2agent.info/docs/concepts/agentcard](https://agent2agent.info/docs/concepts/agentcard/)
- MCP Specification (2025-11-25): [modelcontextprotocol.io/specification/2025-11-25](https://modelcontextprotocol.io/specification/2025-11-25)
- MCP GitHub: [github.com/modelcontextprotocol/modelcontextprotocol](https://github.com/modelcontextprotocol/modelcontextprotocol)
- Agentic AI Foundation (AAIF) Announcement: [anthropic.com/news/donating-the-model-context-protocol-and-establishing-of-the-agentic-ai-foundation](https://www.anthropic.com/news/donating-the-model-context-protocol-and-establishing-of-the-agentic-ai-foundation)

### Agent Frameworks

- LangGraph: [langchain.com/langgraph](https://www.langchain.com/langgraph)
- LangGraph Documentation: [docs.langchain.com/oss/python/langgraph/overview](https://docs.langchain.com/oss/python/langgraph/overview)
- CrewAI: [docs.crewai.com/en/introduction](https://docs.crewai.com/en/introduction)
- CrewAI GitHub: [github.com/crewaiinc/crewai](https://github.com/crewaiinc/crewai)
- Microsoft Agent Framework 1.0: [devblogs.microsoft.com/agent-framework/microsoft-agent-framework-version-1-0](https://devblogs.microsoft.com/agent-framework/microsoft-agent-framework-version-1-0/)
- Microsoft Agent Framework Overview: [learn.microsoft.com/en-us/agent-framework/overview](https://learn.microsoft.com/en-us/agent-framework/overview/)
- OpenAI Agents SDK: [openai.github.io/openai-agents-python](https://openai.github.io/openai-agents-python/)
- OpenAI Agents SDK Docs: [openai.github.io/openai-agents-python/agents](https://openai.github.io/openai-agents-python/agents/)
- Google ADK: [adk.dev](https://adk.dev/)
- Google ADK Agents: [adk.dev/agents](https://adk.dev/agents/)
- IBM BeeAI Framework: [github.com/i-am-bee/beeai-framework](https://github.com/i-am-bee/beeai-framework)
- BeeAI Platform: [beeai.dev](https://beeai.dev/)
- AG2 (formerly AutoGen): [github.com/ag2ai/ag2](https://github.com/ag2ai/ag2)
- Microsoft AutoGen: [github.com/microsoft/autogen](https://github.com/microsoft/autogen)
- Anthropic Claude Code: [code.claude.com/docs/en/overview](https://code.claude.com/docs/en/overview)
- Anthropic Claude Managed Agents: [anthropic.com/product/claude-code](https://www.anthropic.com/product/claude-code)

### Enterprise Platforms

- AWS Agent Registry (Preview): [aws.amazon.com/about-aws/whats-new/2026/04/aws-agent-registry-in-agentcore-preview](https://aws.amazon.com/about-aws/whats-new/2026/04/aws-agent-registry-in-agentcore-preview/)
- AWS Agent Registry Blog: [aws.amazon.com/blogs/machine-learning/the-future-of-managing-agents-at-scale-aws-agent-registry-now-in-preview](https://aws.amazon.com/blogs/machine-learning/the-future-of-managing-agents-at-scale-aws-agent-registry-now-in-preview/)
- AWS Agent Registry Documentation: [docs.aws.amazon.com/bedrock-agentcore/latest/devguide/registry.html](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/registry.html)
- AWS A2A Agent Registry on AWS (open source): [github.com/awslabs/a2a-agent-registry-on-aws](https://github.com/awslabs/a2a-agent-registry-on-aws)
- IBM watsonx.governance: [ibm.com/products/watsonx-governance](https://www.ibm.com/products/watsonx-governance)

### Kubernetes & Red Hat

- kagenti: [kagenti.github.io/.github](https://kagenti.github.io/.github/)
- kagenti GitHub: [github.com/kagenti](https://github.com/kagenti)
- kagenti Zero-Trust Blog: [next.redhat.com/2026/03/05/zero-trust-ai-agents-on-kubernetes-what-i-learned-deploying-multi-agent-systems-on-kagenti](https://next.redhat.com/2026/03/05/zero-trust-ai-agents-on-kubernetes-what-i-learned-deploying-multi-agent-systems-on-kagenti/)
- Kubernetes Agent Sandbox: [github.com/kubernetes-sigs/agent-sandbox](https://github.com/kubernetes-sigs/agent-sandbox)
- Kubernetes Agent Sandbox Blog: [kubernetes.io/blog/2026/03/20/running-agents-on-kubernetes-with-agent-sandbox](https://kubernetes.io/blog/2026/03/20/running-agents-on-kubernetes-with-agent-sandbox/)

### MLflow

- MLflow ResponsesAgent: [mlflow.org/docs/latest/genai/flavors/responses-agent-intro](https://mlflow.org/docs/latest/genai/flavors/responses-agent-intro/)
- MLflow ChatAgent Guide: [mlflow.org/docs/latest/genai/flavors/chat-model-guide](https://mlflow.org/docs/latest/genai/flavors/chat-model-guide/)
- Varsha's Agent Registry Proposal: [agents/agent-registry-upstream-proposal.md](/features/agent-registry/strategy/upstream-proposal.md)

### Internal References

- Skills Ecosystem Research: [skills/skills-registry/research/01-skills-ecosystem.md](/features/skills-registry/research/01-skills-ecosystem.md)
- AI Asset Types: [docs/knowledge-review/assets/asset-types.md](https://github.com/solaius/ai-asset-registry/blob/main/docs/knowledge-review/assets/asset-types.md)
- Knowledge Registry: [docs/knowledge-registry.md](https://github.com/solaius/ai-asset-registry/blob/main/docs/knowledge-registry.md)
