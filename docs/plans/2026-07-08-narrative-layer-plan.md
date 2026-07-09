# Narrative Layer & Connection Axis — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the hub's second axis per the approved spec (`/docs/specs/2026-07-08-narrative-layer-design.md`): a top-level `narrative/` tree, a validated `features:` cross-reference field, new entry types (`pillar`, `story`, `qa`, `jtbd`, `artifact`), four generated views, updated conventions/docs/skills, and a gated seed batch.

**Architecture:** Extend the two existing enforcement surfaces — `scripts/hublib/schema.py` (lint contract) and `scripts/hublib/indexer.py` (deterministic generation) — with the narrative tree treated exactly like a feature partition (same skeleton, wider type set). Connections are *declared* in frontmatter (`features:`) and *rendered* by generation, never hand-maintained. Zero new skills; classifier text extensions only.

**Tech Stack:** Python 3.11+ (stdlib + `pyyaml`), `pytest`, bash (Git Bash on Windows), markdown/YAML-frontmatter entries.

## Global Constraints

- Repo is **PUBLIC** — every tracked write is world-readable; restricted bar per `/conventions/memory.md`.
- Windows + Git Bash: invoke `python` (never `python3`); write files with LF (`newline="\n"` — the `write()` test helper and `write_all` already do this).
- Generated files carry `MARKER` and are never hand-edited; after any entry/generator change run `python scripts/hub_index.py` and **commit the regenerated files in the same commit** (CI fails on stale).
- Full gate before every commit: `python -m pytest scripts/tests -q` (all pass) · `python scripts/hub_lint.py` (0 errors) · `python scripts/hub_index.py --check` (0 stale).
- Budgets: `AGENTS.md` ≤ 150 lines, `memory/index.md` ≤ 200 lines (lint-enforced).
- Commit style: `feat(schema)|feat(indexer)|docs|feat(skills)|know(narrative)` prefixes as given per task; push after each task (`git push origin main`; if rejected, `git fetch && git pull --rebase origin main`, re-run the verification gate, then push — the owner works from a second machine).
- Task 10 (seed) is **owner-gated**: present the batch, wait for rulings, never apply unapproved items.
- No new skills; no `publish/manifest.yaml` changes anywhere in this plan.

## File Structure

| file | responsibility |
|---|---|
| `scripts/hublib/schema.py` | lint contract: vocabularies, prefixes, per-type enums, `features:`/`asks:`/persona validation, narrative-tree + artifact-descriptor lint |
| `scripts/hublib/indexer.py` | generation: narrative indexes, shared-view inclusion, Connections sections, 4 new views |
| `scripts/tests/test_schema.py` | schema regression tests (extend) |
| `scripts/tests/test_indexer.py` | indexer regression tests (extend) |
| `conventions/layout.md`, `conventions/type-vocabulary.md`, `conventions/memory.md` | the normative rulebook (extend) |
| `docs/architecture.md`, `AGENTS.md`, `README.md`, `docs/working-here.md`, `docs/skills.md` | guides (extend) |
| `.claude/skills/{hub.capture,hub.file,hub.consolidate,hub.migrate}/SKILL.md` | routing/classifier text (extend) |
| `narrative/knowledge/*.md`, `features/platform/knowledge/*`, `features/features.yaml`, `memory/log.md` | Task 10 seed content (owner-gated) |

---

### Task 1: Schema — new types, prefixes, per-type status enums, persona + asks validation

**Files:**
- Modify: `scripts/hublib/schema.py` (constants block lines 10–29; status block in `lint_entry` lines 89–95)
- Test: `scripts/tests/test_schema.py`

**Interfaces:**
- Consumes: existing `lint_repo(root)`, `lint_entry(...)`, `ENTRY`/`write`/`make_repo` test helpers.
- Produces: constants `KNOWLEDGE_TYPES` (now incl. `qa`, `jtbd`), `NARRATIVE_TYPES`, `PERSONAS`, `ASK_BY`, `STATUS_ENUMS`, `DEFAULT_STATUS_ENUM` — Tasks 2–3 extend the same file; Task 3 uses `NARRATIVE_TYPES`.

- [ ] **Step 1: Write the failing tests** — append to `scripts/tests/test_schema.py`:

```python
QA = ("---\ntype: qa\ndescription: d\ntimestamp: 2026-07-08\nstatus: answered\n"
      "asks:\n- date: 2026-07-08\n  by: customer\n---\n## Question\nq\n## Answer\na\n")


def test_qa_entry_valid(tmp_path):
    root = make_repo(tmp_path)
    write(root, "features/x/knowledge/qa-airgap.md", QA)
    errors, _ = lint_repo(root)
    assert errors == []


def test_qa_missing_asks_is_error(tmp_path):
    root = make_repo(tmp_path)
    write(root, "features/x/knowledge/qa-airgap.md",
          "---\ntype: qa\ndescription: d\ntimestamp: 2026-07-08\nstatus: answered\n---\nb\n")
    errors, _ = lint_repo(root)
    assert any("requires field 'asks'" in e for e in errors)


def test_qa_bad_ask_by_is_error(tmp_path):
    root = make_repo(tmp_path)
    write(root, "features/x/knowledge/qa-airgap.md",
          "---\ntype: qa\ndescription: d\ntimestamp: 2026-07-08\nstatus: answered\n"
          "asks:\n- date: 2026-07-08\n  by: random-person\n---\nb\n")
    errors, _ = lint_repo(root)
    assert any("asks[0].by must be" in e for e in errors)


def test_qa_status_uses_question_enum(tmp_path):
    root = make_repo(tmp_path)
    write(root, "features/x/knowledge/qa-airgap.md",
          "---\ntype: qa\ndescription: d\ntimestamp: 2026-07-08\nstatus: current\n"
          "asks:\n- date: 2026-07-08\n  by: sales\n---\nb\n")
    errors, _ = lint_repo(root)
    assert any("status must be open|answered" in e for e in errors)


def test_jtbd_entry_valid(tmp_path):
    root = make_repo(tmp_path)
    write(root, "features/x/knowledge/jtbd-find-approved-servers.md",
          "---\ntype: jtbd\ndescription: d\ntimestamp: 2026-07-08\n"
          "persona: ai-engineer\nstatus: candidate\n---\n## Job\nWhen …\n")
    errors, _ = lint_repo(root)
    assert errors == []


def test_jtbd_bad_persona_is_error(tmp_path):
    root = make_repo(tmp_path)
    write(root, "features/x/knowledge/jtbd-a.md",
          "---\ntype: jtbd\ndescription: d\ntimestamp: 2026-07-08\n"
          "persona: wizard\nstatus: candidate\n---\nb\n")
    errors, _ = lint_repo(root)
    assert any("persona must be one of" in e for e in errors)


def test_jtbd_status_enum(tmp_path):
    root = make_repo(tmp_path)
    write(root, "features/x/knowledge/jtbd-a.md",
          "---\ntype: jtbd\ndescription: d\ntimestamp: 2026-07-08\n"
          "persona: data-scientist\nstatus: open\n---\nb\n")
    errors, _ = lint_repo(root)
    assert any("status must be candidate|validated|delivered|retired" in e for e in errors)


def test_pillar_and_story_invalid_under_features(tmp_path):
    root = make_repo(tmp_path)
    write(root, "features/x/knowledge/pillar-agents.md", ENTRY.format(t="pillar", extra=""))
    errors, _ = lint_repo(root)
    assert any("type 'pillar' not in vocabulary" in e for e in errors)
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd /c/Users/peter/code/rh/rhoai-agentic-hub && python -m pytest scripts/tests/test_schema.py -q`
Expected: the 8 new tests FAIL (`type 'qa' not in vocabulary …` errors making `errors == []` assertions fail, and missing-message assertions fail); the 13 pre-existing tests still PASS.

- [ ] **Step 3: Implement.** In `scripts/hublib/schema.py`, replace the constants block (currently lines 10–27, `KNOWLEDGE_TYPES` through `TYPE_EXTRA_REQUIRED`) with:

```python
KNOWLEDGE_TYPES = {"decision", "fact", "reference", "person", "question", "qa", "jtbd"}
# pillar/story are narrative-layer-only (spec D12/D14) — invalid under features/.
NARRATIVE_TYPES = KNOWLEDGE_TYPES | {"pillar", "story"}
MEMORY_TYPES = {"profile", "fact", "preference", "feedback"}
PREFIX_TO_TYPE = {
    "decision-": "decision",
    "fact-": "fact",
    "ref-": "reference",
    "person-": "person",
    "question-": "question",
    "qa-": "qa",
    "jtbd-": "jtbd",
    "pillar-": "pillar",
    "story-": "story",
}
SKELETON_DIRS = {"knowledge", "research", "strategy", "enablement", "work"}
RESERVED = {"index.md", "log.md"}
REQUIRED_BASE = ("type", "description", "timestamp")
TYPE_EXTRA_REQUIRED = {
    "reference": ("resource",),
    "decision": ("decided",),
    "person": ("role", "org"),
    "question": ("status",),
    "qa": ("status", "asks"),
    "jtbd": ("persona", "status"),
    "story": ("features",),
}
# Per-type status enums (canonical order — used verbatim in messages).
STATUS_ENUMS = {
    "question": ("open", "answered"),
    "qa": ("open", "answered"),
    "jtbd": ("candidate", "validated", "delivered", "retired"),
}
DEFAULT_STATUS_ENUM = ("current", "superseded")
# Locked JTBD persona vocabulary — source of truth:
# features/platform/knowledge/fact-personas.md. Extend BOTH together (gated).
PERSONAS = ("ai-engineer", "platform-engineer", "agentops-admin",
            "business-consumer", "data-scientist", "cluster-admin", "rhoai-admin")
# qa asks[].by role buckets (spec §5.3, owner-confirmed).
ASK_BY = ("customer", "partner", "sales", "ssa", "pm", "eng", "exec", "other")
```

