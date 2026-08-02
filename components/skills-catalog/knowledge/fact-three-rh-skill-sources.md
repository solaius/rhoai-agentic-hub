---
type: fact
title: Three independent Red Hat skill sources exist with no consolidation
description: Three RH orgs produce skills independently -- EX agentic-plugins (7 packs, ~68 skills), openshift/agentic-skills (Lightspeed-tied, 3 skills), opendatahub-io/ai-helpers (ODH Claude Code marketplace); Kubeflow hub can federate all three via separate source configs but no one owns the consolidation.
timestamp: 2026-08-02
tags: [skills-catalog, fragmentation, coordination]
components: [skills-catalog, skills-registry]
review_after: 2026-10-02
source: research 08-upstream-refresh
---

Three independent Red Hat skill sources exist:

| Source | Org | Skills | Format | Distribution |
|---|---|---|---|---|
| RHEcosystemAppEng/agentic-plugins | EX (Ecosystem Engineering) | ~68 (7 packs) | SKILL.md + collection.yaml | catalog.redhat.com/en/ai, Lola marketplace, bootstrap prompt |
| openshift/agentic-skills | Lightspeed | 3 (cluster-update, documentation, find-token) | Container image | Ships with Lightspeed |
| opendatahub-io/ai-helpers | ODH | Varies | SKILL.md + categories.yaml | Claude Code marketplace plugin |

No coordination mechanism exists. The Kubeflow hub catalog can federate
all three by configuring separate `git-skills-plugin` source entries in
`catalog-sources.yaml`, but someone needs to own:
- Which source configs exist
- Deduplication (if a skill appears in multiple sources)
- Trust tier assignment per source
- Update cadence synchronization

This is a coordination problem, not a technical problem.
