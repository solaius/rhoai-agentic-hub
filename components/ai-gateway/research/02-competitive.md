---
title: "AI Gateway Competitive Landscape (July 2026)"
description: Competitive analysis of the AI gateway/proxy market covering open-source, cloud-provider, and commercial solutions with feature matrix and gap analysis.
timestamp: 2026-07-31
lens: competitive
review_after: 2026-10-31
---

# AI Gateway Competitive Landscape (July 2026)

The AI gateway category formalized rapidly in 2025-2026. Gartner published
its first Market Guide for AI Gateways in February 2026, and its Technology
Adoption Roadmap found that more than two-thirds of software engineering
leaders are already engaged with the technology. Worldwide spend on AI
platforms is projected at $64B in 2026 (up 63% YoY). This document surveys
the competitive field across three segments — open-source, cloud-provider,
and commercial/SaaS — then maps Red Hat's Praxis-based AI Gateway against
the field.

---

## 1. Open-Source AI Gateways and Proxies

### 1.1 LiteLLM

LiteLLM is the most widely adopted open-source AI proxy, supporting 140+
providers and 1,892 models behind a unified OpenAI-compatible API. In
2025-2026 it began migrating its hot path from Python to Rust, splitting
the codebase into a Rust core (request transforms, streaming, token
counting) and a Python host (I/O, auth, routing, callbacks). Two deployment
modes are available: a hybrid mode where Python handles the request and
Rust handles translation (opt-in per model), and a full Rust gateway mode
using an Axum server binary.

Benchmarks show the Rust gateway adding approximately 0.05 ms overhead per
request versus 7.5 ms for the Python path, serving 6,782 RPS at 31.7 MB
peak memory versus 358.9 MB for Python. Against Portkey and Bifrost, the
Rust path showed roughly 7x lower overhead and 9x less memory.

**Strengths**: Widest provider coverage by far. Production-proven. Strong
cost tracking and virtual key management. Growing Rust performance story.
Apache 2.0 license.

**Gaps relative to Red Hat**: Not Kubernetes-native — no CRDs, no EPP
integration, no InferencePool-aware routing. No server-side agentic
orchestration (Responses API loop). No composable filter pipeline. No
native guardrails integration (relies on callbacks). No distributed
inference scheduling. No air-gapped deployment story.

### 1.2 Envoy AI Gateway / Gateway API Inference Extension (GIE)

The Gateway API Inference Extension (kubernetes-sigs/gateway-api-inference-extension)
is the Kubernetes-native approach to inference routing. It uses Envoy's
ext_proc protocol to upgrade any Gateway API-compatible proxy (Envoy
Gateway, kgateway, GKE Gateway) into an inference gateway. Core CRDs
include InferencePool and InferenceModel. The Endpoint Picker (EPP)
examines live pod metrics (queue depth, KV cache utilization, loaded
adapters) to select the optimal model server replica.

The project recently restructured: the EPP, InferenceObjective, and
Body-Based Router packages moved to separate repositories. The original
repo now hosts the lightweight EPP (LWEPP) and InferencePool API plus
conformance tests. GIE is driven by WG-Serving under SIG-Network and has
partnered with vLLM/llm-d for scheduling integration.

**Strengths**: Kubernetes-native with proper CRDs. Community-driven under
k8s-sigs governance. Model-aware routing with live metrics. Conformance
test suite. Foundation for GKE AI Gateway.

**Gaps relative to Red Hat**: GIE solves placement, not the AI application
layer. No API translation, no credential management, no guardrails, no
agentic orchestration. The ext_proc model that GIE depends on is exactly
the extension ceiling that motivated the Praxis decision — each capability
requires another gRPC round trip, and filters cannot share request context.

### 1.3 agentgateway

Originally created by Solo.io and donated to the Linux Foundation's
Agentic AI Foundation in June 2026, agentgateway is a Rust-based proxy
focused on AI-native protocols (MCP, A2A). It provides four unified
functions: LLM gateway (multi-provider routing with OpenAI-compatible API),
MCP gateway (tool federation, stdio/HTTP/SSE/Streamable HTTP), A2A gateway
(agent-to-agent communication), and inference routing (via GIE integration).

It achieves approximately 500K QPS with 512 connections and sub-0.2 ms P99
latency at 30K QPS. Contributors include AWS, Cisco, Huawei, IBM, Microsoft,
Red Hat, Shell, and Zayo. The project supports the upcoming MCP 2026-07-28
protocol version.

