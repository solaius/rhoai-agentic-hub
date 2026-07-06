---
type: fact
title: AI asset registry program risks — upstream process and registry-strategy migration
description: Two execution risks to the registry program — the Databricks upstream review cadence, and migration implications of moving from a Kubeflow-based to an MLflow-based registry direction.
timestamp: 2026-07-06
tags: [platform, mlflow, kubeflow, risk, upstream]
review_after: 2026-08-05
source: ai-asset-registry/docs/knowledge-registry.md §13 (as of 2026-07-05)
---
**Databricks upstream process**: design-approval review takes roughly a month; PRs must stay small and focused to move through it — a real constraint on how much of any registry proposal (MCP, agent, skills) can land in one pass. See [question-mlflow-upstream-registry-scope.md](/features/mcp-registry/knowledge/question-mlflow-upstream-registry-scope.md) for the MCP-specific scoping question this creates.

**Model registry transition**: moving the model registry direction from Kubeflow-based to MLflow-based (see [decision-registry-vs-catalog.md](/features/platform/knowledge/decision-registry-vs-catalog.md)) has migration implications that haven't been worked through — existing Kubeflow-registry consumers and data need a path forward.
