### RFE-001: Framework-agnostic agent memory service for AI agents on OpenShift AI
**Feasibility**: feasible
**Strategy considerations**: see list below (carry forward into `/strat.refine`)
**Blockers**: none
**Scope assessment**: needs splitting / phasing — the in-scope set is program-sized across 3.6→3.8; the Dev Preview (3.6) slice must be right-sized during strategy

```
Overlays applied:
- 0003: Llama Stack renamed to OGX; adopted in RHOAI 3.5 (naming + substrate identity)
- 0008: RHOAI does not auto-install external operator dependencies (vector-DB backend constraint)
- 0015: OpenShell is the agent security runtime, replacing Kagenti (agent-runtime context)
```
(Architecture context: `rhoai-3.5-ea.2`, read successfully. Overlays 0006 Connection API and 0005 HardwareProfile were reviewed but not formally applied — their `release` lists do not contain `3.5` or `all` — 0006 is noted below as supplementary context only.)

---

## Feasibility

**Feasible, and strongly aligned with the platform's direction.** This is an extension of the existing architecture, not a rearchitecture. The platform already ships the exact building blocks the RFE needs:

- **OGX Distribution (formerly Llama Stack)** is a running HTTP server (port 8321) built on the "pluggable providers activated by env vars" pattern — which *is* the framework-agnostic access model the RFE is asking for. It already exposes vector storage (`/v1/vector-io/insert|query`, `/v1/vector-stores`), an agentic Responses API with conversation/response state (`/v1/responses`, `openai_conversations` table), and OpenAI-compatible + Anthropic-Messages-compatible + native REST surfaces. Any framework that can speak HTTP can be a client, which directly supports "same memory across ≥3 frameworks."
- **Operator-configurable storage backends already exist in OGX**: vector DBs (Milvus, pgvector, Qdrant) plus file-based/inline (FAISS) providers, each toggled by an env var without the client changing. This maps almost one-to-one onto the RFE's acceptance criterion "vector database and file-based storage at minimum, backend model open to future types such as graph stores; agents unaffected by the backend choice."
- **Deployment, ingress, auth, disconnected, multi-arch are all handled**: OGX is deployed and lifecycle-managed by rhods-operator, exposed via Gateway API HTTPRoutes, authenticated via OAuth2/OIDC (JWKS), inherits FIPS from the AIPCC base, builds for amd64/arm64/ppc64le, and the RHOAI fork pre-caches the granite embedding model for offline/air-gapped file processing (RELATED_IMAGE + digest pinning). This covers the "self-hosted on OpenShift, including disconnected/air-gapped" criterion.
- **ai4rag** confirms OGX is the platform's sanctioned vector-store/retrieval substrate (provider-agnostic RAG over OGX Milvus/Qdrant), and **Feast** provides a second, feature-store-shaped substrate with vector similarity search and an MCP endpoint — so there is more than one credible storage foundation to build on.

The need does not fight the architecture; it sits squarely on the platform's emerging agentic direction (OGX agentic APIs + OpenShell agent runtime). A framework-agnostic memory capability is precisely what a pluggable-provider HTTP gateway is designed to host. That the unified memory API does not yet exist is not a feasibility problem — that is what the RFE is for.

## What is genuinely net-new (not yet in the platform)

OGX gives you vector storage (semantic) and conversation/response state (working-ish), but it does **not** today provide a unified, governed store spanning **working, episodic, semantic, and procedural** memory as first-class access patterns, nor a framework-neutral memory abstraction with a portability guarantee. That memory model is the core new work. This is legitimate RFE territory; it is called out here only to size the effort honestly.

## Strategy considerations (for `/strat.refine` — none of these block submission)

1. **Four memory types over one governed store is the central design risk.** Working (short-lived session state), episodic (event log), semantic (vector), and procedural (learned procedures) have different lifetimes and access patterns. OGX supplies vector storage + conversation state, not a unified four-type model. The abstraction that unifies them over one store — without leaking the backend — is the hard part and should be the primary strategy focus.

2. **"100% memory retention on framework switch" needs a precise definition.** Retaining raw memory *content* across a framework change is feasible (it is just data behind a stable API). Retaining *retrieval behavior* is not automatic: embeddings are embedding-model-specific, so if two frameworks or two deployments use different embedding models/chunking, preserving semantic-recall parity may require re-embedding. Strategy must define the guarantee as content-retention vs. behavior-retention and pin the embedding-model contract accordingly.

