---
title: MLflow Skills Registry - Upstream Research
description: MLflow's current and planned work on skills, and Red Hat's opportunity to drive upstream design.
source: ai-asset-registry/skills/skills-registry/research/02-mlflow-upstream.md (as of 2026-07-05)
timestamp: 2026-07-06
review_after: 2026-08-05
---

# MLflow Skills Registry - Upstream Research

**Date**: 2026-04-15
**Author**: Peter Double (Principal PM - MCP)
**Purpose**: Document MLflow's current and planned work on skills, identify Red Hat's opportunity to drive upstream design.

---

## Executive Summary

**There is no dedicated "Skills Registry" in MLflow today.** The term "skills" in the MLflow ecosystem currently refers to two distinct things:

1. **Coding agent skills** (SKILL.md files that teach AI coding assistants how to use MLflow)
2. **An emerging proposal** to integrate the Agent Skills specification into MLflow's evaluation/judging framework

A community feature request for **version management of Agent Skills** exists but has no implementation. The April 2026 Databricks prototype target mentioned by Edson Tirelli is not visible in any public upstream activity — if it exists, it is happening internally.

---

## 1. Key GitHub Issues & PRs

### Issue #20435 - Version Management for Agent Skills
- **URL**: https://github.com/mlflow/mlflow/issues/20435
- **Date**: January 29, 2026 (OPEN)
- **Author**: KMichan (community)
- **Request**: Version control for Agent Skills similar to the Prompt Registry
- **Core ask**: "Manage and evaluate both Skills and Prompts within MLflow" as "a single source of truth for all GenAI assets"
- **Maintainer response (Feb 10)**: Corey Zumar (dbczumar, Databricks MLflow maintainer): *"I think this would be a nice extension to our Prompt Registry. Is this something you'd be able to share a brief design for? We'd love to support you in the process of delivering this."*
- **Significance**: This is the closest thing to an official signal that skills registry work could happen. The maintainer explicitly invited a design proposal — and no one has submitted one yet. **This is Red Hat's opportunity.**

### Issue #21255 - Agent Skills as Evaluation Criteria
- **URL**: https://github.com/mlflow/mlflow/issues/21255
- **Date**: March 2, 2026 (OPEN)
- **Author**: forrestmurray-db (Databricks)
- **Proposal**: Integrate SKILL.md files as composable evaluation criteria for LLM judges
- **Architecture**: SkillSet data model, tool-based progressive disclosure, serialization support
- **Open question #3**: *"Should skills be registerable with MLflow's tracking store? This would enable team-wide sharing and versioning via the registry."*
- **Out of Scope note**: *"Skills could become a specialized prompt type"* stored in the Prompt Registry
- **Significance**: Shows Databricks thinking about skills-in-registry but explicitly punting it to future work

### PR #21725 - Skills Evaluation Implementation (Phase 1)
- **URL**: https://github.com/mlflow/mlflow/pull/21725
- **Date**: March 16, 2026 (OPEN, under review)
- **Implements**: Phase 1 of #21255
- **Adds**: `mlflow/genai/skills/` module with Skill and SkillSet data model
- **New features**: `skills` parameter on `make_judge()`, two new judge tools (`read_skill`, `read_skill_reference`), model-family-aware prompt formatting
- **Assignees**: B-Step62 (Yuki Watanabe), dbczumar (Corey Zumar), daniellok-db (Daniel Lok)
- **Status**: Under review, Phase 1 only (evaluation use case, NOT registry)

### Issue #20450 - PR Template Skills Checkbox
- **URL**: https://github.com/mlflow/mlflow/issues/20450
- **Date**: January 30, 2026 (CLOSED)
- **Added**: PR template checkbox: "Does this PR require updating the MLflow Skills repository?"
- **Significance**: Skills are now a first-class concern in MLflow development process

---

## 2. MLflow Registry Architecture Pattern

The MLflow registry follows a consistent pattern that would extend to skills:

### Model Registry (Mature)
| Aspect | Detail |
|--------|--------|
| Entities | `RegisteredModel` -> `ModelVersion` (1:many) |
| Versioning | Auto-incrementing integer versions |
| Lifecycle | MLflow 3 moved from stages (None/Staging/Production/Archived) to **aliases** (mutable named references like "champion", "production") |
| Tags | Key-value metadata on both model and version levels |
| REST API | Full CRUD at `2.0/mlflow/registered-models/` and `2.0/mlflow/model-versions/` |
| Stores | Abstract store pattern with SqlAlchemy, file, and REST implementations |

