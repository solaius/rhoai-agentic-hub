---
title: Skills Registry Research -- Executive Summary
description: Living synthesis of all skills registry research -- 8-doc series covering ecosystem, upstream MLflow, landscape, competitive, requirements, and RHOAI patterns. Refreshed August 2026.
timestamp: 2026-08-04
review_after: 2026-11-04
---

# Skills Registry Research -- Executive Summary

**Last refreshed**: 2026-08-04
**Series**: 8 documents (4 original April 2026, 4 refresh August 2026)

---

## The Bottom Line (August 2026)

**The gap is closing fast.** In April 2026, no standardized skills registry
existed anywhere. By August, Databricks Unity Catalog, JFrog, and Microsoft
APM all shipped production-grade solutions. SKILL.md won the format war
(40+ tools). Red Hat now owns the upstream MLflow skills registry design
(RFC-0008, authored by Bill Murdock) but faces a narrowing window as
competitors converge on GA.

**Red Hat's differentiation holds**: hybrid-first, MLflow-native,
Kubernetes-governed skills governance that spans on-prem, edge, and
multi-cloud. No competitor offers this. The EU AI Act enforcement
(August 2 2026) creates a compliance forcing function that favors
portable, auditable governance -- Red Hat's strength.

**Immediate action**: Thursday 2026-08-07 PM sync with Databricks PM Adam
and tech lead Yuki is the next critical alignment gate. Doc 08 has the
user journeys and vision doc structure ready.

---

## Research Documents

| # | Document | Lens | Date | What it covers |
|---|----------|------|------|----------------|
| 01 | [Skills Ecosystem](01-skills-ecosystem.md) | landscape | 2026-04 | Terminology, framework analysis, packaging formats, metadata schemas, composition patterns, standards |
| 02 | [MLflow Upstream](02-mlflow-upstream.md) | upstream | 2026-04 | MLflow issues/PRs, registry architecture, Databricks prototype, Red Hat contributor activity |
| 03 | [Skill Management Landscape](03-skill-management-landscape.md) | landscape | 2026-04 | 30+ platforms surveyed, feature comparison matrix, enterprise vs. open source, emerging standards |
| 04 | [RHOAI Patterns & Meetings](04-rhoai-patterns-and-meetings.md) | — | 2026-04 | MCP registry patterns, meeting transcript analysis, decisions, open questions, people |
| 05 | [Skills Landscape Refresh](05-skills-landscape-refresh-2026-08.md) | landscape | 2026-08 | SKILL.md universality, Unity Catalog agents, Nvidia skills maturation, UIE/Compass discovery, OCP5 distribution |
| 06 | [Competitive Analysis](06-competitive-skills-registries-2026-08.md) | competitive | 2026-08 | AWS/Google/Databricks/IBM/Nvidia/Anthropic/Microsoft competitive deep dives, positioning matrix, threats |
| 07 | [MLflow Upstream Refresh](07-mlflow-upstream-refresh-2026-08.md) | upstream | 2026-08 | RFC-0008/0009 status, strategy pivot to user-journeys-first, Red Hat authorship, Databricks PM sync setup |
| 08 | [User Journeys for Databricks](08-user-journeys-databricks-alignment.md) | requirements | 2026-08 | 7 user journeys, agent-first UX shift, vision doc structure, mockup recommendations for Thursday sync |

---

## Key Findings (August 2026 Refresh)

### What changed since April

**1. SKILL.md crossed the chasm**
From 7 tools (Dec 2025) to 40+ (Aug 2026). Anthropic, OpenAI, Microsoft,
Google, JetBrains, AWS, Databricks, ByteDance all ship compatible
implementations. The format question from April is settled.

**2. Enterprise registries shipped**
- Databricks Unity Catalog (DAIS June 2026): agents, skills, MCP as
  UC securables with governance, tracing, budget controls
- JFrog Agent Skills Registry (GTC March 2026): scan-verify-sign with
  NVIDIA SkillSpector integration
- Microsoft APM: dependency manager with lockfiles and multi-agent support
- AWS Agent Registry: preview with Cedar-based policy (GA March 2026)

**3. Red Hat owns the upstream design**
Bill Murdock (jwm4) authored RFC-0008 (MVP Skill Registry) and RFC-0009
(Extended Skill Bundles) in mlflow/rfcs. RFC-0008 is under active review
with 28 commits. This is a dramatic shift from April when we were waiting
for an opportunity to submit.

**4. RFC strategy pivoted**
Matt Prahl's new approach: user-journey-only RFC first, get cross-company
alignment (RH + Databricks + AWS), then technical implementation RFC.
Root insight: vision misalignment is the blocker, not technical details.

