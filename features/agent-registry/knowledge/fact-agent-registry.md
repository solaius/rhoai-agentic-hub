---
type: fact
title: Agent Registry (upstream proposal)
description: Post-deployment registry for live, running agents — identity, health, discovery, trust — as a draft MLflow RFC Peter Double is taking over.
timestamp: 2026-07-06
tags: [agent-registry, mlflow, proposal]
review_after: 2026-08-05
source: ai-asset-registry/docs/knowledge-registry.md §3 (as of 2026-07-05)
---
Draft upstream proposal (Varsha Prasad Narsing, 2026-02-16; Peter Double now taking over) for a post-deployment-only registry: agents as live services with network endpoints, not pre-deployment artifacts (that's a separate, deferred proposal). Governs identity, URL/endpoint, protocol (openai-compatible/a2a/custom), skills, health status, trust verification (SPIFFE/SPIRE), and lifecycle state (ACTIVE → UNHEALTHY → STALE → REMOVED — simpler than MCP Registry's multi-track governance since it's runtime-focused).

Architecture: pluggable discovery providers via `mlflow.agent_discovery` entry points (poll/watch/webhook sync), with reference plugins for Kubernetes (via kagenti AgentCard CRD), Docker, Consul, and Static. Optional auto-sync into the Gateway as endpoints for tracing/routing/fallback. Key distinction from MCP Registry: this governs live services with runtime state, not static assets with multi-track governance — complementary, not overlapping.

See [ref-mlflow-agent-registry-proposal-branch.md](/features/agent-registry/knowledge/ref-mlflow-agent-registry-proposal-branch.md) for the full proposal.