**Strengths**: Rust performance. Strong MCP and A2A protocol support. Linux
Foundation governance with broad contributor base. Native Entra OAuth
provider. Growing community (300+ contributors, 60+ organizations).

**Gaps relative to Red Hat**: Monolithic architecture — no composable filter
pipeline or extension mechanism. No server-side Responses API orchestration.
No inline streaming guardrails during an agentic loop. No native distributed
inference integration (wraps GIE rather than owning placement). Red Hat's AI
Gateway team evaluated agentgateway twice and found it structurally unfit
for the full-stack needs: it proxies but does not own the AI request
lifecycle.

### 1.4 Portkey AI Gateway

Portkey was an open-source (Apache 2.0) AI gateway with a managed cloud
offering. It supported 250+ models, real-time dashboards, content-safety
guardrails (PII redaction, jailbreak detection), and SOC2/ISO/HIPAA
certifications. However, Palo Alto Networks completed its acquisition of
Portkey in May 2026, folding it into the Prisma AIRS security platform.

**Post-acquisition impact**: Portkey is now a proprietary security-suite
component. Its TypeScript runtime adds 30-40 ms gateway overhead. Teams
not in the Prisma ecosystem face uncertainty. No automatic fallbacks,
adaptive load balancing, or geo-aware routing.

### 1.5 Bifrost (Maxim AI)

Bifrost is an open-source (Apache 2.0) AI gateway built in Go, launched
August 2025. It unifies LLM, MCP, and Agents gateway capabilities. In
benchmarks at 5,000 RPS, it adds only 11 microseconds of overhead per
request. It supports 20+ providers, hierarchical cost control, virtual
keys, and MCP tool allow-lists per key.

**Strengths**: Very low latency. Apache 2.0 with no paywalled core features.
Growing MCP support. Prometheus/OTEL observability.

**Gaps relative to Red Hat**: Smaller provider coverage (20+ vs LiteLLM's
140+). No Kubernetes-native CRDs or inference-aware routing. No server-side
agentic orchestration. Newer project with maturing community.

### 1.6 TrueFoundry

TrueFoundry is a venture-backed AI infrastructure platform recognized in
Gartner's 2025 Market Guide for AI Gateways. It processes over 1 trillion
tokens per day and manages 1,000+ clusters. In June 2026 it launched
Agent Gateway, a unified control plane for agent-tool-LLM traffic with
JWT/RBAC, sub-3 ms internal latency, and SOC 2/HIPAA/ITAR compliance. It
acquired Seldon AI in 2026.

**Strengths**: Enterprise-grade at scale. MCP gateway with cost-savings
claims. On-premise/VPC deployment. Gartner recognition.

**Gaps relative to Red Hat**: Proprietary SaaS platform, not open-source
infrastructure. No composable filter pipeline. No distributed inference
integration. Vendor lock-in risk.

---

## 2. Cloud Provider AI Gateways

### 2.1 Google GKE AI Gateway

The closest architectural analog to Red Hat's approach. Built on GIE, it
adds GKE-specific CRDs (InferencePool, InferenceObjective), body-based
routing, prefix-cache-aware routing, load-aware routing, and admission
control. In March 2026, Google announced multi-cluster GKE Inference Gateway
for cross-region routing. At Next '26 (April), "predictive latency boost"
replaced heuristic routing with ML-driven capacity-aware routing, cutting
TTFT latency by over 70%.

Vertex AI reduced TTFT P95 by 2x for DeepSeek V3.1 and doubled prefix
cache hit rates (35% to 70%) using the gateway. Apigee integration adds
policy enforcement via GCPTrafficExtension. Model Armor provides guardrails.

**Assessment**: Most advanced inference routing in production, but GKE-only.
No multi-provider API translation. No server-side agentic orchestration.
Tightly coupled to Google Cloud. Not available for on-premise or air-gapped
environments.

### 2.2 AWS: Bedrock + AgentCore Gateway

AWS has two distinct approaches. First, a reference architecture using
Amazon API Gateway in front of Bedrock for JWT auth, quotas, throttling,
and WAF integration — essentially a traditional API gateway pattern with
Lambda-based request signing.

