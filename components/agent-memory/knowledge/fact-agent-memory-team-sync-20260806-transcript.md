---
type: fact
title: "Agent Memory Team sync (2026-08-06)"
description: Hindsight disqualified (Vectorize CEO rejected governance + schema standardization), MemoryHub Claude+OpenClaw cross-agent demo, specification-first strategy proposed, context pollution security risk raised, 70/30 MemoryHub investment split, dogfooding plan.
tags: [agent-memory, meeting, competitive, architecture]
timestamp: 2026-08-07
source: meeting transcript 2026-08-06 (work/transcripts/, local); participants Bill Murdock, Josh Salomon, Peter Double, Sanjeev Rampal, Wes Jackson
---

42-min weekly sync. Highlights:

- **Hindsight (Vectorize) disqualified**
  ([decision](/components/agent-memory/knowledge/decision-hindsight-vectorize-disqualified.md)):
  Sanjeev had a 1:1 with the Vectorize CEO. Explicit rejection of
  multi-vendor governance ("no benefit to our company"), AND of schema
  interop standardization ("not interested at the moment"). VC-backed
  monetization model incompatible with Red Hat's open governance
  requirement. Same pattern as Mem0 (SaaS-first, limited open source).
  Bill: "they don't want to work with us is disqualifying." GBrain (Visa)
  similarly single-vendor, personal-AI-first. No evaluated competitor is
  open to multi-vendor governance.
- **MemoryHub demo** (Sanjeev): Claude Code + OpenClaw (two separate
  machines, two different LLMs) sharing memories through MemoryHub on an
  OpenShift cluster. RBAC-isolated by default, shared when opted into a
  project scope. OpenClaw plugin v2 (npm `@memory-hub/openclaw-plugin`,
  0.1.3) shown. Four agents (Claude Code, Hermes, OpenClaw, Pips Agents)
  demonstrated sharing in Wes's security-operations-center demo.
- **Specification-first strategy** (Wes): proposed writing a formal
  specification for what a platform-level memory system needs to do
  (store, retrieve, scope, provenance), potentially submitting through
  Linux Foundation. MemoryHub as the reference implementation. Bill
  endorsed. Sanjeev: OKF is limited to file-based memory; these threads
  (spec, community, product) should progress in parallel. See
  [question](/components/agent-memory/knowledge/question-agent-memory-protocol-standardization.md).
- **Context pollution risk** (Josh Salomon): in multi-agent swarms, an
  agent can leak privileged memories to sub-agents via the initial
  prompt -- not just via shared memory. Requires fine-grained token-style
  controls (analogy: GitHub personal access token scopes, not a single
  on/off switch). Bill agreed: absolute isolation kills the value of
  institutional memory; the hard problem is selective sharing.
- **Memory provenance** (Wes): agent security projects (Praxis, OSAC,
  Sago) recognizing memory as a strong injection path -- memory tainted
  by default. Provenance solvable if the system writes metadata
  deterministically (not the agent). Links to Wes's
  [ptc-gal-standards](/components/agent-memory/knowledge/ref-ptc-gal-standards-repo.md)
  project on agent provenance and authority granting.
- **Cold-start evaluation problem** (Peter): memory systems need weeks
  of use before they perform well; first-session evaluation is
  misleading. Needs migration tooling ("Migration Toolkit for Memory")
  to avoid vendor lock-in and enable fair A/B comparison.
- **Dogfooding plan**: multiple internal setups planned (MemoryHub,
  Hindsight, GBrain) for feature comparison and quantitative
  token-savings measurement. Repo now contribution-ready (issues open,
  contribution process added).
- **Investment split** (Sanjeev): 70% MemoryHub, 30% watching other
  projects. Not dropping the ball on alternatives but MemoryHub is the
  primary investment.
- **Harness configuration** (Wes): `memory-hub config init` sets up
  Claude Code integration (CLAUDE.md section + .claude/rules/); hook-
  based startup option loads all project memories on session start.
  Opus 4.6 follows instructions well; other models may ignore MemoryHub
  in favor of their own memory systems.
