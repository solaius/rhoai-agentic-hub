# Component hub build-out, umbrella devolution, and the internal publish target - design spec

- **Date:** 2026-07-11 · **Owner:** Peter Double · **Status:** approved design,
  pre-implementation
- **Closes:** enhancements backlog #35 (component hub build-out + Management
  umbrella devolution, full plan A+B) and #13 in its interim form (`audience:
  internal` publish target; the protected-GitLab tail stays open).
- **Supersedes in part:** the publish placement in
  [/features/mcp-ecosystem/work/management-hub-umbrella-plan.md](/features/mcp-ecosystem/work/management-hub-umbrella-plan.md)
  (hubs are now internal-audience, not public); its devolution map and
  sequenced build plan are adopted unchanged and detailed here.

## Problem

Enhancement #35 (owner ruling 2026-07-10) commits to dedicated knowledge hubs
for the MCP Catalog, MCP Lifecycle Operator (MCPLO), and MCP Registry, with
the Management hub thinning to a cross-component umbrella. The slugs are
pre-staged as coming-soon in the Management hub's HUB_NETWORK; the devolution
map and 7-step sequenced plan are recorded. Three things have changed or
crystallized since the ruling:

1. **Audience (owner ruling 2026-07-11, this design session):** knowledge
   hubs do not belong on the public pages site. The two already published
   (RHCL/Gateway hub at `mcp-gateway/rhcl/`, Management hub at
   `mcp-ecosystem/hub/`) come off it, and the three new hubs never go there.
   They are viewed from THIS repo's GitHub Pages for now, moving to protected
   GitLab Pages later. That means implementing backlog #13 (`audience:
   internal`, schema-reserved since v1) now, in interim form.
2. **Standard hub sections (owner ruling, this session):** every knowledge
   hub gains a Jobs to be Done page (Understand section) and a Jira Tracker
   page (Plan section, RHAISTRAT issues only), and `hub.refresh-site` is
   extended to build and maintain both as part of its contract.
3. **Fresh facts:** the 2026-07-10/11 Registry/Catalog re-plan and the
   2026-07-11 MCPLO roadmap enrichment postdate parts of the parent-hub
   content that seeds the new hubs. A contradiction checklist (below) must be
   burned down during authoring, not inherited.

## Decisions already made (do not re-litigate)

- **Full plan (A+B):** all 7 steps of the recorded sequenced plan, including
  the umbrella IA restructure, in this effort.
- **Approach A, per-component increments:** each component hub is built,
  published, and its launch conversion (parent thinning + link flips) done in
  the same increment. No wave of unthinned parents; the duplication window
  per component is one increment.
- **Build order:** Catalog, then MCPLO, then Registry (owner ruling
  2026-07-10, unchanged).
- **Internal hosting, interim:** this repo's GitHub Pages (`gh-pages`
  branch). Accepted caveat: the repo is public, so until GitLab this is
  reduced discoverability, not access control. Hub sources stay in the
  public tree and keep following public-tree sanitization rules.
- **Skill:** `hub.refresh-site` (not a new skill) gains the JTBD and Jira
  Tracker section contracts.
- **features.yaml:** checked 2026-07-11, all 12 partitions routed; no
  routing additions needed. It DOES need `jira:` scope blocks added for
  `mcp-catalog` and `mcp-gateway` so their tracker pages have stored scopes
  (see Jira Tracker below).

## Target topology

| Hub | Source (repo) | Published dest (internal target) | Role after this effort |
|---|---|---|---|
| Management (umbrella) | `features/mcp-ecosystem/enablement/management-hub/` | `mcp-ecosystem/hub/` | Cross-component story, ~12-14 pages, links out to component hubs |
| Gateway | `features/mcp-gateway/enablement/rhcl-hub/` | `mcp-gateway/rhcl/` | Unchanged role; govern component pages thinned to gateway-vantage summaries; gains HUB_NETWORK |
| Catalog (new) | `features/mcp-catalog/enablement/catalog-hub/` | `mcp-catalog/hub/` | Component depth: discovery/storefront |
| MCPLO (new) | `features/mcp-lifecycle-operator/enablement/mcplo-hub/` | `mcp-lifecycle-operator/hub/` | Component depth: deployment/lifecycle operator |
| Registry (new) | `features/mcp-registry/enablement/registry-hub/` | `mcp-registry/hub/` | Component depth: governance/system-of-record; launches lean, grows toward 3.6 EA1 |

Dest slugs are contracts and match the coming-soon paths already staged in
the Management HUB_NETWORK. Each hub is self-contained (own `nav.js`,
`styles.css`, adapted from the Management hub's) with its own SITE_MAP and
the shared five-entry HUB_NETWORK block. Because the internal target
preserves the same dest layout, all existing `../../<feature>/<dest>/`
cross-hub links keep working unmodified, both now and after a GitLab move.

## Publish layer: `audience: internal` (#13 interim)

One manifest, two targets:

- `audience: public` - unchanged: `publish.yml` pushes to
  `solaius/rhoai-agentic-hub-pages`; public landing regenerated from public
  entries only.
- `audience: internal` - new: the same publish run pushes internal artifacts
  to this repo's `gh-pages` branch, same dest-slug layout, its own generated
  landing page (clearly labeled internal). Viewable at
  `https://solaius.github.io/rhoai-agentic-hub/`. Push uses the workflow's
  own GITHUB_TOKEN (no cross-repo PAT). GitHub Pages must be enabled on the
  repo (Settings, or `gh api`), serving the `gh-pages` branch root.

