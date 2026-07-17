---
type: question
title: Is the registry record-only in the revocation path?
description: Fleet evidence demands seconds-level agent revocation that must not depend on registry sync — open whether the registry is strictly the lookup (identity linkage one query away) with enforcement in the identity/gateway plane, or participates in enforcement.
status: open
timestamp: 2026-07-16
tags: [agent-registry, fleet-management, identity]
features: [agent-interop]
---
Evidence: [research/10-requirements](/features/agent-registry/research/10-requirements.md)
(revocation-speed grading, registry-as-lookup recommendation). Bears
directly on [jtbd-manage-agent-fleet](/narrative/knowledge/jtbd-manage-agent-fleet.md)'s
"revoke access in seconds" phrasing and on SLO design (registry sync
latency tolerance).
