---
type: fact
title: Agent registry market position (2026-07)
description: The registry layer GA'd around us — Microsoft ships inventory free + $15/user governance (Agent 365 GA 2026-05-01), Google shipped, IBM's control plane is SaaS-only (on-prem window open, time-boxed), AWS still preview; federation arrives bilaterally; wedge = self-managed + disconnected + governed fleet registry with lineage, lag ~6-12 months.
timestamp: 2026-07-16
tags: [agent-registry, competitive, market]
---
As of 2026-07-16 (details + sources:
[research/08-landscape](/features/agent-registry/research/08-landscape.md)):

- **Microsoft** closed the April series' "notable gap" hard: Agent 365 GA
  2026-05-01; Entra Agent ID makes agents directory objects; core
  registry/inventory reportedly license-free, the governance stack is
  $15/user/mo — **inventory is commoditizing, governance is monetized**.
- **AWS** Agent Registry is *still* Public Preview (no GA Apr→Jul);
  per-"Net-Record" GA pricing signaled; but AgentCore GA'd in GovCloud —
  sovereign-cloud erosion of the compliance wedge.
- **Google** shipped a documented registry product (Gemini Enterprise
  Agent Platform, 2026-04-22): agents + MCP servers + tools,
  auto-registration, A2A import.
- **IBM** repositioned as "Agentic Control Plane" — live June 2026 on
  AWS + IBM Cloud **only**; only classic Orchestrate installs on
  OpenShift. The on-prem fleet-governance slot is open and time-boxed by
  their eventual port.
- **Federation ships bilaterally, not via standards**: ServiceNow AI
  Control Tower ↔ Agent 365 dual-registry publishing; Salesforce Agent
  Scanners (GA Jan 2026) auto-discover cross-cloud agents to A2A cards.
- **Wedge re-read**: nobody ships a self-managed, disconnected, governed
  fleet registry with lineage; infra-priced TCO argument is stronger now
  that meters are visible, blunted by Microsoft's free inventory floor.
  Registry lag vs market ≈ 6–12 months (catalog's is 12–18).
