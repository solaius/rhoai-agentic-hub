---
title: "Skills Catalog -- strategy"
description: Living strategy for the RHOAI Skills Catalog -- curated Git-backed Kubeflow hub storefront for agent skills, 3.6 TP target, extend kubeflow/hub, NVIDIA trust pipeline alignment, RHAISTRAT-1940 content as existential risk.
timestamp: 2026-07-23
status: current
review_after: 2026-09-23
source: hub.strategy run 2026-07-23; inputs -- skills-catalog intake (3 transcripts, 2 GDocs, NVIDIA repo, Slack channel) + 4-lens research (upstream, landscape, architecture, requirements) + sibling context (skills-registry, agent-catalog)
---

## The brief

The Skills Catalog is RHOAI's fourth AI Hub storefront -- the discovery
layer for agent skills, built on kubeflow/hub alongside model, MCP, and
agent catalogs. **The bet**: a curated, Git-backed, trust-tiered catalog
of 15-20 working skills delivers more enterprise value than a large
unverified marketplace (SkillsBench: curated +16.2pp pass rate vs public
average 6.2/12). Catalog ships independently of the MLflow registry
timeline (~90% confidence for 3.6 TP). **Today**: direction established
2026-07-23, RHAISTRAT-1780 exists as 3.6 candidate, no code yet.
**Next milestone**: resolve extend-hub-vs-new-service architecture
question and assign a PM to RHAISTRAT-1940 (pre-loaded content) by
August 2026 -- the empty-catalog risk is existential.


## What

### Release train

| Release | Scope | Status |
|---|---|---|
| **3.6 TP** (Oct 2026 code freeze) | Browse-only catalog: search/filter UI, skill detail cards, 15-20 pre-loaded RH skills, Git-backed YAML metadata, trust tier badges, ConfigMap disconnected import, category/tag filtering | Direction set 2026-07-23; RHAISTRAT-1780 New |
| **3.6 GA** | Installation UX (copy-paste commands per harness, npx/lola), partner skill feeds, telemetry | Not scoped |
| **3.7+** | One-click install to harness, catalog-to-registry pull (MLflow integration), quality scores/benchmarks, OCI artifact distribution, ARD federation, semantic search | Future |

### Boundaries -- what this feature is NOT

- **Not the Skills Registry** ([skills-registry](/features/skills-registry/)) -- the registry is the MLflow-based governance/workspace layer (read-write, namespace-scoped, lifecycle management, RBAC). The catalog is read-only, cluster-scoped, Git-backed. See [decision-skills-catalog-registry-separation](/features/skills-catalog/knowledge/decision-skills-catalog-registry-separation.md).
- **Not a marketplace** -- no publishing, no monetization, no community submission flow. Curated content from Red Hat, partners, and admin-approved org skills.
- **Not skills development tooling** -- no IDE, no authoring UI, no testing framework. Skills are authored in Git repos outside the catalog.
- **Not package management** -- packaging (APM, LOLA, NPM, OCI) lives in the registry via RFC-0008's PackageManagerPlugin. The catalog may surface install commands but does not own the installation machinery. See [question-skills-installation-features-location](/features/skills-catalog/knowledge/question-skills-installation-features-location.md).


## Why

### The problem

AI engineers and platform engineers have no centralized way to discover,
evaluate, and acquire agent skills for their RHOAI environments. Skills
are scattered across GitHub repos, npm packages, and vendor catalogs with
no trust signals, no enterprise governance, and no disconnected support.
The supply-chain risk is real: 1,184 malicious skills on ClawHub (8.5%
infection rate), 36% of public skills have security flaws (Snyk
ToxicSkills), 73% carry elevated safety risk (SkillsBench). See
[fact-skills-competitive-landscape-2026](/features/skills-catalog/knowledge/fact-skills-competitive-landscape-2026.md).

### The bet

A curated catalog with trust tiers beats an open marketplace. Evidence:
SkillsBench shows curated skills raise agent pass rates by +16.2pp while
self-generated provide -1.3pp. Focused skills (2-3 modules) outperform
larger bundles (+18.6pp vs +5.9pp). See [fact-skillsbench-quality-evidence](/features/skills-catalog/knowledge/fact-skillsbench-quality-evidence.md).

Red Hat's differentiation: **open source + self-hosted + governed +
disconnected**. No other vendor ships a vendor-supported, self-run skills
catalog with trust tiers and air-gapped support. NVIDIA has the most
mature catalog (2.7K stars) but it is a public GitHub repo, not an
enterprise-governed platform. JFrog has enterprise governance but is
proprietary and tightly coupled. See [fact-nvidia-skills-catalog-landscape](/features/skills-catalog/knowledge/fact-nvidia-skills-catalog-landscape.md).

