---
type: fact
title: Self-healing agents — competitive landscape
description: Competitive landscape for agent self-healing/improvement — LangSmith Engine (closed, metered), Raindrop 2.0 ($15M raise, MCP-based), plus eval alerting table (6 competitors ship it, MLflow has none). No open-source platform ships the full detect-diagnose-fix loop.
timestamp: 2026-08-07
tags: [agent-ops, competitive, self-healing]
review_after: 2026-10-07
source: https://github.com/Nehanth/agent-improvement-rfc/pull/1
---

## Eval alerting (table stakes — MLflow has none)

| Platform | Eval alerting | Notes |
|----------|--------------|-------|
| LangSmith | Yes | Threshold alerts on production eval scores |
| Langfuse | Yes | Monitors with notification integrations |
| Arize | Yes | Configurable monitors + integrations |
| Braintrust | Yes | Automations on eval results |
| Datadog LLM Obs | Yes | Full monitoring stack integration |
| Galileo | Yes | Alert setup on logs |
| **MLflow** | **No** | No webhook events for traces, evals, or issues |
| **Databricks managed MLflow** | **No** | Same gap in managed offering |

## Self-healing / improvement loop

**LangSmith Engine** (LangChain, 2026) — Detects recurring issues in
production traces, diagnoses root cause against connected source code,
proposes fixes as GitHub PRs. Closed source, runs only on LangChain-managed
inference, metered per scan. Tight LangChain framework coupling.

**Raindrop 2.0** (2026) — "Self-Healing Agents" branding. Detects and
root-causes failures; customer's own coding agent pulls context over MCP,
fixes it, opens the PR. Raised $15M from Lightspeed Venture Partners.
Customers include Vercel, Replit, Speak. Framework-agnostic approach via
MCP.

## Open-source gap

No open-source platform ships the full detect-diagnose-fix loop. MLflow
already has tracing, online judges (auto-eval), issue detection, prompt
registry, the MLflow Assistant, and an MCP server. The agent-improvement
RFC proposes connecting these pieces to close the loop — positioning
MLflow as the first open-source platform with end-to-end self-healing.
