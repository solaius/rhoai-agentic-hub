---
title: "Skills Catalog research -- upstream refresh: NVIDIA skills lifecycle"
description: "Full reverse-engineering of NVIDIA's end-to-end skills lifecycle: hourly sync from 35+ product repos via components.d onboarding, 3-defense signature drift detection, 4-artifact compliance gate (skill.oms.sig + skill-card.md + evals.json + BENCHMARK.md), NVSkills-CI bot-driven signing, SkillSpector 64-pattern scanning, Skill Evaluator 3-tier eval (static/dedup/agent-based with 5 benchmark dimensions), AI-enriched marketplace metadata generation, SemVer auto-bump plugin packaging, and multi-marketplace syndication (Claude/Codex/Cursor plugins + ClawHub + Skills.sh)"
timestamp: 2026-08-06
lens: upstream
review_after: 2026-11-06
supersedes_context: "Deepens upstream coverage from 01/08 with full NVIDIA lifecycle reverse-engineering"
---

# NVIDIA skills lifecycle -- end-to-end reverse engineering

This document reverse-engineers NVIDIA's complete skills lifecycle pipeline
from source code inspection of [NVIDIA/skills](https://github.com/NVIDIA/skills)
(2.8K stars, Apache 2.0 + CC-BY-4.0) as of 2026-08-06. The prior upstream
research ([08-upstream-refresh](/components/skills-catalog/research/08-upstream-refresh.md))
described WHAT NVIDIA has; this document describes HOW IT WORKS, step by
step, as a lifecycle.

Sources: all `.github/workflows/*.yml`, `.github/scripts/*.py`,
`components.d/`, `plugins.d/`, `docs/*.mdx`, `CONTRIBUTING.md`,
`CHANGELOG.md`, `CODEOWNERS`, and the PR template from the NVIDIA/skills
repository, plus NVIDIA's published documentation at
[docs.nvidia.com/skills](https://docs.nvidia.com/skills) and the
[NVIDIA technical blog](https://developer.nvidia.com/blog/nvidia-verified-agent-skills-provide-capability-governance-for-ai-agents/).


## 1. Product team onboarding

### The `components.d/` model

Onboarding is self-serve. A product team opens a single PR adding one YAML
file: `components.d/<slug>.yml`. The per-file layout means concurrent
onboarding PRs from different teams never touch the same file, eliminating
merge conflicts at scale.

Source: [`components.d/README.md`](https://github.com/NVIDIA/skills/blob/main/components.d/README.md)

### Required fields

| Field | Type | Description |
|---|---|---|
| `name` | string | Display name (e.g., `CUDA-Q`, `Nemotron Voice Agent`) |
| `repo` | string | GitHub repository (`owner/repo`) |
| `description` | string | One-line description for the README |
| `skills` | list | Skill source locations (one entry per skill) |

Each `skills` entry requires:

| Field | Type | Description |
|---|---|---|
| `path` | string | Directory in the source repo containing `SKILL.md` |
| `catalog_dir` | string | Unique top-level name under `skills/` in the catalog |

Optional fields: `ref` (default `main`), `links.contributing`, `links.discussions`, `links.security`.

### Concrete example

```yaml
# components.d/aiq.yml
name: AIQ
repo: NVIDIA-AI-Blueprints/aiq
ref: develop
description: NVIDIA AI-Q Blueprint - deploy local AI-Q services and run research workflows.
skills:
  - path: skills/aiq-research/
    catalog_dir: aiq-research
  - path: skills/aiq-deploy/
    catalog_dir: aiq-deploy
```

Source: [`components.d/aiq.yml`](https://github.com/NVIDIA/skills/blob/main/components.d/aiq.yml)

### Approval process

The PR template enforces author affirmations:

1. Skills cleared for open-source release per NVIDIA's internal IP review (six-question check).
2. License selected: Apache 2.0 / CC-BY 4.0 / dual.
3. No new license or third-party component beyond what the source repo carries.
4. Source repo is public and under an NVIDIA-owned GitHub org.

The Verify Authors workflow blocks PRs with non-`@nvidia.com` committer
emails (reviewed external contributors can be allowlisted in
`.github/external-contributors.yml`, scoped to specific PR numbers, and
read from the base branch so a PR cannot allowlist itself). DCO sign-off is
enforced by the `dco.yml` workflow.

Three CODEOWNERS (`@mosheabr @sayalinvidia @jasonnvidia`) must approve. The
reviewer checklist includes validating the `components.d` entry, sampling
SKILL.md frontmatter compliance, and confirming no new OSRB filing is needed.

Source: [`.github/PULL_REQUEST_TEMPLATE.md`](https://github.com/NVIDIA/skills/blob/main/.github/PULL_REQUEST_TEMPLATE.md),
[`verify-authors.yml`](https://github.com/NVIDIA/skills/blob/main/.github/workflows/verify-authors.yml),
[`.github/CODEOWNERS`](https://github.com/NVIDIA/skills/blob/main/.github/CODEOWNERS)

### Timeline

From the CHANGELOG, initial onboarding (v0.1.0, 2026-03-23) took 4 product
repos with 24 skills. Within 5 months the catalog grew to 35+ product teams
and 300+ skills. A new component is typically available in the catalog within
one sync cycle (up to 1 hour) after its onboarding PR merges.

Source: [`CHANGELOG.md`](https://github.com/NVIDIA/skills/blob/main/CHANGELOG.md)

### Deprecated bulk layout

An older "bulk" pattern where one `skills[]` entry pointed at a parent
directory with many skills is deprecated. New components must use the flat
layout (one entry per skill, each landing at its own top-level `skills/<dir>/`).
Existing bulk components are migrated incrementally.


## 2. Skill authoring lifecycle

### Required artifacts per skill

Every catalog skill must ship four artifacts. The sync pipeline drops any
skill missing any of them:

| Artifact | Purpose |
|---|---|
| `SKILL.md` | Skill definition with YAML frontmatter (agentskills.io spec) |
| `skill.oms.sig` | Detached NVIDIA OMS signature (Sigstore bundle) |
| `skill-card.md` | Human-readable metadata card (owner, license, risks, output shape) |
| `evals.json` | Tier-3 evaluation dataset (NV-ACES format) |

A `BENCHMARK.md` file capturing evaluation results is also expected for
publication. The compliance gate accepts eval data in several forms:
`evals/evals.json` (canonical), any `*.json` under `evals/` or `eval/`,
or `evals.json` anywhere in the skill directory tree.

Source: [`sync-skills.yml` compliance step](https://github.com/NVIDIA/skills/blob/main/.github/workflows/sync-skills.yml),
[`docs/agent-skill-trust-pipeline.mdx`](https://github.com/NVIDIA/skills/blob/main/docs/agent-skill-trust-pipeline.mdx)

### Recommended source directory path

Product repos should keep skills in `skills/` at the repo root as
first-class artifacts. `.agents/skills/` is for installed/runtime skills.
Agent-specific paths (`.claude/skills/`, `.codex/skills/`) are discouraged
for new entries to avoid duplication.

Source: [`CONTRIBUTING.md`](https://github.com/NVIDIA/skills/blob/main/CONTRIBUTING.md)

### Release gate sequence

The documented order for NVIDIA-Verified skills:

1. Author the skill with narrow purpose, clear triggers, explicit permissions.
2. Run SkillSpector against the complete skill directory.
3. Fix high-risk findings or record why a finding is accepted.
4. Complete the skill card.
5. Sign the skill directory, publishing `skill.oms.sig`.
6. Consumers/CI verify the signature before installation.

Source: [`docs/agent-skill-trust-pipeline.mdx`](https://github.com/NVIDIA/skills/blob/main/docs/agent-skill-trust-pipeline.mdx)


## 3. The sync pipeline (reverse-engineered)

### Trigger and frequency

The sync runs **hourly** (`cron: "0 * * * *"`) and can be manually triggered.
It uses a `SKILLS_SYNC_PAT` secret with read access to all product repos.

Source: [`sync-skills.yml`](https://github.com/NVIDIA/skills/blob/main/.github/workflows/sync-skills.yml)

### Step-by-step pipeline

The sync is a single job with 13 sequential steps:

**Step 1: Aggregate components.d**
```bash
yq ea '[.] | {"components": .}' components.d/*.yml > /tmp/components.aggregated.yml
```
Per-file YAML is merged into a single config for iteration.

**Step 2: Clone and rsync** -- For each component, the workflow:
- Shallow-clones the source repo with sparse checkout
- Captures upstream HEAD SHA/date for version tracking
- Copies each skill path to its catalog directory via `rsync -a --delete`
- Records which components synced and which have diffs

**Step 3: Fail if nothing synced** -- Hard failure if all component clones failed.

**Step 4: Detect signature drift (3-defense model)**

This is the most sophisticated step. It scans every rsynced skill directory
for three failure modes:

| Defense | Condition | Existing skill | New skill |
|---|---|---|---|
| Defense 1: sig missing | No `skill.oms.sig` at all | **Revert** to HEAD (preserves prior signed version) | **Drop** outright |
| Defense 2: sig drift | Content changed but `skill.oms.sig` unchanged | **Revert** to HEAD | **Drop** outright |
| Defense 3: sig mismatch | Signature refreshed but content hashes don't match | **Revert** to HEAD | **Drop** outright |

Defense 3 includes an inline Python script that parses the DSSE/in-toto
payload from the Sigstore bundle and compares sha256 digests of every
signed resource against the on-disk files. This catches pipeline ordering
faults where skill files are edited after the signing run.

**Step 5: Enforce skill compliance** -- Scans all `SKILL.md` files via `find`.
Drops any skill missing: `skill.oms.sig`, `skill-card.md`, or eval data.
Also drops orphan product directories with no `SKILL.md` inside.

**Step 6: Prune orphaned skill dirs** -- Runs `prune-orphans.sh`: removes
`skills/` directories whose `components.d` registration was removed. Safety
cap of 5 deletions per run; exceeding it triggers human triage. Exceptions
listed in `catalog-exceptions.yml` are preserved.

**Step 7: Resolve skill contacts** -- For each dropped/reverted skill, resolves
the original onboarder via `git blame` on the owning `components.d/*.yml`,
then maps the author email to a GitHub login via the GitHub user search API.
Results are cached in-memory across the run.

**Step 8: Track dropped skills** -- Opens or updates a rolling GitHub issue
(label: `missing-compliance`) with a categorized breakdown: missing artifacts,
signature drift, signature mismatch, signature missing, orphan product dirs.
Each entry includes a cc to the resolved contact. Assignees are set via the
`CATALOG_TRACKER_ASSIGNEES` secret. Auto-closes when all skills are compliant.

**Step 9: Ping skill owners for new drops** -- Posts a comment on the tracker
issue tagging contacts for skills dropped for the first time in this run
(avoids repeat pings on subsequent cycles).

**Step 10: Rebuild plugin catalog** -- Runs `build-plugins.sh` to regenerate
the `plugins/` tree and marketplace JSONs from the updated `skills/`.

**Step 11: Auto-bump plugin versions** -- Runs `version-plugins.sh --apply`
to SemVer-bump any plugin whose content moved (z for in-place edits,
y for structural changes).

**Step 12: Regenerate README tables** -- Runs `regenerate-readme.sh`.

**Step 13: Recompute changed components after reverts** -- Recalculates
the changed-components list from the working tree (since drift and compliance
steps may have reverted some changes), builds a title under 256 characters,
and opens a PR via `peter-evans/create-pull-request`.

### Failure tracking

A separate `actions/github-script` step maintains a rolling `sync-failure`
labeled issue. It auto-updates on each failing sync and auto-closes when
sync runs cleanly again.

Source: [`sync-skills.yml`](https://github.com/NVIDIA/skills/blob/main/.github/workflows/sync-skills.yml)


## 4. SkillSpector scanning in detail

### Scope and capabilities

[SkillSpector](https://github.com/NVIDIA/SkillSpector) is an open-source
scanner (Apache 2.0) that detects vulnerabilities, malicious patterns, and
policy risks in AI agent skills. It accepts Git repositories, URLs, zip
files, directories, and single files.

Source: [`docs/scanning-agent-skills.mdx`](https://github.com/NVIDIA/skills/blob/main/docs/scanning-agent-skills.mdx),
[SkillSpector README](https://github.com/NVIDIA/SkillSpector/blob/main/README.md),
[Help Net Security coverage](https://www.helpnetsecurity.com/2026/08/03/skillspector-open-source-agent-skill-security-scanner/)

### Vulnerability categories (64 patterns, 16 categories)

| Category | What it catches |
|---|---|
| Prompt injection | Hidden instructions, invisible characters, encoding tricks |
| Data exfiltration | Network sends of sensitive data, clipboard hijacking |
| Privilege escalation | Sudo, root access, permission manipulation |
| Supply-chain issues | Vulnerable dependencies (OSV.dev lookup), typosquatting |
| Excessive agency | Overbroad permissions, underdeclared capabilities |
| Output handling | Unsafe output processing, injection via output |
| System prompt leakage | Extraction of system prompts or agent configuration |
| Memory poisoning | Contamination of agent memory or conversation history |
| Tool misuse | Unauthorized tool invocation, tool chaining exploits |
| Rogue-agent behavior | Agent self-modification, goal hijacking |
| Trigger abuse | Overly broad or hidden activation triggers |
| Dangerous code (AST) | exec, eval, subprocess, dynamic imports |
| Taint tracking | Environment variables/file contents flowing to network sinks |
| YARA signatures | Known malware patterns |
| MCP least privilege | MCP servers requesting excessive permissions |
| MCP tool poisoning | Tool description manipulation to alter agent behavior |

### Two analysis modes

| Mode | Speed | How it works |
|---|---|---|
| Static (default) | Seconds | AST walk, taint tracker, YARA, string matching, dependency audit |
| Semantic (opt-in) | Minutes | LLM compares claimed purpose vs actual behavior; ~87% precision |

Semantic analysis requires an OpenAI-compatible endpoint. Configure via
`SKILLSPECTOR_PROVIDER` and `OPENAI_API_KEY` environment variables.

### Risk scoring

| Score range | Label | Action |
|---|---|---|
| 0-20 | LOW (SAFE) | Install |
| 21-50 | MEDIUM (CAUTION) | Review findings |
| 51-80 | HIGH | Do not install |
| 81-100 | CRITICAL | Do not install |

Points per finding: CRITICAL +50, HIGH +25, MEDIUM +10, LOW +5.

### Output formats

Terminal (interactive), JSON (automation), Markdown (review packets), SARIF
(CI/code scanning systems).

### Triage policy

| Finding type | Recommended action |
|---|---|
| Critical or high severity | Block release until fixed or formally accepted |
| Hidden instructions or tool poisoning | Remove hidden content |
| Underdeclared capability | Update permissions or remove behavior |
| Known vulnerable dependency | Upgrade, pin fixed version, or document acceptance |
| Description-behavior mismatch | Rewrite description or change code |


## 5. Skill Evaluator (NVSkills-Eval) -- 3-tier evaluation

The evaluation system is referenced as "Skill Evaluator" in BENCHMARK.md
files and as "NVSkills CI" in the workflow infrastructure. It is an
internal NVIDIA system (not open-sourced) that runs via the `nv-skills-ci[bot]`
service account. Source repos trigger it by commenting `/nvskills-ci` on a PR.

Source: [`request-nvskills-ci.yml`](https://github.com/NVIDIA/skills/blob/main/.github/workflows/request-nvskills-ci.yml),
[`require-nvskills-status.yml`](https://github.com/NVIDIA/skills/blob/main/.github/workflows/require-nvskills-status.yml),
[`BENCHMARK.md` examples](https://github.com/NVIDIA/skills/blob/main/skills/nvidia-skill-finder/BENCHMARK.md)

### Tier 1: Static validation

Automated structural checks on the skill directory:

- Schema compliance of `SKILL.md` frontmatter
- Presence of recommended sections (`## Examples`)
- Author format validation (`Name <email@host>`)
- Unexpected files in skill root
- File structure conformance

Findings are categorized as MEDIUM or LOW severity. Tier 1 "passed with
observations" is the expected outcome -- it flags issues but does not
block publication for LOW/MEDIUM findings.

### Tier 2: Deduplication

Checks for duplicate or near-duplicate skills in the catalog. Prevents
the same skill from being published under different names or by different
teams. Often reports "not run or did not produce findings" when the skill
is clearly unique.

### Tier 3: Agent-based evaluation

The most substantive tier. Runs the skill against real agent harnesses
with a dataset of evaluation tasks (`evals/evals.json`).

**Dataset structure** (from the nvidia-skill-finder example):

```json
{
  "id": "nvidia-skill-finder-pos-vehicle-routing",
  "question": "I need to solve a vehicle routing problem...",
  "expected_skill": "nvidia-skill-finder",
  "expected_script": null,
  "ground_truth": "The agent identifies Decision Optimization...",
  "expected_behavior": [
    "Treats vehicle routing as a strong NVIDIA Decision Optimization signal",
    "Checks the live NVIDIA catalog before naming a specific skill",
    "Recommends a cuOpt routing-related skill if present",
    "Asks before installing the skill"
  ]
}
```

Tasks are classified as positive (skill should activate) or negative (skill
should not activate). The nvidia-skill-finder dataset has 17 tasks: 12
positive, 5 negative.

**Five benchmark dimensions:**

| Dimension | What it measures |
|---|---|
| Security | Avoids unsafe behavior (secret leakage, destructive commands, unauthorized access) |
| Correctness | Follows expected workflow, produces correct final output |
| Discoverability | Loads the skill when relevant, avoids it when irrelevant |
| Effectiveness | Measurably better performance with skill than without |
| Efficiency | Fewer tokens, avoids redundant work |

**Underlying evaluation signals:**

| Signal | Maps to dimension |
|---|---|
| `security` | Security |
| `skill_execution` | Skill Execution (agent loaded expected skill and workflow) |
| `skill_efficiency` | Efficiency (routing quality, decoy avoidance) |
| `accuracy` | Correctness (final-answer correctness vs reference) |
| `goal_accuracy` | Effectiveness (overall task completion) |
| `behavior_check` | Correctness (expected behavior steps, safety expectations) |

**Results format** (from nvidia-skill-finder BENCHMARK.md):

| Dimension | Num | Score (uplift vs baseline) |
|---|---|---|
| Security | 17 | 100% (+0%) |
| Correctness | 17 | 100% (+24%) |
| Discoverability | 17 | 100% (+50%) |
| Effectiveness | 17 | 99% (+52%) |
| Efficiency | 17 | 86% (+38%) |

A pass threshold of 50% is configured. Overall verdict is PASS/FAIL.

### NVSkills-CI signing flow

When Tier 3 passes, the `nv-skills-ci[bot]` service account pushes a
generated commit containing: `BENCHMARK.md`, `skill-card.md`,
`skill.oms.sig`, and optionally `skill-card-review-needed.md`. This commit
has a specific title (configurable via `NVSKILLS_SIGNATURE_COMMIT_TITLE`,
default: "Attach NVSkills validation signatures").

The `require-nvskills-status.yml` workflow enforces that PRs touching
`skills/`, `team-skills/`, `rules/team-rules/`, or `plugins/` have a
successful `NVSkills CI` status. It polls the status API for up to 55
minutes (configurable), with a 2-minute grace period for the status to
appear.

Bot-managed branches (`automated/sync-skills`, `bot/regenerate-skill-metadata`)
are exempt from this requirement.

Source: [`require-nvskills-status.yml`](https://github.com/NVIDIA/skills/blob/main/.github/workflows/require-nvskills-status.yml)


## 6. Skill card generation

### The Skill Card Generator

A separate tool published at
[NVIDIA/Trustworthy-AI](https://github.com/NVIDIA/Trustworthy-AI/blob/main/Skill%20Card.md)
walks through each section interactively. It is also registered in the
skills catalog itself at `components.d/skill-card-generator.yml`.

Source: [`docs/skill-cards.mdx`](https://github.com/NVIDIA/skills/blob/main/docs/skill-cards.mdx)

### Skill card sections

| Section | Question it answers |
|---|---|
| Description | What does this skill do in one sentence? |
| Owner | Who is accountable? |
| License/Terms | What rules govern use and redistribution? |
| Use Case | Who should use it, and for what purpose? |
| Deployment Geography | Where is it intended to be used? (Global/regional/country) |
| Requirements/Dependencies | API keys, external credentials, runtime deps? |
| Known Risks and Mitigations | What could go wrong, and how is risk reduced? |
| References | Docs, papers, scan reports, model cards |
| Skill Output | Type, format, parameters, side effects |
| Evaluation Agents Used | Which agent harnesses were used for Tier 3 |
| Evaluation Tasks | Dataset size, positive/negative split |
| Evaluation Metrics Used | Benchmark dimensions and underlying signals |
| Evaluation Results | Per-dimension scores with uplift vs baseline |
| Skill Version | Version, release tag, or signing identifier |
| Ethical Considerations | Governance, misuse concerns, industry constraints |

### Generation vs manual authoring

The NVSkills-CI pipeline generates `skill-card.md` and `BENCHMARK.md`
automatically from the Tier 3 evaluation results. The generated card
includes the evaluation metrics, agent names, results table, and version
automatically populated from the eval run. Human-authored sections
(description, risks, references) are either extracted from existing
`SKILL.md` content or flagged for manual completion via a
`skill-card-review-needed.md` marker file.

### Approval rule

A skill card is complete when a reviewer can understand the skill's purpose,
owner, output, risks, and release evidence without opening the source code.

Source: [`docs/skill-cards.mdx`](https://github.com/NVIDIA/skills/blob/main/docs/skill-cards.mdx)


## 7. OMS signing flow

### When signing happens

Signing occurs after scanning and evaluation pass. The exact sequence:

1. SkillSpector scan completes
2. Tier 1-3 evaluation passes
3. Skill card is generated
4. **The exact directory that passed review is signed**
5. `skill.oms.sig` is published at the top level of the skill directory
6. The generated commit (containing BENCHMARK.md + skill-card.md + skill.oms.sig)
   is pushed by `nv-skills-ci[bot]`

### Who holds the keys

The signing certificate is NVIDIA's `nv-agent-root-cert.pem`, distributed
at the repository root. The signing is performed by the `nv-skills-ci[bot]`
service account (configurable via `NVSKILLS_SIGNATURE_PUSH_ACTOR` and
`NVSKILLS_FORK_SERVICE_ACCOUNT_LOGIN` / `NVSKILLS_SIGNATURE_COMMIT_LOGIN`
variables). For fork PRs, the service account (`svc-nvskills-signing`)
must be added as a collaborator with write access.

Source: [`docs/signing-agent-skills.mdx`](https://github.com/NVIDIA/skills/blob/main/docs/signing-agent-skills.mdx),
[`nv-agent-root-cert.pem`](https://github.com/NVIDIA/skills/blob/main/nv-agent-root-cert.pem)

### Signature format

The signature is a Sigstore bundle wrapping a DSSE/in-toto statement. The
statement's `predicate.resources` lists every signed file with its sha256
digest. This enables file-level integrity verification.

### Verification for consumers

```bash
pip install model-signing
model_signing verify certificate SKILL_DIR \
  --signature SKILL_DIR/skill.oms.sig \
  --certificate-chain nv-agent-root-cert.pem
```

### Content integrity enforcement

A daily sweep (`verify-content-integrity.yml`, 07:17 UTC) recomputes
sha256 hashes for every signed file in the catalog and compares them to the
manifest in `skill.oms.sig`. On PRs, it checks only changed skills.
Failures trigger a rolling `integrity-failure` labeled issue that
auto-closes when a sweep passes.

The verification logic (`verify_content_integrity.py`) handles:
- MISSING: file listed in signature but absent on disk
- HASH MISMATCH: file content doesn't match signed digest
- Malformed bundles (treated as real problems)

Source: [`verify-content-integrity.yml`](https://github.com/NVIDIA/skills/blob/main/.github/workflows/verify-content-integrity.yml),
[`.github/scripts/verify_content_integrity.py`](https://github.com/NVIDIA/skills/blob/main/.github/scripts/verify_content_integrity.py)


## 8. Versioning and updates

### Plugin versioning (SemVer)

Plugin versions follow SemVer (`x.y.z`). The `version-plugins.py` script
auto-bumps on each sync:

| Change type | Bump | Trigger |
|---|---|---|
| Content-only (in-place edits) | z (patch) | Auto |
| Structural (skill add/remove, capability change) | y (minor) | Auto |
| Breaking change | x (major) | Builder-only (manual) |

Validation rules for builder-set versions:
- Must be monotonically increasing
- No pre-release tags (must match `^\d+\.\d+\.\d+$`)
- No oversized major skip (e.g., 1.x to 5.x rejected as likely typo)

Source: [`.github/scripts/version-plugins.py`](https://github.com/NVIDIA/skills/blob/main/.github/scripts/version-plugins.py)

### Skill updates

Skills are updated at the source repo. On the next sync cycle (up to 1 hour),
the rsync picks up the changes. However, the sync pipeline enforces that
signature and content stay aligned:

- If content changes without a signature refresh: **reverted** to last
  signed version (existing skill) or **dropped** (new skill)
- Recovery: comment `/nvskills-ci` on a follow-up PR in the source repo

### Deprecation and removal

Removing a skill is handled by deleting its entry from `components.d/<slug>.yml`.
The orphan-pruning step removes the catalog copy on the next sync.
`catalog-exceptions.yml` lists dirs allowed to exist without registration
(e.g., contributor-facing skills, infrastructure skills).

Safety rails on removal:
- Pruning cap of 5 deletions per run (exceeding triggers human triage)
- Parse failure in any `components.d` file skips pruning entirely
- All removals are visible in the sync PR diff

### Changelog

Major releases are tracked in `CHANGELOG.md` following Keep a Changelog
format. Individual skill updates are tracked via the sync PR diffs and
version tables in the README.

Source: [`CHANGELOG.md`](https://github.com/NVIDIA/skills/blob/main/CHANGELOG.md)


## 9. Marketplace syndication

### Plugin architecture

The `plugins.d/` directory defines plugins, built by `build-plugins.py`.
Each plugin gets three agent-specific manifests:

```
plugins/<name>/
  .claude-plugin/plugin.json
  .codex-plugin/plugin.json
  .cursor-plugin/plugin.json
  skills/<skill>/              # symlinks or copies from canonical skills/
  assets/                      # branding (logo)
  README.md
```

Three top-level marketplace registries are also generated:
- `.claude-plugin/marketplace.json` (Claude Code)
- `.agents/plugins/marketplace.json` (Codex)
- `.cursor-plugin/marketplace.json` (Cursor)

Source: [`plugins.d/README.md`](https://github.com/NVIDIA/skills/blob/main/plugins.d/README.md)

### Defaults and overrides

`plugins.d/_defaults.yml` provides shared defaults:

```yaml
version: "1.0.0"
author:
  name: NVIDIA
  url: https://github.com/NVIDIA/skills
homepage: https://build.nvidia.com/skills/
license: Apache-2.0 AND CC-BY-4.0
brand_color: "#76b900"
capabilities:
  - Interactive
  - Write
skill_files: copy  # copy (Codex-compatible) or symlink
```

Per-plugin YAML overrides any default (shallow merge).

### Copy vs symlink modes

| Mode | On disk | Use when |
|---|---|---|
| `copy` (default) | Real files via rsync | Codex/Anthropic publishing (Codex drops symlinks during install) |
| `symlink` | Relative symlinks | Claude-only or `npx skills add` consumers |

### Discovery-first plugin pattern

The primary `nvidia-skills` plugin ships only the `nvidia-skill-finder`
skill -- a catalog router. Rather than bundling all 300+ skills (which
would crowd the limited context space), the finder routes users to any
skill on demand. Individual skills are version-managed independently of the
plugin, so a skill update doesn't force a plugin re-release.

Source: [`plugins.d/nvidia-skills.yml`](https://github.com/NVIDIA/skills/blob/main/plugins.d/nvidia-skills.yml)

### AI-enriched metadata for Skills.sh

The `generate-skill-metadata.py` script produces two catalog-wide files:

- `.github/scripts/marketplace/metadata.json` -- enriched internal metadata
- `skills.sh.json` -- published index for Skills.sh

The pipeline: discover `skills/**/SKILL.md` -> parse YAML frontmatter ->
map to product via `components.d` -> classify against baseline (added/
removed/renamed/changed) -> carry forward existing valid metadata -> AI
enrichment for missing fields (NVIDIA Inference API, strict-JSON,
taxonomy-bound) -> validate against JSON Schema -> emit byte-stable
outputs.

The metadata schema includes controlled taxonomies for product, category,
subdomain, audience, and activity tags. Schema validation uses
Draft 2020-12 JSON Schema.

This workflow fires on PR (check mode, no AI), on manual dispatch
(regenerate with AI), and after each successful sync (post-sync regeneration).

Source: [`.github/scripts/marketplace/generate-skill-metadata.py`](https://github.com/NVIDIA/skills/blob/main/.github/scripts/marketplace/generate-skill-metadata.py),
[`generate-skill-metadata.yml`](https://github.com/NVIDIA/skills/blob/main/.github/workflows/generate-skill-metadata.yml)

### Benchmark aggregation

`aggregate_benchmarks.py` walks `skills/*/BENCHMARK.md`, extracts
evaluation summaries, agents, and per-dimension results (skill-assisted
score + uplift vs baseline), and writes `benchmarks.json` at the repo root.
Supports two report layouts (v1 and v2 from different Skill Evaluator versions).

### ClawHub syndication

The `clawhub-publish.yml` workflow publishes to ClawHub via the
`openclaw/clawhub/.github/workflows/skill-publish.yml` reusable workflow.
Three modes: `dry-run`, `publish-single` (one skill), `publish-catalog`
(all skills). Manual trigger only, requires `CLAWHUB_TOKEN`.

Source: [`clawhub-publish.yml`](https://github.com/NVIDIA/skills/blob/main/.github/workflows/clawhub-publish.yml)

### Syndication targets summary

| Target | Mechanism | Frequency |
|---|---|---|
| Claude Code plugin | `.claude-plugin/marketplace.json` + `plugins/<name>/` | Each sync PR merge |
| Codex plugin | `.agents/plugins/marketplace.json` + `plugins/<name>/` | Each sync PR merge |
| Cursor plugin | `.cursor-plugin/marketplace.json` + `plugins/<name>/` | Each sync PR merge |
| Skills.sh | `skills.sh.json` at repo root | Post-sync metadata regeneration |
| ClawHub | Reusable workflow dispatch | Manual |
| `npx skills add` | Direct repo install (`npx skills add nvidia/skills`) | Live (reads repo) |


## 10. The lifecycle state machine

Based on the reverse-engineered pipeline, a skill passes through these
states:

```
                    [Source Repo]
                         |
                    Author skill
                    (SKILL.md + scripts + references)
                         |
                    Run SkillSpector scan
                         |
                    Fix findings / accept risks
                         |
                    Comment /nvskills-ci on PR
                         |
                  +-------v--------+
                  | NVSkills CI    |
                  | Tier 1: Static |---> findings (MEDIUM/LOW)
                  | Tier 2: Dedup  |---> pass/fail
                  | Tier 3: Agent  |---> PASS/FAIL (5 dimensions)
                  +-------+--------+
                         |
                    [PASS] generates:
                    - BENCHMARK.md
                    - skill-card.md
                    - skill.oms.sig
                         |
                    Merge PR to source repo
                         |
                    [Catalog Sync - hourly]
                         |
              +----------v-----------+
              | Sync Pipeline Gates  |
              | 1. Signature present |
              | 2. Signature fresh   |
              | 3. Signature matches |
              | 4. skill-card.md     |
              | 5. evals.json        |
              +----------+-----------+
                         |
                   [ALL PASS]          [ANY FAIL]
                      |                    |
                Published to           Dropped/Reverted
                skills/<dir>/          (tracker issue opened,
                      |                owner notified)
                      |
              +-------v--------+
              | Post-sync      |
              | - Plugin build |
              | - Version bump |
              | - README regen |
              | - Metadata AI  |
              | - Benchmark agg|
              +-------+--------+
                      |
              Syndicated to:
              Claude / Codex / Cursor / Skills.sh / ClawHub
                      |
              [Live in catalog]
                      |
              +-------v--------+
              | Maintenance    |
              | - Content edit |----> must re-sign (/nvskills-ci)
              | - Removal      |----> delete from components.d
              | - Deprecation  |----> orphan pruning
              +----------------+
```

### State transitions

| From | To | Trigger |
|---|---|---|
| Authored | Under evaluation | `/nvskills-ci` comment on PR |
| Under evaluation | Signed | NVSkills CI PASS + generated commit |
| Under evaluation | Failed | NVSkills CI FAIL |
| Signed | Published | Next sync cycle (up to 1 hour) |
| Signed | Held (drift) | Content changed after signing |
| Published | Updated | Source edit + re-sign + next sync |
| Published | Held (drift) | Source edit without re-sign |
| Published | Removed | `components.d` entry deleted + orphan prune |
| Held (drift) | Published | Re-sign at source + next sync |


## Key findings

1. NVIDIA's sync pipeline runs **hourly** (not daily as previously reported), cloning all 35+ product repos with sparse checkout and rsync, gated by a 3-defense signature drift model that reverts or drops skills when content and signature diverge.

2. Product team onboarding is fully self-serve via a single YAML file in `components.d/`, with the per-file layout specifically designed to eliminate merge conflicts between concurrent onboarding PRs.

3. The compliance gate enforces **four required artifacts** (SKILL.md, skill.oms.sig, skill-card.md, evals.json), not two as the typical "scan + sign" narrative suggests -- evaluation data and skill cards are hard requirements, not optional.

4. NVSkills-CI ("Skill Evaluator") is an **internal, non-open-source NVIDIA system** triggered by `/nvskills-ci` PR comments, running 3-tier evaluation (static schema validation, deduplication, and agent-based eval measuring 5 dimensions: security, correctness, discoverability, effectiveness, and efficiency) and generating the signature commit on success.

5. The signature-integrity enforcement is defense-in-depth: the sync pipeline has 3 inline defenses (missing sig, stale sig, mismatching sig), the `verify-content-integrity.yml` runs a **daily full-catalog sha256 sweep**, and the `require-nvskills-status.yml` gates PRs on successful NVSkills CI status.

6. Plugin versioning is automated via SemVer: z-bumps for content edits, y-bumps for structural changes, with major bumps reserved for manual builder assertion -- all computed from deterministic payload hashing that excludes the version field itself.

7. Marketplace syndication serves **six distinct distribution channels** (Claude Code, Codex, and Cursor plugins via generated marketplace JSONs; Skills.sh via `skills.sh.json`; ClawHub via reusable workflow; `npx skills add` via direct repo access), each rebuilt on every sync PR merge.

8. The "discovery-first" plugin pattern ships only a catalog-router skill (`nvidia-skill-finder`) instead of bundling all 300+ skills, avoiding context-space bloat and decoupling skill versioning from plugin versioning.

9. Skill card generation is semi-automated: the NVSkills-CI pipeline generates evaluation metrics, agent names, and results automatically from the Tier 3 run, while human-authored sections (description, risks, references) are either extracted from SKILL.md or flagged for manual completion via a marker file.

10. The orphan-pruning system has **three safety rails** (parse-failure skip, 5-deletion cap with human-triage overflow, and `catalog-exceptions.yml` for intentionally unregistered dirs), addressing a real operational problem where teams assumed deregistering automatically removed catalog copies.

11. The AI-enriched metadata pipeline (`generate-skill-metadata.py`) uses NVIDIA's own Inference API to fill taxonomy fields (product, category, subdomain, audience, activity tags) for new skills, validating against a controlled JSON Schema with enumerated allowed values -- combining human curation with automated enrichment at scale.

12. For Red Hat's skills catalog integration, the most transferable elements are the `components.d/` onboarding pattern (self-serve, merge-conflict-free), the multi-defense signature verification model, and the 4-artifact compliance gate; the least transferable is NVSkills-CI (internal, NVIDIA-specific) which would need to be replaced with our own evaluation harness.
