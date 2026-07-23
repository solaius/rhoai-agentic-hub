---
type: fact
title: Catalog deploy wizard — dashboard-owned, BFF path
description: The deploy wizard is dashboard-owned (Gage Krumbach); catalog-to-deploy uses extensions + BFF communication to prefill the wizard; env vars settable at deploy time; MCP/skills not in UX designs yet (discovery only).
timestamp: 2026-07-11
tags: [agent-catalog, deploy-ux, dashboard, bff]
features: [agent-catalog]
source: Slack group DM Ann Marie/Andrew/Gage ~2026-07-11
review_after: 2026-10-11
---

The catalog-to-deploy flow is a **dashboard-owned path** (Gage
Krumbach, ~2026-07-11):

- Uses **extensions + BFF communication** to pass data from the catalog
  to the deploy wizard, prefilling the form. Andrew notes the BFF
  pattern is not technically in place yet but will be part of his
  proposal.
- The current UX design allows setting **any number of environment
  variables** for the image at deploy time.
- **MCP and skills set at runtime are NOT part of the UX designs** as
  of 2026-07-11. The designs only cover discovering what agent-card
  skills and MCPs exist — not configuring them at deploy time.

Prototype links (VPN-only):
- Deploy wizard: project-navigator-rhoai-da8b8e.pages.redhat.com/ai-hub/agents/deployments/
- Catalog: project-navigator-rhoai-da8b8e.pages.redhat.com/ai-hub/agents/catalog

Andrew flagged inconsistencies between prototype versions (different
subdomain links circulating from different teams).
