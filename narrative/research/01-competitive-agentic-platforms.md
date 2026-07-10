---
title: "Competitive landscape: agentic AI platforms (2026)"
description: "How NVIDIA, IBM, Google, AWS, Azure, Databricks position agentic AI capabilities vs. Red Hat AI's five-theme strategy — MCP ecosystem, agent security, observability, and inference economics."
lens: competitive
timestamp: 2026-07-10
review_after: 2026-10-10
tags: [narrative, competitive, agentic]
---

# Competitive landscape: agentic AI platforms (2026)

## Executive summary

The enterprise agentic AI platform market in mid-2026 has entered a
consolidation phase — every major vendor ships production-grade agent
capabilities. Gartner forecasts 40% of enterprise applications will embed
task-specific AI agents by end of 2026, up from under 5% in 2025 [1].
Yet Forrester observes a persistent gap: three-quarters of enterprise
leaders claim adoption, but few have agents running in meaningful
production beyond "agentish" chatbots [2].

Two protocol standards have settled the interoperability question.
Anthropic's MCP, donated to the Linux Foundation's Agentic AI Foundation
in December 2025, has 97 million monthly SDK downloads and 19,800+
indexed servers [3]. Google's A2A protocol reached 150+ supporting
organizations by April 2026; IBM's ACP merged into A2A in August 2025
[4]. The two-layer stack — MCP for vertical tool integration, A2A for
horizontal agent coordination — is becoming the architectural default.

NVIDIA has made the most ambitious platform play with its Agent Toolkit
(GTC 2026), combining OpenShell sandboxing, NemoClaw blueprints, AI-Q
research tools, and Nemotron models [5]. OpenShell has become the
reference implementation for agent sandboxing, with security partnerships
spanning Cisco, CrowdStrike, Google, Microsoft, and Trend Micro [6].
Red Hat is both an OpenShell contributor/maintainer and a platform
integration partner — the only vendor providing the Kubernetes-native
runtime (OpenShift AI) underneath NVIDIA's agent infrastructure layer.

Red Hat's competitive position is strongest in the infrastructure and
operations layer — the "from metal to agents" thesis. Its combination of
vLLM-based inference, llm-d distributed inference (accepted into CNCF
Sandbox), OpenShell integration, and hybrid/multi-cloud portability via
OpenShift creates a uniquely open, vendor-neutral foundation [7][8]. The
gap is in higher-level developer experience: competitors like AWS
(AgentCore), Google (Gemini Enterprise Agent Platform), and Databricks
(Agent Bricks) offer more turnkey agent-building experiences with managed
runtimes, pre-built templates, and visual builders.

## Competitor profiles

### NVIDIA AI Enterprise / Agent Toolkit

**Agentic offering:** NVIDIA Agent Toolkit (GTC 2026) combining the
Nemotron model family (including the 550B-parameter Nemotron 3 Ultra MoE),
NemoClaw agent blueprints, NeMo Agent Tools for evaluation/guardrails,
AI-Q for enterprise knowledge retrieval, and OpenShell for secure runtime
[5].

**GA vs announced:** OpenShell is open source and GA. Nemotron 3 Ultra is
GA. NemoClaw blueprints are GA for select partners. Full Agent Toolkit is
GA with Adobe, Salesforce, SAP, ServiceNow, Siemens, CrowdStrike,
Atlassian, Red Hat, Cisco, and 10+ enterprise partners [5].

**Strengths vs Red Hat:** NVIDIA owns the hardware layer (Blackwell GPUs,
Vera CPUs optimized for agent workloads delivering 3.2x higher throughput
[5]) and is extending into the platform layer. OpenShell is the most
architecturally rigorous agent sandbox available. The ISV ecosystem is
unmatched.

**Weaknesses vs Red Hat:** NVIDIA does not provide the Kubernetes
orchestration layer — depends on partners like Red Hat. NVIDIA's stack
assumes NVIDIA hardware; Red Hat AI supports multiple accelerators. Not
an open-source platform company.

**Relationship:** Partner, not pure competitor. Red Hat is an active
OpenShell contributor/maintainer and listed among Agent Toolkit launch
partners [5][6]. Risk: NVIDIA could favor hyperscaler partners for the
managed runtime layer.

### IBM watsonx

