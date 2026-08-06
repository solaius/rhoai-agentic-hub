---
title: "Skills Catalog research -- executive summary"
description: "Living synthesis of the 14-doc research series (standard 4-lens 2026-07-23 + competitive/architecture/requirements refresh 2026-07-30 + upstream/requirements refresh 2026-08-02 + landscape/architecture refresh 2026-08-04 + upstream/competitive/partnership refresh 2026-08-06) -- NVIDIA lifecycle fully reverse-engineered (hourly sync, 4-artifact gate, 3-defense signature model); no competitor covers full lifecycle with provenance; curated-with-federation is the right partner model; deprecation is the market's weakest dimension; proportional governance is unimplemented everywhere."
timestamp: 2026-08-06
review_after: 2026-11-06
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
Refresh 3: **standard, 2 lenses, 2026-08-04** (landscape and
architecture refreshed after UIE/Compass discovery + OCP5 distribution
model + no-portfolio-owner finding).
Refresh 4: **standard, 3 lenses, 2026-08-06** (upstream NVIDIA lifecycle
deep-dive + competitive lifecycle models + partnership ecosystem models,
triggered by NVIDIA skills inclusion decision and partner contact
confirmation).

| Doc | Lens | One line |
|---|---|---|
| [01-upstream](/components/skills-catalog/research/01-upstream.md) | upstream | Kubeflow hub 3-catalog pattern, agentskills.io/AAIF governance, SKILL.md cross-agent matrix, npx CLI, MLflow RFC handoff, ODH ai-helpers. **Superseded by 08 for KEP-0005, format mapping, ecosystem growth, and security crisis.** |
| [02-landscape](/components/skills-catalog/research/02-landscape.md) | landscape | 3-layer taxonomy, Git-backed curation, SkillsBench quality data, trust pipelines, ARD v0.9, EU AI Act, supply-chain attacks, governance gap. **Superseded by 10 for UIE/Compass, OCP5, catalog.redhat.com/en/ai, and NVIDIA growth.** |
| [03-architecture](/components/skills-catalog/research/03-architecture.md) | architecture | Extend hub vs new service, BFF reuse, disconnected pipeline, source federation, metadata normalization, trust tiers, catalog-to-registry orchestration. **Superseded by 06 for supply chain, installer, metadata, OpenShell, and disconnected topics.** |
| [04-requirements](/components/skills-catalog/research/04-requirements.md) | requirements | 3.6 browse-only TP feasible, RHAISTRAT-1940 risk, SkillsBench evidence, RH seed content, instructional install, disconnected constraint, EU AI Act Article 50. **Superseded by 07 for content list, partner verification, installation UX, skill cards, evals, signing, syndication, metadata governance.** |
| [05-competitive](/components/skills-catalog/research/05-competitive.md) | competitive | Supply chain security positioning (Konflux vs NVIDIA/JFrog/Snyk/Cisco), feature matrices (14 vendors, 13 dimensions), installer ecosystems, pricing, blind spots, win/loss analysis. **Deepened by 13 for lifecycle-focused competitive analysis.** |
| [06-architecture-refresh](/components/skills-catalog/research/06-architecture-refresh.md) | architecture | Supply chain pipeline (Konflux CI/CD, three-layer scanning), OCI artifact distribution (strategic convergence), installer architecture, metadata source-of-truth resolution, OpenShell layered sandboxing, NVIDIA trust pipeline reference, disconnected delivery. **Superseded by 11 for Compass/MLflow coexistence, OCP5 distribution, KEP-0005 plugin architecture.** |
| [07-requirements-refresh](/components/skills-catalog/research/07-requirements-refresh.md) | requirements | Initial content list (Peter's action), partner verification program (NVIDIA 8-stage reference), installation UX (7 methods, OCI strategic), skill cards, evaluations, signature verification (Sigstore), marketplace syndication (3.7+), metadata governance (OCI resolves debate), EU AI Act Article 50. **Superseded by 09 for EX onboarding pipeline, curation recommendation, pack readiness, trust tier classification, and Article 50 compliance analysis.** |
| [08-upstream-refresh](/components/skills-catalog/research/08-upstream-refresh.md) | upstream | KEP-0005 merged in kubeflow/hub (SKILL.md parser + OpenAPI, Jul 2026); EX format 90% spec-compliant (model/color divergence); catalog.redhat.com/en/ai is parallel surface with federation risk; 3 independent RH skill sources; MLflow #22833 supersedes RFC-0008; security crisis (Snyk ToxicSkills 36% flawed). **Deepened by 12 for NVIDIA lifecycle mechanics.** |
| [09-requirements-refresh](/components/skills-catalog/research/09-requirements-refresh.md) | requirements | EX-to-RHOAI 8-stage onboarding pipeline; metadata mapping (5 gaps + 8 EX-only fields, all resolvable); Konflux bypass viable for 3.6 TP via YAML source provider; curated 30-35 skills from 4 packs; rh-ai-engineer ORANGE but most valuable; platformProvided trust tier; 5/7 packs have Article 50 exposure |
| [10-landscape-refresh-2026-08](/components/skills-catalog/research/10-landscape-refresh-2026-08.md) | landscape | UIE/Compass discovery (300+ engineers, gold/silver scorecards), OCP5 operator-gated distribution model, NVIDIA catalog growth (2.8K stars, 300+ skills), catalog.redhat.com/en/ai launched, RHEcosystemAppEng/agentic-collections revealed |
| [11-architecture-refresh-2026-08](/components/skills-catalog/research/11-architecture-refresh-2026-08.md) | architecture | Three-layer decomposition (content/registry/distribution), Compass/MLflow registry coexistence patterns, KEP-0005 implementation architecture, OCP5 operator-gated distribution, no-portfolio-owner implications |
| [12-upstream-nvidia-lifecycle](/components/skills-catalog/research/12-upstream-nvidia-lifecycle.md) | upstream | **Full NVIDIA lifecycle reverse-engineering**: hourly sync (not daily), 4-artifact compliance gate (SKILL.md + skill.oms.sig + skill-card.md + evals.json), 3-defense signature drift model, NVSkills-CI (internal, non-open-source), SkillSpector 64 patterns/16 categories, self-serve components.d/ onboarding, SemVer auto-bump, 6-channel marketplace syndication, discovery-first plugin pattern |
| [13-competitive-lifecycle-models](/components/skills-catalog/research/13-competitive-lifecycle-models.md) | competitive | **Skills lifecycle comparison across 10 platforms**: no competitor covers full lifecycle with provenance; NVIDIA leads verification depth but has no deprecation states; Google has clearest state machine (5 states); deprecation is market's weakest dimension; proportional governance unimplemented everywhere; RHOAI can own the end-to-end lifecycle gap |
| [14-partnership-skills-ecosystems](/components/skills-catalog/research/14-partnership-skills-ecosystems.md) | partnership | **8-vendor partner model survey**: curated/gated vs federated vs aggregated patterns; NVIDIA+JFrog is closest RHOAI precedent; Red Hat ISV certification (container/operator) is the template; curated-with-federation hybrid recommended; partnerVerified trust tier for NVIDIA with Red Hat verification overlay |

## What the sweep establishes

**1-16 carry over from prior sweeps (see previous summary versions).**

**17-24 are new from the 2026-08-06 refresh (12-14).**

**17. NVIDIA's sync pipeline runs hourly, not daily.** The sync
clones all 35+ product repos via sparse checkout every hour, gated by
a 3-defense signature drift model (missing sig, stale sig, mismatching
sig). Content that diverges from its signature is reverted (existing
skill) or dropped (new skill). A daily full-catalog sha256 sweep adds
a fourth defense layer (12).

**18. NVIDIA requires four artifacts per skill, not two.** Beyond
SKILL.md and skill.oms.sig, every catalog skill must also ship
skill-card.md and evals.json. The compliance gate drops any skill
missing any of them. This is a harder bar than "scan + sign" (12).

**19. NVSkills-CI is internal and non-open-source.** The evaluation
system (3-tier: static validation, dedup, agent-based with 5 benchmark
dimensions) and the signing bot are NVIDIA-internal. Red Hat cannot
adopt these directly -- we need our own evaluation harness. The most
transferable elements are the components.d/ onboarding pattern, the
multi-defense signature model, and the 4-artifact compliance gate (12).

**20. No competitor manages the full skill lifecycle with provenance.**
NVIDIA leads verification depth (68 patterns) but has no formal
deprecation states. Google has the clearest state machine (5 states)
but no supply-chain provenance. AWS has the most structured approval
workflow but no skill versioning. RHOAI's Konflux + OCI + MLflow +
Kubeflow Hub combination can be the first to cover intake through
decommission with SLSA L3 provenance at every transition (13).

**21. Deprecation is the market's weakest lifecycle dimension.** Only
Google (5 states with terminal Decommissioned) and AWS (terminal
DEPRECATED) have explicit deprecation. Only the MCP specification
mandates a minimum sunset period (12 months). Gartner forecasts 150K
agents per Fortune 500 by 2028 -- without formal deprecation,
"zombie skill" accumulation is inevitable (13).

**22. Proportional governance is an unmet design opportunity.** Gartner
warns that uniform governance across all agents leads to enterprise AI
agent failure. No current platform implements proportional governance
for skills. RHOAI could classify skills by autonomy/risk level and
apply proportional lifecycle controls (13).

**23. Curated-with-federation is the right partner model for RHOAI.**
Red Hat controls curation (which NVIDIA skills appear); NVIDIA controls
content lifecycle (hourly sync from product repos); Kubeflow Hub
federates via catalog source YAML. This avoids both the maintenance
burden of fork/copy and the security risk of open aggregation. NVIDIA
skills enter as partnerVerified with a Red Hat verification overlay
(Konflux scan + metadata validation + platform relevance filter) (14).

**24. Red Hat's ISV certification programs are the template.** The
operator-pipelines Tekton model (partner-triggered, automated preflight,
PR-based promotion) maps directly to a skills partner program. The
skills program should follow Partner Connect enrollment, Konflux
pipeline validation, and RHOAI Skills Catalog distribution -- mirroring
container and operator certification (14).

## Recommended follow-ups (not auto-run)

- **jira-gap lens** -- once a Jira scope is stored for skills-catalog
  (via hub.jira-sweep), crossing active work against these findings
  would surface blind spots. Retry:
  `hub.research skills-catalog jira-gap`.
- **hub.strategy skills-catalog** -- the strategy doc (last refreshed
  2026-08-02) should be updated to incorporate the NVIDIA lifecycle
  findings, partner model recommendation, and lifecycle gap
  positioning. The series is now 14 docs deep.
- **hub.jira-sweep skills-catalog** -- store the Jira scope and create
  the work snapshot, prerequisite for jira-gap lens and strategy.
- **Proportional governance design** -- the finding that no competitor
  implements proportional governance for skills is a design opportunity
  worth a dedicated architecture pass. Retry:
  `hub.research skills-catalog architecture` with proportional
  governance as the focus.
