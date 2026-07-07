---
title: Skills Registry — Proposed Data Model
description: Proposed data model for the Skills Registry, mirroring the MCP Registry pattern of a minimal upstream model extended by an RHOAI governance layer.
source: ai-asset-registry/skills/skills-registry/strategy/data-model.md (as of 2026-07-05)
timestamp: 2026-07-06
review_after: 2026-08-05
---

# Skills Registry — Proposed Data Model

## Summary

This document proposes a data model for the Skills Registry, mirroring the MCP Registry data model pattern (logical asset + versioned record with separated governance tracks). The upstream (MLflow) model is intentionally minimal and packaging-agnostic. The RHOAI governance layer extends it with enterprise metadata.

This is a proposal for discussion — not a finalized design.

---

## Upstream Model (MLflow)

### Skill Entity

The logical governed asset, scoped to a workspace.

| Field | Type | Description |
|-------|------|-------------|
| `name` | string (required) | Unique skill identifier within workspace. Follows naming convention (lowercase, hyphens, max 64 chars) |
| `description` | string | Human-readable description of what the skill does |
| `tags` | key-value pairs | Freeform metadata for categorization, relationships, and filtering |
| `aliases` | string list | Mutable named references (e.g., "latest", "production", "recommended") |
| `creation_timestamp` | timestamp | When the skill was first registered |
| `last_updated_timestamp` | timestamp | When the skill was last modified |

### SkillVersion Entity

An immutable skill artifact plus mutable governance metadata. Each Skill can have multiple versions.

| Field | Type | Description |
|-------|------|-------------|
| `version` | integer (auto-incremented) | Version number |
| `skill_artifact` | artifact reference | Opaque reference to the skill payload stored in MLflow artifact store (S3, PVC, etc.). Content is immutable once registered. |
| `commit_message` | string | Description of what changed in this version |
| `publish_state` | enum | Draft / Published / Deprecated |
| `tags` | key-value pairs | Version-specific metadata |
| `aliases` | string list | Version-specific named references |
| `creation_timestamp` | timestamp | When this version was created |
| `source` | string | Optional provenance — git repo, registry URL, etc. |

### Design Principles (Upstream)

1. **`skill_artifact` is opaque**: MLflow stores whatever artifact is provided — markdown file, directory, archive, OCI reference. The registry does not interpret or validate the content. This is packaging-agnostic by design.

2. **Follows the Prompt Registry pattern**: Just as prompts are stored with a template and metadata, skills are stored with an artifact and metadata. The API surface mirrors `register_prompt()` / `load_prompt()`.

3. **Tags for relationships**: Dependencies on MCP servers, models, prompts, or other skills are expressed via tags (e.g., `depends_on_mcp: email-tools-server`). No formal relationship enforcement.

4. **Aliases for lifecycle**: Instead of complex lifecycle states in the upstream model, aliases (e.g., "production", "staging") provide flexible lifecycle management that aligns with MLflow 3's model registry approach.

5. **Workspace-scoped**: All skills are scoped to a workspace for visibility boundaries.

### Predicted API Surface

Following the Prompt Registry pattern:

| Operation | Endpoint Pattern | Description |
|-----------|-----------------|-------------|
| Register | `register_skill(name, artifact, ...)` | Create a new skill or new version |
| Load | `load_skill(name, version)` | Retrieve skill artifact and metadata |
| Search | `search_skills(filter, ...)` | List skills with filtering |
| Set alias | `set_skill_alias(name, alias, version)` | Set a named reference |
| Set tag | `set_skill_tag(name, key, value)` | Set metadata on skill |
| Set version tag | `set_skill_version_tag(name, version, key, value)` | Set metadata on version |
| Delete | `delete_skill(name)` | Remove a skill |

URI scheme: `skills:/name/version` or `skills:/name@alias`

---

## RHOAI Governance Extension

RHOAI extends the upstream model with enterprise governance metadata. This metadata lives in the RHOAI governance layer, not in MLflow core.

### Governance Tracks

Four independent status tracks, mirroring MCP Registry:

