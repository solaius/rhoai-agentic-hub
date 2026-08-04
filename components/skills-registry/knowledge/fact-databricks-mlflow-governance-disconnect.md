---
type: fact
title: Databricks does not see MLflow as their governance strategy
description: Databricks uses Unity Catalog for governance, not MLflow; MLflow team mantra is "make MLflow famous"; open to agent/skill registry if proven to increase GenAI adoption, but leadership won't prioritize non-Databricks-roadmap work.
timestamp: 2026-08-04
tags: [skills-registry, agent-registry, mlflow, databricks, unity-catalog]
components: [skills-registry, agent-registry]
source: Internal Sync on Agent/Skill Registries 2026-08-04
---

Key dynamics from the 2026-08-04 internal sync:

**Databricks' MLflow position:**
- Unity Catalog is their governance strategy, not MLflow
- MLflow team's mantra is "make MLflow famous" -- they want to increase
  adoption, especially around GenAI/agents
- They have agent catalog/MCP solutions in preview in their downstream
  (Unity Catalog)
- Leadership doesn't let the MLflow team prioritize work that doesn't
  help the Databricks roadmap (with some latitude for community health)

**What this means for Red Hat:**
- Databricks is open to expanding MLflow scope for agent/skill registry
  if we show good reason it increases GenAI adoption
- They want to see our customer feedback (anonymized) to understand
  governance needs they don't hear from their own customers
- They're cautious about committing to standards that might not become
  industry standard (why MCP registry went smoother -- existing spec)
- Bill: tension between "fame" (mass audience) and "governance" (IT
  execs who want to control developers) may be a structural headwind

**Adel's question for PM sync:** Does Databricks want to align MLflow
upstream with what they've built in Unity Catalog for agents? Understanding
their downstream strategy would clarify how much they'll invest upstream.
