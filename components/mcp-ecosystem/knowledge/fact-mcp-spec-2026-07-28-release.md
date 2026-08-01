---
type: fact
title: MCP 2026-07-28 specification released -- protocol goes stateless
description: The MCP 2026-07-28 spec is final (published July 28, 2026). Transforms MCP from a bidirectional stateful protocol into a stateless request/response protocol. Biggest release since remote MCP launched.
timestamp: 2026-07-28
tags: [mcp-spec, protocol, stateless, release]
components: [mcp-gateway, mcp-lifecycle-operator, mcp-registry, mcp-catalog]
review_after: 2026-10-28
source: https://blog.modelcontextprotocol.io/posts/2026-07-28/
---

MCP 2026-07-28 replaces the previous 2025-11-25 revision. The protocol
moves from bidirectional stateful to stateless request/response.

## Headline changes

1. **No handshake or sessions** -- initialize/initialized exchange and
   Mcp-Session-Id header retired. Every request carries protocol
   version, client identity, and capabilities in `_meta`. New optional
   `server/discover` RPC for capability probing. (SEP-2575, SEP-2567)

2. **Multi Round-Trip Requests (MRTR)** -- replaces server-initiated
   sampling/elicitation/roots. Server returns `resultType:
   "input_required"` with requests; client retries with
   `inputResponses`. (SEP-2322)

3. **Header-based routing** -- Streamable HTTP requests must include
   `Mcp-Method` and `Mcp-Name` headers, enabling gateway/WAF routing
   without body parsing. Custom headers from tool parameters via
   `x-mcp-header`. (SEP-2243)

4. **Cacheable list results** -- tools/list, prompts/list,
   resources/list, resources/read carry `ttlMs` and `cacheScope`
   (`public`/`private`). (SEP-2549)

5. **Authorization hardening** -- issuer validation per RFC 9207,
   application_type in DCR, credentials bound to issuing server. DCR
   deprecated in favor of Client ID Metadata Documents (CIMD).

6. **Tasks as extension** -- moved from experimental core to
   `io.modelcontextprotocol/tasks` extension. Poll-based `tasks/get`,
   new `tasks/update`, `subscriptions/listen` replaces HTTP GET
   endpoint. (SEP-2663)

7. **Deprecations with policy** -- Roots, Sampling, Logging enter
   12-month deprecation window. HTTP+SSE transport formally deprecated.
   `includeContext` values deprecated. Formal feature lifecycle policy
   adopted. (SEP-2577, SEP-2596)

## Other notable changes

- `subscriptions/listen` replaces resources/subscribe as a single
  long-lived stream with per-type opt-in
- `ping`, `logging/setLevel`, `notifications/roots/list_changed` removed
- Per-request log level via `io.modelcontextprotocol/logLevel` in `_meta`
- All results carry required `resultType` field (`complete` or
  `input_required`)
- SSE stream resumability (Last-Event-ID) removed
- OpenTelemetry trace context propagation documented (SEP-414)
- Error code allocation policy: -32020 to -32099 reserved for MCP spec
- `inputSchema`/`outputSchema` loosened to full JSON Schema 2020-12
- SEP workflow formalized (PR-based, seps/ directory)

## Extensions framework

Formally established. Named extensions:
- Tasks (`io.modelcontextprotocol/tasks`)
- MCP Apps
- Enterprise Managed Authorization (EMA)
- Skills over MCP (working group)

## SDK adoption

Tier 1 SDKs (all support 2026-07-28): TypeScript, Python, Go, C#,
Rust (beta). Nearly 500M SDK downloads/month; TS and Python each past
1B total downloads.

## Ecosystem signals

AWS (contributed Tasks), Cloudflare, Google Cloud, Microsoft, Figma,
Honeycomb, Supabase, Xero publicly endorsing. Honeycomb reports ~20%
of interactive queries now from agents. FastMCP 4.0 supports the spec.
