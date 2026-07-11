---
rfe_id: RHAIRFE-2636
title: Automatic memory creation and curation for agents
priority: Normal
size: L
status: Submitted
parent_key: null
original_labels: null
---
**Parent Outcome:** [RHAISTRAT-1345](https://redhat.atlassian.net/browse/RHAISTRAT-1345) (Agent Memory) · Phase: RHOAI 3.7 Tech Preview

## Summary

Agents using the platform memory service today remember only what someone explicitly stores. AI engineers need memory that builds and maintains itself: relevant information captured automatically during interactions, consolidated over time, weighted by whether the remembered approach actually worked, and pruned when stale, so long-running agents get better with use instead of accumulating noise.

## Problem Statement

With explicit-only capture, memory quality depends entirely on engineers and users remembering to save the right things at the right moments, which they do not. Over weeks of use, stores fill with duplicates, stale facts, and trivia, and recall quality degrades. Episodic memories carry no signal about outcomes, so an agent is as likely to repeat a failed approach as a successful one. Teams with their own curation approach have no way to bring it: capture behavior is take-it-or-leave-it.

## Affected Customers

- Every account piloting the 3.6 memory Dev Preview: the interim capability's implicit auto-remember is its most-used behavior in demos, and the comprehensive service must match and exceed it or pilots regress at Tech Preview.
- Accounts explicitly requesting agent memory (on file with the PM), whose use cases (multi-week assistants, operations agents) are exactly the long-horizon scenarios where manual curation breaks down.

## Business Justification

- Strategic: RHOAI 3.7 is the Tech Preview release that sets up the Summit 2027 announcement under RHAISTRAT-1345. Every competing memory offering (hyperscaler GA features, leading open-source memory projects) captures and consolidates automatically; a service that only stores explicit saves fails side-by-side evaluation.
- Production precedent validates the specific behaviors: outcome-weighted episodic memory and scheduled consolidation are shipping in production systems today and are the documented drivers of memory usefulness at scale; the industry's measured gap between benchmark and production performance is a curation-quality gap.
- Pluggability protects customers and Red Hat from betting on a single curation approach in a consolidating market.

## User Scenarios

1. As an AI engineer, my support agent automatically remembers a customer's environment details mentioned in passing, without the user saying "remember this," and recalls them next session.
2. As an AI engineer, my agent's memory is consolidated in the background: duplicates merge, stale records age out, and I did not have to schedule or script any of it.
3. As an AI engineer, my agent remembers that a previous approach to a task failed and avoids repeating it, because unsuccessful outcomes are retained with appropriate weight.
4. As a platform team, we replace the built-in curation behavior with our own domain-specific approach without losing the rest of the memory service.

## Acceptance Criteria

- [ ] Agents capture relevant information automatically during interactions, with explicit "remember this" still available.
- [ ] Memories are consolidated over time (duplicates merged, stale and low-value records pruned) without user action.
- [ ] Episodic memories carry outcome signal, and unsuccessful outcomes are retained and weighted so agents avoid repeating failures.
- [ ] Users can see why a memory exists: whether it came from an explicit save, automatic capture, or consolidation.
- [ ] Customers can substitute their own memory-creation and curation approach for the built-in one.
- [ ] The quality of automatic capture is measurable, so operators can validate and tune what is kept versus discarded.

## Success Criteria

- In Tech Preview evaluations (RHOAI 3.7 timeframe), agents with automatic capture and curation enabled measurably outperform explicit-only memory on multi-session tasks.
- Pilot feedback confirms noise does not accumulate: recall quality holds or improves over multi-week usage.

## Scope

### In Scope
- Automatic capture, background consolidation, outcome weighting, capture-quality measurement, and pluggable curation for the platform memory service.

### Out of Scope
- The memory substrate and its storage backends (delivered under RHAIRFE-2630).
- Sensitive-data screening on the write path (RHAIRFE-2634 governs what may be written; this RFE governs what is worth writing).
- Context assembly and compaction at inference time (separate context-engineering RFE).

## Open Questions

- Which built-in curation behavior ships as the default, and how is the quality bar validated before Tech Preview?
