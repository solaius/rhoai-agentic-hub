---
rfe_id: RHAIRFE-2639
title: Agent memory as a governed asset in the AI Asset Registry
priority: Normal
size: M
status: Submitted
parent_key: null
original_labels: null
---
**Parent Outcome:** [RHAISTRAT-1345](https://redhat.atlassian.net/browse/RHAISTRAT-1345) (Agent Memory) · Phase: RHOAI 3.7 Tech Preview

## Summary

Memory services and their relationships to agents need to be governed like the platform's other AI assets. Platform engineers need memory services registered with ownership and lifecycle state, and agent-to-memory bindings recorded and queryable, so the organization's memory estate is managed through the same control plane as its models, prompts, and MCP servers rather than becoming a parallel, untracked category.

## Problem Statement

At Dev Preview the memory service runs but is not a registered asset. From the platform engineer's perspective:

- There is no ownership or lifecycle record: nobody can say who owns a memory service, whether it is approved for production, or when it should be retired.
- There is no record of which agents depend on which memory service or store, so decommissioning or changing one is a blind operation.
- Asset-level policy (approval workflows, deprecation) cannot be applied to memory at all, while it applies to every other asset type, which invites ungoverned DIY memory deployments in the gap.

## Affected Customers

- **SAS**: blocked on production agents without a complete governance trail; an unregistered memory service is a hole in that trail.
- **Infineon**: chose the platform for one governance layer across three frameworks; memory outside the registry re-fragments exactly what they consolidated.
- Enterprise accounts using the AI Asset Registry as their control plane against DIY proliferation (accounts on file with the PM): memory is the next asset category to proliferate if it is not registrable.

## Business Justification

- "Registry = governance" is the platform's stated model; memory is the first asset type that is itself a live datastore, and registering the service (not the records) is the settled resolution from the parent Outcome's research. Leaving memory out of the registry undermines the registry's control-plane claim for every asset type.
- Recorded agent-to-memory bindings are a prerequisite for the operational and audit stories already committed in the Dev Preview RFEs (who is affected by this store, whose memories are these).

## Acceptance Criteria

- [ ] A memory service can be registered as a governed asset with ownership and lifecycle status.
- [ ] Agent-to-memory bindings are recorded and queryable: which agents use which memory service and store.
- [ ] Asset-level governance actions (approve, deprecate, retire) apply to memory services as they do to other asset types.
- [ ] Viewing an agent in the registry shows its memory dependencies alongside its models and tools.

## Success Criteria

- At Tech Preview (RHOAI 3.7 timeframe), a platform engineer answers "which agents would this store's retirement affect?" from the registry alone.
- A customer governance review finds no gap between memory and other asset types in registration, ownership, and lifecycle coverage.
