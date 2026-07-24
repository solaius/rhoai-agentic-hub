---
title: "Skills Catalog research -- executive summary"
description: Living synthesis of the 4-lens standard sweep (2026-07-23) -- extend kubeflow/hub not new service, browse-only 3.6 TP feasible, curation beats volume, RHAISTRAT-1940 is existential risk, NVIDIA trust pipeline is the model, no upstream skills catalog exists (first-mover).
timestamp: 2026-07-23
review_after: 2026-10-23
---

# Skills Catalog research -- executive summary

First research run for the partition: **standard, 4 lenses, 2026-07-23**,
all lenses completed. No lens gaps to retry.

## The series

| Doc | Lens | One line |
|---|---|---|
| [01-upstream](/features/skills-catalog/research/01-upstream.md) | upstream | Kubeflow hub 3-catalog pattern, agentskills.io/AAIF governance, SKILL.md cross-agent matrix, npx CLI, MLflow RFC handoff, ODH ai-helpers |
| [02-landscape](/features/skills-catalog/research/02-landscape.md) | landscape | 3-layer taxonomy, Git-backed curation, SkillsBench quality data, trust pipelines, ARD v0.9, EU AI Act, supply-chain attacks, governance gap |
| [03-architecture](/features/skills-catalog/research/03-architecture.md) | architecture | Extend hub vs new service, BFF reuse, disconnected pipeline, source federation, metadata normalization, trust tiers, catalog-to-registry orchestration |
| [04-requirements](/features/skills-catalog/research/04-requirements.md) | requirements | 3.6 browse-only TP feasible, RHAISTRAT-1940 risk, SkillsBench evidence, RH seed content, instructional install, disconnected constraint, EU AI Act Article 50 |

## What the sweep establishes

**1. No upstream skills catalog exists -- this is a first-mover opportunity
and risk.** Unlike models (Hugging Face Hub, NVIDIA NGC) or MCP servers
(Docker MCP Catalog, mcp.directory), there is no established upstream
catalog for agent skills. skills.sh (Vercel, 669K+ indexed) is a
lightweight directory, not a governed enterprise catalog. RHOAI's skills
catalog would be the first enterprise-grade, self-hosted skills
storefront. The opportunity is differentiation; the risk is no pattern to
inherit (01, 02).

**2. Extend kubeflow/hub rather than building a new service.** The hub
already supports three catalog types (models, MCP servers, agents) with a
proven extensibility model: OpenAPI-first Go REST server, PostgreSQL
backend, pluggable CatalogSourceProvider, BFF module in odh-dashboard.
Adding skills as the fourth type is structurally identical to how MCP
servers and agents were added. A separate Go + PostgreSQL service (per
RHAISTRAT-1780) duplicates infrastructure without clear architectural
justification. The hub extension path is lower risk, lower effort, and
aligned with upstream trajectory (03).

**3. The 3.6 timeline is tight but feasible for a browse-only TP.** 6-7
two-week sprints to the October 23 code freeze fits the low end of the
6-9 sprint estimate, but only if scope is held to read-only browse/search
with pre-loaded content. Installation automation and registry integration
must be deferred. The MCP Catalog (DP 3.4, TP/GA 3.6) and Agent Catalog
(DP 3.5, deploy added 3.6 EA1) both shipped MVP as link-out, read-only
experiences first. Bill Murdock rates catalog confidence at ~90% for 3.6
(04).

**4. RHAISTRAT-1940 (pre-loaded content) is the existential risk.** No PM
is assigned. Without 15-20 working, curated skills at launch, the catalog
ships empty. Marketplace research is unanimous: empty catalogs train users
to bypass them permanently (Port 2025: 3% full trust in portal metadata,
permanent routing-around on stale data). Red Hat already has seed content
at redhat.com/skills (Summit 2026 launch: subscription-backed skill packs
for RHEL, OpenShift, Ansible with live API connections). Converting these
to catalog entries is the minimum viable content path. PM assignment by
August 2026 is critical (04).

