---
title: "Skills Catalog research -- upstream refresh"
description: "KEP-0005 merged in kubeflow/hub (SKILL.md parser + OpenAPI, Jul 2026); EX agentic-collections format extends agentskills.io spec with model/color fields; catalog.redhat.com/en/ai is a parallel surface with federation risk; MLflow #22833 proposes skill registry primitives; ecosystem grew to 40+ agents and 1.9M indexed skills with security crisis (Snyk ToxicSkills: 36% flawed)"
timestamp: 2026-08-02
lens: upstream
review_after: 2026-11-02
supersedes_context: "Updates 01-upstream (2026-07-23) with EX agentic-collections format analysis, agentskills.io compliance mapping, catalog.redhat.com/en/ai federation question, and new upstream developments"
---

# Skills Catalog research -- upstream refresh

This document refreshes the upstream landscape analysis from
[01-upstream](/components/skills-catalog/research/01-upstream.md)
(2026-07-23) with findings from the EX agentic-collections repo,
Kubeflow hub skills catalog implementation, and ecosystem developments
through 2026-08-02.

## 1. EX agentic-collections repo deep-dive

### Repository identity

The GitHub repo is **RHEcosystemAppEng/agentic-plugins** (Apache 2.0).
The marketing name "agentic-collections" appears on the landing page at
redhat.com/en/agentic-skills, but the actual repo slug is
`agentic-plugins`. This naming mismatch is a minor source confusion.

Source: https://github.com/RHEcosystemAppEng/agentic-plugins

### Directory conventions

```
<pack>/
  .catalog/
    collection.yaml      # canonical catalog metadata
    collection.json       # JSON mirror (CI-enforced parity)
    *.md                  # prose fragments referenced by YAML
  skills/
    <skill-name>/
      SKILL.md            # per agentskills.io spec + EX extensions
      docs/               # optional, symlinks allowed
  mcps.json               # MCP server definitions (pack-level)
  README.md               # golden source (persona, scope)
  AGENTS.md               # intent routing and persona description
```

The `<pack>/.catalog/collection.yaml` is the routing table for
catalog.redhat.com publishing. It carries a `maturity` field (GREEN =
promote, ORANGE = exclude). Schema validation via
`catalog/schema.yaml` + `scripts/validate_collection_compliance.py`.

### SKILL.md frontmatter schema (EX format)

Confirmed across multiple packs (rh-sre/system-context,
rh-ai-engineer/model-deploy):

```yaml
---
name: system-context                    # agentskills.io spec (required)
description: |                          # agentskills.io spec (required)
  <multi-line, includes Use when: and NOT for: examples>
model: inherit                          # EX EXTENSION (not in spec)
color: blue                             # EX EXTENSION (not in spec)
license: Apache-2.0                     # agentskills.io spec (optional)
allowed-tools: tool1 tool2 tool3        # agentskills.io spec (experimental)
---
```

### EX design principles (DP1-DP7) summary

| ID | Principle | Enforcement |
|---|---|---|
| DP1 | Document consultation transparency | Must Read files before claiming consultation |
| DP2 | Precise parameter specification | Exact types, constraints, formats per step |
| DP3 | Skill precedence + concise descriptions | <500 tokens; include Use when/NOT for |
| DP4 | Skill-to-skill invocation standard | Slash format (`/skill-name`) consistently |
| DP5 | Dependencies declaration | MCP servers, tools, related skills, reference docs |
| DP6 | Human-in-the-loop | Explicit confirmation for create/delete/modify ops |
| DP7 | Mandatory sections in order | Frontmatter, overview, HITL, Prerequisites, When to Use, Workflow, Dependencies |

Validation: `make validate` and `make validate-skill-design` in CI.

### Skill body structure requirements (DP7)

Beyond frontmatter, EX requires these body sections in order:
1. Skill heading + 1-2 sentence overview
2. Human-in-the-Loop Requirements (if applicable)
3. Prerequisites (MCP servers, tools, env vars, verification, Human
   Notification Protocol, security warning)
4. When to Use This Skill (3+ scenarios + Do NOT use when)
5. Workflow (numbered steps with MCP tool, parameters, expected output,
   error handling)
6. Dependencies (4 categories: MCP servers, MCP tools, related skills,
   reference docs)
7. Example Usage (recommended)

### model and color fields

**model**: `inherit` (default, use parent agent model), `sonnet`
(complex reasoning), `haiku` (simple/fast). Controls which model the
agent uses when executing the skill.

