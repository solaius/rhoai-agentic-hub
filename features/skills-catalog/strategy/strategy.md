---
title: "Skills Catalog -- strategy"
description: Living strategy for the RHOAI Skills Catalog -- governance-first curated storefront on kubeflow/hub, Konflux SLSA L3 + OCI + MLflow as unique moat, 3.6 TP in progress (no blockers), RHAISTRAT-1940 content + supply chain pipeline as top risks, initial content list is Peter's action item.
timestamp: 2026-07-30
status: current
review_after: 2026-09-30
source: hub.strategy refresh 2026-07-30; inputs -- 7-doc research series (01-07), Ann Marie Fred architectural strategy GDoc intake (2026-07-30), 30 knowledge entries, sibling context (skills-registry, agent-catalog), roadmap + strategy profiles
---

## The brief

The Skills Catalog is RHOAI's fourth AI Hub storefront -- the discovery
layer for agent skills, built on kubeflow/hub alongside model, MCP, and
agent catalogs. **The bet**: a governance-first, curated catalog backed
by Konflux SLSA L3 provenance + OCI distribution + MLflow governance
delivers more enterprise value than a large unverified marketplace. No
competitor combines open-source provenance attestation, disconnected
distribution, and ML lifecycle governance in one stack
([05-competitive](/features/skills-catalog/research/05-competitive.md)).
Development in progress with no blockers (Ann Marie Fred, July 2026).
**Top risks**: initial catalog content list needs Peter's decision
(RHAISTRAT-1940 PM still unassigned) and the supply chain build/sign
pipeline is epic-sized unplanned work. **Next milestone**: resolve
content list and assign RHAISTRAT-1940 PM by August 2026; integrate
SkillSpector or Snyk agent-scan into Konflux before TP.


## What

### Release train

| Release | Scope | Status |
|---|---|---|
| **3.6 TP** (Oct 2026 code freeze) | Browse-only catalog: search/filter UI, skill detail cards, 15-20 pre-loaded RH skills, Git-backed YAML metadata, trust tier badges, ConfigMap disconnected import, category/tag filtering, skill card display (where available), signing status badge (informational) | In progress, no blockers ([ref-skills-architectural-strategy-gdoc](/features/skills-catalog/knowledge/ref-skills-architectural-strategy-gdoc.md)) |
| **3.6 GA** | Skills Registry DP (MLflow, POC developed, working with Databricks), installation UX (copy-paste commands per harness), partner skill feeds | Registry depends on RFC-0008 upstream merge |
| **3.7+** | OCI artifact distribution via Quay, one-click install, catalog-to-registry pull, quality scores/benchmarks, signature verification enforcement, partner verification program (Tekton pipelines), marketplace syndication (Skills.sh, ARD), semantic search | Future |

### Boundaries -- what this feature is NOT

- **Not the Skills Registry** ([skills-registry](/features/skills-registry/)) -- the registry is the MLflow governance/workspace layer (read-write, namespace-scoped, lifecycle management, RBAC). The catalog is read-only, cluster-scoped, Git-backed. See [decision-skills-catalog-registry-separation](/features/skills-catalog/knowledge/decision-skills-catalog-registry-separation.md).
- **Not a marketplace** -- no publishing, no monetization, no community submission flow. Curated content from Red Hat, partners, and admin-approved org skills.
- **Not skills development tooling** -- no IDE, no authoring UI, no testing framework. Skills are authored in Git repos outside the catalog.
- **Not the supply chain pipeline** -- the Konflux CI/CD pipeline for scanning, signing, and attesting skills is a separate epic-sized workstream. The catalog consumes its outputs (signed artifacts, scan results) but does not own the build/publish machinery. See [fact-skills-supply-chain-security](/features/skills-catalog/knowledge/fact-skills-supply-chain-security.md).
- **Not package management** -- packaging (APM, LOLA, NPM, OCI) lives in the registry via RFC-0008's PackageManagerPlugin or as standalone tools. The catalog surfaces install commands but does not own installation. See [question-skills-installation-features-location](/features/skills-catalog/knowledge/question-skills-installation-features-location.md).


## Why

### The problem

