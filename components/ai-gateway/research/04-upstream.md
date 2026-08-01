---
title: "AI Gateway Upstream Projects and Standards Alignment"
description: Analysis of upstream projects, specifications, and standards that the AI Gateway depends on or must align with — Gateway API, GIE, Open Responses, Praxis, Istio/OSSM, Kuadrant, llm-d, MCP, and A2A.
timestamp: 2026-07-31
lens: upstream
review_after: 2026-10-31
---

# AI Gateway Upstream Projects and Standards Alignment

This document maps the upstream projects, industry specifications, and standards
bodies that the AI Gateway depends on or must align with. For each upstream, it
assesses maturity, Red Hat's involvement, alignment with the Praxis convergence
decision, and standards risks.

## 1. Kubernetes Gateway API

**Maturity**: GA (v1.5, released February 2026). The specification has been
stable since v1.0 (October 2023), with v1.5 graduating ReferenceGrant to v1
and adding ListenerSet. Over 20 conformant implementations exist. AWS, Istio,
NGINX, Envoy Gateway, and Contour all ship GA support. Monthly experimental
channel releases continue for new features.

**Red Hat involvement**: Red Hat engineers (Shane Utt, Keith Mattix) serve as
chairs of SIG Network and maintainers of Gateway API. Shane Utt co-founded
the AI Gateway Working Group (announced March 9, 2026), which operates under
SIG Network sponsorship.

**Alignment**: Praxis runs the official Gateway API conformance suite in CI
on every change. The 3.6 architecture attaches Praxis via ext_proc behind a
Gateway API-conformant gateway (OSSM 3.4), so conformance is both a CI gate
and a deployment prerequisite. The post-3.6 trajectory, in which Istio deploys
Praxis directly as the gateway data-plane image, preserves Gateway API
compatibility through the conformance suite.

**Risk**: Gateway API versioning follows a 4-month cadence with a "content
flexible, date fixed" policy. Praxis must track monthly experimental releases
for AI-relevant features (e.g., ListenerSet, BackendTLSPolicy updates) to
avoid drift between the conformance suite it runs and the spec version OSSM
ships.

## 2. Gateway API Inference Extension (GIE)

**Maturity**: GA. InferencePool graduated to v1
(`inference.networking.k8s.io/v1`) and is the sole supported API version.
InferenceModel, InferenceObjective, and InferenceModelRewrite provide the
companion CRDs. The Endpoint Picker (EPP) and Body Based Router (BBR) have
moved to separate repositories, with the main repo hosting the lightweight
EPP (LWEPP), InferencePool API, and conformance tests.

**Red Hat involvement**: Red Hat is a founding contributor to GIE through the
AI Gateway WG. Shane Utt and Morgan Foster are WG organizers. The llm-d
project, co-founded by Red Hat, implements the EPP specification and provides
the inference scheduling pipeline (Filter, Score, Pick) that GIE standardizes.

**Key proposals under the WG**:

- **Payload Processing**: Defines declarative processor configuration, ordered
  pipelines, and failure modes for prompt inspection, content filtering, and
  guardrails before requests reach the model server. This directly parallels
  the Praxis filter pipeline architecture.
- **Egress Gateways**: Standards for routing AI traffic to external providers
  (OpenAI, Vertex AI, Bedrock) with credential injection, regional compliance,
  and failover. Aligns with the 3.6 multi-provider API translation scope.
- **Agentic Networking Subproject**: Proposal for external MCP/A2A services,
  making them a stakeholder for egress gateways.

**Alignment**: The ext_proc protocol is the contractual interface between GIE
and proxy implementations. Praxis currently attaches as an ext_proc server
behind Envoy. The GIE EPP architecture proposal (0683) defines the same
three-stage pipeline (Routing, Flow Control, Scheduling) that llm-d
implements. The key alignment question is whether Praxis can subsume the
Body Based Router role natively through its filter pipeline, eliminating the
separate BBR ext_proc hop.

**Risk**: GIE's conformance tests are the community benchmark for inference
gateways. If Praxis deviates from the ext_proc interaction model (e.g., by
internalizing EPP logic directly), it must still pass conformance. The WG's
payload processing proposal may standardize filter semantics that differ from
Praxis's filter-chain model — track and contribute early.

## 3. Open Responses Specification

