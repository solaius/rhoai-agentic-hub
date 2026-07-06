---
type: fact
title: Partner MCP Catalog (3.4 DP — completed)
description: A partner + community MCP server catalog shipped in the RHOAI 3.4 DP catalog for Summit.
timestamp: 2026-07-06
tags: [mcp-ecosystem, partners, 3.4-dp]
review_after: 2026-08-05
source: ai-asset-registry/docs/knowledge-registry.md §3 (as of 2026-07-05)
---
A curated set of partner and community MCP servers was integrated into the RHOAI 3.4 DP catalog by the April 10 code freeze — 5 partner servers and 2 community servers, the latter positioned in the "periphery" (demos/blogs/Gen AI Studio configmap only, not full catalog treatment).

Quay org `quay.io/rhoai-partner-mcp` hosts the images; upstream metadata repo is `opendatahub-io/model-metadata-collection`. Technical bar for partners: Streamable HTTP only, on-cluster/local hosting only, UBI-based container, ongoing maintenance commitment, and no RHOAI support for partner-server tickets.

Who made the cut, the consent process, and post-Summit partner-specific plans live in the restricted counterpart of this entry. See [fact-mcp-catalog-metadata-schema.md](/features/mcp-ecosystem/knowledge/fact-mcp-catalog-metadata-schema.md) for the catalog metadata shape.