**color**: Risk-tier visual indicator:
- cyan = read-only
- green = additive
- blue = reversible modification
- yellow = destructive but recoverable
- red = irreversible
- magenta = creative/generative

These are EX innovations with no equivalent in the agentskills.io spec.

## 2. Format mapping: EX vs agentskills.io vs Kubeflow hub

### Field-by-field compliance matrix

| Field | agentskills.io spec | EX agentic-plugins | Kubeflow hub parser (SKC-104) | Notes |
|---|---|---|---|---|
| `name` | Required, max 64 chars, lowercase+hyphens | Compliant | Parsed, warns on mismatch/overlength | Full alignment |
| `description` | Required, max 1024 chars | Compliant (uses multi-line) | Parsed, skips if missing | Full alignment |
| `license` | Optional | Used (Apache-2.0) | Parsed | Full alignment |
| `compatibility` | Optional, max 500 chars | Not observed in samples | Parsed, warns if over-length | EX omits, spec allows |
| `metadata` | Optional, string-to-string map | Not observed in samples | Parsed defensively (map) | EX omits, spec allows |
| `allowed-tools` | Optional, space-separated (experimental) | Used (MCP tool names) | Parsed as space-separated string | Full alignment |
| `model` | **Not in spec** | Required by DP7 | **Not parsed** | EX-only extension |
| `color` | **Not in spec** | Required by DP7 | **Not parsed** | EX-only extension |

### What EX adds beyond the spec

1. **`model` field** -- execution model selection (inherit/sonnet/haiku).
   Not in agentskills.io. Not parsed by Kubeflow hub. Would need to go
   into `metadata` map for spec compliance.
2. **`color` field** -- risk-tier visual coding. Same situation.
3. **Mandatory body sections** (DP7) -- the spec has "no format
   restrictions" on the body. EX requires 7 ordered sections with
   specific content. This is a superset constraint, not a violation.
4. **Pack-level metadata** -- `collection.yaml` with maturity,
   deploy_and_use, sample_workflows, mcp_section, security_model.
   No spec equivalent; this is a grouping/catalog concern.

### What EX omits from the spec

1. **`compatibility` field** -- not observed in sampled SKILL.md files.
   The information is present in README/AGENTS.md but not in the
   per-skill frontmatter.
2. **`metadata` map** -- not used. The `model` and `color` fields are
   top-level rather than under `metadata:`, meaning they are
   technically spec-non-compliant extra fields.

### Compliance assessment

EX skills are **functionally compliant** with agentskills.io (both
required fields present, name format correct, allowed-tools parsed
correctly) but **structurally divergent** in two ways:
- `model` and `color` are top-level fields, not under `metadata:`
- The spec validation tool (`skills-ref validate`) would flag these
  as unknown frontmatter keys

**Migration path**: Move `model` and `color` under `metadata:`:
```yaml
metadata:
  model: inherit
  color: blue
```
This preserves the information while achieving strict spec compliance.

### Kubeflow hub catalog schema mapping

The Kubeflow hub skills catalog (KEP-0005) maps SKILL.md to its
internal schema as follows:

| SKILL.md field | Hub catalog field | Notes |
|---|---|---|
| `name` | `name` | Direct mapping |
| `description` | `description` | Direct mapping |
| `license` | `license` | Direct mapping |
| `compatibility` | `compatibility` | Direct mapping |
| `allowed-tools` | `allowedTools` | Space-separated string |
| `metadata` | `metadata` (map) | Passed through |
| (body content) | `readme` | Full markdown body stored |
| (file line count) | `lineCount` | Computed by parser |

Catalog-level metadata not from SKILL.md:
- `trustTier`: platformProvided / partnerVerified / organizationApproved / communityContributed
- `provider`, `category`, `labels`: assigned in source file
- `repository`, `path`, `version`, `resolvedCommit`: identity fields
- Supporting file paths (scripts/, references/): linked, not stored

## 3. catalog.redhat.com/en/ai as a parallel surface

### What it is

catalog.redhat.com/en/ai is the **Red Hat Ecosystem Catalog** agentic
capabilities page. It currently lists:
- 4 skill packs (rh-basic, rh-sre, ocp-admin, rh-virt)
- 2 individual agentic skills (RHEL best practices, RHEL translator)
- 5 MCP servers (RHEL, OpenShift, AAP, Lightspeed, Satellite)

All items are "by Red Hat." No third-party entries. Skill packs link
to `/en/ai/skills/detail/` paths; MCP servers link to container catalog
paths (`/en/software/containers/`).

