---
type: fact
title: Keycloak CIMD support is experimental (26.6.0-26.7.0) with blocking MCP bug
description: "Keycloak introduced experimental CIMD in 26.6.0 (Apr 2026). As of 26.7.0 (Jul 2026), CIMD remains experimental. Bug #49730 prevents MCP client compatibility (none not in token_endpoint_auth_methods_supported). Red Hat build of Keycloak 26.6 requires --features=cimd."
timestamp: 2026-07-29
tags: [keycloak, cimd, auth, mcp-spec]
features: [mcp-gateway, mcp-registry]
review_after: 2026-10-29
source: hub.research mcp-ecosystem requirements 2026-07-29; Keycloak 26.6.0/26.7.0 release notes
---

Client ID Metadata Documents (CIMD) replaces DCR in MCP 2026-07-28.
Keycloak status:

- **26.6.0 (Apr 2026):** Introduced CIMD as experimental feature.
  Requires `--features=cimd` flag. Red Hat build of Keycloak 26.6
  documents it as experimental.
- **26.7.0 (Jul 2026):** Bug fixes (#49456, #49457) for policy
  enforcement gaps. CIMD remains **experimental** (not Preview, not
  Supported).
- **Bug #49730:** `none` is not included in
  `token_endpoint_auth_methods_supported`, preventing CIMD from working
  with MCP clients like Claude Code. Open as of 2026-07-29.

**Impact on RHOAI:** Gateway GA (Nov 2026) auth story cannot depend on
experimental Keycloak features. DCR (deprecated but functional) is the
safe path for GA. CIMD readiness is a 3.7 planning dependency.

Sources:
- https://www.keycloak.org/2026/04/keycloak-2660-released
- https://www.keycloak.org/2026/07/keycloak-2670-released
- https://github.com/keycloak/keycloak/issues/49730
- https://github.com/keycloak/keycloak/issues/45106
