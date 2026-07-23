---
type: question
title: Skills packaging format — plugin architecture resolves format, standardization gap remains
description: RFC-0008's PackageManagerPlugin interface resolves the multi-format question (APM, LOLA, NPM, OCI coexist as plugins), but no single standard has emerged and the plugin interface is not yet merged upstream.
status: open
timestamp: 2026-07-23
tags: [skills-registry, packaging, mlflow, apm, lola, npm, oci]
source: ai-asset-registry/docs/knowledge-registry.md §13; updated from research session 2026-07-23
---

**Substantially answered** by the RFC-0008 plugin architecture and the
emerging 4-option landscape (see
[fact-skills-packaging-landscape](/features/skills-registry/knowledge/fact-skills-packaging-landscape.md)):

- **APM** (Microsoft) — git-based, must for Databricks
- **LOLA** (Red Hat) — convention-based, must for Red Hat
- **NPM/NPX** — general standard, already de facto MCP transport
- **OCI** — under discussion, strongest enterprise/air-gapped story

The `PackageManagerPlugin` interface means these are **not mutually
exclusive** — the registry governs, plugins install. This resolves the
original concern about competing formats.

**Still open**: the plugin interface itself is not merged upstream
(RFC PR #26 is still open). No single standard has emerged — risk of
fragmentation remains if the plugin architecture doesn't ship. The
Databricks MVP (`SKILL.md` + artifact store) predates the plugin design
and may evolve independently.
