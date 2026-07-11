---
rfe_id: RHAIRFE-2641
title: Agent memory governance console in AI Hub
priority: Normal
size: L
status: Submitted
parent_key: null
original_labels: null
---
**Parent Outcome:** [RHAISTRAT-1345](https://redhat.atlassian.net/browse/RHAISTRAT-1345) (Agent Memory) · Phase: RHOAI 3.7 Tech Preview

## Summary

Platform engineers and cluster admins govern the Dev Preview memory capabilities through APIs alone. They need one AI Hub surface where the organization's memory estate is visible and operable: inventory of memory services and stores, agent-to-memory bindings, review and disposition of quarantined writes, write-log review and export, and scope-policy administration. The enforcement capabilities ship in the Dev Preview RFEs; this console is what makes them operable by the admin persona day to day.

## Problem Statement

Governance without a surface fails in operational reality:

- Customer security reviewers ask to be shown isolation, quarantine, and audit working; "here is the API" does not pass review workflows at regulated accounts.
- Sensitive-data screening produces quarantined writes that need human disposition; without a review queue they pile up unseen, which converts a safety feature into a silent data loss bug from the user's perspective.
- The compliance officer scenario committed in the Dev Preview (review who wrote what, when, into which scope, and export it) has no home an auditor can actually use.
- Disconnected customers cannot be pointed at a hosted console; the surface must live in the cluster with the rest of AI Hub.

## Affected Customers

- **SAS**: the auditable-trace requirement is a review workflow performed by compliance staff, not engineers; it needs a surface they can operate.
- **OCBC Bank**: must demonstrate team isolation to internal security; a bindings-and-scopes view is how that demonstration happens.
- **BNP Paribas** and **ITZBund**: audit review and export inside disconnected deployments, where an in-cluster console is the only option.

## Business Justification

- The governance depth Red Hat is differentiating on (scope isolation, screening, auditability) only converts to won deals when the customer's admin and compliance personas can see and operate it; the console is the last mile of the investment already committed under the parent Outcome.
- AI Hub is the platform's established admin surface for governed AI assets; memory governance appearing there completes the "one control plane" story alongside models, prompts, and MCP servers, matching the persona split the platform already follows (admins govern in AI Hub, engineers consume in Gen AI Studio).

## User Scenarios

1. As a platform admin, I review this week's quarantined memory writes, release the false positives, delete the true PII hits, and escalate one for investigation.
2. As a compliance officer, I filter the memory write log by scope and date range and export it for an audit, entirely from the console.
3. As a platform admin decommissioning a store, I first check which agents are bound to it and at which scopes, so nothing breaks blind.

## Acceptance Criteria

- [ ] An admin sees an inventory of memory services and stores with status and governed-asset state.
- [ ] An admin sees which agents are bound to which memory stores and scopes.
- [ ] An admin reviews flagged and quarantined memory writes and disposes of them (release, delete, escalate).
- [ ] An admin or authorized reviewer reviews the memory write log and exports it from the console.
- [ ] An admin administers scope policy: who can read and write which tiers.
- [ ] The console is fully functional in disconnected and air-gapped deployments.

## Success Criteria

- At Tech Preview (RHOAI 3.7 timeframe), a regulated pilot's security review is conducted against the console rather than raw APIs and passes.
- Quarantine dwell time is visible and bounded: flagged writes get human disposition instead of accumulating.

## Scope

### In Scope
- The AI Hub admin surface over capabilities delivered by the memory service and its governance RFEs, in-cluster and disconnected-capable.

### Out of Scope
- The enforcement mechanisms themselves: isolation (RHAIRFE-2633), screening and quarantine (RHAIRFE-2634), write logging (RHAIRFE-2635), tiers and provenance (the shared-memory RFE).
- Engineer-facing memory views in Gen AI Studio (separate RFE for that persona).

## Open Questions

- Which console capabilities land at Tech Preview versus GA, given the audit trail itself completes at GA?
