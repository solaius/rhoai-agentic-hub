---
type: fact
title: AI Gateway team structure and delivery model
description: First networking org team with direct AI BU responsibility — cross-org matrixed delivery (AI Gateway team + MaaS + Agentic API + RHCL/Kuadrant + llm-d), Praxis upstream with CNCF sandbox planned, kicked off July 6 2026.
timestamp: 2026-07-31
tags: [ai-gateway, team, organization]
review_after: 2026-10-31
source: AI Gateway Project GDoc — team section and kickoff notes
---

The AI Gateway team is the first team within the networking
organization holding direct responsibility to the AI BU, with its
backlog and priorities set by AI needs. It owns the Praxis runtime and
AI filters.

## Core team (AI Gateway)

- Architect: Shane Utt
- PM: Christopher Ferreira
- Engineering lead: Matus Makovy
- Engineers: Alex Snaps, Aslak Knutsen, Alexander Cristurean, Didier
  Di Cesare, Tim Walsh, Jamie Land, Alexa Griffith, Ricardo
  Pchevuzinske Katz, Marius Danciu, Pierangelo Di Pilato

## Collaborating workstreams

- **MaaS teams**: subscription management, billing, usage tracking,
  token minting, watsonx.ai workstream
- **AAET Agentic API** (Sebastien Han, Francisco Arceo): Responses
  API, Messages API, API translation
- **RHCL/Kuadrant component teams**: policy foundations, plugins,
  migration scaffolding
- **llm-d/EPP**: placement layer (Morgan Foster, Brent Salisbury)
- **Platform AI Safety** (Christina Xu): NeMo guardrails integration
- **Praxis upstream**: engineers across Red Hat and IBM

## Coordination

- Slack: #forum-ai-gateway (general), #team-ai-gateway (scrum),
  #wg-ai-gateway-internal
- Weekly team syncs + weekly upstream Praxis syncs
- Shared project board: github.com/orgs/praxis-proxy/projects
- Jira: RHAIGW project
- Bi-weekly status emails

## Key technical contracts holding the seams

- API layering: gateway CRDs wrapped by MaaS higher-level APIs
- Filter contract: sole extension path into the pipeline
- EPP wire contract: language-neutral placement interface
- Praxis-OGX internal contract: forwarded identity/tenant/scope/trace
- Parity gates: handoff criteria for each enforcement duty migration
- Conformance suites: Gateway API in CI, Responses/Messages
