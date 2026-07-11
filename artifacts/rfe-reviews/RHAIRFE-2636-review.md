---
rfe_id: RHAIRFE-2636
score: 10
pass: true
recommendation: submit
feasibility: feasible
needs_attention: true
needs_attention_reason: Passes 10/10 and is feasible with no blockers, but the feasibility
  scope assessment recommends right-sizing the 3.7 Tech Preview slice because the
  size-L RFE bundles six independently substantial capabilities — a delivery-scope
  concern the 2/2 right-sized rubric score (business-need coherence) does not capture.
scores:
  what: 2
  why: 2
  open_to_how: 2
  not_a_task: 2
  right_sized: 2
before_score: 10
before_scores:
  what: 2
  why: 2
  open_to_how: 2
  not_a_task: 2
  right_sized: 2
auto_revised: false
error: null
---
## Assessor Feedback

TITLE: Automatic memory creation and curation for agents

| Criterion | Score | Notes |
|-----------|-------|-------|
| WHAT      | 2/2   | Clear, specific need: AI engineers need self-maintaining memory — automatic capture during interactions, background consolidation (dedup/pruning), outcome-weighted episodic memory, provenance, pluggable curation, and capture-quality measurement — so long-running agents improve with use instead of accumulating noise. Problem statement and acceptance criteria describe concrete, observable behaviors. |
| WHY       | 2/2   | Strongest evidence is a strategic investment with a clear causal chain: RHOAI 3.7 Tech Preview "sets up the Summit 2027 announcement under RHAISTRAT-1345," and the specific capability is required because "every competing memory offering captures and consolidates automatically; a service that only stores explicit saves fails side-by-side evaluation." Reinforced by a customer consequence — accounts piloting the 3.6 Dev Preview whose most-used behavior is implicit auto-remember would "regress at Tech Preview" without it — plus accounts requesting agent memory on file with the PM. Matches the Y=2 strategic-investment-with-causal-chain pattern. |
| Open to HOW | 2/2 | Describes needs and observable outcomes, not internals. "Automatic capture," "consolidation," "outcome weighting," and "episodic memory" are domain vocabulary for the behaviors/need, not architecture. Pluggable curation is framed as a customer capability ("platform teams substitute their own approach"), not a mandated plugin architecture — engineering chooses the mechanism. Production precedent (outcome-weighted memory, scheduled consolidation) is explicitly framed as validating prior art/context, not as the mandated implementation; the need stands without it. No schemas, repos, or design docs prescribed. |
| Not a task | 2/2  | Clear business need — self-maintaining memory quality so long-running agents get better with use — not a chore, tech-debt item, or engineering activity. |
| Right-sized | 2/2 | Independent deliverables: (1) automatic capture, (2) background consolidation, (3) outcome weighting, (4) provenance visibility, (5) pluggable curation, (6) capture-quality measurement. Applying the independence test, all consolidate into one group: provenance shows origin of captured/consolidated memories (requires them), measurement validates auto-capture quality (requires it), pluggability substitutes "the built-in curation" (requires it to exist), and the stated value — "better with use instead of accumulating noise" — requires capture and consolidation together (capture alone worsens noise, the very problem). Tightly coupled facets of a single self-maintaining-memory experience. PM has deliberately scoped it, carving substrate (RHAIRFE-2630), sensitive-data screening (RHAIRFE-2634), and context assembly to other RFEs. Maps to ~1 strategy feature. |
| **Total** | **10/10** | **PASS** |

### Verdict
A focused, well-justified RFE that clearly states a customer need, grounds it in a strategic investment with a competitive causal chain and pilot-regression consequences, leaves implementation to engineering, and scopes cleanly to a single coherent capability.

### Feedback
Strengths: exemplary scoping discipline — the explicit In/Out of Scope section carves the curation slice out of adjacent RFEs, and the acceptance criteria are outcome-based rather than prescriptive. The WHY layers strategic, competitive, and customer-consequence evidence. Minor improvements: naming even one or two specific pilot accounts (rather than "every account piloting the 3.6 Dev Preview") would move the customer evidence from segment-level to account-level and make the justification bulletproof. The open question about which built-in curation ships as default and how the quality bar is validated is worth resolving before Tech Preview commitment, since Success Criteria depend on it.

## Technical Feasibility

**Feasibility**: feasible
**Blockers**: none
**Scope assessment**: needs splitting (size L bundles six independently substantial capabilities; right-size the 3.7 Tech Preview slice during strategy)

**Feasible.** This is an extension of the platform's emerging agentic layer, not a rearchitecting of it. Nothing in RHOAI 3.5-ea.2's architecture fundamentally conflicts with a memory service that captures automatically, consolidates in the background, weights episodic memories by outcome, and accepts a pluggable curation approach. The RFE governs the *curation layer* that sits on top of the memory substrate delivered by its declared sibling RHAIRFE-2630 — and the platform already ships the building blocks that layer needs:

