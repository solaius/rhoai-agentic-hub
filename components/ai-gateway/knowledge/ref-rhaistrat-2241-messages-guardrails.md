---
type: reference
title: Anthropic Messages API endpoint for NeMo Guardrails server
description: Feature to add native /v1/messages endpoint to NeMo Guardrails -- applies full guardrail pipeline to Anthropic Messages API traffic with streaming support; In Progress, fix_version 3.6 EA1.
resource: https://redhat.atlassian.net/browse/RHAISTRAT-2241
tags: [ai-gateway, guardrails, messages-api, nemo, anthropic]
timestamp: 2026-07-31
review_after: 2026-10-31
source: hub.jira-sweep 2026-07-31
---

Adds /v1/messages endpoint to NeMo Guardrails FastAPI server for
Anthropic Messages API format. Includes bidirectional translation
layer (content block arrays vs string content, system prompt handling,
tool use differences). Full rail pipeline: input, output, retrieval,
tool call, and tool response rails. Clones RHAIRFE-2657. Fix_version:
3.6 EA1.
