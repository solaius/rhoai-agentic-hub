---
type: fact
title: OpenShell product timeline (RHOAI integration)
description: Tentative milestones for OpenShell in RHOAI — DP in 3.5 (Jul-Aug 2026), TP in 3.6 EA (Nov 2026), GA in 3.7 (early 2027). Subject to change.
timestamp: 2026-07-11
tags: [agent-interop, openshell, timeline, roadmap]
review_after: 2026-08-15
source: GDoc "Kagenti to OpenShell Executive Summary" + convergence email 2026-07-02
---

| Milestone | Target | What ships |
|-----------|--------|------------|
| RHOAI 3.5 | Jul-Aug 2026 | OpenShell **Dev Preview**. Documentation + enablement. Konflux pipeline setup for images. |
| RHOAI 3.6 EA1/EA2 | Nov 2026 | OpenShell **Tech Preview**. Operator for lifecycle. SPIFFE identity integration. Team-based policy. Observability integration. Single and multi-player support. |
| RHOAI 3.6 GA / 3.7 EAs | 2027 | **GA**. Full identity, policy, discovery. Declarative agent onboarding. Service binding for LLM endpoints and MCP gateway. |

Disclaimer: subject to change per Adel's announcement.

Dependencies: Agent Sandbox TP readiness (KATA-4728) is a prerequisite
for OpenShell productization. The kubernetes-sigs/agent-sandbox went
v1beta1 but API is still changing fast.
