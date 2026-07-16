---
type: reference
title: Starter Kit Deployment Spec / 3.5 agent discovery (Gage)
description: Gage's spec for deployable starter kits — container rules, catalog YAML schema, deploy flow; written for 3.5, deploy since slipped to 3.6; doubles as the 3.5 agent-discovery doc.
resource: https://docs.google.com/document/d/1iiSzz32I00d879HQTtHzwLd4ZzGmN4A5iKr1tG2mh88
tags: [agent-catalog, starter-kits, deploy]
timestamp: 2026-07-16
review_after: 2026-09-01
source: ai-asset-registry/docs/knowledge-registry.md §12 (as of 2026-07-05); updated at agent-catalog intake 2026-07-16
---
Proposal by Gage Krumbach (references RHAISTRAT-1740): container image rules
(port 8000, agent-card path, non-root, env-var config), catalog YAML schema
for env var metadata (mirrors MCP catalog's `McpEnvVarMetadata`), and the
full deploy flow. Primary source for
[fact-agent-catalog-starter-kits.md](/features/agent-catalog/knowledge/fact-agent-catalog-starter-kits.md).
Deploy was cut from 3.5 on 2026-07-09
([decision](/features/agent-catalog/knowledge/decision-agent-catalog-no-deploy-35.md));
the flow described here is now the 3.6 path.