Second, Amazon Bedrock AgentCore Gateway (August 2025) — a fully managed
service providing a centralized entry point for agentic traffic with
native MCP support, zero-code MCP tool creation from REST APIs (OpenAPI
and Smithy), intelligent tool discovery, and built-in authorization. It
transforms existing APIs into MCP servers and integrates with AWS
Marketplace.

**Assessment**: AgentCore Gateway is a strong agentic play within the AWS
ecosystem. However, it is fully managed (no self-hosting), AWS-only, and
focused on MCP tool governance rather than full-stack inference routing.
No open-source component. No air-gapped option.

### 2.3 Azure AI Gateway (API Management)

Azure API Management has evolved into a comprehensive AI gateway. At Build
2026, Microsoft shipped three headline features: a Unified Model API
(standardize on OpenAI format while APIM transforms to Anthropic, Vertex,
etc.), content safety policies extended to MCP and A2A traffic, and
expanded token metrics covering reasoning, cached, and audio tokens.

Additional capabilities include token-aware rate limiting, semantic caching,
MCP server support (September 2025), and API Center MCP Server (GA) for
unified discovery. The Unified Model API is the closest analog to Red Hat's
API translation ambitions, though it currently supports only OpenAI Chat
Completions as the client-facing format.

**Assessment**: Broadest multi-protocol governance among cloud providers.
Strong MCP and A2A content safety. But Azure-only, no self-hosting, no
inference-aware routing, and no agentic orchestration loop. APIM is an
API management platform being extended for AI, not an AI-native proxy.

### 2.4 IBM API Connect AI Gateway

IBM's AI Gateway is an integrated feature within API Connect (not a
separate service). It provides REST proxies for AI models, cost management
through rate limiting and response caching, governance via policy
enforcement and PII masking, and a guided wizard for developer self-service.
Expanded to additional models and deployments in November 2025. API Connect
V12 (December 2025) added the DataPower Nano Gateway (sub-20 MB footprint),
AI-powered API Studio, and a converged control plane.

**Assessment**: Enterprise API governance strength, but no model-aware
routing, no inference scheduling, no agentic orchestration. Positioned as
API management with AI features rather than an AI-native gateway.

---

## 3. Commercial / SaaS AI Gateways

### 3.1 Kong AI Gateway

Kong extends its general-purpose API gateway with 60+ AI-specific features
through a plugin architecture (MetaPlugin with lifecycle filters). Key
plugins include AI Proxy Advanced (multi-provider routing with semantic
routing and load balancing), AI Prompt Guard (regex/string-based content
inspection), AI RAG Injector, AI Compressor, MCP Proxy, and A2A Plugin.
Third-party guardrails integrations include AWS Guardrails, Azure AI
Content Safety, and Google Model Armor. CrowdStrike and Impart Security
integrations address prompt/response inspection.

**Strengths**: Mature API gateway platform. Extensive plugin ecosystem.
MCP and A2A support. OpenTelemetry. Metering and billing.

**Gaps relative to Red Hat**: Plugin architecture grafted onto a general-
purpose gateway — not AI-native. No inference-aware routing or distributed
scheduling. No server-side agentic orchestration. Proprietary enterprise
tier for advanced features.

### 3.2 Cloudflare AI Gateway

An edge AI proxy running on Cloudflare's global network. Supports 23+
providers. Core features include response caching (up to 90% latency
reduction), rate limiting (fixed/sliding window plus cost-based budgets),
retry/fallback, request routing by geography/user segment, and guardrails
with content moderation. A unified REST API launched May 2026. Free tier
includes 100K logs/month.

**Strengths**: Edge deployment at global scale. Free core tier. Strong
caching and rate limiting. Simple setup.

**Gaps relative to Red Hat**: SaaS-only, no self-hosting or air-gapped
deployment. No inference-aware routing. No agentic orchestration. No
Kubernetes integration. Limited to edge proxy use case.

### 3.3 Intelligent Routing (RouteLLM, Unify AI, Martian)

A distinct sub-category focused on per-request model selection rather than
full gateway functionality. RouteLLM (Berkeley/LMSys, ICLR 2025) uses
trained routers achieving 85% cost reduction while maintaining 95% of
GPT-4 performance. Unify AI focuses on evaluation-driven routing based on
empirical quality metrics. Martian raised a $9M Series A in 2024 but has
pivoted to AI interpretability research in 2026.

