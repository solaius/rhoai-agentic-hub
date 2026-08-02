---
type: reference
title: RHEcosystemAppEng/agentic-collections -- EX agentic skills source repo
description: GitHub source for all Red Hat Emerging Technology agentic skill packs -- 7 packs (~68 skills) covering SRE, Developer, Virt, OCP Admin, AI Engineer, Automation, and Basic personas; Apache 2.0 licensed with design principles, eval reports, and contribution tooling.
timestamp: 2026-08-02
resource: https://github.com/RHEcosystemAppEng/agentic-collections
tags: [skills-catalog, ex, source-code, github]
components: [skills-catalog]
---

Source repository for all Red Hat Emerging Technology (EX) agentic skills.
Maintained by Red Hat Ecosystem Engineering under Apache 2.0.

**Packs** (persona-scoped collections):

| Pack | Skills | Persona |
|---|---|---|
| rh-sre | 13 | Site Reliability Engineers |
| rh-developer | 14 | Application Developers |
| rh-virt | 10 | Virtualization Admins |
| ocp-admin | 3 | OpenShift Administrators |
| rh-ai-engineer | 11 | AI/ML Engineers |
| rh-automation | 11 | Automation Leads |
| rh-basic | 6 | General Red Hat Users |

**Key files**: SKILL_DESIGN_PRINCIPLES.md (7 design principles),
COLLECTION_SPEC.md (pack structure spec), eval/ (skill evaluation reports).

**Skill format**: SKILL.md frontmatter with `model` (inherit|sonnet|haiku)
and `color` fields; mandatory sections: Prerequisites, When to Use, Workflow.

**Distribution**: pre-packaged ZIP files per pack on Releases page; catalog
UI at catalog.redhat.com/en/ai aggregates periodically from this repo.

Contact: agentskills@redhat.com
