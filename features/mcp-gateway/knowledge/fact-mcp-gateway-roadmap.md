---
type: fact
title: MCP Gateway feature roadmap (DP -> TP -> GA)
description: Phased MCP Gateway rollout — what ships at Developer Preview, Technical Preview, and GA, including MCP Registry Integration landing at GA.
timestamp: 2026-07-06
tags: [mcp-gateway, roadmap, rhcl]
review_after: 2026-08-05
source: ai-asset-registry/docs/knowledge-registry.md §3 (as of 2026-07-05)
---
Per the RHCL product deck ([ref-rhcl-product-deck.md](/features/mcp-gateway/knowledge/ref-rhcl-product-deck.md)):

- **Developer Preview** (Feb 2026): OAuth-based auth, fine-grained authz, virtual MCP servers (focused tool collections).
- **Technical Preview** (Apr 2026): isolated gateway deployments (multiple MCP Gateways), Vault integration, MCP elicitation support, content guardrails at the gateway, hosts for virtual MCP servers, router OTEL tracing.
- **General Availability** (Q4 2026): MCP Gateway Operator, security plug-in (DDoS/bot mgmt), resumable session management, HA (health checks/failover), **MCP Registry Integration**, extended capabilities (prompts, resources, sampling).

MCP Gateway 0.6.0 shipped as TP in RHCL 1.3.3 on April 30, 2026.
