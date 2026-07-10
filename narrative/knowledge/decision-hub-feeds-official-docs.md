---
type: decision
title: Hub serves as structured input feeding official product documentation
description: "Decision: the knowledge hub provides internal dissemination and JTBD-structured content that the docs team converts to official product documentation — not a replacement for docs."
decided: 2026-07-10
timestamp: 2026-07-10
source: ref-peter-adel-sync-20260710.md
tags: [narrative, docs, process]
---
**Context:** Peter built feature-level knowledge hubs (e.g., RHCL hub for
MCP Gateway) that the docs team (Lindsay Frazier, Lindsay Barbie) initially
perceived as competing with official product documentation. Adel has been
struggling to get agentic documentation produced — docs team (Linda
Alexander) not producing output despite having Jiras with product
documentation labels.

**Decision:** The hub is internal dissemination, not external documentation.
It structures knowledge around JTBD (evaluate agents, make agents safe,
make inference work for agents, etc.) and connects that to features, Jiras,
customer signals, and strategy. The docs team uses this as structured
input to build official product documentation. The hub gives them:
- JTBD framework for documentation structure
- Feature knowledge already organized and verified
- Links to all Jiras, strategy docs, and upstream repos
- A place where engineers can flag corrections (submit PRs or Slack)

**Consequences:**
- Hub content is optimized for internal consumption + docs-team handoff
- Official product docs remain the docs team's responsibility
- The JTBD structure from the hub should map to documentation areas
- Field teams (Brian Ball et al.) get the hub as their immediate
  dissemination channel while docs catches up
