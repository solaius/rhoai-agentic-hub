---
title: RHOAI Patterns & Meeting Insights for Skills Registry
description: MCP registry patterns applicable to skills, and skills-related discussion extracted from meeting transcripts.
source: ai-asset-registry/skills/skills-registry/research/04-rhoai-patterns-and-meetings.md (as of 2026-07-05)
timestamp: 2026-07-06
review_after: 2026-08-05
---

# RHOAI Patterns & Meeting Insights for Skills Registry

**Date**: 2026-04-15
**Author**: Peter Double (Principal PM - MCP)
**Purpose**: Extract MCP registry patterns applicable to skills and document all skills-related discussion from meeting transcripts.

---

## Part 1: MCP Patterns Applicable to Skills Registry

### 1.1 Data Model Pattern: Logical Asset + Versioned Record

The MCP Registry establishes a two-tier entity pattern directly reusable for skills:

| MCP Entity | Skills Equivalent | Purpose |
|------------|-------------------|---------|
| MCPServer | Skill | Logical governed asset, scoped to a workspace. Name, description, status, tags, aliases, audit fields |
| MCPServerVersion | SkillVersion | Immutable skill payload (e.g., `skill_md` or bundled artifact reference) plus mutable governance metadata |

The MCP registry design doc explicitly calls this out: *"This data model is MCP-specific, but the pattern (logical asset + versioned record, separated governance tracks, workspace scoping) could inform future data models for agents, skills, and other AI assets."*

**Key difference**: MCPServerVersion stores an immutable `server_json` payload. SkillVersion would store an immutable skill artifact reference — likely a markdown file, zip bundle, or OCI artifact URI.

### 1.2 Four Independent Governance Tracks

Instead of a single linear lifecycle, governance is separated into four independent tracks:

| Track | States | Applicability to Skills |
|-------|--------|------------------------|
| **Lifecycle State** | Draft -> Candidate -> Published -> Deprecated -> Retired | Directly applicable, unchanged |
| **Approval Status** | Draft -> Pending -> Approved -> Rejected -> Revoked | Directly applicable, unchanged |
| **Verification Status** | Unverified -> Verified | Applicable — skill testing/evaluation results |
| **Certification Status** | None -> Candidate -> Certified -> Expired -> Revoked | Applicable — Red Hat / partner certification |

**Invariant preserved**: `lifecycle_state=PUBLISHED` requires `approval_status=APPROVED`

### 1.3 Metadata-First Records

Registry stores metadata and references, NOT actual asset runtimes/payloads. Skills would similarly store references to skill content (markdown files, zip bundles, repo pointers, or OCI artifacts) rather than the skill code itself.

### 1.4 Workspace-Scoped Visibility

All registry records are scoped to a workspace for RBAC-aware access. Skills would need the same scoping for enterprise multi-tenancy.

### 1.5 Eight-Stage Generic Asset Flow

The generic lifecycle flow applies to skills with modifications:

| Stage | MCP Flow | Skills Equivalent | Key Difference |
|-------|----------|-------------------|----------------|
| 1. Ingress | MCP enters ecosystem | Skill enters (internal dev, community, partner) | Similar |
| 2. Validation | Security scanning, provenance | Security scanning of skill scripts/code | Skills contain executable code — different scanning needs |
| 3. Registration | Metadata-first registration in MLflow | Same | Same |
| 4. Governance | Lifecycle state management, approval | Same | Same |
| 5. Promotion | Dev registry to prod registry | Same | Same |
| 6. Deployment | Lifecycle Operator deploys MCPServer CRD | **No equivalent** — skills are not "deployed" | Fundamental difference |
| 7. Runtime | Gateway registration, ConfigMap | **No equivalent** — skills consumed directly | Fundamental difference |
| 8. Consumption | Available through AAA/Studio | Skills resolved and attached to agents | Different consumption model |

**Key insight**: Skills lack the deployment/runtime phase that makes MCP lifecycle complex. Steps 6-7 are fundamentally different — skills are consumed as files/bundles, not deployed as services.

### 1.6 Transferable User Stories (from MCP 3.5)

| MCP Story | Skills Equivalent | Transfers? |
|-----------|-------------------|------------|
| Story 1: Register an internal MCP server | Register an internally developed skill | Yes |
| Story 2: Register an external MCP server | Register an externally sourced skill | Yes |
| Story 3: Retrieve and list records | List and retrieve skill records | Yes |
| Story 4: Change publish state | Manage skill lifecycle states | Yes |
| Story 5: Surface to catalog | Surface published skills to catalog | Yes (if catalog exists) |
| Story 6: Deployment/runtime references | N/A | **No** — skills not deployed |
| Story 7: Gateway-relevant metadata | N/A | **No** — skills don't use gateway |
| Story 8: Surface to AAA/Studio | Resolve skills for AI engineer consumption | Yes |
| Story 9: Enforce scoped visibility | RBAC-scoped skill access | Yes |
| Story 10: Version history and deprecation | Track skill versions with deprecation | Yes |