**5. Curation beats volume by a measured margin.** SkillsBench
(Stanford/CMU/Berkeley/Oxford) scored 47,150 public skills: average
quality 6.2/12, 73% carry elevated safety risk. Curated skills raise
agent pass rates by +16.2 percentage points; self-generated skills
provide negligible benefit (-1.3pp). Focused skills with 2-3 modules
outperform larger bundles (+18.6pp vs +5.9pp). Ship 15-20 high-quality
working skills, not hundreds of unverified entries (02, 04).

**6. SKILL.md is the standard; agentskills.io/AAIF is the governance.**
The Agent Skills specification is AAIF-governed (Linux Foundation, 170+
members including Anthropic, OpenAI, Google, Microsoft, AWS). 40+ tools
support SKILL.md natively. Six major agents parse it (Claude Code, Codex,
Cursor, Gemini CLI, Cline, OpenCode). Core SKILL.md is fully portable;
divergence exists only in experimental features (allowed-tools, hooks).
The catalog should build on this standard (01, 02).

**7. Git-backed is the right catalog model for enterprise.** NVIDIA,
Microsoft, and Kubeflow Hub all use Git-backed catalogs for vendor-curated
content. GitOps-native, auditable history, works in disconnected
environments (mirror the repo). The kubeflow/hub YAML catalog source
pattern is the direct implementation vehicle. Day-1 source types: YAML
(disconnected-safe) and admin-uploaded ConfigMap. Day-2: Git repo polling
(connected-only). Future: ARD registries, Hugging Face skills (01, 03).

**8. Trust pipeline is table stakes for enterprise.** ClawHavoc (1,184
malicious skills on ClawHub, 8.5% infection rate), Snyk ToxicSkills (36%
of skills had security flaws, 76 confirmed credential-stealing payloads),
and SkillsBench (73% elevated safety risk) prove the cost of no
governance. NVIDIA's trust pipeline (SkillSpector scanning, OMS signing,
skill cards, Skill Evaluator) is the reference implementation. JFrog
partnered with NVIDIA at GTC 2026. Trust tiers (Red Hat/Partner/
Organization/Community) with visible verification status are a hard
enterprise requirement (02, 03).

**9. EU AI Act compliance is a tailwind.** Article 50 transparency
obligations take effect August 2, 2026. Skills that generate user-facing
outputs trigger disclosure requirements. Catalog metadata should flag
user-interaction scope per skill for downstream compliance. The high-risk
deadline was deferred to December 2027 (Annex III), but traceability,
risk management, and human oversight requirements are unchanged. A catalog
with skill cards, signing, and load-time logging directly supports
compliance (02, 04).

**10. The governance gap is the market opportunity.** 96% of enterprises
run AI agents in production; only 12% can govern them (OutSystems 2026).
82% have agent workflows their security teams did not know about. Every
major cloud shipped governance tooling in 2026 (AWS AgentCore, Azure
Agent 365, Google Gemini Enterprise, Databricks Unity AI). A skills
catalog with built-in trust signals, curation, and integration with the
MLflow governance registry addresses the gap limiting enterprise agent
adoption (02, 04).

## Recommended follow-ups (not auto-run)

- **competitive lens** -- the intake competitive landscape is solid but
  a focused competitive analysis could go deeper on pricing, feature
  matrices, and win/loss positioning. Retry:
  `hub.research skills-catalog competitive`.
- **jira-gap lens** -- once a Jira scope is stored for skills-catalog
  (via hub.jira-sweep), crossing active work against these findings
  would surface blind spots. Retry:
  `hub.research skills-catalog jira-gap`.
- **hub.strategy skills-catalog** -- the living strategy doc synthesizes
  this research series + knowledge + Jira scope into the WHAT/WHY, gaps
  and risks, and watchlist.
