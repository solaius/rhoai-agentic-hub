---
title: "Skills Catalog research -- requirements refresh (EX onboarding)"
description: EX-to-RHOAI onboarding pipeline mapped end-to-end, metadata gap analysis reveals 5 missing fields and 8 EX-only fields needing new mapping, Konflux bypass viable for 3.6 TP via Git-backed YAML source provider, curated 30-35 skills recommended from 4 packs, trust tier classification is platformProvided, and 5 of 7 EX packs have Article 50 exposure via interactive agent outputs.
timestamp: 2026-08-02
lens: requirements
review_after: 2026-11-02
supersedes_context: "Updates 07-requirements-refresh (2026-07-30) with EX-to-RHOAI onboarding pipeline, metadata mapping gaps, content curation recommendation, pack readiness, first-party classification, and EU AI Act Article 50 compliance status"
---

# Skills Catalog research -- requirements refresh (EX onboarding)

This document investigates the concrete requirements for bringing Red Hat
Emerging Technology (EX) agentic skills into the RHOAI Skills Catalog.
It updates 07-requirements-refresh (2026-07-30) with the pipeline,
metadata mapping, supply chain gap analysis, curation recommendation,
pack readiness assessment, trust classification, and EU AI Act compliance
status as of August 2, 2026.

## 1. EX-to-RHOAI onboarding pipeline

Bringing EX skills from RHEcosystemAppEng/agentic-collections into a
browseable RHOAI AI Hub catalog entry requires an end-to-end pipeline
with 8 stages. Each stage has concrete prerequisites and decision
points.

### Stage 1: Source selection (human)

Peter Double + EX team select which packs/skills from
agentic-collections enter the RHOAI catalog. Decision criteria:
persona alignment, API dependency viability, disconnected compatibility,
evaluation coverage.

**Decision point**: pack-level or skill-level granularity. The EX
`.catalog/collection.yaml` operates at the pack level. The Kubeflow
hub `Skill` entity operates at the individual skill level.
Recommendation: ingest at skill level (see Section 4).

### Stage 2: Metadata extraction

Each SKILL.md in the selected set has frontmatter that must be mapped
to the Kubeflow hub `Skill` schema (see Section 2 for the full gap
analysis). The `.catalog/collection.yaml` provides pack-level metadata
(categories, personas, sample_workflows, resources) that supplements
individual skill frontmatter.

**Tool**: a script reads SKILL.md frontmatter + collection.yaml and
produces the Kubeflow hub YAML source file entry. This is
straightforward to build -- the mapping is mechanical once field
correspondence is established.

### Stage 3: Content packaging

For 3.6 TP, skills are packaged as entries in a YAML catalog source
file mounted into the catalog pod via ConfigMap (the `type: "yaml"`
CatalogSourceProvider). No OCI packaging required at this stage.

For 3.7+, skills should be packaged as OCI artifacts per the draft
specification (Thomas Vitale, April 2026) and stored in Quay.

**Input**: SKILL.md body (the `readme` field in the Kubeflow schema)
+ supporting files list (`supportingFiles` array -- paths only, not
contents, per schema).

### Stage 4: Quality gate

EX already runs evaluations (eval/ directory covers all 7 packs, with
per-skill report.json + report.md files). The rh-sre/cve-impact
evaluation report demonstrates the structure: Treatment vs Control
trials, pass rate, mean/median reward, Welch's t-test, Fisher's exact
test, and provenance (commit SHA, container image digests).

For 3.6 TP, evaluation results are metadata-only (displayed in the
catalog but not re-run by the catalog pipeline). The catalog consumes
the existing eval/ output. No new evaluation infrastructure required.

**Decision point**: what is the minimum evaluation coverage for
catalog inclusion? Recommendation: every skill entering the catalog
must have at least a report.json with pass rate >= 0.7 across >= 3
trials. rh-sre has 9 of 13 skills evaluated -- the 4 without evals
(fleet-inventory, playbook-executor, remediation-verifier,
job-template-creator) need evaluation runs before catalog inclusion.

### Stage 5: Security scanning

