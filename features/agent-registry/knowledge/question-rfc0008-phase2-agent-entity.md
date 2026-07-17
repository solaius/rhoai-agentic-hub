---
type: question
title: Who authors RFC-0008 Phase 2, and does the post-deployment design attach to it?
description: Phase 1 (skills) defers agent-shaped entities to Phase 2 — open who writes Phase 2, whether the dual-entity structure (AgentVersion + runtime instance with SUSPENDED) lands there, and whether Varsha's dormant discovery proposal becomes its runtime companion.
status: open
timestamp: 2026-07-16
tags: [agent-registry, mlflow, upstream, rfc]
---
RFC-0008 ([ref-mlflow-rfc-0008](/features/agent-registry/knowledge/ref-mlflow-rfc-0008.md))
is skills-only Phase 1. The registry's upstream needs — dual entities,
SUSPENDED runtime state, card-verification fields — must be shaped into
Phase 2 before Phase 1 review hardens the patterns. Varsha's branch is
dormant since 2026-04-23 and kagenti-baselined; re-baselining it
([research/09-architecture](/features/agent-registry/research/09-architecture.md) §1)
as the Phase-2 runtime-discovery companion is the recommended vehicle.

**Evidence 2026-07-16 (jira-gap lens)**: the downstream EA2 backend
([RHAISTRAT-1436](/features/agent-registry/knowledge/ref-rhaistrat-1436-agent-registry-backend.md))
is assigned to the RFC-0008 author — upstream and downstream share an
author, so the alignment channel exists; the Phase-2 question is now
also a 1436-schema question
([question-agent-registry-backend-dual-entity](/features/agent-registry/knowledge/question-agent-registry-backend-dual-entity.md)).