Then in `lint_entry`, replace the status block (currently):

```python
    if etype == "question":
        if meta.get("status") not in (None, "open", "answered"):
            errors.append(f"{rel}: question status must be open|answered")
    elif meta.get("status") not in (None, "current", "superseded"):
        errors.append(f"{rel}: status must be current|superseded")
```

with:

```python
    enum = STATUS_ENUMS.get(etype, DEFAULT_STATUS_ENUM)
    if meta.get("status") not in (None, *enum):
        errors.append(f"{rel}: status must be {'|'.join(enum)}")
    if etype == "qa" and meta.get("asks") is not None:
        asks = meta["asks"]
        if not isinstance(asks, list) or not asks:
            errors.append(f"{rel}: asks must be a non-empty list")
        else:
            for i, item in enumerate(asks):
                if not isinstance(item, dict) or not item.get("date") or not item.get("by"):
                    errors.append(f"{rel}: asks[{i}] needs 'date' and 'by'")
                elif str(item["by"]) not in ASK_BY:
                    errors.append(f"{rel}: asks[{i}].by must be {'|'.join(ASK_BY)}")
    if etype == "jtbd" and meta.get("persona") is not None:
        if str(meta["persona"]) not in PERSONAS:
            errors.append(f"{rel}: persona must be one of {'|'.join(PERSONAS)}")
```

(The existing `superseded_by` warning line directly after stays unchanged.)

- [ ] **Step 4: Run the full suite**

Run: `python -m pytest scripts/tests -q`
Expected: all pass (21 in test_schema, 6 in test_indexer, plus frontmatter/publisher suites — 42 total).
Also run: `python scripts/hub_lint.py` → `0 error(s)` (live repo has no new-type entries yet) and `python scripts/hub_index.py --check` → 0 stale.

- [ ] **Step 5: Commit and push**

```bash
git add scripts/hublib/schema.py scripts/tests/test_schema.py
git commit -m "feat(schema): qa/jtbd/pillar/story types, per-type status enums, persona + asks validation

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
git push origin main
```

---

### Task 2: Schema — `features:` cross-reference validation + story `pillar:` dangling warning

**Files:**
- Modify: `scripts/hublib/schema.py` (`lint_entry` signature + body; `_lint_tree`; `lint_repo`; new helpers)
- Test: `scripts/tests/test_schema.py`

**Interfaces:**
- Consumes: Task 1 constants.
- Produces: `lint_entry(root, path, allowed_types, check_prefix, errors, warnings, feature_ids=None)` (new kwarg), `_feature_ids(base) -> set`, `_check_features(rel, meta, feature_ids, errors)` — Task 3 passes `feature_ids` through for narrative/artifact entries.

- [ ] **Step 1: Write the failing tests** — append to `scripts/tests/test_schema.py`:

```python
FEATURES_YAML = ("features:\n- id: mcp-registry\n  title: R\n  description: d\n"
                 "- id: mcp-gateway\n  title: G\n  description: d\n")


def test_known_feature_ids_pass(tmp_path):
    root = make_repo(tmp_path)
    write(root, "features/features.yaml", FEATURES_YAML)
    write(root, "features/mcp-registry/knowledge/fact-a.md",
          ENTRY.format(t="fact", extra="features: [mcp-registry, mcp-gateway]\n"))
    errors, _ = lint_repo(root)
    assert errors == []


def test_unknown_feature_id_is_error(tmp_path):
    root = make_repo(tmp_path)
    write(root, "features/features.yaml", FEATURES_YAML)
    write(root, "features/mcp-registry/knowledge/fact-a.md",
          ENTRY.format(t="fact", extra="features: [mcp-registry, made-up]\n"))
    errors, _ = lint_repo(root)
    assert any("unknown feature id 'made-up'" in e for e in errors)


def test_features_must_be_a_list(tmp_path):
    root = make_repo(tmp_path)
    write(root, "features/features.yaml", FEATURES_YAML)
    write(root, "features/mcp-registry/knowledge/fact-a.md",
          ENTRY.format(t="fact", extra="features: mcp-registry\n"))
    errors, _ = lint_repo(root)
    assert any("features must be a list" in e for e in errors)


def test_features_on_memory_file_is_error(tmp_path):
    root = make_repo(tmp_path)
    write(root, "memory/facts/fact-a.md",
          "---\ntype: fact\ndescription: d\ntimestamp: 2026-07-08\n"
          "features: [mcp-registry]\n---\nb\n")
    errors, _ = lint_repo(root)
    assert any("only allowed on knowledge entries" in e for e in errors)
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python -m pytest scripts/tests/test_schema.py -q`
Expected: `test_unknown_feature_id_is_error`, `test_features_must_be_a_list`, `test_features_on_memory_file_is_error` FAIL (no such messages yet); `test_known_feature_ids_pass` passes trivially (no validation yet) — that's fine, it pins the happy path.

- [ ] **Step 3: Implement.** In `scripts/hublib/schema.py`:

Add after `_check_resource` (module level):

```python
def _feature_ids(base):
    """Known feature ids from features/features.yaml (the closed routing table)."""
    p = base / "features" / "features.yaml"
    if not p.is_file():
        return set()
    try:
        data = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError:
        return set()
    return {f.get("id") for f in (data.get("features") or []) if isinstance(f, dict)}


def _check_features(rel, meta, feature_ids, errors):
    """features: cross-refs — closed vocabulary, unlike dangling links (spec D13)."""
    feats = meta.get("features")
    if feats is None:
        return
    if feature_ids is None:
        errors.append(f"{rel}: features: is only allowed on knowledge entries "
                      f"and artifact descriptors")
        return
    if not isinstance(feats, list) or not all(isinstance(x, str) for x in feats):
        errors.append(f"{rel}: features must be a list of feature ids")
        return
    for fid in feats:
        if fid not in feature_ids:
            errors.append(f"{rel}: unknown feature id '{fid}' "
                          f"(not in features/features.yaml)")
```

Change `lint_entry`'s signature line to:

```python
def lint_entry(root, path, allowed_types, check_prefix, errors, warnings, feature_ids=None):
```

and append at the end of `lint_entry` (after the restricted-hints check):

```python
    _check_features(rel, meta, feature_ids, errors)
    if etype == "story" and meta.get("pillar"):
        target = str(meta["pillar"])
        if not (root / target.lstrip("/")).exists():
            warnings.append(f"{rel}: pillar target {target} does not exist (dangling)")
```

Change `_lint_tree`'s signature to `def _lint_tree(root, base, errors, warnings, feature_ids):`, its knowledge call to `lint_entry(root, entry, KNOWLEDGE_TYPES, True, errors, warnings, feature_ids=feature_ids)`, and its memory call to `lint_entry(root, entry, MEMORY_TYPES, False, errors, warnings, feature_ids=None)`.

In `lint_repo`, before the `_lint_tree` calls insert `feature_ids = _feature_ids(root)` and pass it to both calls (`_lint_tree(root, root, errors, warnings, feature_ids)` and the restricted one — restricted mirrors use the **public** routing table by design).

- [ ] **Step 4: Run the full suite**

Run: `python -m pytest scripts/tests -q` → all pass. `python scripts/hub_lint.py` → 0 errors. `python scripts/hub_index.py --check` → 0 stale.

- [ ] **Step 5: Commit and push**

```bash
git add scripts/hublib/schema.py scripts/tests/test_schema.py
git commit -m "feat(schema): features: cross-reference validation + story pillar dangling warning

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
git push origin main
```

---

### Task 3: Schema — narrative tree lint + enablement artifact descriptors + link scan

**Files:**
- Modify: `scripts/hublib/schema.py` (`_lint_tree`, `_lint_links`, new `_lint_artifacts`)
- Test: `scripts/tests/test_schema.py`

**Interfaces:**
- Consumes: `NARRATIVE_TYPES` (Task 1), `feature_ids` plumbing (Task 2).
- Produces: `narrative/` linted with the feature skeleton contract; `*/enablement/<slug>/artifact.md` linted with `allowed_types={"artifact"}`, `check_prefix=False` — Task 10's seed content must satisfy this.

- [ ] **Step 1: Write the failing tests** — append to `scripts/tests/test_schema.py`:

