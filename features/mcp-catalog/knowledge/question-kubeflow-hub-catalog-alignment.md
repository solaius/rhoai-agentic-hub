---
type: question
title: Is Kubeflow Hub's MCP Catalog the RHOAI MCP Catalog's upstream?
description: Hub (RH-driven) shipped MCP Catalog v1alpha1 in Feb 2026; timing and stewardship suggest it is the RHOAI catalog's upstream implementation, but no doc states the relationship — confirm and document.
status: open
tags: [mcp-catalog, upstream, kubeflow]
timestamp: 2026-07-09
source: hub.research run 2026-07-09 — /features/mcp-catalog/research/01-upstream-mcp-catalog-registry.md
---

Kubeflow Hub (ex-model-registry, "Red Hat drives development") merged
MCP Catalog endpoints (`/api/mcp_catalog/v1alpha1/*`, PRs #2213/#2269)
in Feb 2026 — three months before the RHOAI 3.4 MCP Catalog DP
announcement. Neither project's docs state the relationship.

1. Confirm: is kubeflow/hub the upstream implementation of the RHOAI
   MCP Catalog (as model-registry is for the model catalog)?
2. If yes: document the lineage (overview fact + a ref update) and
   correct the intake-provided "upstream repo" record permanently.
3. If no: two RH-driven MCP catalog surfaces exist in parallel —
   surface the coordination question to the catalog/registry teams.

See [ref-kubeflow-hub-repo](/features/mcp-catalog/knowledge/ref-kubeflow-hub-repo.md)
and [ref-kubeflow-mcp-server-repo](/features/mcp-catalog/knowledge/ref-kubeflow-mcp-server-repo.md).
