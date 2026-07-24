---
title: "Skills Catalog research -- upstream projects and standards"
description: Kubeflow hub 3-catalog pattern (skills would be 4th), agentskills.io AAIF governance (170+ members), SKILL.md cross-agent compatibility (6 native, 40+ total), npx skills CLI ecosystem, MLflow RFC-0008 catalog handoff, ODH repos (ai-helpers already produces skills), no upstream skills catalog exists.
timestamp: 2026-07-23
lens: upstream
review_after: 2026-10-23
---

# Skills Catalog research -- upstream projects and standards

## 1. Kubeflow Hub catalog patterns

kubeflow/hub (Apache-2.0, Go 57% / TypeScript 29%, alpha, v0.3.12) is the
Kubeflow umbrella repo providing a central metadata repository plus a
federated catalog service. Red Hat is the primary maintainer.

Three catalog surfaces are merged:

| Catalog | API prefix | Status |
|---|---|---|
| Model Catalog | `/api/model_catalog/v1alpha1` | Shipped (3.4+) |
| MCP Server Catalog | `/api/mcp_catalog/...` | DP shipped (3.4) |
| Agent Catalog | `/api/agent_catalog/v1alpha1` | Shipped (3.5) |

No skills catalog surface exists yet. A skills catalog would be the
fourth type following the identical pattern.

### What a catalog surface consists of

- **OpenAPI-first REST server** (Go) -- contract in `api/openapi/`
- **Backend RDBMS** (PostgreSQL or MySQL) with extensible ER model
  (ML-Metadata-inspired, generic key-value, typed overlays)
- **CatalogSourceProvider** plugin -- YAML (static) and Hugging Face
  Hub (remote). Configured in `catalog-sources.yaml` with hot-reload.
- **BFF** (Go backend-for-frontend) serving React/PatternFly 6
- **React frontend** as a module in odh-dashboard

### What skills can reuse vs build new

**Reuse**: CatalogSourceProvider interface, customProperties
extensibility, REST API pattern, BFF pattern, PostgreSQL backend,
ConfigMap-based disconnected import.

**Build new**: Git-backed CatalogSourceProvider reading SKILL.md
frontmatter from GitHub repos, skills-specific schema fields (mapping
from agentskills.io spec), trust tier classification logic,
skills-specific filtering, catalog-to-registry handoff API.

## 2. agentskills.io specification

The Agent Skills specification was created by Anthropic (Claude Code
October 2025, open-sourced December 2025) and published at
agentskills.io under Apache 2.0. Governance has migrated to the
**Agentic AI Foundation (AAIF)** under the Linux Foundation, announced
December 9, 2025, with 170+ member organizations. AAIF co-founders:
Anthropic, OpenAI, Block. Platinum members: AWS, Bloomberg, Cloudflare,
Google, Microsoft.

### What the specification defines

Directory structure: `skill-name/SKILL.md` (required) plus optional
`scripts/`, `references/`, `assets/`.

YAML frontmatter fields:

| Field | Required | Constraints |
|---|---|---|
| `name` | Yes | Max 64 chars, lowercase + hyphens |
| `description` | Yes | Max 1024 chars |
| `license` | No | License name or file reference |
| `compatibility` | No | Max 500 chars, environment requirements |
| `metadata` | No | Arbitrary key-value map |
| `allowed-tools` | No | Space-separated pre-approved tools (experimental) |

Progressive disclosure: Discovery (~100 tokens, name+description only)
-> Activation (<5,000 tokens, full SKILL.md) -> Execution (scripts/refs
loaded on demand).

### Implications

Only two fields are required. The catalog must define extended metadata
beyond the spec (trust tier, category, tested agents, source URL,
version). The `metadata` map is the spec-sanctioned extension point.

## 3. SKILL.md standard -- adoption and divergence

40+ products support the standard. 6 major agents parse SKILL.md
natively: Claude Code, Codex CLI, Cursor (2.4+), Cline, Gemini CLI
(0.26+), OpenCode. 50+ additional agents consume via the Vercel
installer. 1.9M public skills indexed by SkillsMP.

### Cross-agent compatibility

| Feature | Claude Code | Codex CLI | Cursor | Gemini CLI | Cline |
|---|---|---|---|---|---|
| Native SKILL.md | Yes | Yes | Yes (2.4+) | Yes (0.26+) | Yes |
| `allowed-tools` parsed | Yes | Best-effort | No | No | No |
| Hooks | Yes | No | No | No | Yes |
| Project skill path | `.claude/skills/` | `.agents/skills/` | `.cursor/skills/` | `.gemini/skills/` | `.cline/skills/` |

**Key divergence**: every agent uses a different directory path. The
Vercel installer resolves this with symlinks. Core SKILL.md is fully
portable; divergence exists only in experimental features.

The catalog should index the spec-standard fields and ignore
agent-specific extensions. Agent compatibility can be inferred from
the `compatibility` field or declared in `metadata`.

## 4. Skills CLI / npx ecosystem

The `skills` CLI (vercel-labs/skills, MIT, 20K+ stars) is the de facto
package manager. Key commands: `add` (install), `find` (search), `list`,
`update`, `use` (one-shot), `init` (scaffold), `remove`. Supports 70+
agents, GitHub shorthands, multi-agent targeting.

The NVIDIA skills catalog is the mature exemplar: skills maintained in
product repos, mirrored daily via automated sync pipeline with
compliance gates (OMS signature, skill card, eval dataset required).
`npx skills add nvidia/skills` for distribution.

The catalog and npx are complementary: catalog handles discovery/
browsing; npx handles installation. The catalog's "acquire" action can
generate `npx skills add` commands.

## 5. MLflow RFC-0008/0009 -- catalog integration points

MLflow has no skills registry today. RFC-0008 (PR #26, Bill Murdock)
proposes metadata-first registry with PackageManagerPlugin interface.
Status: draft, unmerged.

The catalog-to-registry handoff: user browses catalog -> selects skill
-> clicks "Register" -> BFF calls MLflow `register_skill()` -> registry
creates Skill entity + SkillVersion. User-initiated pull, no automated
sync. The catalog can ship independently of the RFC timeline.

## 6. ODH/RHOAI upstream repos

- **opendatahub-io/ai-helpers**: already produces skills in SKILL.md
  format. Categories.yaml registry. Claude Code marketplace plugin.
  Container images published. These are candidates for "Red
  Hat-provided" catalog tier.
- **odh-dashboard**: BFF host for catalog UI modules. Skills would be
  the 10th BFF sidecar.
- **opendatahub-operator**: no skills-specific CRDs or components. The
  catalog would be a catalog service, not a Kubernetes operator.
- **agentic-starter-kits**: agent.yaml manifests indexed into agent
  catalog; same pattern applies for SKILL.md -> skills catalog.

## Key findings

1. **The catalog pattern is well-established**: 3 types already merged,
   skills would be the 4th with the same architecture.
2. **SKILL.md is the right metadata source**: AAIF-governed, 40+ tools.
3. **npx skills is the distribution layer, not a competitor**.
4. **NVIDIA's trust pipeline is the governance model to align with**.
5. **Catalog-to-registry is user-initiated pull, not automated sync**.
6. **No upstream skills catalog exists** -- first-mover opportunity.
7. **ODH already produces skills** (ai-helpers) -- seed content exists.