| Track | States | Purpose |
|-------|--------|---------|
| **Lifecycle State** | Draft → Candidate → Published → Deprecated → Retired | Progression state of the version |
| **Approval Status** | Draft → Pending → Approved → Rejected → Revoked | Authorization/governance decision |
| **Verification Status** | Unverified → Verified | Testing/evaluation results |
| **Certification Status** | None → Candidate → Certified → Expired → Revoked | Certification program compliance |

**Governance invariants**:
- `lifecycle_state=PUBLISHED` requires `approval_status=APPROVED`
- `approval_status=REJECTED` or `REVOKED` cannot coexist with `lifecycle_state=PUBLISHED`

### Extended Metadata (RHOAI-Only)

These fields are managed by the RHOAI governance layer, stored as structured tags or in a RHOAI-specific metadata extension:

| Field | Type | Description |
|-------|------|-------------|
| `trust_tier` | enum | Red Hat / Partner / Community / Unverified |
| `packaging_type` | string | How the skill is packaged — skill-md, oci-artifact, mcp-server, cli-tool, python-package, etc. |
| `consumption_model` | enum | Client-side / Server-side / Both |
| `security_scan_status` | enum | None / Pending / Passed / Failed |
| `security_scan_date` | timestamp | Last security scan |
| `provider` | string | Organization that created/maintains the skill |
| `license` | string | SPDX license identifier |
| `framework_compatibility` | string list | Compatible agent frameworks (e.g., claude-code, langchain, crewai, semantic-kernel) |

### Relationship Metadata (Phase 1 — Tags)

In Phase 1, relationships are expressed as tags on SkillVersion:

| Tag Key | Example Value | Description |
|---------|--------------|-------------|
| `depends_on_mcp` | `email-tools-server` | MCP server dependency |
| `depends_on_model` | `text-generation` | Model dependency |
| `depends_on_skill` | `identity-provider` | Skill dependency |
| `depends_on_prompt` | `email-template-v2` | Prompt dependency |
| `framework` | `claude-code` | Target framework |
| `category` | `communication` | Functional category |

### Relationship Model (Phase 2 — Entity Associations)

In Phase 2, formal entity associations replace tags for dependency tracking:

```
SkillAssociation {
  source_skill: string       # Skill name
  source_version: integer    # Skill version
  target_type: enum          # mcp-server, model, skill, prompt
  target_name: string        # Target asset name
  target_version_constraint: string  # SemVer range (e.g., ">=1.0.0, <2.0.0")
  association_type: enum     # depends_on, recommends, replaces, conflicts_with
}
```

The registry can validate:
- Referenced assets exist
- Referenced assets are in compatible lifecycle states
- Version constraints are satisfiable
- No circular dependencies

---

## Data Model Comparison

| Aspect | MCP Registry | Skills Registry | Difference |
|--------|-------------|-----------------|------------|
| Logical entity | MCPServer | Skill | Same pattern |
| Versioned entity | MCPServerVersion | SkillVersion | Same pattern |
| Immutable payload | `server_json` (MCP server definition) | `skill_artifact` (opaque artifact reference) | Skills are packaging-agnostic |
| Governance tracks | 4 (lifecycle, approval, verification, certification) | Same 4 | Identical |
| Deployment reference | `is_deployed` boolean, endpoint refs | **None** — skills are not deployed | Key difference |
| Gateway relevance | Yes — gateway reads registry metadata | **None** — skills don't route through gateway | Key difference |
| Consumption model | N/A (gateway-mediated) | Client-side / Server-side | Skills-specific |
| Packaging type | Implicit (MCP server = container or remote endpoint) | Explicit metadata field (skill-md, oci, mcp, cli, python) | Skills need this |
| Framework compatibility | N/A | Explicit metadata field | Skills-specific |

---

## Mapping to MLflow Internals

Based on how MLflow Prompt Registry is implemented (prompts as specialized ModelVersions):

| MLflow Concept | Skills Mapping |
|----------------|---------------|
| RegisteredModel | Skill (with `IS_SKILL_TAG_KEY` tag) |
| ModelVersion | SkillVersion (with skill-specific tags) |
| Artifact store | Skill artifact storage (S3, PVC, etc.) |
| Aliases | Skill aliases (production, staging, etc.) |
| Tags | Skill metadata (governance, relationships, packaging) |
| URI scheme | `skills:/name/version` or `skills:/name@alias` |

