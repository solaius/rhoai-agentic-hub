### RFE-007: Agent-memory write auditability

**Feasibility**: feasible
**Strategy considerations**: see list below (7 items for /strat.refine)
**Blockers**: none
**Scope assessment**: appropriate (with a sequencing/effort risk tied to the memory store's write path)

---

## Feasibility

**Feasible.** This is an extension of the platform, not a rearchitecting of it. Nothing in RHOAI 3.5-ea.2's architecture fundamentally conflicts with a reviewable, exportable write-event log for agent memory. The core requirement — emit a structured record (who / what / when / which scope) on every memory write and let authorized users export it, including to a customer-managed sink in disconnected environments — maps cleanly onto patterns the platform already uses:

- **Structured, exportable, SIEM-bound audit events already exist for agent activity.** Per overlay 0015, OpenShell (the agent security runtime that replaces Kagenti) generates OCSF v1.7 security events across four categories (network, HTTP, process, filesystem activity) explicitly designed for enterprise SIEM consumption (Splunk, QRadar, Sentinel). This establishes that emitting structured agent-audit events and exporting them to a customer-controlled system is an established platform direction, not a novel capability. Note the boundary: OCSF events cover *infrastructure-level* activity, not *application-semantic* memory writes (who wrote what content into which memory scope). So the write log itself is a distinct, application-level artifact the memory store must emit — but the export/SIEM plumbing has a proven precedent to align with.
- **On-behalf-of principal attribution has existing primitives.** The agentic layer already carries identity: OpenShell provides SPIFFE-based workload identity with token exchange, and the former Kagenti/agents-operator model wires SPIFFE/SPIRE (X.509/JWT SVIDs) plus Keycloak OAuth2 token exchange to move a caller's identity into the agent runtime. The human principal's identity is therefore obtainable at the agent runtime; the open question is propagating it the last mile to the memory write point — an integration concern, not a missing capability.
- **A customer-managed / disconnected export target is the platform-consistent design.** The platform has comprehensive air-gapped support (RELATED_IMAGE, digest-pinned images), and overlay 0008 codifies that RHOAI does not manage external systems on the customer's behalf. The RFE's own constraint — the export contract must not assume a hosted sink — aligns with platform policy rather than fighting it. A customer-owned export sink is the correct architecture, not a workaround.

**On the missing component:** "Agent memory" is not in the architecture inventory — there is no memory-store component doc in `rhoai-3.5-ea.2`. This is expected: the RFE states it delivers auditability *alongside the first memory Dev Preview*, so the memory store is itself a net-new, in-flight capability. A capability that does not exist yet is not infeasible — that is precisely what an RFE is for. The absence of the memory store is recorded below as a strategy consideration (a hard dependency/sequencing item), not a blocker.

## Overlays applied

```
Overlays applied:
- 0015: OpenShell is the agent security platform for RHOAI (OCSF v1.7 audit events for SIEM; SPIFFE identity + token exchange). Target agentic strategies at OpenShell, not Kagenti/AgentRuntime.
- 0008: RHOAI does not auto-install/manage external operators or systems — reinforces that the audit-log export sink is customer-managed and must not assume a hosted target.
```

(Other platform-scoped 3.5 overlays — 0009, 0012, 0013, 0017 — matched the mechanical filter but have no substantive bearing on memory-write auditability and were not applied.)

## Strategy Considerations

These are for engineering to resolve during /strat.refine. None blocks submission.

1. **Hard dependency on the not-yet-defined memory-store write path.** The log's entire design is downstream of the memory store's architecture — where writes land, what a backing store is (vector DB, PostgreSQL, OGX vector stores?), and what a "scope" is. The auditability design cannot be finalized until the memory store's write path and scope model are defined. This RFE and its declared siblings (record-level scope isolation, write-path sensitive-data screening) all instrument the *same* write path; a shared, enforced memory-write interception point is implied but never stated. Surface the cross-RFE coordination and sequencing explicitly.

2. **On-behalf-of attribution is the genuinely hard part and is under-specified.** The RFE itself flags this as an open question. The platform has the primitives (Keycloak token exchange, SPIFFE JWT-SVID, OpenShell token exchange), but there is no single existing pathway that carries a *human* principal's identity into an arbitrary memory-write call. The chain crosses the agent framework, the identity layer (OpenShell/Keycloak), and the memory store. It also needs a defined semantics for multi-hop agent scenarios (agent invoked by agent invoked by human): what "the principal on whose behalf" means when there is a chain of principals is a real modeling decision, not a plumbing detail.

3. **"100% of memory writes appear in the write log" implies non-bypassable, fail-closed logging.** A compliance-grade guarantee means an agent must not be able to write memory without generating a log entry. The interception point therefore has to be architecturally mandatory — at the memory service API boundary, not in client SDK code an agent could skip. This is a design constraint with teeth that shapes where the memory store enforces writes.

4. **Dev-Preview log vs. compliance-grade audit trail — manage the expectation gap.** The RFE correctly scopes OUT the full append-only, tamper-evident audit trail with erasure primitives (GA-gating, separate RFE). Good scoping — but the success criterion ("a regulated pilot customer's internal security review passes with the write log enabled") sets a high bar for a deliberately weaker Dev Preview artifact. Strategy should make explicit that a *reviewable* log is not an append-only/tamper-evident trail, and confirm the pilot's security review will accept that distinction; regulated accounts (SAS, BNP Paribas, ITZBund) may conflate the two.

5. **Export contract is undefined and has schema-alignment consequences.** Whether export is an event schema, a file, or an API is an open question. OCSF v1.7 is already emitted by OpenShell for agent activity and would give SIEM compatibility for free — but the RFE does not commit. If the memory write-log invents its own schema while OpenShell emits OCSF, customers get two incompatible audit feeds for the same agents. Aligning the log schema with OpenShell's OCSF output is a cross-team decision worth deciding early.

6. **"Which scope" presupposes a scope model owned by a different RFE.** The log must record "which scope," but the scope model is being designed in the sibling record-level-scope-isolation RFE (explicitly out of scope here). Logging a scope identifier the isolation RFE has not finalized is a data-model coupling — if the scope model changes, the log schema changes.

7. **The log is itself sensitive data — export authorization and content handling need a model.** Recording "what an agent memorized about this customer" means the log contains (or references) the same regulated data as the memory store. Two consequences: (a) "authorized users" export needs a multi-tenant RBAC model so a compliance officer in tenant A cannot export tenant B's memory writes — the platform's kube-rbac-proxy / SubjectAccessReview pattern covers this, but the RFE does not mention export authorization scoping; and (b) for data sovereignty (ITZBund) and future erasure obligations, the log becomes another copy of sensitive data inside the governance perimeter, subject to the same retention/erasure rules — strategy must decide whether the log stores content, a hash, or a reference.

## Scope assessment

**Appropriate.** The In Scope is narrow (a basic write-event log plus export), and the split-out siblings are disciplined and correct: record-level scope isolation, write-path sensitive-data screening, and the full append-only audit trail with erasure primitives are all explicitly out of scope. A single strategy feature can plausibly deliver a basic, reviewable write log plus export. The one scope/effort risk is that the effort is contingent on the memory store exposing a single, enforced write path (consideration 1) and on the on-behalf-of identity chain (consideration 2); if those are not already being built as part of the memory Dev Preview, the real effort exceeds an M. Because the RFE is explicitly paired with the first memory Dev Preview, that write-path work is presumably shared — so M is defensible, but the sizing hinges on that assumption.
