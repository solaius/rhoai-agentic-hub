---
title: "AI Gateway Research: Executive Summary"
description: Living synthesis across architecture, competitive, requirements, and upstream lenses for the AI Gateway / Praxis convergence.
timestamp: 2026-07-31
updated: 2026-07-31
review_after: 2026-10-31
---

# AI Gateway Research: Executive Summary

This is the living synthesis for the ai-gateway research series. It
summarizes findings across four strategic lenses conducted 2026-07-31,
covering the Praxis convergence architecture, the AI gateway competitive
landscape, enterprise requirements, and upstream standards alignment.

## Series index

| Doc | Lens | Sources | Date |
|-----|------|---------|------|
| [01-architecture](01-architecture.md) | architecture | 22 | 2026-07-31 |
| [02-competitive](02-competitive.md) | competitive | 30+ | 2026-07-31 |
| [03-requirements](03-requirements.md) | requirements | 21 | 2026-07-31 |
| [04-upstream](04-upstream.md) | upstream | 33 | 2026-07-31 |
| [05-jira-gap](05-jira-gap.md) | jira-gap | internal cross-ref | 2026-07-31 |

## Key findings

### Strategic position

The Praxis convergence is architecturally differentiated through its
single-authority, composable filter pipeline — a design novel in the AI
gateway space where competitors either bolt AI capabilities onto existing
proxies (Envoy AI Gateway, Kong) or build application-layer routing
without infrastructure-grade proxy foundations (LiteLLM, agentgateway).
No competitor offers the combination of server-side agentic loop
orchestration under unified policy, KV-cache-aware inference scheduling
(llm-d EPP), and full Kubernetes-native deployment with air-gapped
support.

### Where Red Hat leads

1. **Agentic loop under unified policy.** Praxis is the only AI gateway
   that owns the server-side Responses API loop inside the policy
   pipeline, meaning every iteration, tool call, and fan-out candidate
   traverses auth, quotas, metering, and audit. No competitor ships this.

2. **Full-stack integration.** The three-layer architecture (front door,
   AI data plane, placement layer) bridges routing + scheduling +
   distributed inference — something gateway-only vendors (LiteLLM,
   Portkey, Cloudflare) structurally cannot replicate.

3. **Composable filter pipeline.** The "one router, one policy plane,
   one config authority" model eliminates the ext_proc proliferation and
   duplicate-router problems the current Envoy stack suffers from. New
   capabilities ship as filters, not new stacks.

4. **Air-gapped and on-premise deployment.** Among full-featured AI
   gateways, only Praxis and self-hosted LiteLLM support disconnected
   operation. Cloud-provider gateways (GKE, Bedrock, Azure APIM) are
   cloud-locked.

### Where Red Hat trails

1. **Provider coverage.** LiteLLM supports 100+ providers out of the
   box. Praxis 3.6 targets four (OpenAI, Anthropic, Bedrock, Vertex
   AI). The gap is meaningful for enterprises with diverse provider
   portfolios.

2. **Production maturity.** Praxis is pre-GA; competitors like LiteLLM,
   Kong, and Cloudflare have production deployments. The 3.6 EA/GA
   timeline is aggressive with FIPS, Konflux, and conformance gates all
   on the critical path.

3. **Developer experience.** LiteLLM's "one base-URL swap" developer
   experience is the standard customers expect. Praxis's Kubernetes-
   native CRD model is powerful but higher-friction for simple use cases.

4. **MCP/A2A protocol maturity.** agentgateway (Linux Foundation) has
   deeper MCP/A2A protocol support and is already experimentally
   integrated into Istio 1.30. Praxis A2A support has just started.

### Critical risks

1. **CNCF sandbox submission.** GPLv3 is unusual in the CNCF ecosystem
   (most projects use Apache-2.0). This may create friction with the
   TOC. agentgateway is already Linux Foundation-hosted with 200+
   contributors.

2. **Istio integration race.** Microsoft is paving the integration path
   for agentgateway in upstream Istio. If agentgateway becomes the
   default AI data-plane in Istio before Praxis achieves the same
   integration, the "Istio deploys Praxis" trajectory faces community
   resistance.

3. **FIPS 140-3 for Rust.** No pure-Rust crypto library has achieved
   FIPS 140-3 validation. Requires FFI to a validated C library
   (aws-lc-rs or similar). FIPS 140-2 sunsets September 21, 2026 —
   overlapping with the 3.6 timeline.

