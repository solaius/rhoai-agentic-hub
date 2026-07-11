---
rfe_id: RFE-003
score: 8
pass: false
recommendation: split
feasibility: feasible
needs_attention: true
needs_attention_reason: Governs an agent-memory substrate that does not yet exist
  in rhoai-3.5-ea.2, so it cannot land independently of the first memory Dev Preview;
  governance and substrate must be co-designed (scope field + write-attribution native
  to the memory data model). Split into three RFEs is recommended.
scores:
  what: 2
  why: 2
  open_to_how: 2
  not_a_task: 2
  right_sized: 0
auto_revised: false
error: null
before_score: 8
before_scores:
  what: 2
  why: 2
  open_to_how: 2
  not_a_task: 2
  right_sized: 0
---
## Assessor Feedback

TITLE: Governed memory writes - scope isolation, sensitive-data screening, and write auditability

| Criterion | Score | Notes |
|-----------|-------|-------|
| WHAT      | 2/2   | Clear, specific need: every memory record must be (a) isolated to its intended scope, (b) screened for sensitive data at write time, and (c) attributable to who/what/when/which-scope. Backed by three concrete personas (compliance officer, platform admin, AI engineer) and observable acceptance criteria (records carry scope, reads return only permitted scope, writes screened for PII/secrets, write-event log exportable). No ambiguity about what "governable memory" means here. |
| WHY       | 2/2   | Named customer accounts with stated blocking consequences: SAS (blocked from production without auditable trace), NTT Data (Zero Trust data-access), OCBC Bank (multi-tenant isolation), BNP Paribas (disconnected compliance audit), ITZBund (federal data sovereignty/auditability), plus field-raised healthcare PHI as a named blocker. Reinforced by regulatory driver (EU AI Act, Aug 2026) and a stated competitive-differentiation thesis. Strongest evidence = named accounts with deal/production-blocking consequences → Y=2. |
| Open to HOW | 2/2 | Describes needs and observable outcomes, not techniques: "screened for PII, secrets... policy determining whether a flagged write is blocked, quarantined, or logged" is a policy/outcome, not an algorithm; the write log describes an auditability capability (who/what/when/scope), not a schema. No mandated technology, no design doc offered as "the solution." The internal governance prototype in Open Questions is explicitly framed as under evaluation and contingent on IP transfer "before any productization decision" — context, not a mandate. Engineering retains architectural freedom. |
| Not a task | 2/2  | Clear business need, not an activity or tech-debt chore: unblock regulated-vertical adoption of agent memory, mitigate compliance/PII exposure risk, and establish governance as a market differentiator. Would not make sense filed as an engineering task. |
| Right-sized | 0/2 | Bundles three independent capabilities. Independent deliverables: (A) record-level scope isolation + read enforcement; (B) write-path sensitive-data screening + admin review/removal of flagged memories; (C) write-event log + export (auditability). Pairwise independence test: A functions without B or C (multi-tenancy alone has value to OCBC); B functions without A or C (PII guardrail alone has value to healthcare); C functions without A or B (audit record alone has value to SAS/BNP/ITZBund). Each ships alone, to a different persona, satisfying a different named customer — the RFE's own User Scenarios map one-to-one to the three personas, and different named accounts drive different pieces. Admin-review couples only to screening; export couples only to logging, leaving three independent groups. Three independent features → R=0. (Comparable to the "overhaul security: RBAC + audit logging + scanning" R=0 calibration example; the shared "governance" label does not unify independently shippable items.) |
| **Total** | **8/10** | **FAIL** |

### Verdict
Strong on need, justification, openness, and framing, but the RFE bundles three independently shippable governance capabilities (isolation, write-path screening, auditability), triggering an automatic fail on Right-sized despite an 8/10 total.

### Feedback
Zero-scored criterion first — Right-sized (0/2): This RFE packages what are effectively three separate strategy features, each mapping to a distinct persona and distinct named customers:
1. **Scope isolation** (record-level scoping + read enforcement + project isolation) — serves the platform admin / multi-tenancy need (OCBC Bank).
2. **Write-path sensitive-data screening** (PII/secret detection with block/quarantine/log policy + admin review/removal) — serves the AI engineer / data-leakage-prevention need (healthcare PHI).
3. **Write auditability** (exportable write-event log of who/what/when/scope) — serves the compliance officer / audit-record need (SAS, BNP Paribas, ITZBund).

The independence test confirms none requires the others to function: a customer could adopt isolation without screening, screening without an audit log, or the audit log without isolation — and the named accounts each need different subsets. Recommend splitting into three RFEs under the same Agent Memory outcome (RHAISTRAT-1345). If the intent is a single coordinated Dev Preview milestone, capture that sequencing at the outcome/epic level rather than collapsing three separable capabilities into one RFE. Each split RFE already has clean, self-contained acceptance criteria in the current text, so decomposition should be low-friction.

