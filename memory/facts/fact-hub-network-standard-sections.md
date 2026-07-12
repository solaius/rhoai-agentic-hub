---
type: fact
description: "every knowledge hub carries Jobs to be Done (Understand) + Jira Tracker Strats (Plan), maintained by hub.refresh-site via the sections: block in refresh configs; tracker rows follow the unauthenticated-probe rule; the mcp-gateway stored Jira scope is provisional pending owner refinement"
timestamp: 2026-07-12
status: current
---

As of the component hub build-out (2026-07-12), all five knowledge hubs
(RHCL/Gateway, Management, MCP Catalog, MCP Lifecycle Operator, MCP
Registry) carry the same two standard pages: a Jobs to be Done page under
Understand (renders every `narrative/knowledge/jtbd-*.md` whose `features:`
list includes the hub's feature id) and a Jira Tracker (Strats) page under
Plan (a static table of the feature's RHAISTRAT issues, generated from its
stored Jira scope).

`hub.refresh-site` owns both going forward via a `sections:` block in each
hub's `work/refresh-<slug>.yaml` config: `sections: {jtbd: true,
jira_tracker: {project: RHAISTRAT}}`. On refresh it re-derives the job set
and re-runs the stored scope, proposing diffs through the normal gated
page-diff flow. Jira tracker rows honor the unauthenticated-probe visibility
rule already used by tracked `jira-snapshot.yaml` files: a null summary
renders as "(summary withheld)" rather than being hand-filled from memory.
Jira unreachable means no tracker change is proposed; the page keeps its
last `data-verified` date and the staleness indicator surfaces it.

**Open item for owner review:** the mcp-gateway Jira scope added to
`features.yaml` to support the RHCL hub's tracker page is provisional, a
summary-match JQL (`project = RHAISTRAT AND summary ~ "MCP Gateway"`) with
no key allowlist. The other four features' scopes anchor on specific keys.
Refine when there's time to curate it.

See [[fact-internal-publish-target]] for the publish side of this effort.
Spec:
[/docs/specs/2026-07-11-component-hub-buildout-design.md](/docs/specs/2026-07-11-component-hub-buildout-design.md).
