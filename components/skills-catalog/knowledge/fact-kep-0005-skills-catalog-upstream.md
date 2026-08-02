---
type: fact
title: KEP-0005 merged in kubeflow/hub -- skills catalog is the 4th catalog type
description: KEP-0005 (Skills Catalog) merged Jul 27-31 2026 in kubeflow/hub -- SKILL.md parser (SKC-104), OpenAPI spec + codegen (SKC-101), plugin scaffold (SKC-103) all landed; rareddy (Red Hat) authored; 32-task tracking issue #3014; git-skills-plugin source type, /api/skill_catalog/v1alpha1 API, 4-tier SkillTrustTier enum, lenient parser (warns on unknown fields, loads anyway).
timestamp: 2026-08-02
tags: [skills-catalog, upstream, kubeflow, kep]
components: [skills-catalog]
review_after: 2026-10-02
source: https://github.com/kubeflow/hub/pull/2973, https://github.com/kubeflow/hub/pull/3015, https://github.com/kubeflow/hub/pull/3040, https://github.com/kubeflow/hub/pull/3041, https://github.com/kubeflow/hub/issues/3014
---

KEP-0005 (Skills Catalog) merged in kubeflow/hub, Jul 27-31 2026.
Red Hat's rareddy authored all four core PRs. Skills is the 4th catalog
type alongside model, MCP server, and agent.

Key implementation details:
- **Source type**: `git-skills-plugin` (reads SKILL.md from Git repos)
- **API base**: `/api/skill_catalog/v1alpha1`
- **Trust tiers**: platformProvided, partnerVerified, organizationApproved,
  communityContributed (labels, not enforced at API level)
- **Identity**: `(repository, path)` + version from git refs
- **Parser**: lenient -- missing description skips skill, name mismatches
  warn but load, unknown fields (like EX's `model`/`color`) ignored
- **No artifact entities** -- skills have no downloadable weights, only
  SKILL.md body stored as `readme`
- **Endpoints**: list, get, filter_options, plus
  `/claude/marketplace.json` per-consumer namespace

Tracking issue #3014 has 32 tasks for full implementation.

This changes the "no upstream skills catalog exists" finding from
01-upstream: the first-mover opportunity has been seized by Red Hat.
