---
title: Agent Registry research — executive summary
description: Living synthesis after the 2026-08-03 requirements + competitive refresh — Google GA'd July 30, AWS GA imminent (Aug 6 namespace migration), Gartner "Guardian Agents" category established, EU AI Act live, 7 new funded entrants; wedge holds but window narrows to 6-9 months; P1-P11 validated, three design questions answered, dependency immutability is a differentiator.
timestamp: 2026-08-03
review_after: 2026-11-03
---

# Agent Registry research — executive summary

This is the living synthesis for the agent-registry research series.
**Refresh run 2026-08-03** (standard depth, requirements + competitive
lenses) — triggered by Adel Zaalouk's product scoping doc (P1-P11
customer problems, product scope decisions), three new design questions
from Jiri Daněk's review, and the competitive lens gap flagged since
July. Prior refresh: 2026-07-16 (standard depth, 4 lenses: upstream,
landscape, architecture, requirements). Docs 01-06 are the migrated
April 2026 series; docs 07-11 are the July refresh; docs 12-13 are this
refresh. Sibling research is standing context throughout:
[agent-interop 00](/components/agent-interop/research/00-executive-summary.md)
(2026-08-03) and
[agent-catalog 00](/components/agent-catalog/research/00-executive-summary.md)
(2026-07-24).

## The series

| Doc | Lens | State |
|---|---|---|
| [01-agent-ecosystem](01-agent-ecosystem.md) | landscape (2026-04) | current — terminology/abstraction ladder still holds |
| [02-standards-and-protocols](02-standards-and-protocols.md) | upstream (2026-04) | superseded in part → 07 (A2A v1.0.1 + extensions, ARD) |
| [03-kagenti-and-kubernetes](03-kagenti-and-kubernetes.md) | architecture (2026-04) | superseded → 09 (kagenti spine removed) |
| [04-agent-management-landscape](04-agent-management-landscape.md) | competitive (2026-04) | superseded in part → 08 (market GA'd past it) |
| [05-mlflow-upstream](05-mlflow-upstream.md) | upstream (2026-04) | superseded in part → 07 (RFC-0008 exists) |
| [06-rhoai-context](06-rhoai-context.md) | requirements (2026-04) | superseded in part → 09/10/12 |
| [07-upstream](07-upstream.md) | upstream | **2026-07-16** |
| [08-landscape](08-landscape.md) | landscape | **2026-07-16** |
| [09-architecture](09-architecture.md) | architecture | **2026-07-16** |
| [10-requirements](10-requirements.md) | requirements | **2026-07-16** |
| [11-jira-gap](11-jira-gap.md) | jira-gap | **2026-07-16** |
| [12-requirements-refresh](12-requirements-refresh.md) | requirements | **new 2026-08-03** |
| [13-competitive](13-competitive.md) | competitive | **new 2026-08-03** |

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
SaaS-only for now). The registry lag is ~6-12 months, smaller than the
catalog's 12-18.

The play that remains is specific: **(1) shape RFC-0008 Phase 2** so the
agent entity lands with the dual-entity structure the platform needs;
**(2) own the post-deployment join nobody owns** — kagenti's removal
split enumeration from enrichment: `Sandbox` CRs enumerate workloads but
carry zero agent semantics, and no component fetches or verifies agent
cards anymore, so the schema's `verified`/`identity`/`trust_domain`
fields have no producer; **(3) hold the wedge** — nobody ships a
self-managed, disconnected, governed fleet registry with lineage, and
regulation now effectively mandates the record shape we'd govern — but
the window is narrowing: Google Agent Registry GA'd July 30 (two GA
cloud competitors now), AWS GA is imminent (Aug 6 namespace migration),
Gartner established "Guardian Agents" as a category, and Solo.io's
four-project OSS suite continues building. **Estimated window: 6-9
months** (down from 6-12 in July), time-boxed by IBM's eventual on-prem
port and Solo.io's agentregistry CNCF Sandbox status.

