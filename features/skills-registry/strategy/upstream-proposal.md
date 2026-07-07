---
title: Skills Registry — Upstream MLflow Proposal
description: Proposal for adding Skills Registry support to MLflow -- requirements, user stories, and a proposed data model for governing skills alongside models and prompts.
source: ai-asset-registry/skills/skills-registry/strategy/upstream-proposal.md (as of 2026-07-05)
timestamp: 2026-07-06
review_after: 2026-08-05
---

# Skills Registry — Upstream MLflow Proposal

## Purpose

This document is a proposal for adding Skills Registry support to MLflow. It defines requirements, user stories, and a proposed data model for governing AI skills as first-class assets alongside models and prompts.

This is intended for submission to the MLflow community (GitHub issue [#20435](https://github.com/mlflow/mlflow/issues/20435)) and for coordination with Databricks on the skills registry design direction.

---

## Motivation

AI skills are becoming a critical component of agent-based AI systems. Agents consume skills — reusable capabilities backed by tools, templates, scripts, and configurations — to perform tasks. As enterprises deploy agents at scale, they need the same governance for skills that MLflow already provides for models and prompts: versioning, lifecycle management, and a centralized registry.

**Current state**:
- MLflow has a mature Model Registry and a Prompt Registry (GA in MLflow 3)
- Skills exist across frameworks (LangChain tools, Semantic Kernel plugins, Claude Code skills, CrewAI tools) with no standard registry
- MLflow issue [#20435](https://github.com/mlflow/mlflow/issues/20435) requests version management for Agent Skills
- MLflow PR [#21725](https://github.com/mlflow/mlflow/pull/21725) adds skills to the evaluation framework — but not to the registry
- The `mlflow/skills` repository uses SKILL.md format for coding agent skills, demonstrating MLflow's familiarity with the format

**Gap**: There is no way to register, version, discover, or lifecycle-manage skills within MLflow. Teams that use skills in their agents have no single source of truth for what skills exist, which versions are in use, or what state they are in.

---

## Requirements

### Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-1 | Register skills as named, versioned assets in a workspace | Must |
| FR-2 | Store skill artifacts (opaque — any format) in MLflow artifact store | Must |
| FR-3 | Auto-increment version numbers for each new registration | Must |
| FR-4 | Retrieve skills by name and version or by alias | Must |
| FR-5 | Search/list skills with filtering by tags and name pattern | Must |
| FR-6 | Set mutable aliases on skill versions (e.g., "production", "recommended") | Must |
| FR-7 | Set key-value tags on skills and skill versions | Must |
| FR-8 | Manage publish state (Draft / Published / Deprecated) per version | Must |
| FR-9 | Workspace-scoped visibility for all skill operations | Must |
| FR-10 | URI scheme for skill references (`skills:/name/version`, `skills:/name@alias`) | Should |
| FR-11 | Immutable skill artifacts (artifact content cannot change after registration) | Must |
| FR-12 | Delete skills and skill versions | Should |
| FR-13 | Record provenance (source reference — git repo, URL, etc.) | Should |

### Non-Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| NFR-1 | Packaging-agnostic — the registry does not interpret or validate artifact content | Must |
| NFR-2 | Consistent with Model Registry and Prompt Registry patterns | Must |
| NFR-3 | Python client SDK support (`mlflow.register_skill()`, `mlflow.load_skill()`, etc.) | Must |
| NFR-4 | REST API support | Must |
| NFR-5 | In-memory caching for loaded skills (configurable TTL) | Should |
| NFR-6 | Extensible via tags for downstream governance metadata | Must |

### Explicitly Out of Scope

These items are intentionally excluded from the upstream proposal. Downstream distributions (e.g., Red Hat OpenShift AI) may add them as governance extensions:

- Approval workflows, review gates, or policy enforcement
- Certification or verification status tracking
- Trust tiers or security scanning
- Skill dependency validation or enforcement
- Packaging format recommendations or validation
- Catalog or discovery UI
- Skill evaluation or testing frameworks
- Skill composition or chaining

---

## Proposed Data Model

### Skill

The logical skill asset, scoped to a workspace.

```
Skill {
  name: string              # Required. Unique within workspace.
  description: string       # Optional. What this skill does.
  tags: Dict[str, str]      # Optional. Key-value metadata.
  aliases: List[str]        # Mutable named references to versions.
  creation_timestamp: int   # Auto-set.
  last_updated_timestamp: int  # Auto-set.
}
```

### SkillVersion

An immutable skill artifact plus mutable metadata.

```
SkillVersion {
  version: int              # Auto-incremented.
  skill_artifact: ArtifactRef  # Immutable reference to stored artifact.
  commit_message: string    # Optional. What changed.
  publish_state: enum       # Draft | Published | Deprecated
  tags: Dict[str, str]      # Version-specific metadata.
  aliases: List[str]        # Version-specific named references.
  creation_timestamp: int   # Auto-set.
  source: string            # Optional. Provenance reference.
}
```

### Rationale for a Dedicated Entity Type

The Prompt Registry is currently implemented as a specialized ModelVersion with distinguishing tags. While pragmatic, this approach has acknowledged tech debt (model-prompt coupling, unclear separation).

For skills, we recommend a dedicated entity type rather than another tag-based specialization. Reasons:

1. **Skills carry artifacts, not templates**: Prompts are text templates. Skills are opaque artifacts (files, directories, archives). The storage and retrieval semantics differ.
2. **Skills have different lifecycle semantics**: Skills are consumed by agents at runtime, not interpolated into prompts. The usage patterns are distinct.
3. **Cleaner extension point**: A dedicated type provides a clean surface for downstream governance extensions without polluting the model or prompt namespaces.
4. **Evaluation integration**: PR #21725 already introduces a `mlflow/genai/skills/` module. A dedicated registry type aligns with this existing code structure.

If a dedicated type is not feasible in the initial implementation, the specialized ModelVersion approach with `IS_SKILL_TAG_KEY` is acceptable — but the API surface should abstract this implementation detail behind skill-specific functions.

---

## Proposed API Surface

### Python Client

```python
import mlflow

# Register a new skill (or new version of existing skill)
skill_version = mlflow.register_skill(
    name="email-assistant",
    artifact_path="/path/to/skill/directory",  # or file
    description="Email management capabilities for AI agents",
    commit_message="Added search inbox capability",
    tags={"category": "communication", "framework": "claude-code"},
    source="https://github.com/org/email-assistant"
)

# Load a skill by version
skill = mlflow.load_skill("email-assistant", version=3)

# Load a skill by alias
skill = mlflow.load_skill("email-assistant", alias="production")

# Load via URI
skill = mlflow.load_skill("skills:/email-assistant/3")
skill = mlflow.load_skill("skills:/email-assistant@production")

# Search skills
skills = mlflow.search_skills(
    filter_string="tags.category = 'communication'",
    max_results=50
)

# Set alias
mlflow.set_skill_alias("email-assistant", alias="production", version=3)

# Set tags
mlflow.set_skill_tag("email-assistant", key="category", value="communication")
mlflow.set_skill_version_tag("email-assistant", version=3, key="framework", value="claude-code")

# Delete
mlflow.delete_skill("email-assistant")
mlflow.delete_skill_version("email-assistant", version=1)
```

### REST API

Following existing MLflow conventions:

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `2.0/mlflow/skills/create` | Register a new skill |
| POST | `2.0/mlflow/skill-versions/create` | Create a new skill version |
| GET | `2.0/mlflow/skills/get` | Get skill by name |
| GET | `2.0/mlflow/skill-versions/get` | Get skill version |
| GET | `2.0/mlflow/skills/search` | Search skills |
| PATCH | `2.0/mlflow/skills/update` | Update skill metadata |
| PATCH | `2.0/mlflow/skill-versions/update` | Update version metadata (tags, publish state) |
| DELETE | `2.0/mlflow/skills/delete` | Delete a skill |
| DELETE | `2.0/mlflow/skill-versions/delete` | Delete a skill version |
| POST | `2.0/mlflow/skills/set-alias` | Set an alias on a version |
| DELETE | `2.0/mlflow/skills/delete-alias` | Remove an alias |
| POST | `2.0/mlflow/skills/set-tag` | Set a tag on a skill |
| POST | `2.0/mlflow/skill-versions/set-tag` | Set a tag on a version |

---

## User Stories

See the companion [User Stories document](user-stories.md) for detailed stories. The upstream stories are:

| Story | Summary |
|-------|---------|
| U1 | Register a skill with artifact |
| U2 | Retrieve and list skills |
| U3 | Change publish state |
| U4 | Set aliases on skill versions |
| U5 | Tag skills and skill versions |
| U6 | Preserve version history |
| U7 | Enforce scoped visibility |

---

## Integration with Existing MLflow Skills Work

### Evaluation Framework (PR #21725)
PR #21725 introduces a `Skill` and `SkillSet` model for evaluation judges. The registry proposal complements this by providing a persistent store for skills that the evaluation framework can reference:

```python
# Current (PR #21725): Skills loaded from files
skill = Skill.from_file("path/to/SKILL.md")

# With registry: Skills loaded from MLflow
skill = mlflow.load_skill("email-assistant@production")
scorer = make_judge(model="...", skills=[skill])
```

This connection is explicitly called out as an open question in PR #21725's issue (#21255, question #3): *"Should skills be registerable with MLflow's tracking store?"*

### mlflow/skills Repository
The `mlflow/skills` repo contains SKILL.md-format coding agent skills. The registry provides a natural home for these skills to be versioned and managed rather than relying solely on git-based versioning.

---

## Implementation Considerations

### Storage Backend
- **SqlAlchemy store**: New `skills` and `skill_versions` tables (or extended existing tables)
- **File store**: Skill metadata in JSON files, artifacts in artifact store
- **REST store**: Proxy to tracking server

### Artifact Storage
- Skill artifacts stored in the configured artifact store (S3, Azure Blob, GCS, local filesystem, etc.)
- Artifacts are directory-based (a skill may consist of multiple files)
- Immutability enforced at the API level — no updates to stored artifacts

### Protobuf
- New `skill_service.proto` and `skill_messages.proto` (following the prompt registry pattern)
- Or extension of existing service definitions

---

## Related Issues and PRs

| Reference | Description |
|-----------|-------------|
| [#20435](https://github.com/mlflow/mlflow/issues/20435) | Feature request: Version Management for Agent Skills |
| [#21255](https://github.com/mlflow/mlflow/issues/21255) | Feature request: Agent Skills as evaluation criteria |
| [#21725](https://github.com/mlflow/mlflow/pull/21725) | PR: Skills evaluation implementation (Phase 1) |
| [mlflow/skills](https://github.com/mlflow/skills) | Repository: Coding agent skills for MLflow |

---

## Databricks MVP Alignment (updated 2026-04-16)

The Databricks Skills Registry MVP prototype is now visible at [B-Step62/mlflow, branch `skill-registry-mvp`](https://github.com/B-Step62/mlflow/tree/skill-registry-mvp). This has significant implications for our upstream proposal.

### What the MVP validates in our proposal
- **Dedicated entity type** (our preferred approach) — confirmed
- **Auto-incrementing integer versions** — confirmed
- **Aliases** (named references to versions) — confirmed
- **Packaging-agnostic artifact storage** — confirmed
- **API pattern** (`register_skill()`, `load_skill()`, `search_skills()`) — confirmed

### What the MVP does NOT include that our proposal adds
These are the features Red Hat can contribute upstream:
- **`publish_state`** (Draft/Published/Deprecated) — our FR-8
- **Skill-level tags** — MVP only has version-level tags
- **URI scheme** (`skills:/name/version`) — our FR-10
- **`commit_message`** on SkillVersion — MVP uses `description` instead

### What the MVP includes that our proposal should adopt
- **`manifest_content`** field — stores full SKILL.md text on each version for preview/search
- **`created_by`** field — username who registered the version (audit trail)
- **`latest_version`** computed field on Skill — convenience for listing
- **GitHub-aware registration** — auto-downloads tarball and extracts commit hash
- **Claude Code integration** — `.mlflow_skill_info` sidecar for tracing linkage

### Revised Strategy
1. **Update this proposal** to adopt MVP patterns (manifest_content, created_by, registration flow) and position our additions (publish_state, skill-level tags, URI scheme) as complementary enhancements
2. **Engage B-Step62 (Yuki Watanabe) directly** — he is the primary builder, not just dbczumar
3. **Submit publish_state as a focused PR** — this is the highest-value addition with the lowest friction
4. **Defer governance extensions** to RHOAI layer — lifecycle, approval, verification, certification stay downstream

## Next Steps

1. ~~Seek community feedback on this proposal via GitHub issue #20435~~ → **Revised**: Engage B-Step62 directly on the MVP branch first, then align proposal with MVP before posting to #20435
2. Coordinate with Databricks maintainers (**B-Step62 is the primary target**, alongside dbczumar) on design direction
3. Align with PR #21725 authors on registry-evaluation integration
4. Update this proposal to adopt MVP patterns and position Red Hat's additions as complementary
5. Submit focused PRs following MLflow contribution process (small, focused, ~1 month design approval cycle)
6. Monitor the `skill-registry-mvp` branch for changes and potential merge to main
