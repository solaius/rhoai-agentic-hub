---
type: fact
title: "Agentic product maturity timeline (as of 2026-07-08)"
description: "GA/TP/coming status of agentic components as presented at the Power 90: Model Gateways, NeMo Guardrails, ODX, MLflow = GA; MCP ecosystem, OpenShell, Eval Hub = coming 3.5-3.6."
timestamp: 2026-07-08
source: Power 90 session 2026-07-08
review_after: 2026-10-01
tags: [narrative, roadmap, maturity]
---
Product maturity snapshot from Adel's Power 90 presentation (2026-07-08):

**GA today:**
- Model Gateways (model access governance layer)
- NeMo Guardrails (guardrail orchestrator — replaced IBM guardrail
  orchestrator, now in maintenance/deprecation)
- ODX (RAG/retrieval layer — near-term, converging to AI Gateway mid-term)
- MLflow (tracing, logging, evaluation — Red Hat is now a contributor)
- Red Teaming (GA very soon — Chatterbox acquisition consolidated)

**Tech Preview / Coming (3.5):**
- MCP ecosystem (registries, lifecycle, gateway) — tech review in 3.5
- Agent Sandbox / workload orchestration — tech review
- Eval Hub (evaluation control plane)
- Agent templates in AI Hub (Learning Resources → more visible placement)

**GA target (3.6, ~November 2026):**
- MCP ecosystem full GA (onboarding → serving → governing → consuming)
- Agent registries (MLflow-based, upstream)
- OpenShell (agent sandboxing — secure onboarding, policy, SDK)

**Directional / longer-term:**
- AI Gateway convergence (ODX + gateways + llm-d)
- A2A protocol support (multi-agent distributed communication)
- Agent composition layer (Asian spec, wiring agents to secure environments)

**Open issue:** MCP Gateway GA may require OCP 5 — team pushing for OCP 4
support to meet 3.6 GA promise (see `ref-peter-adel-sync-20260710.md`).
