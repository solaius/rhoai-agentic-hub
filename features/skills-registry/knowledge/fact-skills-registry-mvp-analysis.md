---
type: fact
title: Skills Registry MVP — data model, packaging, and gap analysis
description: The Databricks Skills Registry MVP's data model, installation modes, what it deliberately omits, and what that means for Red Hat's own upstream skills-registry proposal.
timestamp: 2026-07-06
tags: [skills-registry, mlflow, mvp, gap-analysis]
review_after: 2026-08-05
source: ai-asset-registry/docs/knowledge-registry.md §7 (as of 2026-07-05)
---
Discovered 2026-04-16 on [ref-mlflow-skill-registry-mvp-branch.md](/features/skills-registry/knowledge/ref-mlflow-skill-registry-mvp-branch.md) (Yuki Watanabe / B-Step62, Databricks) — an MVP prototype, not merged upstream, not announced publicly.

**Confirmed design decisions**: a dedicated entity type (not a specialized ModelVersion) — the same architecture Red Hat's own upstream proposal advocated for. SKILL.md (with YAML frontmatter) is the canonical format; the full manifest is stored on each version. Artifacts are packaging-agnostic, stored in MLflow's artifact repo at `mlflow-artifacts:/skills/{name}/{version}/` (S3/GCS/Azure/local). Versions auto-increment (same pattern as Model Registry/Prompt Registry). Aliases are named pointers (e.g. `copilot@champion → v3`).

**Data model**: `Skill` (name, description, timestamps, latest_version, aliases), `SkillVersion` (name, version, source, manifest_content, artifact_location, tags, aliases, created_by), `SkillAlias` (name, alias, version), and a `SkillTag` table added via a later migration for skill-level (not just version-level) key-value metadata.

**Interfaces**: REST under `/ajax-api/3.0/mlflow/skills/` (full CRUD); SDK under `mlflow.genai` (`register_skill`, `load_skill`, `preview_skills`, `search_skills`, `install_skill`, plus alias/tag setters); CLI under `mlflow skills` (`register`, `list`, `load`, `show`).

**Claude Code integration & multi-agent support**: `install_skill()` copies to `~/.claude/skills/{name}/` (global) or `.claude/skills/{name}/` (project), writing an `.mlflow_skill_info` JSON sidecar (version/source/commit_hash/tracking_uri/installed_at) that tracing then reads to enrich tool spans (`tool_Skill:{skillName}`) — links skill usage back to the registry with no runtime server dependency. Five agent platforms are supported with dedicated install paths (claude-code, cursor, copilot, gemini, codex), and three install modes: global (canonical dir + symlink), project-with-symlink (canonical dir + project symlink), project-with-copy (isolated copy) — trading disk usage against team-specific customization.

**What the MVP deliberately omits** (the gap Red Hat's governance layer fills): no lifecycle states beyond implicit (no Draft/Published/Deprecated), no approval workflows/certification/verification tracks, no trust tiers or security scanning, no formal dependency/relationship model, no workspace-scoped RBAC beyond the basic workspace boundary, no packaging-format validation.

**Implications for Red Hat**: our preferred dedicated-entity-type architecture was independently chosen, validating the upstream proposal's recommendation. Our proposal still adds real value — publish_state, governance tracks, and formal relationships are all still missing from the MVP. Risk is reduced (a well-architected prototype already exists) — the question shifts from "will they build it" to "how do we influence the design before merge." Yuki Watanabe (B-Step62) is the key Databricks engineer to align with (he also built the Skills Evaluation PR #21725). A gap analysis comparing Red Hat's proposed data model/API against this implementation is still needed to decide what to align with vs. propose as extensions.
