### RFE-002: Agent memory available as governed MCP tools
**Feasibility**: feasible
**Strategy considerations**: see list below (7 items for /strat.refine)
**Blockers**: none
**Scope assessment**: appropriate for the MCP-surface slice, with a scope-creep risk on the bundled catalog + full-governance ACs (confirm during /strat.refine)

---

Architecture context: `rhoai-3.5-ea.2` (PLATFORM.md read).

Overlays applied:
- 0010: Project Navigator (rhoai-mcp) maturity — Developer Preview in 3.4, planned Tech Preview in 3.5; feature spans rhoai-mcp (frontend) + llm-d-planner (backend)
- 0015: OpenShell replaces Kagenti as the agent security/identity platform (SPIFFE workload identity, OPA, OCSF audit)
- 0008: Platform policy — RHOAI does not auto-install external operator dependencies

## Feasibility rationale

This is feasible and, more than that, it runs *with* the platform's architecture rather than against it. Nothing here requires rearchitecting; it extends surfaces that already exist.

- **The MCP surface already exists and is extensible.** `rhoai-mcp` (RHOAI MCP Server) is a Python/FastMCP service with a pluggy-based plugin architecture where each domain registers its own MCP tools, resources, and prompts. It explicitly supports third-party/out-of-tree plugins via Python entry points (`rhoai_mcp.plugins`). A "memory" domain plugin (store/search/retrieve) fits this model directly. It already serves stdio and HTTP transports (SSE, streamable-http), so off-the-shelf MCP clients can reach it (Success Criterion 1 is achievable).
- **The stateless-scoping concern the RFE calls out is already solved.** rhoai-mcp derives caller identity per request from an OIDC Bearer token (JWT via JWKS, or opaque token via K8s TokenReview), then enforces per-tool RBAC via SubjectAccessReview and impersonates the user for downstream calls. Identity travels on each request, not on a transport session — exactly what AC #3 needs for stateless MCP connections. Feasible with the existing auth model.
- **A real MCP catalog surface exists (AC #2).** The Model Registry's Model Catalog service exposes `/api/mcp_catalog/v1alpha1/mcp_servers` (list servers, get details, list tools); the three-tier catalog (Red Hat / partner / community) is generated build-time by `model-metadata-collection` (`--mcp-index`) and surfaced in the dashboard. Listing memory-as-MCP there is a known, shipping path.
- **MCP governance surfaces exist or are emerging (AC #4).** Options in-platform: rhoai-mcp's own per-tool SubjectAccessReview RBAC; Gateway API + Kuadrant AuthPolicy (as used by MaaS); the MCP Gateway pathway (NeMo Guardrails watching `MCPGatewayExtension` resources, new in TrustyAI 3.5); Prometheus `/metrics` for usage; and OpenShell OCSF security events for audit. Governing memory MCP traffic is feasible against these.

No architectural incompatibility found. A memory storage backend does not exist in the 3.5-ea.2 component inventory — but that is the parent Outcome (RHAISTRAT-1345, Agent Memory), not a prerequisite this RFE must invent, and "capability not existing yet" is not infeasibility.

## Strategy considerations (carry into /strat.refine — none of these block submission)

1. **Backend dependency / sequencing.** This RFE is the *MCP surface over* a memory capability, not the memory store itself. No store/search/retrieve memory service is in the platform inventory today; it must be delivered by sibling work under the parent Outcome (RHAISTRAT-1345). The MCP surface cannot go end-to-end before that backend's API exists. Cross-team dependency to make explicit.

2. **"Existing MCP governance capabilities" overstates current maturity.** The platform does not yet have one uniform MCP governance plane. It has *several* young, non-uniform mechanisms: rhoai-mcp's per-tool RBAC, MaaS-style Kuadrant AuthPolicy, and the MCP Gateway/NeMo-Guardrails path (MCPGatewayExtension) introduced in 3.5. Engineering must decide which plane memory-MCP plugs into and accept that "governed exactly like every other MCP server" describes a target state, not today's state. Pulls in the TrustyAI/guardrails and model-catalog teams.

3. **Host decision: extend rhoai-mcp vs. a dedicated memory MCP server.** rhoai-mcp is v0.1, Developer Preview in RHOAI (overlay 0010), and its RHOAI overlay ships **read-only mode on by default**. Memory is inherently read-write. Whether memory tools live inside rhoai-mcp (requiring writes to be enabled in a read-only-by-default, DP-maturity server) or in a separate memory MCP server is an architecture decision with real consequences for the enterprise-grade governance the ACs assume.

4. **Three-way scoping (user + agent + project) crosses two identity planes.** rhoai-mcp scopes to *user* (OIDC/K8s identity) and *project* (namespace RBAC) today, but *agent* identity is a distinct dimension. Platform agent identity now comes from OpenShell (SPIFFE workload identity, replacing Kagenti — overlay 0015), a different system from the OIDC-user model rhoai-mcp uses. Reconciling user-vs-agent-vs-project scoping across the OIDC plane and the SPIFFE agent-identity plane is a genuine cross-cutting design question, not a config tweak.

5. **Catalog registration is a build-time, cross-team content task.** Discoverability (AC #2) means adding memory-MCP to the curated three-tier index consumed by `model-metadata-collection` and mounted by the dashboard — owned by the model-registry/catalog team, not the memory team. Also note the current MCP catalog GET APIs are largely unauthenticated reads (a design detail to confirm, not a blocker).

6. **AC #5's "emerging community memory-tool conventions" is a moving target.** Naming/semantics parity with third-party memory tools is technically easy, but the conventions are unstandardized and shifting. Committing interop to "what leading harnesses currently do" is a design/maintenance risk to name explicitly.

7. **External-operator policy (overlay 0008).** If the memory backend needs an external datastore/operator (e.g., a vector DB and its operator), RHOAI will not auto-install it; it must be a documented prerequisite surfaced on DSC/DSCI. Relevant chiefly to the backend, but the "off-the-shelf client uses platform memory end to end" success criterion inherits that dependency.

## Scope note

The core slice — expose memory store/search/retrieve as MCP tools with correct per-user/project scoping — is a reasonable M. The risk is that ACs #2 (catalog listing) and #4 (full governance parity) each recruit a different team and a different still-maturing surface (Model Catalog pipeline; MCP Gateway / NeMo Guardrails; Kuadrant). If those are treated as must-haves *for this RFE* rather than fast-follows, the true effort exceeds M. Recommend /strat.refine explicitly decide whether catalog listing and full governance parity are in-scope here or separate follow-ups. Not a hard "needs splitting," but a scope-creep risk worth naming.