AI engineers and platform engineers have no centralized way to discover,
evaluate, and acquire agent skills for their RHOAI environments. Skills
are scattered across GitHub repos, npm packages, and vendor catalogs with
no trust signals, no enterprise governance, and no disconnected support.
96% of enterprises run AI agents; only 12% can govern them (OutSystems
2026). The supply-chain risk is severe: 1,184 malicious skills on
ClawHub (8.5% infection rate), 36% of public skills have security flaws
(Snyk ToxicSkills), 73% carry elevated safety risk (SkillsBench). See
[fact-skills-competitive-landscape-2026](/features/skills-catalog/knowledge/fact-skills-competitive-landscape-2026.md),
[fact-skills-supply-chain-security](/features/skills-catalog/knowledge/fact-skills-supply-chain-security.md).

### The bet

**Governance-first, not discovery-first.** Position the catalog as the
enterprise trust layer: trust tiers, signing status, compliance metadata,
and scan results are the primary UI elements, not just search and browse.
Evidence: SkillsBench shows curated skills raise agent pass rates by
+16.2pp while self-generated provide -1.3pp. Focused skills (2-3
modules) outperform larger bundles (+18.6pp vs +5.9pp). See
[fact-skillsbench-quality-evidence](/features/skills-catalog/knowledge/fact-skillsbench-quality-evidence.md).

**The moat: Konflux SLSA L3 + OCI + MLflow.** No competitor combines
SLSA Level 3 provenance attestation (cryptographic source-to-artifact
chain), OCI artifact distribution (same registries, mirrors, and signing
as containers), and open-source ML lifecycle governance in a single
stack. AWS has strong RBAC but no scanning/signing. Google has governance
but no air-gapped story. NVIDIA has the best trust pipeline but is not
a registry. JFrog has scanning + signing but not a catalog UX.
([05-competitive](/features/skills-catalog/research/05-competitive.md)).

### Why now

- Every cloud shipped governance tooling in 2026. The window to
  establish RHOAI as the enterprise skills platform is open but closing.
- EU AI Act Article 50 transparency obligations took effect August 2,
  2026. Skills generating user-facing outputs trigger disclosure
  requirements. Open-source is NOT exempt.
- SKILL.md is the standard (40+ tools, AAIF/Linux Foundation governed).
  See [ref-agentskills-io-spec](/features/skills-catalog/knowledge/ref-agentskills-io-spec.md).
- The catalog/registry pair pattern is proven in RHOAI (models, MCP
  servers, agents). Skills is the natural fourth asset type.


## Where we stand

### Decisions to date

| Date | Decision | Link |
|---|---|---|
| 2026-07-23 | Catalog and registry are separate products; catalog ships first | [decision-skills-catalog-registry-separation](/features/skills-catalog/knowledge/decision-skills-catalog-registry-separation.md) |
| 2026-07-23 | Push skills and agent registry RFCs upstream simultaneously | [decision-dual-rfc-push-upstream](/features/skills-registry/knowledge/decision-dual-rfc-push-upstream.md) |

### Delivery state

- **RHAISTRAT-1780** (Skills Catalog): development in progress, no
  blockers. Go backend, PostgreSQL, odh-dashboard React/PF6 BFF UI,
  trust tiers, 6-9 sprints. Catalog TP target: 3.6 GA release. See
  [fact-skills-catalog-rhaistrat-1780-scope](/features/skills-catalog/knowledge/fact-skills-catalog-rhaistrat-1780-scope.md).
- **RHAISTRAT-1940** (Pre-loaded skills): **PM unassigned**. Top risk.
  See [fact-skills-preloaded-content-risk](/features/skills-catalog/knowledge/fact-skills-preloaded-content-risk.md).
- **RFC-0008/0009** (Skills Registry in MLflow): POC code developed,
  working with Databricks for design acceptance before upstream
  contribution. Split into 2 RFCs per Databricks request. See
  [fact-skills-rfc-split-databricks](/features/skills-registry/knowledge/fact-skills-rfc-split-databricks.md).
- **Supply chain pipeline**: NOT YET PLANNED. Epic-sized Konflux CI/CD
  work for scanning, signing, and attesting skills. See
  [fact-skills-supply-chain-security](/features/skills-catalog/knowledge/fact-skills-supply-chain-security.md).

### In-flight work

- Ann Marie Fred: authored the cross-team architectural strategy for the
  skills ecosystem (catalog, registry, lifecycle, supply chain,
  installers, OpenShell). See
  [ref-skills-architectural-strategy-gdoc](/features/skills-catalog/knowledge/ref-skills-architectural-strategy-gdoc.md).
- Ramesh Reddy: catalog spec work, Kubeflow hub implementation.
- Bill Murdock: skills RFC design + agent registry RFC.
- Aditi Saluja: skills landscape mapping, status/scope/roadmap doc.


