---
type: question
title: OpenShell elevated privilege requirements
description: OpenShell requires CAP_SYS_ADMIN and NetTrace to bootstrap sandboxes; flagged as red flag by enterprise customers. Working to eliminate when running inside VM boundary.
status: open
timestamp: 2026-07-11
tags: [agent-interop, openshell, security, scc]
source: OpenShell Weekly Update Jun 15-19; OpenShell issue #1959; GDoc "OpenShell on OpenShift" footnote (Christian Zaccaria)
---

OpenShell requires elevated privileges (CAP_SYS_ADMIN, NetTrace) to
bootstrap network namespaces and Landlock restrictions. Enterprise
customers have flagged this as a deployment blocker.

Mitigation path: eliminate SCC requirement when running inside VM boundary
(Kata/gVisor topology). The crate decomposition (Topology B) enables
running the proxy outside gVisor without elevated privileges. Potentially
resolved within two months (per Jun 2026 assessment).

Christian Zaccaria (Jul 2026 GDoc) confirmed this is a "meaningful
security exposure" -- the OpenShift install path should be treated as
experimental and not used in production. The sandbox needs elevated
permissions to set up its own isolated network and security controls.
For GA, plan is to replace with a custom, narrowly-scoped permission
set before removing the experimental label.

Related: sandbox user elimination tracked in OpenShell issue #1959.
