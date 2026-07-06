---
type: fact
title: MCP catalog metadata schema
description: The defined metadata fields for MCP servers listed in the RHOAI catalog — core, MCP-specific, and security-indicator fields.
timestamp: 2026-07-06
tags: [mcp-ecosystem, catalog, schema]
review_after: 2026-08-05
source: ai-asset-registry/docs/knowledge-registry.md §3 (as of 2026-07-05)
---
Defined for the 3.4 DP partner catalog effort:
- **Core**: name, description, provider, logo, license (SPDX), licenseLink, readme.
- **MCP-specific**: `tools[]` (name, description, parameters, access type, revoked/revokedReason), transportType, deploymentMode, `artifacts[]` (OCI URIs), `endpoints[]`.
- **Security indicators**: verifiedSource, sast, secureEndpoint, readOnlyTools.

No standardized upstream schema exists beyond this — all 4 partner MCPs in 3.4 shipped with different metadata shapes before this was defined.
