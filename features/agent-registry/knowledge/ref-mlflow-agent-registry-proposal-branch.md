---
type: reference
title: "varshaprasad96/mlflow (branch: spike/gateway)"
description: Draft agent registry RFC — domain model, discovery plugin interface, trust verification, Python client API. Not merged upstream.
resource: https://github.com/varshaprasad96/mlflow/blob/spike/gateway/proposals/agent-registry-discovery.md
tags: [agent-registry, mlflow, proposal, github]
timestamp: 2026-07-06
source: ai-asset-registry/docs/knowledge-registry.md §12 (as of 2026-07-05)
review_after: 2026-08-05
---
Draft RFC starting point by Varsha Prasad Narsing (Peter Double now taking over): Agent entity + AgentSkill domain model, 4 lifecycle states (ACTIVE/UNHEALTHY/STALE/REMOVED), `AgentDiscoveryProvider` interface with 3 sync mechanisms, reference Kubernetes/kagenti plugin, SPIFFE/JWS trust verification, Gateway auto-sync, and `mlflow.agents` Python client API. Full source for [fact-agent-registry.md](/features/agent-registry/knowledge/fact-agent-registry.md). Not merged upstream — a proposal, not finalized.
