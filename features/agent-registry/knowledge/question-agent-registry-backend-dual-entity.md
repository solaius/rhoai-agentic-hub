---
type: question
title: Will the backend schema gain runtime instance states and version_ref before the EA2 freeze?
description: RHAISTRAT-1436's schema is single-entity with one governance lifecycle — no runtime instance states, no SUSPENDED, no version_ref join, no risk-tier/log-refs/identity-linkage/retention — all cheap before the EA2 schema freeze and breaking after.
status: open
timestamp: 2026-07-16
tags: [agent-registry, mlflow, backend, schema]
---
The research architecture recommends dual entities (AgentVersion under
governance tracks ↔ runtime instance under ACTIVE/UNHEALTHY/STALE/
REMOVED + SUSPENDED, joined by nullable `version_ref` — the unlinked
state IS the shadow inventory), and the requirements lens adds the
regulatory field set (risk tier, log refs, permissions/identity linkage,
REMOVED retention ≥6 months). None of it is in
[RHAISTRAT-1436](/features/agent-registry/knowledge/ref-rhaistrat-1436-agent-registry-backend.md)'s
current shape (paraphrased). The upstream/downstream shared author is
the natural alignment channel
([question-rfc0008-phase2-agent-entity](/features/agent-registry/knowledge/question-rfc0008-phase2-agent-entity.md)).
See [research/11-jira-gap](/features/agent-registry/research/11-jira-gap.md)
Direction B rows 2/6/7.
