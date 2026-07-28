---
type: question
title: OpenShell gateway has no HA / leader election
description: The gateway is a single point of failure -- no documented HA pattern, no leader election, no HPA guidance. GitHub #1012 open. Multi-replica with external Postgres works but without HA guarantees.
status: open
timestamp: 2026-07-27
tags: [agent-interop, openshell, operations, availability]
source: operations lens (08-operations.md); OpenShell GitHub #1012
---

The OpenShell gateway has no documented high-availability pattern.
GitHub issue #1012 ("High-availability Kubernetes Support") is open
with no resolution.

Gaps:
- No leader election for multi-replica deployments
- No documented active-active or active-passive HA
- No HPA configuration guidance or resource recommendations
- Multi-replica Deployment mode with external Postgres works but no
  documented guarantees on concurrent write safety

For DP/TP, single-replica with Postgres is likely sufficient. GA will
need an HA story -- this requires upstream engagement or downstream
engineering.