**New in this refresh:** **(4) the product scope is now defined** — Adel's
scoping doc establishes discover/register/audit as the three end
behaviors, catalog-as-view, A2A schema, phased delivery (3.5/3.6/3.7+),
and seven explicit exclusions; **(5) the customer problems are
independently validated** — P2 (visibility) confirmed as #1 by Gartner,
P4 (shadow IT) elevated to #1 CISO risk by Forrester, P11 (costs) is
universal not FSI-specific; **(6) three design requirements have external
evidence** — four-layer versioning + eval-gated promotion, OCI-style
dependency pinning with negotiated deprecation, three-tier visibility
scoping (Backstage model + Bazel deprecation-visibility); **(7)
dependency immutability is a differentiator** — no existing registry
(AWS, Google, Databricks, Solo.io) enforces that active agents' pinned
dependencies cannot be unilaterally deprecated.

## Key findings (2026-07-16, carried forward)

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
   expose infrastructure fields only. Recommended architecture: WATCH
   Sandbox CRs to enumerate; register-on-deploy (WEBHOOK) for rich
   records; an ADR-#142-style sync controller adopting out-of-band/GitOps
   deployments as **unlinked instances** (the shadow inventory,
   visible); registry-side card-fetch + JWS-verification loop as the
   only path back to `verified=true` (09).
4. **Dual entities, not one**: AgentVersion (four governance tracks,
   MCP Registry pattern) ↔ Agent instance (runtime states), joined by a
   nullable `version_ref` (09).
5. **Governance and runtime state machines don't map — by design.**
   Four join points instead. SUSPENDED state missing. Naming hazard on
   verification track vs runtime `verified` bit (09).
6. **Sequencing risk — re-timed 2026-07-16 (owner)**: registry work
   starts 3.6 EA2 at the earliest, multi-release path to DP (~3.7 EA1
   directional, no committed GA) (09).
7. **Regulation converged on the record shape**: eight-field agent record
   mandated across regimes (10).
8. **Shadow-agent inventory is the best-evidenced fleet need** (82%
   discovered unknown agents; discovery tooling is now a commercial
   category) (08, 10).
9. **The registry market inverted its monetization**: inventory
   commoditizing, governance monetized (08).
10. **Federation is arriving bilaterally, not via standards** (08).
11. **Unity Catalog made agents first-class** (07, 08).
12. **Upstream kagenti is NOT winding down** — rebranding to Rosso (07).
13. **Base images are supply-chain metadata on versions** (07, 09, 10).
14. **Scale/SLO**: tens-to-hundreds governed per tenant, thousands
    discovered per fleet; keep runtime-critical resolution OUT of the
    registry (10).
15. **The card-verification vehicle closed** (RHAISTRAT-1956 Closed,
    zero active Jira paths to `verified=true`) (11).
16. **The EA2 backend (RHAISTRAT-1436) diverges** from dual-entity
    design — schema input cheap before EA2 freeze, breaking after (11).

## Key findings (2026-08-03 requirements refresh)

17. **P1-P11 independently validated.** Gartner names "Build Centralized
    Agent Inventory" as foundational step #2; Gravitee confirms 82%
    shadow-agent discovery; Forrester elevates shadow agents to #1 CISO
    risk; all three confirm the product scoping doc's problem taxonomy.
    The priority ordering holds (12).
18. **P4 (shadow IT) may be underweighted.** Forrester's #1 CISO risk
    elevation + AvePoint's 88.4% agent-related breach rate + CSA's
    perception-reality gap (68% claim high visibility, 82% find unknowns)
    suggest P4 deserves higher severity framing than Tier 1 alongside
    P1-P3 (12).
19. **P11 (costs) is universal, not FSI-specific.** EY's 30x cost per
    interaction, Goldman's 24x token growth projection, and Uber's
    budget overrun are cross-sector. The registry's cost attribution role
    (stable identity as the join key for FinOps) is a universal
    requirement (12).
20. **Agent versioning: four layers + eval-gated promotion.** Industry
    converged on versioning code, prompt, model, and tool contracts
    independently; SemVer does not map to non-deterministic systems;
    eval-gated promotion replaces semantic version numbering; MLflow's
    LoggedModel + Prompt Registry are the reference (12).
