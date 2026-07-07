---
title: Agent Memory Workstream — Task Breakdown
description: Structured task breakdown organizing the Agent Memory team's candidate work items (from the first team sync, 2026-06-09) against the RHAISTRAT-1345 Outcome and RFE roadmap.
source: ai-asset-registry/agent-memory/workstream-tasks.md (as of 2026-07-05)
timestamp: 2026-07-06
review_after: 2026-08-05
---

# Agent Memory Workstream — Task Breakdown

**Purpose:** Organize the candidate tasks and categories identified by the Agent Memory team into a structured work plan, expanded with discussion context from the first team sync (2026-06-09). Each item maps back to the RHAISTRAT-1345 Outcome and the existing [RFE Roadmap](/features/agent-memory/strategy/rfe-roadmap.md).

**Date:** 2026-06-09

**Jira Outcome:** [RHAISTRAT-1345 — Agent Memory Primitives](https://redhat.atlassian.net/browse/RHAISTRAT-1345) (Status: New, Assignee: Sanjeev Rampal, Reporter: Adel Zaalouk, Labels: 3.6-candidate, agentic-theme)

**Source Documents:**
- [Agent Memory Team Sync Transcript](https://docs.google.com/document/d/1hJh7qqgWZiCUMEaxHt1pxNxFpPv5uwcQOjBpX_Wp_Qk/edit)
- [Agent Memory Team Notes (Ongoing)](https://docs.google.com/document/d/1_OqkVGVTdWHK7pLD9k3J5nH6JNMrk9FvgALJCH3ZC-E/edit)

**Team:**
- **PM Lead:** Peter Double (driving RFEs, customer engagement, strategy)
- **PM (Agentic Strategy):** Adel Zaalouk (sponsor alignment, joining periodically)
- **OCTO/ET Coordination:** Sanjeev Rampal (task prioritization, meeting coordination)
- **OCTO/ET Research:** Ben Capper, Ray Carroll, Kateryna Romashko
- **MemoryHub / SSA:** Wes Jackson (MemoryHub prototype, customer engagement)
- **Initiative Lead:** Ryan Cook (OCTO initiative owner)
- **Engineering Sponsors Needed:** Bill Murdock, Ann Marie Fred (AI Engineering)

**Slack:** #wg-agent-memory

**Cadence:** Tuesdays 11:30 AM ET (weekly/biweekly TBD)

**Related Repos:**
- [ai-asset-registry/agent-memory](https://github.com/solaius/ai-asset-registry/tree/main/agent-memory) — strategy, research, RFE roadmap
- [redhat-ai-americas/memory-hub](https://github.com/redhat-ai-americas/memory-hub) — MemoryHub prototype + research folder

**Related Jira:**
- [RHAISTRAT-1349](https://redhat.atlassian.net/browse/RHAISTRAT-1349) — Work with General Purpose Agents: Runtime Compatibility (Adel's agent validation tracking)

---

## How This Relates to the RFE Roadmap

The candidate tasks below are **research and pre-RFE work** — they feed the evidence base, design decisions, and engineering buy-in needed before the [RFE Roadmap](/features/agent-memory/strategy/rfe-roadmap.md) items (RFE-M1 through RFE-M9) can move from PROPOSED to filed. Some tasks map directly to specific RFEs; others are cross-cutting research that informs multiple RFEs. The mapping is noted per task.

---

## 1. JIRA Tracking of Our Work

**Status:** In Discussion
**Owner:** Peter Double + Sanjeev Rampal

**What:** Decide on tracking mechanism for workstream tasks — Jira (under RHAISTRAT-1345), this document, GitHub Issues, or a combination.

**Context from sync:** Sanjeev proposed using the notes doc as informal tracking. Adel emphasized that Jira tracking matters for engineering buy-in: "we can create all the Jiras in the world, but if we don't have a good sponsor from AI Engineering, this work won't land." Peter plans to repurpose RHAISTRAT-1345 as the umbrella for the full memory solution, with child RFEs filed underneath.

**Decision needed:** Whether to use Jira actively from the start or rely on informal tracking until engineering sponsors are engaged. Consensus leaning toward lightweight tracking now, Jira when RFEs are ready to file.

**RFE mapping:** Prerequisite — enables all RFEs.

---

## 2. Agent Memory Primitives — RHAISTRAT-1345 Scope & RFE Filing

**Status:** Active — Peter drafting RFEs
**Owner:** Peter Double

**What:** Refine the RHAISTRAT-1345 Outcome scope and file child RFE/STRAT tickets for the individual memory capabilities.

**Context from sync:** Peter has an RFE drafting session scheduled for the same day as the sync. The [RFE Roadmap](/features/agent-memory/strategy/rfe-roadmap.md) has 9 outlined RFEs (RFE-M1 through RFE-M9) ready to feed `/rfe.create`. Adel clarified the lifecycle: RFE → STRAT → Engineering (epics). Key requirement: need an AI Engineering sponsor (Bill Murdock or Ann Marie Fred) before STRATs can be picked up.

**Next steps:**
1. Peter to finalize and file RFEs under RHAISTRAT-1345
2. Identify and engage AI Engineering sponsor
3. Adel to connect Peter with engineering counterparts

**RFE mapping:** Direct — this IS the RFE filing process.

---

## 3. OpenClaw Memory Plugins and Options Analysis

**Status:** Started (initial work in ET blog)
**Owner:** OCTO/ET team (Ben Capper, Sanjeev Rampal)

**What:** Detailed analysis of OpenClaw's default memory capabilities vs. enhanced memory plugins. Differentiate scenarios where default file-system-based markdown memories are sufficient vs. when specialized plugins are needed. Extend to other harnesses (OpenShell, Hermes, Codex, Claude Code).

**Context from sync:**
- OpenClaw uses both file-system-based markdown AND a plugin architecture with tool calls (memory create/update/delete). OpenClaw also uses hooks for memory operations (Wes).
- Hermes has its own philosophy around memory. Claude Code has memory primitives but not explicitly labeled as such. OpenAI's approach is largely server-side.
- Adel: "memory in the context of OpenClaw is very different than Claude Code" — need to understand these differences before designing abstractions.
- Wes: "we should have a broad survey because if we allow ourselves to get dragged down a specific rathole, we'll end up designing with unintended influences."

**Key questions:**
- What do you get with just built-in file-system-based plugins?
- When do you need Mem0, MemoryHub, or similar enhanced solutions?
- What is the granularity of pluggability? (e.g., could you bring your own dreaming solution?)
- How do hooks vs. tool calls vs. native APIs differ across harnesses?

**RFE mapping:** Informs RFE-M2 (framework-agnostic API design), RFE-M9 (client-side hybrid path).

---

## 4. Alignment with Red Hat's Enterprise Claw Plan / Architecture

**Status:** Needs alignment
**Owner:** Peter Double + Adel Zaalouk

**What:** Ensure memory architecture aligns with Red Hat's enterprise agent harness strategy. Red Hat is planning to support multiple harnesses (OpenClaw, Hermes, Codex, Claude Code, etc.) — the memory solution must work across all of them.

**Context from sync:**
- Peter: "It's more about the plumbing around them, not a specific claw itself, but being able to have memory solutions that could work for those... in a governed way, centralized for management."
- Adel: "Are you going to build a new memory abstraction, or show how to connect existing memory abstractions such that they are optimized for KV caches, our runtime (vLLM)?"
- Two strategic approaches identified:
  1. **Intrude into the harness** — provide own abstraction layer (higher control, more work)
  2. **Connect existing abstractions** — take what exists in each harness and optimize for Red Hat's stack (lower friction, less control)
- Adel: "either way, we need to build connective tissue from what customers are thinking about and then how to tie to the platform."

**Key decision:** Build a new memory abstraction vs. optimize existing harness memory for the Red Hat AI stack. This remains an open question.

**RFE mapping:** Core architectural decision — affects RFE-M2 (API design), RFE-M3 (governance layer).

---

## 5. Comparison of Agent Memory Solutions (Mem0 etc.)

**Status:** Started (initial comparison done for blog)
**Owner:** OCTO/ET team

**What:** Comprehensive feature comparison across agent memory solutions: Mem0, OpenViking, Letta, Zep/Graphiti, Cognee, MemoryHub, Claude's memory/dreaming, and others. Identify which are doing something genuinely innovative vs. functionally similar.

**Context from sync:**
- Wes on OpenViking: "actually pretty good but owned by ByteDance. A lot of customers would not be interested in a ByteDance product. Their plan is a SaaS business model, not a truly open community." Still fair game to examine since open-sourced.
- Mem0 has traction; does asynchronous memory processing (not at every turn — kicks off async process to decide what to retain).
- Need to look at Claude's recent memory features, including dreaming (offline curation algorithm).
- Sanjeev: "many of these things maybe functionally similar, but we should show some numbers."

**Deliverable:** Feature comparison matrix with innovation assessment, licensing/ownership risks, and community health evaluation.

**RFE mapping:** Informs RFE-M2 (API patterns), RFE-M3 (governance features from competitors).

---

## 6. Benchmarking Setup and Impact of Optimizations at Different Layers

**Status:** Not started
**Owner:** OCTO/ET team

**What:** Build the quantitative business case for sophisticated memory architecture. Benchmark workflows with and without memory optimization at different layers (session, retrieval, compaction, KV-cache).

**Context from sync:**
- Sanjeev: "Many of our customers right now are early enough, they'll say 'why do I need more complication if I just have some file system? That's good enough for me.' We have to sell the case by showing genuine performance improvement or quality improvement."
- Need to show: (a) quality improvement in long conversation results, (b) performance impact (latency, throughput), (c) token efficiency gains.
- Wes: KV-cache efficiency is uniquely important for Red Hat — "part of our selling point is vLLM/llm-d, how those things work together. Most implementations aren't doing cache optimizations at all."

**Key benchmarks needed:**
- Baseline: file-system memory only
- Enhanced: structured memory (Mem0-style, MemoryHub-style)
- Optimized: with KV-cache-aware ordering and compaction
- Multi-turn conversation quality metrics
- Token efficiency at quality thresholds

**RFE mapping:** Evidence base for RFE-M4 (inspectable context engineering), differentiator for all RFEs.

---

## 7. Evals — Long Conversation Quality (Separated from Benchmarking)

**Status:** Not started
**Owner:** TBD

**What:** Evaluation framework specifically for long-conversation and multi-turn memory quality — distinct from raw performance benchmarking. Focus on whether memories are actually *useful* and *correct* over time.

**Context from sync:** Separated from benchmarking in the candidate task list. The distinction matters: benchmarking measures speed/efficiency, evals measure *quality of recall and reasoning* with memory vs. without. This includes detecting context rot and memory degradation over extended conversations.

**Key evaluation dimensions:**
- Memory recall accuracy over N turns
- Contradiction detection rate
- Context rot measurement (quality degradation over time)
- Memory curation effectiveness (useful memories retained, noise discarded)

**RFE mapping:** Quality evidence for RFE-M3 (governance/curation), RFE-M4 (context engineering).

---

## 8. Multi-Agent Memory

**Status:** Design principle established, no implementation
**Owner:** Peter Double (direction), OCTO/ET (research)

**What:** Design and research shared memory across multiple agents — the team's agreed long-term north star.

**Context from sync:**
- Peter: "It's almost worth working backwards from that... that's where we need to land eventually. Multi-agent. But it doesn't mean that the path there doesn't go through single agent. We should always be focused on that longer goal... so we don't just get something in right now for single agent and then have to rework it."
- Sanjeev: "The real killer use case... is eventually getting towards the enterprise brain architecture. That's where the value of memory to an enterprise."
- Ray: Critical guardrails concern — "if you're sharing memory across agent processes, there's obviously a massive risk... memories bleeding across the boundary. There has to be some sort of broader guardrail."
- Wes: Healthcare scenario — multi-agent with shared memory for processing prior authorization claims. Other customers also heading toward multi-agent.

**Key design questions:**
- Scope isolation: which agents can see which memories?
- Memory bleeding prevention across security boundaries
- Shared vs. private memory partitioning
- Conflict resolution when agents write contradictory memories
- Performance implications of shared memory at scale

**RFE mapping:** Design driver for RFE-M3 (scope tiers), future RFEs beyond M9.

---

## 9. Alignment with RHOAI, OGX, Kagenti Architecture

**Status:** Partially started (research 08 covers OGX alignment)
**Owner:** Peter Double + OCTO/ET

**What:** Map how agent memory fits into the existing Red Hat AI platform stack (RHOAI, OGX, Kagenti, etc.). Identify what platform features already exist that memory can leverage vs. what needs to be built new.

**Context from sync:**
- Wes: "As we do this research, we should be flagging what features in Kagenti, or OGX, or existing OpenShift AI really enhance our ability to deliver... I think there's a lot we won't have to reinvent because we already have, like in Kagenti there is InspireAI, and if you need to write in a specific auth context you can already do that."
- Adel: "In the past we discussed this... we said we give you the primitives underneath in the platform. OGX gives you file/associate API, you can do retrieval, conversations, state management. But all these are plumbing. How do I map these to short-term memory, long-term memory, semantic memory, procedural memory?"
- Kagenti already has a memory plugin layer that MemoryHub can plug into (Wes).
- Francisco Arceo from engineering has already put some things upstream for OGX memory.

**Action items from notes:**
- "Add to research items: what features (now or roadmapped) of RHOAI, Kagenti, OGX, etc., make it easy to implement any of this?"

**RFE mapping:** Direct input to RFE-M1 (OGX baseline), RFE-M2 (API substrate selection).

---

## 10. Claude Memory Features Analysis (esp. Dreaming)

**Status:** Not started
**Owner:** OCTO/ET team

**What:** Deep analysis of Claude's memory features, especially the "dreaming" capability (offline memory curation/consolidation). Assess applicability to Red Hat's memory architecture and pluggability model.

**Context from sync:**
- Sanjeev: "Definitely need to look at Claude's recent memory features... they're making a big deal about their memory features including dreaming."
- Key question: "Should the dreaming solution be pluggable? Probably yes, because that's just an offline algorithm that curates memories. But then are those memories accessible via a standard API, so that any dreaming algorithm could work?"
- This connects to the pluggability granularity question — how fine-grained should the plugin architecture be?

**Deliverable:** Analysis of Claude's memory architecture, dreaming mechanism, and recommendations for how Red Hat could offer similar capabilities in a pluggable, open way.

**RFE mapping:** Design input for RFE-M3 (curation/governance layer — dreaming is a form of memory curation).

---

## 11. Enterprise Memory Features / Memory Hub Evaluation

**Status:** In progress (Sanjeev evaluating MemoryHub)
**Owner:** Sanjeev Rampal, Wes Jackson

**What:** Critical evaluation of MemoryHub as the candidate governance architecture. Determine whether it should become the team's reference architecture (in current or evolved form).

**Context from sync:**
- Sanjeev: "We haven't yet decided whether MemoryHub is our architecture, but obviously it has lots of good pieces so we would love to make it our architecture. But that's a decision we need to make together."
- MemoryHub strengths: OpenShift-focused from the start, RBAC features, tenancy features, MCP server interface, scope isolation.
- Open question: Does MemoryHub in its current form allow enough for other industry plugins (Mem0, etc.)?
- Wes: MemoryHub as personal project, but "open to us making it a team project."
- Currently at prototype stage; needs evaluation against the full requirements set.

**Decision needed:** Formally adopt MemoryHub (as-is or evolved) as the reference governance architecture vs. build fresh or adopt alternatives.

**RFE mapping:** Direct input to RFE-M3 (MemoryHub-derived governance layer).

---

## 12. Memory Types Analysis: File System vs Vector DB vs PostgreSQL

**Status:** Partially covered in research (research 04, 07)
**Owner:** OCTO/ET team

**What:** Analysis of storage backend trade-offs for different memory types. When is each appropriate, and what does the Red Hat stack prefer?

**Context from sync:**
- Wes: "The things that don't matter to the agent — like what's the specific database flavor, is it Postgres, is it Neo4j — the agent doesn't care. Things that DO matter: token efficiency, KV-cache efficiency."
- MemoryHub uses PostgreSQL + pgvector (relational/vector/graph in one).
- Carpathy-style implementations are "just a bunch of markdown files."
- Need to determine: when is each approach appropriate, and what aligns with RHOAI's existing data services?

**RFE mapping:** Substrate decision for RFE-M2, RFE-M8 (re-home).

---

## 13. Trial Customer Engagement and Use Cases

**Status:** Active — several customers identified
**Owner:** Peter Double (PM), Wes Jackson (SSA)

**What:** Identify and engage initial customers with agent memory requirements to validate design and prioritize tasks.

Several customers across defense, healthcare, finance, IT, and other verticals have been identified with agent memory requirements ranging from multi-agent shared memory to context optimization.

> **Note:** Client names and engagement details are maintained in the [Agent Memory Team Notes (Google Doc)](https://docs.google.com/document/d/1_OqkVGVTdWHK7pLD9k3J5nH6JNMrk9FvgALJCH3ZC-E/edit) — refer there for the full customer list and status.

**RFE mapping:** Customer evidence for all RFEs, prioritization input.

---

## 14. OpenShift Product Alignment — 2026 Deliverables

**Status:** Peter has initial list, needs team input
**Owner:** Peter Double

**What:** Define concrete deliverables for 2026 that can land in RHOAI releases, working backward from what engineering can absorb.

**Peter's 2026 Phase 1 candidates (from sync):**
1. **Surface OGX memory baselines** — make sure OGX memory primitives are fully featured and surfaced → *maps to RFE-M1*
2. **Framework-agnostic governed memory API** — API layer around memory, something like MemoryHub-derived → *maps to RFE-M2*
3. **Governance and scope layer** — governable memory "slot" → *maps to RFE-M3*
4. **Inspectable context engineering capabilities** — ability to see and manage context → *maps to RFE-M4*
5. **Memory over MCP** — tool calls via MCP server for memory operations, CLI capability → *maps to RFE-M5*
6. **AI Asset Registry integration** — memory as a governed asset, viewable alongside MCPs, models, prompts → *maps to RFE-M5*
7. **UI presence in OpenShift AI dashboard** — surface memory in Gen AI Studio / AI Hub → *new — not in current RFE roadmap as standalone*

**Context from sync:**
- Adel: "RHOAI 3.6, 3.7 timeframe" for initial deliverables.
- Need AI Engineering sponsor (Bill Murdock / Ann Marie Fred) to validate feasibility and commit engineering resources.
- Sanjeev: "We'll discuss this more when we have the OpenShift AI Engineering people join us."

**RFE mapping:** This IS the RFE roadmap — validates [rfe-roadmap.md](/features/agent-memory/strategy/rfe-roadmap.md).

---

## 15. Enterprise Use Cases Beyond Coding (RH ITOps, Workflows)

**Status:** Not started (beyond customer identification)
**Owner:** Peter Double + Wes Jackson

**What:** Explore memory use cases beyond coding agents — ITOps, healthcare workflows, financial services, enterprise knowledge management.

**Context from sync:**
- Wes's healthcare scenario: doctor reviewing SOAP notes, agent surfacing "this is the fifth patient in two weeks with this exact symptom cluster."
- Peter's enterprise brain vision: memory as backbone for "how the business works, how the business should act, how they achieve goals, how they fix problems."
- Peter's knowledge management insight from personal project (Luminth): graph knowledge management from canon facts down through beliefs, continuity checking — applicable to enterprise regulations, policies, rules.
- Agent self-healing will be a big part of this going forward.

**RFE mapping:** Long-term vision beyond current RFE scope; informs enterprise brain direction.

---

## 16. Existing Agent Harnesses vs. Write New Ones

**Status:** Not started
**Owner:** OCTO/ET team

**What:** Evaluate whether to work within existing agent harnesses' memory mechanisms or build new harness-level components.

**Context from sync:**
- This connects to task #4 (enterprise claw alignment) — the "intrude vs. connect" question.
- Adel's two approaches: (1) intrude into the harness and provide own abstraction, (2) take existing abstractions and optimize for Red Hat's stack.
- Wes: "We won't be able to realistically implement every memory model, but we can come up with an acceptable compromise — this is what the platform can provide."

**RFE mapping:** Architectural decision affecting RFE-M2, RFE-M9.

---

## 17. Multi-Modal Memory (Audio, Video Memories)

**Status:** Not started — long-term
**Owner:** TBD

**What:** Research memory capabilities for non-text modalities — audio transcriptions, video content, image context.

**Context from sync:** Listed in candidate tasks but not discussed in the meeting. This is a forward-looking research item as agents increasingly handle multi-modal inputs.

**RFE mapping:** Beyond current RFE scope — future directional.

---

## 18. Next ET Blog (Part 2 in Series)

**Status:** Planning
**Owner:** OCTO/ET team (Sanjeev Rampal coordinating)

**What:** Write a follow-up to the [first ET blog post](https://next.redhat.com/2026/06/01/from-context-to-dreams-architecting-memory-for-ai-agents/) incorporating team alignment, benchmarking results, and architectural direction.

**Context from sync:** The first blog was the team's initial published position. Part 2 should reflect the broader team's aligned view and include quantitative results from benchmarking efforts.

**RFE mapping:** Marketing/positioning — supports all RFEs.

---

## 19. Context Rot, Context Injection, and Adversarial Risks

**Status:** Identified as critical — not started
**Owner:** Peter Double (raised), Ray Carroll (guardrails perspective)

**What:** Research and mitigate negative scenarios: context rot (memory quality degradation over time), context injection (bad input contaminating shared memory), adversarial attacks on memory systems.

**Context from sync:**
- Peter: "We need to look at the negative... What about context rot? What about context injection? When you have agent shared memory, one bad input could destroy all of that."
- Peter: "How you're promoting context up the tiers, how you're making sure that what's being put in is judged correctly and not going to destroy your entire context management library."
- Wes: "Inspectable context engineering — there's so much packed in there. We need observability, manageability. Somebody has to deal with it when there's a conflicted memory or a classified data spill into memory."
- Ray: Guard rails for shared memory — "if we're talking about shared memory, you may have multi-agent processes where one agent is looking at health information in a very sandboxed environment... memories bleeding across the boundary."
- Peter: "How could someone break the system? In a multi-agent situation, you could really break a company."

**Key research areas:**
- Memory promotion/demotion policies (preventing garbage accumulation)
- Input validation and quality gates for memory writes
- Classified data spill detection and remediation
- Cross-boundary memory bleed prevention
- Adversarial memory injection attacks and defenses

**RFE mapping:** Critical input to RFE-M3 (governance/curation), RFE-M6 (audit trail).

---

## 20. Engineering Sponsor Engagement

**Status:** Action item — immediate
**Owner:** Peter Double + Adel Zaalouk

**What:** Engage AI Engineering sponsors to ensure workstream output lands in product.

**Context from sync:**
- Adel: "We need someone from Engineering to sponsor this work... If we don't have a good sponsor from AI Engineering, it's just to make sure this work is impactful."
- Candidates: Bill Murdock, Ann Marie Fred, Roland, or other staff engineers in AI Engineering.
- Adel: "We need everyone to be bought in before we build it, otherwise we build something the other party from engineering does not like."
- Add AI Engineering representative to recurring meeting.

**Next steps:**
1. Peter + Adel to identify and invite engineering sponsor
2. Add sponsor to Tuesday sync meetings
3. Present RFE roadmap for engineering feasibility validation

**RFE mapping:** Prerequisite — no RFE can move to STRAT without engineering sponsor.

---

## Priority Grouping

### Immediate (Next 2 Weeks)
1. **Engineering Sponsor Engagement** (#20) — prerequisite for everything
2. **RHAISTRAT-1345 RFE Filing** (#2) — Peter's active work
3. **JIRA Tracking Decision** (#1) — lightweight, enables coordination

### Near-Term (Next 1 Month)
4. **OpenClaw/Harness Memory Analysis** (#3) — active ET research
5. **Memory Solutions Comparison** (#5) — builds on existing blog research
6. **MemoryHub Evaluation** (#11) — Sanjeev actively evaluating
7. **RHOAI/OGX/Kagenti Alignment** (#9) — informs API design
8. **Customer Engagement** (#13) — Peter + Wes pursuing leads

### Medium-Term (1-3 Months)
9. **Enterprise Claw Architecture Alignment** (#4) — needs broader team input
10. **Benchmarking Setup** (#6) — quantitative evidence building
11. **Evals Framework** (#7) — quality measurement
12. **Claude Memory/Dreaming Analysis** (#10) — competitive research
13. **Context Rot / Adversarial Research** (#19) — negative scenario planning
14. **2026 Deliverables Alignment** (#14) — once engineering sponsor engaged

### Longer-Term (3+ Months)
15. **Multi-Agent Memory Design** (#8) — north star, baby-step approach
16. **Memory Types / Storage Analysis** (#12) — substrate decisions
17. **Enterprise Use Cases Beyond Coding** (#15) — vision expansion
18. **Harness Build vs. Adopt** (#16) — architectural decision
19. **ET Blog Part 2** (#18) — after benchmarking results
20. **Multi-Modal Memory** (#17) — future directional

---

## Sources

| Source | Used for |
|---|---|
| [Agent Memory Team Sync Transcript](https://docs.google.com/document/d/1hJh7qqgWZiCUMEaxHt1pxNxFpPv5uwcQOjBpX_Wp_Qk/edit) | Discussion context, quotes, decisions |
| [Agent Memory Team Notes (Ongoing)](https://docs.google.com/document/d/1_OqkVGVTdWHK7pLD9k3J5nH6JNMrk9FvgALJCH3ZC-E/edit) | Candidate task list, attendees, links |
| [RHAISTRAT-1345](https://redhat.atlassian.net/browse/RHAISTRAT-1345) | Jira Outcome for RFE filing |
| [RHAISTRAT-1349](https://redhat.atlassian.net/browse/RHAISTRAT-1349) | Related — agent runtime compatibility validation |
| [RFE Roadmap](/features/agent-memory/strategy/rfe-roadmap.md) | Existing RFE-M1 through RFE-M9 outlines |
| [Agent Memory Strategy](/features/agent-memory/strategy/agent-memory-strategy.md) | Strategic approach and architecture decisions |
| [ET Blog: From Context to Dreams](https://next.redhat.com/2026/06/01/from-context-to-dreams-architecting-memory-for-ai-agents/) | Team's published position |
| [MemoryHub repo](https://github.com/redhat-ai-americas/memory-hub) | Prototype + research folder |
