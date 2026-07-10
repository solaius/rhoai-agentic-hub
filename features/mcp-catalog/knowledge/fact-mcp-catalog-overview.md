---
type: fact
title: MCP Catalog — overview
description: The MCP server storefront in RHOAI — what it is, the discover→deploy→connect→consume chain, roadmap (DP 3.4 shipped → TP 3.6 EA1 → GA 3.6 Stable, Nov 2026), tiers, and key links.
tags: [mcp-catalog, roadmap, overview]
features: [mcp-ecosystem, mcp-registry]
timestamp: 2026-07-09
review_after: 2026-09-15
---

The MCP Catalog is the storefront of deployable MCP servers in RHOAI — "a
curated catalog of MCP servers that you can discover, deploy, and manage
directly on Red Hat OpenShift"
([launch blog](/features/mcp-ecosystem/knowledge/ref-mcp-catalog-launch-blog.md)).
Unlike discovery-only registries it provides a governed path from discovery
to deployment to consumption: **Discover** in the catalog UI → **Deploy**
via the MCP Lifecycle Operator → **Connect** through the MCP Gateway →
**Consume** in Gen AI Studio. AI Hub treats MCP servers as first-class
citizens alongside models.

## Status & roadmap (owner statement, 2026-07-09)

- **DP shipped** in RHOAI 3.4 (announced 2026-05-12; MCPLO dev preview,
  Gateway tech preview at that point).
- **TP scheduled** for RHOAI 3.6 EA1.
- **GA scheduled** for RHOAI 3.6 Stable (November 2026).

## Tiers & content

Red Hat, Partner, Community, and approved enterprise MCP servers. 3.4 DP
partners: Confluent, EDB, IBM, Microsoft Azure, Dynatrace; community:
MongoDB, MariaDB. Catalog content upstream:
[model-metadata-collection](/features/mcp-ecosystem/knowledge/ref-model-metadata-collection-repo.md).

## Boundaries (routing)

- Partner onboarding pipeline, evaluation, server building →
  [mcp-ecosystem](/features/mcp-ecosystem/index.md)
- Governance / system-of-record / data model →
  [mcp-registry](/features/mcp-registry/index.md)
- Runtime connectivity → [mcp-gateway](/features/mcp-gateway/index.md)
- This partition: the catalog product surface — discovery UX, AI Hub
  integration, release train, catalog STRATs.

## Key links

- [Launch blog (live)](/features/mcp-ecosystem/knowledge/ref-mcp-catalog-launch-blog.md)
- [PM write-up / requirements GDoc](/features/mcp-registry/knowledge/ref-mcp-catalog-writeup.md)
- [Catalog STRAT Jiras](/features/mcp-catalog/knowledge/ref-mcp-catalog-strat-jiras.md)
- Slack: [#forum-ai-asset-management](https://redhat-internal.slack.com/archives/C091PSZ5BB8)
  (see the [channel index](/features/platform/knowledge/fact-slack-channels-by-product-area.md))
- Presentation: [MCP management hub](/features/mcp-ecosystem/enablement/management-hub/index.html)
  — ecosystem fit and component overview
