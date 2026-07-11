---
type: fact
description: Kagenti is being removed from the roadmap; OpenShell will expand to cover its capabilities (owner ruling 2026-07-10)
timestamp: 2026-07-10
features: [agent-registry, mcp-gateway]
---
Owner ruling (2026-07-10, during the first RHCL hub refresh gate): Kagenti
is being removed from the roadmap, and OpenShell will expand to take over
its capabilities. A field-channel signal to the same effect surfaced in the
gateway Slack sweep the same day (a PM-facing member describing Red Hat AI
PMs and engineering "backing away from kagenti as our downstream").

Consequences tracked so far:

- The RHCL hub pages that leaned on Kagenti forward-commitments now carry
  caveats (plan/gaps.html Redis line) and a new open question about which
  OpenShell capabilities replace the Kagenti-provided paths, and on what
  timeline (plan/open-questions.html).
- Historical attributions ("confirmed by the Kagenti engineering team") and
  current install mechanics (kagenti helm chart source) remain factual and
  were not rewritten.
- Follow-up: this partition's own description in features/features.yaml
  still names "Kagenti lifecycle management"; agent-registry content should
  be re-scoped once the OpenShell expansion details land.
