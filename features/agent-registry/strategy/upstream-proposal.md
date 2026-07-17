---
title: Proposal: Post-Deployment Agent Registry with Pluggable Discovery
description: Varsha Prasad Narsing's upstream MLflow RFC starting point for a post-deployment agent registry with pluggable discovery backends.
source: ai-asset-registry/agents/agent-registry-upstream-proposal.md (as of 2026-07-05)
timestamp: 2026-07-06
review_after: 2026-08-05
---

# Proposal: Post-Deployment Agent Registry with Pluggable Discovery

> Caveat 2026-07-16: the abstract discovery design below survives, but the "Reference Plugin: Kubernetes with kagenti" section describes a dead substrate (kagenti removed from the RH roadmap 2026-07-10) — see [research/09-architecture](/features/agent-registry/research/09-architecture.md) for the post-kagenti sources; the lifecycle model also needs a SUSPENDED state. The branch has had no commits since 2026-04-23.

> **Source**: [varshaprasad96/mlflow (branch: spike/gateway)](https://github.com/varshaprasad96/mlflow/blob/spike/gateway/proposals/agent-registry-discovery.md)
> **Author**: Varsha Prasad Narsing
> **Date**: 2026-02-16
> **Status**: Draft — starting point for upstream MLflow RFC
> **Scope**: Post-deployment agent registry only (pre-deployment artifacts deferred to separate proposal)

**Note**: This proposal focuses on agents as the first discoverable artifact type. The pluggable discovery design is intentionally generic enough to extend to a broader "AI Artifact Registry" in the future.

---

## Motivation

MLflow provides registries for prompts (Prompt Registry) and models (Model Registry), but has no registry for agents — autonomous AI systems deployed and running in production environments.

Organizations deploy agents across diverse infrastructure (Kubernetes, cloud services, on-premise). Today there is no unified way to:

1. **Discover** agents running in these environments
2. **Catalog** them in a central registry with metadata (tools, protocol, health)
3. **Route** requests to them through the AI Gateway with tracing, fallbacks, and traffic splitting
4. **Monitor** their availability and lifecycle (healthy, unhealthy, stale, removed)

---

## Goals

1. Central, dynamic registry of live agents across any environment
2. Pluggable discovery backends (Kubernetes, Docker, Consul, static files, etc.) — inspired from MLflow plugin mechanism
3. Multiple sync mechanisms: polling, watching, and webhooks
4. Track agent lifecycle (active, unhealthy, stale, removed)
5. Integrate with existing AI Gateway for routing and tracing
6. Follow MLflow's established plugin patterns (entry points, registries)

## Non-Goals

1. Pre-deployment agent registry (versioning agent definitions/images) — follow up
2. Agent execution or orchestration — MLflow discovers and routes, not runs
3. Replacing existing service meshes or service discovery — MLflow aggregates from them

---

## Domain Model

### What Is an "Agent" in This Registry?

An agent is a live, deployed service that:
- Accepts requests (chat messages, task instructions, tool calls)
- Acts autonomously (reasons, calls tools, produces responses)
- Runs somewhere in an environment (K8s pod, Docker container, cloud service, bare metal process)
- Is reachable via a network URL

An agent is **not** a model, a prompt, or an artifact. It is a running process with runtime state.

### Core Entity: `Agent`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `agent_id` | `string` | Yes (auto) | Unique identifier, e.g. `"ag-<uuid>"` |
| `name` | `string` | Yes | Unique human-readable name (URL-safe) |
| `description` | `string` | No | Human-readable description |
| `url` | `string` | Yes | Network endpoint for the agent |
| `external_url` | `string` | No | Externally routable URL (when `url` is cluster-internal) |
| `protocol` | `enum` | Yes | API protocol: `openai-compatible`, `a2a`, `custom` |
| `skills` | `list[AgentSkill]` | No | Structured capabilities the agent exposes |
| `version` | `string` | No | Agent version (informational) |
| `health_check_path` | `string` | No | HTTP path for health checks |
| `source_plugin` | `string` | Yes | Which discovery plugin registered this agent |
| `status` | `enum` | Yes (auto) | Lifecycle state: `ACTIVE`, `UNHEALTHY`, `STALE`, `REMOVED` |
| `verified` | `bool` | No | Cryptographic identity verification status |
| `identity` | `string` | No | Verified identity claim (e.g. SPIFFE ID) |
| `trust_domain` | `string` | No | Trust domain for organizational boundary filtering |
| `metadata` | `dict[string, string]` | No | Arbitrary key-value pairs from source environment |
| `last_seen_at` | `timestamp` | Yes (auto) | Last time discovery plugin confirmed this agent |
| `last_health_check_at` | `timestamp` | No | Last health check time |
| `created_at` | `timestamp` | Yes (auto) | First registration time |
| `updated_at` | `timestamp` | Yes (auto) | Last modification time |

### AgentSkill

Structured capability aligned with A2A protocol's skill model (used by kagenti):

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | `string` | Yes | Unique skill identifier |
| `name` | `string` | Yes | Human-readable name |
| `description` | `string` | No | What this skill does |
| `tags` | `list[string]` | No | Keywords/categories for filtering |
| `examples` | `list[string]` | No | Example prompts/scenarios |
| `input_modes` | `list[string]` | No | Accepted media types |
| `output_modes` | `list[string]` | No | Produced media types |
| `parameters` | `list[SkillParameter]` | No | Parameters the skill accepts |

### Agent Lifecycle States

```
discovered by plugin
       │
       ▼
┌───────────────────────────────┐
│            ACTIVE             │  ◄── discovered and healthy
└───────┬───────────────┬───────┘
        │               │
health check fails    not seen in discovery
        │               │
        ▼               ▼
┌───────────────┐  ┌───────────────┐
│  UNHEALTHY    │  │    STALE      │  ◄── grace period (configurable)
└───────┬───────┘  └───────┬───────┘
        │                  │
health recovers      grace period expires
        │                  │
        ▼                  ▼
┌───────────────┐  ┌───────────────┐
│    ACTIVE     │  │   REMOVED     │
└───────────────┘  └───────────────┘
```

| State | Meaning |
|-------|---------|
| `ACTIVE` | Discovered and passing health checks |
| `UNHEALTHY` | Known but failing health checks |
| `STALE` | Not reported by source plugin within grace period |
| `REMOVED` | Gone — grace period expired or explicit DELETE |

---

## Architecture

### Discovery Plugin System

```
┌─────────────────────────────────────────────────────────────┐
│                     MLflow Server                           │
│                                                             │
│  ┌───────────────────────────────────────────────────────┐  │
│  │              Agent Registry (DB-backed)               │  │
│  └────────────────────────▲──────────────────────────────┘  │
│                           │                                  │
│           ┌───────────────┼───────────────┐                  │
│           │               │               │                  │
│  ┌────────┴─────┐ ┌──────┴──────┐ ┌──────┴──────────┐      │
│  │  Poll Sync   │ │ Watch Sync  │ │ Webhook Endpoint │      │
│  │  (Huey task) │ │ (bg thread) │ │ (REST API)       │      │
│  └──────┬───────┘ └──────┬──────┘ └──────┬───────────┘      │
│         │                │               │                   │
│  ┌──────┴────────────────┴───────────────┴───────────┐      │
│  │          Agent Discovery Plugin Registry          │      │
│  └──────┬─────────┬──────────┬──────────┬────────────┘      │
│         │         │          │          │                    │
└─────────┼─────────┼──────────┼──────────┼────────────────────┘
          │         │          │          │
     ┌────┴───┐ ┌──┴───┐ ┌───┴───┐ ┌───┴──────┐
     │  K8s   │ │Docker│ │Consul │ │  Static  │
     │ plugin │ │plugin│ │plugin │ │  plugin  │
     └────────┘ └──────┘ └───────┘ └──────────┘
```

### Discovery Provider Interface

- **Entry point group**: `mlflow.agent_discovery`
- **Abstract base class**: `AgentDiscoveryProvider`
- **Required method**: `discover(filters)` → `list[DiscoveredAgent]`
- **Optional method**: `watch(filters)` → `Iterator[AgentEvent]`
- **Capabilities**: `POLL`, `WATCH`, `WEBHOOK`

### Reference Plugin: Kubernetes with kagenti

The Kubernetes plugin uses kagenti-operator's `AgentCard` CRD as the source of truth:
1. kagenti auto-discovers labeled workloads (`kagenti.io/type=agent`)
2. kagenti fetches `/.well-known/agent-card.json`, verifies JWS signatures, caches in AgentCard status
3. MLflow plugin reads reconciled AgentCard CRs (does not re-fetch/re-verify)

**Three integration architectures**:
- **Option A (Pull)**: MLflow polls/watches AgentCard CRDs directly via K8s API
- **Option B (Push)**: kagenti pushes events to MLflow's webhook endpoint (extends existing MLflowReconciler)
- **Option C (Hybrid)**: Push for real-time + poll for consistency

### Database Schema

Dedicated `agent_registry` table (not reusing ModelVersion with tags):
- Core fields: agent_id, name, description, url, external_url, protocol, skills (JSON), metadata (JSON)
- Trust fields: verified, identity, trust_domain
- Lifecycle fields: status, source_plugin, last_seen_at, last_health_check, created_at, updated_at
- Indexes on: name, status, source_plugin, verified, trust_domain

### Python Client API

```python
import mlflow

# List/filter agents
agents = mlflow.agents.list_agents(status="ACTIVE", source="kubernetes")
agents = mlflow.agents.list_agents(verified=True, trust_domain="example.org")
agents = mlflow.agents.list_agents(skill_tags=["code-search"])

# Get specific agent
agent = mlflow.agents.get_agent("coding-agent")

# Trigger on-demand discovery
newly_found = mlflow.agents.discover(source="kubernetes", filters={"namespace": "agents"})

# Invoke via Gateway
response = mlflow.agents.invoke("coding-agent", messages=[...])
```

### Gateway Integration

Discovered agents can be auto-bridged as Gateway endpoints (opt-in via `MLFLOW_AGENT_GATEWAY_AUTO_SYNC=true`):
- Agent → Gateway Endpoint (tracing, routing, fallback for free)
- REMOVED agents → deactivated endpoints
- Prefer routing to `verified=true` agents when multiple match

---

## Compatibility

- No breaking changes — new, opt-in subsystem
- Database migration: one new `agent_registry` table via Alembic
- Existing registries (Prompt, Model) untouched
- Gateway: agents bridged as `mlflow-model-serving` provider endpoints
