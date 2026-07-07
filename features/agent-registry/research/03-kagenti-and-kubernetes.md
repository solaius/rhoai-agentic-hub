---
title: Agent Registry Research - Kagenti & Kubernetes Agent Patterns
description: The Kubernetes agent landscape with deep focus on kagenti as the RHOAI runtime discovery partner, disambiguated from similarly-named projects.
source: ai-asset-registry/agents/agent-registry/research/03-kagenti-and-kubernetes.md (as of 2026-07-05)
timestamp: 2026-07-06
review_after: 2026-08-05
---

# Agent Registry Research - Kagenti & Kubernetes Agent Patterns

**Date**: 2026-04-24
**Author**: Peter Double (Principal PM - MCP & AI Asset Registries)
**Purpose**: Document the Kubernetes agent landscape with deep focus on kagenti as the RHOAI runtime discovery partner. Disambiguate kagenti from similarly-named projects.

---

## 1. Three Projects, Three Purposes

Three projects -- kagenti, kagent, and agent-sandbox -- occupy overlapping Kubernetes territory but solve fundamentally different problems. Conflating them leads to incorrect architectural assumptions about what the MLflow Agent Registry needs from its Kubernetes integration.

| Dimension | **kagenti** | **kagent** | **agent-sandbox** |
|---|---|---|---|
| **Organization** | Red Hat (kagenti GitHub org) | Solo.io (kagent-dev GitHub org) | kubernetes-sigs (SIG Apps) |
| **Purpose** | Agent control plane: deploy, secure, govern agents on K8s | DevOps/platform agent framework on K8s | Isolated execution sandboxes for agent runtimes |
| **Focus** | Enterprise security, identity, governance | Cloud-native operations automation | Workload isolation and stateful execution |
| **CNCF/K8s Status** | Red Hat incubation project | CNCF Sandbox (accepted May 2025) | SIG Apps subproject |
| **Primary CRD** | AgentCard (with targetRef) | Agent, ToolServer (now via kmcp) | Sandbox, SandboxTemplate, SandboxClaim |
| **Protocol** | A2A native, MCP for tools | A2A, MCP for tools | Protocol-agnostic (runtime isolation) |
| **Identity Model** | SPIFFE/SPIRE cryptographic identity | Kubernetes-native identity | Kubernetes pod identity |
| **Agent Framework** | Framework-agnostic (LangGraph, CrewAI, AG2) | Google ADK (default), Go ADK | Framework-agnostic (runtime environment) |
| **License** | Apache 2.0 | Apache 2.0 | Apache 2.0 |
| **GitHub Stars** | ~110 | ~4,000+ | ~1,900 |

