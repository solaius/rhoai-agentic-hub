---
type: question
title: What is the initial list of skills for the RHOAI Skill Catalog?
status: open
description: What Red Hat and partner skills should ship pre-loaded in the RHOAI Skill Catalog out of the box? Peter working with EX and PE teams to build the list; deadline before 3.6 EA1 (EA2+Stable for integration). RHAISTRAT-1940 PM now assigned.
timestamp: 2026-08-02
tags: [skills-catalog, content, partnerships, pre-loaded]
components: [skills-catalog]
asks:
  - Ann Marie Fred (2026-07-30, architectural strategy GDoc)
source: Ann Marie Fred architectural strategy GDoc -- TODO comment tagging Peter Double
---

From Ann Marie Fred's architectural strategy document: "What is the
initial list of skills that we intend to have in our Catalog? See also:
https://catalog.redhat.com/en/ai/skills - will these lists be the same?"

Ann Marie tagged Peter Double as the owner, noting: "Peter handles the
partnership programs, so IMO this would fall under his purview, but it
could verge into Agent Ops and Adel's area."

Catherine Weeks also asked: "Who is responsible for defining what skills
we'll put into the public domain - is there a team already working on
this or does this need to be defined?"

**Update 2026-08-02**: Peter Double is actively working with Emerging
Technology (EX) and Partnership Ecosystem (PE) teams to build the
initial skills list. RHAISTRAT-1940 now has a PM assigned. Timeline
constraint: the list must be understood before 3.6 EA1 completes so
that EA2 and Stable releases have time to integrate the content.

**Dependencies**:
- RHAISTRAT-1940 (pre-loaded content risk -- without content, catalog
  launches empty)
- Red Hat skills production pipeline (build/sign/publish via Konflux --
  not yet planned as of late July 2026, epic-sized)
- Partner verification program (similar to model verification)
- catalog.redhat.com/en/ai/skills (existing external catalog -- should
  these lists align?)

**EX skills inventory** (2026-08-02): detailed breakdown of all 7 EX
agentic packs (~68 skills) now filed -- see
[fact-ex-agentic-skills-detailed-inventory](/components/skills-catalog/knowledge/fact-ex-agentic-skills-detailed-inventory.md).
Peter confirmed interest in bringing these into the RHOAI catalog as the
primary seed content pool.

**Research-backed curation recommendation** (2026-08-02, research
09-requirements-refresh): 30-35 curated skills from 4 packs for 3.6 TP:
- rh-basic (6) -- foundation, GREEN maturity
- rh-sre (9-10) -- evaluated skills only, GREEN maturity
- ocp-admin (3) -- all skills, GREEN maturity
- rh-ai-engineer (11) -- ORANGE maturity, needs fast-track promotion
Deferred: rh-developer (ORANGE, overlaps quickstarts), rh-virt (GREEN
but non-core persona), rh-automation (ORANGE, adjacent persona).
SkillsBench evidence: curated +16.2pp pass rate vs uncurated.
See [fact-ex-onboarding-36-viable-without-konflux](/components/skills-catalog/knowledge/fact-ex-onboarding-36-viable-without-konflux.md),
[question-rh-ai-engineer-pack-promotion](/components/skills-catalog/knowledge/question-rh-ai-engineer-pack-promotion.md).

**Related**: [fact-skills-preloaded-content-risk](/components/skills-catalog/knowledge/fact-skills-preloaded-content-risk.md),
[fact-redhat-agentic-skills-seed-content](/components/skills-catalog/knowledge/fact-redhat-agentic-skills-seed-content.md),
[ref-ex-agentic-collections-repo](/components/skills-catalog/knowledge/ref-ex-agentic-collections-repo.md),
[ref-redhat-ai-catalog-page](/components/skills-catalog/knowledge/ref-redhat-ai-catalog-page.md)
