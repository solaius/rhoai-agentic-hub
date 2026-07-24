---
type: fact
title: Skills Catalog 3.6 scope -- browse-only TP with pre-loaded content
description: Research-backed 3.6 scope recommendation -- read-only browse/search with 15-20 pre-loaded curated skills; installation automation and registry integration deferred to 3.7+; matches MCP Catalog DP-to-TP and Agent Catalog DP link-out precedents.
timestamp: 2026-07-23
tags: [skills-catalog, scope, 3.6, recommendation]
features: [skills-catalog]
review_after: 2026-09-23
source: skills-catalog research 04-requirements (2026-07-23)
---

Based on the 4-lens research sweep (2026-07-23), the recommended 3.6
scope is a **read-only browse/search experience** with pre-loaded
content. This matches the MCP Catalog DP-to-TP progression and the
Agent Catalog DP link-out pattern.

**Must ship (3.6 TP)**: browse/search/filter UI, skill detail cards,
15-20 pre-loaded Red Hat skills, Git-backed metadata (YAML source),
trust tier badges, ConfigMap disconnected import, category/tag
filtering.

**Defer to 3.7+**: one-click install to harness, automated install
commands (npx, APM, LOLA), partner feed ingestion, telemetry, semantic
search, registry integration (pull-to-register), quality scores.

**Feasibility**: 6-7 two-week sprints to October 23 code freeze fits
the low end of the 6-9 sprint RHAISTRAT-1780 estimate. 90% confidence
(Bill Murdock) if scope stays here. Pattern reuse from existing
catalogs reduces greenfield risk.

**Existential risk**: RHAISTRAT-1940 (pre-loaded content) has no PM
assigned. Without seed content, the catalog ships empty and has
negative value.
