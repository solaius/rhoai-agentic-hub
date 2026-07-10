---
title: "Market & direction refresh (July 2026)"
description: Quick-depth refresh — internal direction shift (standalone service, 3.6 DP → 3.7 TP → 3.8 GA), EU AI Act timing nuance (GPAI enforcement stands, high-risk deferral provisional), hyperscaler/startup moves, and MCP 2026-07-28 statelessness implications for memory-as-MCP.
timestamp: 2026-07-10
lens: landscape
review_after: 2026-09-10
---

# Market & direction refresh (July 2026)

Quick-depth refresh (`hub.research agent-memory refresh quick`,
2026-07-10): one inline pass, ~8 sources, no fan-out. Internal signals
come from the filed 2026-06-30/07-07 meeting facts; MCP spec claims
reuse the adversarially verified findings from the mcp-catalog run
(2026-07-09). Confidence labels inline.

## 1. Internal direction shift (since the June 10 OGX-deprecation note)

Filed at intake 2026-07-10 — this doc records the research-series
consequences; detail in the
[1:1 fact](/features/agent-memory/knowledge/fact-agent-memory-1on1-paths-forward-20260630.md)
and the
[06-30](/features/agent-memory/knowledge/fact-agent-memory-team-sync-20260630-transcript.md) /
[07-07](/features/agent-memory/knowledge/fact-agent-memory-team-sync-20260707-transcript.md)
sync facts:

- **Standalone service**: agent memory decoupled from OGX *and* the AI
  Gateway (gateways are network devices; memory is database-shaped).
  This supersedes doc 16's premise that the gateway-native Responses API
  absorbs the memory substrate — supersede note added there. The
  substrate-agnostic API posture from REVIEW-NOTES (2026-06-10) is
  retained; the delivery vehicle is now "own service."
- **Phasing revised**: **3.6 = DP (deliberately, not TP) → 3.7 = TP (Feb
  2027, Summit 2027 setup) → 3.8 = GA.** Supersedes the "3.7+ GA" sketch
  in 00 §5. Org constraint: agent memory is not on leadership's 12-month
  priority list ("a 2027 topic"); scoped RFEs are the response.
- **Interim candidates**: Feast ruled out as interim memory by its own
  maintainer; the interim slot = OGX memory tool (server-side Responses
  tool call, dev-build shipped) + MemoryHub as the governance-layer
  leader. Multi-backend (vector + file, extensible to graph) is the
  stated substrate requirement — matching doc 08 §8's PostgreSQL+pgvector
  recommendation as *one* configurable backend, not "the" solution.
- **Workstream infrastructure**: official team repo
  ([opendatahub-io/agent-memory](/features/agent-memory/knowledge/ref-odh-agent-memory-repo.md)),
  "open everywhere" ruling, evaluation-criteria framework PR.

## 2. Compliance timing — the audit-trail forcing function nuanced

The series treats "EU AI Act enforcement August 2026" as the hard
deadline behind Q-G7 (audit trail). Current state [verified where
noted]:

- **GPAI enforcement stands**: Commission enforcement powers over GPAI
  providers (incl. fines) apply from 2025-08-02 obligations with
  enforcement from **2026-08-02** [multiple trackers agree].
- **High-risk (Annex III) deferral is PROVISIONAL**: the Digital
  Omnibus (provisional agreement 2026-05-07) would defer the Annex III
  deadline from 2026-08-02 to **2027-12-02** — but formal adoption and
  Official Journal publication are pending; **until publication the
  original dates remain binding law** [reported — secondary trackers
  (Legiscope, Trilateral); the canonical FLI timeline page predates the
  Omnibus. Confirm adoption status at next refresh.]
- **Implication for Q-G7**: if adopted, the deferral relieves the
  hardest external date pressure on the audit trail — but does NOT
  change the conclusion: finding 21 (all six enterprise verticals
  independently require audit trails) and GPAI transparency obligations
  keep audit/inspectability GA-gating on customer grounds, merely with
  more sequencing room for the 3.6 DP.

## 3. Market moves since June

