---
type: question
title: Is Kubeflow Hub's MCP Catalog the RHOAI MCP Catalog's upstream?
description: ANSWERED (owner, 2026-07-10) — kubeflow/hub IS the RHOAI MCP Catalog's current upstream; lineage now documented in the ref and the overview fact.
status: answered
tags: [mcp-catalog, upstream, kubeflow]
timestamp: 2026-07-09
source: hub.research run 2026-07-09 — /features/mcp-catalog/research/01-upstream-mcp-catalog-registry.md
---

**Answer (owner, 2026-07-10): yes — kubeflow/hub is the RHOAI MCP
Catalog's current upstream.** Lineage documented in
[ref-kubeflow-hub-repo](/features/mcp-catalog/knowledge/ref-kubeflow-hub-repo.md)
and the
[overview fact](/features/mcp-catalog/knowledge/fact-mcp-catalog-overview.md);
the intake-provided kubeflow/mcp-server record stands corrected.

Original question (for the record): Kubeflow Hub (ex-model-registry,
"Red Hat drives development") merged MCP Catalog endpoints
(`/api/mcp_catalog/v1alpha1/*`, PRs #2213/#2269) in Feb 2026 — three
months before the RHOAI 3.4 MCP Catalog DP announcement. Neither
project's docs stated the relationship.

1. Confirm: is kubeflow/hub the upstream implementation of the RHOAI
   MCP Catalog (as model-registry is for the model catalog)?
2. If yes: document the lineage (overview fact + a ref update) and
   correct the intake-provided "upstream repo" record permanently.
3. If no: two RH-driven MCP catalog surfaces exist in parallel —
   surface the coordination question to the catalog/registry teams.

See [ref-kubeflow-hub-repo](/features/mcp-catalog/knowledge/ref-kubeflow-hub-repo.md)
and [ref-kubeflow-mcp-server-repo](/features/mcp-catalog/knowledge/ref-kubeflow-mcp-server-repo.md).
