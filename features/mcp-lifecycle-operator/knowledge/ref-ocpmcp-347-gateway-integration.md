---
type: reference
title: "OCPMCP-347: MCP Gateway integration (GA scope)"
description: Gateway integration for MCPLO -- deferred from TP to GA scope. Formal proposal doc by aliok (May 2026). HTTPRoute-based server registration with MCP Gateway.
resource: https://redhat.atlassian.net/browse/OCPMCP-347
tags: [mcp-lifecycle-operator, mcp-gateway, jira, gateway-integration]
timestamp: 2026-07-11
features: [mcp-gateway]
source: Slack channel review 2026-07-11
---

Gateway integration is explicitly GA scope, not TP. aliok wrote a
formal proposal doc (May 2026) for how MCPLO-deployed servers
integrate with the MCP Gateway via HTTPRoute-based registration.

Related upstream work: PR #219 (POC for HTTPRoute gateway integration,
WIP/XXL). The integration would automatically register deployed
MCPServer instances with the gateway for external routing, auth,
and observability.
