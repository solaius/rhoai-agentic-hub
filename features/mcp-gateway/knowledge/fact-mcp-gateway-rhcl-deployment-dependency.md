---
type: fact
title: "MCP Gateway <-> RHCL deployment dependency"
description: The dependency direction between MCP Gateway and RHCL, how it's packaged release over release, and the OLM 1.0 question at OCP 5.0.
timestamp: 2026-07-06
tags: [mcp-gateway, rhcl, deployment, olm]
review_after: 2026-08-05
source: ai-asset-registry/docs/knowledge-registry.md §6 (as of 2026-07-05)
---
Dependency runs one direction: RHCL does not depend on MCP Gateway, but MCP Gateway depends on RHCL (Kuadrant Operator, Authorino, Limitador — see [fact-mcp-gateway.md](/features/mcp-gateway/knowledge/fact-mcp-gateway.md)).

Packaging over the release train:
- **RHOAI 3.4**: RHCL listed as a prerequisite — not auto-deployed alongside MCP Gateway.
- **RHOAI 3.5**: request to include MCP Gateway deployment directly in RHOAI (RHAIRFE-1457).
- **OCP 5.0**: OLM 1.0 removes dependency declarations entirely — needs an alternative strategy for expressing the RHCL dependency once that lands.

Adjacent packaging concern for a different component: the MCP Lifecycle Operator's own OLM/OperatorHub bundling choice is covered in [ref-rhoai-limited-mcp-lifecycle-faq.md](/restricted/features/mcp-registry/knowledge/ref-rhoai-limited-mcp-lifecycle-faq.md) (restricted).