For 3.6 TP without the full Konflux pipeline (see Section 3), minimum
viable scanning is a one-time manual review using SkillSpector against
the selected skills. SkillSpector (Apache 2.0, 64 patterns, 16
categories) can be run as a CI step in the agentic-collections repo
or as a manual audit.

**Decision point**: who runs the scan? If EX runs it in their CI
(they already have pre-commit hooks and `make validate`), the catalog
team consumes the results. If RHOAI runs it, the ProdSec team needs
to own the process.

### Stage 6: Trust tier assignment

Assign the Kubeflow hub `SkillTrustTier` enum value. For EX skills,
this is `platformProvided` (see Section 6 for the full analysis).

### Stage 7: Catalog source configuration

Add entries to the RHOAI `catalog-sources.yaml` (or the downstream
equivalent ConfigMap). For a YAML source provider, this means
authoring the YAML catalog file with all mapped metadata per Stage 2.

For Hugging Face model sources, the catalog supports hot-reloading
of source configuration. The YAML source provider likely supports
the same pattern. Confirm with the catalog team.

### Stage 8: UI verification

Verify that skills render correctly in the AI Hub UI. The Kubeflow
hub SkillCatalogService exposes: List skills, Get skill by ID,
Filter options. The UI BFF (Go backend-for-frontend) and React
frontend must render the Skill entity -- this is PR #2973's scope.

**End-to-end timeline estimate**: Stages 1-3 (metadata mapping +
packaging) = 1-2 sprints. Stage 4 (eval gap fill) = 1 sprint for
missing evals. Stage 5 (security scan) = 1 sprint. Stages 6-8
(configuration + verification) = 1 sprint. Total: 3-5 sprints,
parallelizable to 2-3 sprints if eval gap fill runs concurrently
with metadata work.

## 2. Metadata mapping

The Kubeflow hub catalog.yaml OpenAPI spec (v1alpha1) defines a `Skill`
entity with specific fields. The EX agentic-collections use SKILL.md
frontmatter + collection.yaml for metadata. The mapping analysis below
identifies what aligns, what gaps exist, and what has no counterpart.

### Direct field mapping (EX provides, catalog consumes)

| EX source | EX field | Kubeflow Skill field | Notes |
|---|---|---|---|
| SKILL.md | `name` | `name` | Direct match |
| SKILL.md | `description` | `description` | Direct match |
| SKILL.md | `license` | `license` | Both use SPDX identifiers (e.g., `Apache-2.0`) |
| SKILL.md | `allowed-tools` | `allowedTools` | Array of permitted tool names |
| SKILL.md | body content | `readme` | SKILL.md body becomes the readme Markdown |
| collection.yaml | `provider` | `provider` | `Red Hat` in both cases |

### Catalog needs, EX does not provide (gaps)

| Kubeflow Skill field | Type | What it needs | How to fill |
|---|---|---|---|
| `source_id` | string | Catalog source identifier | Assigned by catalog configuration (e.g., `ex-agentic-skills`) |
| `category` | string | Classification category | Map from collection.yaml `categories` (e.g., "Site Reliability", "Security") |
| `trustTier` | SkillTrustTier enum | One of: platformProvided, partnerVerified, organizationApproved, communityContributed | Assign `platformProvided` for all EX skills |
| `labels` | string array | Discovery labels/tags | Derive from collection.yaml `keywords` + `personas` |
| `version` | string | Git ref (tag, release, commit) | Use the agentic-collections release tag (ZIP files published per release) |
| `resolvedCommit` | string | Exact commit SHA | Capture at catalog build time from the Git source |
| `repository` | string (URI) | Upstream Git repository URL | `https://github.com/RHEcosystemAppEng/agentic-collections` |
| `path` | string | Directory containing SKILL.md | e.g., `rh-sre/skills/cve-impact` |
| `compatibility` | string | Supported clients/versions | Not in EX frontmatter; derive from collection.yaml `marketplaces` (Claude Code, Cursor) |

### EX provides, catalog has no direct field (unmapped EX metadata)