## Gaps & risks

### Existential

- **RHAISTRAT-1940 has no PM** -- without 15-20 curated skills at
  launch, the catalog ships empty. Marketplace evidence: empty catalogs
  train users to bypass them permanently. The initial content list is
  Peter's action item (Ann Marie tagged Peter, Catherine Weeks asked who
  decides). Red Hat already has seed content at redhat.com/skills. See
  [question-initial-catalog-skill-list](/features/skills-catalog/knowledge/question-initial-catalog-skill-list.md),
  [fact-redhat-agentic-skills-seed-content](/features/skills-catalog/knowledge/fact-redhat-agentic-skills-seed-content.md).

### Supply chain

- **Konflux skills pipeline not planned** -- the three-layer scanning
  pipeline (static via SkillSpector/miasma-detect, ML-model via Snyk
  agent-scan, LLM-as-reviewer) plus signing/attestation via Tekton
  Chains is epic-sized and has no Jira work. Without it, Red Hat's SLSA
  L3 differentiation is aspirational, not deliverable. **Close the
  scanning gap immediately** by integrating SkillSpector or agent-scan
  as a Tekton task. See
  [06-architecture-refresh](/features/skills-catalog/research/06-architecture-refresh.md).

### Competitive gaps (from [05-competitive](/features/skills-catalog/research/05-competitive.md))

1. **No skills-specific scanning** -- no SkillSpector equivalent in
   the RHOAI pipeline. Most visible competitive gap.
2. **No skill cards / compliance metadata** -- no structured format
   beyond SKILL.md frontmatter. NVIDIA owns the reference.
3. **Developer install UX** -- `npx skills add` is one command; RHOAI's
   OCI path needs a CLI wrapper.
4. **No runtime policy enforcement** -- AWS Cedar, Google semantic
   governance, and Databricks service policies enforce at runtime.
5. **Ecosystem breadth** -- Red Hat's catalog is small vs Azure 193,
   AWS 43 packs, community 600K+.

### Architecture

- **Metadata source-of-truth debate** -- Roland Huss challenges the
  Git/MLflow split. Research resolves it: frontmatter = identity, catalog
  = discovery, registry = governance, OCI Referrers = verification. But
  no formal decision recorded. See
  [question-skills-metadata-source-split](/features/skills-catalog/knowledge/question-skills-metadata-source-split.md).
- **LOLA has no active maintainers** -- may be archived unless AAET
  commits. Deprioritize in favor of OCI + npx/APM. See
  [07-requirements-refresh](/features/skills-catalog/research/07-requirements-refresh.md).

### Open questions

- **Installation features location** -- catalog, registry, or both?
  Research recommends: admin installs via OCI (catalog), developer
  installs via npx/git (unmanaged). Needs formal STRAT. See
  [question-skills-installation-features-location](/features/skills-catalog/knowledge/question-skills-installation-features-location.md).
- **NVIDIA collaboration model** -- collaborate on verification pipeline,
  integrate via federation, or independent? Strong "collaborate" signal.
  See [question-skills-catalog-nvidia-collaboration](/features/skills-catalog/knowledge/question-skills-catalog-nvidia-collaboration.md).

### Missing inputs

- No Jira scope stored (`jira:` block and `work/jira-snapshot.yaml`
  absent). Run `hub.jira-sweep skills-catalog` to build the snapshot.


## Jira map

**No Jira scope stored for skills-catalog.** Known keys from intake:

| Element | Key | Type | Status (from docs) |
|---|---|---|---|
| Skills Catalog: Discovery and Acquisition | RHAISTRAT-1780 | Feature | In Progress |
| Pre-loaded skills for out-of-box value | RHAISTRAT-1940 | Feature | New, unassigned |
| Skills Registry: Self-Hosted | RHAISTRAT-1630 | Feature | New |
| AI Hub AI Asset Delivery for Agentic Solutions | RHAISTRAT-1339 | Feature | In Progress |

**First gap**: no stored Jira scope. Run `hub.jira-sweep skills-catalog`.

### Candidate jiras

