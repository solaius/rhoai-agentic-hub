---
type: reference
title: "AI Gateway: Full API Fidelity for Tool-Calling Clients"
description: Feature requiring the AI Gateway to pass Messages API and Responses API traffic faithfully for Claude Code, Codex, and OpenCode -- conformant-proxy vs non-conformant-proxy decision; parent RHAISTRAT-1357.
resource: https://redhat.atlassian.net/browse/RHAISTRAT-1810
tags: [ai-gateway, tool-calling, conformance]
timestamp: 2026-07-31
review_after: 2026-10-31
source: hub.jira-sweep 2026-07-31
---

Validates that the AI Gateway preserves tool calls, tool_choice,
reasoning content, and SSE streaming for agentic clients end-to-end.
References the Inference Proxy Conformance Guidelines to determine
whether the gateway operates as a conformant proxy (zero-impact,
passthrough) or non-conformant proxy (takes on full eval burden).
Parent: RHAISTRAT-1357 (Make Red Hat Inference Server Best for
Agents). Clones RHAIRFE-2256.
