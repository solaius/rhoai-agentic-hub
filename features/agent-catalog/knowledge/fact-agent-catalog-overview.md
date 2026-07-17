---
type: fact
title: Agent Catalog — overview
description: The agent storefront in RHOAI AI Hub — RH-curated starter-kit templates in 3.5 (link-out, no deploy), deployment via supported images in 3.6 EA1; Kubeflow hub, sibling of the MCP and Model catalogs.
tags: [agent-catalog, roadmap, overview]
features: [agent-registry, agent-interop, mcp-catalog]
timestamp: 2026-07-16
review_after: 2026-08-31
---

The Agent Catalog is the storefront for agent examples in the RHOAI AI Hub —
the third catalog in the Model Catalog → MCP Catalog → Agent Catalog pattern
(Andrew Ballantyne, Slack 2026-06-04), built on
[kubeflow/hub](/features/mcp-catalog/knowledge/ref-kubeflow-hub-repo.md) like
its siblings. In 3.5 it surfaces the RH-curated
[agentic starter kits](/features/agent-catalog/knowledge/ref-agentic-starter-kits-repo.md)
as browsable templates whose cards link out to their GitHub repos; the goal
is pointing people at working examples of agents on the Red Hat AI stack.

## Status & roadmap

- **RHOAI 3.5 (DP)** — read-only catalog + read-only agent deployments view.
  No deploy button, no agent-card discovery, no rich detail page
  ([decision 2026-07-09](/features/agent-catalog/knowledge/decision-agent-catalog-no-deploy-35.md)).
  Metadata from each kit's agent.yaml, baked into a YAML catalog source for
  disconnected support. OpenAPI spec merged 2026-07-03 (kubeflow/hub #2907).
  Full shape: [fact-agent-catalog-35-scope](/features/agent-catalog/knowledge/fact-agent-catalog-35-scope.md).
- **RHOAI 3.6 EA1 (planned)** — agent deployment from the catalog via the
  OpenShell Go SDK, restricted to
  [supported images](/features/agent-catalog/knowledge/fact-agent-catalog-36-supported-images.md);
  shape still in discussion.
- **Agent Registry** — work starts 3.6 EA2 at the earliest, multi-release
  to DP (~3.7 EA1 directional; RHAISTRAT-1436 unscheduled, UI later —
  RHAIRFE-1313); versioned/configured agents are
  [agent-registry](/features/agent-registry/index.md) scope.

## Boundaries (routing)

- Deployment runtime, sandboxing, identity, declarative harness →
  [agent-interop](/features/agent-interop/index.md)
- Versioning/governance of deployed agents →
  [agent-registry](/features/agent-registry/index.md)
- Catalog UI pattern sibling → [mcp-catalog](/features/mcp-catalog/index.md)
- This partition: the catalog product surface — starter kits as content,
  metadata schema, discovery UX, supported-images program, release train.

## Key links

- Jira: [RHAISTRAT-1740](/features/agent-catalog/knowledge/ref-rhaistrat-1740.md) (owner: Alessio Pragliola)
- Content: [agentic-starter-kits repo](/features/agent-catalog/knowledge/ref-agentic-starter-kits-repo.md)
- Spine doc: [alignment/proposal GDoc](/features/agent-catalog/knowledge/ref-agent-catalog-alignment-gdoc.md)
- Slack: [#tmp-agent-catalog-templates-align](/features/agent-catalog/knowledge/ref-slack-tmp-agent-catalog-templates-align.md) ·
  [#forum-ai-asset-management](/features/platform/knowledge/ref-slack-forum-ai-asset-management.md)
- RHOAI architecture context: [opendatahub architecture repo](/features/platform/knowledge/ref-opendatahub-architecture-context-repo.md)
- UI prototype: https://project-navigator-rhoai-a8158d.pages.redhat.com/ai-hub/agents/catalog (VPN)
