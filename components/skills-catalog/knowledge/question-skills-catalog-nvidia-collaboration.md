---
type: question
title: How should Red Hat collaborate with NVIDIA on skills for the catalog?
status: open
description: "Inclusion decided (2026-08-05) -- PE/Eng/PM aligned on filtered NVIDIA skills as pre-loaded partner content. Remaining open: curation process (which of 300+ skills?), verification pipeline integration with ai-asset-pipeline, lifecycle model adoption, and broader NVIDIA collaboration strategy."
timestamp: 2026-07-23
tags: [skills-catalog, nvidia, collaboration, strategy]
components: [skills-catalog, skills-registry, ai-asset-pipeline]
source: three intake meetings 2026-07-23; Slack alignment 2026-08-05
---

NVIDIA's skills repo (github.com/nvidia/skills) is the most mature
public skills catalog in the ecosystem. Ann Marie: "really good, we
should build something like that." Peter: "play nice with NVIDIA, be
the Robin to their Batman."

## Decided (2026-08-05)

PE (Adel), Eng arch (Ann Marie), PM (Peter) aligned on including a
curated subset of NVIDIA skills as pre-loaded partner content for
skills catalog launch. NVIDIA is VIP partner tier. Babak Mozaffari
and Raj Rao confirmed as NVIDIA PM contacts.
See [[decision-include-nvidia-skills-as-partner-content]].

## Remaining open items

1. **Curation process**: which of the 300+ NVIDIA skills are relevant
   for RHOAI? Ann Marie: "skills for using their GPUs effectively",
   not CUDA driver skills. Adel: "skills align with things that are
   reusable on RHAI". Need a filtering pass with NVIDIA.
2. **Verification pipeline integration**: how does NVIDIA's trust
   pipeline (SkillSpector, OMS signing, Tier-3 evals) fit into the
   ai-asset-pipeline intake flow? Peter: "We love how NVIDIA is
   verifying/validating and are looking at integrating that into our
   pipeline."
3. **Lifecycle model adoption**: Adel interested in NVIDIA's skill
   lifecycle model ("their skill lifecycle would be interesting too").
4. **Broader collaboration strategy**: case-by-case or a broader
   NVIDIA collaboration strategy? Needs Partnership Ecosystem input
   (Paul Christensen, sdashet tagged but not yet responded).

## Original options (2026-07-23)

1. **Model on NVIDIA's approach**: build an equivalent Red Hat skills
   GitHub repo with signing, cards, evals, and sync pipeline. Catalog
   (Kubeflow) surfaces it in the RHOAI UI. Ann Marie's recommendation.
2. **Integrate via federation**: pull NVIDIA skill data (cards, evals,
   scan results) into our catalog. Ramesh's preference -- "whatever the
   data they have, we can slurp it in."
3. **Sell our framework to NVIDIA**: Ramesh suggests NVIDIA may benefit
   from our catalog framework (indexing, search, filtering); their
   roadmap items like syndication are not all complete.
4. **Adopt NVIDIA's verification pipeline**: use SkillSpector, Skill
   Evaluator, and OMS signing in our CI/CD. Loosely coupled integration
   per Aditi's analysis.

**Signals**: NVIDIA is moving fast and building on primitives Red Hat
taught them (Adel). OpenShell precedent -- NVIDIA reached out, RH
productized. Peter concerned about being outpaced.