**Maturity**: Published specification (January 15, 2026). Defines the
`POST /v1/responses` endpoint, Items as fundamental context units, semantic
event streaming (SSE with typed events), tool definitions (internal and
external), and the agentic loop (reasoning, tool invocation, response
generation). Compliance tester available at openresponses.org/compliance.

**Ecosystem**: Launch partners include Hugging Face, OpenRouter, Vercel,
LM Studio, Ollama, and vLLM. Adoption is growing across the agentic AI
stack. Databricks documents Responses API compatibility in its model serving
layer.

**Red Hat involvement**: Red Hat contributes to vLLM, which is a launch
partner. The 3.6 scope includes native Responses API support with
server-side agentic loop orchestration in Praxis. Red Hat is exploring a
stateless variant optimized for vLLM's architecture, where conversation state
is managed by the gateway rather than the inference engine.

**Alignment**: Open Responses is the target API surface for Praxis's agentic
orchestration. The specification's tool definitions map to Praxis's tool
execution and fan-out primitives. The streaming semantics (SSE with
`[DONE]` terminal, typed event bodies) must be faithfully preserved through
the Praxis filter pipeline and guardrails inspection.

**Risk**: The specification is young and governed by a TSC that includes
OpenAI as the primary contributor. Features gaining "broad adoption among
frontier models" are candidates for standardization, which means the spec
could evolve in directions driven by proprietary provider interests. Red Hat
should contribute actively to ensure stateless and open-source inference
engine concerns are represented.

## 4. Praxis Upstream

**Maturity**: Active development. Praxis is a Rust-based, AI-native proxy
built on Cloudflare's Pingora framework (v0.8.1, June 2026). The upstream
organization (`praxis-proxy`) hosts multiple repositories: `praxis` (core
proxy), `ai` (AI-specific filters), `extproc` (ext_proc attachment mode),
and `operator` (Kubernetes lifecycle). Architecture follows a filter-first
extensibility model supporting multiple build profiles: reverse-proxy,
forward-proxy, AI inference, and agentic gateway.

**Pingora foundation**: Pingora is battle-tested at Cloudflare scale (40M+
requests/second). The v0.8.x series added mTLS client certificate
verification, L4 stream abstraction, and connection filtering. It provides
HTTP/1, HTTP/2, gRPC, and WebSocket proxying, with HTTP/3 on the roadmap.
MSRV is Rust 1.85. Linux is the tier-1 platform.

**CNCF trajectory**: A CNCF sandbox submission is planned. The competitive
landscape is crowded: agentgateway (Linux Foundation, backed by Solo.io and
Microsoft), kgateway (CNCF sandbox), Higress (CNCF sandbox, Alibaba),
Envoy AI Gateway (built on CNCF Envoy Gateway), and IBM ContextForge all
occupy adjacent space. Praxis differentiates through its filter-first
composition model and its role as the single AI data plane for RHOAI.

**Cross-org development**: Red Hat and IBM engineers contribute to Praxis.
The license is GPLv3 / LGPLv3.

**Risk — CNCF governance**: The sandbox submission requires allies and a
clear governance model. The GPLv3 license is unusual in the CNCF ecosystem
(most projects use Apache-2.0). This may create friction with the CNCF TOC
during evaluation and with potential contributors who prefer permissive
licenses. The governance structure needs to demonstrate multi-vendor
participation beyond Red Hat and IBM to satisfy CNCF sandbox requirements
of broad community support.

**Risk — competitive positioning**: Agentgateway already has Istio
integration (experimental in 1.30), Linux Foundation hosting, and backing
from Microsoft, Apple, Adobe, and others with 200+ contributors. Praxis
must articulate a distinct value proposition — the filter-first composition
model and deep integration with llm-d EPP are the strongest differentiators.

## 5. Istio and OpenShift Service Mesh (OSSM) Integration

**Current state**: OSSM 3.4 (July 2026) ships Istio 1.30 and introduces
the TrafficExtension API for extending Istio functionality. Praxis attaches
as an ext_proc server in the OSSM 3.4 deployment model, with Envoy remaining
the front-door proxy for TLS termination and non-AI traffic.

**Istio 1.30 features**: Ambient multicluster beta, Gateway API Inference
Extension beta support, and experimental agentgateway integration. The
TrafficExtension API (replacing WasmPlugin) supports both WebAssembly and
Lua extensions, providing a lighter-weight alternative to EnvoyFilter.

