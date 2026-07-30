---
type: reference
title: "Agent Skills Architectural Strategy (GDoc, Ann Marie Fred)"
description: Cross-team architectural strategy for the skills ecosystem -- plan (catalog TP + registry DP in 3.6), catalog/registry separation of concerns, skill lifecycle journeys (developer, verify/publish, catalog admin, catalog user, agent builder), supply chain security (threats + mitigations), installer comparison (7 methods), OpenShell mitigation, NVIDIA-style features (skill cards, CI/CD evals, signed skills, partner verification); living doc with active comment threads from Roland Huss, Bill Murdock, Ramesh Reddy, Catherine Weeks.
resource: https://docs.google.com/document/d/1L8jM6UdCX665zn87M6x5fzXAgQ4eicpvseSb3SY1fsE
tags: [skills-catalog, skills-registry, architecture, strategy, supply-chain, gdoc]
features: [skills-catalog, skills-registry]
timestamp: 2026-07-30
source: Google Doc by Ann Marie Fred, contributors Bill Murdock, Ramesh Reddy, Edson Tirelli; shared July 2026
---

Ann Marie Fred's architectural strategy document covering the full skills
ecosystem for RHOAI. Internal draft, living document with active comment
threads.

**Plan** (as of late July 2026):
- Skill Catalog: TP in RHOAI v3.6 GA. AI Hub team, Kubeflow. In
  progress, no blockers.
- Skill Registry: DP in RHOAI v3.6 GA. Agent Dev team, MLflow. POC
  developed, working with Databricks for design acceptance before
  upstream contribution.
- Agent Registry: design work in parallel, RFC upstream soon. Timing
  depends on upstream review pace.

**Key sections**: catalog vs registry separation of concerns (detailed
table + source-of-truth/download/cardinality/update explanations),
terminology definitions, skill lifecycle (5 journeys), supply chain
security (threat landscape + mitigation controls + build/package/publish
pipeline), skill installers (7 methods compared), NVIDIA-inspired
features (skill cards, CI/CD evals, automated signature verification,
partner verification program, marketplace syndication).

**Notable comment threads**:
- Roland Huss: challenges Git/MLflow metadata split; asks why catalog
  can't manage governance; wants skill bundles as first-class KEP
- Catherine Weeks: who defines the public skills list? (Ann Marie:
  Peter handles partnerships)
- Ramesh Reddy: drop homegrown CLI bundles to simplify RFC; mirrored
  Git for disconnected golden copies; SkillSpector reference
- Bill Murdock: NVIDIA signing signs the skill/card/eval/benchmark
  tuple, not just the skill; Databricks likes APM; MLflow RBAC is
  built-in per-resource granularity

**Design docs referenced**:
- [Kubeflow hub PR #2973](/features/skills-catalog/knowledge/ref-kubeflow-skills-catalog-design.md) (catalog)
- [MLflow RFC PR #26](/features/agent-registry/knowledge/ref-mlflow-rfc-0008.md) (registry)
- [MLflow RFC PR #27](/features/skills-registry/knowledge/ref-mlflow-skills-registry-post-mvp-rfc.md) (post-MVP)
