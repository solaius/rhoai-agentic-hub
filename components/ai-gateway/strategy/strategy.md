---
title: AI Gateway — strategy
description: Living strategy for AI Gateway / Praxis — the bet on a single AI data plane that owns the agentic loop under unified policy, replacing Envoy's AI layer with a composable Rust filter pipeline.
timestamp: 2026-07-31
status: current
review_after: 2026-09-30
source: hub.strategy from knowledge (32 entries), research (5 lenses), Jira scope (38 issues), roadmap/strategy profiles — 2026-07-31
---

## The brief

AI Gateway is Red Hat's AI-native data plane for all AI traffic:
inference, agentic orchestration, tool calling, A2A, and provider
egress. The bet: converge on Praxis (Rust, filter pipeline,
single-authority) to replace Envoy's AI application layer — one router,
one policy plane, one configuration authority. 3.6 target: Praxis
replaces IPP via ext_proc and provides Responses API with server-side
agentic loop at GA quality. Envoy remains the front door for 3.6;
full replacement in subsequent releases. The differentiation no
competitor has: the agentic loop runs inside the policy pipeline, so
every iteration, tool call, and fan-out candidate traverses auth,
quotas, metering, audit, and guardrails. AI Gateway team kicked off
July 6, 2026 — first networking org team with direct AI BU
responsibility. CNCF sandbox submission planned for Praxis.

## What

### Release train

| Release | Scope | Status |
|---|---|---|
| 3.5 (Aug 2026) | Current stack ships as-is. Praxis productization begins (downstream repo, Konflux, FIPS start). | Shipping |
| 3.6 EA1 | Anthropic Messages API guardrails endpoint (RHAISTRAT-2241). OGX-to-Praxis migration starts (RHAISTRAT-2277). | In Progress |
| 3.6 EA2 | Messages API on llm-d (RHAISTRAT-2018). | In Progress |
| 3.6 GA (target) | Praxis replaces IPP behind same API contracts. Responses API + agentic loop. Messages API. Multi-provider API translation (OpenAI, Anthropic, Bedrock, Vertex AI). Guardrails (NeMo). Credential management. ITS as gateway component (RHAISTRAT-178). IPP componentized under AI Gateway Operator (RHAISTRAT-2452). TP as fallback if GA gates fail. | Engineering goal |
| Post-3.6 | Envoy front-door replacement (Istio deploys Praxis as gateway data-plane image). MaaS enforcement migration. OGX decommission. Multi-cluster routing. A2A protocol. Semantic routing/caching. | Planning |

### Boundaries

| This feature IS | This feature is NOT |
|---|---|
| The AI data plane (inference routing, agentic loop, API translation, guardrails, credentials, metering) | MCP protocol traffic governance (→ [mcp-gateway](/components/mcp-gateway/knowledge/fact-mcp-gateway.md), converging via same migration track post-3.6) |
| The Praxis runtime and AI filters | The placement layer (→ llm-d EPP, separate project) |
| Policy composition and enforcement for AI traffic | MaaS API definition and subscription management (→ MaaS teams, Praxis consumes their config) |
| Agent governance at the network plane (identity, auth, audit in transit) | Agent sandboxing and execution isolation (→ [agent-interop](/components/agent-interop/knowledge/fact-agent-interop-overview.md) / OpenShell) |

## Why

**The problem**: today multiple components inspect the same AI request
with partial context and independent configuration. Envoy provides no
substrate where business logic composes — each capability became a
component beside the proxy, and they cannot share request context,
identity, ordering, or configuration. The committed roadmap (Responses
with server-side orchestration under policy, fallback routing, native
Messages, whole-session enforcement, agent governance) is structurally
inexpressible on the current stack
([decision-praxis-convergence](/components/ai-gateway/knowledge/decision-praxis-convergence.md)).

**The bet**: composition as the invariant, not the achievement. One
ordered filter pipeline over one request context, fed by one
configuration authority. Every current and future capability is a
filter. This is architecturally novel — no competitor offers a server-
side agentic loop inside a composable policy pipeline
([02-competitive](/components/ai-gateway/research/02-competitive.md),
Section 5).

