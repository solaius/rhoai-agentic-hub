### RFE-014: Agent memory governance console in AI Hub
**Feasibility**: feasible
**Strategy considerations**: see list below
**Blockers**: none
**Scope assessment**: needs splitting

---

Overlays applied:
- 0008: RHOAI does not auto-install external operator dependencies (affects: platform, release: all)
- 0015: OpenShell is the agent security platform for RHOAI, replacing Kagenti (affects: platform; release 3.5/3.6/next — applied as the go-forward agent architecture for a 3.7 target, with the release-match caveat noted)

Architecture context: `rhoai-3.5-ea.2` (latest available; the RFE targets RHOAI 3.7 Tech Preview, so the context is read forward). No `RFE-014-comments.md` and no prior `rfe-review-report.md` were present.

## Feasibility

**Feasible.** This is a new admin surface in AI Hub (odh-dashboard) layered over backend APIs that sibling RFEs deliver. That is exactly the pattern the platform already runs at scale, and nothing in the architecture conflicts with the need.

Grounding in the platform:

- **odh-dashboard is the platform's admin console and has the most outgoing integrations (22)** — it already fronts governed assets from Model Registry, MLflow, Data Science Pipelines, TrustyAI, MaaS, and the RHOAI MCP Server. RHOAI 3.5 added a "dashboard module controller" and an "agent-ops BFF," confirming that new admin surfaces ship as dashboard modules with backend-for-frontend sidecars. A memory-governance module fits this established mechanism; the "one control plane" framing in the RFE is consistent with how the dashboard is built.
- **Disconnected / air-gapped operation is first-class**, not aspirational: all 129 images are RELATED_IMAGE / digest-pinned, mirrored via oc-mirror, and the dashboard runs in-cluster in `redhat-ods-applications`. The AC "fully functional in disconnected and air-gapped deployments" is directly supported and aligns with — rather than fights — platform strategy.
- **Auth/RBAC for a dashboard surface is a solved pattern** — kube-rbac-proxy with TokenReview + SubjectAccessReview is the standard enforcement point for dashboard-fronted services.

Per the feasibility rubric, the fact that the memory service and its governance APIs do not yet exist in the component inventory is **not** a blocker — that is what the sibling RFEs are for, and the RFE correctly scopes the enforcement mechanisms out. The "memory service" and "memory stores" are the author's proposed backend, not a platform prerequisite that must pre-exist. Assessed on the underlying need — an operable governance surface for a memory estate — this is buildable.

## Strategy considerations

These carry forward into `/strat.refine`; none blocks submission.

1. **Hard dependency on sibling RFEs' API surface, with sequencing risk.** The console is a consumer of APIs delivered by RHAIRFE-2633 (isolation), -2634 (screening/quarantine), -2635 (write logging), and the shared-memory (tiers/provenance) RFE. The console can only be as good as those APIs allow. If any of them is designed API-first without a console consumer in mind (e.g., no "list quarantined writes," "dispose with reason," "query write-log by scope+date," or "administer scope policy" operations), the console's scope balloons to fill the gap. Strategy must confirm each backing API exposes the operations the six ACs require, and sequence the console behind them.

2. **Audit trail "completes at GA" while the console targets Tech Preview.** The RFE's own Success Criteria and Open Question state the audit trail itself is not complete until GA, yet the write-log review/export console feature is in the TP-timeframe scope. Building an audit-review UI over an audit backend that is still maturing is a real sequencing/coverage risk. Resolving the "which capabilities land at TP vs GA" open question is a prerequisite to sizing this.

3. **Overlap and boundary with OpenShell's OCSF event stream (overlay 0015).** OpenShell (the agent security platform) already generates OCSF v1.7 security events for network/HTTP/process/filesystem activity intended for enterprise SIEMs. The RFE's "memory write log review and export" is conceptually adjacent. Strategy must define the boundary: is the memory write-log a distinct store owned by the memory service, or a projection/filter over OpenShell's OCSF events? Two parallel audit paths (in-console export vs SIEM ingestion) risk divergence unless reconciled.

4. **Where do "agent-to-memory bindings" live, and how are they discovered?** The console must render which agents are bound to which stores at which scopes. That binding model spans the agent runtime (OpenShell), the memory service, and possibly the DSC. The source of truth for bindings is unspecified — this is cross-component coordination (agent-platform team + memory-service team + dashboard team) that the RFE does not name.

5. **Scope-policy administration vs. platform RBAC / OPA.** AC "administers scope policy: who can read/write which tiers" implies a policy authoring surface. It is unspecified whether tier scope maps onto Kubernetes RBAC (the dashboard's native authz model) or onto a separate policy engine (OpenShell enforces OPA/Rego policies per sandbox). A console that writes into one model while enforcement reads from another would be broken by construction. Strategy must pin the policy model the console administers and confirm it is the same one the enforcement RFEs read.

6. **Quarantine disposition is a stateful, auditable workflow, not a read-only view.** "Release / delete / escalate" with a bounded, visible dwell-time SLA (Success Criteria) implies mutation APIs, a durable disposition record, reviewer identity/authorization, and an escalation target/route. This is materially heavier than the inventory/bindings read views and is easy to under-size.

7. **External-operator dependency policy (overlay 0008).** If the memory service or its audit/export path depends on optional OpenShift operators (e.g., an observability/log stack for write-log retention or SIEM export), RHOAI will not auto-install them. Those must be documented as admin-provisioned prerequisites and surfaced as status conditions — especially material given the disconnected/air-gapped ACs where such operators are often absent.

8. **"Gen AI Studio" persona-split reference is not a named platform component.** The RFE anchors an out-of-scope boundary on an engineer-facing "Gen AI Studio" surface, which does not appear as a distinct component in the inventory (the platform console is odh-dashboard). This is a naming/product-framing note, not a feasibility issue, but the persona-split boundary should be tied to concrete dashboard areas during refinement.

## Scope assessment: needs splitting

Size L is optimistic for what is bundled here. The RFE packs five distinct governance surfaces — (a) memory service/store inventory, (b) agent-to-memory bindings view, (c) quarantine review + disposition workflow, (d) write-log review + audit export, (e) scope-policy administration — plus full disconnected/air-gapped support, each riding on a different backing RFE with its own maturity timeline. The read-only surfaces (inventory, bindings) are relatively light; the quarantine disposition workflow and the audit-grade write-log export are each substantial features in their own right, and the latter is explicitly gated on a GA-timeframe audit backend.

The RFE's own Open Question ("which console capabilities land at Tech Preview versus GA") is effectively a request to split. A natural decomposition is along the TP/GA line at minimum — read/observe surfaces and quarantine disposition for TP, audit write-log review/export aligned to the GA audit trail — and possibly per capability where the backing RFEs mature independently. Recommend splitting during strategy refinement rather than carrying this as one L feature.
