### RFE-009: Ready-made memory integrations for agent harnesses and frameworks

**Feasibility**: feasible
**Strategy considerations**: see list below (for /strat.refine)
**Blockers**: none
**Scope assessment**: needs splitting (also likely larger than the stated size M)

---

**Architecture context**: `rhoai-3.5-ea.2` (`PLATFORM.md`). The RFE targets RHOAI 3.7 Tech Preview; the generated context baseline is 3.5-ea.2, corrected forward by the overlays below.

**Overlays applied:**
- 0015: OpenShell is the agent security/runtime platform for RHOAI, replacing Kagenti (affects `platform`, `openshell`; release `3.5/3.6/next`)
- 0008: Platform policy — RHOAI does not auto-install external operator dependencies (affects `platform`; release `all`)

Release-filter note: the RFE targets 3.7, which no overlay lists literally. 0008 matches via `all`. 0015 lists `next` (the forward line past the 3.5-ea.2 baseline); it is applied because it is the authoritative correction to the platform's agent-runtime story — the generated `PLATFORM.md` still describes Kagenti/agents-operator as the agent platform, which is now deprecated. Grounding an agent-memory RFE in the deprecated component would be wrong. Overlay 0011 (KServe/llm-d self-hosted LLM serving) and 0003 (Llama Stack → OGX) are noted as background but not formally matched (affects lists don't include `platform`, and the RFE doesn't directly touch those components' internals).

---

### Feasibility rationale

This is fundamentally buildable and there is no architectural conflict. Shipping ready-made memory integrations for agent frameworks is standard adapter/plugin work against each framework's documented extension points, layered on top of the framework-agnostic memory service (the parent capability, RHAIRFE-2630 / roadmap RFE-M2). The platform is actively expanding into agentic workloads (overlay 0015, OpenShell), and self-hosted LLM serving already exists on-platform (vLLM via LLMInferenceService/llm-d, overlay 0011), so both halves of the RFE — the integrations and the "effective on smaller self-hosted models" criterion — sit on capabilities the platform already has or is already building. Nothing here requires rearchitecting the platform; it extends it. A capability not yet existing (the memory service, per-harness adapters) is exactly what the RFE stack exists to deliver, not a feasibility barrier.

The hub's own agent-memory strategy corroborates this: `research/09-agent-harness-memory.md` catalogs the harness/framework memory landscape and portable patterns, and `strategy/recommended-architecture.md` frames a single governed memory abstraction with server-side and client-side ("harness tier") deployment modes that keep an agent's memory portable across modes — precisely the portability this RFE's success criteria assert.

### Strategy considerations (carry into /strat.refine — none of these block the RFE)

1. **Hard sequencing dependency on the memory service (RHAIRFE-2630 / RFE-M2).** "Ready-made integrations" are only meaningful once the framework-agnostic memory API exists and is stable enough to integrate against. The RFE's own summary concedes this ("only as adoptable as its integrations"). The integrations cannot be validated before the API surface stabilizes. Per the roadmap the substrate is 3.7 Dev Preview — so the memory API and these integrations are being asked to land in the same window; strat.refine should confirm the API is stable enough to build maintained adapters on in that timeframe.

2. **"Harnesses" and "frameworks" are conflated, and they are not equally tractable.** The RFE's named examples (AutoGen, LangChain, LangGraph) are agent *frameworks* — SDK libraries with documented, pluggable memory/checkpointer/store interfaces. Integrating there (ship a backend adapter implementing each framework's memory interface, so memory participates when the framework assembles context) is squarely feasible and matches AC-2. But the parent RFE-2630 names a different set (LangGraph / CrewAI / OpenClaw), and the supporting research (09) covers closed CLI *harnesses* (Claude Code, Codex CLI, Gemini CLI) that manage memory internally as a "Harness-as-Memory-Store" and expose no clean hook for external context assembly. For those, AC-2 ("memory available when the harness assembles context, not only through manual tool invocation") is bounded by what the harness vendor exposes and may not be achievable without the harness's cooperation. Research 09 explicitly advises RHOAI "should not try to replace the harness's internal memory management." Strat.refine must pin down the exact target list and, per target, whether native context participation is even possible or whether it degrades to a tool/MCP integration.

