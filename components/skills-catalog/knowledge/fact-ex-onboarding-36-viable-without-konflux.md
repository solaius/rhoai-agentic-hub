---
type: fact
title: EX skills can enter 3.6 TP catalog without Konflux via YAML source provider
description: EX agentic skills can enter the RHOAI catalog for 3.6 TP using the YAML catalog source provider (ConfigMap-baked, ships with operator) -- no OCI/Cosign/Tekton needed; one-time SkillSpector scan for security; 30-35 curated skills from 4 packs (rh-basic, rh-sre, ocp-admin, rh-ai-engineer); 2-3 sprint effort parallelized; full Konflux pipeline deferred to 3.7+.
timestamp: 2026-08-02
tags: [skills-catalog, ex, onboarding, konflux, pipeline]
components: [skills-catalog]
review_after: 2026-10-02
source: research 08-upstream-refresh, research 09-requirements-refresh
---

The minimum viable pipeline for getting EX skills into the RHOAI 3.6
TP catalog does NOT require Konflux:

1. **Source**: agentic-collections Git repo pinned to a release tag
2. **Transform**: script maps SKILL.md frontmatter + collection.yaml
   to Kubeflow YAML catalog format
3. **Scan**: one-time SkillSpector run (64 patterns, 16 categories)
4. **Package**: YAML catalog source baked into ConfigMap in RHOAI
   operator manifests
5. **Distribute**: ships with the RHOAI operator image

This is acceptable because EX skills are Red Hat-authored, Red Hat-
controlled, and the catalog is read-only (no runtime execution risk).

**Content recommendation**: 30-35 curated skills from 4 packs:
- rh-basic (6) -- foundation skills, all GREEN maturity
- rh-sre (9-10) -- evaluated skills only, GREEN maturity
- ocp-admin (3) -- all skills, GREEN maturity
- rh-ai-engineer (11) -- ORANGE maturity but most valuable RHOAI pack;
  needs fast-track promotion to GREEN

**Timeline**: 2-3 sprints parallelized (metadata mapping + eval gap
fill concurrent).

**What 3.6 TP does NOT provide**: automated rebuild, Cosign signing,
in-toto attestation, SBOM generation, continuous scanning, partner
skill ingestion. All deferred to 3.7+ Konflux pipeline.
