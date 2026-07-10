---
type: jtbd
title: "Control my agentic AI costs"
description: "When I scale agents across my organization, I want budget controls, model routing, and per-agent cost attribution, so token consumption doesn't bankrupt my AI program."
persona: platform-engineer
status: candidate
timestamp: 2026-07-10
source: narrative/research/02-agentic-requirements-landscape.md
tags: [narrative, jtbd, economics, cost, research-gap]
---
**When** I scale agents across my organization,
**I want to** control costs with budget caps, intelligent model routing,
and per-agent cost attribution,
**so** token consumption doesn't bankrupt my AI program and I can tie
spending to business outcomes.

**Evidence (from research):**
- Token usage grew 1,001% from Jan 2025 to Apr 2026 [doc 02, source 8]
- Uber burned through its entire 2026 AI budget by April [doc 02, src 8]
- Ramp data: 680x spending gap — top 1% spend $7,450/employee/month vs
  median $11.38 [doc 02, source 9]
- Accenture (2026): 95% of enterprise AI usage runs on premium frontier
  models for tasks that do not require them [doc 02, source 8]
- Gartner: cost optimizations reduce agentic AI costs 40-55% within 12
  months [doc 01, source 11]
- Hybrid routing achieves 35-40% cost reduction maintaining 98%+ accuracy
- Linux Foundation launched the Tokenomics Foundation (June 2026) with
  Oracle, Google, Microsoft, JPMorganChase [doc 02, source 8]

**Gap vs existing JTBDs:** JTBD #4 (Make inference work for agents)
focuses on inference performance, availability, and self-hosting
capability. This JTBD covers the economic governance layer: budget
enforcement, model routing for cost optimization, cost attribution to
business outcomes, and anomaly detection (runaway agents).

**Pillar:** Inference × Agents (the intersection — the cost paradox)
