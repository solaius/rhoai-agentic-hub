# MLflow Prototype Target Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make MLflow a declared, repeatable hub.prototype target — target registry, per-target subskill files, doctor section 13 (clone + prepare), env-var-driven fork selection, and per-branch GitLab Pages previews on the pedouble/mlflow fork.

**Architecture:** `conventions/prototype-fork.yaml` becomes a nested target registry (`prototype-targets.yaml`); hub.prototype's SKILL.md keeps the target-agnostic spine and dispatches to `targets/<id>.md` instruction files; doctor gains a section-13 mirror of section 12 for the MLflow clone; a Pages CI job on the gitlab fork's `page-composer-upstream` branch gives every prototype branch a `/branch-<slug>/` preview.

**Tech Stack:** Bash (doctor.sh), Python 3 + PyYAML (hublib schema/indexer, pytest), Markdown skill files, GitLab CI (parallel Pages deployments), yarn 4 + craco (mlflow frontend).

**Spec:** /docs/superpowers/specs/2026-08-05-mlflow-prototype-target-design.md

## Global Constraints

- The hub repo is PUBLIC — nothing NDA-adjacent in tracked files; real credentials only in `restricted/.env` (gitignored).
- Never `git add -A` in the hub — always explicit pathspecs; hub commits end with `Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>`.
- Never hand-edit generated files (`views/*`, `*/index.md`, `memory/index.md`) — run `python scripts/hub_index.py`.
- Doctor semantics: `check` = read-only, `setup` = writes. Doctor NEVER mutates an existing clone's checked-out branch or working tree.
- Env fallbacks (exact): `MLFLOW_SOURCE_REPO` empty → `https://github.com/mlflow/mlflow`; `MLFLOW_SOURCE_BRANCH` empty → `master`; `MLFLOW_DIR` empty → `<hub parent>/mlflow`, else `~/code/rh/mlflow`.
- Owner values (exact): `MLFLOW_SOURCE_REPO=https://github.com/DaoDaoNoCode/mlflow`, `MLFLOW_SOURCE_BRANCH=page-composer-upstream`, `MLFLOW_PUSH_REPO=https://gitlab.cee.redhat.com/pedouble/mlflow/`.
- The UXD-fork flow must not change behavior (only move); `uxd-rhoai` stays the default target.
- The local mlflow clone at `F:/code/rh/mlflow` is on branch `skills-registry-rfc` with uncommitted pilot work — never check out another branch in it directly; use `git worktree` for the CI-file commit.
- Verification trio must stay green: `python -m pytest scripts/tests -v`, `python scripts/hub_lint.py` (0 errors), `python scripts/hub_index.py --check`.
- All hub work happens on `main` (house style: direct small commits, no feature branch — matches how #16 landed).

---

### Task 1: Target registry — rename prototype-fork.yaml to prototype-targets.yaml

**Files:**
- Rename: `conventions/prototype-fork.yaml` → `conventions/prototype-targets.yaml` (git mv, new nested content)
- Modify: `scripts/doctor.sh` (section 12e references: lines ~881-913)
- Modify: `conventions/layout.md:57` (path reference)
- Modify: `.claude/skills/hub.prototype/SKILL.md` lines 12, 30, 166 (path string only — full restructure is Task 3)

**Interfaces:**
- Produces: `conventions/prototype-targets.yaml` with top-level `targets:` map; keys `uxd-rhoai` (has `default: true`) and `mlflow`. Tasks 3, 4, 5 read this exact shape.
- Produces: doctor helper convention — read a target's `pages_base_url` via PyYAML: `yaml.safe_load(...)['targets'][<id>].get('pages_base_url')`.

- [ ] **Step 1: git mv and write the new registry content**

```bash
cd F:/code/rh/rhoai-agentic-hub
git mv conventions/prototype-fork.yaml conventions/prototype-targets.yaml
```

Then replace the file's entire content with:

```yaml
# Prototype target registry -- single tracked source of truth for the
# multi-target prototype pipeline (specs:
# /docs/superpowers/specs/2026-08-04-uxd-fork-prototyping-design.md,
# /docs/superpowers/specs/2026-08-05-mlflow-prototype-target-design.md).
# Each target's pages_base_url is discovered by `bash scripts/doctor.sh
# setup` (needs GITLAB_CEE_TOKEN) or filled by hand from the fork's
# GitLab Pages settings; commit the change when it lands. Local clone
# paths are machine-specific and live in restricted/.env (the env var
# named by each target's clone_dir_env).
# `instructions:` paths are relative to .claude/skills/hub.prototype/.
targets:
  uxd-rhoai:
    default: true
    upstream_repo: https://gitlab.cee.redhat.com/uxd/prototypes/rhoai
    upstream_project_id: 155361
    fork_repo: git@gitlab.cee.redhat.com:pedouble/rhoai.git
    fork_project_path: pedouble/rhoai
    base_branch: "3.6"
    pages_base_url: "https://rhoai-a4b259.pages.redhat.com"
    clone_dir_env: UXD_FORK_DIR
    instructions: targets/uxd-rhoai.md
  mlflow:
    source_repo_default: https://github.com/mlflow/mlflow
    source_repo_env: MLFLOW_SOURCE_REPO
    source_branch_env: MLFLOW_SOURCE_BRANCH
    source_branch_default: master
    push_repo_env: MLFLOW_PUSH_REPO
    push_project_path: pedouble/mlflow
    pages_base_url: ""
    clone_dir_env: MLFLOW_DIR
    instructions: targets/mlflow.md
```

- [ ] **Step 2: Update doctor.sh section 12e to the nested shape**

In `scripts/doctor.sh`, three spots (all inside section 12e, ~lines 881-913):

(a) The sync heredoc (currently `SYNC=$(PAGES_LIVE=... "$PYTHON" - "$ROOT/conventions/prototype-fork.yaml" "$MODE" <<'PY'`). Replace the whole `SYNC=` assignment with a target-aware version:

```bash
        # keep conventions/prototype-targets.yaml in sync (tracked -- commit it).
        SYNC=$(PAGES_LIVE="$PAGES_LIVE" "$PYTHON" - "$ROOT/conventions/prototype-targets.yaml" "$MODE" uxd-rhoai <<'PY'
import os, re, sys
path, mode, target = sys.argv[1], sys.argv[2], sys.argv[3]
url = os.environ["PAGES_LIVE"].rstrip("/")
text = open(path, encoding="utf-8").read()
block = re.search(r'(?ms)^  ' + re.escape(target) + r':\n.*?(?=^  \S|\Z)', text)
if not block:
    print("stale"); sys.exit()
m = re.search(r'(?m)^    pages_base_url:\s*"?([^"\n]*)"?\s*$', block.group(0))
if not m:
    print("stale"); sys.exit()
cur = m.group(1)
if cur == url:
    print("ok")
elif mode == "setup":
    s = block.start() + m.start()
    e = block.start() + m.end()
    open(path, "w", encoding="utf-8").write(
        text[:s] + f'    pages_base_url: "{url}"' + text[e:])
    print("written")
else:
    print("stale")
PY
)
```

(b) The `case "$SYNC"` messages: change the two `prototype-fork.yaml` strings to `prototype-targets.yaml`.

(c) The no-token fallback read (currently `PB=$(grep -E '^pages_base_url:' ...)`). Replace with:

```bash
      PB=$("$PYTHON" -c "import yaml; d=yaml.safe_load(open(r'$ROOT/conventions/prototype-targets.yaml', encoding='utf-8')); print(d['targets']['uxd-rhoai'].get('pages_base_url') or '')" 2>/dev/null)
```

and in the following `warn` message change `conventions/prototype-fork.yaml pages_base_url` to `conventions/prototype-targets.yaml (targets.uxd-rhoai.pages_base_url)`.

- [ ] **Step 3: Update path references in layout.md and SKILL.md**

- `conventions/layout.md` line 57: `(conventions/prototype-fork.yaml points at it)` → `(conventions/prototype-targets.yaml, target uxd-rhoai, points at it)`.
- `.claude/skills/hub.prototype/SKILL.md`: replace the string `conventions/prototype-fork.yaml` with `conventions/prototype-targets.yaml` at lines 12, 30, and 166 (content restructure comes in Task 3; for line 30 also change "Read `conventions/prototype-targets.yaml`" context to read the `uxd-rhoai` target's keys — a one-line touch-up: `Read conventions/prototype-targets.yaml (targets.uxd-rhoai).`; line 166: `pages_base_url` from the `uxd-rhoai` target).

- [ ] **Step 4: Verify**

```bash
bash -n scripts/doctor.sh
bash scripts/doctor.sh check 2>&1 | tail -30   # section 12 must still print its checks; VPN-off is fine (warn+skip)
grep -rn "prototype-fork" --include="*.md" --include="*.sh" --include="*.yaml" . | grep -v docs/superpowers | grep -v ai-asset  # expect no hits
python -m pytest scripts/tests -q
python scripts/hub_lint.py > /dev/null; echo "lint exit: $?"
```

Expected: syntax OK; doctor runs; only historical spec/plan docs still mention the old name; tests pass; lint exit 0.

- [ ] **Step 5: Commit**

```bash
git add conventions/prototype-targets.yaml scripts/doctor.sh conventions/layout.md .claude/skills/hub.prototype/SKILL.md
git commit -m "feat(prototype): target registry — prototype-fork.yaml → prototype-targets.yaml (#17)

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>" -- conventions/prototype-fork.yaml conventions/prototype-targets.yaml scripts/doctor.sh conventions/layout.md .claude/skills/hub.prototype/SKILL.md
```

---

### Task 2: Env vars + prototype.yaml target/composes validation (TDD)

**Files:**
- Modify: `restricted/.env.example` (tracked)
- Modify: `restricted/.env` (LOCAL ONLY — gitignored, never committed)
- Modify: `scripts/hublib/schema.py` (`_lint_prototypes`, ~line 206)
- Test: `scripts/tests/test_schema.py`

**Interfaces:**
- Consumes: `conventions/prototype-targets.yaml` (Task 1) — `targets:` keys are the valid `target:` values.
- Produces: prototype.yaml optionally carries `target: <registry key>` (absent = uxd-rhoai) and `composes: [<branch>, ...]`; lint errors on unknown target or non-list composes. Tasks 3/4/8 rely on these fields being lint-legal.

- [ ] **Step 1: Write the failing tests**

Append to `scripts/tests/test_schema.py` (reuse the existing `write()` helper, `run_lint`-style invocation, and `V2_YAML` fixture defined near line 679 — follow the shape of `test_prototype_yaml_bad_status_is_error`):

```python
def test_prototype_target_known_is_ok(tmp_path):
    root = make_root(tmp_path, components=["x"])
    write(root, "conventions/prototype-targets.yaml",
          "targets:\n  uxd-rhoai:\n    default: true\n  mlflow:\n    pages_base_url: \"\"\n")
    write(root, "components/x/prototype/registry-ui/prototype.yaml",
          V2_YAML + "target: mlflow\n")
    errors, _ = lint_all(root)
    assert not any("target" in e for e in errors)


def test_prototype_target_unknown_is_error(tmp_path):
    root = make_root(tmp_path, components=["x"])
    write(root, "conventions/prototype-targets.yaml",
          "targets:\n  uxd-rhoai:\n    default: true\n")
    write(root, "components/x/prototype/registry-ui/prototype.yaml",
          V2_YAML + "target: figma\n")
    errors, _ = lint_all(root)
    assert any("unknown target 'figma'" in e for e in errors)


def test_prototype_composes_must_be_string_list(tmp_path):
    root = make_root(tmp_path, components=["x"])
    write(root, "components/x/prototype/registry-ui/prototype.yaml",
          V2_YAML + "composes: some-branch\n")
    errors, _ = lint_all(root)
    assert any("composes" in e for e in errors)


def test_prototype_composes_list_is_ok(tmp_path):
    root = make_root(tmp_path, components=["x"])
    write(root, "components/x/prototype/registry-ui/prototype.yaml",
          V2_YAML + "composes: [skills-registry-rfc]\n")
    errors, _ = lint_all(root)
    assert not any("composes" in e for e in errors)
```

NOTE: match the file's ACTUAL fixture helpers — open `scripts/tests/test_schema.py`, look at how `test_prototype_yaml_bad_status_is_error` builds its root and collects `errors`, and use exactly that pattern (helper names above are indicative; the existing test file is the authority).

- [ ] **Step 2: Run tests to verify the new ones fail**

Run: `python -m pytest scripts/tests/test_schema.py -q -k "target or composes"`
Expected: the two negative tests FAIL (no such validation yet); positive tests may pass vacuously.

- [ ] **Step 3: Implement validation in schema.py**

In `scripts/hublib/schema.py`, inside `_lint_prototypes` (after the `snapshots` block, before the `comps` block), add:

```python
        target = data.get("target")
        if target is not None:
            targets_file = root / "conventions" / "prototype-targets.yaml"
            known = None
            if targets_file.is_file():
                try:
                    tdata = yaml.safe_load(targets_file.read_text(encoding="utf-8")) or {}
                    known = set((tdata.get("targets") or {}).keys())
                except yaml.YAMLError:
                    known = None
            if known is not None and target not in known:
                errors.append(f"{yrel}: unknown target '{target}' "
                              f"(not in conventions/prototype-targets.yaml)")
        composes = data.get("composes")
        if composes is not None:
            if not isinstance(composes, list) or not all(
                    isinstance(x, str) and x for x in composes):
                errors.append(f"{yrel}: composes must be a list of branch names")
```

(`root` is already a parameter of `_lint_prototypes`; if it is a string in that scope, wrap with `Path(root)` consistent with the file's imports.)

- [ ] **Step 4: Run the full test suite**

Run: `python -m pytest scripts/tests -q`
Expected: PASS (all, including the 4 new tests).

- [ ] **Step 5: Add the env section to restricted/.env.example**

Append before the rhai-customer-tracker section (keep the file's `# ── Title ──…` style):

```
# ── Optional: MLflow prototyping (hub.prototype, mlflow target) ─────
# Source fork to clone and ground against ('origin' remote).
# Empty/unset falls back to https://github.com/mlflow/mlflow (branch master).
# MLFLOW_SOURCE_REPO=https://github.com/DaoDaoNoCode/mlflow
# MLFLOW_SOURCE_BRANCH=page-composer-upstream
# Push target for completed prototype branches ('gitlab' remote);
# its GitLab Pages hosts the /branch-<slug>/ previews. If unset, push
# and Pages steps are skipped (local-only prototyping still works).
# MLFLOW_PUSH_REPO=https://gitlab.cee.redhat.com/pedouble/mlflow/
# Clone location override. Default: sibling of this repo (../mlflow),
# else ~/code/rh/mlflow.
# MLFLOW_DIR=
```

- [ ] **Step 6: Set the owner's values in restricted/.env (local, no commit)**

Append to `restricted/.env`:

```
MLFLOW_SOURCE_REPO=https://github.com/DaoDaoNoCode/mlflow
MLFLOW_SOURCE_BRANCH=page-composer-upstream
MLFLOW_PUSH_REPO=https://gitlab.cee.redhat.com/pedouble/mlflow/
```

- [ ] **Step 7: Commit (tracked files only)**

```bash
git add scripts/hublib/schema.py scripts/tests/test_schema.py restricted/.env.example
git commit -m "feat(prototype): target/composes lint + MLflow env vars (#17)

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>" -- scripts/hublib/schema.py scripts/tests/test_schema.py restricted/.env.example
```

(`restricted/.env.example` is tracked via git-crypt-exempt path — verify with `git check-ignore restricted/.env.example; echo $?` → expect exit 1, meaning NOT ignored. If it IS ignored on this machine, stop and report instead of forcing.)

---

### Task 3: hub.prototype SKILL.md restructure + targets/uxd-rhoai.md extraction

**Files:**
- Create: `.claude/skills/hub.prototype/targets/uxd-rhoai.md`
- Modify: `.claude/skills/hub.prototype/SKILL.md` (full rewrite of body; frontmatter description updated)

**Interfaces:**
- Consumes: `conventions/prototype-targets.yaml` (Task 1).
- Produces: SKILL.md "Step 0.5: Target resolution" contract — later tasks (4, and the pilot run) rely on: resolved target id `T`, its registry entry, and `targets/<T>.md` being read and followed for target-specific steps. The target file MUST define these named hooks, which SKILL.md references: **[T-prereq]** (prerequisites), **[T-plan]** (component/idiom planning), **[T-generate]** (branch + codegen mechanics), **[T-verify]** (verification recipe), **[T-metadata]** (prototype.yaml field values incl. preview_url semantics), **[T-push]** (gate execution: remote push mechanics), **[T-report]** (what to tell the user).

- [ ] **Step 1: Create targets/uxd-rhoai.md**

Content — a pure extraction of today's UXD-specific text (KEEP WORDING VERBATIM where possible; source lines refer to the current SKILL.md read in full before editing):

````markdown
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
````

- [ ] **Step 2: Rewrite SKILL.md as the target-agnostic spine**

Replace the SKILL.md body (keep the YAML frontmatter, but update `description:` to mention multi-target: append "Targets: the UXD RHOAI fork (default) and the MLflow fork — declared in conventions/prototype-targets.yaml." to the existing description). New body:

````markdown
# hub.prototype

Input: a subcommand (`create`, `version`, `list`) plus a component id
and/or slug. Default subcommand: `create`.

Specs: /docs/superpowers/specs/2026-08-04-uxd-fork-prototyping-design.md
(owner rulings R1-R6),
/docs/superpowers/specs/2026-08-05-mlflow-prototype-target-design.md
(multi-target). Target registry: /conventions/prototype-targets.yaml.
Structure: /conventions/layout.md (prototype/ leg, prototype.yaml v2).

Prototypes are internal-only (fork GitLab Pages / Red Hat network).
There is no publish mode: the preview URL is the shareable artifact.

## Step 0: Target resolution (CREATE and VERSION)

Read `/conventions/prototype-targets.yaml`. Resolve the target `T`:

1. Explicit: the user named one ("in mlflow", "mlflow target").
2. VERSION: the prototype's `prototype.yaml` `target:` field (absent =
   `uxd-rhoai`).
3. CREATE: if the component's existing prototypes declare a `target:`,
   offer that as the default; else the registry entry with
   `default: true` (`uxd-rhoai`).

Then read `targets/<T>.md` (path from the registry's `instructions:`,
relative to this skill directory) and run its **[T-prereq]** section.
Every later step marked [T-*] follows that file. Skip Step 0 for LIST.

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

Resolve the component id against `components/components.yaml` (offer
`hub.intake` and stop if unknown), then deep-read, skipping what does
not exist:

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
   components; open their preview URLs for continuity). Note their
   `target:` and `composes:` -- a new prototype that needs another's
   screens composes that branch (see the target file's [T-generate]).
h. Restricted context (if `restricted/` exists locally -- informs design,
   NEVER surfaces in output; fork branches are internal but the hub repo
   is PUBLIC).
i. Target design context: whatever the target file's [T-plan] names as
   its design references.

### Step 2: Scope

Summarize the most design-relevant findings (2-5 sentences), then ask
what to prototype. Accept a description, a Jira key, a knowledge entry
reference, a Figma link/screenshot, or "the whole thing".

### Step 3: Slug

Derive a kebab-case slug (e.g. `registry-ui`). It becomes BOTH the hub
metadata dir (`components/<id>/prototype/<slug>/`) and the target repo
branch name. If a branch of that name already exists there, prefix the
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

Follow the target file's **[T-plan]** section, then produce a content
plan (files, routes, nav placement). User confirms.

### Step 7: Generate

Follow the target file's **[T-generate]** section.

### Step 8: Verify (non-negotiable)

Follow the target file's **[T-verify]** section.

### Step 9: Metadata (in the hub)

Write `components/<id>/prototype/<slug>/prototype.yaml`:

```yaml
title: <title>
description: <one line>
status: active
components: [<id>]
target: <T>              # omit for uxd-rhoai (the default)
source_repo: <from [T-metadata]>
branch: <slug>
base: <from [T-metadata]>
preview_url: <from [T-metadata]>
composes: [<branches>]   # only if other prototype branches were merged in
current: v1
versions:
  v1: {timestamp: <today>, commit: <sha after the target-repo commit>, summary: <one line>}
```

### Step 10: Gate (two-part, one confirm)

Show: target repo branch name, files created/changed, verification
results, the prototype.yaml content, and the computed preview URL. On OK:
a. Target repo: commit + push per the target file's **[T-push]**.
b. Hub: fill `commit:` with the target-repo sha, then stage the
   prototype dir + regenerated indexes (Step 11) and commit with
   pathspecs (`proto(<id>): <slug> v1`).
On reject: discard both sides, ask what to change.

### Step 11: Reindex

`python scripts/hub_index.py` then `python scripts/hub_lint.py` (0
errors). Stage `components/<id>/prototype/<slug>/`, the component
`index.md`, `components/index.md`, `views/prototypes.md` -- never
`git add -A`.

### Step 12: Report

Follow the target file's **[T-report]** section.

## VERSION

Input: `<component>/<slug>`.

1. Read `components/<id>/prototype/<slug>/prototype.yaml` (error +
   suggest `create` if missing). Resolve the target from its `target:`
   field (Step 0 rule 2) and run [T-prereq].
2. Context: re-run the deltas of CREATE step 1 (what changed in
   knowledge/strategy/Jira since the last version) plus the user's
   feedback. Show a brief; user confirms.
3. In the target repo: check out the prototype branch; iterate;
   re-verify ([T-verify]).
4. Snapshot on request: if the user wants the CURRENT state kept
   viewable side by side, snapshot per the target file's [T-push]
   snapshot mechanics before iterating; record under `snapshots:` with
   its own preview URL.
5. Gate (same two-part shape): target repo commit+push ([T-push]); hub
   prototype.yaml gets a new `versions:` entry (sha, date, summary),
   `current:` bumped.
6. Reindex + report ([T-report]).

## Key principles

1. **Grounded, not invented.** The context load exists so the prototype
   reflects reality -- real entity names, states, navigation.
2. **Native accuracy is mandatory.** Each target file defines how design
   accuracy is enforced (PatternFly MCP for uxd-rhoai, design-system
   types + named reference screens for mlflow); those rules are law.
3. **Real app, real chrome.** Targets provide an actual product shell,
   nav, and components -- never hand-approximate them.
4. **Branch per prototype, off the target's declared base.** Keeps
   previews isolated and upstream MRs clean by construction.
5. **Internal-only.** Preview URLs are the artifact; no public mirror
   from this skill, ever.
6. **The gate is sacred.** Nothing is committed or pushed -- in either
   repo -- before the user approves.
````

- [ ] **Step 3: Verify by inspection + tooling**

```bash
ls .claude/skills/hub.prototype/targets/
python scripts/hub_lint.py > /dev/null; echo "lint exit: $?"
python -m pytest scripts/tests -q
```

Also diff-check completeness: every numbered step and rule from the pre-restructure SKILL.md (git show HEAD:.claude/skills/hub.prototype/SKILL.md) must appear either in the new SKILL.md or in targets/uxd-rhoai.md. Read both and confirm; list anything dropped.

- [ ] **Step 4: Commit**

```bash
git add .claude/skills/hub.prototype/SKILL.md .claude/skills/hub.prototype/targets/uxd-rhoai.md
git commit -m "feat(prototype): SKILL.md target-agnostic spine + uxd-rhoai target file (#17)

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>" -- .claude/skills/hub.prototype/SKILL.md .claude/skills/hub.prototype/targets/uxd-rhoai.md
```

---

### Task 4: targets/mlflow.md

**Files:**
- Create: `.claude/skills/hub.prototype/targets/mlflow.md`

**Interfaces:**
- Consumes: registry entry `targets.mlflow` (Task 1), env vars (Task 2), SKILL.md [T-*] hook contract (Task 3), doctor section 13 (Task 5 — referenced by name; Task 5 may land after, the reference is stable).
- Produces: the complete MLflow flow instruction file the pilot run follows.

- [ ] **Step 1: Write the file**

````markdown
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
````

- [ ] **Step 2: Verify**

```bash
python scripts/hub_lint.py > /dev/null; echo "lint exit: $?"
```

Cross-check the [T-*] hook names against SKILL.md (Task 3): every hook SKILL.md references exists in this file.

- [ ] **Step 3: Commit**

```bash
git add .claude/skills/hub.prototype/targets/mlflow.md
git commit -m "feat(prototype): mlflow target instruction file (#17)

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>" -- .claude/skills/hub.prototype/targets/mlflow.md
```

---

### Task 5: doctor.sh section [13] MLflow prototyping

**Files:**
- Modify: `scripts/doctor.sh` — insert the new section between the end of section 12 (the closing `fi` at ~line 917, after Task 1's edits) and the `echo "== result: ..."` line.

**Interfaces:**
- Consumes: env vars from `restricted/.env` (sourced by section 4): `MLFLOW_SOURCE_REPO`, `MLFLOW_SOURCE_BRANCH`, `MLFLOW_PUSH_REPO`, `MLFLOW_DIR`, `GITLAB_CEE_TOKEN`. Helpers already defined in the file: `ok`, `warn`, `fail`, `note`, `$MODE`, `$ROOT`, `$PYTHON`, `$GITLAB_CEE`.
- Produces: doctor section `[13] MLflow prototyping (hub.prototype)` implementing spec 13a-13f.

- [ ] **Step 1: Insert the section**

```bash
echo "[13] MLflow prototyping (hub.prototype)"
# Spec: docs/superpowers/specs/2026-08-05-mlflow-prototype-target-design.md
# 13a-13f. GitHub-side checks always run; gitlab-side checks (13b push
# remote reachability, 13f Pages) are VPN/token gated like section 12.
MLF_SRC="${MLFLOW_SOURCE_REPO:-https://github.com/mlflow/mlflow}"
MLF_BR="${MLFLOW_SOURCE_BRANCH:-master}"
# 13a. clone. MLFLOW_DIR overrides; default sibling of the hub repo.
MLF=""
SIBLING="$(dirname "$ROOT")/mlflow"
for CAND in "${MLFLOW_DIR:-}" "$SIBLING" "$HOME/code/rh/mlflow"; do
  [ -n "$CAND" ] && [ -d "$CAND/.git" ] && MLF="$CAND" && break
done
if [ -z "$MLF" ]; then
  if [ "$MODE" = "setup" ]; then
    MLF="${MLFLOW_DIR:-$SIBLING}"
    note "cloning $MLF_SRC (branch $MLF_BR) to $MLF (large repo, takes a while)..."
    if git clone --branch "$MLF_BR" "$MLF_SRC" "$MLF" >/dev/null 2>&1; then
      ok "mlflow clone created at $MLF"
    else
      fail "could not clone $MLF_SRC — check the URL/branch (MLFLOW_SOURCE_REPO/MLFLOW_SOURCE_BRANCH in restricted/.env)"
      MLF=""
    fi
  else
    fail "mlflow clone not found — set MLFLOW_DIR in restricted/.env or run: bash scripts/doctor.sh setup"
  fi
else
  ok "mlflow clone at $MLF"
fi
if [ -n "$MLF" ]; then
  # 13b. remotes: origin = source repo; gitlab = push repo (if configured).
  ORIGIN_URL=$(git -C "$MLF" remote get-url origin 2>/dev/null || echo "")
  # compare ignoring a trailing .git / trailing slash
  NORM_SRC=$(printf '%s' "$MLF_SRC" | sed 's|/$||;s|\.git$||')
  NORM_ORI=$(printf '%s' "$ORIGIN_URL" | sed 's|/$||;s|\.git$||')
  if [ "$NORM_ORI" = "$NORM_SRC" ]; then
    ok "origin -> $MLF_SRC"
  else
    warn "origin is '$ORIGIN_URL' (expected $MLF_SRC from MLFLOW_SOURCE_REPO)"
  fi
  if [ -n "${MLFLOW_PUSH_REPO:-}" ]; then
    PUSH_URL=$(git -C "$MLF" remote get-url gitlab 2>/dev/null || echo "")
    NORM_PUSH_WANT=$(printf '%s' "$MLFLOW_PUSH_REPO" | sed 's|/$||;s|\.git$||')
    NORM_PUSH_HAVE=$(printf '%s' "$PUSH_URL" | sed 's|/$||;s|\.git$||')
    if [ "$NORM_PUSH_HAVE" = "$NORM_PUSH_WANT" ]; then
      ok "gitlab remote -> $MLFLOW_PUSH_REPO"
    elif [ -z "$PUSH_URL" ] && [ "$MODE" = "setup" ]; then
      git -C "$MLF" remote add gitlab "$MLFLOW_PUSH_REPO" \
        && ok "gitlab remote added ($MLFLOW_PUSH_REPO)" \
        || fail "could not add gitlab remote"
    elif [ -z "$PUSH_URL" ]; then
      fail "no 'gitlab' remote — run: bash scripts/doctor.sh setup"
    else
      warn "gitlab remote is '$PUSH_URL' (expected $MLFLOW_PUSH_REPO from MLFLOW_PUSH_REPO)"
    fi
  else
    note "MLFLOW_PUSH_REPO not set — push/Pages checks skipped (local-only prototyping)"
  fi
  # 13c. toolchain + prepare. uv >= 0.10.12 (older uv fails on uv.lock).
  if command -v uv >/dev/null 2>&1; then
    UV_V=$(uv --version 2>/dev/null | sed 's/^uv //;s/ .*//')
    UV_OK=$("$PYTHON" -c "import sys;v='$UV_V'.split('.');print('yes' if tuple(map(int,v[:3]))>=(0,10,12) else 'no')" 2>/dev/null || echo no)
    if [ "$UV_OK" = "yes" ]; then
      ok "uv $UV_V"
    else
      warn "uv $UV_V < 0.10.12 (fails to parse uv.lock) — run: uv self update"
    fi
  else
    fail "uv not installed — https://docs.astral.sh/uv/getting-started/installation/"
  fi
  if command -v yarn >/dev/null 2>&1 || [ -x "$HOME/.local/bin/yarn" ]; then
    ok "yarn available"
  elif [ "$MODE" = "setup" ] && command -v corepack >/dev/null 2>&1; then
    corepack enable --install-directory "$HOME/.local/bin" >/dev/null 2>&1 \
      && ok "yarn enabled via corepack (~/.local/bin)" \
      || fail "corepack enable failed — run: corepack enable --install-directory ~/.local/bin"
  else
    fail "yarn missing — run: corepack enable --install-directory ~/.local/bin (then re-run doctor)"
  fi
  if [ "$MODE" = "setup" ]; then
    if [ ! -d "$MLF/.venv" ] && ! (cd "$MLF" && uv sync >/dev/null 2>&1); then
      warn "uv sync failed in $MLF — run it manually"
    else
      ok "python env ready (uv sync)"
    fi
    if [ -d "$MLF/mlflow/server/js/node_modules" ]; then
      ok "frontend node_modules installed"
    else
      note "running yarn install in mlflow/server/js (~580 MB, takes a while)..."
      (cd "$MLF/mlflow/server/js" && yarn install >/dev/null 2>&1) \
        && ok "yarn install done" \
        || fail "yarn install failed — run it manually in $MLF/mlflow/server/js"
    fi
  else
    [ -d "$MLF/mlflow/server/js/node_modules" ] \
      && ok "frontend node_modules installed" \
      || fail "frontend node_modules missing — run: bash scripts/doctor.sh setup"
  fi
  # 13d. ready probe (non-blocking; does NOT boot the dev servers —
  # that's the clone's own dev-server skill at prototype time).
  if (cd "$MLF" && uv run mlflow --version >/dev/null 2>&1); then
    ok "mlflow importable — clone ready for use"
  else
    warn "uv run mlflow --version failed — run: bash scripts/doctor.sh setup (uv sync)"
  fi
  # 13e. session wiring: additional working directory (same as 12d).
  AD13=$(FORK="$MLF" "$PYTHON" - "$ROOT/.claude/settings.local.json" "$MODE" <<'PY'
import json, os, sys
path, mode = sys.argv[1], sys.argv[2]
fork = os.environ["FORK"].replace("\\", "/")
try:
    data = json.load(open(path, encoding="utf-8"))
except (OSError, ValueError):
    data = {}
dirs = data.setdefault("permissions", {}).setdefault("additionalDirectories", [])
if fork in dirs:
    print("ok")
elif mode == "setup":
    dirs.append(fork)
    json.dump(data, open(path, "w", encoding="utf-8"), indent=2)
    print("written")
else:
    print("missing")
PY
)
  case "$AD13" in
    ok) ok "mlflow clone granted as additional working directory" ;;
    written) ok "mlflow clone added to additionalDirectories (restart Claude Code to take effect)" ;;
    *) fail "mlflow clone not in .claude/settings.local.json additionalDirectories — run: bash scripts/doctor.sh setup" ;;
  esac
  # 13f. Pages base URL discovery (pedouble/mlflow), token + VPN gated.
  if [ -n "${MLFLOW_PUSH_REPO:-}" ]; then
    HTTP13=$(curl -sk --connect-timeout 5 -o /dev/null -w '%{http_code}' \
      "$GITLAB_CEE/api/v4/projects/pedouble%2Fmlflow" 2>/dev/null || echo 000)
    if [ "$HTTP13" != "200" ]; then
      warn "cannot reach gitlab.cee.redhat.com — connect to the Red Hat VPN (mlflow Pages checks skipped)"
    elif [ -n "${GITLAB_CEE_TOKEN:-}" ]; then
      MPROJ="$GITLAB_CEE/api/v4/projects/pedouble%2Fmlflow"
      MPAGES_JSON=$(curl -sk --connect-timeout 5 -H "PRIVATE-TOKEN: $GITLAB_CEE_TOKEN" "$MPROJ/pages" 2>/dev/null || echo "")
      MPAGES_LIVE=$(printf '%s' "$MPAGES_JSON" | "$PYTHON" -c 'import json,sys
try: print(json.load(sys.stdin).get("url",""))
except Exception: print("")')
      if [ -n "$MPAGES_LIVE" ]; then
        ok "mlflow fork Pages enabled: $MPAGES_LIVE"
        SYNC13=$(PAGES_LIVE="$MPAGES_LIVE" "$PYTHON" - "$ROOT/conventions/prototype-targets.yaml" "$MODE" mlflow <<'PY'
import os, re, sys
path, mode, target = sys.argv[1], sys.argv[2], sys.argv[3]
url = os.environ["PAGES_LIVE"].rstrip("/")
text = open(path, encoding="utf-8").read()
block = re.search(r'(?ms)^  ' + re.escape(target) + r':\n.*?(?=^  \S|\Z)', text)
if not block:
    print("stale"); sys.exit()
m = re.search(r'(?m)^    pages_base_url:\s*"?([^"\n]*)"?\s*$', block.group(0))
if not m:
    print("stale"); sys.exit()
cur = m.group(1)
if cur == url:
    print("ok")
elif mode == "setup":
    s = block.start() + m.start()
    e = block.start() + m.end()
    open(path, "w", encoding="utf-8").write(
        text[:s] + f'    pages_base_url: "{url}"' + text[e:])
    print("written")
else:
    print("stale")
PY
)
        case "$SYNC13" in
          ok) ok "prototype-targets.yaml mlflow pages_base_url in sync" ;;
          written) ok "prototype-targets.yaml mlflow pages_base_url written — commit the change" ;;
          *) warn "prototype-targets.yaml mlflow pages_base_url is stale/empty — run: bash scripts/doctor.sh setup" ;;
        esac
      else
        warn "mlflow fork Pages not reachable via API — push a branch with the Pages CI once, then re-run"
      fi
    else
      note "no GITLAB_CEE_TOKEN — mlflow Pages URL discovery skipped (fill targets.mlflow.pages_base_url by hand from the fork's Deploy > Pages settings)"
    fi
  fi
fi
```

- [ ] **Step 2: Verify**

```bash
bash -n scripts/doctor.sh
bash scripts/doctor.sh check 2>&1 | sed -n '/\[13\]/,$p'
```

Expected on this machine: clone found at `F:/code/rh/mlflow`; origin matches the DaoDaoNoCode URL; gitlab remote matches; uv/yarn ok; node_modules ok; mlflow importable; additionalDirectories either ok or "run setup"; 13f warns/notes depending on VPN + token. ZERO mutations in check mode (confirm `git -C F:/code/rh/mlflow status --porcelain` unchanged before/after).

- [ ] **Step 3: Run setup mode and verify idempotence**

```bash
bash scripts/doctor.sh setup 2>&1 | sed -n '/\[13\]/,$p'
```

Expected: same or better results; a second consecutive run reports all-ok with no new writes.

- [ ] **Step 4: Commit**

```bash
git add scripts/doctor.sh
git commit -m "feat(doctor): section 13 — MLflow prototyping clone/prepare/pages (#17)

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>" -- scripts/doctor.sh
```

---

### Task 6: Pages CI job on the mlflow fork (gated push)

**Files:**
- Create (in the MLFLOW FORK, not the hub): `.gitlab-ci.yml` committed to branch `page-composer-upstream`, pushed to the `gitlab` remote (pedouble/mlflow).

**Interfaces:**
- Consumes: the fork clone at `F:/code/rh/mlflow` (dirty on `skills-registry-rfc` — MUST use a worktree, never checkout).
- Produces: every branch pushed to pedouble/mlflow that descends from `gitlab/page-composer-upstream` builds a Pages parallel deployment at `/branch-<slug>/`.

**Facts locked by exploration:** `mlflow/server/js/package.json` has `"packageManager": "yarn@4.12.0"`, `"homepage": "static-files"`, build script `GENERATE_SOURCEMAP=false craco --max_old_space_size=8192 build` (CRA — outputs `build/`); craco sets a RELATIVE `output.publicPath` (`static-files/`), and the app uses hash routing — so the built app works from any sub-path with no ASSET_PATH machinery. The cee GitLab instance supports Pages parallel deployments (`pages.path_prefix`) — the UXD fork (`F:/code/rh/rhoai/.gitlab-ci.yml`) is the proven reference, runner tag `itup-alm-arm`.

- [ ] **Step 1: Create a worktree for page-composer-upstream**

```bash
git -C F:/code/rh/mlflow fetch origin page-composer-upstream
git -C F:/code/rh/mlflow fetch gitlab page-composer-upstream
git -C F:/code/rh/mlflow worktree add ../mlflow-ci-worktree gitlab/page-composer-upstream
```

(If `gitlab/page-composer-upstream` is behind `origin/page-composer-upstream`, note it in the gate summary — do NOT auto-sync; the CI commit goes on top of the gitlab copy.)

- [ ] **Step 2: Write `.gitlab-ci.yml` in the worktree**

`F:/code/rh/mlflow-ci-worktree/.gitlab-ci.yml`:

```yaml
# ============================================================================
# GitLab CI — MLflow prototype previews (hub.prototype, mlflow target)
# ============================================================================
# Builds the MLflow frontend statically and deploys every branch to a
# GitLab Pages parallel deployment at /branch-<slug>/. The app uses hash
# routing and a relative webpack publicPath ("static-files/"), so the
# build works from any sub-path unchanged. Only mock-backed prototype
# sections are fully functional; the rest of the app degrades to
# empty/error states — share links to the prototyped route, e.g.
# <pages-url>/branch-<slug>/#/skills
#
# Managed by rhoai-agentic-hub (spec:
# docs/superpowers/specs/2026-08-05-mlflow-prototype-target-design.md).
# Pattern source: uxd/prototypes/rhoai fork .gitlab-ci.yml.
# ============================================================================

image: node:22

stages:
  - build
  - deploy

variables:
  NODE_OPTIONS: "--max-old-space-size=8192"

workflow:
  rules:
    - if: $CI_COMMIT_BRANCH

default:
  tags:
    - itup-alm-arm

build:
  stage: build
  variables:
    KUBERNETES_MEMORY_REQUEST: "8Gi"
    KUBERNETES_MEMORY_LIMIT: "12Gi"
  script:
    - corepack enable
    - cd mlflow/server/js
    - yarn install --immutable
    - yarn build
    - cd ../../..
    - rm -rf public && mv mlflow/server/js/build public
  artifacts:
    paths:
      - public
    expire_in: 1 week

pages:
  stage: deploy
  dependencies:
    - build
  pages:
    path_prefix: "branch-$CI_COMMIT_REF_SLUG"
    expire_in: 60 days
  script:
    - echo "Deploying branch-$CI_COMMIT_REF_SLUG to GitLab Pages"
  artifacts:
    paths:
      - public
```

- [ ] **Step 3: Local build smoke test (proves the yaml's build steps)**

```bash
cd F:/code/rh/mlflow/mlflow/server/js && yarn build
ls build/index.html build/static-files 2>/dev/null || ls build | head
```

Expected: `build/` exists with `index.html`; asset references in `index.html` are RELATIVE (grep for `static-files/` — no leading `/`). This runs in the MAIN clone (same package state as the worktree); worktree build is unnecessary duplication.

- [ ] **Step 4: Commit in the worktree**

```bash
cd F:/code/rh/mlflow-ci-worktree
git add .gitlab-ci.yml
git commit -m "ci: GitLab Pages parallel deployments for prototype branch previews"
```

(mlflow-fork commit — hub trailer conventions don't apply there; keep the message plain.)

- [ ] **Step 5: GATE — show the user, then push**

Show the user: the full `.gitlab-ci.yml`, the worktree commit sha, and whether `gitlab/page-composer-upstream` was behind `origin/page-composer-upstream`. This is an outward push to a shared fork — WAIT for explicit OK. On OK:

```bash
cd F:/code/rh/mlflow-ci-worktree
git push gitlab HEAD:page-composer-upstream
cd .. && git -C F:/code/rh/mlflow worktree remove mlflow-ci-worktree
```

Then watch the pipeline start: `https://gitlab.cee.redhat.com/pedouble/mlflow/-/pipelines`. If the pipeline fails on runner tags or memory, iterate on the CI file with the same worktree flow (fetch, fix, push) — do NOT leave a red pipeline unreported.

- [ ] **Step 6: Record the outcome**

If the pipeline succeeds and Pages activates: re-run `bash scripts/doctor.sh setup` — section 13f should discover the Pages URL and write `targets.mlflow.pages_base_url`; commit that:

```bash
git add conventions/prototype-targets.yaml
git commit -m "conf(prototype): mlflow pages_base_url discovered (#17)

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>" -- conventions/prototype-targets.yaml
```

If Pages doesn't activate on the first push (GitLab sometimes needs the pages job to succeed once before the API reports a URL), note it and move on — 13f will catch it on a later doctor run.

---

### Task 7: Documentation sweep

**Files:**
- Modify: `docs/skills.md` (hub.prototype section, ~line 112)
- Modify: `docs/capabilities.md` (lines ~28, 43, 63, 112-121 region)
- Modify: `conventions/layout.md` (prototype.yaml v2 field list, ~lines 45-65)
- Modify: `docs/setup.md` (optional-tooling lines ~34-43)
- Modify: `AGENTS.md` (hub.prototype row)

**Interfaces:**
- Consumes: everything shipped in Tasks 1-6 (names, paths, env vars must match exactly).

- [ ] **Step 1: layout.md — prototype.yaml v2 additions**

In the prototype.yaml field list (the block ending "…`mr_url` (set when upstreamed)"), extend the optional line to:

```
- optional: `target` (a key of conventions/prototype-targets.yaml
  `targets:`; absent = `uxd-rhoai`), `composes` (list of other prototype
  branches merged into this one), `snapshots` (map `vN -> {branch,
  preview_url}` for frozen side-by-side branches), `mr_url` (set when
  upstreamed)
```

And replace the paragraph "Prototypes normally live in the UXD fork; an owner-approved prototype in another repo (e.g. the MLflow fork)…" with:

```
The React pages themselves live in the target repo declared by
`target:` (conventions/prototype-targets.yaml) — the UXD fork
(`uxd-rhoai`, default, branches off `upstream/3.6`) or the MLflow fork
(`mlflow`, branches off the configured source branch). `preview_url`
points at the target's Pages deployment (`<pages_base_url>/branch-<slug>/`)
when one exists, else the branch URL as a stand-in. Cross-component
prototypes keep their metadata in `narrative/prototype/<slug>/`.
```

- [ ] **Step 2: docs/skills.md — hub.prototype entry**

Update the `hub.prototype` bullet (~line 112): change "UI prototypes as real React + PatternFly 6 pages … in the UXD fork" to name both targets, e.g. append after the existing first sentence:

```
Targets are declared in `conventions/prototype-targets.yaml` and each
has an instruction file under the skill's `targets/` dir: `uxd-rhoai`
(default — React + PatternFly 6 in the UXD RHOAI fork) and `mlflow`
(MLflow's own design system in the MLflow fork; env-selected source
fork via MLFLOW_SOURCE_REPO/MLFLOW_SOURCE_BRANCH, pushed to
MLFLOW_PUSH_REPO with per-branch GitLab Pages previews). Doctor
sections 12-13 keep both target environments healthy.
```

- [ ] **Step 3: docs/capabilities.md — multi-target wording**

- Line ~28 (pain-point row): append to the answer cell: "Targets now include MLflow itself — prototypes land in the MLflow fork in its native design system."
- Line ~43 (day-in-the-life): after "generates a React page on a branch in the UXD fork", change to "generates a page on a branch in the chosen target repo (UXD fork by default; MLflow fork for MLflow-native prototypes)".
- The `hub.prototype` capability bullet (~112-121): same treatment as skills.md — one added sentence naming the mlflow target and its preview story.

- [ ] **Step 4: docs/setup.md — env vars + doctor 13**

After the existing "Optional (hub.prototype): the UXD RHOAI fork clone…" block (~line 40-43), add:

```
Optional (hub.prototype, mlflow target): the MLflow fork clone —
`bash scripts/doctor.sh setup` clones and prepares it (uv sync + yarn
install) as a sibling of this repo; set MLFLOW_DIR / MLFLOW_SOURCE_REPO /
MLFLOW_SOURCE_BRANCH / MLFLOW_PUSH_REPO in `restricted/.env` to override
(see restricted/.env.example). Building the frontend needs Node.js +
corepack (yarn 4); the Python side needs uv >= 0.10.12.
```

- [ ] **Step 5: AGENTS.md — hub.prototype row**

Change the row text from "React/PF6 pages in the UXD fork with live previews" wording to: `create/version/list prototypes — multi-target (UXD RHOAI fork default, MLflow fork) React pages with live GitLab Pages previews, grounded in component knowledge and upstream repos`.

- [ ] **Step 6: Verify + commit**

```bash
python scripts/hub_lint.py > /dev/null; echo "lint exit: $?"
python -m pytest scripts/tests -q
git add docs/skills.md docs/capabilities.md conventions/layout.md docs/setup.md AGENTS.md
git commit -m "docs: multi-target prototyping — skills, capabilities, layout, setup, AGENTS (#17)

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>" -- docs/skills.md docs/capabilities.md conventions/layout.md docs/setup.md AGENTS.md
```

---

### Task 8: Pilot metadata migration + reindex + full verification

**Files:**
- Modify: `components/skills-registry/prototype/skills-registry-mlflow/prototype.yaml`
- Regenerate: `views/prototypes.md`, `components/skills-registry/index.md`, `components/index.md`, `memory/index.md` (via hub_index.py — never by hand)

**Interfaces:**
- Consumes: `target`/`composes` lint support (Task 2), registry (Task 1).

- [ ] **Step 1: Migrate the pilot's prototype.yaml**

Edit `components/skills-registry/prototype/skills-registry-mlflow/prototype.yaml`:
- After `components: [skills-registry]` add `target: mlflow`.
- `base: page-composer-upstream` (it currently reads `page-composer-upstream` — confirm; the field records the SOURCE BRANCH name per [T-metadata], no remote prefix).
- Leave `preview_url` as the branch URL stand-in unless Task 6 landed a `pages_base_url`; if it did, update to `<pages_base_url>/branch-skills-registry-rfc/#/skills` — BUT only if the skills-registry-rfc branch actually has the CI file (it branched before the CI commit, so it likely does NOT — in that case keep the stand-in and note that the preview upgrades when the branch is next versioned/rebased onto the CI-carrying base).

- [ ] **Step 2: Reindex and verify everything**

```bash
python scripts/hub_index.py
python scripts/hub_lint.py            # 0 errors required
python scripts/hub_index.py --check   # 0 stale
python -m pytest scripts/tests -v     # all pass
bash scripts/doctor.sh check 2>&1 | tail -5
```

- [ ] **Step 3: Commit**

```bash
git add components/skills-registry/prototype/skills-registry-mlflow/prototype.yaml components/skills-registry/index.md components/index.md views/prototypes.md
git commit -m "proto(skills-registry): pilot prototype.yaml → mlflow target (#17)

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>" -- components/skills-registry/prototype/skills-registry-mlflow/prototype.yaml components/skills-registry/index.md components/index.md views/prototypes.md
```

(If hub_index touched other generated files, add them to the same pathspec list explicitly.)

---

## After the plan: acceptance run (NOT a subagent task)

Per spec ruling R4, the mcp-registry pilot is an interactive session, not a plan task: run `hub.prototype create mcp-registry`, pick the `mlflow` target, and drive it through grounding → screens → gate. That session (plus `hub.prototype version` on the result) is the acceptance test for everything above. When it completes, close #17 via `hub.enhance` complete (which re-runs the docs-impact checklist).
