---
type: fact
title: MLflow RFC-0008 — registry stream is live, skills-first, Red Hat-authored
description: RFC-0008 (MVP Skill Registry Phase 1, mlflow/rfcs PR #26, 2026-07-14, Bill Murdock) puts metadata-first records and lifecycle stages upstream; agent-shaped entities are deferred to Phase 2 — the April "open window" play has executed, skills-first.
timestamp: 2026-07-16
tags: [agent-registry, mlflow, upstream, rfc]
features: [skills-registry]
---
The upstream MLflow registry conversation now runs through
[RFC-0008](https://github.com/mlflow/rfcs/pull/26) ("MVP Skill Registry —
Phase 1", draft PR opened 2026-07-14 by Bill Murdock
([person-bill-murdock](/features/platform/knowledge/person-bill-murdock.md)),
no reviewers assigned as of 2026-07-16), fed by
[mlflow/mlflow#22833](https://github.com/mlflow/mlflow/issues/22833)
(2026-04-23, RHOAI-framed motivation incl. federated discovery). Design:
metadata-first + typed source pointers + lifecycle stages **in the
upstream core** + package-manager plugins. Subagents/hooks/MCP-refs — the
agent-shaped entities — are explicitly deferred to Phase 2.

Consequences for the agent registry: (1) the upstream stream is Red
Hat-authored, not just Red Hat-lobbied — the play is shaping Phase 2, not
racing a standalone RFC; (2) lifecycle stages upstream contradicts the
April assumption that lifecycle is strictly downstream and shrinks the
RHOAI governance delta if accepted; (3) Varsha's dormant post-deployment
proposal is the natural runtime-discovery companion to Phase 2. See
[research/07-upstream](/features/agent-registry/research/07-upstream.md).
