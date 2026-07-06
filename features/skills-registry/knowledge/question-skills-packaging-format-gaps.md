---
type: question
title: Skills packaging format — gaps beyond the Databricks MVP
description: Databricks' MVP settled on SKILL.md + YAML frontmatter as the skill packaging format, but OCI artifacts and other formats remain unaddressed.
status: open
timestamp: 2026-07-06
tags: [skills-registry, packaging, mlflow]
source: ai-asset-registry/docs/knowledge-registry.md §13 (as of 2026-07-05)
---
Partially answered: [ref-mlflow-skill-registry-mvp-branch.md](/features/skills-registry/knowledge/ref-mlflow-skill-registry-mvp-branch.md) confirms Databricks' MVP uses SKILL.md with YAML frontmatter as the canonical format, stored as directory artifacts via a hidden `_mlflow_skill_artifacts` system experiment. Still open: OCI artifacts and other packaging formats aren't addressed in the MVP, and no standard exists yet beyond this one prototype — a risk given multiple competing packaging approaches could emerge before one is standardized.
