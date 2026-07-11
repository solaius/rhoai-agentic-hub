---
type: fact
title: "AI Hub vs Gen AI Studio: surfaces and personas"
description: AI Hub serves cluster admins and platform engineers (governance/registry surfaces, no playground); Gen AI Studio serves AI engineers (AI asset consumption plus the playground, the odh-dashboard gen-ai module).
tags: [platform, ai-hub, gen-ai-studio, personas, ux]
timestamp: 2026-07-10
---

Owner ruling (2026-07-10, while correcting the agent-memory RFE surface
framing):

- **AI Hub**: cluster admins and platform engineers. Governance and
  registry surfaces (asset registry, catalog administration). It has NO
  playground.
- **Gen AI Studio**: AI engineers. AI asset consumption and the
  playground. Implemented as the odh-dashboard gen-ai module (playground,
  BFF, OGX integration, per
  [fact-slack-channels-by-product-area](/features/platform/knowledge/fact-slack-channels-by-product-area.md)).
- **Platform pattern**: assets are governed and cataloged for admins in
  AI Hub, then discovered and consumed by AI engineers in Gen AI Studio
  (MCP precedent: catalog is an AI Hub surface; the enterprise demand for
  MCP discovery sits inside Gen AI Studio).
- **Routing consequence**: user-facing playground features carry the
  Gen AI Studio component/label; admin governance surfaces carry AI Hub.
  Applied 2026-07-10 to RHAIRFE-2632, retitled "Built-in agent memory in
  Gen AI Studio (interim Dev Preview)".

Caution: internal transcripts and docs use "AI Hub" loosely as an
umbrella for the whole gen-AI dashboard area (e.g. "wireable into AI Hub"
in the 2026-07-07 agent-memory sync). Do not take that phrasing literally
when filing, labeling, or scoping UI work.