### Prompt Registry (GA in MLflow 3)
| Aspect | Detail |
|--------|--------|
| Entities | `Prompt` (name, description, tags) -> `PromptVersion` (template, commit_message, tags, aliases) |
| Versioning | Auto-incrementing integers, immutable versions |
| Key design | Prompts stored as a specialized type of ModelVersion with special tags (`IS_PROMPT_TAG_KEY`, `PROMPT_TEXT_TAG_KEY`, `PROMPT_TYPE_TAG_KEY`) |
| APIs | `register_prompt()`, `load_prompt()`, `search_prompts()`, `set_prompt_alias()`, `set_prompt_tag()`, `set_prompt_version_tag()`, `set_prompt_model_config()` |
| URI scheme | `prompts:/name/version` or `prompts:/name@alias` |
| Caching | In-memory with configurable TTL (infinite for version-based, 60s for alias-based) |
| Proto | Dedicated `unity_catalog_prompt_service.proto` and `unity_catalog_prompt_messages.proto` |

### Predicted Skills Extension Pattern
Based on dbczumar's comment on #20435 and the "Out of Scope" section of #21255:
- Skills would likely become **a specialized Prompt type** (just as Prompts are a specialized ModelVersion type)
- Same versioning, aliasing, tagging patterns would apply
- URI scheme would likely be `skills:/name/version` or `skills:/name@alias`
- APIs would mirror: `register_skill()`, `load_skill()`, `search_skills()`, etc.

---

## 3. The mlflow/skills Repository

**URL**: https://github.com/mlflow/skills (Created January 14, 2026)

This is a **coding agent skills** repository, NOT a skills registry. It contains SKILL.md-format files that teach coding agents (Claude Code, Cursor, Codex) how to use MLflow.

**Skills include**: instrumenting-with-mlflow-tracing, analyze-mlflow-trace, agent-evaluation, querying-mlflow-metrics, etc.

**Installation**: `npx skills add mlflow/skills` or git clone

**Key insight**: The mlflow/skills repo demonstrates that MLflow's team is familiar with the SKILL.md format and uses it internally. This creates natural alignment for a registry that governs SKILL.md-formatted skills.

### databricks/databricks-agent-skills
**URL**: https://github.com/databricks/databricks-agent-skills (Created January 14, 2026 — same day as mlflow/skills)

Contains SKILL.md files for Databricks development. These are also coding agent skills, not a registry product.

---

## 4. Databricks Context

### Unity Catalog & AI Functions
- Unity Catalog governs AI assets (models, tables, files) but has **no dedicated "skills" asset type**
- UC Functions can be used as agent tools (SQL or Python functions with governance)
- Databricks recommends MCP servers over UC functions for most agent tool use cases
- The Mosaic AI Agent Framework integrates UC functions as tool sources

### No Public "Skills Registry" Product
- No Databricks blog, documentation, or announcement mentions a "Skills Registry" product
- Data + AI Summit 2025 announcements covered Unity Catalog enhancements but not skills
- Databricks' approach to agent tools is through UC Functions governance, not a skills-specific registry

### Databricks Prototype (from Meeting Transcripts)
From the 2026-04-07 AI Asset Registries Sync meeting, Edson Tirelli and Matt Prahl discussed:
- Databricks/MLflow maintainers are building a skills catalog/registry experience in MLflow
- Targeting end of April 2026 for delivery; prototype already exists and can be run locally
- Stores markdown files as artifacts, piggybacking on MLflow's existing artifact capabilities (S3 or PVC)
- The experience should be equivalent to "npm install" with a lock file and specific versions
- Matt Prahl has been providing Red Hat requirements to Databricks via Slack
- Edson qualified: *"I don't know if that is going to happen"* — suggesting the timeline is uncertain

### Databricks MVP Discovered (2026-04-16)

