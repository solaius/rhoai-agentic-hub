---
title: "AI Gateway Enterprise Requirements Synthesis"
description: Cross-industry enterprise requirements for AI gateways — FSI compliance, agent governance, multi-provider operations, security, and deployment — mapped to Praxis roadmap status.
timestamp: 2026-07-31
lens: requirements
review_after: 2026-10-31
---

# AI Gateway Enterprise Requirements Synthesis

Enterprise AI gateways have moved from optional middleware to essential
infrastructure. Gartner's October 2025 Market Guide for AI Gateways projects
that by 2028, 70% of software engineering teams building multimodel
applications will use AI gateways, up from 25% in 2025. By 2027, 40% of
enterprises will have two or more AI gateways deployed to control and monitor
heterogeneous multi-agent systems. The total addressable market is estimated at
$50--100M in 2025, growing sharply as multimodel and agentic architectures
become the norm.

This document synthesizes enterprise requirements across six categories,
assigns priority tiers (table-stakes, differentiating, future), and maps each
to its status in the Praxis roadmap.

**Priority definitions:**
- **Table-stakes** -- required for production deployment; blocking without it.
- **Differentiating** -- expected by advanced buyers; creates competitive
  separation.
- **Future** -- emerging requirement; early movers gain positioning advantage.

---

## 1. Financial Services Industry (FSI) Requirements

FSI is the most demanding enterprise segment for AI gateways. 2026 is a major
enforcement year: NYDFS Part 500, PCI-DSS 4.0.1, and DORA are in full
enforcement with no grace periods remaining. The EU AI Act's high-risk system
requirements take effect in August 2026.

| Requirement | Priority | Praxis Status |
|---|---|---|
| SOC 2 Type II audit evidence (continuous, not periodic) | Table-stakes | Organizational -- not a Praxis feature, but Praxis must produce the audit artifacts (structured logs, access records) that SOC 2 evidence demands. Post-3.6. |
| PCI-DSS 4.0.1: unique agent identity, CDE access logging, minimum-necessary access | Table-stakes | Agent identity is a 3.6 target (Tier 1 in the architecture direction). Full CDE-scoped access logging is post-3.6. |
| GDPR / EU AI Act: PII detection, data residency, explainability, human oversight | Table-stakes | PII detection via NeMo/TrustyAI guardrails is a 3.6 target. Data residency depends on deployment topology (self-managed). EU AI Act traceability is post-3.6. |
| Multi-provider failover with automatic circuit-breaking | Table-stakes | Not in current IPP. Praxis architecture enables this (Filter/Scorer/Picker model selection) but automatic failover is post-3.6 -- 3.6 focuses on IPP parity. |
| Cost attribution by org / team / key | Differentiating | Token rate limiting (Kuadrant) is a 3.6 workstream. Per-key cost attribution requires metering integration, targeted post-3.6. |
| Model governance (approval workflows, model card enforcement) | Differentiating | Not planned in current roadmap. Composable filter architecture makes it structurally possible. |
| Complete audit trails (every agent action reconstructable) | Table-stakes | Praxis's single-pipeline architecture means every loop iteration traverses the policy pipeline. Structured audit logging format is post-3.6. |
| Air-gapped / disconnected operation | Table-stakes | Praxis supports on-prem deployment. Full air-gap validation (offline bundles, internal PKI, local registry) is a deployment qualification item, not a code feature. Requires Konflux pipeline maturity. |
| FIPS 140-3 compliance for cryptographic operations | Table-stakes | Identified as a 3.6 delivery risk. Rust binaries require FFI to a validated C library (aws-lc-rs or similar). No pure-Rust crypto library has achieved FIPS 140-3 validation. FIPS 140-2 sunsets September 21, 2026. |

