---
type: decision
title: Include filtered NVIDIA skills as pre-loaded partner content in skills catalog
description: PE (Adel), Eng arch (Ann Marie), and PM (Peter) aligned on including a curated subset of NVIDIA skills as pre-loaded partner content for skills catalog launch; filtering for RHOAI platform relevance required; NVIDIA is VIP partner tier.
decided: 2026-08-05
timestamp: 2026-08-05
tags: [skills-catalog, nvidia, partnership]
components: [skills-catalog, ai-asset-pipeline]
source: Slack channels C0BNLNRB6FK + D0BAMG10K8Q, 2026-08-05
---

## Context

NVIDIA has the most mature public skills catalog (300+ skills across
35+ product lines, OMS signing, SkillSpector scanning, Tier-3 evals).
Babak Mozaffari (NVIDIA PM) reached out about including NVIDIA skills
in RHOAI for the Red Hat AI Factory with NVIDIA joint offering.

## Decision

PE, Eng architecture, and PM aligned on including a curated subset of
NVIDIA skills as pre-loaded partner content for the skills catalog
launch. Filtering is required for RHOAI platform relevance -- not all
300+ NVIDIA skills are appropriate (e.g., CUDA driver skills vs.
GPU-effectiveness skills).

Key constraints:
- Red Hat skills are the top priority ("100% top of list")
- NVIDIA skills need curation for RHOAI platform relevance
- Adel also interested in adopting NVIDIA's skill lifecycle model
- NVIDIA is VIP partner tier for DP/TP launch

## Consequences

- Need a curation process to select relevant NVIDIA skills from the
  300+ available
- Need to work with NVIDIA (Babak/Raj) on filtering
- Verification/validation pipeline alignment with ai-asset-pipeline
- Skills catalog launch planning should include NVIDIA partner track

See also: [[question-skills-catalog-nvidia-collaboration]],
[[ref-nvidia-skills-repo]], [[fact-nvidia-skills-catalog-landscape]],
[[person-babak-mozaffari]], [[person-raj-rao]]
