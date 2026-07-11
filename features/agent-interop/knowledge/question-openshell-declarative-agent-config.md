---
type: question
title: Declarative agent configuration path for OpenShell
description: OpenShell has no CRD or K8s-native declarative path today; community discussion on right abstraction (SDK, console, provider config, or layered CR).
status: open
timestamp: 2026-07-11
tags: [agent-interop, openshell, declarative, gitops]
source: GDoc "Strategic Assessment" section 3; Roland Huss comment
---

Kagenti had AgentRuntime CR (kubectl apply gives a fully wired agent pod).
OpenShell is SDK/CLI/TUI driven with no Kubernetes-native declarative path.

Community alignment: do not lead with Kubernetes-first (avoid binding agent
onboarding to just K8s). Solution should live at the sandbox layer or above
to preserve OpenShell's portable experience (local, OpenShift AI, CI).

The emerging direction is that agents are sandbox images (analogous to
containers): harness + config + skills + scripts form the atomic deployable
unit. The UX for onboarding agents securely into sandboxes, from console
and programmatically, needs refinement.

Roland Huss: before settling on a CR, investigate whether a separated
control-plane is more appropriate given OpenShell's cross-platform nature.
