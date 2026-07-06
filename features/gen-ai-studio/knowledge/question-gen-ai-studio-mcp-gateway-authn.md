---
type: question
title: How does MCP Gateway OAuth token exchange flow through Playground user identity?
description: When Gen AI Studio's Playground calls MCP servers behind the MCP Gateway, how does the end user's identity flow through for per-tool authorization — requires BFF/OGX/Gateway coordination not yet designed.
status: open
timestamp: 2026-07-06
tags: [gen-ai-studio, mcp-gateway, identity, oauth]
source: ai-asset-registry/docs/knowledge-review/components/gen-ai-studio-architecture.md §9, §14 (as of 2026-07-05)
---
Phase 2 of Gen AI Studio's MCP Gateway integration plan ([RHAIRFE-2479](https://redhat.atlassian.net/browse/RHAIRFE-2479) OAuth auth, [RHAIRFE-2480](https://redhat.atlassian.net/browse/RHAIRFE-2480) identity delegation — see [fact-gen-ai-studio-mcp-integration-roadmap.md](/features/gen-ai-studio/knowledge/fact-gen-ai-studio-mcp-integration-roadmap.md)) requires the Playground user's own identity to flow through to MCP servers sitting behind the MCP Gateway, so per-tool authorization reflects the actual end user rather than a shared service identity. This needs coordination across the Gen AI Studio BFF, OGX, and MCP Gateway — the token-exchange mechanics aren't designed yet. Related but distinct from the platform-level [question-ai-gateway-tenancy-mcp-registry.md](/features/platform/knowledge/question-ai-gateway-tenancy-mcp-registry.md) (group-based tenancy for MCP tool catalogs) and [question-registry-state-gateway-behavior.md](/features/mcp-gateway/knowledge/question-registry-state-gateway-behavior.md) (registry state informing gateway behavior) — this question is specifically about per-user identity delegation from a Gen AI Studio client, not tenancy or registry-state propagation.
