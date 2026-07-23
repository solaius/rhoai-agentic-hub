---
type: question
title: Skills/MCP configuration at deploy time — not in UX designs
description: MCP and skills set at runtime are not part of the deploy wizard UX designs (Gage, 2026-07-11); only agent-card skill/MCP discovery exists. No mechanism to say "use this skill for my harness" at deploy time.
timestamp: 2026-07-11
status: open
tags: [agent-catalog, skills, mcp, deploy-ux, gap]
features: [agent-catalog, skills-registry]
source: Slack group DM Ann Marie/Andrew/Gage ~2026-07-11
asks:
  - Ann Marie 2026-07-11 — wants POC to include skill selection in catalog deploy flow
  - Gage 2026-07-11 — clarifies MCP/skills not in current designs, only discovery
---

**Question**: How will users select and configure skills/MCP servers
when deploying an agent from the catalog?

**Context**: Gage Krumbach confirmed (~2026-07-11) that MCP and
runtime-set skills are **not part of the current UX designs**. The
designs only cover discovering what agent-card skills and MCPs exist —
not binding them to a deployment.

The deploy wizard currently allows setting arbitrary environment
variables, which could carry skill bundle names if MLflow RFC PR #26
lands (see
[fact-ann-marie-poc-proposal](/features/agent-catalog/knowledge/fact-ann-marie-poc-proposal.md)).
But there is no first-class UX for "I want to use this skill from the
catalog for my harness/agent" — a gap Adel also flagged in the
harness support boundary discussion (RHAIRFE-2310 scope; see
[fact-catalog-deploy-stack](/features/agent-interop/knowledge/fact-catalog-deploy-stack.md)).

**Related**: [question-agent-catalog-harness-playground-integration](/features/agent-catalog/knowledge/question-agent-catalog-harness-playground-integration.md)
(adjacent gap — harness chat-interface integration also not in 3.5 scope).

**Status**: open as of 2026-07-11. Ann Marie's POC proposal may
address this experimentally.
