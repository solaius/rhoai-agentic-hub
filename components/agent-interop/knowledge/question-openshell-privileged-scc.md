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

Three concrete mitigation paths identified (deployment lens, 2026-07-27):

1. **Topology B (sidecar)**: proxy sidecar in root network namespace
   does NOT need elevated privileges; agent runs in its own namespace
   with Landlock/seccomp. Helm chart now ships
   `supervisor.topology=sidecar` with strict/relaxed sub-modes.
2. **User namespaces** (K8s 1.33+): `server.enableUserNamespaces=true`
   maps container UID 0 to unprivileged host UID, making CAP_SYS_ADMIN
   namespaced to container-local resources. OpenShift support WIP.
3. **Layered sandboxing**: OpenShell inside Kata micro-VM (Topology B
   with RuntimeClass). Validated on OpenShift 4.21 (Red Hat Developer
   article Jul 2026) -- stops both app-layer and kernel-level attacks.

OpenShell #899 tracks restricted SCC support specifically.

Related: sandbox user elimination tracked in OpenShell issue #1959.
