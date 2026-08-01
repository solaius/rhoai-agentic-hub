---
title: "Requirements: MCP 2026-07-28 spec impact on the RHOAI MCP stack"
description: Requirements impact analysis -- which RHOAI roadmap items build on deprecated MCP capabilities, auth hardening gaps, deprecation timeline vs release train, spec-version compatibility policy.
timestamp: 2026-07-29
lens: requirements
review_after: 2026-10-29
---

## Summary

The MCP 2026-07-28 specification directly affects four shipped or
in-progress roadmap items, forces an auth-stack decision before Gateway
GA (Q4 2026), and creates an open spec-version compatibility question
for Catalog GA (Nov 2026). Nothing is broken today -- the 12-month
deprecation window means deprecated features remain functional through
at least July 2027 -- but three items need roadmap-level decisions
before October 2026.


## 1. Roadmap items building on deprecated or removed capabilities

### 1.1 Gateway TP: "MCP elicitation support"

**Roadmap says:** Shipped at TP (RHCL 1.3.3, April 30, 2026).

**Spec now requires:** The old `elicitation/create` server-initiated
request is replaced by MRTR. `notifications/elicitation/complete` and
`elicitationId` are removed.

**Assessment: RENAME + PARTIAL REDESIGN.** The intent survives -- the
Gateway still needs to support servers that ask users for input
mid-operation. But the wire protocol changes. The Gateway must recognize
`resultType: "input_required"` responses and handle the retry pattern.
Since MRTR is request/response (not server-initiated), the Gateway no
longer needs to proxy server-to-client messages -- a simplification.

**Risk:** If Gateway 0.6.0 hardcodes `elicitation/create`, it won't
interoperate with 2026-07-28 servers. Servers rebuilt on new SDKs use
MRTR immediately.

> **DECISION NEEDED (D1):** Confirm whether Gateway TP elicitation
> targets 2025-11-25 only (acceptable for TP) or needs dual-version
> support before GA.

### 1.2 Gateway GA: "resumable session management"

**Roadmap says:** GA (Q4 2026) -- HA failover with session continuity.

**Spec now requires:** Sessions removed. `Mcp-Session-Id` header gone.
SSE stream resumability (Last-Event-ID) also removed.

**Assessment: OBSOLETE AS NAMED.** The operational problem persists
(some servers maintain application-level state via server-minted
handles), but this is standard HTTP affinity routing, not MCP session
management. AWS AgentCore confirms: they removed session mechanics
entirely and rely on standard LB affinity.

> **DECISION NEEDED (D2):** Re-scope from "session management" to
> optional HTTP affinity routing. Is that still a GA requirement, or
> post-GA?

### 1.3 Gateway GA: "extended capabilities (prompts, resources, sampling)"

**Spec now requires:** Sampling deprecated (12-month window, earliest
removal July 2027). Prompts and resources remain active.

**Assessment:** Shipping new sampling at GA (Nov 2026) delivers a
feature with ~8 months of spec life remaining. Migration path: direct
LLM API integration.

> **DECISION NEEDED (D3):** Ship sampling support (deprecated but
> functional for 3.6 lifecycle), skip it, or ship as
> "deprecated"-labeled? Option A is safest for existing servers.

### 1.4 MCPLO: protocol-level handshake for readiness

**Spec now requires:** `initialize`/`initialized` removed. Replacement
is `server/discover` (MUST implement).

**Assessment: RENAME -- same intent, different RPC.** Surgical code
change: replace initialize call with server/discover + initialize
fallback. Low risk.

**Timeline:** Address before MCPLO GA (3.6 Stable, Nov 2026). The
upstream kubernetes-sigs project will likely implement this.

### 1.5 Other items

| Feature | Dependency | Risk |
|---|---|---|
| Roots | No RHOAI roadmap dependency | LOW |
| Logging | Gateway OTEL tracing uses OpenTelemetry, not MCP Logging | NONE -- already aligned |
| HTTP+SSE transport | MCPLO supports SSE + Streamable HTTP; Catalog requires Streamable HTTP | LOW for 3.6; revisit 3.7 |
| `ping` | Verify gateway/MCPLO don't use it for health checks | Check |
| `logging/setLevel` | Verify gateway doesn't expose this control | Check |


## 2. Auth hardening gaps

### 2.1 DCR to CIMD migration

**Keycloak status:** CIMD support introduced experimentally in 26.6.0
(April 2026). As of 26.7.0 (July 2026), CIMD remains **experimental**
(not Preview, not Supported). Known issue #49730 prevents CIMD from
working with MCP clients because `none` is not included in
`token_endpoint_auth_methods_supported`.

