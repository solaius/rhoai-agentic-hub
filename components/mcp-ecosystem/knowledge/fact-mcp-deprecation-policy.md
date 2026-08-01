---
type: fact
title: MCP adopts formal feature lifecycle and deprecation policy
description: "MCP 2026-07-28 introduces a formal feature lifecycle (Active/Deprecated/Removed) with a minimum 12-month deprecation window and a deprecated features registry. First batch: Roots, Sampling, Logging, HTTP+SSE transport, includeContext values, DCR."
timestamp: 2026-07-28
tags: [mcp-spec, governance, deprecation, protocol]
components: [mcp-gateway, mcp-lifecycle-operator]
review_after: 2027-07-28
source: https://modelcontextprotocol.io/specification/2026-07-28/changelog
---

SEP-2596 establishes the policy:

- **States**: Active, Deprecated, Removed
- **Minimum deprecation window**: 12 months from the spec revision
  that marks a feature Deprecated
- **Registry**: a tracked list of all currently deprecated features
  at /specification/2026-07-28/deprecated

## Currently deprecated features (as of 2026-07-28)

| feature | SEP | earliest removal |
|---------|-----|-----------------|
| Roots | 2577 | 2027-07-28 |
| Sampling | 2577 | 2027-07-28 |
| Logging | 2577 | 2027-07-28 |
| HTTP+SSE transport | 2596 | 2027-07-28 |
| includeContext thisServer/allServers | 2596 | 2027-07-28 |
| Dynamic Client Registration (DCR) | PR 2858 | 2027-07-28 |

**Migration paths** (from spec):
- Roots: pass directories/files via tool parameters, resource URIs, or
  server configuration
- Sampling: integrate directly with LLM provider APIs
- Logging: log to stderr (stdio) or use OpenTelemetry
- HTTP+SSE: migrate to Streamable HTTP
- DCR: migrate to Client ID Metadata Documents (CIMD)

**Impact**: the MCP Gateway's roadmap includes elicitation support at
TP and sampling at GA -- Sampling's deprecation means the gateway
should target MRTR instead. MCPLO's transport assumptions should
account for the HTTP+SSE offramp timeline.
