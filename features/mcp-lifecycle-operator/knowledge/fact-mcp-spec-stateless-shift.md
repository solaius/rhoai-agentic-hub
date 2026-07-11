---
type: fact
title: MCP 2026-07-28 spec goes stateless -- architectural shift for MCPLO
description: The MCP spec removes session state (no initialize handshake, no session header, self-contained requests), adds routing headers for gateways, caching, and distributed tracing. Simplifies MCPLO horizontal scaling.
timestamp: 2026-07-11
tags: [mcp-lifecycle-operator, mcp-spec, stateless, architecture]
features: [mcp-gateway, mcp-ecosystem, mcp-catalog]
review_after: 2026-08-15
source: landscape research 2026-07-11; MCP 2026-07-28 RC blog
---

The MCP 2026-07-28 Release Candidate (locked May 21, 2026, publishing
July 28) makes MCP stateless at the protocol layer:

- initialize/initialized handshake removed
- Session header removed
- Every request is self-contained (version, client info, capabilities
  in `_meta`)
- New `server/discover` method for on-demand capability fetch
- Required `Mcp-Method` and `Mcp-Name` routing headers on Streamable
  HTTP (SEP-2243)
- Caching support with `ttlMs` and `cacheScope` (SEP-2549)
- W3C Trace Context propagation in `_meta` (SEP-414)
- Extensions framework with independent versioning
- Roots, Sampling, and Logging enter 12-month deprecation

**Implications for MCPLO:**
- No session stickiness needed -- MCP servers become standard HTTP
  microservices, exactly what K8s operators are built to manage
- MCPServer spec.mcp.stateless field may need revisiting (the
  protocol itself is now stateless)
- Routing headers enable gateway-level policy without body parsing
- Caching and tracing standards provide hooks for operator-managed
  observability
- Standard RollingUpdate works without sticky session concerns

Source: [MCP 2026-07-28 RC](https://blog.modelcontextprotocol.io/posts/2026-07-28-release-candidate/)
