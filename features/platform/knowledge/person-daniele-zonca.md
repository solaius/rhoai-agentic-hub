---
type: person
title: Daniele Zonca
description: RHOAI serving/supportability engineering leader — guards the validated-vs-supported image boundary, CVE/maintenance scope, and framework-support due diligence; commenting on the AIPCC ADR.
role: Engineering Leader
org: RHOAI Model Serving
timestamp: 2026-07-16
tags: [platform, serving, supportability]
features: [agent-catalog]
---
The supportability gatekeeper in the agent-catalog supported-images
discussion (2026-07-10): supplied the validated = vendor-maintained
precedent (NVIDIA Triton) behind
[the terminology decision](/features/agent-catalog/knowledge/decision-supported-not-validated-images.md);
holds that skills can only ship as "tested with these models"; warns that
embedding LangChain/LangGraph/CrewAI in shipped images pulls the team into
CVE/serialization maintenance outside original scope
([framework boundary question](/features/agent-catalog/knowledge/question-agent-catalog-framework-support-boundary.md)).
Taking the reconciliation to the
[AIPCC base-images ADR](/features/agent-catalog/knowledge/ref-aipcc-agent-base-images-adr.md)
directly.
