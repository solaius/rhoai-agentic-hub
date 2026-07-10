---
type: fact
title: "MCP upstream status — registry, governance, spec (July 2026)"
description: Official registry is big but immature (≥36K records, still preview/v0.1); MCP governed by the Linux Foundation's AAIF since Dec 2025; largest-ever spec revision finalizes 2026-07-28 (stateless HTTP); upstream expects vendor catalogs to federate as subregistries.
tags: [mcp-catalog, upstream, mcp-spec]
features: [mcp-registry, mcp-gateway]
timestamp: 2026-07-09
review_after: 2026-08-15
source: hub.research run 2026-07-09 (adversarially verified) — /features/mcp-catalog/research/01-upstream-mcp-catalog-registry.md
---

Decision-ready upstream atoms (all primary-source verified 2026-07-09;
detail in [research 01](/features/mcp-catalog/research/01-upstream-mcp-catalog-registry.md)):

- **Official MCP Registry**: ≥36,000 total / ≥10,000 latest server
  records (live API pagination) — yet still **preview**, API frozen at
  **v0.1** since 2025-10-24, no GA committed in the 2026 roadmap.
  Moderation is deliberately minimal (illegal/malware/spam only);
  quality and security are pushed to subregistries.
- **Federation model**: downstream vendor catalogs are expected to poll
  as aggregators or implement the subregistry OpenAPI spec with
  namespaced `_meta` extensions; host apps are told not to consume the
  official registry directly. RHOAI catalog posture: unstated →
  [open question](/features/mcp-catalog/knowledge/question-official-registry-federation.md).
- **Governance**: MCP donated to the **Agentic AI Foundation** (Linux
  Foundation directed fund; Anthropic/Block/OpenAI co-founders; AWS,
  Google, Microsoft, Cloudflare, Bloomberg platinum) on 2025-12-09;
  maintainer process unchanged.
- **Spec**: largest revision since launch finalizes **2026-07-28**
  (RC since 2026-05-21): streamable HTTP goes stateless (no
  `initialize`, no `Mcp-Session-Id`), mandatory `server/discover`, SSE
  resumability removed, OAuth DCR deprecated for Client ID Metadata
  Documents, full JSON Schema 2020-12 in tool schemas. No
  server.json/registry schema changes ride along. GA-window impact →
  [open question](/features/mcp-catalog/knowledge/question-spec-version-policy-ga.md).
- **No protocol-level signing standard exists** — trust chains (Docker
  Cosign+SBOM, ToolHive Sigstore+attestations) are tooling-layer;
  the catalog's enterprise-tier trust story has no upstream default to
  inherit and must state its own chain.
