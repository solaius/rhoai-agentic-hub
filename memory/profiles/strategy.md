---
type: profile
description: "Strategy: registry=governance (MLflow), catalog=discovery (Kubeflow hub); metadata-first, plugin-based"
timestamp: 2026-07-05
status: current
valid_from: 2026-07-05
review_after: 2026-08-04
source: carried from ai-asset-registry CLAUDE.md at hub creation
---
- Core split: Registry = Governance (MLflow) · Catalog = Discovery (Kubeflow
  Hub). Metadata-first, plugin-based extensibility.
- Three separated concerns in the proposal: (1) Registry — storage/versioning/
  distribution; (2) Studio — prompt/skill iteration UI; (3) Ecosystem/
  marketplace — packaging, distribution, partner plugins.
- Upstream: MLflow/Databricks collaboration; design approval before coding.

## History
- 2026-07-05 — **Creation** at hub seed; values carried from old repo.
