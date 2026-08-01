---
type: reference
title: "[Feat] Enable its_hub to run as an AI Gateway component"
description: Feature to deliver its_hub as a modular gateway component for inference-time scaling -- dual-stream (IPP plugin on Envoy for 3.5, Praxis filter for future); In Progress, fix_version 3.6 GA.
resource: https://redhat.atlassian.net/browse/RHAISTRAT-178
tags: [ai-gateway, its, inference-time-scaling]
timestamp: 2026-07-31
review_after: 2026-10-31
source: hub.jira-sweep 2026-07-31
---

Delivers ITS (Best-of-N, Self-Consistency) as a gateway-integrated
capability. Stream 1: Envoy integration via IPP routing plugin
(X-ITS-Budget header detection, fan-out to ITS Service). Stream 2:
Praxis-native integration (design phase). Clones RHAIRFE-782.
Fix_version: 3.6 GA.
