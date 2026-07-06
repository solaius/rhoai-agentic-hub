---
type: fact
title: Databricks/MLflow upstream collaboration — process & current status
description: How Red Hat's upstream contribution process to MLflow works, and a snapshot of what MLflow is doing natively for GenAI/registry capabilities.
timestamp: 2026-07-06
tags: [platform, mlflow, databricks, upstream, process]
review_after: 2026-08-05
source: ai-asset-registry/docs/knowledge-registry.md §7 (as of 2026-07-05)
---
**Process**: design approval is required before coding begins (roughly a 1-month lead time). PRs are broken into small, focused pieces rather than landing as one large change. Red Hat needs to extract focused design documents from its comprehensive requirements doc before proposing upstream — a single omnibus doc doesn't work as a PR-sized upstream proposal.

**Current upstream work snapshot**: MLflow's own Prompt Registry already exists, and MLflow is expanding its native GenAI capabilities more broadly — separate from, but adjacent to, Red Hat's own registry proposals. See [fact-skills-registry-mvp-analysis.md](/features/skills-registry/knowledge/fact-skills-registry-mvp-analysis.md) and [fact-agent-registry.md](/features/agent-registry/knowledge/fact-agent-registry.md) for the two concrete upstream proposals/prototypes Red Hat is tracking, and [fact-model-registry-kubeflow-hub.md](/features/platform/knowledge/fact-model-registry-kubeflow-hub.md) for the Kubeflow-side plugin-architecture work (PR #2219) already underway.

Earliest recorded discussion of this process: [fact-registry-proposal-discussion-transcript.md](/features/platform/knowledge/fact-registry-proposal-discussion-transcript.md) (2026-03-19 meeting).