**7 of 10 user stories transfer directly** — strong foundation for skills registry user stories.

### 1.7 Component Boundaries

| Component | MCP Role | Skills Equivalent |
|-----------|----------|-------------------|
| Registry (MLflow) | Governed identity, versioning, lifecycle | Same |
| Catalog (Kubeflow Hub) | Discovery and browsing | Unclear if needed (see debate below) |
| Lifecycle Operator | Deployment (MCPServer CRD) | **No direct equivalent** |
| Gateway | Runtime mediation | **No direct equivalent** |
| AAA/Studio | Consumption for AI engineers | Skill resolution and attachment to agents |

### 1.8 Trust Tiers

MCP catalog defines trust tiers that apply directly to skills:
- **Red Hat certified** — Red Hat-provided or fully certified skills
- **Partner** — Partner-provided skills with consent and maintenance commitment
- **Community** — Community-contributed skills with basic validation
- **Unverified** — External skills with no validation

### 1.9 "Store State vs. Automate Behavior" Principle

The 3.5 MCP approach stores governed state first, automates handoffs later. The same phased approach is appropriate for a skills registry MVP — start with registration, versioning, and lifecycle tracking; add automated promotion, evaluation, and policy enforcement later.

---

## Part 2: Skills Discussion from Meeting Transcripts

### 2.1 AI Asset Registries Sync (2026-04-07) — PRIMARY SOURCE

This is the richest source of skills discussion, with extensive dialogue between Peter Double, Ann Marie Fred, Edson Tirelli, Matt Prahl, Adam Bellusci, Adel Zaalouk, and Hunter Gerlach.

#### Databricks Skills Registry Prototype
- Databricks/MLflow maintainers are building a skills catalog/registry experience in MLflow
- Targeting end of April 2026 for delivery; prototype already exists and can be run locally
- Stores markdown files as artifacts, piggybacking on MLflow's existing artifact capabilities (S3 or PVC)
- The experience should be equivalent to "npm install" with a lock file and specific versions
- Matt Prahl has been providing Red Hat requirements to Databricks via Slack
- Edson qualified: *"I don't know if that is going to happen"* — uncertain timeline

#### Skills Packaging Debate
**The fundamental issue**: Ann Marie Fred: *"That's the fundamental issue — there is no good portable format for skills across agents yet."*

Key points from the debate:
- Skills are NOT container images — they are files or bundles of files (markdown, config, scripts)
- OCI artifacts considered "heavy for individual skills" (Hunter Gerlach)
- OCI artifacts described as "not consumable" for skills even if technically possible (Ann Marie Fred)
- MLflow is "not tied to a specific packaging format for artifacts" — downstream plugins can customize (Edson)
- Databricks prototype is simply storing markdown as MLflow artifacts
- Peter: skills are "more similar to a prompt than it would be to MCPs" — text files with config
- Adam: OCI layer being explored as storage layer for MLflow; could store skills as OCI artifacts for governance/signing but TBD
- Adel noted skills can have scripts as well, meaning scanning skills means also scanning code/scripts shipping with them
- Multiple competing skill distribution approaches: ClawHub, SkillNet, Azure Skills, OpenAI Skills API, Llama Stack skills API

**Tactical proposal (Ann Marie Fred)**: Start with an ODH repo for validated/scanned skills as Dev Preview, buy time for format to mature.

#### Registry vs. Catalog for Skills
- **Peter**: *"I saw the registry being important... I'm still interested though if people have ways in which the catalog would be very valuable for skills."* Skeptical about skills catalog value given volume and lack of optimization per use case.
- **Edson**: Governance and asset linking/versioning is key — *"the linking between the assets and the version of the skills... if the skill is depending on a particular version of tools"* — versioned dependency tracking is what makes registry essential
- **Adam**: Customers historically adopt catalogs first, registries second: *"I thought registries were the be all and end all. That has not proven to be the case."*
- **Hunter Gerlach** (Consulting): Real-world use case — consultants need trusted skill registries to scale: *"What would a trusted skills registry look like?"*

#### Two Skill Consumption Models
1. **Client-side**: Download skill code directly and use it in your agent (currently dominant)
2. **Server-side**: Server executes the skill for you via Responses API (emerging, more governable)

Ann Marie Fred: These two stories are "very disjoint right now."

#### Microsoft Interest
Peter noted: *"Microsoft yesterday was very interested in our future for skills"* and linked https://github.com/microsoft/azure-skills

### 2.2 Registry Proposal Discussion (2026-03-19)

