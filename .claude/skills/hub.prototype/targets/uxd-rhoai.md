# Target: uxd-rhoai (UXD RHOAI fork — default)

Registry entry: `targets.uxd-rhoai` in /conventions/prototype-targets.yaml.
Spec: /docs/superpowers/specs/2026-08-04-uxd-fork-prototyping-design.md
(owner rulings R1-R6). Prototypes are internal-only (fork GitLab Pages,
Red Hat network). The fork's manual whole-app public deploy exists but is
owner-only and NEVER fired by this skill (ruling R4).

## [T-prereq] Prerequisites (CREATE and VERSION)

1. **VPN probe (automatic, silent).** Run
   `curl -sk --connect-timeout 5 -o /dev/null -w '%{http_code}' https://gitlab.cee.redhat.com/api/v4/projects/155361`.
   On `200`, proceed silently -- no output, no question. Otherwise STOP:
   > Can't reach gitlab.cee.redhat.com -- make sure you're connected to
   > the Red Hat VPN.
2. **PatternFly MCP.** Call `searchPatternFlyDocs` with
   `searchQuery: "button"`, `version: "v6"`. On failure STOP and point at
   `bash scripts/doctor.sh setup` + /docs/mcp-servers.md.
3. **Fork ready.** Resolve the clone dir (UXD_FORK_DIR from
   restricted/.env, else `F:/code/rh/rhoai`, else `~/code/rh/rhoai`).
   Verify: clone exists, `git -C <fork> remote get-url upstream` works,
   `node_modules/` present, the registry's `pages_base_url` non-empty.
   On any miss STOP and point at `bash scripts/doctor.sh setup`
   (section 12).

## [T-plan] Component planning (MANDATORY)

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

Fork design context for the grounding step: the fork's
`.design/features/` for the closest feature area, plus
`.agents/rules/design-guidelines.md`.

## [T-generate] Generate (in the fork)

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

## [T-verify] Verify (non-negotiable)

a. `npx eslint <changed files> --no-warn` -- 0 errors (use
   `--fix` first for import sorting).
b. `npm run build` -- passes.
c. Optional: `npm run start:dev` (port 9000) + Playwright/browser visual
   check; the fork's `check-patternfly-compliance` and `review-design`
   skills as extra review passes.

## [T-metadata] prototype.yaml values

- `source_repo: git@gitlab.cee.redhat.com:pedouble/rhoai.git`
- `base: upstream/3.6`
- `preview_url` = registry `pages_base_url` + `/branch-<branch>/`
- `target:` may be omitted (uxd-rhoai is the default).

## [T-push] Gate execution (fork side)

`git -C <fork> add <files>`, commit with a descriptive message, then
`git -C <fork> push -u origin <slug>`.
Snapshots (VERSION step 4): `git -C <fork> branch <slug>-v<N>` (the old
version), push it, record under `snapshots:` with its own
`/branch-<slug>-v<N>/` preview URL.

## [T-report] Report

Print the preview URL and note it goes live when the fork pipeline
finishes (watch: `<fork web url>/-/pipelines`). VPN required to view.
No publish offer -- there is nothing to publish.

## Upstreaming (manual, opportunistic -- ruling R5)

Not a subcommand. When a design earns a place in the canonical UXD
prototype, run the fork's own `prepare-merge-request` skill from the fork
(branches base off upstream/3.6, so fork-local divergences never ride
along), then record the MR URL in prototype.yaml `mr_url:` through the
normal gate.
