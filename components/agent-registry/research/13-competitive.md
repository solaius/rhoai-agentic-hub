---
title: "Agent Registry research — competitive (2026-08)"
description: First dedicated competitive lens for agent registries — Google GA'd July 30, AWS GA imminent (Aug 6 namespace migration), Microsoft cross-cloud sync in preview, Gartner "Guardian Agents" category inaugural, 7 new funded entrants, EU AI Act live Aug 2; wedge holds but window narrows to 6-9 months.
timestamp: 2026-08-03
lens: competitive
review_after: 2026-10-03
---

First dedicated competitive-lens pass for the
[Agent Registry](/components/agent-registry/index.md). Prior competitive
coverage was folded into the landscape lens
([08-landscape](/components/agent-registry/research/08-landscape.md),
2026-07-16); this doc adds vendor-by-vendor deltas, analyst coverage, new
entrants, and an updated wedge assessment. Delta period: 2026-07-16 to
2026-08-03 (2.5 weeks — fast-moving market).

## 1. Vendor deltas since July 16

### 1.1 Google — Agent Registry GA (July 30, 2026)

The most significant competitive event since the last refresh. Google's
Agent Registry went **GA on July 30, 2026** as part of the Gemini
Enterprise Agent Platform. RHOAI now has **two GA cloud competitors**
(Google + Microsoft), not one.

Key developments:
- **Agentic Resource Discovery (ARD) specification announced** — the
  first vendor-backed federated discovery protocol for agent registries,
  standardizing how capabilities are published under domain names and
  indexed across federated registries.
- **Agent Identity (SPIFFE-based) in Public Preview** — agents get
  SPIFFE IDs viewable in the Agent details page. Notably, SPIFFE is
  cloud-neutral by design — a closer competitor to what RHOAI would
  naturally use than Microsoft's Entra Agent ID.
- **Enterprise adoption signals**: Commerzbank AG and WellSky cited as
  early adopters.

Evidence grade: **strong** (GA announcement, official docs).

RHOAI implication: ARD is the most architecturally significant
development. If it becomes a de facto federated discovery standard,
RHOAI's 3.7+ federation roadmap needs to either adopt ARD or demonstrate
A2A Agent Cards + MLflow metadata is a better alternative. The SPIFFE
identity approach makes Google a closer architectural competitor than
Microsoft.

### 1.2 AWS — GA imminent

- **Still Public Preview** as of August 3, but a **namespace migration
  from `bedrock-agentcore` to `agent-registry` is confirmed for August 6,
  2026** — three days from now. AWS typically does not invest in
  standalone namespaces for features that will remain in preview.
- **Bedrock Agents Classic entered maintenance mode July 30** as
  scheduled. No new customers. Model catalog frozen. AgentCore is the
  sole path forward.
- **Production-scale quotas shipped July 2026**: active sessions raised
  to 5,000/account, InvokeAgentRuntime API bumped from 25 to 200 TPS per
  agent. These are not preview numbers.
- **Registry MCP endpoint**: the registry itself is consumable as an MCP
  server from IDEs — validating the registry-as-MCP-server pattern.

Evidence grade: **strong** (primary AWS docs, confirmed dates).

RHOAI implication: GA is likely near-term (namespace migration is a
strong signal), possibly re:Invent 2026 or sooner. Once GA, the
"preview-only" caveat disappears from competitive comparisons. The
per-"Net Records" pricing model (records alive at any moment, deletions
decrement) will be the first per-inventory-record meter in the market.
Registry remains cloud-only (five AWS regions), no air-gapped story.

### 1.3 Microsoft — cross-cloud governance play

- **License enforcement completed July 1, 2026**: $15/user/month
  (standalone) or M365 E7 ($99/user). Free inventory tier confirmed.
- **Cross-cloud registry sync in Public Preview**: Agent 365 can
  discover and inventory agents across AWS Bedrock and Google Cloud
  connections. This is the most direct threat to RHOAI's multi-cloud
  governance positioning.
- **Silent enforcement gap**: existing block rules stopped enforcing on
  July 1 — organizations must re-define under the new policy experience.
  Operational risk for early adopters.
- **Shadow AI detection expanded**: Defender now maps devices, MCP
  servers, identities, and reachable cloud resources per agent. 18 agent
  types detected by June 2026, including Claude Code and GitHub Copilot
  CLI.
