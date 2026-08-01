---
type: reference
title: Oracle AI Agent Memory (competitive blog)
description: Oracle's oracleagentmemory — a framework-agnostic governed memory core on Oracle AI Database, with a four-type access-pattern taxonomy.
resource: https://blogs.oracle.com/developers/oracle-ai-agent-memory-a-governed-unified-memory-core-for-enterprise-ai-agents
tags: [agent-memory, competitive, oracle]
timestamp: 2026-07-06
source: ai-asset-registry/docs/knowledge-registry.md §12 (as of 2026-07-05); benchmark detail from ai-asset-registry/docs/knowledge-review/assets/agent-memory-knowledge.md §4 (as of 2026-07-05)
---
Author: Richmond Alake, 2026-05-01. Frames working/semantic/episodic/procedural memory as four access patterns over one substrate: short-term threads with summaries/context cards, long-term durable memories with vector search, automatic LLM extraction, multi-tenant isolation, audit/erasure primitives. Competitive reference point for Red Hat's own memory taxonomy debate — see the old registry's §13 open question on whether Peter's 3-area split holds up against this 4-type model.

**Published benchmark claims** (Oracle's own numbers, not independently verified): LongMemEval 93.8% (469/500) — 100% single-session recall, 96% temporal reasoning, 95% knowledge-update, 88% multi-session (the hardest category). Cost/context management: periodic thread summarization plus prompt-time compaction held an 80-turn conversation flat at ~1,300 tokens/request vs. a flat-history baseline growing past 13,900 (~9.5x) over the same run; an impartial judge scored the summarized approach 48 wins to 13 (19 ties) over flat-history on that same run, on the reasoning that "a retrieved context card focuses the model; a sprawling transcript dilutes attention." Cost is framed as a tunable knob via the summarization-trigger threshold.
