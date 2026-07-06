---
type: question
title: MCP implementation UX gaps found by hands-on RHOAI 3.4 testing
description: Four concrete documentation/UX gaps Fernando Lozano hit deploying MCP on RHOAI 3.4 — docs, Workbench, Catalog prerequisites, cluster-admin.
status: open
timestamp: 2026-07-06
tags: [mcp-ecosystem, ux, documentation, gaps]
source: ai-asset-registry/docs/knowledge-registry.md §13 (as of 2026-07-05)
---
Four related open items from Fernando Lozano's practical RHOAI 3.4 testing (June 2026; see [ref-fernando-lozano-mcp-research-notes.md](/features/mcp-ecosystem/knowledge/ref-fernando-lozano-mcp-research-notes.md)):

1. **Documentation gap**: product docs reference MCP features (playground, catalog) but don't document the prerequisites that make them work (`gen-ai-aa-mcp-servers` configmap, namespace labels, MCPLO installation, service account setup) — circular references between docs/blogs/repos. Partially addressed by MCP Registry in 3.5 replacing the configmap approach.
2. **Workbench integration gap**: no documented way to call MCP servers from Python code in a RHOAI workbench; the playground's exported code doesn't work for MCP calls.
3. **Catalog prerequisite automation**: the MCP Catalog's "Deploy" button requires a ServiceAccount, ConfigMap, and ClusterRoleBinding to already exist in the namespace, but doesn't create them — by design, to prevent privilege escalation (Jaideep Rao), but with significant UX impact.
4. **Cluster-admin requirement**: currently needed for configmap patches and MCPLO installation (Erwan Granger raised this); temporary state, resolved once the registry replaces the configmap approach.