### Why now

- Every cloud shipped governance tooling in 2026 (AWS AgentCore, Azure
  Agent 365, Google Gemini Enterprise, Databricks Unity AI). 96% of
  enterprises run agents; only 12% can govern them.
- EU AI Act Article 50 transparency obligations take effect August 2,
  2026. Skills generating user-facing outputs trigger disclosure
  requirements.
- SKILL.md is the emerging standard (40+ tools, AAIF/Linux Foundation
  governed). The window to establish RHOAI as the enterprise skills
  platform is open but closing as competitors ship.
- The catalog/registry pair pattern is proven in RHOAI (models, MCP
  servers, agents). Skills is the natural fourth asset type.


## Where we stand

### Decisions to date

| Date | Decision | Link |
|---|---|---|
| 2026-07-23 | Catalog and registry are separate products; catalog ships first | [decision-skills-catalog-registry-separation](/features/skills-catalog/knowledge/decision-skills-catalog-registry-separation.md) |
| 2026-07-23 | Push skills and agent registry RFCs upstream simultaneously | [decision-dual-rfc-push-upstream](/features/skills-registry/knowledge/decision-dual-rfc-push-upstream.md) |

### Delivery state

- **RHAISTRAT-1780** (Skills Catalog): New, 3.6 candidate. Go backend,
  PostgreSQL, odh-dashboard React/PF6 BFF UI, trust tiers, 6-9 sprints.
  See [fact-skills-catalog-rhaistrat-1780-scope](/features/skills-catalog/knowledge/fact-skills-catalog-rhaistrat-1780-scope.md).
- **RHAISTRAT-1940** (Pre-loaded skills): New, **PM unassigned**. Top
  risk. See [fact-skills-preloaded-content-risk](/features/skills-catalog/knowledge/fact-skills-preloaded-content-risk.md).
- **RFC-0008/0009** (Skills Registry in MLflow): draft, unmerged. Bill
  Murdock splitting into 2 RFCs per Databricks request. See
  [fact-skills-rfc-split-databricks](/features/skills-registry/knowledge/fact-skills-rfc-split-databricks.md).

### In-flight work

- Bill Murdock: continuing skills RFC design + writing agent registry
  RFC for immediate submission after second skills RFC.
- Ramesh Reddy: catalog spec work, NPX/Claude plugin support.
- Aditi Saluja: skills landscape mapping, status/scope/roadmap doc.
- Ann Marie Fred: evaluating NVIDIA skills repo as a model; talking to
  Jason/Edson/Daniele about catalog+registry alignment.


## Gaps & risks

### Existential

- **RHAISTRAT-1940 has no PM** -- without 15-20 curated skills at
  launch, the catalog ships empty. Marketplace evidence: empty catalogs
  train users to bypass them permanently. Red Hat already has seed
  content at redhat.com/skills (Summit 2026 launch) -- conversion is the
  fastest path. **PM assignment by August 2026 is critical.** See
  [fact-redhat-agentic-skills-seed-content](/features/skills-catalog/knowledge/fact-redhat-agentic-skills-seed-content.md).

### Architecture

- **Extend hub vs new service** -- RHAISTRAT-1780 proposes standalone
  Go+PostgreSQL. Research recommends extending kubeflow/hub as the 4th
  catalog type (proven pattern, lower risk). Unresolved. See
  [question-skills-catalog-extend-hub-vs-new-service](/features/skills-catalog/knowledge/question-skills-catalog-extend-hub-vs-new-service.md).

### Open questions

- **NVIDIA collaboration model** -- model on their approach? integrate
  via federation? use their verification pipeline? Strong "collaborate"
  signal but no decision. See [question-skills-catalog-nvidia-collaboration](/features/skills-catalog/knowledge/question-skills-catalog-nvidia-collaboration.md).
- **Installation features location** -- catalog, registry, or both?
  Needs own STRAT. See [question-skills-installation-features-location](/features/skills-catalog/knowledge/question-skills-installation-features-location.md).
- **Ramesh governance position** -- skills are static with no governance
  need; governance at agent level. Bill/Ann Marie/Edson disagree on the
  registry side. Affects scope of catalog metadata. See
  [fact-ramesh-skills-governance-position](/features/skills-registry/knowledge/fact-ramesh-skills-governance-position.md).

### Timeline

