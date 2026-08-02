---
type: fact
title: EX agentic skills -- detailed inventory for RHOAI catalog planning
description: Full breakdown of Red Hat Emerging Technology (EX) agentic skill packs -- 7 packs, ~68 skills total, organized by persona; key input for building the initial RHOAI skills catalog list (RHAISTRAT-1940).
timestamp: 2026-08-02
tags: [skills-catalog, ex, inventory, content-planning]
components: [skills-catalog]
review_after: 2026-09-15
source: https://github.com/RHEcosystemAppEng/agentic-collections, https://www.redhat.com/en/agentic-skills, https://catalog.redhat.com/en/ai
---

Full inventory of EX agentic skills as of August 2026. These are the
primary candidate pool for RHAISTRAT-1940 (pre-loaded skills) and the
initial RHOAI skills catalog list.

## Packs and personas

| Pack | Count | Persona | Product coverage |
|---|---|---|---|
| rh-basic | 6 | General Red Hat users | CVE, diagnostics, lifecycle, support cases |
| rh-sre | 13 | Site Reliability Engineers | OpenShift + RHEL ops |
| rh-developer | 14 | Application Developers | Dev workflows |
| rh-virt | 10 | Virtualization Admins | OpenShift Virt |
| ocp-admin | 3 | OpenShift Administrators | Cluster admin |
| rh-ai-engineer | 11 | AI/ML Engineers | AI/ML workflows |
| rh-automation | 11 | Automation Leads | Ansible + automation |

Total: ~68 skills across 7 packs.

## rh-basic pack (detailed -- publicly documented)

| Skill | Invocation | What it does |
|---|---|---|
| CVE Explainer | /red-hat-cve-explainer | CVE lookup with Red Hat severity ratings, impact assessment, recommendations |
| Diagnostic Data Gathering | /red-hat-diagnostics | sosreport, must-gather, Ansible diagnostic bundles for support cases |
| Security MCP Setup | /red-hat-security-mcp-setup | One-time setup helper for Red Hat Security MCP (Dev Preview, self-deletes) |
| Product Lifecycle Advisor | /red-hat-product-lifecycle | Support phase lookup, update eligibility, upgrade planning |
| Support Severity Helper | /red-hat-support-severity | Support case severity determination, SLA guidance, 24x7 coverage advice |
| Bootstrap Installer | /red-hat-get-started | Meta-skill that installs all other skills, then self-deletes |

## Live data connections

Skills connect to Red Hat production APIs (not cached/synthetic):
- Red Hat CVE Database
- Security Advisories API
- Vulnerability Service
- Product Lifecycle API (coming soon)
- Red Hat Customer Portal

## Catalog status

On catalog.redhat.com/en/ai:
- 4 skill packs listed (basic, SRE, OCP, OCP Virt)
- 2 individual skills listed (RHEL Best Practices, RHEL Translator)
- "Coming soon" placeholders signal active expansion

Not yet listed: rh-developer, rh-ai-engineer, rh-automation packs.

## Design principles

EX skills follow 7 design principles (SKILL_DESIGN_PRINCIPLES.md):
DP1 document consultation transparency, DP2 parameter spec/ordering,
DP3 description conciseness, DP4 dependencies declaration, DP5 human-
in-the-loop for critical ops, DP6 mandatory sections (Prerequisites/
When to Use/Workflow), DP7 credential security.

## Relevance to RHOAI catalog

These skills are the fastest path to solving RHAISTRAT-1940 because:
1. Already exist and are production-tested
2. Subscription-backed (aligns with RHOAI value prop)
3. Already have an external catalog presence
4. Apache 2.0 licensed (permissive)
5. Structured format (SKILL.md) is close to catalog metadata needs

Open questions:
- Which packs/skills go into RHOAI catalog vs. remain external-only?
- Does catalog.redhat.com/en/ai list == RHOAI catalog list? (Ann Marie's question)
- Supply chain: who builds/signs/publishes these into RHOAI?
- Are the 3 unlisted packs (developer, ai-engineer, automation) ready?