**Agentgateway in Istio**: Solo.io's agentgateway, now a Linux Foundation
project, has experimental integration in Istio 1.30 as a data-plane proxy
replacement for Envoy on gateway pods. Built in Rust (like ztunnel), it
handles MCP, A2A, and inference traffic with claims of 300x memory and 35x
throughput improvements over traditional gateways.

**Future trajectory for Praxis**: The post-3.6 plan is for Istio to deploy
and manage Praxis as the gateway data-plane image, similar to how
agentgateway is being integrated experimentally today. This requires
either XDS support in Praxis or a lightweight configuration distribution
alternative.

**Risk**: Microsoft is actively paving the integration path for agentgateway
in upstream Istio. If agentgateway becomes the default AI data-plane in
Istio before Praxis achieves the same integration level, the "Istio deploys
Praxis" trajectory may face community resistance. Contributing the Praxis
integration upstream to Istio should be a priority track.

## 6. Kuadrant Policy Model

**Current state**: Kuadrant v1 APIs are GA — AuthPolicy, RateLimitPolicy,
DNSPolicy, and TLSPolicy have graduated to v1 in their CRDs.
TokenRateLimitPolicy (v1alpha1) adds token-based rate limiting for AI
workloads, extracting `usage.total_tokens` from OpenAI-compatible responses
and enforcing limits through Limitador.

**Core components**:
- **Authorino**: Lightweight Envoy external authorization server supporting
  JWT, API key, mTLS, OPA, and K8s RBAC.
- **Limitador**: Rust-based generic rate limiter implementing the Envoy Rate
  Limit Service protocol (v3).

**Token rate limiting**: TokenRateLimitPolicy supports non-streaming
OpenAI-style responses. After receiving the response, the gateway extracts
token usage and sends a rate limit request to Limitador with the actual
token count as `hits_addend`. User segmentation integrates with AuthPolicy
for tier-based limits (e.g., free: 20K tokens/day, gold: 200K tokens/day).
Streaming response support is planned.

**Migration path**: In the Praxis convergence model, policy enforcement
(auth, rate limiting, metering) moves into the Praxis filter pipeline.
MaaS remains the definition layer — users define policies through MaaS CRDs,
and the MaaS controller translates them into Praxis filter configuration.
Kuadrant's Authorino and Limitador continue as the enforcement backends
that Praxis filters call.

**Alignment**: The key interface is the Envoy RLS protocol (v3), which
Limitador implements. As long as Praxis's rate-limiting filter speaks this
protocol, the Kuadrant integration is preserved. The token rate limiting
implementation requires response-body inspection, which fits naturally in
Praxis's filter pipeline but was a challenge in the ext_proc model.

**Risk**: Streaming token counting (the primary gap in TokenRateLimitPolicy)
is harder in Praxis because SSE events must be parsed incrementally. This
is an active development area for both Kuadrant and Praxis teams (Eguzki
Astiz Lezaun owns token rate limiting for 3.6).

## 7. llm-d and the Endpoint Picker (EPP)

**Maturity**: CNCF sandbox project (accepted March 2026 at KubeCon EU
Amsterdam). Founded by Red Hat, Google Cloud, IBM Research, CoreWeave,
and NVIDIA. Additional backing from AMD, Cisco, Hugging Face, Intel,
Lambda, and Mistral AI. Latest release: v0.7 (May 2026).

**EPP architecture**: The EPP is the intelligent routing layer that selects
the optimal model-server pod for each inference request. It follows a
three-stage pipeline: Filter (remove unhealthy or incompatible pods),
Score (rate pods on prefix cache locality, queue depth, hardware topology),
and Pick. In benchmarks on shared-prefix workloads, llm-d cut TTFT by
over 99% and doubled throughput without hardware changes.

**Key capabilities**: Prefix-cache-aware routing, disaggregated serving,
hierarchical KV cache (GPU hot, CPU warm, disk cold), multi-node tensor
and expert parallelism via LeaderWorkerSet, and predicted-latency
scheduling (GA in v0.7).

**Contract with Praxis**: The EPP communicates with the proxy through the
ext_proc protocol, the same interface GIE standardizes. The
scheduling-hints contract is bidirectional: the gateway sends request-level
hints (e.g., prefix hash, priority) downstream, and llm-d exposes pod-level
signals (cache state, queue depth, model readiness) upstream. This contract
must be preserved as Praxis replaces Envoy.

