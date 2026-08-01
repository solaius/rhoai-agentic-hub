---
title: Skills Registry — User Stories
description: User stories for the Skills Registry in RHOAI, organized by scope.
source: ai-asset-registry/skills/skills-registry/strategy/user-stories.md (as of 2026-07-05)
timestamp: 2026-07-06
review_after: 2026-08-05
---

# Skills Registry — User Stories

## Purpose

This document defines user stories for the Skills Registry in RHOAI. Stories are organized by scope:

- **Upstream stories** are suitable for the MLflow proposal — they describe registry primitives that MLflow should support.
- **RHOAI stories** describe enterprise governance, catalog integration, and consumption behaviors that RHOAI adds on top of MLflow.

The format and terminology mirror the [MCP Registry 3.5 DP User Stories](https://github.com/solaius/ai-asset-registry/blob/main/mcps/mcp-registry-3.5-user-stories.md) for consistency.

---

## Terminology

This document uses **publish state** instead of "approval" to describe how a skill record becomes eligible for downstream surfacing. This is intentional and matches the MCP Registry approach:

- **Publish state** describes a concrete lifecycle position — a skill record is either draft, published, or deprecated.
- **Approval** implies workflow scaffolding that is out of scope for the initial proposal.

---

## Actors

| Actor | Description |
|---|---|
| **Platform Engineer** | Sets up and maintains the AI platform. Registers, manages, and governs skill assets. |
| **AI Engineer** | Develops AI applications. Discovers and consumes governed skills for use in agents and workflows. |
| **Skill Author** | Creates and submits skills for registration (may be internal developer, partner, or community contributor). |
| **Catalog** (integration) | Discovery surface that reads registry state to present publishable skills. |
| **AAA / Studio** (integration) | Consumption surface that resolves published, scope-appropriate skills for AI engineers. |
| **Ingestion Pipeline** (integration) | Automated pipeline that validates, scans, and registers incoming skills. |

---

## Upstream Stories (MLflow Proposal)

These stories describe the registry primitives that MLflow should support. They are packaging-agnostic and governance-minimal — focused on registration, versioning, and lifecycle.

### Story U1 — Register a skill

**As a** Platform Engineer or Skill Author
**I want to** create a registry record for a skill with its associated artifact
**So that** the skill exists as a governed asset with stable identity, version, and metadata

**Acceptance notes**

- A skill record can be created with name, description, and a skill artifact
- The artifact is stored in MLflow's artifact store (S3, PVC, etc.) and is immutable once registered
- The record starts in draft publish state
- The artifact format is opaque — the registry does not interpret or validate the content
- Each registration creates a new auto-incremented version

**Upstream relevance**: Core registry write surface. Mirrors `register_prompt()`.

---

### Story U2 — Retrieve and list skills

**As a** Platform Engineer, AI Engineer, or integrating component
**I want to** retrieve a single skill record or list skill records
**So that** I can understand what skills exist, what state they are in, and what metadata they carry

**Acceptance notes**

- A single skill can be retrieved by name and version (or alias)
- Skills can be listed with basic filtering (by tag, publish state, name pattern)
- Returned data includes name, version, description, tags, aliases, publish state, and artifact reference
- Results are filtered by the caller's workspace scope

**Upstream relevance**: Core read surface. Mirrors `load_prompt()` and `search_prompts()`.

---

### Story U3 — Change publish state

**As a** Platform Engineer
**I want to** move a skill version between publish states: draft, published, or deprecated
**So that** the platform can distinguish between skills that are only recorded and skills that are eligible for downstream use

**Acceptance notes**

- Each skill version has a publish state
- A Platform Engineer can transition the publish state
- Only published skills are eligible for downstream surfacing
- Deprecated skills remain queryable but are no longer preferred for new use
- Publish state transitions are recorded for auditability

**Upstream relevance**: Lifecycle control. May be implemented via aliases (e.g., removing/adding a "published" alias) or via a dedicated publish state field.

---

### Story U4 — Set aliases on skill versions

**As a** Platform Engineer
**I want to** assign named aliases (e.g., "production", "recommended", "latest") to specific skill versions
**So that** consumers can reference skills by meaningful names rather than version numbers

**Acceptance notes**

- An alias is a mutable named reference that points to a specific version
- Multiple aliases can point to the same version
- Moving an alias to a different version is an atomic operation
- Consumers can resolve skills by alias: `skills:/email-assistant@production`

**Upstream relevance**: Mirrors MLflow 3's alias-based lifecycle model for models and prompts.

---

### Story U5 — Tag skills and skill versions

**As a** Platform Engineer or Skill Author
**I want to** attach key-value tags to skills and skill versions
**So that** skills carry metadata for categorization, relationships, and filtering

**Acceptance notes**

- Tags can be set on both the Skill entity and individual SkillVersions
- Tags are freeform key-value pairs
- Tags support relationship references (e.g., `depends_on_mcp: email-tools-server`)
- Tags support categorization (e.g., `category: communication`, `framework: claude-code`)
- Tags are searchable and filterable

**Upstream relevance**: MLflow's existing tag model. Used for loose relationship references (Phase 1).

---

### Story U6 — Preserve version history

**As a** Platform Engineer
**I want to** retain prior skill versions and their metadata
**So that** the platform preserves continuity and supports auditability

**Acceptance notes**

- Multiple versions of the same skill can exist in the registry
- Each version carries its own publish state, tags, and metadata
- Older versions remain queryable — deprecation does not erase history
- Version history shows progression and allows rollback

**Upstream relevance**: Core versioning. Same pattern as ModelVersion.

---

### Story U7 — Enforce scoped visibility

**As a** Platform Engineer or AI Engineer
**I want to** see only the skills appropriate to my workspace scope
**So that** governed skill visibility aligns with enterprise boundaries

**Acceptance notes**

- Registry reads are workspace-scoped
- Different users see different subsets of skills based on their workspace
- Scoped visibility applies to both management operations and consumption queries

**Upstream relevance**: Workspace scoping. Aligns with Matt Prahl's workspace support work in MLflow.

---

## RHOAI Stories (Downstream)

These stories describe enterprise governance, catalog integration, and consumption behaviors that RHOAI adds on top of the MLflow primitives.

### Story R1 — Surface published skills to the catalog

**As a** Catalog integration
**I want to** read only skill records that are published and eligible for surfacing
**So that** the catalog reflects governed registry state rather than maintaining its own governance truth

**Acceptance notes**

- The catalog can query skill records from the registry
- Only skills with published state and appropriate visibility scope are returned
- The catalog presents these records with trust tier information and categorization
- The catalog does not define its own separate governance state for skills

**Cross-component implication**: Registry is governance source of truth; catalog is discovery surface.

---

### Story R2 — Surface consumable skills to AAA / Studio

**As an** AAA or Studio integration
**I want to** resolve skills that are published and visible to the current scope
**So that** AI engineers can discover and attach governed skills to their agents

**Acceptance notes**

- AAA/Studio can query skill records from the registry (directly or via catalog)
- Returned skills are filtered by publish state and visibility scope
- Returned metadata includes artifact reference, tags, and trust information
- AI engineers can select skills and attach them to agents or workflows
- The consumption path supports both client-side (download artifact) and server-side (resolve endpoint reference) models

**Cross-component implication**: This is the end-to-end value demonstration — skills go from registry through catalog/AAA to agent consumption.

---

### Story R3 — Assign and display trust tiers

**As a** Platform Engineer
**I want to** assign trust tiers (Red Hat, Partner, Community, Unverified) to skill records
**So that** consumers can assess the provenance and trustworthiness of skills

**Acceptance notes**

- Each skill version has a trust tier assignment
- Trust tier is visible in catalog and AAA/Studio
- Trust tier influences default visibility (e.g., Unverified skills may be hidden by default)
- Trust tier can be changed as skills move through governance workflows

**Cross-component implication**: Catalog displays trust indicators. AAA/Studio may filter by trust tier.

---

### Story R4 — Track governance status (approval, verification, certification)

**As a** Platform Engineer
**I want to** track approval, verification, and certification status independently of publish state
**So that** governance decisions are auditable and multi-dimensional

**Acceptance notes**

- Approval status tracks authorization decisions (Draft → Pending → Approved → Rejected → Revoked)
- Verification status tracks testing/evaluation results (Unverified → Verified)
- Certification status tracks certification program compliance (None → Candidate → Certified → Expired → Revoked)
- These are independent of lifecycle state but subject to invariants (Published requires Approved)
- Status changes are recorded for auditability

**Cross-component implication**: Catalog and AAA/Studio can display governance status. Approval status gates publishing.

---

### Story R5 — Register skills from external sources

**As a** Platform Engineer
**I want to** register skills sourced from external registries, repositories, or marketplaces (ClawHub, Azure Skills, LangChain Hub, community repos)
**So that** externally sourced skills can be governed through the same platform experience

**Acceptance notes**

- A registry record can represent an externally sourced skill
- The record stores the external source reference (URL, registry, repo)
- External skills start as Unverified and can be promoted through governance
- The ingestion pipeline can scan and validate external skills before registration
- Internal and external skills use the same record structure

**Cross-component implication**: Connects RHAIRFE-1712 (Public Registry) with RHAIRFE-1713 (In-Cluster Registry).

---

### Story R6 — Ingest and validate skills

**As an** Ingestion Pipeline
**I want to** validate, scan, and register incoming skills automatically
**So that** skills entering the registry meet minimum quality and security standards

**Acceptance notes**

- Skills submitted for registration can be routed through an ingestion pipeline
- The pipeline validates format integrity and metadata completeness
- The pipeline performs security scanning (code scanning, dependency scanning, prompt injection detection)
- Successfully validated skills are registered as draft records
- Failed validation produces actionable error reports
- The pipeline is extensible for additional validation steps

**Cross-component implication**: Ingestion pipeline writes to registry. Platform Engineers review and publish.

---

### Story R7 — Track skill dependencies via tags

**As a** Platform Engineer or AI Engineer
**I want to** see what other assets a skill depends on (MCP servers, models, prompts, other skills)
**So that** I can understand the skill's requirements and assess compatibility

**Acceptance notes**

- Skills carry dependency information as tags (Phase 1)
- Tag keys follow a convention (e.g., `depends_on_mcp`, `depends_on_model`, `depends_on_skill`)
- Dependency tags are visible in catalog and AAA/Studio
- Dependencies are informational — not enforced by the registry in Phase 1
- Phase 2 will introduce formal entity associations with version constraints

**Cross-component implication**: Enables dependency-aware consumption and impact analysis.

---

### Story R8 — Filter skills by packaging type and framework compatibility

**As an** AI Engineer
**I want to** filter skills by their packaging type and compatible frameworks
**So that** I can find skills that work with my agent framework and consumption model

**Acceptance notes**

- Skills carry `packaging_type` metadata (skill-md, oci-artifact, mcp-server, cli-tool, python-package, etc.)
- Skills carry `framework_compatibility` metadata (claude-code, langchain, crewai, semantic-kernel, etc.)
- Catalog and AAA/Studio support filtering by these fields
- Skills may be compatible with multiple frameworks

**Cross-component implication**: Directly impacts AI Engineer experience in catalog and Studio.

---

## Story Summary

### Upstream (MLflow Proposal)

| Story | Capability | MCP Equivalent |
|-------|-----------|----------------|
| U1 | Register a skill | Story 1 (Register internal MCP) |
| U2 | Retrieve and list skills | Story 3 (Retrieve and list MCP records) |
| U3 | Change publish state | Story 4 (Change publish state) |
| U4 | Set aliases | N/A (new for skills, but matches MLflow 3 pattern) |
| U5 | Tag skills | Implicit in MCP stories |
| U6 | Preserve version history | Story 10 (Version history and deprecation) |
| U7 | Enforce scoped visibility | Story 9 (Enforce scoped visibility) |

### RHOAI (Downstream)

| Story | Capability | MCP Equivalent |
|-------|-----------|----------------|
| R1 | Surface to catalog | Story 5 (Surface to catalog) |
| R2 | Surface to AAA/Studio | Story 8 (Surface consumable MCPs) |
| R3 | Trust tiers | N/A (new — MCP has this conceptually but not as a story) |
| R4 | Governance status tracking | N/A (out of scope for MCP 3.5) |
| R5 | Register from external sources | Story 2 (Register external MCP) |
| R6 | Ingest and validate | N/A (new — MCP pipeline is separate) |
| R7 | Track dependencies via tags | N/A (new — skills-specific) |
| R8 | Filter by packaging/framework | N/A (new — skills-specific) |

### Stories NOT applicable to skills (from MCP)

| MCP Story | Why it doesn't apply |
|-----------|---------------------|
| Story 6 (Deployment/runtime references) | Skills are not deployed as services |
| Story 7 (Gateway-relevant metadata) | Skills do not route through MCP Gateway |
