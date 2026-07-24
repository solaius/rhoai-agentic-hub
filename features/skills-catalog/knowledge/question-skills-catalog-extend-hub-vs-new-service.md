---
type: question
title: Should the skills catalog extend kubeflow/hub or build a standalone service?
status: open
description: Architecture question -- extend kubeflow/hub as 4th catalog type (proven pattern, lower risk, same Go+PostgreSQL+BFF stack, MCP/agent catalog precedent) vs build standalone Go+PostgreSQL per RHAISTRAT-1780. Research recommends hub extension.
timestamp: 2026-07-23
tags: [skills-catalog, architecture, kubeflow]
features: [skills-catalog]
source: skills-catalog research 03-architecture
---

RHAISTRAT-1780 proposes a new standalone Go + PostgreSQL service. The
research (03-architecture) recommends extending kubeflow/hub instead:

**Hub extension (recommended)**:
- Reuses existing PostgreSQL schema (ML-Metadata ER model)
- Reuses REST framework, source aggregation, BFF integration
- Avoids new Deployment, Service, StatefulSet, operator path
- MCP catalog and agent catalog both followed this path
- The current direction (Git-backed, YAML-source, read-only) is
  architecturally identical to existing catalogs

**Standalone service**:
- Team autonomy, performance isolation
- Potentially different data model requirements
- Independent scaling

**Counter-argument**: a standalone service makes sense only if skills
have fundamentally different aggregation requirements that hub's
source-type plugin model cannot accommodate. The current direction does
not suggest this is the case.

This needs resolution before implementation begins -- it determines the
entire development approach and effort estimate.
