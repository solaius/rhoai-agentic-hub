---
title: "Agent Registry research — jira-gap"
description: Registry-scoped cross-reference of the 2026-07-16 research refresh (07–10) against active RHAISTRAT work — a previously unmapped backend feature found, the card-verification vehicle closed days ago with no successor, and a Direction-B early-warning table for the capabilities nobody is tracking.
timestamp: 2026-07-16
lens: jira-gap
review_after: 2026-10-16
---

# Agent Registry research — jira-gap

Cross-reference run 2026-07-16, registry capabilities only. The sibling
[agent-interop jira-gap](/features/agent-interop/research/06-jira-gap.md)
(2026-07-11) covers the broad agent domain (FIPS, SCC, multi-tenancy,
identity); nothing there is re-litigated here. Landscape input: the
refreshed registry series
([07-upstream](/features/agent-registry/research/07-upstream.md),
[08-landscape](/features/agent-registry/research/08-landscape.md),
[09-architecture](/features/agent-registry/research/09-architecture.md),
[10-requirements](/features/agent-registry/research/10-requirements.md),
all 2026-07-16) plus the knowledge-base open questions.

**Public-repo note:** Jira serves nothing anonymously, so no issue
summary is quoted verbatim. All issue descriptions below are
paraphrased from the tracker (marked "paraphrased" on first use per
issue); cite keys to verify.

## Baseline

- **Primary baseline**: active RHAISTRAT Features/Outcomes (status In
  Progress / New / To Do). The unfiltered query hit the tool's
  500-issue cap, so the working set was narrowed to issues whose
  summaries mention agents/agentic/registry: **110 active
  Features/Outcomes** (2026-07-16). Registry-relevant issues whose
  titles use other vocabulary could be missed; the known-cluster keys
  were checked individually to compensate.
- **Auxiliary baselines** (committed snapshots, summaries withheld for
  disclosure reasons):
  [agent-interop/work/jira-snapshot.yaml](/features/agent-interop/work/jira-snapshot.yaml)
  (209 issues, swept 2026-07-11) and
  [agent-catalog/work/jira-snapshot.yaml](/features/agent-catalog/work/jira-snapshot.yaml)
  (37 issues, swept 2026-07-16). The interop snapshot supplies a
  useful before/after: it records the state of the registry cluster
  five days before this run.
- **Scope caveat — RHAIRFE excluded**: the RHAIRFE project (feature
  requests) was not systematically searched; RHAIRFE keys below
  (RHAIRFE-2443, -2388, -2387, -2389, -1484, -1313, -2310) surfaced
  only through issue links from the RHAISTRAT cluster. A dedicated
  RHAIRFE sweep could surface additional registry-shaped demand.
- **The registry cluster, as of 2026-07-16** (all paraphrased):

| Key | Type | Status | What it is (paraphrased) |
|---|---|---|---|
| RHAISTRAT-1355 | Outcome | In Progress | unified governance of agentic assets (agents, skills, MCP servers) |
| RHAISTRAT-1697 | Outcome | In Progress | Agent Hub UI umbrella — registry view + deployments view + deploy |
| RHAISTRAT-1758 | Feature | In Progress (fixVersion 3.5 GA) | dashboard view of running agent instances |
| RHAISTRAT-1742 | Feature | In Progress (fixVersion 3.6 EA1) | deploy agent images from the deployments page |
| RHAISTRAT-1436 | Feature | New (3.6-candidate, no fixVersion) | **MLflow-native agent registry backend** — schema, CRUD, governance lifecycle; 9 child epics |
| RHAISTRAT-1955 | Feature | New | agent lifecycle management — register via a single CR, discovery, cleanup |
| RHAISTRAT-1956 | Feature | **Closed** | automated, authenticated sync of agent capability metadata from running workloads |
| RHAISTRAT-2019 | Feature | New | the platform↔agent runtime contract (injection surface + agent obligations incl. the well-known card endpoint) |
| RHAISTRAT-2239 | Feature | New | OTEL trace ingestion into managed MLflow via OpenShell env-var injection |
| RHAISTRAT-2067 | Feature | In Progress | validated agentic base images (RHAISTRAT clone of RHAIRFE-2443, Approved; AIPCC epic In Progress) |

