---
type: fact
title: "Agentic strategy: five themes (2026)"
description: "The five strategic themes from the 2026 agentic AI strategy: Bring Your Own Agent, Capture API Surface, MCP Ecosystem, Self-hosted Inference + AI Hub, Agent Ops."
timestamp: 2026-07-08
source: Power 90 session 2026-07-08
tags: [narrative, strategy]
---
Adel Zaalouk's five-theme framework presented to field at the Power 90
(2026-07-08). These are the execution themes under the Agents pillar:

1. **Bring Your Own Agent (BYOA):** regardless of framework (LangGraph,
   CrewAI, Strands, ADK, harnesses like OpenClaw/Claude Code), RHOAI
   provides the production onboarding path — secure execution, identity,
   lifecycle management.

2. **Capture API Surface:** standardize on open implementations of the
   agentic APIs — Chat Completions, Responses API, Messages API,
   Interactions API. Only ~4 APIs across 1000+ frameworks. OGX (formerly
   Llama Stack) provides the open translation layer.

3. **MCP Ecosystem:** standardize tool calling via MCP. The ecosystem
   covers onboarding, serving, governing, and consuming MCP servers.
   MCP Lifecycle Operator, MCP Gateway, MCP Registry, MCP Catalog.
   GA target: RHOAI 3.6.

4. **Self-hosted Inference + AI Hub:** self-managed inference for cost
   control, sovereignty, and customization. AI Hub as the discovery
   plane for AI assets (models, MCP servers, agents, skills, prompts).
   GenAI Studio for experimentation. Agent templates as first agent
   form factor.

5. **Agent Ops:** the operational layer — security (OpenShell sandboxing,
   SPIFFE identity), observability (MLflow tracing, OpenTelemetry),
   evaluation (Eval Hub), governance (AI Gateway, guardrails, red
   teaming), access control (model/tool/agent identity layers).

See also: `fact-agentic-ai-four-pillars.md` (the broader four-pillar
framing these themes sit within).