- **Windows Agent Runtime (WAR) preview shipping**: MXC sandbox
  isolation, per-agent capability grants, C#/Rust support. Backport to
  24H2 covers 500M+ devices.
- **Entra Agent ID criticism surfaced**: independent analysis notes it
  "doesn't work outside Azure" without wrapping agents in Azure service
  principals — the cross-cloud story is thinner than marketing implies.

Evidence grade: **strong** (Microsoft official docs, licensing analyses).

RHOAI implication: The cross-cloud sync preview is the most significant
threat since July 16. If it matures, Microsoft becomes the governance
overlay for multi-cloud estates. However, the Entra Agent ID criticism
and enforcement gap suggest the cross-cloud story has substance gaps.
The free inventory tier continues to set a floor that
infrastructure-priced alternatives must justify with governance
differentiation.

### 1.4 IBM — on-prem gap persists

- **No on-prem Agentic Control Plane confirmed**. Remains AWS + IBM
  Cloud only (launched June 2026). Classic Orchestrate on OpenShift is
  current-gen.
- **IBM Sovereign Core GA (Think 2026)**: built on Red Hat OpenShift and
  Red Hat AI — infrastructure governance, but NOT agent-registry-specific
  governance. There is an architectural seam between IBM's infrastructure
  governance (Sovereign Core) and agent governance (Orchestrate
  next-gen on cloud).
- **128 AI agents per human worker**: cited by IBM exec as the current
  production ratio.
- **Credential health monitoring** and Agent Access overview added to the
  Agentic Control Plane.

Evidence grade: **moderate** (Think 2026 confirmed, on-prem gap inferred
from absence of announcements).

RHOAI implication: IBM's on-prem gap remains RHOAI's best competitive
validation. Sovereign Core runs on OpenShift but lacks agent governance —
Red Hat can fill the gap IBM left in their own stack. The 128:1
agent-to-human ratio is useful for sizing arguments. IBM will likely
close the gap (their hybrid story depends on it), so this is time-boxed —
Think 2027 (Q2) is a plausible preview target.

### 1.5 Databricks — registration only, no runtime invocation

- **Agent Services in Unity Catalog confirmed**: agents can be
  registered, discovered, and permissioned alongside data objects, but
  **runtime invocation is not available** — registration and permissions
  only.
- **14,000+ organizations on Unity Catalog**: massive governance
  installed base.
- **Unity AI Gateway expanded**: MCP server governance, on-behalf-of user
  execution, end-to-end MLflow tracing. Contextual Service Policies in
  beta.

Evidence grade: **strong** (official Databricks docs).

RHOAI implication: Databricks' "no runtime invocation" matches RHOAI's
phased approach (registry metadata, not deployment). The MLflow tracing
integration is directly relevant. The 14,000-org installed base is a
moat for data-centric companies, but Databricks has no on-prem product.

### 1.6 Salesforce — cross-platform MCP bridge

- **Agent Broker GA June 2026** with deterministic routing.
- **AI Gateway with LLM Governance GA**: centralized token usage, costs,
  data flows.
- **MCP Bridge GA**: makes existing APIs MCP-compatible at scale,
  consumable by Claude, OpenAI, Bedrock agents — not just Agentforce.
- **Agent Scanners expanded**: now support Amazon Bedrock, Microsoft
  Foundry, and GoDaddy.

Evidence grade: **strong** (Salesforce official).

RHOAI implication: MCP Bridge is practically relevant — it turns existing
APIs into MCP servers at scale, competing with MCP catalog approaches.
SaaS-only, Salesforce-ecosystem-centric — not competition for on-prem
registries.

### 1.7 ServiceNow — governance bundled free, Anthropic partnership

- **AI Control Tower expanded at Knowledge 2026**: five dimensions
  (Discover, Observe, Govern, Secure, Measure).
- **MCP servers now a governed asset type**: AI Stewards can require
  approval before activation.
- **Microsoft Agent 365 deeper integration**: cross-publishing between
  ServiceNow and Agent 365 Marketplace.
- **Anthropic is first named design partner**: Claude Cowork connected to
  ServiceNow's governed system of action.
- **NVIDIA partnership (Project Arc)**: desktop agent secured by NVIDIA
  OpenShell runtime, governed by AI Control Tower.
