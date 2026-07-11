---
rfe_id: RHAIRFE-2630
title: Framework-agnostic agent memory service for AI agents on OpenShift AI
priority: Normal
size: L
status: Submitted
parent_key: null
original_labels: null
---
**Parent Outcome:** [RHAISTRAT-1345](https://redhat.atlassian.net/browse/RHAISTRAT-1345) (Agent Memory)

## Summary

Agent developers on OpenShift AI need a platform-provided memory capability: agents store what they learn during interactions and recall it in later sessions, working consistently across agent frameworks and harnesses, with storage that platform operators can configure for their environment. Today every agent team builds its own memory plumbing per framework, and an agent's accumulated memory is lost when the team changes frameworks.

## Problem Statement

There is no convergence on what good agent memory looks like on OpenShift AI (discovery signal, Feb-Mar 2026). Every agent team reinvents conversation state and long-term persistence as custom, per-framework code. The results, from the user's perspective:

- Duplicated effort: each team writes and maintains its own storage and recall logic before it can build anything useful.
- No portability: memory is welded to the framework it was built in. Switching models is cheap; switching memory is not. Teams stay locked to a framework because leaving it means losing what their agents have learned.
- Ad hoc storage: teams pick whatever store is at hand, with no path to the storage their production environment actually supports (including disconnected and air-gapped clusters).

Current workaround is hand-rolled files or databases per team, invisible to the platform.

## Affected Customers

- **Infineon**: runs AutoGen, LangChain, and LangGraph simultaneously and needs one platform capability that works across all three rather than three parallel integrations.
- **ITZBund** (German federal IT, ~900 GPUs) and **BNP Paribas**: require self-hosted and disconnected deployments, so any memory capability must run in their environment on storage they control.
- Broad pipeline interest: sales teams consistently ask when OpenShift AI delivers agent memory; a small set of accounts is explicitly requesting an implementation (details on file with the PM).

## Business Justification

- Agent memory is part of the agentic-theme strategic investment tracked by RHAISTRAT-1345: agents that cannot remember cannot deliver the multi-session, multi-step enterprise workflows the agentic strategy is selling.
- Competitive whitespace: hyperscaler memory offerings (AWS AgentCore, Google Memory Bank, OpenAI) are GA but cloud-only; Oracle's requires Oracle Database; OSS memory startups are governance-thin with real consolidation risk (~$62M across five-plus startups converging on the same designs in 18 months). No vendor today combines enterprise readiness, Kubernetes-native self-hosted deployment, air-gap support, and an open interface. That combination is exactly Red Hat's profile.
- Betting on any single startup product risks picking a non-survivor; a platform capability with configurable backends protects customers from that consolidation.

## User Scenarios

1. As an AI engineer, I build an agent in LangGraph and later move it to OpenClaw; the agent keeps its accumulated memories and behaves no differently after the switch.
2. As a platform engineer in an air-gapped environment, I enable memory using the storage my cluster supports (file-based to start, a vector database later) without agent teams changing any code.
3. As an AI engineer, my agent keeps working context during a task, recalls relevant past episodes, accumulates facts, and refines learned procedures through one consistent platform capability instead of four bolted-on mechanisms.

## Acceptance Criteria

- [ ] Agents can store and retrieve memories through a stable, documented platform capability without writing custom storage plumbing.
- [ ] The same agent memory works from at least three major agent frameworks/harnesses (for example LangGraph, CrewAI, OpenClaw), and switching an agent between them preserves its memories.
- [ ] Working, episodic, semantic, and procedural memory access patterns are supported over one governed store.
- [ ] Platform operators can choose the storage backend: a vector database and file-based storage at minimum, with the backend model open to future storage types such as graph stores; agents are unaffected by the backend choice.
- [ ] Retrieval combines semantic similarity and keyword matching so recalled memories are relevant to the agent's current task.
- [ ] The capability deploys self-hosted on OpenShift, including disconnected/air-gapped environments.

## Success Criteria

- An agent team can adopt platform memory in under a day without writing storage code.
- A framework migration retains 100% of stored memories.
- Dev Preview available in the RHOAI 3.6 timeframe, generating pilot-customer feedback that shapes Tech Preview (3.7) and GA (3.8) without throwing away delivered work.

## Scope

### In Scope
- Single-agent memory store and recall across sessions.
- Multi-framework client usage and framework-switch portability.
- Operator-configurable storage backends (vector, file; extensible).
- Hybrid (semantic + keyword) retrieval.

### Out of Scope
- Scope isolation, sensitive-data screening, and write auditability (separate RFE: governed memory writes).
- Exposure of memory as MCP tools (separate RFE).
- Automatic memory extraction, consolidation, and curation intelligence (planned follow-on RFE).
- Multi-agent shared memory (later phase, tracked under the Outcome).
- Org-wide Agent Knowledge / enterprise knowledge layer (separate Outcome).

## Open Questions

- Which frameworks/harnesses are first-class validated clients at Dev Preview versus documented-only?
- Naming: "agent memory as a service" is the working product framing; final naming needs PM/PMM alignment.
