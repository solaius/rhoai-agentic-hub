# Components Rename Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rename the `features/` layer to `components/` across the entire repo — structure, code, machine keys, links, prose — and add `jira_component:`/`jira_labels:` metadata, per the approved spec `docs/superpowers/specs/2026-07-31-components-rename-design.md`.

**Architecture:** One atomic mechanical commit (git mv + scripted path/key rewrite + hand-edited code identifiers + tests) so the tree is never half-renamed, followed by additive commits: new lint rules (TDD), yaml metadata population, then judgment-based prose sweeps (skills, docs, memory/content), and a final residual audit.

**Tech Stack:** Python 3 (pyyaml, pytest), git, git-crypt (restricted/ tree), Git Bash on Windows.

## Global Constraints

- **Branch:** all work on `components-rename`, branched from `main`. Do NOT use a separate git worktree — `restricted/` is git-crypt encrypted and only this checkout is unlocked; a fresh worktree would check out ciphertext.
- **Preflight invariant:** `restricted/` must be READABLE (git-crypt unlocked) before any task touches it. Check: `head -c 9 restricted/lint-patterns.txt` must NOT print `\0GITCRYPT`. If locked, STOP and report — do not run any rewrite.
- **Verification trio** (required green before every commit unless the task says otherwise): `python -m pytest scripts/tests -q` (all pass) · `python scripts/hub_lint.py` (0 errors; warnings exactly the pre-existing baseline of 120 — investigate any delta) · `python scripts/hub_index.py --check` (0 stale).
- **NEVER hand-edit generated files** (`components/index.md`, per-partition `index.md`, `views/*`, `memory/index.md`, `*/knowledge/index.md`, `*/work/jira-snapshot.yaml`) — run `python scripts/hub_index.py` to regenerate.
- **NEVER bypass a restricted-pattern lint ERROR** (`--no-verify` is forbidden — that error is the disclosure net).
- **Commit messages** end with: `Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>`

### Canonical rename table (use these names exactly, all tasks)

| old | new |
|---|---|
| `features/` (dir) | `components/` |
| `restricted/features/` | `restricted/components/` |
| `features/features.yaml` | `components/components.yaml` |
| yaml top-level key `features:` | `components:` |
| entry/artifact/story frontmatter key `features:` | `components:` |
| `jira-snapshot.yaml` / triage-log key `feature:` | `component:` |
| `_feature_ids` | `_component_ids` |
| `_check_features` | `_check_components` |
| `_features_table` (indexer) | `_components_table` |
| `_feature_titles` (publisher) | `_component_titles` |
| function params/locals `feature`, `feature_id`, `feature_ids`, `feature_jql`, `feats` | `component`, `component_id`, `component_ids`, `component_jql`, `comps` |
| CLI flag `--feature` (hub_triage.py) | `--component` |
| CLI metavar `FEATURE` | `COMPONENT` |
| HTML `data-feature` / JS `dataset.feature` (triage_html.py) | `data-comp` / `dataset.comp` |
| generated heading `# Features` | `# Components` |
| test helper const `FEATURES_YAML` | `COMPONENTS_YAML` |

### Canonical message-string table (code AND test assertions)

| old fragment | new fragment |
|---|---|
| `unknown feature id` | `unknown component id` |
| `unknown related feature id` | `unknown related component id` |
| `not in features/features.yaml` | `not in components/components.yaml` |
| `features must be a list of feature ids` | `components must be a list of component ids` |
| `related must be a list of feature ids` | `related must be a list of component ids` |
| `must not include the feature itself` | `must not include the component itself` |
| `features: is only allowed on knowledge entries` | `components: is only allowed on knowledge entries` |
| `not part of the feature skeleton` | `not part of the component skeleton` |
| `files directly under a feature` | `files directly under a component` |
| `feature '…' does not match` (jiramap) | `component '…' does not match` |
| `unknown feature '…'` (hub_jira/hub_triage) | `unknown component '…'` |
| `site must be features/<f>/enablement/<slug>/` (refresh) | `site must be components/<c>/enablement/<slug>/` |
| `_No feature partitions yet — hub.file creates them on first use._` | `_No component partitions yet — hub.file creates them on first use._` |
| `type 'story' requires field 'features'` | `type 'story' requires field 'components'` |

