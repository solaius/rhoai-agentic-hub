---
rfe_id: RHAIRFE-2633
score: 10
pass: true
recommendation: submit
feasibility: feasible
needs_attention: true
needs_attention_reason: 'Feasibility is feasible with no blockers, but the effort
  estimate (M) is likely optimistic and the rubric cannot see it: isolation must be
  built into a net-new memory service from day one, and principal->agent->memory identity
  propagation is a non-trivial cross-component (OpenShell + memory service) design
  with unstated cross-team coordination.'
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

TITLE: Record-level scope isolation for agent memory

| Criterion | Score | Notes |
|-----------|-------|-------|
| WHAT      | 2/2   | Clear, specific need: multi-tenant/regulated customers cannot share a memory store until every record is isolated to its intended scope and reads return only what the caller is permitted to see. The requirement is concrete — record-level scoping, read/query-path enforcement, and project isolation on a shared cluster — and the problem statement frames it precisely from both the admin and agent perspectives. |
| WHY       | 2/2   | Named customer accounts with deal-level consequence: OCBC Bank (multi-tenant requirement that teams' agents must not see each other's data) and NTT Data (Zero Trust requirement that agent reads follow the principal's data-access policy). Business justification states these accounts "impose the requirement contractually today" and calls them "blocked-deal governance gaps, not future risks." Also supported by a competitive-differentiation argument (governance depth vs. hyperscaler/startup memory offerings), but the named blocked-deal accounts alone reach Y=2. |
| Open to HOW | 2/2 | Describes needs as outcomes: records carry a scope, reads return only permitted records, isolation is demonstrable to a security reviewer. The "enforce on the read/query path, not only at the storage boundary" criterion is a security-correctness guarantee (defense against storage-only filtering being bypassed), not a mandated internal architecture — the mechanism is left open. OpenShift namespace and RBAC appear only in Open Questions as things to resolve (platform vocabulary), not as prescribed solutions. Engineering retains full freedom over the design. |
| Not a task | 2/2  | A genuine business need — unblocking multi-tenant and regulated customers from adopting agent memory at all. Framed by customer outcomes and security guarantees, not by an engineering chore, refactor, or tech-debt cleanup. |
| Right-sized | 2/2 | Deliverables are record-level scope, read/query-path enforcement, and project isolation. Independence test: scope metadata with no read enforcement provides no value; read enforcement is meaningless without per-record scope; project isolation is an application of the same scope/enforcement mechanism. They cannot function without one another — a single coherent capability. Sibling concerns (write-path sensitive-data screening, write auditability, and the full multi-tier scope hierarchy) are explicitly carved out as out of scope, keeping this focused on one strategy feature (maps cleanly to RHAISTRAT-1345, Agent Memory). |
| **Total** | **10/10** | **PASS** |

### Verdict
An exemplary RFE: a clearly scoped multi-tenancy/isolation need, justified by named blocked-deal accounts, described as security outcomes without prescribing architecture, and disciplined about splitting sibling capabilities out.

### Feedback
Strengths: named accounts tied to contractual/blocked-deal impact, outcome-oriented acceptance and success criteria (zero cross-scope reads; a customer security review passing), and deliberate scoping that pushes write-path screening, write auditability, and the richer tier model into sibling RFEs. Minor polish only: the "read/query path, not only at the storage boundary" line reads slightly implementation-flavored — if you want to keep it purely need-shaped, phrase it as the guarantee ("an unpermitted read must be rejected even if the record is retrievable from storage") and let engineering decide where that check lives. The two Open Questions are appropriately framed as design questions for engineering rather than mandates.

## Technical Feasibility

**Feasibility**: feasible

**Blockers**: none. Nothing in the platform architecture conflicts with this need — the opposite is true. RHOAI is built around multi-tenant namespace isolation (per-project namespaces for tenant workloads), RBAC (684 role entries), NetworkPolicies, the kube-rbac-proxy SubjectAccessReview pattern, and SPIFFE/SPIRE workload identity via OpenShell. Record-level scoping (a scope attribute per record plus read-path filtering) is a standard service/data pattern, and the agent-memory store and its scope model not existing yet is exactly what this RFE is for — not an infeasibility.

**Scope assessment**: appropriate. This is a deliberate, well-reasoned split from RFE-003 with clean In/Out of Scope and explicit deferrals (write-path screening → sibling, write auditability → sibling, full user/project/role/org tier model → Tech Preview). Further splitting the Dev Preview isolation slice would not help. The one caveat is effort credibility: because the memory service is net-new, this cannot ship independently of the foundational memory data model + read API, and the principal→agent→memory identity-propagation design is non-trivial, so the `M` estimate looks optimistic.

_Overlays applied:_
- _0015: OpenShell is the agent security platform for RHOAI, replacing Kagenti (SPIFFE identity + token exchange, integrated OPA policy, sandbox isolation) — agent-memory scope/identity work must target OpenShell, not Kagenti_
- _0008: RHOAI does not auto-install external operator dependencies — any memory-store backend operator is a documented prerequisite, not platform-managed_

_Architecture context: rhoai-3.5-ea.2 (PLATFORM.md). OGX naming (overlay 0003) noted as supplementary context for the likely memory host; not a formally matched overlay since the RFE names no component. No prior review report present; this is a first-pass review._

## Strategy Considerations

Route the following to /strat.refine:

- **Coupled to a net-new memory service.** There is no "agent memory" component in the RHOAI 3.5-ea.2 architecture inventory (65 components) — this RFE ships isolation "alongside the first memory Dev Preview," so it is not "add scoping to an existing store" but "stand up the store with scoping built in." The scope attribute and the read/query-path filter must be designed into the memory service's foundational data model and query API from day one, not bolted on. This tightly couples the RFE to the foundational memory-service work and is the main reason the `M` size estimate may be optimistic.
- **Owning component is undefined.** The enforcement point depends on where memory lives — a net-new memory service, an OGX (formerly Llama Stack, per overlay 0003) memory provider, or an OpenShell-integrated store. The RFE is deliberately implementation-agnostic (good), but /strat.refine must name the owning component because that choice decides whether isolation is enforced in-application, via namespace/RBAC, or both.
- **Identity propagation is the hard part (and the RFE's own open question).** Deriving the caller's scope from human principal → agent → memory read requires a delegated / on-behalf-of identity chain. NTT Data's Zero Trust requirement means the scope must reflect the *principal's* entitlements, not merely the agent's own service identity. The platform primitives exist — OpenShell (overlay 0015) provides SPIFFE-based workload identity and SVID token exchange, and the former Kagenti AuthBridge pattern performed JWT validation + token exchange + OPA — but wiring principal-delegated identity through an autonomous agent into a memory read is a cross-component identity design (OpenShell + memory service + possibly OGX). This is the primary complexity to resolve in strategy refinement.
- **"Project" = namespace composition (RFE open question).** Mapping project isolation to the OpenShift namespace boundary is idiomatic and would let the design reuse RBAC / SubjectAccessReview / NetworkPolicy. But if one shared memory-service instance serves multiple namespaces, namespace RBAC alone does not isolate records — enforcement falls to the in-application scope filter, and how record-level scope *composes* with namespace + RBAC must be designed explicitly. A per-namespace memory instance (cf. Model Registry's per-instance PostgreSQL model) would yield hard namespace isolation but changes the deployment shape. This is an architecture decision for strategy, not a blocker.
- **Shared-store blast radius.** If the Dev Preview memory service is a single shared instance/DB, a defect in query-path scope filtering is a cross-tenant data leak — precisely the disqualifying scenario the named banks describe. The "zero cross-scope reads" success criterion is high-stakes; the RFE's insistence on read/query-path enforcement (not only the storage boundary) is the right defense-in-depth call, and isolation testing needs to be treated as a gate, not a nice-to-have.
- **Cross-team coordination is unstated.** The work plausibly spans the memory-service team, the OpenShell / identity team, and possibly OGX. None of this coordination is called out in the RFE; flag it for planning.
- **External backend prerequisite (overlay 0008).** If the memory store depends on an external operator (e.g., a vector DB or database operator), standing platform policy is that RHOAI does not auto-install external operators — it must be documented as a prerequisite and any missing dependency surfaced on DSC/DSCI. Applies only if such a dependency is chosen.
- **"Demonstrable to a security reviewer" (AC #2) may leak into sibling scope.** Proving read isolation to a customer reviewer may imply read-path evidence/observability of enforcement. Write auditability and the exportable write-event log are explicitly a sibling RFE, so ensure the read-isolation demonstrability here does not quietly pull in logging scope that belongs to the sibling.

## Revision History

none (first pass)
