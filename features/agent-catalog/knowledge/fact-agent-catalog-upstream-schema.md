---
type: fact
title: Upstream agent-catalog schema (kubeflow/hub) and the product divergence
description: PR #2907 demoted protocol/models/imageVersion to customProperties — the exact fields the 3.5 field-set decision made load-bearing; agent.yaml is served via the artifacts endpoint (#2928) on a v1alpha1 API.
timestamp: 2026-07-16
tags: [agent-catalog, upstream, schema, kubeflow-hub]
review_after: 2026-10-16
source: 5-lens research sweep 2026-07-16 (02-upstream; adversarially verified against the PRs)
---

Verified against [kubeflow/hub](https://github.com/kubeflow/hub) (alpha
status, v0.3.12, Red Hat-maintained with a 12-month maintenance-notice
commitment):

- **Typed, filterable fields** after
  [PR #2907](https://github.com/kubeflow/hub/pull/2907) (merged 2026-07-03):
  `name, source_id, displayName, description, readme, framework, labels,
  logo, repositoryUrl, env, artifacts`. `agentType` deleted; **`protocol`,
  `models`, and `imageVersion` demoted to the free-form `customProperties`
  map**; `publishedDate` dropped.
- **Divergence to watch**: the
  [3.5 field-set decision](/features/agent-catalog/knowledge/decision-agent-catalog-35-field-set.md)
  made "communication protocol" (multi-value), optional "tested models", and
  image version the priority display fields — upstream they are untyped
  customProperties, so filtering on them has no typed contract. Worth an
  explicit check with the dashboard/backend teams before the filter UX
  hardens.
- **Deploy-flow contract**:
  [PR #2928](https://github.com/kubeflow/hub/pull/2928) (merged 2026-07-07)
  serves each kit's agent.yaml via
  `GET /api/agent_catalog/v1alpha1/agents/{id}/artifacts` as a
  `template-artifact` JSON-encoded string — the endpoint the 3.6 deploy path
  reads templates from, on a `v1alpha1` API.
- agent.yaml lives at `agents/<framework>/templates/<template>/agent.yaml`
  in the [starter-kits repo](/features/agent-catalog/knowledge/ref-agentic-starter-kits-repo.md)
  (kit roots hold deployment/, examples/, templates/, README.md).
