---
title: MLflow Upstream Refresh (August 2026)
description: Four-month update on MLflow skills work — RFC pivot, Databricks strategy shift, Red Hat's expanding role
timestamp: 2026-08-04
lens: upstream
review_after: 2026-11-04
---

# MLflow Upstream Refresh (August 2026)

**Date**: 2026-08-04  
**Refreshes**: [02-mlflow-upstream.md](./02-mlflow-upstream.md) (April 2026)  
**Focus**: What changed since April — RFC strategy pivot, Databricks alignment, contributor activity, product releases

---

## Executive Summary

**Four months ago (April 2026)**, the MLflow Skills Registry was a Databricks prototype (`B-Step62/mlflow` branch `skill-registry-mvp`) with no formal upstream proposal. Red Hat's opportunity was to "submit a design proposal to issue #20435 before Databricks ships."

**Today (August 2026)**, the landscape has fundamentally shifted:

### Major Changes

1. **RFC Strategy Pivot** (July 2026): The upstream design approach evolved from "comprehensive technical RFC" to **user-journey-first alignment**, then implementation details. RFC-0008 (Skills Registry MVP) and RFC-0009 (Extended Skill Bundles) are now under formal review in the new `mlflow/rfcs` repository.

2. **Red Hat authorship established**: J. William Murdock (jwm4, Red Hat Senior Principal ML Engineer) is the author of both RFCs — Red Hat now **owns the upstream design**.

3. **Databricks strategy clarified**: Weekly PM syncs (Thursdays) now include Databricks PM Adam and tech lead Yuki (B-Step62). Databricks sees MLflow as "making MLflow famous" (not governance — Unity Catalog fills that role), and is willing to compromise on implementation details once user-journey buy-in is secured.

4. **Skills shipped in MLflow 3.14 and 3.15**: `mlflow agent setup` (one-command agent onboarding with MLflow skills), `mlflow skills view/list` CLI, and MCP Registry all landed in June-July 2026 releases.

5. **RFC split into two phases**: Skills and bundles (RFC-0008, open) + extended bundles with subagents/hooks/MCP (RFC-0009, draft). Trace linking further deferred to post-MVP.

6. **Skills evaluation stalled**: PR #21725 (skills as evaluation criteria) remains open since March with no merge progress.

### Strategic Position

**Red Hat's influence has increased dramatically** — from "waiting for a design proposal opportunity" in April to **authoring the canonical upstream design** in August. The risk shifted from "will Databricks ship first?" to "will the RFC get merged, and when?"

The governance gap identified in April (lifecycle states, approval workflows, certification) **remains unaddressed in the RFC** — this is still RHOAI's value-add layer.

---

## 1. RFC Status Update

### RFC-0008: MVP Skill Registry (PR #26)

**URL**: https://github.com/mlflow/rfcs/pull/26  
**Author**: jwm4 (J. William Murdock, Red Hat)  
**Status**: Open (opened Jul 14, 2026; last updated Aug 4, 2026)  
**Commits**: 28 commits from `jwm4:mvp-skill-registry` into `mlflow:main`

#### Scope

