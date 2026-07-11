---
rfe_id: RHAIRFE-2637
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

TITLE: Organization-wide shared agent memory with scope tiers, conflict handling, and provenance

| Criterion | Score | Notes |
|-----------|-------|-------|
| WHAT      | 2/2   | Clear and specific: memory shared deliberately across organizational boundaries (user, project, role, organization tiers), with conflicts detected/flagged rather than silently coexisting, and every record traceable to its origin. Problem statement, user scenarios, and acceptance criteria make the need concrete. |
| WHY       | 2/2   | Named customer accounts with demonstrated consequences: OCBC Bank (tiered sharing with enforced boundaries is "the exact ask"), NTT Data (Zero Trust, role-scoped memory), plus healthcare accounts on file. Explicit causal chain: named accounts "cannot move past pilot without it — isolation-only memory caps them at single-team usage." Reinforced by strategic-differentiation argument (governance depth as Red Hat's stated market differentiation). |
| Open to HOW | 2/2 | Describes needs and observable outcomes, not internal architecture. "Conflicts are detected and flagged," "records carry provenance," "reads respect tier visibility rules" are all outcomes engineering can satisfy any number of ways. Platform-vocabulary references only (platform identity/roles, OpenShift-native analogue). No DB schemas, tools, or design docs mandated as the solution. |
| Not a task | 2/2  | Clear business need — enterprises need shared, trustworthy agent memory to unlock the "enterprise brain" value and unblock regulated pilots. Not a chore, tech-debt item, or engineering activity. |
| Right-sized | 2/2 | Deliverables identified: (a) scope tiers + visibility rules, (b) controlled cross-tier sharing, (c) conflict detection/flagging, (d) provenance + origin tracing. Independence test: sharing requires tiers to exist; conflicts only arise within shared scopes (so conflict handling depends on sharing); conflict flagging surfaces both records' origins (so it depends on provenance); the RFE argues untrusted shared memory is "worse than none," so sharing without conflict-handling and provenance is not shippable value. The four facets are one coherent trust capability, matching the R=2 pattern. Adjacent concerns (isolation, adversarial defense, admin console) are explicitly scoped out to separate RFEs — deliberate right-sizing. Maps to one strategy feature (RHAISTRAT-1345 Agent Memory, Tech Preview slice). |
| **Total** | **10/10** | **PASS** |

### Verdict
A model RFE: a tightly scoped, trust-centered shared-memory capability justified by named enterprise accounts blocked at pilot, described as outcomes without prescribing architecture.

### Feedback
Strengths: named accounts (OCBC Bank, NTT Data) with an explicit blocked-at-pilot consequence chain; a coherent "one trust problem" framing that survives the independence test; disciplined scoping that pushes isolation, adversarial defense, and admin-console surfaces to separate RFEs; measurable success criteria (regulated two-team pilot passing security review, zero unflagged contradictions in conflict-injection testing). Minor improvements only: the open question about prototype tiers with no OpenShift-native analogue could note a decision owner/date, and the healthcare accounts could be named (as OCBC and NTT Data are) to make that evidence as strong as the rest.

## Technical Feasibility

### RFE-010: Organization-wide shared agent memory with scope tiers, conflict handling, and provenance

**Feasibility**: feasible
**Strategy considerations**: scope-tier → platform-identity mapping; identity-scoped read enforcement (target OpenShell, not Kagenti); cross-tenant shared store vs. per-instance norm; conflict detection is a semantic (non-platform) capability with an absolute success bar; provenance needs write-path coordination with the agent runtime; storage substrate not yet a named platform service; external-operator dependency policy; poisoning-defense expectation gap; promotion audit surface.
**Blockers**: none
**Scope assessment**: appropriate for a Tech Preview trust story, with a split risk — conflict detection is the most separable and highest-effort pillar and is the primary candidate to carve out during `/strat.refine`.

```
Overlays applied:
- 0015: OpenShell is the agent security/identity platform for RHOAI, replacing Kagenti (SPIFFE identity, OPA policy, OCSF events)
- 0008: RHOAI does not auto-install external operator dependencies (admin-owned prerequisites, surfaced on DSC/DSCI)
```

Architecture context available: yes (rhoai-3.5-ea.2, PLATFORM.md + agents-operator, ai4rag, plus overlays 0015 and 0008).

---

#### Summary of judgment

This is **feasible**. Nothing in the RFE requires rearchitecting the platform — it extends it. Every primitive the RFE leans on already exists in some form: rich identity/authorization (Kubernetes RBAC with 684 role entries, OIDC/Keycloak, SPIFFE/SPIRE via OpenShell, kube-rbac-proxy SubjectAccessReview, Kuadrant/Authorino AuthPolicy, OpenShell's integrated OPA engine), persistence substrates (OGX/Llama Stack vector stores — Milvus/Qdrant, Feast, PostgreSQL as the dominant state store), and a lineage-tracking precedent (ML Metadata for pipeline provenance). Building org-wide shared memory with scope tiers, controlled promotion, conflict flagging, and provenance is net-new capability, but "a capability not existing yet is not a blocker — that's what RFEs are for." The RFE is well-structured, the underlying need is unambiguous, and it names no non-existent component as a prerequisite, so it is neither infeasible nor indeterminate.

The RFE's direction *aligns with* rather than fights the platform's architecture: governance depth (SPIFFE identity, OPA policy, OCSF security events through OpenShell; Kuadrant/Authorino auth; kube-rbac-proxy) is exactly the substrate that identity-scoped, auditable shared memory should build on. This is a genuine architectural fit, not a forced one.

The real work is concentrated in strategy refinement, and it is substantial. The considerations below are for `/strat.refine`, not reasons to block.

---

#### Strategy Considerations

1. **Scope-tier → platform-identity mapping is a design decision, not a given.** The four tiers (user / project / role / organization) map only partially onto OpenShift-native constructs: user → user identity, project → namespace/project, role → OpenShift Group / ClusterRole, organization → cluster/org scope. The mapping for "role" and "organization" needs deliberate design, and the RFE's own open question flags the prototype tiers (campaign, enterprise-wide beyond org) that have *no* OpenShift-native analogue. Strategy must decide the tier→identity mapping and whether the non-native tiers are in scope for Tech Preview or stay a design horizon.

2. **Identity-scoped read enforcement must reuse an existing enforcement point.** AC "access to shared tiers honors platform identity and roles, demonstrably to a customer security reviewer" requires the memory store to enforce platform identity *at read time*. Strategy should pick an existing enforcement mechanism (SubjectAccessReview / kube-rbac-proxy, Kuadrant AuthPolicy + Authorino, or OpenShell's OPA engine) rather than inventing a bespoke auth path — a new auth path is where security review fails. Per overlay **0015**, agent identity is OpenShell SPIFFE + platform OIDC/Keycloak; the deprecated Kagenti AgentRuntime CRD / AuthBridge sidecar / bundle-service must NOT be referenced. This is a strong fit for NTT Data's Zero Trust ask (SPIFFE workload identity + role-scoped access) and OCBC's tiered-with-enforced-boundaries ask.

3. **A cross-tenant shared store is a different isolation model than the platform norm.** The platform's prevailing pattern is per-namespace / per-instance state stores (Model Registry is per-instance with its own PostgreSQL and no cross-instance replication; DSPA is per-instance). Org-wide shared memory that enforces *internal* scope isolation is a single logical cross-tenant service with record/scope-level access control — architecturally novel for RHOAI, though not incompatible. Strategy must design the tenant-isolation-within-a-shared-store model (and its HA/data-residency story) explicitly; this is the crux of OCBC's "shared within a team but never leaks across teams" requirement.

4. **Conflict detection is a semantic capability, not a platform primitive — and the success bar is absolute.** Detecting "contradictory" memories is fundamentally different engineering from scope-tier access control or provenance: it needs semantic comparison (embedding similarity plus contradiction reasoning, likely LLM-assisted), which is inherently probabilistic. The success criterion "zero unflagged contradictions in conflict-injection testing" is an absolute guarantee against a probabilistic capability. Strategy should define the conflict taxonomy the system *detects deterministically* vs. *surfaces as divergent candidates*, and reset the guarantee accordingly. This is the highest-risk, most separable pillar — see scope note below.

5. **Provenance requires write-path coordination with the agent runtime.** Capturing "what created it, from which interaction, and its scope history" means the memory write path must stamp agent identity + interaction ID at write time, which requires the agent runtime (OpenShell) to supply that context. MLMD's lineage model is a usable precedent for the store side. This is real cross-team coordination between the agent-memory team, the OpenShell team, and the platform identity layer — it isn't mentioned in the RFE and should be surfaced.

6. **The storage substrate is not yet a named platform service.** No dedicated agent-memory component exists in the 3.5-ea.2 inventory; the Dev Preview record-level isolation (RHAIRFE-2633/2635) is the first increment and is correctly declared out of scope here. Candidate substrates to evaluate in strategy: OGX/Llama Stack vector stores (Milvus/Qdrant), Feast, and PostgreSQL/MLMD for metadata and lineage. Selecting and standing up the substrate is strategy work, not an RFE gap.

7. **External-operator dependency policy applies (overlay 0008).** If the chosen memory/vector substrate depends on an external operator (e.g., a vector-DB operator), RHOAI will not auto-install, upgrade, or configure it — it must be documented as an admin-owned prerequisite and missing-dependency status surfaced on DSC/DSCI. This directly affects the "regulated pilot" success criterion, where a clean prerequisites/deployment story matters for the internal security review.

8. **Poisoning-defense expectation gap.** The healthcare accounts' stated fear is "one contaminated input can poison a shared store," but the RFE explicitly defers adversarial memory-injection defense to a GA RFE and only surfaces origin + conflicts. The de-scoping is sensible, but there is a tension between the affected-customer justification (poisoning) and what Tech Preview actually delivers (traceability, not contamination defense). Manage that expectation explicitly in the strategy and customer messaging.

9. **Promotion + audit is a control-plane workflow with a natural home.** "Sharing across a tier boundary is a deliberate, controlled, recorded action" is a promotion operation with an immutable audit record. OpenShell already emits OCSF v1.7 security events for enterprise SIEM consumption — a natural surface for the recorded-action and provenance-audit trail, and worth aligning to rather than building a parallel audit log.

#### Scope note

The RFE frames scope tiers, conflict handling, and provenance as "one trust problem," and as a *product* narrative that holds. As an *engineering* effort (size L), the three pillars are separable disciplines: identity-scoped access (RBAC/identity), semantic conflict detection (embeddings/LLM reasoning), and provenance/lineage (metadata). Conflict detection — with its absolute "zero unflagged contradictions" bar and its distinct skill set — is the clearest candidate to split into its own feature if the effort proves large during refinement. The RFE is coherent enough to enter strategy as-is, but flag conflict detection as a split risk up front.

## Revision History

none (first pass)
