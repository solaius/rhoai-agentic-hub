---
type: fact
title: Model Registry / Kubeflow Hub
description: The existing Kubeflow/RHOAI model registry, evolving into a broader multi-asset-type hub — already serves MCP servers via assetType.
timestamp: 2026-07-06
tags: [asset-registry, kubeflow, model-registry]
review_after: 2026-08-05
source: ai-asset-registry/docs/knowledge-registry.md §3 (as of 2026-07-05)
---
Existing registry in Kubeflow/OpenShift AI. Architecture: GORM + MySQL/PostgreSQL, REST API v1alpha3, generic `customProperties` for extensibility. Its catalog service already supports MCP servers alongside models via the `assetType` query parameter, and datasets/prompts/notebooks are planned future asset types. PR #2219 (Alessio) is genericizing the asset-type model beyond models.

See [decision-kubeflow-hub-rename.md](/features/asset-registry/knowledge/decision-kubeflow-hub-rename.md) for the KEP-0003 rename, and [ref-kubeflow-model-registry-repo.md](/features/asset-registry/knowledge/ref-kubeflow-model-registry-repo.md) for the code.
