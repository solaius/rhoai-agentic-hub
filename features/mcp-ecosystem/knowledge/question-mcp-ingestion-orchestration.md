---
type: question
title: How should the partner MCP ingestion pipeline be orchestrated?
description: Konflux was suggested for orchestrating the partner ingestion pipeline stages, but this needs investigation.
status: open
timestamp: 2026-07-06
tags: [mcp-ecosystem, ingestion, konflux]
source: ai-asset-registry/docs/knowledge-registry.md §13 (as of 2026-07-05)
---
[fact-mcp-ingestion-pipeline.md](/features/mcp-ecosystem/knowledge/fact-mcp-ingestion-pipeline.md) documents the two ingestion lanes and shared pipeline stages (validate, scan, evaluate, containerize), but not what runs/schedules them. Konflux has been suggested as the orchestration mechanism; not yet investigated.