21. **Dependency immutability is a differentiator.** No existing agent
    registry (AWS, Google, Databricks, Solo.io) enforces that ACTIVE
    agents' pinned dependencies cannot be unilaterally deprecated. OCI
    digest-pinning semantics + negotiated deprecation is the proposed
    pattern (12).
22. **Three-tier visibility scoping answers the Bazel question.** The
    Backstage public/restricted/private model maps cleanly; default
    should be "restricted" (workspace-scoped); deprecation restricts
    visibility to current consumers (Bazel pattern); "no list-all path"
    (TrueFoundry) should be the architectural default (12).
23. **Eight gap requirements not in P1-P11**: NHI identity lifecycle,
    inter-agent boundary testing, eval status as metadata, cost
    attribution tags, context/grounding declaration, dependency
    immutability enforcement, interoperability profile tracking,
    behavioral drift detection (12).

## Key findings (2026-08-03 competitive)

24. **Google Agent Registry GA'd July 30.** RHOAI now faces two GA cloud
    competitors (Google + Microsoft), not one. Google's SPIFFE-based
    agent identity is cloud-neutral by design — a closer architectural
    competitor than Entra Agent ID (13).
25. **AWS GA imminent.** August 6 namespace migration
    (`bedrock-agentcore` → `agent-registry`) is a strong GA signal;
    production-scale quotas (5,000 sessions, 200 TPS) shipped July.
    Three GA competitors approaching (13).
26. **ARD federated discovery protocol announced by Google.** The first
    vendor-backed federated agent discovery standard. If ARD becomes
    de facto, RHOAI's 3.7+ federation roadmap must adopt or compete (13).
27. **Microsoft cross-cloud registry sync in preview.** Agent 365 can
    discover/inventory agents across AWS Bedrock and Google Cloud — the
    most direct threat to RHOAI's multi-cloud positioning. Entra Agent
    ID criticized as "doesn't work outside Azure" (the cross-cloud
    story has substance gaps) (13).
28. **Gartner "Guardian Agents" category established (Feb 2026,
    inaugural).** Explicitly calls for "independent guardian agent layers
    that work across clouds and platforms" — this IS the RHOAI
    positioning. AX (Agent Experience) appears in Platform Engineering
    Hype Cycle (13).
29. **Seven new funded entrants ($160M+ total).** Geordie AI, JetStream
    ($34M), Oasis Security ($120M Series B), AvePoint AgentPulse,
    Kosmoy, Credo AI, Arthur AI. All SaaS, none on-prem — but shaping
    buyer expectations (13).
30. **Solo.io four-project suite.** agentgateway has air-gapped docs;
    agentregistry does not yet. kagent has 300+ contributors from major
    vendors. The OSS alternative is building faster than the RHOAI
    registry (13).
31. **EU AI Act took effect August 2.** Cross-platform agent governance
    is now a compliance requirement. NIST SP 800-53 agent overlays
    targeting Q4 2026 will create procurement requirements (13).
32. **Wedge window narrows to 6-9 months** (from 6-12 in July). The
    on-prem/disconnected gap is unfilled but under pressure from
    Microsoft cross-cloud sync, Google ARD, and Solo.io air-gapped
    momentum (13).

## Boundary notes (siblings)

- The registry-shaped Jira surface (RHAISTRAT-1355, -1697, -1758, -1955,
  -1956, -2019) is filed under agent-interop and cross-listed here via
  `components:` — no re-filing needed.
- "Deploy always registers, reconcile the rest" comes from the catalog
  series (their 04/01) and is adopted by 09's architecture; the deploy
  path is catalog territory, the registration semantics are ours.
- Agentic base images (RHAIRFE-2443/AIPCC) are shared with agent-catalog
  (their supported-images program consumes them; our registry records
  their provenance). Licensing/air-gap depth lives in catalog 04.
- The "catalog is a read-only view of the registry" decision
  ([decision](/components/agent-registry/knowledge/decision-agent-catalog-is-registry-view.md))
  narrows the agent-catalog component's scope to UX/experience, not a
  separate backend.

