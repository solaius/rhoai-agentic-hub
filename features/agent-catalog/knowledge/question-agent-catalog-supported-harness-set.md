---
type: question
title: Which harnesses ship as supported images in 3.6?
description: Candidate set open (OpenCode/Hermes favored; Claude Code/Antigravity need licensing; OpenCode self-update vs disconnected); no committed list or rotation policy yet.
status: open
timestamp: 2026-07-16
tags: [agent-catalog, 3.6, harnesses]
---

From the 2026-07-10 supported-images meeting: candidates are OpenCode,
Hermes, Codex, Pi, OpenClaw, Goose, Claude Code (likely needs an Anthropic
agreement), Antigravity (likely Google) —
[Jehlum's doc](/features/agent-catalog/knowledge/ref-harness-candidates-gdoc.md).
Peter's floor proposal: OpenCode + something like Hermes, with a
validated-models-style rotation. Unresolved: the committed list; whether
vendor-specific harnesses (Claude Code, Codex) are viable given forced
updates/lock-in; whether OpenCode's self-updating needs a patch/fork for
disconnected; one image per harness or vanilla + RHOAI-preconfigured
flavors; and whether a mostly field/demo-value feature justifies the
maintenance (Bill Murdock / Daniele Zonca). If no harness can be supported,
"do we still have a catalog?" (Bill).

**Research findings (2026-07-16, verified — narrows the question):**
licensing is now fact, not risk — Claude Code's license prohibits
modification/redistribution (Anthropic agreement required), while **Codex
CLI is Apache-2.0** (not proprietary as assumed in the meetings) and Goose
is Apache-2.0 under the Linux Foundation. Four of five open candidates
self-update in some form (OpenClaw channels, Hermes runtime skill
self-creation, pi `update --self`, OpenCode installer — upstream air-gap
issues #16117/#20027 open), conflicting with image-pinned governance. See
[fact-supported-images-enterprise-requirements](/features/agent-catalog/knowledge/fact-supported-images-enterprise-requirements.md)
and the [upstream research](/features/agent-catalog/research/02-upstream.md).