3. **Hybrid (semantic + keyword) retrieval is not uniform across backends.** Milvus supports hybrid natively; pgvector needs Postgres full-text/BM25; the file-based FAISS/inline path (the natural air-gap default) is vector-only and would need a separate keyword index. "Hybrid retrieval" + "same behavior across all backends" + "file-based backend at minimum" are in tension and must be reconciled (e.g., define a capability floor per backend, or ship keyword indexing in the memory layer).

4. **Vector-DB backend vs. the no-auto-install policy (overlay 0008).** RHOAI will not install, upgrade, or manage an external vector-DB operator (Milvus, Qdrant, etc.) on the customer's behalf. For self-hosted/air-gapped accounts (ITZBund ~900 GPUs, BNP Paribas), a vector DB offered via its own operator becomes an admin-provisioned, admin-mirrored prerequisite. The zero-external-dependency paths — file-based (FAISS) to start, or pgvector on a platform-managed PostgreSQL — sidestep this and align with the RFE's own "file-based to start, a vector database later" phasing. Strategy must choose the backend story against this standing policy and surface any missing dependency on DSC/DSCI status rather than auto-installing.

5. **Substrate decision is an open architectural choice (keep it in strategy, not the RFE).** OGX is the strongest fit (agentic APIs, pluggable vector/file providers, framework-agnostic HTTP, operator-managed, air-gap-ready). Feast is a viable alternative for the storage/registry layer (vector search + MCP) but is feature-store-shaped, not memory-shaped. A net-new component is a third option. The RFE correctly does not prescribe this; strategy should decide OGX-provider vs. Feast-backed vs. new-component.

6. **Multi-tenancy floor must not be foreclosed.** OGX's built-in access policy is owner-based without namespace-level isolation. A *platform* memory service holding per-agent/per-tenant memories needs a tenancy model. The RFE defers scope isolation to the governed-memory follow-on RFE — acceptable — but the base store and API must be designed so that per-tenant/per-agent isolation can be added without a data-model migration.

7. **Design governance hooks in early even though governance is out of scope.** The out-of-scope items (scope isolation, sensitive-data screening, write auditability) overlap with OpenShell's OPA policy and OCSF audit-event capabilities (overlay 0015). The memory API should expose the seams (identity on writes, policy-check points, audit event emission) so the governed-memory follow-on and OpenShell can plug in later without reworking the interface. This is a cross-component coordination note between the memory service, the governed-memory RFE, and OpenShell.

8. **"OpenClaw" is not in the platform inventory.** It is named in User Scenario 1 and the acceptance criteria as an example harness. Treat it as the author's illustrative client, not a prerequisite — consistent with the RFE's own open question about which frameworks are first-class validated clients vs. documented-only. Not a blocker; the framework-agnostic HTTP surface makes the *set* of clients a configuration/validation decision, not an architectural one.

9. **Air-gap embedding-model story.** The default embedding model (OGX ships granite-embedding-125m-english pre-cached) must be mirrorable/in-image for disconnected clusters, and its choice couples to consideration #2 (embedding-space portability). Confirm the embedding model is part of the shipped/mirrored artifact set for air-gapped installs.

10. **Supplementary (not an applied overlay): Connection API (overlay 0006).** If the memory store's backend credentials/endpoints are wired through the platform's existing Connection API (S3/OCI/URI Secrets injected at admission with RBAC), strategy gets a consistent, already-GA credential path instead of bespoke Secret plumbing. Flagged as an integration opportunity; the overlay's release list does not include 3.5, so treat as advisory.

## Scope assessment (adversarial)

As an RFE describing the business need (WHAT/WHY) with explicit in/out-of-scope carve-outs, the framing is clean and coherent. The concern is the **delivery scope of the in-scope set**: a unified four-type memory model + a framework-neutral portability guarantee + ≥2 storage backends + hybrid retrieval + air-gap, delivered Dev Preview (3.6) → Tech Preview (3.7) → GA (3.8). That is a multi-release program, not a single strategy feature. The natural split seams are (a) the memory model / core API, (b) the multi-framework client + portability guarantee, and (c) the backend/retrieval matrix (hybrid across vector + file). Recommend strategy right-size the **Dev Preview** slice to a minimal memory API + one or two zero-external-dependency backends + a subset of validated framework clients, and treat portability-at-100% and hybrid-across-all-backends as later-phase hardening. This is a phasing/splitting note, not a reason to hold the RFE.
