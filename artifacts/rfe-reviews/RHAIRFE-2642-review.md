---
rfe_id: RHAIRFE-2642
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

TITLE: Ready-made memory integrations for agent harnesses and frameworks

| Criterion | Score | Notes |
|-----------|-------|-------|
| WHAT      | 2/2   | Clear, specific need: AI engineers using major agent harnesses/frameworks need platform memory to work out of the box without per-harness glue code, to participate in each harness's native context-assembly workflow (not only manual tool calls), and to be versioned/maintained with the service so upgrades don't silently break users. The problem statement, scenarios, and acceptance criteria are concrete and unambiguous. |
| WHY       | 2/2   | Named customer account (Infineon) running AutoGen, LangChain, and LangGraph simultaneously, with a demonstrated consequence: per-framework custom integration multiplies their cost by three and undermines the single-governance-layer requirement that brought them to the platform. Also ties to the parent Outcome's central promise (framework-agnostic memory) with a clear causal chain showing why ready-made integrations are required to make that promise real at adoption time, plus the 3.6 Dev Preview pilots re-implementing glue code. Named account + demonstrated customer consequence + strategic causal chain. |
| Open to HOW | 2/2 | Describes the need (memory available when the harness assembles context, versioned integrations) without prescribing internal architecture. Named frameworks (AutoGen, LangChain, LangGraph) appear as the customer's environment/need, not as mandated implementation. The open question explicitly leaves the supported target list and the technical approach (native context participation vs. tool/MCP degradation) to engineering. No design docs mandated. |
| Not a task | 2/2  | Clear business need: adoption enablement and protecting the single-control-plane value proposition that customers chose the platform for. Not a chore, refactor, or tech-debt item. |
| Right-sized | 2/2 | Single coherent deliverable: ready-made native-workflow memory integrations across the supported set of harnesses, versioned and maintained with the service. The multiple harnesses are delivery targets, not separate features (same capability across targets). Native-workflow participation and versioning/maintenance are inseparable facets of the integration deliverable, not independently shippable capabilities. Explicitly scopes out the memory service itself (RHAIRFE-2630) and the smaller-model guidance (separate RFE). One strategy-feature summary fits cleanly. |
| **Total** | **10/10** | **PASS** |

### Verdict
A well-scoped, customer-driven RFE that clearly articulates the adoption need for framework-native memory integrations, backed by a named account and a causal chain to the parent Outcome, without prescribing implementation.

### Feedback
Strengths: named customer (Infineon) with a concrete cost consequence, a clear tie to the parent Outcome's core promise, disciplined scope with explicit out-of-scope carve-outs, and an honest open question that leaves technical approach to engineering. Minor improvements: the "supported set of major agent harnesses and frameworks" is left deliberately open — resolving the target list (currently an open question) would tighten the success criteria and sizing, and quantifying Infineon's cost/deal impact in dollars would further strengthen an already-strong WHY.

## Technical Feasibility

### RFE-015: Ready-made memory integrations for agent harnesses and frameworks

**Feasibility**: feasible
**Strategy considerations**: see list below (for /strat.refine)
**Blockers**: none
**Scope assessment**: appropriate at the RFE-framing level (the parent split is resolved); residual right-sizing hinges on the target-list Open Question — may need a further split if the list is large or native-context depth is required uniformly

---

**Architecture context**: `rhoai-3.5-ea.2` (`PLATFORM.md`), read successfully. The RFE targets RHOAI 3.7 Tech Preview; the generated context baseline is 3.5-ea.2, corrected forward by the overlays below.

**Overlays applied:**
- 0015: OpenShell is the agent security/runtime platform for RHOAI, replacing Kagenti (affects `platform`, `openshell`; release `3.5/3.6/next`)
- 0008: Platform policy — RHOAI does not auto-install external operator dependencies (affects `platform`; release `all`)

Release-filter note: the RFE targets 3.7, which no overlay lists literally. 0008 matches via `all`. 0015 lists `next` (the forward line past the 3.5-ea.2 baseline) and is applied because it is the authoritative correction to the platform's agent-runtime story — the generated `PLATFORM.md` still describes Kagenti/agents-operator as the agent platform, which is now deprecated; grounding an agent-memory-integration RFE in the deprecated runtime would be wrong. Overlay 0003 (Llama Stack → OGX) is treated as **supplementary** context, not a formal match: its `affects` list names the llama-stack components (not `platform`) and its `release` list is `3.5` only. It is relevant here because OGX (formerly Llama Stack) is one of the concrete native-integration targets and a delivery mechanism for this RFE, so OGX naming and its pluggable-provider model are used below as background.

**Cross-reference**: This RFE is the split of RFE-009's deliverable (a) "ready-made per-framework/harness integrations." The RFE-009 feasibility review recommended splitting (a) from (b) "memory effectiveness on smaller self-hosted models"; RFE-015 correctly carves (b) into a separate RFE (Out of Scope). The parent memory service it consumes (RHAIRFE-2630) was reviewed feasible (10/10, submit) with a multi-release-program scope note (3.6→3.8). Both reviews are on file and inform the assessment below.

