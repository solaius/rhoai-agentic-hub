---
type: fact
title: AI Gateway overview
description: Red Hat's AI-native proxy/gateway for all AI traffic — Praxis runtime, transitioning from Envoy, backing MaaS with inference routing, agentic orchestration, API translation, guardrails, and credential management.
timestamp: 2026-07-31
tags: [ai-gateway, praxis, infrastructure]
review_after: 2026-09-30
source: intake from Architecture & Direction GDoc (2026-07-30) and AI Gateway Project GDoc (2026-07-31)
---

The AI Gateway is the unified data plane for all AI traffic in RHOAI:
inference, agentic orchestration (Responses API), tool calling, A2A,
and external provider egress. It is transitioning from an Envoy + IPP
(Inference Payload Processor) architecture to Praxis, a Rust-based
AI-native proxy that owns the AI request lifecycle through composable
filters in a centrally configured pipeline.

**Key people**: Jason Greene (technical direction, author of
Architecture & Direction doc), Shane Utt (Architect), Christopher
Ferreira (PM), Matus Makovy (engineering lead/scrum).

**Key links**:
- [Architecture & Direction](/components/ai-gateway/knowledge/ref-ai-gateway-architecture-direction.md)
- [AI Gateway Project doc](/components/ai-gateway/knowledge/ref-ai-gateway-project-doc.md)
- [RHOAI architecture repo](/components/platform/knowledge/ref-opendatahub-architecture-context-repo.md)
- Upstream: [praxis-proxy/praxis](https://github.com/praxis-proxy/praxis),
  [praxis-proxy/ai](https://github.com/praxis-proxy/ai)
- Downstream: [opendatahub-io/praxis-extproc](https://github.com/opendatahub-io/praxis-extproc)
- Jira: RHAIGW project
- Slack: #forum-ai-gateway, #team-ai-gateway, #wg-ai-gateway-internal

**Current status (July 2026)**: Praxis convergence underway. AI Gateway
team kicked off July 6, 2026. 3.6 target: Praxis replaces IPP via
ext_proc (requires OSSM 3.4 / Envoy 1.38), providing Responses API +
agentic loop, Messages API, API translation, guardrails, credential
management. Envoy remains the front door for 3.6; full replacement in
subsequent releases. CNCF sandbox submission planned.

Distinct from MCP Gateway (MCP protocol traffic), but the two converge
via the same Kuadrant/Istio migration track when Praxis takes the
front-door role.
