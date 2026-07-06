---
type: fact
title: MCP Gateway (Kuadrant/mcp-gateway)
description: Envoy-based WASM plug-in providing runtime connectivity and tool governance for MCP traffic — not a standalone gateway, not a guardrails replacement.
timestamp: 2026-07-06
tags: [mcp-gateway, rhcl, envoy, wasm]
review_after: 2026-08-05
source: ai-asset-registry/docs/knowledge-registry.md §3 (as of 2026-07-05); optionality clarification from ai-asset-registry/docs/knowledge-review/flows/mcp-implementation-end-to-end.md (as of 2026-07-05)
---
Runtime connectivity/enforcement layer for MCP traffic, implemented as a WASM plug-in for Envoy Proxy (NOT a standalone gateway) — OpenShift Service Mesh/Istio/Envoy-ingress users need no major changes to adopt it. Uses ext_proc, Gateway API, Istio. Provides virtual MCP servers, identity-aware filtering, per-tool auth/metrics/audit, and streaming HTTP. Two CRDs: `MCPServer`, `MCPGatewayExtension`. Ships with OCP for platform use; RHOAI is required for customer-facing MCP servers.

Sits inside the broader RHCL stack: Ingress Gateway (Envoy/Gateway API) → Limitador (rate limiting) + Authorino (auth config); MCP Gateway subsystem = MCP Router (ext_proc, parses MCP protocol, sets routing headers) → MCP Broker (default `/mcp` backend, holds configured MCP Servers) + Cache, with an MCP Controller watching for `MCPServer` resources. RHCL adds Kuadrant Operator (orchestration), Cert Manager, DNS Operator, and TLS/Auth/DNS/Rate-Limit policy APIs around this.

**Not required for basic use**: MCP Gateway is NOT required for basic Gen AI Studio Playground usage (confirmed by Peter Double and Jaideep Rao in a Slack troubleshooting thread) — without it, each MCP server is registered directly in the `gen-ai-aa-mcp-servers` ConfigMap; with it, the Gateway URL goes in that ConfigMap instead, adding auth, routing, and per-tool metrics on top. The Gateway becomes necessary once you need identity-based tool access control, per-tool metrics, or virtual MCP server aggregation.

See [decision-mcp-gateway-tool-governance-scope.md](/features/mcp-gateway/knowledge/decision-mcp-gateway-tool-governance-scope.md) for scope boundaries and [fact-mcp-gateway-roadmap.md](/features/mcp-gateway/knowledge/fact-mcp-gateway-roadmap.md) for phased rollout.
