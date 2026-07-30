---
type: question
title: Should EMA (Enterprise Managed Authorization) be added to the Gateway roadmap?
description: EMA is now a stable MCP extension for centralized IdP-managed MCP access (ID-JAG tokens, RFC 8693). Not on any RHOAI roadmap. AWS AgentCore and ToolHive Enterprise already support centralized IdP. Decision D5 by Oct 2026.
status: open
timestamp: 2026-07-29
tags: [mcp-gateway, auth, ema, enterprise, competitive]
features: [mcp-ecosystem, mcp-registry]
source: hub.research mcp-ecosystem requirements 2026-07-29
---

Enterprise Managed Authorization (EMA) is a stable MCP extension
(formalized in the 2026-07-28 spec). It replaces per-user per-server
OAuth consent with centralized IdP-managed access using ID-JAG
(Identity Assertion JWT Authorization Grant) tokens via RFC 8693
token exchange.

Adopters: Okta (branded Cross App Access / XAA), Claude, VS Code,
Asana, Atlassian, Figma.

**Gap:** EMA is not on the Gateway or Registry roadmap. The Gateway
would need to:
1. Accept ID-JAG tokens from enterprise IdPs
2. Exchange them for MCP access tokens
3. Enforce IdP-level access policies

This is a significant feature, not a configuration change. Target
customers (enterprises with existing IdP infrastructure) will expect it.
Competitive gap: AWS AgentCore and ToolHive Enterprise already support
centralized IdP integration.

Decision D5 from research series. Target: Oct 2026 (before 3.7
planning).