```python
def test_narrative_story_and_pillar_valid(tmp_path):
    root = make_repo(tmp_path)
    write(root, "features/features.yaml", FEATURES_YAML)
    write(root, "narrative/knowledge/pillar-agents.md", ENTRY.format(t="pillar", extra=""))
    write(root, "narrative/knowledge/story-governed-mcp.md",
          ENTRY.format(t="story",
                       extra="features: [mcp-registry, mcp-gateway]\n"
                             "pillar: /narrative/knowledge/pillar-agents.md\n"))
    errors, warnings = lint_repo(root)
    assert errors == []
    assert not any("pillar target" in w for w in warnings)


def test_story_requires_features(tmp_path):
    root = make_repo(tmp_path)
    write(root, "narrative/knowledge/story-a.md", ENTRY.format(t="story", extra=""))
    errors, _ = lint_repo(root)
    assert any("type 'story' requires field 'features'" in e for e in errors)


def test_story_dangling_pillar_is_warning(tmp_path):
    root = make_repo(tmp_path)
    write(root, "features/features.yaml", FEATURES_YAML)
    write(root, "narrative/knowledge/story-a.md",
          ENTRY.format(t="story", extra="features: [mcp-registry]\n"
                                        "pillar: /narrative/knowledge/pillar-gone.md\n"))
    errors, warnings = lint_repo(root)
    assert errors == []
    assert any("pillar target /narrative/knowledge/pillar-gone.md" in w for w in warnings)


def test_stray_dir_under_narrative_is_error(tmp_path):
    root = make_repo(tmp_path)
    write(root, "narrative/stories/a.md", ENTRY.format(t="fact", extra=""))
    errors, _ = lint_repo(root)
    assert any("not part of the narrative skeleton" in e for e in errors)


def test_stray_file_under_narrative_is_error(tmp_path):
    root = make_repo(tmp_path)
    write(root, "narrative/notes.md", "x\n")
    errors, _ = lint_repo(root)
    assert any("files directly under narrative/" in e for e in errors)


def test_artifact_descriptor_valid(tmp_path):
    root = make_repo(tmp_path)
    write(root, "features/features.yaml", FEATURES_YAML)
    write(root, "features/mcp-registry/enablement/deck/index.html", "<html></html>")
    write(root, "features/mcp-registry/enablement/deck/artifact.md",
          ENTRY.format(t="artifact", extra="features: [mcp-gateway]\n"))
    errors, _ = lint_repo(root)
    assert errors == []


def test_artifact_wrong_type_is_error(tmp_path):
    root = make_repo(tmp_path)
    write(root, "features/mcp-registry/enablement/deck/artifact.md",
          ENTRY.format(t="fact", extra=""))
    errors, _ = lint_repo(root)
    assert any("type 'fact' not in vocabulary ['artifact']" in e for e in errors)


def test_artifact_directly_under_enablement_is_error(tmp_path):
    root = make_repo(tmp_path)
    write(root, "features/mcp-registry/enablement/artifact.md",
          ENTRY.format(t="artifact", extra=""))
    errors, _ = lint_repo(root)
    assert any("must live inside an enablement/<slug>/ directory" in e for e in errors)


def test_artifact_assets_are_not_linted(tmp_path):
    root = make_repo(tmp_path)
    write(root, "features/mcp-registry/enablement/deck/README.md", "no frontmatter here\n")
    errors, _ = lint_repo(root)
    assert errors == []
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python -m pytest scripts/tests/test_schema.py -q`
Expected: narrative/artifact tests FAIL (narrative tree unlinted → no errors produced where expected; artifact.md unlinted). `test_artifact_assets_are_not_linted` passes trivially — it pins the non-goal.

- [ ] **Step 3: Implement.** In `scripts/hublib/schema.py`:

Add module-level helper after `_check_features`:

```python
def _lint_artifacts(root, enablement, errors, warnings, feature_ids):
    """artifact.md descriptors inside enablement slug dirs. All other files in
    an artifact directory are the artifact's own assets — never linted."""
    if not enablement.is_dir():
        return
    stray = enablement / "artifact.md"
    if stray.is_file():
        errors.append(f"{_rel(root, stray)}: artifact.md must live inside an "
                      f"enablement/<slug>/ directory")
    for slug in sorted(p for p in enablement.iterdir() if p.is_dir()):
        desc = slug / "artifact.md"
        if desc.is_file():
            lint_entry(root, desc, {"artifact"}, False, errors, warnings,
                       feature_ids=feature_ids)
```

In `_lint_tree`, inside the per-feature loop (after the `know` block), add:

```python
            _lint_artifacts(root, feat / "enablement", errors, warnings, feature_ids)
```

and after the whole `features` block (before the `memory` block), add:

```python
    narrative = base / "narrative"
    if narrative.is_dir():
        for child in sorted(narrative.iterdir()):
            if child.is_dir() and child.name not in SKELETON_DIRS:
                errors.append(f"{_rel(root, child)}: not part of the narrative skeleton "
                              f"({', '.join(sorted(SKELETON_DIRS))})")
            elif child.is_file() and child.name != "index.md":
                errors.append(f"{_rel(root, child)}: files directly under narrative/ "
                              f"are not allowed (only index.md)")
        know = narrative / "knowledge"
        if know.is_dir():
            for entry in sorted(know.glob("*.md")):
                if entry.name in RESERVED:
                    continue
                lint_entry(root, entry, NARRATIVE_TYPES, True, errors, warnings,
                           feature_ids=feature_ids)
        _lint_artifacts(root, narrative / "enablement", errors, warnings, feature_ids)
```

In `_lint_links`, change `scan_dirs` to:

```python
    scan_dirs = ["conventions", "features", "memory", "docs", "views", "narrative"]
```

- [ ] **Step 4: Run the full suite**

Run: `python -m pytest scripts/tests -q` → all pass. `python scripts/hub_lint.py` → 0 errors (live repo: no `narrative/` yet, the one live enablement dir has no `artifact.md` — both correctly silent). `python scripts/hub_index.py --check` → 0 stale.

- [ ] **Step 5: Commit and push**

```bash
git add scripts/hublib/schema.py scripts/tests/test_schema.py
git commit -m "feat(schema): narrative tree lint + enablement artifact descriptors

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
git push origin main
```

---

### Task 4: Indexer — narrative loading, narrative indexes, shared-view inclusion

**Files:**
- Modify: `scripts/hublib/indexer.py` (`_load_entries`, new `_home`, `build_all` restructure)
- Test: `scripts/tests/test_indexer.py`

**Interfaces:**
- Consumes: schema constants unchanged.
- Produces: `_load_entries(root, subdir_glob, base="features")` (new kwarg), `_home(rootpath) -> str` (group label: feature id or `"narrative"`), `entries` list hoisted to the top of `build_all` (Tasks 5–7 read it), generated `narrative/index.md` + `narrative/knowledge/index.md`.

- [ ] **Step 1: Write the failing tests** — append to `scripts/tests/test_indexer.py`:

```python
def add_narrative(root: Path):
    write(root, "narrative/knowledge/pillar-agents.md",
          "---\ntype: pillar\ntitle: Agents\ndescription: control plane pillar\n"
          "timestamp: 2026-07-01\nstatus: current\n---\nb\n")
    write(root, "narrative/knowledge/story-governed-mcp.md",
          "---\ntype: story\ntitle: Governed MCP\ndescription: registry to gateway\n"
          "timestamp: 2026-07-01\nfeatures: [mcp-registry]\n"
          "pillar: /narrative/knowledge/pillar-agents.md\nstatus: current\n---\nb\n")
    write(root, "narrative/knowledge/decision-narrative-home.md",
          "---\ntype: decision\ntitle: Narrative home\ndescription: top-level layer\n"
          "timestamp: 2026-07-02\ndecided: 2026-07-02\nstatus: current\n---\nb\n")
    write(root, "narrative/knowledge/person-joe.md",
          "---\ntype: person\ntitle: Joe Strategist\ndescription: strategy owner\n"
          "timestamp: 2026-07-01\nrole: VP\norg: Red Hat\n---\nb\n")
    return root


def test_narrative_indexes_generated(tmp_path):
    built = build_all(add_narrative(make_repo(tmp_path)), today=TODAY)
    assert "narrative/index.md" in built
    idx = built["narrative/knowledge/index.md"]
    assert "## pillar" in idx and "## story" in idx
    assert "[Governed MCP](/narrative/knowledge/story-governed-mcp.md)" in idx


def test_narrative_entries_reach_shared_views(tmp_path):
    built = build_all(add_narrative(make_repo(tmp_path)), today=TODAY)
    assert "Narrative home" in built["views/decisions.md"]
    assert "- narrative · [Joe Strategist](/narrative/knowledge/person-joe.md)" \
        in built["views/people.md"]


def test_no_narrative_dir_no_narrative_index(tmp_path):
    built = build_all(make_repo(tmp_path), today=TODAY)
    assert "narrative/index.md" not in built


def test_convergence_with_narrative(tmp_path):
    root = add_narrative(make_repo(tmp_path))
    write_all(root, today=TODAY)
    assert check(root, today=TODAY) == []
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python -m pytest scripts/tests/test_indexer.py -q`
Expected: the first two FAIL (`narrative/index.md` missing; narrative decisions/people absent — note the people view would today mislabel the group as `knowledge`). `test_no_narrative_dir_no_narrative_index` passes trivially (pins the guard). `test_convergence_with_narrative` FAILs only if generation is nondeterministic — expect PASS; keep it as the regression pin.

- [ ] **Step 3: Implement.** In `scripts/hublib/indexer.py`:

Replace `_load_entries` with:

```python
def _load_entries(root, subdir_glob, base="features"):
    """Yield (rootpath, meta, body) for knowledge entries matching the glob."""
    basedir = root / base
    if not basedir.is_dir():
        return
    for entry in sorted(basedir.glob(subdir_glob)):
        if entry.name in RESERVED or not entry.is_file():
            continue
        try:
            meta, body = frontmatter.load_file(entry)
        except frontmatter.FrontmatterError:
            continue  # lint reports this; indexes skip unparseable files
        yield "/" + entry.relative_to(root).as_posix(), meta, body
```

Add after `_line`:

```python
def _home(rootpath):
    """Group label for an entry: its feature id, or 'narrative'."""
    parts = rootpath.split("/")
    return parts[2] if parts[1] == "features" else parts[1]
```

In `build_all`, directly after `feats = _features_table(root)`, insert the hoisted load:

```python
    entries = list(_load_entries(root, "*/knowledge/*.md"))
    entries += list(_load_entries(root, "knowledge/*.md", base="narrative"))
```

and DELETE the later line `entries = list(_load_entries(root, "*/knowledge/*.md"))` at the top of the `# views/` section.

After the `memory/index.md` block (before `# views/`), add the narrative indexes:

```python
    # narrative/ indexes (only when the layer exists on disk)
    ndir = root / "narrative"
    if ndir.is_dir():
        lines = [MARKER + "# Narrative", "",
                 "The story layer: pillars, cross-feature stories, and the "
                 "strategy spine.", ""]
        for sub in ("knowledge", "research", "strategy", "enablement", "work"):
            lines.append(f"- [{sub}/](/narrative/{sub}/)")
        built["narrative/index.md"] = "\n".join(lines) + "\n"
        if (ndir / "knowledge").is_dir():
            lines = [MARKER + "# Narrative — knowledge", ""]
            by_type = {}
            for rootpath, meta, _ in _load_entries(root, "knowledge/*.md",
                                                   base="narrative"):
                by_type.setdefault(meta.get("type", "other"), []).append(
                    (rootpath, meta))
            for etype in sorted(by_type):
                lines.append(f"## {etype}")
                for rootpath, meta in sorted(by_type[etype]):
                    lines.append(_line(rootpath, meta))
                lines.append("")
            built["narrative/knowledge/index.md"] = \
                "\n".join(lines).rstrip("\n") + "\n"
```

In the people view, replace `feature = rp.split("/")[2]` with `feature = _home(rp)`.

Note: `narrative/index.md`'s links to not-yet-existing subdirs (e.g. `/narrative/research/`) produce lint **warnings** only — the established dangling-link convention for feature indexes; do not "fix" it.

- [ ] **Step 4: Run the full suite**

Run: `python -m pytest scripts/tests -q` → all pass. Then `python scripts/hub_index.py` (regenerates; live repo has no narrative/ yet → no new files, no diffs), `python scripts/hub_lint.py` → 0 errors, `python scripts/hub_index.py --check` → 0 stale, `git status --porcelain` → only the two modified files.

- [ ] **Step 5: Commit and push**

```bash
git add scripts/hublib/indexer.py scripts/tests/test_indexer.py
git commit -m "feat(indexer): narrative layer — indexes, shared-view inclusion, home labels

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
git push origin main
```

---

### Task 5: Indexer — feature Connections sections from `features:` cross-refs

**Files:**
- Modify: `scripts/hublib/indexer.py` (`build_all` per-feature block; new `_load_artifacts`)
- Test: `scripts/tests/test_indexer.py`

**Interfaces:**
- Consumes: hoisted `entries` (Task 4).
- Produces: `_load_artifacts(root)` yielding `(rootpath, meta)` for every `*/enablement/*/artifact.md` (Task 7 reuses it); `connections` dict (feature id → list) built right after the hoisted load; a `## Connections` section in `features/<id>/index.md` listing cross-referencing entries/artifacts from OTHER homes.

- [ ] **Step 1: Write the failing tests** — append to `scripts/tests/test_indexer.py`:

```python
def test_feature_connections_section(tmp_path):
    root = add_narrative(make_repo(tmp_path))
    built = build_all(root, today=TODAY)
    idx = built["features/mcp-registry/index.md"]
    assert "## Connections" in idx
    assert "[Governed MCP](/narrative/knowledge/story-governed-mcp.md)" in idx


def test_connections_exclude_own_home_and_absent_when_empty(tmp_path):
    root = make_repo(tmp_path)
    # entry in mcp-registry listing itself must NOT create a self-backlink
    write(root, "features/mcp-registry/knowledge/fact-self.md",
          "---\ntype: fact\ndescription: d\ntimestamp: 2026-07-01\n"
          "features: [mcp-registry]\n---\nb\n")
    idx = build_all(root, today=TODAY)["features/mcp-registry/index.md"]
    assert "## Connections" not in idx


def test_artifact_descriptor_creates_connection(tmp_path):
    root = make_repo(tmp_path)
    write(root, "features/features.yaml",
          "features:\n- id: mcp-registry\n  title: MCP Registry\n  description: d\n"
          "- id: mcp-gateway\n  title: MCP Gateway\n  description: d\n")
    write(root, "features/mcp-gateway/enablement/deck/artifact.md",
          "---\ntype: artifact\ntitle: Big Deck\ndescription: cross deck\n"
          "timestamp: 2026-07-01\nfeatures: [mcp-registry]\n---\nb\n")
    idx = build_all(root, today=TODAY)["features/mcp-registry/index.md"]
    assert "[Big Deck](/features/mcp-gateway/enablement/deck/artifact.md)" in idx
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python -m pytest scripts/tests/test_indexer.py -q`
Expected: first and third FAIL (`## Connections` absent); second passes trivially (pins the exclusion).

- [ ] **Step 3: Implement.** In `scripts/hublib/indexer.py`:

Add after `_meta_of`:

```python
def _load_artifacts(root):
    """Yield (rootpath, meta) for enablement artifact descriptors."""
    for pattern in ("features/*/enablement/*/artifact.md",
                    "narrative/enablement/*/artifact.md"):
        for desc in sorted(root.glob(pattern)):
            meta = _meta_of(desc)
            if meta:
                yield "/" + desc.relative_to(root).as_posix(), meta
```

In `build_all`, directly after the hoisted `entries` load (Task 4), add:

```python
    artifacts = list(_load_artifacts(root))
    # connection axis (spec D13): features: declarations → per-feature backlinks
    connections = {}
    for rp, m, _ in entries:
        for fid in (m.get("features") or []):
            connections.setdefault(fid, []).append((rp, m))
    for rp, m in artifacts:
        for fid in (m.get("features") or []):
            connections.setdefault(fid, []).append((rp, m))
```

In the per-feature index block, after the five `lines.append(f"- [{sub}/]...")` lines and before `built[f"features/{f['id']}/index.md"] = ...`, add:

```python
        conns = [(rp, m) for rp, m in connections.get(f["id"], [])
                 if not rp.startswith(f"/features/{f['id']}/")]
        if conns:
            lines.append("")
            lines.append("## Connections")
            for rp, m in sorted(conns):
                lines.append(f"- {m.get('type', '?')} · {_line(rp, m)[2:]}")
```

- [ ] **Step 4: Run the full suite**

Run: `python -m pytest scripts/tests -q` → all pass. `python scripts/hub_index.py` (live repo: no `features:` fields exist yet → feature indexes unchanged), `python scripts/hub_lint.py` → 0 errors, `python scripts/hub_index.py --check` → 0 stale.

- [ ] **Step 5: Commit and push**

```bash
git add scripts/hublib/indexer.py scripts/tests/test_indexer.py
git commit -m "feat(indexer): feature Connections sections from features: cross-refs

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
git push origin main
```

---

### Task 6: Indexer — `views/narrative-map.md`, `views/faq.md`, `views/jtbd.md`

**Files:**
- Modify: `scripts/hublib/indexer.py` (`build_all` views section)
- Test: `scripts/tests/test_indexer.py`

**Interfaces:**
- Consumes: `entries`, `_home` (Task 4).
- Produces: three new generated view files (always emitted — empty-state sections allowed), shapes per spec §6.

- [ ] **Step 1: Write the failing tests** — append to `scripts/tests/test_indexer.py`:

```python
def test_narrative_map_view(tmp_path):
    root = add_narrative(make_repo(tmp_path))
    write(root, "narrative/knowledge/story-orphan.md",
          "---\ntype: story\ntitle: Orphan\ndescription: no pillar yet\n"
          "timestamp: 2026-07-01\nfeatures: [mcp-registry]\nstatus: current\n---\nb\n")
    v = build_all(root, today=TODAY)["views/narrative-map.md"]
    assert "## [Agents](/narrative/knowledge/pillar-agents.md)" in v
    assert "[Governed MCP](/narrative/knowledge/story-governed-mcp.md)" in v
    assert "connects: [mcp-registry](/features/mcp-registry/index.md)" in v
    assert "## Stories without a pillar" in v and "Orphan" in v


def test_faq_view(tmp_path):
    root = make_repo(tmp_path)
    write(root, "features/mcp-registry/knowledge/qa-airgap.md",
          "---\ntype: qa\ntitle: Airgap?\ndescription: does it airgap\n"
          "timestamp: 2026-07-01\nstatus: answered\n"
          "asks:\n- date: 2026-07-01\n  by: customer\n- date: 2026-07-03\n  by: ssa\n"
          "---\nb\n")
    write(root, "features/mcp-registry/knowledge/qa-open.md",
          "---\ntype: qa\ntitle: Quotas?\ndescription: open one\n"
          "timestamp: 2026-07-02\nstatus: open\n"
          "asks:\n- date: 2026-07-02\n  by: sales\n---\nb\n")
    v = build_all(root, today=TODAY)["views/faq.md"]
    assert "## Unanswered" in v and "Quotas?" in v
    assert "## Most asked" in v and "2x · [Airgap?]" in v
    assert "## All, by feature" in v and "### mcp-registry" in v


def test_stale_view_includes_overdue_qa(tmp_path):
    root = make_repo(tmp_path)
    write(root, "features/mcp-registry/knowledge/qa-old.md",
          "---\ntype: qa\ntitle: Old\ndescription: aging answer\n"
          "timestamp: 2026-01-01\nstatus: answered\nreview_after: 2026-06-01\n"
          "asks:\n- date: 2026-01-01\n  by: pm\n---\nb\n")
    v = build_all(root, today=TODAY)["views/stale-facts.md"]
    assert "/features/mcp-registry/knowledge/qa-old.md" in v


def test_jtbd_view(tmp_path):
    root = make_repo(tmp_path)
    write(root, "features/mcp-registry/knowledge/jtbd-find.md",
          "---\ntype: jtbd\ntitle: Find approved\ndescription: find servers\n"
          "timestamp: 2026-07-01\npersona: ai-engineer\nstatus: candidate\n"
          "evidence:\n- /features/mcp-registry/knowledge/qa-airgap.md\n---\nb\n")
    write(root, "features/mcp-registry/knowledge/jtbd-bare.md",
          "---\ntype: jtbd\ntitle: Bare job\ndescription: no proof\n"
          "timestamp: 2026-07-01\npersona: rhoai-admin\nstatus: validated\n---\nb\n")
    v = build_all(root, today=TODAY)["views/jtbd.md"]
    assert "## candidate" in v and "persona: ai-engineer · 1 evidence" in v
    assert "## validated" in v and "NO EVIDENCE" in v
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python -m pytest scripts/tests/test_indexer.py -q`
Expected: all three FAIL with `KeyError: 'views/narrative-map.md'` (etc.).

