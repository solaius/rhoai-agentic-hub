---
type: question
title: Model selection x rate limiting x ITS fan-out — cost multiplication gap
description: Intelligent model-selection failover could pick a more expensive model while inference-time-scaling fan-out multiplies the request count, compounding cost.
status: open
timestamp: 2026-07-06
tags: [platform, ai-gateway, cost, its]
source: ai-asset-registry/docs/knowledge-registry.md §13 (as of 2026-07-05)
---
Gap identified at the AI Gateway F2F: if the gateway's intelligent routing (Filter/Scorer/Picker, decision 3 in [decision-ai-gateway-f2f-architecture.md](/restricted/features/platform/knowledge/decision-ai-gateway-f2f-architecture.md)) selects a more expensive model on failover, and inference-time-scaling fan-out multiplies requests on top of that, costs could compound in a way nothing currently guards against.
