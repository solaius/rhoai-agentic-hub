---
type: fact
title: MCP Lifecycle Operator overview
description: Kubernetes operator (kubernetes-sigs) providing declarative MCPServer CRD for deploying and managing MCP servers — bundled in RHOAI operator for 3.5, used by MCP Catalog and MCP Registry.
timestamp: 2026-07-11
tags: [mcp-lifecycle-operator, deployment, kubernetes-sigs, rhoai-3.5]
features: [mcp-catalog, mcp-registry, mcp-gateway]
review_after: 2026-09-11
source: upstream README, blog post (May 28, 2026), FAQ GDoc, user journey GDoc
---

The MCP Lifecycle Operator is a Kubernetes-native operator under
kubernetes-sigs (SIG Apps) that provides a declarative API to deploy,
manage, and safely roll out MCP servers. Core abstraction: the
`MCPServer` custom resource (API group `mcp.x-k8s.io/v1alpha1`).

**What it does:** When an MCPServer resource is created, the operator
automatically provisions a Deployment, Service, and NetworkPolicy with
security-hardened defaults (non-root, read-only filesystem, dropped
capabilities, seccomp RuntimeDefault). It validates referenced
ConfigMaps/Secrets before rollout, injects a default readiness probe,
and performs an MCP protocol-level handshake to verify the server is
actually serving MCP before marking it Ready.

**Productization:** Created by the OCP team, scheduled for productization
in the RHOAI operator for RHOAI 3.5. Ships bundled with RHOAI operator
releases -- not available as a standalone OperatorHub/OLM listing. The
upstream project is public and can be used independently by customers
who want to BYO MCP servers on Kubernetes.

**Relationships:**
- MCP Catalog requires the MCPServer CRD to deploy servers (deploy
  button disabled without it)
- MCP Registry will integrate for governance (identity, lifecycle state)
- MCP Gateway is downstream -- used for routing after deployment, no
  install dependency
- OLS (OpenShift Lightspeed) will transition to using MCPLO-deployed
  OCP MCP servers (currently uses its own internal MCP server)

**Qualification:** Joint responsibility -- OCP team owns functional
qualification (server deployment, discovery, management), RHOAI team
owns deployment/integration qualification (rollout via RHOAI operator,
prerequisites satisfied).

Current version: v0.2.0 (alpha). API status: v1alpha1 (subject to
change).

Key links:
- Upstream: [ref-upstream-repo.md](/features/mcp-lifecycle-operator/knowledge/ref-upstream-repo.md)
- RHOAI architecture context: [ref-opendatahub-architecture-context-repo.md](/features/platform/knowledge/ref-opendatahub-architecture-context-repo.md)
- RHOAI Outcome: [ref-rhaistrat-1339-rhoai-outcome.md](/features/mcp-lifecycle-operator/knowledge/ref-rhaistrat-1339-rhoai-outcome.md)
- TP Productization: [ref-rhaistrat-1773-tp-productization.md](/features/mcp-lifecycle-operator/knowledge/ref-rhaistrat-1773-tp-productization.md)