Mechanics:

- `hub_publish.py` routes entries by audience; each target gets its own
  snapshot (`.publish-snapshot.json` stays public's; internal gets
  `.publish-snapshot-internal.json`, same v2 schema) so NEW/UPDATED badges
  work per target and neither side sees phantom changes.
- The two live hub entries flip `audience: public` to `internal`. Existing
  removal mechanics then clean the public site on the next publish run
  (absent-from-target means removed), and the public landing regenerates
  without hub cards. Already-published copies remain in the pages repo's git
  history: accepted residue, that content was sanitized for public when it
  shipped.
- Three new hubs enter the manifest as `audience: internal` from day one.
  Everything else public today (decks, blog previews, registry UI prototype)
  stays public.
- **Cross-boundary link rule** (settles #13's open design question):
  internal pages may link to public artifacts freely; public artifacts must
  not link into internal dests. `hub_lint.py` gains a check that scans
  public-audience sources for links into internal dest paths. Any existing
  public-to-hub links found get fixed in increment 0.
- `conventions/publishing.md` updated to the two-target contract (replacing
  the "v1 publishes public only" sentence) and documents the interim
  caveat. `hub.publish` offers the audience choice explicitly; audience
  flips are gated in both directions (public-to-internal is a retraction,
  internal-to-public is a disclosure).

## The three hubs, page by page

Family skeleton: Home (`index.html`), Quick Reference (`reference.html`),
sections Understand / Sell / Build / Govern / Plan. Two standard pages in
every hub: Jobs to be Done (Understand) and Jira Tracker (Plan). Page names
directional; exact titles may shift during authoring.

**Catalog hub, 14 pages** (seed: RHCL `govern/catalog.html` is ~90% moves;
the Catalog card in Management `component-overview.html`; the mcp-catalog
partition: 3 facts + 3 questions + 2-lens research):

| Section | Pages |
|---|---|
| Understand | What Is the MCP Catalog · Jobs to be Done · Upstream & Ecosystem (kubeflow/hub code upstream, model-metadata-collection content upstream, official registry / AAIF posture) |
| Sell | Positioning & Trust Tiers · Competitive Landscape (the 12-entry catalog/registry table plus the July 2026 refresh: Docker OCI, Databricks Unity, ToolHive coopetition, new entrants) |
| Build | Bring Your Own MCP Server (packaging checklist, catalog-yaml spec, SCC table) · Enablement & Troubleshooting (mcpCatalog patch, prereq ConfigMap issues) |
| Govern | Partner Onboarding Pipeline (6 steps, technical requirements, consent/attestation) · Trust & Policy (RBAC/approval, federation posture) |
| Plan | Roadmap · Jira Tracker (Strats) · Gaps & Open Questions |

**MCPLO hub, 16 pages** (richest seed: RHCL `govern/lifecycle-operator.html`
~95% moves; MCPLO card; install/CRD fragments; full 5-lens research series;
26 knowledge entries):

| Section | Pages |
|---|---|
| Understand | What Is MCPLO (deployment primitive, not governance) · Architecture (three-repo model, CRD to controller to Deployment+Service, DSC module) · Jobs to be Done · Upstream (kubernetes-sigs, RH ~83% of commits, v0.1-to-v0.2 velocity) |
| Sell | Positioning & Competitive (ToolHive/Stacklok, three-tier market) - one page, sell seed is thin |
| Build | Installation (two-tier model, oc apply + DSC paths) · MCPServer CRD Reference · Supported Servers & Troubleshooting |
| Govern | Distribution & Entitlement (OCP entitlement, not-in-OperatorHub, update delivery, disconnected) · Qualification & Security (OCP-functional vs RHOAI-deployment split, TLS, NSA/OWASP, stateless spec shift) · Gateway Integration (OCPMCP-347, GA scope) |
| Plan | Roadmap · Jira Tracker (Strats) · Gaps & Open Questions (P0 gaps, maturity L1-2 to L3-4, OLS transition, cluster-admin, OLM removal) |

**Registry hub, 12 pages** (launches as the design-decision record it is;
seed: RHCL `govern/registry.html` ~90% moves; the largest component card;
`govern/lifecycle-flow.html` is near-total Registry; deep ref set; no
research series):

| Section | Pages |
|---|---|
| Understand | What Is the MCP Registry (system of record) · Data Model (MCPServer / MCPServerVersion / MCPObservedTool; current two-enum model vs four-track proposal, explicitly separated) · Jobs to be Done |
| Sell | The Governance Story (vision vs shipped, honestly labeled; anonymized early-access signals) |
| Build | MVP Scope & Prototype (forward-looking: data model, API sketch, link to the public UI prototype) |
| Govern | Lifecycle & Governance (stages, enums, invariants, phasing) · Integrations (Registry-Gateway, Catalog-Registry RHAISTRAT-2027, MCPLO update_mode, MLflow/Databricks RFC) |
| Plan | Roadmap · Jira Tracker (Strats) · Gaps & Open Questions |

### Standard page: Jobs to be Done

Renders every `narrative/knowledge/jtbd-*.md` whose `features:` list
includes the hub's feature id: persona, the When / I want / So I can
statement, evidence status, and how this component addresses the job.
Source entries cited (GitHub blob links are fine, the repo is public). The
RHCL and Management hubs get retrofitted with the same page (increment 5)
so the contract is uniform across all five hubs.

### Standard page: Jira Tracker (Strats)

A static table of RHAISTRAT issues only for the hub's feature: key, type,
public summary, status, fix version, link to issues.redhat.com. Generated
from the feature's stored Jira scope via `hub_jira.py`, honoring the same
unauthenticated-probe visibility rule as the tracked `jira-snapshot.yaml`
files (sources are in the public tree). `data-verified` footer as usual.
The Management hub's existing `plan/jira-tracker.html` becomes the
cross-component Strats outcome rollup (increment 4), same machinery.

Prerequisite: `features.yaml` `jira:` blocks exist for `mcp-registry`,
`mcp-lifecycle-operator`, `agent-interop` only. Add scoped blocks for
`mcp-catalog` (increment 1; seed keys from
`features/mcp-catalog/knowledge/ref-mcp-catalog-strat-jiras.md`:
RHAISTRAT-1339 umbrella, 1084/1306/1149/1859/1994) and `mcp-gateway`
(increment 4; scope discovery during implementation, hub.jira-sweep
conversation shape). The Management rollup derives from the component
scopes plus the RHAISTRAT-1339 parent jql already in
`refresh-management-hub.yaml`.

## Increments

Six increments, each ending in a green publish run and a consistent hub
network. Worst interruption case: a component still marked coming-soon.

- **Increment 0 · Publish layer.** Implement the internal target
  (`hub_publish.py`, `publish.yml`, per-target snapshots, internal landing);
  enable Pages on this repo; flip the two live hub entries to internal
  (public site cleanup happens on the same run); add the public-to-internal
  link lint and fix any offenders; update `conventions/publishing.md`,
  backlog #13 and #35.
- **Increment 1 · Catalog.** Extend `hub.refresh-site` first (JTBD + Jira
  Tracker section contracts, built once here, used by every hub; includes
  the `sections:` config schema). Add the mcp-catalog `jira:` block. Build
  the Catalog hub seeded from BOTH parents in one pass. Publish internal
  (gated). Launch conversion: flip Catalog comingSoon in the Management
  HUB_NETWORK and its coming-soon badges (landing card, component overview,
  reference); thin Management pages for Catalog (component-overview card to
  summary+link; configuration-reference BYO/catalog-yaml out, seam
  artifacts stay; troubleshooting catalog issues; catalog gaps/questions;
  roadmap sub-table to matrix row; competitive: the catalog/registry
  landscape table moves to the Catalog hub, both parents keep a pointer);
  thin RHCL `govern/catalog.html` to a gateway-vantage summary + link; ship
  `features/mcp-catalog/work/refresh-catalog-hub.yaml`.
- **Increment 2 · MCPLO.** Same shape: build, publish, convert. Thins the
  MCPLO card; `operator-installation` (MCPLO install out; two-tier model
  and cross-component version matrix stay); `configuration-reference`
  (MCPServer CRD out; seam artifacts stay); troubleshooting issue #9; MCPLO
  gaps/questions; roadmap sub-table; RHCL `govern/lifecycle-operator.html`
  to summary. Carries the MCPLO roadmap corrections (see checklist) into
  every page it touches. Ships `refresh-mcplo-hub.yaml`.
- **Increment 3 · Registry.** Build (lean), publish, convert. Thins the
  Registry card; `lifecycle-flow` (Registry governance tables out, 7-stage
  flow stays); the Registry open-questions block; registry gaps; roadmap
  sub-table; fixes the "3.5 early access" residue in
  customer-stories/summit-feedback and the four-track-as-shipped error in
  the competitive pages; RHCL `govern/registry.html` to summary. Ships
  `refresh-registry-hub.yaml`.
- **Increment 4 · Umbrella restructure.** Convert component-overview into
  the Component Directory; merge ecosystem-architecture +
  component-integration into one umbrella architecture page; reshape the IA
  to Ecosystem / Components / Choose & Integrate / Sell / Plan & Govern
  with the "which component do I need?" decision guide; add the
  mcp-gateway `jira:` block to features.yaml; rescope the Management
  jira-tracker to the cross-component Strats outcome rollup; rebalance
  `refresh-management-hub.yaml` to the umbrella page set. Management lands
  at ~12-14 pages.
- **Increment 5 · Network pass.** Reciprocal links across all five hubs;
  add HUB_NETWORK to the RHCL hub's `nav.js` (it has none today); retrofit
  Jobs to be Done pages onto the RHCL and Management hubs and a Jira
  Tracker (Strats) page onto the RHCL hub (using the increment-4 gateway
  scope), so all five hubs carry both standard pages; consistency
  sweep of `data-verified` footers; confirm the contradiction checklist is
  burned down; full reindex + lint + publish.

## `hub.refresh-site` extension

Two standard section types, maintained through the existing gated page-diff
flow:

- **JTBD section:** on refresh, re-derive the hub's job set (narrative
  jtbd entries filtered by `features:`), diff against the page (new jobs,
  changed evidence status, removals), propose updates through the gate.
