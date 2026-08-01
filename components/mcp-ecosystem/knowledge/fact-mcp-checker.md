---
type: fact
title: MCP Checker (mcpchecker)
description: Generic MCP server evaluation framework, extracted from Gen MCP, that runs evals against any MCP server with configurable agents.
timestamp: 2026-07-06
tags: [mcp-ecosystem, evaluation, mcpchecker]
source: ai-asset-registry/docs/knowledge-registry.md §3 (as of 2026-07-05)
---
Runs evals against any MCP server (not just Gen MCP-generated ones) with configurable agent backends, producing per-tool eval scores. Three uses: ingestion-pipeline evaluation step, customer-side re-evaluation with their own agent, and pre-release quality gate (e.g., OpenShift MCP Server evals before release). Key insight: customers may want to re-evaluate catalog MCPs with a different agent than the one Red Hat tested with (e.g., tested with Claude Code/Gemini, customer runs Amazon Q).
