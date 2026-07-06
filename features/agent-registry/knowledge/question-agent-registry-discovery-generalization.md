---
type: question
title: Should the agent discovery plugin interface generalize beyond agents?
description: Whether AgentDiscoveryProvider should be broadened to support other discoverable AI asset types, as the proposal's design hints.
status: open
timestamp: 2026-07-06
tags: [agent-registry, mlflow, extensibility]
source: ai-asset-registry/docs/knowledge-registry.md §13 (as of 2026-07-05)
---
[fact-agent-registry.md](/features/agent-registry/knowledge/fact-agent-registry.md) describes pluggable discovery providers via `mlflow.agent_discovery` entry points. The proposal itself notes the design is "intentionally generic enough to extend to a broader AI Artifact Registry" — open whether that generalization should actually happen, and when.