- **Jira Tracker section:** on refresh, re-run the feature's stored scope
  via `hub_jira.py`, filter to RHAISTRAT, regenerate the table, propose the
  diff through the gate. Jira unreachable = no change proposed; the page
  keeps its last `data-verified` date and the staleness indicator surfaces
  it. No partial writes.

Refresh config schema gains an optional `sections:` block, e.g.
`sections: {jtbd: true, jira_tracker: {project: RHAISTRAT}}`. All five hubs
opt in to both. Skill README documents the contract.

### Refresh configs shipped

- `features/mcp-catalog/work/refresh-catalog-hub.yaml`: GDocs (MCP Catalog,
  Partners MCP Catalog), GitHub (kubeflow/hub, model-metadata-collection),
  Jira (catalog scope), Slack (forum-ai-asset-management), local
  knowledge + research.
- `features/mcp-lifecycle-operator/work/refresh-mcplo-hub.yaml`: GDocs
  (MCPLO Weekly Meeting Notes), GitHub (kubernetes-sigs/mcp-lifecycle-operator
  + the opendatahub-io module repo), Jira (stored MCPLO jql), Slack
  (forum-mcp-lifecycle-operator), local knowledge + research.
- `features/mcp-registry/work/refresh-registry-hub.yaml`: GDocs (MCP
  Registry MVP Requirements, MCP Registry Data Model Proposal), Jira
  (stored registry jql), Slack (forum-ai-asset-management), local knowledge.
