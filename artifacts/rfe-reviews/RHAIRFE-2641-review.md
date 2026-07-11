---
rfe_id: RHAIRFE-2641
score: 10
pass: true
recommendation: submit
feasibility: feasible
needs_attention: true
needs_attention_reason: Feasibility analysis recommends splitting the RFE along the
  TP/GA line despite right_sized scoring 2/2, and it references an unnamed 'Gen AI
  Studio' component; the TP-vs-GA capability boundary, sibling-API sequencing, and
  the scope-policy/RBAC-vs-OPA model need human/strategy resolution before commitment.
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

TITLE: Agent memory governance console in AI Hub

| Criterion | Score | Notes |
|-----------|-------|-------|
| WHAT      | 2/2   | Crisp, specific need: a single AI Hub admin surface making the memory estate visible and operable — inventory of memory services/stores, agent-to-memory bindings, quarantined-write review/disposition, write-log review/export, and scope-policy administration. The problem statement grounds it (API-only governance fails security reviews; unreviewed quarantines become silent data loss). Clear and specific. |
| WHY       | 2/2   | Named customer accounts with concrete consequences: SAS (compliance staff need an operable audit-trace surface), OCBC Bank (must demonstrate team isolation to internal security via a bindings/scopes view), BNP Paribas and ITZBund (audit review/export inside disconnected deployments). Also a strategic causal chain — the console is the "last mile" that converts already-committed governance investment into won deals. Strongest evidence (named accounts) puts this at 2. |
| Open to HOW | 2/2 | Describes user-facing surfaces and observable outcomes: admin sees inventory/bindings, reviews and disposes of quarantined writes (release/delete/escalate), reviews and exports the log, administers scope policy. "AI Hub" is established platform admin-surface vocabulary; "in-cluster / disconnected-capable" is a customer requirement, not an architecture mandate. Cross-references to RHAIRFE-2633/2634/2635 are scope boundaries, not design prescription. No internal schemas, repos, or algorithms mandated. |
| Not a task | 2/2  | A clear business need, not a chore: makes governance operable for the admin/compliance personas, lets regulated pilots pass security review against the console rather than raw APIs, and prevents quarantined writes from accumulating unseen (safety/data-loss risk). Not tech debt or housekeeping. |
| Right-sized | 2/2 | Deliverables identified: (1) service/store inventory, (2) bindings view, (3) quarantine review/disposition, (4) write-log review/export, (5) scope-policy admin. These are the coupled views of one console — the RFE is explicitly "one AI Hub surface / one control plane," and the deal-winning value (a passing security review showing isolation, quarantine, and audit together) requires the views to exist as a whole, not piecemeal. All operate over the same memory estate within the same admin surface, mapping to one strategy feature (parent RHAISTRAT-1345). The audit-log/export view is the only facet with a plausible standalone-compliance read, but the "one surface" framing and shared security-review narrative keep this a focused single feature. Enforcement mechanisms and engineer-facing views are correctly scoped out to separate RFEs. |
| **Total** | **10/10** | **PASS** |

### Verdict
A model RFE: a clearly scoped, persona-driven admin console with named regulated accounts driving it, a strategic last-mile justification, and clean separation of enforcement (out of scope) from the operable surface (in scope).

### Feedback
Strengths: named accounts tied to specific review/audit/isolation consequences; explicit persona split (admins govern in AI Hub, engineers consume in Gen AI Studio); disciplined scoping that pushes enforcement mechanisms and engineer views to their own RFEs; observable acceptance criteria with no architecture leakage. Minor improvements: the open question about which capabilities land at Tech Preview vs GA (given the audit trail completes at GA) is worth resolving before commitment so the TP success criterion — a pilot's security review passing against the console — is provably achievable within the 3.7 slice. If the audit-log review/export view ever grows its own compliance-specific requirements, watch that it doesn't drift into a separately shippable feature.

## Technical Feasibility

**Feasibility**: feasible
**Blockers**: none
**Scope assessment**: needs splitting

Overlays applied:
- 0008: RHOAI does not auto-install external operator dependencies (affects: platform, release: all)
- 0015: OpenShell is the agent security platform for RHOAI, replacing Kagenti (affects: platform; release 3.5/3.6/next — applied as the go-forward agent architecture for a 3.7 target, with the release-match caveat noted)

Architecture context: `rhoai-3.5-ea.2` (latest available; the RFE targets RHOAI 3.7 Tech Preview, so the context is read forward). No `RFE-014-comments.md` and no prior `rfe-review-report.md` were present.

**Feasible.** This is a new admin surface in AI Hub (odh-dashboard) layered over backend APIs that sibling RFEs deliver. That is exactly the pattern the platform already runs at scale, and nothing in the architecture conflicts with the need.

Grounding in the platform:

- **odh-dashboard is the platform's admin console and has the most outgoing integrations (22)** — it already fronts governed assets from Model Registry, MLflow, Data Science Pipelines, TrustyAI, MaaS, and the RHOAI MCP Server. RHOAI 3.5 added a "dashboard module controller" and an "agent-ops BFF," confirming that new admin surfaces ship as dashboard modules with backend-for-frontend sidecars. A memory-governance module fits this established mechanism; the "one control plane" framing in the RFE is consistent with how the dashboard is built.
- **Disconnected / air-gapped operation is first-class**, not aspirational: all 129 images are RELATED_IMAGE / digest-pinned, mirrored via oc-mirror, and the dashboard runs in-cluster in `redhat-ods-applications`. The AC "fully functional in disconnected and air-gapped deployments" is directly supported and aligns with — rather than fights — platform strategy.
- **Auth/RBAC for a dashboard surface is a solved pattern** — kube-rbac-proxy with TokenReview + SubjectAccessReview is the standard enforcement point for dashboard-fronted services.

