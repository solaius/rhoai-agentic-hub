---
title: "Requirements landscape: enterprise agentic AI (2026)"
description: "What enterprises demand for agentic AI in production — mapped against analyst frameworks, regulatory mandates, cost economics, and Red Hat AI's JTBD hypothesis."
lens: requirements
timestamp: 2026-07-10
review_after: 2026-10-10
tags: [narrative, requirements, agentic, enterprise]
---

# Requirements landscape: enterprise agentic AI (2026)

## Executive summary

Enterprise agentic AI in mid-2026 sits at the inflection point between
hype and operational reality. Gartner forecasts 40% of enterprise
applications will embed task-specific AI agents by end of 2026 [1]. IDC
projects global enterprise AI agent spend will reach $1.4 trillion by
2027 [2]. Yet the dominant statistic is failure: 88% of agent pilots
never reach production [3], and Gartner predicts over 40% of agentic AI
projects will be canceled by end of 2027 due to escalating costs, unclear
business value, or inadequate risk controls [4].

The blockers are overwhelmingly non-technical. Across Gartner, Forrester,
McKinsey, and Deloitte, the same three gaps recur: governance (only 21%
of enterprises have a mature governance model for autonomous agents [5]),
data readiness (only 15% believe their data and systems are fully
prepared [3]), and cost control (22% of agent deployments report negative
ROI at 12 months [3]). The technology works. The organizational muscle to
deploy, govern, observe, and budget for it does not.

The economic context makes urgency unavoidable. Per-token costs dropped
over 90% since 2023, but agentic workloads consume ~1,000x more tokens
than standard chat interactions [6]. Goldman Sachs forecasts global token
usage will multiply 24x between 2026 and 2030 [7]. Apollo's chief
economist calls this "Jevons paradox in action" — as the unit cost of
intelligence collapses, aggregate enterprise spend rises [8]. The average
enterprise AI budget grew from $1.2M/year in 2024 to $7M in 2026 [9].

For Red Hat AI, this landscape validates the broad direction of the 7-JTBD
hypothesis but reveals gaps in three areas: agent fleet management (the
"AgentOps" layer beyond individual operationalization), data readiness and
context architecture (the knowledge layer agents depend on), and cost
management infrastructure (budget controls, model routing, token
governance). The August 2, 2026 EU AI Act enforcement deadline adds
regulatory urgency to every gap.

## Enterprise demand signals

### The pilot-to-production gap

Enterprise appetite is unambiguous but production maturity lags:
- **Gartner (2026):** 17% have deployed agents, 42% plan to within one
  year [1].
- **McKinsey:** 62% experimenting, 23% scaling [10].
- **Deloitte:** 72% using generative AI with agentic capabilities, but
  only 14% deployment-ready, 11% in active production [5].
- **Forrester:** "Three-quarters claim adoption, but few have agents in
  meaningful production beyond 'agentish' chatbots" [12].

### Top 5 production blockers

1. **Governance and risk controls (57-82%):** Only 12% have mature AI
   governance processes [13]. Less than 6% have advanced AI security
   strategies [1].
2. **Evaluation and observability (64%):** 70% name "non-deterministic
   outputs" as the #1 production-readiness barrier [3].
3. **Data readiness and integration (52%):** Integration complexity —
   APIs, legacy systems, data access — is the primary reason for failed
   agent initiatives [3].
4. **Cost management and unclear ROI:** 22% report negative ROI at 12
   months. Forrester attributes 41% of failures to unclear success
   criteria [3].
5. **People and process redesign:** Agent deployments built against
   documented process rather than live operational reality fail at
   go-live [3].

### Shadow agents and ungoverned sprawl

A critical emerging signal: only 47.1% of deployed agents are actively
monitored or secured [16]. 68% of organizations cannot distinguish human
from agent activity in logs [16]. HFS Research: 82% of enterprises have
agents their security teams did not know existed [13].

## Analyst frameworks

### Gartner: five-stage agentic evolution