**Impact on Gateway:** The Gateway uses Authorino backed by Keycloak.
For Gateway GA (Q4 2026), the auth story cannot depend on an
experimental Keycloak feature.

> **DECISION NEEDED (D4):** Gateway GA auth story: DCR (deprecated but
> functional), CIMD (Keycloak experimental), or Gateway-side CIMD
> implementation? Safest for Nov 2026: DCR with CIMD roadmapped.

### 2.2 RFC 9207 issuer validation

Authorization servers SHOULD return `iss` per RFC 9207; MCP clients
MUST validate. Keycloak has supported this since its OAuth 2.1 alignment
work. Verify Authorino's conformance.

### 2.3 Credential binding

Client credentials bound to issuing authorization server (SEP-2352).
If the Gateway persists OAuth credentials for downstream MCP servers,
it must partition them by issuer. Vault key structure may need the AS
issuer identifier.

### 2.4 Enterprise Managed Authorization (EMA)

EMA is now a stable MCP extension. Replaces per-user per-server OAuth
consent with centralized IdP-managed access using ID-JAG tokens via
RFC 8693 token exchange. Okta (branded as Cross App Access / XAA) is
in market. Claude, VS Code, Asana, Atlassian, Figma support it.

**Gap:** EMA is not on the Gateway or Registry roadmap. The Gateway
would need to accept ID-JAG tokens, exchange them for MCP access tokens,
and enforce IdP-level policies. Significant feature, not configuration.

> **DECISION NEEDED (D5):** Add EMA to Gateway roadmap? Which
> milestone? AWS AgentCore and ToolHive Enterprise already support
> centralized IdP integration.


## 3. Deprecation timeline vs RHOAI release train

### 3.1 Timeline mapping

| Feature | Deprecated in | Earliest removal | 3.6 GA (Nov 2026) | 3.7 (H1 2027) | 3.8+ (H2 2027) |
|---|---|---|---|---|---|
| Sampling | 2026-07-28 | 2027-07-28 | SAFE (5mo) | SAFE (1-2mo) | AT RISK |
| Roots | 2026-07-28 | 2027-07-28 | SAFE | SAFE | AT RISK |
| Logging | 2026-07-28 | 2027-07-28 | SAFE | SAFE | AT RISK |
| HTTP+SSE | 2026-07-28 | 2027-07-28 | SAFE | SAFE | AT RISK |
| DCR | 2026-07-28 | 2027-07-28 | SAFE | SAFE | AT RISK |
| `ping` | **REMOVED** | N/A | BROKEN NOW | BROKEN | BROKEN |
| `logging/setLevel` | **REMOVED** | N/A | BROKEN NOW | BROKEN | BROKEN |
| `initialize` | **REMOVED** | N/A | BROKEN for 2026-07-28 servers | BROKEN | BROKEN |

### 3.2 Safe to ship using deprecated capabilities in 3.6

- Gateway sampling support -- 8 months of spec life
- Gateway DCR-based auth -- 8 months of spec life
- MCPLO SSE transport support -- 8 months of spec life

### 3.3 Must address for 3.6 GA

- MCPLO readiness probe: must handle `server/discover` because
  2026-07-28 SDK servers won't respond to `initialize`
- Gateway: must handle `Mcp-Method`/`Mcp-Name` headers from
  2026-07-28 clients (required on Streamable HTTP POST)
- Gateway: must handle `resultType` field in all 2026-07-28 responses

### 3.4 What needs migration before 3.7

- **Sampling:** Migration plan in place, document deprecation
- **DCR:** Keycloak CIMD must reach Preview, or alternative path needed
- **HTTP+SSE:** MCPLO-managed servers using SSE must migrate


## 4. Spec-version compatibility policy for Catalog GA

### 4.1 What server/discover enables

The new RPC returns supported protocol versions, capabilities, and
identity. The catalog can call `server/discover` during certification to
determine spec versions. SDK-built servers answer both `server/discover`
(2026-07-28) and `initialize` (2025-11-25 fallback).

### 4.2 resultType -- not a breaking change

All 2026-07-28 responses carry required `resultType`. The spec says
clients MUST treat results from older servers that omit it as
`"complete"`. Servers adding `resultType` don't break older clients
(JSON-RPC allows extra fields). Not a breaking change for certification.

### 4.3 How competitors handle multi-version

- **AWS AgentCore Gateway:** Multi-version per-request via
  `MCP-Protocol-Version` header. Can translate between versions for
  basic operations. Three-stage rollout: add version, migrate, trim.