- [ ] **Step 3: Implement.** In `scripts/hublib/indexer.py`, at the end of the views section (after the `views/stale-facts.md` block, before `return built`), add:

```python
    # views/narrative-map.md — pillars → stories → features (spec §6)
    pillars = sorted([(rp, m) for rp, m, _ in entries if m.get("type") == "pillar"])
    stories = sorted([(rp, m) for rp, m, _ in entries if m.get("type") == "story"])
    lines = [MARKER + "# Narrative map", ""]
    used = set()
    for prp, pm in pillars:
        lines.append(f"## [{_title(pm, prp)}]({prp})")
        lines.append(pm.get("description", ""))
        owned = [(rp, m) for rp, m in stories if m.get("pillar") == prp]
        for rp, m in owned:
            used.add(rp)
            lines.append(f"- [{_title(m, rp)}]({rp}) — {m.get('description', '')}")
            feats_str = ", ".join(f"[{fid}](/features/{fid}/index.md)"
                                  for fid in (m.get("features") or []))
            if feats_str:
                lines.append(f"  - connects: {feats_str}")
        if not owned:
            lines.append("- _no stories yet_")
        lines.append("")
    orphans = [(rp, m) for rp, m in stories if rp not in used]
    if orphans:
        lines.append("## Stories without a pillar")
        for rp, m in orphans:
            lines.append(_line(rp, m))
        lines.append("")
    built["views/narrative-map.md"] = "\n".join(lines).rstrip("\n") + "\n"

    # views/faq.md — the field Q&A rollup ("FAQ" is the audience-facing name)
    qas = [(rp, m) for rp, m, _ in entries if m.get("type") == "qa"]

    def _ask_count(m):
        asks = m.get("asks")
        return len(asks) if isinstance(asks, list) else 0

    lines = [MARKER + "# FAQ — field questions & answers", ""]
    unanswered = sorted([(rp, m) for rp, m in qas if m.get("status") == "open"],
                        key=lambda t: str(t[1].get("timestamp", "")), reverse=True)
    if unanswered:
        lines.append("## Unanswered")
        for rp, m in unanswered:
            lines.append(f"- {_line(rp, m)[2:]} (asked {_ask_count(m)}x)")
        lines.append("")
    recurring = sorted([(rp, m) for rp, m in qas if _ask_count(m) >= 2],
                       key=lambda t: (-_ask_count(t[1]), t[0]))
    if recurring:
        lines.append("## Most asked")
        for rp, m in recurring:
            lines.append(f"- {_ask_count(m)}x · {_line(rp, m)[2:]}")
        lines.append("")
    by_home = {}
    for rp, m in qas:
        by_home.setdefault(_home(rp), []).append((rp, m))
    if by_home:
        lines.append("## All, by feature")
        for home in sorted(by_home):
            lines.append(f"### {home}")
            for rp, m in sorted(by_home[home]):
                lines.append(_line(rp, m))
            lines.append("")
    built["views/faq.md"] = "\n".join(lines).rstrip("\n") + "\n"

    # views/jtbd.md — jobs by status, evidence-count flagged (spec §6, D15)
    jtbds = [(rp, m) for rp, m, _ in entries if m.get("type") == "jtbd"]
    lines = [MARKER + "# Jobs to be done", ""]
    for status in ("candidate", "validated", "delivered", "retired"):
        group = sorted([(rp, m) for rp, m in jtbds if m.get("status") == status])
        if not group:
            continue
        lines.append(f"## {status}")
        for rp, m in group:
            ev = m.get("evidence")
            ev_n = len(ev) if isinstance(ev, list) else 0
            ev_str = f"{ev_n} evidence" if ev_n else "NO EVIDENCE"
            jira = f" · {m['jira']}" if m.get("jira") else ""
            lines.append(f"- {_home(rp)} · persona: {m.get('persona', '?')} · "
                         f"{ev_str}{jira} · {_line(rp, m)[2:]}")
        lines.append("")
    built["views/jtbd.md"] = "\n".join(lines).rstrip("\n") + "\n"
```

Also in this task (spec §6: stale-facts picks up qa/jtbd via `review_after` —
no new staleness machinery): in the `views/stale-facts.md` block, directly
after the existing knowledge-fact loop (`for rp, m, _ in entries: if
m.get("type") == "fact" …`) and BEFORE the `built["views/stale-facts.md"]`
line, add:

```python
    for rp, m, _ in entries:
        if m.get("type") in ("qa", "jtbd"):
            review = _date(m.get("review_after"))
            if review and review < today:
                stale_rows.append(f"- {rp} — {m.get('description', '')} "
                                  f"(review overdue)")
```

- [ ] **Step 4: Run the full suite, regenerate, and commit the new generated views**

Run: `python -m pytest scripts/tests -q` → all pass. Then `python scripts/hub_index.py` — this now WRITES `views/narrative-map.md`, `views/faq.md`, `views/jtbd.md` (empty-state) in the live repo; `python scripts/hub_lint.py` → 0 errors; `python scripts/hub_index.py --check` → 0 stale.

- [ ] **Step 5: Commit and push (code + generated views together)**

```bash
git add scripts/hublib/indexer.py scripts/tests/test_indexer.py views/
git commit -m "feat(indexer): narrative-map, faq, jtbd views

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
git push origin main
```

---

### Task 7: Indexer — `views/artifacts.md` with publish-manifest cross-reference

**Files:**
- Modify: `scripts/hublib/indexer.py` (`build_all` views section)
- Test: `scripts/tests/test_indexer.py`

**Interfaces:**
- Consumes: `_meta_of` (existing). This view deliberately does NOT reuse `_load_artifacts` — it walks the slug DIRECTORIES so descriptor-less artifacts get listed too.
- Produces: `views/artifacts.md`; publish state derived from `publish/manifest.yaml` (never stored — spec §5.5).

- [ ] **Step 1: Write the failing test** — append to `scripts/tests/test_indexer.py`:

```python
def test_artifacts_view(tmp_path):
    root = make_repo(tmp_path)
    write(root, "features/mcp-registry/enablement/deck/index.html", "<html></html>")
    write(root, "features/mcp-registry/enablement/deck/artifact.md",
          "---\ntype: artifact\ntitle: Catalog Deck\ndescription: the deck\n"
          "timestamp: 2026-07-01\nfeatures: [mcp-registry]\n---\nb\n")
    write(root, "features/mcp-registry/enablement/bare/index.html", "<html></html>")
    write(root, "publish/manifest.yaml",
          "- source: features/mcp-registry/enablement/deck/\n  dest: mcp-registry/deck/\n"
          "  audience: public\n  title: T\n  description: D\n")
    v = build_all(root, today=TODAY)["views/artifacts.md"]
    assert "[Catalog Deck](/features/mcp-registry/enablement/deck/)" in v
    assert "published → mcp-registry/deck/" in v
    assert "connects: mcp-registry" in v
    assert "_no artifact.md descriptor yet_" in v and "(unpublished)" in v
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest scripts/tests/test_indexer.py::test_artifacts_view -q`
Expected: FAIL with `KeyError: 'views/artifacts.md'`.

- [ ] **Step 3: Implement.** In `build_all`, after the `views/jtbd.md` block (before `return built`), add:

```python
    # views/artifacts.md — every enablement artifact; publish state from manifest
    manifest_dest = {}
    mpath = root / "publish" / "manifest.yaml"
    if mpath.is_file():
        try:
            for e in (yaml.safe_load(mpath.read_text(encoding="utf-8")) or []):
                if isinstance(e, dict) and e.get("source") and e.get("dest"):
                    key = str(e["source"]).replace("\\", "/").strip("/")
                    manifest_dest[key] = str(e["dest"])
        except yaml.YAMLError:
            pass
    lines = [MARKER + "# Artifacts", ""]
    slug_dirs = []
    for pattern in ("features/*/enablement/*", "narrative/enablement/*"):
        slug_dirs += [p for p in sorted(root.glob(pattern)) if p.is_dir()]
    for slug in slug_dirs:
        rel = slug.relative_to(root).as_posix()
        desc = _meta_of(slug / "artifact.md") if (slug / "artifact.md").is_file() else None
        pub = manifest_dest.get(rel)
        pub_str = f"published → {pub}" if pub else "unpublished"
        if desc:
            feats = ", ".join(desc.get("features") or [])
            feat_str = f" · connects: {feats}" if feats else ""
            lines.append(f"- [{desc.get('title') or slug.name}](/{rel}/) — "
                         f"{desc.get('description', '')} ({pub_str}){feat_str}")
        else:
            lines.append(f"- [{slug.name}](/{rel}/) — _no artifact.md descriptor "
                         f"yet_ ({pub_str})")
    built["views/artifacts.md"] = "\n".join(lines) + "\n"
```

- [ ] **Step 4: Run the full suite, regenerate, commit generated view**