**Why now**: enterprise customers converge on needing unified
multi-provider endpoints, automatic failover, session budgets, agent
governance, and audit trails. The EU AI Act's high-risk rules take
full effect August 2026. Competitors (LiteLLM, agentgateway, Kong)
are shipping production AI gateways now — every quarter of delay
increases the risk that one adds enough K8s-native features to close
the gap ([02-competitive](/components/ai-gateway/research/02-competitive.md),
Section 9).

## Where we stand

### Decisions to date

| Date | Decision | Source |
|---|---|---|
| 2026-04 | Six binding F2F architecture decisions (restricted) | restricted/decision-ai-gateway-f2f-architecture.md |
| 2026-07-06 | AI Gateway team formed — first networking→AI BU team | [fact-ai-gateway-team](/components/ai-gateway/knowledge/fact-ai-gateway-team.md) |
| 2026-07-30 | Praxis convergence: one router, one policy, one config | [decision-praxis-convergence](/components/ai-gateway/knowledge/decision-praxis-convergence.md) |

### Delivery state

- **Praxis upstream**: active development, Pingora-based, multiple
  builds (reverse-proxy, AI inference, agentic gateway). Gateway API
  conformance suite runs in CI. AI filters split to praxis-proxy/ai.
- **Downstream**: opendatahub-io/praxis-extproc created. Konflux
  onboarding in progress (AIPCC support). FIPS compliance in planning.
- **In-flight 3.6 work**: 15 RHAISTRAT Features (New/In Progress),
  3 Outcomes (In Progress), plus 20 RHAIRFE tracking RFEs.
- **Team**: ~15 engineers (AI Gateway core) + collaborating workstreams
  (MaaS, AAET Agentic API, RHCL/Kuadrant, llm-d, Platform AI Safety).

## Gaps & risks

### Open questions

| Question | Why it matters | Status |
|---|---|---|
| [Agentic loop x filter pipeline ordering](/components/ai-gateway/knowledge/question-ai-gateway-agentic-loop-ipp.md) | Different orderings needed for outer gateway vs inner loop | Research says Praxis makes this structural; needs validation |
| [Conversation state management](/components/ai-gateway/knowledge/question-ai-gateway-conversation-state.md) | Auto-compaction for server-side Responses | No model cooperation for self-hosted; Praxis must implement |
| [Cross-DC rate limiting](/components/ai-gateway/knowledge/question-ai-gateway-cross-dc-rate-limiting.md) | Single user's budget across multiple DCs | Split-budget with reconciliation is pragmatic approach |
| [Cost multiplication (selection x fan-out)](/components/ai-gateway/knowledge/question-ai-gateway-model-selection-cost.md) | Failover + ITS fan-out compounds costs silently | Pre-flight budget checks needed; no Jira tracks this |
| [Tenancy x MCP Registry governance](/components/ai-gateway/knowledge/question-ai-gateway-tenancy-mcp-registry.md) | Group-based tenancy must compose with Registry governance | Needs ABAC spike (RHAISTRAT-2409) to land first |

### Research-identified risks

| Risk | Severity | Detail |
|---|---|---|
| CNCF sandbox GPLv3 friction | High | Most CNCF projects use Apache-2.0; license may block acceptance ([04-upstream](/components/ai-gateway/research/04-upstream.md)) |
| Istio integration race | High | agentgateway has experimental Istio 1.30 integration; Microsoft paving the path. Praxis has no upstream Istio contribution tracked ([05-jira-gap](/components/ai-gateway/research/05-jira-gap.md)) |
| FIPS 140-3 for Rust | High | No pure-Rust crypto has FIPS validation. FIPS 140-2 sunsets Sep 2026. Delivery risk for 3.6 ([03-requirements](/components/ai-gateway/research/03-requirements.md)) |
| 3.6 scope convergence | Medium | Praxis + Responses at GA quality, Konflux pipeline, IPP parity, conversation state continuity — all converge on one release |
| Provider coverage gap | Medium | 4 providers vs LiteLLM's 140+. Community contribution model needed post-3.6 ([02-competitive](/components/ai-gateway/research/02-competitive.md)) |

### Execution risks (from prior F2F)

