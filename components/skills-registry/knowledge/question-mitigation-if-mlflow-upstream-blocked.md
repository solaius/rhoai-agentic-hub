---
type: question
title: Mitigation strategy if MLflow upstream implementation is blocked
description: What is the product strategy if MLflow RFCs are approved but implementation is significantly delayed or hindered? Options discussed include midstream, kubeflow, and ecosystem team solutions. status -- open
timestamp: 2026-08-04
status: open
tags: [skills-registry, agent-registry, mlflow, mitigation, strategy]
components: [skills-registry, agent-registry]
source: Internal Sync on Agent/Skill Registries 2026-08-04
---

Adel raised worst-case scenario planning: what if RFCs get approved but
implementation is majorly hindered (e.g., Databricks agrees on vision but
doesn't want it this year)?

**Options discussed:**
- **Midstream fork** -- Myriam noted this is viable but asked whether
  we should evaluate if the feature truly can't wait
- **Kubeflow hub surface** -- Ann Marie's architecture strategy doc
  identified this as fastest path for 3.6 skills; publishing a validated
  skills library doesn't require MLflow
- **OCP5 ecosystem team solution** -- Peter: "you're going to hear me
  get a lot louder about the hub we've already created using the
  partnership ecosystem team"
- **Invest in other portfolio products** -- Myriam: don't force 100%
  MLflow alignment; MLflow's core strength is observability, invest
  there; for features where timing doesn't align, use other products

**Myriam's framing:** before rushing to alternatives, evaluate whether
the feature truly needs to land now or if waiting for proper upstream
collaboration produces higher quality (citing MCP registry as example
where collaboration improved the outcome).

**Peter's counter:** speed is critical due to competitive pressure and
customers building their own solutions; get to DP fast, GA when ready.
