---
title: "AI Gateway Jira-Gap Analysis"
description: Cross-reference of 38-issue Jira scope against research findings (both directions) — what active work maps to which industry signals, and which significant developments have no corresponding Jira work.
timestamp: 2026-07-31
lens: jira-gap
review_after: 2026-10-31
---

# AI Gateway Jira-Gap Analysis

This document crosses the ai-gateway Jira scope (38 issues across
RHAISTRAT and RHAIRFE) against findings from the architecture,
competitive, requirements, and upstream research lenses. Two
directions: Direction A maps active work to industry context; Direction
B identifies significant external developments with no corresponding
Jira work.

Jira summaries are not quoted verbatim (this repo is public and Jira
serves nothing anonymously). Each issue is described in the author's
own words, with the key for reference.

## Direction A: Active Jira work vs landscape

### Agentic API surface (RHAISTRAT-1073, -1456, -1810, -1812, -2018)

Five issues cover the consistent agentic API layer: multi-protocol
support (OpenAI Responses, Anthropic Messages), Codex Agent SDK
compatibility, API fidelity for tool-calling clients, and MaaS
conformance validation.

**Industry alignment: ahead.** Praxis's plan to own the server-side
Responses API loop inside the policy pipeline has no competitor
equivalent (see competitive lens, Section 5). LiteLLM proxies
Responses but does not orchestrate. agentgateway proxies MCP/A2A but
does not run the loop. The Codex SDK support (RHAISTRAT-1456) and
conformance validation (RHAISTRAT-1812) align with the market trend
that agentic coding tools (Claude Code, Codex, OpenCode) are becoming
the primary client category for AI gateways.

**Risk:** The conformance validation work (RHAISTRAT-1812) correctly
identifies that MaaS layers may silently modify API traffic. The
Inference Proxy Conformance Guidelines referenced in RHAISTRAT-1810
are the right framework, but no timeline is committed for the
conformance test suite itself.

### OGX-to-Praxis migration (RHAISTRAT-2277, -2409)

Two issues cover the 3.6 migration: making Praxis the single
customer-facing entrypoint and validating tenant isolation across the
Praxis-to-OGX boundary.

**Industry alignment: different approach.** Most competitors don't
face this problem because they started from scratch rather than
migrating from an existing system. The migration spike
(RHAISTRAT-2409) is well-scoped. The architecture lens notes that
Praxis's single-pipeline model eliminates the dual-router problem by
construction — the migration is toward the architecturally correct
state.

**Risk:** RHAISTRAT-2277 notes 61 existing customer deployments, 39 in
regulated industries. Conversation state continuity across the engine
swap is an explicit open line item with no assigned owner in the Jira
scope.

### Guardrails (RHAISTRAT-1210, -1777, -2378, -2240, -2241)

Five issues cover guardrails: the cross-gateway guardrails Outcome,
AI Gateway-specific guardrails Outcome, NeMo GA for Praxis, and
Responses/Messages API endpoints for NeMo Guardrails.

**Industry alignment: ahead on integration, behind on execution.** The
plan to share a single guardrail plugin across both MCP Gateway and AI
Gateway surfaces is architecturally cleaner than any competitor's
approach. However, the competitive lens shows that Portkey, Azure APIM,
and AWS all ship production guardrails today. The GA promotion
(RHAISTRAT-2378) is the critical path item.

**Gap within the work:** Streaming guardrails inside agentic loops (SSE
token-level inspection mid-generation) is identified in the
requirements lens as an unsolved industry problem and a first-mover
opportunity. None of the five guardrails issues explicitly scope
in-stream guardrails for the agentic loop — they cover pre-request and
post-response guardrails.

### ITS integration (RHAISTRAT-178, -2442, -2443, -2444)

Four issues cover inference-time scaling: the ITS Hub gateway
component, IPP-based routing (Envoy path), Praxis-native filter,
and Rust orchestration layer.

**Industry alignment: ahead.** No competitor offers governed
inference-time scaling (Best-of-N, Self-Consistency) as a first-class
pipeline capability with per-candidate policy enforcement. GKE has
prefix-cache routing but not algorithmic fan-out. The three-track
approach (IPP plugin now, Praxis filter next, native Rust long-term)
shows deliberate progression.

### IPP componentization (RHAISTRAT-2452)

Extracting IPP from MaaS into the AI Gateway Operator.

**Industry alignment: neutral (internal architecture).** This is
deployment architecture, not market-facing. However, it unblocks the
"Praxis replaces IPP" trajectory — a necessary precondition.

### Gen AI Studio integration (RHAISTRAT-1935)

Decoupling Gen AI Studio playground from OGX-only backend.

**Industry alignment: different approach.** Cloud providers (GKE,
Bedrock) offer integrated playground experiences. Red Hat's playground
is coupled to OGX. This issue is about removing that coupling, which
the competitive lens identifies as trailing developer experience.

## Direction B: Landscape developments with NO corresponding Jira work

### Gap table

