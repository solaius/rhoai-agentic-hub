---
type: fact
title: Agent Catalog & Starter Kits (3.5 target)
description: RHOAI AI Hub's curated deployable-agent catalog with a one-click deploy wizard, mirroring the MCP server catalog pattern.
timestamp: 2026-07-06
tags: [agent-registry, catalog, 3.5-target]
review_after: 2026-08-05
source: ai-asset-registry/docs/knowledge-registry.md §3 (as of 2026-07-05)
---
Follows the MCP catalog model: catalog source YAML → Catalog service API (RHAISTRAT-1740) → Deploy wizard UI → BFF → K8s Deployment → agent container. Containers must listen on port 8000, serve `/.well-known/agent-card.json` (A2A agent card), run as non-root (USER 1000), and take all config via env vars (platform auto-injects PORT/HOST/AGENT_ENDPOINT/UV_CACHE_DIR). 3.5 limitation: API keys are plaintext env vars in the Deployment spec — Kubernetes Secrets support is deferred.

Two categories: **template/starter agents** (educational, forkable best-practice examples) and **agentic harness images** (pre-built OpenCode/Claude Code/etc., each needing a thin wrapper for the agent-card + port-8000 contract; full A2A message translation is explicitly NOT 3.5 scope).

See [question-agent-catalog-protocol-diversity.md](/features/agent-registry/knowledge/question-agent-catalog-protocol-diversity.md) for the open protocol-standardization question, and [ref-starter-kit-deployment-spec-rhoai-35.md](/features/agent-registry/knowledge/ref-starter-kit-deployment-spec-rhoai-35.md) for the full spec.
