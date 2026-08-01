---
type: fact
title: ROSA/OCP MCP Server — Customer Guidance
description: Point customers to the Red Hat build of the Kubernetes MCP server (not upstream) for connecting AI tools to ROSA or any OCP cluster.
timestamp: 2026-07-30
tags: [mcp-ecosystem, rosa, customer-guidance]
source: Slack — Calum Murray confirming guidance for Jason Mitsky's customer query
---
For customers connecting AI tools (Claude, etc.) to ROSA or any OpenShift
cluster via MCP, recommend the **Red Hat build** of the Kubernetes MCP server:

- **Red Hat docs**: https://docs.redhat.com/en/documentation/openshift_container_platform/4.22/html/ai_applications/mcp-server

The upstream repos (`containers/kubernetes-mcp-server`,
`openshift/openshift-mcp-server`) are the same underlying project, but
customers should use the supported Red Hat build.

The server works with any OpenShift cluster including ROSA — it connects via
standard kubeconfig. No ROSA-specific configuration is needed beyond having a
valid kubeconfig pointing to the cluster.
