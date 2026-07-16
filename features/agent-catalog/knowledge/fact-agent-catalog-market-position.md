---
type: fact
title: Agent Catalog — market position
description: The industry converged on the same template→deployable→registry split we're sequencing (validating the design, 12-18mo late); nobody ships supported self-run harness images; IBM is the on-prem coopetitor; registries are now monetized.
timestamp: 2026-07-16
tags: [agent-catalog, competitive, positioning]
review_after: 2026-10-16
source: 5-lens research sweep 2026-07-16 (01-landscape, 05-competitive; adversarially verified)
---

From the [landscape](/features/agent-catalog/research/01-landscape.md) and
[competitive](/features/agent-catalog/research/05-competitive.md) research
(2026-07-16, claims adversarially verified):

- **The three-layer pattern is industry-wide**: template gallery (copy code)
  → marketplace/store (install with a trust gate) → registry (versioned
  running instances). Microsoft's Foundry "agent catalog" is exactly RHOAI
  3.5's shape (curated code samples, GitHub link-out, no deploy); Databricks
  ships the same catalog→MLflow-registry architecture we plan. Our
  sequencing is validated — and 12-18 months behind first movers (Agent
  Garden at Next '25; AWS 900+ listings Jul 2025; IBM's 150-agent catalog GA
  since May 2025).
- **Nobody ships vendor-supported self-run harness images** — the market
  sells managed runtimes (AgentCore, Agent Engine, Databricks Apps) instead.
  NVIDIA's free-blueprints / paid-AI-Enterprise-support tier is the proven
  analog for our supported-images model.
- **Registries are monetized**: Microsoft Agent 365 GA 2026-05-01 at
  $15/user/mo; Unity Catalog agent registry GA Jun 2026; AgentCore on
  consumption pricing — an infra-priced MLflow Agent Registry is a TCO wedge
  at fleet scale.
- **IBM is the coopetitor**: watsonx Orchestrate's catalog (GA since Think
  2025) is the only competitor catalog with documented on-prem/air-gapped
  deployment — running on OpenShift/Software Hub, monetizing the layer above
  our platform.
- **The wedge** — open + portable + supported + governed + disconnected —
  is real but time-boxed: Gemini is already GA on air-gapped GDC (US
  Secret/TS), so "hyperscalers can't do disconnected" is eroding. Analysts
  (Gartner agent-washing, Forrester agent-sprawl) reward curated, supported,
  governance-first catalogs over listing counts; the Forrester Agentic
  Development Platforms Wave (Q4 2026) is the nearest analyst-inclusion
  target.
