---
type: fact
title: RHAISTRAT-1780 -- Skills Catalog scope and architecture
description: RHAISTRAT-1780 Skills Catalog scope -- Go backend with PostgreSQL, odh-dashboard React/PatternFly 6 BFF UI module, trust tiers (RH/Partner/Org/Community), ConfigMap disconnected import, usage telemetry, 6-9 sprint effort estimate.
timestamp: 2026-07-23
tags: [skills-catalog, rhaistrat, scope, architecture]
features: [skills-catalog]
review_after: 2026-09-23
source: Aditi Saluja status/scope/roadmap GDoc (2026-07-21)
---

RHAISTRAT-1780: Skills Catalog -- Discovery and Acquisition.
Status: New, 3.6-candidate. Eng: Ramesh Reddy.

**Planned architecture**:

| Component | Details |
|---|---|
| Backend service | New skills-catalog service (Go, PostgreSQL, source aggregation) |
| UI module | New skills-catalog-ui BFF module in odh-dashboard (React/PatternFly 6) |
| UX | Browse, explore, acquire for skills and skill packages |
| Trust tiers | Red Hat-provided, Partner-verified, Organization-approved, Community-contributed |
| Telemetry | Usage telemetry (views, explores, acquisitions) |
| Disconnected | ConfigMap-based offline import |
| Effort | Large (6-9 sprints) |

**Open questions** (from the STRAT):
- Formal definition/taxonomy of a skill in RHOAI (align with RFC-0008
  entity types)
- Which Red Hat-authored assets seed the initial catalog (depends on
  RHAISTRAT-1940)
- Partner feed format (Microsoft Azure team asking)
- Acquisition UX per skill type (different flows for SKILL.md vs MCP
  vs OCI)
