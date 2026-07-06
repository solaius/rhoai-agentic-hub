---
type: fact
title: Gen MCP
description: Tool for generating, containerizing, and production-wrapping MCP servers from API/CLI/HTTP definitions.
timestamp: 2026-07-06
tags: [mcp-ecosystem, gen-mcp, tooling]
source: ai-asset-registry/docs/knowledge-registry.md §3 (as of 2026-07-05)
---
Generates MCP servers from OpenAPI definitions, CLI interfaces, or HTTP backends; containerizes with the KO build tool; adds security/auth/TLS/observability wrappers for production readiness. Team: Calum Murray, Matthias Weßendorf, Nader Ziada. Useful in the ingestion pipeline for wrapping stdio/unsecured HTTP MCPs that partners provide without production-ready containers — though its containerization is opinionated to its own generated servers, so fully production-ready partner MCPs are usually better served by standard podman/docker builds.

Evaluations were extracted into their own project — see [fact-mcp-checker.md](/features/mcp-ecosystem/knowledge/fact-mcp-checker.md) — so they can run against any MCP server, not just Gen MCP's. Broader build-tool landscape: see `mcps/mcp-build-server/knowledge-registry.md` in the old repo (out of scope for this batch) and [fact-mcp-build-server-ecosystem.md](/features/mcp-ecosystem/knowledge/fact-mcp-build-server-ecosystem.md).