Skills mentioned in context of prioritization:
- Peter: *"For three five, we're shooting to try to get not only the MCP registry out there but the agent registry and now the Skills Registry is on the table as well."*
- Peter on skills: *"There's no real deployment or anything to worry about... they're just the MD files. It's more of just a tracking system at that point of what's the version."*
- Adam: *"Skills was probably third on my list"* after MCP and agents
- Edson: Prompts are currently handled as "models with a special flag" in MLflow — *"there is some tech debt in there on how they did that"* — relevant because skills would follow a similar pattern
- Edson: Need focused design documents; Databricks process requires ~1 month per design approval
- Ann Marie Fred already "actively looking at skills" at the time of this meeting

### 2.3 Sharon/Peter 1:1 (2026-04-13)

Skills in context of AI Hub and registry strategy:
- Sharon: MCP servers are "the underlying building block" even as skills and plugins emerge: *"It's not like we miss the train and now everyone is speaking only about skills."*
- Peter: *"In three five, we're going to have agents, skills and MCPs in Kubeflow [for catalog]... the registry has the MCP registry in MLflow."*
- Peter: *"The three critical [AI assets] are agents, MCPs and skills"* — out of ~12 identified AI asset types
- Peter: Build toward the plugin architecture with MCPs, agents, and skills as the first three
- Sharon: *"It makes sense that MCP and skills and plugins will be the same... it's philosophical discussion."*

### 2.4 Agentic AI Pod v2 (2026-04-14)

No direct skills discussion. Meeting focused on IBM/Red Hat positioning for agentic AI and MCP catalog blog. Indirectly relevant: Red Hat "staying the course" on Agent Ops, MCP Gateway, evaluations/traces with MLflow.

### 2.5 MCP Pipeline w/ Gen MCP (2026-04-10)

No skills mentions. Focused on MCP server ingestion pipeline. However, the pipeline pattern (validate -> scan -> evaluate -> containerize -> registry) could inform a future skills ingestion pipeline with modified steps — particularly for skills that contain executable code.

---

## Part 3: Key Decisions and Open Questions

### Decided

| Decision | Source | Date |
|----------|--------|------|
| Skills registry backend is MLflow | Adam Bellusci | 2026-04-07 |
| Skills catalog backend is Kubeflow Hub | Same decision | 2026-04-07 |
| Skills are third priority after MCP and agents | Adam Bellusci | 2026-04-07 |
| MCPs, agents, and skills are the first three asset types for plugin architecture | Peter Double | 2026-04-13 |
| Databricks/MLflow building skills registry prototype | Edson Tirelli, Matt Prahl | 2026-04-07 |
| Skills are more like prompts than MCPs (file-based, no runtime deployment) | Peter Double | 2026-04-07 |

### Open Questions (as of 2026-04-15)

1. **Packaging format**: No standard exists. Options: plain markdown, zip bundles, OCI artifacts. OCI considered "heavy" and "not consumable." Databricks prototype uses plain markdown as MLflow artifacts. No industry consensus.

2. **Did the Databricks prototype ship by end of April 2026?** Target was end of April. Edson: *"I don't know if that is going to happen."* Status unknown.

3. **Skills catalog: yes or no?** Peter questions value of skills catalog given volume. Edson and Adam argue catalogs always come first with customers. Unresolved.

4. **Client-side vs server-side consumption**: Two fundamentally different models exist. How the registry represents and supports both is unresolved.

5. **Skill dependencies and asset linking**: Edson identified versioned dependency tracking (skill -> tool versions -> MCP server versions) as the key differentiator. Implementation TBD.

6. **Security scanning for skills**: Skills contain code/scripts. Need code scanning, not just container image scanning. Snyk for AI-specific scanning raised but not investigated.

7. **Ann Marie Fred's ODH repo proposal**: Simple repo of tested/validated skills as Dev Preview. Status unknown.

8. **Skill Packs**: Identified as secondary/future asset type. Relationship to individual skills registry unresolved.

9. **Framework portability**: No portable format across agent frameworks. Ann Marie Fred: *"There is no good portable format for skills across agents yet."*

10. **Llama Stack Skills API overlap**: Francisco Arceo is building the Llama Stack skills API. Relationship to MLflow skills registry unclear.

---

## Key People & Ownership

| Person | Skills-Related Role |
|--------|-------------------|
| **Peter Double** | Principal PM — skills registry ownership |
| **Edson Tirelli** | Agents/Skills lead; liaison with Databricks on MLflow prototype |
| **Matt Prahl** | Engineering; upstream collaboration with Databricks, Red Hat requirements via Slack |
| **Ann Marie Fred** | Skills packaging research; ODH repo proposal for skills Dev Preview |
| **Adam Bellusci** | Leadership — MLflow for registries, Kubeflow for catalogs (firm) |
| **Adel Zaalouk** | Agentic strategy; skills as pervasive building blocks |
| **Hunter Gerlach** | Consulting; real-world skills registry demand from field |
| **Francisco Arceo** | Building Llama Stack skills API implementation |
| **Aakanksha Duggal** | Coordinating across teams on registry efforts |
| **Dan Kuc** | MLflow/Registry engineering (no visible skills involvement yet) |
