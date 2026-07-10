---
type: fact
title: "Agent Memory Team sync (2026-06-30)"
description: Team repo launched (opendatahub-io/agent-memory), configurable-backends consensus (vector + file, extensible), Wes's file-vs-DB guidance, the PII/governance gap, and the episodic outcome-evaluation thread.
tags: [agent-memory, meeting, architecture]
timestamp: 2026-07-10
source: meeting transcript 2026-06-30 (work/transcripts/, local); participants Jaideep Rao, Justin Sun, Kateryna Romashko, Nehanth Narendrula, Peter Double, Sam Schifman, Sanjeev Rampal, Wes Jackson
---

48-min weekly sync. Highlights:

- **Team repo live**:
  [opendatahub-io/agent-memory](/features/agent-memory/knowledge/ref-odh-agent-memory-repo.md)
  — starter issues opened, research/ + product/ folders, be conservative
  about committing (avoid dead pages). Research issues shareable by up to
  two people.
- **Architecture notes (Sanjeev)**: architects reluctant to grow OGX
  (Daniel Lezonka, chief architect under Anne-Marie, included); Responses
  API moving to AI Gateway; gateways are network devices while memory is
  database-shaped → keep memory decoupled from both; RAG still leans on
  OGX so a coexistence story is required; architecture doc in progress.
- **Backends consensus**: configurable storage is the requirement —
  vector DB + file system minimum ("enterprise brain" scale doubts on
  file-only approaches), Google's Open Knowledge Format + Karpathy
  LLM-wiki momentum acknowledged but "restrictive if the only format."
  Wes's practitioner rule: **files when humans must read/edit them
  (Markdown + YAML frontmatter); database for everything else**;
  postgres+pgvector covers temporal + similarity.
- **Memory types are retrieval-time concerns** (Wes): once in context,
  type doesn't matter to the model — types guide storage/retrieval
  decisions; heavy procedural accumulation should graduate into skills.
  Memory-types paper:
  [ref-wes-jackson-memory-types-doc](/features/agent-memory/knowledge/ref-wes-jackson-memory-types-doc.md).
- **Governance gap called out** (Wes/Sam): nothing in current approaches
  (LLM-wiki, Obsidian, Mem0) prevents PII/credit-card/classified data
  entering shared memory — PHI/HIPAA/federal exposure; echoes the series'
  governance findings.
- **Episodic outcome evaluation** (Sam + Wes): memories should carry
  outcome quality — bad outcomes weighted MORE (humans ~10x likelier to
  retain negative experience); async curation agent evaluates traces;
  outcome evals are domain-specific; Perplexity's episodic feature
  (successful-sequence tracking) cited as precedent.
- **OpenViking eval** (Kateryna): 3 layers (L0 abstraction / L1 summary /
  L2 raw); multi-agent shared-memory privacy is the open problem;
  extraction quality is LLM-dependent (local Llama hallucinated
  abstractions) — benchmark claims mostly reflect the extraction LLM, not
  the framework (Sanjeev's caveat).
- Staffing: Ben (Mem0+OpenClaw integration) on medical leave (~2 months);
  Ray back the following week. Comparison plan: 4–5 dimensions (community,
  coupling, memory-creation strategy, …) to structure project evaluations.
