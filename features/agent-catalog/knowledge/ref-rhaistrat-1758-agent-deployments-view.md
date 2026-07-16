---
type: reference
title: RHAISTRAT-1758 — agent deployments view
description: The read-only runtime-visibility view (which agents are running, health, endpoints) — one of the two 3.5 MUSTs; discovers sandbox CRs. In Progress.
resource: https://redhat.atlassian.net/browse/RHAISTRAT-1758
tags: [agent-catalog, jira, deployments-view, 3.5]
features: [agent-interop]
timestamp: 2026-07-16
---

The operational half of the Agent Hub story: a dashboard view of running
agents (vs the catalog's "what exists" half, and distinct from the Agent
Registry's metadata store). In 3.5 it ships read-only, discovering
sandbox CRs via the agent-ops BFF
([3.5 scope](/features/agent-catalog/knowledge/fact-agent-catalog-35-scope.md));
3.5-deployed sandboxes become read-only ghosts under 3.6 OpenShell (no
adoption).
