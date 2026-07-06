---
type: reference
title: "B-Step62/mlflow (branch: skill-registry-mvp)"
description: Databricks' Skills Registry MVP prototype — full CRUD, CLI, UI, and Claude Code integration. Not merged upstream.
resource: https://github.com/B-Step62/mlflow
tags: [skills-registry, mlflow, prototype, github]
timestamp: 2026-07-06
source: ai-asset-registry/docs/knowledge-registry.md §12 (as of 2026-07-05)
review_after: 2026-08-05
---
Author: Yuki Watanabe (B-Step62). Dedicated entity type (Skill/SkillVersion) across 4 DB tables, REST API (`/ajax-api/3.0/mlflow/skills/`), CLI (`mlflow skills`), SDK (`mlflow.genai`), Claude Code integration (`.mlflow_skill_info` sidecar), and a list/detail UI with usage analytics. Not merged upstream — the most concrete prototype evidence for how a skills registry could actually work; relevant to Red Hat's own upstream skills-registry proposal (RHAIRFE-1712/1713). Lives on the `skill-registry-mvp` branch, not `main` — the canonical repo URI above doesn't carry branch info.