Note: the four passing criteria are genuinely strong — the WHY section (named accounts with blocking consequences) and the disciplined Out-of-Scope carve-outs are model examples. The scope problem is breadth, not depth; each of the three pieces would likely score a clean pass on its own.

## Technical Feasibility

**Feasibility**: feasible

1. **No agent-memory substrate exists in the platform inventory yet (primary sequencing/dependency risk).** rhoai-3.5-ea.2 has no agent-memory component. The nearest data stores are OGX (formerly Llama Stack) vector stores (Milvus/Qdrant, surfaced via ai4rag), Feast, and per-component PostgreSQL — none is a purpose-built agent-memory store. This RFE governs a substrate that is itself still being built (the "first memory Dev Preview" it rides alongside). Governance and substrate must be co-designed: if the memory data model does not carry a scope field and write-attribution natively, retrofitting them later is exactly the "compliance liability to retrofit" the RFE warns against. `/strat.refine` must first pin which component owns the memory store before the governance model can be finalized. This is the single biggest coupling risk and is why this RFE cannot land independently of the memory feature.

2. **"Project isolation" is cheap on platform primitives; "record-level scoping" is the hard, new half.** The platform's native isolation is Kubernetes namespace + RBAC (SubjectAccessReview via kube-rbac-proxy) + NetworkPolicies. If "project" maps to an OpenShift namespace, project-level isolation (AC: teams on a shared cluster cannot read each other's memories) is largely namespace-scoping the memory store + RBAC — well-supported, no architectural conflict. But "every memory record carries a scope, and reads return only records the caller's scope permits" is an application-layer enforcement the platform does NOT provide out of the box — it must be built into the memory service's query/read path. The RFE conflates these two under one AC; the effort gap between them is not surfaced and could hide significant work.

