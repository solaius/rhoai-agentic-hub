---
type: question
title: How should MCP server icons transfer from Catalog to Registry?
description: The catalog stores icons as base64 SVGs; MLflow expects icon URLs. Air-gapped clusters rule out URL-only approaches. Needs MLflow team input.
status: open
timestamp: 2026-08-01
tags: [mcp-registry, mcp-catalog, metadata, icons, air-gap]
people: [Dan Kuc]
---
The MCP Catalog (Kubeflow Hub) stores server icons as inline base64-encoded
SVGs in its `logo` metadata field. The MCP Registry (MLflow) expects to load
icons from URLs. This gap blocks icon transfer during the Catalog-to-Registry
registration flow (RHAISTRAT-2027).

## Constraint

Disconnected (air-gapped) clusters rule out any approach that requires the
registry to fetch icons from an external URL at render time. The solution
must work when the catalog and registry are co-located but have no outbound
network access.

## Options considered

1. **Catalog serves icons at a URL** (e.g.
   `/api/mcp_catalog/v1alpha1/servers/{name}/icon`) — registry stores that
   URL. Simple, but breaks in air-gapped environments if the catalog is
   unreachable from the registry's UI consumer.

2. **`icon_data` field on MLflow** — registry accepts inline base64 SVG at
   registration time, stores it alongside governance metadata. Works in all
   environments. Requires an upstream MLflow change.

3. **Hybrid** — registry stores a URL, but the deployment operator (MCPLO)
   or catalog operator bundles icons into a cluster-local static route so
   the URL resolves locally. More moving parts.

## Current leaning

Option 2 (`icon_data`) is the most robust for air-gap support. Needs MLflow
team input on whether they would accept an inline icon field upstream.

## Source

Raised by Dan Kuc (2026-08-01) during MCP Registry implementation work.
Discussed in Slack with Peter Double.
