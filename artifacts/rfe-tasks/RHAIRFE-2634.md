---
rfe_id: RHAIRFE-2634
title: Sensitive-data screening on the agent-memory write path
priority: Normal
size: M
status: Submitted
parent_key: RFE-003
original_labels: null
---
**Parent Outcome:** [RHAISTRAT-1345](https://redhat.atlassian.net/browse/RHAISTRAT-1345) (Agent Memory)
**Split from:** RFE-003

## Summary

Nothing in current agent-memory approaches prevents PII, credentials, or classified data from entering memory. Regulated customers need every memory write screened for sensitive-data patterns at write time, with policy determining whether a flagged write is blocked, quarantined, or logged, plus a way for administrators to review and remove flagged memories. This RFE delivers that write-path guardrail alongside the first memory Dev Preview.

## Problem Statement

An AI engineer has no guardrail when an agent tries to memorize a credit-card number or a patient identifier from a conversation. Once sensitive data enters shared memory, it can be recalled and re-exposed later. From the user's perspective:

- An AI engineer cannot stop an agent from memorizing sensitive data pulled from a conversation.
- An administrator has no way to find and remove sensitive memories after they are written.

For healthcare (PHI/HIPAA) and other regulated verticals, this is disqualifying today, before any memory feature can even be piloted.

## Affected Customers

- Healthcare accounts raised by field engineering: PHI exposure through shared agent memory is the named blocker to multi-agent healthcare workflows.

## Business Justification

- Write-path governance is a common requirement across regulated verticals (healthcare, financial services, defense): the mechanism is shared, only the policy differs. A write-time guardrail against sensitive data is what those verticals require before enabling memory.
- EU AI Act obligations for general-purpose AI are enforced from August 2026; regardless of the pending high-risk timeline revision, the named healthcare and regulated accounts impose sensitive-data controls contractually today. These are blocked-deal governance gaps, not future risks.
- Governance depth is Red Hat's differentiation in the memory market: hyperscaler and startup memory offerings are exactly weakest here, with no write-time sensitive-data guardrail on a self-hosted store.

## User Scenarios

1. As an AI engineer, when my agent attempts to memorize sensitive data (a card number, a patient identifier), the write is intercepted according to policy and I can see why.
2. As an administrator, I review memories flagged or quarantined by screening and remove any that should not have been stored.

## Acceptance Criteria

- [ ] Memory writes are screened for PII, secrets, and other sensitive-data patterns, with policy determining whether a flagged write is blocked, quarantined, or logged.
- [ ] Administrators can review and remove flagged, quarantined, or otherwise sensitive memories.
- [ ] The screening policy outcome (block, quarantine, or log) is configurable per deployment.

## Success Criteria

- A regulated pilot customer's internal security review passes with sensitive-data screening enabled on the memory write path.
- Sensitive-data patterns configured in policy are intercepted on writes during validation testing.

## Scope

### In Scope
- Sensitive-data screening on the memory write path with configurable policy outcome (block, quarantine, or log).
- Admin review and removal of flagged, quarantined, or otherwise sensitive memories.

### Out of Scope
- Record-level scope isolation and read enforcement (sibling RFE: record-level scope isolation for agent memory).
- Write auditability and the exportable write-event log (sibling RFE: agent-memory write auditability).
- Adversarial memory-injection defense (separate later RFE; screening here targets sensitive-data leakage, not attack patterns).
- Contradiction detection and provenance metadata (Tech Preview phase).

## Open Questions

- Default screening policies per vertical (block vs quarantine) and who ships them.
- Screening must operate in disconnected and air-gapped deployments; any model-based detection needs a locally served detector, which constrains detector choice.
- The write-path latency budget, since screening is synchronous with the write.
- The internal governance prototype under evaluation is contingent on a written IP/license transfer before any productization decision.