This approach minimizes the upstream changes required — skills can potentially be implemented as a specialized type on the existing entity infrastructure, just as prompts were.

### Risk: Prompt Registry Tech Debt

Edson Tirelli noted that prompts are currently handled as "models with a special flag" and there is "some tech debt in there." The skills implementation should aim for a cleaner separation than prompts achieved. If possible, advocate for a proper skills entity type rather than another tag-based specialization of ModelVersion.

---

## Databricks MVP Comparison (discovered 2026-04-16)

The Databricks MVP prototype ([B-Step62/mlflow, branch skill-registry-mvp](https://github.com/B-Step62/mlflow/tree/skill-registry-mvp)) reveals the actual implementation choices. Key comparison with our proposal:

| Aspect | Our Proposal | Databricks MVP | Action |
|--------|-------------|----------------|--------|
| Entity type | Dedicated (preferred) | **Dedicated** — own tables | ✅ Validated — no change needed |
| Skill fields | name, description, tags, aliases, timestamps | name, description, timestamps, latest_version, aliases, **tags** (added via separate migration) | ✅ Aligned — skill-level tags now present |
| SkillVersion fields | version, skill_artifact, commit_message, publish_state, tags, aliases, timestamps, source | version, source, description, manifest_content, artifact_location, timestamps, tags, aliases, created_by (**no publish_state, no commit_message**) | Propose publish_state upstream |
| `manifest_content` | Not in our model | Stores full SKILL.md text on each version | Consider adopting — useful for preview without downloading artifacts |
| `created_by` | Not in our model | Username who registered the version | Consider adopting — useful for audit |
| Artifact handling | Opaque `skill_artifact` reference | Directory-based, artifact_location URI + system tag | Align with this approach |
| URI scheme | `skills:/name/version`, `skills:/name@alias` | Not implemented | Still propose upstream |
| Name validation | "lowercase, hyphens, max 64 chars" | Regex: `^[a-zA-Z0-9_.-]+$` (allows uppercase, dots, underscores) | Align with actual regex |

**Fields to add to our upstream proposal** (from MVP):
- `manifest_content` on SkillVersion — enables preview and search without downloading full artifacts
- `created_by` on SkillVersion — audit trail for who registered each version
- `latest_version` on Skill — computed field for convenience

**Fields to propose that MVP lacks** (our value-add):
- `publish_state` enum (Draft/Published/Deprecated) on SkillVersion
- URI scheme (`skills:/name/version`, `skills:/name@alias`)
- `commit_message` on SkillVersion (MVP uses `description` instead, which is different semantically)

**Multi-agent install support** (MVP includes, not in our proposal):
- Supports 5 agent platforms: claude-code, cursor, copilot, gemini, codex
- Three-mode installation: global (canonical + symlink), project symlink, project copy
- Artifact storage via hidden `_mlflow_skill_artifacts` system experiment

## Open Questions

1. ~~Should skills use a dedicated entity type in MLflow or follow the Prompt Registry pattern (specialized ModelVersion)?~~ **ANSWERED**: Databricks MVP uses a dedicated entity type with its own tables. This validates our recommendation.

2. ~~How should `skill_artifact` handle multi-file skills (e.g., SKILL.md + scripts/ + references/)?~~ **ANSWERED**: MVP stores skills as directory artifacts in MLflow's artifact store. The entire skill directory (SKILL.md + associated files) is uploaded as an artifact bundle.

3. Should `packaging_type` be part of the upstream model or RHOAI-only metadata? Having it upstream would help other consumers interpret the artifact, but Databricks may resist. (Still open — MVP does not include packaging_type.)

4. How does the `EntityAssociationType` work need to be coordinated across MCP and Skills registries? Both need formal relationships — should this be a shared capability? (Still open — MVP has no formal relationship model.)

5. **(New)** Should we adopt `manifest_content` as a first-class field in our model? The MVP stores the full SKILL.md text alongside the artifact — this enables preview and search without downloading. Our proposal currently treats the artifact as fully opaque.

6. **(New)** How should Red Hat's governance extensions (lifecycle, approval, verification, certification) layer onto the MVP's simpler model? Options: extend via tags (like our Phase 1 relationship model), extend via additional columns (requires upstream agreement), or maintain a separate RHOAI metadata sidecar.
