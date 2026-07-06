---
type: fact
title: Model Registry / Kubeflow Hub
description: The existing Kubeflow/RHOAI model registry, evolving into a broader multi-asset-type hub — already serves MCP servers via assetType.
timestamp: 2026-07-06
tags: [platform, kubeflow, model-registry]
review_after: 2026-08-05
source: ai-asset-registry/docs/knowledge-registry.md §3, §7 (as of 2026-07-05)
---
Existing registry in Kubeflow/OpenShift AI. Architecture: GORM + MySQL/PostgreSQL, REST API v1alpha3, generic `customProperties` for extensibility. Its catalog service already supports MCP servers alongside models via the `assetType` query parameter, and datasets/prompts/notebooks are planned future asset types. PR #2219 (Alessio) is genericizing the asset-type model beyond models.

A future move toward an MLflow-based direction for the model registry itself has also been flagged, as part of the broader Databricks/MLflow upstream collaboration (see [fact-databricks-mlflow-upstream-process.md](/features/platform/knowledge/fact-databricks-mlflow-upstream-process.md)) — consistent with [decision-registry-vs-catalog.md](/features/platform/knowledge/decision-registry-vs-catalog.md)'s registry=MLflow split, though not yet a committed plan as of source capture.

See [decision-kubeflow-hub-rename.md](/features/platform/knowledge/decision-kubeflow-hub-rename.md) for the KEP-0003 rename, and [ref-kubeflow-model-registry-repo.md](/features/platform/knowledge/ref-kubeflow-model-registry-repo.md) for the code.
