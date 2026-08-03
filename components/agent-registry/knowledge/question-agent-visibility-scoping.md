---
type: question
title: Should the registry enforce visibility scopes to prevent accidental coupling?
description: Global agent discoverability risks accidental coupling (Bazel/Google3 analogy) -- Team B depends on Team A's brittle agent, Team A changes it, Team B breaks; registry may need explicit visibility scopes (team-local/org-wide/public) per agent.
status: open
timestamp: 2026-08-03
tags: [agent-registry, discovery, governance, rbac]
source: https://docs.google.com/document/d/1hqW1HrqWJw7R90irulIIAxTy-_vP7eM7g_IsNbbNmkE (Jiri Danek comment)
---
Raised by Jiri Danek, citing Google's internal monorepo (Google3) and Bazel's
strict visibility attributes. Making everything globally visible by default
is a trap: if Team A builds a highly specific, brittle "PDF Extraction Agent"
and it's globally discoverable, Team B will depend on it. When Team A changes
it for their own use case, Team B breaks.

Proposed fix (Jiri): the registry needs explicit visibility scopes, e.g.
`visibility: ["team-local", "org-wide", "public"]`. Discovery is good, but
discovering an agent you shouldn't rely on creates accidental coupling.

Open sub-questions:
- Does RBAC (namespace-scoped access) already solve this, or is visibility
  a separate concept from access control?
- How do Kubernetes namespaces map to visibility scopes?
- Should the default be "team-local" (opt-in to wider visibility) or
  "org-wide" (opt-in to restriction)?
- How does this interact with the catalog-as-view model -- does the catalog
  only show agents visible to the browsing user's scope?