Per the feasibility rubric, the fact that the memory service and its governance APIs do not yet exist in the component inventory is **not** a blocker — that is what the sibling RFEs are for, and the RFE correctly scopes the enforcement mechanisms out. The "memory service" and "memory stores" are the author's proposed backend, not a platform prerequisite that must pre-exist. Assessed on the underlying need — an operable governance surface for a memory estate — this is buildable.

**Scope assessment: needs splitting.** Size L is optimistic for what is bundled here. The RFE packs five distinct governance surfaces — (a) memory service/store inventory, (b) agent-to-memory bindings view, (c) quarantine review + disposition workflow, (d) write-log review + audit export, (e) scope-policy administration — plus full disconnected/air-gapped support, each riding on a different backing RFE with its own maturity timeline. The read-only surfaces (inventory, bindings) are relatively light; the quarantine disposition workflow and the audit-grade write-log export are each substantial features in their own right, and the latter is explicitly gated on a GA-timeframe audit backend. The RFE's own Open Question ("which console capabilities land at Tech Preview versus GA") is effectively a request to split. A natural decomposition is along the TP/GA line at minimum — read/observe surfaces and quarantine disposition for TP, audit write-log review/export aligned to the GA audit trail — and possibly per capability where the backing RFEs mature independently. Recommend splitting during strategy refinement rather than carrying this as one L feature.

Note: the assessor scored `right_sized` 2/2 on the "one control plane / one surface" framing, while the feasibility analysis reads the same bundle as needing a split along the TP/GA line during strategy refinement. This tension is left for human/strategy judgment (see needs_attention).

## Strategy Considerations

These carry forward into `/strat.refine`; none blocks submission.

1. **Hard dependency on sibling RFEs' API surface, with sequencing risk.** The console is a consumer of APIs delivered by RHAIRFE-2633 (isolation), -2634 (screening/quarantine), -2635 (write logging), and the shared-memory (tiers/provenance) RFE. The console can only be as good as those APIs allow. If any of them is designed API-first without a console consumer in mind (e.g., no "list quarantined writes," "dispose with reason," "query write-log by scope+date," or "administer scope policy" operations), the console's scope balloons to fill the gap. Strategy must confirm each backing API exposes the operations the six ACs require, and sequence the console behind them.

2. **Audit trail "completes at GA" while the console targets Tech Preview.** The RFE's own Success Criteria and Open Question state the audit trail itself is not complete until GA, yet the write-log review/export console feature is in the TP-timeframe scope. Building an audit-review UI over an audit backend that is still maturing is a real sequencing/coverage risk. Resolving the "which capabilities land at TP vs GA" open question is a prerequisite to sizing this.

3. **Overlap and boundary with OpenShell's OCSF event stream (overlay 0015).** OpenShell (the agent security platform) already generates OCSF v1.7 security events for network/HTTP/process/filesystem activity intended for enterprise SIEMs. The RFE's "memory write log review and export" is conceptually adjacent. Strategy must define the boundary: is the memory write-log a distinct store owned by the memory service, or a projection/filter over OpenShell's OCSF events? Two parallel audit paths (in-console export vs SIEM ingestion) risk divergence unless reconciled.

4. **Where do "agent-to-memory bindings" live, and how are they discovered?** The console must render which agents are bound to which stores at which scopes. That binding model spans the agent runtime (OpenShell), the memory service, and possibly the DSC. The source of truth for bindings is unspecified — this is cross-component coordination (agent-platform team + memory-service team + dashboard team) that the RFE does not name.

5. **Scope-policy administration vs. platform RBAC / OPA.** AC "administers scope policy: who can read/write which tiers" implies a policy authoring surface. It is unspecified whether tier scope maps onto Kubernetes RBAC (the dashboard's native authz model) or onto a separate policy engine (OpenShell enforces OPA/Rego policies per sandbox). A console that writes into one model while enforcement reads from another would be broken by construction. Strategy must pin the policy model the console administers and confirm it is the same one the enforcement RFEs read.

6. **Quarantine disposition is a stateful, auditable workflow, not a read-only view.** "Release / delete / escalate" with a bounded, visible dwell-time SLA (Success Criteria) implies mutation APIs, a durable disposition record, reviewer identity/authorization, and an escalation target/route. This is materially heavier than the inventory/bindings read views and is easy to under-size.

7. **External-operator dependency policy (overlay 0008).** If the memory service or its audit/export path depends on optional OpenShift operators (e.g., an observability/log stack for write-log retention or SIEM export), RHOAI will not auto-install them. Those must be documented as admin-provisioned prerequisites and surfaced as status conditions — especially material given the disconnected/air-gapped ACs where such operators are often absent.

8. **"Gen AI Studio" persona-split reference is not a named platform component.** The RFE anchors an out-of-scope boundary on an engineer-facing "Gen AI Studio" surface, which does not appear as a distinct component in the inventory (the platform console is odh-dashboard). This is a naming/product-framing note, not a feasibility issue, but the persona-split boundary should be tied to concrete dashboard areas during refinement.

## Revision History

none (first pass)
