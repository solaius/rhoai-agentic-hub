---
title: Agent Registry research — executive summary
description: Living synthesis after the 2026-07-16 post-split refresh — the April first-mover thesis is retired, the play is now RFC-0008 Phase 2 upstream plus owning the unowned post-deployment join (enumeration without enrichment), inside a time-boxed self-managed/disconnected wedge.
timestamp: 2026-07-16
review_after: 2026-10-16
---

# Agent Registry research — executive summary

This is the living synthesis for the agent-registry research series.
**Refresh run 2026-07-16** (standard depth, 4 lenses: upstream, landscape
with competitive signals folded in, architecture, requirements) — the
first refresh since the partition split (catalog/starter kits →
agent-catalog; sandboxing/identity → agent-interop) and since kagenti was
removed from the roadmap (owner ruling 2026-07-10). Docs 01–06 are the
migrated April 2026 series and stand as written except where their
supersede notes say otherwise; docs 07–10 are this refresh. Sibling
research is standing context throughout:
[agent-interop 00](/features/agent-interop/research/00-executive-summary.md)
(2026-07-11) and
[agent-catalog 00](/features/agent-catalog/research/00-executive-summary.md)
(2026-07-16).

## The series

| Doc | Lens | State |
|---|---|---|
| [01-agent-ecosystem](01-agent-ecosystem.md) | landscape (2026-04) | current — terminology/abstraction ladder still holds |
| [02-standards-and-protocols](02-standards-and-protocols.md) | upstream (2026-04) | superseded in part → 07 (A2A v1.0.1 + extensions, ARD) |
| [03-kagenti-and-kubernetes](03-kagenti-and-kubernetes.md) | architecture (2026-04) | superseded → 09 (kagenti spine removed) |
| [04-agent-management-landscape](04-agent-management-landscape.md) | competitive (2026-04) | superseded in part → 08 (market GA'd past it) |
| [05-mlflow-upstream](05-mlflow-upstream.md) | upstream (2026-04) | superseded in part → 07 (RFC-0008 exists) |
| [06-rhoai-context](06-rhoai-context.md) | requirements (2026-04) | superseded in part → 09/10 |
| [07-upstream](07-upstream.md) | upstream | **new 2026-07-16** |
| [08-landscape](08-landscape.md) | landscape | **new 2026-07-16** |
| [09-architecture](09-architecture.md) | architecture | **new 2026-07-16** |
| [10-requirements](10-requirements.md) | requirements | **new 2026-07-16** |
| [11-jira-gap](11-jira-gap.md) | jira-gap | **new 2026-07-16** (same-day follow-up run) |

## The bottom line

The April thesis — "the MLflow namespace is unoccupied, move before a
competitor does" — is retired, half by success and half by the market.
The upstream registry stream now exists and is **Red Hat-authored**:
RFC-0008 (MVP Skill Registry, Phase 1, draft PR 2026-07-14) puts
metadata-first records and lifecycle stages upstream, with agent-shaped
entities explicitly deferred to Phase 2. Meanwhile every hyperscaler
shipped or GA'd a registry around us (Microsoft GA'd Agent 365 with a
free inventory floor; Google shipped a documented registry product; AWS
is still in preview; IBM repositioned as an "Agentic Control Plane" —
SaaS-only for now). The registry lag is ~6–12 months, smaller than the
catalog's 12–18.

The play that remains is specific: **(1) shape RFC-0008 Phase 2** so the
agent entity lands with the dual-entity structure the platform needs;
**(2) own the post-deployment join nobody owns** — kagenti's removal
split enumeration from enrichment: `Sandbox` CRs enumerate workloads but
carry zero agent semantics, and no component fetches or verifies agent
cards anymore, so the schema's `verified`/`identity`/`trust_domain`
fields have no producer (the former vehicle RHAISTRAT-1956 closed
between 2026-07-11 and 07-16 with no successor — see finding 15); **(3) hold
the wedge** — nobody ships a self-managed, disconnected, governed fleet
registry with lineage, and regulation now effectively mandates the
record shape we'd govern — but the window is time-boxed by IBM's
eventual on-prem port and by Solo.io's `agentregistry` occupying the OSS
slot (CNCF Sandbox review 2026-09-22).

## Key findings (2026-07-16)

1. **RFC-0008 is skills-first, agents are Phase 2.** The upstream
   registry conversation runs through mlflow/rfcs PR #26 (Bill Murdock,
   draft, no review activity yet) and feeder issue mlflow/mlflow#22833.
   Lifecycle stages are proposed **in the upstream core** — shrinking
   the downstream governance delta if accepted (07).
2. **Varsha's post-deployment branch is dormant** (no commits since
   2026-04-23; the last one deepened the now-dead kagenti dependency).
   Its abstract `AgentDiscoveryProvider` interface survives; its
   reference plugin does not. Natural vehicle: the runtime-discovery
   companion to RFC Phase 2 (07, 09).
