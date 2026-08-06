---
name: hub.prototype
description: Create, version, or list UI prototypes for a component or across components. Generates React + PatternFly 6 pages in the UXD RHOAI fork (branch per prototype, live GitLab Pages preview), grounded in the component's real architecture, knowledge, and upstream repos. Use when the user says "prototype", "mockup", "UI prototype", "create a prototype for <component>", "new version of the prototype", "list prototypes", or "prototype the <feature>". Targets: the UXD RHOAI fork (default) and the MLflow fork — declared in conventions/prototype-targets.yaml.
---

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