- Conversation state continuity across 3.5→3.6 engine swap — explicit open item, no owner ([fact-ai-gateway-execution-risks](/components/ai-gateway/knowledge/fact-ai-gateway-execution-risks.md))
- SGLang/vLLM divergence risk — community may adopt competing router

## Jira map

### Coverage

| Strategy element | Jira keys | Status |
|---|---|---|
| Praxis convergence / IPP replacement | RHAISTRAT-2452, -2277 | New |
| Responses API + agentic loop | RHAISTRAT-1073 (Outcome), -1456, -1810 | In Progress / New |
| Messages API | RHAISTRAT-2018, -2241 | In Progress |
| API conformance/fidelity | RHAISTRAT-1812, -1810 | New |
| Guardrails GA | RHAISTRAT-1210, -1777 (Outcomes), -2378, -2240, -2241 | In Progress / New |
| ITS integration | RHAISTRAT-178, -2442, -2443, -2444 | In Progress / New |
| Tenant isolation / ABAC | RHAISTRAT-2409 | New (spike) |
| Gen AI Studio decoupling | RHAISTRAT-1935 | New |
| Observability | RHAIRFE-2856, -2858, -2799 | New |

### Candidate jiras

Gaps identified by the [jira-gap analysis](/components/ai-gateway/research/05-jira-gap.md) with no current Jira work:

| Gap | Problem statement | Suggested project |
|---|---|---|
| Automatic multi-provider failover | Enterprises list automatic failover as unavailable today; competitors ship it. Praxis enables re-entrant fallback with rewritten requests but no work is scoped. | RHAIRFE |
| Cost attribution and chargeback | Every enterprise AI governance framework lists cost controls as table-stakes. Token metering exists but reporting, attribution by org/team/key, and chargeback integration are unscoped. | RHAIRFE |
| Streaming guardrails in agentic loops | No competitor applies guardrails to SSE tokens mid-stream during agentic loop iterations. First-mover advantage; the pipeline structurally supports it but no work scopes it. | RHAIRFE |
| Agent identity distinct from human identity | NIST, CSA, and Gartner published AI agent governance frameworks in 2026. Agent identity in Praxis is architecturally possible but unscoped beyond the OGX boundary ABAC spike. | RHAIRFE |
| CNCF sandbox preparation | GPLv3 license risk is high-severity. No Jira tracks governance model, contributor coalition, or license evaluation. | RHAISTRAT |
| Upstream Istio integration contribution | agentgateway is experimentally integrated in Istio 1.30. No Jira tracks Praxis's upstream Istio contribution track, which is a prerequisite for the "Istio deploys Praxis" trajectory. | RHAISTRAT |

## Watchlist

| Trigger | If it fires → what changes |
|---|---|
| agentgateway graduates from experimental to GA in Istio (next: 1.31, expected Q4 2026) | The "Istio deploys Praxis" trajectory needs acceleration or a different integration path. Upstream contribution becomes urgent. |
| CNCF TOC rejects GPLv3 for sandbox | License change to Apache-2.0 or dual-license required before resubmission. Contributor agreements may need rework. |
| FIPS 140-2 sunset (Sep 21, 2026) | Any FIPS-dependent customer blocks on 3.6 until 140-3 validation completes. Praxis must ship with validated crypto by GA or offer a non-FIPS path. |
| EU AI Act high-risk enforcement (Aug 2026) | Structured audit trail format becomes urgent for European enterprise customers. Observability RFEs (2856, 2858) gain priority. |
| LiteLLM Rust rewrite reaches production (tracking: litellm.ai blog) | LiteLLM gains the performance characteristics that currently differentiate Praxis. Provider coverage gap becomes the primary competitive axis. |
| MCP 2026-07-28 deprecation window (12 months from Jul 2026) | Praxis MCP filter updates needed by mid-2027. Plan during post-3.6. |
| Multi-cluster inference workstream (3.6 TP evaluation) | If confirmed, Praxis cross-cluster routing becomes a 3.6 scope addition. |

## History

- 2026-07-31 — **Creation** — first strategy doc from intake (2 GDocs, 2 Slack channels), Jira sweep (38 issues, 18 refs), and 5-lens research (architecture, competitive, requirements, upstream, jira-gap). (source: hub.strategy, 2026-07-31)