| EX field | Source | Value example | Disposition |
|---|---|---|---|
| `model` | SKILL.md frontmatter | `inherit`, `sonnet`, `haiku` | Store as `customProperties.model` (MetadataStringValue) |
| `color` | SKILL.md frontmatter | `cyan`, `blue`, `red` | Store as `customProperties.color`; useful for UI rendering and risk indication |
| `user_invocable` | SKILL.md frontmatter | `true`/`false` | Store as `customProperties.user_invocable` (MetadataBoolValue) |
| `maturity` | collection.yaml | `GREEN`/`ORANGE` | Store as `customProperties.maturity`; ORANGE skills should NOT enter the catalog |
| `personas` | collection.yaml | `["Site Reliability Engineer"]` | Store as `labels` (already mapped above) |
| `marketplaces` | collection.yaml | `["Claude Code", "Cursor"]` | Store as `customProperties.marketplaces` |
| `support_level` | collection.yaml | `Unknown` | Store as `customProperties.support_level` |
| `sample_workflows` | collection.yaml | Named workflow sequences | No catalog equivalent; include in readme or omit |
| `skills_decision_guide` | collection.yaml | Intent-to-skill routing | No catalog equivalent; agent routing concern, not catalog concern |

### Metadata mapping verdict

The gap is manageable. Of 5 fields the catalog needs that EX does not
directly provide, 4 (source_id, trustTier, version, resolvedCommit) are
assigned at catalog build time, not authored by skill developers. Only
`compatibility` requires a new derivation step. The 8 EX-only fields
map cleanly to `customProperties` (the Kubeflow hub extensibility
mechanism), with `maturity: ORANGE` serving as a pre-catalog gate
filter.

### supportingFiles handling

The Kubeflow `Skill` schema includes `supportingFiles` (string array
of companion file paths, contents NOT stored in catalog). EX skills
have extensive supporting files: `references/` directories with flow
documents, parsers, templates, and embedded docs. These paths should
be listed in `supportingFiles` for provenance tracking, but the files
themselves are not catalog content -- they travel with the skill
artifact (Git repo or OCI bundle).

`bodyLineCount` (int32) is a read-only field the catalog computes
when the SKILL.md body exceeds recommended length. EX skills vary
significantly: rh-basic/red-hat-cve-explainer is ~100 lines;
rh-sre/cve-impact is ~300+ lines. The catalog should surface this
as a quality signal.

## 3. Build/sign/publish gap analysis

The 07-requirements-refresh established that the Konflux pipeline for
skills is "epic-sized and not yet planned." The question: can EX skills
enter the catalog WITHOUT the full Konflux pipeline for 3.6 TP?

### Answer: yes, with a minimum viable supply chain

The Kubeflow hub catalog architecture supports a `type: "yaml"` source
provider that reads static YAML files from a ConfigMap. This is the
same mechanism used for curated model catalogs. The pipeline for 3.6
TP is:

1. **Source**: agentic-collections Git repository (pinned to a release
   tag or commit SHA)
2. **Transform**: Script maps SKILL.md frontmatter + collection.yaml
   to Kubeflow YAML catalog format
3. **Scan**: One-time SkillSpector scan of the skill set (64 patterns,
   outputs a report)
4. **Package**: YAML catalog source file baked into a ConfigMap in the
   RHOAI operator manifests
5. **Distribute**: Ships as part of the RHOAI operator image; no
   separate OCI artifact distribution needed

This bypasses Konflux entirely. The tradeoff: no automated signing,
no in-toto attestations, no continuous rebuild pipeline. These are
acceptable for 3.6 TP because:

- The skills are Red Hat-authored (no supply chain trust gap)
- The source repo is Red Hat-controlled (RHEcosystemAppEng org)
- The transform and scan are auditable one-time steps
- The catalog is read-only (no runtime execution, no code path risk)

### What this does NOT provide

| Capability | Status for 3.6 TP | When needed |
|---|---|---|
| Automated rebuild on skill update | Manual | 3.7 (Konflux pipeline) |
| Cosign signature on skill artifacts | None | 3.7 (OCI distribution) |
| In-toto attestation for provenance | None | 3.7 (Konflux Chains) |
| SBOM generation | None | 3.7 (Konflux standard output) |
| Continuous security scanning | One-time | 3.7 (Konflux pipeline step) |
| Partner skill ingestion pipeline | N/A for RH-authored | 3.7+ |