**The prototype is now visible publicly** at [B-Step62/mlflow, branch `skill-registry-mvp`](https://github.com/B-Step62/mlflow/tree/skill-registry-mvp).

**Author**: Yuki Watanabe (B-Step62) — the same Databricks engineer leading PR #21725 (Skills Evaluation Phase 1). This confirms B-Step62 is the primary Databricks engineer for all skills work.

**Architecture — Key Findings**:

1. **Dedicated entity type chosen** (not tag-based ModelVersion specialization):
   - 5 new database tables: `registered_skills`, `skill_versions`, `skill_version_tags`, `skill_tags`, `skill_aliases`
   - Dedicated entity classes: `Skill`, `SkillVersion`, `SkillAlias`
   - This is the cleaner approach Red Hat's upstream proposal advocated for in Section 4 of this document

2. **SKILL.md as canonical skill format**:
   - Skills identified by SKILL.md files with YAML frontmatter (`name`, `description`)
   - `manifest_content` field stores full SKILL.md text on each version
   - Name validation regex: `^[a-zA-Z0-9_.-]+$`

3. **Full CRUD implementation**:
   - REST API at `/ajax-api/3.0/mlflow/skills/` (newer API version than Model Registry's `2.0/`)
   - SDK under `mlflow.genai`: `register_skill()`, `load_skill()`, `preview_skills()`, `search_skills()`, `install_skill()`, plus tag/alias management
   - CLI: `mlflow skills register|list|load|show`

4. **Data Model** (detailed):
   - `Skill`: name (PK), description, creation_timestamp, last_updated_timestamp, latest_version (computed), aliases
   - `SkillVersion`: (name, version) composite PK, source (GitHub URL or local path), description, manifest_content, artifact_location, creation_timestamp, tags, aliases, created_by
   - System tags: `mlflow.skill.commit_hash`, `mlflow.skill.artifact_location`
   - Artifact storage: `mlflow-artifacts:/skills/{name}/{version}/` — supports S3, GCS, Azure, local

5. **Registration flow**:
   - Accepts GitHub URL (downloads tarball via API, extracts commit hash) or local directory path
   - Recursively searches for SKILL.md files
   - Supports bulk registration from a single source (e.g., a repo with multiple skills)
   - Auto-increments version per skill

6. **Claude Code integration**:
   - `install_skill()` copies artifacts to `~/.claude/skills/{name}/` (global) or `.claude/skills/{name}/` (project)
   - Writes `.mlflow_skill_info` JSON sidecar (version, source, commit_hash, tracking_uri, installed_at)
   - Tracing integration enriches `tool_Skill` spans with skill metadata from sidecar
   - Usage analytics extracted from span names: `tool_Skill:{skillName}`

7. **UI** (React/TypeScript):
   - List page: search, collapsible skill groups, usage breakdown chart (stacked bar, 24h/7d/30d), register modal, bulk selection
   - Detail page: version table, rendered SKILL.md preview, file browser, tag/alias management, usage tab

**What the MVP does NOT include** (confirms scope for Red Hat's governance extensions):
- No lifecycle states (no Draft/Published/Deprecated enum on SkillVersion)
- No approval workflows or review gates
- No verification or certification status tracking
- No trust tiers or security scanning
- No formal dependency model (no EntityAssociation-style relationships)
- No workspace-scoped RBAC beyond implicit workspace boundary
- No URI scheme (`skills:/name/version`) — uses `name/version` or `name@alias` string references instead

**Alignment with Red Hat's Upstream Proposal**:

| Aspect | Red Hat Proposal | Databricks MVP | Alignment |
|--------|-----------------|----------------|-----------|
| Entity type | Dedicated (preferred) or ModelVersion (fallback) | **Dedicated** | ✅ Aligned — our preferred approach |
| Versioning | Auto-incrementing integers | Auto-incrementing integers | ✅ Aligned |
| Aliases | Named references (production, staging) | Named references (champion, prod) | ✅ Aligned |
| Tags | Key-value on skill and version | Key-value on both skill and version (skill_tags table added via separate migration) | ✅ Aligned |
| Artifact storage | Opaque, packaging-agnostic | Directory artifacts in MLflow artifact store | ✅ Aligned |
| Publish state | Draft / Published / Deprecated | **Not implemented** | ❌ Gap — Red Hat should propose |
| Source provenance | Git repo, URL | GitHub URL with commit hash auto-extraction | ✅ Aligned (MVP is richer) |
| API pattern | `register_skill()`, `load_skill()`, `search_skills()` | Same function names under `mlflow.genai` | ✅ Aligned |
| REST API path | `2.0/mlflow/skills/` | `ajax-api/3.0/mlflow/skills/` | ⚠️ Different base path |
| URI scheme | `skills:/name/version`, `skills:/name@alias` | Not implemented | ❌ Gap — Red Hat should propose |
| Claude Code integration | Not in proposal (downstream) | First-class with sidecar + tracing | 🆕 Novel — not in our proposal |
| commit_message | On SkillVersion | Not in MVP (description instead) | ⚠️ Minor gap |
| Workspace scope | Explicit requirement | Implicit (no workspace field visible) | ⚠️ Unclear |

**Strategic Implications**:

1. **Our core architecture bet was right**: Dedicated entity type validates our recommendation. We don't need to argue for this anymore.
2. **Our proposal adds governance value the MVP lacks**: publish_state, skill-level tags, URI scheme, commit_message are all features we can contribute upstream.
3. **New coordination target**: B-Step62 (Yuki Watanabe) is the key person, not just dbczumar. He is building both the evaluation (PR #21725) and registry (this MVP) capabilities.
4. **Claude Code integration is ahead of us**: The sidecar-based tracing approach is novel and well-designed. Our RHOAI skills strategy should account for this installation/tracing pattern.
5. **Risk update**: The prototype is well-built and production-ready-ish. The risk shifts from "will they build it?" to "when will it merge and will our requirements be included?"

---

## 5. Red Hat Contributors in MLflow

### Dan Kuc (GitHub: dkuc)
- Red Hat employee per GitHub profile
- Has forked both `mlflow/mlflow` and `kubeflow/model-registry`
- No public commits, issues, PRs, or comments in mlflow/mlflow as of today
- No visible involvement in skills-related discussions on GitHub

### Matt Prahl (GitHub: mprahl)
- Very active — 20+ PRs since Feb 2026
- Focus: workspace support, trace archival, labeling, UI (execution recovery, workspace navigation)
- No skills-specific PRs, but his workspace/registry work provides the infrastructure foundation

### Other Red Hat Contributors
- **pboyd**: 1 PR (dev tooling — uv support)

---

## 6. Related Upstream Work

### Kubeflow Hub Plugin Architecture
- **Issue**: https://github.com/kubeflow/model-registry/issues/2220
- Proposes a plugin-based catalog architecture supporting multiple asset types (models, MCP servers, datasets, prompt templates, agents)
- This is the Catalog-side architecture that would complement an MLflow-based Skills Registry
- Skills could be a plugin alongside models and MCP servers

---

## 7. Strategic Implications for RHOAI

### The Opportunity
1. **Issue #20435 is waiting for a design proposal.** Corey Zumar (Databricks maintainer) explicitly invited one in February. No one has submitted it. Red Hat could own the skills registry design upstream.

2. **The likely implementation path is clear**: Skills as a specialized entity type within the existing registry infrastructure, following the Prompt Registry pattern.

3. **Red Hat has the people positioned**: Dan Kuc on MLflow/registry, Matt Prahl actively contributing infrastructure, Edson Tirelli as the liaison with Databricks.

4. **RHOAI adds what MLflow won't**: Enterprise governance (lifecycle states, approval workflows, certification, trust tiers, workspace-scoped RBAC) on top of MLflow's registry primitives. This is the same value-add pattern as MCP Registry.

### Risks
1. **Databricks may ship their prototype first** and establish the design direction before Red Hat can influence it. The end-of-April target is days away.

2. **The Prompt Registry pattern has tech debt**: Edson noted prompts are currently handled as "models with a special flag" — *"there is some tech debt in there on how they did that."* Skills should learn from this and have a cleaner architecture.

3. **The ~1 month design approval process** with Databricks means Red Hat needs to start the design proposal now to have any influence on the direction.

### Recommended Actions
1. **Submit a design proposal to MLflow issue #20435** for skills version management, incorporating Red Hat's governance requirements
2. **Coordinate with Edson Tirelli** on the Databricks prototype status and alignment
3. **Follow up with Matt Prahl** on Red Hat requirements already shared with Databricks via Slack
4. **Design RHOAI governance layer** that extends whatever MLflow primitive emerges (paralleling MCP Registry pattern)

---

## Key Links

| Resource | URL |
|----------|-----|
| **B-Step62/mlflow Skills Registry MVP** | https://github.com/B-Step62/mlflow/tree/skill-registry-mvp |
| MLflow Issue #20435 - Skills Version Management | https://github.com/mlflow/mlflow/issues/20435 |
| MLflow Issue #21255 - Skills as Evaluation Criteria | https://github.com/mlflow/mlflow/issues/21255 |
| MLflow PR #21725 - Skills Evaluation (Phase 1) | https://github.com/mlflow/mlflow/pull/21725 |
| mlflow/skills Repository | https://github.com/mlflow/skills |
| databricks/databricks-agent-skills | https://github.com/databricks/databricks-agent-skills |
| MLflow Prompt Registry Docs | https://mlflow.org/docs/latest/genai/prompt-registry/ |
| MLflow Model Registry Docs | https://mlflow.org/docs/latest/ml/model-registry/ |
| MLflow REST API | https://mlflow.org/docs/latest/rest-api.html |
| Databricks UC Functions as Agent Tools | https://docs.databricks.com/aws/en/generative-ai/agent-framework/create-custom-tool |
| Dan Kuc (dkuc) GitHub | https://github.com/dkuc |
| Kubeflow Hub Plugin Architecture (#2220) | https://github.com/kubeflow/model-registry/issues/2220 |
| MLflow Skills Blog (Self-Improving Agent Loop) | https://mlflow.org/blog/self-improving-agent-loop |