- **Vertex AI Memory Bank → GA** (sessions + Memory Bank; now "Agent
  Platform Memory Bank" under the Gemini Enterprise rebrand), with
  **Memory Revisions** (preview): immutable versioned snapshots of every
  memory create/update/delete with an inspection API [reported — Google
  release notes + docs]. Notable: a hyperscaler shipping memory
  *versioning/inspectability* — the exact property the series argues is
  compliance-critical (findings 10, 13). The hyperscaler camp's
  governance gap is narrowing.
- **Mem0**: April 2026 token-efficient algorithm (single-pass
  hierarchical extraction; largest gains on temporal +29.6 and multi-hop
  +23.1 vs their old algorithm) [reported — vendor blog]; claims
  "exclusive memory provider for AWS's Agent SDK" and 186M API calls in
  Q3 2025 [reported — vendor]; 21-framework integration surface. Total
  funding $24M (Oct 2025). Consolidation-risk finding 5 unchanged; Mem0
  is the strongest consolidation candidate.
- **Perplexity "Brain"** [reported — secondary coverage]: continuously
  learning context graph in the Computer agent — records successful AND
  failed outcomes plus corrections, consolidates overnight, feeds
  subsequent tasks; claimed 95% recall (Feb 2026), +25% accuracy on
  history-dependent tasks. Validates two series positions at production
  scale: dream-style async consolidation (finding 17) and
  outcome-weighted episodic memory — the exact thread from the 06-30
  sync (bad outcomes weighted more; async curation agent).
- **MemPalace** [reported — thin sourcing, personal-blog tier]: local
  MIT-licensed memory claiming 96.6% R@5 on LongMemEval with zero API
  calls, v3.4.0 (2026-06-06). Watch-list only until independently
  verified; if real, strengthens the local/self-hosted memory camp.

## 4. Standards — MCP statelessness hits memory-as-MCP

Reusing verified findings from the mcp-catalog run (2026-07-09):

- The MCP spec's largest-ever revision finalizes **2026-07-28**:
  streamable HTTP becomes stateless — `initialize` handshake and
  **`Mcp-Session-Id` removed**, mandatory `server/discover`, SSE
  resumability removed, OAuth DCR deprecated [verified].
- **Consequence for finding 16 (memory-as-MCP)**: a governed memory
  service exposed as an MCP tool can no longer lean on protocol-level
  session identity for working/episodic scoping — session keying must
  live in the memory service's own data model (conversation/actor IDs in
  tool arguments or auth claims). This strengthens the case for
  memory-native scope identity (MemoryHub-style tiers, `AuthorizedSqlStore`
  ABAC) and for the RFE-M5 design to define its own session semantics.
  Feeds
  [question-agent-memory-protocol-standardization](/features/agent-memory/knowledge/question-agent-memory-protocol-standardization.md).
- MCP now governed by the Linux Foundation's Agentic AI Foundation
  (since 2025-12-09) [verified] — the doc-05 §6.2 "AAIF memory project"
  path now has a concrete foundation door to knock on. Still **no memory
  standard**; the opportunity window (finding 9) remains open.

## 5. What this changes in the series

| Series item | Status after this refresh |
|---|---|
| 00 §5 phasing ("3.7+ GA") | Superseded — 3.6 DP → 3.7 TP → 3.8 GA (see §1) |
| Doc 16 premise (gateway absorbs substrate) | Superseded — standalone-service direction (note added in 16) |
| Q-G7 hard-date framing (Aug 2026) | Nuanced — GPAI enforcement stands; Annex III deferral provisional (see §2) |
| Finding 5 (consolidation risk) | Unchanged; Mem0 strongest |
| Findings 10/13 (inspectable compaction/audit) | Strengthened — hyperscalers now shipping memory versioning |
| Finding 16 (memory-as-MCP) | Sharpened — spec statelessness moves session identity into the memory service |
| Finding 17 (dream consolidation) | Validated at production scale (Perplexity Brain) |
| Docs 02/08 solution-survey rows | Not edited this pass — hyperscaler updates recorded here; fold into doc 02 at the next standard-depth refresh |

## Sources

Web (this pass): legiscope.com + trilateralresearch.com EU AI Act
timelines, artificialintelligenceact.eu implementation timeline
[fetched — predates Omnibus], docs.cloud.google.com Memory Bank overview
[fetched] + Gemini Enterprise Agent Platform release notes, mem0.ai
state-of-memory blog, supermemory.ai + explainx.ai Perplexity Brain
coverage, rohitraj.tech MemPalace note. Internal: the three 2026-06-30/
07-07 meeting facts (intake `daaef27`). Reused verified: mcp-catalog
research 01 (2026-07-09) for MCP RC + AAIF claims.