Run: `python -m pytest scripts/tests -q` → all pass. `python scripts/hub_index.py` — writes `views/artifacts.md` (live repo: the catalog-deck dir appears as "no descriptor yet" + "published → mcp-registry/catalog-deck/"). `python scripts/hub_lint.py` → 0 errors. `python scripts/hub_index.py --check` → 0 stale.

- [ ] **Step 5: Commit and push**

```bash
git add scripts/hublib/indexer.py scripts/tests/test_indexer.py views/artifacts.md
git commit -m "feat(indexer): artifacts view with publish-manifest cross-reference

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
git push origin main
```

---

### Task 8: Conventions + docs

**Files:**
- Modify: `conventions/layout.md`, `conventions/type-vocabulary.md`, `conventions/memory.md`, `docs/architecture.md`, `AGENTS.md`, `README.md`, `docs/working-here.md`

No test file — verification is the lint/budget/pytest gate.

- [ ] **Step 1: `conventions/layout.md`** — replace the "## The two filing questions" section header + first line:

Old:
```markdown
## The two filing questions
Every addition answers: **which feature? which type?**
```
New:
```markdown
## The filing questions
Every addition answers: **which home — `narrative/` (story-shaped) or which
feature? which type?**
```

After the "## Feature skeleton contract" section, insert:

```markdown
## The narrative layer
`narrative/` is a peer of `features/` holding the connective story — pillars,
cross-feature stories, the strategy spine, cross-feature artifacts. Same
five-dir skeleton and rules as a feature. Route here only when content would
be *wrong* under any single feature; otherwise pick the primary feature and
declare the spread with `features:` (see
[type-vocabulary.md](/conventions/type-vocabulary.md)). `pillar-` / `story-`
entries live only here.
```

In "## Generated files — never hand-edit", change the file list line to:

```markdown
`features/index.md`, `features/*/index.md`, `features/*/knowledge/index.md`,
`narrative/index.md`, `narrative/knowledge/index.md`, `memory/index.md`,
`views/*` — regenerate with `python scripts/hub_index.py`.
```

- [ ] **Step 2: `conventions/type-vocabulary.md`** — add two rows to the knowledge-entries table:

```markdown
| `qa`        | `qa-`       | a **field** question with our canonical answer; `asks:` list of `{date, by, context?}` records recurrence (`by`: customer\|partner\|sales\|ssa\|pm\|eng\|exec\|other) | `status: open\|answered`, `asks` |
| `jtbd`      | `jtbd-`     | a job to be done ("When …, I want …, so I can …"); execution status stays in Jira (`jira:` field) | `persona` (locked list), `status: candidate\|validated\|delivered\|retired` |
```

After that table, insert:

```markdown
`question-` = **our** open product questions, tracked to resolution.
`qa-` = **the field's** answered questions, tracked for reuse/recurrence.
Don't merge them. `persona` locked list (source of truth:
[fact-personas.md](/features/platform/knowledge/fact-personas.md); extend both
together): `ai-engineer` · `platform-engineer` · `agentops-admin` ·
`business-consumer` · `data-scientist` · `cluster-admin` · `rhoai-admin`.

## Narrative entries (`narrative/knowledge/` only)

| `type` | filename prefix | it is | extra required fields |
|---|---|---|---|
| `pillar` | `pillar-` | an RHAI strategic pillar | — |
| `story`  | `story-`  | a cross-feature narrative connecting features to customer value; optional `pillar:` root-path link | `features` (non-empty) |

Narrative knowledge also accepts the standard vocabulary above.

## Artifact descriptors (`*/enablement/<slug>/artifact.md`)

| `type` | filename | it is |
|---|---|---|
| `artifact` | exactly `artifact.md`, inside the slug dir | makes a deck/write-up indexable (`views/artifacts.md`); optional `features:`; publish state is derived from the manifest, never stored |

## Cross-references (`features:`)
Any knowledge entry or artifact descriptor may declare `features: [ids…]` —
validated against `features/features.yaml` (unknown id = lint **error**; the
routing table is closed, unlike dangling links). The indexer renders the
backlinks: per-feature `## Connections` sections plus the views.
```

- [ ] **Step 3: `conventions/memory.md`** — in "## The gate", append bullet 6:

```markdown
6. qa asker identity: customer/partner names and deal context behind a field
   question → the `restricted/` sibling entry; the public `qa-` entry carries
   only the role bucket (`asks[].by`).
```

- [ ] **Step 4: `docs/architecture.md`** — four edits:

(a) Anatomy table: after the `features/features.yaml` row add:

```markdown
| `narrative/<skeleton>` | the story layer: pillars, cross-feature stories, strategy spine | humans + skills |
```

(b) "## The two filing questions" — rename heading to `## The filing questions` and change item 1's opening to: `1. **Which home?** Story-shaped content (pillars, cross-feature stories, the strategy spine) → \`narrative/\`; everything else picks its feature: \`features/features.yaml\` is the routing table. Current partitions: …` (keep the rest of the item verbatim).

(c) Views table: append rows:

```markdown
| `views/narrative-map.md` | pillars → stories → the features each story connects |
| `views/faq.md` | all `qa` entries — unanswered, most-asked (by `asks:` count), by feature |
| `views/jtbd.md` | all `jtbd` entries by status × feature, evidence-count flagged |
| `views/artifacts.md` | every enablement artifact + publish state from the manifest |
```

(d) Decisions table: append rows (one line each):

```markdown
| D12 | the connection layer is a top-level `narrative/` tree (peer of `features/`, same skeleton), never a pseudo-feature |
| D13 | `features:` cross-reference field, validated against `features.yaml`; connections are declared then generated, never hand-maintained |
| D14 | type vocabulary extension: `pillar`/`story` (narrative-only), `qa`/`jtbd` (any knowledge), `artifact` descriptors + four views |
| D15 | execution status stays in Jira — `jtbd` tracks the job's truth (`candidate→validated→delivered`, `retired`), `jira:` points at delivery |
| D16 | capture-first, publish-later: FAQ/JTBD views repo-internal; curated publishing and the Slack sweep are Phase 2, pulled by demand |
```

Also update the intro sentence of that section from "The design spec settled these (D1–D11)" to "The design specs settled these (D1–D11; D12–D16 from [/docs/specs/2026-07-08-narrative-layer-design.md](/docs/specs/2026-07-08-narrative-layer-design.md))".

- [ ] **Step 5: `AGENTS.md`** — two edits (budget: stays ≤ 150 lines; currently 70):

Map table, after the `features/features.yaml` row:

```markdown
| `narrative/` | the story layer: pillars, cross-feature stories, strategy spine — same skeleton as a feature |
```

Writing-rules first bullet, old:
```markdown
- Filing = two questions: which feature (features.yaml) × which type
  (/conventions/type-vocabulary.md). Working context vs domain knowledge
  boundary: /conventions/memory.md.
```
new:
```markdown
- Filing = which home — narrative/ (story-shaped) or which feature
  (features.yaml) — × which type (/conventions/type-vocabulary.md).
  Cross-feature spread: `features:` list. Working context vs domain
  knowledge boundary: /conventions/memory.md.
```

- [ ] **Step 6: `README.md`** — "Layout in one breath" paragraph, after the `features/<feature>/` clause insert: `` `narrative/` is the story layer above them (pillars, cross-feature stories, the strategy spine — same skeleton); `` so the sentence reads `…skeleton (\`knowledge/ research/ strategy/ enablement/ work/\`); \`narrative/\` is the story layer above them (pillars, cross-feature stories, the strategy spine — same skeleton); \`memory/\` holds working context…`

- [ ] **Step 7: `docs/working-here.md`** — two edits:

In "## The loop", insert after step 1:

```markdown
2. A field question answered (sales/SSA/PM/customer/partner) → `hub.capture`
   files a `qa-` entry — or appends a dated item to an existing one's
   `asks:` list. A validated user job → `jtbd-` entry.
```
(renumber the following steps 2–5 → 3–6).

In "## Filing by example", append rows:

```markdown
| "does the registry work air-gapped?" (asked by an SSA) | `features/mcp-registry/knowledge/qa-…md` — recurrence appends to `asks:` |
| a user job for UX/Docs | `features/<f>/knowledge/jtbd-…md` (persona from the locked list) |
| cross-feature strategy deck or write-up | `narrative/enablement/<slug>/` (+ `artifact.md`) or `narrative/{research,strategy}/` |
| a strategic pillar or connective story | `narrative/knowledge/pillar-…md` / `story-…md` |
```

- [ ] **Step 8: Verify and commit**

Run: `python -m pytest scripts/tests -q` → all pass; `python scripts/hub_lint.py` → 0 errors (new doc links to `/narrative/…` are dangling **warnings**, allowed); `python scripts/hub_index.py --check` → 0 stale; confirm `wc -l AGENTS.md` ≤ 150.

```bash
git add conventions/ docs/architecture.md AGENTS.md README.md docs/working-here.md
git commit -m "docs: connection-axis conventions + guides (layout, vocabulary, memory, architecture D12-D16, AGENTS, README, working-here)

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
git push origin main
```

---

### Task 9: Skills — route narrative/qa/jtbd through capture/file/consolidate/migrate

**Files:**
- Modify: `.claude/skills/hub.capture/SKILL.md`, `.claude/skills/hub.file/SKILL.md`, `.claude/skills/hub.consolidate/SKILL.md`, `.claude/skills/hub.migrate/SKILL.md`, `docs/skills.md`

- [ ] **Step 1: `hub.capture/SKILL.md`** — replace step 1 with:

```markdown
1. Classify with the boundary rule (/conventions/memory.md): working context
   (state, preference, feedback, process fact) → memory store; domain
   knowledge (a colleague would look it up) → features/<f>/knowledge/;
   story-shaped (pillar, cross-feature narrative — wrong under any single
   feature) → narrative/knowledge/; a field question someone asked us →
   qa- entry (dedupe rule in step 2); a user job for UX/Docs → jtbd- entry
   (persona from the locked list, evidence: links); NDA-adjacent → the
   restricted/ mirror of the same location. Entries touching multiple
   features declare `features: [ids]`.
```

and in step 2, after the "Knowledge entries: first check the feature partition exists…" bullet, add:

```markdown
   - qa entries: BEFORE creating, grep existing `qa-*` for the same
     question; on a match, append a dated item to its `asks:` list
     (`by:` role bucket) and refresh the answer if knowledge moved —
     never a duplicate entry. A pasted Slack permalink goes in `source:`.
     Asker identity (customer/partner name, deal context) → the restricted
     sibling; the public entry keeps only the role bucket.
```

- [ ] **Step 2: `hub.file/SKILL.md`** — replace step 1 with:

```markdown
1. Pick the home: story-shaped sources (pillars, cross-feature narrative,
   strategy-spine material) → narrative/knowledge/. Otherwise pick the
   feature: read features/features.yaml. If nothing fits, propose a
   new partition (id, title, one-line description); on approval append it to
   features.yaml and create ONLY the subdirectories this filing needs — never
   all five empty (see /conventions/layout.md). Multi-feature sources keep a
   primary home and declare `features:` cross-refs.
```

- [ ] **Step 3: `hub.consolidate/SKILL.md`** — replace step 3 with:

```markdown
3. Classify each survivor: profile update | new memory fact | knowledge entry
   (which feature — or narrative/ for story-shaped; typed qa-/jtbd- where the
   item is a field question or a user job) | preference/feedback | RESTRICTED
   | discard.
```

- [ ] **Step 4: `hub.migrate/SKILL.md`** — in "Migrate-on-touch" step 2, after "…move whole documents into features/<f>/{research|strategy|enablement}/ when they have standalone value as documents", append: `Story-shaped old-repo content (strategy, pillars, connective write-ups) routes to narrative/{knowledge|strategy}/.` And in step 5, change the first sentence to:

```markdown
5. Published HTML artifacts: copy sources into
   features/<f>/enablement/<artifact>/ (or narrative/enablement/ for
   cross-feature ones), add an artifact.md descriptor (type: artifact,
   features: spread), and add the manifest entry via hub.publish.
```

- [ ] **Step 5: `docs/skills.md`** — in "The `hub.*` skills in more depth", append to the `hub.capture` paragraph: `Field questions become qa- entries (dedupe first — recurrence appends to asks:); user jobs become jtbd- entries; story-shaped items route to narrative/knowledge/.`

- [ ] **Step 6: Verify and commit**

Run: `python scripts/hub_lint.py` → 0 errors; `python -m pytest scripts/tests -q` → all pass; `python scripts/hub_index.py --check` → 0 stale.

```bash
git add .claude/skills/ docs/skills.md
git commit -m "feat(skills): route narrative/qa/jtbd through capture/file/consolidate/migrate

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
git push origin main
```

---

### Task 10: Seed batch — OWNER GATE

**Files:**
- Create: `narrative/knowledge/pillar-inference.md`, `pillar-agents.md`, `pillar-data.md`, `pillar-safety-governance.md`, `ref-rhai-cy2027-product-strategy.md`, `ref-pillar-component-mapping.md`, `story-governed-mcp-access.md`, `story-agent-lifecycle.md`; `features/mcp-registry/enablement/mcp-registry-catalog-deck/artifact.md`
- Move: `features/platform/knowledge/{fact-agentic-ai-four-pillars,fact-agentic-ai-messaging-position,ref-agentic-ai-strategy-2026}.md` → `narrative/knowledge/`
- Modify: `features/features.yaml` (platform description), `features/platform/knowledge/fact-personas.md` (JTBD vocabulary section), `memory/log.md`
- Regenerate: all indexes/views

**Gate protocol:** draft everything, present the numbered batch to the owner (hub.consolidate-style: approve all / pick numbers / edit / reject), apply only approved items. Do not push without the owner's OK on the batch.

- [ ] **Step 1: Draft the four pillar entries.** Content below is the proposal — the owner may edit at the gate. All four use `status: current`, `timestamp: 2026-07-08`, `tags: [narrative, pillar]`.

`narrative/knowledge/pillar-inference.md`:

```markdown
---
type: pillar
title: Inference
description: "RHAI strategic pillar: the open enterprise AI inference platform — any model, any accelerator, any cloud — with inference economics as the deciding cost factor."
timestamp: 2026-07-08
status: current
source: Red Hat AI CY2027 Product Strategy (see ref-rhai-cy2027-product-strategy)
tags: [narrative, pillar]
---
One of the four RHAI strategic pillars. Objective: be the leading enterprise
AI inference platform — run and manage any agent, any model, on any
accelerator, across cloud, datacenter, and edge — treating inference/token
economics as the primary cost lever of enterprise AI.

Component families (per the mapping sheet): vLLM, llm-d, inference midstream,
llm-compressor/speculators, optimized + validated models, model serving
runtimes and orchestration, GuideLLM, tool calling for agentic workloads.

Sources: [ref-rhai-cy2027-product-strategy](/narrative/knowledge/ref-rhai-cy2027-product-strategy.md) ·
[ref-pillar-component-mapping](/narrative/knowledge/ref-pillar-component-mapping.md)
```

`narrative/knowledge/pillar-agents.md`:

```markdown
---
type: pillar
title: Agents
description: "RHAI strategic pillar: the enterprise control plane for agentic AI — Bring Your Own Agent on an open, interoperable platform (MCP, A2A, agent registries, lifecycle, secure execution)."
timestamp: 2026-07-08
status: current
source: Red Hat AI CY2027 Product Strategy (see ref-rhai-cy2027-product-strategy)
tags: [narrative, pillar]
---
One of the four RHAI strategic pillars. Objective: establish Red Hat AI as
the enterprise control plane for agentic AI. Principle: **Bring Your Own
Agent** — customers keep their frameworks/models; Red Hat provides the
platform layer frameworks don't: identity, security, governance,
observability, lifecycle, evaluation, policy, operational control.

Component families (per the mapping sheet): Model Context Protocol
(PM: Peter Double), GenAI Studio (PM: Peter Double), AgentOps, AgentDev,
OGX core, agentic tooling experience. This hub's feature partitions ladder
primarily here (mcp-*, agent-*, gen-ai-studio, skills-registry).

The agentic sub-strategy's own pillar set:
[fact-agentic-ai-four-pillars](/narrative/knowledge/fact-agentic-ai-four-pillars.md).
Sources: [ref-rhai-cy2027-product-strategy](/narrative/knowledge/ref-rhai-cy2027-product-strategy.md) ·
[ref-pillar-component-mapping](/narrative/knowledge/ref-pillar-component-mapping.md)
```

`narrative/knowledge/pillar-data.md`:

```markdown
---
type: pillar
title: Data
description: "RHAI strategic pillar: enterprise knowledge and evaluation as first-class platform services — RAG, customization, synthetic data, evaluation-driven development."
timestamp: 2026-07-08
status: current
source: Red Hat AI CY2027 Product Strategy (see ref-rhai-cy2027-product-strategy)
tags: [narrative, pillar]
---
One of the four RHAI strategic pillars. Objective: make enterprise knowledge
and evaluation first-class platform services — connect enterprise context to
models and agents (prompts, RAG, customization, synthetic data) and make
Evaluation-Driven Development a core operating practice.

Component families (per the mapping sheet): EvalHub/model eval, AutoRAG/RAG,
AutoML, development platform, data processing, SDG, Training Hub,
fine-tuning/Kubeflow + Ray training, inference-time techniques.

Sources: [ref-rhai-cy2027-product-strategy](/narrative/knowledge/ref-rhai-cy2027-product-strategy.md) ·
[ref-pillar-component-mapping](/narrative/knowledge/ref-pillar-component-mapping.md)
```

`narrative/knowledge/pillar-safety-governance.md`:

```markdown
---
type: pillar
title: Safety & Governance
description: "RHAI strategic pillar: the operational foundation for Private and Sovereign AI — AI Gateway/MaaS as the governance layer, AI safety, trusted supply chain, AI-as-an-internal-service."
timestamp: 2026-07-08
status: current
source: Red Hat AI CY2027 Product Strategy (see ref-rhai-cy2027-product-strategy)
tags: [narrative, pillar]
---
One of the four RHAI strategic pillars. Objective: make Red Hat AI the
operational foundation for Private and Sovereign AI — operate AI as a
governed internal service: who has access, where models run, where data
lives, how policy is enforced, how consumption is metered and audited.

Component families: the mapping sheet groups these under its "Platform"
heading — AI Gateway, MaaS, GPUaaS, AI Hub, AI Safety, Observability,
AI Navigator — alongside platform services (MLflow, pipelines, feature
store, notebooks). Note: the sheet's "AIPCC" grouping is org infrastructure,
not a strategy pillar.

Sources: [ref-rhai-cy2027-product-strategy](/narrative/knowledge/ref-rhai-cy2027-product-strategy.md) ·
[ref-pillar-component-mapping](/narrative/knowledge/ref-pillar-component-mapping.md)
```

- [ ] **Step 2: Draft the two source refs.**

`narrative/knowledge/ref-rhai-cy2027-product-strategy.md`:

