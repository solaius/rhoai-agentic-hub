---
type: decision
title: Compass alignment session and unified skills repo exploration
description: Two action items from cross-product meeting -- Greg arranges Compass team alignment session with RHAI; all parties share existing repos and requirements for a unified Red Hat skills source-of-truth following the Nvidia model.
timestamp: 2026-08-04
decided: 2026-08-04
tags: [skills-catalog, ai-asset-pipeline, compass, unified-repo, nvidia]
components: [skills-catalog, ai-asset-pipeline, skills-registry]
source: Publishing Red Hat skills meeting 2026-08-04
---

## Context

Cross-product meeting revealed RHAI and UIE/Compass teams both building
skills registries and pipelines independently. Nvidia's single-repo +
security pipeline model endorsed by multiple parties as the target
pattern. No unified GitHub repo for Red Hat skills exists today.

## Decision

Two concrete next steps agreed:

1. **Compass alignment session:** Greg Bowman to arrange a meeting
   with the Compass team so RHAI can understand their capabilities,
   and Compass can review the MLflow RFC (PR #26). "Double-long
   meeting" to walk through both Compass and MLflow at 10,000-foot
   level.

2. **Unified repo exploration:** all parties to share existing skill
   repos and requirements. Greg to share UIE's requirements for a
   skills repo. Adel to share the MLflow RFC. Goal: determine if a
   single Red Hat skills source-of-truth repo is feasible, following
   the Nvidia model (centralized repo + security/evaluation pipeline
   + validated output).

## Consequences

- RHAI team needs to evaluate Compass capabilities before spinning up
  a separate skills repo
- Potential to avoid duplicate infrastructure if Compass already covers
  the registry/metadata layer
- Content layer (skill source code) and registry layer (metadata/
  lifecycle) may be separable -- converge on content first