**Future consideration**: A Rust migration path for EPP exists as a
long-term possibility. If EPP were embedded as a library within Praxis
(rather than communicating via ext_proc), it could eliminate the gRPC
round-trip overhead. This is architecturally attractive but requires the
EPP maintainers (a multi-vendor community) to agree on a Rust
implementation alongside or replacing the current Go implementation.

**Risk**: llm-d's CNCF governance means its EPP interface is a community
standard. Praxis cannot unilaterally change the interaction model. Any
optimization (e.g., embedded EPP) must go through the llm-d community
process and maintain backward compatibility with other proxy
implementations (Envoy Gateway, Istio, NGINX Gateway Fabric).

## 8. Protocol Support: MCP, A2A, and Context Forge

### Model Context Protocol (MCP)

**Maturity**: The 2026-07-28 specification was published July 28, 2026 —
the largest revision since launch. Key changes: stateless protocol core
(sessions removed), `_meta` parameter carries version and capabilities per
request, `Mcp-Method` and `Mcp-Name` headers enable gateway routing without
JSON-RPC body inspection, cacheable list results with `ttlMs` and
`cacheScope`, W3C Trace Context propagation, and a formal extensions
framework.

**AI Gateway relevance**: The stateless core and routability headers are
directly designed for gateway infrastructure. The specification blog
explicitly calls out load balancers and gateways as first-class consumers
of the new headers. MCP tool-call traffic flowing through the Praxis
pipeline is a 3.6 scope item.

**Alignment**: The new `Mcp-Method` / `Mcp-Name` headers eliminate the
need for Praxis to parse JSON-RPC bodies for routing decisions — a
significant simplification. The deprecation of Roots, Sampling, and Logging
(with a 12-month window) means Praxis need not implement these features.
The extensions framework (Tasks, Skills over MCP, MCP Apps) will drive
future filter requirements.

### Agent-to-Agent Protocol (A2A)

**Maturity**: v1.0 stable (early 2026). Linux Foundation governance with
a TSC including AWS, Cisco, Google, IBM, Microsoft, Salesforce, SAP, and
ServiceNow. Over 150 production organizations, 22K+ GitHub stars, SDKs
in five languages. IBM's ACP merged into A2A in August 2025.

**AI Gateway relevance**: A2A defines agent-to-agent communication via
JSON-RPC 2.0 over HTTP/SSE/gRPC. Agent Cards
(`/.well-known/agent.json`) enable discovery. The Praxis agentic-gateway
build profile has started A2A support. The WG AI Gateway's Agentic
Networking Subproject is developing proposals for external MCP/A2A service
access through egress gateways.

**Alignment**: A2A's transport model (HTTP + SSE + optional gRPC) maps
cleanly to Praxis's protocol handling. The filter pipeline can enforce
policy on A2A traffic (auth, rate limiting, audit) without protocol-level
changes. Agent Card discovery could be cached and served through Praxis
as a registry function.

### IBM ContextForge

**Maturity**: v1.0.6 (July 22, 2026). Open-source AI gateway, registry,
and proxy from IBM that federates MCP, A2A, and REST/gRPC APIs. Supports
40+ plugins, OAuth RFC 8693 token exchange, HashiCorp Vault integration,
and MCP 2026-07-28 spec compliance.

**Relevance**: ContextForge represents IBM's approach to the same problem
space. Given IBM and Red Hat's shared investment in Praxis, ContextForge's
capabilities (protocol translation, plugin extensibility, registry) inform
what the community expects from an AI gateway. The Q3 2026 research
milestone for Context Forge compatibility should evaluate whether
ContextForge plugins or patterns can be adopted in Praxis.

## Standards Risk Summary

| Risk | Severity | Mitigation |
|---|---|---|
| CNCF sandbox rejection due to GPLv3 license | High | Evaluate license change to Apache-2.0 or dual-license; build coalition of non-Red Hat contributors before submission |
| Agentgateway preempts Praxis in Istio integration | Medium | Accelerate upstream Istio contribution track; differentiate on filter composition and llm-d EPP integration |
| Open Responses spec evolves toward proprietary provider interests | Medium | Active TSC participation; contribute stateless variant proposal; ensure vLLM alignment |
| GIE payload processing proposal standardizes different filter semantics | Medium | Shane Utt and Morgan Foster are WG organizers — contribute filter-pipeline perspective to the proposal |
| MCP 2026-07-28 deprecation timeline creates migration pressure | Low | Deprecation window is 12 months; plan Praxis MCP filter updates for Q1 2027 |
| llm-d community resists embedded EPP (Rust migration) | Low | This is a long-term optimization; maintain ext_proc compatibility as primary contract |
| Streaming token counting gap in Kuadrant | Low | Active development by Kuadrant team; Praxis's inline access to response bodies provides a better substrate than ext_proc |