3. **Ongoing compatibility-matrix / sustaining-engineering burden (AC-3).** "Versioned, documented, and maintained with the memory service, so a service upgrade does not silently break harness users" is a per-release CI/test matrix across fast-moving upstream harness/framework APIs, not a one-time build. Research 09 documents heavy churn (Gemini CLI rewrote its memory architecture in v0.40; Hermes' pluggable-provider system; Codex regional limits). This is a cross-team, long-lived commitment — the effort estimate must include the maintained matrix, not just the initial adapters.

4. **The "smaller self-hosted models" criterion (AC-4) is a different discipline and only partly in RHOAI's control.** Whether an agent "uses memory reliably" on a smaller model is largely model-dependent; RHOAI's levers are task-specific guidance, prompt/tool-use scaffolding, few-shot assets, and possibly fine-tuned adapters, validated against an eval bar (lm-evaluation-harness / eval-hub exist on-platform). The AC as written asserts an outcome RHOAI cannot fully guarantee — strat.refine should define the measurable bar and the model tier(s) tested. This work also overlaps conceptually with RFE-M4 (context engineering) and RFE-M11 (memory quality benchmarking, currently 3.8+ directional); coordinate to avoid duplication. Cross-component reach: model serving (vLLM/llm-d) and eval-hub.

5. **Phasing tension against the current strategy.** Both the recommended architecture (§4/§5) and the RFE roadmap (RFE-M9, "Client-side memory hybrid path — the harness tier") place the harness-tier/client-side integration work in **Phase 2, RHOAI 3.8+ (directional)** and flag it as "the least-researched element of the deployment model." RFE-009 targets **3.7 Tech Preview**. Additionally, the harness-integration + small-model concern is not represented among the six already-filed sibling RFEs (RHAIRFE-2630..2635). Surface this to strat.refine: either the roadmap pulls harness integration forward into 3.7, or the RFE's target moves — a positioning decision, not a feasibility issue.

6. **Target the current agent runtime, not the deprecated one (overlay 0015).** Agent frameworks/harnesses on RHOAI run under OpenShell (CLI/SDK at 3.5 Dev Preview, operator at 3.6); OpenShell injects the SPIFFE workload identity that the memory service uses as its RBAC principal (recommended-architecture §3). Integrations should be built against the OpenShell SDK/runtime — do not reference the removed Kagenti AgentRuntime CRD / AuthBridge.

7. **External-dependency policy (overlay 0008, low impact here).** Most of these integrations ship as client libraries/adapters, but if any target requires an external operator or cluster component, RHOAI will not auto-install it — it must be a documented prerequisite (reference GitOps path). Flagged for completeness; unlikely to bite.

8. **Deployment-mode portability must not fork the memory format.** The success criterion "a framework switch preserves memory and requires no integration work" has to hold across both server-side and client-side deployment modes of the one governed abstraction (recommended-architecture §4). Adapters must not persist harness-specific memory formats that break portability — otherwise the core Outcome promise ("memory survives a framework switch") is undermined by the integrations meant to deliver it.

### Scope assessment detail

The RFE bundles two separable deliverables under a single size-M label:
- (a) **Ready-made per-framework/harness integrations** (AC-1/2/3) — integration engineering across an unbounded "each supported major harness and framework," plus a maintained compatibility matrix and the harder "native context participation" requirement.
- (b) **Memory effectiveness on smaller self-hosted models** (AC-4) — a model-behavior + guidance-assets + evaluation effort, a different discipline with different owners (model serving / eval).

Recommend splitting (a) from (b). Independently, (a) alone — spanning multiple harnesses/frameworks, native-context integration, and an ongoing versioned/maintained lifecycle — is plausibly larger than M once the target list is fixed. Right-size after the harness/framework list and the small-model eval bar are pinned down in strat.refine.
