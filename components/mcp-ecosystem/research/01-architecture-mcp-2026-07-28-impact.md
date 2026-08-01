---
title: "Architecture: MCP 2026-07-28 spec impact on the RHOAI MCP stack"
description: Architectural impact analysis of MCP 2026-07-28 stateless protocol on Gateway ext_proc, MCPLO CRD/scaling, header routing, tasks extension, and subscriptions/listen.
timestamp: 2026-07-29
lens: architecture
review_after: 2026-10-29
---

## Summary

The MCP 2026-07-28 specification transforms MCP from a bidirectional
stateful protocol into a stateless request/response protocol. This
document analyzes the architectural impact on the four components of the
RHOAI MCP stack: the MCP Gateway (Kuadrant/mcp-gateway), the MCP
Lifecycle Operator (kubernetes-sigs), the MCP Registry, and the MCP
Catalog.

The net assessment: **the stateless shift is broadly favorable** to the
RHOAI stack. It simplifies horizontal scaling across the board,
eliminates session-management infrastructure the gateway was building
toward, and makes MCP servers behave like the stateless HTTP
microservices that Kubernetes operators are designed to manage. However,
it also invalidates several GA-roadmap line items, introduces new design
work around MRTR forwarding and cacheable intermediary semantics, and
compresses the timeline for a spec-version compatibility policy that
affects every tier of the catalog.

