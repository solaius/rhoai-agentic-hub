---
type: fact
title: MCP 2026-07-28 auth hardening -- DCR deprecated, CIMD introduced, issuer binding
description: Authorization changes in MCP 2026-07-28 -- DCR (RFC 7591) deprecated for Client ID Metadata Documents (CIMD), issuer validation per RFC 9207, credentials bound to issuing authorization server, application_type required in DCR.
timestamp: 2026-07-28
tags: [mcp-spec, auth, security, protocol]
components: [mcp-gateway, mcp-registry]
review_after: 2026-10-28
source: https://modelcontextprotocol.io/specification/2026-07-28/changelog
---

Four authorization changes in the 2026-07-28 spec:

1. **Issuer validation (SEP-2468)** -- authorization servers SHOULD
   return the `iss` parameter per RFC 9207; clients MUST validate
   before redeeming an authorization code.

2. **application_type in DCR (SEP-837)** -- clients set
   `application_type` during Dynamic Client Registration so
   authorization servers stop rejecting localhost redirects for
   desktop/CLI apps.

3. **Credential binding (SEP-2352)** -- client credentials bound to
   the authorization server that issued them. Clients MUST key
   persisted credentials by issuer identifier, MUST NOT reuse across
   authorization servers, MUST re-register on server change.

4. **DCR deprecated for CIMD (PR #2858)** -- Dynamic Client
   Registration (RFC 7591) formally deprecated in favor of Client ID
   Metadata Documents. DCR remains for backward compatibility but will
   be removed in a future version under the 12-month deprecation
   policy.

**Impact on MCP Gateway/Registry:** gateway auth enforcement and
registry certification flows need to track which auth mechanism
(DCR vs CIMD) a server uses. The credential-binding requirement
means gateways cannot share client credentials across different
authorization server endpoints.