These are routing algorithms, not gateways. They can be embedded within a
gateway but do not provide API translation, credential management, guardrails,
or orchestration. Red Hat's Praxis architecture subsumes this capability
through composable routing filters (Semantic Router convergence) and
llm-d's inference scheduler.

---

## 4. Feature Comparison Matrix

| Capability | Red Hat (Praxis) | LiteLLM | Envoy AI GW / GIE | agentgateway | Portkey | Bifrost | TrueFoundry | GKE AI GW | AWS AgentCore | Azure APIM | IBM API Connect | Kong | Cloudflare |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **Multi-provider API translation** | Planned (3.6) | 140+ providers | No | Partial (OpenAI-compat) | 250+ | 20+ | Multi-provider | No (GKE-only) | Bedrock-focused | Unified Model API (preview) | Limited | Multi-provider | 23+ providers |
| **Server-side agentic loop** | Planned (3.6) | No | No | No | No | No | No | No | MCP tool orchestration | No | No | No | No |
| **Composable filter pipeline** | Core design | Callbacks | ext_proc chain | No | No | No | No | No | No | Policy chain | Policy chain | Plugin chain | No |
| **Inline streaming guardrails** | Planned (3.6) | Via callbacks | No | No | Yes (built-in) | Enterprise tier | Yes | Model Armor | AWS Guardrails | Content safety policies | PII masking | 3rd-party plugins | Content moderation |
| **Multi-tenancy / policy composition** | Planned (3.6) | Virtual keys | No | RBAC/JWT | SOC2/HIPAA | Virtual keys | JWT/RBAC | Via Apigee | IAM-based | Subscription keys | API plans | Consumer groups | Per-gateway |
| **Credential mgmt / BYOK** | Planned (3.6) | Virtual keys | No | No | Vault | Virtual keys | Key management | GCP IAM | IAM roles | Managed Identity | API keys | Vaults | BYOK |
| **Cost controls / session budgets** | Planned | Spend tracking | No | Budget controls | Log-based | Hierarchical | Token tracking | No | No | Token-aware quotas | Rate limiting | AI Rate Limiting | Cost-based budgets |
| **Inference-time scaling (fan-out)** | Planned (Praxis fan-out) | No | EPP placement | Via GIE | No | No | No | Prefix-cache routing | No | No | No | No | No |
| **Kubernetes-native** | Yes (CRDs) | No | Yes (CRDs) | Optional | No | No | K8s support | GKE-only | Managed | Managed | Hybrid | Optional | No |
| **Distributed inference (llm-d)** | Integrated | No | Partnered | No | No | No | No | Integrated (GKE) | No | No | No | No | No |
| **Air-gapped operation** | Yes | Self-host capable | Yes | Yes | No | Self-host | VPC/on-prem | No | No | No | On-prem | Self-host | No |
| **MCP protocol support** | Via MCP Gateway | No | No | Native | Limited | Yes | MCP Gateway | No | Native MCP | MCP server support | No | MCP Proxy plugin | No |
| **A2A protocol support** | Future | No | No | Native | No | No | No | No | No | A2A content safety | No | A2A plugin | No |
| **Open-source governance** | CNCF planned | Apache 2.0 | k8s-sigs | LF Agentic AI | Acquired (Palo Alto) | Apache 2.0 | Proprietary | Proprietary | Proprietary | Proprietary | Proprietary | Apache 2.0 core | Proprietary |
| **Implementation language** | Rust | Python + Rust | Go | Rust | TypeScript | Go | Unknown | Go | Managed | Managed | Managed | Lua/Go | Managed |

---

## 5. Where Red Hat Leads

**Server-side agentic orchestration under unified policy.** No competitor
offers a server-side Responses API loop where every iteration, tool call,
and fan-out candidate traverses the full policy pipeline (auth, quotas,
metering, audit, guardrails). LiteLLM proxies the Responses endpoint but
does not own the loop. agentgateway proxies MCP and A2A but does not
orchestrate. Azure APIM applies content safety to MCP tool calls but does
not run the agentic loop itself. This is the single most differentiating
capability in the Praxis design.

**Full-stack integration (routing + scheduling + distributed inference).**
Praxis owns the AI application layer while llm-d (CNCF sandbox, co-founded
by Red Hat) owns placement. No other solution integrates API translation,
agentic orchestration, guardrails, and inference scheduling in a single
traversal. GKE AI Gateway comes closest but is locked to Google Cloud and
lacks API translation and agentic orchestration.

