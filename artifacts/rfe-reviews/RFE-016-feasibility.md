### RFE-016: Memory effectiveness on smaller self-hosted models
**Feasibility**: feasible
**Strategy considerations**: (1) "governed memory" is not a single named service in the architecture — pin down which component/API realizes it and its 3.7 maturity; (2) defining and building the "effectiveness bar" is net-new eval work, not just running existing harness tasks — largest hidden complexity; (3) the "named smaller self-hosted model tier" is undefined and effectiveness is model-specific — a scoping decision that drives size; (4) "guidance or assets" spans a wide effort range (docs/prompts vs. scaffolding code vs. model fine-tuning) — must be nailed down to hold M size; (5) cross-team coordination (Agent Memory/OGX + Model Runtimes/vLLM + Evaluation teams; ai4rag is IBM-owned) is unstated; (6) small-model tool-calling reliability is partly a model-capability constraint, not only a prompting gap — the bar must be calibrated to the named tier; (7) disconnected eval (AC #3) must avoid a cloud "LLM-as-judge" and use a self-hosted judge or deterministic metrics; (8) confirm assets are consumable independently of RFE-009's harness integrations.
**Blockers**: none
**Scope assessment**: appropriate as a single strategy feature, with a scope-guard — at risk of exceeding "M" or needing a split if it expands into large-scale eval-harness task authoring across many models, or into model fine-tuning for tool-use.

---

## Feasibility verdict: Feasible

This can be built as an extension of the existing platform, not a rearchitecture. Every building block the RFE depends on already exists in RHOAI:

- **The memory/RAG capability is present.** OGX (formerly Llama Stack, per overlay 0003) ships a multi-provider gateway with vector storage (`/v1/vector-io/*`, `vector_stores`), an agentic tool-calling **Responses API** (`/v1/responses`), and pluggable vector-DB backends (Milvus, pgvector, Qdrant, FAISS). `ai4rag` sits on top of OGX and already performs RAG hyperparameter optimization with **Unitxt** evaluation (answer correctness, faithfulness, context correctness). The RFE's premise — "the capability to store and retrieve governed memory exists" — is consistent with these components. OGX's access-policy model (unowned readable by all; create requires auth; CRUD restricted to the resource owner) is the closest existing realization of "governed."
- **Self-hosted small-model serving is a first-class, heavily invested pathway.** vLLM is the primary self-hosted inference runtime (overlays 0014, 0015-vllm), served via KServe `LLMInferenceService` → `InferencePool` → llm-d (overlay 0011). Running memory workloads against a small model on the customer's own GPUs is exactly the supported topology; OGX activates a self-hosted vLLM backend via `VLLM_URL`/`VLLM_EMBEDDING_URL`.
- **Evaluation infrastructure to anchor an "effectiveness bar" exists.** eval-hub, lm-evaluation-harness (with HF-offline auto-detect), and ai4rag/Unitxt provide harness plumbing; the Model Runtimes test suite (`opendatahub-tests`, overlays 0014/0015-vllm) provides a validation home.
- **Disconnected/self-hosted is comprehensively supported.** RELATED_IMAGE + oc-mirror for air-gapped images; OGX pre-caches its default embedding model (granite-embedding-125m-english) and Docling models for offline operation; ai4rag ships a hermetic `uv.lock`. AC #3 (no dependence on frontier cloud models/external services) is satisfiable.

Because the ask is to author guidance + prompt/scaffolding assets and a measurable eval on top of capabilities that already ship, nothing in the platform architecture fundamentally conflicts with this need. Verdict: **feasible**.

There is no newly-named component in this RFE. The "platform memory service" / "governed memory" is described generically; its concrete realization today is OGX's memory/RAG APIs plus ai4rag. That gap is a definitional item for refinement (see consideration 1), not a blocker.

## Strategy considerations (carry into /strat.refine)

1. **"Governed memory" has no single named service in the 3.5-ea.2 architecture.** The parent Outcome (RHAISTRAT-1345, Agent Memory) presumably defines it, but the architecture context shows the capability distributed across OGX (vector-io / vector_stores / Responses) and ai4rag. Refinement must pin down precisely which component and API constitute "governed memory," what "governed" means (owner-scoped access control, tenancy, retention), and confirm its maturity at the 3.7 Tech Preview target.

2. **Defining and building the effectiveness bar is the core hidden complexity.** AC #2 requires validation against "a defined effectiveness bar," but no benchmark for *"does an agent invoke memory well"* exists today. This is net-new eval design — deciding what to measure (when to store, when to retrieve, correct recall, avoidance of spurious writes), which metrics, and what threshold counts as "reliable." The harness plumbing (Unitxt, lm-evaluation-harness, eval-hub) exists, but the memory-usage task/benchmark does not. This is the single largest effort driver and the most likely place scope balloons.

3. **The "named smaller self-hosted model tier" is undefined and effectiveness is model-specific.** Guidance tuned for one small model (e.g., a specific Granite size) may not transfer to another. AC #2/Success Criteria correctly say *"a named"* tier, but the RFE names none. Refinement must fix one named model/tier as the validation target; treating "smaller self-hosted models" as an open set makes validation unbounded and breaks the size estimate.

4. **"Guidance or assets" spans a wide effort range and must be bounded.** It could mean docs/prompting patterns (low), shipped system prompts / tool descriptions / scaffolding code (medium), a tuned configuration, or — at the far end — fine-tuning small models for better tool-use (large; pulls in the Training Hub/trainer stack). The RFE text ("prompting and scaffolding patterns") implies prompt-engineering assets, not retraining. The **M** size holds only if scope stays at guidance + prompt/scaffolding assets + one eval; drift toward per-model fine-tuning changes the effort class.

5. **Unstated cross-team coordination.** Delivery touches at least three teams: Agent Memory / OGX (memory API + governance), Model Runtimes / vLLM (self-hosted serving and the named model tier — overlays 0014, 0015-vllm), and Evaluation (eval-hub / lm-evaluation-harness for the bar). ai4rag is IBM-owned. The single-strategy, M-sized framing does not acknowledge this coordination surface.

6. **Small-model tool-calling reliability is partly a model-capability constraint, not only a prompting gap.** The RFE frames the problem as "the model does not reliably decide when and how to use [memory]" and proposes guidance/scaffolding as the fix. Below a certain capability level, function/tool-calling competence is intrinsic to the model and prompt guidance may not clear an arbitrary "reliable" bar. The effectiveness bar should be calibrated to what the named tier can actually achieve, or AC #1 ("use memory reliably") risks being unattainable by prompting alone on the smallest models. Feasible for a reasonably-capable small tier; flag as a calibration risk, not a blocker.

7. **Disconnected eval design constraint (AC #3).** A common eval pattern uses a frontier "LLM-as-judge," which would violate AC #3. The effectiveness bar must rely on a self-hosted judge model or deterministic/reference-based metrics (Unitxt supports the latter). Call this out so refinement does not design an eval that needs a cloud judge.

8. **Independence from the sibling split (RFE-009).** Split from RFE-009 (multi-framework harness integration); the business justification correctly asserts standalone value for the sovereign/on-prem self-hosted persona. Ensure the memory-effectiveness assets are consumable independently of the RFE-009 harness integrations, as the AC implies. No scope-overlap concern.

## Notes on architecture context and overlays

- Architecture context version read: **rhoai-3.5-ea.2**. The RFE targets **RHOAI 3.7** (Tech Preview), which is beyond the documented version, and **no overlay lists 3.7 or "all"** for the relevant components. I therefore treated the forward-marked (`release: next`) overlays whose `affects` intersect this RFE's components as applicable, and applied the durable OGX naming (overlay 0003, `release: 3.5`) as a naming correction. This is an interpretation of the release filter for a future-release RFE, flagged here for transparency.

Overlays applied:
- 0003: Llama Stack renamed to OGX — memory/RAG capability naming (durable; docs use "OGX (formerly Llama Stack)")
- 0011: KServe LLMInferenceService and llm-d integration — self-hosted serving pathway for the small model
- 0014: Model Runtimes team architecture — vLLM ownership and the opendatahub-tests validation home for the effectiveness bar
- 0015 (vllm-variant): vLLM variant architecture — self-hosted vLLM accelerator matrix and test suite
- 0015 (openshell): OpenShell is the agent security platform (replacing Kagenti) — current agent-runtime context if assets run inside agent sandboxes