1. End of 2025: almost every enterprise app embeds AI assistants
2. 2026: 40% integrate task-specific agents
3. 2027: one-third use collaborative multi-agent systems
4. 2028: multi-agent ecosystems dynamically collaborate across apps
5. 2029: 50%+ of knowledge workers create/govern/deploy agents on demand

Gartner warns of "agentwashing" — only ~130 vendors offer legitimate
agentic AI technology [1]. Multi-agent inquiries surged 1,445% from Q1
2024 to Q2 2025. Published inaugural Market Guide for Guardian Agents
(Feb 2026) defining Reviewers, Monitors, and Protectors [17]. By 2028,
40% of CIOs will demand Guardian Agents to contain other agents.

### Forrester: the trust tax

Forrester identifies the "trust tax" — every autonomous action must be
logged and defensible to an auditor, and the current compliance cost is
too high [12]. Predicts vendor fragmentation will force enterprises to
compose "agentlakes" — composable architectures managing fractured
deployments across hyperscalers [12]. 30% of enterprise app vendors will
launch MCP servers in 2026 [12].

### McKinsey: trust maturity and the agentic mesh

2026 AI Trust Maturity Survey (~500 orgs) added agentic AI governance as
a new fifth dimension [14]. Average Responsible AI maturity score: 2.3
(from 2.0 in 2025), but only one-third reach level 3+ in any dimension.
Two critical failure modes: **agent sprawl** (ungoverned proliferation)
and **cascading failures** (flaws propagating in multi-agent systems).
Less than 10% of agentic programs reach meaningful scale [14].

### Deloitte: the silicon workforce

3,235 leaders across 24 countries. Frames agents as "silicon-based
workforce complementing the human workforce" [5]. Three infrastructure
obstacles: legacy integration, data architecture constraints, and data
discoverability (48% cite searchability, 47% reusability as challenges).
42% still developing strategy roadmaps; 35% have no formal strategy [5].

## Security, governance, and compliance

### EU AI Act (enforceable August 2, 2026)

High-risk provisions become enforceable August 2, 2026 [18]. For agentic
AI: risk management, data governance (Article 10), logging/auditability
(Article 12), human oversight (Article 14), cybersecurity resilience
(Article 15). Penalties: up to €35M or 7% of global annual revenue.

Recitals 99-100 address multi-agent architectures: the compliance
boundary extends to every agent performing a high-risk function [18].
Open-source models publishing technical documentation qualify for certain
exemptions — directly benefits Red Hat's approach.

### Agent identity: SPIFFE as the standard

On March 2, 2026, engineers from AWS, Zscaler, Ping Identity, and Defakto
Security published AIMS (Agent Identity Management System) — the first
blueprint mapping SPIFFE for workload identity, WIMSE for workload-to-
workload auth, and OAuth 2.0 for authorization onto a 9-layer stack
purpose-built for AI agents [16].

NIST published its NCCoE concept paper recommending SPIFFE and OAuth as
the baseline (Feb 2026). Google Cloud launched Agent Identity at Cloud
Next built on SPIFFE. Red Hat's Kagenti wires SPIFFE, AuthBridge via
RFC 8693, and agent lifecycle management together [16].

### Governance architecture requirements

The emerging enterprise consensus requires: explainable outputs, full
audit trails, transparent decision logic, and human-in-the-loop approval
gates at defined risk thresholds [3]. Ten minimum control areas: agent
discovery/inventory, identity/access, action boundaries, data access,
behavioral monitoring, human-in-the-loop, multi-agent pipeline governance,
vendor assessment, compliance documentation, continuous improvement [13].

Gartner: "Through 2028, at least 80% of unauthorized agent transactions
will be caused by internal policy violations rather than malicious
attacks" [17].

## Observability, evaluation, and trust

### The observability imperative

The most dangerous failure pattern is "silent success" — the agent follows
flawed reasoning while metrics stay green. Traditional APM cannot detect
this [15]. The most dangerous blind spot: agents encountering errors
often produce plausible-sounding outputs rather than explicit error
messages [15].

