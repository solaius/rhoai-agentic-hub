---
type: fact
title: Multi Round-Trip Requests (MRTR) replaces server-initiated requests in MCP
description: MRTR (SEP-2322) eliminates server-to-client requests (sampling, elicitation, roots). Servers return resultType "input_required" with inputRequests; clients retry the original call with inputResponses. Stateless-compatible.
timestamp: 2026-07-28
tags: [mcp-spec, mrtr, protocol, stateless]
features: [mcp-gateway, mcp-lifecycle-operator, mcp-registry, mcp-catalog]
review_after: 2026-10-28
source: https://modelcontextprotocol.io/specification/2026-07-28/changelog
---

MRTR is the mechanism that makes MCP stateless while preserving
interactive tool flows. Before 2026-07-28, three server-initiated
request types required held-open bidirectional streams:

- `sampling/createMessage` (model inference)
- `elicitation/create` (user input)
- `roots/list` (workspace discovery)

All three are replaced by a single pattern: when a tool needs more
information mid-call, the server returns `resultType: "input_required"`
with an `inputRequests` field describing what it needs. The client
gathers the answers and retries the *same* original request with
`inputResponses` containing the answers.

**Why this matters for gateways/operators:** no long-lived connections
required between retry cycles. Each retry is an independent HTTP
request, compatible with round-robin load balancing and standard K8s
service routing. Servers that need to correlate retries encode their
own identifier in `requestState`.

SEP: https://github.com/modelcontextprotocol/modelcontextprotocol/pull/2322
