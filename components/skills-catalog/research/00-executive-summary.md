---
title: "Skills Catalog research -- executive summary"
description: Living synthesis of the 9-doc research series (standard 4-lens 2026-07-23 + competitive/architecture/requirements refresh 2026-07-30 + upstream/requirements refresh 2026-08-02) -- KEP-0005 merged (skills catalog now being built); EX onboarding viable for 3.6 TP without Konflux; 30-35 curated skills from 4 packs; rh-ai-engineer is ORANGE but most valuable; 3 RH skill sources need consolidation; EU AI Act Article 50 now in effect.
timestamp: 2026-08-02
review_after: 2026-11-02
---

# Skills Catalog research -- executive summary

## The series

Initial run: **standard, 4 lenses, 2026-07-23** (all completed).
Refresh 1: **standard, 3 lenses, 2026-07-30** (competitive new +
architecture and requirements refreshed after Ann Marie Fred's
architectural strategy GDoc intake).
Refresh 2: **standard, 2 lenses, 2026-08-02** (upstream and requirements
refreshed after EX agentic skills inventory intake + RHAISTRAT-1940 PM
assignment).

| Doc | Lens | One line |
|---|---|---|
| [01-upstream](/components/skills-catalog/research/01-upstream.md) | upstream | Kubeflow hub 3-catalog pattern, agentskills.io/AAIF governance, SKILL.md cross-agent matrix, npx CLI, MLflow RFC handoff, ODH ai-helpers. **Superseded by 08 for KEP-0005, format mapping, ecosystem growth, and security crisis.** |
| [02-landscape](/components/skills-catalog/research/02-landscape.md) | landscape | 3-layer taxonomy, Git-backed curation, SkillsBench quality data, trust pipelines, ARD v0.9, EU AI Act, supply-chain attacks, governance gap |
| [03-architecture](/components/skills-catalog/research/03-architecture.md) | architecture | Extend hub vs new service, BFF reuse, disconnected pipeline, source federation, metadata normalization, trust tiers, catalog-to-registry orchestration. **Superseded by 06 for supply chain, installer, metadata, OpenShell, and disconnected topics.** |
| [04-requirements](/components/skills-catalog/research/04-requirements.md) | requirements | 3.6 browse-only TP feasible, RHAISTRAT-1940 risk, SkillsBench evidence, RH seed content, instructional install, disconnected constraint, EU AI Act Article 50. **Superseded by 07 for content list, partner verification, installation UX, skill cards, evals, signing, syndication, metadata governance.** |
| [05-competitive](/components/skills-catalog/research/05-competitive.md) | competitive | Supply chain security positioning (Konflux vs NVIDIA/JFrog/Snyk/Cisco), feature matrices (14 vendors, 13 dimensions), installer ecosystems, pricing, blind spots, win/loss analysis |
| [06-architecture-refresh](/components/skills-catalog/research/06-architecture-refresh.md) | architecture | Supply chain pipeline (Konflux CI/CD, three-layer scanning), OCI artifact distribution (strategic convergence), installer architecture, metadata source-of-truth resolution, OpenShell layered sandboxing, NVIDIA trust pipeline reference, disconnected delivery (OCI mirror vs Go git-pull service) |
| [07-requirements-refresh](/components/skills-catalog/research/07-requirements-refresh.md) | requirements | Initial content list (Peter's action), partner verification program (NVIDIA 8-stage reference), installation UX (7 methods, OCI strategic), skill cards, evaluations, signature verification (Sigstore), marketplace syndication (3.7+), metadata governance (OCI resolves debate), EU AI Act Article 50 (3 days away at time of writing). **Superseded by 09 for EX onboarding pipeline, curation recommendation, pack readiness, trust tier classification, and Article 50 compliance analysis.** |
| [08-upstream-refresh](/components/skills-catalog/research/08-upstream-refresh.md) | upstream | KEP-0005 merged in kubeflow/hub (SKILL.md parser + OpenAPI, Jul 2026); EX format 90% spec-compliant (model/color divergence); catalog.redhat.com/en/ai is parallel surface with federation risk; 3 independent RH skill sources; MLflow #22833 supersedes RFC-0008; security crisis (Snyk ToxicSkills 36% flawed) |
| [09-requirements-refresh](/components/skills-catalog/research/09-requirements-refresh.md) | requirements | EX-to-RHOAI 8-stage onboarding pipeline; metadata mapping (5 gaps + 8 EX-only fields, all resolvable); Konflux bypass viable for 3.6 TP via YAML source provider; curated 30-35 skills from 4 packs; rh-ai-engineer ORANGE but most valuable; platformProvided trust tier; 5/7 packs have Article 50 exposure |

## What the sweep establishes

**1-3 carry over from the initial sweep (01-04, 2026-07-23).**

**1. Extend kubeflow/hub rather than building a new service.** The hub
already supports three catalog types with a proven extensibility model.
Adding skills as the fourth type is lower risk, lower effort, and
aligned with upstream trajectory. Settled (03). **Now confirmed: KEP-0005
merged Jul 27-31, skills IS the fourth catalog type (08).**

**2. The 3.6 timeline is tight but feasible for a browse-only TP.**
6-7 sprints to code freeze, ~90% confidence if scope stays at read-only
browse/search with pre-loaded content. Installation automation and
registry integration deferred (04).

**3. Quality beats quantity by a measured margin.** SkillsBench: curated
+16.2pp pass rate, focused 2-3 modules +18.6pp. Cold-start evidence:
start curated, expand later (04, 07).

**4-10 from the 2026-07-30 refresh (05-07).**

**4. The Konflux + OCI + MLflow combination is unique -- no competitor
matches it.** No vendor combines SLSA Level 3 provenance attestation,
OCI artifact distribution, and open-source ML lifecycle governance in a
single stack (05).

**5. Supply chain security is table stakes -- Red Hat's differentiation
is SLSA L3 provenance, not scanning.** The security landscape has
become a crisis: Snyk ToxicSkills found 36% of community skills contain
flaws, 76 confirmed malicious (05, 08). This makes the curated
`platformProvided` tier a critical trust differentiator.

**6. OCI artifact distribution is the strategic convergence point.** It
reuses existing container infrastructure. The OCI spec for skills exists
(Thomas Vitale v0.1.0, April 2026) with reference implementations (06,
07). **For 3.6 TP, the YAML source provider bypasses OCI entirely --
OCI is 3.7+ (09).**

**7. The installer question is partially resolved.** Two paths: admin
installs via OCI pull (3.7+), developer installs via npx/git (06, 07).

**8. Governance-first positioning wins.** 96% of enterprises run agents;
12% can govern them. EU AI Act Article 50 is now in effect (Aug 2, 2026).
5 of 7 EX packs generate user-facing outputs triggering disclosure.
Catalog metadata should flag `eu_ai_act_article_50` (05, 07, 09).

**9. Five competitive gaps to close before TP** (05) -- unchanged.

**10. RHAISTRAT-1940 existential risk is mitigated.** PM assigned
Aug 2. Peter working with EX + PE teams on the initial skills list (07).

**11-16 are new from the 2026-08-02 refresh (08-09).**

**11. KEP-0005 merged -- the skills catalog is now being built.** The
first-mover window from 01-upstream has closed in the best way: Red Hat
(rareddy) authored the implementation. SKILL.md parser, OpenAPI spec,
and plugin scaffold all landed. Tracking issue #3014 has 32 tasks for
full implementation (08).

**12. EX skills can enter the 3.6 TP catalog without Konflux.** The
YAML catalog source provider (`type: "yaml"`) bakes skill metadata
into a ConfigMap shipped with the RHOAI operator. One-time SkillSpector
scan provides security coverage. No OCI, no Cosign, no Tekton needed.
This is acceptable for Red Hat-authored, Red Hat-controlled skills (09).

**13. Curate 30-35 skills from 4 packs for initial catalog.** rh-basic
(6), rh-sre (9-10 evaluated), ocp-admin (3), rh-ai-engineer (11).
SkillsBench evidence and cold-start research support curation over
volume. Three packs deferred (rh-developer, rh-virt, rh-automation) for
maturity or persona-alignment reasons (09).

**14. rh-ai-engineer is ORANGE but is the most valuable RHOAI pack.**
It covers model serving, vLLM, KServe, NVIDIA NIM, pipelines, model
registry, guardrails -- the core RHOAI workflow. Peter should prioritize
fast-tracking its promotion to GREEN with EX (09).

**15. Three independent Red Hat skill sources exist with no
consolidation.** RHEcosystemAppEng/agentic-plugins (EX, 7 packs, 68
skills), openshift/agentic-skills (Lightspeed-tied, 3 skills), and
opendatahub-io/ai-helpers (ODH, Claude Code marketplace). The Kubeflow
hub catalog can federate all three via separate source configs, but
someone needs to configure and maintain them (08).

**16. EX format is 90% spec-compliant; migration is trivial.** The
only divergence is `model` and `color` as top-level fields instead
of under `metadata:`. The Kubeflow hub parser silently ignores unknown
fields (warns, loads). Migration to `metadata:` is a one-line change
per skill (08).

## Recommended follow-ups (not auto-run)

- **jira-gap lens** -- once a Jira scope is stored for skills-catalog
  (via hub.jira-sweep), crossing active work against these findings
  would surface blind spots. Retry:
  `hub.research skills-catalog jira-gap`.
- **hub.strategy skills-catalog** -- the living strategy doc synthesizes
  this research series + knowledge + Jira scope into the WHAT/WHY, gaps
  and risks, and watchlist. The series is now deep enough (9 docs) to
  support a strong strategy doc.
- **hub.jira-sweep skills-catalog** -- store the Jira scope and create
  the work snapshot, prerequisite for jira-gap lens and strategy.
