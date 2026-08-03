---
type: decision
title: Agent catalog is a read-only RBAC view of the registry
description: The agent catalog is not a separate service -- it is a read-only RBAC view of the Agent Registry, same pattern as Skills (one system, two RBAC levels -- developers browse, platform teams manage).
timestamp: 2026-08-03
decided: 2026-08-03
tags: [agent-registry, agent-catalog, architecture]
components: [agent-catalog]
source: https://docs.google.com/document/d/1hqW1HrqWJw7R90irulIIAxTy-_vP7eM7g_IsNbbNmkE
---
## Context

The Agent Registry scoping doc establishes the relationship between the agent
catalog and the agent registry. The question was whether the agent catalog
would be a separate service (as it is today for starter-kit templates in 3.5)
or a view of the registry.

## Decision

The agent catalog is a read-only RBAC view of the Agent Registry. Same pattern
as skills: one system, two RBAC levels. Developers browse (catalog view),
platform teams manage (registry view). No separate catalog service.

This means the current 3.5 agent catalog (starter-kit templates, link-out only)
is a transitional state. When the Agent Registry ships in 3.6, the catalog
becomes its read surface.

## Consequences

- The agent-catalog component's scope narrows to the catalog UX/experience
  (what developers see), not a separate backend.
- Registration, lifecycle, and RBAC are registry concerns, not catalog concerns.
- The same model applies across all three catalogs: skills catalog = Skills
  Registry view, MCP catalog = MCP Registry view, agent catalog = Agent
  Registry view.
- The 3.5 starter-kit catalog is a stepping stone, not the long-term architecture.
