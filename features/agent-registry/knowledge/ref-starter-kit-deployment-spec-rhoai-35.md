---
type: reference
title: Starter Kit Deployment Spec — RHOAI 3.5
description: How starter kits must be structured for the 3.5 deploy wizard — container rules, catalog YAML schema, deploy flow.
resource: https://docs.google.com/document/d/1iiSzz32I00d879HQTtHzwLd4ZzGmN4A5iKr1tG2mh88
tags: [agent-registry, starter-kits, 3.5-target]
timestamp: 2026-07-06
source: ai-asset-registry/docs/knowledge-registry.md §12 (as of 2026-07-05)
review_after: 2026-08-05
---
Proposal by Gage Krumbach (references RHAISTRAT-1740): container image rules (port 8000, agent-card path, non-root, env-var config), catalog YAML schema for env var metadata (mirrors MCP catalog's `McpEnvVarMetadata`), and the full deploy flow. Primary source for [fact-agent-catalog-starter-kits.md](/features/agent-registry/knowledge/fact-agent-catalog-starter-kits.md).
