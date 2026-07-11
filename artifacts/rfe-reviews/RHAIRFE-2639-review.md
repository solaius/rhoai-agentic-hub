---
rfe_id: RHAIRFE-2639
score: 10
pass: true
recommendation: submit
feasibility: feasible
needs_attention: false
needs_attention_reason: null
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

TITLE: Agent memory as a governed asset in the AI Asset Registry

| Criterion | Score | Notes |
|-----------|-------|-------|
| WHAT      | 2/2   | Clear, specific need: memory services must be governed like other AI assets — registered with ownership and lifecycle state, with agent-to-memory bindings recorded and queryable. The problem (unregistered memory = untracked parallel asset category, blind decommissioning) and the four acceptance criteria are concrete and unambiguous. |
| WHY       | 2/2   | Named customer accounts with demonstrated consequences: SAS is "blocked on production agents without a complete governance trail" (unregistered memory is a hole in that trail); Infineon "chose the platform for one governance layer across three frameworks" and memory outside the registry "re-fragments exactly what they consolidated." Also cites enterprise accounts on file using the registry against DIY proliferation. Named accounts tied to specific customer-level outcomes clear the bar for a 2. |
| Open to HOW | 2/2 | Describes needs and observable outcomes — register the service, record/query bindings, apply governance actions (approve/deprecate/retire), surface memory dependencies when viewing an agent. AI Asset Registry / Model Registry are platform vocabulary. "Register the service (not the records)" is a scoping decision about what the governed asset is (a WHAT/asset-model call, framed as the settled resolution from the parent Outcome's research), not a mandate on DB schemas, repos, or internal architecture. Engineering retains freedom on implementation. |
| Not a task | 2/2  | A clear business need — governance, audit, and lifecycle coverage of memory as an asset, driven by customer governance reviews and control-plane consistency. Not a chore, tech-debt item, or engineering activity. |
| Right-sized | 2/2 | Deliverables — service registration, agent-to-memory binding recording/query, asset-level governance actions, and dependency visibility — are interdependent facets of one capability: memory as a governed registry asset. Governance actions cannot function without registration; binding views cannot function without recorded bindings; the success criterion ("which agents would this store's retirement affect?") requires both together. Single coherent need mapping to the one parent Outcome (RHAISTRAT-1345, Agent Memory). |
| **Total** | **10/10** | **PASS** |

### Verdict
A model RFE: a clear, customer-grounded need for governing agent memory as a first-class registry asset, backed by named accounts, scoped to a single coherent feature, and left open on implementation.

### Feedback
Strengths: named-account justification (SAS, Infineon) with concrete governance consequences; tight interdependent scope tied to one parent Outcome; needs expressed as outcomes and business capabilities rather than architecture. Minor optional improvements: the enterprise "accounts on file with the PM" reference could be strengthened by naming one or two of those accounts as SAS and Infineon are named; and quantifying deal or renewal impact (e.g., revenue tied to SAS's blocked production agents) would harden an already-strong WHY.

## Technical Feasibility

**Feasibility**: feasible
**Blockers**: none
**Scope assessment**: appropriate (with an effort-credibility caveat and a natural seam noted)

Overlays applied:
- 0015: OpenShell is the agent security platform for RHOAI, replacing Kagenti (affects: platform, openshell; release 3.5/3.6/next — applied as the go-forward agent architecture for a 3.7 target, with the release-match caveat noted)
- 0008: RHOAI does not auto-install external operator dependencies (affects: platform; release: all) — applied, but only marginally relevant to this RFE (see consideration 7)

Architecture context: `rhoai-3.5-ea.2` (latest available; the RFE targets RHOAI 3.7 Tech Preview, so the context is read forward — the memory service and any 3.7 registry work are ahead of this context). No `RFE-012-comments.md` and no prior `rfe-review-report.md` were present; this is a first-pass review.

**Feasible.** This extends an existing, extensible asset-governance control plane to a new asset category and a new relationship edge — the platform's intended extension path, not a re-architecture. Nothing in the architecture conflicts with the need.

Grounding in the platform:

- **The platform already runs an asset-governance registry.** The Model Registry stores asset metadata in PostgreSQL via the ML Metadata gRPC protocol (RegisteredModel / ModelVersion / ModelArtifact), and its **catalog controller aggregates assets from multiple heterogeneous sources into a unified catalog** (registered models, ConfigMap catalogs, benchmark-data init containers). Workflow 4 ("Model Registration and Governance") is exactly the registry-as-governance pattern the RFE wants memory brought into. Adding a new asset *type* (memory service) with ownership + lifecycle state is metadata-model and API/UI extension work over a substrate designed for it.
- **There is precedent for syncing runtime relationships into the registry.** odh-model-controller "optionally syncs InferenceService state back to Model Registry for serving-status tracking." An agent-to-memory binding is the same shape of edge (a runtime relationship reflected into the registry), so the pattern the RFE needs is already present in the architecture, even though a memory-binding sync path does not yet exist.
- **Agents already have a stable, resolvable identity (overlay 0015).** OpenShell (the agent security platform, formerly Kagenti) provides SPIFFE-based workload identity and A2A JWS-signed agent cards. That an agent has a first-class identity is what makes "agent as a registry entity" and "agent→memory binding" tractable rather than speculative.

Per the feasibility rubric, the fact that the memory service does not yet appear in the 3.5-ea.2 component inventory (65 components) is **not** a blocker — the memory service is a 3.7-targeted Dev Preview capability, and the RFE is precisely what registers it. Assessed on the underlying need — bringing a live memory datastore under the same ownership/lifecycle/governance control plane as every other asset type — this is buildable.

The RFE's own settled decision is architecturally sound and worth affirming: **registering the memory *service*, not the memory *records*.** A metadata control plane governs service/asset-level entities; attempting to govern individual records would collide with the data plane (and would duplicate the record-level scoping that is a sibling data-plane RFE). Keeping the registered unit at the service level keeps the registry a control plane.

### Scope assessment: appropriate (watch the effort estimate)

The four ACs are a genuinely cohesive capability — register the memory service as a governed asset (AC1), record and query its agent bindings (AC2), apply lifecycle governance to it (AC3), and surface those bindings in the agent view (AC4). They are coupled by construction: you cannot record bindings before the asset exists, and AC4 is just surfacing the AC2 data. Unlike RFE-014 (which bundled five distinct governance surfaces), this does not read as an over-packed feature, so a mandatory split is not warranted.

Two caveats for `/strat.refine`:

- **The `M` estimate is optimistic.** The work spans registry data-model extension + governance workflow on a new type + a **cross-component binding-capture pipeline** + a dashboard agent-detail slice, plus a dependency on the agent-as-asset view (AC4) and on the memory service exposing registrable identity/ownership metadata. The binding-capture pipeline in particular is net-new integration, not a metadata add.
- **If a seam is wanted, it falls between the registry/governance half and the binding-capture half.** AC1 + AC3 (register the memory service as an asset + apply approve/deprecate/retire to it) are registry-internal and could stand alone; AC2 + AC4 (capture, query, and surface agent→memory bindings) are the cross-component pipeline and its UI. Splitting there is a reasonable option if the binding-capture design proves heavier than the registry-type work — but it is a strategy-discretion call, not a required split.

## Strategy Considerations

These carry forward into `/strat.refine`; none blocks submission.

1. **"AI Asset Registry" as one control plane over models + prompts + MCP servers is partly a product framing, not a fully-realized single component.** In the 3.5-ea.2 architecture there is no single "AI Asset Registry" component: models live in **Model Registry** (ML Metadata / PostgreSQL); prompts live in **MLflow's prompt registry** (overlay 0002); MCP servers exist (RHOAI MCP Server) but do not appear as registered governed assets. The RFE's premise — "memory is the next asset category" governed alongside models, prompts, and MCP servers under one control plane — inherits whatever is still unfinished about that unification. Strategy should confirm which substrate the memory asset actually attaches to (Model Registry's type system, a higher-level catalog abstraction, or a net-new registry surface) before "just add memory to the one registry" is treated as a small delta.

2. **AC #4 presupposes agents are already registered assets that show models and tools.** "Viewing an agent in the registry shows its memory dependencies alongside its models and tools" only makes sense if agent-as-registered-asset with model/tool bindings already exists (from the parent Outcome RHAISTRAT-1345 and the Dev Preview RFEs). If that agent-asset view is itself still in flight, AC #4 has a hard upstream dependency and cannot be sized independently of it. Confirm the agent-asset representation lands (or ships in the same slice) before committing AC #4.

3. **The binding-capture mechanism is unspecified and is cross-component.** Recording "which agents use which memory service and store" requires *something* to observe and report the binding. Candidates span the agent runtime (OpenShell), the memory service reporting its consumers, and the dashboard's agent-ops BFF. This is agent-platform + memory-service + registry coordination that the RFE does not name. The InferenceService→Model Registry sync is the closest existing analogue, but no memory-binding sync path exists today — it must be designed. This is the single largest hidden complexity.

4. **This RFE is the source of truth that the console RFE (RFE-014) consumes.** RFE-014's open question "where do agent-to-memory bindings live?" is answered here. Strategy should treat RFE-012's binding model + query API as an upstream dependency for the console, and make sure the query surface (list bindings by agent, by store, "which agents would this store's retirement affect?") exposes the operations the console and audit stories need — designing the binding API console-blind would push scope back onto RFE-014.

5. **Governance actions on a live datastore = metadata/lifecycle-state change, not decommissioning.** "Approve / deprecate / retire" applied to a memory *service* are asset-lifecycle state transitions that drive workflow and impact queries; they are not an actual teardown of the running datastore. The success criterion ("which agents would this store's retirement affect?") is an impact query answered from the recorded bindings — well within a metadata store's reach — but strategy must draw the line explicitly between the governance state machine (registry) and any operational decommissioning (a separate step), or "retire" risks being read as "delete the data."

6. **Modeling non-model assets and edges in an ML-Metadata-shaped schema is real data-model work.** Model Registry's native schema is model-centric (RegisteredModel / ModelVersion / ModelArtifact). Representing a "memory service" asset, an "agent" asset, and a typed "agent→memory" relationship may require extending the type system or working through the catalog aggregation layer. The catalog controller already aggregates heterogeneous sources, so this is feasible — but it is data-model design, not a trivial field add, and it should be estimated as such.

7. **External-backend prerequisite (overlay 0008) — low relevance here.** A memory service is typically backed by a datastore (vector DB, PostgreSQL, Redis) that may ride an external operator, and RHOAI does not auto-install those. This matters for the RFEs that *deploy* the memory service; this RFE only *registers* it as metadata, so the dependency is marginal. Noted for completeness and consistency with the sibling reviews.

8. **Agent platform is OpenShell, not Kagenti (overlay 0015).** If strategy refinement reaches for an agent-runtime component to source identity or bindings, it must target OpenShell (SPIFFE identity, A2A agent cards) — there is no kagenti-operator / AgentRuntime CRD / AuthBridge to reference. This does not change feasibility; it is a naming/redirect guardrail for the HOW discussion.

## Revision History

none (first pass)
