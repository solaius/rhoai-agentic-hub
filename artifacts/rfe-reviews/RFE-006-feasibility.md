### RFE-006: Sensitive-data screening on the agent-memory write path

**Feasibility**: feasible
**Strategy considerations**: see list below (7 items for /strat.refine)
**Blockers**: none
**Scope assessment**: appropriate

---

Overlays applied:
- 0008: Platform policy — RHOAI does not auto-install external operator dependencies (affects: platform)
- 0015: OpenShell is the agent security platform for RHOAI, replacing Kagenti (affects: platform)
- 0017: AIPCC base images (affects: platform)

Architecture context: `rhoai-3.5-ea.2` (PLATFORM.md + guardrails stack + agents-operator). Assessment grounded in the actual platform.

---

## Feasibility rationale

The underlying need — intercept content on a write path, screen it against PII / secret / sensitive-data patterns, apply a policy-driven outcome (block / quarantine / log), and give administrators a way to review and remove flagged records — is technically feasible and well-aligned with how the platform is built. Two facts make this clear:

1. **The platform already ships a mature sensitive-data detection stack that does exactly this class of pattern matching.** This RFE's detection capability is not net-new to the platform:
   - `guardrails-regex-detector` (Rust) has built-in `email`, `ssn`, and `credit-card` detectors plus arbitrary request-time custom regex, and returns matches with character offsets and scores. It uses a finite-automaton regex engine (linear-time, ReDoS-safe), is self-contained with no external service or DB dependencies, and is a single UBI9 binary.
   - `guardrails-detectors` (Python) provides a built-in regex PII detector, file-type validation, and custom Python detectors, plus a HuggingFace detector that supports token-classification (NER) models — including Granite Guardian — for ML-based sensitive-data detection with per-label thresholds.
   - `fms-guardrails-orchestrator` (Rust) coordinates detectors and exposes content-detection endpoints (`/api/v2/text/detection/content`, streaming variants). It is deployed and managed by the TrustyAI Service Operator (GORCH), a first-party platform component.

   These are proven, shipping building blocks for the "screen for PII/secrets" requirement.

2. **The one platform capability the RFE presumes — the agent-memory store — does not exist yet, and that is not a blocker.** There is no agent-memory component in the 3.5-ea.2 inventory; agent memory is the parent Outcome (RHAISTRAT-1345), which the RFE itself frames as reaching its "first memory Dev Preview." Per the feasibility standard, a capability not existing yet is precisely what RFEs are for — it is not infeasible. Nothing in the platform's architecture fundamentally conflicts with adding write-time screening to a memory store; this is an extension, not a rearchitecture.

The RFE's own open questions about disconnected/air-gapped operation are already answered favorably by the platform: the built-in and regex detectors run with no ML model and no external dependency, the HuggingFace detector loads a locally-served model from in-cluster S3-compatible storage, and the whole platform ships via the RELATED_IMAGE pattern for air-gapped mirroring. A locally-served detector is available today — this is not a barrier.

## Strategy considerations (carry into /strat.refine — none of these block the RFE)

1. **Co-dependency on the not-yet-existing memory store — a sequencing/cross-team dependency.** The guardrail is defined entirely relative to a memory write path, a "flagged/quarantined" record state, and an admin review/removal surface that all live in the memory store being built under RFE-003 / RHAISTRAT-1345. This screening RFE cannot land independently of the store's own data model and write API. Strategy must sequence/co-deliver it with the sibling memory RFEs, not treat it as standalone.

2. **Synchronous write-path latency budget (the RFE flags this).** Screening is synchronous with the write. Regex detection is cheap and linear-time, but ML/NER (HuggingFace / Granite Guardian) or LLM-judge detection adds a network hop plus model inference on every memory write, which can dominate write latency. The detector-modality choice (regex vs ML vs LLM-judge) is a real latency/accuracy tradeoff to settle in strategy, and it interacts with the disconnected constraint (an ML detector needs a locally served model and GPU/CPU budget).

3. **Detection efficacy vs. the block/quarantine/log policy.** Regex reliably catches structured tokens (card numbers, SSNs) but misses free-text PHI (patient identifiers, clinical narrative) — exactly the healthcare case the RFE names as the disqualifying blocker. ML NER catches more but introduces false positives, and a hard "block" policy on a noisy detector can break legitimate agent workflows. "Default screening policies per vertical (block vs quarantine) and who ships them" (the RFE's open question) is a genuine product decision, not an engineering unknown — but the efficacy/false-positive coupling to the policy outcome should be designed deliberately.

4. **Admin review/removal surface is a cross-component addition.** "Administrators can review and remove flagged/quarantined memories" implies a management surface (likely odh-dashboard), an RBAC model defining who a memory administrator is, and a quarantine store — which itself holds sensitive data that must be access-controlled and eventually purged. This spans the memory store, the dashboard, and platform RBAC; scope it explicitly.

5. **Agent security platform is OpenShell, not Kagenti (overlay 0015).** The generated `agents-operator.md` describes Kagenti (AuthBridge sidecar, AgentRuntime CRD, bundle-service) — that stack is deprecated and consolidated into OpenShell for 3.5+. If strategy considers intercepting at the agent-runtime layer, target OpenShell. Note, though, that OpenShell's controls are network/HTTP/kernel-layer (OPA L4/L7, OCSF events, sandboxing); memory-write content screening is more naturally a property of the memory store's write API than of a sandbox network policy. Do not design against the deprecated Kagenti AuthBridge.

6. **No auto-install of external operator dependencies (overlay 0008).** The guardrails/TrustyAI detection stack is first-party (managed by the TrustyAI Service Operator), so reusing it stays in-platform. But if any screening design pulls in an external operator dependency (e.g., Kuadrant, an external detector operator), platform policy forbids RHOAI auto-installing it — it must be a documented prerequisite surfaced on DSC/DSCI status. Keep the design first-party or prerequisite-documented.

7. **Business/legal and build contingencies on one candidate implementation.** The RFE's open questions note (a) the "internal governance prototype under evaluation is contingent on a written IP/license transfer before any productization decision," and (b) reuse of `guardrails-detectors` would still require its migration to AIPCC base images (overlay 0017) for product-security compliance. Neither gates the *need* — the platform's own guardrails detectors are an unencumbered, shipping path — but strategy should avoid hard-binding to the prototype and should treat the AIPCC migration as a productization task.

## Scope assessment

Appropriate for a single strategy feature (size M). The RFE has already been split from RFE-003 and cleanly carves out record-level scope isolation / read enforcement, write auditability / exportable event log, adversarial memory-injection defense, and contradiction/provenance metadata into sibling or later RFEs. The remaining scope — write-path screening + configurable policy outcome + admin review/removal — is a coherent unit. One mild scope-risk note for strategy: the admin review/removal surface plus a policy-configurable quarantine store is a non-trivial second workstream layered on the detector integration; if the memory store's own admin surface is not landing in the same release window, this piece could grow. As currently bounded, though, it is correctly right-sized and does not need further splitting.
