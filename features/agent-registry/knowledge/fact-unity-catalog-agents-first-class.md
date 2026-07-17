---
type: fact
title: Unity Catalog registers agents first-class; Unity AI Gateway parts open-sourced into MLflow
description: At DAIS 2026 (June), agents/skills/MCP services became registrable and governable in Unity Catalog via Unity AI Gateway, with gateway/governance pieces open-sourced into MLflow — upstream MLflow is becoming a governance surface with Databricks steering the substrate.
timestamp: 2026-07-16
tags: [agent-registry, mlflow, databricks, competitive]
features: [skills-registry]
---
The April claim "Unity Catalog has no Agent asset type" is false since
DAIS 2026: agents, skills, and MCP services are now registrable +
governable in Unity Catalog via Unity AI Gateway, and Databricks
open-sourced gateway/governance pieces into Unity Catalog + MLflow
(3.13 added access control, trace lifecycle, richer agent support). The
"Databricks builds it first" risk materialized **in the proprietary
layer** with no OSS entity attached — while simultaneously giving the
RHOAI registry free governance primitives upstream. Double-edged:
consume the primitives, expect Databricks to steer the substrate.
Sources: [research/07-upstream](/features/agent-registry/research/07-upstream.md),
[research/08-landscape](/features/agent-registry/research/08-landscape.md).
