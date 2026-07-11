---
rfe_id: RHAIRFE-2643
title: Memory effectiveness on smaller self-hosted models
priority: Normal
size: M
status: Submitted
parent_key: RFE-009
original_labels: null
---
**Parent Outcome:** [RHAISTRAT-1345](https://redhat.atlassian.net/browse/RHAISTRAT-1345) (Agent Memory) · Phase: RHOAI 3.7 Tech Preview
**Split from:** RFE-009

## Summary

Teams running smaller self-hosted models need the platform memory service to be effective in that model tier, not only with frontier cloud models. The capability to store and retrieve governed memory exists, but a smaller model does not reliably invoke it well without task-specific guidance. These teams need shipped guidance and assets that make memory usage effective on the models they actually run on their own GPUs.

## Problem Statement

Teams running smaller self-hosted models find that agents use memory poorly without task-specific guidance: the memory capability is present, but the model does not reliably decide when and how to use it. This gap is invisible to teams on frontier cloud models and acute for the on-premise, sovereign, and disconnected accounts that run self-hosted models by requirement. Today these teams are left to discover prompting and scaffolding patterns on their own, with no measurable bar for what effective memory usage means in their model tier.

## Affected Customers

- Sovereign and on-premise accounts such as **ITZBund**, whose deployments run self-hosted models on their own GPUs: memory must be effective in that model tier, not only with frontier cloud models.
- The broader on-premise, sovereign, and disconnected segment that chooses OpenShift AI precisely because it does not send traffic to frontier cloud models, and therefore depends on memory working well on smaller self-hosted models.

## Business Justification

- Effectiveness on smaller self-hosted models is a Red Hat-specific differentiator: the on-premise, sovereign, and disconnected accounts that choose OpenShift AI are exactly the ones not sending traffic to frontier cloud models. If governed memory works well only on frontier models, the differentiator is hollow for the accounts most likely to buy on it.
- This value stands on its own: it improves memory usage for self-hosted deployments whether or not a team uses the ready-made harness integrations, and it targets a persona and account set (sovereign and on-premise self-hosted) distinct from the multi-framework adopter.

## Acceptance Criteria

- [ ] Agents running on smaller self-hosted models use memory reliably, with shipped guidance or assets that make memory usage effective in that model tier.
- [ ] The guidance or assets are validated against a defined effectiveness bar on a named smaller-self-hosted-model tier, not only asserted.
- [ ] The guidance and assets are documented and usable in a disconnected, self-hosted deployment, without dependence on frontier cloud models or external services.

## Success Criteria

- At Tech Preview (RHOAI 3.7 timeframe), an agent running on a supported smaller self-hosted model uses governed memory reliably, meeting the defined effectiveness bar without the team having to discover its own prompting or scaffolding patterns.
