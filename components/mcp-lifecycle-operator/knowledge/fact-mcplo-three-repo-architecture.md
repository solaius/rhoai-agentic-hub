---
type: fact
title: MCPLO three-repo architecture pattern
description: RHOAI integrates the lifecycle operator through three repos -- upstream (kubernetes-sigs), module operator (opendatahub-io), and parent operator (opendatahub-io) -- with a two-tier image pattern.
timestamp: 2026-07-11
tags: [mcp-lifecycle-operator, architecture, rhoai]
review_after: 2026-09-11
source: architecture research 2026-07-11; opendatahub-operator source code
---

The MCPLO integration into RHOAI follows a three-repo pattern:

1. **kubernetes-sigs/mcp-lifecycle-operator** -- upstream SIG Apps
   operator that reconciles MCPServer CRs (the deployment primitive)
2. **opendatahub-io/mcp-lifecycle-module-operator** -- ODH module
   wrapper that reconciles MCPLifecycleOperator CRs and deploys the
   upstream controller as an operand
3. **opendatahub-io/opendatahub-operator** -- parent operator that
   embeds the module handler in the DSC (DataScienceCluster) CR as
   the `mcplifecycleoperator` component

Two-tier image pattern:
- Module operator image (RELATED_IMAGE_ODH_MCP_LIFECYCLE_MODULE_OPERATOR_IMAGE)
  runs in RHOAI namespace
- Lifecycle operator image (RELATED_IMAGE_ODH_MCP_LIFECYCLE_OPERATOR_IMAGE)
  is the actual MCPLO controller deployed by the module operator

The DSC integration provides a Managed/Removed toggle per component.
Manifest sources are pinned to commit SHAs in get_all_manifests.sh
(ODH branch: main, RHOAI branch: rhoai-3.5).

The downstream fork (openshift/mcp-lifecycle-operator, 264 commits)
adds CI/build infrastructure (Dockerfile.ocp, .ci-operator.yaml,
.tekton/ pipelines) but core operator code tracks upstream.