## Sources

- [Gateway API v1.5 release blog](https://kubernetes.io/blog/2026/04/21/gateway-api-v1-5/)
- [Gateway API implementations](https://gateway-api.sigs.k8s.io/implementations/)
- [Gateway API Inference Extension (GIE)](https://github.com/kubernetes-sigs/gateway-api-inference-extension)
- [InferencePool v1 API reference](https://gateway-api-inference-extension.sigs.k8s.io/reference/spec/)
- [EPP architecture proposal (0683)](https://github.com/kubernetes-sigs/gateway-api-inference-extension/tree/main/docs/proposals/0683-epp-architecture-proposal)
- [Announcing the AI Gateway Working Group](https://kubernetes.io/blog/2026/03/09/announcing-ai-gateway-wg/)
- [WG AI Gateway proposals repo](https://github.com/kubernetes-sigs/wg-ai-gateway)
- [WG AI Gateway egress proposal](https://github.com/kubernetes-sigs/wg-ai-gateway/blob/main/proposals/10-egress-gateways.md)
- [Shane Utt — personal site and SIG Network chair](https://shaneutt.com/)
- [Open Responses specification](https://www.openresponses.org/specification)
- [Open Responses — Hugging Face explainer](https://huggingface.co/blog/open-responses)
- [Open Responses — InfoQ coverage](https://www.infoq.com/news/2026/02/openai-open-responses/)
- [Cloudflare Pingora (v0.8.1)](https://github.com/cloudflare/pingora)
- [CNCF sandbox applications](https://github.com/cncf/sandbox/issues)
- [Istio 1.30 release](https://istio.io/latest/news/releases/1.30.x/announcing-1.30/)
- [OSSM 3.4 introduction](https://www.redhat.com/en/blog/introducing-red-hat-openshift-service-mesh-34)
- [Istio ambient multicluster and GIE announcement](https://www.cncf.io/announcements/2026/03/25/istio-brings-future-ready-service-mesh-to-the-ai-era-with-new-ambient-multicluster-gateway-api-inference-extension-and-more/)
- [Agentgateway — Solo.io](https://agentgateway.dev/)
- [Agentgateway design blog](https://www.solo.io/blog/designing-agentgateway-a-unified-high-performance-gateway-for-ai-and-api-traffic)
- [Kuadrant TokenRateLimitPolicy overview](https://docs.kuadrant.io/dev/kuadrant-operator/doc/overviews/token-rate-limiting/)
- [Kuadrant TokenRateLimitPolicy — Red Hat Developer](https://developers.redhat.com/articles/2026/02/18/manage-ai-resource-use-tokenratelimitpolicy)
- [Kuadrant TokenRateLimitPolicy blog](https://kuadrant.io/blog/token-rate-limiting/)
- [llm-d — official site](https://llm-d.ai/)
- [llm-d GitHub](https://github.com/llm-d/llm-d)
- [llm-d CNCF acceptance blog](https://www.cncf.io/blog/2026/03/24/welcome-llm-d-to-the-cncf-evolving-kubernetes-into-sota-ai-infrastructure/)
- [llm-d — Red Hat Developer scheduling guide](https://developers.redhat.com/articles/2026/06/11/intelligent-inference-scheduling-llm-d-red-hat-ai)
- [MCP 2026-07-28 specification](https://modelcontextprotocol.io/specification/2026-07-28)
- [MCP 2026-07-28 release blog](https://blog.modelcontextprotocol.io/posts/2026-07-28/)
- [MCP stateless core — The Register](https://www.theregister.com/devops/2026/07/23/model-context-protocol-prepares-to-break-with-its-stateful-past/5276722)
- [A2A protocol specification](https://a2a-protocol.org/latest/specification/)
- [A2A GitHub](https://github.com/a2aproject/A2A)
- [A2A 150+ organizations milestone](https://stellagent.ai/insights/a2a-protocol-google-agent-to-agent)
- [IBM ContextForge](https://github.com/ibm/mcp-context-forge)
- [ContextForge architecture explainer](https://starlog.is/articles/ai-agents/ibm-mcp-context-forge/)
