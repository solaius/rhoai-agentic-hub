# UXD Fork Prototyping -- hub.prototype Retrofit

**Date:** 2026-08-04
**Status:** Approved (owner rulings 2026-08-04)
**Enhancement:** [#16](https://github.com/solaius/rhoai-agentic-hub/issues/16)
**Supersedes:** P1/P3/P8 of
[/docs/specs/2026-08-02-prototype-system-design.md](/docs/specs/2026-08-02-prototype-system-design.md)
and the entire
[/docs/superpowers/specs/2026-08-03-prototype-template-system-design.md](/docs/superpowers/specs/2026-08-03-prototype-template-system-design.md)

## Problem

The hub's prototypes are self-contained static HTML approximating
PatternFly 6. Even with the template system (shell + patterns extracted
from the UXD repo), the approach has a ceiling: hand-derived HTML, no
real component behavior, no shared app chrome evolution, and no path
into the design/engineering conversation. The template system exists
solely to chase the UXD repo's styling from the outside.

The UXD team's RHOAI prototype repo
(`gitlab.cee.redhat.com/uxd/prototypes/rhoai`, branch `3.6`) IS the
thing being approximated: React 18 + TypeScript + PatternFly 6 +
webpack, the real console masthead/sidebar, per-branch GitLab Pages
previews, and an MR path into the team's canonical prototype. A working
fork exists (`pedouble/rhoai`, local clone `F:\code\rh\rhoai`).

This retrofit keeps what the hub is uniquely good at -- grounding a
prototype in real knowledge, research, strategy, and Jira -- and hands
generation to the fork.

## Owner rulings (2026-08-04)

| # | question | ruling |
|---|---|---|
| R1 | Replace or coexist | **Full replace.** All new prototypes are React pages in the fork. The static pipeline (shell, patterns, extract/build scripts) retires. Already-published static artifacts stay frozen only until their prototype migrates. |
| R2 | Branch model | **Branch per prototype.** One branch per prototype, named after the hub slug (component-prefixed only on collision), each with its own preview at `/branch-<slug>/`. |
| R3 | Versioning | **Commits + snapshot branches.** Versions are commits on the prototype branch, recorded in prototype.yaml; the preview shows the latest. Side-by-side on demand via a frozen `<slug>-vN` snapshot branch (auto-previewed). |
| R4 | Hosting/disclosure | **Internal-only; unpublish on migrate.** Fork GitLab Pages (Red Hat network) is the only hosting. As each static prototype migrates, its manifest entry is removed through the hub.publish gate -- including the public registry-ui entry, after an inbound-link check. Public mirroring is out of scope; the fork's manual whole-app deploy (`npm run deploy` to `solaius/RHOAI`) remains a documented, owner-only escape hatch the skill never fires -- it ships every 3.6 route in the branch, including other designers' unreleased work. |
| R5 | Upstream contribution | **Opportunistic, by hand.** hub.prototype ends at branch pushed + preview URL recorded. Upstreaming is a deliberate follow-up via the fork's `prepare-merge-request` skill; the MR URL is recorded in prototype.yaml. Branches base off `upstream/3.6` so fork-local divergences never ride along. |
| R6 | Execution model | **One session, both repos.** hub.doctor grants the fork as an additional working directory; hub.prototype grounds in the hub, writes/verifies/pushes in the fork, records metadata in the hub -- all in the interactive session with inline gates intact. |

## Architecture

```
rhoai-agentic-hub (this repo)              pedouble/rhoai fork (F:\code\rh\rhoai)
  grounding: knowledge/research/             generation: src/app/<Area>/<Feature>/
    strategy/jira/restricted                 routes.tsx entry + nav link
  metadata: prototype/<slug>/                verification: eslint + npm run build
    prototype.yaml                           preview: push -> CI -> GitLab Pages
  views: views/prototypes.md                   /branch-<slug>/  (VPN-gated)
  gates: inline confirm before any          upstream path: prepare-merge-request
    commit (both repos)                        -> MR to uxd/prototypes/rhoai
```

- The hub never holds generated UI code again; the fork never holds
  grounding or metadata.
- The session works both repos directly (R6). Nothing in the fork is
  committed or pushed without the same inline gate discipline as hub
  writes.

### Branch discipline

- `hub.doctor setup` adds the `upstream` remote
  (`https://gitlab.cee.redhat.com/uxd/prototypes/rhoai.git`).
- Every CREATE starts `git fetch upstream`, then branches from
  `upstream/3.6` (base branch configurable in
  `conventions/prototype-fork.yaml`).
- Basing on `upstream/3.6` -- not the fork's own `3.6` -- keeps the
  fork's committed divergences (the `solaius/RHOAI` package.json
  repository/homepage/deploy edits) out of every prototype branch, so
  an upstream MR is clean by construction (R5). The fork CI's
  `mr-scope-check` remains the backstop.
