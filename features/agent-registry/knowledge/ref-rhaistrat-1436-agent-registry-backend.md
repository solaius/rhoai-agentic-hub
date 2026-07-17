---
type: reference
title: "RHAISTRAT-1436: Agent Registry Backend (MLflow-native)"
description: The previously unmapped EA2 backend vehicle — New, no fixVersion, parent RHAISTRAT-1339 (AI Hub), 9 RHAI epics (schema, REST + workspace-aware store, Python client, Go SDK, operator RBAC, status transitions, sync controller, license, docs); assigned to the RFC-0008 author, so upstream and downstream share an author.
resource: https://redhat.atlassian.net/browse/RHAISTRAT-1436
timestamp: 2026-07-16
tags: [agent-registry, mlflow, backend, jira]
---
Found by the 2026-07-16 jira-gap lens
([research/11-jira-gap](/features/agent-registry/research/11-jira-gap.md))
— the hub had assumed the EA2 backend was untracked. Paraphrased shape:
MLflow-native agent registry backend, single entity with a single
governance lifecycle (experimental→active→deprecated→archived), required
owner field, compliance/access-tier fields reserved, soft-delete default,
and a sync epic still targeting the removed kagenti operator. Divergences
from the research architecture (no runtime instance states, no SUSPENDED,
no version_ref dual-entity join, no risk-tier/log-refs/identity-linkage
fields, no retention period) are schema-freeze-sensitive — see
[question-agent-registry-backend-dual-entity](/features/agent-registry/knowledge/question-agent-registry-backend-dual-entity.md).