- **Licensing change**: AI Control Tower **bundled into all three
  AI-native tiers**. Every ServiceNow customer gets it — another free
  governance floor.
- **GA expected August 2026**.

Evidence grade: **strong** (ServiceNow official releases).

RHOAI implication: ServiceNow validating MCP-servers-as-governed-asset is
significant. The Anthropic partnership and NVIDIA OpenShell integration
show ServiceNow positioning as the cross-vendor governance layer.
SaaS-only, different segment, but the free bundling adds to the pricing
pressure.

### 1.8 Solo.io / OSS — four-project suite

- **Solo.io now has a four-project agentic suite**: kagent (CNCF
  Sandbox), agentgateway (Linux Foundation), agentregistry (CNCF
  submission), agentevals (new — benchmarking agent behavior).
- **kagent attracted 300+ contributors** from Microsoft, Amazon, Oracle,
  Amdocs, Orange in under a year.
- **Kagenti/Rosso rebranding confirmed**: Kagenti project becoming
  "Rosso" — focuses on governing agents as Kubernetes workloads.
- **agentgateway has air-gapped installation docs**: container images and
  Helm charts mirrorable to private registries. agentregistry does NOT
  have air-gapped docs yet.
- **CNCF Sandbox review**: board review may have already occurred (June
  9 date surfaced); original Sept 22 date from baseline may have been
  different.

Evidence grade: **moderate** (OSS project activity, CNCF application
public).

RHOAI implication: The four-project suite is the most complete OSS
competitor to RHOAI's agent infrastructure stack. The agentgateway
air-gapped docs show Solo.io is already addressing the disconnected use
case — once agentregistry follows, RHOAI's "only on-prem registry" claim
weakens. RHOAI needs to decide: contribute to/integrate with
agentregistry, or compete with it via the MLflow-based approach. The 300+
contributor momentum is significant.

## 2. New entrants

Seven funded entrants since July 2026 — the agent governance space is
attracting serious capital.

| Entrant | Focus | Funding | Note |
|---|---|---|---|
| **Geordie AI** | Agent governance security (RSAC 2026 Innovation Sandbox winner) | $6.5M seed (Ten Eleven + General Catalyst) | Security-first governance |
| **JetStream Security** | Agent governance, security-native | $34M seed (CrowdStrike alumni) | Largest seed in agent governance |
| **Oasis Security** | Non-human identity + agentic access governance | $120M Series B | NHI focus validates the identity requirement |
| **AvePoint AgentPulse** | Multicloud agent governance at scale | Public company (28K customer relationships) | First public company shipping multicloud governance |
| **Kosmoy** | Four registries (AI systems, models, MCP servers, master agent registry) + gateway | Not confirmed | OpenAI-compatible gateway |
| **Credo AI** | Agent Registry with agent cards, shadow AI discovery, EU AI Act policy packs | Established | Governance/compliance focus |
| **Arthur AI** | "Agent Discovery & Governance" (ADG) platform | Established | First to name ADG as a category |

Evidence grade: **strong** (funding announcements, product launches).

RHOAI implication: The capital flowing in ($160M+ across these entrants)
confirms the market is real and growing fast. The NHI/identity focus
(Oasis, JetStream) validates the requirements refresh finding that NHI
lifecycle is a gap in P1-P11. The multicloud governance focus (AvePoint)
is the same positioning RHOAI targets. None of these are on-prem — the
startups are all SaaS/cloud — but they are shaping buyer expectations
and analyst framing.

## 3. Analyst coverage

The agent governance space has gone from unnamed to multi-analyst-covered
in one quarter:

- **Gartner Market Guide for Guardian Agents (Feb 2026, inaugural)**:
  defines guardian agents as "AI governance + AI runtime controls."
  Explicitly calls for **independent guardian agent layers that work
  across clouds and platforms** — the vendor-neutral governance pattern
  RHOAI should claim.
- **Gartner Hype Cycle for Agentic AI (2026)**: 17% of organizations
  have deployed agents, 60%+ expect to within two years — most
  aggressive adoption curve Gartner has recorded.
- **Gartner Hype Cycle for Platform Engineering 2026**: introduces
  "Agent Experience (AX)" — preparing systems to be machine-readable
  and discoverable by agents.
