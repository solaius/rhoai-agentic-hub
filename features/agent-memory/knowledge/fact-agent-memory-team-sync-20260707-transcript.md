---
type: fact
title: "Agent Memory Team sync (2026-07-07)"
description: Francisco's OGX memory-tool demo (interim DP candidate), Feast ruled out as interim memory by its own maintainer, Mem0 engagement opened, MemoryHub gap list, and the "open everywhere" ruling.
tags: [agent-memory, meeting, architecture]
timestamp: 2026-07-10
source: meeting transcript 2026-07-07 (work/transcripts/, local); participants Bill Murdock, Francisco Arceo, Justin Sun, Khaled Sulayman, Nehanth Narendrula, Peter Double, Sanjeev Rampal
---

55-min weekly sync. Highlights:

- **OGX memory-tool demo**
  ([Francisco](/features/agent-memory/knowledge/person-francisco-arceo.md)):
  memory as another server-side tool call in the Responses API, built on
  the existing files/vector-stores/search plumbing — memory store +
  memory vector store, explicit "remember this" AND implicit
  auto-remember, ANN retrieval with an inherent precision/recall
  trade-off (reasoning may discard retrieved chunks). Shipped in the
  latest OGX dev build; SQLite-vec provider in the demo; multi-tenancy
  already hardened via the files/vector-stores API. Positioning: the
  **quickest interim path** — wireable into AI Hub with modest UI work by
  3.6 (possibly 3.5.x) as a Dev Preview, deliberately allowed to compete
  with the comprehensive solution ("intersecting dev-preview features are
  fine"). Not chat-completions capable today; could later satisfy
  Anthropic's memory-tool API. One-pager + demo upload promised.
- **Feast: out as interim memory.** Its own maintainer (Francisco): a
  feature store is for predictive-AI features — "just because it can
  doesn't mean it should"; Sanjeev concurs (proposed only if no interim
  options existed; there are now two). Zarecki absent (wedding) — his
  presentation may still happen, but the room's call was no.
- **Mem0 engagement opened** (Nehanth): meeting same day; three
  questions — why two codebases (self-hosted vs SaaS), self-hosted lacks
  multi-tenancy (add? collaborate?), maintainership/governance. Posture:
  listen mode, no commitments; gauge multi-vendor willingness (Francisco's
  caution: multi-tenancy IS their business — MLflow/Databricks economics
  don't transfer).
- **MemoryHub assessment** (Sanjeev): no major architectural gotchas;
  gaps are second-order — triggers/hooks are Claude-Code-centric (need
  skills/hooks for Codex, OpenClaw, OpenCode, LangGraph), missing prompt
  hooks (Mem0 has them). AI-Hub-ready and OpenShift-ready by design.
  "No community" reframed: ODH projects are implicitly single-vendor
  anyway; control of direction is the benefit; Jessica Forrester et al.
  to advise on broader community later — must not hold up 3.5.x/3.6.
- **Evaluation criteria framework**
  ([Khaled](/features/agent-memory/knowledge/person-khaled-sulayman.md)):
  PR opened on the team repo — licensing hard-criteria, quantitative
  measures, feature checklist; to merge with Peter's architecture-options
  v0.2 feature matrix; focus on the top 3–4 criteria.
- **"Open everywhere" ruling**: product requirements AND analysis live in
  the open GitHub repo (Peter + Bill Murdock aligned); Jira is
  customer-visible anyway.
- Logistics: sync likely moving to Thursdays; repo structure may be
  reshaped if MemoryHub is ported with commit history preserved.