- **Baseline deltas vs what the research assumed** (the interop-filed
  cluster of 1355/1697/1758/1955/1956/2019):
  1. **RHAISTRAT-1436 exists and was not on the map.** A dedicated
     agent-registry-backend Feature (paraphrased: metadata schema,
     required owner field, CRUD API, Python client, governance
     lifecycle, workspace-aware MLflow store), decomposed into nine
     epics (RHAI-8…RHAI-16), assigned to the same person who authored
     upstream RFC-0008. The research treated the EA2 backend as
     untracked; it is tracked — under the AI Hub outcome
     (RHAISTRAT-1339), not the interop cluster.
  2. **RHAISTRAT-1956 closed within the last five days.** The interop
     snapshot (2026-07-11) records it as New; today it is Closed, with
     no children, no fixVersion, and its cloned feature request
     (RHAIRFE-2388) still Approved. Its written strategy was
     implemented entirely on the kagenti operator (card reconciler,
     AuthBridge, SPIFFE-verified JWS fetch — paraphrased), so closure
     is consistent with the kagenti roadmap removal (2026-07-10) —
     but the close reason is not visible anonymously: **unconfirmed —
     needs owner check**.
  3. The adjacent card-discovery chain is also closed:
     RHAISTRAT-1213 (early dev-preview of agent-card-based
     post-deployment discovery, paraphrased) and RHAISTRAT-1599
     (productizing the agent operator, paraphrased) — both Closed.

## Direction A — active work vs the landscape

Per registry-relevant active item: **ahead** (Jira anticipates the
research), **behind** (research moved past the issue's assumptions),
or **different approach** (deliberate or accidental divergence).

### RHAISTRAT-1436 — agent registry backend (New)

- **Ahead — existence and authorship.** The backend the research
  called for is not only tracked but decomposed (nine epics spanning
  schema/protobuf, REST + workspace-aware store, Python client, Go SDK
  CRUD, operator RBAC, transition enforcement, docs — paraphrased) and
  owned by the RFC-0008 author. That collapses the
  upstream/downstream alignment problem
  ([question-rfc0008-phase2-agent-entity](/features/agent-registry/knowledge/question-rfc0008-phase2-agent-entity.md))
  into one person's roadmap: the Phase-2 agent entity and the RHOAI
  backend schema have a common author to converge through.
- **Different approach — single entity, single track.** The schema
  (paraphrased) is one Agent record carrying identity/versioning,
  runtime/deployment references (endpoint, environment, runtime type),
  capabilities, and governance fields, with one lifecycle
  (experimental → active → deprecated → archived) enforced by a
  dedicated epic (RHAI-14). That is Pattern A from
  [09 §2.1](/features/agent-registry/research/09-architecture.md) —
  the research recommends Pattern B (AgentVersion + runtime instance
  joined by `version_ref`), and Jira's own UI split (1697's registry
  vs deployments views) implies Pattern B. There are **no runtime
  instance states** (ACTIVE/UNHEALTHY/STALE/REMOVED) anywhere in the
  epic decomposition, and no four-track governance (approval /
  verification / certification are absent; the MCP-registry precedent
  is not mirrored). This is the biggest design divergence between
  active work and the research, and it is cheap to fix before the EA2
  schema freeze and expensive after.
- **Behind — the sync epic targets a removed component.** One child
  epic (RHAI-12, paraphrased: a uni-directional controller syncing
  kagenti deployment state into the registry) is built on the
  substrate removed from the roadmap on 2026-07-10. The MCP-precedent
  replacement (watch `Sandbox` CRs, ADR-#142 pattern generalized —
  09 §3.2) exists as a design but not as a Jira update.
- **Partial vs the regulatory record** (10 §1.2): owner is a required
  registration field (good — strongest requirement), and the schema
  reserves compliance-tag and access-tier extension fields
  (paraphrased). Missing against the eight-field record: an explicit
  **risk-classification field**, purpose taxonomy, **log/audit-trail
  references**, and **permissions/identity linkage** (SPIFFE
  ID/service account). Deregistration is soft-delete-to-archived by
  default (good instinct) but with **no retention commitment** — Art.
  26 needs ≥6 months on removed-instance records.

### RHAISTRAT-1697 / -1758 / -1742 — Agent Hub UI (In Progress)

