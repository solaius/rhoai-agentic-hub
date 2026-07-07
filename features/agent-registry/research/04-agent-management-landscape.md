---
title: Agent Registry Research - Agent Management Landscape
description: Competitive landscape survey of agent registry, catalog, and governance products -- features, gaps, and RHOAI differentiation opportunities.
source: ai-asset-registry/agents/agent-registry/research/04-agent-management-landscape.md (as of 2026-07-05)
timestamp: 2026-07-06
review_after: 2026-08-05
---

# Agent Registry Research - Agent Management Landscape

**Date**: 2026-04-24
**Author**: Peter Double (Principal PM - MCP & AI Asset Registries)
**Purpose**: Survey the competitive landscape of agent registry, catalog, and governance products. Identify features, gaps, and RHOAI differentiation opportunities.

---

## 1. Executive Summary

The agent management landscape has undergone a decisive shift in early 2026. Several key trends define the current state:

1. **Agent registries are now a product category.** AWS launched the first dedicated agent registry from a hyperscaler in April 2026, validating the market need for centralized agent discovery and governance. This follows IBM's Agent Catalog and Google's Cloud API Registry, all recognizing that unmanaged agent sprawl is an enterprise risk.

2. **Governance is the differentiator, not orchestration.** Every major framework (LangGraph, CrewAI, Microsoft Agent Framework) can orchestrate agents. The unsolved enterprise problem is governing them at scale: who registered this agent, what can it access, is it approved for production, and what is it doing? The platforms investing in governance (AWS AgentCore Policy, IBM watsonx.governance, Google Agent Gateway) are pulling ahead.

3. **MCP + A2A convergence defines the interop layer.** MCP handles agent-to-tool communication; A2A handles agent-to-agent communication. Both are now supported by AWS, Google, Microsoft, Salesforce, CrewAI, and BeeAI. Platforms that support both protocols have a structural advantage. The A2A project and MCP are collaborating on a unified entity card for agents and tools, enabling shared registries.

4. **Kubernetes-native agent management is emerging.** Two open-source projects (kagent from Solo.io/CNCF, Kagenti from Red Hat) are bringing agent lifecycle management into Kubernetes with CRDs, operators, and service mesh integration. This creates an opportunity for Red Hat to define the on-premises agent control plane.

5. **The market is growing at 44-46% CAGR.** MarketsandMarkets projects the AI agents market growing from $7.8B in 2025 to $52.6B by 2030. Gartner predicts 40% of enterprise applications will include task-specific AI agents by end of 2026. IDC projects total AI spending reaching $1.3 trillion by 2029, with agentic AI as the fastest-growing segment.

---

## 2. Enterprise AI Platforms

### 2.1 AWS Bedrock AgentCore / Agent Registry (Preview April 2026)

**First hyperscaler with a dedicated agent registry.** AWS launched the Agent Registry in preview on April 9, 2026, as part of Amazon Bedrock AgentCore. It provides a centralized catalog for registering, discovering, and governing agents, MCP servers, tools, skills, and custom resources across any cloud or on-premises environment.

**Discovery and Search:**
- Hybrid search combining keyword and semantic matching. Queries like "payment processing" surface tools tagged as "billing" or "invoicing."
- URL-based discovery automatically retrieves metadata from live MCP server or agent endpoints.
- The registry itself is accessible as a remote MCP endpoint, so any MCP-compatible client can query it directly.

**Governance and Approval Workflow:**
- Lifecycle: Draft -> Pending Approval -> Approved -> Deprecated.
- Three-persona model: Admin (infrastructure/IAM), Publisher (registration), Curator/Consumer (review/discovery).
- EventBridge integration emits events on state transitions, enabling CI/CD pipelines for security scanning and validation.
- Limitation: updating any record resets status to DRAFT, requiring re-approval.

**Authentication and Security:**
- IAM + OAuth/JWT for flexible access control.
- CloudTrail audit trail for all operations.
- AgentCore Policy (GA March 2026): Cedar-based policy language for runtime access control, intercepting all agent traffic through gateways.

**Protocol Support:**
- Native MCP and A2A protocol support.
- Provider-agnostic indexing: catalogs agents regardless of where they run (AWS, other clouds, on-premises).
- Custom schemas for non-standard resource types.

**Roadmap:**
- Automatic indexing of agents upon deployment.
- Cross-registry federation for searching multiple registries as one.
- Custom categories and taxonomies.
- Integration of operational data (invocation counts, latency, uptime) from AgentCore Observability directly into registry records.

**Known Limitations:** Semantic search underperforms on non-English queries; record update -> DRAFT reset creates friction; preview limited to five regions.