3. **Enumeration and enrichment have split.** Sandbox v1beta1 CRs
   (v0.5.0 2026-06-24, v0.5.1 2026-07-09) expose infrastructure fields
   only. The recommended architecture: WATCH Sandbox CRs to enumerate;
   register-on-deploy (WEBHOOK) for rich records gated on approval;
   an ADR-#142-style sync controller adopting out-of-band/GitOps
   deployments as **unlinked instances** (the shadow inventory,
   visible); a registry-side card-fetch + JWS-verification loop as the
   only path back to `verified=true` (09).
4. **Dual entities, not one**: AgentVersion (four governance tracks,
   MCP Registry pattern) ↔ Agent instance (runtime states), joined by a
   nullable `version_ref`; join keys in strength order: stamped
   annotations > image digest + config hash > card identity claims.
   RHAISTRAT-1697 (registry view) vs -1758 (deployments view) already
   encode the two-entity split (09).
5. **Governance and runtime state machines don't map — by design.**
   Four join points instead (deploy gate, deprecation impact,
   retire-safety evidence, forensics). Varsha's model needs a
   **SUSPENDED** state (Sandbox `operatingMode: Suspended` has no home),
   and the governance Verification track vs the runtime `verified` bit
   is a naming hazard to resolve before the EA2 schema freeze (09).
6. **Sequencing risk — re-timed 2026-07-16 (owner)**: registry work
   starts 3.6 EA2 at the earliest, on a multi-release path to DP
   (~3.7 EA1 directional, no committed GA), and deployment is its own
   workstream — so any registry-view surface shipped before the backend
   exists would predate it. A Sandbox-CR-fed stopgap view would collapse
   the 1697/1758 distinction on arrival — the first registry view's data
   source is an open product call, including "don't ship one early"
   (09; re-timing per /memory/profiles/roadmap.md History).
7. **Regulation converged on the record shape**: EU AI Act (Art.
   26/49/50) + OMB M-25-21 + NIST GV-1.6/CSA jointly force an eight-field
   agent record (identity+version, owner, purpose, risk class, lineage,
   status, log refs, permissions); the pre/post dual structure maps 1:1
   onto "approved vs running". Registry retention: keep REMOVED-instance
   records ≥6 months. Caution: the Apr 2026 interagency MRM guidance
   **excludes** agentic AI from model-risk scope — don't claim SR 11-7
   extends to agents (10).