- **Forrester Wave: Bot and Agent Trust Management Software, Q2 2026**:
  evaluates the shift from "block bots" to "enable trusted automated
  traffic."
- **Forrester Wave: Workforce Identity Security Platforms, Q2 2026**:
  renamed to capture identity governance across human, machine, and AI
  agent identities.

Evidence grade: **strong** (Gartner/Forrester primary).

RHOAI implication: The "Guardian Agents" framing — independent governance
layers that work across clouds — is exactly RHOAI's positioning. Gartner
analysts can be briefed on the MLflow-based registry as the open-source
guardian-agent infrastructure layer. The AX concept (Agent Experience)
could frame the registry as the platform engineering surface for agent
governance.

## 4. Regulatory developments

- **EU AI Act high-risk obligations took effect August 2, 2026** —
  cross-platform agent governance is now a compliance requirement, not a
  nice-to-have, for any organization deploying AI in the EU.
- **NIST AI Agent Standards Initiative** (launched Feb 17, 2026): SP
  800-53 control overlays for agent systems in development, AI Agent
  Test Suite planned Q4 2026. Three pillars: industry-led standards,
  open-source agent protocols (including MCP), agent security research
  (especially agent identity).
- **Colorado AI Act enforceable June 2026**: state-level obligations.

Evidence grade: **strong** (regulatory text, NIST official).

RHOAI implication: EU AI Act effective date is the most important
tailwind. Organizations deploying high-risk AI systems must now have
governed registries. NIST SP 800-53 agent overlays (Q4 2026) will create
explicit procurement requirements — RHOAI should participate in the NIST
standards development to shape them.

## 5. Updated wedge assessment

### The wedge: self-managed, disconnected, governed fleet registry with lineage

**Strengthening the wedge:**
1. **No competitor has shipped an on-prem/air-gapped agent registry.**
   IBM's Agentic Control Plane remains cloud-only. All hyperscalers are
   SaaS. All funded startups are SaaS.
2. **EU AI Act live** — regulated industries with sovereign data
   requirements cannot use cloud-only registries.
3. **Gartner explicitly calls for vendor-neutral, cross-cloud guardian
   agent layers** — this IS the RHOAI positioning.
4. **Entra Agent ID "doesn't work outside Azure" criticism** validates
   that platform-specific identity is insufficient for hybrid.
5. **IBM Sovereign Core lacks agent governance** — Red Hat fills the gap
   in IBM's own stack.
6. **Solo.io agentgateway has air-gapped docs but agentregistry does
   not** — first-mover advantage for disconnected registry is still
   available.

**Eroding the wedge:**
1. **Microsoft cross-cloud registry sync in preview** — if this matures,
   it weakens "only RHOAI does multi-cloud governance."
2. **Google Agent Registry GA** with ARD federated discovery — if ARD
   becomes standard, cloud-native federation may be "good enough."
3. **Google's SPIFFE-based identity** is cloud-neutral by design,
   undermining "cloud providers can only do platform-specific identity."
4. **Solo.io's four-project OSS suite** continues building momentum
   (300+ contributors from major vendors). Once agentregistry gets
   air-gapped docs, the disconnected differentiator weakens.
5. **Free governance floors**: Microsoft (free inventory), ServiceNow
   (bundled in all tiers), and startup free tiers make it harder to
   charge separately for registry.
6. **Category formation speed**: Gartner Market Guide, Forrester Wave,
   $160M+ startup funding — the window for "first governed registry
   on-prem" is narrowing.

### Net assessment

**The wedge holds for 2026 but the window is narrower than 30 days ago.**
Estimated window: **6-9 months** (down from 6-12 in July 16 baseline).
The critical milestones:

1. Ship before Solo.io agentregistry achieves CNCF Sandbox + air-gapped
   support.
2. Ship before IBM brings the Agentic Control Plane to OpenShift.
3. Participate in NIST SP 800-53 agent overlays and ARD to shape
   standards before they crystallize.

### Updated market-position fact

The July 16 fact-agent-registry-market-position.md should be updated:
- Google Agent Registry GA (July 30) — two GA cloud competitors now
- AWS GA imminent (Aug 6 namespace migration signal)
- Gartner "Guardian Agents" category established
- Wedge window narrows to 6-9 months
- EU AI Act live Aug 2 — regulatory tailwind active
- Seven new funded entrants ($160M+ total)

