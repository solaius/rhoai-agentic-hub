---
type: fact
title: Gen AI Studio's MCP Gateway integration — 3 planned phases
description: How Gen AI Studio moves off hand-authored ConfigMaps to registry-discovered, gateway-mediated MCP tool access — discovery, then gateway auth/aggregation, then AI Assets convergence.
timestamp: 2026-07-06
tags: [gen-ai-studio, mcp-gateway, mcp-registry, roadmap]
review_after: 2026-08-05
source: ai-asset-registry/docs/knowledge-review/components/gen-ai-studio-architecture.md §9 (as of 2026-07-05)
---
Today, MCP servers reach Gen AI Studio only via hand-authored Kubernetes ConfigMaps (`gen-ai-aa-mcp-servers`, per [fact-mcp-lifecycle-operator.md](/features/mcp-registry/knowledge/fact-mcp-lifecycle-operator.md)'s description of the same bridge from the deployment side) — no browse-and-select UI. Three planned phases move this onto governed rails:

1. **MCP Discovery from Registry** ([RHAISTRAT-1678](https://redhat.atlassian.net/browse/RHAISTRAT-1678)) — browse MCP servers from the MCP Registry directly in the Gen AI Studio UI, eliminating manual ConfigMap authoring. Named enterprise customers driving this demand are restricted — see [fact-mcp-discovery-customer-demand.md](/restricted/features/gen-ai-studio/knowledge/fact-mcp-discovery-customer-demand.md) (restricted).
2. **MCP Gateway integration** (3.6) — OAuth authentication for MCP Gateway endpoints, identity delegation (user identity flows through to MCP servers), multi-server tool aggregation behind one gateway endpoint, virtual MCP server selection (curated tool collections), and token lifecycle management for gateway connections.
3. **AI Assets integration** ([RHAISTRAT-1576](https://redhat.atlassian.net/browse/RHAISTRAT-1576)) — surface MCP endpoints in the AI Asset Endpoints view alongside model-serving endpoints, for unified discovery across all AI assets.

This is the consumption-side mirror of the registry-governed target flow already captured in [fact-mcp-flow-34-to-35.md](/features/mcp-registry/knowledge/fact-mcp-flow-34-to-35.md) — that entry covers how MCP servers get governed and deployed; this one covers how Gen AI Studio, specifically, will discover and use them once governed. See [question-gen-ai-studio-mcp-gateway-authn.md](/features/gen-ai-studio/knowledge/question-gen-ai-studio-mcp-gateway-authn.md) for the open identity-flow-through question phase 2 raises, and the full architecture in [gen-ai-studio-architecture.md](/features/gen-ai-studio/research/gen-ai-studio-architecture.md).
