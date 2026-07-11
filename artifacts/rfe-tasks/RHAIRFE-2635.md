---
rfe_id: RHAIRFE-2635
title: Agent-memory write auditability
priority: Normal
size: M
status: Submitted
parent_key: RFE-003
original_labels: null
---
**Parent Outcome:** [RHAISTRAT-1345](https://redhat.atlassian.net/browse/RHAISTRAT-1345) (Agent Memory)
**Split from:** RFE-003

## Summary

Regulated customers cannot let agents write to memory in production without a record of who wrote what, when, and into which scope. This RFE delivers a reviewable, exportable write-event log for agent memory alongside the first memory Dev Preview, so compliance teams can answer what an agent memorized and export that record for an audit.

## Problem Statement

There is no record of who wrote what, when, into which scope. Nothing in current agent-memory approaches captures it. From the user's perspective:

- A compliance officer cannot answer "what did this agent memorize about this customer last week?"
- An auditor has no exportable record of memory activity to review against the customer's compliance obligations.

For customers who must produce a full auditable trace of every data access, and for disconnected deployments with strict compliance-audit requirements, this is disqualifying today, before any memory feature can even be piloted.

## Affected Customers

- **SAS**: blocked from moving agents to production without a full auditable trace of every data access.
- **BNP Paribas**: strict compliance audit requirements in disconnected deployments.
- **ITZBund** (German federal IT): data sovereignty and auditability; all AI activity must stay inside the governance perimeter.

## Business Justification

- Auditability is the production-gating requirement for regulated accounts: without a write-event record they cannot pass internal security review, so memory cannot leave pilot.
- EU AI Act obligations for general-purpose AI are enforced from August 2026; regardless of the pending high-risk timeline revision, the named accounts above impose auditability contractually today. These are blocked-deal governance gaps, not future risks.
- Governance depth is Red Hat's differentiation in the memory market: hyperscaler and startup memory offerings are exactly weakest here, and none offers an exportable audit record on a self-hosted, disconnected store.

## User Scenarios

1. As a compliance officer, I review which memories an agent wrote last week, on whose behalf, into which scope, and export that record for an audit.
2. As an auditor in a disconnected environment, I export the memory write log into the compliance tooling my organization controls.

## Acceptance Criteria

- [ ] Every memory write is recorded (who, what, when, which scope) in a log administrators can review.
- [ ] The write log can be exported by authorized users for compliance review.
- [ ] Each write is attributed to the principal on whose behalf it was made.

## Success Criteria

- 100% of memory writes appear in the write log.
- A regulated pilot customer's internal security review passes with the write log enabled, and the customer can export the record into its own compliance tooling.

## Scope

### In Scope
- A basic, reviewable write-event log capturing who, what, when, and which scope for every memory write.
- Export of the write log by authorized users for compliance review.

### Out of Scope
- Record-level scope isolation and read enforcement (sibling RFE: record-level scope isolation for agent memory).
- Sensitive-data screening on the write path (sibling RFE: write-path sensitive-data screening).
- The full append-only audit trail of reads and writes with erasure primitives (GA-gating capability, separate later RFE).

## Open Questions

- The export contract (for example an open event schema, file, or API) and whether the export sink is a customer-managed system outside the platform.
- On-behalf-of attribution: propagating the human principal's identity from the agent runtime to the memory write point.
- In disconnected deployments the export target is a customer-managed system, so the export contract must not assume a hosted sink.
