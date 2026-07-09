---
type: fact
title: MCP catalog/registry competitive landscape
description: How Smithery, Docker, GitHub, ToolHive, Microsoft, and Databricks position their MCP catalogs/registries, and Red Hat's differentiation.
timestamp: 2026-07-06
tags: [mcp-ecosystem, competitive, mcp-registry]
review_after: 2026-08-05
source: ai-asset-registry/docs/knowledge-registry.md §9 (as of 2026-07-05); third-party directories and three-way distinction from ai-asset-registry/docs/knowledge-review/competitive/landscape.md (as of 2026-07-05)
---
Seven competitors identified, each solving a slice of MCP discovery:

| Competitor | Type | Key differentiator |
|---|---|---|
| Smithery | Open marketplace | Billed as the "largest" open marketplace; CLI/SDK |
| Docker MCP Catalog | Curated + containerized | Verified Docker images; Docker Desktop integration |
| GitHub MCP Registry | Open registry | GitHub identity; announced Sep 2025 |
| Official MCP Registry | Protocol-official | "App store for MCP servers" |
| ToolHive (Stacklok) | Open + secure runtime | Security-focused; sandboxed containers |
| Microsoft Copilot Studio | Closed vendor | In-product certified connectors |
| Databricks Unity Catalog | Enterprise | Unified governance for data + AI |

**Red Hat's differentiator**: none of the above own enterprise governance, lifecycle management, policy enforcement, and platform integration — they solve discovery/listing, not governance. This is the gap the MCP Registry (see [fact-mcp-registry.md](/features/mcp-registry/knowledge/fact-mcp-registry.md)) is built to fill.

**Two more third-party aggregators** (a different competitive category — scale-focused directories, not governed registries): MCP.so (third-party directory, claims 16K+ servers) and Pulse MCP (directory, reports 6K+ servers).

**Three-way distinction** this landscape falls into: **Directory/Marketplace** (discovery only — Smithery, MCP.so, Pulse MCP) vs. **Registry** (governed, runnable assets — Docker MCP, ToolHive, Red Hat MCP Registry) vs. **Enterprise Platform** (full lifecycle governance + runtime — Red Hat's proposed registry, Databricks Unity Catalog). Red Hat's target tier is the third; the two aggregators above are pure scale plays, a different category entirely from the governance argument above.

Likely sourced from the same "Agentic AI Strategy 2026" doc as [ref-agentic-ai-strategy-2026.md](/narrative/knowledge/ref-agentic-ai-strategy-2026.md) (that entry's description explicitly promises "competitive analysis") — the monolith didn't cite an explicit source line for the original seven-row table, so treat that link as inferred, not confirmed. The two additional aggregators and the three-way distinction come from a separately-sourced competitive-landscape writeup in the old repo's `docs/knowledge-review/` decomposition (no explicit source line there either — same caveat applies).
