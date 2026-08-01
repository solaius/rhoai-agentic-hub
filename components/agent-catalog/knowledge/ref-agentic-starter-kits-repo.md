---
type: reference
title: agentic-starter-kits repo
description: The RH-curated starter-kit repo that IS the 3.5 catalog content — ~10-15 agents; agent.yaml per kit drives catalog metadata (claude-code/openclaw entries being filled in).
resource: https://github.com/red-hat-data-services/agentic-starter-kits
tags: [agent-catalog, starter-kits, github]
timestamp: 2026-07-16
---

Everything the 3.5 catalog shows comes from here: agent.yaml (displayName,
description, framework, logo, labels), README (card body), repo URL. 11/15
kits had agent.yaml descriptions as of 2026-06-04; A2A implemented only by
the CrewAI and LangGraph kits. Tags taxonomy + logo artwork land here via
small PRs. The OpenClaw kit's manifests were tested on OpenShift 4.19 with
the upstream community image (a supported UBI image is a separate track).
