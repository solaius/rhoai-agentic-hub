---
name: hub.prototype
description: Create, version, or list UI prototypes for a component or across components. Generates React + PatternFly 6 pages in the UXD RHOAI fork (branch per prototype, live GitLab Pages preview), grounded in the component's real architecture, knowledge, and upstream repos. Use when the user says "prototype", "mockup", "UI prototype", "create a prototype for <component>", "new version of the prototype", "list prototypes", or "prototype the <feature>".
---

# hub.prototype

Input: a subcommand (`create`, `version`, `list`) plus a component id
and/or slug. Default subcommand: `create`.

Spec: /docs/superpowers/specs/2026-08-04-uxd-fork-prototyping-design.md
(owner rulings R1-R6). Fork config: /conventions/prototype-fork.yaml.
Structure: /conventions/layout.md (prototype/ leg, prototype.yaml v2).

Prototypes are internal-only (fork GitLab Pages, Red Hat network). There
is no publish mode: the preview URL is the shareable artifact. The fork's
manual whole-app public deploy exists but is owner-only and NEVER fired
by this skill (ruling R4).

## Step 0: Prerequisites (CREATE and VERSION)

1. **VPN probe (automatic, silent).** Run
   `curl -sk --connect-timeout 5 -o /dev/null -w '%{http_code}' https://gitlab.cee.redhat.com/api/v4/projects/155361`.
   On `200`, proceed silently -- no output, no question. Otherwise STOP:
   > Can't reach gitlab.cee.redhat.com -- make sure you're connected to
   > the Red Hat VPN.
2. **PatternFly MCP.** Call `searchPatternFlyDocs` with
   `searchQuery: "button"`, `version: "v6"`. On failure STOP and point at
   `bash scripts/doctor.sh setup` + /docs/mcp-servers.md.
3. **Fork ready.** Read `conventions/prototype-fork.yaml`. Resolve the
   clone dir (UXD_FORK_DIR from restricted/.env, else `F:/code/rh/rhoai`,
   else `~/code/rh/rhoai`). Verify: clone exists, `git -C <fork> remote
   get-url upstream` works, `node_modules/` present, `pages_base_url`
   non-empty. On any miss STOP and point at
   `bash scripts/doctor.sh setup` (section 12).

Skip Step 0 for LIST.

## Subcommand dispatch

| invocation pattern | mode |
|---|---|
| `hub.prototype create <component>` | CREATE |
| `hub.prototype <component>` (no subcommand) | CREATE (default) |
| `hub.prototype version <component>/<slug>` | VERSION |
| `hub.prototype list [<component>]` | LIST |

Cross-component prototypes: use `narrative` as the component id; metadata
lands in `narrative/prototype/<slug>/`.

## LIST

Read `views/prototypes.md`, display (filtered to the component if given).
Done.

## CREATE

### Step 1: Context load

Unchanged from the original skill: resolve the component id against
`components/components.yaml` (offer `hub.intake` and stop if unknown),
then deep-read, skipping what does not exist:

a. Knowledge entries (`components/<id>/knowledge/` -- decisions, refs,
   facts; architecture and upstream-repo refs first).
b. Research series (`research/00-executive-summary.md` + relevant lenses).
c. Strategy doc (`strategy/strategy.md`).
d. Related components (via `related:` in components.yaml -- their
   knowledge index, research summary, strategy).
e. Jira scope (`work/jira-snapshot.yaml`, stored JQL).
f. Upstream repos (ref- entries pointing at GitHub/GitLab -- real UI
   patterns, data models, API shapes).
g. Existing prototypes (prototype.yaml files here and in related
   components; open their preview URLs for continuity).
h. Restricted context (if `restricted/` exists locally -- informs design,
   NEVER surfaces in output; the fork branch is internal but the hub repo
   is PUBLIC).
i. Fork design context: the fork's `.design/features/` for the closest
   feature area, plus `.agents/rules/design-guidelines.md`.

### Step 2: Scope

Summarize the most design-relevant findings (2-5 sentences), then ask
what to prototype. Accept a description, a Jira key, a knowledge entry
reference, a Figma link/screenshot, or "the whole thing".

### Step 3: Slug

Derive a kebab-case slug (e.g. `registry-ui`). It becomes BOTH the hub
metadata dir (`components/<id>/prototype/<slug>/`) and the fork branch
name. If a branch of that name already exists in the fork, prefix the
component id. Confirm with the user.

### Step 4: Architecture grounding

Brief shown to the user (not a file): real data model (entities, fields,
states), real API surface / interaction patterns, design constraints from
strategy/decisions, and an explicit grounded-vs-invented split. User
confirms BEFORE any code. Mandatory checkpoint.

### Step 5: Design decisions

If layout/interaction choices exist, surface 2-3 options referencing the
grounding; user picks. Skip (say why) if the scope prescribes the answer.

### Step 6: Component planning (MANDATORY)

a. List every PatternFly component the page(s) will use.
b. Query the PatternFly MCP for each: `searchPatternFlyDocs(searchQuery,
   version: "v6")` then `usePatternFlyDocs(name, version: "v6")` --
   React docs apply directly now.
c. Map the plan to the fork's existing idioms -- reuse patterns from
   `src/app/AIHub/` (AgentCatalog's Gallery grid, MCPCatalog's
   Sidebar filter rail, *WithTabs wrappers, `isTabContent` dual-mode).