**Composable filter pipeline in an AI-native proxy.** Praxis filters share
request context, identity, and configuration within a single traversal.
This avoids the ext_proc round-trip tax (Envoy AI Gateway, GIE) and the
plugin-chain overhead (Kong, Azure APIM). Only Praxis is designed from the
ground up as an AI-first proxy rather than an API gateway extended for AI.

**Air-gapped and on-premise deployment.** Among full-featured AI gateways,
only Red Hat, Envoy AI Gateway, and agentgateway support fully disconnected
deployment. Cloud provider gateways (GKE, AWS, Azure) are managed services.
Portkey is now proprietary. Red Hat's OpenShift-native deployment with
FIPS-validated cryptography and disconnected registry support is a hard
requirement for regulated industries (defense, financial services, healthcare).

---

## 6. Where Red Hat Trails

**Provider coverage.** LiteLLM supports 140+ providers today. Red Hat's
API translation is planned for 3.6 with an initial set. Catching up on
long-tail providers will require community contribution or a translation
shim layer.

**Production maturity.** LiteLLM, Kong, and Cloudflare have years of
production deployment. Praxis is pre-GA. The 3.6 delivery (Praxis replacing
IPP via ext_proc, with Envoy still at the front door) is the first
production milestone. Full Envoy replacement is post-3.6.

**MCP and A2A protocol support.** agentgateway and Kong have native MCP and
A2A protocol handling today. Red Hat's MCP Gateway is a separate component
(converging with AI Gateway in subsequent releases). A2A is not yet on the
roadmap. As MCP and A2A mature into the standard agent connectivity
protocols, parity will be expected.

**Edge and global distribution.** Cloudflare AI Gateway runs on 300+ edge
locations globally. Red Hat's gateway is cluster-local. Multi-cluster
inference routing (as GKE announced in March 2026) is not yet addressed.

**Self-serve developer experience.** Portkey (pre-acquisition), Cloudflare,
and TrueFoundry offer dashboard-driven setup with minutes-to-first-request.
Red Hat's operator-based deployment targets platform teams, not individual
developers.

---

## 7. Unsolved Problems (Industry Gaps)

**Whole-session cost enforcement across agentic loops.** No gateway today
can enforce a dollar budget across a multi-turn Responses API session that
spans tool calls, fan-out candidates, and guardrail invocations. Token-
level rate limiting (Azure APIM, Kong) and spend tracking (LiteLLM) operate
per-request, not per-session. Praxis's design (the agentic loop inside the
policy pipeline) is the only architecture positioned to solve this, but
it is not yet implemented.

**Cross-provider guardrails in streaming agentic loops.** Guardrails today
are either pre-request (prompt guards) or post-response (content filters).
No solution applies guardrails to streaming tokens mid-generation within
an agentic loop iteration, across different providers, with the ability to
halt the loop. Praxis's filter pipeline could enable this but the
implementation is future work.

**Portable inference scheduling across clouds and on-premise.** GKE AI
Gateway has the most advanced inference routing but is GKE-only. llm-d is
Kubernetes-native and multi-cloud, but integration with a full AI gateway
(API translation, guardrails, orchestration) exists only in Red Hat's
design. No vendor offers a portable stack that works identically on GKE,
EKS, AKS, and bare metal.

**Multi-tenant agentic governance.** Enterprises need per-tenant tool
allow-lists, per-tenant model access policies, and per-tenant cost
envelopes — all enforced within the agentic loop. Bifrost has per-key MCP
tool allow-lists; Azure APIM has subscription-level token quotas; but no
solution composes these into tenant-level agentic session governance.

---

## 8. Market Trends

### Consolidation along two axes

The market is splitting between **security/platform incumbents acquiring
gateways** (Palo Alto acquiring Portkey, Kong adding AI plugins to its
existing platform, Azure extending APIM) and **open-source neutral ground**
(agentgateway under the Linux Foundation, llm-d under CNCF, GIE under
k8s-sigs). Red Hat's CNCF sandbox plan for Praxis aligns with the
neutral-ground trajectory, which is strategically important for enterprise
buyers who want to avoid single-vendor AI infrastructure lock-in.

### Rust becoming the AI infrastructure language

