---
type: jtbd
title: "Evaluate and observe agents"
description: "When I run agents in production, I want to evaluate and observe agent behavior, so I can detect failures, track costs, and prove compliance — MLflow, Eval Hub, OpenTelemetry."
persona: platform-engineer
status: candidate
timestamp: 2026-07-10
source: ref-power-90-agentic-ai-20260708.md
features: [agent-ops]
tags: [narrative, jtbd, observability, evaluation]
---
**When** I run agents in production,
**I want to** evaluate and observe agent behavior end-to-end,
**so I can** detect failures, track token costs, iterate on prompts, and
prove compliance to auditors.

**How RHOAI addresses this:**
- MLflow (GA) — single pane of glass for agent tracing: inputs, outputs,
  tool calls, token usage, latency. OpenTelemetry compatible. Red Hat is
  now a contributor.
- Eval Hub — evaluation control plane supporting multiple frameworks,
  pluggable into CI/CD pipelines. Adapters for custom benchmarks. OCI
  artifact storage for reproducible evaluations.
- LLM-as-judge — evaluate agent outputs using another LLM for semantic
  correctness, business alignment, safety compliance.
- End-to-end system evaluation — not just the model, but the full agent
  system (model + tools + prompts + knowledge).

**Key insight from Myriam (Power 90):** observability shouldn't be optional
for developers — it should be built into the platform so platform engineers
always have visibility, even over agents they didn't build.

**Pillar:** Agents (Agent Ops theme)