4. **3.6 delivery scope.** Praxis replacing IPP + Responses support at
   GA quality is the engineering goal, but multiple delivery risks
   converge: Konflux pipeline (largest risk per team), FIPS compliance,
   IPP parity conformance, conversation state continuity across the
   engine swap.

### Unsolved industry problems (opportunities)

No competitor has solved these; first-mover advantage is real:

- **Whole-session cost enforcement** spanning every loop iteration, tool
  call, and fan-out candidate as one budget tree
- **Streaming guardrails inside agentic loops** — applying PII detection
  and prompt injection defense to SSE tokens mid-stream during a
  multi-turn agentic session
- **Portable inference scheduling** — KV-cache-aware pod selection that
  works across providers and clusters (llm-d EPP is closest)
- **Multi-tenant agentic governance** — agent identity distinct from
  human identity with per-action authorization at scale

### Requirements readiness (3.6)

| Category | Table-Stakes Coverage | Key Gaps |
|---|---|---|
| FSI Compliance | Partial — guardrails and credentials land; FIPS is a risk | Automatic failover, structured audit format |
| Agent Governance | Structural foundation (loop under policy) | Explicit approval gates, delegated authority UI |
| Multi-Provider | Core 4 providers + model aliasing | 100+ provider parity with LiteLLM, semantic caching |
| Operational | Session budgets, credential management | Chargeback/cost attribution, cross-DC rate limiting |
| Security | Guardrails, tenant isolation, credential security | FIPS 140-3, streaming guardrails |
| Deployment | Kubernetes-native, on-prem | Air-gap qualification, multi-cluster routing (evaluating for 3.6 TP) |

The primary gaps are in operational maturity (chargeback, structured
audit trails, automatic failover) rather than structural architecture.
The Praxis filter pipeline provides the right substrate for closing
these gaps incrementally post-3.6.

### Open questions addressed

All five hub-tracked open questions received research input:

- **Agentic loop x filter pipeline integration**: Praxis makes this
  structural — the loop IS in the pipeline, not beside it. Different
  plugin orderings are filter-chain configuration.
- **Conversation state management**: OpenAI's server-side auto-
  compaction (Feb 2026) is the reference. For self-hosted models,
  Praxis must implement this without model cooperation.
- **Cross-DC rate limiting**: split-budget with reconciliation is the
  pragmatic approach (per architecture lens analysis).
- **Cost multiplication (model selection x ITS fan-out)**: pre-flight
  budget checks before fan-out, with per-candidate metering in the
  budget tree (per requirements lens).
- **Tenancy x MCP Registry governance**: the filter pipeline treats
  tenant identity as a first-class signal that flows through to MCP
  tool authorization; implementation details need the ABAC spike
  (RHAISTRAT-2409) to land first.

### Jira-gap highlights (Direction B)

Two blind spots need immediate attention:

1. **Automatic multi-provider failover** — named in the Architecture &
   Direction doc as Praxis-enabled, listed as "not available" in
   customer requirements, shipped by competitors. No Jira issue.
2. **Cost attribution and chargeback** — table-stakes per every
   enterprise AI governance framework. Metering architecture exists but
   no Jira work on reporting/attribution/chargeback.

Two time-sensitive emerging opportunities:

1. **Streaming guardrails in agentic loops** — first-mover advantage;
   existing guardrails Jira work covers pre/post but not in-stream.
2. **Agent identity and governance** — NIST, CSA, Gartner all published
   frameworks in 2026. No Jira scopes agent identity as distinct from
   human identity.

Two items need upstream strategy work (no Jira): CNCF sandbox
preparation (GPLv3 risk) and Istio data-plane integration (agentgateway
race).

## Lenses not run

- **landscape** — retry with `hub.research ai-gateway landscape`

## Recommended follow-ups

1. **`hub.strategy ai-gateway`** — synthesize this research + knowledge
   + Jira scope into the living strategy document
2. **Competitive deep-dive on agentgateway** — the Istio integration
   race is the most time-sensitive competitive risk; a focused analysis
   of agentgateway's Istio integration path would inform Praxis's
   upstream contribution timeline
3. **RFE creation** for the two blind spots (automatic failover, cost
   attribution/chargeback) and two emerging opportunities (streaming
   guardrails in loops, agent identity)