Phase 1 of skills work, narrowed from the original larger proposal (PR #10):

- **Skills**: SKILL.md directories with versioning, lifecycle, aliases, tags
- **Skill bundles**: versioned collections grouping related skills
- **Pull semantics**: harness-agnostic content fetch from Git, OCI, ZIP, MLflow artifact storage
- **Package manager integration**: delegates harness-specific installation to plugins (APM, Lola)
- **Trace integration**: creates SKILL spans with registry coordinates

**Explicitly deferred to Phase 2** (RFC-0009): subagents, hooks, MCP server references.

#### Review Activity

Three primary reviewers:

1. **mprahl** (Matt Prahl, Red Hat, MLflow Collaborator): ~15 comment threads. Initially approved Jul 28, then requested changes. Later suggested splitting out trace linking to merge faster.

2. **HumairAK** (Humair Khan, MLflow Maintainer): Reviewed Jul 22-23. Raised questions about unregistered content types, auto-log support, local materialization decisions.

3. **B-Step62** (Yuki Watanabe, Databricks, Contributor): Reviewed Jul 30-Aug 2. Pushed for simpler interfaces — "majority of these fields can be derived from the repo itself." Advocated for auto-increment versioning over semver, URI-based references (`skills:/name/version`) over object refs, field inference over manual configuration. Requested UI mockups.

#### Key Design Decisions (Influenced by Review)

| Decision | Before Review | After Review | Driver |
|----------|--------------|--------------|--------|
| **Versioning** | Semver strings | Server-assigned monotonic integers | B-Step62: "majority of public skill repos don't have semantic versions" |
| **Bundle member refs** | `SkillMemberRef` objects | `skills:/name/version` URI strings | B-Step62: MLflow pattern consistency |
| **Field inference** | Manual configuration | Server-side inference for name, source_type, harness | B-Step62: "make as many manual knobs optional" |
| **Trace linking** | In RFC-0008 | Deferred to follow-up PR | mprahl: "faster to merge if we remove trace linking" |
| **Installation** | In RFC-0008 | Deferred to separate installation RFC | jwm4 response to review |

#### Timeline

- **Jul 14**: PR opened (7 commits)
- **Jul 22-23**: First reviews (HumairAK, mprahl)
- **Jul 27**: 5 commits addressing feedback (Phase references, CLI naming, bundle fields)
- **Jul 28**: mprahl approved
- **Jul 29**: B-Step62 review requested; related PR #29 mentioned
- **Jul 30-31**: B-Step62 substantive review; 4 commits addressing feedback
- **Aug 1**: mprahl suggested removing trace linking
- **Aug 2-4**: Continued discussion on versioning, `latest_version` persistence; jwm4's latest updates

#### Current Blockers

- No explicit blockers listed, but the PR is unmerged after 3 weeks
- B-Step62 suggested UI mockups ("UI discussion on text is not very effective"), but mprahl countered with "agree on user journeys and data entities here, then start UI mocks during backend implementation" (referencing MCP registry delay)
- mprahl requested competitor mention (Google Gemini skill registry) to position MLflow as "the open source and vendor neutral skill registry"

---

### RFC-0009: Extended Skill Bundles (PR #27)

**URL**: https://github.com/mlflow/rfcs/pull/27  
**Author**: jwm4 (J. William Murdock, Red Hat)  
**Status**: Draft (opened Jul 23, 2026; last updated Jul 27, 2026)  
**Commits**: 2 commits

#### Scope

Companion to RFC-0008 that extends bundle membership beyond skills:

- **Agents, hooks, MCP server references**: Uses generic `member_type` field for harness-specific component types
- **Trace integration**: Same context manager, trace manifest, autologger mechanisms as RFC-0008
- **Intentionally limited**: "introduction, motivation, and user journeys" only — no schema, store interface, API endpoints, SDK signatures, or CLI mapping

**Goal**: "Get alignment on the approach before filling in specifics."

#### Review Activity

- **No reviews submitted** as of Aug 4
- **No assignees, labels, milestones, or projects**
- Only 1 participant (jwm4)
- PR description notes: "Posted by Bill Murdock with assistance from Claude Code"
- Commits co-authored with "Claude Opus 4.6"

#### Timeline

- **Jul 23**: PR opened and immediately marked as draft
- **Jul 27**: Second commit aligning with RFC-0008 round-2 review changes (CLI group renaming, schema migration text, open questions resolved)
- **Jul 29**: Referenced by PR #29 (non-technical overview, now closed)

#### Strategic Note

The draft status and lack of reviews suggest this is **parked pending RFC-0008 approval**. The "user-journey-first" strategy means getting buy-in on the foundational skills work before expanding scope.

---

### The RFC Strategy Pivot (Context from 2026-08-04 Meetings)

The current RFC approach reflects a **major strategic shift** in how Red Hat is engaging upstream:

#### Old Approach (Pre-July)
- Comprehensive technical RFCs with full implementation details upfront
- Risk: "so many little minutias... how many hours have we spent on naming" (Bill Murdock quote)
- Result: Internal misalignment reflected on community, reconciliation required

#### New Approach (Post-July)
- **User-journey-only RFC first** → get alignment → **then** technical details
- Once user-journey buy-in secured, "Databricks willing to compromise on implementation details" (Humair Khan)
- Bill Murdock: evolved from July RFC split decision

#### Databricks Context (Thursday PM Syncs)
- **Participants**: Databricks PM Adam, tech lead Yuki (B-Step62), Red Hat team
- **Databricks mantra**: "make MLflow famous" — Unity Catalog is the governance layer, MLflow is the famous open-source platform
- **Implication**: Databricks doesn't see MLflow as governance (that's UC's job), so governance features (lifecycle, approval workflows, certification) are **RHOAI's domain**

---

## 2. Databricks MVP Evolution

### April 2026 Status (from doc 02)

- **Branch**: `B-Step62/mlflow` branch `skill-registry-mvp`
- **Discoverable**: Publicly visible prototype
- **Architecture**: Dedicated entity type (5 new tables), SKILL.md canonical format, full CRUD REST API (`ajax-api/3.0/mlflow/skills/`), SDK under `mlflow.genai`, CLI (`mlflow skills register|list|load|show`)
- **Claude Code integration**: `install_skill()` to `~/.claude/skills/`, `.mlflow_skill_info` sidecar, tracing integration

### August 2026 Status

The MVP branch status is **unclear** — web searches found no references to `skill-registry-mvp` branch activity since April. GitHub API check of B-Step62's fork shows an `allow-skills` branch exists but no `skill-registry-mvp` branch listed.

**Likely interpretation**: The MVP branch served its purpose as a prototype. The formal design has moved to RFC-0008/RFC-0009, and implementation will likely merge directly to `mlflow:main` rather than maintaining the fork.

**B-Step62's focus shifted**: Yuki Watanabe is now the primary reviewer on RFC-0008, shaping the official design rather than maintaining a separate prototype.

---

## 3. Skills Evaluation PR #21725 (Stalled)

**URL**: https://github.com/mlflow/mlflow/pull/21725  
**Title**: "Support Agent Skills (SKILL.md) as reusable evaluation criteria for judges"  
**Author**: forrestmurray-db (Databricks)  
**Status**: Open (opened Mar 16, 2026; last updated May 6, 2026)  
**Merged**: False

### What Changed Since April

**Nothing.** The PR has been dormant since early May with no merge progress.

**April status**: "Under review, Phase 1 only (evaluation use case, NOT registry)"  
**August status**: Still under review, no movement for 3 months

### Context

This PR implements Issue #21255 (skills as evaluation criteria for LLM judges). It's **separate from the registry work** — focuses on using SKILL.md files within the evaluation framework, not versioning/governance.

**Strategic implication**: The registry work (RFC-0008) is proceeding **independently** of the evaluation use case. The two will eventually integrate (skills from the registry used as evaluation criteria), but evaluation isn't blocking registry.

---

## 4. MLflow 3.14 and 3.15 Releases — Skills Features Shipped

### MLflow 3.14.0 (June 17, 2026)

**URL**: https://github.com/mlflow/mlflow/releases/tag/v3.14.0

#### Major Skills Features

1. **`mlflow agent setup`** — One-command agent onboarding
   - Installs MLflow, sets up tracing, hands skills to coding agent (Claude Code, OpenAI Codex, OpenCode)
   - "All from a single command"
   - Databricks backend support added (#23783, @harupy)

2. **`mlflow skills view/list` CLI** (#23907, @joshuawong-db)
   - Command-line access to view and list available skills

3. **Skills installation path** standardized (#23847, @harupy)
   - Codex/OpenCode skills install at `.agents/skills/`

4. **Durable, low-latency tracing for Claude Code**
   - Write-ahead-log (WAL) prevents slowing agent or losing traces during network issues
   - `MlflowWalSpanExporter` introduced (#23641)
   - UC trace location support via `MLFLOW_TRACE_LOCATION` for Claude Code (#23770) and Codex (#23771)

5. **Documentation**
   - Skills and agent setup surfaced in official docs (#23859, @joshuawong-db)
   - Claude Code plugin installation docs updated (#23679, @harupy)

#### Other 3.14 Highlights (Agent Ecosystem)

- Review Queues for structured feedback on traces
- Revamped evaluation dataset UI
- pytest integration gating GenAI quality in CI
- In-browser LLM Playground

**Strategic note**: MLflow 3.14 shipped **coding agent skills** (teaching agents how to use MLflow), not the **skills registry** (versioning/governance for skills). The registry is still pre-merge in RFC-0008.

---

### MLflow 3.15.0 (July 31, 2026)

**URL**: https://github.com/mlflow/mlflow/releases/tag/v3.15.0

#### Major Features

1. **MCP Registry** (centralized catalog for Model Context Protocol servers)
   - Semantic-versioned configs with aliases and tags
   - Auto-discovered tools from registered MCP servers
   - Connection instructions for Claude Code and `.mcp.json`
   - Manageable via UI, REST API, or Python
   - Docs contributed by @dkuc (Dan Kuc, Red Hat) — PRs #24713, #24519

2. **MLflow Assistant upgraded**
   - Multi-provider support (Claude Code, Codex, OpenAI-compatible/Gateway endpoints)
   - Single settings page for configuration
   - Live per-session token usage and estimated cost display
   - `mlflow agent setup` can enable assistant "in one prompt" with secure API key storage
   - Tool call permission granting (#24084)

3. **Skills improvements**
   - Python 3.14 compatibility fix in `skill_installer` module (#24103, @krishtyagi0109-pixel) — switched to `pathlib.Path`

4. **Agent-adjacent features**
   - Pydantic AI 2.x autologging support (#24721)
   - OpenAI-protocol coding agents authenticate through RBAC gateway (#24294)
   - Multi-modal attachments in LLM judges (vision tasks, screenshots) via `get_span_image` tool
   - Playground UI redesigned (per-tool cards, Monaco JSON editor, improved add-tools flow) (#24102, #24129)

**Strategic note**: The MCP Registry (analogous to Skills Registry for MCP servers) shipped in MLflow 3.15 with **Dan Kuc (Red Hat) contributing documentation**. This establishes the pattern for Red Hat's upstream presence in MLflow registry work.

---

### MLflow 3.15.1 (August 3, 2026)

**URL**: https://github.com/mlflow/mlflow/releases/tag/v3.15.1  
Patch release — no skills-specific changes noted.

---

## 5. Red Hat Contributor Analysis

### Matt Prahl (mprahl) — Highly Active

**April status**: "Very active — 20+ PRs since Feb 2026"  
**August status**: **Even more active** — now an MLflow maintainer and RFC author

#### Recent Activity (April-August 2026)

- **RFC-0008 review**: Primary reviewer (~15 comment threads), approved then requested changes, suggested strategic splits (trace linking deferral)
- **RFC-0028**: Authored "Advanced trace archival with Iceberg" (opened Jul 29, 2026) — own RFC demonstrating deep MLflow engagement
- **Maintainer status**: Listed as "Collaborator" on RFC-0008 reviews (elevated from contributor)
- **Focus areas**: Workspace support, trace archival, RBAC, UI (per April doc), now expanding to RFC-level architecture

**Strategic implication**: Matt Prahl is Red Hat's **technical anchor** in MLflow — infrastructure contributions (workspaces, tracing, archival) create the foundation for skills registry work, and his RFC authorship shows Red Hat shaping MLflow's roadmap.

---

### Dan Kuc (dkuc) — Newly Visible

**April status**: "No public commits, issues, PRs, or comments in mlflow/mlflow as of today. No visible involvement in skills-related discussions."  
**August status**: **Active in MLflow 3.15** — MCP Registry documentation contributor

#### Recent Activity

- **MLflow 3.15 MCP Registry docs**: PRs #24713 (MCP Registry feature docs) and #24519 (Swagger UI API docs for MCP Server Registry)
- **Still no skills-specific work visible** in GitHub searches

**Strategic implication**: Dan Kuc's MCP Registry work positions Red Hat across **multiple MLflow registry types** (MCP servers, and soon skills). His Kubeflow Model Registry fork (noted in April) suggests he's the bridge between MLflow and Kubeflow catalog architectures.

---

### J. William Murdock (jwm4) — New Red Hat Upstream Lead

**April status**: Not mentioned (Bill Murdock referenced in meeting transcripts but no GitHub activity noted)  
**August status**: **RFC author** for Skills Registry — Red Hat's most visible upstream contributor on skills

#### Profile

- **GitHub**: jwm4
- **Red Hat title**: Senior Principal Machine Learning Engineer
- **Team**: Agentic/MCP team for Red Hat AI
- **Background**: IBM Watson Research (original Watson project, Watson Discovery cloud services)
- **Education**: PhD, Georgia Institute of Technology
- **Other work**: InstructLab, RHEL AI, Llama Stack, AI Alliance Llama Stack Examples, Docling SDG

#### MLflow Activity (2026)

- **RFC-0008** (PR #26): Authored Skills Registry MVP (Jul 14, 2026)
- **RFC-0009** (PR #27): Authored Extended Skill Bundles (Jul 23, 2026)
- **Issue #22833**: Created "[FR] Add skill registry primitives for governed skill metadata and versioning" (Apr 23, 2026) — the feature request that seeded the RFC work
- **Co-authorship**: All RFC commits co-authored with "Claude Opus 4.6" — demonstrating AI-assisted design workflow

**Strategic implication**: Bill Murdock is Red Hat's **design lead** for MLflow skills work — he's not just contributing code, he's **authoring the canonical upstream design**. His background (Watson, InstructLab) brings enterprise AI governance perspective that Databricks (focused on "making MLflow famous") doesn't prioritize.

---

### Humair Khan (HumairAK) — MLflow Maintainer (Non-Red Hat)

**April status**: Mentioned as MLflow core maintainer  
**August status**: Active reviewer on RFC-0008, quoted in 2026-08-04 meeting context

#### Recent Activity

- **RFC-0008 review**: Reviewed Jul 22-23, raised questions about unregistered content types, auto-log support, local materialization
- **Strategic input** (from meeting notes): "Once user-journey buy-in secured, Databricks willing to compromise on implementation details"

**Affiliation clarification**: Humair Khan is a **Databricks/MLflow maintainer**, not Red Hat (April doc listed him as maintainer but didn't specify employer). He's a key bridge for Red Hat-Databricks alignment.

---

## 6. Strategy Pivot Analysis — User-Journey-First Approach

### The Evolution (From Meeting Transcripts)

#### Phase 1: Comprehensive Technical RFC
- Original approach: Full implementation details upfront
- **Problem**: "So many little minutias... how many hours have we spent on naming" (Bill Murdock)
- **Result**: Internal misalignment reflected on community, reconciliation required in second version

#### Phase 2: RFC Split (July 2026)
- Recognition that bundling too much creates review bottlenecks
- Split into:
  - **RFC-0008**: Skills and bundles MVP
  - **RFC-0009**: Extended bundles (subagents, hooks, MCP)
  - **Post-MVP**: Trace linking, installation (deferred)

#### Phase 3: User-Journey-First (Current)
- **New principle**: Get alignment on **user journeys** before technical details
- **Databricks response**: Willing to compromise on implementation once user-journey buy-in secured
- **Rationale**: Databricks PM Adam and tech lead Yuki (B-Step62) need to see the "why" before debating the "how"

### Databricks Strategic Context (Thursday PM Syncs)

#### Key Insights

1. **"Make MLflow famous"** — Databricks' north star for MLflow
   - MLflow is the open-source platform that brings users to Databricks
   - Unity Catalog is the governance layer (enterprise features, RBAC, lineage)
   - MLflow stays lightweight, vendor-neutral, famous

2. **Governance is not MLflow's job** (in Databricks' view)
   - Databricks doesn't see MLflow as the governance layer
   - Skills registry in MLflow: versioning, storage, retrieval
   - Skills governance in RHOAI/Unity Catalog: lifecycle, approval, certification, trust tiers

3. **Red Hat's window of influence**
   - User-journey alignment phase: Red Hat has full voice (equal partner in defining the use cases)
   - Implementation details phase: Databricks willing to compromise (Red Hat can shape the API, data model, CLI)
   - Post-merge: RHOAI adds governance on top (doesn't need to be in MLflow core)

### Strategic Implications for RHOAI

#### What This Means

1. **Red Hat owns the design** — RFC-0008/RFC-0009 authorship gives Red Hat the pen on upstream skills work
2. **Governance stays downstream** — RHOAI's value-add (lifecycle states, approval workflows, certification, trust tiers) doesn't need to merge to MLflow; it's a governance layer on top
3. **The "famous" play** — If MLflow becomes the de facto open-source skills registry, RHOAI becomes the "enterprise governance for the famous skills registry" (same pattern as Unity Catalog for Databricks)

#### Risks

1. **RFC merge timeline uncertain** — RFC-0008 has been open for 3 weeks with active review but no merge
2. **User-journey buy-in not yet secured** — Databricks reviewers (B-Step62) pushing back on details suggests the "why" isn't fully sold
3. **UI mockup request** — B-Step62's push for UI mocks (not yet delivered) could delay merge if it becomes a blocker

---

## 7. Kubeflow Hub Plugin Architecture — Closed

**URL**: https://github.com/kubeflow/model-registry/issues/2220  
**Title**: "[Proposal] Plugin-Based Catalog Architecture and catalog-gen tool to generate new catalog types"  
**Author**: Al-Pragliola  
**Status**: **Closed** (opened Feb 11, 2026; closed with 7/7 sub-issues completed; last updated Jul 28, 2026)

### What Changed Since April

**April status**: "Proposes a plugin-based catalog architecture supporting multiple asset types (models, MCP servers, datasets, prompt templates, agents)"  
**August status**: **Shipped** — issue closed with all sub-issues completed, assigned to Kubeflow 26.10 roadmap milestone

### Architecture (From Issue #2220)

- **Unified catalog server**: Multiple catalog plugins in a single process
- **Plugin model**: Each plugin gets own API routes, database tables, data providers, OpenAPI spec
- **Shared infrastructure**: Database connection (GORM: SQLite/MySQL/PostgreSQL), config system, HTTP server
- **catalog-gen CLI**: Scaffolding tool (inspired by kubebuilder) generates complete plugin boilerplate from `catalog.yaml`
- **Agentic workflows**: Generated `.claude/` directory with skills and architecture summaries for AI-assisted development

### MCP Plugin as Validation

The MCP (Model Context Protocol) plugin was the first non-model catalog type, demonstrating the architecture works. Generated entirely via `catalog-gen`, serves its own API at `/api/mcp_catalog/v1alpha1/mcpservers`.

### Strategic Implication for Skills Registry

The Kubeflow Hub plugin architecture creates a **catalog-side counterpart** to MLflow's registry-side Skills Registry:

- **MLflow Skills Registry**: Versioning, storage, retrieval, lifecycle (RFC-0008/RFC-0009)
- **Kubeflow Hub Skills Plugin**: Catalog discovery, filtering, pagination, source management (plugin architecture)

Skills could be a Hub plugin alongside models and MCP servers, enabling **federated discovery** across MLflow-governed skills.

---

## 8. Risks and Timeline

### Risks

#### 1. RFC Merge Uncertainty
- **Status**: RFC-0008 open for 3 weeks, active review, no merge
- **Blocker potential**: UI mockup request (B-Step62) not yet delivered
- **Mitigation**: mprahl suggested "agree on user journeys and data entities, then UI mocks during implementation" (learned from MCP registry delay)

#### 2. Databricks User-Journey Buy-In
- **Status**: Review pushback on implementation details (versioning, field inference, URI scheme) suggests "why" isn't fully sold
- **Risk**: If Databricks doesn't see the user-journey value, implementation details become never-ending debates
- **Mitigation**: Thursday PM syncs with Databricks PM Adam and Yuki (B-Step62) are the alignment forum

#### 3. Skills Evaluation Integration Unclear
- **Status**: PR #21725 (skills as evaluation criteria) stalled since May
- **Risk**: If evaluation doesn't integrate with registry, the "skills as reusable evaluation criteria" use case (a key user journey) doesn't materialize
- **Mitigation**: Registry work is proceeding independently; evaluation can integrate post-MVP

#### 4. Governance Scope Creep
- **Status**: RFC-0008 deliberately excludes lifecycle states, approval workflows, certification
- **Risk**: Downstream RHOAI governance layer could be seen as "not upstream-first" if not positioned correctly
- **Mitigation**: Databricks' "make MLflow famous" strategy validates that governance is **not MLflow's job** (it's Unity Catalog's / RHOAI's)

### Timeline

| Milestone | Status | Date | Next Step |
|-----------|--------|------|-----------|
| **Issue #22833 created** | ✅ Done | Apr 23, 2026 | — |
| **RFC-0008 opened** | ✅ Done | Jul 14, 2026 | — |
| **RFC-0009 opened (draft)** | ✅ Done | Jul 23, 2026 | — |
| **MLflow 3.14 shipped** (skills CLI) | ✅ Done | Jun 17, 2026 | — |
| **MLflow 3.15 shipped** (MCP Registry) | ✅ Done | Jul 31, 2026 | — |
| **RFC-0008 first approval** | ✅ Done | Jul 28, 2026 (mprahl) | — |
| **RFC-0008 changes requested** | ✅ Done | Jul 30-Aug 2 (B-Step62) | — |
| **RFC-0008 merge** | ⏳ Pending | TBD | Address B-Step62 feedback, resolve UI mockup question |
| **RFC-0009 review** | ⏳ Pending | TBD | Exit draft status, await RFC-0008 merge |
| **Skills Registry implementation** | ⏳ Pending | TBD (post-RFC-0008 merge) | Likely target: MLflow 3.16 or 3.17 (Sep-Oct 2026?) |
| **RHOAI governance layer design** | ⏳ Not started | TBD | Parallel to MLflow implementation |

**Optimistic timeline**: RFC-0008 merges in August, implementation lands in MLflow 3.16 (September 2026), RHOAI governance layer designed in parallel, ships in RHOAI 2.x (Q4 2026).

**Realistic timeline**: RFC-0008 merges in September after UI alignment, implementation lands in MLflow 3.17 (October 2026), RHOAI governance layer ships in RHOAI 2.x (Q1 2027).

---

## 9. Key Links

### RFCs and PRs

| Resource | URL | Status |
|----------|-----|--------|
| RFC-0008: Skills Registry MVP | https://github.com/mlflow/rfcs/pull/26 | Open |
| RFC-0009: Extended Skill Bundles | https://github.com/mlflow/rfcs/pull/27 | Draft |
| Issue #22833: Skills Registry FR | https://github.com/mlflow/mlflow/issues/22833 | Open |
| Issue #21255: Skills as Evaluation Criteria | https://github.com/mlflow/mlflow/issues/21255 | Open |
| PR #21725: Skills Evaluation (Phase 1) | https://github.com/mlflow/mlflow/pull/21725 | Open (stalled) |
| Matt Prahl RFC-0028: Trace Archival | https://github.com/mlflow/rfcs/pull/28 | Open |

### Releases

| Resource | URL |
|----------|-----|
| MLflow 3.14.0 (Skills CLI) | https://github.com/mlflow/mlflow/releases/tag/v3.14.0 |
| MLflow 3.15.0 (MCP Registry) | https://github.com/mlflow/mlflow/releases/tag/v3.15.0 |
| MLflow 3.15.1 (Latest) | https://github.com/mlflow/mlflow/releases/tag/v3.15.1 |
| MLflow Releases Page | https://mlflow.org/releases/ |

### Repositories

| Resource | URL |
|----------|-----|
| mlflow/rfcs | https://github.com/mlflow/rfcs |
| mlflow/mlflow | https://github.com/mlflow/mlflow |
| mlflow/skills | https://github.com/mlflow/skills |
| B-Step62/mlflow | https://github.com/B-Step62/mlflow |

### Contributors

| Resource | URL |
|----------|-----|
| J. William Murdock (jwm4) GitHub | https://github.com/jwm4 |
| J. William Murdock Red Hat Profile | https://www.redhat.com/en/authors/j-william-murdock |
| Matt Prahl (mprahl) GitHub | https://github.com/mprahl |
| Dan Kuc (dkuc) GitHub | https://github.com/dkuc |
| MLflow Contributors Graph | https://github.com/mlflow/mlflow/graphs/contributors |

### Related

| Resource | URL |
|----------|-----|
| Kubeflow Hub Plugin Architecture (#2220) | https://github.com/kubeflow/model-registry/issues/2220 |
| MLflow Blog: Testing Skills with MLflow | https://mlflow.org/blog/evaluating-skills-mlflow/ |
| MLflow Prompt Registry Docs | https://mlflow.org/docs/latest/genai/prompt-registry/ |

---

## 10. Comparison to April 2026 Findings

| Dimension | April 2026 | August 2026 | Change |
|-----------|------------|-------------|--------|
| **Upstream proposal** | None (opportunity to submit) | RFC-0008/RFC-0009 (Red Hat authored) | ✅ **Red Hat owns design** |
| **Databricks prototype** | `skill-registry-mvp` branch visible | Branch status unclear; focus shifted to RFC review | ⚠️ Prototype served purpose; formal design in progress |
| **Red Hat influence** | "Submit design proposal" opportunity | **Authoring canonical RFC** | ✅ **Dramatic increase** |
| **Skills in MLflow releases** | Not shipped | 3.14 (skills CLI), 3.15 (MCP Registry) | ✅ **Shipped** (coding agent skills, not registry yet) |
| **Skills evaluation** | PR #21725 under review | Still under review (stalled) | ❌ **No progress** |
| **Matt Prahl activity** | 20+ PRs (infrastructure) | RFC reviewer + own RFC (trace archival) | ✅ **Elevated to RFC author** |
| **Dan Kuc activity** | No visible MLflow work | MCP Registry docs contributor | ✅ **Active in 3.15** |
| **Bill Murdock activity** | Meeting transcripts only | **RFC author** (jwm4) | ✅ **Upstream design lead** |
| **Governance gap** | Identified (lifecycle, approval, cert) | Still unaddressed in RFC-0008 | ✅ **Confirms RHOAI value-add** |
| **Databricks strategy** | "Make MLflow famous" mentioned | Formalized in Thursday PM syncs | ✅ **Clarified and validated** |
| **RFC strategy** | N/A (no RFC yet) | User-journey-first, then details | 🆕 **New approach** |
| **Kubeflow Hub plugin arch** | Proposed (#2220) | **Shipped** (closed with 7/7 complete) | ✅ **Delivered** |
| **Timeline risk** | "Databricks may ship first" | "RFC merge timing uncertain" | ⚠️ **Risk shifted** (not "will it happen" but "when") |

---

## 11. Strategic Recommendations (Updated)

### For RHOAI Product Team

1. **Accelerate RFC-0008 merge**
   - Coordinate with Bill Murdock (jwm4) on addressing B-Step62 feedback
   - Resolve UI mockup question (follow mprahl's advice: user journeys first, UI during implementation)
   - Ensure Thursday PM sync with Databricks PM Adam and Yuki secures user-journey buy-in

2. **Design RHOAI governance layer in parallel**
   - Don't wait for RFC-0008 merge to start RHOAI design
   - Governance features (lifecycle states, approval workflows, certification, trust tiers) are **not** MLflow's job (per Databricks strategy)
   - RHOAI's value-add: "Enterprise governance for the open-source skills registry" (same as Unity Catalog for Databricks)

3. **Leverage "make MLflow famous" alignment**
   - Position RHOAI as **making MLflow more enterprise-ready** without bloating MLflow core
   - Governance-as-a-layer allows MLflow to stay lightweight and famous
   - Red Hat's upstream contributions (RFCs, MCP docs) build credibility for downstream governance claims

4. **Monitor skills evaluation integration**
   - PR #21725 stalled — evaluate whether "skills as evaluation criteria" is a critical user journey for RHOAI
   - If yes, consider Red Hat engineering support to unstick the PR (post-RFC-0008 merge)

### For Red Hat MLflow Contributors

1. **Bill Murdock (jwm4)**: Own the RFC-0008 merge — address feedback, drive Thursday syncs, secure Databricks buy-in
2. **Matt Prahl (mprahl)**: Continue RFC review + infrastructure work (trace archival RFC-0028 positions Red Hat as MLflow architecture partner)
3. **Dan Kuc (dkuc)**: MCP Registry docs work is great; consider expanding to skills registry docs (post-RFC-0008 merge)
4. **Coordinate upstream-downstream**: Ensure RFC-0008 primitives (versioning, aliases, tags, artifact storage) support RHOAI governance layer needs

### For Cross-Component Coordination

1. **Skills Registry ↔ MCP Registry alignment**
   - Dan Kuc contributed MCP Registry docs; same patterns apply to Skills Registry
   - Both registries follow MLflow's entity-version-alias-tag pattern
   - RHOAI governance layer should work across **both** registries (unified governance for MCP servers and skills)

2. **Skills Registry ↔ Kubeflow Hub alignment**
   - Kubeflow Hub plugin architecture (#2220 shipped) enables Skills Plugin for catalog discovery
   - MLflow Skills Registry (versioning/governance) + Kubeflow Hub Skills Plugin (catalog/discovery) = full stack
   - Dan Kuc's dual forks (mlflow, kubeflow/model-registry) position him as the bridge engineer

---

## Appendix: User-Journey Examples (From RFC-0008 Context)

The user-journey-first approach centers on **why** users need a skills registry, not **how** it's implemented. Key journeys driving RFC-0008:

### Journey 1: "npm install for skills"
**Actor**: AI developer using Claude Code  
**Goal**: Install a versioned skill from a registry with dependency locking  
**Steps**:
1. `mlflow skills search --query "data analysis"`
2. `mlflow skills install mlflow/analyze-trace@v1.2.0`
3. Skill installs to `.claude/skills/analyze-trace/` with lock file (version, commit hash, source)
4. Claude Code loads skill, traces usage back to registry

**Why this matters**: Databricks' "equivalent to npm install" vision (from April meeting transcripts)

### Journey 2: "Share skills across team"
**Actor**: ML platform team  
**Goal**: Publish internal skills to team registry, version and alias them  
**Steps**:
1. `mlflow skills register --source ./internal-skills/sagemaker-deploy/ --name rh/sagemaker-deploy`
2. Registry auto-increments version (v1), extracts SKILL.md, stores artifacts
3. `mlflow skills set-alias rh/sagemaker-deploy --alias production --version 1`
4. Team members: `mlflow skills install rh/sagemaker-deploy@production`

**Why this matters**: "Team-wide sharing and versioning via the registry" (from Issue #21255)

### Journey 3: "Skill bundle for onboarding"
**Actor**: New AI developer joining team  
**Goal**: Install entire onboarding bundle (10+ skills)  
**Steps**:
1. `mlflow bundles install rh/onboarding-bundle@latest`
2. Bundle contains skills for MLflow tracing, evaluation, Databricks auth, RHOAI deployment, etc.
3. All skills install atomically with versions locked

**Why this matters**: "Coherent toolboxes or workflows discovered as a unit" (RFC-0008 scope)

### Journey 4: "Trace skill usage for governance"
**Actor**: ML governance team  
**Goal**: Understand which skills are used in production traces  
**Steps**:
1. Claude Code agent invokes skill `rh/sagemaker-deploy@v2`
2. Skill span created in trace with registry coordinates (name, version, alias, commit hash)
3. Governance team queries traces: "Which agents are using deprecated skill versions?"

**Why this matters**: "Usage analytics extracted from span names" (from Databricks MVP analysis in doc 02)

---

**End of Report**