**Agentic offering:** watsonx Orchestrate with the Agentic Control Plane
(GA on AWS and IBM Cloud, June 2026) [9]. Centralized agent operations
including dashboards, governance policies, credential health monitoring,
and 150+ enterprise connectors. Agent Development Kit integrates with
LangChain and CrewAI. AgentOps observability layer and Langflow
integration for visual agent design [9][10].

**GA vs announced:** watsonx Orchestrate with Agentic Control Plane is GA
(June 2026). AgentOps and Agentic Workflows are GA. IBM named a Leader in
the 2026 Gartner Magic Quadrant for both AI Platforms (DSML) and AI
Governance Platforms [11]. IBM Sovereign Core on OpenShift and Red Hat AI
went GA at Think 2026 [12].

**Strengths vs Red Hat:** Most complete enterprise orchestration story
with 150+ connectors, no-code/pro-code dual builder, and the Agentic
Control Plane for centralized governance. The Anthropic strategic
partnership adds Claude access.

**Weaknesses vs Red Hat:** Proprietary platform with premium pricing. The
Agentic Control Plane is cloud-only (AWS, IBM Cloud); on-premises story
depends on Red Hat.

**Relationship:** Parent company and closest ally. IBM Sovereign Core is
built on OpenShift and Red Hat AI. However, watsonx Orchestrate competes
for mindshare on the agent management layer.

### Google Cloud (Gemini Enterprise Agent Platform)

**Agentic offering:** Rebranded from Vertex AI at Cloud Next 2026 —
Agent Builder, Agentspace, and Agent Engine unified [13]. ADK (code-first),
Agent Studio (low-code), managed Agent Engine runtime, persistent memory,
200+ foundation models. A2A protocol leadership. Managed remote MCP
servers for Google Maps, BigQuery, Compute Engine, GKE (GA Dec 2025) [13].

**Strengths vs Red Hat:** Owns the model (Gemini), the runtime (Agent
Engine), the silicon (TPUs), and the distribution channel (Workspace).
Pioneered A2A for agent-to-agent communication. Fastest-growing cloud
(50% YoY in Q4 2025 [13]).

**Weaknesses vs Red Hat:** Cloud-only — no on-premises or hybrid
deployment. Agent Engine is a managed service with no self-hosted option.
Locks developers into GCP's identity, networking, and billing.

### AWS (Bedrock AgentCore)

**Agentic offering:** Framework-agnostic platform supporting LangChain,
OpenAI Agents SDK, Claude Agent SDK, Strands SDK, and custom frameworks
[14]. AgentCore Identity (agent directory, authorizer, credential vault),
Code Interpreter sandboxing, Episodic Memory for cross-session
persistence, Managed Harness (preview April 2026), bidirectional
streaming for voice agents [14][15].

**Strengths vs Red Hat:** AgentCore Identity is the most complete managed
agent identity service — purpose-built agent directory, authorizer, and
credential vault [15]. Largest cloud ecosystem. Framework-agnostic
approach parallels Red Hat's BYOA.

**Weaknesses vs Red Hat:** Cloud-only. Palo Alto Networks Unit 42
published sandbox escape vulnerabilities in AgentCore's Code Interpreter
via DNS tunneling and metadata service exploitation (patched Feb 2026)
[16]. Agent identity is AWS-specific (Cognito-based), not standards-based
like SPIFFE.

### Microsoft Azure AI

**Agentic offering:** Microsoft Agent Framework (public preview) converging
AutoGen and Semantic Kernel with A2A and MCP support [17]. Azure AI
Foundry managed platform. Six Azure Copilot agents for cloud operations
(gated preview). Windows execution containers with OpenShell integration
announced at Build 2026 [18].

**Strengths vs Red Hat:** Broadest distribution channel (Azure + M365 +
Windows + GitHub + VS Code). The only cloud offering both Claude and GPT
frontier models. Windows + OpenShell integration brings agent sandboxing
to the desktop [18].

**Weaknesses vs Red Hat:** Agent story fragmented across Copilot Studio,
Azure AI Foundry, Agent Framework, and Security Copilot — no single
control plane. Core capabilities still in public preview. Deeply coupled
to Entra ID.

### Databricks (Mosaic AI / Unity AI Gateway)

**Agentic offering:** Agent Bricks for automated agent creation, Mosaic AI
Agent Framework (GA early 2026) with LangChain/LangGraph/LlamaIndex,
managed MCP servers exposing Unity Catalog Functions, Genie, Vector
Search, and DBSQL as governed tools, Unity AI Gateway (GA April 2026),
and MLflow 3 as the GenAI-native lifecycle backbone [19][20].

