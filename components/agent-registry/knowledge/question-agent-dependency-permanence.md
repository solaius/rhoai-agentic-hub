---
type: question
title: Dependency permanence -- the npm/left-pad problem for live agent dependencies
description: If Agent X depends on a shared skill or MCP server owned by another team, deprecation or schema changes break Agent X in production; registries must enforce immutable versioning or dependency snapshotting while dependencies are in active use.
status: open
timestamp: 2026-08-03
tags: [agent-registry, dependencies, skills-registry, mcp-registry]
components: [skills-registry, mcp-registry]
source: https://docs.google.com/document/d/1hqW1HrqWJw7R90irulIIAxTy-_vP7eM7g_IsNbbNmkE (Jiri Danek comment)
---
Raised by Jiri Danek: agents reference skills and MCP tools from their
respective registries, but "who ensures v1.2.3 is still up tomorrow?" If
Agent X relies on a shared Jira MCP Server owned by another team, and that
team deprecates it or alters its schema, Agent X dies in production.

The A2A schema and MLflow backend define metadata but don't guarantee runtime
permanence. This recreates the NPM dependency tree, but with live, stateful
services instead of static code libraries.

Proposed fix (Jiri): registries must enforce immutable versioning -- if an
agent depends on Skill v1.2.3, that skill definition cannot be deleted or
mutated as long as the agent is active. Also need a strategy for "vendor
locking" dependencies (snapshotting skills/tools).

Open sub-questions:
- Should the registry enforce a "pinned dependency" model where active agents
  block deprecation of their dependencies?
- How does this interact with the Skill Registry's lifecycle (draft/active/deprecated)?
- Is snapshotting (copying the dependency definition at registration time) viable
  for live services vs. static definitions?
- How do other registries handle this? (npm has immutable published versions;
  container registries have immutable digests)
