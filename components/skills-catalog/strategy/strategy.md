---
title: "Skills Catalog -- strategy"
description: Living strategy for the RHOAI Skills Catalog -- governance-first curated storefront on kubeflow/hub (KEP-0005 merged Jul 2026); Konflux SLSA L3 + OCI + MLflow as unique moat; 3.6 TP on track with 30-35 EX skills via YAML source (Konflux bypass); RHAISTRAT-1940 PM assigned; rh-ai-engineer ORANGE promotion is top action; supply chain pipeline remains epic-sized unplanned.
timestamp: 2026-08-02
status: current
review_after: 2026-10-02
source: hub.strategy refresh 2026-08-02; inputs -- 9-doc research series (01-09), EX agentic skills intake (2026-08-02), Jira sweep (7 issues), 34 knowledge entries, sibling context (skills-registry, agent-catalog), roadmap + strategy profiles
---

## The brief

The Skills Catalog is RHOAI's fourth AI Hub storefront -- now with
upstream implementation landed (KEP-0005 merged in kubeflow/hub, Jul
2026, authored by rareddy). **The bet**: governance-first, curated
catalog backed by Konflux SLSA L3 + OCI + MLflow delivers more
enterprise value than a large unverified marketplace. No competitor
combines all three
([05-competitive](/components/skills-catalog/research/05-competitive.md)).
RHAISTRAT-1940 PM now assigned (existential risk mitigated). **Next
actions**: fast-track rh-ai-engineer from ORANGE to GREEN with EX; build
metadata mapping script; run one-time SkillSpector scan. 30-35 curated
skills from 4 EX packs for 3.6 TP, entering via YAML source provider
without Konflux. **Top remaining risk**: supply chain pipeline is
epic-sized unplanned work; rh-ai-engineer ORANGE maturity blocks the
most valuable RHOAI pack.


## What

### Release train