- **A pluggable-provider substrate already exists and is the natural home for pluggable curation.** OGX (formerly Llama Stack, overlay 0003) is a running HTTP server built on the "pluggable providers activated by configuration" pattern, already exposing vector storage (`/v1/vector-io`, `/v1/vector-stores`) and an agentic Responses API with conversation/response state (`/v1/responses`). That pattern *is* the substitution model AC-5 asks for: a custom memory-creation/curation provider swapped in without the client changing. The framework-agnostic HTTP surface also means automatic capture and consolidation can be offered to any agent client that speaks HTTP.
- **Background consolidation maps onto standard platform patterns.** Periodic merge/age-out/prune is a scheduled or reconciled workload — a Kubernetes CronJob or an operator reconcile loop, both of which the platform (rhods-operator, DSC-managed components) uses pervasively. "Without user action" is a control-plane responsibility, not a novel capability.
- **Provenance and outcome signal are data-model additions, not architectural conflicts.** AC-4 (why a memory exists: explicit / auto-captured / consolidated) is a provenance field plus, ideally, an emitted event; the platform already has a structured agent-audit precedent (OpenShell OCSF v1.7 events, overlay 0015). AC-3 (episodic memories carry outcome signal) is a schema/weighting addition on top of the episodic store. Neither fights the architecture.

