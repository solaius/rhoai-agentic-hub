---
type: question
title: Cross-datacenter rate limit enforcement
description: How to enforce a single user's token-rate limit across multiple datacenters without unacceptable latency or complexity.
status: open
timestamp: 2026-07-06
tags: [platform, ai-gateway, rate-limiting]
source: ai-asset-registry/docs/knowledge-registry.md §13 (as of 2026-07-05)
---
Example: a user with a 100K token/hour limit hitting both DC-East and DC-West. Options on the table: shared Redis (adds latency), split per-DC budgets, or eventual consistency with reconciliation. Raised at the AI Gateway F2F (April 2026) as an open item — not one of the six binding decisions in [decision-ai-gateway-f2f-architecture.md](/restricted/features/platform/knowledge/decision-ai-gateway-f2f-architecture.md). See [fact-ai-gateway.md](/features/platform/knowledge/fact-ai-gateway.md) for the broader ~60%-detailed status this falls under.
