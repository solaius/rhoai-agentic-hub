---
type: fact
title: Ramesh's position -- skills need no governance; governance at agent level
description: Ramesh argues skills are static resources with no behavior/deployment, needing no governance layer; governance belongs at agent create/deploy/execute level; registry value is lower than catalog value for skills specifically.
timestamp: 2026-07-23
tags: [skills-registry, skills-catalog, governance, architecture]
features: [skills-registry, skills-catalog]
review_after: 2026-09-23
source: Ramesh/Peter 1:1 transcript + Ramesh catalog-vs-registry GDoc
---

Ramesh Reddy's position on skills governance, articulated in both the
1:1 with Peter and the catalog-vs-registry GDoc:

**Core argument**: "Skills are static resources -- they don't have any
behavior on their own. There is no deployment or none of it, so they
shouldn't require a governance aspect. The governance aspect comes in
terms of the agents: 'agent, you can't use this skill' or 'this agent
is using XYZ skills.' Those are agent-specific governance, not
skill-specific."

**Consequence**: the skills registry RFC has "less value" because it
cannot ship, rebuild, or distribute skills. The catalog already handles
discovery and browsing. Governance metadata beyond Approved/Deprecated
is an open question -- "until there is a customer use case on how this
can be defined, it is an open question."

**Counterpoints** (from the meeting and GDoc):
- Bill raised consistency concern with other asset registry pairs
- Ann Marie and Bill still want the registry for lifecycle, versioning,
  and observability tracing
- Edson: the registry handles modifications, new versions, and
  deployment-from -- things the catalog cannot
- Agreement: both are needed, but catalog delivers faster value

**Position classification**: this is a **reprioritization**, not a
cancellation of the skills registry.