- `refresh-management-hub.yaml`: rebalanced in increment 4 (component-deep
  local sources hand off to the component configs).

## Authoring inputs: contradiction checklist

Found in the 2026-07-11 seed inventory (parent hubs read in full) plus the
2026-07-11 roadmap enrichment. Each must be resolved in the increment that
touches the content; increment 5 verifies the full list.

1. `sell/competitive.html` (both parents) presents the Registry four-track
   governance model as SHIPPED. Current truth: two enums (MCPServerStatus,
   MCPPublishState) + update_mode; four-track deferred post-MVP; Registry
   not built. Correct to vision-vs-shipped framing.
2. Two-enum (current) vs four-track (proposal) must be explicitly separated
   wherever the data model appears; `fact-mcp-registry-data-model-proposal.md`
   describes the proposal, not the current model.
3. "MCP Registry 3.5 early access" residue in `sell/customer-stories.html`
   and `sell/summit-feedback.html` predates the re-plan (Registry DP misses
   3.5 stable). Fix in increment 3.
4. GA phrasing drift: "Q4 2026" vs "RHOAI 3.6 (code freeze Oct 23 2026)" vs
   "GA 3.6 Stable, Nov 2026". Normalize to the roadmap profile's phrasing.
5. Resolved-question annotations citing "3.5 Dev Preview" scope are
   re-target-in-progress notes (Jira fixversions still being moved to 3.6
   EA1); keep the annotation pattern, verify against live Jira at authoring
   time.