**FSI-specific gap analysis:** The most critical missing capability for FSI
buyers today is automatic multi-provider failover with circuit-breaking.
Intelligent routing (Filter/Scorer/Picker) is architecturally defined in the
Praxis convergence decision but not scheduled for 3.6 GA. FSI customers
converge on needing this as table-stakes because downtime in risk scoring or
fraud detection systems has immediate financial and regulatory consequences.
The CFPB has determined that incorrect information from AI chatbots can
constitute a UDAAP violation, making hallucination control a compliance
requirement rather than a quality preference.

---

## 2. Agent Governance Requirements

Gartner warns that enterprises treating AI agent governance as binary --
"either locked down or fully trusted" -- will fail. Agents operate at different
autonomy levels across different trust boundaries and require proportional
governance. The 2026 CISO AI Risk Report found that among 235 large-enterprise
security leaders, 92% lack full visibility into their AI identities and 86% do
not enforce access policies for them. Non-human identities outnumber human
identities 17:1 in the average enterprise, with AI agents the
fastest-growing segment.

| Requirement | Priority | Praxis Status |
|---|---|---|
| Agent identity distinct from human identity | Table-stakes | Architecture direction defines agent identity as Tier 1 for 3.5/3.6. MaaS group-based tenancy generalizes to agent identities. |
| Per-action authorization on tool calls | Table-stakes | Praxis filter pipeline applies policy per loop iteration and per tool call. Authorization granularity at the individual tool-call level is architecturally enabled. Implementation is 3.6 target. |
| Approval gates at risk thresholds inside running loops | Differentiating | Praxis's agentic loop orchestration (Responses API) structurally supports mid-loop policy checks. Explicit human-approval gates are post-3.6. |
| Complete attributable audit records (who, what, why, with whose authorization) | Table-stakes | Single-pipeline architecture means every action traverses policy. Structured audit format with delegation chain recording is post-3.6. |
| Delegated authority with least-privilege scoping | Differentiating | Requires integration with enterprise IdP (OIDC/OAuth 2.1). MCP spec mandates OAuth 2.1 with PKCE. Gateway-side enforcement of scoped tokens is post-3.6. |
| Proportional governance (autonomy-level-based controls) | Future | Gartner's May 2026 recommendation. No current product in the market implements this well. Praxis's composable filter model is the right substrate. |

**The delegation problem:** OAuth 2.1 handles authentication but does not
answer: Who authorized this agent? What is it allowed to do on behalf of which
human? Can a downstream service verify that chain? When an orchestrator agent
delegates to a sub-agent which calls an API which modifies a database, the
accountability chain spans multiple layers. Traditional security models break
down when agents authenticate on behalf of users who may not know the specific
actions being taken. This is an industry-wide unsolved problem that Praxis's
architecture is well-positioned to address through its single-pipeline policy
enforcement model.

**NIST guidance (February 2026):** NIST's AI Agent Standards Initiative
proposes applying OAuth 2.0, Zero Trust (SP 800-207), and Digital Identity
Guidelines (SP 800-63-4) to agent scenarios -- providing an architectural
blueprint for organizations making identity infrastructure decisions before
standards finalize. The MCP spec's OAuth 2.1 mandate aligns with this
direction.

---

## 3. Multi-Provider and Protocol Requirements

Production AI applications route requests across OpenAI, Anthropic, AWS
Bedrock, Google Vertex AI, and self-hosted models to balance cost, latency,
and capability. Without a unified control layer, teams maintain multiple SDKs,
authentication schemes, and failure paths. The Forbes analysis (July 2026)
identifies this as the fundamental driver of agent gateway adoption: "dozens of
agents hitting production systems directly, and no single place to see the
traffic or stop it."