---

### Feasibility rationale

This is fundamentally buildable and there is no architectural conflict. Shipping ready-made memory integrations for agent frameworks is standard adapter/plugin work against each framework's documented extension points (memory / checkpointer / store interfaces), layered on top of the framework-agnostic memory service (the parent capability, RHAIRFE-2630), which is explicitly out of scope here and being delivered separately. The platform is actively expanding into agentic workloads (overlay 0015, OpenShell), and it already ships framework SDKs as pip dependencies in workbench/universal images (CodeFlare SDK, Kubeflow SDK — no operator manifest, own release cadence), so the delivery pattern for framework-side integrations already exists on-platform. OGX (formerly Llama Stack) is a running HTTP server built on the "pluggable providers activated by env vars" model — a native memory provider registered there is exactly the "participate in the harness's native workflow" experience AC-2 describes. Nothing here requires rearchitecting the platform; it extends it. A capability not yet existing (the memory service, the per-harness adapters) is precisely what this RFE stack exists to deliver, not a feasibility barrier.

### Strategy considerations (carry into /strat.refine — none of these block the RFE)

1. **Hard sequencing dependency on the memory service (RHAIRFE-2630).** "Ready-made integrations" are only meaningful once the framework-agnostic memory API exists and is stable enough to integrate against — the RFE's own Summary concedes this ("only as adoptable as its integrations"). The integrations cannot be built or validated before the API surface stabilizes. Per the RHAIRFE-2630 feasibility review, that service is a multi-release program (Dev Preview 3.6 → GA 3.8). RFE-015 targets 3.7 TP, so the memory API and these maintained adapters are being asked to land in overlapping windows. Strat.refine must confirm the API is stable enough to build *maintained* (versioned, upgrade-safe) adapters on in that timeframe, and confirm which slice of the service API is frozen by 3.7.

2. **"Harnesses" and "frameworks" are conflated, and they are not equally tractable.** The named examples (AutoGen, LangChain, LangGraph — the Infineon stack) are agent *frameworks*: SDK libraries with documented, pluggable memory/checkpointer/store interfaces where "memory participates when the framework assembles context" (AC-2) is squarely feasible. But closed CLI *harnesses* manage memory internally as a harness-owned store and expose no clean hook for external context assembly — for those, AC-2 is bounded by what the harness vendor exposes and may degrade to a tool or MCP integration where the harness still manages memory internally. The RFE's own Open Question flags exactly this ("is native context participation achievable or does it degrade to a tool or MCP integration"). This is the central hidden complexity: the acceptance criterion "memory participates in each supported harness's native workflow" cannot be guaranteed uniformly across a heterogeneous target set. Strat.refine must pin the exact target list and, per target, classify native-context vs. tool/MCP fallback — otherwise AC-2 is written as a universal guarantee the platform cannot uniformly meet.

3. **Ongoing compatibility-matrix / sustaining-engineering burden (AC-3).** "Versioned, documented, and maintained with the memory service, so a service upgrade does not silently break harness users" is a per-release CI/test matrix across fast-moving upstream harness/framework APIs (each framework release × each memory-service release), not a one-time build. The RFE itself notes each harness "moves independently and quickly." This is a long-lived, cross-team commitment; the size-L estimate must include the maintained matrix and its owning model, not just the initial adapter build. Under-counting this is the most likely way the effort estimate proves optimistic.

4. **Target the current agent runtime, not the deprecated one (overlay 0015).** Agent frameworks/harnesses on RHOAI run under OpenShell (CLI/SDK at 3.5 Dev Preview, operator at 3.6), which injects the SPIFFE workload identity the memory service uses as its RBAC principal. Integrations should be built against the OpenShell SDK/runtime — do not reference the removed Kagenti AgentRuntime CRD / AuthBridge sidecar. Additionally, agents in OpenShell sandboxes execute under OPA L4/L7 network-policy enforcement (allow/deny by destination): an integration that makes network calls to the memory service must have that egress permitted in the sandbox spec / provider profiles. Coordination point between the integrations, the memory service, and OpenShell — not a blocker.

5. **Two delivery mechanisms with two owners (cross-component coordination the RFE does not mention).** External Python frameworks (AutoGen/LangChain/LangGraph) ship as pip packages in workbench/universal images (the CodeFlare/Kubeflow SDK pattern: no operator manifest, independent release cadence, AIPCC onboarding for new extras). The OGX target ships as a native OGX memory *provider* (midstream-fork pattern, overlay 0003). These are two distinct delivery pipelines, release processes, and likely owning teams. Strat.refine should name the owning team(s) and reconcile release cadences against the AC-3 "maintained with the service" commitment.