**5. Databricks governance disconnect surfaced**
Databricks uses Unity Catalog for governance; their MLflow mantra is "make
MLflow famous." They're open to skills/agent registry if it increases
GenAI adoption but won't prioritize non-Databricks-roadmap work. This
clarifies where Red Hat's governance value-add belongs: on top of MLflow,
not in it.

**6. Red Hat's internal skills ecosystem is fragmented**
UIE/Compass team (300+ engineers) has a skills registry with scorecards
and marketplace publishing -- RHAI team was unaware until 2026-08-04.
OCP5 ships skills with operators. No "editor-in-chief" for RH skills
portfolio. Light Trail team building MCP hosting. At least 3 parallel
efforts with no coordination.

**7. Skills customization is a real enterprise need**
Generic skills break for enterprise SDLC. Josh Salomon prototyping
extension-point model (customization without forking) in Ozark. This
maps to a broader industry gap -- no platform solves skill composition
or declarative customization.

### What still holds from April

- Enterprise governance remains the differentiator (governance gap in
  MLflow is unchanged)
- MCP registry patterns transfer (7/10 user stories still apply)
- Security is first-order concern (ClawHub crisis validated this)
- Two consumption models (client-side vs server-side) remain disjoint

---

## Competitive Positioning (Updated August 2026)

| Competitor | Strength | Status | RHOAI Differentiator |
|------------|----------|--------|---------------------|
| Databricks Unity AI | First-class UC governance, budget controls, MCP | GA | Open source, on-prem, not locked to Databricks cloud |
| AWS Agent Registry | Cedar policy, semantic search, 3-persona model | Preview | Multi-cloud, no AWS lock-in, MLflow-native |
| Google Cloud API Registry | GCP integration, MCP via Apigee | Preview | Not locked to GCP, broader governance |
| IBM watsonx Orchestrate | 400+ tools, AI asset discovery, any-framework | GA | Not locked to IBM, deeper lifecycle governance |
| JFrog + NVIDIA | Supply chain security, SkillSpector, provenance | GA | Broader governance (lifecycle, approval), not just security |
| Microsoft Agent Framework | Unified SK+AutoGen, MCP steering committee | GA | Open source, not locked to Azure/M365 |
| Anthropic Marketplace | ~600 skills, growing ecosystem | GA | Enterprise governance, on-prem, multi-framework |

**Red Hat's unique position**: the only open-source, hybrid-first,
MLflow-native skills governance platform. Every competitor is locked to
a single cloud or ecosystem.

---

## Superseded Findings

The following April findings are superseded by August research:

| April finding | August status | Superseded by |
|---------------|---------------|---------------|
| "No standardized skills registry anywhere" (00, line 19) | Databricks, JFrog, Microsoft all shipped | 05 section 2 |
| "Nobody has submitted [a design proposal]" (00, line 37) | Bill Murdock authored RFC-0008/0009 | 07 section 1 |
| "SKILL.md format is emerging" (00, finding 3) | SKILL.md is now universal (40+ tools) | 05 section 1 |
| "Databricks prototype may ship first" risk (02, line 261) | Red Hat now owns the upstream design | 07 executive summary |
| Competitive table (00, lines 77-85) | All competitors advanced significantly | 06 full analysis |

---

## Recommended Actions

### Immediate (This Week)

1. **Thursday PM sync** (2026-08-07): Bring vision doc + UI mockups to
   Databricks. Doc 08 has the user journey structure and mockup
   recommendations. Key message: "our enterprise customers need
   governance Databricks customers get from Unity Catalog."

2. **Compass alignment session**: Greg Bowman arranging follow-up with
   UIE/Compass team. Evaluate before spinning up separate RHAI skills
   repo (decision from today's meeting).

### Short-term (August)

3. **RFC-0008 merge push**: Address B-Step62's review feedback (UI
   mockups, field inference). Matt's suggestion to defer trace linking
   should accelerate merge.

4. **Internal skills coordination**: Resolve the no-editor-in-chief
   problem. At minimum, map the 3+ parallel efforts (Compass, RHAI
   MLflow, OCP5 operators) and identify overlap.

### Medium-term (3.6 planning)

5. **RHOAI governance layer design**: The governance gap (lifecycle
   states, approval workflows, certification, trust tiers) is still
   unaddressed upstream and remains the value-add. Design it now.

6. **Skills-catalog research**: Run hub.research on skills-catalog
   with landscape + architecture lenses -- the Compass/UIE discovery
   and OCP5 distribution model create new architecture questions.

---

## Lenses Not Run

- **architecture**: not requested; recommend for follow-up -- the
  Compass/UIE discovery and MLflow RFC architecture decisions create
  design questions worth researching. Retry:
  `hub.research skills-registry architecture`
- **jira-gap**: no `jira:` block in components.yaml for skills-registry;
  add one to enable. Retry after adding scope:
  `hub.research skills-registry jira-gap`