**Strengths vs Red Hat:** Most tightly integrated data-to-agent pipeline.
Unity Catalog provides unified governance from data to models to agents to
MCP servers. CLEARS evaluation rubric (Correctness, Latency, Execution,
Adherence, Relevance, Safety) is the most structured agent evaluation
framework in production [19]. Agent Bricks automated optimization is
differentiated.

**Weaknesses vs Red Hat:** SaaS-only (no self-hosted). Data-centric —
less suited for infrastructure automation or DevOps agents. Does not
provide compute infrastructure.

**Key differentiator:** Unity AI Gateway with managed MCP servers is the
closest analog to Red Hat's planned MCP Lifecycle Operator + Gateway +
Registry + Catalog — and it's GA today [20].

## MCP ecosystem comparison

| Capability | Red Hat AI | Databricks | Google | AWS | Azure |
|---|---|---|---|---|---|
| MCP server hosting | Coming (3.5-3.6) | Managed (GA) | Managed (GA) | Via frameworks | Via frameworks |
| MCP gateway/proxy | Yes (MCP Gateway) | Unity AI Gateway (GA) | Platform routing | No | No |
| MCP registry | Yes (MCP Registry) | Unity Catalog | Cloud API Registry | No (Agent Registry preview) | No |
| MCP lifecycle mgmt | Yes (Lifecycle Operator) | No | No | No | No |
| MCP catalog | Yes (MCP Catalog) | Partial | Partial | Partial | Partial |
| MCP governance | Full stack (planned) | ABAC + on-behalf-of (GA) | Agent identities (GA) | IAM (GA) | Entra ID |

Red Hat's planned MCP ecosystem would be the most Kubernetes-native and
operationally complete approach, but Databricks Unity AI Gateway is the
production leader today. Every quarter of delay increases the risk that
enterprises standardize on a competitor's MCP governance before Red Hat
ships.

Pinterest engineering published details of their production MCP ecosystem
handling 66,000 monthly invocations from 844 active users [3].

## Agent security and identity

### Sandboxing

| Vendor | Approach | Isolation | Status |
|---|---|---|---|
| NVIDIA OpenShell | Kernel-level (Landlock, seccomp, SELinux, OPA/Rego) | OS-level | GA (open source) |
| AWS AgentCore | Firecracker MicroVMs | VM-level | GA (patched vulnerabilities [16]) |
| Microsoft | Windows Execution Containers + OpenShell | OS-level | Preview (Build 2026) |
| Google | Agent Engine managed runtime | Container-level | GA |
| Red Hat | OpenShell on OpenShift + confidential containers | OS + container | Planned (3.5) |

OpenShell treats agent security as governance, not just isolation —
enforcing policy at the kernel level where the agent cannot override it
[6]. Red Hat's unique contribution: combining OpenShell with OpenShift's
confidential containers and SPIFFE-based identity.

### Identity

SPIFFE has become "the TCP/IP of agent identity" in 2026 [22]. HashiCorp
Vault 1.21 added native SPIFFE authentication for non-human identities.
Red Hat's Kagenti wires SPIFFE for workload identity, AuthBridge via
RFC 8693 for user delegation, and agent lifecycle management together.

| Vendor | Approach | Standards-based | Status |
|---|---|---|---|
| Red Hat | SPIFFE/SPIRE on OpenShift | Yes (CNCF) | Planned (3.5) |
| AWS | AgentCore Identity (Cognito) | No (proprietary) | GA |
| Google | Agent identities in Vertex | No (GCP IAM) | GA |
| Databricks | Unity Catalog identity | No (proprietary) | GA |

Red Hat's SPIFFE-based approach is the only standards-based, portable
agent identity strategy — a genuine differentiator for multi-cloud and
regulated environments.

## Observability and evaluation

MLflow 3.6.0 made OpenTelemetry the default tracing substrate with
bidirectional OTel integration, OTLP ingestion, and native GenAI Semantic
Conventions support [23]. MLflow is the only tool that is fully open
source (Apache 2.0), Linux Foundation-governed, and combines
observability, evaluation, governance, and AI gateway with no enterprise
paywall [23].

| Vendor | Observability | Evaluation | Status |
|---|---|---|---|
| Red Hat | MLflow (integrated) + OTel | Eval Hub (planned) + Garak red-teaming (GA) | Mixed GA/planned |
| Databricks | MLflow 3 (creator) | CLEARS rubric + Agent Bricks benchmarks | GA |
| AWS | AgentCore tracing | AgentCore evaluations | Preview |
| Google | Agent Engine observability | ADK evaluation | GA |
| Microsoft | Azure AI Foundry monitoring | Responsible AI evaluators | Preview |