8. **Shadow-agent inventory is the best-evidenced fleet need** (82% of
   orgs discovered unknown agents; 67% of NHIs unseen by IAM; discovery
   tooling is now a commercial category — Zenity, WitnessAI, plus
   Microsoft's free tier). The unlinked-instance state is the direct
   answer (08, 10).
9. **The registry market inverted its monetization**: Microsoft ships
   the inventory free and charges $15/user/mo for the governance stack;
   AWS signals per-record GA pricing; registries are directly monetized
   — an infra-priced registry is a TCO argument, blunted by Microsoft's
   free floor (08).
10. **Federation is arriving bilaterally, not via standards**:
    ServiceNow ↔ Agent 365 dual-registry publishing ships; Salesforce
    Agent Scanners auto-discover cross-cloud agents normalized to A2A
    cards; the ARD spec (Google+Microsoft+9, v0.9, /.well-known/ai-catalog.json)
    formalizes the discovery layer but adoption is thin — implement-and-
    influence window, cheap hedge is URN-mappable IDs + native-media-type
    card storage (07, 08).
11. **Unity Catalog made agents first-class** (DAIS 2026) and Databricks
    open-sourced Unity AI Gateway pieces into MLflow — upstream MLflow is
    becoming a governance surface; free primitives for us, Databricks
    steering the substrate (07, 08).
12. **Upstream kagenti is NOT winding down** — it remains active
    (v0.6.1, Jun 2026) and is rebranding to **Rosso**. The roadmap
    removal is Red Hat's decision, not upstream's status; public docs
    must keep the two claims separate (07).
13. **Base images are supply-chain metadata on versions, not registry
    entities**: AgentVersion pins the harness image digest + Konflux
    attestation refs (SLSA/in-toto/cosign); attestations mirror via the
    OCI referrers API (verification recorded at ingestion — no live
    Rekor calls in enclaves). Payoff: the CVE blast-radius query
    ("which ACTIVE agents run the affected base?") only the registry can
    answer. Public pipeline tip: opendatahub-io/agentic-ci publishes
    daily coding-agent runner images to quay.io/aipcc/ (07, 09, 10).
14. **Scale/SLO**: design for tens-to-hundreds of governed agents per
    tenant, thousands of discovered instances per fleet; the scaling
    pressure is the discovery write path. Keep runtime-critical
    resolution OUT of the registry (revocation is enforced in the
    identity/gateway plane; the registry is the lookup) (10).
15. **The card-verification vehicle closed days after being identified
    as the long pole.** RHAISTRAT-1956 (New in the 2026-07-11 interop
    snapshot) is Closed as of 07-16, no children, close reason not
    anonymously visible; the whole card chain (1956, 1213, 1599) is
    closed while clone RHAIRFE-2388 remains Approved. Zero active Jira
    paths to `verified=true` — the single most urgent re-file (11).
16. **The EA2 backend is tracked after all — and diverges.**
    RHAISTRAT-1436 (unscheduled, parent AI Hub, 9 epics) is MLflow-native
    with a single entity and single governance lifecycle: no runtime
    states, no SUSPENDED, no `version_ref`, no risk-tier/log-refs/
    retention fields, and a sync epic still targeting removed kagenti.
    It is assigned to the RFC-0008 author — upstream and downstream
    share an author, so the alignment channel exists. Schema input is
    cheap before the EA2 freeze, breaking after (11).

## Boundary notes (siblings)

- The registry-shaped Jira surface (RHAISTRAT-1355, -1697, -1758, -1955,
  -1956, -2019) is filed under agent-interop and cross-listed here via
  `features:` — no re-filing needed.
- "Deploy always registers, reconcile the rest" comes from the catalog
  series (their 04/01) and is adopted by 09's architecture; the deploy
  path is catalog territory, the registration semantics are ours.
- Agentic base images (RHAIRFE-2443/AIPCC) are shared with agent-catalog
  (their supported-images program consumes them; our registry records
  their provenance). Licensing/air-gap depth lives in catalog 04.

## Open question status

| Question | Finding | Status |
|---|---|---|
| kagenti integration architecture (pull/push/hybrid) | Moot — kagenti removed; dissolves into Sandbox WATCH + deploy WEBHOOK + sync controller | answered (09) |
| Pre- vs post-deployment relationship | Recommendation: separate entities + hard `version_ref`, LoggedModel as lineage hub; regulators need both views | open — evidence added (09, 10) |
| Lifecycle ↔ governance mapping | Don't map: orthogonal machines, four join points; SUSPENDED missing; verified-naming hazard | open — evidence added (09, 10) |
| Discovery plugin generalization | Unchanged (RFC-0008's typed-source design points the same way); duplicate entry removed | open |
| Governance integration (multi-track) | AWS approval-workflow precedent; RFC-0008 puts lifecycle stages upstream | open — evidence added (07, 10) |
| Composition graphs | CSA delegation-lineage expectations make it compliance-adjacent, still deferred | open — evidence added (10) |
| Base images: UBI version, product ID | No new external data; two Red Hat shapes coexist (UBI runner images vs fedora-bootc host proposal) sharpens the ADR question | open (07) |

## Lens gaps

- ~~**jira-gap not run**~~ — DONE same day (2026-07-16), see
  [11-jira-gap](11-jira-gap.md): 12-row Direction B table, RHAISTRAT-1436
  found, 1956 closure caught.
- **competitive not run as a separate lens** — competitive signals were
  folded into 08 by plan; a dedicated pass (e.g. IBM ACP on-prem
  tracking, AWS GA pricing) remains available:
  `hub.research agent-registry competitive`.

## Recommended follow-ups (not auto-run)

- **Re-file card verification** (most urgent, from 11): RHAISTRAT-1956
  closed with no successor while RHAIRFE-2388 sits Approved — an owner
  check on the close reason, then a post-kagenti re-file (registry-side
  fetch + JWS verify per 09 §3), is the only path back to
  `verified=true`.
- **1436 schema input before the EA2 freeze** (from 11): runtime
  instance states + SUSPENDED, `version_ref`, risk tier, log refs,
  retention — cheap now, breaking later; the shared author with RFC-0008
  is the channel.
- **Shape RFC-0008 Phase 2**: the agent entity design (dual-entity,
  SUSPENDED state, card-verification fields) should be prepared as
  upstream input before Phase 1 review concludes — this is the
  strategy-doc work `strategy/strategy-status.md` has been waiting on.
- **Re-baseline Varsha's proposal** off kagenti onto Sandbox/OpenShell
  (doc 09 §1 is the input) as the Phase-2 runtime-discovery companion.
- **hub.jira-sweep agent-registry** — the partition still has no stored
  Jira scope of its own (11 ran off the domain JQL + sibling snapshots);
  a sweep would make the next jira-gap cheaper and enable hub.jira-sync.
- **First-registry-view data source decision** (question filed, now
  Jira-confirmed) — registry work starts 3.6 EA2 at the earliest (owner
  re-timing 2026-07-16), so any earlier registry-view surface needs a
  deliberate product call — or an explicit deferral.
- **Watch list for next refresh**: RFC-0008 PR #26 review state; OpenShell
  Go SDK PR series (only Part A open as of 07-16); Solo.io agentregistry
  CNCF review (2026-09-22); IBM ACP on-prem port; AWS registry GA +
  pricing; ARD adoption beyond GitHub Agent Finder; agent-sandbox
  post-v1beta1 API churn.

## Verification

Standard run — no adversarial verification pass (deep-run feature). The
orchestrator re-verified the one flagged ambiguity: agent-sandbox
v0.5.0 = 2026-06-24, v0.5.1 = 2026-07-09 (GitHub releases API), and
HTTP-verified the four load-bearing new-source URLs (RFC-0008 PR, ARD
site, sigstore-a2a, Solo.io agentregistry). Load-bearing claims carry
inline primary-source citations in 07–10.
