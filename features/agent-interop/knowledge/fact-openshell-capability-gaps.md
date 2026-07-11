---
type: fact
title: OpenShell capability gaps from Kagenti
description: What OpenShell lacks that Kagenti had (or planned) -- declarative CR, GitOps, Agent Runtime Contract, token exchange at high severity; MLflow, A2A discovery, SPIFFE maturity at medium.
timestamp: 2026-07-11
tags: [agent-interop, openshell, kagenti, gaps]
features: [agent-interop, agent-registry]
review_after: 2026-09-01
source: GDoc "Strategic Assessment" section 3
---

## High severity gaps

| Capability | Kagenti status | OpenShell status | Path to resolution |
|-----------|---------------|-----------------|-------------------|
| Declarative agent representation (CR) | AgentRuntime CR with metadata, skills, MCP endpoints | Sandbox CR only (labels for discovery) | Propose enhanced Sandbox CR or layered operator CR upstream |
| GitOps-friendly deployment | AgentRuntime CR in Git, ArgoCD/Flux compatible | Imperative SDK calls; no declarative K8s-native path | Sandbox CR or operator-level CR |
| Agent Runtime Contract | Draft spec (AGENTS.md), service binding, mounted skills | Nothing; imperative SDK-only | OpenShift-specific layer; propose skill mounting via provider config |
| Token exchange | Keycloak integration for on-behalf-of flows | API key based today | Identity driver extension; Keycloak outside sandbox |
| Operator/lifecycle management | Operator actively being productized for 3.5 | No operator; blocked on architecture stabilization + multi-tenancy | Solvable once architecture settles (~1 month) |

## Medium severity gaps

| Capability | Notes |
|-----------|-------|
| MLflow/OTEL tracing | Kagenti auto-wires MLflow experiments + RBAC; OpenShell can set OTEL env vars but nothing built-in |
| Non-sandboxed agent tracking | Kagenti's AgentRuntime CR attaches to any pod; OpenShell requires every agent in a sandbox |
| A2A discovery | Kagenti fetches well-known endpoints, stores in CR status; OpenShell has no discovery mechanism |
| SPIFFE/SPIRE identity | Kagenti has full mTLS mesh; OpenShell has foundation (token grants, workload API), actively closing gap |
| Service binding | Kagenti auto-injects LLM endpoints, MCP gateway URLs; OpenShell requires manual provider YAML |

## What OpenShell has that Kagenti does not

Kernel-level isolation, hot-reloadable policies, multi-platform portability
(Podman/K8s/VM/desktop), Policy Advisor (agent-driven), credential
masking/rewriting, GPU sandbox support, TUI/CLI, Agent Sandbox SIG
integration, inference routing with credential injection.
