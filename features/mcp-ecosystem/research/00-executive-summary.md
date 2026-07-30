---
title: "MCP 2026-07-28 spec impact -- executive summary"
description: Living synthesis of the MCP 2026-07-28 specification's impact on the RHOAI MCP stack (Gateway, MCPLO, Registry, Catalog). Two lenses completed; four available for follow-up.
timestamp: 2026-07-29
review_after: 2026-10-29
---

## What this series covers

The MCP 2026-07-28 specification, published July 28, 2026, transforms
MCP from a bidirectional stateful protocol into a stateless
request/response protocol -- the largest revision since launch. This
research series analyzes its impact on the RHOAI MCP stack.

## Series docs

| # | Doc | Lens | Status |
|---|---|---|---|
| 00 | This summary | -- | Living |
| 01 | [01-architecture-mcp-2026-07-28-impact](01-architecture-mcp-2026-07-28-impact.md) | architecture | Complete |
| 02 | [02-requirements-mcp-2026-07-28-impact](02-requirements-mcp-2026-07-28-impact.md) | requirements | Complete |

## Lens gaps

The following lenses were not run. Retry invocations:

- **competitive**: How competitors (AWS AgentCore, ToolHive, Docker,
  Smithery) are adapting their full stacks to the stateless shift.
  `hub.research mcp-ecosystem competitive`
- **upstream**: SDK migration guides, SEP implementation status in
  upstream repos, AAIF governance response.
  `hub.research mcp-ecosystem upstream`
- **landscape**: Industry analyst coverage, enterprise adoption signals,
  standards-body positioning.
  `hub.research mcp-ecosystem landscape`
- **jira-gap**: Which RHAISTRAT features are misaligned with the new
  spec; direction A (active work vs spec) and B (spec vs active work).
  `hub.research mcp-ecosystem jira-gap`

## Key findings

### The stateless shift is broadly favorable

The protocol changes simplify the RHOAI stack more than they complicate
it. MCP servers become standard HTTP microservices (what K8s operators
are built to manage), session infrastructure becomes unnecessary,
routing moves from body parsing to native HTTP headers, and caching +
tracing get first-class spec support.

### Seven decisions are needed

| # | Decision | Deadline | Impact |
|---|---|---|---|
| D1 | Gateway TP elicitation: 2025-11-25 only or dual-version? | Aug 2026 | Scopes GA engineering |
| D2 | Gateway GA "session management": rename/reduce or drop? | Aug 2026 | Removes/reshapes line item |
| D3 | Ship Gateway sampling (deprecated) or skip? | Aug 2026 | Effort vs 8-month spec life |
| D4 | Gateway GA auth: DCR, CIMD, or Gateway-side CIMD? | Sep 2026 | Auth architecture; Keycloak CIMD is experimental |
| D5 | Add EMA to Gateway roadmap? Which milestone? | Oct 2026 | Enterprise auth competitive gap |
| D6 | Catalog GA spec-version policy per tier? | Aug 2026 | Partner onboarding, certification pipeline |
| D7 | Track MCPLO server/discover upstream | Aug 2026 | Readiness probes against new servers |

### Four roadmap items are affected

1. **Gateway TP "elicitation support"** -- MRTR replaces `elicitation/create`.
   Intent survives; wire protocol changes. Needs redesign for GA.
2. **Gateway GA "resumable session management"** -- **Obsolete as named.**
   Sessions removed from protocol. Rename to optional HTTP affinity.
3. **Gateway GA "sampling"** -- Deprecated with 12-month window. Still
   functional for 3.6 lifecycle but building new investment on it is
   questionable.
4. **MCPLO readiness probe** -- `initialize` removed; replace with
   `server/discover` + fallback. Surgical code change.

### Auth transition is the hardest gap

Keycloak CIMD support is experimental (26.6.0 / 26.7.0). Known bug
#49730 prevents it from working with MCP clients. DCR is deprecated but
functional. The Gateway GA (Nov 2026) auth story cannot depend on
experimental Keycloak features. EMA (Enterprise Managed Authorization)
is now a stable MCP extension but not on any RHOAI roadmap.

### Deprecation timeline gives breathing room for 3.6

Everything deprecated has a 12-month window (earliest removal July
2027). RHOAI 3.6 GA (Nov 2026) can safely ship using deprecated
capabilities. RHOAI 3.7 (H1 2027) is the migration deadline. RHOAI
3.8+ (H2 2027) is at risk.

**Removed features** (not deprecated -- gone now): `initialize`,
`Mcp-Session-Id`, `ping`, `logging/setLevel`,
`notifications/roots/list_changed`. These break against 2026-07-28
servers immediately.

### Architecture wins

- **Gateway ext_proc**: 4 of 8 responsibilities eliminated by headers +
  statelessness. Accelerates the native Envoy MCP filter migration
  (issue #809).
- **MCPLO scaling**: No session affinity needed. Standard
  RollingUpdate, standard HPA.
- **Gateway caching**: `ttlMs` + `cacheScope` enable spec-blessed
  caching of tool/prompt/resource lists.
- **Tracing**: W3C Trace Context in `_meta` aligns with Gateway OTEL.
- **Registry metadata**: `server/discover` provides machine-queryable
  capabilities, versions, identity.

## Recommended follow-ups

1. **hub.research mcp-ecosystem jira-gap** -- map the 7 decisions
   against active RHAISTRAT/RHOAIENG work and identify misaligned Jira
   items.
2. **hub.strategy mcp-ecosystem** -- synthesize this research series
   into the living strategy doc.
3. Update the published [MCP 2026-07-28 RHOAI Impact Analysis](/narrative/enablement/mcp-spec-rc-impact/artifact.md)
   artifact with the new findings (the artifact was written against the
   RC; this research covers the final spec with deeper analysis).
