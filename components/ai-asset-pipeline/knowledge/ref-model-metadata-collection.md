---
type: reference
title: "opendatahub-io/model-metadata-collection -- AI asset metadata tool"
description: Go tool that extracts/enriches/catalogs metadata from OCI model images and MCP servers; already multi-asset (models + MCP); generates catalog YAML for Kubeflow Hub; the natural extension point for skills and agents.
resource: https://github.com/opendatahub-io/model-metadata-collection
tags: [ai-asset-pipeline, metadata, catalog, oci, go]
components: [ai-asset-pipeline, platform]
timestamp: 2026-08-03
source: GitHub repo README + session research 2026-08-02
---

Go application that discovers, extracts, enriches, and catalogs metadata
from Red Hat AI assets. Already handles **two asset types**:

- **Models**: discovers from HuggingFace collections, extracts from OCI
  ModelCar container layers, enriches with HuggingFace API data,
  classifies as generative/predictive/unknown
- **MCP servers**: generates separate catalog YAMLs for Red Hat, partner,
  and community MCP servers

**Pipeline**: discovery -> OCI extraction -> enrichment (priority:
HuggingFace YAML -> modelcard -> API -> registry -> defaults) ->
classification/validation -> catalog YAML assembly -> quality reporting.
Runs via GitHub Actions with configurable concurrency.

**Extension point**: adding skills and agents as asset types would
follow the same pattern -- extract metadata from SKILL.md frontmatter
or agent manifests, enrich, classify, and generate catalog YAML. The
tool's multi-asset architecture already supports this.

No skills or agent support exists yet.