### PRESERVE list — the find/replace must NEVER touch these

- `RFE_FILTER = 'issuetype = "Feature Request" AND resolution = Unresolved'` (triage.py)
- `DEFAULT_REF_TYPES = ["Outcome", "Feature"]` (hub_jira.py)
- `ref_types:` values (`Outcome`, `Feature`, `Feature Request`) in components.yaml
- The words `Feature` / `Feature Request` / `Outcome` wherever they name **Jira issue types** — in JQL strings, prose, skill docs, views
- External URLs containing `features` (e.g. github.com paths)
- `docs/plans/*`, `docs/specs/*` (dated historical records — links get mechanically rewritten, prose stays), `docs/history.md` prose, `docs/superpowers/**` (the spec/plan for THIS change)

---

### Task 1: Atomic mechanical rename (structure + code + tests + links)

**Files:**
- Rename: `features/` → `components/`, `restricted/features/` → `restricted/components/`, `features/features.yaml` → `components/components.yaml`
- Modify (code): `scripts/hublib/schema.py`, `indexer.py`, `jiramap.py`, `triage.py`, `triage_html.py`, `disclosure.py`, `publisher.py`, `refresh.py`, `status.py`, `scripts/hub_jira.py`, `scripts/hub_triage.py`
- Modify (tests): `scripts/tests/test_schema.py`, `test_indexer.py`, `test_publisher.py`, `test_refresh.py`, `test_disclosure.py`, `test_jiramap.py`, `test_hub_triage.py`, `test_hub_jira.py`, `test_status.py`, `test_triage.py`, `test_triage_html.py`
- Modify (content, scripted): every tracked `*.md|yaml|yml|py|txt|json|html|js|css` incl. `publish/manifest.yaml`, `.claude/skills/**`, `.github/workflows/*`, `restricted/**`
- Regenerate: all indexes and `views/*`

**Interfaces:**
- Consumes: nothing (first task).
- Produces: the renamed tree + renamed public API later tasks rely on: `components/components.yaml` with top key `components:`; `schema._component_ids(base)`; `schema._lint_routing_table(root, errors, warnings)` (name unchanged, now reads components.yaml); frontmatter key `components:`; snapshot key `component:`; CLI `hub_jira.py --sweep <component>`, `hub_triage.py --scan <component> / --component`.

- [ ] **Step 1: Preflight** — `git checkout -b components-rename`; verify git-crypt unlocked (see Global Constraints); run the verification trio to confirm the baseline is green (record the warning count — expected 120). Also record the Jira-vocab baseline: `git grep -in 'feature request' | wc -l`.

- [ ] **Step 2: git mv** (order matters — yaml rename after the dir move):

```bash
git mv features components
git mv components/features.yaml components/components.yaml
git mv restricted/features restricted/components
```

- [ ] **Step 3: Write the rewrite script** to the session scratchpad (NOT the repo) as `rename_components.py`, exactly:

```python
"""One-off: rewrite feature->component paths/keys in tracked text files.
Run from repo root AFTER the git mv steps."""
import re, subprocess
from pathlib import Path

EXCLUDE_PREFIXES = ("docs/superpowers/",)
EXT = {".md", ".yaml", ".yml", ".py", ".txt", ".json", ".html", ".js", ".css"}

RULES = [
    # leading-slash repo links / abs paths; \1 preserves the delimiter.
    # Delimiter guard skips external URLs (their /features/ follows an alnum path char).
    (re.compile(r'(^|[\s|>("\'`\[=])/features/'), r"\1/components/"),
    # repo-relative paths (yaml source:, table cells, py glob strings)
    (re.compile(r'(^|[\s|>("\'`\[=])features/'), r"\1components/"),
    # frontmatter / yaml top-level key at column 0
    (re.compile(r"^features:", re.M), "components:"),
]
SNAP_RULE = (re.compile(r"^feature:", re.M), "component:")

files = subprocess.run(["git", "ls-files"], capture_output=True, text=True,
                       check=True).stdout.splitlines()