| Release | Scope | Status |
|---|---|---|
| **3.6 TP** (Oct 2026 code freeze) | Browse-only catalog: search/filter UI, skill detail cards, 30-35 pre-loaded EX skills (4 packs: rh-basic, rh-sre, ocp-admin, rh-ai-engineer), Git-backed YAML source provider (ConfigMap, ships with operator), trust tier badges (platformProvided), category/tag filtering, signing status badge (informational), EU AI Act Article 50 metadata | In progress -- KEP-0005 merged, RHAISTRAT-1940 PM assigned, EX onboarding pipeline mapped ([09-requirements-refresh](/components/skills-catalog/research/09-requirements-refresh.md)) |
| **3.6 GA** | OCI artifact distribution via Quay, installation UX (copy-paste per harness → OCI pull), partner skill feeds, skill card display, evaluation scores (metadata-only) | OCI spec exists (Thomas Vitale v0.1.0); Konflux pipeline is the gating dependency |
| **3.7+** | Skills Registry DP (MLflow #22833, further out than expected), one-click install, catalog-to-registry pull, quality scores/benchmarks, signature verification enforcement, partner verification program (Tekton pipelines), marketplace syndication (Skills.sh, ARD), semantic search, runtime policy enforcement | MLflow timeline uncertain (#22833 defers detailed design); ARD spec (Google, v0.9) has backers but near-zero adoption |

### Boundaries -- what this component is NOT

- **Not the Skills Registry** ([skills-registry](/components/skills-registry/)) -- the registry is the MLflow governance/workspace layer (read-write, namespace-scoped, lifecycle management). The catalog is read-only, cluster-scoped, Git-backed. See [decision-skills-catalog-registry-separation](/components/skills-catalog/knowledge/decision-skills-catalog-registry-separation.md).
- **Not a marketplace** -- no publishing, no monetization, no community submission flow. Curated content from Red Hat, partners, and admin-approved org skills.
- **Not skills development tooling** -- no IDE, no authoring UI, no testing framework.
- **Not the supply chain pipeline** -- the Konflux CI/CD pipeline for scanning, signing, and attesting skills is a separate workstream. The catalog consumes its outputs. See [fact-skills-supply-chain-security](/components/skills-catalog/knowledge/fact-skills-supply-chain-security.md), [fact-konflux-ai-asset-pipeline-positioning](/components/platform/knowledge/fact-konflux-ai-asset-pipeline-positioning.md).
- **Not package management** -- packaging (APM, npx, OCI) lives in the registry or as standalone tools. The catalog surfaces install commands but does not own installation. See [question-skills-installation-features-location](/components/skills-catalog/knowledge/question-skills-installation-features-location.md).


## Why

### The problem

AI engineers and platform engineers have no centralized way to discover,
evaluate, and acquire agent skills for their RHOAI environments. Skills
are scattered across GitHub repos, npm packages, and vendor catalogs with
no trust signals, no enterprise governance, and no disconnected support.
96% of enterprises run AI agents; only 12% can govern them (OutSystems
2026). The supply-chain crisis is now measured: 36% of community skills
contain security flaws, 76 confirmed malicious payloads (Snyk
ToxicSkills), 73% carry elevated safety risk (SkillsBench), 1,184
poisoned skills on ClawHub. See
[fact-skills-competitive-landscape-2026](/components/skills-catalog/knowledge/fact-skills-competitive-landscape-2026.md),
[fact-skills-supply-chain-security](/components/skills-catalog/knowledge/fact-skills-supply-chain-security.md).

### The bet

**Governance-first, not discovery-first.** Position the catalog as the
enterprise trust layer: trust tiers, signing status, compliance metadata,
and scan results are the primary UI elements. Evidence: curated skills
raise agent pass rates by +16.2pp; unfocused bundles dilute quality
(+5.9pp vs +18.6pp for focused 2-3 module sets). See
[fact-skillsbench-quality-evidence](/components/skills-catalog/knowledge/fact-skillsbench-quality-evidence.md).

**The moat: Konflux SLSA L3 + OCI + MLflow.** No competitor combines
SLSA Level 3 provenance attestation, OCI artifact distribution, and
open-source ML lifecycle governance. AWS has strong RBAC but no
scanning/signing. Google has governance but no air-gapped story. NVIDIA
has the best trust pipeline but is not a registry. JFrog has scanning +
signing but not a catalog UX
([05-competitive](/components/skills-catalog/research/05-competitive.md)).

### Why now

- Every cloud shipped governance tooling in 2026. The window is open but closing.
- EU AI Act Article 50 took effect August 2, 2026. Skills generating user-facing outputs trigger disclosure. Open-source NOT exempt. 5 of 7 EX packs are exposed.
- SKILL.md is the standard (40+ native agents, 70+ total, AAIF/Linux Foundation governed). See [ref-agentskills-io-spec](/components/skills-catalog/knowledge/ref-agentskills-io-spec.md).
- KEP-0005 merged -- the upstream foundation is real. Red Hat authored it.


## Where we stand

### Decisions to date

| Date | Decision | Link |
|---|---|---|
| 2026-07-23 | Catalog and registry are separate products; catalog ships first | [decision-skills-catalog-registry-separation](/components/skills-catalog/knowledge/decision-skills-catalog-registry-separation.md) |
| 2026-07-23 | Push skills and agent registry RFCs upstream simultaneously | [decision-dual-rfc-push-upstream](/components/skills-registry/knowledge/decision-dual-rfc-push-upstream.md) |
| 2026-08-02 | EX skills are platformProvided trust tier (Red Hat-authored, Summit-launched, subscription-backed) | [09-requirements-refresh](/components/skills-catalog/research/09-requirements-refresh.md) §6 |
| 2026-08-02 | 3.6 TP enters via YAML source provider without Konflux (acceptable for RH-authored skills) | [fact-ex-onboarding-36-viable-without-konflux](/components/skills-catalog/knowledge/fact-ex-onboarding-36-viable-without-konflux.md) |

### Delivery state

- **KEP-0005** (Skills Catalog in kubeflow/hub): merged Jul 27-31. SKILL.md parser (SKC-104), OpenAPI spec (SKC-101), plugin scaffold (SKC-103) all landed. 32-task tracking issue #3014. See [fact-kep-0005-skills-catalog-upstream](/components/skills-catalog/knowledge/fact-kep-0005-skills-catalog-upstream.md).
- **RHAISTRAT-1780** (Skills Catalog Feature): New, fix version 3.6 EA2. Development in progress. See [ref-rhaistrat-1780-skills-catalog](/components/skills-catalog/knowledge/ref-rhaistrat-1780-skills-catalog.md).
- **RHAISTRAT-1940** (Pre-loaded skills): New, **PM now assigned** (2026-08-02). Peter working with EX + PE teams on initial list. See [fact-skills-preloaded-content-risk](/components/skills-catalog/knowledge/fact-skills-preloaded-content-risk.md).
- **EX onboarding pipeline**: 8-stage flow mapped end-to-end. Metadata mapping is mechanical (5 gaps, 8 unmapped EX fields, all resolvable). 2-3 sprint effort parallelized. See [09-requirements-refresh](/components/skills-catalog/research/09-requirements-refresh.md).
- **MLflow #22833** (Skill Registry): supersedes RFC-0008 with a metadata-first, governed approach. Detailed design deferred to future RFC. Registry timeline further out than expected. See [08-upstream-refresh](/components/skills-catalog/research/08-upstream-refresh.md) §4.5.
- **Supply chain pipeline**: NOT YET PLANNED. Epic-sized. See [fact-skills-supply-chain-security](/components/skills-catalog/knowledge/fact-skills-supply-chain-security.md).

### In-flight work

- **Peter Double**: building initial skills list with EX + PE teams; fast-tracking rh-ai-engineer ORANGE → GREEN.
- **Ramesh Reddy** (rareddy): landed KEP-0005 in kubeflow/hub. Catalog implementation underway.
- **Ann Marie Fred**: authored cross-team architectural strategy. See [ref-skills-architectural-strategy-gdoc](/components/skills-catalog/knowledge/ref-skills-architectural-strategy-gdoc.md).
- **Bill Murdock**: MLflow skills registry design (#22833 path).
- **Aditi Saluja**: skills landscape mapping. See [person-aditi-saluja](/components/skills-catalog/knowledge/person-aditi-saluja.md).

### EX skills sources (3 independent, no consolidation)

| Source | Org | Count | Status |
|---|---|---|---|
| RHEcosystemAppEng/agentic-plugins | EX | ~68 (7 packs) | 4 packs GREEN, 3 ORANGE |
| openshift/agentic-skills | Lightspeed | 3 | Ships with Lightspeed |
| opendatahub-io/ai-helpers | ODH | Varies | Claude Code marketplace |

See [fact-three-rh-skill-sources](/components/skills-catalog/knowledge/fact-three-rh-skill-sources.md).


## Gaps & risks

### Content (demoted from existential -- PM assigned)

- **rh-ai-engineer ORANGE maturity** -- the most valuable RHOAI pack (model serving, vLLM, KServe, NIM, pipelines, model registry, guardrails) is not on catalog.redhat.com and cannot enter the RHOAI catalog at GREEN. Peter must fast-track promotion with EX. See [question-rh-ai-engineer-pack-promotion](/components/skills-catalog/knowledge/question-rh-ai-engineer-pack-promotion.md).
- **Evaluation gaps** -- rh-sre has 4/13 skills without eval reports. Minimum threshold for catalog inclusion: pass rate >= 0.7 across >= 3 trials.

### Supply chain

- **Konflux skills pipeline not planned** -- three-layer scanning + signing + attestation is epic-sized with no Jira work. Without it, SLSA L3 differentiation is aspirational. Close the scanning gap by integrating SkillSpector as a Tekton task. See [06-architecture-refresh](/components/skills-catalog/research/06-architecture-refresh.md).

### Coordination

- **3 independent RH skill sources** -- EX, Lightspeed, and ODH produce skills independently. The Kubeflow hub can federate all three via source configs, but nobody owns the consolidation. This creates duplication risk with catalog.redhat.com/en/ai (the parallel external surface). See [fact-three-rh-skill-sources](/components/skills-catalog/knowledge/fact-three-rh-skill-sources.md).

### Compliance

- **EU AI Act Article 50 now in effect** -- 5 of 7 EX packs generate user-facing outputs triggering disclosure. EX format has no compliance metadata. RHOAI catalog entries shipping after Aug 2 do NOT get the grace period. Add `eu_ai_act_article_50` to catalog `customProperties`. See [09-requirements-refresh](/components/skills-catalog/research/09-requirements-refresh.md) §7.

### Competitive gaps (from [05-competitive](/components/skills-catalog/research/05-competitive.md))

1. No skills-specific scanning in the RHOAI pipeline
2. No skill cards / compliance metadata format
3. Developer install UX gap (npx is one command; OCI path needs a wrapper)
4. No runtime policy enforcement
5. Ecosystem breadth (30-35 vs Azure 193, AWS 43 packs, community 600K+)

### Architecture

- **Metadata source-of-truth debate** -- research resolves it (frontmatter = identity, catalog = discovery, registry = governance, OCI Referrers = verification) but no formal decision recorded. See [question-skills-metadata-source-split](/components/skills-catalog/knowledge/question-skills-metadata-source-split.md).
- **Disconnected gap** -- all EX packs except rh-virt require live Red Hat API connectivity. Air-gapped environments see the catalog but cannot use most skills. The catalog must display connectivity requirements as a filter dimension.

### Open questions

- **Installation features location** -- catalog, registry, or both? Needs its own STRAT. See [question-skills-installation-features-location](/components/skills-catalog/knowledge/question-skills-installation-features-location.md).
- **NVIDIA collaboration model** -- collaborate on verification pipeline, integrate via federation, or independent? See [question-skills-catalog-nvidia-collaboration](/components/skills-catalog/knowledge/question-skills-catalog-nvidia-collaboration.md).


## Jira map

### Stored scope (7 issues, swept 2026-08-02)

| Key | Type | Status | Fix Version | What it covers |
|---|---|---|---|---|
| RHAISTRAT-1339 | Outcome | In Progress | -- | Parent Outcome for AI Hub agentic asset delivery (skills, MCP, agents) |
| RHAISTRAT-1780 | Feature | New | 3.6 EA2 | Skills Catalog: discovery and acquisition in AI Hub |
| RHAISTRAT-1940 | Feature | New | -- | Pre-loaded skills for out-of-box value (PM assigned 2026-08-02) |
| RHAIRFE-2207 | Feature Request | Approved | 3.5 GA | Customer RFE for skills catalog discovery and acquisition |
| RHAIRFE-2382 | Feature Request | Approved | -- | Customer RFE for pre-loaded skills (counterpart of RHAISTRAT-1940) |
| RHAIRFE-1567 | Feature Request | Stakeholder review | -- | Reusable safety skills (content moderation, PII detection) as catalog entries |
| RHOAIENG-66140 | Task | Closed/Done | -- | Implementation task (completed) |

### Coverage assessment

| Strategy element | Jira coverage | Gap |
|---|---|---|
| Browse/search catalog UI | RHAISTRAT-1780 | Covered |
| Pre-loaded content | RHAISTRAT-1940 | Covered (PM assigned) |
| Safety skills | RHAIRFE-1567 | In stakeholder review |
| Supply chain scanning pipeline | None | **Gap** -- epic-sized |
| OCI artifact distribution | None | **Gap** |
| Skill card / compliance metadata format | None | **Gap** |
| Installation features location | None | **Gap** -- needs STRAT |
| EX skill source consolidation | None | **Gap** |
| EU AI Act Article 50 compliance metadata | None | **Gap** |
| Partner verification program | None | **Gap** (3.7+) |
| Marketplace syndication | None | **Gap** (3.7+) |

### Candidate jiras

| Gap | Problem statement | Suggested project |
|---|---|---|
| No skills-specific scanning in Konflux | The Konflux pipeline has no agent-skills scanning stage; integrating SkillSpector as a Tekton task would close the most visible competitive gap and enable SLSA L3 differentiation | RHAISTRAT (new, epic-sized) |
| No OCI artifact distribution for skills | OCI is the strategic convergence point for disconnected, signing, and mirroring but no Jira work exists | RHAISTRAT (new, under RHAISTRAT-1780) |
| No Red Hat Skill Card format | No structured metadata format for trust/compliance/quality beyond SKILL.md frontmatter; NVIDIA's skill card is the de facto reference | RHAISTRAT (new, under RHAISTRAT-1780) |
| Installation features location unresolved | Where install features live (catalog vs registry vs shared service) needs its own STRAT | RHAISTRAT (new) |
| No NVIDIA verification integration | SkillSpector/OMS pipeline is complementary; no work to integrate scan results or signatures into the catalog | RHAISTRAT (new, cross-component) |
| EX ORANGE maturity gate for rh-ai-engineer | The most valuable RHOAI pack is blocked from catalog inclusion by EX maturity status; needs a cross-team fast-track process | Process (Peter + EX, no Jira needed) |
| 3 RH skill sources with no consolidation | EX, Lightspeed, and ODH produce skills independently; catalog source config ownership undefined | Process (Peter to define ownership) |
| No marketplace syndication plan | Publishing RH skills to Skills.sh, ARD format, and plugin directories would drive adoption | RHAISTRAT (new, 3.7+) |
| EU AI Act Article 50 compliance metadata | 5/7 EX packs generate user-facing outputs; no compliance field in EX frontmatter or catalog schema | RHAISTRAT (new, under RHAISTRAT-1780) |


## Watchlist

| Date | Trigger | If it fires, what changes |
|---|---|---|
| 2026-08 | rh-ai-engineer ORANGE → GREEN promotion outcome | If promoted: 11 AI/ML skills enter the catalog (strongest RHOAI value). If blocked: catalog launches without AI/ML skills -- significant value gap. |
| 2026-08 (est.) | MLflow #22833 detailed design RFC | If published: registry timeline firms up, catalog-to-registry path clarifies. If deferred: catalog standalone value increases further. |
| 2026-09 (est.) | ARD v1.0 specification release | If ARD ships with adoption: plan an ARD catalog source type. If stalls: YAML+Git remain safe default. |
| 2026-10-23 | RHOAI 3.6 code freeze | Hard deadline for catalog TP. 30-35 skills, metadata mapping, SkillSpector scan must all be ready. |
| Ongoing | OCI agent skills spec maturity | If v0.1.0 gains tooling: accelerate OCI distribution for 3.6 GA. If stalls: stay on YAML source. |
| Ongoing | NVIDIA SkillSpector maturity | If NVIDIA ships enterprise scanning: integration urgent. If GitHub-only: wrap as Tekton task. |
| Ongoing | APM adoption trajectory | If APM becomes enterprise standard: ensure OCI works alongside it. Microsoft/Databricks backing makes this likely. |
| Ongoing | 3 RH skill source consolidation | If a single source emerges: simplify catalog config. If fragmentation persists: define ownership or accept multi-source federation. |
| Ongoing | Snyk/OWASP agent security tooling | If scanning tools mature: integrate into Konflux pipeline. The 36% flaw rate makes this urgent. |


## History

- 2026-08-02 -- **Refresh** -- upstream + requirements research refresh (08-09) after EX agentic skills intake + Jira sweep (7 issues, 3 new RFE refs). Key shifts: KEP-0005 merged in kubeflow/hub (upstream foundation real, rareddy authored); RHAISTRAT-1940 PM assigned (existential risk mitigated -- demoted to content gap); EX onboarding pipeline mapped end-to-end (8 stages, Konflux bypass viable for 3.6 TP via YAML source provider); 30-35 curated skills from 4 packs recommended (rh-basic 6 + rh-sre 9-10 + ocp-admin 3 + rh-ai-engineer 11); rh-ai-engineer ORANGE but most valuable RHOAI pack -- fast-track promotion is top action item; 3 independent RH skill sources discovered (EX, Lightspeed, ODH -- fragmentation risk); EU AI Act Article 50 now in effect (5/7 packs exposed, no compliance metadata in EX format); MLflow RFC-0008 superseded by #22833 (registry further out); Jira scope stored (7 issues). Release train adjusted: 3.6 TP refined to 30-35 EX skills via YAML source; 3.6 GA adjusted for OCI + Konflux; 3.7+ for registry (MLflow timeline uncertain). Candidate jiras expanded from 7 to 9.
- 2026-07-30 -- **Refresh** -- 3-lens research refresh (competitive + architecture + requirements) after Ann Marie Fred architectural strategy GDoc intake. Key shifts: governance-first positioning (96% run agents, 12% govern -- lead with trust); Konflux SLSA L3 + OCI + MLflow as unique moat; 5 competitive gaps; supply chain pipeline epic-sized unplanned; initial content list is Peter's action item; LOLA deprioritized; OCI as strategic convergence; metadata debate resolved in research; EU AI Act Article 50 imminent. Candidate jiras expanded from 5 to 7.
- 2026-07-23 -- **Creation** -- first strategy doc. Synthesized from intake (3 transcripts, 2 GDocs, NVIDIA repo, Slack channel -- 25 entries) + 4-lens standard research (upstream, landscape, architecture, requirements -- 11 entries). Key positions: extend kubeflow/hub, browse-only 3.6 TP, RHAISTRAT-1940 as existential risk, curation-over-volume bet, NVIDIA trust pipeline alignment. No Jira scope stored.