- 6-7 sprints to October 23 code freeze = low end of 6-9 sprint
  estimate. Browse-only TP feasible only if scope is held and
  architecture question resolved quickly. See
  [fact-skills-catalog-36-scope-recommendation](/features/skills-catalog/knowledge/fact-skills-catalog-36-scope-recommendation.md).

### Missing inputs

- No Jira scope stored (`jira:` block and `work/jira-snapshot.yaml`
  absent). Offer: `hub.jira-sweep skills-catalog`.
- No skills-registry research refresh since April 2026 (migrated from
  old repo, substantially out of date given the explosion in the space).


## Jira map

**No Jira scope stored for skills-catalog.** The following keys are
known from intake sources but have not been swept:

| Element | Key | Type | Status (from docs) |
|---|---|---|---|
| Skills Catalog: Discovery and Acquisition | RHAISTRAT-1780 | Feature | New |
| Pre-loaded skills for out-of-box value | RHAISTRAT-1940 | Feature | New, unassigned |
| Skills Registry: Self-Hosted | RHAISTRAT-1630 | Feature | New |
| AI Hub AI Asset Delivery for Agentic Solutions | RHAISTRAT-1339 | Feature | In Progress |

**First gap**: no stored Jira scope. Run `hub.jira-sweep skills-catalog`
to discover the full issue set and build the snapshot.

### Candidate jiras

| Gap | Problem statement | Suggested project |
|---|---|---|
| No skills-specific catalog source provider in kubeflow/hub | The hub has YAML and HuggingFace source providers but nothing that reads SKILL.md frontmatter from Git repos; this is the core backend work for the catalog | RHAISTRAT (Feature under RHAISTRAT-1780) |
| No RHAISTRAT-1940 PM assignment | The pre-loaded content STRAT exists but has no PM owner; without one the catalog ships empty and has negative value | RHAISTRAT-1940 (assign PM) |
| No ODH ADR for Skills Catalog | Agent Catalog and MCP Catalog both went through ODH ADRs; skills catalog needs the same upstream alignment | RHAISTRAT (new, under RHAISTRAT-1780) |
| Installation features location unresolved | Where install features live (catalog vs registry vs shared service) affects both RHAISTRAT-1780 and RFC-0008; needs its own STRAT | RHAISTRAT (new) |
| No NVIDIA skills verification integration | NVIDIA's SkillSpector/OMS pipeline is complementary to MLflow but no Jira work exists to integrate scan results or signature verification into the catalog or registry | RHAISTRAT (new, cross-feature with skills-registry) |


## Watchlist

| Date | Trigger | If it fires, what changes |
|---|---|---|
| 2026-08-02 | EU AI Act Article 50 transparency obligations take effect | Skills generating user-facing outputs need disclosure metadata in catalog cards. Compliance metadata becomes a hard requirement, not a nice-to-have. |
| 2026-08 (est.) | MLflow RFC-0008 Phase 1 review outcome | If approved: registry timeline firms up, catalog-to-registry integration path is defined. If rejected/stalled: registry decoupling validated, catalog standalone value increases. |
| 2026-08 (est.) | MLflow next release code freeze | Determines whether any registry capability can ride RHOAI 3.6. Affects whether catalog must own install features or can delegate to registry. |
| 2026-09 (est.) | ARD v1.0 specification release | If ARD ships and gains adoption: plan an ARD catalog source type for skills discovery federation. If stalls: YAML+Git sources remain the safe default. |
| 2026-10-23 | RHOAI 3.6 code freeze | Hard deadline for catalog TP. If RHAISTRAT-1940 content is not ready, the catalog ships empty. |
| Ongoing | NVIDIA skills repo growth + SkillSpector maturity | If NVIDIA ships a full enterprise catalog: the collaboration question becomes urgent. If they stay GitHub-only: our enterprise surface remains differentiated. |
| Ongoing | skills.sh / Anthropic Marketplace scale | If a dominant marketplace emerges with enterprise features: catalog's browse-only model may need to accelerate installation and governance features. |


## History

- 2026-07-23 -- **Creation** -- first strategy doc for skills-catalog. Synthesized from intake (3 transcripts, 2 GDocs, NVIDIA repo, Slack channel -- 25 entries committed) + 4-lens standard research (upstream, landscape, architecture, requirements -- 11 entries committed). Key positions: extend kubeflow/hub (not new service), browse-only 3.6 TP, RHAISTRAT-1940 as existential risk, curation-over-volume bet, NVIDIA trust pipeline as alignment model. No Jira scope stored yet.