6. **Governance must hold uniformly across heterogeneous integration paths.** The parent Outcome's promise is "governed memory" behind a "single governance layer." When memory is reached through diverse harness-native paths (native context assembly vs. tool call vs. MCP), the governance/policy/audit layer — which overlaps OpenShell's OPA policy and OCSF audit events (per the RHAIRFE-2630 review, consideration #7) — must be enforced consistently on every path. If a native-context-assembly path bypasses the tool-call path, it must still traverse the same identity/policy/audit checkpoints. Verify per integration so the integrations do not become a governance bypass.

7. **Deployment-mode portability must not fork the memory format.** The success criterion "a framework switch between two supported harnesses preserves memory and requires no integration work" must hold across both the server-side and client-side / harness-tier deployment modes of the single governed abstraction. Adapters must not persist harness-specific memory formats that break portability — otherwise the integrations meant to deliver "an agent's memory survives a framework switch" would undermine the very Outcome promise they exist to make real.

8. **External-dependency policy (overlay 0008, low impact here).** These integrations ship as client libraries/adapters and OGX providers, so the no-auto-install policy is unlikely to bite. But if any specific target requires an external operator or cluster component, RHOAI will not auto-install it — it must be a documented prerequisite via the reference GitOps path, with any missing dependency surfaced on DSC/DSCI status. Flagged for completeness.

9. **Phasing tension against the current strategy (positioning, not feasibility).** The RFE-009 review noted the hub's own recommended architecture and roadmap place the harness-tier / client-side integration work in Phase 2 (RHOAI 3.8+, directional) and flag it as "the least-researched element of the deployment model," while this RFE targets 3.7 TP. This is a roadmap-positioning decision for strat.refine (pull harness integration forward into 3.7, or move the target), not a technical feasibility issue.

### Scope assessment detail

The parent RFE-009's primary split concern — bundling per-framework integrations (a) together with small-self-hosted-model effectiveness (b) — is **resolved**: RFE-015 explicitly carves (b) into a separate RFE (Out of Scope) and cleanly consumes, rather than restates, the memory service (RHAIRFE-2630, also Out of Scope). That is the correct decomposition and removes the largest scope objection.

The residual scope risk is internal to (a): "the supported set of major agent harnesses and frameworks" is unbounded in the RFE text, and each additional target is a separate integration surface with its own memory abstraction, its own release cadence, and — for closed harnesses — a native-context requirement that may not be achievable (see consideration #2). Size L is plausible for a small target list at framework-SDK depth; it is likely optimistic if the list is large or if native-context participation is required uniformly across both frameworks and closed harnesses plus the ongoing maintained matrix. Recommend strat.refine right-size after the target-list Open Question is answered, and consider whether a further split is warranted along a natural seam — by delivery mechanism (framework-SDK adapters vs. OGX provider) or by depth tier (native-context targets vs. tool/MCP-fallback targets). This is a right-sizing note contingent on the Open Question, not a reason to hold the RFE.

## Strategy Considerations

Flagged for /strat.refine (verbatim from the feasibility analysis above — none block the RFE):

1. **Hard sequencing dependency on the memory service (RHAIRFE-2630).** Confirm the framework-agnostic memory API is stable enough to build *maintained* (versioned, upgrade-safe) adapters on in the 3.7 TP window, and confirm which slice of the service API is frozen by 3.7 (service is a multi-release program, Dev Preview 3.6 → GA 3.8; overlapping windows).
2. **"Harnesses" vs. "frameworks" are conflated and not equally tractable.** Pin the exact target list and, per target, classify native-context participation vs. tool/MCP fallback — AC-2 cannot be a universal guarantee across a heterogeneous set (frameworks with pluggable interfaces vs. closed CLI harnesses).
3. **Ongoing compatibility-matrix / sustaining-engineering burden (AC-3).** Size L must include the per-release CI/test matrix (each framework release × each memory-service release) and its owning model, not just the initial adapter build — the most likely source of estimate optimism.
4. **Target the current agent runtime, not the deprecated one (overlay 0015).** Build against the OpenShell SDK/runtime (SPIFFE identity, OPA L4/L7 egress must permit memory-service calls); do not reference the removed Kagenti AgentRuntime CRD / AuthBridge sidecar.
5. **Two delivery mechanisms with two owners.** Name the owning team(s) and reconcile release cadences: pip-package framework adapters (CodeFlare/Kubeflow SDK pattern) vs. native OGX memory provider (midstream-fork pattern) against the AC-3 "maintained with the service" commitment.
6. **Governance must hold uniformly across heterogeneous integration paths.** Verify per integration that native-context, tool-call, and MCP paths all traverse the same identity/policy/audit checkpoints (overlaps OpenShell OPA policy + OCSF audit) so integrations do not become a governance bypass.
7. **Deployment-mode portability must not fork the memory format.** Adapters must not persist harness-specific memory formats; the "framework switch preserves memory, no integration work" criterion must hold across server-side and client-side/harness-tier deployment modes.
8. **External-dependency policy (overlay 0008, low impact).** If any target needs an external operator/cluster component, it must be a documented GitOps prerequisite (surfaced on DSC/DSCI status) — RHOAI will not auto-install it.
9. **Phasing tension (positioning, not feasibility).** Roadmap places harness-tier/client-side integration in Phase 2 (3.8+, directional, "least-researched element"); this RFE targets 3.7 TP. Decide whether to pull the work forward or move the target.

## Revision History

none (first pass)
