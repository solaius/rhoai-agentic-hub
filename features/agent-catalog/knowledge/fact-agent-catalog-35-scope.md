---
type: fact
title: Agent Catalog 3.5 — scope and delivery state
description: 3.5 = read-only starter-kit catalog + read-only deployments view; YAML catalog source (disconnected mandatory); no admin UI; OpenAPI merged 2026-07-03; ownership map across AI Hub/Razzmatazz/AgentDev/AgentOps.
timestamp: 2026-07-16
tags: [agent-catalog, 3.5, scope]
review_after: 2026-08-31
---

**Shape** (MUSTs from Adel Zaalouk's 2026-06-03/04 MVP cut of RHAISTRAT-1697,
narrowed by the
[2026-07-09 no-deploy decision](/features/agent-catalog/knowledge/decision-agent-catalog-no-deploy-35.md)):

- Agents View: RH-curated starter-kit templates from
  [agentic-starter-kits](/features/agent-catalog/knowledge/ref-agentic-starter-kits-repo.md),
  cards linking out to GitHub; fields per the
  [3.5 field set](/features/agent-catalog/knowledge/decision-agent-catalog-35-field-set.md).
- Agent Deployments view: read-only discovery of AgentSandbox CRs
  (label `openshell.ai/managed-by`).
- No deploy button, no agent-card discovery, no admin/settings UI
  (`settings/agent-resources` cut 2026-06-18/22, Andrew Ballantyne — MCP
  admin UI took priority; the consumer `ai-hub/agents/catalog` view stays).

**Implementation.**

- Catalog source = YAML baked at build time — mandatory disconnected support,
  mirroring the MCP catalog (sources YAML → image → DB); GitHub slurping is a
  later enhancement (Ramesh Reddy, 2026-06-08). The "open GitHub" link dims
  when the repo is unreachable.
- Catalog = "v3" of the Model Catalog → MCP Catalog pattern (Andrew
  Ballantyne); backend in kubeflow/hub — OpenAPI spec merged 2026-07-03
  (PR #2907); agent.yaml exposed via `/agents/{id}/artifacts` (PR #2928).
- A2A today: only the CrewAI and LangGraph kits implement it; chat
  completions is the common interface across kits.

**Ownership.** Backend: Alessio Pragliola + Luca Giorgi (AI Hub team, per
Ramesh Reddy 2026-06-04). Dashboard/BFF: Razzmatazz (Gage Krumbach, Daniel
Warner, et al.; BFF build started after the spec merge, show-and-tell
~2026-07-17). UX: Yabbes Rajan (catalog), Daniel Warner (rest of AI Hub).
Images/kits: AgentDev (Aakanksha Duggal) near-term. Deployments backend:
AgentOps (Dimitri Saridakis) — kagenti REST API explicitly out of scope;
interface with opendatahub-io/agents-operator via kube API only.
