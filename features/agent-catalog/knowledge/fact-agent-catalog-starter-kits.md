---
type: fact
title: Starter kit deploy contract (now 3.6)
description: The container contract for deployable starter kits — port 8000, A2A agent-card endpoint, non-root, env-var config; written for the 3.5 deploy wizard, now governs the 3.6 deploy flow.
timestamp: 2026-07-16
tags: [agent-catalog, starter-kits, deploy-contract]
review_after: 2026-09-01
source: ai-asset-registry/docs/knowledge-registry.md §3 (as of 2026-07-05); updated at agent-catalog intake 2026-07-16
---
Follows the MCP catalog model: catalog source YAML → Catalog service API
(RHAISTRAT-1740) → Deploy wizard UI → BFF → K8s Deployment → agent
container. Containers must listen on port 8000, serve
`/.well-known/agent-card.json` (A2A agent card), run as non-root (USER
1000), and take all config via env vars (platform auto-injects
PORT/HOST/AGENT_ENDPOINT/UV_CACHE_DIR). Known limitation: API keys are
plaintext env vars in the Deployment spec — Kubernetes Secrets support is
deferred.

Originally the RHOAI 3.5 deploy-wizard spec; the deploy button was cut from
3.5 on 2026-07-09
([decision](/features/agent-catalog/knowledge/decision-agent-catalog-no-deploy-35.md)),
so this contract now governs the 3.6 deployment flow — with "supported",
not "validated", images
([decision](/features/agent-catalog/knowledge/decision-supported-not-validated-images.md)).

Two categories: **template/starter agents** (educational, forkable
best-practice examples) and **agentic harness images** (pre-built
OpenCode/Claude Code/etc., each needing a thin wrapper for the agent-card +
port-8000 contract; full A2A message translation is explicitly out of
near-term scope).

See
[question-agent-catalog-protocol-diversity.md](/features/agent-catalog/knowledge/question-agent-catalog-protocol-diversity.md)
for the open protocol-standardization question, and
[ref-starter-kit-deployment-spec-rhoai-35.md](/features/agent-catalog/knowledge/ref-starter-kit-deployment-spec-rhoai-35.md)
for the full spec.