- **Docker MCP Catalog:** Governance-focused (blocking unapproved
  servers), no public spec-version matrix.
- **ToolHive:** Version-agnostic registry. Client compatibility by
  minimum Streamable HTTP support.
- **Official MCP Registry:** 36K+ records, version-agnostic by design.

No competitor has published an explicit spec-version compatibility
matrix. AWS is most sophisticated with per-request version selection.

### 4.4 Recommended policy

> **DECISION NEEDED (D6):** Catalog GA spec-version policy.

**Recommended tier-based approach:**
1. **Red Hat tier:** MUST support 2026-07-28. 4 months is enough lead
   time to rebuild on new SDKs.
2. **Partner tier:** SHOULD support 2026-07-28; MUST support at least
   2025-11-25. Grace period for older SDKs.
3. **Community tier:** No version requirement. Display detected version.

**Metadata:** Store and display detected spec versions (from
`server/discover`). Display as filter/badge in catalog UI. Do NOT block
2025-11-25 servers at GA -- deprecation window guarantees they function.

**Gateway:** Must handle both spec versions at GA, matching AgentCore's
approach. Route on `MCP-Protocol-Version` header/`_meta` field.


## 5. Summary of decisions needed

| # | Decision | Owner(s) | Deadline | Impact |
|---|---|---|---|---|
| D1 | Gateway TP elicitation: 2025-11-25 only or dual-version for GA? | Gateway PM + Eng | Aug 2026 | Scopes GA work |
| D2 | Gateway GA "session management": rename/reduce or drop? | Gateway PM | Aug 2026 | Removes/reshapes line item |
| D3 | Ship Gateway GA sampling (deprecated) or skip? | Gateway PM + Eng | Aug 2026 | Effort vs customer need |
| D4 | Gateway GA auth: DCR, CIMD, or Gateway-side CIMD? | Gateway PM + Security | Sep 2026 | Auth architecture |
| D5 | Add EMA to Gateway roadmap? Which milestone? | Gateway PM + Strategy | Oct 2026 | Competitive positioning |
| D6 | Catalog GA spec-version policy per tier? | Catalog PM + Registry PM | Aug 2026 | Partner communication |
| D7 | Track MCPLO server/discover upstream | MCPLO PM | Aug 2026 | Readiness probes |


## 6. What the spec change makes easier

1. **MCPLO scaling** -- MCP servers are standard HTTP microservices. No
   sticky sessions, no state migration during rollouts.
2. **Gateway routing** -- required headers eliminate JSON body parsing
   for routing decisions. Performance improvement.
3. **Caching** -- `ttlMs`/`cacheScope` enable gateway-level caching of
   `tools/list` responses, reducing backend calls.
4. **Tracing** -- W3C Trace Context in `_meta` aligns with gateway OTEL.
5. **Registry metadata** -- `server/discover` provides machine-queryable
   capabilities, reducing manual curation effort.


## Sources

- [MCP 2026-07-28 Blog](https://blog.modelcontextprotocol.io/posts/2026-07-28/)
- [MCP 2026-07-28 Changelog](https://modelcontextprotocol.io/specification/2026-07-28/changelog)
- [MCP SDK Betas](https://blog.modelcontextprotocol.io/posts/sdk-betas-2026-07-28/)
- [Enterprise Managed Authorization Extension](https://modelcontextprotocol.io/extensions/auth/enterprise-managed-authorization)
- [Keycloak 26.6.0 Release Notes](https://www.keycloak.org/2026/04/keycloak-2660-released)
- [Keycloak 26.7.0 Release Notes](https://www.keycloak.org/2026/07/keycloak-2670-released)
- [Keycloak CIMD Issue #45106](https://github.com/keycloak/keycloak/issues/45106)
- [Keycloak CIMD none Bug #49730](https://github.com/keycloak/keycloak/issues/49730)
- [AWS AgentCore Gateway MCP Support](https://aws.amazon.com/blogs/machine-learning/how-agentcore-gateway-supports-the-mcp-2026-07-28-spec/)
- [MCP Auth Evolution](https://medium.com/@ayshsandu/the-evolution-of-mcp-auth-every-spec-every-lesson-2024-11-05-2026-07-28-draft-e3f165a12fdb)
- [RFC 9207 Mix-Up Attacks (WorkOS)](https://workos.com/blog/oauth-mix-up-attacks-rfc-9207)
- [MCP Feature Lifecycle](https://modelcontextprotocol.io/community/feature-lifecycle)
