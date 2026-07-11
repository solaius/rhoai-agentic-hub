---
rfe_id: RHAIRFE-2640
score: 10
pass: true
recommendation: submit
feasibility: feasible
needs_attention: true
needs_attention_reason: 'The M effort estimate is only credible if four net-new memory-service
  APIs plus per-turn retrieval provenance (AC #3) are delivered by the parent Outcome''s
  memory service rather than built in this UI slice; the agent-attach path (AC #5/attach)
  also targets a mid-transition platform (OpenShell replacing Kagenti) with no stable
  CRD — sequencing/dependency risks the clean 10/10 rubric score does not reflect.'
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

TITLE: Memory visibility and control for AI engineers in Gen AI Studio

| Criterion | Score | Notes |
|-----------|-------|-------|
| WHAT      | 2/2   | Clear, specific need: AI engineers need to discover available memory stores, attach/detach them to an agent or playground session, inspect what an agent remembered and what it recalled in a given exchange, and correct records — all inside Gen AI Studio without dropping to APIs. The problem (memory is invisible from the studio, forcing "API spelunking" that ends in memory being turned off) is concrete and well-scoped. |
| WHY       | 2/2   | Strongest evidence is a strategic investment with a clear causal chain: the parent Outcome (RHAISTRAT-1345, Agent Memory, RHOAI 3.7 Tech Preview) is the investment, and the RFE argues engineer-level inspectability is what keeps memory trusted enough to leave enabled — opaque memory reads as nondeterministic behavior, gets disabled, and "forfeits the entire investment under the parent Outcome." Reinforced by the Summit 2027 demo (stated purpose of the 3.7 Tech Preview) running in Gen AI Studio, and by a precedent argument (the enterprise cohort that demanded in-studio MCP discovery, "named accounts on file with the PM," expecting the same for memory). Accounts aren't named in the text (which alone would sit at 1), but the strategic-investment causal chain lifts it to 2. |
| Open to HOW | 2/2 | Describes user-facing outcomes and surfaces only: see stores, attach/detach without code, inspect remembered/recalled, edit/delete within scope, changes take effect in the running session. "Governed memory service," "interim playground tool," and "Gen AI Studio" are product/context vocabulary, not architecture. No internal design (schemas, storage engine, service topology) is mandated — engineering retains full freedom on implementation. |
| Not a task | 2/2  | This is a business need — trust and adoption of the memory investment, plus demo readiness for Tech Preview — not a chore, tech-debt item, or engineering activity. The value (memory stays enabled because it is inspectable) is the point, not the work. |
| Right-sized | 2/2 | Deliverables (discover, attach/detach, inspect remembered+recalled, correct, live effect) are tightly coupled facets of one memory-management experience for a single persona (AI engineer) on a single surface (Gen AI Studio). Applying the independence test: discovery is inert without attach; attach is unusable without inspection; correction operates on what inspection surfaces; live-effect is a property of the same session. None ships as standalone value on its own. Maps cleanly to ~1 strategy feature (the studio-facing slice of the parent Agent Memory Outcome). Comparable to the R=2 "dashboard homepage / entry points + launch" calibration. |
| **Total** | **10/10** | **PASS** |

### Verdict
A well-formed RFE that states a clear, single-persona need with a genuine strategic-investment justification, leaves architecture open, and stays scoped to one coherent studio experience.

### Feedback
Strong across the board. The one place to firm up is WHY: the "named accounts on file with the PM" reference gestures at customer-level evidence without surfacing it. Naming even one or two of those enterprise accounts (or citing the deal/pilot they map to) would move the justification from a strong strategic-investment chain to unambiguous customer-level evidence and make the case bulletproof. Otherwise, the acceptance and success criteria are observable and testable — keep them.

## Technical Feasibility

**Feasibility**: feasible

**Blockers**: none. Nothing in the platform architecture conflicts with this need — the opposite is true. Gen AI Studio is already the dashboard's `gen-ai` federated module fronted by a Go BFF that proxies OGX (formerly Llama Stack) and related services, and the platform already ships the exact pattern this RFE needs: **in-studio discovery of backend resources via CRD watch + BFF proxy** (the dashboard watches `OGXServer`, `AgentRuntime`, and `MCPServerRegistration` CRs; the `agent-ops` BFF does MCP tool-connection discovery). The RFE's own precedent claim — "the platform already accepted in-studio discovery for MCP servers" — is accurate and shipped. Surfacing memory discovery/attach/inspect/correct is a new instance of an established extension pattern (federated UI module + user-token BFF proxy + owner-scoped CRUD), not a rearchitecture. The governed memory service not existing yet is what the parent Outcome is for; it is not an infeasibility.

**Scope assessment**: appropriate. As a Gen AI Studio experience slice for a single persona (the iterating AI engineer) with clean, demoable success criteria, the RFE is right-sized and the five ACs cohere around one user journey. The caveat is effort credibility, not scope shape: ACs #3 (recall inspection) and #5 (live apply) smuggle in backend contracts (per-turn retrieval provenance; session-context invalidation) that, if they must be built here rather than delivered by the memory service, push this well beyond `M`. That is a sequencing/dependency risk for /strat.refine to resolve, not a reason to split the RFE.

_Overlays applied:_
- _0008: RHOAI does not auto-install external operator dependencies — if the governed memory service uses an external backend operator it is a documented prerequisite, surfaced on DSC/DSCI, not platform-managed (conditional; likely moot since OGX ships in-image vector-io providers)._
- _0015: OpenShell is the agent security platform for RHOAI, replacing Kagenti — the "attach memory to an agent" path must target OpenShell-era constructs, not the deprecated AgentRuntime/AuthBridge CRs the agent-ops BFF still watches._

_Architecture context: rhoai-3.5-ea.2 (PLATFORM.md + odh-dashboard.md, ogx-distribution.md). OGX = formerly Llama Stack (overlay 0003) noted as supplementary naming context for the memory host and the gen-ai BFF's proxy target; not a formally matched overlay for the 3.7 target release. Connection API (overlay 0006) noted only to disambiguate: it governs S3/OCI/URI data-source connections, not memory-store attachment — do not conflate the two. No prior review report and no comments file present; this is a first-pass review._

## Strategy Considerations

- **This is a UI/UX slice riding on a net-new memory-service contract — the studio cannot lead the service.** There is no "agent memory" or "governed memory service" component in the RHOAI 3.5-ea.2 inventory (65 components); it is being stood up under the parent Outcome (RHAISTRAT-1345). Every acceptance criterion resolves to a backend API the memory service must expose before Gen AI Studio can render it: (a) a per-user-scoped **discovery/list** API for available stores, (b) an **attach/detach binding** API at agent/session granularity, (c) a per-exchange **recall-trace / retrieval-provenance** API, and (d) a **scope-filtered edit/delete** API. The studio work is a proxy-and-render layer; its critical dependency is that these four contracts exist and are stable. /strat.refine must sequence this RFE behind (or co-designed with) the foundational memory-service APIs — the `M` estimate is only credible if those APIs are treated as a given, not built here.
- **"What it recalled in a given exchange" (AC #3) is the hardest requirement and it is a backend contract, not a UI feature.** Showing *which* remembered items were retrieved for a specific turn requires the memory service AND the agent/inference path (OGX `/v1/responses` agentic API, or the governed service's equivalent) to emit per-turn retrieval provenance — a record of what was queried, what matched, what was injected into context. If that trace is not emitted at inference time, no studio panel can reconstruct it after the fact. This is the load-bearing dependency behind the RFE's entire "trust" thesis and must be a named deliverable of the memory service, coordinated with whoever owns the recall path. Flag as the top cross-team item.
- **"Take effect in the running session" (AC #5) depends on the session's memory-consumption model.** Whether an edit/delete propagates into an already-running playground/agent session depends on whether that session re-queries memory each turn or snapshots memory context at session start. If sessions cache retrieved context, a correction will not surface until the next fetch/turn unless the session context is invalidated. "Live apply" is therefore a runtime-consistency contract between the agent/OGX session layer and the memory service — not something the dashboard can guarantee on its own. Define the semantics (next-turn vs immediate) in strategy.
- **Two memory backends must coexist or converge.** The RFE explicitly graduates 3.6 Dev Preview pilots from the interim playground tool (whose view/delete covers only its own memories) to the governed service, and notes the interim tool does not see the governed store. The studio must either unify both behind one memory surface or clearly delineate them, and graduating pilots implies a coexistence UX and possibly migration of already-remembered facts. Migration/coexistence is unstated in the RFE and is a real hidden complexity.
- **Scope/governance model is assumed but undefined.** "Stores available to them" and "records their scope permits" presuppose an ownership model (per-user vs per-project/namespace vs per-agent vs shared/team). Gen AI Studio proxies with the user token, and OGX enforces owner-only CRUD (create = authenticated user; read/update/delete = resource owner), which gives a baseline. But personal-vs-shared memory, and any admin/governance view, are design decisions that can expand scope well beyond the AI-engineer persona this RFE (correctly) targets. Keep the persona boundary; name the scope model in strategy.
- **Agent-side surface is a moving target (overlay 0015).** "Attach a memory store for an agent" touches the agent runtime, and the agent platform is now **OpenShell**, which replaces Kagenti — there is no AgentRuntime CRD / AuthBridge to build against. Yet the dashboard's shipped `agent-ops` BFF still watches `AgentRuntime` (agent.kagenti.dev) CRs. Whichever construct represents "an agent" for the attach operation is mid-transition; coordinate the target with the OpenShell direction rather than the deprecated Kagenti CRs. (For the *playground-session* attach path, this is largely an OGX/Gen AI Studio concern and is less affected.)
- **External backend prerequisite (overlay 0008), conditional.** If the governed memory service is backed by an external operator (e.g., a standalone vector DB / database operator), standing platform policy is that RHOAI does not auto-install external operators — it must be a documented prerequisite with missing-dependency status surfaced on DSC/DSCI. This is likely mitigated here because OGX (formerly Llama Stack) already ships in-image vector-io providers (Milvus/pgvector/Qdrant) and PostgreSQL-backed state, so a memory backend can exist without an external operator — but the choice belongs to the memory-service strategy, not this UI slice.
- **Cross-team coordination is unstated.** Delivery spans the gen-ai/dashboard team (federated module + BFF), the memory-service team (the four APIs above + recall trace), OGX (agents/responses + memory host), and possibly OpenShell (agent-scoped attach). None of this is called out in the RFE; flag for planning.

## Revision History

none (first pass)
