---
type: reference
title: Tenant isolation and ABAC enforcement across Praxis-to-OGX boundary
description: Spike investigating whether tenant isolation and ABAC remain intact when Praxis becomes the entrypoint in 3.6 with OGX serving resource APIs behind it -- delivers findings doc with gap analysis.
resource: https://redhat.atlassian.net/browse/RHAISTRAT-2409
tags: [ai-gateway, security, tenancy, abac, ogx]
timestamp: 2026-07-31
review_after: 2026-10-31
source: hub.jira-sweep 2026-07-31
---

OGX and the Praxis-based gateway enforce access control through
architecturally different mechanisms (application-level ABAC vs
Kuadrant/Authorino policy primitives). This spike catalogs every OGX
ABAC enforcement point, maps it to the Authorino model, and validates
composability across the service boundary. Deliverable: ABAC mapping
table, identified gaps, trust boundary model, recommended approach.
Clones RHAIRFE-2919. Related: RHAIENG-6638.