([kagenti GitHub org](https://github.com/kagenti); [kagent-dev/kagent GitHub](https://github.com/kagent-dev/kagent); [kubernetes-sigs/agent-sandbox GitHub](https://github.com/kubernetes-sigs/agent-sandbox))

All three operate on Kubernetes, all three deal with AI agents, and "kagenti" and "kagent" differ by a single letter. But their scopes are complementary, not competing:

- **kagenti** answers: "How do I securely deploy, discover, and govern agents across my enterprise Kubernetes clusters?"
- **kagent** answers: "How do I build AI agents that automate cloud-native operations like debugging Istio routes or analyzing Prometheus alerts?"
- **agent-sandbox** answers: "How do I provide isolated, stateful execution environments for agents that need to run untrusted code?"

For the MLflow Agent Registry, kagenti is the primary integration partner -- it provides the Kubernetes-native discovery mechanism that feeds agent metadata into the registry. Kagent is a potential secondary discovery source with a different CRD format. Agent-sandbox is a runtime concern that the registry does not directly integrate with but may reference as an execution environment.

---

## 2. Kagenti Architecture Deep Dive

Kagenti is a Kubernetes-based control plane for AI agents, developed as a Red Hat incubation project. It provides a framework-neutral, scalable, and secure platform for deploying and orchestrating AI agents through standardized agent communication protocols (A2A, MCP). Kagenti is planned for inclusion in Red Hat OpenShift AI in the second half of 2026, making it the primary Kubernetes runtime partner for the Agent Registry ([kagenti project site](https://kagenti.github.io/.github/), 2026).

### 2.1 Core Components

The kagenti platform is organized around four architectural pillars, each supported by dedicated sub-projects:

| Component | Repository | Language | Purpose |
|---|---|---|---|
| **kagenti-operator** | [kagenti/kagenti-operator](https://github.com/kagenti/kagenti-operator) | Go | Kubernetes operator for agent lifecycle management, AgentCard discovery, signature verification, and network policy enforcement |
| **MCP Gateway** | [Kuadrant/mcp-gateway](https://github.com/Kuadrant/mcp-gateway) | Go | Envoy-based gateway for routing MCP tool calls, protocol translation, and tool governance |
| **agentic-control-plane** | [kagenti/agentic-control-plane](https://github.com/kagenti/agentic-control-plane) | Python | Control plane composed of specialized A2A agents coordinated through kagenti CRDs |
| **kagenti-extensions** | [kagenti/kagenti-extensions](https://github.com/kagenti/kagenti-extensions) | Go | Security extensions for zero-trust agent authentication (AuthBridge) |

Additional sub-projects include **plugins-adapter** (Python; security/safety plugins for MCP Gateway), **onecli** (TypeScript; credential vault for agents), and **workload-harness** (Python; agent load generation). The platform also includes a web-based operational interface (React + FastAPI) and Ansible-automated deployment for OpenShift, upstream Kubernetes, or Kind ([kagenti GitHub org](https://github.com/kagenti), April 2026).

### 2.2 AgentCard CRD Specification

The AgentCard is the central custom resource definition in kagenti. It discovers, indexes, and verifies agent metadata for Kubernetes-native agent discovery. The AgentCard CRD was introduced to replace the legacy Component/Agent CRD, aligning kagenti with A2A's standard metadata format.

#### Key Fields

| Field | Location | Description |
|---|---|---|
| `spec.targetRef` | Spec | Reference to the Kubernetes workload (Deployment or StatefulSet) that the agent runs in. Contains `apiVersion`, `kind`, and `name`. |
| `status.agentCardJSON` | Status | The synced A2A AgentCard JSON, fetched from the agent's `/.well-known/agent-card.json` endpoint. Contains the full A2A-standard metadata including name, description, provider, capabilities, skills, security schemes, and supported interfaces. |
| `status.phase` | Status | Runtime phase tracking: Pending, Active, or Error |
| `status.conditions` | Status | Structured conditions for reconciliation state |
| `status.verified` | Status | Whether the AgentCard's JWS signature has been cryptographically verified |

The `targetRef` pattern is consistent with Kubernetes Gateway API conventions, binding the AgentCard metadata to a specific workload without coupling the CRD to a particular deployment mechanism ([kagenti-operator README](https://github.com/kagenti/kagenti-operator), 2026; [Red Hat Developer: Deploying agents with Red Hat AI](https://developers.redhat.com/articles/2026/04/14/deploying-agents-red-hat-ai-openclaw), April 2026).

A companion **AgentRuntime CRD** works alongside AgentCard -- it specifies trace and identity configuration for the workload. Together, AgentRuntime and AgentCard give the platform visibility into what agents are running, where, what they can do, and how they are configured ([Red Hat Developer: Deploying agents with Red Hat AI](https://developers.redhat.com/articles/2026/04/14/deploying-agents-red-hat-ai-openclaw), April 2026).

### 2.3 Discovery Flow

The kagenti-operator implements a multi-controller architecture that automates the full lifecycle from workload deployment to agent metadata indexing:

1. **Label workloads.** Agents are deployed as standard Kubernetes Deployments or StatefulSets with labels `kagenti.io/type: agent` and `protocol.kagenti.io/a2a: ""`.

2. **AgentCard Sync Controller watches.** The sync controller watches cluster-wide for the agent label. When a matching workload is detected, it auto-creates a corresponding AgentCard CR.

3. **AgentCard Controller reconciles.** It resolves the `targetRef` to find the agent's service endpoint, fetches metadata from `/.well-known/agent-card.json` via HTTP, and stores the result in `status.agentCardJSON`.

4. **Signature verification.** If the AgentCard contains JWS signatures, the controller validates them using the agent's SPIFFE-backed x5c certificate chain. Results are recorded in the AgentCard status.

5. **Network policy enforcement.** The NetworkPolicy controller creates permissive or restrictive policies based on verification status.

6. **Continuous reconciliation.** The operator re-fetches metadata on a configurable interval, detecting capability and security posture changes. A config hash mechanism triggers rolling updates when configuration changes.

([kagenti-operator README](https://github.com/kagenti/kagenti-operator), 2026; [Zero trust AI agents on Kubernetes](https://next.redhat.com/2026/03/05/zero-trust-ai-agents-on-kubernetes-what-i-learned-deploying-multi-agent-systems-on-kagenti/), March 2026)

### 2.4 Security Model: SPIFFE/SPIRE and Zero Trust

Kagenti's security architecture is built on the premise that AI agents need workload identity, not API keys. The platform uses SPIFFE (Secure Production Identity Framework For Everyone) to give each agent pod a cryptographic identity that is automatically rotated and scoped to its namespace and service account ([Zero trust AI agents on Kubernetes](https://next.redhat.com/2026/03/05/zero-trust-ai-agents-on-kubernetes-what-i-learned-deploying-multi-agent-systems-on-kagenti/), March 2026).

#### Identity Architecture

Each agent pod receives a SPIFFE ID in the format:

```
spiffe://localtest.me/ns/{namespace}/sa/{service-account}
```

Two sidecars are automatically injected into agent pods without manual configuration:

1. **spiffe-helper**: Fetches and rotates X.509 SPIFFE Verifiable Identity Documents (SVIDs) from the SPIRE server. These are short-lived certificates that replace static API keys.
2. **kagenti-client-registration**: Registers the agent as an OAuth2 client in Keycloak, enabling token exchange with scoped, short-lived tokens.

#### SPIFFE vs. Kubernetes Service Account Tokens

| Dimension | Kubernetes SA Tokens | SPIFFE/SPIRE |
|---|---|---|
| Scope | Namespace-scoped | Cross-cluster, cross-cloud |
| Lifetime | Long-lived by default | Short-lived, automatically rotated |
| Backing | JWT tokens | X.509 certificates |
| Trust boundary | Single cluster | Trust domain spanning multiple clusters |
| Identity portability | Cluster-specific | Identity follows the workload |

#### mTLS via Istio Ambient

Kagenti uses Istio Ambient mesh for transport-level security. Unlike traditional Istio with per-pod Envoy sidecars, Ambient uses a shared, per-node `ztunnel` proxy written in Rust. This approach handles Layer 4 mutual TLS enforcement without injecting proxies into agent pods -- important for AI workloads where sidecar proxies compete for memory and CPU with resource-heavy LLM inference containers.

Authorization policies enforce namespace-level isolation, allowing agents within the same namespace to communicate while blocking cross-namespace traffic at the TCP layer.

#### JWS Signature Verification

The kagenti-operator performs JWS-based cryptographic verification of AgentCards using RSA and ECDSA algorithms. In recent releases, the platform added A2A Agent Card signature verification via SPIRE x5c signing -- the same SPIFFE identity used for workload authentication also signs the AgentCard, creating an end-to-end cryptographic trust chain from pod identity to published metadata ([Zero trust AI agents on Kubernetes](https://next.redhat.com/2026/03/05/zero-trust-ai-agents-on-kubernetes-what-i-learned-deploying-multi-agent-systems-on-kagenti/), March 2026).

This end-to-end trust chain is unique to kagenti and directly relevant to the Agent Registry. When the MLflow registry ingests agents from kagenti, it knows that metadata was published by a cryptographically verified workload, not a spoofed endpoint.

### 2.5 A2A Integration

Kagenti is natively built around the A2A protocol. Agents communicate via HTTPS using JSON-RPC, each agent exposes an AgentCard for capability discovery, and the A2A task lifecycle governs request/response handling. The framework-agnostic design means any container that exposes an A2A-compatible HTTP endpoint works with kagenti -- LangGraph, CrewAI, AG2, and BeeAI agents all deploy without code modifications.

As covered in [02-standards-and-protocols](02-standards-and-protocols.md) Section 2, the A2A AgentCard is the canonical metadata format that both kagenti and the MLflow Agent Registry align around. Kagenti's AgentCard CRD is the Kubernetes-native representation of the same A2A AgentCard -- the CRD's `status.agentCardJSON` field contains exactly the JSON that the A2A specification defines.

### 2.6 MCP Gateway

The MCP Gateway ([Kuadrant/mcp-gateway](https://github.com/Kuadrant/mcp-gateway)) is an Envoy-based gateway that routes MCP tool invocations, translates between protocols, and provides rate limiting and access control for tool calls. It integrates with kagenti's security model for zero-trust tool access. The MCP Gateway is the tool-layer counterpart to kagenti's agent-layer governance: kagenti governs which agents are deployed and discovered; the MCP Gateway governs which tools agents can access.

---

## 3. Kagenti as MLflow Discovery Backend

The upstream MLflow Agent Registry RFC must define abstract provider interfaces that any discovery backend can implement. Kagenti is the reference Kubernetes implementation, but the RFC cannot be kagenti-specific. This section explains the three integration architectures and what belongs in the upstream RFC versus what stays downstream.

### 3.1 Three Integration Architectures

Varsha Prasad Narsing's agent registry proposal defines three integration patterns between kagenti and MLflow (see [agent-registry-upstream-proposal.md](/features/agent-registry/strategy/upstream-proposal.md)):

#### Option A: Pull (MLflow watches AgentCard CRDs)

MLflow's Kubernetes plugin uses the K8s API to poll or watch AgentCard CRDs directly. The plugin reads reconciled AgentCard status -- it does not re-fetch `/.well-known/agent-card.json` from pods. **Strengths**: Simple, uses native K8s API, inherits kagenti's trust verification. **Weaknesses**: Requires K8s API access from MLflow, coupling to AgentCard CRD schema.

#### Option B: Push (kagenti pushes to MLflow webhook)

The kagenti-operator is extended with an MLflow reconciler that pushes agent events (discovered, updated, removed) to MLflow's webhook endpoint. MLflow receives pre-formatted metadata without needing K8s API access. **Strengths**: Decoupled architectures, real-time notifications. **Weaknesses**: Requires kagenti-side changes, webhook reliability concerns.

#### Option C: Hybrid (Push + Poll)

Push for real-time event notification, periodic poll for consistency reconciliation. Combines the strengths of both approaches. **Strengths**: Real-time plus consistency, most resilient. **Weaknesses**: Most complex to implement and operate.

### 3.2 What the Upstream MLflow RFC Needs

The MLflow RFC must define abstractions that work with kagenti but are not coupled to it. The following belong in the upstream specification:

**1. Abstract Discovery Provider Interface**

An `AgentDiscoveryProvider` base class with a required `discover(filters) -> list[DiscoveredAgent]` method, an optional `watch(filters) -> Iterator[AgentEvent]` method, and a `capabilities` property returning supported sync modes (`POLL`, `WATCH`, `WEBHOOK`). This interface is generic -- implementable by a Kubernetes plugin (reading AgentCard CRDs), a Docker plugin (scanning container labels), a Consul plugin (reading service catalog), or a static file plugin. The entry point group `mlflow.agent_discovery` follows MLflow's existing plugin patterns.

**2. Webhook Endpoint**

A REST endpoint at `/api/agents/webhook` that accepts push notifications from any discovery source, with event types for agent discovered, updated, and removed. This endpoint is protocol-agnostic -- kagenti pushes to it, but so could any other discovery backend.

**3. AgentCard-Compatible Metadata Schema**

The `DiscoveredAgent` data class should be compatible with the A2A AgentCard schema (see [02-standards-and-protocols](02-standards-and-protocols.md) Section 2.1). Fields like `name`, `description`, `skills`, `provider`, `securitySchemes`, and `supportedInterfaces` map directly from A2A. Fields like `source_plugin`, `status`, `last_seen_at`, and `verified` are registry-specific extensions.

**4. Trust Verification Interface**

An optional `verify(agent: DiscoveredAgent) -> VerificationResult` method that discovery plugins can implement. The Kubernetes plugin delegates to kagenti's existing JWS verification; other plugins implement their own trust models.

### 3.3 What Stays Downstream-Only

The following are kagenti-specific concerns that should not appear in the upstream MLflow RFC:

- **AgentCard CRD bindings**: The specific Go types, API group (`kagenti.io`), and version (`v1alpha1`) of the AgentCard CRD are kagenti implementation details. The MLflow plugin translates them into the abstract `DiscoveredAgent` format.
- **SPIFFE trust chain**: The SPIFFE/SPIRE identity model is kagenti's security foundation, but MLflow should accept verified/unverified status from any identity system. The upstream interface exposes `verified: bool` and `identity: str` -- it does not mandate SPIFFE.
- **AgentRuntime CRD**: The companion CRD for trace and identity configuration is a kagenti deployment concern, not a registry concern.
- **Istio Ambient integration**: Network-level mTLS is kagenti's transport security, invisible to the registry layer.
- **kagenti-operator reconciler extensions**: Any modifications to the kagenti-operator for MLflow push integration are downstream changes to kagenti, not to MLflow.

### 3.4 Why This Separation Matters

This separation is essential for the RFC's acceptance:

1. **MLflow is vendor-neutral.** Databricks maintains MLflow as an open platform. An RFC that requires kagenti would be rejected. It must work equally well with kagent, Docker, Consul, or static files.

2. **Red Hat's downstream advantage is preserved.** Abstract interfaces upstream let Red Hat provide the best-in-class Kubernetes plugin downstream -- leveraging kagenti's AgentCard CRDs, SPIFFE trust chain, and MCP Gateway. This follows the OpenShift pattern: contribute generic capabilities upstream, differentiate with enterprise features downstream.

3. **The plugin ecosystem grows.** Other contributors implement discovery plugins for their own environments. AWS implements one for their Agent Registry, Google for Vertex AI Agent Engine -- each implementing the same interface.

---

## 4. Kagent (CNCF Sandbox)

Kagent is a separate project from kagenti, developed by Solo.io and contributed to the CNCF as a Sandbox project in May 2025. Where kagenti focuses on enterprise security and governance, kagent focuses on making it easy for DevOps and platform engineers to build AI agents that automate cloud-native operations ([Solo.io: Bringing Agentic AI to Kubernetes](https://www.solo.io/blog/bringing-agentic-ai-to-kubernetes-contributing-kagent-to-cncf), 2025; [CNCF kagent project page](https://www.cncf.io/projects/kagent/), 2026).

### 4.1 Architecture

Kagent is built on three layers:

1. **Tools**: Pre-defined functions that agents can use -- sending emails, searching databases, displaying pod logs, calling external APIs. Tools integrate via MCP (Model Context Protocol). The ToolServer CRD (now migrated to a separate `kmcp` subproject) manages tool lifecycle.

2. **Agents**: Autonomous systems capable of planning, executing tasks, analyzing results, and iterating on outcomes. Each agent is defined declaratively via a CRD specifying its LLM backend, tools, system prompt, and runtime configuration.

3. **Framework**: A Kubernetes-native controller (written in Go) that reconciles agent CRDs, plus an engine that runs the agent's conversation loop. The engine supports two runtimes:
   - **Python ADK** (default): Built on Google's Agent Development Kit (ADK), supporting integrations with CrewAI, LangGraph, and OpenAI frameworks
   - **Go ADK**: Native Go implementation with faster startup (~2 seconds vs ~15 seconds) and lower resource consumption

([kagent architecture docs](https://kagent.dev/docs/kagent/concepts/architecture), 2026; [kagent-dev/kagent GitHub](https://github.com/kagent-dev/kagent), 2026)

### 4.2 Framework Migration

Kagent was originally built on Microsoft's AutoGen framework. In 2026, the project migrated its default runtime to Google's Agent Development Kit (ADK), reflecting the broader industry shift toward ADK as the reference A2A implementation. Both runtimes support MCP tools, human-in-the-loop (HITL) functionality, and agent memory. The BYO (Bring Your Own) agent pattern allows users to deploy agents built with any framework through the A2A protocol, without decomposing agent logic into kagent-native CRDs ([kagent release notes](https://kagent.dev/docs/kagent/resources/release-notes), 2026).

### 4.3 Solo.io's Broader Agentic Suite

At KubeCon + CloudNativeCon Europe 2026, Solo.io announced the contribution of **agentregistry** to the CNCF -- an AI-native open source registry for AI agents, MCP tools, and agent skills. Solo.io's agentic infrastructure now spans four projects ([Cloud Native Now: Solo.io at KubeCon Europe 2026](https://cloudnativenow.com/kubecon-cloudnativecon-europe-2026/solo-io-launches-agentevals-open-source-project-contributes-agentregistry-to-cncf/), March 2026):

| Project | Purpose | Governance |
|---|---|---|
| **kagent** | Agent framework for K8s | CNCF Sandbox |
| **agentgateway** | AI gateway with MCP/A2A support | Linux Foundation |
| **agentregistry** | Agent, tool, and skill registry | Contributed to CNCF (March 2026) |
| **agentevals** | Agent evaluation and benchmarking | Open source (Solo.io) |

The agentregistry contribution is notable -- it represents a competing vision for agent discovery and governance, with centralized cataloging, semantic search, and integrations with AWS AgentCore and Google Vertex AI.

### 4.4 Relationship to Agent Registry

Kagent is a potential discovery source for the MLflow Agent Registry, but with a different CRD format than kagenti. The MLflow Kubernetes plugin could be extended to discover kagent-managed agents by watching kagent's Agent CRDs (API group `kagent.dev/v1alpha2`). However, the metadata available from kagent's CRDs is less rich than kagenti's AgentCard CRDs -- kagent agents may not expose `/.well-known/agent-card.json` (this is an open feature request: [kagent-dev/kagent#1118](https://github.com/kagent-dev/kagent/issues/1118)).

The MLflow discovery provider interface should not assume AgentCard CRDs specifically -- it should accept any Kubernetes CRD with sufficient agent metadata, using per-plugin mapping logic.

---

## 5. Agent-Sandbox (kubernetes-sigs)

Agent-sandbox is a subproject of Kubernetes SIG Apps that provides a declarative API for managing isolated, stateful, singleton workloads -- ideal for AI agent runtimes that need to execute untrusted code. It is hosted at [kubernetes-sigs/agent-sandbox](https://github.com/kubernetes-sigs/agent-sandbox) and was launched as a formal SIG Apps subproject with backing from Google ([Google Open Source Blog: Agent Sandbox](https://opensource.googleblog.com/2025/11/unleashing-autonomous-ai-agents-why-kubernetes-needs-a-new-standard-for-agent-execution.html), November 2025; [Kubernetes Blog: Running Agents with Agent Sandbox](https://kubernetes.io/blog/2026/03/20/running-agents-on-kubernetes-with-agent-sandbox/), March 2026).

### 5.1 CRDs

| CRD | Purpose |
|---|---|
| **Sandbox** | Core resource: a single, stateful pod with stable identity, persistent storage, and configurable isolation backend |
| **SandboxTemplate** | Reusable definitions for creating multiple similar Sandboxes |
| **SandboxClaim** | User-facing resource for provisioning Sandboxes from templates (like PVC claims PVs) |
| **SandboxWarmPool** | Pre-warmed pool of Sandbox instances for sub-second provisioning latency |

### 5.2 Isolation Backends and Capabilities

The architecture decouples execution from isolation technology, supporting **gVisor** (user-space kernel, syscall-level isolation), **Kata Containers** (lightweight VMs, hardware-virtualization isolation), and standard containers. Key capabilities include stable hostname/identity, persistent storage, lifecycle management (creation, deletion, hibernation, auto-resume), scale-to-zero for idle sandboxes, and warm pools for sub-second provisioning.

As of April 2026, agent-sandbox is at version 0.4.2 with approximately 1,900 GitHub stars. GKE offers agent-sandbox at no extra charge ([agent-sandbox docs](https://agent-sandbox.sigs.k8s.io/docs/overview/), 2026).

### 5.4 Relationship to Agent Registry

Agent-sandbox is a runtime environment concern, not a discovery or governance concern. The Agent Registry does not integrate with agent-sandbox directly. However, the registry may record metadata about an agent's execution environment:

- **Isolation level**: Whether an agent runs in a gVisor sandbox, Kata container, or standard container
- **Sandbox configuration**: Template references and warm pool membership
- **Security posture**: The isolation backend informs the registry's trust assessment of an agent

The key distinction is: kagenti discovers *what agents exist and what they can do*. Agent-sandbox manages *where and how agents execute code*. The registry cares about the former; it may annotate the latter.

---

## 6. Kubernetes-Native Agent Patterns

Synthesizing the three projects above, several patterns emerge for how Kubernetes is being extended to support agentic AI workloads. These patterns inform the design of the MLflow Agent Registry's Kubernetes discovery plugin.

### 6.1 Label-Based Discovery

Both kagenti and kagent use Kubernetes labels as the entry point for agent discovery:

| Project | Discovery Label | Purpose |
|---|---|---|
| kagenti | `kagenti.io/type: agent` | Marks workloads as agent deployments |
| kagenti | `protocol.kagenti.io/a2a: ""` | Indicates A2A protocol compatibility |
| kagent | `kagent.dev/type: agent` | Marks workloads as kagent-managed agents |

Labels are the Kubernetes-native mechanism for workload classification. They enable watch-based discovery without full-cluster scanning -- controllers watch only labeled resources, minimizing API server load. The MLflow Kubernetes plugin should similarly use label selectors to scope its discovery to relevant workloads.

### 6.2 CRD-as-Metadata

All three projects use custom resource definitions as the primary metadata store for their respective concerns:

- **kagenti AgentCard**: A2A-compatible agent metadata with JWS verification status
- **kagent Agent**: Agent definition including LLM backend, tools, system prompt, and runtime
- **agent-sandbox Sandbox**: Execution environment specification with isolation backend

This pattern -- CRD as the authoritative metadata record -- is important for registry integration. The MLflow discovery plugin reads CRDs rather than probing individual agent endpoints. This means the plugin benefits from Kubernetes' built-in consistency guarantees: CRDs are stored in etcd, reconciled by controllers, and queryable via the standard API.

### 6.3 Operator-Driven Reconciliation

The operator pattern is the backbone of all three projects. Controllers watch for changes and reconcile desired state with actual state:

1. **kagenti-operator**: Watches labeled workloads, creates AgentCard CRs, fetches agent metadata, verifies signatures, enforces network policies
2. **kagent controller**: Watches Agent CRDs, provisions agent pods, manages the conversation loop engine
3. **agent-sandbox controller**: Watches Sandbox CRDs, provisions isolated pods, manages lifecycle (hibernation, warm pools)

For the registry, the operator pattern means that agent metadata is always eventually consistent. The kagenti-operator continuously reconciles AgentCard CRDs -- if an agent's metadata changes (new skills, updated capabilities), the CRD is updated within the reconciliation interval. The MLflow plugin's poll/watch mechanisms inherit this consistency.

### 6.4 Kubernetes as ONE Discovery Source

A critical design principle for the MLflow Agent Registry: Kubernetes is one discovery source among many. Not all agents run on Kubernetes. Some run as Docker containers, cloud-managed services (AWS AgentCore, Azure AI Agent Service, Google Vertex AI Agent Engine), SaaS endpoints, or bare-metal processes.

The upstream MLflow RFC must not assume Kubernetes as the only -- or even the primary -- discovery backend. The plugin architecture described in Section 3.2 ensures that Kubernetes (via kagenti) is treated the same as any other discovery source: implementing the abstract `AgentDiscoveryProvider` interface and registering via the `mlflow.agent_discovery` entry point.

This means the registry's data model cannot depend on Kubernetes-specific concepts (namespaces, labels, CRDs). These are translated by the plugin into the generic `DiscoveredAgent` format. The registry stores agents uniformly regardless of their source environment.

### 6.5 Implications for the Registry

The Kubernetes agent landscape informs several registry design decisions:

1. **Plugin-per-platform, not plugin-per-project.** A single Kubernetes plugin should discover agents from kagenti, kagent, and any other CRD-based agent platform. The plugin uses configurable label selectors and CRD mappings to support multiple sources.

2. **Trust is source-dependent.** Kagenti provides cryptographic trust verification (SPIFFE + JWS). Kagent does not. The registry must track trust verification status per agent, per source -- not assume a uniform trust level.

3. **Metadata richness varies.** Kagenti's AgentCard CRDs contain full A2A metadata. Kagent's Agent CRDs contain different metadata. The plugin must handle varying levels of metadata completeness and map available fields to the registry's schema.

4. **Runtime environment is metadata, not identity.** Whether an agent runs in a gVisor sandbox, a Kata container, or a standard pod is useful context for governance decisions, but does not define the agent's registry identity.

5. **Kubernetes-native discovery complements, not replaces, the registry.** Kagenti's AgentCard CRDs provide Kubernetes-native discovery within a cluster. The MLflow Agent Registry provides cross-environment discovery across clusters, clouds, and on-premise deployments. Both are needed; neither subsumes the other.

---

## 7. References

### Kagenti

- Kagenti Project Site: [kagenti.github.io/.github](https://kagenti.github.io/.github/)
- Kagenti GitHub Organization: [github.com/kagenti](https://github.com/kagenti)
- Kagenti Operator: [github.com/kagenti/kagenti-operator](https://github.com/kagenti/kagenti-operator)
- Zero Trust AI Agents on Kubernetes (Red Hat ET blog): [next.redhat.com](https://next.redhat.com/2026/03/05/zero-trust-ai-agents-on-kubernetes-what-i-learned-deploying-multi-agent-systems-on-kagenti/), March 2026
- Deploying Agents with Red Hat AI (Red Hat Developer): [developers.redhat.com](https://developers.redhat.com/articles/2026/04/14/deploying-agents-red-hat-ai-openclaw), April 2026
- Kagenti vs Kagent Comparison (Red Hat ET): [github.com/redhat-et/agent-orchestration/issues/13](https://github.com/redhat-et/agent-orchestration/issues/13)

### Kagent (Solo.io / CNCF)

- Kagent Project Site: [kagent.dev](https://kagent.dev/)
- Kagent GitHub: [github.com/kagent-dev/kagent](https://github.com/kagent-dev/kagent)
- Kagent CNCF Page: [cncf.io/projects/kagent](https://www.cncf.io/projects/kagent/)
- Kagent Architecture: [kagent.dev/docs/kagent/concepts/architecture](https://kagent.dev/docs/kagent/concepts/architecture)
- Solo.io CNCF Contribution Blog: [solo.io/blog/bringing-agentic-ai-to-kubernetes-contributing-kagent-to-cncf](https://www.solo.io/blog/bringing-agentic-ai-to-kubernetes-contributing-kagent-to-cncf), 2025
- Solo.io Agentregistry CNCF Contribution: [cloudnativenow.com](https://cloudnativenow.com/kubecon-cloudnativecon-europe-2026/solo-io-launches-agentevals-open-source-project-contributes-agentregistry-to-cncf/), March 2026

### Agent-Sandbox (kubernetes-sigs)

- Agent-Sandbox GitHub: [github.com/kubernetes-sigs/agent-sandbox](https://github.com/kubernetes-sigs/agent-sandbox)
- Agent-Sandbox Documentation: [agent-sandbox.sigs.k8s.io](https://agent-sandbox.sigs.k8s.io/)
- Running Agents on K8s (Kubernetes Blog): [kubernetes.io/blog/2026/03/20/running-agents-on-kubernetes-with-agent-sandbox](https://kubernetes.io/blog/2026/03/20/running-agents-on-kubernetes-with-agent-sandbox/), March 2026
- Google Open Source Blog: [opensource.googleblog.com](https://opensource.googleblog.com/2025/11/unleashing-autonomous-ai-agents-why-kubernetes-needs-a-new-standard-for-agent-execution.html), November 2025

### SPIFFE/SPIRE

- SPIFFE Specification: [spiffe.io](https://spiffe.io/)

### Internal References

- Agent Ecosystem & Terminology: [01-agent-ecosystem.md](01-agent-ecosystem.md)
- Agent Standards & Protocols: [02-standards-and-protocols.md](02-standards-and-protocols.md)
- Varsha's Agent Registry Proposal: [agent-registry-upstream-proposal.md](/features/agent-registry/strategy/upstream-proposal.md)
- Agentic AI Strategy Context: [agentic-strategy.md](https://github.com/solaius/ai-asset-registry/blob/main/docs/knowledge-review/strategy/agentic-strategy.md)
