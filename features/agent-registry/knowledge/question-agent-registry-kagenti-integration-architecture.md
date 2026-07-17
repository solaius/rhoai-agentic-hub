---
type: question
title: Which kagenti integration architecture should be the RHOAI default?
description: Pull, push, or hybrid — which kagenti/agent-registry integration pattern should RHOAI standardize on?
status: answered
timestamp: 2026-07-16
tags: [agent-registry, kagenti, mlflow]
source: ai-asset-registry/docs/knowledge-registry.md §13 (as of 2026-07-05)
---
Push via an `MLflowReconciler` is the most natural fit for [fact-agent-registry.md](/features/agent-registry/knowledge/fact-agent-registry.md)'s Kubernetes discovery plugin (kagenti AgentCard CRD) but adds complexity versus pull or a hybrid model. Not yet decided.

**Answered 2026-07-16**: moot — kagenti was removed from the roadmap (2026-07-10, [fact-kagenti-roadmap-removal.md](/features/agent-registry/knowledge/fact-kagenti-roadmap-removal.md)). The pull/push/hybrid choice dissolves into the post-kagenti architecture: Sandbox-CR WATCH (pull) for enumeration + deploy-time WEBHOOK (push) for rich records + an ADR-#142-style sync controller for reconciliation. See [research/09-architecture](/features/agent-registry/research/09-architecture.md).
