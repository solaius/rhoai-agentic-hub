---
type: fact
title: "RHAISTRAT-1345 child RFEs filed (RHAIRFE-2630..2643, 2026-07-10)"
description: Fourteen agent-memory RFEs filed as children of RHAISTRAT-1345 via the rfe-creator pipeline - six 3.6 DP basics (2630..2635, target 3.6 EA2 RHOAI RELEASE) plus eight 3.7 TP wave (2636..2643, no target version until 3.7 exists in Jira); fulfills the 06-30 1:1 commitment.
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

## 3.7 TP wave (filed later the same day)

Eight more children, same pipeline (reviewed 9-10/10, all feasible), no
target version until the 3.7 versions exist in Jira; labels add
`3.7-candidate`, with `gen-ai-studio`+`uxd` on 2640 and `ai-hub`+`uxd` on
2641 per the [surface/persona rule](/features/platform/knowledge/fact-ai-hub-vs-gen-ai-studio-surfaces.md).

| Key | Title | Notes |
|---|---|---|
| [RHAIRFE-2636](https://redhat.atlassian.net/browse/RHAIRFE-2636) | Automatic memory creation and curation | depends on 2630; relates to 2634 (shared write path) |
| [RHAIRFE-2637](https://redhat.atlassian.net/browse/RHAIRFE-2637) | Org-wide shared memory: tiers, conflict handling, provenance | depends on 2633 |
| [RHAIRFE-2638](https://redhat.atlassian.net/browse/RHAIRFE-2638) | Inspectable context engineering | depends on 2630 |
| [RHAIRFE-2639](https://redhat.atlassian.net/browse/RHAIRFE-2639) | Memory as a governed AI Asset Registry asset | depends on 2630 |
| [RHAIRFE-2640](https://redhat.atlassian.net/browse/RHAIRFE-2640) | Memory visibility for AI engineers in Gen AI Studio | depends on 2630; relates to 2632 (interim-tool graduation) |
| [RHAIRFE-2641](https://redhat.atlassian.net/browse/RHAIRFE-2641) | Memory governance console in AI Hub | depends on 2639, 2637, 2634, 2635 |
| [RHAIRFE-2642](https://redhat.atlassian.net/browse/RHAIRFE-2642) | Harness/framework memory integration packs | depends on 2630; split sibling of 2643 |
| [RHAIRFE-2643](https://redhat.atlassian.net/browse/RHAIRFE-2643) | Memory effectiveness on smaller self-hosted models | depends on 2630; split sibling of 2642 |

2642/2643 are the review-driven split of the harness-integrations draft
(right-sized 1/2: different segments, independently shippable). Reviewer
flag on closed CLI harnesses stands: they may only support tool/MCP-level
integration. Owner ruling 2026-07-10: the proposed landings are planning
proposals, not commitments; there is no pull-forward concern on 2642/2643,
the team plans around the filed RFEs and sees where they land (narrative
page: /features/agent-memory/enablement/agent-memory-rfe-narrative/).

The Outcome description was rewritten in Jira 2026-07-10 (standalone
service, three layers, 3.6 DP / 3.7 TP / 3.8 GA) and lists both waves.
Remaining gap: the 3.8 GA wave (full audit trail + erasure,
operator/observability/FIPS, adversarial defense, benchmarking) stays
unfiled per the staging plan.
