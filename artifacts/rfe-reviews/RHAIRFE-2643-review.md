---
rfe_id: RHAIRFE-2643
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

TITLE: Memory effectiveness on smaller self-hosted models

| Criterion | Score | Notes |
|-----------|-------|-------|
| WHAT      | 2/2   | Clear, specific need: teams running smaller self-hosted models need the platform memory service to be effective in that model tier. The capability to store/retrieve governed memory exists, but a smaller model does not reliably decide when/how to invoke it without task-specific guidance; they need shipped guidance and assets that make memory usage effective on the models they run on their own GPUs. Well scoped and unambiguous. |
| WHY       | 2/2   | Named account: ITZBund, a sovereign/on-premise account running self-hosted models on its own GPUs, directly tied to the need. Backed by a clear strategic causal chain: on-premise/sovereign/disconnected accounts choose OpenShift AI precisely because they do not send traffic to frontier cloud models, so governed memory working only on frontier models leaves the differentiator hollow for exactly the accounts most likely to buy on it. Named account plus a coherent strategic rationale. |
| Open to HOW | 2/2 | Describes the outcome (memory effective on smaller self-hosted models, validated against a defined effectiveness bar, usable disconnected) without prescribing architecture. "Guidance or assets" is deliberately left open for engineering to determine the form (prompting, scaffolding, fine-tuning, etc.). "Prompting and scaffolding patterns" appear only as the problem teams face today, not as a mandated solution. Platform vocabulary (governed memory service, self-hosted models, GPUs) only. |
| Not a task | 2/2  | A genuine business need — making a differentiating capability effective for a specific, distinct persona/account set (sovereign, on-premise, disconnected self-hosted). Driven by customer requirement and a Red Hat differentiator, not a chore, tech-debt, or engineering activity. |
| Right-sized | 2/2 | Focused single need mapping to one strategy feature (parent RHAISTRAT-1345, Agent Memory). The three acceptance criteria — shipped guidance/assets, validation against an effectiveness bar, and disconnected-deployment documentation — are interdependent facets of one deliverable; none ships or provides value without the others. |
| **Total** | **10/10** | **PASS** |

### Verdict
A well-formed, focused RFE that pairs a clear customer need with a named sovereign account and a strong strategic differentiator rationale, leaving implementation fully open to engineering.

### Feedback
Strengths: crisp WHAT, a named account (ITZBund) tied to a persuasive differentiator causal chain, outcome-based acceptance criteria that avoid prescribing HOW, and tight scope under a single strategy parent. Minor improvements to consider (not required for pass): quantify the ITZBund impact (deal size, number of affected accounts) to further harden the WHY, and name or bound the "smaller self-hosted model tier" and the "defined effectiveness bar" so success is testable at Tech Preview rather than left to later definition.

## Technical Feasibility

**Feasibility verdict: Feasible**

This can be built as an extension of the existing platform, not a rearchitecture. Every building block the RFE depends on already exists in RHOAI:

- **The memory/RAG capability is present.** OGX (formerly Llama Stack, per overlay 0003) ships a multi-provider gateway with vector storage (`/v1/vector-io/*`, `vector_stores`), an agentic tool-calling **Responses API** (`/v1/responses`), and pluggable vector-DB backends (Milvus, pgvector, Qdrant, FAISS). `ai4rag` sits on top of OGX and already performs RAG hyperparameter optimization with **Unitxt** evaluation (answer correctness, faithfulness, context correctness). The RFE's premise — "the capability to store and retrieve governed memory exists" — is consistent with these components. OGX's access-policy model (unowned readable by all; create requires auth; CRUD restricted to the resource owner) is the closest existing realization of "governed."
- **Self-hosted small-model serving is a first-class, heavily invested pathway.** vLLM is the primary self-hosted inference runtime (overlays 0014, 0015-vllm), served via KServe `LLMInferenceService` → `InferencePool` → llm-d (overlay 0011). Running memory workloads against a small model on the customer's own GPUs is exactly the supported topology; OGX activates a self-hosted vLLM backend via `VLLM_URL`/`VLLM_EMBEDDING_URL`.
- **Evaluation infrastructure to anchor an "effectiveness bar" exists.** eval-hub, lm-evaluation-harness (with HF-offline auto-detect), and ai4rag/Unitxt provide harness plumbing; the Model Runtimes test suite (`opendatahub-tests`, overlays 0014/0015-vllm) provides a validation home.
- **Disconnected/self-hosted is comprehensively supported.** RELATED_IMAGE + oc-mirror for air-gapped images; OGX pre-caches its default embedding model (granite-embedding-125m-english) and Docling models for offline operation; ai4rag ships a hermetic `uv.lock`. AC #3 (no dependence on frontier cloud models/external services) is satisfiable.

Because the ask is to author guidance + prompt/scaffolding assets and a measurable eval on top of capabilities that already ship, nothing in the platform architecture fundamentally conflicts with this need. Verdict: **feasible**.

There is no newly-named component in this RFE. The "platform memory service" / "governed memory" is described generically; its concrete realization today is OGX's memory/RAG APIs plus ai4rag. That gap is a definitional item for refinement (see strategy consideration 1), not a blocker.

