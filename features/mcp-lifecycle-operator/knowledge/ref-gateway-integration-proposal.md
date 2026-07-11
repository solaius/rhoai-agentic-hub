---
type: reference
title: MCP Gateway integration proposal (aliok, May 2026)
description: Formal design document for MCPLO-Gateway integration -- HTTPRoute-based registration, SSA status updates, auth integration. Drives OCPMCP-347 (GA scope).
resource: https://docs.google.com/document/d/13A60i0eGJfUNRs4l75-RhFeQ9xYCyb3GQKtNuuuUl2Q
tags: [mcp-lifecycle-operator, mcp-gateway, gateway-integration, design]
timestamp: 2026-07-11
features: [mcp-gateway]
source: Slack #forum-mcp-lifecycle-operator, aliok, 2026-05-05 and 2026-05-15
---

Formal proposal document for how MCPLO-deployed MCPServer instances
integrate with the MCP Gateway. Covers HTTPRoute-based server
registration, Server-Side Apply (SSA) for status updates (chosen to
avoid status field conflicts), and auth integration patterns.

Written by aliok (May 2026), shared twice in the channel. This
design drives OCPMCP-347 (gateway integration, GA scope). Related
upstream POC: PR #219 (WIP/XXL).