### Relationship to RHOAI skills catalog

These are **two separate catalog surfaces** with different publishing
pipelines:

| Aspect | catalog.redhat.com/en/ai | RHOAI skills catalog (Kubeflow hub) |
|---|---|---|
| Publisher | Red Hat Ecosystem Catalog team | Kubeflow hub, RHOAI dashboard |
| Content source | EX agentic-plugins via agentic-catalog build | Git repos via git-skills-plugin |
| Audience | External (developers, field) | Internal (RHOAI platform users) |
| Format | HTML pages + Lola marketplace YAML | REST API + React UI |
| Third-party content | Not yet | Supported (source file config) |
| Content gate | maturity: GREEN in collection.yaml | trustTier in source config |

### Federation risk

**Duplication is likely.** The same EX skill packs will appear in both
catalogs unless the RHOAI catalog explicitly deduplicates or the EX
agentic-catalog build pipeline becomes a source for Kubeflow hub.

Three possible resolutions:
1. **Ecosystem Catalog is upstream** -- Kubeflow hub reads from
   catalog.redhat.com API (requires API existence)
2. **Shared source** -- both read from the same git repos
   (RHEcosystemAppEng/agentic-plugins) with independent rendering
3. **Distinct scopes** -- Ecosystem Catalog handles Red Hat-authored
   skills only; Kubeflow hub handles all tiers including community

Option 3 is the most natural given KEP-0005's trustTier model. The
Ecosystem Catalog maps to `platformProvided` tier; the Kubeflow hub
indexes all tiers.

### The agentic-catalog repo

**RHEcosystemAppEng/agentic-catalog** (Apache 2.0) is the publishing
artifact for catalog.redhat.com/en/ai. It is not a skills development
repo.

Source: https://github.com/RHEcosystemAppEng/agentic-catalog

Contents:
- `marketplace/rh-agentic-collection.yml` -- Lola marketplace YAML
  with module entries (name, title, description, version, repository,
  path, icon, tags)
- `docs/data.json` -- generated catalog data for the website
- `docs/mcp.json` -- MCP server metadata
- `docs/collections/` -- auto-generated per-pack HTML pages
- `scripts/` -- build tooling

Pipeline: agentic-plugins (source) -> eval/scoring -> agentic-catalog
(generated output) -> catalog.redhat.com (published). Evaluation
reports live in the source repo (`eval/<pack>/<skill>/report.json`),
not in the catalog repo.

The marketplace YAML uses a simple module schema:
```yaml
modules:
  - name: ocp-admin
    title: "Skill pack for Red Hat OpenShift"
    description: "..."
    version: "0.1.0"
    repository: https://github.com/RHEcosystemAppEng/agentic-plugins
    path: ocp-admin
    icon: "..."
    tags: [openshift, security, cve]
```

### Distribution: the bootstrap pattern

redhat.com/en/agentic-skills uses a novel "distribution-via-prompt"
pattern: users copy a prompt into their AI agent, the agent reads the
page, downloads a bootstrap skill from GitHub, invokes
`/red-hat-get-started`, and the bootstrap fetches remaining skills then
self-deletes. This bypasses traditional package managers entirely.

### The openshift/agentic-skills repo

A separate repo (**openshift/agentic-skills**) exists with skills for
OpenShift Container Platform tied to Red Hat OpenShift Lightspeed. It
contains cluster-update, documentation, and find-token skills. Ships as
a container image. No visible connection to RHEcosystemAppEng/
agentic-plugins. This is a third independent skills source, adding to
the fragmentation picture.

Source: https://github.com/openshift/agentic-skills

## 4. Upstream developments since 2026-07-23

### 4.1 Kubeflow hub: skills catalog is now real (major update)

**The first-mover window from 01-upstream has closed.** The skills
catalog is now being built. Key merged PRs:

