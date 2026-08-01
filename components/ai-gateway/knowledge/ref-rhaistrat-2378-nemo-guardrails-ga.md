---
type: reference
title: GA Support for NeMo Guardrails for AI Gateway Traffic via Praxis
description: Feature to promote NeMo Guardrails integration from DP/TP to GA for MaaS traffic -- ext_proc plugin hardening, TrustyAI lifecycle, MaaS CRD configuration, telemetry; parent RHAISTRAT-1210.
resource: https://redhat.atlassian.net/browse/RHAISTRAT-2378
tags: [ai-gateway, guardrails, nemo, ga-readiness]
timestamp: 2026-07-31
review_after: 2026-10-31
source: hub.jira-sweep 2026-07-31
---

Hardens the existing nemo-request-guard and nemo-response-guard IPP
plugins for GA: error handling, the modified-response code path (403
for blocked, content redaction for modified), TrustyAI
NemoGuardrails controller lifecycle, administrator-facing MaaS CRD
configuration, and violation telemetry. Parent: RHAISTRAT-1210.
Clones RHAIRFE-2896.
