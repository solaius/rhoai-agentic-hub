---
type: question
title: Multi-tenancy gap in OpenShell
description: Neither OpenShell nor Kagenti implemented multi-tenancy; high priority for both NVIDIA and Red Hat, active community discussion on tenant model.
status: open
timestamp: 2026-07-11
tags: [agent-interop, openshell, multi-tenancy]
source: GDoc "Strategic Assessment" section 3; OpenShell issue #1722
---

Multi-tenancy is a gap in both projects. OpenShell issue #1722 tracks
requirements gathering. High priority for NVIDIA and Red Hat. NVIDIA+SAP
meeting (as of Jun 2026) on multi-tenancy design.

Key open sub-questions: tenant model, isolation boundaries, namespace
strategy, shared gateway configuration per namespace/team.
