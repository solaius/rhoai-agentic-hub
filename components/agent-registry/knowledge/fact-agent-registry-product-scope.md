---
type: fact
title: Agent Registry product scope (Adel Zaalouk, 2026-08)
description: Product scope from Adel's scoping doc -- three end behaviors (discover/register/audit), seven explicit exclusions, phased delivery (3.5/3.6/3.7+), A2A schema as metadata format, MLflow backend (third registry after MCP + Skills), catalog-as-RBAC-view, no hard Skill Registry dependency, and runtime connection model (registry stores metadata, OpenShell enforces).
timestamp: 2026-08-03
tags: [agent-registry, product-scope, a2a, mlflow, phased-delivery]
components: [agent-catalog, agent-interop, skills-registry, mcp-registry]
review_after: 2026-11-03
source: https://docs.google.com/document/d/1hqW1HrqWJw7R90irulIIAxTy-_vP7eM7g_IsNbbNmkE
---
Product scope defined in Adel Zaalouk's scoping/discussion document
([ref](/components/agent-registry/knowledge/ref-agent-registry-scoping-gdoc.md)).

## What it is

A governed inventory of what agents exist, who owns them, what they can do,
and where they're running. Answers "what do we have?" -- single pane of glass
for both agent definitions AND runtime state. Doesn't deploy agents, but
reflects deployment state (running, healthy, sandboxed, degraded).

## Three end behaviors

1. **Discover** -- single view of all registered agents; search by capability,
   owner, namespace, or skill; find existing agents before building duplicates.
2. **Register** -- via SDK, CLI, or dashboard UI; captures owner, capabilities
   (A2A schema), skills, MCP tools, sandbox policy, runtime state, lifecycle
   status (draft/active/deprecated). Template-driven onboarding as default path.
3. **Audit** -- queryable metadata linking agents to skills, tools, models, and
   policies; ownership chains; vulnerability blast radius in one query.

## Key design decisions

- **A2A Agent Card schema as metadata format** -- adopted for structure
  (name, description, capabilities, skills, auth, endpoint), not necessarily the
  full A2A runtime protocol. Industry convergence: v1.2, 150+ orgs, Linux
  Foundation.
- **MLflow backend** -- third MLflow registry after MCP Registry (RFC-0004,
  merged) and Skill Registry (RFC-0008, in review). Same governance patterns.
- **Catalog is a read-only RBAC view of the registry** -- no separate catalog
  service. See [decision](/components/agent-registry/knowledge/decision-agent-catalog-is-registry-view.md).
- **No hard dependency on Skill Registry** -- agent entries describe capabilities
  directly in A2A schema; skill references are enrichment, not prerequisite.
- **Registry vs. Deployments View** -- registry = "what agents are approved to
  exist?" (metadata, cross-cluster, lifecycle: draft/active/deprecated);
  deployments view = "what agents are running right now?" (operational, single-cluster).
  Delta between them = shadow IT.
- **Runtime connection** -- registry stores metadata (what's allowed); OpenShell
  enforces (what actually happens). Identity via existing mechanisms (K8s
  service accounts, SPIFFE, Keycloak), not a proprietary identity system.

## What we don't build

1. Agent deployment system (operators, Helm, GitOps handle this)
2. Agent observability platform (MLflow tracing + OpenTelemetry)
3. Per-agent cost management (observability/billing concern)
4. Cross-cluster federation (MVP) -- later via ARD or A2A discovery
5. Shadow IT auto-detection (MVP) -- Microsoft has this, we note the gap
6. Proprietary agent identity system -- use existing (K8s SA, SPIFFE, Keycloak)
7. Proprietary metadata format -- A2A schema is the industry standard

## Phased delivery

- **3.5 (Now)** -- rudimentary agent catalog (starter-kit templates only);
  define agent metadata schema (A2A-based); ship agent templates producing
  pre-registered agents; MLflow MCP Registry ships (establishing pattern).
- **3.6 (Next)** -- Agent Registry RFC to MLflow upstream; Agent Registry in
  RHOAI (register, search, lifecycle, RBAC); dashboard integration for agent
  inventory (browse agents, view Agent Cards, see linked skills/tools);
  sandboxing UI + runtime connection foundation; template-driven onboarding
  as default.
- **3.7+ (Later)** -- shadow IT visibility (surface unregistered agents);
  policy enforcement integration (registry metadata drives runtime); cross-cluster
  agent discovery (A2A or ARD); federation across clusters and clouds.

## Connection to other registries

| Registry | Answers | Backend |
|----------|---------|---------|
| Agent Registry | "What agents exist and what can they do?" | MLflow (WIP RFC) |
| Skill Registry | "What expertise is available?" | MLflow (RFC-0008) |
| MCP Registry | "What tools are governed?" | MLflow (RFC-0004) |

Agent entries reference skills by Skill Registry ID. Cross-referencing
("which agents carry skill X?", "which agents affected by CVE Y?") is a
registry query. Both registries use the same governance patterns, RBAC model,
and dashboard surface.
