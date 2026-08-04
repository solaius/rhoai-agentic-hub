---
type: fact
title: OCP5 skills distribution model -- core payload + operator gating
description: OCP5 ships core agentic skills as a single image in core payload; layered product skills ship with their operator (e.g. troubleshooting -> observability operator); skill availability gated by operator installation.
timestamp: 2026-08-04
tags: [skills-catalog, ocp5, distribution, operators]
components: [skills-catalog]
source: Publishing Red Hat skills meeting 2026-08-04
---

Ju Lim described OCP5's skills distribution model:

**Core payload skills:** shipped as a single image containing all core
agentic skills.

**Layered product skills:** ship with the component's operator:
- Troubleshooting skill -> cluster observability operator
- Update-related skill -> TechPreview component (short-term), core
  payload (long-term)

**Gating model:** skill is available only if the associated operator is
installed. Peter emphasized this as an upsell mechanism and dynamic
catalog enrichment: "if you are installing that, you have installed it,
so therefore it needs to dynamically be added to the catalog."

**Source repos:** one GitHub repo for core skills; layered product
skills live in their own repos.

**Distribution format:** GitHub repo -> OCI image (via supply chain
pipeline). Ju: "We like the Nvidia pipeline too."
