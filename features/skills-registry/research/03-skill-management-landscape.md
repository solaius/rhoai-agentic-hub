---
title: AI Skill Management Landscape Survey
description: Survey of existing platforms, tools, and solutions for AI skill management informing the RHOAI Skills Registry design.
source: ai-asset-registry/skills/skills-registry/research/03-skill-management-landscape.md (as of 2026-07-05)
timestamp: 2026-07-06
review_after: 2026-08-05
---

# AI Skill Management Landscape Survey

> **Date**: 2026-04-15
> **Author**: Peter Double (Principal PM - MCP)
> **Purpose**: Comprehensive survey of existing platforms, tools, and solutions for AI skill management to inform the RHOAI Skills Registry design.

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Enterprise AI Platforms](#1-enterprise-ai-platforms-with-skill-management)
3. [Open Source Skill Registries](#2-open-source-skill-registries-and-catalogs)
4. [Agent Orchestration Platforms](#3-agent-orchestration-platforms)
5. [Developer Tool Ecosystem Analogies](#4-developer-tool-ecosystem-analogies)
6. [Emerging Standards](#5-emerging-standards)
7. [Feature Comparison Matrix](#6-feature-comparison-matrix)
8. [Key Takeaways for RHOAI Skills Registry](#7-key-takeaways-for-rhoai-skills-registry)
9. [Sources](#sources)

---

## Executive Summary

The AI skill management landscape has undergone rapid transformation in 2025-2026. Several key trends emerge:

1. **Skills are the new packages**: JFrog, OpenClaw/ClawHub, and the Agent Skills specification all treat skills as first-class software artifacts requiring packaging, versioning, and supply chain security.

2. **Convergence on open standards**: The Agent Skills specification (SKILL.md) launched by Anthropic in December 2025 has been adopted by OpenAI Codex, Google Gemini CLI, GitHub Copilot, and others. MCP Registry specifications are being standardized through the Agentic AI Foundation (AAIF).

3. **Enterprise governance is the differentiator**: While open ecosystems (ClawHub, LangChain Hub) focus on discovery and sharing, enterprise platforms (IBM watsonx, Salesforce Agentforce, AWS AgentCore, JFrog) emphasize governance, approval workflows, security scanning, and audit trails.

4. **OCI containers as the distribution standard**: Docker, JFrog, and the cloud providers are converging on OCI artifacts as the standard packaging and distribution format for AI models, skills, and MCP servers.

5. **Security is a first-order concern**: The ClawHub security crisis (1,467 malicious skills discovered) demonstrated that AI skill registries face the same supply chain risks as npm/PyPI, but with added prompt injection vectors.

---

## 1. Enterprise AI Platforms with Skill Management

### Microsoft Semantic Kernel / Copilot Studio / Agent Framework

**Approach**: Plugin-based architecture with bidirectional integration between code-first (Semantic Kernel) and low-code (Copilot Studio) environments. As of late 2025, Microsoft merged Semantic Kernel and AutoGen into the unified **Microsoft Agent Framework** (GA targeted Q1 2026).

**Skill/Plugin Management Features**:
- **Plugin System**: Reusable AI "skills" or "plugins" that encapsulate specific capabilities. Plugins can be composed together into workflows.
- **Copilot Studio Skill Registration**: Register skills via URL-based manifest (`API_URL/manifest`). Skills become nodes in topic flows.
- **Prebuilt Plugins**: Contacts, Messages, Calendar, DriveItems, M365 Copilot plugins available out of the box.
- **MCP Support**: Microsoft joined the MCP Steering Committee in May 2025, contributing authorization specs and registry service designs for dynamic tool discovery.
- **Reusable Skills**: The Agent Framework supports modular Skills to standardize automation across projects.

| Feature | Status |
|---------|--------|
| Discovery/Search | Via Copilot Studio UI and plugin import |
| Versioning | Semantic versioning via Agent Framework |
| Governance | Enterprise-grade via Azure AD integration |
| Security | Prompt injection detection, content filtering, audit logging |
| Dependency Management | Plugin composition model |
| Composition | Plugins composable in topic flows and workflows |
| Lifecycle Management | Full SDLC via Azure DevOps integration |
| Analytics | Azure Monitor integration |
| Multi-tenant | Yes, via Azure AD / M365 tenants |

**Docs**: [Microsoft Agent Framework Overview](https://learn.microsoft.com/en-us/agent-framework/overview/) | [Semantic Kernel Overview](https://learn.microsoft.com/en-us/semantic-kernel/overview/)

---

### Google Vertex AI Agent Builder

**Approach**: Full-stack agent platform with a new **Cloud API Registry** integration for centralized tool governance. Uses Agent Development Kit (ADK) for code-first development and Agent Designer for low-code.

**Skill/Tool Management Features**:
- **Cloud API Registry**: Private catalog for administrators to curate which tools (including MCP servers) are approved for production use. Prevents "shadow AI" tool sprawl.
- **MCP Server Support**: Pre-built MCP tools for Google services (BigQuery, Maps) plus custom MCP server registration via Apigee.
- **ApiRegistry Object**: ADK introduces a new `ApiRegistry` object for developers to leverage managed tools programmatically.
- **Agent Engine**: GA for sessions, memory bank; supports A2A protocol, bidirectional streaming.
- **Security**: Agent identity via IAM, VPC Service Controls, threat detection via Security Command Center.
- **Discovery**: `gcloud beta api-registry mcp servers list` for CLI-based tool discovery.

| Feature | Status |
|---------|--------|
| Discovery/Search | Cloud API Registry in console + CLI |
| Versioning | Via ADK and Agent Engine versioning |
| Governance | Cloud API Registry admin controls |
| Security | IAM, VPC Service Controls, threat detection |
| Dependency Management | API dependencies tracked in Apigee |
| Composition | Multi-agent via A2A protocol |
| Lifecycle Management | Agent Engine sessions/memory |
| Analytics | Built-in monitoring, cost tracking |
| Multi-tenant | Yes, via GCP projects/organizations |

**Docs**: [Vertex AI Agent Builder](https://cloud.google.com/products/agent-builder) | [Cloud API Registry Tool Governance](https://cloud.google.com/blog/products/ai-machine-learning/new-enhanced-tool-governance-in-vertex-ai-agent-builder)

---

### AWS Bedrock Agents / AgentCore

**Approach**: Action group-based tool model with a new **Agent Registry** (preview April 2026) and **AgentCore Policy** (GA March 2026) for governance.

**Skill/Tool Management Features**:
- **Action Groups**: Define agent capabilities via OpenAPI schemas or function details. Execution via Lambda, return-control, or inline code.
- **Agent Registry** (Preview): Centralized catalog for registering, discovering, and governing agents, MCP tools, skills, and custom resources. Supports multi-framework, multi-cloud.
- **Three-persona model**: Admin (infrastructure), Publisher (registration), Consumer (discovery/use).
- **URL-based discovery**: Automatically retrieves metadata from live MCP servers or agent endpoints.
- **AgentCore Policy** (GA): Cedar-based policy language for fine-grained access control. Intercepts all agent traffic through gateways. Supports natural language policy authoring.
- **Security**: IAM policies, OAuth with JWT authorizers, PrivateLink, VPC endpoints, CloudTrail audit trails.

| Feature | Status |
|---------|--------|
| Discovery/Search | Agent Registry with semantic + keyword search |
| Versioning | Action group versioning |
| Governance | AgentCore Policy (Cedar-based), approval workflows |
| Security | IAM, OAuth, PrivateLink, automated scanning |
| Dependency Management | Action group composition |
| Composition | Multi-agent collaboration |
| Lifecycle Management | Agent Registry lifecycle states |
| Analytics | CloudWatch metrics and logs |
| Multi-tenant | Yes, via AWS accounts/organizations |

**Docs**: [AWS Agent Registry Preview](https://aws.amazon.com/about-aws/whats-new/2026/04/aws-agent-registry-in-agentcore-preview/) | [AgentCore Policy](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/policy.html)

---

### IBM watsonx Orchestrate

**Approach**: Framework-agnostic agent catalog with 100+ prebuilt agents and 400+ tools. Strongest enterprise catalog story with partner ecosystem (Agent Connect).

**Skill/Tool Management Features**:
- **Agent Catalog**: Browse prebuilt agents, partner contributions, and custom builds. Each listing shows APIs, tools, and workflows.
- **Framework-Agnostic**: Any agent, any framework. Not tied to a single SDK, LLM, or cloud.
- **Agent Connect**: Partner program for ISVs to integrate agents and list them in the catalog.
- **Validated & Connected**: Every agent is validated, observable by design, ready to connect with 700+ enterprise systems (Microsoft 365, Salesforce, SAP, Workday, AWS).
- **Low-Code to Pro-Code**: Low-code agent builder plus SDK with tools, documentation, and code samples.
- **Multi-Agent Orchestration**: Agents wired into orchestration engine for end-to-end workflows spanning domains, systems, and teams.

| Feature | Status |
|---------|--------|
| Discovery/Search | Agent Catalog with browsing and search |
| Versioning | Agent lifecycle management |
| Governance | Centralized catalog prevents sprawl; built-in compliance |
| Security | Built-in security, governance, and compliance |
| Dependency Management | Proven connectors for enterprise systems |
| Composition | Multi-agent orchestration engine |
| Lifecycle Management | Full lifecycle from build to deploy to manage |
| Analytics | Observable by design |
| Multi-tenant | Yes, SaaS or on-premises deployment |

**Docs**: [IBM watsonx Orchestrate Agent Catalog](https://www.ibm.com/products/watsonx-orchestrate/skills-studio) | [Agent Catalog Blog](https://www.ibm.com/new/product-blog/any-agent-any-framework-inside-the-ibm-watsonx-orchestrate-agent-catalog)

---

### Salesforce Agentforce (formerly Einstein)

**Approach**: Topics and Actions model with Agent Builder. Rebranded from Einstein to Agentforce in January 2025. Focused on CRM-native skill management.

**Skill/Tool Management Features**:
- **Agent Builder**: Low-code builder using Topics (job definitions), natural language instructions, and Actions (automation logic).
- **Action Library**: Actions implemented via Flow or Apex. Recommended limits: 10-15 topics per agent, 15 actions per topic.
- **Agentforce Script** (Spring '26): Hybrid reasoning combining deterministic workflows with LLM reasoning.
- **Agent Lifecycle**: Systematic framework with daily monitoring, weekly validation, monthly regression, quarterly reviews, annual upgrade planning.
- **Governance**: Agent inventory, defined ownership, version control, least-privilege access.

| Feature | Status |
|---------|--------|
| Discovery/Search | Agent Builder library |
| Versioning | Version control for agents and actions |
| Governance | Agent inventory, ownership, approval workflows |
| Security | Least-privilege access, compliance monitoring |
| Dependency Management | Flow and Apex dependencies |
| Composition | Multi-agent collaboration |
| Lifecycle Management | Comprehensive maintenance framework |
| Analytics | Action/output logging for compliance |
| Multi-tenant | Yes, native to Salesforce platform |

**Docs**: [Salesforce Agentforce](https://www.salesforce.com/agentforce/) | [Agentforce Maintenance Guide](https://www.girikon.com/blog/salesforce-agentforce-a-step-by-step-maintenance-guide-in-2026/)

---

### ServiceNow AI Agent Studio

**Approach**: 300+ AI Skills across 30+ product modules organized under the Now Assist ecosystem. Deep ITSM, ITOM, CSM, HR, and GRC coverage.

**Skill/Tool Management Features**:
- **AI Skills**: Discrete, reusable GenAI capabilities (e.g., incident summarization, resolution notes generation). 300+ skills across 30+ modules.
- **AI Agents**: Autonomous entities that orchestrate multiple skills to investigate and act.
- **Agentic Workflows**: Chain skills and agents into end-to-end business outcomes.
- **AI Agent Orchestrator**: Guides teams of AI agents to collaborate.
- **AI Agent Fabric**: Unify third-party agents/tools from any platform.
- **AI Control Tower**: Centralized hub for managing, monitoring, and optimizing any AI.
- **Categories**: Content/Record Skills, Analysis/Recommendation Skills, across ITSM, ITOM, CSM, HR, GRC, SecOps, FSM.

| Feature | Status |
|---------|--------|
| Discovery/Search | Skill catalog across 30+ modules |
| Versioning | Platform release-based versioning |
| Governance | AI Control Tower for centralized governance |
| Security | Pro Plus / Enterprise Plus SKU gating |
| Dependency Management | Skill-to-module dependencies |
| Composition | Agentic Workflows chaining skills |
| Lifecycle Management | Platform release lifecycle |
| Analytics | Consumption-based licensing tracking |
| Multi-tenant | Yes, ServiceNow platform multi-tenancy |

**Docs**: [ServiceNow AI Agents](https://www.servicenow.com/products/ai-agents.html) | [AI Skills Guide](https://teivasystems.com/blog/servicenow-ai-skills-agents-workflows-complete-guide/)

---

## 2. Open Source Skill Registries and Catalogs

### OpenClaw / ClawHub

**The largest open skill registry as of 2026.** OpenClaw is an MIT-licensed AI agent framework; ClawHub is its public skill registry with 18,140+ skills across 11 categories.

**Key Features**:
- **Skill Format**: SKILL.md file with YAML frontmatter + markdown instructions, plus optional configs, scripts, and metadata.
- **Versioning**: SemVer with changelogs and tags (including `latest`). Lock file (`.clawhub/lock.json`) for reproducibility.
- **Discovery**: Vector search (OpenAI embeddings) for semantic skill discovery.
- **Security**: Post-crisis measures include automated scanning, author verification badges, code signing for new submissions. VirusTotal integration.
- **Governance**: GitHub account age requirement (1 week), community reporting, moderation hooks.
- **Known Risks**: 12-20% of skills found to be malicious in security audits. CVE-2026-25253 (local RCE). "ClawHavoc" attack in Feb 2026.

**Docs**: [ClawHub](https://docs.openclaw.ai/tools/clawhub) | [ClawHub GitHub](https://github.com/openclaw/clawhub)

---

### JFrog Agent Skills Registry

**Enterprise-grade skill supply chain security.** Part of JFrog AI Catalog, validated with NVIDIA Agent Toolkit.

**Key Features**:
- **Centralized System of Record**: For MCPs, models, agent skills, and agentic binary assets.
- **Automated Security Scanning**: Scans, verifies, and signs all AI skills upon upload. Detects vulnerabilities, malicious payloads, and compliance risks.
- **Policy-Driven Governance**: Strict approval workflows; developers and agents can only access permitted, verified skills.
- **NVIDIA Partnership**: Supports NVIDIA Agent Toolkit (NemoClaw), AI-Q Blueprint.
- **MCP Registry**: Separate JFrog MCP Registry for governing MCP servers.
- **Provenance**: Cryptographic provenance for all artifacts.

**Docs**: [JFrog Agent Skills Registry](https://jfrog.com/blog/agent-skills-new-ai-packages/) | [JFrog AI Catalog](https://jfrog.com/)

---

### OneSkill

**Open directory for agent artifacts.** Automatically indexes skills, MCP servers, Cursor rules, n8n nodes from GitHub. Compatible with 38+ agent platforms.

**Docs**: [OneSkill](https://oneskill.dev/)

---

### OpenAI GPT Store / Actions -> Apps + Skills

**Evolution**: GPT Store (Jan 2024) -> App Directory (Dec 2025) -> Skills ("Hazelnut" project, expected 2026).

**Key Features**:
- **App Directory**: Third-party apps with Apps SDK. Public submissions via developer portal.
- **Skills (Emerging)**: Modular abilities that can be combined automatically. Portable across web, desktop, and API. Slash-command interactions, Skill editor, one-click conversion from GPTs.
- **Codex Skills**: Agent skills for Codex CLI. Packages instructions, resources, and scripts for task-specific workflows.
- **Cross-Platform**: Adopted the Agent Skills (SKILL.md) open standard.

**Docs**: [OpenAI Codex Skills](https://developers.openai.com/codex/skills) | [OpenAI Platform](https://platform.openai.com/)

---

### Hugging Face Hub / Spaces

**The "GitHub for ML"** — a model for how a community-driven artifact registry can work at scale.

**Key Features**:
- **Scale**: 2M+ models, 500K+ datasets, 1M+ Spaces (demo apps).
- **Hub**: Central repository with versioning, metadata, documentation, public/private hosting.
- **Spaces**: Interactive demos built with Gradio/Streamlit. Browsable and forkable.
- **Enterprise**: Private hubs, access controls, SOC 2 compliance, cloud provider integrations.
- **Community**: Open-source libraries, contributions, discussions, model cards.
- **Pricing**: Free tier for public use; PRO at $9/month, Team at $20/user/month.

**Relevance to Skills**: Hugging Face demonstrates a successful model for community-driven artifact discovery, sharing, and versioning that a skills registry could emulate. The model card concept (standardized metadata) is directly analogous to skill metadata.

**Docs**: [Hugging Face Hub](https://huggingface.co/) | [Hugging Face Spaces](https://huggingface.co/spaces)

---

### SkillForge, SkillNet, OpenSpace

Emerging open-source projects for skill creation and evolution:
- **SkillForge**: Generates valid SKILL.md files from natural language descriptions with security analysis (20+ rules).
- **SkillNet**: Positions skills as "portable procedural capability packages" using the AgentSkills specification.
- **OpenSpace**: Self-evolving skill engine that captures and reuses task patterns. 46% token reduction demonstrated.

---

## 3. Agent Orchestration Platforms

### CrewAI

**Role-based multi-agent orchestration** with first-class tool objects.

**Tool Management**:
- Tools are first-class objects: define once, any agent can use. Modular and scalable.
- Enterprise Tools Repository with pre-built connectors for business systems.
- Built-in error handling and caching for all tools.
- MCP integration (CrewAI 2.1+) for connecting to external tool servers.
- Agent-to-Agent (A2A) task execution in 2026.
- Event hierarchy for deterministic, traceable workflows.

**Docs**: [CrewAI Tools](https://docs.crewai.com/en/concepts/tools)

---

### LangChain Hub / LangSmith

**Prompt and tool management** with version control, environments, and observability.

**Key Features**:
- **Prompt Hub**: Centralized storage with commit-hash-based versioning (Git-like).
- **Environments**: Staging and Production promotion for commit tags.
- **Access Control**: Prompt owners control promotion and deletion.
- **Playground**: Visual editor for side-by-side testing across models.
- **SDK Integration**: Push/pull prompts programmatically. Webhook support for CI/CD triggers.
- **Public Hub**: Community-contributed prompts (unverified).
- **Tracing**: Deep observability showing how prompts perform in context.
- **Limitations**: Linear versioning only (no branching), no automated evaluation triggers, no approval workflows.

**Docs**: [LangSmith Prompt Management](https://docs.langchain.com/langsmith/manage-prompts) | [LangChain Hub](https://blog.langchain.com/langchain-prompt-hub/)

---

### Composio

**Developer-first integration platform** for AI agent tool management.

**Key Features**:
- **850+ Pre-built Connectors**: Unified framework for Slack, GitHub, Notion, Gmail, Salesforce, etc.
- **Managed Authentication**: Handles OAuth 2.0 flows and API key management end-to-end.
- **MCP Support**: Universal MCP server (Rube) for cross-client tool connectivity.
- **Smart Tool Routing**: Automatic tool selection with context optimization.
- **Security**: SOC 2 Type II, least-privilege access, token isolation, audit trails.
- **Framework Support**: Works with 25+ frameworks (LangChain, CrewAI, AutoGen, OpenAI, Anthropic).
- **Limitation**: Closed-source tools; only supports tool calls (no data syncs, webhooks, batch writes).

**Docs**: [Composio](https://composio.dev/) | [Composio Docs](https://docs.composio.dev/docs)

---

### Toolhouse

**App-store model for AI tools** with Backend-as-a-Service.

**Key Features**:
- **Tool Store**: Pre-built AI tools (RAG, code execution, web search) installable with one click.
- **Universal SDK**: 3 lines of code integration across all major LLMs.
- **Debugging**: Inspect every tool call, fork agents to test versions.
- **BaaS**: Pre-loaded features (RAG, evals, memory, edge functions, storage).

**Docs**: [Toolhouse](https://www.toolify.ai/tool/toolhouse)

---

### Kong MCP Registry

**Enterprise MCP tool governance** integrated with existing API management.

**Key Features**:
- **MCP Registry**: Enterprise directory within Kong Konnect Catalog for registering, discovering, and governing MCP servers.
- **Standards Compliance**: Implements the official MCP Registry OpenAPI specification (AAIF standard).
- **API Linkage**: Links MCP servers to underlying APIs for deeper visibility and governance.
- **Context Mesh**: Auto-discovers enterprise APIs, transforms them into agent tools, deploys with runtime governance.
- **Dynamic Discovery**: Agents discover tools programmatically via registry endpoint instead of hardcoded configurations.

**Docs**: [Kong MCP Registry](https://konghq.com/company/press-room/press-release/kong-introduces-mcp-registry) | [Dynamic Tool Discovery](https://konghq.com/blog/engineering/mcp-registry-dynamic-tool-discovery)

---

## 4. Developer Tool Ecosystem Analogies

### npm / PyPI (Package Registries)

**Relevance**: The most mature model for artifact packaging, versioning, and distribution.

| Feature | npm | PyPI | Skill Registry Lesson |
|---------|-----|------|----------------------|
| Versioning | SemVer with lockfiles | SemVer with requirements.txt/poetry.lock | Skills need SemVer + lockfiles for reproducibility |
| Dependency Mgmt | `dependencies` / `devDependencies` / nested resolution | `install_requires` / poetry / pip-tools | Skills need declared dependencies on other skills, MCP servers, models |
| Security | `npm audit`, Sigstore signing, 2FA for publishing | `pip-audit`, Trusted Publishers (OIDC), Sigstore | Supply chain security is non-negotiable |
| Private Registries | Verdaccio, Artifactory, AWS CodeArtifact | devpi, Artifactory, AWS CodeArtifact | Enterprise needs private skill registries |
| Scoping | `@org/package` scoping | No native scoping | Organizational scoping helps prevent name squatting |
| Governance | Working groups (OpenSSF, Node.js Package Maintenance) | Python Packaging Authority | Skills need governance bodies |

---

### Docker Hub / OCI Registries

**Relevance**: The emerging standard for packaging AI skills as OCI artifacts.

| Feature | Docker Hub / OCI | Skill Registry Lesson |
|---------|-----------------|----------------------|
| Packaging | OCI container images and artifacts | Skills, models, MCP servers can all be OCI artifacts |
| Versioning | Tags + immutable digests | Pin specific versions; avoid floating `latest` |
| Distribution | Pull/push to any OCI-compatible registry | Universal distribution via standard registries |
| Signing | Docker Content Trust, Sigstore/cosign | Cryptographic signing for skill provenance |
| Governance | Registry Access Management (RAM) | Policy-based access controls |
| Scanning | Integrated vulnerability scanning | Automated security scanning on upload |
| Ecosystem | Docker Hub, Quay, Artifactory, ECR, GCR, ACR | Leverage existing enterprise registry infrastructure |

**Key Insight**: Docker Model Runner already packages LLMs as OCI artifacts. The same model extends naturally to skills and MCP servers.

---

### Helm Charts (Kubernetes Packaging)

**Relevance**: Declarative packaging with values-based configuration.

| Feature | Helm | Skill Registry Lesson |
|---------|------|----------------------|
| Packaging | Chart archives with templates + values | Skills could use similar template/values separation |
| Versioning | Chart version + app version | Skill version vs. underlying tool version |
| Repositories | OCI-based registries, ChartMuseum | Leverage OCI for skill distribution |
| Dependencies | `Chart.yaml` dependencies with version constraints | Skills need dependency declarations |
| Configuration | `values.yaml` with overrides | Skills need configurable parameters |
| Testing | `helm test`, `helm lint` | Skills need validation and testing frameworks |

---

### Terraform Registry

**Relevance**: Module registry with provider/consumer model.

| Feature | Terraform Registry | Skill Registry Lesson |
|---------|-------------------|----------------------|
| Discovery | Search by provider, category, keyword | Skills need rich search and categorization |
| Versioning | SemVer with pinning | Pin skill versions for reproducibility |
| Documentation | Auto-generated from code | Auto-generate skill docs from SKILL.md |
| Providers | Verified vs. community providers | Verified vs. community skills |
| Modules | Reusable, composable infrastructure modules | Reusable, composable skill modules |

---

### VS Code Extensions Marketplace

**Relevance**: The most mature model for extension/plugin governance and trust.

| Feature | VS Code Marketplace | Skill Registry Lesson |
|---------|-------------------|----------------------|
| Security | Multi-layer malware scanning, dynamic detection, secret scanning | Skills need automated malware and prompt injection scanning |
| Trust | Publisher verification badges, trust prompts, workspace trust | Skills need publisher verification and trust levels |
| Signing | Signature verification on install | Cryptographic signing for all skills |
| Enterprise | Extension allowlisting, version pinning, private marketplace | Enterprise skill allowlists and private registries |
| Impersonation | Name reservation, typosquatting prevention | Protect against skill name squatting |
| Community | Report a concern, community moderation | Community reporting for malicious skills |
| Versioning | SemVer, pre-release versions | Skills need pre-release/beta channels |

---

## 5. Emerging Standards

### Agent Skills Specification (SKILL.md)

The open standard published by Anthropic at [agentskills.io](https://agentskills.io/specification) in December 2025. Adopted by OpenAI, Google, GitHub, and community tools.

**Key Elements**:
- **Format**: Directory with SKILL.md file (YAML frontmatter + markdown instructions)
- **Frontmatter**: Required `name` and `description`; optional metadata fields
- **Progressive Disclosure**: Metadata loaded at startup; full instructions on demand; resources loaded during execution
- **Size Guidelines**: < 5,000 tokens for instructions; < 500 lines for SKILL.md
- **Supporting Files**: `scripts/`, `references/`, `assets/` directories
- **Naming**: Lowercase, hyphens, max 64 chars
- **Web Discovery**: `/.well-known/skills/default/skill.md` convention

**Platform Support**: Claude Code, OpenAI Codex CLI, Google Gemini CLI, GitHub Copilot (VS Code), Cursor, Cline, Windsurf, OpenCode.

### MCP Registry Specification

Donated by Anthropic to the Agentic AI Foundation (AAIF) in December 2025. Defines an OpenAPI-based specification for MCP server registries.

**Implementations**: Kong MCP Registry, AWS Agent Registry, Google Cloud API Registry, JFrog MCP Registry.

### OCI Artifacts for AI

Docker Model Runner and the broader OCI ecosystem are standardizing on OCI artifacts for packaging AI models, skills, and tools. This enables leveraging existing container registry infrastructure for AI artifact distribution.

---

## 6. Feature Comparison Matrix

### Enterprise Platforms

| Feature | Microsoft Agent Framework | Google Vertex AI | AWS AgentCore | IBM watsonx Orchestrate | Salesforce Agentforce | ServiceNow AI Agent Studio |
|---------|--------------------------|-----------------|---------------|------------------------|-----------------------|---------------------------|
| **Discovery/Search** | Plugin import, Copilot Studio UI | Cloud API Registry, CLI | Agent Registry (semantic + keyword) | Agent Catalog browsing | Agent Builder library | 300+ skills across 30+ modules |
| **Versioning** | SemVer via framework | ADK versioning | Action group versioning | Agent lifecycle | Version control | Platform release-based |
| **Governance** | Azure AD, MCP steering committee | Admin tool controls, IAM | Cedar-based policy, approval workflows | Validated catalog, Agent Connect | Agent inventory, ownership | AI Control Tower |
| **Security** | Prompt injection detection, audit logging | IAM, VPC SC, threat detection | IAM, OAuth, PrivateLink, CloudTrail | Built-in compliance | Least-privilege, compliance | SKU-gated access |
| **Dependencies** | Plugin composition | API dependencies (Apigee) | Action group composition | 700+ enterprise connectors | Flow/Apex dependencies | Skill-to-module |
| **Composition** | Topic flows, workflows | Multi-agent (A2A) | Multi-agent collaboration | Multi-agent orchestration | Multi-agent | Agentic Workflows |
| **Lifecycle** | Full SDLC (Azure DevOps) | Agent Engine sessions/memory | Registry lifecycle states | Build-deploy-manage | Maintenance framework | Platform releases |
| **Analytics** | Azure Monitor | Built-in monitoring | CloudWatch | Observable by design | Action/output logging | Consumption tracking |
| **Multi-tenant** | Azure AD / M365 | GCP projects/orgs | AWS accounts/orgs | SaaS or on-prem | Salesforce platform | ServiceNow platform |
| **MCP Support** | Yes (steering committee member) | Yes (Cloud API Registry) | Yes (Agent Registry) | Partial | No | No |
| **Open Standards** | MCP, A2A, OpenAPI | MCP, A2A, ADK | MCP, Cedar | Any framework | Proprietary | Proprietary |
| **Pricing Model** | Per-seat (M365/Azure) | Per-use (Agent Engine) | Per-use (consumption) | $500-custom/month | $2/conversation or per-seat | Pro Plus / Enterprise Plus SKU |

### Open Source / Developer Platforms

| Feature | OpenClaw ClawHub | JFrog Agent Skills | LangChain Hub | Composio | Toolhouse | Kong MCP Registry |
|---------|------------------|-------------------|---------------|----------|-----------|-------------------|
| **Discovery/Search** | Vector search (semantic) | Catalog browsing | Prompt search by name/handle | Smart tool routing | Tool Store | MCP Registry + Context Mesh |
| **Versioning** | SemVer, changelogs, tags, lockfile | Full artifact versioning | Commit-hash-based | N/A (connector-based) | Agent version forking | Registry versioning |
| **Governance** | Community moderation, age gates | Policy-driven approval workflows | Prompt owners, environments | SOC 2 Type II | N/A | Enterprise API governance |
| **Security** | VirusTotal scanning, post-crisis badges | Automated scanning, signing, provenance | N/A | SOC 2, token isolation, audit | N/A | Inherited API policies |
| **Dependencies** | Declared in frontmatter | Full dependency tracking | N/A | 850+ connectors | Pre-built integrations | API dependency mapping |
| **Composition** | Multi-skill loading | Artifact composition | Prompt chaining | Tool chaining | Agent composition | Context Mesh pipelines |
| **Lifecycle** | Publish, soft-delete, restore | Full artifact lifecycle | Push, pull, delete | Connection lifecycle | Deploy via CLI | Full API lifecycle |
| **Analytics** | Install counts | Usage analytics | Trace-based evaluation | Execution analytics | Token usage optimization | API analytics |
| **Multi-tenant** | Per-user | Enterprise multi-tenant | Organization-based | Per-connection | Per-account | Kong Konnect multi-tenant |
| **MCP Support** | No | Yes (MCP Registry) | Via LangChain MCP adapter | Yes (Rube universal MCP) | No | Yes (native) |
| **Pricing** | Free (open source) | Enterprise licensing | Free to $39/seat/month | Free tier + usage | Free tier + usage | Kong Konnect pricing |

---

## 7. Key Takeaways for RHOAI Skills Registry

### Must-Have Features (Based on Market Consensus)

1. **Standardized Skill Format**: Adopt or extend the Agent Skills specification (SKILL.md). The industry is converging on this format. Consider how it maps to OCI artifact packaging for distribution.

2. **Versioning with SemVer**: Every platform uses semantic versioning. Support lockfiles for reproducibility (like ClawHub's `.clawhub/lock.json` or npm's `package-lock.json`).

3. **Security Scanning**: The ClawHub crisis proved that AI skill registries face supply chain attacks identical to npm/PyPI, plus new vectors (prompt injection). Automated scanning on upload is non-negotiable. JFrog's approach (scan, verify, sign) is the gold standard.

4. **Governance and Approval Workflows**: Enterprise platforms (AWS AgentCore Policy, IBM watsonx, JFrog) all provide approval workflows. Cedar-based policy (AWS) or policy-driven governance (JFrog) are emerging patterns.

5. **Discovery (Semantic + Keyword)**: Vector-based semantic search (ClawHub, AWS Agent Registry) outperforms keyword-only search for finding relevant skills.

6. **MCP Integration**: MCP is the interop standard. The registry should be accessible as an MCP server itself (AWS Agent Registry pattern) and should register/govern MCP servers.

### Differentiating Features

7. **OCI Artifact Packaging**: Package skills as OCI artifacts to leverage existing container registry infrastructure (Quay, Artifactory). This aligns with Red Hat's container-first strategy and Docker's direction.

8. **Multi-Framework Support**: IBM watsonx's "any agent, any framework" approach prevents vendor lock-in. The registry should be framework-agnostic.

9. **Publisher Verification**: VS Code Marketplace's verified publisher badges and trust prompts translate directly to skill publishers. JFrog's cryptographic provenance adds supply chain assurance.

10. **Progressive Disclosure**: The Agent Skills spec's metadata-first loading model (metadata at startup, instructions on demand, resources during execution) is efficient for context management.

### Architecture Patterns to Consider

11. **Three-Persona Model** (AWS): Admin / Publisher / Consumer separation maps well to enterprise roles.

12. **API Registry Integration** (Google, Kong): Link skills to underlying APIs/MCP servers for dependency visibility and governance inheritance.

13. **Federated Discovery** (Kong Context Mesh): Auto-discover and register skills from existing infrastructure rather than requiring manual registration.

14. **Policy-as-Code** (AWS Cedar): External policy enforcement that doesn't require modifying skill code.

### Gaps in the Market

15. **No platform fully solves skill composition**: While multi-agent orchestration exists, declarative skill chaining/composition (like Helm chart dependencies) remains immature.

16. **No cross-platform skill portability**: Despite the Agent Skills spec, skills with platform-specific features require adaptation. A truly portable skill format needs more work.

17. **Testing frameworks are missing**: Unlike Helm (`helm test`), no standard framework exists for skill testing and validation.

18. **Lifecycle governance is nascent**: Salesforce's maintenance framework (daily/weekly/monthly/quarterly checks) is the most mature, but no platform automates skill health monitoring.

---

## Sources

### Enterprise Platforms
- [Microsoft Agent Framework Overview](https://learn.microsoft.com/en-us/agent-framework/overview/)
- [Semantic Kernel Overview](https://learn.microsoft.com/en-us/semantic-kernel/overview/)
- [Semantic Kernel & Copilot Studio Integration](https://devblogs.microsoft.com/semantic-kernel/guest-blog-semantic-kernel-and-copilot-studio-usage-series-part-1/)
- [Vertex AI Agent Builder](https://cloud.google.com/products/agent-builder)
- [Google Cloud API Registry Tool Governance](https://cloud.google.com/blog/products/ai-machine-learning/new-enhanced-tool-governance-in-vertex-ai-agent-builder)
- [Vertex AI Agent Builder Release Notes](https://docs.cloud.google.com/agent-builder/release-notes)
- [AWS Agent Registry Preview](https://aws.amazon.com/about-aws/whats-new/2026/04/aws-agent-registry-in-agentcore-preview/)
- [AWS Agent Registry Blog](https://aws.amazon.com/blogs/machine-learning/the-future-of-managing-agents-at-scale-aws-agent-registry-now-in-preview/)
- [AgentCore Policy GA](https://aws.amazon.com/about-aws/whats-new/2026/03/policy-amazon-bedrock-agentcore-generally-available/)
- [AgentCore Policy Documentation](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/policy.html)
- [AWS Bedrock Action Groups](https://docs.aws.amazon.com/bedrock/latest/userguide/agents-action-create.html)
- [IBM watsonx Orchestrate](https://www.ibm.com/products/watsonx-orchestrate)
- [IBM Agent Catalog Blog](https://www.ibm.com/new/product-blog/any-agent-any-framework-inside-the-ibm-watsonx-orchestrate-agent-catalog)
- [Salesforce Agentforce](https://www.salesforce.com/agentforce/)
- [Agentforce 2026 Product Guide](https://vantagepoint.io/blog/sf/the-complete-guide-to-salesforces-agentforce-ecosystem-understanding-the-full-product-portfolio-in-2026)
- [Agentforce Maintenance Guide](https://www.girikon.com/blog/salesforce-agentforce-a-step-by-step-maintenance-guide-in-2026/)
- [ServiceNow AI Agents](https://www.servicenow.com/products/ai-agents.html)
- [ServiceNow AI Skills Guide](https://teivasystems.com/blog/servicenow-ai-skills-agents-workflows-complete-guide/)
- [ServiceNow Agentic AI 2026](https://www.kellton.com/kellton-tech-blog/servicenow-agentic-ai-2026-guide)

### Open Source & Developer Platforms
- [OpenClaw ClawHub](https://docs.openclaw.ai/tools/clawhub)
- [ClawHub GitHub](https://github.com/openclaw/clawhub)
- [ClawHub Skill Format](https://github.com/openclaw/clawhub/blob/main/docs/skill-format.md)
- [ClawHub Security Guide](https://blink.new/blog/openclaw-clawhub-skills-safe-install-guide-2026)
- [JFrog Agent Skills Registry](https://jfrog.com/blog/agent-skills-new-ai-packages/)
- [JFrog + NVIDIA Partnership](https://www.businesswire.com/news/home/20260408282466/en/JFrog-Delivers-Trust-Layer-for-AI-Driven-Software-with-NVIDIA)
- [JFrog MCP Registry](https://techedgeai.com/jfrog-unveils-universal-mcp-registry-delivering-a-secure-system-of-record-for-the-ai-driven-software-supply-chain/)
- [OneSkill](https://oneskill.dev/)
- [OpenAI Codex Skills](https://developers.openai.com/codex/skills)
- [OpenAI App Directory & SDK](https://www.datastudios.org/post/chatgpt-app-directory-and-gpt-store-marketplace-launch-sdk-features-and-platform-evolution)
- [OpenAI Skills Feature](https://dig.watch/updates/chatgpt-may-move-beyond-gpts-as-openai-develops-new-skills-feature)
- [Hugging Face Hub](https://huggingface.co/)
- [Hugging Face Complete Guide 2026](https://www.techaimag.com/latest-hugging-face-models/hugging-face-complete-guide-2026-models-datasets-development)
- [SkillForge](https://github.com/calderbuild/skillforge)

### Agent Orchestration
- [CrewAI Tools](https://docs.crewai.com/en/concepts/tools)
- [CrewAI 2026 Review](https://aiagentslist.com/agents/crewai)
- [LangSmith Prompt Management](https://docs.langchain.com/langsmith/manage-prompts)
- [LangChain Hub Announcement](https://blog.langchain.com/langchain-prompt-hub/)
- [Composio](https://composio.dev/)
- [Composio GitHub](https://github.com/ComposioHQ/composio)
- [Composio 2026 AI Agent Report](https://composio.dev/blog/why-ai-agent-pilots-fail-2026-integration-roadmap)
- [Kong MCP Registry](https://konghq.com/company/press-room/press-release/kong-introduces-mcp-registry)
- [Kong Dynamic Tool Discovery](https://konghq.com/blog/engineering/mcp-registry-dynamic-tool-discovery)
- [Kong Context Mesh](https://konghq.com/company/press-room/press-release/kong-launches-context-mesh-to-connect-enterprise-data-to-ai-agents)

### Standards
- [Agent Skills Specification](https://agentskills.io/specification)
- [Agent Skills in VS Code](https://code.visualstudio.com/docs/copilot/customization/agent-skills)
- [Agent Skills (The New Stack)](https://thenewstack.io/agent-skills-anthropics-next-bid-to-define-ai-standards/)
- [SKILL.md Open Standard (Mintlify)](https://www.mintlify.com/blog/skill-md)

### Developer Ecosystem Analogies
- [VS Code Extension Security](https://developer.microsoft.com/blog/security-and-trust-in-visual-studio-marketplace)
- [VS Code Extension Runtime Security](https://code.visualstudio.com/docs/configure/extensions/extension-runtime-security)
- [VS Code Enterprise Extension Management](https://code.visualstudio.com/docs/enterprise/extensions)
- [Palantir VS Code Extension Governance](https://blog.palantir.com/managing-and-securing-vs-code-extensions-at-scale-b75b2cf72b02)
- [Docker OCI Artifacts for AI](https://www.docker.com/blog/oci-artifacts-for-ai-model-packaging/)
- [Docker Model Runner](https://www.docker.com/blog/introducing-docker-model-runner/)
- [npm Security Cheat Sheet (OWASP)](https://cheatsheetseries.owasp.org/cheatsheets/NPM_Security_Cheat_Sheet.html)
- [Package Management Landscape 2026](https://nesbitt.io/2026/01/03/the-package-management-landscape.html)
- [Red Hat: Containers for AI Workloads](https://www.redhat.com/en/blog/using-containers-bring-software-engineering-rigor-ai-workloads)
- [Terraform Registry](https://registry.terraform.io/)
