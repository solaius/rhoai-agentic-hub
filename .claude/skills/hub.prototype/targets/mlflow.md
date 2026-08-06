# Target: mlflow (MLflow fork)

Registry entry: `targets.mlflow` in /conventions/prototype-targets.yaml.
Spec: /docs/superpowers/specs/2026-08-05-mlflow-prototype-target-design.md.
Pilot: components/skills-registry/prototype/skills-registry-mlflow/
(branch `skills-registry-rfc`) — the worked example for everything below.

Effective config (resolve once, from restricted/.env):
- source repo = `MLFLOW_SOURCE_REPO`, empty → `https://github.com/mlflow/mlflow`
- source branch = `MLFLOW_SOURCE_BRANCH`, empty → `master`
- push repo = `MLFLOW_PUSH_REPO` (unset → local-only mode: skip push +
  Pages steps, preview_url falls back to the branch web URL)
- clone dir = `MLFLOW_DIR`, empty → sibling `../mlflow` of the hub repo,
  else `~/code/rh/mlflow`

Remote mapping in the clone: `origin` → source repo, `gitlab` → push repo.

## [T-prereq] Prerequisites (CREATE and VERSION)

1. Clone healthy: dir exists with `.git`, `origin` matches the effective
   source repo, `uv run mlflow --version` succeeds,
   `mlflow/server/js/node_modules/` present. On any miss STOP and point
   at `bash scripts/doctor.sh setup` (section 13).
2. If push repo configured: silent VPN probe
   `curl -sk --connect-timeout 5 -o /dev/null -w '%{http_code}' https://gitlab.cee.redhat.com/api/v4/projects/pedouble%2Fmlflow`
   — on non-200 STOP: connect to the Red Hat VPN.
3. Local demo/visual verification runs through the clone's own
   `.claude/skills/dev-server/` skill — a HARD dependency on Windows.
   Backend `:5000` must be up or the app hangs on a loading skeleton;
   `dev/run-dev-server.sh` rejects `--dev` on Windows; default workers
   crash-loop with WinError 10022 (use `--workers 1`); `uv >= 0.10.12`.
   Read that skill BEFORE starting servers.

## [T-plan] Screen planning (MANDATORY)

No PatternFly here — MLflow's design accuracy rules:

a. Every new screen names an EXISTING MLflow page it mirrors.
   `model-registry`, `prompts`, and `gateway` under
   `mlflow/server/js/src/` are complete worked examples (list + detail +
   create patterns). The grounding step must cite the chosen reference
   screen per new screen.
b. Databricks design-system components only
   (`@databricks/design-system`); respect `componentId` discipline
   (every interactive component gets one, kebab-case, page-prefixed).
c. Prop discovery: the package ships NO `index.d.ts` — read
   `node_modules/@databricks/design-system/dist-types/` for real prop
   types before using a component.
d. Mock data: colocated typed mocks (JSON or TS) with real entity
   names/fields/states from the grounding; session-store pattern for
   cross-page mock state (see the pilot's skills-registry screens).
e. i18n: wrap user-visible strings the way the neighboring pages do
   (react-intl `FormattedMessage`/`defineMessage` patterns).
f. Routing: hash router — register routes exactly as the reference
   screen's section does.

## [T-generate] Generate (in the clone)

a. `git -C <clone> fetch origin && git -C <clone> fetch gitlab` (skip
   gitlab in local-only mode).
b. Base ref: `gitlab/<source branch>` when the push repo is configured
   (it carries the Pages CI commit on top of the source branch — see
   [T-push] sync note), else `origin/<source branch>`.
   `git -C <clone> checkout -b <slug> <base ref>`.
   NEVER switch branches if the clone's working tree is dirty — STOP and
   tell the user what's uncommitted.
c. Composition: when this prototype needs another prototype's screens,
   `git -C <clone> merge <that-branch>` instead of rebuilding; record
   each merged branch in prototype.yaml `composes:`.
d. Write the files per the content plan, mirroring the reference
   screen's file layout (component per file, colocated mocks, barrel
   exports where the neighbors have them).

## [T-verify] Verify (scoped, changed-files-only — non-negotiable)

The base branch carries ~20 pre-existing type errors and prettier is not
uniformly applied in-tree. Verify ONLY what this prototype changed:

a. `cd mlflow/server/js && ./node_modules/.bin/eslint <changed files>`
   — 0 errors. NEVER `npx eslint`: cwd-casing (`F:\Code` vs `F:\code`)
   double-resolves plugins on Windows.
b. Prettier: format ONLY files that were prettier-clean before your
   change (`./node_modules/.bin/prettier --check` each file at the base
   ref first; skip files that were already dirty).
c. Types: `./node_modules/.bin/tsc --noEmit` diff-compared — capture
   errors at the base ref and after your change; the delta must be zero
   new errors.
d. Visual check via the dev-server skill (backend :5000 + frontend
   :3000), drive the new screens in a browser.

## [T-metadata] prototype.yaml values

- `target: mlflow` (REQUIRED — mlflow is not the default target)
- `source_repo:` the push repo URL when configured, else the source repo
- `base:` `<source branch>` (e.g. `page-composer-upstream`)
- `preview_url:` registry `pages_base_url` + `/branch-<branch>/` when
  `pages_base_url` is non-empty; else the branch web URL stand-in
  (`<push repo web url>/-/tree/<branch>`). Upgrade stand-ins once doctor
  section 13f fills `pages_base_url` — hub.sweep flags them.
- `composes:` list of merged prototype branches (omit if none)

## [T-push] Gate execution (clone side)

`git -C <clone> add <files>`, commit with a descriptive message, then
`git -C <clone> push -u gitlab <slug>` (local-only mode: skip push; the
gate records the local branch only).

Pages inheritance note: prototype branches get their `/branch-<slug>/`
preview because `gitlab/<source branch>` carries the `.gitlab-ci.yml`
Pages job. Doctor 13f + the CI-sync note in that file describe how
`gitlab/<source branch>` = `origin/<source branch>` + the CI commit; if
origin moves, re-sync by rebasing the CI commit onto the new
`origin/<source branch>` and force-pushing `gitlab/<source branch>`
(owner action, not this skill).

Snapshots (VERSION step 4): `git -C <clone> branch <slug>-v<N>`, push it
to gitlab, record under `snapshots:` with its `/branch-<slug>-v<N>/`
preview URL.

## [T-report] Report

Print the preview URL; note it goes live when the fork pipeline finishes
(watch: `https://gitlab.cee.redhat.com/pedouble/mlflow/-/pipelines`).
VPN required to view. In local-only mode: report the branch name and how
to demo via the dev-server skill instead.
