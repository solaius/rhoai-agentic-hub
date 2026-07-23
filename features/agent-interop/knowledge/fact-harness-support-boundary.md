---
type: fact
title: Harness support boundary — validated, not supported
description: Harness binaries (Open Code, Codex, etc.) are not RH-supported software; the platform layers around them (sandbox, MCP APIs, bootstrapping, deploy UX) are. Adel uses "validated" to describe the harness image posture.
timestamp: 2026-07-12
tags: [agent-interop, harness, support-boundary]
features: [agent-interop, agent-catalog]
source: Slack group DM Jehlum/Adel/Peter ~2026-07-12
review_after: 2026-10-12
---

Harness binaries (Open Code, Codex, Claude Code, etc.) are **not**
Red Hat-supported software. The platform layers around them — sandbox
runtime, MCP APIs, credential injection, bootstrapping, deploy UX —
**are** the supported surface.

Adel's preferred terminology: "validated" rather than "supported" for
the harness images AIPCC builds (RHAIRFE-2443). The 4 initial harness
images need ongoing maintenance to remain useful; unmaintained images
defeat the purpose. Default posture: do not commit to full support
unless significant customer demand materialises.

Jehlum's framing: admin installs either the sandbox + binary
(connected) or the baked image (disconnected). End user picks a
catalog card and goes. The support boundary sits between what Red Hat
builds/validates and what the upstream harness project ships.