3. **Sensitive-data screening: detector coverage vs. the breadth of the promise.** The screening capability is feasible by reusing the existing TrustyAI/Guardrails stack (FMS Guardrails Orchestrator + guardrails-regex-detector, which already detects email/SSN/credit-card + custom regex; plus NeMo Guardrails and detector backends). Screening a memory write is a new integration point on the write path, not a new capability. However, the AC "PII, secrets, and other sensitive-data patterns" is broad: regex covers structured PII, but comprehensive PHI/HIPAA identifiers and credential/secret detection may need additional (possibly LLM-based) detectors with latency and false-positive tradeoffs on a synchronous write path. Two unstated concerns: (a) a write-path latency budget (screening is synchronous with the write), and (b) per-vertical policy packs (block vs quarantine — the RFE's own Open Question) are a real content/ownership workstream, not a config toggle.

4. **Write attribution ("on whose behalf") is an on-behalf-of delegation problem — easy to under-scope.** "Who wrote it" and User Scenario 1's "on whose behalf" require trustworthy end-to-end identity propagation from the human principal, through the agent, to the memory write point. OpenShell/SPIFFE provides workload identity, but attributing a write to a human principal requires token/identity propagation across the agent runtime, the memory service, and the identity layer — cross-component coordination that is not mentioned.

5. **Agent security controls must target OpenShell, not Kagenti; and OpenShell is CLI/SDK-only in 3.5.** Any isolation/policy/audit enforcement that leans on the agent security layer must use OpenShell's integrated OPA engine, OCSF security-event generation, and SPIFFE identity — there is no AgentRuntime CRD, AuthBridge sidecar, or bundle-service to reference (overlay 0015). For a 3.5 Dev Preview, OpenShell's interface is CLI/SDK; the declarative operator/CRDs do not arrive until 3.6 (Tech Preview). So governance controls in 3.5 are either imperative or built directly into the memory service, not declaratively managed via CRDs. Sequencing dependency on OpenShell maturity.

6. **Audit is feasible on an existing primitive, but the export contract needs definition and the sink is customer-owned.** OpenShell already emits OCSF v1.7 security events (network/HTTP/process/filesystem) designed for SIEM (Splunk/QRadar/Sentinel), and OpenTelemetry tracing is pervasive — a structured, exportable memory-write log is analogous and feasible. But "the write log can be exported by authorized users for compliance review": if export means pushing to an enterprise SIEM/observability stack (COO, OpenTelemetry, Loki, Tempo), those operators are customer-managed prerequisites, not installed or managed by RHOAI (overlay 0008). Strategy should define the export contract (OCSF? file? API?) and treat the sink as external.

7. **Admin review/removal of flagged memories implies an unscoped management surface.** "Administrators can review and remove flagged, quarantined, or otherwise sensitive memories" implies a quarantine store, a management API/UI (likely odh-dashboard integration), and RBAC defining who administers memory. This dashboard + backend workstream is not reflected in the In-Scope list and is a cross-component (dashboard) coordination item.

8. **Disconnected/air-gapped constraint on screening (BNP Paribas, ITZBund).** Named accounts require disconnected operation. Regex detectors are self-contained; any LLM-based PII/PHI detection needs a locally served model. This constrains detector choice and must be validated in air-gapped mode.

9. **Non-technical: the internal governance prototype's IP/license transfer contingency.** The RFE notes a prototype "contingent on a written IP/license transfer before any productization decision." This does not affect feasibility of the need (which is satisfiable on platform primitives regardless), but it is a supply-chain/legal risk that could dictate the implementation source and should be tracked as such — not a technical blocker.

**Blockers**: none. The core objection ("nothing prevents PII from entering shared memory / cross-team reads / no write record") is a capability that does not exist yet for the memory feature — that is what this RFE is for, not an architectural incompatibility. Each of the three pillars maps cleanly onto existing platform primitives (namespace/RBAC isolation, the Guardrails detector stack, OpenShell OCSF/OTel audit). Nothing requires rearchitecting the platform.

**Scope assessment**: appropriate (monitor for split during /strat.refine). The out-of-scope carve-outs (full append-only audit trail + erasure, contradiction detection/provenance, adversarial injection defense, full multi-tier scope hierarchy) are disciplined and sensible. The remaining three pillars are defensible as one strategy feature because they share the memory write path. However, once the missing memory substrate dependency (consideration 1), the record-level enforcement code (2), and the admin review/removal surface (7) are counted, this is at the upper edge of a size-L feature. Strategy refinement should scrutinize whether the admin review/removal UI and the per-vertical screening policy packs warrant splitting out.

Overlays applied:
- 0015: OpenShell is the agent security platform for RHOAI, replacing Kagenti (affects platform + openshell; release 3.5/3.6/next)
- 0008: RHOAI does not auto-install external operator dependencies (affects platform; release all)

Architecture context: rhoai-3.5-ea.2. Target release inferred as 3.5 (Dev Preview, parent RHAISTRAT-1345 Agent Memory). No `RFE-003-comments.md` and no prior `rfe-review-report.md` were present, so this is a first-pass assessment.

## Strategy Considerations

The following items are flagged for `/strat.refine`:

- **Pin the memory-store owner before finalizing governance (consideration 1).** No agent-memory substrate exists in rhoai-3.5-ea.2. Governance and substrate must be co-designed so the memory data model carries a scope field and write-attribution natively; `/strat.refine` must first decide which component owns the memory store. This RFE cannot land independently of the first memory Dev Preview.
- **Surface the effort gap between "project isolation" and "record-level scoping" (consideration 2).** Namespace/RBAC covers project-level isolation cheaply, but record-level scope enforcement is new application-layer work in the memory service's read/query path. The single AC hides this gap.
- **Scope the sensitive-data screening promise (consideration 3).** Regex detectors cover structured PII; comprehensive PHI/secret detection may need LLM-based detectors. Define a write-path latency budget and treat per-vertical policy packs (block/quarantine/log) as a content/ownership workstream, not a config toggle.
- **Scope on-behalf-of write attribution (consideration 4).** End-to-end human-principal identity propagation across agent runtime → memory service → identity layer is cross-component work not currently mentioned.
- **Target OpenShell (not Kagenti); account for 3.5 CLI/SDK-only maturity (consideration 5).** In 3.5, governance controls are imperative or built into the memory service; declarative operator/CRDs arrive in 3.6.
- **Define the audit export contract; treat the sink as external (consideration 6).** Specify OCSF/file/API export; enterprise SIEM/observability sinks are customer-managed (overlay 0008).
- **Account for the admin review/removal management surface (consideration 7).** Quarantine store + management API/UI (likely odh-dashboard) + admin RBAC — a cross-component workstream absent from In-Scope.
- **Validate screening in air-gapped mode (consideration 8).** BNP Paribas / ITZBund require disconnected operation; LLM-based detectors need a locally served model.
- **Track the internal-prototype IP/license-transfer contingency (consideration 9).** Non-technical supply-chain/legal risk that could dictate the implementation source.
- **Split recommendation (rubric):** Right-sized scored 0/2. Split into three RFEs under the Agent Memory outcome (RHAISTRAT-1345): (A) scope isolation, (B) write-path sensitive-data screening + admin review, (C) write auditability + export. During `/strat.refine`, also scrutinize whether the admin review/removal UI and per-vertical screening policy packs warrant their own split.

## Revision History

none (first pass)
