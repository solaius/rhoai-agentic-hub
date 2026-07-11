---
rfe_id: RHAIRFE-2638
title: Inspectable context engineering for long-running agents
priority: Normal
size: M
status: Submitted
parent_key: null
original_labels: null
---
**Parent Outcome:** [RHAISTRAT-1345](https://redhat.atlassian.net/browse/RHAISTRAT-1345) (Agent Memory) · Phase: RHOAI 3.7 Tech Preview

## Summary

Long-running agents outgrow their context windows, and today the platform gives their operators no visibility into what happens next: context is either lost or compacted opaquely. AI engineers need context handling that keeps long sessions coherent, assembles relevant memory into context at the right moments, and is inspectable end to end, so that both an engineer debugging behavior and a reviewer reconstructing a decision can see exactly what the agent knew when it acted, and so token spend is measurably efficient.

## Problem Statement

- Agents degrade in long sessions: earlier instructions and facts fall out of context, and quality decay is invisible until outputs go wrong.
- Where compaction exists it is opaque: no one can answer "what was summarized away, and what did the agent actually see before this response?" For regulated customers that question is the same inspectability requirement that applies to memory writes, extended to reads.
- Token costs grow with context length; without measured, quality-preserving compaction and assembly, memory makes agents more expensive instead of more efficient.

## Affected Customers

- The regulated cohort driving the governance RFEs (SAS, BNP Paribas, ITZBund, detailed on RHAIRFE-2633/2635): their reviewers must reconstruct agent decisions, which requires knowing the context the agent had, not only what it wrote to memory.
- Every long-horizon pilot from the 3.6 Dev Preview: multi-week assistants and operations agents hit context limits first and are the accounts most exposed to silent quality decay.

## Business Justification

- Inspectable context handling is the read-side completion of the compliance story the parent Outcome leads with; opaque compaction is explicitly non-reviewable, and the industry's opaque-by-default implementations are a documented gap Red Hat can differentiate against.
- Token efficiency at a quality threshold is a measurable cost story that gives sales a number, and efficient context assembly on Red Hat's own inference stack (vLLM, llm-d) is a cross-layer advantage only the platform vendor can deliver end to end.

## Acceptance Criteria

- [ ] Long-running agent sessions maintain output quality past context limits: older material is compacted rather than silently lost.
- [ ] Compaction is inspectable: a human-readable record shows what was kept, summarized, and dropped, and when.
- [ ] Relevant memories are assembled into agent context automatically at the right moments, without the engineer hand-building context.
- [ ] A reviewer can reconstruct what context an agent had when it produced a given response.
- [ ] Context assembly and compaction demonstrate measured token-efficiency gains at equivalent output quality.

## Success Criteria

- At Tech Preview (RHOAI 3.7 timeframe), long-session evaluations show quality held past the context limit with a published token-efficiency measurement.
- A compliance-style review exercise successfully reconstructs an agent's context for a chosen response using only the inspectable record.
