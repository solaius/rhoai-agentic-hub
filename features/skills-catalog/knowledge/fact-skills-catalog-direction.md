---
type: fact
title: Skills Catalog direction -- Kubeflow, Git-backed, disconnected image
description: Catalog direction established 2026-07-23 -- Kubeflow hub surface, GitHub repos as skill source, downstream image build for disconnected, metadata labels for grouping (no bundling), admin-manages/user-browses.
timestamp: 2026-07-23
tags: [skills-catalog, direction, kubeflow, disconnected]
features: [skills-catalog]
review_after: 2026-09-23
source: three intake meetings 2026-07-23
---

Direction agreed across AgentDev priority call, Ramesh/Peter 1:1, and
Skills Registry/Catalog meeting (2026-07-23):

**Surface**: Kubeflow hub in odh-dashboard, same pattern as MCP
catalog, model catalog, and agent catalog.

**Source of truth**: skills live in Git repos (GitHub). Catalog indexes
metadata and provides searchable UI. No artifact storage by AI Hub.

**Identity**: Git URL + commit/version uniquely identifies a skill. No
registry-generated ID at the catalog level.

**Disconnected/air-gapped**: downstream image build pulls bare GitHub
repos and builds a directory of skills. ConfigMap-based offline import.
Air-gapped uses internal Git server.

**Grouping**: labels/categories at the presentation layer. No bundling
concept in the catalog -- repos are the natural grouping unit.

**Access model**: admin-manages (pre-loads Red Hat and partner skills),
user-browses (links to skills, eventually install commands). Initially
read-only for users; install features need separate STRAT.

**Pre-loading**: Red Hat skills and partner skills pre-loaded at
delivery time. Customer admins can add organization-approved skills.
Without pre-loaded content, catalog launches empty (see RHAISTRAT-1940).
