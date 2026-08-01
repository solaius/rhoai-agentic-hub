---
type: reference
title: MaaS Responses/Messages API Conformance and Tool-Calling Validation
description: Feature to audit and validate MaaS as a conformant proxy for Responses and Messages API surfaces used by agentic clients (Claude Code, Codex) for 3.5/6.
resource: https://redhat.atlassian.net/browse/RHAISTRAT-1812
tags: [ai-gateway, conformance, maas, testing]
timestamp: 2026-07-31
review_after: 2026-10-31
source: hub.jira-sweep 2026-07-31
---

Addresses the risk that MaaS proxy layers (3scale, litellm, product
gateway) silently modify Messages/Responses API traffic, breaking
agentic workflows. Identifies failure modes: missing API coverage,
parameter filtering, response mangling, streaming corruption, payload
modification. Linked from RHAISTRAT-1357. Clones RHAIRFE-2258.