### Four production evaluation signals

1. **Hallucination rate:** per-trace LLM-as-judge scoring
2. **Faithfulness scoring:** verifying responses stay grounded in context
3. **Task success rate:** binary/graded goal completion + prompt injection
   detection
4. **User feedback signals:** direct behavioral indicators

### OpenTelemetry as the standard

OpenTelemetry has emerged as the vendor-neutral standard. Leading
platforms (Arthur AI, Arize Phoenix, MLflow, Langfuse, Opik) have adopted
OTel-first pipelines [15]. The emerging approach: runtime deterministic
governance — policy kernels intercepting every action before execution.

### Evaluation-first architectures

Teams succeeding in 2026 treat observability as a foundational design
requirement, building traces, evaluations, and governance guardrails into
agent architecture from day one [15]. Tracing has commoditized — the
platforms that matter score what they capture, surface failing runs, and
turn production traces into the next test cycle.

## Economics and cost management

### The agentic inference cost paradox — confirmed

The Jevons Paradox in AI is now empirically validated:
- Token usage grew 1,001% from Jan 2025 to Apr 2026 [8]
- A single agentic interaction costs ~$1.20, up from $0.04 for linear
  workflows in 2023 — 30x increase [8]
- AT&T's internal AI system: 27B tokens/day, up from 1B 18 months ago [8]
- Uber burned through its entire 2026 AI budget by April [8]
- Ramp data: 680x spending gap — top 1% spend $7,450/employee/month vs
  median $11.38 [9]
- Accenture (2026): 95% of enterprise AI usage runs on premium frontier
  models for tasks that do not require them [8]

### Cost management as a first-class requirement

Inference costs replaced model training costs as the primary driver of
enterprise AI budgets in 2026 [8]. The Linux Foundation launched the
Tokenomics Foundation in June 2026 (Oracle, Google, Microsoft,
JPMorganChase) [8]. Gartner: organizations implementing cost
optimizations reduce agentic AI operational costs by 40-55% within 12
months. Hybrid reasoning/fast-model routing achieves 35-40% cost
reduction while maintaining 98%+ accuracy [11].

Enterprise requirement: budget controls, model routing, per-agent cost
tracking, and token governance policies are production prerequisites.

## Persona-specific requirements

### AI engineer (builder)
- Time-to-first-agent under minutes (GenAI Studio, starter kits) [20]
- Framework flexibility (LangGraph, CrewAI, Strands, Anthropic SDK)
- MCP tool integration as baseline skill — 41% of orgs already in
  production with MCP servers [21]
- Evaluation infrastructure: "the hardest skill to fake" [20]
- Salary context: $185K-$320K, 20-40% premium over general AI eng [20]

### Platform engineer (operator)
- Multi-agent orchestration replacing single-model serving as core
  concern [20]
- SPIFFE-based identity, least-privilege tool access, sandbox isolation
- OTel-based tracing, evaluation pipelines, cost tracking
- Model routing and budget caps
- EU AI Act compliance infrastructure

### AgentOps admin (governor)
- Centralized agent registry with discovery of shadow agents [22]
- Cross-platform policy enforcement
- Guardian agent capabilities (Reviewers, Monitors, Protectors) [17]
- Emergency revocation within seconds [13]
- Fleet-level visibility with owner, purpose, risk posture per agent

### Data scientist (evaluator)
- Evaluation methodology for silent failures and faithfulness degradation
- Model selection/fine-tuning matching task complexity to capability
- RAG and knowledge architecture — 60% of failures trace to data
  freshness, not retrieval quality [23]

## JTBD gap analysis

### Assessment of current 7 JTBDs

