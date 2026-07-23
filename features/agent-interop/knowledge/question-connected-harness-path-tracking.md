---
type: question
title: Connected harness path — untracked, needs AIPCC + OpenShell confirmation
description: The connected deployment path (sandbox + runtime harness binary pull) has no Jira tracking and needs confirmation from AIPCC and the OpenShell team.
timestamp: 2026-07-12
status: open
tags: [agent-interop, harness, connected-path, openshell]
features: [agent-interop, agent-catalog]
source: Slack group DM Jehlum/Adel/Peter ~2026-07-12
asks:
  - Jehlum 2026-07-12 — flagged as uncaptured, needs tracking
---

**Question**: Is the connected harness deployment path (sandbox +
runtime binary pull) confirmed and tracked?

**Context**: Jehlum's 5-layer catalog experience model (see
[fact-catalog-deploy-stack](/features/agent-interop/knowledge/fact-catalog-deploy-stack.md))
describes two harness packaging paths:
- *Connected*: platform pulls the harness binary at runtime, layered
  on top of the OpenShell sandbox.
- *Disconnected*: AIPCC ships a baked image with harness included.

Jehlum flagged (~2026-07-12) that the connected path needs to be
confirmed and tracked with AIPCC + OpenShell team: "I haven't seen
this captured."

**Status**: untracked as of 2026-07-12. No Jira issue identified for
this path specifically.
