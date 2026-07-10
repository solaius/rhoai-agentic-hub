---
type: reference
title: opendatahub-io/architecture-context — THE RHOAI architecture repo
description: Per-release architecture snapshots for all of RHOAI (~48 components) — component summaries, Mermaid/C4 diagrams, build metadata; agent entry point AGENT_USAGE.md. Standing context for every feature.
resource: https://github.com/opendatahub-io/architecture-context
tags: [platform, architecture, github, standing-context]
timestamp: 2026-07-10
review_after: 2026-09-10
source: repo README, fetch-verified 2026-07-10; originally filed from ai-asset-registry/docs/knowledge-registry.md §12
---

The RHOAI architecture source of truth for humans and agents — an
automated pipeline that "clones ODH/RHOAI component repositories,
generates per-component architecture summaries using Claude agents,
aggregates them into platform-level documents, and produces Mermaid/C4
diagrams" (README). Actively maintained: v4.0.0 released 2026-05-15.

What's inside: versioned snapshots per platform release (e.g.
`rhoai-3.4-ea.1`) covering ~17 manifest-managed components + the
operator + ~31 adjacent repos; per-component markdown summaries;
Mermaid diagrams (component, dataflow, dependencies, RBAC,
security/network); C4 context diagrams (DSL); build metadata (OCP
versions, CPU architectures, Konflux image topology).

How to use it:

- Agents start at `AGENT_USAGE.md`, then navigate `architecture/` to
  the snapshot matching the release in question.
- Architecture questions in ANY feature route here first —
  `hub.research` hands the matching snapshot to every lens agent as
  standing context, and new feature overview facts link this entry.
- The recorded "why" behind these architectures lives in the companion
  [ADR repo](/features/platform/knowledge/ref-odh-architecture-decision-records-repo.md).

Cross-cutting by design — routed to `platform`.