| PR | Title | Date | Author |
|---|---|---|---|
| [#2973](https://github.com/kubeflow/hub/pull/2973) | KEP-0005: Skills Catalog proposal | Jul 27 | rareddy (Red Hat) |
| [#3015](https://github.com/kubeflow/hub/pull/3015) | Skill Catalog OpenAPI spec + codegen (SKC-101) | Jul 28 | rareddy |
| [#3040](https://github.com/kubeflow/hub/pull/3040) | Scaffold skill plugin and boot (SKC-103) | Jul 31 | rareddy |
| [#3041](https://github.com/kubeflow/hub/pull/3041) | SKILL.md parser (SKC-104) | Jul 31 | rareddy |
| [#2975](https://github.com/kubeflow/hub/pull/2975) | Agent catalog source creation skill | Jul 20 | lugi0 |

Related infrastructure PRs (Al-Pragliola):
- [#2794](https://github.com/kubeflow/hub/pull/2794) (Jun 9) --
  skill chain for scaffolding catalog plugins
- [#2865](https://github.com/kubeflow/hub/pull/2865) (Jun 22) --
  align plugin scaffolding with UI-compatible API shape

Tracking issue [#3014](https://github.com/kubeflow/hub/issues/3014)
has 32 tasks for the full implementation.

KEP-0005 architecture:
- **New source type**: `git-skills-plugin` (alongside existing yaml, hf)
- **API base**: `/api/skill_catalog/v1alpha1`
- **Endpoints**: list skills, get skill, filter options, plus
  `/claude/marketplace.json` (per-consumer namespace)
- **No artifact entities** -- skills have no downloadable weights,
  only SKILL.md body stored as `readme`
- **Identity**: `(repository, path)` + version from git refs
- **Trust tiers**: platformProvided, partnerVerified,
  organizationApproved, communityContributed (labels, not enforced)
- **Version strategy**: git refs (tags/releases/commits), not semver
- **Parser model**: lenient -- missing description skips the skill,
  name mismatches warn but load, unknown fields ignored

### 4.2 agentskills.io spec

The spec remains at its original form with no version number. The
repository (github.com/agentskills/agentskills, Apache 2.0 code +
CC-BY-4.0 docs) has 130 commits, 34 open issues, 22 open PRs, but
no formal releases. The two required fields (`name`, `description`)
and four optional fields (`license`, `compatibility`, `metadata`,
`allowed-tools`) are unchanged from 01-upstream.

The governance position within AAIF has not materialized into a formal
governance structure for agentskills.io specifically. AAIF's public
roadmap focuses on MCP v2, A2A, and AGENTS.md v1.0 -- agentskills.io
is not listed as a tracked workstream. Anthropic remains the de facto
steward.

### 4.3 Agent ecosystem growth

The 01-upstream figure of "6 native agents, 40+ total" has grown
significantly. The agentskills.io client showcase now lists 40+
agents with native SKILL.md support, including major additions:
- GitHub Copilot (VS Code integration)
- Google Gemini CLI
- JetBrains Junie
- AWS Kiro
- OpenAI Codex
- Databricks Genie Code
- Snowflake Cortex Code

The total number of agents consuming SKILL.md (natively or via
installer) is estimated at 70+.

### 4.4 skills CLI (Vercel)

The `skills` CLI (`vercel-labs/skills`) has evolved from v1.0
(Jan 2026) to v1.5.21 (Jul 2026). Key additions since 01-upstream:
- `npx skills find` -- interactive fzf-style search (v1.1.1)
- 410,000+ total installs through the CLI
- skills.sh web directory and leaderboard launched
- 27+ officially supported agents

The 20K+ stars figure from 01-upstream remains roughly current. No
breaking changes to the CLI interface.

### 4.5 MLflow: RFC-0008 superseded, #22833 filed

The MLflow RFC-0008 referenced in 01-upstream (PR #26, Bill Murdock,
PackageManagerPlugin interface) appears to have been superseded by a
more focused approach. Issue
[#22833](https://github.com/mlflow/mlflow/issues/22833) (filed
2026-04-23, jwm4) proposes **skill registry primitives** as a
governed, metadata-first registry within MLflow.

Key design points:
- Stores metadata + typed source pointers (Git repos, OCI registries,
  ZIP archives), not skill artifacts directly
- Lifecycle states: draft, published, deprecated, retired
- Skill groups for organizing related skills
- Builds on MCP Server Registry pattern (#22625)
- Explicit RHOAI requirements: multi-tenancy isolation, security scan
  tracking, OCI distribution support
- Detailed design deferred to mlflow/rfcs (not yet published)

Additionally, **mlflow/skills** is a new repo providing MLflow-specific
agent skills (instrumenting-with-mlflow-tracing, agent-evaluation,
etc.). This is a skills pack, not a registry implementation.

Source: https://github.com/mlflow/skills

### 4.6 Security: the trust crisis

The 01-upstream document identified trust as an important concern. The
situation has become a full crisis:

**Snyk ToxicSkills study** (Feb 2026): Scanned 3,984 skills from
ClawHub and skills.sh.
- 36.8% contain at least one security flaw
- 13.4% have critical-level issues (malware, prompt injection, secrets)
- 76 confirmed malicious payloads (credential theft, backdoors,
  data exfiltration)
- 91% of malicious skills combine prompt injection with traditional
  malware
- 10.9% contain hardcoded secrets

Source: https://snyk.io/blog/toxicskills-malicious-ai-agent-skills-clawhub/

**Industry responses**:
- **NVIDIA** shipped Verified Agent Skills (May 2026): SkillSpector,
  skill cards, cryptographic signing
- **Snyk + Tessl** partnership: automated security scoring in the
  Tessl Registry
- **OWASP** published Agentic Skills Top 10 (Apr 2026)
- **SkillSieve** (arxiv 2604.06550): academic framework for malicious
  skill detection

This validates KEP-0005's trustTier model and makes the
`platformProvided` tier (curated, scanned, Red Hat-owned) a significant
differentiator vs. community registries.

## 5. Format gap analysis and recommendations

### For catalog ingestion of EX skills

The Kubeflow hub SKILL.md parser (SKC-104) will parse EX skills
correctly -- `model` and `color` will be silently ignored as unknown
fields (warns, loads). But this means the risk-tier and model-selection
information is lost.

**Recommendation**: EX should migrate `model` and `color` under the
`metadata:` map for spec compliance. The Kubeflow hub parser already
passes `metadata` through, so the information would be preserved and
available for UI rendering (e.g., color-coded risk badges).

### For the RHOAI catalog surface

The catalog needs to define how EX pack-level metadata
(collection.yaml) maps to the hub's source configuration. Today:
- EX maturity (GREEN/ORANGE) -> hub trustTier (platformProvided)
- EX tags -> hub labels
- EX sample_workflows -> hub customProperties (or ignored)
- EX deploy_and_use -> hub (no equivalent, would need customProperties)

### For MLflow registry handoff

Issue #22833's skill group concept maps well to EX's pack concept. The
catalog-to-registry handoff from 01-upstream (user-initiated pull)
remains viable. The `metadata-first` approach in #22833 means the
registry would store pointers to skills the catalog has already indexed.

## Key findings

1. **The first-mover window has closed, but in the best way**: KEP-0005
   merged in kubeflow/hub (Jul 27-31), with SKILL.md parser,
   OpenAPI spec, and plugin scaffold all landed. Red Hat (rareddy) is
   the author. The skills catalog is the fourth catalog type, as
   predicted by 01-upstream.

2. **EX agentic-collections format is 90% spec-compliant**: The two
   required fields and allowed-tools follow the agentskills.io spec.
   The `model` and `color` fields are the only divergence -- top-level
   instead of under `metadata:`. Migration is trivial.

3. **Three independent Red Hat skill sources exist with no
   consolidation**: RHEcosystemAppEng/agentic-plugins (EX, 7 packs,
   68 skills), openshift/agentic-skills (Lightspeed-tied, 3 skills),
   and opendatahub-io/ai-helpers (ODH, Claude Code marketplace). The
   Kubeflow hub catalog can federate all three, but someone needs to
   configure the source file.

4. **catalog.redhat.com/en/ai and the RHOAI skills catalog are
   parallel surfaces with duplication risk**: The Ecosystem Catalog
   publishes from the agentic-catalog build pipeline; the RHOAI catalog
   will read the same git repos directly. Scope separation
   (Ecosystem = Red Hat-authored only, RHOAI = all tiers) is the
   cleanest resolution.

5. **The security landscape has shifted fundamentally**: Snyk
   ToxicSkills found 36% of community skills contain flaws, 76
   confirmed malicious. This makes the curated `platformProvided` tier
   a critical trust differentiator. The RHOAI catalog's value
   proposition is not just discovery but trust.

6. **MLflow skill registry is further out than expected**: RFC-0008
   was superseded by issue #22833 (Apr 2026), which defers the
   detailed design to a future RFC. The catalog-to-registry handoff
   design can proceed but should not block on MLflow timelines.

7. **The agentskills.io spec is stable but ungoverned**: No version
   number, no formal releases, AAIF does not list it as a tracked
   workstream. The spec is a de facto standard maintained by
   Anthropic, not a de jure standard with governance. This is fine
   for now but creates long-term risk if a competing spec emerges.

8. **EX design principles (DP1-DP7) are a quality framework the
   catalog should surface**: The risk-tier color coding, mandatory
   HITL requirements, and dependency declarations are valuable metadata
   for catalog users. These should map to searchable/filterable
   attributes in the hub UI, not be silently dropped by the parser.
