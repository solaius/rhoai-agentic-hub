---
type: decision
title: kubeflow/model-registry renamed to "Kubeflow Hub"
description: KEP-0003 renames the project and moves its images to reflect a broader multi-asset-type scope.
decided: 2026-07-06
timestamp: 2026-07-06
tags: [platform, kubeflow, rename]
source: ai-asset-registry/docs/knowledge-registry.md §3 (as of 2026-07-05)
review_after: 2026-08-05
---
**Context**: `kubeflow/model-registry` was outgrowing a models-only scope as datasets, prompts, notebooks, and MCP servers needed representation.

**Decision**: KEP-0003 renames the project to "Kubeflow Hub"; container images move to `ghcr.io/kubeflow/hub/*`.

**Consequences**: Signals the project's direction toward a generic multi-asset-type hub, aligning with the registry-vs-catalog framing (see [decision-registry-vs-catalog.md](/features/platform/knowledge/decision-registry-vs-catalog.md)). Repo name itself (`kubeflow/model-registry`) has not yet changed as of source capture.

Note: source doesn't give the KEP-0003 approval date; `decided` set to drafting date.