- **Ahead — the two-entity split is institutionalized.** The outcome's
  own framing (paraphrased) distinguishes the registry view (what is
  registered, MLflow-fed) from the deployments view (what is running)
  and records that the two concepts had been generating duplicate
  issues. This matches 09 §2 exactly and is the strongest Jira-side
  evidence for the dual-entity model — ironically stronger than the
  backend's current schema.
- **Ahead — OpenShell re-baselining is underway on the UI side**: a
  design-revision story for the OpenShell backend hangs off both 1758
  and 1742 (paraphrased), and the deployments view carries a 3.5 GA
  fixVersion with BFF/UI epics in progress/testing.
- **Behind — the registry view has no scheduled data source.** The
  registry-view UI vehicle (RHAIRFE-1313, paraphrased: browse/search
  registered agents in the dashboard) is still in stakeholder review,
  and its declared data source (1436) has no fixVersion. Meanwhile
  the deploy path (1742) is committed to 3.6 EA1. This is
  [question-registry-view-ea1-data-source](/features/agent-registry/knowledge/question-registry-view-ea1-data-source.md)
  made visible in Jira structure: EA1 ships a deploy flow and a
  deployments view, and either the registry view slips or it ships on
  a stopgap feed that collapses the 1697/1758 distinction (09 §4.3).
  No issue records the decision either way.

### RHAISTRAT-1955 — agent lifecycle management (New)

- **Different approach, currently stranded.** The core concept
  (paraphrased: register any existing Deployment by creating one
  custom resource; the platform makes it discoverable and cleans up
  on removal) is exactly the "declarative registration CR as a fourth
  discovery source" that 09 §3.2 endorsed as the GitOps-native
  registration path — and it is the **only** active vehicle for
  discovering Mode-1/BYO agents that don't run as Sandbox CRs.
- **Behind — the strategy is written on the dead substrate** (kagenti
  operator, its label convention, sidecar injection, card sync —
  paraphrased). Its sibling (1956) was closed post-kagenti; 1955
  remains New. Whether it survives re-baselined onto
  OpenShell/Sandbox or follows its sibling is **unconfirmed — needs
  owner check**; the answer determines whether the BYO discovery gap
  (Direction B, row 4) has a home or not.

### RHAISTRAT-2019 — agent runtime contract (New)

- **Ahead — the contract content**: agent obligations include exposing
  health probes and an A2A agent card at the well-known path
  (paraphrased) — the contractual guarantee the registry's enrichment
  loop depends on (09 §1.3 assumes the endpoint exists; this issue is
  what makes that assumption enforceable).
- **Behind — the injection mechanism** is specified via the kagenti
  webhook and label convention (paraphrased); needs the same
  OpenShell re-baseline as everything else in the cluster. No
  suspend/lifecycle semantics in the contract — consistent with the
  SUSPENDED gap below.

### RHAISTRAT-1956 — agent metadata extraction (Closed)

- **Behind the landscape by subtraction.** The research (09 §1.6,
  00 finding 3) called this "the only vehicle" for the card-fetch +
  verification loop — the only path back to a `verified=true` agent
  record. Its acceptance criteria (paraphrased: capability metadata
  stays current with the running workload, re-syncs on rollout,
  mutually authenticated exchange) are precisely the enrichment loop.
  It is now Closed with no successor issue, while the demand-side
  feature request (RHAIRFE-2388) remains Approved. Every hyperscaler
  registry the landscape doc surveys does the equivalent ingestion
  (AWS ingests from live A2A/MCP endpoints; Salesforce scanners
  normalize to A2A cards). This is Direction B row 1.

### RHAISTRAT-2239 — OTEL trace ingestion via OpenShell (New)

- **Ahead**: re-implements the observability-wiring capability that
  died with kagenti (09 §1.6 gap 6) on the OpenShell substrate
  (paraphrased: inject standard OTEL env vars pointing at MLflow's
  OTLP endpoint). **Partial**: nothing yet joins those traces to
  registry version records (the LoggedModel/`version_ref` linkage of
  09 §2.2) — traces land in MLflow, but "which governed version
  produced this trace" is not in scope anywhere.

### RHAISTRAT-2067 / RHAIRFE-2443 — agentic base images (In Progress)

- **Aligned**: Konflux-built, signed-SBOM, multi-arch base images with
  an active AIPCC epic (paraphrased) — matches 07 §4. The
  registry-side seam (AgentVersion pinning image digests + attestation
  references, enabling the CVE blast-radius query of 09 §5) belongs to
  neither this feature nor 1436's schema — Direction B row 9.

