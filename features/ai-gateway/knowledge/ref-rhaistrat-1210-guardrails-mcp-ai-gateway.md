---
type: reference
title: "[Outcome] Integration Safety/Guardrails for MCP/AI Gateway"
description: Outcome for guardrail enforcement across both MCP Gateway and AI Gateway paths -- PII, prompt injection, budget control, compliance audit; In Progress; 14 links spanning HPSTRAT, RHAIRFE, RHOAIENG.
resource: https://redhat.atlassian.net/browse/RHAISTRAT-1210
tags: [ai-gateway, outcome, guardrails, safety]
timestamp: 2026-07-31
review_after: 2026-10-31
source: hub.jira-sweep 2026-07-31
---

Cross-cutting Outcome for integration safety across both gateway
surfaces. Depends on NeMo Guardrails (RHAIRFE-299) and MCP guardrails
integration (CONNLINK-751). Depended on by HPSTRAT-97 (OCP 5.0
Agentic AI), HPSTRAT-125 (post-5.0), and OCPSTRAT-2798 (MCP Gateway
TP1). Related to RHAISTRAT-1269 (platform-level safety for agent tool
calls). Now depends on RHAIRFE-2656 (Responses API guardrails
endpoint) and RHAIRFE-2657 (Messages API guardrails endpoint).

Child: RHAISTRAT-2378 (GA NeMo Guardrails for AI Gateway via Praxis).