**Sources**: [AWS Agent Registry Preview Announcement](https://aws.amazon.com/about-aws/whats-new/2026/04/aws-agent-registry-in-agentcore-preview/) | [AWS Agent Registry Blog](https://aws.amazon.com/blogs/machine-learning/the-future-of-managing-agents-at-scale-aws-agent-registry-now-in-preview/) | [Agent Registry Documentation](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/registry.html) | [InfoQ Coverage](https://www.infoq.com/news/2026/04/aws-agent-registry-preview/) | [The Register Coverage](https://www.theregister.com/2026/04/09/aws_ai_agent_registry/)

---

### 2.2 IBM watsonx Orchestrate Agent Catalog

**Most mature enterprise agent catalog with governance integration.** IBM watsonx Orchestrate provides a framework-agnostic Agent Catalog with 100+ prebuilt agents and 400+ validated tools, backed by watsonx.governance for full lifecycle AI governance.

**Agent Catalog:**
- 100+ prebuilt agents, partner contributions (Agent Connect), and custom builds.
- Framework-agnostic: "Any agent, any framework." Not tied to a single SDK, LLM, or cloud.
- Every agent validated, observable, connected to 700+ enterprise systems.
- Governed Agentic Catalog integrates with watsonx.governance for tool/agent selection and reuse.

**watsonx.governance for Agents (2026 Updates):**
- "AI Agent" object type in the governance console for agentic lifecycle management.
- Agent Monitoring and Insights (Q1 2026): tracks decisions, behaviors, and performance with real-time alerts.
- Root cause analysis tracks decision chains, not just final output.
- AI Risk Atlas integration: comprehensive risk library for generative AI, supplementable with custom risk inventories.
- Automated compliance with EU AI Act, NIST AI RMF.
- Guardium AI Security metrics flow directly into governance workflows.

**Multi-Agent Orchestration:**
- Agent Connect partner program: ISVs integrate agents as first-class catalog citizens.
- Staging area governance: testing for quality, security, cost, and latency before production.
- Hybrid cloud via OpenShift (SaaS or on-premises).
- OpenTelemetry and Traceloop for comprehensive observability.

**Sources**: [IBM watsonx Orchestrate Agent Catalog](https://www.ibm.com/products/watsonx-orchestrate/agent-catalog) | [Agent Catalog Blog](https://www.ibm.com/new/product-blog/any-agent-any-framework-inside-the-ibm-watsonx-orchestrate-agent-catalog) | [watsonx.governance](https://www.ibm.com/products/watsonx-governance) | [Agentic AI Governance Announcement](https://www.ibm.com/new/announcements/agentic-ai-governance-evaluation-and-lifecycle) | [Agent Monitoring & Security](https://www.ibm.com/new/announcements/new-security-metrics-agent-monitoring-and-insights-in-watsonx-governance)

---

### 2.3 Google Vertex AI Agent Builder / Gemini Enterprise Agent Platform

**Tool governance through Cloud API Registry with emerging Agent Registry.** Google has been building agent governance capabilities through its Cloud API Registry integration with Vertex AI Agent Builder, and at Cloud Next 2026, consolidated its platform under the Gemini Enterprise Agent Platform brand.

**Cloud API Registry:**
- Private registry where administrators curate approved tools (including MCP servers) for developers across the organization. Prevents "shadow AI" tool sprawl.
- Pre-built MCP tools for Google services (BigQuery, Maps).
- Custom MCP servers via Apigee integration: transforms existing managed APIs into MCP servers.
- Agent Development Kit (ADK) introduces `ApiRegistry` object for programmatic tool access.
- CLI-based discovery: `gcloud beta api-registry mcp servers list`.

**Agent Engine:**
- GA for sessions and memory bank.
- Supports A2A protocol with bidirectional streaming.
- Durable execution for long-running agent workflows.

**Cloud Next 2026 Announcements:**
- Rebranded to Gemini Enterprise Agent Platform (formerly Vertex AI).
- New **Agent Registry**: centralized catalog for discovering, tracking, and managing all agents, tools, and MCP servers.
- New **Agent Gateway**: central policy enforcement point governing all agent tool calls, managing authentication, and applying security policies.
- **Governance Policies**: Content Protection and Semantic Governance for data leakage prevention and compliance.
- Agentspace absorbed into unified Gemini Enterprise product.

**Security:**
- Agent identity via IAM.
- VPC Service Controls for network isolation.
- Threat detection via Security Command Center.
- Content Protection policies for sensitive data handling.

**Sources**: [Cloud API Registry Tool Governance](https://cloud.google.com/blog/products/ai-machine-learning/new-enhanced-tool-governance-in-vertex-ai-agent-builder) | [Vertex AI Agent Builder Overview](https://docs.cloud.google.com/agent-builder/overview) | [Gemini Enterprise Agent Platform](https://cloud.google.com/products/agent-builder) | [Cloud Next 2026 Coverage](https://thenextweb.com/news/google-cloud-next-ai-agents-agentic-era)

---

### 2.4 Microsoft Agent Framework 1.0 (GA April 2026)

**Unified SDK, not a registry product.** Microsoft shipped Agent Framework 1.0 GA on April 3, 2026 -- the production-ready convergence of Semantic Kernel (enterprise stability) and AutoGen (multi-agent research) into a single open-source SDK. Combined, the two predecessor projects accumulated over 75,000 GitHub stars. Microsoft does not offer a dedicated agent registry product.

**Architecture:**
- Semantic Kernel as foundation layer (kernel, plugin model, connectors) with AutoGen's multi-agent orchestration rebuilt as graph-based workflow engine.
- Connectors for Azure OpenAI, OpenAI, Anthropic Claude, Bedrock, Gemini, and Ollama.
- Declarative YAML agents: instructions, tools, memory, and orchestration topology in version-controlled files.
- Stable orchestration patterns: sequential, concurrent, handoff, group chat, Magentic-One -- all with streaming, checkpointing, and human-in-the-loop.

**Interoperability:**
- MCP for dynamic tool discovery, A2A for cross-runtime agent collaboration, AG-UI for agent-to-frontend.
- Multi-provider: swap LLM providers with a single registration line.

**AutoGen Migration:**
- AutoGen in maintenance mode (Feb 2026). AG2 community fork continues independently.
- Migration: 2-4 hours for Semantic Kernel apps; harder for AutoGen due to conversation-to-graph model change.

**Notable Gap:** No dedicated agent registry, catalog, or governance product. Microsoft relies on Azure AD for identity and Azure DevOps for lifecycle management, but there is no centralized place to discover and approve agents across an organization.

**Sources**: [Microsoft Agent Framework 1.0 Blog](https://devblogs.microsoft.com/agent-framework/microsoft-agent-framework-version-1-0/) | [Agent Framework Overview](https://learn.microsoft.com/en-us/agent-framework/overview/) | [Visual Studio Magazine Coverage](https://visualstudiomagazine.com/articles/2026/04/06/microsoft-ships-production-ready-agent-framework-1-0-for-net-and-python.aspx) | [AutoGen Migration Guide](https://learn.microsoft.com/en-us/agent-framework/migration-guide/from-autogen/)

---

### 2.5 Salesforce Agentforce

**Enterprise agent deployment at scale with A2A interoperability.** Salesforce's Agentforce platform has moved from pilot programs to production-grade infrastructure, with the "Customer Zero" deployment at Reddit driving 84% reductions in case resolution times.

**Agent Architecture:**
- Agent Builder: low-code using Topics (job definitions) and Actions (automation via Flow/Apex).
- Atlas Reasoning Engine; Agentforce Script (Spring 2026) for hybrid deterministic + LLM reasoning.

**A2A Integration:**
- A2A in production at 150+ organizations. Salesforce agents hand off to Google Vertex AI, ServiceNow, or other platforms without understanding internal architecture.
- MuleSoft Agent Fabric with Agent Scanners: automatically detect and catalog agents across Agentforce, Bedrock, Vertex AI into a central registry, normalized to A2A card specs.
- Einstein Trust Layer guardrails and Human-in-the-Loop controls.

**Lifecycle Management:**
- Systematic maintenance: daily monitoring, weekly validation, monthly regression, quarterly reviews.
- Agent inventory with ownership, version control, least-privilege access, and action/output logging.

**Sources**: [Salesforce Agentforce](https://www.salesforce.com/agentforce/) | [A2A Protocol Page](https://www.salesforce.com/agentforce/ai-agents/agent2agent-protocol/) | [Agentforce A2A Architecture](https://www.salesforceben.com/how-to-design-salesforce-agent-to-agent-a2a-architecture/) | [Agentforce Maintenance Guide](https://www.girikon.com/blog/salesforce-agentforce-a-step-by-step-maintenance-guide-in-2026/)

---

## 3. Open Source Agent Platforms

### 3.1 LangChain / LangGraph

**The most widely adopted open-source agent framework.** LangGraph (part of the LangChain ecosystem) has become the default choice for teams needing fine-grained control over agent orchestration, trusted by Klarna, Uber, and J.P. Morgan. The LangChain repository has 97K+ GitHub stars.

**LangGraph Core:**
- Low-level orchestration for stateful, long-running agents as graphs.
- Durable execution, human-in-the-loop state inspection, short-term + long-term memory.
- MCP and A2A support via adapters.

**LangSmith Deployment (formerly LangGraph Platform):**
- Purpose-built deployment for stateful workflows. ~400 companies in production.
- Enterprise tier: RBAC, workspaces, BYOC and self-hosted options.

**LangSmith Observability:**
- Framework-agnostic tracing (works with CrewAI, AutoGen, OpenAI Agents, PydanticAI, and custom agents).
- Insights Agent (2026): auto-analyzes traces for usage patterns and failure modes.

**Notable Gap:** No dedicated agent registry or governance product. LangSmith Deployment provides deployment management but not the discovery, approval workflow, or governance controls that enterprise registries require. LangChain Hub exists for prompts but not for agents.

**Sources**: [LangGraph](https://www.langchain.com/langgraph) | [LangSmith Observability](https://www.langchain.com/langsmith/observability) | [LangGraph Platform GA](https://www.langchain.com/blog/langgraph-platform-ga) | [LangGraph GitHub](https://github.com/langchain-ai/langgraph)

---

### 3.2 CrewAI

**Role-based multi-agent orchestration with the broadest protocol support.** CrewAI has 44,600+ GitHub stars, processes 450M+ monthly workflows, and offers native MCP and A2A protocol support.

**Core Architecture:**
- Three concepts: Agents (roles + tools), Tasks (work units), Crews (orchestration).
- Sequential, hierarchical, and hybrid execution patterns. Flows API for event-driven orchestration.
- YAML-based agent configuration.

**Protocol Support:**
- Native MCP via `crewai-tools[mcp]` with automatic transport negotiation and tool discovery.
- Native A2A task execution (v1.9.0): async chains with poll, stream, and push updates.

**Enterprise Features:**
- HIPAA/SOC2 compliance. Event hierarchy for traceable workflows. Enterprise Tools Repository.
- Common pattern: teams prototype in CrewAI, then migrate to LangGraph for complex conditional logic.
- No dedicated agent registry or governance product.

**Sources**: [CrewAI](https://crewai.com/) | [CrewAI Tools](https://docs.crewai.com/en/concepts/tools) | [MCP + A2A + CrewAI Production Guide](https://47billion.com/blog/ai-agents-in-production-frameworks-protocols-and-what-actually-works-in-2026/)

---

### 3.3 IBM BeeAI / Agent Stack

**Framework-agnostic agent deployment infrastructure under the Linux Foundation.** BeeAI began as an IBM Research project in early 2024 and evolved into Agent Stack, an open infrastructure for fast, cross-framework agent deployment built on the A2A protocol.

**Agent Stack:**
- Deploy agents from any framework (LangGraph, CrewAI, custom code) in minutes.
- SDK handles A2A protocol implementation automatically; all agents exposed as A2A-compatible.
- Managed services: LLM routing, vector storage, authentication, file handling.
- Helm chart for custom infrastructure. One-line install for Linux/macOS.

**A2A Protocol Integration:**
- IBM's Agent Communication Protocol (ACP) merged into A2A.
- A2A Proxy for instant agent connectivity. Collaboration underway with MCP to standardize a unified entity card for agents and tools.

**Open Governance:** Linux Foundation (LF AI & Data), Apache 2.0, incubation phase.

**Notable Gap:** Agent Stack focuses on deployment, not governance. No approval workflows, security scanning, or audit trails. The discovery model is Kubernetes-native (via A2A agent cards) but lacks the searchability and governance controls of a full registry.

**Sources**: [BeeAI](https://beeai.dev/) | [Introducing Agent Stack](https://beeai.dev/blog/introducing-agent-stack) | [Agent Stack GitHub](https://github.com/i-am-bee/agentstack) | [BeeAI A2A Integration](https://a2aprotocol.ai/blog/beeai-a2a-acp)

---

### 3.4 AutoGen / AG2

**In maintenance mode; succeeded by Microsoft Agent Framework.** AutoGen was placed in maintenance mode on February 19, 2026. The original project has split into three paths:

- **Microsoft Agent Framework** (1.0 GA): the official, production-grade successor. Merges AutoGen's orchestration with Semantic Kernel's enterprise stability. See section 2.4.
- **AutoGen (v0.5+)**: the "innovation lab" where research like Magentic-One is first integrated. Security patches only.
- **AG2** (community fork): independent development as a production-focused alternative for teams avoiding Microsoft's ecosystem. On the path to v1.0; current framework being tidied through deprecations.

The migration from AutoGen to Agent Framework requires moving from implicit GroupChat management to explicit graph-based workflows. Microsoft published an official migration guide in February 2026.

**Sources**: [AutoGen Migration Guide](https://learn.microsoft.com/en-us/agent-framework/migration-guide/from-autogen/) | [AG2 GitHub](https://github.com/ag2ai/ag2)

---

### 3.5 Kubernetes-Native Agent Platforms

Two open-source projects are bringing agent lifecycle management directly into Kubernetes:

**kagent (Solo.io / CNCF Sandbox):**
- Kubernetes-native framework with CRDs for agents and tools (ToolServer custom resources).
- Built-in MCP server with tools for Kubernetes, Istio, Helm, Argo, Prometheus, Grafana, Cilium.
- Declarative YAML-based agent and tool definitions.
- OpenTelemetry tracing for observability.
- Architecture: controller (watches CRDs), UI (web management), engine (runs agents via ADK), CLI.
- CNCF sandbox project.

**Kagenti (Red Hat Incubation):**
- Kubernetes-based control plane for AI agents using Component CRD for deployment.
- Framework-neutral: agents run as Kubernetes workloads over A2A protocol. LangGraph, CrewAI, and AG2 supported without agent code modifications.
- Zero-trust security: automatic SPIFFE identity injection for each agent (cryptographic identity, not API keys).
- Istio Ambient mesh integration for mTLS between all workloads.
- AgentCard CRDs index deployed agents automatically -- no external registry required.
- Phoenix-based observability stack.
- Roadmap: persistent long-running agents with memory, sandboxing, Agent Development Kit.

**Key Difference:** Kagent manages lifecycle through a single controller with a dependency graph. Kagenti uses a separate Platform operator with Component CRDs, where dependencies are modeled and reconciled as Kubernetes objects. Both support A2A and MCP, both are Apache 2.0 licensed.

**Sources**: [kagent](https://kagent.dev/) | [kagent GitHub](https://github.com/kagent-dev/kagent) | [Kagenti](https://kagenti.github.io/.github/) | [Red Hat Zero-Trust Agents on Kubernetes](https://next.redhat.com/2026/03/05/zero-trust-ai-agents-on-kubernetes-what-i-learned-deploying-multi-agent-systems-on-kagenti/)

---

## 4. Developer Ecosystem Analogies

Established developer tool ecosystems offer proven patterns for how agent registries should work. Each analogy highlights a specific lesson.

### 4.1 npm / PyPI -- Agent Package Management

| Feature | npm / PyPI | Lesson for Agent Registry |
|---------|-----------|--------------------------|
| Versioning | SemVer with lockfiles (`package-lock.json`, `poetry.lock`) | Agents need SemVer + lockfiles for reproducible deployments |
| Dependency resolution | Nested dependencies, conflict resolution, deduplication | Agents depend on tools, MCP servers, models, and other agents -- all need declared dependencies |
| Security | `npm audit`, `pip-audit`, Sigstore signing, 2FA for publishing | Supply chain security is non-negotiable; scanning on registration required |
| Private registries | Verdaccio, Artifactory, AWS CodeArtifact | Enterprise needs private agent registries alongside public discovery |
| Scoping | `@org/package` in npm | Organizational scoping prevents agent name squatting |
| Governance | OpenSSF working groups, Python Packaging Authority | Agent registries need governance bodies and quality standards |

**Lesson**: Agents are software artifacts. They need the same packaging, versioning, and supply chain rigor that npm and PyPI have built over decades -- plus additional protections for prompt injection and tool abuse vectors.

---

### 4.2 Docker Hub / OCI -- Agent Image Distribution

| Feature | Docker Hub / OCI | Lesson for Agent Registry |
|---------|-----------------|--------------------------|
| Packaging | OCI container images and artifacts | Agents can be packaged as OCI artifacts for universal distribution |
| Versioning | Tags + immutable digests | Pin specific agent versions; avoid floating `latest` in production |
| Distribution | Pull/push to any OCI-compatible registry | Leverage existing registry infrastructure (Quay, Artifactory, ECR) |
| Signing | Docker Content Trust, Sigstore/cosign | Cryptographic signing for agent provenance |
| Scanning | Integrated vulnerability scanning | Automated security scanning on agent registration |
| Governance | Registry Access Management (RAM) | Policy-based access controls for agent consumption |

**Lesson**: OCI is already the packaging standard for models (Docker Model Runner) and MCP servers. Extending it to agents enables a single distribution mechanism across all AI asset types, leveraging Red Hat's existing Quay infrastructure.

---

### 4.3 Helm -- Agent Deployment Templates

| Feature | Helm | Lesson for Agent Registry |
|---------|------|--------------------------|
| Packaging | Chart archives with templates + values | Agents need separation of definition (template) from configuration (values) |
| Versioning | Chart version + app version | Agent version vs. underlying model/tool version tracking |
| Dependencies | `Chart.yaml` with version constraints | Agent dependency declarations for tools, MCP servers, models |
| Configuration | `values.yaml` with overrides | Agent parameters configurable per-environment without code changes |
| Testing | `helm test`, `helm lint` | Agents need validation and testing frameworks before deployment |
| Repositories | OCI-based distribution | Leverage OCI registries for agent distribution |

**Lesson**: Helm's separation of template from values is directly applicable. An agent's instructions and tool bindings (template) should be separable from its runtime configuration (values), enabling the same agent definition to run in dev, staging, and production with different parameters.

---

### 4.4 VS Code Marketplace -- Trust Tiers and Publisher Verification

| Feature | VS Code Marketplace | Lesson for Agent Registry |
|---------|-------------------|--------------------------|
| Security | Multi-layer malware scanning, dynamic detection, secret scanning | Agents need automated scanning for malicious tool calls and prompt injection |
| Trust tiers | Publisher verification badges, workspace trust | Agents need trust levels: verified publisher, community, unverified |
| Signing | Signature verification on install | Cryptographic signing for all registered agents |
| Enterprise | Extension allowlisting, version pinning, private marketplace | Enterprise agent allowlists and private registries |
| Impersonation | Name reservation, typosquatting prevention | Protect against agent name squatting |
| Community | Report a concern, community moderation | Community reporting for misbehaving agents |

**Lesson**: The VS Code Marketplace's trust model translates directly. Agent registries need verified publishers, trust tiers, and enterprise allowlisting. The difference is that agent misbehavior can be more consequential than extension misbehavior -- agents take actions, not just render UI.

---

### 4.5 Terraform Registry -- Provider/Module Discovery and Versioning

| Feature | Terraform Registry | Lesson for Agent Registry |
|---------|-------------------|--------------------------|
| Discovery | Search by provider, category, keyword, popularity | Agents need rich search with semantic matching and categorization |
| Trust levels | Verified providers vs. community modules | Verified agent publishers vs. community-contributed agents |
| Documentation | Auto-generated from code + README | Auto-generate agent documentation from agent cards and metadata |
| Modules | Reusable, composable infrastructure modules | Agents as reusable, composable capability modules |
| Versioning | SemVer with pinning and constraint syntax | Pin agent versions with compatibility constraints |
| Nested modules | Modules compose other modules | Agents that orchestrate other agents need explicit dependency tracking |

**Lesson**: Terraform's two-tier trust model (verified/community) and auto-generated documentation from code are patterns worth adopting directly. The registry should auto-generate agent documentation from A2A agent cards and MCP tool schemas.

---

## 5. Feature Comparison Matrix -- Enterprise

| Feature | AWS AgentCore | IBM watsonx | Google Gemini Platform | Microsoft Agent Framework | Salesforce Agentforce |
|---------|--------------|-------------|----------------------|--------------------------|----------------------|
| **Agent registration** | Agent Registry (preview) | Agent Catalog + Governed Agentic Catalog | Agent Registry + Cloud API Registry | No dedicated registry | MuleSoft Agent Fabric scanners |
| **Discovery** | Hybrid (keyword + semantic) | Catalog browsing + search | Console + CLI + ADK | N/A | Agent Builder library |
| **Versioning** | Registry lifecycle states | Agent lifecycle management | ADK + Agent Engine versioning | YAML-based declarative | Version control per agent |
| **Approval workflow** | Draft -> Pending -> Approved -> Deprecated | Staging area governance | Admin tool controls | N/A | Agent inventory + ownership |
| **Semantic search** | Yes (hybrid) | No (catalog browsing) | Partial (Cloud API Registry) | N/A | No |
| **Protocol support (A2A/MCP)** | MCP + A2A | Any framework (Agent Connect) | MCP + A2A | MCP + A2A | MCP + A2A |
| **Identity/trust** | IAM + OAuth/JWT | Built-in compliance | IAM + Agent Gateway | Azure AD | Einstein Trust Layer |
| **Audit trail** | CloudTrail + EventBridge | OpenTelemetry + Traceloop | Cloud Audit Logs | Azure Monitor | Action/output logging |
| **Multi-cloud** | Yes (provider-agnostic indexing) | Yes (hybrid cloud) | GCP-centric | Azure-centric | Salesforce-centric |
| **On-premises** | Via AgentCore Gateway | Yes (OpenShift) | Via GKE Enterprise | Via Azure Arc | No |
| **Open source** | No (proprietary) | Partial (BeeAI is OSS) | Partial (ADK is OSS) | Yes (Agent Framework) | No |
| **Governance tracks** | AgentCore Policy (Cedar) | watsonx.governance (AI Risk Atlas) | Agent Gateway + Semantic Governance | N/A (no governance product) | Trust Layer + maintenance framework |

---

## 6. Feature Comparison Matrix -- Open Source

| Feature | LangGraph | CrewAI | BeeAI/Agent Stack | kagent (CNCF) | Kagenti (Red Hat) |
|---------|-----------|--------|-------------------|---------------|-------------------|
| **Agent definition** | Python graph API | YAML config + Python | Framework-agnostic SDK | Kubernetes CRDs | Component CRD |
| **Deployment** | LangSmith Deployment (managed) | CrewAI Enterprise (managed) | Agent Stack (self-hosted) | Kubernetes operator | Kubernetes operator |
| **Discovery** | LangSmith UI (deploy-time) | Enterprise dashboard | A2A agent cards | ToolServer CRDs | AgentCard CRDs |
| **Versioning** | Via deployment platform | YAML version fields | A2A protocol versioning | CRD spec versioning | CRD spec versioning |
| **Governance** | RBAC on enterprise tier | HIPAA/SOC2 compliance | None (incubation) | None | SPIFFE identity + Istio mTLS |
| **Protocol support** | MCP + A2A (adapters) | MCP + A2A (native) | A2A (native) | MCP (native ToolServers) | MCP + A2A |
| **K8s native** | No (cloud-hosted) | No (cloud-hosted) | Yes (Helm chart) | Yes (controller + CRDs) | Yes (operator + CRDs) |
| **Security model** | API keys + RBAC | API keys + enterprise auth | A2A protocol auth | Kubernetes RBAC | SPIFFE + Istio Ambient mTLS |

---

## 7. Key Takeaways

### Must-Haves (Table Stakes)

Every enterprise agent registry must include these features based on market consensus:

1. **Centralized agent catalog with search.** AWS, IBM, and Google all provide centralized catalogs. Without a single place to discover what agents exist, organizations face agent sprawl -- duplicate agents, unmanaged agents, and shadow AI. Hybrid search (keyword + semantic) is the emerging standard.

2. **Versioning and lifecycle states.** Agents need explicit lifecycle management: draft, pending approval, approved, deprecated, retired. AWS Agent Registry's lifecycle model is the clearest implementation. All platforms support some form of versioning.

3. **Approval workflows.** Uncontrolled agent registration is an enterprise risk. AWS, IBM, and Salesforce all provide approval workflows before agents become discoverable. The draft -> review -> approve pattern from AWS is becoming standard.

4. **Protocol support (MCP + A2A).** Every major platform now supports both MCP (agent-to-tool) and A2A (agent-to-agent). A registry that does not support both protocols is already behind. The ongoing A2A + MCP collaboration on unified entity cards will further cement this requirement.

5. **Identity and access control.** Agents need identity, not just API keys. AWS uses IAM + OAuth, Google uses IAM + Agent Gateway, Kagenti uses SPIFFE. The pattern is clear: agents are workloads that need workload identity.

6. **Audit trail.** Every agent action, registration, approval, and invocation must be auditable. CloudTrail (AWS), OpenTelemetry (IBM), and Cloud Audit Logs (Google) are all deployed in production.

### Differentiators (What Sets Leaders Apart)

7. **Registry-as-MCP-server.** AWS Agent Registry's approach of exposing the registry itself as an MCP endpoint is a breakthrough pattern. Any MCP-compatible client can query the registry using the same protocol it uses to invoke tools. This makes the registry a first-class participant in the agentic ecosystem, not a side system.

8. **Governance integration.** IBM watsonx.governance provides the deepest governance story: AI Risk Atlas integration, agent monitoring with root cause analysis, compliance automation (EU AI Act, NIST AI RMF), and security metrics from Guardium. No other vendor matches this depth.

9. **Kubernetes-native control plane.** Kagenti and kagent demonstrate that agent lifecycle management belongs in Kubernetes for on-premises deployments. SPIFFE identity, Istio service mesh, and CRD-based agent definitions are patterns that align with Red Hat's infrastructure strengths.

10. **Provider-agnostic indexing.** AWS Agent Registry indexes agents regardless of where they run. A registry locked to a single cloud provider or framework will not satisfy hybrid/multi-cloud enterprises.

11. **Cross-registry federation.** On AWS's roadmap but not yet available anywhere. The ability to search across multiple registries as one would be a significant differentiator for organizations with agents spread across clouds and on-premises environments.

### Gaps (What Nobody Does Well Yet)

12. **No unified agent + tool registry.** AWS Agent Registry comes closest by supporting agents, MCP servers, tools, skills, and custom resources. But no platform provides a single, coherent registry that treats agents, tools, models, and prompts as related assets with dependency tracking between them. This is the AI Asset Registry opportunity.

13. **Agent composition and dependency management.** While multi-agent orchestration is common, declarative agent composition (like Helm chart dependencies) remains immature. No platform provides a dependency graph showing "Agent A depends on MCP Server B, which requires Model C, which needs Guardrail D." This is a gap RHOAI can fill.

14. **Agent testing frameworks.** Unlike Helm (`helm test`) or npm (`npm test`), no standard framework exists for testing agent behavior before deployment. IBM's staging area governance is the closest, but it is manual and platform-specific. The industry needs automated agent validation.

15. **Cross-cloud agent portability.** Despite MCP and A2A standardization, moving an agent from AWS to Azure to on-premises requires significant rework of authentication, tool bindings, and deployment configuration. No platform provides true "write once, deploy anywhere" for agents.

16. **Runtime governance for on-premises.** AWS AgentCore Policy (Cedar-based) is the most mature runtime governance product, but it is cloud-only. IBM watsonx.governance works on-premises via OpenShift but focuses on observability rather than runtime policy enforcement. There is no open-source, on-premises equivalent of AgentCore Policy.

17. **Supply chain security for agents.** The npm/PyPI ecosystems learned hard lessons about supply chain attacks. Agent registries have not yet experienced their equivalent of the `event-stream` or `ua-parser-js` incidents, but they will. JFrog's scan-verify-sign approach for skills has not been extended to agents. No platform provides comprehensive agent supply chain security with signing, provenance, and vulnerability scanning.

### Architecture Patterns Worth Adopting

18. **Three-persona model** (AWS): Admin / Publisher / Consumer separation maps cleanly to enterprise roles and RBAC policies. The curator role (between publisher and consumer) adds governance without bottlenecking.

19. **Registry-as-MCP-server** (AWS): Exposing the registry as an MCP endpoint enables programmatic discovery by agents themselves. Agents can query the registry to find tools and other agents, enabling dynamic composition.

20. **Unified entity card** (A2A + MCP collaboration): A single metadata format describing both agents (A2A) and tools/resources (MCP) would enable a truly unified registry. This is in active development and represents a strategic opportunity to shape the standard.

21. **Policy-as-code** (AWS Cedar, OPA): External policy enforcement that does not require modifying agent code. Cedar (AWS) and OPA (Kubernetes ecosystem) are complementary models. Red Hat has existing OPA/Gatekeeper expertise.

22. **SPIFFE workload identity** (Kagenti): Cryptographic agent identity tied to Kubernetes namespace and service account. More secure than API keys, automatically rotated, and aligned with zero-trust architecture principles.

---

## 8. References

### Enterprise Platforms -- AWS
- [AWS Agent Registry Preview Announcement](https://aws.amazon.com/about-aws/whats-new/2026/04/aws-agent-registry-in-agentcore-preview/)
- [AWS Agent Registry Blog](https://aws.amazon.com/blogs/machine-learning/the-future-of-managing-agents-at-scale-aws-agent-registry-now-in-preview/)
- [Agent Registry Documentation](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/registry.html)
- [Agent Registry Searching](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/registry-searching.html)
- [AgentCore Policy GA Announcement](https://aws.amazon.com/about-aws/whats-new/2026/03/policy-amazon-bedrock-agentcore-generally-available/)
- [AgentCore Policy Documentation](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/policy.html)
- [InfoQ Coverage](https://www.infoq.com/news/2026/04/aws-agent-registry-preview/)
- [The Register Coverage](https://www.theregister.com/2026/04/09/aws_ai_agent_registry/)
- [Xebia AgentCore Registry Guide](https://xebia.com/blog/govern-and-discover-ai-agents-and-tools-with-amazon-bedrock-agentcore-registry/)

### Enterprise Platforms -- IBM
- [IBM watsonx Orchestrate Agent Catalog](https://www.ibm.com/products/watsonx-orchestrate/agent-catalog)
- [Agent Catalog Blog](https://www.ibm.com/new/product-blog/any-agent-any-framework-inside-the-ibm-watsonx-orchestrate-agent-catalog)
- [watsonx.governance](https://www.ibm.com/products/watsonx-governance)
- [Agentic AI Governance Announcement](https://www.ibm.com/new/announcements/agentic-ai-governance-evaluation-and-lifecycle)
- [Agent Monitoring & Security Metrics](https://www.ibm.com/new/announcements/new-security-metrics-agent-monitoring-and-insights-in-watsonx-governance)
- [Governance & Observability](https://www.ibm.com/products/watsonx-orchestrate/governance-and-observability)
- [watsonx.governance Features Comparison 2026](https://blog.exceeds.ai/ibm-watsonx-governance-features-comparison/)
- [e& and IBM Agentic AI Collaboration](https://newsroom.ibm.com/2026-01-19-e-and-ibm-unveil-enterprise-grade-agentic-AI-to-transform-governance-and-compliance)

### Enterprise Platforms -- Google
- [Cloud API Registry Tool Governance](https://cloud.google.com/blog/products/ai-machine-learning/new-enhanced-tool-governance-in-vertex-ai-agent-builder)
- [Vertex AI Agent Builder Overview](https://docs.cloud.google.com/agent-builder/overview)
- [Gemini Enterprise Agent Platform](https://cloud.google.com/products/agent-builder)
- [Cloud Next 2026 Coverage](https://thenextweb.com/news/google-cloud-next-ai-agents-agentic-era)
- [Agent Governance Analysis](https://hyperframeresearch.com/2025/12/24/agent-governance-comes-of-age-google-cloud-reinforces-vertex-ai-guardrails/)

### Enterprise Platforms -- Microsoft
- [Agent Framework 1.0 Blog](https://devblogs.microsoft.com/agent-framework/microsoft-agent-framework-version-1-0/)
- [Agent Framework Overview](https://learn.microsoft.com/en-us/agent-framework/overview/)
- [Visual Studio Magazine Coverage](https://visualstudiomagazine.com/articles/2026/04/06/microsoft-ships-production-ready-agent-framework-1-0-for-net-and-python.aspx)
- [AutoGen Migration Guide](https://learn.microsoft.com/en-us/agent-framework/migration-guide/from-autogen/)
- [MCP + A2A Convergence Analysis](https://byteiota.com/microsoft-agent-framework-1-0-ships-mcp-a2a-converge/)
- [European AI & Cloud Summit Analysis](https://cloudsummit.eu/blog/microsoft-agent-framework-production-ready-convergence-autogen-semantic-kernel)

### Enterprise Platforms -- Salesforce
- [Salesforce Agentforce](https://www.salesforce.com/agentforce/)
- [A2A Protocol Page](https://www.salesforce.com/agentforce/ai-agents/agent2agent-protocol/)
- [A2A Architecture Guide](https://www.salesforceben.com/how-to-design-salesforce-agent-to-agent-a2a-architecture/)
- [AI Agent Integrations](https://www.salesforce.com/agentforce/ai-agent-integrations/)
- [Agentforce Maintenance Guide](https://www.girikon.com/blog/salesforce-agentforce-a-step-by-step-maintenance-guide-in-2026/)
- [FY26 Q4 Highlights](https://www.salesforce.com/news/stories/fy26-q4-highlights/)

### Open Source Platforms
- [LangGraph](https://www.langchain.com/langgraph) | [GitHub](https://github.com/langchain-ai/langgraph)
- [LangSmith Observability](https://www.langchain.com/langsmith/observability)
- [LangGraph Platform GA](https://www.langchain.com/blog/langgraph-platform-ga)
- [CrewAI](https://crewai.com/) | [CrewAI Tools](https://docs.crewai.com/en/concepts/tools)
- [BeeAI](https://beeai.dev/) | [Agent Stack GitHub](https://github.com/i-am-bee/agentstack)
- [Introducing Agent Stack](https://beeai.dev/blog/introducing-agent-stack)
- [BeeAI A2A Integration](https://a2aprotocol.ai/blog/beeai-a2a-acp)
- [AG2 GitHub](https://github.com/ag2ai/ag2)

### Kubernetes-Native Agent Platforms
- [kagent](https://kagent.dev/) | [GitHub](https://github.com/kagent-dev/kagent)
- [Kagenti](https://kagenti.github.io/.github/)
- [Red Hat: Zero-Trust Agents on Kubernetes](https://next.redhat.com/2026/03/05/zero-trust-ai-agents-on-kubernetes-what-i-learned-deploying-multi-agent-systems-on-kagenti/)
- [kagent vs. Kagenti Analysis](https://github.com/redhat-et/agent-orchestration/issues/13)

### Market Analysis
- [MarketsandMarkets: AI Agents Market Report 2025-2030](https://www.marketsandmarkets.com/Market-Reports/ai-agents-market-15761548.html)
- [MarketsandMarkets: Agentic AI Market Report 2025-2032](https://www.marketsandmarkets.com/Market-Reports/agentic-ai-market-208190735.html)
- [Gartner: Guardian Agents 10-15% of Market by 2030](https://www.gartner.com/en/newsroom/press-releases/2025-06-11-gartner-predicts-that-guardian-agents-will-capture-10-15-percent-of-the-agentic-ai-market-by-2030)
- [Gartner: SCM with Agentic AI to $53B by 2030](https://www.gartner.com/en/newsroom/press-releases/2026-04-07-gartner-forecasts-supply-chain-management-software-with-agentic-ai-will-grow-to-53-billion-in-spend-by-2030)
- [Gartner: Data and Analytics Predictions 2026](https://www.gartner.com/en/newsroom/press-releases/2026-03-11-gartner-announces-top-predictions-for-data-and-analytics-in-2026)
- [Agentic AI Adoption Rates, ROI & Market Trends](https://onereach.ai/blog/agentic-ai-adoption-rates-roi-market-trends/)
- [Enterprise AI Agent Orchestration April 2026 Playbook](https://www.fifthrow.com/blog/ai-agent-orchestration-goes-enterprise-the-april-2026-playbook-for-systematic-innovation-risk-and-value-at-scale)

### Framework Comparisons
- [LangGraph vs CrewAI 2026](https://redwerk.com/blog/langgraph-vs-crewai/)
- [Best Multi-Agent Frameworks 2026](https://gurusup.com/blog/best-multi-agent-frameworks-2026)
- [Definitive Guide to Agentic Frameworks 2026](https://blog.softmaxdata.com/definitive-guide-to-agentic-frameworks-in-2026-langgraph-crewai-ag2-openai-and-more/)
- [MCP + A2A + CrewAI Production 2026](https://47billion.com/blog/ai-agents-in-production-frameworks-protocols-and-what-actually-works-in-2026/)
