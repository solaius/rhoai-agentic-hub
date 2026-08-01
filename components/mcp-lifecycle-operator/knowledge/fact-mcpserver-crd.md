---
type: fact
title: MCPServer CRD technical details
description: The MCPServer custom resource (mcp.x-k8s.io/v1alpha1) -- spec fields, auto-created resources, status conditions, and discovery URL pattern.
timestamp: 2026-07-11
tags: [mcp-lifecycle-operator, crd, api]
review_after: 2026-09-11
source: upstream README v0.2.0, blog post (May 28, 2026)
---

API group: `mcp.x-k8s.io/v1alpha1`, Kind: `MCPServer`.

**Spec fields:**
- `source`: container image reference (`type: ContainerImage`,
  `containerImage.ref: <OCI image>`)
- `config`: port, command-line arguments, storage mounts
  (ConfigMaps/Secrets mounted at specified paths)
- `runtime.security`: service account name for RBAC scoping

**Auto-created resources** (same name as the MCPServer):
- Deployment (security-hardened: non-root, read-only rootfs, all
  capabilities dropped, seccomp RuntimeDefault)
- Service (cluster-internal discovery)
- NetworkPolicy
- Pods labeled `mcp-server=<name>`

**Status fields:**
- `deploymentName`, `serviceName`
- `address.url` -- cluster-internal MCP endpoint
  (pattern: `http://<name>.<namespace>.svc.cluster.local:<port>/mcp`)
- Conditions: `Accepted` (reason: Valid) and `Ready` (reason: Available)

**Validation behavior:**
- If referenced ConfigMap/Secret doesn't exist, sets Accepted=False
  with a clear error message instead of creating a broken deployment
- Injects default TCP socket readiness probe if none specified
- Performs MCP protocol-level handshake beyond TCP health check

`kubectl get mcpservers` shows: READY, ACCEPTED, IMAGE, PORT, ADDRESS.

Prerequisites: Kubernetes v1.28+.
