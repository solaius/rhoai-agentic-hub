---
type: fact
title: "MCP catalog competitive landscape (July 2026)"
description: Refreshed landscape — incumbents' moves (Docker OCI catalogs, Databricks Unity AI Gateway, ToolHive coopetition) plus five new enterprise entrants (AWS, Google, IBM, Salesforce/MuleSoft, Kong); the governance differentiator is eroding, the integrated-chain card still holds.
tags: [mcp-catalog, competitive]
features: [mcp-ecosystem, mcp-registry]
timestamp: 2026-07-09
review_after: 2026-09-15
source: hub.research run 2026-07-09 (adversarially verified) — /features/mcp-catalog/research/02-competitive-mcp-catalogs.md
---

Supersedes the 2026-07-06 seven-competitor snapshot
([old entry](/features/mcp-ecosystem/knowledge/fact-competitive-landscape-mcp-catalogs.md)).
Full detail and sources: [research 02](/features/mcp-catalog/research/02-competitive-mcp-catalogs.md).

| Player | Position (July 2026) |
|---|---|
| Docker MCP Catalog | Signed composable OCI catalog artifacts, private catalogs anywhere; AI Governance product (May 2026) blocks unapproved servers by default |
| Databricks Unity AI Gateway | Unity governance extended to MCP; content-aware per-action policies (beta); managed MCP servers |
| ToolHive (Stacklok) | **Coopetition — co-maintained by Red Hat**; multi-source federation into named catalogs; Sigstore trust chain; runs on OpenShift |
| Microsoft Copilot Studio | MCP GA since 2025-05-29; agent-workflow MCP tools GA 2026-07-15 |
| GitHub MCP Registry | Publish-once flow with official registry; org/enterprise config; auth-centric roadmap |
| Official MCP Registry | ≥36K total / ≥10K latest records (live pull 2026-07-09) yet still preview/v0.1; minimal moderation by design |
| AWS Agent Registry | NEW (preview 2026-04-09) — private governed catalog, approval workflow, semantic search, CloudTrail audit |
| Google Cloud API Registry | NEW (preview) — curated MCP tool registry for Vertex Agent Builder; Apigee API→MCP conversion |
| IBM watsonx Orchestrate | NEW — Agent Catalog + Agentic Control Plane (June 2026) |
| Salesforce/MuleSoft | NEW — Agent Registry of SaaS-provider-hosted MCP servers; AgentExchange listings |
| Kong MCP Registry | NEW — Konnect tech preview (since 2026-02), API-dependency linkage, OAuth 2.1 RS posture |
| Directories | PulseMCP 21.5K (verified) and MCP.so ~21K lead; Smithery (~7K) no longer "largest" |

**Differentiation read:** "nobody owns enterprise governance end-to-end"
is eroding — AWS, Databricks, Docker, and Kong are all building
discovery+governance+runtime. Red Hat's still-unmatched cards: the
shipped single-platform discover→deploy→connect→consume chain, and
hybrid/multi-cloud open-source positioning vs single-cloud lock-in.
UBI+scanning trust is now table stakes, not a differentiator. The
three-way Directory/Registry/Enterprise-Platform framing survives as
analysis but is not market vocabulary.
