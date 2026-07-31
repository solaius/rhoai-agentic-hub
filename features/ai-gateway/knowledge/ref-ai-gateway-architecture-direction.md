---
type: reference
title: "Red Hat AI Gateway: Architecture & Direction"
description: Live technical reference for the Praxis convergence decision — rationale, architecture (three-layer), migration plan, what changes/stays/becomes possible, and 3.6 delivery plan. Jason Greene, July 30, 2026.
resource: https://docs.google.com/document/d/1-c6qyeLpS2y1aCUUj6CCOtwtXu7AkAkQZuNU878qCpQ
tags: [ai-gateway, praxis, architecture, strategy]
timestamp: 2026-07-31
review_after: 2026-09-30
source: user-provided, fetched via Google Workspace MCP 2026-07-31
---

The canonical Architecture & Direction document for the AI Gateway's
transition to Praxis. Written by Jason Greene for engineers and PMs
across AI.

Covers: why Envoy's extension model cannot support the needed
capabilities (composition failure, ext_proc proliferation); the
three-layer target architecture (front door, Praxis AI data plane,
llm-d EPP placement); what happens to IPP, OGX, ITS, Semantic Router,
Kuadrant, and EPP; what becomes possible (tenant isolation,
whole-session enforcement, agent governance, intelligent routing,
native Messages/Responses, cross-path guardrails); the delivery
timeline (3.5 as-is, 3.6 Praxis replaces IPP + Responses, post-3.6
Envoy replacement); the cross-org delivery model and team structure.

Live document; aspects noted as evolving.