## 6. Timing risks (next 90 days)

| Risk | Timing | Impact |
|---|---|---|
| AWS Agent Registry GA | Likely re:Invent (Nov/Dec 2026) or sooner | High — three GA competitors |
| CNCF Sandbox decision on agentregistry | Board review may have occurred; decision pending | High — OSS legitimacy |
| IBM Agentic Control Plane on OpenShift | No signal; Think 2027 plausible | Medium — closes IBM's gap |
| Microsoft cross-cloud sync GA | Unknown, currently preview | High — multi-cloud governance overlay |
| Google ARD adoption | Next 6 months | Medium — federated discovery standard |
| NIST SP 800-53 agent overlays draft | Q4 2026 target | High — procurement requirements |
| EU AI Act enforcement actions | August 2026 onward | Medium — urgency for governed registries |
| MLflow Skill Registry RFC | Needs to land before RHOAI 3.6 | High for RHOAI — upstream alignment |
| Forrester ADP Wave | Q4 2026 | Medium — analyst positioning |

## Sources

1. [Google ARD Specification announcement](https://developers.googleblog.com/announcing-the-agentic-resource-discovery-specification/)
2. [Gemini Enterprise Agent Platform release notes](https://docs.google.com/gemini-enterprise-agent-platform/release-notes)
3. [AWS AgentCore release notes](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/release-notes.html)
4. [Bedrock Agents Classic maintenance mode](https://docs.aws.amazon.com/bedrock/latest/userguide/agents-classic-maintenance-mode.html)
5. [Agent 365 license enforcement (Medium)](https://derkvanderwoude.medium.com/microsoft-agent-365-license-enforcement-july-1-2026-security-impact-summary-47d7f02b46be)
6. [Shadow AI in M365 Admin Center](https://learn.microsoft.com/en-us/microsoft-365/admin/manage/agent-shadow-ai?view=o365-worldwide)
7. [Windows Agent Runtime (Build 2026)](https://windowsnews.ai/article/build-2026-microsoft-turns-windows-into-the-agent-runtime.422261)
8. [Entra Agent ID criticism (Aethyr)](https://aethyrresearch.com/blog/microsoft-entra-agent-id)
9. [IBM Agentic Control Plane](https://www.ibm.com/new/announcements/introducing-the-agentic-control-plane)
10. [IBM Sovereign Core (Cloud Native Now)](https://cloudnativenow.com/features/ibm-adds-sovereign-core-platform-based-on-red-hat-openshift/)
11. [Databricks Agent Services in Unity Catalog](https://docs.databricks.com/aws/en/ai-gateway/agent-services)
12. [Salesforce Agent Fabric control plane](https://www.salesforce.com/news/stories/agent-fabric-control-plane-announcement/)
13. [ServiceNow AI Control Tower expansion](https://newsroom.servicenow.com/press-releases/details/2026/ServiceNow-expands-AI-Control-Tower-to-discover-observe-govern-secure-and-measure-AI-deployed-across-any-system-in-the-enterprise/)
14. [ServiceNow + Microsoft Agent 365 integration](https://newsroom.servicenow.com/press-releases/details/2026/ServiceNow-expands-AI-agent-governance-through-deeper-integration-with-Microsoft/)
15. [Solo.io agentregistry + agentevals announcement](https://www.solo.io/press-releases/introducing-new-agentic-open-source-project-agentevals)
16. [kagent CNCF page](https://www.cncf.io/projects/kagent/)
17. [Kagenti/Rosso](https://kagenti.github.io/.github/)
18. [Gartner Guardian Agents Market Guide](https://thehackernews.com/2026/03/5-learnings-from-first-ever-gartner.html)
19. [Gartner Hype Cycle Platform Engineering 2026](https://www.truefoundry.com/blog/decoding-the-gartner-hype-cycle-for-platform-engineering-2026)
20. [Agent governance landscape fragmenting (iEnable)](https://ienable.ai/blog/ai-agent-governance-landscape-fragmenting.html)
21. [NIST AI Agent Standards Initiative](https://www.nist.gov/news-events/news/2026/02/announcing-ai-agent-standards-initiative-interoperable-and-secure)
22. [agentgateway air-gapped install](https://docs.solo.io/agentgateway/2.3.x/install/airgap/)