```markdown
---
type: reference
title: Red Hat AI CY2027 Product Strategy (Joe Fernandes)
description: "The RHAI strategy source of truth: four strategic pillars (Inference, Agents, Data, Safety & Governance), GTM, ecosystem — the doc this layer's pillar entries derive from."
timestamp: 2026-07-08
resource: https://docs.google.com/document/d/178H9aSpKZxn1_7qMd_QUeHvnM6dgzu2nsZXf4O8HgaI
tags: [narrative, strategy]
---
Names the four strategic pillars with per-pillar CY2027 investment areas,
GTM strategy, and the partner/community ecosystem. Appendix 1 links the
per-pillar deep-dive strategy docs; appendix 2 carries business-sensitive
material (bookings/ARR/customers) that stays out of this repo entirely.
Read the pillar- entries here first; open the doc for the full text.
```

`narrative/knowledge/ref-pillar-component-mapping.md`:

```markdown
---
type: reference
title: Pillar to component mapping
description: "Sheet mapping RHAI components (with PM/eng leads) to pillar groupings — Inference, Data, Agents, Platform (≈ Safety & Governance + platform services), AIPCC (org infra, not a pillar)."
timestamp: 2026-07-08
resource: https://docs.google.com/spreadsheets/d/13TfWjWeh0TMVicfrkD1O7FI5EwP9rVsurSOvq82x7q4
tags: [narrative, strategy]
---
The component-level breakdown behind the pillars. Naming note: the sheet's
"Platform" grouping holds the Safety & Governance pillar's components
(AI Gateway, MaaS, GPUaaS, AI Hub, AI Safety, Observability) plus platform
services; "AIPCC" is organizational infrastructure, not a strategy pillar.
Peter's components (Model Context Protocol, GenAI Studio) sit under Agents.
```

- [ ] **Step 3: Draft the two seed stories.**

`narrative/knowledge/story-governed-mcp-access.md`:

```markdown
---
type: story
title: Governed MCP access, end to end
description: "How MCP Registry, MCP Gateway, and the MCP Ecosystem compose: from any MCP server, through governance, to safe agent consumption at runtime."
timestamp: 2026-07-08
features: [mcp-registry, mcp-gateway, mcp-ecosystem]
pillar: /narrative/knowledge/pillar-agents.md
status: current
tags: [narrative, story]
---
**The claim:** an enterprise can adopt MCP servers from anywhere — partners,
community, in-house — and give agents access to them with the same
governance discipline it applies to any other production dependency.

**How the features compose:**
1. The **MCP Ecosystem** supplies the raw material: partner/community
   servers, build tooling, validation and security scanning.
2. The **MCP Registry** is the system of record: lifecycle states, metadata,
   approval — governance deciding what is *allowed to exist*.
3. The **MCP Gateway** enforces at runtime: authenticated, policy-checked,
   observable tool traffic — governance deciding what is *allowed to happen*.

**Customer value:** platform teams onboard tools once; agents consume them
safely everywhere; security review stops being a per-project one-off.
**Business result:** the trust layer that makes agentic adoption on RHOAI
defensible in regulated environments — registry + gateway is the wedge.

Pillar: [Agents](/narrative/knowledge/pillar-agents.md). Backing knowledge:
each feature's `knowledge/` index.
```

`narrative/knowledge/story-agent-lifecycle.md`:

```markdown
---
type: story
title: "The agent lifecycle: build, run, operate"
description: "How Gen AI Studio, Agent Registry, Agent Memory, and Agent Ops compose into the full lifecycle story for enterprise agents on RHOAI."
timestamp: 2026-07-08
features: [gen-ai-studio, agent-registry, agent-memory, agent-ops]
pillar: /narrative/knowledge/pillar-agents.md
status: current
tags: [narrative, story]
---
**The claim:** RHOAI covers the whole life of an enterprise agent — built and
iterated in the studio, registered and governed as an asset, remembering
across sessions, operated with real observability.

**How the features compose:**
1. **Gen AI Studio** — where agents and prompts are built and iterated.
2. **Agent Registry** — the governed asset record: versions, approval,
   catalog and starter kits for reuse.
3. **Agent Memory** — the knowledge substrate that makes agents useful
   beyond a single session.
4. **Agent Ops** — deployment oversight: tracing, evaluation, operational
   control (the AgentOps control plane).

**Customer value:** one platform from prototype to production instead of a
per-team toolchain. **Business result:** positions RHOAI as the enterprise
control plane for agentic AI — the Agents pillar objective — rather than a
collection of point tools.

Pillar: [Agents](/narrative/knowledge/pillar-agents.md). Backing knowledge:
each feature's `knowledge/` index.
```

- [ ] **Step 4: Re-home the three platform entries.**

```bash
mkdir -p narrative/knowledge
git mv features/platform/knowledge/fact-agentic-ai-four-pillars.md narrative/knowledge/
git mv features/platform/knowledge/fact-agentic-ai-messaging-position.md narrative/knowledge/
git mv features/platform/knowledge/ref-agentic-ai-strategy-2026.md narrative/knowledge/
```

Then, in each moved file: change `tags:` value `platform` → `narrative` (leave other tags), leave body/timestamp otherwise unchanged. Repoint inbound links:

```bash
grep -rn "platform/knowledge/fact-agentic-ai-four-pillars\|platform/knowledge/fact-agentic-ai-messaging-position\|platform/knowledge/ref-agentic-ai-strategy-2026" --include="*.md" --exclude-dir=.git .
```

For every hit in a NON-generated file, rewrite the path prefix `/features/platform/knowledge/` → `/narrative/knowledge/` (generated files fix themselves at reindex).

- [ ] **Step 5: Narrow the platform description.** In `features/features.yaml`, replace the platform entry's description line with:

```yaml
  description: Platform components and org reference — AI Gateway, AI Hub UI, releases/SKUs, people, personas, org process. Story/strategy content lives in /narrative/.
```

- [ ] **Step 6: Backfill the artifact descriptor.** Create `features/mcp-registry/enablement/mcp-registry-catalog-deck/artifact.md`:

```markdown
---
type: artifact
title: MCP Registry & Catalog
description: Slide deck covering MCP Registry and Catalog capabilities, lifecycle governance, pre-loaded MCP servers, and the roadmap from Dev Preview through GA.
timestamp: 2026-07-08
features: [mcp-registry]
source: migrated from ai-asset-registry (R4 wave 1)
---
Self-contained HTML slide deck; published to the pages site via
publish/manifest.yaml (dest mcp-registry/catalog-deck/).
```

(Note: the manifest's `source:` is the whole directory, so this descriptor
ships to the pages site alongside the deck — harmless, and the repo is
public anyway.)

- [ ] **Step 7: Record the persona vocabulary.** In `features/platform/knowledge/fact-personas.md`: bump `timestamp:` to `2026-07-08`, and append to the body:

```markdown

## JTBD persona vocabulary (2026-07-08)
The locked `persona:` values for `jtbd-` entries (lint-enforced — extend this
list and the linter's `PERSONAS` enum together, through the gate): the four
personas above as `ai-engineer`, `platform-engineer`, `agentops-admin`,
`business-consumer`, plus owner additions `data-scientist`, `cluster-admin`,
`rhoai-admin` (2026-07-08 ruling — audiences the UX/Docs JTBD consumers
work with).
```

- [ ] **Step 8: PRESENT THE GATE.** Show the owner the numbered batch (9 new files, 3 moves + tag edits, 2 file edits), each as `N. [kind] <path> — <description> [public]`. All items are public (pillar/story bodies carry only public-safe paraphrases — verified: no bookings/ARR/customer material). Wait for rulings; apply edits/rejections exactly.

- [ ] **Step 9: Apply, log, regenerate, verify.** After approval:

Add to `memory/log.md` under a `## 2026-07-08` heading (top of body, above existing entries for the date if the heading already exists — append this line first under the heading):

```markdown
- **Creation** — narrative layer live (D12–D16): narrative/ seeded (4 RHAI pillars + 2 source refs + 2 stories), features: connection axis, qa/jtbd/artifact types, 4 new views; platform shed story content to narrative/; JTBD persona vocabulary locked (7).
```

Then:

```bash
python scripts/hub_index.py
python scripts/hub_lint.py        # 0 errors required
python scripts/hub_index.py --check
python -m pytest scripts/tests -q
```

Manual verification of the rendered axis:
- `views/narrative-map.md` shows all four pillars; both stories under Agents; Inference/Data/Safety & Governance show `_no stories yet_`.
- `features/mcp-registry/index.md` has a `## Connections` section listing both the story and nothing self-referential.
- `views/artifacts.md` shows the catalog deck with its descriptor + `published → mcp-registry/catalog-deck/`.
- `views/faq.md` / `views/jtbd.md` exist with empty-state content (headline only).

- [ ] **Step 10: Commit and push**

```bash
git add -A
git commit -m "know(narrative): seed — 4 RHAI pillars, 2 source refs, 2 stories; platform re-home (gated)

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
git push origin main
```

Confirm CI (`validate`, `publish`) green: `gh run list --limit 2`.

---

## Acceptance check (spec §10)

- [ ] `python -m pytest scripts/tests -q` green (≈ 34 pre-existing + ≈ 24 new)
- [ ] `python scripts/hub_lint.py` → 0 errors on the seeded repo
- [ ] `python scripts/hub_index.py --check` → 0 stale; convergence test green
- [ ] `views/narrative-map.md` renders pillars → stories → features from seed content
- [ ] `views/faq.md`, `views/jtbd.md`, `views/artifacts.md` render (empty-state OK)
- [ ] Every feature index with cross-refs shows `## Connections`
- [ ] `AGENTS.md` ≤ 150 lines; `memory/index.md` ≤ 200 lines
- [ ] CI green on final push; no new skills; `publish/manifest.yaml` untouched
- [ ] Seed batch applied with owner rulings recorded (Task 10 gate)