changed = 0
for rel in files:
    p = Path(rel)
    if rel.startswith(EXCLUDE_PREFIXES) or p.suffix.lower() not in EXT:
        continue
    try:
        text = p.read_bytes().decode("utf-8")   # bytes: preserve CRLF exactly
    except (UnicodeDecodeError, FileNotFoundError):
        continue  # locked git-crypt blob or gone — never rewrite ciphertext
    orig = text
    for rx, sub in RULES:
        text = rx.sub(sub, text)
    if p.name == "jira-snapshot.yaml" or p.name.startswith("triage-log"):
        text = SNAP_RULE[0].sub(SNAP_RULE[1], text)
    if text != orig:
        p.write_bytes(text.encode("utf-8"))
        changed += 1
print(f"rewrote {changed} files")
```

- [ ] **Step 4: Run it** — `python <scratchpad>/rename_components.py` from repo root. Then spot-check the PRESERVE list survived: `git grep -in 'feature request' | wc -l` equals the Step 1 baseline; `git grep -n 'DEFAULT_REF_TYPES'` still shows `["Outcome", "Feature"]`; `git grep -n 'https\?://[^ ]*components/'` — any hit is a corrupted external URL: revert that line by hand to `features`.

- [ ] **Step 5: Hand-edit the hublib modules** per the rename + message tables. File-by-file checklist (line refs are pre-edit):
  - `schema.py`: `_feature_ids`→`_component_ids` (+ path, docstring); `_lint_routing_table` internals (path, `data.get("components")` after script, messages); `_check_features`→`_check_components` (+ `meta.get("components")`, param `component_ids`, messages); `TYPE_EXTRA_REQUIRED["story"] = ("components",)`; `_lint_tree` (`base / "components"`, local var, skeleton messages); `_lint_links` `scan_dirs` `"features"`→`"components"`; `lint_repo` wiring; comments at lines 11 and 46; every `feature_ids=` kwarg → `component_ids=`.
  - `indexer.py`: `_load_entries(base="components")`; `_home` (`parts[1] == "components"`, docstring); `_features_table`→`_components_table`; `m.get("components")` (three sites); headings `# Features`→`# Components`; empty-state string; `desc.get("components")` (artifacts view); line 239 `cross-feature stories`→`cross-component stories`; glob strings already rewritten by script — verify.
  - `jiramap.py`: docstring; `SNAPSHOT_GLOB` (script-rewritten — verify); `build_snapshot(component_id, ...)` writing `"component":`; `validate` mismatch check `data.get("component")` + message; `scan("*/knowledge/*.md", "components")`.
  - `triage.py`: `compose_jql(component_jql)`; `build_triage_log(component, ...)` + doc key `"component":`; line 126 comment → `cloned into a RHAISTRAT Feature` (Jira type — keep the word, capitalize); `RFE_FILTER` UNTOUCHED.
  - `triage_html.py`: `render(component, ...)`; `data-feature=`→`data-comp=`; JS `document.body.dataset.feature`→`dataset.comp`; title/h1 interpolations follow the param rename.
  - `disclosure.py`, `publisher.py` (`_feature_titles`→`_component_titles`, `parts[0] == "components"`), `refresh.py` (`CONFIG_GLOBS`, `parts[0] == "components"`, site message), `status.py`: glob strings script-rewritten — verify + rename identifiers/comparisons.
  - `hub_jira.py`: usage text; `_jira_cfg(root, component)` (+ path, docstring, messages); `_sweep`/`_sync` params + snapshot paths + output names `jira-snapshot-{component}.yaml` / `candidates-{component}.yaml`; metavars `COMPONENT`; `DEFAULT_REF_TYPES` UNTOUCHED.
  - `hub_triage.py`: usage text; `_jira_cfg`; `_scan`/`_apply` params + report/rows filenames; `--feature`→`--component` (`args.component`); error string in the `ap.error` line; metavars.

