---
type: question
title: Harness binary release cadence — no AIPCC conversation yet
description: Engineering concerned that frequent upstream harness releases outpace validated image builds; no AIPCC discussion on cadence yet (RHAIRFE-2443 scope). Adel proposes set cadence + communicate which versions are validated.
timestamp: 2026-07-12
status: open
tags: [agent-interop, harness, release-cadence, aipcc]
features: [agent-interop, agent-catalog]
source: Slack group DM Jehlum/Adel/Peter ~2026-07-12
asks:
  - Jehlum 2026-07-12 — engineering raising two concerns, (1) support scope, (2) release frequency vs adoption
---

**Question**: What is the release cadence for validated harness images,
and has this been discussed with AIPCC?

**Context**: Engineering raised two concerns (Jehlum, ~2026-07-12):
1. Support scope for the harness images (see
   [fact-harness-support-boundary](/features/agent-interop/knowledge/fact-harness-support-boundary.md)).
2. Harness binaries are released extremely frequently upstream. Even if
   AIPCC builds an image, it may be out of date by release time and
   therefore not adopted.

**Adel's position**: we do not have to support every version. Set a
cadence and communicate which versions we validate — better than no
validation at all. The conversation can happen in the scope of
RHAIRFE-2443.

**Jehlum**: offered to ask Doug or Emilien at AIPCC directly.

**Status**: no AIPCC conversation on cadence yet as of 2026-07-12.
