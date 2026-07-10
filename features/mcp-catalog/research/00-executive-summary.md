---
title: "MCP Catalog research — executive summary"
description: Living synthesis of the mcp-catalog research series — July 2026 upstream + competitive run; headline findings, two-way gap list, and the questions the run raised for TP (3.6 EA1) and GA (3.6 Stable, Nov 2026).
timestamp: 2026-07-09
review_after: 2026-09-15
---

# MCP Catalog research — executive summary

**Series** (run 2026-07-09, standard depth + adversarial verification;
lenses scoped by owner to upstream + competitive):

- [01 — Upstream: MCP catalog/registry ecosystem](01-upstream-mcp-catalog-registry.md)
- [02 — Competitive: enterprise MCP catalogs](02-competitive-mcp-catalogs.md)

**Lens gaps** (not run, by owner scoping): landscape, architecture,
requirements — retry with `hub.research mcp-catalog <lens>`.

## Headline findings

1. **Kubeflow Hub (RH-driven, ex-model-registry) shipped an MCP Catalog
   (v1alpha1) in Feb 2026** — almost certainly the RHOAI MCP Catalog's
   upstream implementation, but no doc states the relationship, and the
   repo handed over at intake (kubeflow/mcp-server) turned out to be an
   unrelated Trainer-ops MCP server. Confirm + document (question filed).
2. **The official MCP registry is big but immature**: ≥36K total / ≥10K
   latest server records (live pull, 2026-07-09) yet still preview with
   the API frozen at v0.1, minimal moderation by design, and governance
   now under the Linux Foundation's Agentic AI Foundation. Upstream
   expects vendor catalogs to be **subregistries** (OpenAPI spec +
   namespaced `_meta`) — RH has no stated federation posture (question
   filed).
3. **Spec churn hits during the TP→GA window**: the largest-ever MCP
   revision finalizes 2026-07-28 (stateless HTTP, handshake removed,
   mandatory `server/discover`, DCR deprecated). GA (Nov) certifies
   servers ~4 months after the flip with no stated compatibility-matrix
   policy (question filed).
4. **The enterprise field roughly doubled since the July-6 snapshot**:
   AWS Agent Registry, Google Cloud API Registry, IBM Agentic Control
   Plane, Salesforce/MuleSoft Agent Registry, Kong MCP Registry all
   entered; Docker moved to signed composable OCI catalogs + org-wide
   MCP governance; Databricks extended Unity governance to MCP with
   content-aware per-action policies. The "nobody owns enterprise
   governance end-to-end" differentiator is eroding — RH's remaining
   unmatched card is the shipped single-platform
   discover→deploy→connect→consume chain plus hybrid/multi-cloud
   open-source positioning.
5. **ToolHive is coopetition, not just a competitor**: Red Hat
   co-maintains it (confirmed on both companies' sites), it runs on
   OpenShift, and its registry federates multi-source catalogs —
   overlapping MCPLO/Catalog. Needs a stated channel story.
6. **Smithery is no longer "largest"** — PulseMCP (21.5K, verified) and
   MCP.so (~21K) lead; the official registry itself now rivals the
   aggregators in raw scale.

## Gaps to close (they-have-we-lack, shortlist)

Composable/signed private catalogs (Docker) · content-aware per-action
policy (Databricks) · semantic search + approval workflow over private
catalogs (AWS) · SaaS-hosted remote-server supply tier
(Salesforce/MuleSoft) · loud spec-aligned OAuth posture (Kong) ·
federation with the official registry (upstream expectation).

## What still holds

Three-way Directory/Registry/Enterprise-Platform framing (as analysis,
not market vocabulary) · RH's integrated-chain advantage · governance
gap vs pure directories · UBI+scanning trust baseline (now table
stakes, not differentiator).

## Questions this run filed

- Kubeflow Hub ↔ RHOAI MCP Catalog relationship (confirm + document).
- Federation posture vs the official registry (aggregator / subregistry
  / none) for TP.
- Spec-version compatibility policy for GA certification.

Existing open question informed (not answered): registry-state →
catalog surfacing — competitor evidence favors visible state badges
over hiding ungoverned entries (see 02 §Bearing).

## Run log

2026-07-09 — series created (01, 02) from a 2-lens scoped run, 3 agents
(2 lens + 1 adversarial verify), ~75 sources consulted, 10 load-bearing
claims verified: 8 confirmed, 1 refuted (registry scale), 1 softened
(Docker "GA" → "launched"). Fetch failures logged in each doc.
