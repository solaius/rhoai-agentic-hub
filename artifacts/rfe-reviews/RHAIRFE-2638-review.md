---
rfe_id: RHAIRFE-2638
score: 10
pass: true
recommendation: submit
feasibility: feasible
needs_attention: true
needs_attention_reason: Assessor scored right-sized 2/2, but the feasibility review
  recommends splitting into three separable capability areas plus a benchmark and
  calls the M estimate optimistic; no platform component currently owns agent memory/context
  engineering, so the owner/home is undecided.
scores:
  what: 2
  why: 2
  open_to_how: 2
  not_a_task: 2
  right_sized: 2
auto_revised: false
error: null
before_score: 10
before_scores:
  what: 2
  why: 2
  open_to_how: 2
  not_a_task: 2
  right_sized: 2
---
## Assessor Feedback

TITLE: Inspectable context engineering for long-running agents

| Criterion | Score | Notes |
|-----------|-------|-------|
| WHAT      | 2/2   | The need is clear and specific: context handling for long-running agents that keeps sessions coherent, automatically assembles relevant memory into the context window, and is inspectable end to end so an engineer or a reviewer can see exactly what the agent knew when it acted. The problem (silent quality decay past context limits, opaque compaction, growing token cost) and the desired outcome are both stated concretely. |
| WHY       | 2/2   | Named customer accounts drive it: SAS, BNP Paribas, and ITZBund (the regulated cohort, cross-referenced to RHAIRFE-2633/2635) whose reviewers must reconstruct agent decisions — a concrete customer consequence tied to this specific capability. Reinforced by every long-horizon pilot from the 3.6 Dev Preview being the accounts most exposed to the decay, plus a differentiation argument against industry opaque-by-default implementations and a measurable token-cost/sales story. Strongest evidence = named accounts with a clear causal chain to the read-side compliance need. |
| Open to HOW | 2/2 | Describes needs and observable outcomes, not architecture. Compaction "rather than silently lost," a "human-readable record" of what was kept/summarized/dropped, automatic memory assembly, reviewer reconstruction, and measured token efficiency are all outcomes — engineering is free to choose compaction algorithms, storage of the record, and assembly logic. vLLM and llm-d are named only as Red Hat's inference stack (platform/inference-optimization vocabulary), a cross-layer advantage claim, not a mandated internal design. No DB schemas, repos, or algorithmic techniques prescribed. |
| Not a task | 2/2  | This is a business need (compliance inspectability, quality preservation, cost efficiency), not a chore or tech-debt task. It would not make sense filed as an engineering task — the value is customer- and compliance-facing. |
| Right-sized | 2/2 | Deliverables: (1) quality-preserving compaction, (2) inspectable compaction record, (3) automatic memory assembly, (4) reviewer reconstruction of context, (5) measured token efficiency. Applying the independence test: (2) requires (1) to exist; (4) — reconstructing "what the agent knew when it acted" — requires seeing both what was compacted away (2) AND what was assembled in (3), so it binds (1)-(3) together; (5) is a measured quality bar on that work and cannot ship alone. The reconstruction requirement is the binding constraint that makes assembly and compaction inseparable facets of one context state. Final count: one independent group — a focused single need ("inspectable context engineering"), mapping cleanly to the parent Agent Memory Outcome (RHAISTRAT-1345). |
| **Total** | **10/10** | **PASS** |

### Verdict
A well-scoped, customer-grounded RFE that clearly states an inspectable-context need for long-running agents, backed by named regulated accounts and left fully open to engineering.

### Feedback
Strengths: the read-side compliance framing ties directly to named accounts (SAS, BNP Paribas, ITZBund) and the parent Outcome, and every acceptance criterion is phrased as an observable outcome rather than a technique, keeping HOW open. The five deliverables are genuinely interlocked through the reconstruction requirement, so the scope stays a single feature. Minor improvements: the "measured token-efficiency gains at equivalent output quality" criterion would be stronger with a target threshold or baseline (what counts as a win), and the reconstruction/inspectability criteria could name the retention or access expectation for the human-readable record so engineering knows how long it must be reproducible. Neither affects the score.

## Technical Feasibility

