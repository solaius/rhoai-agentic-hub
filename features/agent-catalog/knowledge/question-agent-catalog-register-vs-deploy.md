---
type: question
title: Must deployments register — and does Deploy become Register?
description: Platform stance on catalog-registry-deployments flow unresolved (ODH ADR #142); whether the catalog's deploy button becomes "register" is to be decided against the 3.5 GA timeframe.
status: open
timestamp: 2026-07-16
tags: [agent-catalog, registry, platform-model]
features: [agent-registry]
---

The catalog/registry/deployments platform model is contested
(#forum-ai-asset-management, June–July 2026): must every deployment be
registered? Andrew Ballantyne pushes back on forcing flows through the
registry (GitOps / `oc apply` can't be policed); Gage Krumbach's
definitions — catalog = curated marketplace, registry = RBAC-backed
versioned inventory; a sync-operator ADR seed exists
(opendatahub-io/architecture-decision-records #142). Ramesh Reddy / Daniel
Warner floated replacing the catalog's Deploy button with "Register"
(2026-06-30) — undecided. Related: Gage, "not sure where registry actually
fits anymore tbh."

**Research direction (2026-07-16, verified):** the evidence supports
**"Deploy always registers, reconcile the rest"** — EU AI Act transparency
(applies 2026-08-02), NIST AI RMF GV-1.6, and CSA's agentic profile expect
per-agent accountability records, but inventory elsewhere works by
discovery/reconciliation, not a mandatory front door (matching the ADR #142
direction); no surveyed vendor exposes "Register" as an end-user catalog
verb — registration is a deploy side-effect
([requirements](/features/agent-catalog/research/04-requirements.md) §5,
[landscape](/features/agent-catalog/research/01-landscape.md) §4).
Sub-question this raises: does the 3.6 deploy flow capture owner metadata
(business + technical owner) at deploy time to seed the registry's
accountability record?
