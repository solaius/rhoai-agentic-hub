---
type: fact
title: MCP Lifecycle Operator (kubernetes-sigs/mcp-lifecycle-operator)
description: Kubernetes operator that deploys MCP servers via the MCPServer CRD — bundled with the RHOAI operator, targeting RHOAI 3.5.
timestamp: 2026-07-06
tags: [mcp-registry, lifecycle-operator, distribution]
review_after: 2026-08-05
source: ai-asset-registry/docs/knowledge-registry.md §3 (as of 2026-07-05)
---
Deployment primitive for MCP servers on Kubernetes: the `MCPServer` CRD creates a Deployment + Service. Supported servers: OpenShift, Ansible AAP, Red Hat Satellite (WIP), Red Hat Insights, Linux/RHEL (WIP). Summit demo (May 11-14, 2026) showed Catalog → Deploy → Gateway Register → ConfigMap → Gen AI Studio → Tool Execution.

Ships bundled with RHOAI operator releases rather than as a standalone OperatorHub/OLM listing. Install presents a catalog during setup (e.g., OCP MCP, ACM MCP) plus Day 2 additions. No dependency on MCP Gateway — the Gateway is downstream, for routing. Qualification is split: the OCP team owns functional qualification, the RHOAI team owns deployment/integration qualification.

Upstream code: [ref-mcp-lifecycle-operator-repo.md](/features/mcp-registry/knowledge/ref-mcp-lifecycle-operator-repo.md). Entitlement/packaging detail (RHOAI restricted use entitlement for OpenShift requirement) lives in the restricted counterpart of this entry.