### Adjacent, correctly-scoped elsewhere

- Skills-registry downstream vehicles exist (RHAISTRAT-1630, -1940,
  paraphrased: self-hosted skills management; pre-loaded skills) —
  consistent with the RFC-0008 Phase-1 posture; linked to 1436.
- Asset signing/attestation has an Outcome (RHAISTRAT-936,
  paraphrased: integrate signing/attestation/verification of AI
  assets) plus model-signing features (RHAISTRAT-2214, -2211) — all
  model/artifact-shaped; none mention agent cards. Candidate umbrella
  for R1 below rather than coverage.
- MCP Registry work (RHAISTRAT-1762, -1993, -2027, paraphrased:
  operational governance, GA, catalog↔registry integration) continues
  to be the governance pattern-setter the agent backend should mirror.

## Direction B — landscape vs active work (the payload)

Signal strength: how strong the external evidence is (per the graded
research). Category: **intentional omission** (a decision not to is on
record) / **blind spot** (no evidence anyone saw it) / **emerging
opportunity** (too new to have decided).

| Area | Signal strength | Category | Notes |
|---|---|---|---|
| 1. Card-verification producer (JWS fetch/verify; `verified`/`identity`/`trust_domain`) | **Strong** — A2A §8.4 spec + sigstore-a2a tooling exist; AWS/Salesforce ship card ingestion; fields have no producer (09 §1.6) | **Blind spot** (regression) | Coverage existed (RHAISTRAT-1956) and closed ~2026-07-1x with no successor; RHAIRFE-2388 still Approved. Closed card-chain: 1956, 1213, 1599. Adjacent signing outcome (936) is artifact-shaped, not agent-card-shaped. The single most urgent re-file. |
| 2. Runtime instance entity + states (incl. SUSPENDED) in the backend | **Moderate-strong** — Sandbox `operatingMode: Suspended` shipping in v1beta1; regulators require the "running" view (10 §1.2); 09 §4.2 | **Blind spot** | RHAISTRAT-1436 has one governance lifecycle only (RHAI-14, paraphrased); no runtime states anywhere. Schema-freeze-sensitive: cheap before EA2, breaking after. Also the verified-naming hazard (09 §4.1 join point 4). |
| 3. EA1 registry-view data source | **Strong** (internal sequencing, not market) | **Emerging opportunity** (decision-shaped) | 1697 declares the registry view MLflow-fed; 1436 unscheduled; registry-UI RFE (RHAIRFE-1313) in stakeholder review while deploy (1742) is committed to EA1. No issue records the stopgap-vs-slip decision. Product call needed before the EA1 build. |
| 4. BYO/Mode-1 discovery convention (post-kagenti label orphan) | **Moderate-strong** — auto-discovery is table stakes (08 trend 4); plain-Deployment agents invisible to Sandbox-CR discovery | **Blind spot** (orphaned) | Only vehicle is 1955's registration CR, whose strategy targets the removed operator; sibling issue closed, this one's fate unconfirmed — needs owner check. No label-convention successor tracked anywhere. |
| 5. Shadow-agent inventory + adopt-into-governance flow | **Strong** — 82% discovered unknown agents; commercial category formed; Microsoft ships inventory free (08, 10 §2) | **Blind spot** | Zero baseline hits for shadow/inventory/unregistered semantics. 1436's sync concept (paraphrased) syncs *registered* deployments one-way; nothing creates unlinked-instance records from unregistered workloads or offers the one-click adopt path (10 §4 moment 4). Interop jira-gap flagged discovery generally (their G12); the registry-side record state and adopt flow are new here. |
| 6. Regulatory record completion (risk tier, purpose, log refs, permissions) | **Strong** — EU AI Act dates 2026-08-02; Gartner tiered-governance mandate; eight-field convergence (10 §1.2) | **Blind spot** (partial) | 1436 requires owner and reserves compliance/access-tier fields (paraphrased) but has no risk-classification field, no log/audit-trail reference, no identity/permissions linkage. Zero baseline hits for risk-tier/AI-Act-shaped registry work. |
| 7. REMOVED/archived record retention (≥6 months) | **Moderate** — Art. 26 log duty; forensics requirement (10 §2) | **Blind spot** (small) | 1436 defaults to soft-delete (paraphrased) — right instinct, no retention period or forensic-record commitment. One acceptance-criterion-sized fix. |
| 8. ARD / federation endpoint (`/.well-known/ai-catalog.json`, URN-mappable IDs) | **Moderate** — v0.9 spec, thin adoption, but federation shipping bilaterally around us (07 §2, 08) | **Emerging opportunity** | Zero baseline hits for federation/ARD/discovery-spec. Research recommends implement-behind-a-flag while the spec is soft; cheap hedges (URN-mappable IDs, native-media-type card storage) are schema decisions that belong in 1436 now. |
| 9. Base-image provenance linkage in registry records (digest + attestation refs → CVE blast-radius query) | **Moderate** — Konflux attestation machinery settled; the query only the registry can answer (09 §5) | **Blind spot** (seam) | Both ends tracked (2067 images; 936 signing) — the join (AgentVersion pins digest, records attestation verification at ingestion) is in nobody's scope. |
| 10. Namespace↔workspace mapping for discovered instances | **Weak-moderate** — inference from MLflow workspace RBAC + GitOps reality (09 §4.3) | **Blind spot** (design point) | RHAI-15 (paraphrased: workspace-aware store) scopes *records*; how a reconciled instance from an arbitrary namespace acquires a workspace has no owner. Attach to the sync-controller re-baseline, not a new feature. |
| 11. Revocation lookup linkage (registry-side) | **Moderate** — kill-switch evidence heavy but vendor-amplified (10 §2); boundary: registry = lookup, not enforcement | **Blind spot** (schema field) | No agent-revocation work in baseline (only a MaaS API-key item, unrelated — paraphrased). Enforcement is interop territory (their series); the registry-side gap is only that 1436's schema carries no identity linkage to make revocation one query away. Fold into row 6, don't file separately. |
| 12. Cross-registry composition/lineage (agents → models/MCP/prompts/sub-agents) | **Moderate** — CSA delegation-lineage expectations make it compliance-adjacent (10 §1.2) | **Intentional omission** (revisit) | Explicitly deferred in the upstream proposal and filed as [question-agent-registry-composition-graphs](/features/agent-registry/knowledge/question-agent-registry-composition-graphs.md); only data-side lineage work exists (RHAISTRAT-1931, paraphrased). The deferral predates the regulatory evidence — the decision deserves a re-vote at Phase-2 time, not silent inheritance. |

