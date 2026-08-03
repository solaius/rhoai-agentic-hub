---
type: fact
title: AI Asset Pipeline -- overview and current status
description: Konflux-based trust pipeline extending the existing model pipeline (ModelCar, RHTAS/Sigstore, model-metadata-collection) to skills, MCP servers, and agents; shared output contract (OCI + cosign + in-toto + SBOM); confirmed extend-not-build-new by Adam Bellusci 2026-08-03; not yet planned, epic-sized.
timestamp: 2026-08-03
tags: [ai-asset-pipeline, konflux, supply-chain, overview]
components: [ai-asset-pipeline]
review_after: 2026-11-03
source: session synthesis 2026-08-02/03; Adam Bellusci confirmation 2026-08-03
---

The AI Asset Pipeline extends Red Hat's existing model trust pipeline
to cover all AI asset types: skills, MCP servers, and agents. It is
shared platform infrastructure consumed by catalogs and registries --
not a feature of either.

**What it is**: a Konflux CI/CD pipeline that scans, signs, attests,
and OCI-packages AI assets before they enter any catalog or registry.

**What already exists for models**:
- ModelCar: models packaged as OCI container images (GA)
- RHTAS/Sigstore: signs ModelCar images
- Konflux: builds RHOAI component images with SLSA L3 provenance
- model-metadata-collection: Go tool that extracts/enriches metadata
  from OCI model images AND MCP servers (already multi-asset)

**What's new**: extending these to handle skills, MCP servers, and
agents as additional artifact types with per-type scan profiles:

| Artifact | Scan profile | Threat focus |
|---|---|---|
| Skills | SkillSpector (68 vuln, 17 categories) | NL malware, prompt injection, memory alteration |
| MCP servers | OWASP MCP Top 10 | Tool poisoning, credential theft, unauthorized network |
| Agents | Composite (skills + MCP + harness-specific) | All of the above plus harness risks |

**Shared output contract**: every artifact type produces OCI artifact +
cosign signature + in-toto attestation + SBOM. Catalogs, registries,
and Quay all consume these the same way.

**Current status** (2026-08-03): direction confirmed by Adam Bellusci
(AI Hub owner). Not yet planned in Jira. Epic-sized. First
implementation targets skills (smallest artifact, most urgent threat
data). See
[decision-extend-existing-model-pipeline](/components/ai-asset-pipeline/knowledge/decision-extend-existing-model-pipeline.md).

**Key links**:
- [RHOAI architecture repo](/components/platform/knowledge/ref-opendatahub-architecture-context-repo.md)
- [Konflux](/components/ai-asset-pipeline/knowledge/ref-konflux.md)
- [KitOps/ModelPack](/components/ai-asset-pipeline/knowledge/ref-kitops-modelpack.md)
- [model-metadata-collection](/components/ai-asset-pipeline/knowledge/ref-model-metadata-collection.md)
- [NVIDIA SkillSpector](/components/ai-asset-pipeline/knowledge/ref-nvidia-skillspector.md)
- [Conforma](/components/ai-asset-pipeline/knowledge/ref-conforma.md)
- [Supply chain threat landscape](/components/skills-catalog/knowledge/fact-skills-supply-chain-security.md)
- [Competitive positioning](/components/skills-catalog/research/05-competitive.md)