Databricks leads in production agent evaluation. Red Hat's MLflow
integration is strong and defensible (MLflow's open-source nature means
full access). The planned Eval Hub with Garak red-teaming would be
differentiated, but is not yet shipping.

## Analyst perspective

- **Gartner:** 40% of enterprise apps will embed agents by end of 2026.
  Published first-ever Hype Cycle for Agentic AI in 2026. By 2028, 40%
  of CIOs will demand "Guardian Agents" to track and contain other
  agents [1][17].
- **Forrester:** "Companies are chasing, few are catching." 49% of
  security decision-makers named agentic AI as a concern. 30% of
  enterprise app vendors will launch MCP servers in 2026 [2].
- **IDC:** Asia-Pacific AI investments will grow 1.7x faster than overall
  digital spending, creating $1.6T economic impact by 2027 [24].
- **Common requirements:** governance/auditability, multi-agent
  orchestration, security/identity, MCP+A2A interoperability, operational
  maturity [1][2].

Red Hat is absent from the 2026 Gartner Magic Quadrant for AI Platforms
(DSML), where IBM and Dataiku are Leaders [11]. Reframing from "AI
infrastructure" to "agentic AI platform" requires shipping the full
AgentOps + MCP ecosystem + Eval Hub stack.

## Red Hat positioning assessment

### Where Red Hat leads

1. **Infrastructure layer ("from metal to agents"):** No competitor
   matches the full stack from RHEL AI through OpenShift AI to llm-d.
   CEO Matt Hicks reported 85% of internal agent calls running on
   open-weight models hosted on Red Hat infrastructure [8].
2. **Open-source strategy:** The only vendor whose entire agentic stack
   is built on open standards (MCP via Linux Foundation, SPIFFE via CNCF,
   OTel via CNCF, vLLM, llm-d, MLflow via Linux Foundation, OpenShell).
3. **Hybrid/multi-cloud portability:** The single largest unaddressed
   market in enterprise agentic AI. Gartner validates: "governance,
   commercial maturity, and market durability matter for medium- to
   long-term commitments" [1].
4. **NVIDIA partnership depth:** Both OpenShell contributor/maintainer
   and platform partner. No other open-source infrastructure vendor has
   this integration level.
5. **Inference economics:** The Jevons Paradox / cost argument is unique
   — no competitor makes this case because they profit from token
   consumption.

### Where gaps exist

1. **MCP ecosystem delivery timing:** Databricks Unity AI Gateway with
   managed MCP servers is GA. Google managed MCP servers GA since Dec
   2025. Red Hat's ecosystem targets 3.5-3.6 (late 2026).
2. **Agent-building developer experience:** No visual builder or managed
   runtime equivalent. GenAI Studio + agent templates coming but not GA.
3. **Managed agent identity:** AWS AgentCore Identity is shipping. Red
   Hat's SPIFFE approach is standards-superior but not yet integrated.
4. **Agent evaluation maturity:** Databricks CLEARS and Agent Bricks are
   GA. Eval Hub is planned.
5. **Analyst recognition:** Absent from Gartner MQ for AI Platforms.
   Needs to be positioned as "agentic AI platform," not just "AI
   infrastructure."
6. **Agent memory:** Emerging competitive dimension. Research exists
   (RHAISTRAT-1345) but no GA product; competitors beginning to offer
   session persistence and long-term memory.

### Strategic recommendations

1. **Accelerate MCP ecosystem delivery** — consider phased GA: Gateway
   first (Envoy-based, closest to ready), then Registry/Catalog, then
   full Operator lifecycle.
2. **Tell the SPIFFE identity story aggressively** — the only
   standards-based, portable agent identity approach. Market before
   AWS's proprietary approach becomes the default.
3. **Invest in developer experience for BYOA** — reference architectures
   for LangChain/CrewAI/Anthropic SDK on OpenShift, agent templates in
   AI Hub, "deploy your first agent" experience competing with AWS's
   3-API-call Managed Harness.
4. **Leverage the OpenShell co-maintainer position** — position OpenShift
   AI as "the production runtime for OpenShell."
5. **Pursue Gartner/Forrester recognition** — submit for MQ
   consideration once AgentOps + MCP + Eval Hub stack is GA.

