---
type: fact
description: MLflow prototyping clone layout -- F:\code\rh\mlflow, push remote 'gitlab' = pedouble/mlflow (gitlab.cee), base branch page-composer-upstream (carries ~20 pre-existing type errors + dirty yarn.lock; scope all verification to changed files); the repo-local .claude/skills/dev-server skill is the required Windows run path
timestamp: 2026-08-05
status: current
---

The MLflow-native prototyping environment used for the skills-registry
RFC-0008 pilot (see
`/components/skills-registry/prototype/skills-registry-mlflow/prototype.yaml`
and enhancement #17):

- Clone: `F:\code\rh\mlflow`. Remotes: `gitlab` =
  `https://gitlab.cee.redhat.com/pedouble/mlflow.git` (the push target;
  https, push with `-c http.sslVerify=false`), `origin` =
  `https://github.com/DaoDaoNoCode/mlflow.git` (upstream-of-the-fork on
  GitHub; the page-composer branches originate there).
- Base branch: `page-composer-upstream`. It is NOT clean: ~20 pre-existing
  type errors and a locally-modified `mlflow/server/js/yarn.lock` plus an
  untracked `.claude/skills/dev-server/`. Never stage those; scope
  type-check/eslint/prettier to changed files only.
- Windows run path: `dev/run-dev-server.sh` does not work on Windows --
  follow the repo-local `.claude/skills/dev-server/SKILL.md` (backend
  uvicorn :5000 + webpack frontend :3000; BOTH must be up even for
  mock-only pages, or the app hangs on a loading skeleton).
- UI conventions: `src/model-registry/` is the copyable worked example;
  `@databricks/design-system` only (componentId required on interactive
  components; prop types under `dist-types/`, no index.d.ts).

Full pilot learnings live in
[enhancement #17](https://github.com/solaius/rhoai-agentic-hub/issues/17).
