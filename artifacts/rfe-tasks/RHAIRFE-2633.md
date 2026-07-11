---
rfe_id: RHAIRFE-2633
title: Record-level scope isolation for agent memory
priority: Normal
size: M
status: Submitted
parent_key: RFE-003
original_labels: null
---
**Parent Outcome:** [RHAISTRAT-1345](https://redhat.atlassian.net/browse/RHAISTRAT-1345) (Agent Memory)
**Split from:** RFE-003

## Summary

Multi-tenant and regulated customers cannot let agents share a memory store until every memory record is isolated to its intended scope and reads return only what the caller is permitted to see. This RFE delivers record-level scoping and read enforcement, including project isolation on a shared cluster, alongside the first memory Dev Preview, so multiple teams can adopt memory on one cluster without one team's agents surfacing another team's data.

## Problem Statement

Memories written by one team's agents can be visible to another team's. Nothing in current agent-memory approaches (file-based memories, open-source memory frameworks) enforces a boundary between them. From the user's perspective:

- A platform admin cannot promise that team A's agents will never surface team B's data.
- An agent has no boundary that keeps a memory written for one project, tenant, or user from being recalled in a different context.

For multi-tenant banks and Zero Trust environments, this is disqualifying today, before any memory feature can even be piloted.

## Affected Customers

- **OCBC Bank**: multi-tenant requirement that agents from different teams must not see each other's data.
- **NTT Data**: Zero Trust requirement that agents follow the same data-access policies as employees, so an agent's reads are constrained to the scope its principal is entitled to.

## Business Justification

- Scope isolation is the multi-tenancy linchpin of the memory investment: without it, no shared cluster serving multiple teams or tenants can enable memory at all.
- Governance depth is Red Hat's differentiation in the memory market: hyperscaler and startup memory offerings are exactly weakest here, and cross-tenant isolation on self-hosted, shared clusters is a capability those offerings do not provide.
- The named accounts above impose the requirement contractually today. These are blocked-deal governance gaps, not future risks.

## User Scenarios

1. As a platform admin at a bank, I verify that agents in one project cannot read memories written in another project on the same cluster.
2. As a security reviewer, I can demonstrate that record-level scoping prevents an agent from recalling a memory outside its permitted scope.

## Acceptance Criteria

- [ ] Every memory record carries a scope, and reads return only records the caller's scope permits.
- [ ] Teams/projects on a shared cluster cannot read each other's memories; isolation is demonstrable to a customer security reviewer.
- [ ] Scope is enforced on the memory service's read/query path, not only at the storage boundary.

## Success Criteria

- Zero cross-scope reads under isolation testing.
- A multi-tenant pilot customer's internal security review passes with memory enabled on a shared cluster.

## Scope

### In Scope
- Record-level scope on every memory record.
- Read/query-path enforcement so reads return only permitted records.
- Project isolation for teams/projects sharing a cluster.

### Out of Scope
- Sensitive-data screening on the write path (sibling RFE: write-path sensitive-data screening).
- Write auditability and the exportable write-event log (sibling RFE: agent-memory write auditability).
- The full multi-tier scope hierarchy (user/project/role/org); this RFE requires record-level scoping and project isolation, with the richer tier model following at Tech Preview.

## Open Questions

- Whether "project" maps to an OpenShift namespace for the isolation boundary, and how record-level scope composes with namespace and RBAC.
- How the caller's scope is derived from the human principal, through the agent, to the memory read.
