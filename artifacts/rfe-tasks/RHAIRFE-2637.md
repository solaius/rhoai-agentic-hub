---
rfe_id: RHAIRFE-2637
title: Organization-wide shared agent memory with scope tiers, conflict handling,
  and provenance
priority: Normal
size: L
status: Submitted
parent_key: null
original_labels: null
---
**Parent Outcome:** [RHAISTRAT-1345](https://redhat.atlassian.net/browse/RHAISTRAT-1345) (Agent Memory) · Phase: RHOAI 3.7 Tech Preview

## Summary

The Dev Preview delivers record-level isolation (RHAIRFE-2633): memory that is safely private. For Tech Preview, enterprises need the other half: memory shared deliberately across organizational boundaries (user, project, role, organization) and trustworthy when shared, meaning conflicting memories are detected and surfaced rather than silently coexisting, and every record can be traced to its origin. Sharing, conflict handling, and origin tracking are one trust problem: users will not adopt shared memory they cannot trust or trace, and untrusted shared memory is worse than none because one bad record propagates to every consumer.

## Problem Statement

With isolation only, every team's agents relearn the same organizational facts independently, and the "enterprise brain" value of memory (what the business knows, accumulated across teams) is unreachable. But naive sharing fails immediately from the user's perspective:

- Two teams' agents write contradictory facts into a shared scope, and consumers get whichever one retrieval happens to surface, with no signal that a conflict exists.
- A wrong memory spreads: a user cannot tell where a shared memory came from, so they cannot judge whether to trust it or get it corrected.
- An admin asked "which agents can see this record, and who put it there?" has no answer, which stops security review of any shared-memory deployment.

## Affected Customers

- **OCBC Bank**: multi-tenant requirement that memory is shared within a team but never leaks across teams; tiered sharing with enforced boundaries is the exact ask.
- **NTT Data**: Zero Trust posture requires shared memory to follow the same access policies as employees; role-scoped memory is how that maps.
- Healthcare accounts (on file with the PM): multi-agent workflows over shared memory are the named use case, with hard boundaries around what may be shared, and the field-raised concern that one contaminated input can poison a shared store.

## Business Justification

- Cross-team shared memory is where memory's enterprise value concentrates: the parent Outcome's long-term case ("the enterprise brain") depends on it, and multi-session/multi-agent memory is the industry's lowest-scoring, least-solved capability, so credible shared-memory support is differentiation, not parity.
- Governance depth is Red Hat's stated differentiation in this market; scope tiers with conflict handling and provenance is precisely the layer hyperscaler and startup offerings lack.
- The named accounts above cannot move past pilot without it: isolation-only memory caps them at single-team usage.

## User Scenarios

1. As a platform admin at a bank, I promote a validated memory from a project scope to the organization scope so every team's agents benefit, and the promotion is a deliberate, recorded action.
2. As an AI engineer, when my agent retrieves a fact that conflicts with another memory visible in my scope, the conflict is flagged with both records' origins, so I can resolve it instead of silently getting one of them.
3. As a security reviewer, I pick any shared memory and see where it came from: who or what created it, in which interaction, and how it reached its current scope.

## Acceptance Criteria

- [ ] Memory can be scoped to user, project, role, and organization tiers, and reads respect tier visibility rules.
- [ ] Sharing a memory across a tier boundary is a deliberate, controlled, recorded action, not a side effect.
- [ ] Conflicting memories visible within a scope are detected and flagged to consumers rather than silently coexisting.
- [ ] Every memory record carries provenance: what created it, from which interaction, and its scope history.
- [ ] A user or admin can trace any shared memory to its origin when resolving a conflict or judging trust.
- [ ] Access to shared tiers honors platform identity and roles, demonstrably to a customer security reviewer.

## Success Criteria

- At Tech Preview (RHOAI 3.7 timeframe), a regulated pilot runs shared memory across at least two teams and passes its internal security review.
- Zero unflagged contradictions in conflict-injection testing; zero cross-tier reads outside policy.

## Scope

### In Scope
- The four scope tiers, controlled cross-tier sharing, conflict detection and flagging, provenance metadata, and origin tracing.

### Out of Scope
- Record-level isolation and the basic write log (Dev Preview, RHAIRFE-2633/2635).
- Adversarial memory-injection defense (a GA-phase RFE; this RFE surfaces conflicts and origins, it does not detect attacks).
- The admin console surfaces for managing tiers and conflicts (separate AI Hub governance-surface RFE).

## Open Questions

- Do the remaining prototype tiers with no OpenShift-native analogue (campaign, enterprise-wide beyond org) stay a design horizon or enter scope at GA?