| Requirement | Priority | Praxis Status |
|---|---|---|
| Unified endpoint across OpenAI, Anthropic, Bedrock, Vertex AI, self-hosted | Table-stakes | 3.6 target: Multi-provider API translation (OpenAI, Anthropic, Bedrock, Vertex AI). |
| Native Responses API support (server-side agentic loop) | Table-stakes | 3.6 committed: Praxis owns the Responses API + server-side agentic loop orchestration. Key owner: Sebastien Han. |
| Native Messages API support (Anthropic) | Table-stakes | 3.6 target: Messages passthrough carried forward to Praxis. Key owner: Francisco Arceo. |
| Chat Completions backward compatibility | Table-stakes | IPP parity conformance gates ensure backward compatibility through 3.6. |
| API translation (format conversion between provider APIs) | Differentiating | 3.6 target: API translation between OpenAI, Anthropic, Bedrock, Vertex AI formats. |
| Model aliasing for unified client experience | Differentiating | MaaSModelRef CRD provides user-facing model abstraction. In current architecture; carries forward to Praxis. |
| Automatic failover across providers | Differentiating | Architecturally enabled (Filter/Scorer/Picker). Not scheduled for 3.6 GA. |
| Semantic caching | Future | Under investigation per hub knowledge. No commitment. |

**API translation vs. passthrough tradeoffs:** Translation (converting between
API formats at the gateway) provides a uniform client experience but risks
losing provider-specific features and introduces a fidelity maintenance burden
as APIs evolve. Passthrough (forwarding native API calls) preserves full
feature access but requires clients to handle multiple API formats. The Praxis
approach for 3.6 supports both: translation for uniform multi-provider access
and passthrough for cases requiring native API fidelity. The conformance
validation workstream (RHAISTRAT-1812) is the mechanism for ensuring
translation fidelity.

**Responses API conversation state:** The Responses API maintains conversation
state server-side via `previous_response_id`, eliminating the need to resend
full conversation history on every turn. OpenAI estimates Chat Completions can
be up to 5x more expensive for long conversations due to history
re-tokenization. For gateway-native implementation, the open question is how
to detect and approximate OpenAI's auto-compaction behavior. The architecture
direction proposes detecting compaction via a `response.compaction` flag and
approximating via summarization -- discussed but not yet designed in detail.

---

## 4. Operational Requirements

Gartner predicts more than 40% of agentic AI projects will be canceled by 2027
over escalating costs, unclear business value, or weak risk controls. Uber
exhausted its entire 2026 AI budget by April. Enterprise AI spend is up 108%
year over year. The operational control plane is what separates sustainable
production deployment from uncontrolled cost escalation.

| Requirement | Priority | Praxis Status |
|---|---|---|
| Whole-session enforcement (token budgets spanning loop iterations, tool calls, fan-out) | Table-stakes | Praxis's single-pipeline architecture is the structural enabler. Every loop iteration traverses the policy pipeline. Token rate limiting (Kuadrant) is a 3.6 workstream. |
| Credential management: per-destination injection | Table-stakes | 3.6 target: Provider credential injection (API key, GCP WI, AWS SigV4, Azure AD). |
| Credential management: BYOK (bring your own key) | Differentiating | Gateway architecture supports virtual keys mapping to provider keys. Not explicitly in 3.6 scope. |
| Credential management: external secret manager integration | Differentiating | Kubernetes-native secret management is baseline. Integration with Vault/external managers is post-3.6. |
| Credential rotation without downtime | Table-stakes | Kubernetes secret rotation is baseline. Praxis hot-reload of credentials is TBD. |
| Cost controls and chargeback (per-team, per-project, per-agent) | Differentiating | Token rate limiting per subscription is current. Per-team/project granularity requires metering evolution. Post-3.6. |
| Observability: structured logging | Table-stakes | Baseline capability. Praxis structured log format is TBD. |
| Observability: distributed tracing (OpenTelemetry) | Table-stakes | Standard practice for Rust services. Not explicitly scoped for 3.6. |
| Observability: metrics (token counts, latency, error rates, cost) | Table-stakes | Kuadrant token metering provides the foundation. Full metrics suite is post-3.6. |

