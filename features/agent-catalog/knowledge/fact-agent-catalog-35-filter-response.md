---
type: fact
title: Agent catalog 3.5 filter_options real data shape
description: Real filter_options endpoint response as of ~2026-07-11 -- 14 agents (templates + harnesses), 11 frameworks, 2 deployment models (config-driven, flow-import), 16 labels; harness kits (OpenCode, Claude Code, OpenClaw) appear alongside template kits.
timestamp: 2026-07-23
tags: [agent-catalog, 3.5, filter-options, metadata]
review_after: 2026-09-01
---
Alessio Pragliola posted the real (non-mock) filter_options response in the
[#openshift-ai-hub-devs thread](/features/agent-catalog/knowledge/ref-slack-ai-hub-devs-filter-options-thread.md).

**Agents** (14): A2A LangGraph <-> CrewAI, AutoGen Agent (MCP), Claude Code,
CrewAI WebSearch Agent, Google ADK Agent, LangGraph Agentic RAG Agent,
LangGraph Human-in-the-Loop Agent, LangGraph ReAct Agent, LangGraph ReAct
Agent with Database Memory, Langflow Simple Tool Calling Agent, LlamaIndex
WebSearch Agent, OpenAI Responses Agent, OpenClaw, OpenCode.

**Frameworks** (11): a2a, autogen, claude-code, crewai, google-adk, langflow,
langgraph, llamaindex, openclaw, opencode, vanilla_python.

**Deployment models** (2): config-driven, flow-import.

**Labels** (16): a2a, cli, coding-agent, database, gateway,
human-in-the-loop, low-code, mcp, memory, multi-agent, no-framework, rag,
react, tool-calling, vector-store, web-search.

Notable: no `models` or `protocol` filters in the real response (consistent
with PR #2907 demoting these to untyped customProperties -- see
[upstream schema divergence](/features/agent-catalog/knowledge/fact-agent-catalog-upstream-schema.md)).
The `deploymentModel.string_value` filter is new -- not in the original mock.