Resolved candidate (not a gap): **registry backend (EA2) tracking
itself** — covered by RHAISTRAT-1436; moved to Direction A.

## Recommended actions

Following the tiering pattern of the
[interop jira-gap §6](/features/agent-interop/research/06-jira-gap.md).

### Tier 1 — file/act now (blocking the registry's own 3.6 story)

| # | Action | Covers | Rationale |
|---|---|---|---|
| R1 | **File the card-fetch + verification successor** — registry-side enrichment loop: fetch cards from discovered endpoints over authenticated channels, verify JWS (sigstore-a2a as candidate producer), record verification status per instance | B1 | The Closed 1956 leaves `verified=true` with zero paths; RHAIRFE-2388's demand survives. Scope it registry-side (not a new operator), reference RHAISTRAT-936 as the signing umbrella. Without it the GA trust story (09 §4.3) has no producer. |
| R2 | **Re-baseline RHAISTRAT-1436's sync epic off kagenti** — watch Sandbox CRs (ADR-#142 pattern generalized), define unlinked-instance adoption semantics, and settle the namespace↔workspace mapping in the same design | B4 (partly), B5, B10, RHAI-12 staleness | One epic rewrite converts three blind spots into scoped work and de-strands the backend from the removed substrate — before the EA2 backend freezes an architecture around a dead controller. |
| R3 | **Force the EA1 registry-view data-source decision** — a recorded product call on 1697/RHAIRFE-1313: deploy-time-registration feed (even file-backed), explicit slip to EA2, or a labeled preview of the deployments view | B3 | Not an RFE — a decision memo. Every week undecided converts into stopgap code that collapses the 1697/1758 split (09 §4.3). |

### Tier 2 — next planning cycle (schema-freeze-sensitive)

