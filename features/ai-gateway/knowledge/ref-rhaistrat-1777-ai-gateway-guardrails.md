---
type: reference
title: "[Outcome] AI Gateway Guardrails"
description: Outcome for reusing the BBR guardrail plugin from MCP Gateway on AI Gateway routes -- single guardrail implementation serving both surfaces; In Progress.
resource: https://redhat.atlassian.net/browse/RHAISTRAT-1777
tags: [ai-gateway, outcome, guardrails]
timestamp: 2026-07-31
review_after: 2026-10-31
source: hub.jira-sweep 2026-07-31
---

Delivers the same guardrail enforcement on AI Gateway (LLM
request/response) that MCP Gateway already has, by reusing the BBR
guardrail plugin. Success criteria: plugin deploys without code
changes, Guardrails Catalog presets apply with same semantics, unified
audit logs. Depends on RHAISTRAT-1775 (Self-Contained Guardrail
Servers) and RHAIRFE-299 (NeMo Guardrails). Related to RHAISTRAT-1776
(MCP Guardrails).