- [ ] **Step 6: Update the 11 test files.** The script already rewrote quoted `features/...` fixture paths. Remaining hand edits per the tables: `FEATURES_YAML`→`COMPONENTS_YAML` and its content string `"components:\n- id: ..."`; fixture frontmatter extras `features: [...]`→`components: [...]`; snapshot fixture key `feature: x`→`component: x` (test_schema line 496, test_jiramap); every assertion string per the message table; imported/called identifiers per the rename table; CLI invocations `--feature`→`--component`; rename test functions whose names say feature (e.g. `test_known_feature_ids_pass`→`test_known_component_ids_pass`, `test_story_requires_features`→`test_story_requires_components`, `test_pillar_and_story_invalid_under_features`→`..._under_components`).

- [ ] **Step 7: Run pytest** — `python -m pytest scripts/tests -q`. Expected: all pass. Fix any straggler the tables missed (they will name themselves in failures).

- [ ] **Step 8: Regenerate + lint** — `python scripts/hub_index.py` then the full verification trio. Expected: 0 errors, warnings == 120, 0 stale. A warning-count delta means a rewrite side-effect — diff-inspect and fix before proceeding.

- [ ] **Step 9: Review the diff for the two failure modes** — `git diff --stat` then targeted looks: (a) `git grep -n 'features/'` — every remaining hit must be an external URL, a PRESERVE path, or docs/superpowers; (b) `git grep -in 'feature request'` — count must equal baseline.

- [ ] **Step 10: Commit** (single atomic commit):

```bash
git add -A
git commit -m "refactor(components)!: rename features/ layer to components/ across structure, code, and links"
```

---

### Task 2: Lint validation for jira_component / jira_labels (TDD)

**Files:**
- Modify: `scripts/hublib/schema.py` (inside `_lint_routing_table`)
- Test: `scripts/tests/test_schema.py`

**Interfaces:**
- Consumes: Task 1's renamed `_lint_routing_table`, `COMPONENTS_YAML` helper, `write()`/`make_repo()` fixtures, `lint_repo(root)` entrypoint.
- Produces: components.yaml entries may carry `jira_component: <str>` and `jira_labels: [<lowercase str>...]`; violations are errors formatted `components/components.yaml[<id>]: ...` (Task 3 relies on these fields passing lint).

- [ ] **Step 1: Write the failing tests** (append to test_schema.py):

```python
def test_jira_component_and_labels_valid(tmp_path):
    root = make_repo(tmp_path)
    write(root, "components/components.yaml",
          "components:\n- id: mcp-catalog\n  title: C\n  description: d\n"
          "  jira_component: AI Hub\n  jira_labels: [mcp-catalog]\n")
    errors, _ = lint_repo(root)
    assert errors == []


def test_jira_component_must_be_string(tmp_path):
    root = make_repo(tmp_path)
    write(root, "components/components.yaml",
          "components:\n- id: mcp-catalog\n  title: C\n  description: d\n"
          "  jira_component: [AI Hub]\n")
    errors, _ = lint_repo(root)
    assert any("jira_component must be a string" in e for e in errors)


def test_jira_labels_must_be_list(tmp_path):
    root = make_repo(tmp_path)
    write(root, "components/components.yaml",
          "components:\n- id: mcp-catalog\n  title: C\n  description: d\n"
          "  jira_labels: mcp-catalog\n")
    errors, _ = lint_repo(root)
    assert any("jira_labels must be a list of strings" in e for e in errors)


def test_jira_labels_uppercase_is_error(tmp_path):
    root = make_repo(tmp_path)
    write(root, "components/components.yaml",
          "components:\n- id: mcp-catalog\n  title: C\n  description: d\n"
          "  jira_labels: [MCP-Catalog]\n")
    errors, _ = lint_repo(root)
    assert any("jira_labels 'MCP-Catalog' must be lowercase" in e for e in errors)
```

- [ ] **Step 2: Run them to verify they fail** — `python -m pytest scripts/tests/test_schema.py -q -k jira_component or jira_labels` adjusted to `-k "jira_component or jira_labels"`. Expected: the three negative tests FAIL (no such errors emitted yet); the valid-case test may already pass.

- [ ] **Step 3: Implement** — in `_lint_routing_table`, inside the `for f in comps:` loop (after the `related` handling), add:

