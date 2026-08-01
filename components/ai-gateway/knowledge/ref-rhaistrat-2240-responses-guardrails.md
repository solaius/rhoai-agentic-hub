---
type: reference
title: OpenAI Responses API endpoint for NeMo Guardrails server
description: Feature to add /v1/responses endpoint to NeMo Guardrails server -- translates Responses API typed input items to Colang for rail evaluation; extends IPP guard plugins.
resource: https://redhat.atlassian.net/browse/RHAISTRAT-2240
tags: [ai-gateway, guardrails, responses-api, nemo]
timestamp: 2026-07-31
review_after: 2026-10-31
source: hub.jira-sweep 2026-07-31
---

Extends NeMo Guardrails to natively accept OpenAI Responses API
requests alongside the existing /v1/chat/completions endpoint.
Translation layer maps typed input items (message, function_call,
function_call_output) to Colang message format. Also extends IPP
NeMo guard plugins for Responses API format. Clones RHAIRFE-2656.
