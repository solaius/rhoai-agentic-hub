---
title: Competitive Analysis — Skills & Agent Registries (August 2026)
description: Competitive landscape analysis for skills/agent registries showing rapid GA convergence, security crisis catalyzing governance, and strategic positioning opportunities for Red Hat
timestamp: 2026-08-04
lens: competitive
review_after: 2026-11-04
---

# Competitive Analysis — Skills & Agent Registries (August 2026)

## Executive Summary

The competitive landscape for skills and agent registries has undergone a dramatic transformation from April to August 2026. What was a fragmented preview market in April is now a battle-tested GA market shaped by three forcing functions:

1. **GA convergence**: AWS Agent Registry (preview April), IBM watsonx Orchestrate (GA May), Microsoft Agent Framework 1.0 (GA April), and Google Gemini Enterprise (rebranded April) all shipped production-ready registry capabilities within 90 days.

2. **Security crisis**: The OpenClaw/ClawHub supply chain attacks (341-800+ malicious skills, CVE-2026-25253) validated the governance thesis and accelerated enterprise demand for trusted registries. Organizations now treat skills as critical supply chain artifacts, not dev tools.

3. **Standards convergence**: MCP (Anthropic/Microsoft/Google/AWS steering committee), A2A Protocol (150+ orgs, Linux Foundation), and ARD spec (Google/Microsoft/Hugging Face) created interoperability foundations that shift competitive differentiation from protocol lock-in to governance depth and ecosystem velocity.

**Red Hat's window**: The hyperscalers are racing to GA but their registries are tightly coupled to their clouds (AWS Bedrock, Azure Agent 365, Google Gemini Enterprise). Red Hat's **hybrid-first, MLflow-native, Kubernetes-governed** approach is the only open architecture that spans on-prem, edge, and multi-cloud — a differentiation that matters more as EU AI Act enforcement begins August 2, 2026 and enterprises seek portable governance.

**Key threat**: Databricks Unity AI Gateway (announced DAIS June 2026) positions as "the MLflow company" with agents as first-class Unity Catalog entities, directly competing with Red Hat's MLflow-based approach. However, Databricks is cloud-native and lacks Red Hat's edge/disconnected story.

---

## Competitor Deep Dive

### 1. AWS — Agent Registry (Preview) + Cedar Policy (GA)

**Current State (August 2026)**

- **Agent Registry**: Preview as of April 2026, available in 5 AWS regions (US West Oregon, Asia Pacific Tokyo/Sydney, Europe Ireland, US East N. Virginia). A private, governed catalog for agents, tools, skills, MCP servers, and custom resources. Accessible via AgentCore Console UI, AWS CLI/SDK, and as an MCP server for IDE integration.

- **Cedar Policy**: Generally available as of March 3, 2026, in 13 AWS regions. Provides fine-grained, runtime controls for agent-tool interactions with natural language-to-Cedar policy authoring.

**Strategy**

AWS is betting on **Cedar-based policy as the differentiator**. Cedar is AWS's open-source policy language (used in Amazon Verified Permissions, AWS Verified Access), and AWS is positioning it as the "least privilege by default" governance model for agentic AI. The three-persona model (Admin/Publisher/Consumer) maps cleanly to enterprise org structures.

The Agent Registry being available **as an MCP server** is a smart move — it means Claude Code, Cursor, and other MCP clients can query AWS's registry directly, creating a developer-first entry point.

**Strengths**

- **Policy depth**: Cedar-based runtime policy is more mature than competitors' governance layers. AWS published extensive policy examples (AgentCore Cedar Policy Examples) showing how to control gateway tool access by resource, action, principal, and context.
- **Semantic search**: Agent Registry supports semantic search over agent/tool metadata, not just keyword search.
- **Cloud-native integration**: Tight integration with Bedrock models, AWS Lambda for tools, and AWS IAM for access control.
- **Three-persona model**: Clear separation of Admin (policy), Publisher (catalog), and Consumer (discovery) roles.

**Weaknesses vs Red Hat**

- **Cloud lock-in**: AgentCore is AWS-only. No on-prem or edge deployment. Enterprises with hybrid/multi-cloud requirements cannot use AWS Agent Registry outside AWS.
- **Cedar adoption**: Cedar is AWS-native but not industry-standard. Red Hat can leverage OPA (Open Policy Agent) for policy, which has broader Kubernetes ecosystem adoption.
- **Preview status**: Agent Registry is still in preview (August 2026). Production SLAs and regional expansion are not yet committed.
- **No MLflow integration**: AWS's agent tracing is Bedrock-native, not MLflow-native. Red Hat's MLflow-first approach aligns with the broader ML/AI ecosystem.

**Sources**

