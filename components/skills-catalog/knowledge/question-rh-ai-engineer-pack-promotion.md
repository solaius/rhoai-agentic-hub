---
type: question
title: Should rh-ai-engineer pack be fast-tracked from ORANGE to GREEN maturity?
status: open
description: rh-ai-engineer is the most valuable EX pack for RHOAI (model serving, vLLM, KServe, NIM, pipelines, model registry, guardrails, workbench) but has ORANGE maturity and is NOT on catalog.redhat.com -- fast-track promotion to GREEN needed for 3.6 TP catalog inclusion.
timestamp: 2026-08-02
tags: [skills-catalog, ex, rh-ai-engineer, maturity, action-item]
components: [skills-catalog]
asks:
  - Peter Double (2026-08-02, research 09-requirements-refresh)
source: research 09-requirements-refresh, EX collection.yaml maturity field
---

The rh-ai-engineer pack (11 skills) is ORANGE maturity in the EX
agentic-collections repo, meaning it is excluded from the public
catalog (catalog.redhat.com/en/ai). But it is the single most
valuable pack for RHOAI users:

- model-deploy, serving-runtime-config, model-registry, pipeline-manage,
  workbench-manage directly assist the core RHOAI workflow
- AI/ML engineers are the primary RHOAI persona
- The pack covers vLLM, KServe, NVIDIA NIM, guardrails -- exactly
  what RHOAI users need help with

**What ORANGE means**: "metadata is maintained for validation and
future promotion but excluded from the public catalog surface until
explicitly changed to GREEN." The gap is likely documentation
completeness and/or eval coverage, not fundamental quality.

**What promotion requires** (estimated):
1. Complete `.catalog/collection.yaml` to GREEN standard
2. Eval coverage for all 11 skills (or minimum top 6)
3. Validate skills work against current RHOAI APIs (3.5/3.6)
4. Add RHOAI-specific deployment instructions

Peter should coordinate with EX to prioritize this. Without
rh-ai-engineer, the RHOAI catalog launches with infrastructure
skills (SRE, OCP admin) but no AI/ML skills -- undermining the
value proposition.

**Related**: [fact-ex-onboarding-36-viable-without-konflux](/components/skills-catalog/knowledge/fact-ex-onboarding-36-viable-without-konflux.md),
[question-initial-catalog-skill-list](/components/skills-catalog/knowledge/question-initial-catalog-skill-list.md)
