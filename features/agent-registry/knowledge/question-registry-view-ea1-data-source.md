---
type: question
title: What feeds the EA1 registry view before the EA2 backend exists?
description: Registry TP (3.6 EA1) lands before its own backend (EA2) — a Sandbox-CR-fed stopgap would make the registry view a second deployments view and collapse the RHAISTRAT-1697/1758 distinction on arrival. Product decision needed before the EA1 build.
status: open
timestamp: 2026-07-16
tags: [agent-registry, sequencing, dashboard]
---
Options sketched in
[research/09-architecture](/features/agent-registry/research/09-architecture.md)
(governance-record stub backed by catalog metadata; delayed registry
view; honest merged view with explicit linkage states). The
registry-view/deployments-view split is the product's own two-entity
commitment — the EA1 stopgap must not erase it.