| # | Action | Covers | Rationale |
|---|---|---|---|
| R4 | **Dual-entity/runtime-state RFE against the backend** — instance records (ACTIVE/UNHEALTHY/STALE/REMOVED + SUSPENDED) with nullable `version_ref`, joined to the governance record; rename the verification/verified collision | B2 | Aligns 1436 with its own UI outcome's two-view model and with the RFC-0008 Phase-2 input the strategy work is preparing — same author both sides, lowest-friction moment. |
| R5 | **Regulatory record completion on the 1436 schema** — risk-classification field, purpose taxonomy, log/audit-trail reference, identity/permissions linkage, ≥6-month archived-record retention | B6, B7, B11 | Five fields and a retention line; turns the schema from governance-flavored into audit-defensible before Art. 26/49 obligations bite (2026-08-02). |
| R6 | **Decide the BYO discovery convention** — either re-baseline 1955 (registration CR + a platform-owned label convention) or fold BYO adoption into the R2 sync controller; either way, name an owner | B4 | The 82%-shadow-agent evidence says unregistered agents are the norm; Mode-1 agents are currently invisible by construction. |
| R7 | **AgentVersion ↔ image-digest/attestation linkage** — pin digests on version records, record attestation verification at ingestion, ship the CVE blast-radius query as the demo | B9 | Joins two funded efforts (2067, 936) at the seam only the registry occupies; the single most demo-able differentiator for the wedge story (08). |

### Tier 3 — backlog / monitor

| # | Action | Covers | Rationale |
|---|---|---|---|
| R8 | ARD emit/consume behind a flag; immediately: keep 1436 IDs URN-mappable and store cards in native media types | B8 | Implement-and-influence window while the spec is soft; the schema hedges cost nothing now. |
| R9 | Composition/delegation lineage — re-vote the deferral when RFC-0008 Phase 2 lands, with the CSA evidence on the table | B12 | Intentional omission whose premises changed; a decision refresh, not yet a feature. |
| Monitor | Solo.io agentregistry CNCF review (2026-09-22) — positioning statement, not an RFE; revocation enforcement stays in the interop lane | — | Per 07/08 watch list and the interop series' scope. |

## Supersedes / corrections

Net-new coverage — this is the first registry-scoped jira-gap lens. Two
sibling touch-ups, no supersessions:

1. **[interop 06-jira-gap](/features/agent-interop/research/06-jira-gap.md)
   coverage matrix (2026-07-11)** — rows listing RHAISTRAT-1956 (New)
   and the registry cluster as confirmed coverage are now stale in one
   cell: 1956 is Closed (this doc, Baseline). Their G12 (shadow-agent
   discovery) gains the registry-side specificity of B5 here.
2. **[00-executive-summary](/features/agent-registry/research/00-executive-summary.md)
   "jira-gap not run" lens-gap note** — discharged by this document.
   Also: 00/09's "RHAISTRAT-1956 is the only vehicle" for card
   verification should now read "the vehicle closed 2026-07-1x; no
   active vehicle exists" (finding, not correction — the closure
   post-dates those docs by hours-to-days).

## Sources

- Live Jira reads 2026-07-16 via `scripts/hub_jira.py` (read-only):
  baseline JQL (500-cap noted), 110-issue narrowed slice, per-key
  audits of RHAISTRAT-1355, -1436, -1697, -1742, -1758, -1955, -1956,
  -2019, -2067, -2239, RHAI-14; targeted JQL probes (federation/ARD,
  shadow/inventory, revocation/suspend, signing/attestation,
  lineage/composition, risk-tier/AI-Act, retention/workspace — hit
  counts as cited inline). All issue content paraphrased.
- Committed snapshots:
  [agent-interop/work/jira-snapshot.yaml](/features/agent-interop/work/jira-snapshot.yaml)
  (209 issues, 2026-07-11) ·
  [agent-catalog/work/jira-snapshot.yaml](/features/agent-catalog/work/jira-snapshot.yaml)
  (37 issues, 2026-07-16)
- Research inputs:
  [07-upstream](/features/agent-registry/research/07-upstream.md) ·
  [08-landscape](/features/agent-registry/research/08-landscape.md) ·
  [09-architecture](/features/agent-registry/research/09-architecture.md) ·
  [10-requirements](/features/agent-registry/research/10-requirements.md) ·
  [knowledge index](/features/agent-registry/knowledge/index.md) ·
  [interop 06-jira-gap](/features/agent-interop/research/06-jira-gap.md)
