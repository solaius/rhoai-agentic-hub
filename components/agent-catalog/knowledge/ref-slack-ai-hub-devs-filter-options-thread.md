---
type: reference
title: "#openshift-ai-hub-devs -- filter_options endpoint thread"
description: 50-message thread (Jul 9-14 2026) driving the agent catalog filter_options endpoint to real data -- metadata PRs (#247, #256), catalog vs deployments requirements split, harness kits confirmed in scope, and the real filter_options response shape.
resource: https://redhat-internal.slack.com/archives/C08G31WCV16/p1783698413247109
tags: [agent-catalog, slack, filter-options, metadata]
timestamp: 2026-07-23
---
Started by Pushpa Padti requesting the exact filter_options response format
to map UI sidebar filters. Escalated when PR #247 (template kit metadata)
stalled in draft. Key outcomes:
- Harness kits (opencode, claude-code, etc.) confirmed in scope for 3.5 by
  Adel Zaalouk -- PR #256 adds them.
- Catalog inclusion vs. deployments list requirements are separate contracts
  (Gage Krumbach); Agent Deployments yellow for 3.5 DP.
- Real filter_options response delivered with 14 agents across 11 frameworks,
  2 deployment models (config-driven, flow-import), and 16 labels.
- Ramesh recommended building extensive mock data early for future releases
  ("code and data are delivered in different cycles").