- Branch previews deploy regardless of base: any branch pushed to the
  fork gets `/branch-<slug>/` on the fork's Pages site.

## VPN preflight (automatic, silent)

`gitlab.cee.redhat.com` and `pages.redhat.com` are reachable only on
the Red Hat network. Every CREATE/VERSION begins with a silent
connectivity probe (short-timeout `curl -sk` against the GitLab API,
or `git ls-remote upstream`). No user prompt, no output on success.
On failure, stop with:

> Can't reach gitlab.cee.redhat.com -- make sure you're connected to
> the Red Hat VPN.

This is distinct from auth failures (missing/invalid token), which get
their own message. hub.doctor runs the same probe first and marks the
network-dependent checks "skipped: VPN" instead of failing them
confusingly.

## The reworked hub.prototype skill

Modes: CREATE (default), VERSION, LIST. PUBLISH mode retires with the
static path (the preview URL is the shareable artifact; R4).

### Step 0: prerequisites

1. Silent VPN probe (above).
2. PatternFly MCP responds (unchanged requirement).
3. Fork ready: clone present, `upstream` remote configured,
   `node_modules` installed. On failure, point at `hub.doctor setup`.

The static-era step 0.5 (shell freshness) is deleted.

### CREATE

Steps 1-5 are unchanged from the current skill: context load
(knowledge, research, strategy, related components, Jira, upstream
repos, existing prototypes, restricted context, UXD design standards),
scope, slug, architecture grounding brief, design decisions.

**Step 6 -- component planning (still mandatory).** PatternFly MCP
queries (`v6`) for every component, but the plan now maps to real
`@patternfly/react-core` components and the fork's existing page
idioms: reuse patterns from `src/app/AIHub/` (MCPCatalog, Models,
Agents) so hub prototypes look native to the app. The plan honors the
fork's design rules (AGENTS.md + `.agents/rules/design-guidelines.md`):
PatternFly components only, semantic design tokens, unique `id`s on PF
components, WCAG 2.1 AA, no custom CSS on PF components. User confirms
the plan before generation.

**Step 7 -- generate.** In the fork:
- `git fetch upstream && git checkout -b <slug> upstream/3.6`
- Write the page component(s) under the fitting `src/app/` area
  (usually `AIHub/<Feature>/`), colocated mock data using real entity
  names/states from the grounding, a `routes.tsx` entry, and a nav
  link so the page is reachable.
- Follow the fork's code style (TS strict, sorted imports, no unused
  vars).

