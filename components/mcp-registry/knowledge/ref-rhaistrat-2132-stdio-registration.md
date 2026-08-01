---
type: reference
title: "STDIO MCP Server Registration (RHAISTRAT-2132)"
description: Transport-aware registration so STDIO servers join the same governance flows as HTTP/SSE.
resource: https://redhat.atlassian.net/browse/RHAISTRAT-2132
tags: [mcp-registry, jira, strategy]
timestamp: 2026-07-10
source: hub.jira-sweep 2026-07-10
review_after: 2026-08-09
---
Makes registration transport-aware: STDIO MCP servers, which have no endpoint URL, can register and flow through the same versioning, lifecycle, and approval governance as HTTP/SSE servers. Closes a validation gap in the access-binding layer.
