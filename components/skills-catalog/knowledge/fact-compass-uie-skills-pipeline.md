---
type: fact
title: UIE/Compass skills pipeline -- alignment gap with RHAI
description: UIE/Compass team (300+ engineers) has a skills registry with security auditing, scorecards (gold=public, silver=internal), and marketplace publishing pipeline; RHAI team was unaware until 2026-08-04 meeting. Light Trail team also building MCP hosting on MP+.
timestamp: 2026-08-04
tags: [skills-catalog, ai-asset-pipeline, compass, uie, light-trail]
components: [skills-catalog, ai-asset-pipeline]
source: Publishing Red Hat skills meeting 2026-08-04
---

The 2026-08-04 cross-product meeting revealed a major alignment gap:

**Compass (UIE):**
- Skills registry with metadata management
- Scorecard system: gold rating = can go public; silver = internal only
- Security auditing, evaluations, and compliance checks
- Publishing pipeline to external marketplaces (Claude, ChatGPT, Gemini)
- Ilan Pinto: "there is an entire organization that is doing the same
  stuff... the UIE organization has like 300 engineers and product
  managers doing exactly what you just described"

**Light Trail (also UIE):**
- Building MCP server hosting on MP+ with SSO
- Similar to Red Hat AI capabilities but unknown to RHAI team
- Ilan: "they don't know about you, you don't know about them"

**Adel's reaction:** "We always have structural problem... better late
than never." The disconnect is organizational -- RHAI team building
MLflow-based registry, UIE building Compass-based registry, neither
aware of the other.

**Compass vs MLflow registry:** Adel framed Compass as metadata
registry overlapping with MLflow's registry layer; proposed separating
content (where skills live) from registry (metadata lifecycle) from
distribution (OCI, Lola, marketplace).