### RFE-011: Inspectable context engineering for long-running agents
**Feasibility**: feasible
**Strategy considerations**: (1) no existing platform component owns "agent memory" or "context engineering" — owner/home must be assigned; (2) the five acceptance criteria span three separable capability areas plus a benchmark, so M sizing is optimistic; (3) token-efficiency claims on vLLM/llm-d cross the RHAII engine boundary; (4) read-side inspectability must be reconciled with the write-side audit model in the governance RFEs (RHAIRFE-2633/2635); (5) automatic memory-into-context assembly implies a retrieval/relevance subsystem (embeddings + store) that is not specified; (6) per-response context reconstruction implies durable, tamper-evident context snapshots with retention and data-governance/multi-tenancy implications; (7) "equivalent output quality" requires a defined evaluation methodology (eval-hub / lm-evaluation-harness / TrustyAI EvalHub).
**Blockers**: none
**Scope assessment**: needs splitting — or, at minimum, the M estimate must be re-justified against the bundled scope

---

Overlays applied:
- 0015: OpenShell is the agent security runtime for RHOAI, replacing Kagenti (3.5/3.6/next)
- 0011: KServe LLMInferenceService + llm-d integration, incl. prefix-cache scoring and KV offloading (3.5/next)
- 0014: Model Runtimes team architecture / RHAII engine boundary for vLLM (3.4/3.5/next) — applied only for the vLLM ownership point
- 0008: platform policy — RHOAI does not auto-install external operator dependencies (all/platform) — considered, not material to this RFE

Release-matching note: the RFE targets RHOAI 3.7 Tech Preview, which is beyond the documented architecture context (3.5-ea.2). No overlay lists "3.7" explicitly, so overlays tagged `next` (the forward bucket) or `all` were treated as applicable to 3.7. This matters here because it keeps the agent-platform assessment on OpenShell (0015) rather than the deprecated Kagenti architecture still implied by the generated PLATFORM.md.

### Is it technically feasible?

Yes. Nothing in the platform architecture conflicts with building inspectable, quality-preserving context handling for long-running agents. Every requirement is an *extension* of existing primitives, not a fight with them:

- **Token efficiency on Red Hat's own inference stack is genuinely differentiated and already partly built.** llm-d ships the exact primitives the RFE leans on: `prefix-cache-scorer` / `precise-prefix-cache-scorer` (prefix reuse), the KV indexer, and `llm-d-kv-cache` tiered offloading (GPU HBM -> CPU RAM -> SSD) (overlay 0011). The claim that "efficient context assembly on vLLM/llm-d is a cross-layer advantage only the platform vendor can deliver" is architecturally credible — those layers exist and are Red Hat-led.
- **Inspectable/non-opaque compaction has no architectural obstacle.** A human-readable "kept / summarized / dropped / when" record is a data-and-storage problem, not an architecture conflict. It aligns with the platform's existing governance/observability direction (TrustyAI, audit).
- **The agent runtime exists.** OpenShell (overlay 0015) provides the sandboxed agent execution environment, SPIFFE identity, OPA policy, OCSF security events, and inference routing/credential injection. It is the runtime an agent-memory capability would sit alongside.

A capability not existing yet is exactly what an RFE is for, so absence of a shipped "agent memory" component is not a feasibility problem.

### Architectural incompatibilities

None. The requirement does not require re-architecting any component. The only structural gap is *ownership*, not *compatibility*: there is no component in the 3.5-ea.2 inventory whose charter is agent memory or context engineering. Note that OpenShell — despite being the agent platform — explicitly scopes to sandboxing, policy, identity, and inference routing; it does **not** provide memory or context management (overlay 0015). So this capability is net-new surface, not an add-on to an existing owner.

### Alignment with technical strategy

Strong. The platform is actively expanding from ML serving into agentic infrastructure (OpenShell agent runtime, OGX agent/inference server with pluggable providers per overlay 0003, RHOAI MCP Server, the `ai4rag` component). Agent memory is a natural next layer. Inspectability aligns with the compliance/governance thrust the parent Outcome leads with, and token efficiency aligns with the heavy llm-d investment. This goes with the grain of the architecture.

### Scope realism

This reads larger than an "M." The acceptance criteria bundle at least three separable capability areas plus a measurement deliverable:

1. **Compaction** — quality-preserving summarize-not-lose behavior past the context limit.
2. **Inspectability / audit** — a durable, human-readable record of what was kept/summarized/dropped and when, and per-response reconstruction of the context the agent saw.
3. **Memory retrieval + assembly** — automatically pulling "relevant memories" into context "at the right moments" (a relevance/retrieval subsystem: embeddings, a store, and a policy for when to inject).
4. **Token-efficiency benchmark** — a published measurement of efficiency gains *at equivalent output quality*, which presupposes an agreed quality-evaluation methodology.

