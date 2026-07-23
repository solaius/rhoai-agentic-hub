---
type: question
title: Should Red Hat model its skill catalog on NVIDIA's approach?
status: open
description: Should RH build a GitHub-based skill catalog modeled on NVIDIA/skills? Integrate via federation? Use NVIDIA's validation/signing infrastructure? Strong "collaborate" signal from Peter/Ann Marie; Ramesh says pull NVIDIA data into our catalog.
timestamp: 2026-07-23
tags: [skills-catalog, nvidia, collaboration, strategy]
features: [skills-catalog, skills-registry]
source: three intake meetings 2026-07-23
---

NVIDIA's skills repo (github.com/nvidia/skills) is the most mature
public skills catalog in the ecosystem. Ann Marie: "really good, we
should build something like that." Peter: "play nice with NVIDIA, be
the Robin to their Batman."

**Options on the table**:

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

**Key question**: should this be a case-by-case evaluation or a
broader NVIDIA collaboration strategy? Needs stakeholder input from
Adel and the NVIDIA partnership team.