**Blockers:** none

**Scope assessment:** appropriate as a single strategy feature, with a scope-guard — at risk of exceeding "M" or needing a split if it expands into large-scale eval-harness task authoring across many models, or into model fine-tuning for tool-use.

### Notes on architecture context and overlays

- Architecture context version read: **rhoai-3.5-ea.2**. The RFE targets **RHOAI 3.7** (Tech Preview), which is beyond the documented version, and **no overlay lists 3.7 or "all"** for the relevant components. The forward-marked (`release: next`) overlays whose `affects` intersect this RFE's components were treated as applicable, and the durable OGX naming (overlay 0003, `release: 3.5`) applied as a naming correction. This is an interpretation of the release filter for a future-release RFE, flagged here for transparency.

Overlays applied:
- 0003: Llama Stack renamed to OGX — memory/RAG capability naming (durable; docs use "OGX (formerly Llama Stack)")
- 0011: KServe LLMInferenceService and llm-d integration — self-hosted serving pathway for the small model
- 0014: Model Runtimes team architecture — vLLM ownership and the opendatahub-tests validation home for the effectiveness bar
- 0015 (vllm-variant): vLLM variant architecture — self-hosted vLLM accelerator matrix and test suite
- 0015 (openshell): OpenShell is the agent security platform (replacing Kagenti) — current agent-runtime context if assets run inside agent sandboxes

## Strategy Considerations

Carry the following into /strat.refine:

1. **"Governed memory" has no single named service in the 3.5-ea.2 architecture.** The parent Outcome (RHAISTRAT-1345, Agent Memory) presumably defines it, but the architecture context shows the capability distributed across OGX (vector-io / vector_stores / Responses) and ai4rag. Refinement must pin down precisely which component and API constitute "governed memory," what "governed" means (owner-scoped access control, tenancy, retention), and confirm its maturity at the 3.7 Tech Preview target.

2. **Defining and building the effectiveness bar is the core hidden complexity.** AC #2 requires validation against "a defined effectiveness bar," but no benchmark for *"does an agent invoke memory well"* exists today. This is net-new eval design — deciding what to measure (when to store, when to retrieve, correct recall, avoidance of spurious writes), which metrics, and what threshold counts as "reliable." The harness plumbing (Unitxt, lm-evaluation-harness, eval-hub) exists, but the memory-usage task/benchmark does not. This is the single largest effort driver and the most likely place scope balloons.

3. **The "named smaller self-hosted model tier" is undefined and effectiveness is model-specific.** Guidance tuned for one small model (e.g., a specific Granite size) may not transfer to another. AC #2/Success Criteria correctly say *"a named"* tier, but the RFE names none. Refinement must fix one named model/tier as the validation target; treating "smaller self-hosted models" as an open set makes validation unbounded and breaks the size estimate.

4. **"Guidance or assets" spans a wide effort range and must be bounded.** It could mean docs/prompting patterns (low), shipped system prompts / tool descriptions / scaffolding code (medium), a tuned configuration, or — at the far end — fine-tuning small models for better tool-use (large; pulls in the Training Hub/trainer stack). The RFE text ("prompting and scaffolding patterns") implies prompt-engineering assets, not retraining. The **M** size holds only if scope stays at guidance + prompt/scaffolding assets + one eval; drift toward per-model fine-tuning changes the effort class.

5. **Unstated cross-team coordination.** Delivery touches at least three teams: Agent Memory / OGX (memory API + governance), Model Runtimes / vLLM (self-hosted serving and the named model tier — overlays 0014, 0015-vllm), and Evaluation (eval-hub / lm-evaluation-harness for the bar). ai4rag is IBM-owned. The single-strategy, M-sized framing does not acknowledge this coordination surface.

6. **Small-model tool-calling reliability is partly a model-capability constraint, not only a prompting gap.** The RFE frames the problem as "the model does not reliably decide when and how to use [memory]" and proposes guidance/scaffolding as the fix. Below a certain capability level, function/tool-calling competence is intrinsic to the model and prompt guidance may not clear an arbitrary "reliable" bar. The effectiveness bar should be calibrated to what the named tier can actually achieve, or AC #1 ("use memory reliably") risks being unattainable by prompting alone on the smallest models. Feasible for a reasonably-capable small tier; a calibration risk, not a blocker.

7. **Disconnected eval design constraint (AC #3).** A common eval pattern uses a frontier "LLM-as-judge," which would violate AC #3. The effectiveness bar must rely on a self-hosted judge model or deterministic/reference-based metrics (Unitxt supports the latter). Call this out so refinement does not design an eval that needs a cloud judge.

8. **Independence from the sibling split (RFE-009).** Split from RFE-009 (multi-framework harness integration); the business justification correctly asserts standalone value for the sovereign/on-prem self-hosted persona. Ensure the memory-effectiveness assets are consumable independently of the RFE-009 harness integrations, as the AC implies. No scope-overlap concern.

## Revision History

none (first pass)
