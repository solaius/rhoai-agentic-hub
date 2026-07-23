---
type: decision
title: Skills Catalog and Skills Registry are separate products
description: Catalog (Kubeflow, marketplace/discovery) and registry (MLflow, workspace/governance) confirmed as separate products with different backends, shipped independently; catalog first.
decided: 2026-07-23
timestamp: 2026-07-23
tags: [skills-catalog, skills-registry, architecture]
features: [skills-catalog, skills-registry]
review_after: 2026-10-23
source: Skills Registry/Catalog meeting 2026-07-23 + Ramesh catalog-vs-registry GDoc
---

## Context

Prior direction was that all skills would live in the registry with a
"view" on top. As the catalog/registry pair pattern matured across MCP
and agent assets, the question was whether skills should follow the
same separation or remain registry-only.

## Decision

Catalog and registry are separate products:

- **Catalog** = marketplace/storefront (Kubeflow, read-only, cluster
  level, Git-backed, pre-populated by Red Hat)
- **Registry** = workspace/governance (MLflow, read-write, namespace
  level, lifecycle management, RBAC)

Catalog ships first. Registry integration follows: user pulls from
catalog into registry, which becomes a new version of the registered
skill. No automated sync -- user decision to pull.

## Consequences

- Catalog can ship independently of MLflow RFC timeline (higher
  confidence, ~90% for 3.6 per Bill Murdock)
- Registry depends on RFC-0008/0009 upstream merge + MLflow release
  cycle (lower confidence, ~60% for 3.6)
- Integration between catalog and registry (pull-to-register, version
  tracking) is a separate workstream post-both-shipping
- Installation features location (catalog vs registry vs both) is an
  open question needing its own STRAT
