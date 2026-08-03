---
type: fact
title: Agent registry market position (2026-08)
description: Two GA cloud competitors (Google July 30 + Microsoft May 1), AWS GA imminent (Aug 6 namespace migration), Gartner "Guardian Agents" category inaugural, 7 new funded entrants ($160M+), EU AI Act live Aug 2; wedge = self-managed + disconnected + governed fleet registry with lineage, window narrows to 6-9 months (from 6-12 in July).
timestamp: 2026-08-03
tags: [agent-registry, competitive, market]
review_after: 2026-10-03
---
As of 2026-08-03 (details + sources:
[research/13-competitive](/components/agent-registry/research/13-competitive.md),
[research/08-landscape](/components/agent-registry/research/08-landscape.md)):

- **Google Agent Registry GA'd July 30, 2026** — part of Gemini Enterprise
  Agent Platform. Includes ARD federated discovery protocol (first
  vendor-backed agent discovery standard) and SPIFFE-based agent identity
  (cloud-neutral, closer to RHOAI's natural approach than Entra Agent ID).
  Two GA cloud competitors now (Google + Microsoft).
- **AWS Agent Registry GA imminent** — August 6 namespace migration
  (`bedrock-agentcore` → `agent-registry`) is a strong GA signal;
  production-scale quotas shipped July (5,000 sessions, 200 TPS). Still
  preview as of Aug 3. Per-"Net Records" GA pricing signaled.
- **Microsoft** closed the gap hard: Agent 365 GA 2026-05-01; license
  enforcement active July 1 ($15/user/mo or M365 E7); **cross-cloud
  registry sync in preview** (AWS Bedrock + Google Cloud connections) —
  the most direct threat to multi-cloud positioning. Free inventory tier
  confirmed. Entra Agent ID criticized as "doesn't work outside Azure."
- **IBM** Agentic Control Plane live June 2026 on AWS + IBM Cloud **only**;
  classic Orchestrate on OpenShift. IBM Sovereign Core (on OpenShift, Red
  Hat AI) lacks agent-specific governance — architectural seam Red Hat
  can fill. On-prem control plane port likely but unconfirmed.
- **Gartner "Guardian Agents" category established** (Market Guide, Feb
  2026, inaugural): explicitly calls for "independent guardian agent
  layers that work across clouds and platforms." AX (Agent Experience)
  in Platform Engineering Hype Cycle. Forrester Wave for Bot and Agent
  Trust Management Software in Q2 2026.
- **Seven new funded entrants** ($160M+ total): Geordie AI ($6.5M),
  JetStream Security ($34M), Oasis Security ($120M Series B), AvePoint
  AgentPulse (public co), Kosmoy, Credo AI, Arthur AI. All SaaS, none
  on-prem — but shaping buyer expectations.
- **Solo.io four-project OSS suite** expanding: kagent (CNCF Sandbox,
  300+ contributors), agentgateway (LF, air-gapped docs exist),
  agentregistry (CNCF submission), agentevals (new). The OSS alternative
  is building faster than the RHOAI registry.
- **EU AI Act high-risk obligations live August 2, 2026** — cross-platform
  agent governance is now a compliance requirement. NIST SP 800-53 agent
  overlays targeting Q4 2026 will create procurement requirements.
- **Wedge re-read**: nobody ships a self-managed, disconnected, governed
  fleet registry with lineage. Window narrows to **6-9 months** (from
  6-12 in July): Google GA + AWS imminent + Microsoft cross-cloud sync +
  Solo.io air-gapped momentum compress the timeline. Infra-priced TCO
  argument blunted by Microsoft's free inventory floor and ServiceNow's
  free bundling.

## History
- 2026-08-03 — **Update** — Google GA July 30 (two GA competitors),
  AWS GA imminent (Aug 6 namespace migration), Gartner Guardian Agents
  category, 7 new funded entrants, EU AI Act live, wedge window narrowed
  to 6-9 months, Microsoft cross-cloud sync in preview added.
- 2026-07-16 — Created. Microsoft GA, Google shipped, IBM SaaS-only,
  AWS still preview; wedge = self-managed + disconnected + governed, lag
  6-12 months.
