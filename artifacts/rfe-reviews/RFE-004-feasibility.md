### RFE-004: Built-in agent memory in AI Hub (interim Dev Preview)

**Feasibility**: feasible
**Strategy considerations**: see list below (per-user isolation depends on OGX auth + identity propagation; view/delete-individual-memory is not a confirmed first-class OGX API; the "memory tool" prior art is not in the 3.5-ea.2 OGX build; persistence/embedding dependencies; interim-vs-comprehensive coexistence; 3.5.x z-stream targeting; OGX naming)
**Blockers**: none
**Scope assessment**: appropriate, with sizing risk concentrated in the isolation and view/delete acceptance criteria

---

Architecture context: `rhoai-3.5-ea.2` (PLATFORM.md + ogx-distribution.md + odh-dashboard.md).

Overlays applied:
- 0003: Llama Stack renamed to OGX in RHOAI 3.5 — the RFE's "Responses layer" is the OGX (formerly Llama Stack) Distribution; use OGX naming.
- 0015: OpenShell replaces Kagenti (affects: platform) — reviewed and matches, but immaterial to memory feasibility. It governs agent *security/sandboxing*, not memory. Only relevant caveat: the dashboard's agent-ops BFF still references `AgentRuntime` (kagenti.dev) CRs, which are deprecated under 0015 — but this RFE targets the gen-ai playground surface, not agent-ops, so it is unaffected.

## Why this is feasible

The RFE's core claim — that the platform's Responses/files/vector-store plumbing already exists and is wireable into AI Hub — is confirmed by the architecture context, so this is an extension/surfacing task, not a rearchitecting one:

- **OGX Distribution (v1.1.2+rhaiv.0, shipping in 3.5-ea.2)** exposes exactly the plumbing the RFE cites: `/v1/responses` (agentic Responses API, tool-calling/streaming), `/v1/vector-io/insert` + `/v1/vector-io/query` (vector store), and `/v1alpha/file-processors/process` (files). It persists state in PostgreSQL with tables that already include `agents_responses`, `openai_conversations`, `files_metadata`, and `vector_store_metadata` — i.e., cross-session persistence is a built-in property, not something to invent.
- **The AI Hub surface already exists and already talks to OGX.** odh-dashboard ships a federated `gen-ai` module ("LLM playground, prompt engineering, guardrails") whose BFF proxies the OGX/LlamaStack API on 8321 using `user_token`. So "enable memory for an agent or playground session in AI Hub" maps onto an existing UI + BFF path — the "modest UI work" framing is credible.
- **User identity already flows to the backend.** The gen-ai BFF proxies with `user_token`, which is the raw material for the per-user isolation AC (OGX's access-policy model restricts CRUD to the resource owner).

No architectural incompatibility exists. A capability gap (a packaged, UI-exposed memory feature) is precisely what an RFE is for.

## Strategy considerations (carry into /strat.refine — not reasons to block)

1. **Per-user isolation hinges on OGX auth being enabled AND identity being propagated as owner identity.** OGX's access policy ("unowned resources readable by all; create requires auth; read/update/delete restricted to the resource owner") only produces per-user isolation when OAuth2/OIDC auth is active — and that auth is *optional*, activated only when `AUTH_ISSUER`/`AUTH_JWKS_URI` are set. If the platform deploys OGX without auth wired, "unowned" memories are readable by all authenticated users, directly contradicting AC "each user's memories are isolated to that user." Whether the gen-ai BFF's `user_token` reaches OGX as a JWT that OGX maps to a distinct resource owner (vs. a shared/service identity) needs to be confirmed. This is cross-component identity-propagation work and the single most likely place for hidden effort. Multi-tenancy note: OGX provides owner-scoped isolation but *not* namespace-level isolation.

2. **"View what an agent has remembered and delete individual memories" (AC4) is not a confirmed first-class OGX API.** The documented vector-io surface is insert/query; there is no documented list/enumerate or delete-by-id for stored memories, and the Responses/conversation tables are backing state rather than a curated memory-management API. Enumerating and deleting individual memory items may require additional OGX (likely upstream) API surface plus dashboard UI, which is cross-repo coordination the "modest UI work" framing does not capture.

3. **The specific "memory tool" prior art is not present in the 3.5-ea.2 OGX build.** The RFE cites a memory tool with explicit "remember this" and implicit auto-remember "shipped in the latest development build." The 3.5-ea.2 OGX Distribution documents the Responses/vector-io/files primitives but no memory-tool abstraction. So the tool lives in a newer dev build / upstream OGX than this snapshot. Delivery depends on that tool landing in the *shipped* OGX distribution and its release train (OGX is pinned per RHOAI release via `ogx v1.1.2+rhaiv.0`); the interim feature inherits OGX's cadence. (Engineering determines the approach — this is non-prescriptive prior art.)

4. **Persistence, embedding, and lifecycle dependencies.** Auto-remember with semantic recall needs a deployed embedding endpoint (`VLLM_EMBEDDING_URL` / `EMBEDDING_MODEL`, default granite-embedding-125m) — a runtime dependency the RFE does not name. Persistent per-user memory grows the vector store and PostgreSQL over time; OGX's backing PostgreSQL is a single-instance store (no built-in cross-instance replication in the platform's DB pattern), so data retention, deletion-cascade, and storage-growth behavior for an always-on memory feature are real design questions.

5. **Coexistence with the comprehensive memory service (parent Outcome RHAISTRAT-1345).** The RFE deliberately runs two intersecting Dev Preview memory implementations under one Outcome. Downstream risk to flag for strategy: memories captured in the interim OGX store may not migrate to the later governed service, and API/behavior divergence could create user-expectation and data-migration debt at the TP (3.7)/GA (3.8) handoff. The RFE acknowledges the team accepted the intersection, so this is a managed risk, not a blocker.

6. **3.5.x z-stream targeting is unusual for a new user-facing feature.** Success criteria prefer 3.6, "3.5.x if feasible." Z-stream updates are conventionally bugfix/CVE-only; introducing a new Dev Preview capability in 3.5.x may conflict with release-train norms and should be validated with release engineering. (3.6 as the primary target is unremarkable.)

7. **Naming.** Per overlay 0003, use "OGX (formerly Llama Stack)." The dashboard and OGX docs are mid-transition and still mix "LlamaStack Service" and "OGX API"; strategy should standardize.

## Scope assessment

Size M is plausible *if* the memory tool is genuinely ready in a shippable OGX build and the work is (a) include it in the shipped OGX distribution, (b) add gen-ai BFF proxy routes, and (c) add dashboard UI for enable/view/delete. The two ACs most likely to push past M are per-user isolation (consideration 1 — potential upstream OGX auth/identity work) and view/delete-individual-memory (consideration 2 — potential new OGX API surface). No split is warranted at RFE stage; strategy refinement should size those two ACs explicitly before committing to M.
