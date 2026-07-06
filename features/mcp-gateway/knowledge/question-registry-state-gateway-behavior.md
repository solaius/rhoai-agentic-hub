---
type: question
title: How should registry state inform gateway behavior?
description: Open question on how MCP Registry governance state (e.g. approval/certification) should feed into MCP Gateway routing/enforcement decisions.
status: open
timestamp: 2026-07-06
tags: [mcp-gateway, mcp-registry, integration]
source: ai-asset-registry/docs/knowledge-registry.md §7 (as of 2026-07-05)
---
Open question for the upstream proposal: once the MCP Registry has governance state for a server/version (lifecycle, approval, verification, certification — see [fact-mcp-registry-data-model-proposal.md](/features/mcp-registry/knowledge/fact-mcp-registry-data-model-proposal.md)), how should that state actually inform MCP Gateway behavior at runtime — e.g., does the gateway refuse to route to an unapproved or revoked version? Ties to "MCP Registry Integration," already tracked as a GA-milestone line item in [fact-mcp-gateway-roadmap.md](/features/mcp-gateway/knowledge/fact-mcp-gateway-roadmap.md), but the runtime behavior contract isn't yet specified.
