---
type: reference
title: "Konflux -- Red Hat's open-source secure software factory"
description: Konflux is a Kubernetes-native software factory built on Tekton achieving SLSA L3 compliance -- hermetic builds, in-toto attestations via Tekton Chains, keyless Sigstore signing, SBOMs, Conforma policy gating; built 2M+ artifacts across 4 architectures.
resource: https://github.com/konflux-ci/konflux-ci
tags: [ai-asset-pipeline, konflux, supply-chain, tekton, slsa]
components: [ai-asset-pipeline]
timestamp: 2026-08-03
source: konflux-ci.dev docs + session research 2026-08-02
---

Red Hat's open-source secure software factory, the foundation of the AI
asset pipeline. Key capabilities:

- **SLSA Build Level 3**: cryptographic provenance chain from source to
  artifact via Tekton Chains
- **Keyless signing**: Sigstore (Cosign + Fulcio + Rekor), no private
  key management
- **Hermetic builds**: network-isolated, reproducible, SBOMs as
  byproduct
- **Multi-architecture**: x86_64, ARM, PPC64, Z from a single pipeline
- **Conforma integration**: machine-readable policy contracts gate
  artifact promotion
- **Contract-first**: `.tekton/` directory in source repo defines the
  pipeline

Already builds RHOAI component images (notebooks, operators,
dashboard). Already signs ModelCar images via RHTAS. The AI asset
pipeline extends this to skills, MCP servers, and agents as additional
OCI artifact types.

Docs: https://konflux-ci.dev/
