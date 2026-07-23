---
type: fact
title: Skills Catalog -- overview and current status
description: Skills Catalog is the AI Hub storefront for AI agent skills (Kubeflow surface, alongside MCP/agent catalogs); direction established 2026-07-23, pre-partition.
timestamp: 2026-07-23
tags: [skills-catalog, overview, kubeflow, ai-hub]
features: [skills-catalog]
review_after: 2026-09-23
source: three intake meetings 2026-07-23 (AgentDev priority, Ramesh 1:1, Skills Registry/Catalog) + Aditi Saluja status doc
---

The Skills Catalog is the discovery and browsing layer for AI agent
skills in RHOAI, implemented as a Kubeflow hub surface in the AI Hub
dashboard -- the same pattern used for MCP servers, models, and agents.

**What it is**: a read-only, Git-backed storefront where platform
engineers and AI engineers browse, search, and acquire skills. Red Hat
and partner skills are pre-loaded at delivery time; cluster admins can
add organization-approved skills. Skills remain in Git repos; the
catalog indexes metadata and provides a searchable UI.

**Current status** (2026-07-23): direction established across three
meetings. RHAISTRAT-1780 (Skills Catalog: Discovery and Acquisition)
exists as a 3.6 candidate. No code yet -- estimated 6-9 sprints.

**Key links**:
- [RHOAI architecture repo](/features/platform/knowledge/ref-opendatahub-architecture-context-repo.md)
- [RHAISTRAT-1780 scope](/features/skills-catalog/knowledge/fact-skills-catalog-rhaistrat-1780-scope.md)
- [Skills Registry (sibling)](/features/skills-registry/)
- [NVIDIA skills repo](/features/skills-catalog/knowledge/ref-nvidia-skills-repo.md)
- [Competitive landscape](/features/skills-catalog/knowledge/fact-skills-competitive-landscape-2026.md)

**Relationship to Skills Registry**: catalog = marketplace/discovery
(Kubeflow); registry = workspace/governance (MLflow). Separate products
-- catalog ships first, registry integration follows. See
[decision-skills-catalog-registry-separation](/features/skills-catalog/knowledge/decision-skills-catalog-registry-separation.md).