| Gap | Problem statement | Suggested project |
|---|---|---|
| No skills-specific scanning in Konflux | The Konflux pipeline has no agent-skills scanning stage; integrating SkillSpector or Snyk agent-scan as a Tekton task would close the most visible competitive gap and enable SLSA L3 differentiation | RHAISTRAT (new, epic-sized) |
| No RHAISTRAT-1940 PM assignment | The pre-loaded content STRAT exists but has no PM owner; without one the catalog ships empty | RHAISTRAT-1940 (assign PM) |
| No Red Hat Skill Card format | No structured metadata format for trust, compliance, and quality data beyond SKILL.md frontmatter; NVIDIA's skill card is the de facto reference but not standardized | RHAISTRAT (new, under RHAISTRAT-1780) |
| No OCI artifact distribution for skills | OCI is the strategic convergence point for disconnected, signing, and mirroring but no Jira work exists to implement the Thomas Vitale v0.1.0 spec for skills | RHAISTRAT (new) |
| Installation features location unresolved | Where install features live (catalog vs registry vs shared service) needs its own STRAT | RHAISTRAT (new) |
| No NVIDIA verification integration | SkillSpector/OMS pipeline is complementary; no work exists to integrate scan results or signatures into the catalog UI | RHAISTRAT (new, cross-feature with skills-registry) |
| No marketplace syndication plan | Publishing RH skills to Skills.sh, Codex/Claude Code plugin directories, and ARD format would drive adoption; no work planned | RHAISTRAT (new, 3.7+) |


## Watchlist

| Date | Trigger | If it fires, what changes |
|---|---|---|
| 2026-08-02 | EU AI Act Article 50 enforcement | Skills generating user-facing outputs need disclosure metadata. Compliance metadata (`eu_ai_act_scope`) becomes a hard requirement. Open-source NOT exempt. |
| 2026-08 (est.) | MLflow RFC-0008 Phase 1 review outcome | If approved: registry timeline firms up, catalog-to-registry integration path is defined. If stalled: catalog standalone value increases. |
| 2026-08 | RHAISTRAT-1940 PM assignment deadline | If assigned: content pipeline starts. If missed: catalog ships empty -- existential risk materializes. |
| 2026-08 (est.) | LOLA maintainership decision | If AAET commits: LOLA remains a supported installer. If archived: deprioritize, focus on OCI + npx/APM. |
| 2026-09 (est.) | ARD v1.0 specification release | If ARD ships with adoption: plan an ARD catalog source type. If stalls: YAML+Git remain safe default. |
| 2026-10-23 | RHOAI 3.6 code freeze | Hard deadline for catalog TP. Content and scanning must be ready. |
| Ongoing | OCI agent skills spec maturity | If v0.1.0 gains traction and tooling matures: accelerate OCI distribution. If stalls: stay on Git-backed YAML. |
| Ongoing | APM adoption trajectory | If APM becomes the enterprise standard: ensure OCI distribution works alongside APM. Microsoft/Databricks backing makes this likely. |
| Ongoing | NVIDIA SkillSpector maturity | If NVIDIA ships enterprise scanning: integration becomes urgent. If they stay GitHub-only: build our own Tekton task wrapping SkillSpector. |
| Ongoing | skills.sh / Anthropic Marketplace scale | If a dominant marketplace emerges with enterprise features: catalog may need to accelerate governance features. |


## History

- 2026-07-30 -- **Refresh** -- 3-lens research refresh (competitive + architecture + requirements) after Ann Marie Fred architectural strategy GDoc intake. Key shifts: governance-first positioning (research finding: 96% run agents, 12% govern -- lead with trust, not discovery); Konflux SLSA L3 + OCI + MLflow identified as unique competitive moat (no other vendor combines all three); 5 competitive gaps to close (scanning, skill cards, developer UX, runtime policy, ecosystem breadth); supply chain pipeline flagged as epic-sized unplanned work; initial content list is Peter's action item (Ann Marie tagged Peter, Catherine Weeks asked who decides); LOLA deprioritized (no active maintainers); OCI artifact distribution identified as strategic convergence point (eliminates Go git-pull service need); metadata source-of-truth debate resolved in research (frontmatter=identity, catalog=discovery, registry=governance, OCI Referrers=verification); EU AI Act Article 50 enforcement imminent. Candidate jiras expanded from 5 to 7.
- 2026-07-23 -- **Creation** -- first strategy doc for skills-catalog. Synthesized from intake (3 transcripts, 2 GDocs, NVIDIA repo, Slack channel -- 25 entries committed) + 4-lens standard research (upstream, landscape, architecture, requirements -- 11 entries committed). Key positions: extend kubeflow/hub (not new service), browse-only 3.6 TP, RHAISTRAT-1940 as existential risk, curation-over-volume bet, NVIDIA trust pipeline as alignment model. No Jira scope stored yet.
