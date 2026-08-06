# MLflow as a first-class prototype target — design

**Date:** 2026-08-05
**Status:** Approved (owner rulings 2026-08-05)
**Enhancement:** [#17](https://github.com/solaius/rhoai-agentic-hub/issues/17)
**Builds on:** /docs/superpowers/specs/2026-08-04-uxd-fork-prototyping-design.md
(the single-target UXD-fork model this generalizes)

## Problem

#16 made hub.prototype generate React prototypes in the UXD RHOAI fork.
The 2026-08-05 MLflow pilot (skills-registry RFC-0008 screens in
`pedouble/mlflow`, branch `skills-registry-rfc`) proved the same
grounding-plus-generation flow works in a second, foreign codebase — but
it was hand-orchestrated: no declared target config, no doctor support
for MLflow's environment quirks, no Pages preview, and the codegen
guidance lived only in session memory. Make MLflow a declared,
repeatable prototype target without growing hub.prototype's SKILL.md.

## Owner rulings (2026-08-05)

| # | question | ruling |
|---|---|---|
| R1 | Default base branch for MLflow prototypes | `page-composer-upstream` on the source fork (the pilot's base; carries Page Composer + upstream MCP-registry backend commits). The stated "page-composter-branch" was a typo for this. |
| R2 | Pilot's relation to the fork's existing mcp-registry branches | Study it, build fresh — unless updating a prototype or extending related functionality. Prototypes may compose other prototype branches (merge them in) to make the full picture. |
| R3 | Pages story for the mlflow fork | Per-branch previews, like the UXD RHOAI fork: every pushed prototype branch builds to `/branch-<name>/`. Heavy webpack build accepted. |
| R4 | mcp-registry pilot scope | The pilot is the acceptance run of this machinery, not designed in this spec. Screen design happens interactively inside `hub.prototype create mcp-registry` (grounding + design checkpoints as the skill already does). |
| R5 | Structure | Approach A: target registry yaml + per-target instruction files inside the hub.prototype skill dir. SKILL.md stays the target-agnostic spine. |

## Architecture

One orchestrator, N targets. `hub.prototype` resolves a target early,
then follows that target's instruction file for everything
repo-specific. Two targets exist at ship time: `uxd-rhoai` (default,
behavior unchanged) and `mlflow`.

### Target registry: conventions/prototype-targets.yaml

`conventions/prototype-fork.yaml` is renamed (git mv) to
`conventions/prototype-targets.yaml`; header comment updated. Shape:

```yaml
targets:
  uxd-rhoai:                     # existing values move here unchanged
    default: true
    upstream_repo: https://gitlab.cee.redhat.com/uxd/prototypes/rhoai
    upstream_project_id: 155361
    fork_repo: git@gitlab.cee.redhat.com:pedouble/rhoai.git
    fork_project_path: pedouble/rhoai
    base_branch: "3.6"
    pages_base_url: "https://rhoai-a4b259.pages.redhat.com"
    clone_dir_env: UXD_FORK_DIR          # restricted/.env override
    instructions: targets/uxd-rhoai.md   # relative to the skill dir
  mlflow:
    source_repo_default: https://github.com/mlflow/mlflow
    source_repo_env: MLFLOW_SOURCE_REPO     # populated → overrides default
    source_branch_env: MLFLOW_SOURCE_BRANCH # base branch on the source repo
    source_branch_default: master
    push_repo_env: MLFLOW_PUSH_REPO         # where finished branches go
    push_project_path: pedouble/mlflow
    pages_base_url: ""                      # discovered by doctor 13f, committed when known
    clone_dir_env: MLFLOW_DIR               # default: sibling dir ../mlflow
    instructions: targets/mlflow.md
```

Anything referencing `prototype-fork.yaml` (hub.prototype SKILL.md,
doctor section 12, docs) is updated to the new path and nested shape.

### Environment variables (restricted/.env + restricted/.env.example)

New "MLflow prototyping" section in `restricted/.env.example`
(suggested values shown, matching the file's existing style) and real
values in the owner's `restricted/.env`:

| var | owner value | empty/unset fallback | meaning |
|---|---|---|---|
| `MLFLOW_SOURCE_REPO` | `https://github.com/DaoDaoNoCode/mlflow` | `https://github.com/mlflow/mlflow` | source fork to clone/ground against (`origin` remote) |
| `MLFLOW_SOURCE_BRANCH` | `page-composer-upstream` | `master` | base branch prototypes branch from |
| `MLFLOW_PUSH_REPO` | `https://gitlab.cee.redhat.com/pedouble/mlflow/` | — (push/Pages features skipped if unset) | push target for completed prototype branches (`gitlab` remote); its Pages hosts previews |
| `MLFLOW_DIR` | unset | `<hub parent>/mlflow`, else `~/code/rh/mlflow` | clone location override |

Clone remote mapping: `origin` → source repo, `gitlab` → push repo.
(The existing clone at `F:/code/rh/mlflow` already has exactly this
shape.) These names appear in a tracked example file in a public repo —
same exposure level as the fork paths already tracked in
`prototype-targets.yaml`; accepted.

### hub.prototype restructure

SKILL.md keeps the target-agnostic spine:

- subcommand dispatch (create / version / list)
- **new: target resolution** — read `prototype-targets.yaml`; if the
  component's existing `prototype.yaml` files declare a `target:`,
  default to that; else the registry's `default: true` entry
  (`uxd-rhoai`). The user can name a target explicitly ("prototype X in
  mlflow"). Once resolved, read `targets/<id>.md` and follow it for
  every target-specific step.
- context load (knowledge, research, strategy, related, Jira, upstream
  repos, existing prototypes, restricted)
- scope, slug, architecture-grounding checkpoint, design decisions
- the two-part gate (target repo + hub), prototype.yaml, reindex, report

Target instruction files live in the skill dir
(`.claude/skills/hub.prototype/targets/`):

- **targets/uxd-rhoai.md** — pure extraction of today's fork-specific
  content: step 0 prerequisites (VPN probe, PatternFly MCP, fork
  readiness), branch mechanics off `upstream/3.6`, PF component
  planning + MCP queries, fork idioms (`src/app/AIHub/` patterns),
  `.design/` recording, eslint/build verification, Pages preview
  semantics. No behavior change.
- **targets/mlflow.md** — the MLflow flow:
  - *Prerequisites*: clone healthy per doctor section 13 (point at
    `bash scripts/doctor.sh setup` on any miss). Local demo/visual
    verification uses the repo-local `dev-server` skill
    (`<clone>/.claude/skills/dev-server/`) — a HARD dependency on
    Windows (backend `:5000` must be up or the app hangs on a loading
    skeleton; `dev/run-dev-server.sh` rejects `--dev`; default workers
    crash-loop with WinError 10022; `--workers 1`).
  - *Branching*: `git fetch origin`, branch off
    `origin/<MLFLOW_SOURCE_BRANCH>`, push to the `gitlab` remote.
  - *Composition* (R2): when a prototype needs another prototype's
    screens, merge that branch in rather than rebuild; record as
    `composes: [<branch>, ...]` in prototype.yaml.
  - *Codegen guidance* (pilot learnings): mirror in-repo idioms —
    `model-registry`, `prompts`, `gateway` are complete worked
    examples; Databricks design-system components only, `componentId`
    discipline; prop discovery via
    `@databricks/design-system/dist-types` (no `index.d.ts`);
    colocated typed mocks; session-store pattern for cross-page mock
    state; hash-route registration; i18n message patterns as
    neighboring pages do. The law of this file: same standards and
    styling as existing MLflow pages — the grounding step must cite
    which existing MLflow page each new screen mirrors.
  - *Verification (scoped, changed-files-only)*: the base branch
    carries ~20 pre-existing type errors and prettier is not uniformly
    applied in-tree, so verify only what changed —
    `./node_modules/.bin/eslint` (never `npx`; `F:\Code` vs `F:\code`
    cwd-casing double-resolves plugins), prettier only on files that
    were clean before, tsc scoped or diff-compared against the base
    branch's error set, frontend build passes.
  - *Design accuracy analog*: no PatternFly MCP here; instead a
    mandatory read of the design-system types plus a named existing
    screen per new screen.

### Doctor: section [13] MLflow prototyping

Mirrors section 12's check/setup split (check = read-only, setup =
writes). VPN probe gates only the gitlab-side checks (13b's gitlab
remote reachability, 13f); GitHub-side checks always run.

- **13a. Clone.** Resolve dir: `MLFLOW_DIR`, else `<hub parent>/mlflow`
  (sibling of this repo), else `~/code/rh/mlflow`. Missing + setup →
  `git clone <effective source repo>` then
  `git checkout <effective source branch>`. NEVER touches an existing
  clone's checked-out branch or working tree (the clone may hold
  uncommitted prototype work).
- **13b. Remotes.** `origin` must match the effective source repo
  (warn on mismatch); `gitlab` remote must point at `MLFLOW_PUSH_REPO`
  — setup adds it when missing (skip with a note if the var is unset).
- **13c. Toolchain + prepare.** `uv >= 0.10.12` (older uv fails on
  `uv.lock`; hint `uv self update`), node present, `yarn` resolvable
  (setup: `corepack enable --install-directory ~/.local/bin`). Setup
  runs `uv sync` at the repo root and `yarn install` in
  `mlflow/server/js` when `node_modules` is missing (~580 MB; noted in
  output).
- **13d. Ready probe.** Non-blocking: `uv run mlflow --version`
  succeeds and `mlflow/server/js/node_modules` exists → "ready for
  use". Doctor does NOT boot the dev servers — that is the dev-server
  skill's job at prototype time.
- **13e. Session wiring.** Add the clone to `additionalDirectories`
  in `.claude/settings.local.json` (same mechanism as 12d).
- **13f. Pages.** With `GITLAB_CEE_TOKEN`: discover the
  `pedouble/mlflow` Pages base URL via the GitLab API and prompt to
  commit it into `prototype-targets.yaml` (same flow as 12e).

### Pages CI job (in the mlflow fork)

Authored once and committed to the `page-composer-upstream` branch on
the gitlab fork, so every prototype branch created from it inherits the
pipeline. Mirrors the UXD fork's `.gitlab-ci.yml` pattern: a `pages`
job that builds the frontend statically (`yarn build`, mock-backed,
hash routing, `publicPath` set for the path prefix) and deploys with
GitLab parallel Pages deployments,
`path_prefix: branch-$CI_COMMIT_BRANCH` → previews at
`<pages_base_url>/branch-<slug>/#/...`. Only the prototyped section is
mock-backed; the rest of the app degrades to empty/error states, so
share links point at the prototyped route. The UXD fork's actual CI
file is the proven reference — if cee GitLab's parallel-deployment
mechanics differ from the above sketch, copy what that file does.
Previews are internal-only (Red Hat network), same stance as the UXD
target.

### prototype.yaml v2 additions

Two optional fields; existing files stay valid:

- `target: <id>` — absent means `uxd-rhoai` (no edits needed to
  existing UXD files).
- `composes: [<branch>, ...]` — other prototype branches merged in.

`preview_url` semantics formalized: with a Pages base URL,
`<pages_base_url>/branch-<slug>/#/<entry-route>`; until Pages is live
for a target, the branch web URL stands in (the pilot's current value).
targets/mlflow.md notes to upgrade stand-in URLs when 13f lands.

Migration: the pilot's
`components/skills-registry/prototype/skills-registry-mlflow/prototype.yaml`
gets `target: mlflow` and its `base:` corrected to the registry's
effective source branch reference.

## Documentation sweep

- `docs/skills.md` — hub.prototype's target model + the mlflow target
- `docs/capabilities.md` — prototyping capability is now multi-target
- `conventions/layout.md` — prototype.yaml v2 additions
- `docs/setup.md` — new env vars + doctor section 13
- `docs/mcp-servers.md` — no new MCP servers; no change expected
- `AGENTS.md` — hub.prototype row wording (multi-target)
- References to `prototype-fork.yaml` updated everywhere

## Error handling

- Every target-file prerequisite failure points at
  `bash scripts/doctor.sh setup`.
- VPN-gated steps degrade like section 12: warn + skip, never fail the
  whole doctor run.
- Doctor never mutates a dirty clone (no checkout, reset, or pull on an
  existing clone).
- The two-part gate is unchanged: nothing committed or pushed in either
  repo before user approval.
- `MLFLOW_PUSH_REPO` unset: create/version still work locally
  (grounding, codegen, local verification); push and Pages steps are
  skipped with a note.

## Verification / acceptance

- `bash scripts/doctor.sh check` and `setup` pass on the owner machine,
  including clone-if-missing + prepare on a machine without the clone.
- `python -m pytest scripts/tests -v`, `python scripts/hub_lint.py`,
  `python scripts/hub_index.py --check` stay green.
- **Pilot (R4)**: `hub.prototype create mcp-registry` runs end-to-end
  on the mlflow target — grounded in the hub's mcp-registry knowledge
  AND the fork's mcp-registry branches (`mcp-registry`,
  `mcp-registry-ui`, `mcp-registry-api-client-layer-and-types`, the
  backend commits already on `page-composer-upstream`), screens styled
  as existing MLflow pages, built fresh on a new branch off
  `page-composer-upstream`.
- A pushed branch yields a working `/branch-<slug>/` Pages preview,
  recorded in prototype.yaml.
- VERSION works against the pilot prototype.
- UXD regression: the uxd-rhoai target file read-through reproduces
  today's behavior; an existing UXD prototype lists/versions unchanged.

## Out of scope

- Changing the UXD-fork flow (it stays the default target).
- Designing the mcp-registry pilot's screens (R4 — decided
  interactively during the pilot run).
- Public publishing of MLflow previews (internal-only, like UXD).
- A generic N-target framework beyond the two declared targets
  (approach B was rejected as YAGNI).