### Disconnected delivery for 3.6 TP

Since the YAML catalog source is baked into a ConfigMap, disconnected
delivery works automatically -- the catalog data ships with the RHOAI
operator image. No separate mirror step needed. This is a significant
advantage of the YAML source approach for initial delivery.

### Konflux pipeline requirements for 3.7+

When the full Konflux pipeline is built, it needs to handle:

1. **Source fetch**: Clone agentic-collections at a pinned ref
2. **Transform**: Same metadata mapping script as 3.6, now automated
3. **Scan**: SkillSpector + Snyk agent-scan (three-layer scanning)
4. **Build**: Package as OCI artifact (`application/vnd.agent-skills.skill.v1`)
5. **Sign**: Cosign keyless signing via Sigstore
6. **Attest**: In-toto attestation via Tekton Chains
7. **Publish**: Push to Quay.io
8. **Gate**: Conforma policy check before catalog inclusion

This is ~4-6 Tekton tasks, composable from existing Konflux task
catalog entries. The effort estimate from the 07 doc ("epic-sized")
is accurate for building the full pipeline, but only 2-3 of these
tasks are novel (transform, SkillSpector scan, OCI skill packaging).

## 4. Content curation recommendation

### Should all ~68 skills enter the catalog?

No. Evidence-based curation is the right approach:

**SkillsBench evidence**: curated skills improve agent pass rate by
+16.2 percentage points. Focused 2-3 module sets perform even better
(+18.6pp). Large unfocused sets dilute quality signals.

**Marketplace cold-start evidence**: cap synthetic/placeholder supply
at 30%; convert to real supply within 60 days. Starting with ~68
skills where some have incomplete evaluations risks the "empty shelf
with too many items" anti-pattern.

### Recommended curation: 30-35 skills from 4 packs

