---
type: reference
title: Seamless OGX-to-Praxis Migration for Responses, Conversations, and RAG APIs in 3.6
description: Feature making Praxis the single customer-facing API entrypoint in 3.6, with OGX retained internally for state persistence and RAG; greenfield Praxis-only, upgraded deployments route through Praxis; fix_version 3.6 EA1.
resource: https://redhat.atlassian.net/browse/RHAISTRAT-2277
tags: [ai-gateway, praxis, ogx, migration]
timestamp: 2026-07-31
review_after: 2026-10-31
source: hub.jira-sweep 2026-07-31
---

Praxis becomes sole publicly reachable implementation of /v1/responses,
/v1/conversations, and /v1/embeddings. Clear per-resource-type ownership
prevents dual-write. Rollback path allows reversion during transition.
Notes 61 existing customer deployments (39 in regulated industries)
that cannot absorb contract changes. Clones RHAIRFE-2711. Fix_version:
3.6 EA1.