| JTBD | Alignment | Assessment |
|---|---|---|
| Build your first agent | Strong | Matches universal onboarding demand |
| Make agents safe | Critical | Top blocker — guardrails GA, sandbox coming |
| Discover agentic assets | Growing | MCP governance is the real need, not just discovery |
| Make inference work | Existential | Jevons Paradox makes cost a survival issue |
| Evaluate and observe | Top-3 blocker | Foundational pieces exist, evaluation-first not yet productized |
| Operationalize agents | Death valley | Where 86-89% of pilots die — heaviest investment area |
| Govern tool/model access | Non-negotiable | Post-EU AI Act, Guardian Agent paradigm missing |

### Missing JTBDs

**Gap A: "Manage my agent fleet at scale"**
Current JTBDs cover individual agents. But enterprise requirements extend
to fleet management: centralized registry with shadow agent discovery,
lifecycle management (creation → deployment → retirement), cross-agent
governance, emergency revocation. All hyperscalers launched fleet
management in 2026. Gartner created Guardian Agents for this [17][22].

**Gap B: "Control my agentic AI costs"**
JTBD #4 focuses on inference performance/availability. But the dominant
2026 conversation is cost, not capability. Token economics, budget
controls, model routing for cost optimization, per-agent cost attribution,
and spending governance are requirements that no current JTBD addresses.
The Tokenomics Foundation launched for this gap [8].

**Gap C: "Make my data agent-ready"**
Every analyst cites data readiness as a top-3 blocker. 52% cite data
quality. 60% of RAG failures trace to freshness, not retrieval quality.
48% cite searchability, 47% reusability [5][23]. The knowledge/context
layer is a prerequisite that maps to no current JTBD.

### Observations on existing JTBDs

- **"Build your first agent" is under-scoped:** needs a "build my next
  100 agents" story — CI/CD for agents, testing pipelines, staging.
- **"Make inference work" is the strongest differentiator:** no other
  vendor makes the self-hosted cost argument. Elevate in positioning.
- **"Govern tool/model access" could absorb regulatory compliance:**
  EU AI Act, SOC2, HIPAA should be explicitly called out.

## Enterprise use case patterns

### Tier 1: proven production (measurable ROI)
- **IT automation:** Getronics automated 1M+ tickets/year [24]. Gartner:
  70% will deploy agentic AI for IT infrastructure ops by 2029.
- **Customer service:** fastest ROI, measured by handle time and ticket
  deflection.
- **Code generation:** highest-adoption function for GenAI in 2026.
  IDE co-pilots now standard tooling.

### Tier 2: scaling from pilot
- **Financial services:** compliance checking, fraud detection. Heavily
  constrained by EU AI Act and DORA [18].
- **Supply chain/procurement:** demand forecasting, vendor assessment.
  Requires deep legacy integration.

### Tier 3: emerging
- **Multi-agent composition:** 2026 as the breakthrough year per
  Gartner/Forrester. A2A protocol at 150+ orgs [11].
- **B2B agent-to-agent commerce:** Gartner predicts 90% of B2B buying
  agent-intermediated by 2028 [1].

### Cross-cutting: MCP + A2A stack

MCP: 97M monthly SDK downloads, 9,400+ public servers, native support
from Anthropic, OpenAI, Google, Microsoft [21]. 41% of orgs in production.
A2A handles agent-to-agent coordination [11]. Enterprise architectures in
2026 plan both: MCP for vertical (agent-to-tool), A2A for horizontal
(agent-to-agent).

## Sources