## Sources

[1] Gartner, "Predicts 40% of Enterprise Apps Will Feature Task-Specific AI Agents by 2026." https://www.gartner.com/en/newsroom/press-releases/2025-08-26-gartner-predicts-40-percent-of-enterprise-apps-will-feature-task-specific-ai-agents-by-2026-up-from-less-than-5-percent-in-2025
[2] Forrester, "The State Of Agentic AI In 2026: Companies Are Chasing, Few Are Catching." https://www.forrester.com/blogs/the-state-of-agentic-ai-in-2026-companies-are-chasing-few-are-catching/
[3] MCP ecosystem data: MCP 2026 Roadmap Blog, ChatForest, Arcade. https://blog.modelcontextprotocol.io/posts/2026-mcp-roadmap/
[4] A2A protocol: Linux Foundation Agentic AI Foundation. https://philippdubach.com/posts/mcp-vs-a2a-in-2026-how-the-ai-protocol-war-ends/
[5] NVIDIA Agent Toolkit / GTC 2026. https://venturebeat.com/technology/nvidia-launches-enterprise-ai-agent-platform-with-adobe-salesforce-sap-among
[6] NVIDIA OpenShell. https://www.redhat.com/en/blog/red-hat-ai-and-openshell-driving-security-enhanced-agent-execution-for-enterprise-ai
[7] Red Hat AI Inference / llm-d / vLLM. https://developers.redhat.com/articles/2026/06/11/intelligent-inference-scheduling-llm-d-red-hat-ai
[8] Red Hat Summit 2026. https://siliconangle.com/2026/05/12/red-hat-targets-enterprise-deployment-new-version-ai-platform/
[9] IBM watsonx Orchestrate / Agentic Control Plane. https://www.ibm.com/new/announcements/introducing-the-agentic-control-plane
[10] IBM Think 2026. https://www.ibm.com/new/announcements/ibm-announcements-at-think-2026
[11] Gartner Magic Quadrants 2026. https://www.ibm.com/new/announcements/ibm-named-a-leader-in-the-2026-gartner-magic-quadrant-ai-platforms
[12] IBM Sovereign Core on Red Hat. https://siliconangle.com/2026/02/24/red-hat-readies-metal-agent-ai-infrastructure-stack-hybrid-cloud-deployments/
[13] Google Gemini Enterprise Agent Platform / Cloud Next 2026. https://cloud.google.com/blog/products/ai-machine-learning/more-ways-to-build-and-scale-ai-agents-with-vertex-ai-agent-builder
[14] AWS Bedrock AgentCore. https://aws.amazon.com/bedrock/agentcore/
[15] AWS AgentCore Identity. https://aws.amazon.com/blogs/machine-learning/introducing-amazon-bedrock-agentcore-identity-securing-agentic-ai-at-scale/
[16] Palo Alto Networks Unit 42 AgentCore sandbox research. https://unit42.paloaltonetworks.com/bypass-of-aws-sandbox-network-isolation-mode/
[17] Gartner, Market Guide for Guardian Agents (Feb 2026). https://www.gartner.com/en/newsroom/press-releases/2025-06-11-gartner-predicts-that-guardian-agents-will-capture-10-15-percent-of-the-agentic-ai-market-by-2030
[18] Microsoft Build 2026 / OpenShell. https://ground.news/article/microsoft-build-2026-windows-gets-built-in-ai-agent-sandboxing-with-mxc-openclaw-support-and-nvidia-openshell
[19] Databricks Mosaic AI / Agent Bricks. https://www.databricks.com/blog/mosaic-ai-announcements-data-ai-summit-2025
[20] Databricks managed MCP servers / Unity AI Gateway. https://www.databricks.com/blog/announcing-managed-mcp-servers-unity-catalog-and-mosaic-ai-integration
[21] Anyscale / Ray. https://www.anyscale.com/blog/announcing-anyscale-agent-skills-ray
[22] SPIFFE / agent identity. https://www.hashicorp.com/en/blog/spiffe-securing-the-identity-of-agentic-ai-and-non-human-actors
[23] MLflow / agent observability. https://mlflow.org/articles/what-is-agent-observability-a-2026-developer-guide/
[24] IDC Asia-Pacific AI forecast. https://medium.com/@Lisamedrouk/2026-ai-predictions-what-gartner-forrester-and-idc-reveal-for-tech-leaders-96cbe36b7985
