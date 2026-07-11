---
type: fact
title: MCPLO key decisions from Slack (Feb-Jul 2026)
description: 10 major architecture and process decisions from #forum-mcp-lifecycle-operator -- OCP entitlement, no-stdio, no auto-SA, standalone DSC component, gateway = GA scope, midstream move, Jenkins gate, image suffixes.
timestamp: 2026-07-11
tags: [mcp-lifecycle-operator, decisions, slack]
features: [mcp-catalog, mcp-gateway, platform]
review_after: 2026-09-11
source: Slack #forum-mcp-lifecycle-operator (C0AGQRDFDJL), full channel review 2026-07-11
---

Key decisions surfaced from full review of #forum-mcp-lifecycle-operator
(2,406 messages, 47 participants, Feb 19 - Jul 10, 2026):

**Architecture:**

1. **MCPLO ships with OCP entitlement, not RHOAI-only** (Feb 2026,
   mrunalp) -- ships as standalone operator with base OCP entitlement.
   Customers can upgrade to RHOAI later.

2. **No stdio support -- SSE and streamable-HTTP only** (Feb/Mar 2026,
   Gordon Sim) -- explicit decision, not a gap.

3. **Operator cannot auto-create ServiceAccounts** (Mar 2026, Gordon
   Sim) -- security concern. Users bring their own SA with appropriate
   RBAC bindings.

4. **MCPLO is a standalone DSC component, not bundled inside AI Hub**
   (Jun 2026, 119-reply thread) -- like KServe, standalone component
   in opendatahub-operator. Catalog UI disables deploy button when
   MCPServer CRD absent, with informative message.

5. **Gateway integration is GA scope, not TP** (May 2026) -- aliok
   wrote formal proposal doc. Tracked as OCPMCP-347.

6. **Single CRD (MCPServer) with logical grouping** (Mar 2026) -- API
   review with Bryce Palmer led to nested structure (source, config,
   management) instead of flat fields. Upstream issue #32, PR #40.

**Build/CI:**

7. **Midstream repo moved from openshift/ to opendatahub-io/ org**
   (Jun 2026) -- original openshift/mcp-lifecycle-operator to be
   deleted.

8. **E2E testing: Jenkins (RHOAI QE), NOT pure Konflux ITS** (Jun
   2026, ksuszyns) -- Konflux ITS will not be the release gate.
   RHOAI internal Jenkins runs the full test matrix.

9. **vSphere testing NOT required** (Jun 2026, Vaclav Tunka) -- none
   of 27 ODH + 8 RHDS components use vSphere. AWS primary, GCP
   secondary.

10. **Upstream-to-midstream sync increased to 2x daily** (Jul 2026) --
    openshift/release PR #81694.

**Conventions:**
- DP/TP/GA image suffixes: `-beta` for DP, `-tech-preview` for TP,
  no suffix for GA
- Downstream branch naming: `rhoai-3.5` convention
