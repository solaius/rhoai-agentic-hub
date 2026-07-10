---
type: question
title: Should the RHOAI MCP Catalog federate with the official MCP registry?
description: Upstream expects vendor catalogs to act as subregistries (OpenAPI spec + namespaced _meta) or aggregators; RH has no stated posture — a TP-window (3.6 EA1) decision.
status: open
tags: [mcp-catalog, upstream, federation]
features: [mcp-registry]
timestamp: 2026-07-09
source: hub.research run 2026-07-09 — /features/mcp-catalog/research/01-upstream-mcp-catalog-registry.md
---

The official registry (≥36K records, preview/v0.1) defines a subregistry
OpenAPI spec with namespaced `_meta` extensions for exactly the metadata
RH adds (scan results, certification, tiers), and tells host apps to
consume subregistries, not the registry itself. GitHub's publish-once
flow shows the pattern working; ToolHive realigned onto the official
server.json schema in April.

Options: (a) implement the subregistry spec (RH catalog becomes a
governed subregistry — upstream-native, discoverable); (b) aggregator
polling only (consume, don't expose); (c) no federation (fully closed
catalog). Decision shapes TP scope, the metadata schema, and whether RH
publishes its own servers to the official registry namespace (none
found there today).
