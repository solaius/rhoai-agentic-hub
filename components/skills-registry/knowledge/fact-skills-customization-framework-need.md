---
type: fact
title: Generic skills impractical -- need customization framework
description: Generic skills break for enterprise SDLC because every project's pipeline differs; Josh Salomon prototyping extension-point model (customization points without forking) in Ozark/Private Sovereign Cloud; POC ~2 weeks from 2026-08-04.
timestamp: 2026-08-04
tags: [skills-registry, skills-customization, sdlc, extension-points]
source: Peter/Josh 1:1 2026-08-04
---

From Peter/Josh Salomon 1:1: generic skills are impractical for
enterprise SDLC because each project's pipeline differs enough that
one-size-fits-all breaks on any configuration change.

**Josh's extension-point model:**
- Skills declare specific customization points (e.g., "read this config
  file for additional reviewers")
- Users provide configuration at those points without forking the skill
- Example: base skill spawns 5 code reviewers; user adds 2 project-
  specific reviewers via config file; upstream adds a 6th reviewer;
  user automatically gets all 8
- Customization points are contracts -- adding new ones is safe,
  removing them is a breaking change

**Analogous to Amdocs framework pattern:** 15 years of telco
customization -- hundreds of extension points, each telco different
but sharing a common framework. Moved from "copy project per customer"
to "framework with customization points."

**Peter's framing:** this is skills v2.0 for enterprise -- current skill
format is single-tenant (one person uses it); need multi-tenant
architecture where the same skill serves many environments.

**POC:** Josh targeting ~2 weeks (from 2026-08-04) in Ozark (Private
Sovereign Cloud SDLC project). Needs upstream maintainer buy-in.