```python
        jc = f.get("jira_component")
        if jc is not None and not isinstance(jc, str):
            errors.append(f"{where}: jira_component must be a string")
        jl = f.get("jira_labels")
        if jl is not None:
            if not isinstance(jl, list) or not all(isinstance(x, str) for x in jl):
                errors.append(f"{where}: jira_labels must be a list of strings")
            else:
                for lab in jl:
                    if lab != lab.lower():
                        errors.append(f"{where}: jira_labels '{lab}' must be lowercase")
```

Note: `where` is only defined inside the existing related-handling block pre-edit — hoist `where = f"components/components.yaml[{f.get('id')}]"` to the top of the loop so both blocks share it.

- [ ] **Step 4: Run the full suite** — `python -m pytest scripts/tests -q`. Expected: all pass.

- [ ] **Step 5: Commit** — `git add scripts/hublib/schema.py scripts/tests/test_schema.py && git commit -m "feat(lint): validate jira_component and jira_labels in components.yaml"`

---

### Task 3: Populate Jira metadata in components.yaml

**Files:**
- Modify: `components/components.yaml`

**Interfaces:**
- Consumes: Task 2's validation.
- Produces: the owner-confirmed mapping data; nothing downstream in this plan reads it yet.

- [ ] **Step 1: Add exactly these fields** (each after the entry's `description:`/`related:` lines, before any `jira:` block): `mcp-catalog`: `jira_component: AI Hub` + `jira_labels: [mcp-catalog]` · `mcp-registry`: `jira_component: AI Hub` + `jira_labels: [mcp-registry]` · `mcp-gateway`: `jira_labels: [mcp-gateway]` · `agent-catalog`: `jira_component: AI Hub` · `agent-registry`: `jira_component: AI Hub`. No other entries get fields (unconfirmed).
- [ ] **Step 2: Update the file's header comment** to document both fields in one line each (loose Jira-component mapping; lowercase labels).
- [ ] **Step 3: Verify** — full trio green.
- [ ] **Step 4: Commit** — `git add components/components.yaml && git commit -m "chore(components): record jira_component and jira_labels mappings"`

---

### Task 4: Skills prose sweep

**Files:**
- Modify: every file under `.claude/skills/` that still says feature-meaning-partition (find with `grep -rin feature .claude/skills`)

**Interfaces:**
- Consumes: Task 1's renamed paths/flags (already mechanically rewritten in these files).
- Produces: skill docs whose prose matches the new vocabulary; no code contract.

- [ ] **Step 1: Enumerate** — `grep -rin feature .claude/skills` and classify every hit: (a) Jira issue type (`Feature`, `Feature Request`, RFE contexts) → KEEP; (b) partition-meaning ("feature area", "per-feature", "the feature's strategy doc", "feature partition") → rewrite to component wording; (c) stale CLI references — hub.jira-triage's `--feature` flag examples → `--component` (verify against `python scripts/hub_triage.py --help`).
- [ ] **Step 2: Rewrite** each (b)/(c) hit in place, sentence by sentence — no blind sed; the same word can be both meanings in one paragraph.
- [ ] **Step 3: Verify** — re-run the grep: remaining hits are all class (a). Full trio green (skills aren't linted, but the trio guards regressions).
- [ ] **Step 4: Commit** — `git add .claude/skills && git commit -m "docs(skills): component terminology sweep"`

---

### Task 5: Docs, conventions, AGENTS/CLAUDE + vocabulary contract

**Files:**
- Modify: `AGENTS.md`, `CLAUDE.md`, `README.md`, `conventions/*.md`, `conventions/staleness.yaml`, `docs/*.md` (top level only — NOT `docs/plans/`, `docs/specs/`, `docs/superpowers/`)

**Interfaces:**
- Consumes: Task 1 renamed paths in these files already.
- Produces: the vocabulary contract in `conventions/layout.md` that Tasks 6–7 apply when classifying prose.

- [ ] **Step 1: Add the contract** to `conventions/layout.md` as a new section:

```markdown
## Vocabulary: components and features

- A **component** is an item in `components/` — a thing that exists in
  RHOAI (MCP Gateway, Agent Catalog, ...). Partitions under
  `components/` are component partitions.
- A **feature** is functionality added to a component (what a RHAISTRAT
  Feature ticket describes). The hub does not model features
  structurally; the word is reserved for that meaning.
- Components map loosely to **Jira components** — not 1:1 (the catalogs
  and registries land in the "AI Hub" Jira component). The mapping
  lives in `components/components.yaml` as `jira_component:`.
- Components have (or can create) **Jira labels** — always lowercase
  (e.g. `mcp-catalog`), stored as `jira_labels:`; lint enforces case.
- Jira issue types keep their own names: `Feature` and `Feature Request`
  in JQL, `ref_types:`, and prose always mean the Jira issue types.
```

- [ ] **Step 2: Sweep prose** — `grep -rin feature AGENTS.md CLAUDE.md README.md conventions docs --include=*.md --include=*.yaml`, classify per the contract, rewrite partition-meaning hits (e.g. AGENTS.md map row, "feature families", type-vocabulary wording). Skip `docs/plans|specs|superpowers`. Keep Jira-type hits.
- [ ] **Step 3: History note** — append to `docs/history.md`: `- 2026-07-31 — features/ layer renamed to components/ (components are RHOAI components; "feature" now reserved for functionality added to a component). Spec: /docs/superpowers/specs/2026-07-31-components-rename-design.md`.
- [ ] **Step 4: Verify** — trio green; AGENTS.md still ≤ 150 lines (lint enforces).
- [ ] **Step 5: Commit** — `git add AGENTS.md CLAUDE.md README.md conventions docs && git commit -m "docs(conventions): component vocabulary contract + terminology sweep"`

---

### Task 6: Memory store + content-body prose sweep

**Files:**
- Modify: `memory/profiles/*.md`, `memory/facts/*.md`, `memory/log.md`, body prose under `components/**`, `narrative/**`, `restricted/components/**`, `restricted/work/**`

**Interfaces:**
- Consumes: the Task 5 contract for classification.
- Produces: nothing downstream; final content state.

- [ ] **Step 1: Memory profiles** — `grep -in feature memory/profiles/*.md`; rewrite partition-meaning hits in place and append one `## History` line to each edited profile: `- 2026-07-31 — terminology: feature → component (repo-wide rename).` (Profiles update in place + History, per conventions/memory.md. These edits ride the reviewed rename branch — that review is the gate for this batch.)
- [ ] **Step 2: Memory facts + log** — same grep-classify-rewrite over `memory/facts/` and `memory/log.md`. Historical log lines get the terminology swap too (full rename: no stale meaning survives).
- [ ] **Step 3: Content bodies** — `grep -rin '\bfeature' components narrative restricted --include=*.md`, one directory at a time. Classify per the contract; rewrite partition-meaning prose ("this feature's roadmap" → "this component's roadmap"). KEEP Jira-type uses (very common in ref-/jira prose) and quoted titles of external sources.
- [ ] **Step 4: Verify** — `python scripts/hub_index.py` (descriptions flow into generated views), then full trio green.
- [ ] **Step 5: Commit** — `git add -A && git commit -m "chore(memory,content): component terminology sweep in memory store and entry prose"`

---

### Task 7: Residual audit + final verification

**Files:**
- Modify: only stragglers the audit finds.

**Interfaces:**
- Consumes: everything prior.
- Produces: the audited, mergeable branch.

- [ ] **Step 1: Audit** — `git grep -in feature -- ':!docs/plans' ':!docs/specs' ':!docs/superpowers' ':!docs/history.md'`. Every hit must match the PRESERVE list (Jira issue types, external URLs/titles). Anything else is a defect — fix it.
- [ ] **Step 2: Path audit** — `git grep -n 'features/'` (same exclusions): only external URLs may remain.
- [ ] **Step 3: Final verification** — regenerate (`python scripts/hub_index.py`) + full trio green; `git log --oneline main..HEAD` shows the expected commit series.
- [ ] **Step 4: Commit fixes** (if any) — `git add -A && git commit -m "chore(components): residual feature-term audit fixes"`.
- [ ] **Step 5: Hand off** to superpowers:finishing-a-development-branch for the merge-to-main decision (merging republishes via publish.yml; dests are unchanged so public URLs are stable).
