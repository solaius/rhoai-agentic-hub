---
type: fact
title: "RHAISTRAT-1345 child RFEs filed (RHAIRFE-2630..2635, 2026-07-10)"
description: Six agent-memory RFEs filed as children of RHAISTRAT-1345 via the rfe-creator pipeline, all targeting 3.6 EA2 RHOAI RELEASE; fulfills the 06-30 1:1 commitment to have scoped RFEs in by the week of 2026-07-07.
tags: [agent-memory, jira, rfe, rhaistrat-1345]
timestamp: 2026-07-10
---

Filed 2026-07-10 through the rfe-creator pipeline (drafted from hub
strategy/transcript content, rubric-reviewed 9-10/10, feasibility-checked
against rhoai-3.5-ea.2 architecture context, submitted via Jira REST).
All six: children of RHAISTRAT-1345 (native parent field), target version
"3.6 EA2 RHOAI RELEASE" (not fix versions), labels agent-memory / ai-hub /
3.6-candidate / should-do / agentic, components AI Hub + AI Core Dashboard.

| Key | Title | Notes |
|---|---|---|
| [RHAIRFE-2630](https://redhat.atlassian.net/browse/RHAIRFE-2630) | Framework-agnostic agent memory service | the core substrate; the other RFEs hang off it |
| [RHAIRFE-2631](https://redhat.atlassian.net/browse/RHAIRFE-2631) | Agent memory available as governed MCP tools | depends on 2630 |
| [RHAIRFE-2632](https://redhat.atlassian.net/browse/RHAIRFE-2632) | Built-in agent memory in AI Hub (interim Dev Preview) | relates to 2630; extra labels ogx + uxd, extra component UXD |
| [RHAIRFE-2633](https://redhat.atlassian.net/browse/RHAIRFE-2633) | Record-level scope isolation for agent memory | depends on 2630 |
| [RHAIRFE-2634](https://redhat.atlassian.net/browse/RHAIRFE-2634) | Sensitive-data screening on the agent-memory write path | depends on 2630 |
| [RHAIRFE-2635](https://redhat.atlassian.net/browse/RHAIRFE-2635) | Agent-memory write auditability | depends on 2630 |

2633/2634/2635 are the review-driven split of one governed-memory-writes
draft (right-sized 0/2 as a bundle); siblings are pairwise "relates to".
Draft/review artifacts live in /artifacts/ (rfe-tasks, rfe-reviews).

Still open: the RHAISTRAT-1345 Outcome text predates the 2026-06-30
direction change (standalone service, 3.6 DP / 3.7 TP / 3.8 GA phasing),
so the children are ahead of their umbrella; the rewrite delta is in
[rhaistrat-1345-outcome-update](/features/agent-memory/strategy/rhaistrat-1345-outcome-update.md),
which itself needs the same revision before pasting.
