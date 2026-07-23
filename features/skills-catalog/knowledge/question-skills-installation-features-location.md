---
type: question
title: Where do skill installation features live -- catalog, registry, or both?
status: open
description: Open question needing its own STRAT -- skill installation could live in catalog (marketplace.json, npx), registry (APM, LOLA, mlflow CLI), or both. Different flows for catalog-sourced vs registry-sourced skills.
timestamp: 2026-07-23
tags: [skills-catalog, skills-registry, installation, packaging]
features: [skills-catalog, skills-registry]
source: Ramesh catalog-vs-registry GDoc TODO + Skills Registry/Catalog meeting 2026-07-23
---

From Ramesh's catalog-vs-registry document: "We need to do more work to
decide whether it's better for the Skills Catalog or the Skills Registry
to offer skill-installation features." Marked as a TODO needing its own
STRAT.

**Current plan distribution**:

| Method | Where | Status |
|---|---|---|
| marketplace.json | Catalog plan | Planned |
| npx | Catalog plan | Planned |
| APM | Registry plan (RFC-0008 plugin) | In RFC |
| LOLA | Registry plan (RFC-0008 plugin) | In RFC |
| Git pull from source repo | Not our responsibility | N/A |
| Git pull from RHOAI-managed source | Catalog plan | Planned |
| mlflow CLI (calls APM/LOLA) | Registry plan | In RFC |

**Complication**: if the catalog ships before the registry, catalog
needs its own install path. If both ship, users may need to install
from either source. Making skills always go through the registry before
install ("push to registry, then install from there") would unify the
path but adds friction.

Edson's comment: installation is orthogonal to governance needs.

Also feeds into how agent installation will happen.