[1] Gartner, "Predicts 40% of Enterprise Apps Will Feature Task-Specific AI Agents by 2026." https://www.gartner.com/en/newsroom/press-releases/2025-08-26-gartner-predicts-40-percent-of-enterprise-apps-will-feature-task-specific-ai-agents-by-2026-up-from-less-than-5-percent-in-2025
[2] IDC, "FutureScape 2026: Rise of Agentic AI." https://my.idc.com/getdoc.jsp?containerId=prUS53883425
[3] SynaptyX, "Agentic AI in 2026: What Scales and What Stalls." https://www.synaptyx.ai/perspectives/agentic-ai-in-2026-what-scales-and-what-stalls-in-pilot/
[4] Gartner, "Predicts Over 40% of Agentic AI Projects Will Be Canceled by End of 2027." https://www.gartner.com/en/newsroom/press-releases/2025-06-25-gartner-predicts-over-40-percent-of-agentic-ai-projects-will-be-canceled-by-end-of-2027
[5] Deloitte, "The State of AI in the Enterprise, 2026." https://www.deloitte.com/us/en/what-we-do/capabilities/applied-artificial-intelligence/content/state-of-ai-in-the-enterprise.html
[6] Microsoft Research, agentic workload token consumption. https://medium.com/@elisowski/token-prices-are-falling-so-why-is-your-ai-bill-going-up-b9bc1a894b1c
[7] Goldman Sachs Research, global token usage forecast. https://greyjournal.net/hustle/work-tech/how-much-companies-spend-ai-tokens-2026/
[8] Fortune, "Tokens are getting cheaper, but companies spending more." https://fortune.com/2026/06/17/why-is-ai-spending-increasing-as-tokens-get-cheaper-jevons-paradox/
[9] Ramp, "June 2026 AI Index." https://greyjournal.net/hustle/work-tech/how-much-companies-spend-ai-tokens-2026/
[10] McKinsey, "Agentic AI: Moving beyond pilots." https://www.mckinsey.com/featured-insights/mckinsey-live/webinars/agentic-ai-moving-beyond-pilots-to-enterprise-impact
[11] AetherLink, "Agentic AI Multi-Agent Orchestration: 2026 Enterprise Guide." https://aetherlink.ai/en/blog/agentic-ai-multi-agent-orchestration-2026-enterprise-guide
[12] Forrester, "The State of Agentic AI in 2026." https://www.forrester.com/blogs/the-state-of-agentic-ai-in-2026-companies-are-chasing-few-are-catching/
[13] AI Agent Governance & Security Guide (2026). https://decasoftsolutions.com/ai-agent-governance-security-guide/
[14] McKinsey, "State of AI Trust in 2026: Shifting to the Agentic Era." https://www.mckinsey.com/capabilities/tech-and-ai/our-insights/tech-forward/state-of-ai-trust-in-2026-shifting-to-the-agentic-era
[15] MLflow, "Monitoring Agentic AI in Production: 2026 Guide." https://mlflow.org/articles/monitoring-agentic-ai-in-production-2026-guide/
[16] SPIFFE identity sources: HashiCorp, Red Hat, SANS. https://next.redhat.com/2026/06/10/wiring-zero-trust-identity-for-ai-agents-spiffe-token-exchange-and-kagenti/
[17] Gartner, "Market Guide for Guardian Agents" (Feb 2026). https://www.gartner.com/en/newsroom/press-releases/2025-06-11-gartner-predicts-that-guardian-agents-will-capture-10-15-percent-of-the-agentic-ai-market-by-2030
[18] EU AI Act compliance. https://www.artificialintelligence-news.com/news/agentic-ais-governance-challenges-under-the-eu-ai-act-in-2026/
[19] NVIDIA OpenShell. https://www.redhat.com/en/blog/red-hat-ai-and-openshell-driving-security-enhanced-agent-execution-for-enterprise-ai
[20] AI Career Lab, "Agentic-AI Job Guide." https://theaicareerlab.com/blog/agentic-ai-jobs-guide-2026
[21] MCP adoption statistics. https://www.digitalapplied.com/blog/mcp-adoption-statistics-2026-model-context-protocol
[22] AWS Agent Registry preview. https://aws.amazon.com/blogs/machine-learning/the-future-of-managing-agents-at-scale-aws-agent-registry-now-in-preview/
[23] Atlan, "AI Memory vs RAG vs Knowledge Graph." https://atlan.com/know/ai-memory-vs-rag-vs-knowledge-graph/
[24] Enterprise AI agent use cases. https://www.techment.com/blogs/agentic-ai-use-cases-enterprise-operations/
