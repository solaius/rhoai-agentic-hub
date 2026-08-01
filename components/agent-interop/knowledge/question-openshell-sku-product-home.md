---
type: question
title: Which product ships OpenShell (SKU decision)
description: Open question on whether OpenShell ships as RHOAI component, separate Red Hat AI SKU, or OCP component. Impacts release cadence and engineering ownership.
status: open
timestamp: 2026-07-11
tags: [agent-interop, openshell, sku, product]
source: GDoc "Strategic Assessment" open questions table
---

Current working assumption: native RHOAI component (per Adel). But
multiple options exist:

- RHOAI umbrella operator integration (hefty process, currently under
  refactoring)
- Separate OLM-based operator (less coupling, upstream-friendly)
- Red Hat AI SKU (different footprint for personal agent use case)
- OCP component (would create release cadence mismatch)

Roland Huss noted separate operator is viable and avoids RHOAI operator
coupling. Dimitri Saridakis flagged release cadence risk if built from
OCP. Ann Marie noted it could be an optional prerequisite operator.
