---
title: "Skills Catalog research -- executive summary"
description: Living synthesis of the 7-doc research series (standard 4-lens 2026-07-23 + competitive/architecture/requirements refresh 2026-07-30) -- Konflux SLSA L3 + OCI + MLflow is unique stack; governance-first positioning; 5 competitive gaps to close; supply chain pipeline epic-sized and unplanned; initial content list is Peter's action item; EU AI Act Article 50 enforcement imminent.
timestamp: 2026-07-30
review_after: 2026-10-30
---

# Skills Catalog research -- executive summary

## The series

Initial run: **standard, 4 lenses, 2026-07-23** (all completed).
Refresh: **standard, 3 lenses, 2026-07-30** (competitive new + architecture
and requirements refreshed after Ann Marie Fred's architectural strategy
GDoc intake).

| Doc | Lens | One line |
|---|---|---|
| [01-upstream](/components/skills-catalog/research/01-upstream.md) | upstream | Kubeflow hub 3-catalog pattern, agentskills.io/AAIF governance, SKILL.md cross-agent matrix, npx CLI, MLflow RFC handoff, ODH ai-helpers |
| [02-landscape](/components/skills-catalog/research/02-landscape.md) | landscape | 3-layer taxonomy, Git-backed curation, SkillsBench quality data, trust pipelines, ARD v0.9, EU AI Act, supply-chain attacks, governance gap |
| [03-architecture](/components/skills-catalog/research/03-architecture.md) | architecture | Extend hub vs new service, BFF reuse, disconnected pipeline, source federation, metadata normalization, trust tiers, catalog-to-registry orchestration. **Superseded by 06 for supply chain, installer, metadata, OpenShell, and disconnected topics.** |
| [04-requirements](/components/skills-catalog/research/04-requirements.md) | requirements | 3.6 browse-only TP feasible, RHAISTRAT-1940 risk, SkillsBench evidence, RH seed content, instructional install, disconnected constraint, EU AI Act Article 50. **Superseded by 07 for content list, partner verification, installation UX, skill cards, evals, signing, syndication, metadata governance.** |
| [05-competitive](/components/skills-catalog/research/05-competitive.md) | competitive | Supply chain security positioning (Konflux vs NVIDIA/JFrog/Snyk/Cisco), feature matrices (14 vendors, 13 dimensions), installer ecosystems, pricing, blind spots, win/loss analysis |
| [06-architecture-refresh](/components/skills-catalog/research/06-architecture-refresh.md) | architecture | Supply chain pipeline (Konflux CI/CD, three-layer scanning), OCI artifact distribution (strategic convergence), installer architecture, metadata source-of-truth resolution, OpenShell layered sandboxing, NVIDIA trust pipeline reference, disconnected delivery (OCI mirror vs Go git-pull service) |
| [07-requirements-refresh](/components/skills-catalog/research/07-requirements-refresh.md) | requirements | Initial content list (Peter's action), partner verification program (NVIDIA 8-stage reference), installation UX (7 methods, OCI strategic), skill cards, evaluations, signature verification (Sigstore), marketplace syndication (3.7+), metadata governance (OCI resolves debate), EU AI Act Article 50 (3 days away at time of writing) |

## What the sweep establishes

**1-3 carry over from the initial sweep (01-04, 2026-07-23).**

**1. No upstream skills catalog exists -- first-mover opportunity and
risk.** Unlike models or MCP servers, there is no established upstream
catalog for agent skills. RHOAI's skills catalog would be the first
enterprise-grade, self-hosted skills storefront. The opportunity is
differentiation; the risk is no pattern to inherit (01, 02).

**2. Extend kubeflow/hub rather than building a new service.** The hub
already supports three catalog types with a proven extensibility model.
Adding skills as the fourth type is lower risk, lower effort, and
aligned with upstream trajectory. Settled (03).

**3. The 3.6 timeline is tight but feasible for a browse-only TP.**
6-7 sprints to code freeze, ~90% confidence if scope stays at read-only
browse/search with pre-loaded content. Installation automation and
registry integration deferred (04).

**4-10 are new or updated from the 2026-07-30 refresh (05-07).**

**4. RHAISTRAT-1940 (pre-loaded content) remains the existential risk,
and the initial content list is now Peter's action item.** Ann Marie Fred
tagged Peter Double: "What is the initial list of skills for the
Catalog?" Catherine Weeks asked who defines what goes public. The
content decision authority and the RHAISTRAT-1940 PM gap both remain
unresolved. Without 15-20 working skills at launch, the catalog ships
empty. Cold-start research confirms: marketplaces that skip single-player
utility fail 4x more often (04, 07).

**5. The Konflux + OCI + MLflow combination is unique -- no competitor
matches it.** No vendor combines SLSA Level 3 provenance attestation,
OCI artifact distribution, and open-source ML lifecycle governance in a
single stack. This is Red Hat's moat. The feature matrix across 14
vendors and 13 dimensions confirms: AWS has strong RBAC but no
scanning/signing; Google has governance but no air-gapped story; NVIDIA
has the best trust pipeline but is not a registry; JFrog has scanning +
signing but not a catalog UX (05).

**6. Supply chain security is table stakes -- Red Hat's differentiation
is SLSA L3 provenance, not scanning.** Every serious vendor now scans,
signs, or both. NVIDIA (SkillSpector, 68 patterns), JFrog (scan-verify-
sign, Gartner Leader), Snyk (agent-scan, MDM mode), and Cisco
(DefenseClaw, 5 OSS components) all have production-ready offerings.
Red Hat's Konflux adds what nobody else has: SLSA Level 3 provenance
via Tekton Chains, hermetic builds, multi-arch (x86/ARM/PPC/Z), and
Conforma policy gating. **But the Konflux skills pipeline is not yet
planned -- it is epic-sized.** Close the scanning gap immediately by
integrating SkillSpector or Snyk agent-scan as a Tekton task (05, 06).

**7. OCI artifact distribution is the strategic convergence point.** It
reuses existing container infrastructure (Quay stores, oc-mirror mirrors,
cosign signs, Konflux builds). It eliminates the need for a separate Go
git-pull service for disconnected delivery. It resolves the metadata
governance debate: inherent metadata (SKILL.md frontmatter) inside the
artifact, external metadata (signatures, attestations, eval scores) via
OCI Referrers API. The OCI spec for skills exists (Thomas Vitale v0.1.0,
April 2026) with reference implementations (Arconia CLI, skills-oci,
skillctl). RHOAI should build on this (06, 07).

**8. The installer question is partially resolved.** Two paths: admin
installs via OCI pull from Quay/mirror (RHOAI-managed), developer
installs via npx/git (unmanaged). The hard question remains: where does
the installed skill land in the agent runtime filesystem? For 3.6 TP,
instructional UX (copy-paste commands) is correct. LOLA has no active
maintainers and should be deprioritized. APM (Microsoft) is the package
manager to watch for enterprise adoption (06, 07).

**9. Governance-first positioning wins.** 96% of enterprises run agents;
12% can govern them. Position the skills catalog as governance-first,
not discovery-first. This means trust tiers, signing status, and
compliance metadata are the primary UI elements, not just search and
browse. EU AI Act Article 50 transparency obligations took effect
August 2, 2026 -- skills generating user-facing outputs are in scope.
Catalog metadata should flag `eu_ai_act_scope` (05, 07).

**10. Five competitive gaps to close before TP.**
1. Skills-specific scanning (integrate SkillSpector or agent-scan into
   Konflux as a Tekton task)
2. Skill cards / compliance metadata (define a Red Hat Skill Card format
   with SLSA provenance, scan results, quality metrics, compliance tags)
3. Developer install UX (`npx skills add` is one command; RHOAI's
   OCI-based install needs a CLI wrapper)
4. Runtime policy enforcement (AWS Cedar, Google semantic governance, and
   Databricks service policies enforce at runtime; RHOAI needs equivalent
   gates, potentially through MCP Gateway)
5. Ecosystem breadth (Red Hat's catalog is small vs Azure 193, AWS 43
   packs, community 600K+; the content list action item is critical)

## Recommended follow-ups (not auto-run)

- **jira-gap lens** -- once a Jira scope is stored for skills-catalog
  (via hub.jira-sweep), crossing active work against these findings
  would surface blind spots. Retry:
  `hub.research skills-catalog jira-gap`.
- **hub.strategy skills-catalog** -- the living strategy doc synthesizes
  this research series + knowledge + Jira scope into the WHAT/WHY, gaps
  and risks, and watchlist. The series is now deep enough to support a
  strong strategy doc.
