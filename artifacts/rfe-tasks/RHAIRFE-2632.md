---
rfe_id: RHAIRFE-2632
title: Built-in agent memory in AI Hub (interim Dev Preview)
priority: Normal
size: M
status: Submitted
parent_key: null
original_labels: null
---
**Parent Outcome:** [RHAISTRAT-1345](https://redhat.atlassian.net/browse/RHAISTRAT-1345) (Agent Memory)

## Summary

Users building and piloting agents in AI Hub need those agents to remember prior sessions now, without waiting for the comprehensive memory service. The platform's Responses layer already demonstrates a working memory tool in current development builds; surfacing that capability to AI Hub users gives customers hands-on agent memory in the RHOAI 3.6 timeframe (possibly a 3.5.x update), while the comprehensive governed service matures on its own track.

## Problem Statement

Every agent session in AI Hub starts cold. Users prototyping agents lose all accumulated context between sessions; demos restart from zero; pilot customers evaluating the platform's agentic story conclude that memory is absent. Field and sales teams are repeatedly asked when OpenShift AI will have agent memory and currently have nothing usable in-product to show before 2027.

## Affected Customers

- Pilot and evaluation customers exercising the agentic capabilities of AI Hub / Gen AI Studio, where session amnesia is immediately visible in every demo.
- A small set of accounts explicitly requesting an agent-memory implementation now (accounts on file with the PM); broad "when will you have memory" pressure across the sales pipeline.

## Business Justification

- Hyperscaler competitors ship memory as a GA feature today; an in-product Dev Preview in the 3.6 timeframe keeps OpenShift AI credible in agentic evaluations that are happening now, not in 2027.
- An interim capability generates real usage feedback that de-risks the comprehensive memory service planned for Tech Preview (3.7) and GA (3.8), and feeds the Summit 2027 announcement runway.
- The team has explicitly accepted intersecting Dev Preview features here: the interim capability and the comprehensive service are allowed to coexist, and this RFE keeps the interim path tracked under the same Outcome rather than shipping unmanaged beside it.
- Engineering context (non-prescriptive, prior art): a memory tool built on the platform's existing Responses/files/vector-store plumbing shipped in the latest development build with explicit "remember this" and implicit auto-remember, and was assessed by the team as wireable into AI Hub with modest UI work. Engineering determines the actual approach.

## Acceptance Criteria

- [ ] A user can enable memory for an agent or playground session in AI Hub without writing code or custom configuration.
- [ ] Agents remember both what the user explicitly asks them to remember and relevant context captured automatically, across sessions.
- [ ] Each user's memories are isolated to that user.
- [ ] Users can view what an agent has remembered and delete individual memories.

## Success Criteria

- Dev Preview available to AI Hub users in the RHOAI 3.6 timeframe (3.5.x if feasible).
- At least one customer pilot and the standard demo flows run with memory enabled, producing feedback that informs the comprehensive memory service.
