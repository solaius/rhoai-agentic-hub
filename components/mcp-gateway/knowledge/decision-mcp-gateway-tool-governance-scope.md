---
type: decision
title: MCP Gateway scope is tool governance, not injection/jailbreak prevention
description: Clarifies the boundary between MCP Gateway and guardrails so the two stop getting conflated.
decided: 2026-07-06
timestamp: 2026-07-06
tags: [mcp-gateway, guardrails, scope]
source: ai-asset-registry/docs/knowledge-registry.md §3 (as of 2026-07-05)
---
**Context**: Ambiguity over whether MCP Gateway protects against prompt injection or jailbreaks, sharpened by Content Guardrails shipping at the gateway layer in TP.

**Decision**: MCP Gateway provides tool governance only — token-based access restriction, per-tool auth/metrics/audit. It does NOT stop prompt injection or jailbreaks; guardrails own that job, and can be integrated into the gateway or consumed standalone (Adel Zaalouk clarification, Agentic Messaging Guide review comments).

**Consequences**: Content Guardrails at the gateway (a TP feature) means guardrails-integrated-into-the-gateway, not a replacement for standalone guardrails deployments.

Note: source gives no exact clarification date (undated review comments); `decided` is set to the drafting date, not the actual clarification date.