| Pack | Recommended skills | Rationale |
|---|---|---|
| rh-ai-engineer (11) | All 11 | Core RHOAI persona -- model serving, vLLM, KServe, NVIDIA NIM, pipelines. Direct alignment with what RHOAI users need. |
| rh-sre (13) | 9-10 (eval'd skills) | Strong eval coverage (9/13 skills evaluated), production-tested CVE remediation workflows. Omit unevaluated skills until evals complete. |
| ocp-admin (3) | All 3 | Core RHOAI persona -- cluster admins manage the platform. Small pack, high value. |
| rh-basic (6) | All 6 | Foundation skills (CVE explainer, diagnostics, lifecycle). Dependency for rh-sre workflows. |
| **Total** | **30-33** | |

### Packs recommended for deferral

| Pack | Skills | Why defer |
|---|---|---|
| rh-developer (14) | 14 | Not yet on catalog.redhat.com. Developer persona overlaps with existing RHOAI quickstarts. Wait for EX to bring to GREEN maturity and list externally first. |
| rh-virt (10) | 10 | Already on catalog.redhat.com but OCP Virt is a specialized persona -- not core RHOAI. Include in 3.7 expansion. |
| rh-automation (11) | 11 | Not yet on catalog.redhat.com. Ansible automation persona is adjacent but not core RHOAI. Wait for maturity promotion. |

### Pack-level vs skill-level catalog entries

**Recommendation: skill-level entries with pack-level grouping.**

The Kubeflow hub `Skill` entity is per-skill (name, description,
readme, labels). There is no "SkillPack" entity type. However, skills
from the same pack should share:
- `source_id` identifying the pack source
- `labels` indicating the pack name (e.g., `rh-sre`)
- `category` matching the pack category
- `customProperties.pack` for explicit grouping

This allows the UI to group by pack while maintaining skill-level
granularity for search, filtering, and detail views.

### Why the 3 unlisted packs are not on catalog.redhat.com yet

Evidence from the EX collection.yaml `maturity` field:

- **GREEN** packs (ready for public catalog): rh-sre, rh-basic,
  ocp-admin, rh-virt. These are the 4 packs on catalog.redhat.com.
- **ORANGE** packs (maintained but excluded from public catalog):
  rh-developer, rh-ai-engineer, rh-automation. These are the 3
  unlisted packs.

The maturity designation is an EX-controlled quality gate. ORANGE
means "metadata is maintained for validation and future promotion
but excluded from the public catalog surface until explicitly changed
to GREEN." This suggests the 3 unlisted packs may have incomplete
documentation, untested workflows, or pending review.

**Important exception**: rh-ai-engineer is ORANGE but is the most
critical pack for RHOAI. Peter should work with EX to fast-track
its promotion to GREEN. If the maturity gate is documentation
completeness (collection.yaml + eval coverage), a targeted sprint
could close the gap.

## 5. Pack readiness assessment

### rh-basic (6 skills) -- READY

| Dimension | Status |
|---|---|
| catalog.redhat.com | Listed (4 skill packs category) |
| Maturity | GREEN |
| RHOAI persona alignment | Foundation for all personas |
| API dependencies | Red Hat CVE Database, Security Advisories API, Vulnerability Service, Product Lifecycle API, Customer Portal |
| Subscription required | Red Hat subscription for API access |
| Disconnected compatible | NO -- all skills connect to live Red Hat APIs (console.redhat.com/insights). Cannot function air-gapped. |
| Eval coverage | To be confirmed (eval/rh-basic directory exists) |

**Disconnected mitigation**: The catalog can list these skills but
must display a connectivity requirement badge. Air-gapped deployments
see the skills in the catalog but cannot use them. This is a metadata
display concern, not a catalog architecture concern.

### rh-sre (13 skills) -- READY with eval gaps

| Dimension | Status |
|---|---|
| catalog.redhat.com | Listed |
| Maturity | GREEN |
| RHOAI persona alignment | Strong -- SREs operate RHOAI clusters |
| API dependencies | Red Hat Lightspeed (Insights), AAP MCP servers (2 servers: job-management, inventory-management) |
| Subscription required | Red Hat Lightspeed + AAP subscriptions |
| Disconnected compatible | NO -- requires Lightspeed API + AAP API connectivity |
| Eval coverage | 9/13 skills evaluated (69%). 4 skills (fleet-inventory, playbook-executor, remediation-verifier, job-template-creator) lack eval reports. |

**Gap**: 4 unevaluated skills. Two MCP validator skills
(mcp-lightspeed-validator, mcp-aap-validator) ARE evaluated, which
is good -- infrastructure readiness is tested. The orchestration
skill (remediation) is also evaluated.

### ocp-admin (3 skills) -- READY

| Dimension | Status |
|---|---|
| catalog.redhat.com | Listed |
| Maturity | GREEN |
| RHOAI persona alignment | Strong -- OCP admins deploy and manage RHOAI |
| API dependencies | OpenShift API (cluster-level) |
| Subscription required | OpenShift subscription (implicit for RHOAI) |
| Disconnected compatible | PARTIAL -- cluster-level operations can work disconnected if the cluster API is accessible; external integrations cannot |
| Eval coverage | To be confirmed (eval/ocp-admin directory exists) |

### rh-virt (10 skills) -- READY but non-core

| Dimension | Status |
|---|---|
| catalog.redhat.com | Listed (as "openshift-virtualization") |
| Maturity | GREEN |
| RHOAI persona alignment | Moderate -- OCP Virt is a specialized subsystem, not core ML/AI |
| API dependencies | OpenShift Virtualization API (KubeVirt) |
| Subscription required | OpenShift Virtualization subscription |
| Disconnected compatible | YES -- cluster-level VM operations work disconnected (kubeconfig-only MCP) |
| Eval coverage | To be confirmed (eval/rh-virt directory exists) |

**Note**: rh-virt is the only pack that could work fully disconnected,
since it only needs kubeconfig access to the local cluster. This makes
it interesting for air-gapped environments even though the persona
is non-core for RHOAI.

### rh-developer (14 skills) -- NOT READY

| Dimension | Status |
|---|---|
| catalog.redhat.com | NOT listed |
| Maturity | ORANGE (not promoted to public catalog) |
| RHOAI persona alignment | Moderate -- developers use RHOAI but this pack covers general app dev (S2I, Helm, deployment) |
| API dependencies | OpenShift API, S2I builder, Helm, container registries |
| Subscription required | OpenShift subscription |
| Disconnected compatible | PARTIAL -- depends on registry access and build infrastructure |
| Eval coverage | eval/rh-developer directory exists |

**Readiness gap**: maturity is ORANGE. The pack covers general
application development patterns (S2I builds, Helm charts, deployment)
rather than AI/ML-specific workflows. Overlaps with existing RHOAI
quickstarts.

### rh-ai-engineer (11 skills) -- STRATEGICALLY CRITICAL, MATURITY GAP

| Dimension | Status |
|---|---|
| catalog.redhat.com | NOT listed |
| Maturity | ORANGE (not yet promoted) |
| RHOAI persona alignment | HIGHEST -- model serving, vLLM, KServe, NVIDIA NIM, model registry, pipelines, guardrails, workbench management |
| API dependencies | OpenShift AI APIs, KServe, vLLM, NVIDIA NIM, model registry |
| Subscription required | RHOAI subscription |
| Disconnected compatible | PARTIAL -- model serving and pipeline skills can work disconnected; NIM requires NVIDIA cloud connectivity |
| Eval coverage | eval/rh-ai-engineer directory exists |

**This is the most important gap to close.** The rh-ai-engineer pack
is the single most valuable pack for RHOAI users (AI/ML engineers are
the primary persona). Skills like model-deploy, serving-runtime-config,
model-registry, pipeline-manage, and workbench-manage directly assist
the core RHOAI workflow.

**Action required**: Peter should prioritize working with EX to
promote rh-ai-engineer from ORANGE to GREEN. Specific needs:
1. Complete the `.catalog/collection.yaml` to GREEN standard
2. Ensure eval coverage for all 11 skills (or at minimum the top 6)
3. Validate that skills work against current RHOAI APIs (3.5/3.6)
4. Add RHOAI-specific deployment and use instructions

### rh-automation (11 skills) -- NOT READY

| Dimension | Status |
|---|---|
| catalog.redhat.com | NOT listed |
| Maturity | ORANGE |
| RHOAI persona alignment | Low -- Ansible Automation Platform governance is adjacent but not core AI/ML |
| API dependencies | AAP APIs, Ansible Galaxy, automation controller |
| Subscription required | AAP subscription |
| Disconnected compatible | PARTIAL -- AAP can run disconnected; some skills query external APIs |
| Eval coverage | eval/rh-automation directory exists |

**Readiness gap**: maturity ORANGE + low RHOAI persona alignment.
Defer to 3.7 expansion.

## 6. First-party classification and trust tier

### The classification question

EX skills are Red Hat-authored (Apache 2.0, maintained by Red Hat
Ecosystem Engineering under `eco-engineering@redhat.com`) but from
a different organization than RHOAI (EX, not Red Hat AI). Should
they be classified as `platformProvided`?

### Analysis

The Kubeflow hub SkillTrustTier enum has four values:

| Tier | Semantics |
|---|---|
| `platformProvided` | Red Hat ships and supports this skill as part of the platform |
| `partnerVerified` | ISV/partner authored, Red Hat verified through trust pipeline |
| `organizationApproved` | Enterprise customer approved for their own use |
| `communityContributed` | Community authored, no formal verification |

**EX skills should be `platformProvided`** because:

1. **Authored by Red Hat employees** in a Red Hat GitHub org
   (RHEcosystemAppEng)
2. **Licensed under Red Hat's standard open-source license** (Apache 2.0)
3. **Listed on catalog.redhat.com** with Red Hat branding (4 packs)
4. **Launched at Red Hat Summit 2026** as a Red Hat product offering
5. **Subscription-backed** -- skills connect to Red Hat APIs that
   require active subscriptions
6. **Maintained with Red Hat engineering standards** -- CI, pre-commit
   hooks, design principles, evaluation pipeline

The organizational boundary (EX vs RHOAI) is an internal structure.
From the customer's perspective, these are Red Hat skills. The
alternative -- classifying them as `partnerVerified` because they
come from a different Red Hat org -- would confuse customers and
undermine trust.

### Governance implications

`platformProvided` classification means:
- **Red Hat is accountable** for the quality and security of these
  skills in the RHOAI context
- **RHOAI PM (Peter) must own the curation** decision -- which skills
  enter, which are excluded
- **RHOAI ProdSec should review** the one-time security scan results
  (even if EX ran the scan)
- **Support implications**: customers may expect support for
  `platformProvided` skills through standard RHOAI support channels.
  This needs alignment with EX on support ownership.
- **Update cadence**: when EX updates a skill (new version, bug fix),
  the RHOAI catalog must update accordingly. This creates a
  cross-org dependency that needs a defined process (e.g., upstream
  release triggers downstream catalog rebuild).

### Recommended governance model

- **EX owns the skill content** (SKILL.md, workflows, supporting files)
- **RHOAI PM owns the catalog inclusion decision** (which skills, when)
- **RHOAI ProdSec owns the security review** (scan results, risk accept)
- **RHOAI engineering owns the catalog integration** (metadata mapping,
  source configuration, UI verification)
- **Joint ownership**: evaluation requirements (EX runs evals, RHOAI
  defines minimum thresholds for catalog inclusion)

## 7. EU AI Act Article 50 compliance

Article 50 enforcement is now in effect (August 2, 2026). The
07-requirements-refresh flagged this as imminent; it is now live.

### Which EX skills trigger Article 50?

Article 50(1) applies to AI systems that "interact directly with
natural persons." The EU Commission's July 2026 Guidelines confirm
that "agentic AI systems fall within Article 50(1)" and "where a
provider cannot reliably predict whether the agent will interact with
a human, it should be designed to disclose its AI nature in every
such interaction scenario."

Skills are instructions for AI agents, not AI systems themselves.
However, when an agent executes a skill, the resulting output may
constitute a direct interaction with a natural person. The question
is: does the skill generate user-facing output that the user might
mistake for human-generated content?

### Pack-by-pack Article 50 exposure

| Pack | Article 50 exposure | Rationale |
|---|---|---|
| rh-basic | YES | CVE Explainer generates advisory text that could be mistaken for expert human analysis. Support Severity Helper provides guidance that reads as human support advice. |
| rh-sre | YES | Remediation workflows generate Ansible playbooks and execution reports. The playbooks themselves are machine-generated; execution summaries read as human-authored reports. |
| rh-developer | YES | Application deployment guidance, Helm chart recommendations read as human expert advice. |
| rh-virt | MODERATE | VM lifecycle operations are more tool-like (create/delete/migrate VMs). Less likely to be mistaken for human output. |
| ocp-admin | MODERATE | Cluster health reports could be mistaken for human administrator reports. |
| rh-ai-engineer | YES | Model serving advisor, guardrails config, and debug-inference skills generate advisory content that reads as expert human analysis. |
| rh-automation | YES | Ansible playbook generation and governance recommendations read as human expert output. |

### Does EX format include compliance metadata?

No. The EX SKILL.md frontmatter has no `eu_ai_act_scope` or
equivalent compliance field. The 07-requirements-refresh recommended
adding such a field to skill cards.

### Compliance requirements for the RHOAI catalog

1. **Metadata**: Add `customProperties.eu_ai_act_article_50` (boolean)
   to skill catalog entries indicating whether the skill generates
   user-facing outputs that trigger Article 50 disclosure.

2. **Runtime disclosure**: The AI agent runtime (not the catalog) is
   responsible for Article 50(1) disclosure -- ensuring users know
   they are interacting with AI. The catalog's role is to surface
   the metadata so the runtime can apply appropriate disclosure
   policies.

3. **Machine-readable marking**: Article 50(2) requires AI-generated
   text to be machine-readably marked. Skills that generate text
   (playbooks, reports, recommendations) should include provenance
   metadata in their outputs. This is a runtime concern, not a
   catalog concern, but the catalog should flag which skills
   generate text outputs.

4. **Exemption analysis**: Skills performing assistive editing (grammar
   correction, formatting) are exempt. Skills that undergo
   "substantive human review" before the output reaches end users
   may qualify for a reduced obligation. The rh-sre remediation
   workflow has a human-in-the-loop gate (DP6) before playbook
   execution -- this may qualify as substantive human review for
   the playbook generation step, but the CVE advisory text does
   not have this gate.

5. **Timeline**: Systems on the market before August 2, 2026, get
   until December 2, 2026, for machine-readable marking compliance.
   EX skills launched at Summit 2026 (before August 2) -- the grace
   period applies. RHOAI catalog entries for 3.6 TP (shipping after
   August 2) do NOT get the grace period and must comply from day one.

### Recommended action

Add `eu_ai_act_article_50: true/false` to the upstream EX SKILL.md
frontmatter standard (propose via PR to agentic-collections). For
3.6 TP, derive the value from the pack-by-pack analysis above and
store in `customProperties`. For 3.7+, the field should be part of
the standard skill card schema.

## Key findings

1. **The Kubeflow hub already has a Skill entity type with trust tiers.**
   The catalog.yaml OpenAPI spec defines `Skill` with `name`,
   `description`, `license`, `allowedTools`, `readme`, `trustTier`
   (4-tier enum: platformProvided | partnerVerified |
   organizationApproved | communityContributed), `repository`, `path`,
   `version`, `resolvedCommit`, `supportingFiles`, and `labels`. PR
   #2973 implements this. The EX-to-catalog metadata mapping is
   mechanical, not architectural.

2. **EX skills can enter the catalog for 3.6 TP without Konflux.**
   The YAML catalog source provider (`type: "yaml"`) bakes skill
   metadata into a ConfigMap shipped with the RHOAI operator.
   No OCI packaging, no Cosign signing, no Tekton pipeline needed.
   Security coverage comes from a one-time SkillSpector scan. This
   is an acceptable tradeoff for Red Hat-authored, Red Hat-controlled
   skills.

3. **Metadata mapping has 5 gaps and 8 unmapped EX fields, all
   resolvable.** The 5 catalog-side gaps (source_id, trustTier,
   version, resolvedCommit, compatibility) are assigned at build
   time. The 8 EX-only fields (model, color, user_invocable,
   maturity, personas, marketplaces, support_level,
   sample_workflows) map to `customProperties` or `labels`. The
   `maturity: ORANGE` field serves as a pre-catalog gate.

4. **Curate 30-35 skills from 4 packs for 3.6 TP; fast-track
   rh-ai-engineer.** rh-basic (6), rh-sre (9-10 evaluated), ocp-admin
   (3), and rh-ai-engineer (11) provide the strongest persona
   alignment. rh-ai-engineer is ORANGE maturity (not on
   catalog.redhat.com) but is the single most valuable pack for
   RHOAI users -- Peter should prioritize its promotion to GREEN
   with EX.

5. **All packs except rh-virt require live API connectivity --
   disconnected environments see the catalog but cannot use the
   skills.** The catalog must display connectivity requirements
   as a badge or filter dimension. rh-virt is the only pack that
   works fully disconnected (kubeconfig-only). This is a significant
   gap for air-gapped enterprise customers.

6. **EX skills are `platformProvided` -- Red Hat is accountable.**
   The organizational boundary (EX vs RHOAI) is internal. Customers
   see Red Hat skills. This means RHOAI PM owns curation, ProdSec
   owns security review, and support ownership needs cross-org
   alignment.

7. **EU AI Act Article 50 is now in effect. 5 of 7 EX packs generate
   user-facing outputs triggering disclosure obligations.** The EX
   format has no compliance metadata. RHOAI should add
   `eu_ai_act_article_50` to catalog entries for 3.6 TP and propose
   the field upstream. The grace period for machine-readable marking
   (until Dec 2, 2026) applies to EX skills launched at Summit but
   NOT to new RHOAI catalog entries shipping after Aug 2.

8. **The evaluation pipeline is a strength to leverage.** EX already
   runs Treatment vs Control evaluations with statistical analysis
   (pass rate, Welch's t-test, Fisher's exact test) and provenance
   tracking (commit SHA, container image digests). The catalog should
   consume these results as metadata. Minimum threshold for catalog
   inclusion: pass rate >= 0.7 across >= 3 trials.