Sources: [MCP 2026-07-28 blog](https://blog.modelcontextprotocol.io/posts/2026-07-28/),
[changelog](https://modelcontextprotocol.io/specification/2026-07-28/changelog),
[AWS AgentCore Gateway blog](https://aws.amazon.com/blogs/machine-learning/how-agentcore-gateway-supports-the-mcp-2026-07-28-spec/),
[Kuadrant mcp-gateway issue #809](https://github.com/Kuadrant/mcp-gateway/issues/809),
[Solo.io engineering details](https://www.solo.io/blog/mcp-stateless-spec-changes-the-engineering-details),
[Envoy MCP filter docs](https://www.envoyproxy.io/docs/envoy/latest/configuration/http/http_filters/mcp_filter).


## 1. MRTR vs. Gateway ext_proc

### What changes

Multi Round-Trip Requests (SEP-2322) replace server-initiated sampling,
elicitation, and roots requests. When a tool needs additional
information mid-call, the server returns `resultType: "input_required"`
with `inputRequests` and an opaque `requestState`. The client gathers
answers and retries the *same* `tools/call` with `inputResponses` and
the echoed `requestState`. Each retry is an independent HTTP request.

This replaces the elicitation support the gateway shipped at TP
(RHCL 1.3.3 / mcp-gateway 0.6.0) and the sampling support planned for
GA. The old mechanisms required the gateway to hold open a bidirectional
SSE stream and proxy server-initiated requests back to the client. MRTR
eliminates that entire flow.

### Is each request independently routable?

**Yes.** Each MRTR retry is a standalone HTTP POST carrying
`Mcp-Method: tools/call` and `Mcp-Name: <tool-name>` headers. The
gateway does not need to understand MRTR semantics for routing -- it
routes on headers exactly as it would any other `tools/call`. The
`requestState` is opaque to intermediaries.

### Virtual server aggregation with MRTR

The gateway should be transparent. The `Mcp-Name` header identifies the
tool, which the gateway already uses to route to the correct backing
server. The client retries with the same tool name, same headers, and
the retry routes to the same backing server. No MRTR-specific logic
needed beyond existing `tools/call` routing.

**Caveat:** If the gateway performs tool-prefix stripping for virtual
server aggregation (rewriting `servername__toolname` to `toolname`),
the `Mcp-Name` header on the retry must also be stripped/rewritten.
This is already required for any `tools/call` routing.

### What breaks or becomes unnecessary

| Gateway capability | Impact |
|---|---|
| Elicitation handling (ext_proc item 7 in issue #809) | **Obsolete.** MRTR replaces server-initiated elicitation. |
| Backend session initialization (ext_proc item 6) | **Obsolete.** No sessions to initialize. |
| Session management (ext_proc item 5) | **Obsolete.** JWT-based gateway sessions mapped to per-backend MCP sessions no longer needed. |
| GA roadmap: "resumable session management" | **Remove.** The protocol no longer has sessions. |
| GA roadmap: "extended capabilities (sampling)" | **Replace with MRTR forwarding.** Transparent pass-through, no gateway-specific sampling implementation needed. |

### Design work needed

1. **Verify MRTR transparency in the broker.** The MCP Broker holds
   configured MCP Servers and may need to pass through `input_required`
   responses without interpreting them.
2. **Header rewriting on MRTR retries.** Ensure `Mcp-Name` header
   rewriting logic applies consistently to MRTR retry requests.


## 2. Stateless protocol vs. MCPLO CRD and scaling

### What simplifies

The stateless shift makes MCP servers standard HTTP microservices:

- **Horizontal scaling.** Standard Kubernetes HPA works without affinity
  rules. No sticky sessions, no shared session stores. Standard
  `RollingUpdate` works without session pinning concerns.
- **Service routing.** The MCPLO's ClusterIP Service now supports
  round-robin load balancing natively. No need for
  `sessionAffinity: ClientIP`.
- **Pod lifecycle.** Rolling updates, scale-down, and node drains no
  longer risk breaking active sessions.

### CRD field impact

| Field/behavior | Current | Recommended |
|---|---|---|
| Readiness check | Performs `initialize` handshake | Switch to `server/discover` with `initialize` fallback |
| Stateful toggle | N/A in v1alpha1 | Do not add. Protocol is stateless by default. |
| Protocol version | Not present | Consider `spec.mcp.protocolVersion` for catalog/gateway interop |
| Transport field | Not present | Consider `spec.mcp.transport` given HTTP+SSE deprecation |

### Health checks: server/discover replaces initialize

The MCPLO health check should be updated:

1. **Primary probe:** Send `server/discover` JSON-RPC POST to `/mcp`.
   A valid response confirms the server is serving MCP.
2. **Backward compatibility:** If `server/discover` returns method-not-
   found, fall back to `initialize` for older servers.
3. **Version reporting:** Surface discovered protocol version(s) in
   MCPServer status. This feeds the catalog's spec-version metadata.

The discovery URL pattern
(`http://<name>.<namespace>.svc.cluster.local:<port>/mcp`) remains valid.

### ToolHive comparison

ToolHive deploys a proxy pod per MCPServer. MCPLO creates standard
Deployments with security-hardened defaults (non-root, read-only rootfs,
dropped capabilities). The stateless shift makes MCPLO's Deployment-
based approach strictly better -- no proxy needed for session management.


## 3. Header-based routing vs. gateway architecture

### How much body-parsing can be eliminated?

The ext_proc currently handles eight responsibilities (per issue #809):

| # | Responsibility | Headers replace body parsing? |
|---|---|---|
| 1 | Request body parsing (method/tool extraction) | **Partially.** Method/tool from headers. Params still need body for auth. |
| 2 | Header injection (x-mcp-method, x-mcp-toolname) | **Eliminated.** Client now sends `Mcp-Method` and `Mcp-Name` natively. |
| 3 | Body rewriting (tool prefix stripping) | **Still needed.** |
| 4 | Routing (setting :authority and :path) | **Mostly header-based.** Envoy native matching can handle simple cases. |
| 5 | Session management | **Eliminated.** |
| 6 | Backend session initialization | **Eliminated.** |
| 7 | Elicitation handling | **Eliminated.** |
| 8 | Tool annotations forwarding | **Still needed.** |

**Net: 4 of 8 eliminated, 1 partially, 3 remain.** The hot path
(routing) can move to header matching.

### Can Envoy handle routing without ext_proc?

For common cases, Envoy's native header matching can route without
ext_proc. However, ext_proc cannot be fully eliminated because tool
prefix stripping requires body modification and authorization may need
param inspection.

### The Envoy native MCP filter path

Issue #809 investigates replacing ext_proc with Envoy's native MCP
filter (available since v1.38). The 2026-07-28 spec makes this more
attractive -- session management code becomes dead weight in either
approach, routing moves to native headers, and the remaining
responsibilities shrink to body rewriting and annotation forwarding.

**Recommendation:** Accelerate issue #809 investigation. The spec
eliminates 4 of 8 ext_proc responsibilities, making native MCP filter +
minimal custom filter significantly more viable.

### Cacheable results at the gateway

`ttlMs` and `cacheScope` on list endpoints enable gateway-level caching.
Key design consideration: `cacheScope: "private"` means the response is
user-specific. The cache must key on user identity for private-scoped
responses. MRTR interim results (`resultType: "input_required"`) are
not cacheable.

### Competitive comparison: AWS AgentCore Gateway

AgentCore supports 2026-07-28 via a single `UpdateGateway` API call. It
routes on `Mcp-Method` headers, enforces header-body consistency (HTTP
400 / code -32020), and passes MRTR through transparently. Kuadrant
should target parity on header-body validation and MRTR transparency.


## 4. Tasks extension + subscriptions/listen

### Tasks as extension

Tasks moved to `io.modelcontextprotocol/tasks` (SEP-2663). Poll-based
`tasks/get` replaces blocking `tasks/result`. `tasks/list` removed.
Task handles survive connection drops.

### Catalog UX impact

The catalog metadata schema should include:
- **Extensions supported:** List of extension IDs from `server/discover`
- **Protocol version(s):** Spec revisions supported
- **Tool TTL:** `ttlMs` from `tools/list` for cache refresh cadence

### Operator observability

Task monitoring is an application-level concern, out of scope for MCPLO.
The operator should focus on `server/discover` health checks and leave
task monitoring to the gateway or dedicated observability.

### subscriptions/listen gateway implications

- **Long-lived POST streams.** The gateway must handle long-lived SSE
  responses on POST requests (different from old GET-based SSE).
- **Routing.** `Mcp-Method: subscriptions/listen` header enables
  routing. For virtual servers, consider multiplexing only if aggregated
  change notifications are needed.
- **Connection lifetime.** Reconnecting and re-issuing is safe, but
  the stream must stay connected to the same backend for its duration.

### GA roadmap item impact

| Item | Status post-2026-07-28 |
|---|---|
| Resumable session management | **Remove.** No sessions, no SSE resumability. |
| HA (health checks/failover) | **Simplifies.** `server/discover` health checks, standard K8s failover. |
| Extended capabilities (prompts, resources, sampling) | **Revise.** Prompts/resources stay. Sampling deprecated -- replace with MRTR transparency. |
| MCP Registry Integration | **Unchanged.** Orthogonal to protocol changes. |


## 5. Recommended actions

### Immediate (before RHOAI 3.6 EA1)

1. **MCPLO:** Switch health check to `server/discover` with `initialize`
   fallback. Surface discovered protocol version in MCPServer status.
2. **Gateway:** Remove "resumable session management" from GA roadmap.
   Replace with "transparent MRTR forwarding" and "dual spec-version
   support."
3. **Catalog:** Define spec-version compatibility policy.

### Near-term (Q4 2026 GA)

4. **Gateway:** Accelerate issue #809 (native Envoy MCP filter).
5. **Gateway:** Implement `cacheScope`-aware caching with identity
   keying for private responses.
6. **Gateway:** Add header-body consistency validation (HTTP 400 /
   code -32020, matching AgentCore).
7. **Gateway:** Support CIMD alongside DCR for 12-month transition.

### Tracking (post-GA)

8. **MCPLO:** Consider `spec.mcp.protocolVersion` and `spec.mcp.transport`
   CRD fields in a future API version.
9. **Gateway:** Handle `subscriptions/listen` forwarding for virtual
   server aggregation.
10. **All:** Track 12-month deprecation clock (July 2027) for HTTP+SSE,
    Sampling, Roots, Logging, DCR.
