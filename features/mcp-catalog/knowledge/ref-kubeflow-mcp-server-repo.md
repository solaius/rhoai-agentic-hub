---
type: reference
title: kubeflow/mcp-server (GitHub)
description: Kubeflow MCP Server (KEP-936, Apache-2.0, pre-release) — exposes Kubeflow Trainer operations as MCP tools; verified unrelated to catalog/registry work — a catalog-entry candidate, not the catalog's upstream.
resource: https://github.com/kubeflow/mcp-server
tags: [mcp-catalog, upstream, kubeflow]
timestamp: 2026-07-09
---

"MCP Server for AI-Assisted Development with Kubeflow Tools" — exposes
Kubeflow Trainer (≥2.2.0) operations as MCP tools so agents can plan,
submit, monitor, and manage training jobs through natural language. 23
tools across five workflow phases (planning, discovery, training,
monitoring, lifecycle); full/progressive/semantic tool modes; bearer/JWT
auth; design proposal KEP-936. Early stage as of 2026-07-09: no releases
yet.

**Relationship to the MCP Catalog — RESOLVED (research run 2026-07-09).**
Verified unrelated to any catalog/registry effort: KEP-936 and the repo
mention no catalog work; it wraps Trainer ops only. The likely intended
"upstream repo" at intake was
[kubeflow/hub](/features/mcp-catalog/knowledge/ref-kubeflow-hub-repo.md)
(ex-model-registry, shipped MCP Catalog v1alpha1 in Feb 2026 —
confirmation tracked in
[question-kubeflow-hub-catalog-alignment](/features/mcp-catalog/knowledge/question-kubeflow-hub-catalog-alignment.md)).
This repo remains relevant as a catalog *entry* candidate. Catalog
content upstream on record:
[model-metadata-collection](/features/mcp-ecosystem/knowledge/ref-model-metadata-collection-repo.md).
