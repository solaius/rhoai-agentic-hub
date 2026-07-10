---
type: reference
title: kubeflow/hub (GitHub) — MCP Catalog upstream (likely)
description: Kubeflow Hub (formerly model-registry; README — "Red Hat drives the project's development") shipped an MCP Catalog (v1alpha1 endpoints, McpServer/McpTool entities) in Feb 2026 — the likely upstream implementation of the RHOAI MCP Catalog.
resource: https://github.com/kubeflow/hub
tags: [mcp-catalog, upstream, kubeflow]
features: [mcp-registry]
timestamp: 2026-07-09
---

Kubeflow Hub (formerly known as Model Registry — repo id redirect
verified) is alpha-status and its README pledges "Red Hat drives the
project's development through Open Source principles."

MCP Catalog capability shipped Feb–Mar 2026 [verified 2026-07-09]:

- PR #2213 "feat(mcp): introduce mcp catalog openapi spec" (merged
  2026-02-16) — `McpServer`/`McpTool` entities,
  `/api/mcp_catalog/v1alpha1/*` endpoints.
- PR #2269 source-label filtering (merged 2026-02-26); catalog landing
  page + tools-section UI work in March 2026.
- Mirrors Hub's Model Catalog pattern (YAML/HuggingFace sources,
  federated discovery) — the same pattern behind
  [model-metadata-collection](/features/mcp-ecosystem/knowledge/ref-model-metadata-collection-repo.md)
  as catalog content.

Timing (Feb build → May RHOAI 3.4 DP announcement) plus RH stewardship
makes this the likely real upstream of the RHOAI MCP Catalog — the repo
provided at intake (kubeflow/mcp-server) verified unrelated. Confirmation
tracked in
[question-kubeflow-hub-catalog-alignment](/features/mcp-catalog/knowledge/question-kubeflow-hub-catalog-alignment.md).