The 2025 State of Rust survey shows 48.8% organizational adoption (up 10.1
points in two years). In AI proxy/gateway infrastructure specifically, the
trend is unmistakable: LiteLLM is rewriting its hot path in Rust,
agentgateway is Rust-native, and Praxis is Rust-native. Go remains strong
(Bifrost, GIE, Envoy Gateway) but Rust's memory safety, zero-GC tail
latency, and async streaming performance (Tokio) make it the preferred
choice for AI data planes where every millisecond of overhead is multiplied
across agentic loop iterations.

### Agentic protocols reshaping the category

The emergence of MCP (now under the Agentic AI Foundation) and A2A as
standard agent connectivity protocols is reshaping what "AI gateway" means.
In 2024, gateways translated API formats. In 2026, gateways must also
govern tool access, orchestrate agent workflows, and enforce policy across
multi-step autonomous operations. This evolution favors AI-native
architectures (Praxis, agentgateway) over extended API gateways (Kong,
Azure APIM, IBM API Connect).

### Inference scheduling as table stakes

GKE's predictive latency boost, llm-d's CNCF acceptance, and GIE's
conformance test suite signal that KV-cache-aware, prefix-aware inference
routing is becoming expected infrastructure. Gateways that only route to
provider APIs (LiteLLM, Cloudflare, Portkey) will face pressure to
integrate scheduling or cede that layer.

### EU AI Act driving compliance features

The EU AI Act's high-risk system rules take full effect in August 2026,
requiring comprehensive logging, traceability, and policy enforcement.
Gateways that can demonstrate audit trails across agentic sessions (not
just individual requests) will have a regulatory compliance advantage.

---

## 9. Strategic Implications for Red Hat

1. **Speed to GA matters more than feature completeness.** LiteLLM and
   agentgateway have production users today. Every quarter of delay
   increases the risk that one of them adds enough Kubernetes-native
   features to close the gap. The 3.6 milestone (Praxis via ext_proc,
   Responses API, API translation, guardrails) must ship on time.

2. **CNCF sandbox submission is a strategic accelerant.** The agentgateway
   donation to the Linux Foundation demonstrates that open governance wins
   enterprise trust. Praxis under CNCF would give Red Hat neutral-ground
   credibility that proprietary competitors (TrueFoundry, Azure, AWS)
   cannot match.