**Open question -- cost multiplication gap:** When the gateway's intelligent
routing selects a more expensive model on failover and inference-time-scaling
fan-out multiplies requests, costs compound in ways nothing currently guards
against. This interaction between model selection, rate limiting, and ITS
fan-out is identified in hub knowledge as an unresolved gap. Praxis's
whole-session enforcement model is the right architectural response, but
the specific budget algebra (how to express "this session's total cost across
all fan-out branches must not exceed X") needs design.

**Open question -- cross-datacenter rate limits:** A user with a 100K
token/hour limit hitting both DC-East and DC-West requires one of: shared
Redis (adds latency), split per-DC budgets (under-utilizes capacity), or
eventual consistency with reconciliation (risks temporary overrun). This
remains open from the April 2026 AI Gateway F2F. The practical answer for
most enterprises is eventual consistency with reconciliation -- accepting
temporary overrun within a tolerance band -- but the tolerance band
definition and reconciliation mechanism need specification.

---

## 5. Security Requirements

Prompt injection is ranked number 1 on the OWASP Top 10 for LLM Applications
in both 2025 and 2026. Documented injection attempts against enterprise AI
rose approximately 340% year over year in late 2025. The UK's National Cyber
Security Centre warned in December 2025 that prompt injection "may be a
problem that is never fully fixed." The working enterprise strategy is
containment: assume some injections will land and ensure a landed injection
cannot do much.

| Requirement | Priority | Praxis Status |
|---|---|---|
| Tenant isolation (data plane separation between orgs) | Table-stakes | MaaS group-based tenancy model. RHAISTRAT-2409 covers tenant isolation for Praxis/OGX. 3.6 scope. |
| ABAC enforcement (attribute-based access control) | Differentiating | MaaSAuthPolicy CRD provides policy-based access. ABAC granularity beyond current RBAC is post-3.6. |
| PII detection at gateway edge | Table-stakes | 3.6 target: NeMo/TrustyAI guardrails integration. Three-layer defense-in-depth (global PII detection, cluster guardrails, inference-layer output filtering). |
| Prompt injection defense | Table-stakes | Guardrails pipeline is the mechanism. NeMo guardrails include prompt injection detection. 3.6 target via RHAISTRAT-1777 / RHAISTRAT-2240 / RHAISTRAT-2241. |
| Credential security (provider keys never exposed to clients) | Table-stakes | Praxis credential injection architecture ensures keys are resolved at the gateway, never sent to clients. 3.6 target. |
| FIPS 140-3 compliance | Table-stakes | 3.6 delivery risk. Rust requires FFI to validated C library. FIPS 140-2 sunsets September 2026. |
| Supply chain security for Rust binaries (SBOM, signing) | Table-stakes | Konflux pipeline onboarding is a 3.6 workstream. SBOM generation and binary signing are Konflux capabilities. |
| Streaming guardrails (latency budget ~100-200ms) | Differentiating | Architecture defines sync checks within a 100-200ms latency budget. Async/parallel guardrails proposed for audio/video. Post-3.6 for full streaming support. |

**Defense-in-depth architecture:** The three-layer guardrails model positions
the gateway as the central enforcement point:

1. **Global gateway (edge):** PII detection before requests leave the
   organization's boundary. Future state.
2. **Cluster gateway (Praxis filters):** PII/prompt-injection checks before
   the model, guardrails output filtering after. 3.6 target.
3. **Inference layer (TrustyAI/NeMo):** Model-specific output filtering and
   safety checks. Existing capability.

The ordering decision -- guardrails run before token-limit checks in the
output flow -- reflects the principle that guardrails may mutate the response
and change its token count.

---

## 6. Deployment Requirements

True air-gapped deployment means running AI systems on infrastructure with no
physical or logical connection to external networks. For defense, critical
infrastructure, and classified environments, this is a regulatory or
operational requirement, not a preference. A Kubernetes deployment referencing
external images will fail at runtime; every image reference must point at a
local registry. Certificate renewal must be wired to internal PKI from day one.

| Requirement | Priority | Praxis Status |
|---|---|---|
| Kubernetes-native (Gateway API, CRDs) | Table-stakes | Core architecture. MaaS controllers manage Praxis deployment. 3.6. |
| Non-Kubernetes support (bare RHEL) | Differentiating | Praxis is a standalone Rust binary. Bare-metal deployment is architecturally feasible but not a 3.6 qualification target. |
| Air-gapped / disconnected operation | Table-stakes | Requires: local container registry (Harbor), offline Helm charts, internal PKI, no external telemetry, signed offline update bundles. Deployment qualification, not code changes. |
| Multi-cluster routing | Future | Requires Praxis federation or external load balancing. Not planned. |
| Upgrade/rollback with conversation state continuity | Table-stakes | Explicitly called out as an open line item for 3.5-to-3.6 engine swap. Critical for customers with active Responses API sessions during upgrade windows. |
| GitOps deployment (ArgoCD, Flux) | Differentiating | CRD-based configuration is GitOps-friendly by design. No special work needed beyond standard Kubernetes patterns. |

**Open question -- tenancy and MCP Registry governance:** The F2F decided that
the existing MaaS group-based tenancy model generalizes to MCP tool catalogs,
but how that tenancy boundary composes with the MCP Registry's own governance
model is still undefined. The practical question: when a tenant's gateway
policy says "this group can access these MCP tools" and the MCP Registry has
its own approval workflow, which authority wins on conflict? This needs a
resolution before the governance story is complete for enterprises running both
AI Gateway and MCP Registry.

---

## Cross-Cutting Open Questions

Four open questions from hub knowledge require resolution to close the
requirements picture. Each represents an interaction between two subsystems
where the individual designs are progressing but the composition is not yet
specified.

1. **Cross-datacenter rate limit enforcement:** Shared Redis vs. split budgets
   vs. eventual consistency. Recommendation: eventual consistency with
   configurable tolerance bands, with the tolerance expressed as a percentage
   of the budget (e.g., "allow up to 10% temporary overrun, reconcile within
   5 minutes").

2. **Model selection x rate limiting x ITS fan-out cost multiplication:** The
   compounding cost scenario where intelligent routing picks an expensive
   fallback model and fan-out multiplies that cost. Recommendation: session-
   level cost ceilings that span all fan-out branches, with circuit-breaking
   when the ceiling is approached.

3. **AI Gateway tenancy x MCP Registry governance:** Which authority wins when
   gateway tenant policy and MCP Registry approval workflows conflict.
   Recommendation: gateway policy is the outer enforcement boundary; MCP
   Registry governs catalog availability, gateway governs runtime access.

4. **Conversation state management (auto-compaction):** How to detect and
   approximate OpenAI's auto-compaction for server-side Responses API state.
   Recommendation: implement compaction as a Praxis filter that can be
   configured per-tenant, with summarization as the default compaction strategy
   and a `response.compaction` event for observability.

---

## Requirements Heat Map

Summarizing readiness across the six categories for Praxis 3.6 GA:

| Category | Table-Stakes Coverage | Key Gaps |
|---|---|---|
| FSI Compliance | Partial -- guardrails and credential injection land; FIPS is a risk; audit format is post-3.6 | Automatic failover, structured audit trail format, continuous compliance evidence generation |
| Agent Governance | Foundation -- agent identity, per-action policy pipeline | Human approval gates, delegation chain recording, proportional governance |
| Multi-Provider | Strong -- Responses, Messages, API translation all 3.6 targets | Automatic failover, semantic caching |
| Operational | Foundation -- token rate limiting, credential injection | Per-team chargeback, cross-DC rate limits, cost multiplication guards |
| Security | Strong -- guardrails, tenant isolation, credential security all 3.6 targets | FIPS 140-3 validation (delivery risk), ABAC beyond current RBAC |
| Deployment | Strong -- Kubernetes-native with CRDs | Conversation state continuity across upgrades, bare RHEL qualification |

The 3.6 release delivers the architectural foundation across all six
categories. The primary gaps are in operational maturity (chargeback,
structured audit trails, automatic failover) rather than in structural
capability. Praxis's single-pipeline, composable-filter architecture is the
right substrate for closing these gaps incrementally in post-3.6 releases.

---

## Sources

- [Gartner Market Guide for AI Gateways (October 2025)](https://www.gartner.com/en/documents/7051698)
- [Gartner: Building the Enterprise AI Control Plane](https://www.truefoundry.com/blog/building-the-enterprise-ai-control-plane-gartner-r-insights-and-truefoundrys-approach)
- [Gartner Predicts 40% of Enterprise Apps Will Feature Task-Specific AI Agents by 2026](https://www.gartner.com/en/newsroom/press-releases/2025-08-26-gartner-predicts-40-percent-of-enterprise-apps-will-feature-task-specific-ai-agents-by-2026-up-from-less-than-5-percent-in-2025)
- [Gartner Says Applying Uniform Governance Across AI Agents Will Lead to Failure](https://www.gartner.com/en/newsroom/press-releases/2026-05-26-gartner-says-applying-uniform-governance-across-ai-agents-will-lead-to-enterprise-ai-agent-failure)
- [Forbes: Agent Gateways Are Becoming The Control Plane For Enterprise AI](https://www.forbes.com/sites/janakirammsv/2026/07/05/agent-gateways-are-becoming-the-control-plane-for-enterprise-ai/)
- [Forrester Predictions 2026: AI Agents and Enterprise Software](https://www.forrester.com/blogs/predictions-2026-ai-agents-changing-business-models-and-workplace-culture-impact-enterprise-software/)
- [CSA Research Note: AI Agent Governance Framework Gap](https://labs.cloudsecurityalliance.org/research/csa-research-note-ai-agent-governance-framework-gap-20260403/)
- [AI Agent Identity Management in 2026: Standards and Gaps](https://articles.idenhq.com/ai-agent-identity-management-2026)
- [AI Agent Audit Trails: The Missing Layer of Enterprise AI Governance](https://www.miniorange.com/blog/ai-agent-audit-trail/)
- [AI Agent Governance and Compliance in 2026](https://zylos.ai/research/2026-05-01-ai-agent-governance-compliance-2026/)
- [NIST: Modernizing FIPS for Safe Languages and Verified Libraries](https://www.nist.gov/document/modernizing-fips-safe-languages-and-verified-libraries)
- [Enabling FIPS-Compliant Cryptography in Rust Applications](https://www.safelogic.com/blog/enabling-fips-compliant-cryptography-in-rust-applications)
- [FIPS Compliance 2026: Requirements and Certifications](https://tuxcare.com/blog/fips-compliance/)
- [OpenAI Responses API: Conversation State](https://developers.openai.com/api/docs/guides/conversation-state)
- [Prompt Injection: The OWASP #1 AI Threat in 2026](https://www.securance.com/blog/prompt-injection-the-owasp-1-ai-threat-in-2026/)
- [AI-SPM for Financial Services: Managing AI Risk Under SOC2, PCI-DSS](https://www.armosec.io/blog/aispm-for-finance/)
- [AI Compliance Requirements for Financial Services Firms](https://www.kiteworks.com/regulatory-compliance/ai-compliance-financial-services-firms/)
- [Top Multi-Provider AI Gateways for OpenAI, Anthropic, Bedrock](https://www.getmaxim.ai/articles/top-multi-provider-ai-gateways-for-openai-anthropic-bedrock/)
- [Definitive Guide to AI Gateways in 2026: Competitive Landscape](https://www.truefoundry.com/blog/a-definitive-guide-to-ai-gateways-in-2026-competitive-landscape-comparison)
- [Air-Gapped AI: Deploying LLMs in Defense and Regulated Finance](https://www.truefoundry.com/blog/air-gapped-ai-deploying-enterprise-llms-in-highly-regulated-industries)
- [The AI Token Economy: Managing Hidden Costs of Agentic AI (CGI)](https://www.cgi.com/en/blog/artificial-intelligence/ai-token-economy-managing-hidden-costs-agentic-ai)
- [AI Agent Cost Per Task 2026: Token Budgets and Math](https://www.kunalganglani.com/blog/ai-agent-cost-per-task-2026)
