---
type: fact
title: Personas (AI asset registry)
description: The four personas the registry/catalog experience is designed around — focus and registry interaction per persona.
timestamp: 2026-07-08
tags: [platform, personas]
review_after: 2026-08-05
source: ai-asset-registry/docs/knowledge-registry.md §5 (as of 2026-07-05)
---
Four personas define the registry/catalog UX — each with a distinct focus and a distinct way of touching the registry:

- **AI Engineers** — develop AI apps, consume assets. Find approved assets, reference them during development, promote them through workflows.
- **Platform Engineers** — set up and maintain the AI platform. Enable registry capabilities, integrate with OpenShift AI, manage tenancy.
- **AgentOps Admins** — governance and operational oversight. Review/approve assets, manage lifecycle, associate policies.
- **Business Consumers** — indirect users. Benefit from governed, trusted AI capabilities without touching the registry directly.

Distinct from the simplified Builders/Operators pair in [ref-agentic-messaging-guide.md](/features/platform/knowledge/ref-agentic-messaging-guide.md) — that's a 2-persona marketing simplification for external messaging, detailed further (with the "what they want / what Red Hat delivers" table) in [fact-agentic-ai-messaging-position.md](/narrative/knowledge/fact-agentic-ai-messaging-position.md). This is the more granular product/UX persona set, each mapped to a specific registry interaction pattern rather than a messaging pillar.

## JTBD persona vocabulary (2026-07-08)
The locked `persona:` values for `jtbd-` entries (lint-enforced — extend this
list and the linter's `PERSONAS` enum together, through the gate): the four
personas above as `ai-engineer`, `platform-engineer`, `agentops-admin`,
`business-consumer`, plus owner additions `data-scientist`, `cluster-admin`,
`rhoai-admin` (2026-07-08 ruling — audiences the UX/Docs JTBD consumers
work with).