6. Kagenti/AuthBridge claims in sell/security pages are under revalidation
   (OpenShell absorbs; owner ruling 2026-07-10). Do not propagate into new
   hubs; keep the "under revalidation" flag where the content stays.
7. MCPLO entitlement: RHCL `govern/lifecycle-operator.html` says "RHOAI
   restricted-use entitlement required"; roadmap profile (2026-07-11) says
   MCPLO ships with OCP entitlement, RHOAI adds Registry/Authorino/Limitador.
   The new hub carries the corrected fact; the RHCL summary gets it too.
8. MCPLO TP dates: OCP-side TP mid-July 2026 (OCPSTRAT-3263) vs RHOAI TP
   mid-Aug 2026 (RHAISTRAT-1773) is a real distinction the parent pages
   collapse. The MCPLO hub carries both, with the qualification split (OCP
   functional, RHOAI deployment/integration).
9. MCPLO gateway integration is GA scope, not TP (Slack decision May 2026;
   OCPMCP-347). Anywhere TP-era integration is implied, correct it.

## Operational safety

- All hub content stays in the public tree: existing disclosure machinery
  applies unchanged (restricted-pattern lint never bypassed, per
  fact-never-bypass-disclosure-gate; anonymization rules as today; nothing
  from `restricted/`).
- Manifest edits and audience flips go through the hub.publish gate. The
  specific flips and additions in this spec are owner-approved (this design
  session); anything beyond them needs a fresh gate.
- Commit hygiene per fact-concurrent-session-git-hygiene: clean-tree check
  before work, `git diff --cached --stat` before every commit; per-session
  worktree if a concurrent session is suspected.
- `gh-pages` branch is publish-run-generated only, never hand-edited.

## Verification

- Unit tests (in `scripts/tests`, run by `validate.yml`): hub_publish
  audience routing + per-target snapshots; the public-to-internal link lint
  rule; JTBD/tracker generation helpers.
- Per increment: `python scripts/hub_index.py --check`, `python
  scripts/hub_lint.py`, `python -m pytest scripts/tests -v`, a green
  `publish.yml` run, and a manual browse of the affected hub on the
  internal Pages URL.
- Increment 5 sweep: contradiction checklist resolved; `data-verified`
  current on every touched page; all HUB_NETWORK links resolve on the
  internal target; no public artifact links into an internal dest.

## Non-goals

- Protected GitLab Pages hosting (the #13 tail; the internal target is
  designed so only the workflow push destination changes).
- Jira write-backs of any kind (fixversion re-targeting is tracked in Jira,
  not done here).
- New jira scopes beyond the mcp-catalog and mcp-gateway blocks named above.
- Retroactive em-dash cleanup or restyling of untouched pages.
- Purging the already-published hub copies from the pages repo's git
  history (accepted residue, content was public-sanitized).
- Search, FAQ publishing, digest (#21, #12, #23 stay in the backlog).
