---
type: reference
title: "KitOps -- CNCF sandbox OCI packaging for AI assets"
description: KitOps packages AI assets (models, agents, MCP servers, datasets, prompts) as OCI artifacts using the CNCF ModelPack spec; Kitfile manifest, Cosign-compatible signing, selective layer unpacking, any OCI registry.
resource: https://github.com/kitops-ml/kitops
tags: [ai-asset-pipeline, oci, cncf, packaging, modelpack]
components: [ai-asset-pipeline]
timestamp: 2026-08-03
source: GitHub repo + session research 2026-08-02
---

CNCF Sandbox project implementing the ModelPack specification. Packages
AI projects as ModelKits -- self-contained, immutable OCI bundles.

**Supported asset types**: models, agents, MCP servers, datasets,
prompts, code, configs, experiment results. Skills not explicitly
mentioned but structurally identical (folder-based artifacts).

**Key properties**: tamper-proof (SHA-256 digests), signable
(Cosign-compatible), registry-agnostic (any OCI-compliant registry),
selective unpacking (pull only the layers you need). v1.13.0 added
`--as-skill` unpacking for Claude Code/Codex.

**Relevance**: KitOps/ModelPack is the standards-based path for
OCI-packaging skills and MCP servers alongside models. The Kitfile
manifest declares what an artifact contains, enabling the pipeline to
select the right scan profile per asset type.

Red Hat contributes to the CNCF ModelPack spec.

Spec: https://modelpack.org/
