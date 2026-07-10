---
type: question
title: What spec-version compatibility policy does the catalog certify at GA?
description: The largest-ever MCP revision finalizes 2026-07-28 (stateless HTTP, handshake removed); catalog GA (Nov 2026) certifies servers ~4 months later with no stated 2025-11-25 vs 2026-07-28 compatibility matrix.
status: open
tags: [mcp-catalog, mcp-spec, ga]
features: [mcp-gateway]
timestamp: 2026-07-09
source: hub.research run 2026-07-09 — /features/mcp-catalog/research/01-upstream-mcp-catalog-registry.md
---

The 2026-07-28 spec makes streamable HTTP stateless (no `initialize`,
no `Mcp-Session-Id`, mandatory `server/discover`), removes SSE
resumability, and deprecates OAuth DCR — with a 12-month deprecation
window policy. Catalog GA (3.6 Stable, Nov 2026) will certify servers
straddling both spec generations.

Needs a stated policy: which spec versions do catalog entries declare,
what does the gateway accept, and what do RH/Partner tiers REQUIRE at
GA (e.g., 2026-07-28 mandatory for RH tier, declared-version metadata
for others)? Affects partner onboarding lead time and gateway
compatibility testing.
