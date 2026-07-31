---
type: reference
title: Praxis ITS Routing Filter with Dynamic Budget Allocation
description: Feature to implement ITS as a native Praxis routing filter with per-candidate policy enforcement and dynamic budget engine adjusting fan-out count N based on priority/load/budget signals; post-migration.
resource: https://redhat.atlassian.net/browse/RHAISTRAT-2443
tags: [ai-gateway, its, praxis]
timestamp: 2026-07-31
review_after: 2026-10-31
source: hub.jira-sweep 2026-07-31
---

Praxis-native successor to the IPP-based ITS routing (RHAISTRAT-2442).
Fans out a single inference request into N candidates, each subject
to individual policy enforcement, metering, and auditing via Praxis
primitives. Dynamic budget engine adjusts N per request. Depends on
Praxis gateway and RHAISTRAT-2444 (native Rust orchestration). Clones
RHAIRFE-2954.
