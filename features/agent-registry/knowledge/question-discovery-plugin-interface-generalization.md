---
type: question
title: Should the agent discovery plugin interface generalize beyond agents?
description: Open question on whether AgentDiscoveryProvider (poll/watch/webhook) should become a generic discoverable-asset-type interface rather than agent-specific.
status: open
timestamp: 2026-07-06
tags: [agent-registry, mlflow, plugin-architecture]
source: ai-asset-registry/docs/knowledge-registry.md §7 (as of 2026-07-05)
---
The agent registry's discovery architecture ([fact-agent-registry.md](/features/agent-registry/knowledge/fact-agent-registry.md)) uses a pluggable `AgentDiscoveryProvider` interface (poll/watch/webhook sync) via `mlflow.agent_discovery` entry points. Open question: should this interface be generalized to support other discoverable asset types beyond agents, rather than being agent-specific? Relevant to the same genericization direction seen in Kubeflow Hub's PR #2219 (see [fact-model-registry-kubeflow-hub.md](/features/platform/knowledge/fact-model-registry-kubeflow-hub.md)).
