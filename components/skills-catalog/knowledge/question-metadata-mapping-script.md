---
type: question
title: Who builds the EX-to-catalog metadata mapping script and when?
status: open
description: The 8-stage EX onboarding pipeline needs a script to map SKILL.md frontmatter + collection.yaml to the Kubeflow hub YAML catalog source format -- mechanical work (5 gaps, 8 unmapped fields, all resolvable) but unowned and unscheduled; blocks 3.6 TP content delivery.
timestamp: 2026-08-02
tags: [skills-catalog, ex, onboarding, tooling, action-item]
components: [skills-catalog]
asks:
  - Peter Double (2026-08-02, research 09-requirements-refresh)
source: research 09-requirements-refresh §1-2
---

The EX-to-RHOAI onboarding pipeline (Stage 2) requires a script that
reads SKILL.md frontmatter + collection.yaml and produces Kubeflow hub
YAML catalog source entries. The mapping is mechanical:

- 6 fields map directly (name, description, license, allowed-tools,
  body → readme, provider)
- 5 catalog fields need build-time assignment (source_id, trustTier,
  version, resolvedCommit, compatibility)
- 8 EX-only fields map to customProperties (model, color,
  user_invocable, maturity, personas, marketplaces, support_level,
  sample_workflows)

Estimated effort: days, not sprints. But it is unowned and unscheduled.
Without it, EX skills cannot enter the catalog for 3.6 TP.

**Open questions**:
- Who builds it -- RHOAI catalog team (rareddy) or Peter?
- Where does it live -- in the agentic-collections repo, in kubeflow/hub,
  or as a standalone script?
- Does it run once (manual) or as a CI step (automated rebuild)?

**Related**: [fact-ex-onboarding-36-viable-without-konflux](/components/skills-catalog/knowledge/fact-ex-onboarding-36-viable-without-konflux.md),
[fact-kep-0005-skills-catalog-upstream](/components/skills-catalog/knowledge/fact-kep-0005-skills-catalog-upstream.md)