**Step 8 -- verify (the fork's non-negotiable).**
- `npx eslint <changed files> --no-warn` -- 0 errors.
- `npm run build` -- passes.
- Optional passes: the fork's `check-patternfly-compliance` and
  `review-design` skills; Playwright against `npm run start:dev`
  (port 9000) for a visual check.

**Step 9 -- metadata.** Write `prototype.yaml` (v2 schema below) in the
hub under `components/<id>/prototype/<slug>/`. `preview_url` is
computed from `conventions/prototype-fork.yaml` + the branch slug.

**Step 10 -- gate (two-part, one confirm).** Show: fork branch + files
+ verification results, hub prototype.yaml. On OK: commit+push the
fork branch, commit the hub metadata (explicit pathspecs, never
`git add -A`). On reject: discard both.

**Step 11 -- reindex.** `hub_index.py` + `hub_lint.py` as today.

**Step 12 -- report.** Print the preview URL and note it goes live
when the fork pipeline finishes (with where to watch it). No publish
offer.

### VERSION

Checkout the branch, iterate, re-verify (step 8), commit+push --
the preview redeploys automatically. Append a `versions:` entry
(commit, date, summary) and bump `current:` through the gate. On
request, freeze the prior state as a `<slug>-vN` snapshot branch and
record it under `snapshots:` with its own preview URL (R3).

### LIST

Unchanged: render `views/prototypes.md`, optionally filtered.

### Composition with fork skills

hub.prototype orchestrates; it follows the fork's AGENTS.md while
working there and may invoke the fork's skills as review passes. The
`prototype-creator` submodule is NOT adopted as the driver -- it
overlaps the grounding+generation role and the hub's grounding is
richer. Documented as related work; revisit if UXD's pipeline and ours
should converge.

## Setup: hub.doctor "UXD fork prototyping" section

`check` = read-only, `setup` = writes. Ordered so a second person can
follow it cold: clone -> remotes -> toolchain -> session wiring ->
Pages/CI variable -> first branch deploys.

| check | setup action |
|---|---|
| VPN probe (silent) | -- (report "connect to the VPN" and skip network checks) |
| Clone at `UXD_FORK_DIR` (from `restricted/.env`; default probe `F:\code\rh\rhoai`, `~/code/rh/rhoai`) | clone `git@gitlab.cee.redhat.com:pedouble/rhoai.git` |
| `origin` = pedouble/rhoai, `upstream` = uxd/prototypes/rhoai | add missing `upstream`, `git fetch upstream` |
| node >= 18, npm, `node_modules` present | `npm install` (postinstall also inits skill submodules) |
| Fork path in `.claude/settings.local.json` additional working directories | add it (same per-machine pattern as `autoMemoryDirectory`) |
| Fork Pages enabled, `PAGES_URL` CI/CD variable set, Pages domain known | with `GITLAB_CEE_TOKEN` (api scope, `restricted/.env`, optional): verify/enable via API, discover the domain, set the variable. Without it: print the manual UI steps and ask for the resulting URL. NEVER edit `.gitlab-ci.yml`. |
| `conventions/prototype-fork.yaml` consistent with discovered state | write/refresh it |

Doctor also mentions (informational): the optional `GITLAB_API_TOKEN`
CI secret that enables the fork CI's MR-comment features.

### conventions/prototype-fork.yaml (new, tracked)

```yaml
upstream_repo: https://gitlab.cee.redhat.com/uxd/prototypes/rhoai
upstream_project_id: 155361
fork_repo: git@gitlab.cee.redhat.com:pedouble/rhoai.git
base_branch: "3.6"
pages_base_url: https://<fork-pages-domain>   # discovered by doctor
```

One tracked source of truth for computing `preview_url` (hostnames are
not secrets; the hub already tracks `pages.redhat.com` URLs). The
local clone path stays machine-specific in `restricted/.env`
(`UXD_FORK_DIR`).

## prototype.yaml v2 schema

```yaml
title: Skills Catalog UI                    # required
description: one-line                       # required
status: active                              # required: active | superseded | archived
components: [skills-catalog]                # required
source_repo: git@gitlab.cee.redhat.com:pedouble/rhoai.git   # required
branch: skills-catalog-ui                   # required
base: upstream/3.6                          # required
preview_url: https://<pages>/branch-skills-catalog-ui/      # required
current: v2                                 # required: key into versions
versions:                                   # required, each with commit
  v1: {timestamp: 2026-08-03, commit: abc1234, summary: ...}
  v2: {timestamp: 2026-08-05, commit: def5678, summary: ...}
snapshots: {}                               # optional: vN -> {branch, preview_url}
mr_url: null                                # optional: set when upstreamed
```

- The `prototype/` skeleton leg stays; each slug directory holds
  `prototype.yaml` and nothing else.
- Migrated prototypes record their static era as a version entry with
  `commit: static` and a "static era, retired" summary.

### Linter (hub_lint.py / hublib/schema.py)

- Validate the v2 required fields; `status` vocabulary unchanged;
  `current` must be a key of `versions`; every version needs `commit`
  (a sha, or the `static` sentinel on migrated static-era entries).
- Drop: version-directory and `index.html` existence rules.

### Indexer (hub_index.py / hublib/indexer.py)

- `views/prototypes.md` and per-component `index.md` entries link
  `preview_url` (live site), showing branch, current version, status.
- The prototypes-portal.html from the 2026-08-02 spec was never built;
  nothing to change there.

## Retirement scope

Deleted (git history preserves everything):

- `conventions/prototype-shell/` (shell.html, shell.css, nav/,
  patterns/, assets/, extraction-metadata.yaml)
- `scripts/extract_uxd_styles.py`, `scripts/build_prototype.py`, and
  their tests in `scripts/tests/`
- The static CREATE/VERSION machinery in
  `.claude/skills/hub.prototype/SKILL.md` (full rewrite per this spec)

Marked superseded in place (never deleted): the two prior specs, each
gaining a status line pointing here.

`hub_lint.py` must finish with zero references to retired paths.

## Migration

**Pilot: skills-catalog-ui** (freshest grounding, internal-only
manifest entry -- no public moving parts while proving the pipeline):

1. Branch `skills-catalog-ui` off `upstream/3.6`; build the catalog
   page(s) under `src/app/AIHub/` reusing existing idioms.
2. eslint + build green; push; CI green; preview URL loads.
3. prototype.yaml rewritten to v2 (static v1 recorded as retired).
4. Delete the static `v1/` directory.
5. Remove the internal manifest entry via the hub.publish gate.
6. Reindex + lint clean.

This run is the acceptance test for the issue's core criteria.

**Second: registry-ui.** Port vs. fresh rebuild decided at migration
time (it is the older MLflow-style mockup; a fresh grounded rebuild
may serve better). Its PUBLIC manifest entry
(`mcp-registry/ui-prototype/`) comes down through the gate per R4,
after grepping published artifacts for inbound links so nothing public
dangles. Until it migrates, the entry stays frozen.

## Documentation sweep

| file | change |
|---|---|
| `docs/capabilities.md` | prototype capability rewritten (fork-based, internal previews) |
| `docs/skills.md` | hub.prototype section rewritten; PUBLISH mode removed |
| `AGENTS.md` | skills-table wording for hub.prototype |
| `conventions/layout.md` | prototype leg = prototype.yaml only; v2 schema |
| `docs/architecture.md` | skeleton/views wording; drop shell references |
| `docs/tooling.md` | retired scripts out; new lint rules in |
| `docs/setup.md` | fork setup, `UXD_FORK_DIR`, `GITLAB_CEE_TOKEN` (optional pattern) |
| `scripts/doctor.sh` | new fork section per this spec |
| `docs/working-here.md` | filing/daily-loop mentions updated |
| `docs/mcp-servers.md` | no change (no new MCP servers) |

## Verification

- Hub: `python -m pytest scripts/tests -v`,
  `python scripts/hub_lint.py`, `python scripts/hub_index.py --check`
  (CI runs the same three).
- Fork: `npx eslint` 0 errors and `npm run build` passing on every
  prototype branch.
- End to end: pushed branch -> green pipeline -> preview URL loads
  (on VPN), recorded in prototype.yaml, rendered in
  `views/prototypes.md`.
- Doctor: `check` passes on this machine; setup steps followable by a
  second person cold.

## Out of scope

- Enablement decks, blogs, and the publishing pipeline (unchanged).
- Public mirroring of fork prototypes (R4; manual escape hatch only).
- Any edit to the fork's CI/config files (`PAGES_URL` is a CI/CD
  variable, never a file change).
- Adopting the `prototype-creator` submodule as the generation driver.