d. Honor the fork's rules: PatternFly components only, semantic design
   tokens, unique kebab-case page-prefixed `id`s, WCAG 2.1 AA, no custom
   CSS on PF components.
e. Produce a content plan: which files under `src/app/<Area>/<Feature>/`
   (page components, colocated typed mock data, barrel index.ts), the
   route path(s), and the nav placement. User confirms.

### Step 7: Generate (in the fork)

a. `git -C <fork> fetch upstream`
b. `git -C <fork> checkout -b <slug> upstream/3.6`
c. Write the files from the content plan. Mock data uses real entity
   names/fields/states from the grounding -- no lorem ipsum. Follow fork
   code style: TS strict, `import * as React from 'react'`, members
   inside one import alphabetized, `_`-prefixed unused params.
d. Wire the route: `src/app/routes.tsx` import + route object entry
   (label to appear in nav; omit label for detail routes). If the page
   lives under AI hub, ALSO wire `filterAIHubRoutes` in
   `src/app/AppLayout/AppLayout.tsx` (it rebuilds the AI hub nav at
   runtime) and re-export the component through the routes barrel.
e. Record design context per fork convention: check
   `.design/feature-mapping.md`; add/extend the matching
   `.design/features/<area>/design-history.md` with a dated entry.

### Step 8: Verify (non-negotiable)

a. `npx eslint <changed files> --no-warn` -- 0 errors (use
   `--fix` first for import sorting).
b. `npm run build` -- passes.
c. Optional: `npm run start:dev` (port 9000) + Playwright/browser visual
   check; the fork's `check-patternfly-compliance` and `review-design`
   skills as extra review passes.

### Step 9: Metadata (in the hub)

Write `components/<id>/prototype/<slug>/prototype.yaml`:

```yaml
title: <title>
description: <one line>
status: active
components: [<id>]
source_repo: git@gitlab.cee.redhat.com:pedouble/rhoai.git
branch: <slug>
base: upstream/3.6
preview_url: <pages_base_url>/branch-<slug>/
current: v1
versions:
  v1: {timestamp: <today>, commit: <sha after the fork commit>, summary: <one line>}
```

`preview_url` = `pages_base_url` from conventions/prototype-fork.yaml +
`/branch-<branch>/`.

### Step 10: Gate (two-part, one confirm)

Show: fork branch name, files created/changed, eslint/build results, the
prototype.yaml content, and the computed preview URL. On OK:
a. Fork: `git -C <fork> add <files>` then commit with a descriptive
   message, then `git -C <fork> push -u origin <slug>`.
b. Hub: fill `commit:` with the fork sha, then stage the prototype dir +
   regenerated indexes (Step 11) and commit with pathspecs
   (`proto(<id>): <slug> v1`).
On reject: discard both sides, ask what to change.

### Step 11: Reindex

`python scripts/hub_index.py` then `python scripts/hub_lint.py` (0
errors). Stage `components/<id>/prototype/<slug>/`, the component
`index.md`, `components/index.md`, `views/prototypes.md` -- never
`git add -A`.

### Step 12: Report

Print the preview URL and note it goes live when the fork pipeline
finishes (watch: `<fork web url>/-/pipelines`). VPN required to view.
No publish offer -- there is nothing to publish.

## VERSION

Input: `<component>/<slug>`.

1. Read `components/<id>/prototype/<slug>/prototype.yaml` (error +
   suggest `create` if missing).
2. Context: re-run the deltas of CREATE step 1 (what changed in
   knowledge/strategy/Jira since the last version) plus the user's
   feedback. Show a brief; user confirms.
3. In the fork: `git -C <fork> checkout <branch>`; iterate; re-verify
   (CREATE step 8).
4. Snapshot on request: if the user wants the CURRENT state kept
   viewable side by side, first `git -C <fork> branch <slug>-v<N>` (the
   old version) and push it; record under `snapshots:` with its own
   `/branch-<slug>-v<N>/` preview URL.
5. Gate (same two-part shape): fork commit+push; hub prototype.yaml gets
   a new `versions:` entry (sha, date, summary), `current:` bumped.
6. Reindex + report preview URL (redeploys automatically on push).

## Upstreaming (manual, opportunistic -- ruling R5)

Not a subcommand. When a design earns a place in the canonical UXD
prototype, run the fork's own `prepare-merge-request` skill from the fork
(branches base off upstream/3.6, so fork-local divergences never ride
along), then record the MR URL in prototype.yaml `mr_url:` through the
normal gate.

## Key principles

1. **Grounded, not invented.** The context load exists so the prototype
   reflects reality -- real entity names, states, navigation.
2. **PatternFly accuracy is mandatory.** Step 6 queries the MCP for every
   component; the fork's design rules are law.
3. **Real app, real chrome.** The fork provides the actual RHOAI shell,
   nav, and components -- never hand-approximate them.
4. **Branch per prototype, off upstream/3.6.** Keeps previews isolated
   and upstream MRs clean by construction.
5. **Internal-only.** Preview URLs are the artifact; no public mirror
   from this skill, ever.
6. **The gate is sacred.** Nothing is committed or pushed -- in either
   repo -- before the user approves.
