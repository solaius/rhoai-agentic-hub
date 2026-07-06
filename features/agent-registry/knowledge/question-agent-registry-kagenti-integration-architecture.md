---
type: question
title: Which kagenti integration architecture should be the RHOAI default?
description: Pull, push, or hybrid — which kagenti/agent-registry integration pattern should RHOAI standardize on?
status: open
timestamp: 2026-07-06
tags: [agent-registry, kagenti, mlflow]
source: ai-asset-registry/docs/knowledge-registry.md §13 (as of 2026-07-05)
---
Push via an `MLflowReconciler` is the most natural fit for [fact-agent-registry.md](/features/agent-registry/knowledge/fact-agent-registry.md)'s Kubernetes discovery plugin (kagenti AgentCard CRD) but adds complexity versus pull or a hybrid model. Not yet decided.