- [Understanding Cedar policies - Amazon Bedrock AgentCore](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/policy-understanding-cedar.html)
- [Policy in Amazon Bedrock AgentCore is now generally available - AWS](https://aws.amazon.com/about-aws/whats-new/2026/03/policy-amazon-bedrock-agentcore-generally-available/)
- [AWS Agent Registry for centralized agent discovery and governance is now available in Preview - AWS](https://aws.amazon.com/about-aws/whats-new/2026/04/aws-agent-registry-in-agentcore-preview/)
- [Why Policy in Amazon Bedrock AgentCore chose Cedar for securing agentic workflows | AWS Security Blog](https://aws.amazon.com/blogs/security/why-policy-in-amazon-bedrock-agentcore-chose-cedar-for-securing-agentic-workflows/)

---

### 2. Google — Cloud API Registry + Gemini Enterprise Agent Platform

**Current State (August 2026)**

- **Cloud API Registry**: Preview integration with Vertex AI Agent Builder announced December 2025. Provides tool governance for agents with pre-built MCP tools for Google services (BigQuery, Google Maps) and custom MCP server support via Apigee.

- **Platform rebrand**: Vertex AI rebranded to "Gemini Enterprise Agent Platform" in April 2026, signaling Google's shift from ML platform to agent platform.

- **MCP Servers UI**: MCP Servers now visible in the Google Cloud console under "Gemini Enterprise Agent Platform → Agents → Build → MCP Servers."

- **Pricing**: Agent Engine runtime pricing lowered; billing started January 28, 2026.

**Strategy**

Google is positioning **API Registry as the governance layer for MCP servers**, treating MCP servers as first-class governed resources alongside APIs. The Apigee integration (transform existing APIs into custom MCP servers) is a bridge strategy to monetize Google's existing API management install base.

The rebrand to "Gemini Enterprise Agent Platform" signals Google's intent to own the full agent lifecycle, not just model inference.

**Strengths**

- **API-first governance**: Cloud API Registry is a mature product (originally for OpenAPI/gRPC governance). Extending it to MCP servers leverages proven governance primitives (versioning, ownership, blast radius, policy inheritance).
- **Apigee bridge**: Organizations with Apigee can expose existing APIs as MCP servers, reducing new tool-building burden.
- **ADK integration**: Agent Development Kit (ADK) provides a streamlined developer experience with Cloud API Registry connector for MCP servers.
- **GCP-native**: Deep integration with Google Cloud services (BigQuery, Vertex AI, Cloud Functions).

**Weaknesses vs Red Hat**

- **Cloud lock-in**: Cloud API Registry is GCP-only. No on-prem or multi-cloud deployment.
- **MCP-centric**: Google's governance is MCP-server-centric, not skill-centric. Red Hat's skill abstraction (markdown + code + metadata) is more portable than MCP server definitions.
- **Preview status**: Cloud API Registry + Vertex AI Agent Builder integration is still in preview (August 2026).
- **No MLflow integration**: Google's agent tracing uses Vertex AI's proprietary telemetry, not MLflow.

**Sources**

- [New Enhanced Tool Governance in Vertex AI Agent Builder | Google Cloud Blog](https://cloud.google.com/blog/products/ai-machine-learning/new-enhanced-tool-governance-in-vertex-ai-agent-builder)
- [Tool governance in Vertex AI Agent Builder with the new Cloud API Registry integration - Agents - Google Developer forums](https://discuss.google.dev/t/tool-governance-in-vertex-ai-agent-builder-with-the-new-cloud-api-registry-integration/298148)
- [Cloud API Registry - Agent Development Kit](https://google.github.io/adk-docs/tools/google-cloud/api-registry/)
- [Vertex AI Is Now Gemini Enterprise Agent Platform: What Changed in 2026](https://gcpstudyhub.com/blog/vertex-ai-replaced-by-gemini-enterprise-agent-platform)

---

### 3. Databricks — Unity Catalog + Unity AI Gateway

**Current State (August 2026)**

- **Unity AI Gateway**: Announced at Data + AI Summit (DAIS) 2026 on June 16. Extends Unity Catalog governance to runtime interactions between models, agents, MCP services, skills, and enterprise tools.

- **Agents as first-class entities**: Agents are now securables in Unity Catalog. An agent is registered as a Unity Catalog model; tools it calls are governed as MCP services, functions, and connections.

- **MLflow integration**: Unity AI Gateway connects with MLflow for tracing, evaluation, and monitoring. MLflow tracing auto-instruments LangChain, LlamaIndex, AutoGen, OpenAI SDK, Anthropic SDK. Traces are landed in Unity Catalog as tables.

- **Contextual Service Policies**: Now in Beta. Extends governance from "who can access" to "what it can do in a given interaction."

- **Cost control**: AI Gateway budgets cover external providers (including BYOK connections) with hard spend caps.

**Strategy**

Databricks is executing a **data-centric governance** play: "If your data is in Unity Catalog, your agents should be too." Unity AI Gateway positions as the single governed endpoint for Databricks-hosted models, Azure OpenAI, AWS Bedrock, and Anthropic, with unified policy, audit, and cost attribution.

The MLflow integration is critical — Databricks is leveraging its ownership of MLflow (acquired 2020) to position Unity AI Gateway as the natural governance layer for agent teams already using MLflow for model tracking.

**Strengths**

- **Data + AI unified governance**: Unity Catalog already governs data, models, and notebooks. Extending to agents/skills is a natural expansion.
- **MLflow-native**: Deep MLflow integration for agent tracing, evaluation, and monitoring. This aligns with the broader ML/AI ecosystem and directly competes with Red Hat's MLflow-based approach.
- **Multi-cloud runtime**: Unity AI Gateway can proxy to Azure OpenAI, AWS Bedrock, Anthropic, not just Databricks models. This creates a multi-provider governance layer.
- **Cost attribution**: Hard spend caps and budget tracking across providers is a unique enterprise feature.
- **Contextual policies**: Runtime policy enforcement (what can an agent do in *this* interaction) is more granular than static RBAC.

**Weaknesses vs Red Hat**

- **Cloud-native only**: Unity Catalog requires Databricks cloud deployment (AWS, Azure, GCP). No on-prem or edge deployment. Red Hat's OpenShift-based approach supports disconnected/edge environments.
- **Databricks dependency**: Unity AI Gateway is tightly coupled to the Databricks platform. Red Hat can offer registry-as-a-service without requiring RHOAI adoption.
- **MLflow tension**: Databricks owns MLflow but their OSS team's mantra is "make MLflow famous" (open ecosystem). Unity AI Gateway is Databricks-proprietary. Red Hat can position as the **pure open MLflow** governance layer.
- **No skills marketplace**: Unity AI Gateway governs agents/tools but doesn't provide a public skills marketplace. Red Hat's Skills Registry can offer both private governance + community marketplace.

**Sources**

- [What's new with Unity Catalog at Data + AI Summit 2026 | Databricks Blog](https://www.databricks.com/blog/whats-new-unity-catalog-data-ai-summit-2026)
- [Expanding agent governance with Unity AI Gateway | Databricks Blog](https://www.databricks.com/blog/ai-gateway-governance-layer-agentic-ai)
- [Governing AI agents at scale with Unity Catalog | Databricks Blog](https://www.databricks.com/blog/governing-ai-agents-scale-unity-catalog)
- [AI governance at Data + AI Summit 2026: What's new with Unity AI Gateway | Databricks Blog](https://www.databricks.com/blog/ai-governance-data-ai-summit-2026-whats-new-unity-ai-gateway)

---

### 4. IBM — watsonx Orchestrate + Agent Catalog

**Current State (August 2026)**

- **General Availability**: Watsonx Orchestrate moved from preview to GA at IBM Think 2026 (Boston, May 2026). Shipped with 150+ enterprise connectors (Salesforce, SAP, Workday, ServiceNow, Microsoft 365, Oracle, Adobe, AWS).

- **Agent Catalog**: Growing collection of prebuilt AI agents and tools from IBM and partners. Every agent is validated and observable before listing. Agents built on any framework, any LLM, or any cloud can be onboarded.

- **Agentic Control Plane**: Announced June 2026, available on AWS and IBM Cloud. Centralized dashboard for operating, governing, and scaling AI agents across enterprise environments. Includes Security Control Center, analytics, natural-language task scheduling, and tenant catalog publishing.

- **Domain Agents**: Prebuilt agents for Finance, Supply Chain (new in 2026), HR, Procurement, Sales, Customer Service.

- **Agent Connect Partner Program**: ISVs and partners can integrate agents with watsonx Orchestrate and list in Agent Catalog.

- **Framework Support**: IBM native agents, Langflow, LangGraph, and agents built with open A2A protocol.

**Strategy**

IBM is positioning as the **"any agent, any framework"** platform. The strategy is to own the orchestration layer (not the agent frameworks) and monetize through enterprise connectors + governance + partner ecosystem (Agent Connect).

The Agentic Control Plane (June 2026) signals IBM's pivot from "build agents" to "operate agent fleets at scale." This is a direct play for enterprise IT departments that need central visibility and policy enforcement.

**Strengths**

- **Framework-agnostic**: Supports IBM native, Langflow, LangGraph, A2A agents. Red Hat must match this openness.
- **Enterprise connectors**: 150+ connectors to SAP, Salesforce, Workday, etc. are battle-tested integrations IBM has built over decades. This is a moat.
- **Governance-first**: Every agent in the catalog is validated and observable *before* listing. This positions IBM as the "trusted registry" alternative to public marketplaces like skills.sh.
- **Agentic Control Plane**: Centralized dashboard, security control center, and analytics provide enterprise IT the control surface they demand.
- **Domain agents**: Prebuilt agents for Finance, Supply Chain, HR, Procurement, Sales, Customer Service reduce time-to-value.

**Weaknesses vs Red Hat**

- **IBM Cloud dependency**: Watsonx Orchestrate is available on IBM Cloud and AWS, but not on-prem or edge. Red Hat's Kubernetes-native approach supports disconnected deployments.
- **Closed ecosystem**: Agent Catalog is curated by IBM + partners. Red Hat can offer both curated (trusted) + community (open) tiers.
- **No MLflow integration**: IBM's telemetry is watsonx-native, not MLflow-native.
- **Pricing**: IBM's enterprise pricing model is opaque. Red Hat can compete on transparent, subscription-based pricing.

**Sources**

- [IBM Think 2026: Watsonx Orchestrate GA and Agent Catalog — Enterprise DNA](https://enterprisedna.co/resources/news/ibm-think-2026-watsonx-orchestrate-agent-catalog-enterprise/)
- [Any agent, any framework: Inside the IBM watsonx Orchestrate Agent Catalog](https://www.ibm.com/new/product-blog/any-agent-any-framework-inside-the-ibm-watsonx-orchestrate-agent-catalog)
- [From Building Agents to Running Them: Watsonx Orchestrate's June Release Adds an Operating System](https://blog.octanesolutions.com.au/from-building-agents-to-running-them-watsonx-orchestrates-june-release-adds-an-operating-system)
- [Agentic Control Plane in IBM watsonx Orchestrate: One place to control every AI agent](https://www.ibm.com/new/announcements/introducing-the-agentic-control-plane)

---

### 5. NVIDIA — Verified Agent Skills + SkillSpector + NemoClaw + JFrog Integration

**Current State (August 2026)**

- **Verified Agent Skills**: Shipped May 22, 2026. A governance framework for the AI agent skill ecosystem. Verified skills undergo automated and human reviews, risk scanning with SkillSpector, signing, and documentation via machine-readable skill cards.

- **SkillSpector**: Open-source security scanner for AI agent skills (GitHub: nvidia/skillspector). Scans Git repos, URLs, zip files, directories, or single files. Detects 68 vulnerability patterns across 17 categories (prompt injection, data exfiltration, privilege escalation, supply chain attacks, MCP-specific risks). Research found 26.1% of AI agent skills contain at least one vulnerability; 5.2% show likely malicious intent.

- **NemoClaw**: Kubernetes-based sandbox for OpenClaw security. Focuses on runtime security: sandboxed execution, controlled access to files/networks, policy enforcement around sensitive actions.

- **JFrog Integration**: Announced March-April 2026 at GTC. JFrog Agent Skills Registry will support NVIDIA Agent Toolkit, including NemoClaw. JFrog Artifactory serves as registry for AI models and agent skills with NVIDIA AI-Q Blueprint. NVIDIA and JFrog validated workflow for ingestion and management of Artifactory as skills registry, using NVIDIA cuOpt as first example of a packaged skill.

**Strategy**

NVIDIA is positioning as the **"trust layer"** for agent skills, not a registry operator. SkillSpector is the reference security scanner; JFrog is the reference supply chain platform. NVIDIA is creating the standards and tooling, then partnering with registry operators (JFrog, potentially Red Hat) to operationalize it.

The NemoClaw + SkillSpector combination addresses the OpenClaw security crisis (800+ malicious skills) by providing both static scanning (SkillSpector) and runtime sandboxing (NemoClaw).

**Strengths**

- **Security-first**: SkillSpector's 68 vulnerability patterns and NemoClaw's runtime sandbox are the most mature security offerings in the market.
- **Open tooling**: SkillSpector is open source. Red Hat can integrate SkillSpector into the Skills Registry pipeline without NVIDIA lock-in.
- **JFrog partnership**: Validates the supply chain approach. JFrog Artifactory is widely deployed in enterprises; using it as a skills registry reduces deployment friction.
- **Skill cards**: Machine-readable skill metadata (skill cards) is the right abstraction for governance. Red Hat should adopt/extend this format.
- **Research credibility**: NVIDIA's research showing 26.1% of skills have vulnerabilities creates market urgency for governed registries.

**Weaknesses vs Red Hat**

- **Not a registry**: NVIDIA is not operating a registry; they're providing tooling. Red Hat must partner with or compete against JFrog for the registry layer.
- **Cloud-agnostic but not Kubernetes-native**: NemoClaw is Kubernetes-based but not OpenShift-optimized. Red Hat can offer tighter OpenShift integration.
- **No MLflow integration**: NVIDIA's telemetry is focused on runtime security, not ML experiment tracking. Red Hat's MLflow integration provides a broader observability story.

**Sources**

- [NVIDIA-Verified Agent Skills Provide Capability Governance for AI Agents | NVIDIA Technical Blog](https://developer.nvidia.com/blog/nvidia-verified-agent-skills-provide-capability-governance-for-ai-agents/)
- [NVIDIA Verified Agent Skills: SkillSpector and Skill Cards (2026) | byteiota](https://byteiota.com/nvidia-verified-agent-skills-skillspector-and-skill-cards-2026/)
- [JFrog Delivers Trust Layer for AI-Driven Software with NVIDIA | JFrog](https://jfrog.com/press-room/jfrog-delivers-trust-layer-for-ai-driven-software-with-nvidia/)
- [GitHub - NVIDIA/SkillSpector: Security scanner for AI agent skills](https://github.com/nvidia/skillspector)

---

### 6. Anthropic — Claude Marketplace

**Current State (August 2026)**

- **Marketplace**: Claude Marketplace features Claude-powered tools for enterprise customers. Launch partners include GitLab, Harvey, Lovable, Replit, Rogo, Snowflake, with more partners joining.

- **Skills system**: Skills are folders of instructions, scripts, and resources that Claude loads dynamically. Anthropic provides pre-built Agent Skills for common document tasks (PowerPoint, Excel, Word, PDF). Custom Skills work the same way: once available, Claude uses them automatically when relevant.

- **Publishing**: Every plugin on the official marketplace passes Anthropic's publishing checks. Directory model: publishers list plugins, users install the ones they want.

- **Governance**: Anthropic recommends using Skills only from trusted sources (self-created or from Anthropic) because Skills give Claude new capabilities through instructions + code, meaning a malicious Skill can direct Claude to invoke tools/execute code in unintended ways.

- **API access**: Pre-built skills and custom skills available via Claude API, Claude Platform on AWS, and Microsoft Foundry.

**Strategy**

Anthropic is positioning the marketplace as a **developer ecosystem play**, not an enterprise registry. The focus is on high-quality, curated skills from trusted partners, not scale (contrast with skills.sh's 669K+ skills).

The multi-cloud distribution (Claude API, AWS, Microsoft Foundry) signals Anthropic's intent to meet developers where they are, not force them onto Anthropic infrastructure.

**Strengths**

- **Curated quality**: Anthropic's publishing checks ensure baseline quality/security. This is a trust differentiator vs public marketplaces.
- **Developer mindshare**: Claude Code is the fastest-growing AI coding tool. Skills that work in Claude Code have built-in distribution.
- **Multi-cloud**: Skills available on AWS and Microsoft Foundry reduce cloud lock-in concerns.
- **MCP leadership**: Anthropic created MCP and donated it to the Linux Foundation. MCP steering committee includes Microsoft, Google, AWS, OpenAI. This positions Anthropic as the standard-bearer for tool/skill interoperability.

**Weaknesses vs Red Hat**

- **Not enterprise-focused**: Claude Marketplace is developer-centric, not IT-centric. No centralized governance dashboard, no policy enforcement, no audit trails for enterprise compliance.
- **No on-prem**: Claude Marketplace is cloud-only. No disconnected/edge deployment.
- **Small scale**: Marketplace is curated, so scale is limited compared to public registries (skills.sh 669K+, Hugging Face 40K+). Red Hat can offer both curated + community.
- **No MLflow integration**: Anthropic's telemetry is Claude-native, not MLflow-native.

**Sources**

- [Claude Marketplace | Claude by Anthropic](https://claude.com/platform/marketplace)
- [Agent Skills - Claude Platform Docs](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)
- [GitHub - anthropics/skills: Public repository for Agent Skills](https://github.com/anthropics/skills)

---

### 7. Microsoft — Agent Framework 1.0 + Copilot Studio

**Current State (August 2026)**

- **Agent Framework 1.0 GA**: Reached GA on April 2, 2026. Convergence of AutoGen and Semantic Kernel into a single, commercially supported SDK for building multi-agent systems. Available for .NET and Python (`pip install agent-framework` or `dotnet add package Microsoft.Agents.AI`).

- **Key features**: Enterprise-grade multi-agent orchestration, multi-provider model support, cross-runtime interoperability via A2A and MCP. Graph-based workflows for explicit multi-agent orchestration. Session-based state management, type safety, middleware, telemetry.

- **MCP integration**: Support for Model Context Protocol (MCP), enabling Copilot agents to share tool surface with Claude and Gemini agents. Significant interoperability improvement for mixed-provider AI stacks.

- **Copilot Studio updates (May 2026)**: Work IQ added REST API access, CLI, and remote MCP server support. MAF now supports building agents on GitHub Copilot SDK as backend, bringing Copilot's coding-oriented capabilities (shell execution, file operations, URL fetching, MCP integration) into MAF programming model.

- **BUILD 2026**: Microsoft BUILD 2026 (June 2-3, San Francisco) showcased unified agent architecture across Windows Agent Runtime, Agent Framework, multi-model Copilot, and Azure AI Foundry.

**Strategy**

Microsoft is executing a **"one Microsoft agent stack"** play: unify AutoGen, Semantic Kernel, Copilot Studio, and Azure AI Foundry into a single developer experience. The A2A and MCP support signals Microsoft's commitment to open standards (reducing lock-in concerns), while the Windows Agent Runtime (BUILD 2026) signals intent to embed agent capabilities into the OS.

**Strengths**

- **Convergence**: AutoGen + Semantic Kernel unification reduces developer confusion and provides production-grade enterprise features (state management, middleware, telemetry).
- **MCP + A2A support**: Cross-runtime interoperability via MCP and A2A is a key differentiator. Microsoft is on the MCP steering committee and A2A technical steering committee.
- **Enterprise features**: Type safety, middleware, telemetry, session-based state management align with enterprise requirements.
- **Multi-provider**: Agent Framework supports Azure OpenAI, AWS Bedrock, Anthropic, not just Microsoft models.
- **Windows Agent Runtime**: OS-level agent capabilities (BUILD 2026) create a platform moat.

**Weaknesses vs Red Hat**

- **Cloud-centric**: Agent Framework is cloud-first (Azure AI Foundry). On-prem deployment is not a priority.
- **Windows-centric**: Windows Agent Runtime is Windows-only. Red Hat's Linux/Kubernetes-native approach supports broader deployment targets.
- **No MLflow integration**: Microsoft's telemetry is Azure-native, not MLflow-native.
- **Framework lock-in**: Despite MCP/A2A support, Agent Framework is a Microsoft SDK. Red Hat can offer framework-agnostic registry (works with LangChain, AutoGen, Agent Framework, etc.).

**Sources**

- [Microsoft Agent Framework at BUILD 2026: Agent Harness, Hosted Agents, CodeAct, and more | Microsoft Agent Framework](https://devblogs.microsoft.com/agent-framework/microsoft-agent-framework-at-build-2026-announce/)
- [Microsoft Agent Framework Version 1.0 | Microsoft Agent Framework](https://devblogs.microsoft.com/agent-framework/microsoft-agent-framework-version-1-0/)
- [Microsoft Agent Framework Overview | Microsoft Learn](https://learn.microsoft.com/en-us/agent-framework/overview/)
- [A2A v1 Is Here: Cross-Platform Agent Communication in Microsoft Agent Framework for .NET | Microsoft Agent Framework](https://devblogs.microsoft.com/agent-framework/a2a-v1-is-here-cross-platform-agent-communication-in-microsoft-agent-framework-for-net/)

---

### 8. Emerging Players — JFrog, TrueFoundry, Portkey, Kong, Tech Leads Club

**JFrog Agent Skills Registry**

- **Launch**: Announced March-April 2026 at GTC (NVIDIA partnership).
- **Position**: Enterprise-grade private skills registry with supply chain security and provenance tracking. Integrated with NVIDIA Agent Toolkit (NemoClaw, SkillSpector).
- **Strength**: JFrog Artifactory is widely deployed in enterprises. Extending to skills reduces deployment friction.
- **Weakness**: Cloud-agnostic but not Kubernetes-optimized. Red Hat can offer tighter OpenShift integration.

**TrueFoundry Skills Registry**

- **Launch**: Introduced in TrueFoundry AI Gateway in May 2026.
- **Position**: Reusable, versioned agent skills for production AI systems.
- **Strength**: Built into AI Gateway, providing integrated governance across models, agents, and skills.
- **Weakness**: Startup with limited enterprise deployment. Red Hat has stronger enterprise credibility.

**Portkey Skills Registry**

- **Launch**: April 2026.
- **Position**: Skills registry that syncs to Claude Code, Cursor, Codex, OpenCode, and GitHub Copilot.
- **Strength**: Multi-IDE integration reduces fragmentation.
- **Weakness**: Focused on developer tools, not enterprise governance.

**Kong MCP Registry**

- **Launch**: February 2026 (tech preview).
- **Position**: MCP server registry integrated with Kong Konnect API Catalog. Extends API governance to MCP servers.
- **Strength**: Unified API + MCP governance. Enterprises with Kong can govern MCP servers in full operational context (underlying API dependencies, ownership, blast radius, inherited policies).
- **Weakness**: Kong-dependent. Red Hat can offer standalone registry.

**Tech Leads Club Agent Skills Registry**

- **Launch**: January 2026.
- **Position**: Curated agent skills registry with 1,717 GitHub stars. Focus on trust and validation.
- **Strength**: Community-driven curation.
- **Weakness**: Not enterprise-grade (no SLA, no support, no compliance certifications).

**Sources**

- [Agent Skills Registry | JFrog](https://jfrog.com/ai-catalog/skills-registry/)
- [Introducing Agent Skills Registry in TrueFoundry](https://www.truefoundry.com/blog/introducing-skills-registry-reusable-agent-skills-for-production-ai-systems)
- [Introducing Skills Registry | Portkey](https://portkey.ai/blog/skills-registry/)
- [Kong Introduces MCP Registry in Kong Konnect to Power AI Connectivity for Agent Discovery and Governance](https://www.prnewswire.com/news-releases/kong-introduces-mcp-registry-in-kong-konnect-to-power-ai-connectivity-for-agent-discovery-and-governance-302676451.html)
- [Agent Skills Registry (tech-leads-club) | Ry Walker Research](https://rywalker.com/research/agent-skills-registry)

---

### 9. Public Marketplaces — skills.sh, Hugging Face, ClawHub

**skills.sh**

- **Launch**: January 2026 (Vercel-backed).
- **Scale**: 669K+ skills as of July 2026.
- **Position**: "npm-style package manager for skills." Installed with `npx skills add`. Works across Claude Code, Codex CLI, Cursor, OpenClaw.
- **Governance**: Community-driven with no formal review. Quality varies.
- **Security**: Research paper analyzing 40K+ skills found explosive hype-driven growth (18.5x increase in 20 days Jan-Feb 2026), 46.3% duplicates or near-duplicates, and security gaps.
- **Red Hat opportunity**: skills.sh validates demand for a skills package manager but lacks governance. Red Hat can offer a **curated public tier** with SkillSpector scanning + skill cards, bridging the gap between skills.sh's scale and enterprise registries' governance.

**Hugging Face Skills**

- **Scale**: 40K+ skills (as of ARD spec launch, June 2026).
- **Position**: Interoperable with all major coding agent tools (OpenAI Codex, Claude Code, Gemini CLI, Cursor). ARD spec reference implementation (Hugging Face Discover Tool).
- **Governance**: Community-driven. No formal security scanning.
- **Strength**: ARD spec backing (Google, Microsoft, Hugging Face, Amazon, Cisco, GitHub, Salesforce, Snowflake, NVIDIA) positions Hugging Face as the "neutral ground" for agent/skill discovery.
- **Red Hat opportunity**: Hugging Face is developer-focused, not enterprise-focused. Red Hat can partner with Hugging Face to offer an **enterprise-hardened fork** of the Discover Tool with SkillSpector scanning, RBAC, audit trails, and compliance certifications.

**ClawHub (OpenClaw)**

- **Launch**: OpenClaw created November 2025, ClawHub marketplace followed.
- **Scale**: 18K+ skills (pre-security-crisis peak). Now reduced after malicious skill removal.
- **Security crisis**: 341-800+ malicious skills discovered (12-20% of registry). CVE-2026-25253 (CVSS 8.8, one-click RCE). Multiple supply chain attacks (ClawHavoc campaign delivering Atomic macOS Stealer).
- **Governance improvements**: Partnered with VirusTotal (June 1, 2026) and NVIDIA (June 2026) for skill screening.
- **Government response**: China banned government agencies + state-owned banks from installing OpenClaw.
- **Red Hat opportunity**: The OpenClaw crisis is the **market-defining event** for governed registries. Red Hat must position as the "never another ClawHub" enterprise alternative with SkillSpector scanning, skill signing, provenance tracking, and runtime sandboxing (via OpenShift sandboxed containers).

**Sources**

- [7 AI Agent Skills Marketplaces in 2026 (Compared)](https://www.agensi.io/learn/best-ai-agent-skills-marketplaces-2026)
- [officialskills.sh — Official Agent Skills Directory](https://officialskills.sh/)
- [The Wild West of Agent Skills: Inside the Explosive, Risky, and Redundant Marketplace of AI Tools | Hugging Face](https://huggingface.co/blog/zhongshsh/agent-skills-analysis)
- [OpenClaw's Skill Marketplace and the Emerging AI Supply Chain Threat | Palo Alto Networks](https://unit42.paloaltonetworks.com/openclaw-ai-supply-chain-risk/)
- [OpenClaw Security Risks: Skills, Exposure and Exploits](https://blog.cyberdesserts.com/openclaw-malicious-skills-security/)
- [OpenClaw March 2026 — China Bans Government Use, 820 Fake Skills, and ClawHub Marketplace](https://www.grandlinux.com/en/blogs/openclaw-march-2026.html)

---

## Competitive Positioning Matrix (Updated August 2026)

| Competitor | Governance Depth | Scale | Hybrid/Edge | MLflow Native | MCP/A2A Support | Security Scanning | Status |
|------------|------------------|-------|-------------|---------------|-----------------|-------------------|--------|
| **AWS Agent Registry** | **High** (Cedar policy) | Medium | **No** (AWS-only) | No | MCP (as server) | Unknown | Preview |
| **IBM watsonx Orchestrate** | **High** (validated catalog) | Medium | **Limited** (AWS + IBM Cloud) | No | A2A | Unknown | GA |
| **Google Cloud API Registry** | **High** (API governance) | Medium | **No** (GCP-only) | No | MCP | Unknown | Preview |
| **Databricks Unity AI Gateway** | **High** (contextual policies) | Medium | **No** (cloud-only) | **Yes** | Unknown | Unknown | GA |
| **Microsoft Agent Framework** | Medium (middleware) | Medium | **Limited** (Azure-first) | No | **MCP + A2A** | Unknown | GA |
| **NVIDIA Verified Skills** | **Very High** (SkillSpector) | Low | **Yes** (tooling) | No | Unknown | **SkillSpector** | GA |
| **JFrog Agent Skills Registry** | **High** (provenance) | Low | **Yes** | No | Unknown | **SkillSpector** (NVIDIA) | GA |
| **Anthropic Claude Marketplace** | Medium (curated) | Low | **No** (cloud-only) | No | **MCP** (created) | Unknown | GA |
| **Kong MCP Registry** | **High** (API governance) | Low | **Yes** (self-hosted) | No | **MCP** | Unknown | Tech Preview |
| **TrueFoundry** | Medium | Low | Unknown | Unknown | Unknown | Unknown | GA |
| **Portkey** | Low | Medium | Unknown | Unknown | Unknown | Unknown | GA |
| **skills.sh** | **Low** (no review) | **Very High** (669K+) | N/A | No | Unknown | **No** | GA |
| **Hugging Face** | **Low** (community) | **Very High** (40K+) | N/A | No | **ARD spec** | **No** | GA |
| **ClawHub** | **Low** (post-crisis) | **High** (18K+) | N/A | No | Unknown | **VirusTotal** (new) | GA |
| **Red Hat (Opportunity)** | **Very High** (K8s-native RBAC + OPA + SkillSpector) | **Scalable** (curated + community tiers) | **Yes** (OpenShift hybrid/edge) | **Yes** (RHOAI) | **Yes** (MCP + A2A) | **SkillSpector** (integrate) | **RFE** |

---

## Standards Convergence — MCP, A2A, ARD

### Model Context Protocol (MCP)

- **Governance**: Donated to Agentic AI Foundation (Linux Foundation) in December 2025. Vendor-neutral, community-governed.
- **Steering Committee**: Anthropic, OpenAI, Google, Microsoft, AWS, community representatives.
- **Adoption**: Major update (July 28, 2026) jointly shipped by Anthropic, OpenAI, Google, Microsoft, AWS.
- **Impact**: MCP is the **de facto standard** for tool/skill interfaces. Red Hat must support MCP servers as first-class citizens in the Skills Registry.

**Sources**

- [MCP Adoption Statistics 2026: The Numbers Behind AI's Fastest-Growing Standard](https://www.affiliatebooster.com/mcp-adoption-statistics-2026/)
- [Why the Model Context Protocol Won - The New Stack](https://thenewstack.io/why-the-model-context-protocol-won/)
- [GitHub, Microsoft join Anthropic's MCP steering committee-Xinhua](https://english.news.cn/northamerica/20250520/2fe7aec1371345c28c9c164fdd91218a/c.html)

### Agent-to-Agent (A2A) Protocol

- **Governance**: Linux Foundation. Technical Steering Committee: AWS, Cisco, Google, IBM Research, Microsoft, Salesforce, SAP, ServiceNow.
- **Adoption**: 150+ supporting organizations as of April 2026 (one-year mark), up from 50+ at April 2025 launch.
- **Impact**: A2A enables cross-framework agent interoperability. Red Hat must support A2A messaging for agents to interoperate with Microsoft Agent Framework, IBM watsonx Orchestrate, etc.

**Sources**

- [What Is Agent2Agent (A2A) Protocol? | IBM](https://www.ibm.com/think/topics/agent2agent-protocol)
- [A2A Protocol Surpasses 150 Organizations, Lands in Major Cloud Platforms, and Sees Enterprise Production Use in First Year | Linux Foundation](https://www.linuxfoundation.org/press/a2a-protocol-surpasses-150-organizations-lands-in-major-cloud-platforms-and-sees-enterprise-production-use-in-first-year)
- [A2A v1 Is Here: Cross-Platform Agent Communication in Microsoft Agent Framework for .NET](https://devblogs.microsoft.com/agent-framework/a2a-v1-is-here-cross-platform-agent-communication-in-microsoft-agent-framework-for-net/)

### Agentic Resource Discovery (ARD)

- **Launch**: June 17, 2026.
- **Co-authors**: Google, Microsoft, Hugging Face.
- **Backers**: Amazon, Cisco, GitHub, Salesforce, Snowflake, NVIDIA.
- **Impact**: ARD defines how agents and tools are cataloged, indexed, and searched across federated registries. Publishers host `ai-catalog.json` at well-known path; registries crawl it; agents search by intent, verify publisher, then connect (MCP, A2A, or plain API).
- **Red Hat opportunity**: Implement ARD spec to enable Skills Registry to be discovered by agents across the ecosystem (Claude, Gemini, Copilot, etc.).

**Sources**

- [Agentic Resource Discovery: Let agents search | Hugging Face](https://huggingface.co/blog/agentic-resource-discovery-launch)
- [Google, Microsoft Back Draft AI Agent Discovery Spec | Search Engine Journal](https://www.searchenginejournal.com/google-microsoft-back-draft-ai-agent-discovery-spec/579894/)
- [ARD Specification - AgenticResourceDiscovery.org](https://agenticresourcediscovery.org/spec/)
- [Introducing the Agentic Resource Discovery specification - Command Line | Microsoft](https://commandline.microsoft.com/agentic-resource-discovery-specification-ard/)

---

## Red Hat Differentiation Opportunities

### 1. Hybrid-First Architecture (Only One)

**Insight**: Every hyperscaler registry (AWS, Google, Microsoft, Databricks, IBM) is cloud-centric. JFrog and Kong are cloud-agnostic but not Kubernetes-optimized. Red Hat is the **only vendor** that can offer:

- **On-prem deployment** via OpenShift (disconnected/air-gapped environments)
- **Edge deployment** via OpenShift on single-node/3-node clusters (factory floors, remote sites, telco edge)
- **Multi-cloud deployment** via OpenShift on AWS, Azure, GCP, bare metal

**EU AI Act forcing function**: EU AI Act enforcement began August 2, 2026. High-risk AI systems (including agents in critical infrastructure, employment, migration) must have **continuous risk management, tamper-evident logging, human oversight, and post-market monitoring**. For organizations in regulated industries (finance, healthcare, telco), on-prem deployment is mandatory for data residency and audit requirements.

**Positioning**: "The only skills registry that deploys where your data lives — on-prem, edge, or multi-cloud — with EU AI Act-compliant audit trails and runtime governance out of the box."

**Sources**

- [EU AI Act Enforcement August 2026 Guide | Trussed AI](https://trussed.ai/resources/eu-ai-act-enforcement-august-2026-guide)
- [AI Agent Governance: Policy and Compliance 2026 Guide](https://www.digitalapplied.com/blog/ai-agent-governance-policy-compliance-2026)

### 2. MLflow-Native Observability (Counter to Databricks)

**Insight**: Databricks Unity AI Gateway is the primary MLflow-native competitor, but it's Databricks-proprietary and cloud-only. Red Hat can position as the **pure open MLflow** governance layer:

- **RHOAI ships MLflow** as the model tracking and experiment management platform.
- **Skills Registry integrates with MLflow** for agent tracing, skill evaluation, and telemetry.
- **No vendor lock-in**: MLflow data is portable. Customers can migrate from RHOAI to another MLflow deployment (or vice versa) without rewriting agent code.

**Counter-narrative to Databricks**: "Databricks owns MLflow but Unity AI Gateway is Databricks-proprietary. Red Hat offers the same MLflow-native governance without the cloud lock-in."

**Technical detail**: RHOAI already includes "embedded MLflow user UI for end-to-end agentic traceability (tech preview)." Skills Registry should extend this to skill-level tracing (which agent invoked which skill, with what inputs/outputs, what was the latency, what errors occurred).

**Sources**

- [Operationalize AI agents with OpenShift and Kubernetes primitives | Red Hat Developer](https://developers.redhat.com/articles/2026/07/21/operationalize-ai-agents-openshift-and-kubernetes-primitives)

### 3. Kubernetes-Native Governance (Only One)

**Insight**: AWS uses Cedar, Google uses Cloud IAM, Microsoft uses Entra, Databricks uses Unity Catalog, IBM uses watsonx-native RBAC. Red Hat can leverage **OpenShift RBAC + OPA (Open Policy Agent)** for skills/agent governance:

- **ConfigMaps for agent definitions** (subagent prompts, models, tools, skills).
- **PVCs for skills and artifacts** (markdown skills, incident data, audit logs).
- **RBAC for access control** (which users/teams can discover/install which skills).
- **OPA for runtime policy** (which agent can invoke which skill under what conditions).
- **Sandboxed containers for skill execution** (OpenShift sandboxed containers = Kata Containers = VM-level isolation for untrusted skills).

**Positioning**: "The only skills registry where governance is Kubernetes-native primitives, not a proprietary policy engine. If you know RBAC and OPA, you know how to govern skills."

**Sources**

- [Operationalize AI agents with OpenShift and Kubernetes primitives | Red Hat Developer](https://developers.redhat.com/articles/2026/07/21/operationalize-ai-agents-openshift-and-kubernetes-primitives)

### 4. SkillSpector Integration + Skill Signing (Match NVIDIA)

**Insight**: NVIDIA's Verified Agent Skills framework (SkillSpector + skill cards + signing) is the **security gold standard**. Red Hat should:

- **Integrate SkillSpector** into the Skills Registry publishing pipeline (scan every skill for 68 vulnerability patterns before accepting).
- **Sign skills** with Red Hat signing keys (GPG or sigstore/cosign).
- **Publish skill cards** (machine-readable metadata: description, author, license, tested platforms, security scan results, provenance).
- **Offer three tiers**:
  - **Red Hat Verified**: Red Hat-authored skills, scanned, signed, supported.
  - **Community Verified**: Community-authored skills, scanned, signed, no support.
  - **Unverified**: Community-authored skills, not scanned, not signed, use at own risk.

**Positioning**: "The only enterprise skills registry with NVIDIA-grade security scanning and Red Hat signing, giving you the confidence to run community skills in production."

**Sources**

- [NVIDIA-Verified Agent Skills Provide Capability Governance for AI Agents | NVIDIA Technical Blog](https://developer.nvidia.com/blog/nvidia-verified-agent-skills-provide-capability-governance-for-ai-agents/)
- [GitHub - NVIDIA/SkillSpector: Security scanner for AI agent skills](https://github.com/nvidia/skillspector)

### 5. Curated + Community Dual Model (Bridge Public Marketplaces)

**Insight**: skills.sh (669K+) and Hugging Face (40K+) prove demand for a **public skills marketplace**, but they lack governance. Enterprise registries (AWS, IBM, Google) are curated but limited scale. Red Hat can bridge the gap:

- **Curated tier**: Red Hat Verified + Community Verified (scanned, signed).
- **Community tier**: Unverified skills from skills.sh, Hugging Face, ClawHub (mirror + SkillSpector scan on install).
- **Private tier**: Enterprise-internal skills (never leave firewall).

**Positioning**: "The only skills registry that gives you both enterprise governance and public marketplace scale — curated skills for production, community skills for experimentation, private skills for proprietary IP."

### 6. 20 Years of Red Hat Institutional Memory (Unique Asset)

**Insight**: Red Hat has 20 years of RHEL, OpenShift, Ansible expertise encoded in runbooks, scripts, and playbooks. This institutional memory can be packaged as **Red Hat-authored skills** that competitors cannot replicate:

- **RHEL skills**: Package management (dnf, rpm), systemd, SELinux, firewalld, networking, troubleshooting.
- **OpenShift skills**: Cluster management, operator development, CI/CD pipelines, service mesh, storage.
- **Ansible skills**: Playbook authoring, role development, inventory management, integration with RHOAI agents.

**Positioning**: "The only skills registry with 20 years of Red Hat's institutional memory — skills that know how to manage RHEL, OpenShift, and Ansible better than any LLM ever could."

**Sources**

- [Red Hat's skill packs give AI agents something a bigger model never could: 20 years of institutional memory - The New Stack](https://thenewstack.io/red-hat-agentic-skills-repository/)

---

## Threats and Risks

### 1. Databricks MLflow Ownership

**Threat**: Databricks owns MLflow and is positioning Unity AI Gateway as the "natural home" for MLflow-based agent governance. Red Hat's differentiation on MLflow-native observability is only sustainable if customers perceive Red Hat as a **peer to Databricks on MLflow**, not a downstream consumer.

**Mitigation**:
- **Upstream MLflow contributions**: Red Hat should contribute agent tracing features to upstream MLflow (not just consume).
- **MLflow community leadership**: Red Hat should take a steering committee seat in the MLflow project (if available) or sponsor MLflow community events.
- **Narrative**: "Databricks owns MLflow, but the MLflow team's mantra is 'make MLflow famous' (open ecosystem). Red Hat is the pure open MLflow governance layer, Databricks is the proprietary layer."

### 2. NVIDIA + JFrog Partnership

**Threat**: NVIDIA's partnership with JFrog (announced GTC April 2026) positions JFrog Artifactory as the reference skills registry for NVIDIA's ecosystem. If NVIDIA/JFrog becomes the de facto standard, Red Hat risks being a "me too" player.

**Mitigation**:
- **Partner with NVIDIA**: Red Hat should explore partnership with NVIDIA to offer SkillSpector + skill cards in the Red Hat Skills Registry. JFrog is NVIDIA's supply chain partner; Red Hat can be NVIDIA's Kubernetes/hybrid partner.
- **Differentiate on deployment**: JFrog Artifactory is cloud-agnostic but not Kubernetes-optimized. Red Hat can position as the "Kubernetes-native JFrog alternative."

### 3. Standards Fragmentation (MCP vs A2A vs ARD)

**Threat**: Three interoperability standards (MCP, A2A, ARD) with partial overlap creates integration burden. If customers perceive skills registries as "too complex to integrate," they may delay adoption.

**Mitigation**:
- **Support all three**: Red Hat Skills Registry should support MCP servers (first-class), A2A messaging (agent interop), and ARD discovery (federated search).
- **Simplify developer experience**: Abstract the complexity behind a unified API (developers specify skill, registry handles MCP/A2A/ARD negotiation).

### 4. Hyperscaler Bundling

**Threat**: AWS, Google, Microsoft, IBM can **bundle** agent registries with their cloud platforms at zero incremental cost, making Red Hat's standalone registry uncompetitive on price.

**Mitigation**:
- **Hybrid/multi-cloud as forcing function**: Enterprises with hybrid/multi-cloud requirements cannot use a single-cloud registry. Red Hat's differentiation is "one registry across all clouds + on-prem."
- **RHOAI bundling**: Red Hat should bundle Skills Registry with RHOAI subscriptions (not a separate SKU), matching hyperscaler bundling economics.

### 5. OpenClaw Security Crisis Backlash

**Threat**: The OpenClaw security crisis (800+ malicious skills, China government ban) could create **generalized fear** of agent skills, slowing market adoption.

**Mitigation**:
- **Lean into governance**: Position the OpenClaw crisis as the **proof point** for governed registries. "OpenClaw's security crisis is why you need Red Hat's SkillSpector-scanned, signed, audited registry."
- **Runtime sandboxing**: Emphasize OpenShift sandboxed containers (Kata) as the defense-in-depth layer that would have prevented OpenClaw's RCE exploits.

---

## Recommendations

### Immediate (Q3 2026)

1. **SkillSpector integration**: Integrate NVIDIA SkillSpector into the Skills Registry publishing pipeline (scan all skills before acceptance). Announce this as "Red Hat Skills Registry is the first enterprise registry with NVIDIA-grade security scanning."

2. **Skill cards + signing**: Adopt NVIDIA's skill card format (machine-readable metadata) and sign all Red Hat Verified skills with Red Hat signing keys (GPG or sigstore/cosign).

3. **MCP + A2A support**: Ensure Skills Registry supports MCP servers as first-class citizens and A2A messaging for agent interoperability.

4. **ARD spec implementation**: Implement ARD spec to enable Skills Registry to be discovered by agents across the ecosystem (Claude, Gemini, Copilot).

5. **MLflow agent tracing**: Ship MLflow agent tracing in RHOAI (upgrade from tech preview to GA) and integrate with Skills Registry for skill-level telemetry.

### Short-term (Q4 2026)

6. **Curated + Community dual model**: Launch three-tier model (Red Hat Verified, Community Verified, Unverified) with SkillSpector scanning for Community Verified tier.

7. **EU AI Act compliance kit**: Package Skills Registry + OpenShift RBAC + OPA policies + MLflow audit trails as "EU AI Act Compliance Kit for Agent Governance" (targeting regulated industries: finance, healthcare, telco).

8. **Red Hat-authored skills**: Publish 50+ Red Hat-authored skills for RHEL, OpenShift, Ansible (leverage 20 years of institutional memory).

9. **NVIDIA partnership**: Explore partnership with NVIDIA to position Red Hat Skills Registry as the "Kubernetes-native, hybrid-cloud reference implementation" for NVIDIA Verified Agent Skills.

### Medium-term (2027)

10. **JFrog interoperability**: Offer JFrog Artifactory as an optional backend for Skills Registry (customers with existing JFrog deployments can use Artifactory as the storage layer, Red Hat provides governance/discovery layer on top).

11. **Hybrid marketplace**: Mirror skills.sh + Hugging Face community skills into Red Hat Skills Registry's Unverified tier, with on-demand SkillSpector scanning when a user installs a community skill.

12. **Kubernetes Operator**: Ship Skills Registry as a Kubernetes Operator (deploy on any Kubernetes cluster, not just OpenShift), expanding addressable market to non-RHOAI customers.

---

## Sources Summary

This analysis drew on 50+ sources covering:

- **Hyperscaler registries**: AWS Agent Registry + Cedar Policy, Google Cloud API Registry + Gemini Enterprise, Microsoft Agent Framework 1.0 + Copilot Studio, IBM watsonx Orchestrate + Agentic Control Plane, Databricks Unity Catalog + Unity AI Gateway.
- **Security/governance**: NVIDIA Verified Agent Skills + SkillSpector + NemoClaw, JFrog Agent Skills Registry, OpenClaw/ClawHub security crisis, EU AI Act enforcement (August 2, 2026).
- **Standards**: MCP steering committee (Anthropic, Microsoft, Google, AWS, OpenAI), A2A Protocol (Linux Foundation, 150+ orgs), ARD spec (Google, Microsoft, Hugging Face).
- **Public marketplaces**: skills.sh (669K+), Hugging Face (40K+, ARD reference implementation), ClawHub (18K+, post-crisis).
- **Emerging players**: JFrog, TrueFoundry, Portkey, Kong MCP Registry, Tech Leads Club.
- **Red Hat context**: RHOAI MLflow integration, OpenShift agent operationalization, Red Hat's agentic skills repository (20 years institutional memory).

All sources are hyperlinked inline in the competitor sections above.