**On the missing component:** "platform memory service" is not in the `rhoai-3.5-ea.2` architecture inventory — there is no memory-store component doc. This is expected and not a blocker: the RFE explicitly builds on the substrate delivered by RHAIRFE-2630 (itself a net-new, in-flight 3.6→3.8 capability per its own review) and scopes the substrate and storage backends OUT. A capability that does not exist yet is precisely what an RFE is for. The substrate is recorded below as a hard dependency/sequencing item (consideration #1), not a blocker.

### Overlays applied

```
Overlays applied:
- 0015: OpenShell is the agent security runtime replacing Kagenti — OPA policy engine + kernel sandboxing (the containment for customer-supplied curation code), OCSF v1.7 events (a precedent for memory provenance/audit), SPIFFE identity. Target agentic strategies at OpenShell, not Kagenti/AgentRuntime.
- 0008: RHOAI does not auto-install/manage external operators — background-consolidation scheduling and any external vector-DB/backend dependency must be admin-owned and surfaced on DSC/DSCI, never auto-installed.
- 0003: Llama Stack renamed to OGX, a pluggable-provider HTTP server — the substrate hosting vector storage + agentic APIs and the natural home for the pluggable-curation extension model.
```

(Overlay 0003's `release` list is 3.5-only and its `affects` names the llama-stack components rather than `platform`; it is applied here as substrate-identity grounding for a 3.7 capability that builds directly on that substrate, consistent with the RHAIRFE-2630 review. Other platform-scoped 3.5 overlays — 0009, 0012, 0013, 0017 — matched the mechanical filter but have no substantive bearing on memory curation and were not applied. Architecture context `rhoai-3.5-ea.2` read successfully.)

### Scope assessment

**Needs splitting.** Framed as a business need (WHAT/WHY) the RFE is coherent and its out-of-scope carve-outs (substrate/backends → RHAIRFE-2630, write-path screening → RHAIRFE-2634, context assembly → separate) are disciplined. The concern is delivery scope: a single size-L item bundles six independently substantial capabilities — (a) automatic capture (an extraction/embedding pipeline with provenance), (b) background consolidation (dedup / age-out / prune scheduling), (c) outcome-weighted episodic memory (gated on the unresolved outcome-signal contract, #2 — the hardest), (d) a pluggable curation extension API with a trust/sandbox model (#4), and (e) a capture-quality evaluation harness (#8). Each has its own hidden dependencies and cross-component coordination; together they are a program slice, not a single strategy feature. Recommend strategy right-size the 3.7 Tech Preview slice — plausibly auto-capture + basic consolidation + provenance as the core, with outcome-weighting, pluggability, and the measurement harness treated as adjacent/later-phase features. This is a phasing/splitting note, not a reason to hold the RFE.

## Strategy Considerations

For engineering to resolve during /strat.refine. None blocks submission.

1. **Hard dependency on the memory substrate (RHAIRFE-2630) — sequencing.** Every curation capability here (capture, consolidation, outcome weighting, provenance, pluggability, measurement) is downstream of the substrate's data model and write/read paths, which RHAIRFE-2630 delivers. That substrate is itself scoped as a multi-release 3.6→3.8 program. RFE-008 at 3.7 Tech Preview therefore depends on the substrate reaching sufficient maturity (episodic store + framework-neutral API + at least one backend) by 3.7. Surface this cross-RFE sequencing explicitly; the curation layer cannot be evaluated before the store exists.

2. **Outcome-signal sourcing is the central under-specified design risk.** AC-3 requires episodic memories to carry outcome signal and retain unsuccessful outcomes "with appropriate weight" so agents avoid repeating failures — but the RFE never says *where* the success/failure signal comes from. The candidates (explicit user feedback, agent self-evaluation via an LLM-judge, task-completion signals from the agent framework / OGX Responses API, or tool-call error results) each imply a different integration point, reliability, and cost. This is the hardest modeling problem in the RFE and crosses the memory service and the agent runtime/framework. Define the outcome-signal contract before this AC is buildable.

3. **Automatic capture is an inference-cost and latency dependency, not just a memory feature.** Capturing "relevant information automatically during interactions" almost certainly means an extraction/summarization model call (deciding what is worth remembering) plus an embedding call per interaction. That is a hard runtime dependency on a serving path (KServe/vLLM or MaaS) and an embedding model, adds per-turn latency and token cost at fleet scale, and needs a fail-open story (capture must never break the interaction). This cross-component coupling to model serving is unstated and materially affects both effort and per-request cost.

4. **Pluggable curation runs customer logic inside the platform — a trust and multi-tenancy boundary.** AC-5 lets customers substitute their own memory-creation/curation approach. Where does that code execute? If it is an OGX provider (overlay 0003) it inherits OGX's process boundary; if it is arbitrary customer curation logic, it likely needs sandboxing — and OpenShell (overlay 0015) is the platform's sanctioned agent sandbox + OPA policy runtime, the natural containment for untrusted curation code. Strategy must define the extension contract (stable interface vs. webhook vs. sandboxed container), its trust model, and per-tenant isolation. This is a cross-component decision spanning the memory service, OGX, and OpenShell.

5. **Auto-capture collides with the sensitive-data screening boundary (RHAIRFE-2634) on a shared write path.** User Scenario 1 has the agent "automatically remember a customer's environment details mentioned in passing" — by construction, auto-capture will write PII/regulated content. The RFE scopes screening OUT (2634 governs "what may be written"; this RFE governs "what is worth writing"), but both decisions fire at the *same* write moment on the *same* content. Designed independently they will fight. Surface the shared, enforced write-path interception point and the ordering (screen before persist), mirroring the same shared-write-path concern already raised in the RFE-007 (write-auditability) and RHAIRFE-2630 reviews.

6. **Provenance (AC-4) should reuse the platform's audit precedent, not invent a parallel schema.** "See why a memory exists — explicit save / automatic capture / consolidation" is a provenance field plus, ideally, an emitted event. OpenShell already emits OCSF v1.7 events for agent activity (overlay 0015), and the sibling RFE-007 is designing a memory-write log. Provenance here, RFE-007's write log, and OCSF describe overlapping "who/what/why wrote this memory" facts. Align the three so customers do not get three incompatible views of the same memory-write history; deciding the schema alignment early avoids rework.

7. **Background consolidation is a fleet-wide scheduled workload — infra cost plus the no-auto-install policy.** "Consolidated in the background without user action" implies a scheduler/controller running periodic merge/age-out/prune jobs across many stores and tenants. Two notes: (a) it is a standing background workload with real resource cost at fleet scale, and (b) per overlay 0008, if consolidation leans on any external operator (an external vector DB's compaction, an external scheduler), that dependency is admin-owned and must be surfaced on DSC/DSCI, not auto-installed. The zero-external-dependency path (platform-managed scheduling over pgvector/file backends) avoids this.

8. **Capture-quality measurement (AC-6) and the Success Criteria require net-new evaluation methodology.** "The quality of automatic capture is measurable so operators can validate and tune what is kept vs. discarded," plus the Success Criteria's "measurably outperform explicit-only memory on multi-session tasks," both need a memory-quality metric and a multi-session benchmark that do not exist today. The platform's eval infrastructure (eval-hub, lm-evaluation-harness, TrustyAI) could host it, but a memory-curation-quality metric is novel methodology and an easily-underestimated sub-effort. The RFE's own Open Question (which built-in curation ships as default, and how the quality bar is validated before Tech Preview) is this same problem plus a product decision — feed both into strategy together.

9. **Multi-tenancy / per-agent isolation must not be foreclosed.** A platform memory service auto-capturing per-agent, per-tenant, per-end-user content needs a tenancy model at the store and API layer even though record-level scope isolation is a deferred sibling concern. OGX's built-in access policy is owner-based without namespace isolation (per the RHAIRFE-2630 review). Critically, consolidation and pluggable curation operate *across* memories — a consolidation job must never merge tenant A's and tenant B's memories, and a curation plugin must not see across tenants. Design the base store and consolidation pass so per-tenant/per-agent isolation can be added without a data-model migration.

10. **"Match and exceed the 3.6 Dev Preview implicit auto-remember" is a stated regression bar.** The Affected Customers note that implicit auto-remember is the most-used behavior in 3.6 demos, and pilots regress at Tech Preview if 3.7 does not at least match it. This is a continuity constraint: strategy should capture the 3.6 interim capture behavior as a baseline/acceptance gate so the "comprehensive" 3.7 service does not accidentally regress the interim capability on the same demo paths.

## Revision History

none (first pass)