3. **Provider coverage needs a community strategy.** Building 140+ provider
   translations in-house is not viable. A community contribution model
   (similar to LiteLLM's provider plugin system) or a compatibility shim
   that wraps LiteLLM's translation layer would accelerate coverage.

4. **MCP/A2A convergence is a timeline question, not an if.** The AI
   Gateway and MCP Gateway are separate components today. Competitors
   (agentgateway, Kong, Azure APIM) already unify LLM, MCP, and A2A
   traffic. The convergence plan should be on the public roadmap.

5. **The agentic-loop-under-policy story is the moat.** No competitor has
   it. Every competitive comparison should lead with this capability
   because it is architecturally difficult to retrofit onto proxy-based
   designs.

---

## Sources

- [LiteLLM GitHub](https://github.com/BerriAI/litellm) and [Rust migration blog](https://docs.litellm.ai/blog/litellm-rust-launch)
- [LiteLLM Rust benchmarks](https://docs.litellm.ai/blog/rust-ai-gateway-benchmarks)
- [Gateway API Inference Extension](https://github.com/kubernetes-sigs/gateway-api-inference-extension) and [docs](https://gateway-api-inference-extension.sigs.k8s.io/)
- [Introducing Gateway API Inference Extension (k8s blog)](https://kubernetes.io/blog/2025/06/05/introducing-gateway-api-inference-extension/)
- [agentgateway GitHub](https://github.com/agentgateway/agentgateway) and [website](https://agentgateway.dev/)
- [Linux Foundation agentgateway announcement](https://www.linuxfoundation.org/press/linux-foundation-welcomes-agentgateway-project-to-accelerate-ai-agent-adoption-while-maintaining-security-observability-and-governance)
- [agentgateway design blog](https://agentgateway.dev/blog/2026-06-04-designing-agentgateway-unified-gateway/)
- [Bifrost AI Gateway docs](https://docs.getbifrost.ai/overview) and [Bifrost vs Portkey comparison](https://www.truefoundry.com/blog/bifrost-vs-portkey)
- [Kong AI Gateway docs](https://developer.konghq.com/ai-gateway/) and [product page](https://konghq.com/products/kong-ai-gateway)
- [Cloudflare AI Gateway docs](https://developers.cloudflare.com/ai-gateway/) and [features](https://developers.cloudflare.com/ai-gateway/features/)
- [GKE Inference Gateway docs](https://docs.cloud.google.com/kubernetes-engine/docs/concepts/about-gke-inference-gateway)
- [Multi-cluster GKE Inference Gateway (Google blog)](https://cloud.google.com/blog/products/containers-kubernetes/multi-cluster-gke-inference-gateway-helps-scale-ai-workloads)
- [GKE Inference Gateway prefix caching (Google blog)](https://cloud.google.com/blog/products/containers-kubernetes/gke-inference-gateway-prefix-caching-accelerates-ai-inference)
- [Apigee + GKE Inference Gateway integration](https://developers.googleblog.com/en/apigee-operator-for-kubernetes-and-gke-inference-gateway-integration-for-auth-and-aillm-policies/)
- [AWS AI Gateway reference architecture](https://aws.amazon.com/blogs/architecture/building-an-ai-gateway-to-amazon-bedrock-with-amazon-api-gateway/)
- [Amazon Bedrock AgentCore Gateway announcement](https://aws.amazon.com/blogs/machine-learning/introducing-amazon-bedrock-agentcore-gateway-transforming-enterprise-ai-agent-tool-development/)
- [Azure APIM AI gateway capabilities](https://learn.microsoft.com/en-us/azure/api-management/genai-gateway-capabilities)
- [Azure APIM Build 2026 announcements (InfoQ)](https://www.infoq.com/news/2026/06/azure-apim-ai-gateway-build/)
- [IBM API Connect AI Gateway expansion](https://www.ibm.com/new/announcements/ibm-api-connect-expands-its-ai-gateway-feature-to-additional-models-and-deployments)
- [IBM API Connect agentic AI announcement](https://www.ibm.com/new/announcements/ibm-api-connect-advances-api-innovation-for-the-agentic-ai-future)
- [TrueFoundry Agent Gateway launch](https://www.businesswire.com/news/home/20260602233322/en/TrueFoundry-Launches-Agent-Gateway-to-Close-the-Enterprise-AI-Governance-Gap)
- [TrueFoundry Gartner recognition](https://www.businesswire.com/news/home/20260220396246/en/CORRECTING-and-REPLACING-TrueFoundry-Recognized-as-a-Representative-Vendor-in-Gartner-Market-Guide-for-AI-Gateways)
- [TrueFoundry MCP Gateway blog](https://www.truefoundry.com/blog/truefoundry-mcp-gateway-critical-infrastructure-for-productive-and-secure-enterprise-ai-in-2026)
- [RouteLLM / LLM routing landscape](https://zylos.ai/research/2026-01-29-llm-routing-intelligent-model-selection/)
- [MCP/A2A protocol landscape (Zuplo)](https://zuplo.com/blog/agent-protocol-stack-mcp-a2a-acp-2026)
- [Agent gateways as control plane (Forbes)](https://www.forbes.com/sites/janakirammsv/2026/07/05/agent-gateways-are-becoming-the-control-plane-for-enterprise-ai/)
- [Gartner AI platforms market forecast](https://www.gartner.com/en/newsroom/press-releases/2026-07-20-gartner-forecasts-worldwide-ai-platforms-and-models-market-to-grow-63-percent-in-2026)
- [LLM Gateway Comparison 2026 (FloTorch)](https://www.flotorch.ai/blogs/llm-gateway-comparison-2026)
- [Rust in AI infrastructure 2026 (Zylos)](https://zylos.ai/research/2026-04-01-rust-native-ai-agent-frameworks-ecosystem-2026/)
- [Rust vs Go for AI infrastructure benchmarks](https://dev.to/gabrielanhaia/rust-vs-go-for-ai-infrastructure-in-2026-heres-what-the-benchmarks-actually-say-4j28)
- [llm-d website](https://llm-d.ai/) and [GitHub](https://github.com/llm-d/llm-d)
- [llm-d CNCF sandbox announcement](https://lucaberton.com/blog/llm-d-cncf-kubernetes-distributed-inference-2026/)
- [llm-d Red Hat Developer article](https://developers.redhat.com/articles/2025/05/20/llm-d-kubernetes-native-distributed-inferencing)