| Area | Signal strength | Category | Notes |
|---|---|---|---|
| **Automatic multi-provider failover** | Strong | Blind spot | FSI customers list this as unavailable today. The Architecture & Direction doc names it as a Praxis-enabled capability. No Jira issue tracks it. LiteLLM and Azure APIM ship it now. |
| **Semantic routing and caching** | Strong | Emerging opportunity | The Architecture & Direction doc mentions a developer preview aim. No Jira issue scopes it. Cloudflare and Portkey ship semantic caching. The k8s AI Gateway WG has no formal proposal yet. |
| **Cost attribution and chargeback** | Strong | Blind spot | The requirements lens shows this is table-stakes for enterprises. The Architecture & Direction doc names "cost overlays and SIEM export" as a roadmap item. No Jira issue tracks cost attribution, chargeback dashboards, or FinOps integration. |
| **Broad provider coverage (>4 providers)** | Strong | Intentional omission (for 3.6) | 3.6 targets 4 providers. The competitive lens shows LiteLLM at 140+. The Architecture & Direction doc's FAQ acknowledges the gap. Community contribution model not yet in Jira. |
| **CNCF sandbox submission preparation** | Medium | Blind spot | CNCF sandbox submission is planned but no Jira tracks the preparation work (governance model, contributor coalition, license evaluation). The upstream lens flags GPLv3 as a high-severity risk for CNCF acceptance. |
| **Istio data-plane integration (upstream contribution)** | Medium | Blind spot | The upstream lens identifies the agentgateway Istio 1.30 integration as a competitive threat. No Jira tracks Praxis's upstream Istio contribution. The "Istio deploys Praxis" trajectory requires this work. |
| **Agent identity and delegated authority** | Medium | Emerging opportunity | NIST published AI Agent Standards Initiative (Feb 2026). The requirements lens shows 92% of enterprise security leaders lack full visibility into AI identities. Agent identity in Praxis is mentioned in the Architecture & Direction doc but has no Jira work beyond the ABAC spike (RHAISTRAT-2409 covers the OGX boundary, not agent identity itself). |
| **Structured audit trail format** | Medium | Blind spot | EU AI Act high-risk rules take full effect Aug 2026. Audit trails spanning agentic sessions are a regulatory compliance advantage (competitive lens). Observability RFEs exist (RHAIRFE-2856, -2858, -2799) but none scope a structured audit format for compliance. |
| **Multi-cluster inference routing** | Medium | Intentional omission (evaluating) | The Architecture & Direction doc notes a workstream evaluating multi-cluster for 3.6 TP. No RHAISTRAT/RHAIRFE in the scope tracks this. RHCL provides multi-cluster today; the Praxis-specific evolution is untracked. |
| **A2A protocol support** | Medium | Emerging opportunity | A2A v1.0 is stable under Linux Foundation governance with 150+ production orgs. agentgateway has native A2A. Praxis's agentic-gateway build has started A2A but no Jira issue tracks it. |
| **Google Interactions API support** | Low | Intentional omission | RHAISTRAT-1073 absorbed RHAISTRAT-1348 (Google Interactions). The Outcome names it as in-scope but no child Feature tracks implementation. Low signal — market demand unclear vs OpenAI/Anthropic. |
| **Wasm/Go filter fallback modes** | Low | Intentional omission (for 3.6) | The AI Gateway Project doc lists Wasm and Go filter support as planned fallback modes. No Jira issue. Low priority for 3.6 given Rust is the primary filter path, but matters for community adoption. |

### Gap analysis summary

**Two blind spots need immediate attention:**

1. **Automatic multi-provider failover** — named in the Architecture &
   Direction doc as a Praxis-enabled capability, listed as "not
   available" in the FSI customer requirements matrix, and shipped by
   competitors today. No Jira issue tracks it. This is the gap most
   likely to surface in a customer evaluation.

2. **Cost attribution and chargeback** — every enterprise AI governance
   framework (Gartner, Forrester, CSA) lists cost controls as
   table-stakes. The metering architecture exists (token counting in the
   pipeline) but the reporting, attribution, and chargeback layer has no
   Jira work.

**Two emerging opportunities are time-sensitive:**

1. **Streaming guardrails in agentic loops** — first-mover advantage is
   real; no competitor has solved this. The existing guardrails Jira work
   covers pre/post-request guardrails but not in-stream inspection during
   the agentic loop.

2. **Agent identity and governance** — NIST, CSA, and Gartner all
   published AI agent governance frameworks in 2026. The enterprise
   demand is crystallizing now. Praxis's architecture supports this
   (the agentic loop under policy is the right substrate) but no Jira
   issue scopes agent identity as distinct from human identity.

**Three items are correctly categorized as intentional omissions** for
3.6 (broad provider coverage, multi-cluster, Wasm/Go filters) — these
should become post-3.6 Jira work.

**Two items need upstream strategy** (CNCF preparation, Istio
integration) — these are not product features but strategic work that
determines whether Praxis succeeds as an open-source project.
