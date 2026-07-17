---
type: question
title: How should the agent registry relate to the pre-deployment agent artifacts registry?
description: Varsha's post-deployment agent registry proposal explicitly defers this — open question on how it should eventually reconcile with a future pre-deployment registry for agent definitions/images.
status: open
timestamp: 2026-07-16
tags: [agent-registry, scope, mlflow]
source: ai-asset-registry/docs/knowledge-registry.md §7 (as of 2026-07-05)
---
The upstream agent registry proposal ([fact-agent-registry.md](/features/agent-registry/knowledge/fact-agent-registry.md)) is scoped to post-deployment only — live, running agents. Pre-deployment agent artifacts (versioning agent definitions/images, closer to how MCP Registry governs static MCP servers) are explicitly deferred to a separate follow-up proposal. Open question: how should the two eventually relate — one registry spanning two lifecycles, or two separate registries that hand off at deploy time?

**Evidence 2026-07-16**: the architecture lens recommends separate entities with a hard nullable `version_ref` (unmatched discovered instances become visible shadow inventory), MLflow LoggedModel as the lineage hub; the requirements lens finds regulators effectively need both views (approved vs running). Recommendation, not decision. See [research/09-architecture](/features/agent-registry/research/09-architecture.md) §2 and [research/10-requirements](/features/agent-registry/research/10-requirements.md).