Any one of (1)-(3) is plausibly its own strategy feature. Delivering all four, cross-layer, to a credible Tech Preview is more than an M typically implies. Recommend splitting (compaction/inspectability vs. retrieval-assembly vs. the efficiency-at-quality benchmark) or, at minimum, re-justifying the M estimate. Flagging as a scope risk rather than a blocker.

### Hidden complexities to carry into /strat.refine

- **Undefined owner/home.** No shipped component owns agent memory/context engineering. OGX (formerly Llama Stack — an HTTP server with pluggable providers, overlay 0003) and the `ai4rag` leaf component are the nearest existing homes for retrieval/assembly, and llm-d owns the caching primitives — but the RFE names none of these and assigns no team. The owning component and cross-team split must be decided in strategy.
- **Cross-layer token-efficiency ownership.** The vLLM engine (prefix caching, KV behavior) is **RHAII** scope, not Model Runtimes (overlay 0014); llm-d KV/prefix components are separate upstream repos (overlay 0011); the agent-memory layer that decides *what* to assemble is a third owner. The "measured token-efficiency gains on vLLM/llm-d" criterion therefore implies coordination across RHAII, the llm-d components, and whoever owns the memory layer. This coordination is not acknowledged in the RFE.
- **Read/write inspectability consistency.** The RFE frames this as the "read-side completion" of the governance story and ties itself to RHAIRFE-2633/2635 (memory-write inspectability, SAS/BNP Paribas/ITZBund). The read-side audit record and the write-side audit record need a consistent model, retention policy, and access-control story; divergence here would undercut the compliance value proposition. Cross-RFE dependency.
- **Durable per-response context snapshots.** "Reconstruct what context an agent had when it produced a given response" implies persisting the assembled context (or enough to reconstruct it) per response, tamper-evidently, for the review window. That is a storage, retention, tenancy, and data-sensitivity problem — the captured context can contain regulated/PII data, so the audit store itself inherits the governance requirements it is meant to satisfy.
- **"Equivalent output quality" needs a methodology.** Both the acceptance and success criteria hinge on holding quality "at equivalent output quality" / "past the context limit." That requires a defined long-session evaluation harness and a quality metric. The platform has eval-hub, lm-evaluation-harness, and TrustyAI EvalHub, but agreeing the evaluation methodology (and what "equivalent" means) is itself non-trivial and is a prerequisite for the measurable criteria to be testable.
- **"At the right moments" is unbounded.** Automatic assembly "without the engineer hand-building context" is a relevance-and-timing problem that can expand significantly (semantic retrieval quality, ranking, injection triggers). If left unspecified it is a scope-inflation vector.
- **Platform policy check (0008).** If any part of the retrieval/assembly subsystem leans on an external operator (e.g., a vector store operator), RHOAI will not auto-install/manage it — it must be a documented prerequisite. Not a blocker, but a constraint strategy must respect.

## Strategy Considerations

Flagged for /strat.refine:
- **Owner/home assignment.** No shipped 3.5-ea.2 component charters agent memory / context engineering; OpenShell scopes to sandboxing/identity/routing only. Nearest existing homes are OGX and the `ai4rag` leaf (retrieval/assembly) and llm-d (caching primitives). The owning component and cross-team split must be decided.
- **Scope vs. sizing.** The five acceptance criteria bundle three separable capability areas (compaction/inspectability, memory retrieval+assembly, and the efficiency-at-quality benchmark). The M estimate reads optimistic; either split or re-justify M.
- **Cross-layer ownership for the token-efficiency claim.** vLLM engine work is RHAII scope; llm-d KV/prefix components are separate upstream repos; the memory-assembly layer is a third owner. The "measured gains on vLLM/llm-d" criterion needs explicit cross-team coordination not yet acknowledged.
- **Read/write inspectability model.** Reconcile the read-side audit record with the write-side model in RHAIRFE-2633/2635 (shared retention and access-control story) so the compliance value proposition holds together.
- **Durable per-response context snapshots.** Tamper-evident persistence of assembled context inherits data-governance, retention, tenancy, and PII/regulated-data requirements — the audit store must itself satisfy the governance it enables.
- **Evaluation methodology.** "Equivalent output quality" requires an agreed long-session eval harness and quality metric (eval-hub / lm-evaluation-harness / TrustyAI EvalHub) before the measurable criteria are testable.
- **Bounding "at the right moments."** Automatic relevance/timing of memory injection is a scope-inflation vector if left unspecified.
- **External-operator constraint (policy 0008).** Any vector-store or similar operator dependency must be a documented prerequisite; RHOAI will not auto-install it.

## Revision History

none