## Open question status

| Question | Finding | Status |
|---|---|---|
| kagenti integration architecture (pull/push/hybrid) | Moot — kagenti removed; dissolves into Sandbox WATCH + deploy WEBHOOK + sync controller | answered (09) |
| Pre- vs post-deployment relationship | Recommendation: separate entities + hard `version_ref`, LoggedModel as lineage hub; regulators need both views | open — evidence added (09, 10) |
| Lifecycle ↔ governance mapping | Don't map: orthogonal machines, four join points; SUSPENDED missing; verified-naming hazard | open — evidence added (09, 10) |
| Discovery plugin generalization | Unchanged (RFC-0008's typed-source design points the same way) | open |
| Governance integration (multi-track) | AWS approval-workflow precedent; RFC-0008 puts lifecycle stages upstream | open — evidence added (07, 10) |
| Composition graphs | CSA delegation-lineage expectations make it compliance-adjacent, still deferred | open — evidence added (10) |
| Base images: UBI version, product ID | No new external data; two Red Hat shapes coexist | open (07) |
| **Agent versioning (non-deterministic)** | Four-layer model + eval-gated promotion; SemVer does not map; MLflow LoggedModel + Prompt Registry are the reference | **open — evidence added (12)** |
| **Dependency permanence (npm/left-pad)** | OCI digest-pinning + negotiated deprecation; no competitor solves this; differentiator | **open — evidence added (12)** |
| **Visibility scoping (Bazel analogy)** | Three-tier (public/restricted/private) + Bazel deprecation-visibility; TrueFoundry no-list-all | **open — evidence added (12)** |

## Lens gaps

- ~~**competitive not run as a separate lens**~~ — DONE same day
  (2026-08-03), see [13-competitive](13-competitive.md): vendor deltas,
  7 new entrants, analyst coverage, updated wedge assessment.

## Recommended follow-ups (not auto-run)

- **Re-file card verification** (most urgent, from 11): RHAISTRAT-1956
  closed with no successor while RHAIRFE-2388 sits Approved — an owner
  check on the close reason, then a post-kagenti re-file (registry-side
  fetch + JWS verify per 09 §3), is the only path back to
  `verified=true`.
- **1436 schema input before the EA2 freeze** (from 11): runtime
  instance states + SUSPENDED, `version_ref`, risk tier, log refs,
  retention — cheap now, breaking later; the shared author with RFC-0008
  is the channel. **New from 12**: also add four-layer version structure,
  dependency manifest fields, and visibility-scope metadata.
- **Shape RFC-0008 Phase 2**: the agent entity design should be prepared
  as upstream input before Phase 1 review concludes — this is the
  strategy-doc work `strategy/strategy-status.md` has been waiting on.
- **Re-baseline Varsha's proposal** off kagenti onto Sandbox/OpenShell.
- **hub.jira-sweep agent-registry** — the partition still has no stored
  Jira scope of its own.
- **First-registry-view data source decision** — registry work starts
  3.6 EA2, so any earlier view surface needs a product call.
- **hub.strategy agent-registry** — the research series (12 docs across
  two refreshes) is now comprehensive enough to synthesize a living
  strategy doc.
- **Watch list for next refresh**: RFC-0008 PR #26 review state; OpenShell
  Go SDK PR series; Solo.io agentregistry CNCF Sandbox decision (board
  review may have occurred); IBM ACP on-prem port; AWS registry GA +
  pricing (post-Aug-6 namespace migration); Google ARD adoption beyond
  Google; Microsoft cross-cloud sync GA; Forrester ADP Wave Q4 2026;
  NIST SP 800-53 agent overlays (Q4 2026); NIST AI Agent
  Interoperability Profile (Q4 2026).

## Verification

Standard run — no adversarial verification pass. The 2026-07-16 refresh
verified agent-sandbox versions and four load-bearing URLs. The 2026-08-03
requirements + competitive refresh cites primary sources inline for all
graded claims; URLs from the research agents' findings are provided
as-found — primary source verification recommended for any load-bearing
citation before it enters strategy or external-facing documents.
