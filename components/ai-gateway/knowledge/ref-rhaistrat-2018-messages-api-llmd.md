---
type: reference
title: Messages API Support on llm-d
description: Feature to add native Anthropic Messages API endpoint to llm-d alongside chat completions -- enabling Anthropic-ecosystem agent frameworks without translation overhead; In Progress, fix_version 3.6 EA2.
resource: https://redhat.atlassian.net/browse/RHAISTRAT-2018
tags: [ai-gateway, messages-api, llm-d, anthropic]
timestamp: 2026-07-31
review_after: 2026-10-31
source: hub.jira-sweep 2026-07-31
---

Adds native Messages API serving to llm-d so Claude Code, Anthropic
Agent SDK, and LangChain Anthropic provider can target llm-d directly.
Platform capabilities (routing, metering, observability) extend to
Messages API traffic at the same fidelity as chat completions.
Fix_version: 3.6 EA2.
