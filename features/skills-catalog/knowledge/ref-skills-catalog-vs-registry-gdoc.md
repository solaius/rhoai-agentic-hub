---
type: reference
title: "Skills Catalog vs. Skills Registry (GDoc, Ramesh Reddy)"
description: Ramesh's catalog vs registry comparison doc -- feature table, storage/identity/governance model, prioritization (Agent Registry first, lightweight Catalog, revisit full Registry), action items, stakeholder map, installation-location TODO.
resource: https://docs.google.com/document/d/1dZHUmOXpAZg-sSLvTFBYu_942dBM0-Fhedbez25PwUc
tags: [skills-catalog, skills-registry, design, gdoc]
features: [skills-catalog, skills-registry]
timestamp: 2026-07-23
source: Google Doc prepared for Skills Registry/Catalog meeting 2026-07-23
---

Ramesh's comparison document prepared for the 3:30pm meeting. Contains:
catalog vs registry feature comparison table, storage model (Git-backed,
no artifact storage by AI Hub), identity model (Git URL + commit, no
registry-generated ID), governance position (enforced at agent
create/deploy/execute, not catalog), prioritization recommendation
(Agent Registry for governance, lightweight Git-backed Catalog first,
revisit full Registry on customer demand), detailed assumptions/plans
for both catalog and registry needs, installation features TODO (needs
own STRAT), and stakeholder list (Catherine Weeks, Jason Greene, Edson
Tirelli, Daniele Zonca, Peter Double, Adel Zaalouk, Andrew Ballantyne).

Comments from Edson Tirelli: push both RFCs upstream, stop
self-throttling; installation orthogonal to governance needs.
