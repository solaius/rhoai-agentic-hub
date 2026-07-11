---
rfe_id: RHAIRFE-2640
title: Memory visibility and control for AI engineers in Gen AI Studio
priority: Normal
size: M
status: Submitted
parent_key: null
original_labels: null
---
**Parent Outcome:** [RHAISTRAT-1345](https://redhat.atlassian.net/browse/RHAISTRAT-1345) (Agent Memory) · Phase: RHOAI 3.7 Tech Preview

## Summary

AI engineers iterating on agents in Gen AI Studio need to see and steer memory where they already work: discover which memory stores are available to them, attach one to an agent or playground session, inspect what the agent has remembered and what it recalled in a given exchange, and correct it, all without leaving the studio or dropping to APIs.

## Problem Statement

At the 3.6 Dev Preview, memory beyond the built-in playground tool is invisible from the studio. An engineer cannot enumerate the memory stores available to them, cannot attach the governed memory service to the agent they are iterating on, and, most damaging for trust, cannot see why an agent just recalled what it recalled. When memory misbehaves (wrong fact recalled, right fact missed) the engineer's only recourse is API spelunking, which in practice means memory gets turned off. The interim tool's view/delete covers only its own memories, not the governed service.

## Affected Customers

- Every 3.6 Dev Preview pilot graduating from the interim playground tool to the governed service: the studio is where they will meet it or fail to.
- The enterprise cohort that demanded in-studio discovery for MCP servers rather than hand-authored configuration (named accounts on file with the PM): the same buyers expect the same for memory, and the platform has already accepted that pattern once.

## Business Justification

- Inspectability at the engineer level is what makes memory trusted enough to leave enabled; opaque memory reads as nondeterministic agent behavior and gets disabled, which forfeits the entire investment under the parent Outcome.
- The Summit 2027 demo (the stated purpose of the 3.7 Tech Preview) runs in Gen AI Studio; memory must be visible and demonstrable there, not only present in APIs.

## Acceptance Criteria

- [ ] An engineer can see the memory stores available to them from within Gen AI Studio.
- [ ] An engineer can attach or detach a memory store for an agent or playground session without writing code.
- [ ] An engineer can inspect what an agent has remembered, and what it recalled in a given exchange.
- [ ] An engineer can correct memory: edit or delete records their scope permits.
- [ ] Memory changes take effect in the running session without leaving the studio.

## Success Criteria

- At Tech Preview (RHOAI 3.7 timeframe), the standard agent-iteration demo shows memory attach, recall inspection, and correction entirely inside Gen AI Studio.
- Pilot engineers debug a wrong-recall incident end to end without using the API directly.
