# Published-Site Trust Batch Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship enhancements #34 (disclosure net gaps), #8 (full-branded pages landing page), and #4 (`hub.refresh-site` skill + configs), then run gated refresh acceptance on both hub sites.

**Architecture:** Three additive slices over the existing `scripts/hublib` lint/publish machinery plus one new skill. #34 widens two existing scan passes; #8 moves the landing page to a tracked template and upgrades the publish snapshot to v2 (hash + published date + badge); #4 adds a config validator (`hublib/refresh.py`), two tracked per-site source configs, and a gated skill that ports the old repo's update flow with a disclosure contract added.

**Tech Stack:** Python 3.12 (stdlib + PyYAML, pytest), plain HTML/CSS template, Claude skill (SKILL.md).

**Spec:** `/docs/specs/2026-07-10-published-site-trust-batch-design.md` (approved 2026-07-10).

## Global Constraints

- Run tests with `python -m pytest scripts/tests -v` from the repo root (Windows; Git Bash for shell steps).
- A pre-commit hook runs `hub_lint.py` (0 errors required) and `hub_index.py --check` on EVERY commit. If it fails on stale indexes, run `python scripts/hub_index.py` and re-stage.
- Lint findings are strings `"<relpath>: <message>"` returned as `(errors, warnings)` tuples. Match this exactly.
- NO EM DASHES in any newly written string, doc, template copy, or commit message (owner ruling 2026-07-10). Pre-existing strings that contain them (e.g. the heuristic warning text) are kept verbatim when moved.
- This repo is PUBLIC. Never introduce customer/partner names or engagement detail anywhere.
- Files are written LF-normalized (`newline="\n"` where code writes files).
- Match hublib style: module docstrings explaining contracts, terse comments only for non-obvious constraints.
- Every commit message ends with: `Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>`
- Tasks 1-8 are subagent-executable. Tasks 9-10 are OWNER-GATED acceptance runs executed in the main session; do not dispatch them to autonomous subagents.

## File Structure

| path | action | responsibility |
|---|---|---|
| `scripts/hublib/schema.py` | modify | #34: heuristic scans full entry text |
| `scripts/hublib/disclosure.py` | modify | #34: generated md + refresh yaml surfaces |
| `scripts/hublib/publisher.py` | modify | #8: groups, snapshot v2, template render |
| `publish/landing-template.html` | create | #8: the branded landing template |
| `scripts/hublib/refresh.py` | create | #4: refresh-config find/load/validate |
| `features/mcp-gateway/work/refresh-rhcl-hub.yaml` | create | #4: RHCL hub source config |
| `features/mcp-ecosystem/work/refresh-management-hub.yaml` | create | #4: Management hub source config |
| `.claude/skills/hub.refresh-site/SKILL.md` | create | #4: the gated refresh skill |
| `scripts/tests/test_schema.py` | modify | #34 tests |
| `scripts/tests/test_disclosure.py` | modify | #34 tests |
| `scripts/tests/test_publisher.py` | modify | #8 tests |
| `scripts/tests/test_refresh.py` | create | #4 validator tests |
| `AGENTS.md`, `docs/skills.md`, `docs/tooling.md`, `docs/publishing.md`, `conventions/publishing.md`, `docs/enhancements.md` | modify | docs + backlog bookkeeping |
| `docs/specs/2026-07-10-published-site-trust-batch-design.md` | modify | one-line snapshot-schema amendment (Task 4) |

---

### Task 1: #34 heuristic scans full entry text (frontmatter included)

**Files:**
- Modify: `scripts/hublib/schema.py:152-207` (`lint_entry`)
- Test: `scripts/tests/test_schema.py`

**Interfaces:**
- Consumes: `frontmatter.load_file(path) -> (meta: dict, body: str)`; `RESTRICTED_HINTS` regex (schema.py:64).
- Produces: unchanged `lint_entry` signature; the heuristic warning now fires on frontmatter-only hits too.

- [ ] **Step 1: Write the failing tests**

Append to `scripts/tests/test_schema.py`:

```python
def test_restricted_hint_in_frontmatter_only_is_warning(tmp_path):
    root = make_repo(tmp_path)
    write(root, "features/x/knowledge/fact-a.md",
          "---\ntype: fact\ndescription: internal-only pricing detail\n"
          "timestamp: 2026-07-05\n---\nclean body\n")
    _, warnings = lint_repo(root)
    assert any("fact-a.md" in w and "restricted-content heuristic" in w
               for w in warnings)


def test_restricted_hint_in_frontmatter_skipped_under_restricted(tmp_path):
    root = make_repo(tmp_path)
    write(root, "restricted/features/x/knowledge/fact-a.md",
          "---\ntype: fact\ndescription: internal-only pricing detail\n"
          "timestamp: 2026-07-05\n---\nclean body\n")
    _, warnings = lint_repo(root)
    assert not any("restricted-content heuristic" in w for w in warnings)
```

- [ ] **Step 2: Run tests to verify the first fails**

Run: `python -m pytest scripts/tests/test_schema.py -k frontmatter_only -v`
Expected: `test_restricted_hint_in_frontmatter_only_is_warning` FAILS (no warning emitted); `..._skipped_under_restricted` may pass already.

- [ ] **Step 3: Implement**

In `scripts/hublib/schema.py`, `lint_entry`: change the load line

```python
    try:
        meta, body = frontmatter.load_file(path)
```

to

```python
    try:
        meta, _ = frontmatter.load_file(path)
```

and replace

```python
    if RESTRICTED_HINTS.search(body) and "restricted" not in path.parts:
        warnings.append(f"{rel}: restricted-content heuristic matched — "
                        f"confirm this belongs in a public repo")
```

with

```python
    # Raw text, not the parsed body: frontmatter (description etc.) leaks
    # into public views, so it is part of the scanned surface (#34).
    if "restricted" not in path.parts and \
            RESTRICTED_HINTS.search(path.read_text(encoding="utf-8")):
        warnings.append(f"{rel}: restricted-content heuristic matched — "
                        f"confirm this belongs in a public repo")
```

(The warning string is pre-existing; keep it byte-identical.)

- [ ] **Step 4: Run the full suite and the real-repo lint**

Run: `python -m pytest scripts/tests -v` -> all PASS.
Run: `python scripts/hub_lint.py` -> MUST report 0 errors. Record any warnings that were not in the pre-change output (new frontmatter hits on real entries) in your task report for owner triage. Do NOT edit repo content to silence them.

- [ ] **Step 5: Commit**

```bash
git add scripts/hublib/schema.py scripts/tests/test_schema.py
git commit -m "lint: heuristic scans full entry text incl frontmatter (#34)

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

### Task 2: #34 disclosure passes cover generated md + refresh configs

**Files:**
- Modify: `scripts/hublib/disclosure.py:36-66` (`_scan_files`, `scan_repo`)
- Test: `scripts/tests/test_disclosure.py`

**Interfaces:**
- Consumes: `RESTRICTED_HINTS` from `.schema`; `load_patterns(root)`.
- Produces: `_scan_files(root)` now yields `(path, heuristic: bool)` tuples; `scan_repo(root) -> (errors, warnings)` unchanged externally.

- [ ] **Step 1: Write the failing tests**

Append to `scripts/tests/test_disclosure.py`:

```python
def test_pattern_match_in_views_is_error(tmp_path):
    write(tmp_path, "restricted/lint-patterns.txt", "acme\n")
    write(tmp_path, "views/artifacts.md", "# artifacts\n- Acme deck (published)\n")
    errors, _ = scan_repo(tmp_path)
    assert errors == ["views/artifacts.md:2: matches restricted pattern "
                      "(lint-patterns.txt:1)"]


def test_generic_hints_warn_on_generated_md(tmp_path):
    write(tmp_path, "views/faq.md", "# faq\nthis answer is internal-only\n")
    write(tmp_path, "memory/index.md", "# m\ndo not share this\n")
    write(tmp_path, "features/index.md", "# f\ncovered by NDA\n")
    write(tmp_path, "features/x/index.md", "# x\npricing tier detail\n")
    write(tmp_path, "narrative/index.md", "# n\nSKU-123 detail\n")
    errors, warnings = scan_repo(tmp_path)
    assert errors == []
    hits = [w for w in warnings if "restricted-content heuristic" in w]
    assert len(hits) == 5


def test_pattern_match_in_refresh_config_is_error(tmp_path):
    write(tmp_path, "restricted/lint-patterns.txt", "acme\n")
    write(tmp_path, "features/x/work/refresh-site.yaml",
          "site: features/x/enablement/site/\nsources:\n  gdocs:\n"
          "  - {id: abc, title: Acme deal deck}\n")
    write(tmp_path, "narrative/work/refresh-nsite.yaml",
          "site: narrative/enablement/nsite/\nsources:\n  github:\n  - acme/repo\n")
    errors, _ = scan_repo(tmp_path)
    assert errors == ["features/x/work/refresh-site.yaml:4: "
                      "matches restricted pattern (lint-patterns.txt:1)",
                      "narrative/work/refresh-nsite.yaml:3: "
                      "matches restricted pattern (lint-patterns.txt:1)"]


def test_refresh_config_gets_no_heuristic_warning(tmp_path):
    write(tmp_path, "features/x/work/refresh-site.yaml",
          "site: features/x/enablement/site/\nnotes: internal-only sweep list\n")
    _, warnings = scan_repo(tmp_path)
    assert warnings == []
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python -m pytest scripts/tests/test_disclosure.py -v`
Expected: the four new tests FAIL (views/index/refresh files are not scanned yet); all pre-existing tests PASS.

- [ ] **Step 3: Implement**

In `scripts/hublib/disclosure.py`, replace `_scan_files` and `scan_repo` with:

```python
def _scan_files(root):
    """The public scan surface as (path, heuristic) pairs. Every file gets the
    restricted-patterns pass (errors); heuristic=True adds the generic
    RESTRICTED_HINTS pass (warnings): enablement HTML plus the generated
    markdown that entry descriptions propagate into (#34). Markdown ENTRIES
    stay heuristic=False here: lint_entry (schema.py) already scans their
    full text. YAML surfaces get the patterns pass only."""
    root = Path(root)
    surfaces = (
        ("features/*/enablement/**/*.html", True),
        ("narrative/enablement/**/*.html", True),
        ("features/*/knowledge/*.md", False),
        ("narrative/knowledge/*.md", False),
        ("features/*/work/jira-snapshot.yaml", False),
        ("features/*/work/refresh-*.yaml", False),
        ("narrative/work/refresh-*.yaml", False),
        ("views/*.md", True),
        ("memory/index.md", True),
        ("features/index.md", True),
        ("features/*/index.md", True),
        ("narrative/index.md", True),
    )
    for pattern, heuristic in surfaces:
        for f in sorted(root.glob(pattern)):
            yield f, heuristic


def scan_repo(root):
    root = Path(root)
    patterns, warnings = load_patterns(root)
    errors = []
    for f, heuristic in _scan_files(root):
        rel = f.relative_to(root).as_posix()
        for n, line in enumerate(
                f.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            for lineno, pat in patterns:
                if pat.search(line):
                    errors.append(f"{rel}:{n}: matches restricted pattern "
                                  f"(lint-patterns.txt:{lineno})")
            if heuristic and RESTRICTED_HINTS.search(line):
                warnings.append(f"{rel}:{n}: restricted-content heuristic matched — "
                                f"confirm this belongs in a public repo")
    return errors, warnings
```

(The module docstring's "enablement HTML" wording may be updated to mention generated markdown; keep the warning string byte-identical.)

- [ ] **Step 4: Run the full suite and the real-repo lint**

Run: `python -m pytest scripts/tests -v` -> all PASS.
Run: `python scripts/hub_lint.py` -> MUST report 0 errors. Record NEW warnings (views/index heuristic hits) in your task report for owner triage; do not edit content.

- [ ] **Step 5: Commit**

```bash
git add scripts/hublib/disclosure.py scripts/tests/test_disclosure.py
git commit -m "lint: disclosure net covers generated views/indexes + refresh configs (#34)

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

### Task 3: #8 landing plan gains area groups

**Files:**
- Modify: `scripts/hublib/publisher.py:23-40` (`build_plan`, new `_feature_titles`)
- Test: `scripts/tests/test_publisher.py`

**Interfaces:**
- Consumes: `features/features.yaml` (`features: [{id, title, ...}]`, routing-table order).
- Produces: plan entries gain `"group": str` (display name) and `"group_key": tuple` sorting `(0, idx)` known features < `(1, raw_id)` unknown < `(2, "")` Narrative. Task 5 consumes both.

- [ ] **Step 1: Write the failing tests**

In `scripts/tests/test_publisher.py`, add after the `MANIFEST` constant:

```python
FEATURES_YAML = """\
features:
- id: x
  title: X Feature
- id: y
  title: Y Feature
"""
```

In `make_repo`, add this line before `return root`:

```python
    write(root, "features/features.yaml", FEATURES_YAML)
```

Append tests:

```python
def test_build_plan_groups_by_source_area(tmp_path):
    root = make_repo(tmp_path)
    write(root, "narrative/enablement/story/index.html", "<html></html>")
    write(root, "publish/manifest.yaml", MANIFEST +
          "- source: narrative/enablement/story/\n  dest: narrative/story/\n"
          "  audience: public\n  title: Story\n  description: narr\n")
    plan = build_plan(root)
    by_dest = {p["dest"]: p for p in plan}
    assert by_dest["x/site"]["group"] == "X Feature"
    assert by_dest["x/site"]["group_key"] == (0, 0)
    assert by_dest["narrative/story"]["group"] == "Narrative"
    assert by_dest["narrative/story"]["group_key"] == (2, "")


def test_build_plan_unknown_feature_id_falls_back(tmp_path):
    root = make_repo(tmp_path)
    write(root, "features/zed/enablement/deck/index.html", "<html></html>")
    write(root, "publish/manifest.yaml",
          "- source: features/zed/enablement/deck/\n  dest: zed/deck/\n"
          "  audience: public\n  title: Z\n  description: D\n")
    plan = build_plan(root)
    assert plan[0]["group"] == "zed"
    assert plan[0]["group_key"] == (1, "zed")
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python -m pytest scripts/tests/test_publisher.py -k groups_by_source or falls_back -v`
Expected: FAIL with `KeyError: 'group'`.

- [ ] **Step 3: Implement**

In `scripts/hublib/publisher.py`, add above `build_plan`:

```python
def _feature_titles(root):
    """id -> display title from features/features.yaml, preserving the
    routing-table order (drives landing-page section order)."""
    p = Path(root) / "features" / "features.yaml"
    if not p.is_file():
        return {}
    try:
        data = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError:
        return {}
    return {f["id"]: (f.get("title") or f["id"])
            for f in (data.get("features") or [])
            if isinstance(f, dict) and f.get("id")}
```

Replace `build_plan` with:

```python
def build_plan(root):
    root = Path(root)
    titles = _feature_titles(root)
    order = list(titles)
    plan = []
    for e in load_manifest(root):
        if e.get("audience") != "public":
            continue
        src = root / e["source"]
        dest = e["dest"].strip("/")
        is_dir = src.is_dir()
        parts = [p for p in str(e["source"]).replace("\\", "/").split("/") if p]
        if parts and parts[0] == "features" and len(parts) > 1:
            fid = parts[1]
            group = titles.get(fid, fid)
            group_key = (0, order.index(fid)) if fid in order else (1, fid)
        elif parts and parts[0] == "narrative":
            group, group_key = "Narrative", (2, "")
        else:
            group, group_key = (parts[0] if parts else "Other",
                                (1, parts[0] if parts else ""))
        plan.append({
            "src": src,
            "dest": dest,
            "is_dir": is_dir,
            "title": e["title"],
            "description": e["description"],
            "href": dest + "/" if is_dir else dest,
            "group": group,
            "group_key": group_key,
        })
    return plan
```

- [ ] **Step 4: Run the full suite**

Run: `python -m pytest scripts/tests -v` -> all PASS.

- [ ] **Step 5: Commit**

```bash
git add scripts/hublib/publisher.py scripts/tests/test_publisher.py
git commit -m "publish: landing plan gains area groups from features.yaml (#8)

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

### Task 4: #8 publish snapshot v2 (hash + published + badge)

**Files:**
- Modify: `scripts/hublib/publisher.py` (`apply`, new `_hash_source`, `_snapshot_entry`, `BADGE_WINDOW_DAYS`)
- Modify: `docs/specs/2026-07-10-published-site-trust-batch-design.md` (snapshot schema amendment)
- Test: `scripts/tests/test_publisher.py`

**Interfaces:**
- Consumes: plan entries from Task 3.
- Produces: snapshot v2 `{dest: {source, hash, published, badge}}`; plan entries gain `"hash"`, `"published"` (ISO date or None), `"badge"` ("new"|"updated"|None), `"show_badge"` (badge if `published` within `BADGE_WINDOW_DAYS = 14` days, else None). Task 5 renders `show_badge`/`published`. Exposes `_hash_source(src: Path) -> str` (sha256 hex).

- [ ] **Step 1: Write the failing tests**

In `scripts/tests/test_publisher.py`, REPLACE the snapshot assertion block at the end of `test_apply_copies_and_snapshots` (the `snap = ...` and `assert snap == {...}` lines) with:

```python
    snap = json.loads((pages / SNAPSHOT).read_text())
    assert set(snap) == {"x/one-pager.html", "x/site"}
    site = snap["x/site"]
    assert site["source"] == "features/x/enablement/site"
    assert site["badge"] == "new"
    assert site["published"] is not None
    assert len(site["hash"]) == 64
```

Append tests:

```python
def test_apply_badge_lifecycle(tmp_path):
    root = make_repo(tmp_path)
    pages = tmp_path / "pages"
    pages.mkdir()
    apply(root, pages)
    snap1 = json.loads((pages / SNAPSHOT).read_text())
    assert snap1["x/site"]["badge"] == "new"
    apply(root, pages)  # unchanged: carried forward verbatim
    snap2 = json.loads((pages / SNAPSHOT).read_text())
    assert snap2["x/site"] == snap1["x/site"]
    write(root, "features/x/enablement/site/index.html", "<html>site v2</html>")
    apply(root, pages)  # content change: flips to updated
    snap3 = json.loads((pages / SNAPSHOT).read_text())
    assert snap3["x/site"]["badge"] == "updated"
    assert snap3["x/site"]["hash"] != snap1["x/site"]["hash"]


def test_apply_migrates_v1_snapshot_without_false_badges(tmp_path):
    root = make_repo(tmp_path)
    pages = tmp_path / "pages"
    pages.mkdir()
    (pages / SNAPSHOT).write_text(json.dumps(
        {"x/one-pager.html": "features/x/enablement/one-pager.html",
         "x/site": "features/x/enablement/site"}), encoding="utf-8")
    apply(root, pages)
    snap = json.loads((pages / SNAPSHOT).read_text())
    assert snap["x/site"]["badge"] is None
    assert snap["x/site"]["published"] is None
    assert len(snap["x/site"]["hash"]) == 64


def test_hash_source_dir_is_deterministic_and_content_sensitive(tmp_path):
    from hublib.publisher import _hash_source
    root = make_repo(tmp_path)
    src = root / "features/x/enablement/site"
    h1 = _hash_source(src)
    assert h1 == _hash_source(src)
    write(root, "features/x/enablement/site/style.css", "body{color:red}")
    assert _hash_source(src) != h1
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python -m pytest scripts/tests/test_publisher.py -v`
Expected: the modified and new tests FAIL (snapshot values are plain strings; no `_hash_source`).

- [ ] **Step 3: Implement**

In `scripts/hublib/publisher.py`, add to the imports: `import hashlib` and `from datetime import date`. Add below `SNAPSHOT`:

```python
BADGE_WINDOW_DAYS = 14


def _hash_source(src):
    """sha256 over artifact content. Directories hash a deterministic walk of
    relative POSIX paths + bytes so a rename counts as a change."""
    h = hashlib.sha256()
    src = Path(src)
    if src.is_dir():
        for f in sorted(p for p in src.rglob("*") if p.is_file()):
            h.update(f.relative_to(src).as_posix().encode("utf-8"))
            h.update(b"\0")
            h.update(f.read_bytes())
    else:
        h.update(src.read_bytes())
    return h.hexdigest()


def _snapshot_entry(old, dest):
    """Old snapshot row as a dict. v1 rows (plain source string) migrate to
    unknown hash + no published date so the first v2 run shows no false
    badges; hashes populate on that run."""
    e = old.get(dest)
    if isinstance(e, str):
        return {"source": e, "hash": None, "published": None, "badge": None}
    return e
```

In `apply`, directly after the line `old = json.loads(...) if snap_path.is_file() else {}`, insert:

```python
    today = date.today()
    for p in plan:
        prev = _snapshot_entry(old, p["dest"])
        digest = _hash_source(p["src"])
        if prev is None:
            published, badge = today.isoformat(), "new"
        elif prev.get("hash") and prev["hash"] != digest:
            published, badge = today.isoformat(), "updated"
        else:
            published, badge = prev.get("published"), prev.get("badge")
        p["hash"], p["published"], p["badge"] = digest, published, badge
        active = (published is not None and
                  (today - date.fromisoformat(published)).days <= BADGE_WINDOW_DAYS)
        p["show_badge"] = badge if active else None
```

Replace the snapshot write at the end of `apply` with:

```python
    snap_path.write_text(
        json.dumps({p["dest"]: {"source": p["src"].relative_to(root).as_posix(),
                                "hash": p["hash"],
                                "published": p["published"],
                                "badge": p["badge"]}
                    for p in plan},
                   indent=2, sort_keys=True) + "\n",
        encoding="utf-8", newline="\n")
```

- [ ] **Step 4: Amend the spec's snapshot schema (approved refinement)**

In `docs/specs/2026-07-10-published-site-trust-batch-design.md`, change the two occurrences of `{dest: {source, hash, published}}` to `{dest: {source, hash, published, badge}}`, and in Part 2 item 4 append after "unchanged: `published` carried forward unchanged.":

```
   The badge KIND ("new"/"updated") is persisted in the snapshot so an
   unchanged artifact keeps its NEW badge for the whole window instead of
   flipping to UPDATED.
```

- [ ] **Step 5: Run the full suite**

Run: `python -m pytest scripts/tests -v` -> all PASS.

- [ ] **Step 6: Commit**

```bash
git add scripts/hublib/publisher.py scripts/tests/test_publisher.py docs/specs/2026-07-10-published-site-trust-batch-design.md
git commit -m "publish: snapshot v2 with content hash, published date, badge (#8)

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

### Task 5: #8 full-branded landing template + grouped render

**Files:**
- Create: `publish/landing-template.html`
- Modify: `scripts/hublib/publisher.py` (`generate_landing`, new `_card`; `apply` call site)
- Test: `scripts/tests/test_publisher.py`

**Interfaces:**
- Consumes: plan entries with `group`, `group_key`, `show_badge`, `published` (Tasks 3-4); template tokens `{{COUNT}}`, `{{META}}`, `{{SECTIONS}}`.
- Produces: `generate_landing(root, plan, hub_sha="") -> str` (NOTE: `root` is now the first parameter; `apply` passes it through).

- [ ] **Step 1: Create the template**

Create `publish/landing-template.html` with exactly:

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>RHOAI Agentic Hub · Published artifacts</title>
  <style>
    :root {
      --bg-canvas: #151515; --bg-elevated: #1a1a1a; --bg-card: #202020;
      --text-primary: #ffffff; --text-secondary: #d2d2d2; --text-muted: #8a8a8a;
      --rh-red: #ee0000; --rh-blue-light: #4394e5;
      --border-subtle: #333333;
      --font-sans: "Red Hat Display", "Inter", -apple-system, "Segoe UI", system-ui, sans-serif;
      --font-text: "Red Hat Text", "Inter", -apple-system, "Segoe UI", system-ui, sans-serif;
    }
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body { background: var(--bg-canvas); color: var(--text-primary);
           font-family: var(--font-text); line-height: 1.55; }
    .hero { background: var(--bg-elevated); border-bottom: 3px solid var(--rh-red);
            padding: 3rem 1.5rem 2.5rem; }
    .hero-inner, .main-inner, .footer-inner { max-width: 1100px; margin: 0 auto; }
    .hero h1 { font-family: var(--font-sans); font-size: 2.2rem; font-weight: 700; }
    .hero .tagline { color: var(--text-secondary); font-size: 1.05rem;
                     margin-top: .55rem; max-width: 46rem; }
    .hero .stats { color: var(--text-muted); font-size: .82rem; margin-top: 1.1rem; }
    main { padding: 1rem 1.5rem 4rem; }
    .area { margin-top: 2.4rem; }
    .area h2 { font-family: var(--font-sans); font-size: 1.22rem; font-weight: 600;
               padding-bottom: .45rem; border-bottom: 1px solid var(--border-subtle); }
    .cards { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
             gap: 1rem; margin-top: 1.1rem; }
    .card { display: block; background: var(--bg-card);
            border: 1px solid var(--border-subtle); border-radius: 8px;
            padding: 1.1rem 1.2rem; text-decoration: none;
            transition: border-color .15s ease, transform .15s ease; }
    .card:hover { border-color: var(--rh-red); transform: translateY(-2px); }
    .card h3 { color: var(--text-primary); font-family: var(--font-sans);
               font-size: 1.02rem; font-weight: 600; }
    .card p { color: var(--text-secondary); font-size: .85rem; margin-top: .45rem; }
    .badge { display: inline-block; font-size: .62rem; font-weight: 700;
             letter-spacing: .06em; text-transform: uppercase; border-radius: 3px;
             padding: .12rem .45rem; margin-left: .5rem; vertical-align: middle; }
    .badge--new { background: var(--rh-red); color: #ffffff; }
    .badge--updated { color: var(--rh-blue-light);
                      border: 1px solid var(--rh-blue-light); }
    .empty { color: var(--text-muted); margin-top: 2.4rem; }
    footer { border-top: 1px solid var(--border-subtle); color: var(--text-muted);
             font-size: .78rem; padding: 1.2rem 1.5rem 2.5rem; }
    footer a { color: var(--rh-blue-light); }
  </style>
</head>
<body>
  <header class="hero">
    <div class="hero-inner">
      <h1>RHOAI Agentic Hub</h1>
      <p class="tagline">Published enablement and strategy artifacts for agentic AI
        on Red Hat OpenShift AI: MCP governance, agent infrastructure, and the
        cross-feature stories behind them.</p>
      <p class="stats">{{COUNT}} published artifacts{{META}}</p>
    </div>
  </header>
  <main>
    <div class="main-inner">
{{SECTIONS}}
    </div>
  </main>
  <footer>
    <div class="footer-inner">Generated from publish/manifest.yaml. Do not edit
      by hand. Source repo:
      <a href="https://github.com/solaius/rhoai-agentic-hub">rhoai-agentic-hub</a>.</div>
  </footer>
</body>
</html>
```

- [ ] **Step 2: Write the failing tests**

In `scripts/tests/test_publisher.py`: add `import shutil` to the imports and add to the top of the file (after the existing imports):

```python
REPO_ROOT = Path(__file__).resolve().parents[2]
```

In `make_repo`, add before `return root`:

```python
    (root / "publish").mkdir(parents=True, exist_ok=True)
    shutil.copy(REPO_ROOT / "publish" / "landing-template.html",
                root / "publish" / "landing-template.html")
```

(NOTE: `make_repo` writes `publish/manifest.yaml` via `write()` which already creates `publish/`; keep the copy line after that write.)

REPLACE `test_generate_landing_escapes_and_lists` with:

```python
def test_generate_landing_escapes_and_lists(tmp_path):
    root = make_repo(tmp_path)
    plan = build_plan(root)
    out = generate_landing(root, plan, hub_sha="abc123")
    assert "A &lt;Site&gt;" in out
    assert 'href="x/site/"' in out
    assert "abc123" in out
    assert "Internal only" not in out
    assert "<h2>X Feature</h2>" in out
```

Append:

```python
def test_generate_landing_group_order(tmp_path):
    root = make_repo(tmp_path)
    write(root, "narrative/enablement/story/index.html", "<html></html>")
    write(root, "features/zed/enablement/deck/index.html", "<html></html>")
    write(root, "publish/manifest.yaml", MANIFEST +
          "- source: narrative/enablement/story/\n  dest: narrative/story/\n"
          "  audience: public\n  title: Story\n  description: narr\n"
          "- source: features/zed/enablement/deck/\n  dest: zed/deck/\n"
          "  audience: public\n  title: Zed\n  description: unknown feature\n")
    out = generate_landing(root, build_plan(root), "")
    assert (out.index("<h2>X Feature</h2>") < out.index("<h2>zed</h2>")
            < out.index("<h2>Narrative</h2>"))


def test_generate_landing_empty_plan(tmp_path):
    root = make_repo(tmp_path)
    out = generate_landing(root, [], "")
    assert "No published artifacts yet." in out


def test_apply_landing_shows_new_badge(tmp_path):
    root = make_repo(tmp_path)
    pages = tmp_path / "pages"
    pages.mkdir()
    apply(root, pages)
    out = (pages / "index.html").read_text(encoding="utf-8")
    assert "badge--new" in out and ">NEW</span>" in out


def test_badge_ages_out_after_window(tmp_path):
    from hublib.publisher import _hash_source
    root = make_repo(tmp_path)
    write(root, "publish/manifest.yaml",
          "- source: features/x/enablement/site/\n  dest: x/site/\n"
          "  audience: public\n  title: Old Site\n  description: D\n")
    pages = tmp_path / "pages"
    pages.mkdir()
    digest = _hash_source(root / "features/x/enablement/site")
    (pages / SNAPSHOT).write_text(json.dumps(
        {"x/site": {"source": "features/x/enablement/site", "hash": digest,
                    "published": "2020-01-01", "badge": "new"}}),
        encoding="utf-8")
    apply(root, pages)
    out = (pages / "index.html").read_text(encoding="utf-8")
    assert "badge--new" not in out
```

- [ ] **Step 3: Run tests to verify they fail**

Run: `python -m pytest scripts/tests/test_publisher.py -v`
Expected: FAIL (old `generate_landing` signature takes `(plan, hub_sha)` and renders the flat list).

- [ ] **Step 4: Implement**

In `scripts/hublib/publisher.py`, replace `generate_landing` entirely with:

```python
def _card(p):
    badge = ""
    if p.get("show_badge") == "new":
        badge = ' <span class="badge badge--new">NEW</span>'
    elif p.get("show_badge") == "updated":
        badge = (' <span class="badge badge--updated">Updated '
                 f'{html.escape(p.get("published") or "")}</span>')
    return (f'        <a class="card" href="{html.escape(p["href"])}">\n'
            f'          <h3>{html.escape(p["title"])}{badge}</h3>\n'
            f'          <p>{html.escape(p["description"])}</p>\n'
            f'        </a>')


def generate_landing(root, plan, hub_sha=""):
    """Render publish/landing-template.html: sections in group_key order,
    cards title-sorted within a section, badges from the publish snapshot."""
    template = (Path(root) / "publish" / "landing-template.html") \
        .read_text(encoding="utf-8")
    groups = {}
    for p in plan:
        key = (p.get("group_key", (1, "")), p.get("group", "Other"))
        groups.setdefault(key, []).append(p)
    sections = []
    for (_, name), items in sorted(groups.items(), key=lambda kv: kv[0][0]):
        cards = "\n".join(_card(p) for p in
                          sorted(items, key=lambda p: p["title"].lower()))
        sections.append(f'      <section class="area">\n'
                        f'        <h2>{html.escape(name)}</h2>\n'
                        f'        <div class="cards">\n{cards}\n        </div>\n'
                        f'      </section>')
    if not sections:
        sections.append('      <p class="empty">No published artifacts yet.</p>')
    meta = f' · hub commit {html.escape(hub_sha)}' if hub_sha else ""
    return (template
            .replace("{{COUNT}}", str(len(plan)))
            .replace("{{META}}", meta)
            .replace("{{SECTIONS}}", "\n".join(sections)))
```

In `apply`, change the landing call to:

```python
    (pages / "index.html").write_text(generate_landing(root, plan, hub_sha),
                                      encoding="utf-8", newline="\n")
```

Update the module docstring's first line to: `"""Manifest-driven publishing: copy allowlisted public artifacts into the pages repo clone and render its landing page from publish/landing-template.html."""`

- [ ] **Step 5: Run the full suite and render the real landing page**

Run: `python -m pytest scripts/tests -v` -> all PASS.
Then render the real landing page for the owner to eyeball (written OUTSIDE the repo; the main session screenshots it and deletes it after review):

```bash
python -c "
import sys; sys.path.insert(0, 'scripts')
from pathlib import Path
from hublib.publisher import build_plan, generate_landing
root = Path('.')
html_out = generate_landing(root, build_plan(root), 'preview')
Path('../landing-preview.html').write_text(html_out, encoding='utf-8')
print('wrote ../landing-preview.html')
"
```

Expected: file written OUTSIDE the repo (parent dir), full sections for MCP Gateway / MCP Registry / MCP Ecosystem / Skills Registry / Agent Memory / Narrative. No badges expected (no snapshot in a plain render).

- [ ] **Step 6: Commit**

```bash
git add publish/landing-template.html scripts/hublib/publisher.py scripts/tests/test_publisher.py
git commit -m "publish: full-branded landing template with grouped cards and badges (#8)

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

### Task 6: #4 refresh-config validator (`hublib/refresh.py`)

**Files:**
- Create: `scripts/hublib/refresh.py`
- Modify: `scripts/hublib/schema.py` (import + `lint_repo` wiring)
- Test: `scripts/tests/test_refresh.py` (create)

**Interfaces:**
- Consumes: nothing from other tasks.
- Produces: `refresh.find_configs(root) -> list[Path]`, `refresh.load_config(path) -> dict`, `refresh.validate(root) -> (errors, warnings)`. `schema.lint_repo` folds `refresh.validate` findings in. The hub.refresh-site skill (Task 8) reads configs via these globs.

- [ ] **Step 1: Write the failing tests**

Create `scripts/tests/test_refresh.py`:

```python
from pathlib import Path

from hublib.refresh import find_configs, validate


def write(root: Path, rel: str, text: str):
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8", newline="\n")
    return p


VALID = """\
site: features/x/enablement/site/
sources:
  gdocs:
  - {id: abc123, title: Overview}
  github:
  - org/repo
  jira:
    keys: [X-1]
  slack:
    channels: [general]
    window_days: 14
  local:
  - features/x/knowledge/
"""


def make_site(root):
    write(root, "features/x/enablement/site/index.html", "<html></html>")


def test_valid_config_passes(tmp_path):
    make_site(tmp_path)
    write(tmp_path, "features/x/work/refresh-site.yaml", VALID)
    assert validate(tmp_path) == ([], [])


def test_find_configs_covers_features_and_narrative(tmp_path):
    write(tmp_path, "features/x/work/refresh-a.yaml", "site: s\n")
    write(tmp_path, "narrative/work/refresh-b.yaml", "site: s\n")
    rels = [p.relative_to(tmp_path).as_posix() for p in find_configs(tmp_path)]
    assert rels == ["features/x/work/refresh-a.yaml", "narrative/work/refresh-b.yaml"]


def test_missing_site_is_error(tmp_path):
    write(tmp_path, "features/x/work/refresh-site.yaml", "sources:\n  github: [a/b]\n")
    errors, _ = validate(tmp_path)
    assert any("missing 'site'" in e for e in errors)


def test_bad_site_shape_is_error(tmp_path):
    write(tmp_path, "features/x/work/refresh-site.yaml",
          "site: features/x/site/\nsources:\n  github: [a/b]\n")
    errors, _ = validate(tmp_path)
    assert any("site must be" in e for e in errors)


def test_nonexistent_site_is_error(tmp_path):
    write(tmp_path, "features/x/work/refresh-site.yaml", VALID)
    errors, _ = validate(tmp_path)
    assert any("site does not exist" in e for e in errors)


def test_unknown_source_type_is_error(tmp_path):
    make_site(tmp_path)
    write(tmp_path, "features/x/work/refresh-site.yaml",
          "site: features/x/enablement/site/\nsources:\n  webscrape: [a]\n")
    errors, _ = validate(tmp_path)
    assert any("unknown source type 'webscrape'" in e for e in errors)


def test_empty_source_type_is_error(tmp_path):
    make_site(tmp_path)
    write(tmp_path, "features/x/work/refresh-site.yaml",
          "site: features/x/enablement/site/\nsources:\n  github: []\n")
    errors, _ = validate(tmp_path)
    assert any("source type 'github' is empty" in e for e in errors)


def test_gdoc_without_id_is_error(tmp_path):
    make_site(tmp_path)
    write(tmp_path, "features/x/work/refresh-site.yaml",
          "site: features/x/enablement/site/\nsources:\n  gdocs:\n"
          "  - {title: No Id}\n")
    errors, _ = validate(tmp_path)
    assert any("gdocs[0] needs an 'id'" in e for e in errors)


def test_slack_without_channels_is_error(tmp_path):
    make_site(tmp_path)
    write(tmp_path, "features/x/work/refresh-site.yaml",
          "site: features/x/enablement/site/\nsources:\n  slack:\n"
          "    window_days: 7\n")
    errors, _ = validate(tmp_path)
    assert any("slack needs a 'channels' list" in e for e in errors)


def test_missing_sources_is_error(tmp_path):
    make_site(tmp_path)
    write(tmp_path, "features/x/work/refresh-site.yaml",
          "site: features/x/enablement/site/\n")
    errors, _ = validate(tmp_path)
    assert any("'sources' must be a non-empty mapping" in e for e in errors)


def test_invalid_yaml_is_error(tmp_path):
    write(tmp_path, "features/x/work/refresh-site.yaml", "site: [unclosed\n")
    errors, _ = validate(tmp_path)
    assert any("invalid YAML" in e for e in errors)


def test_lint_repo_wires_refresh_validation(tmp_path):
    from hublib.schema import lint_repo
    write(tmp_path, "AGENTS.md", "# a\n")
    write(tmp_path, "features/x/work/refresh-site.yaml", "sources:\n  github: [a/b]\n")
    errors, _ = lint_repo(tmp_path)
    assert any("refresh-site.yaml" in e and "missing 'site'" in e for e in errors)
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python -m pytest scripts/tests/test_refresh.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'hublib.refresh'`.

- [ ] **Step 3: Implement**

Create `scripts/hublib/refresh.py`:

```python
"""Refresh-site source configs (work/refresh-<slug>.yaml): find + load +
validate. Consumed by the hub.refresh-site skill; findings fold into
schema.lint_repo. Configs are tracked and PUBLIC (owner ruling 2026-07-10);
the disclosure passes in disclosure.py scan them."""
from pathlib import Path

import yaml

SOURCE_TYPES = {"gdocs", "github", "jira", "slack", "local"}
CONFIG_GLOBS = ("features/*/work/refresh-*.yaml", "narrative/work/refresh-*.yaml")


def find_configs(root):
    root = Path(root)
    out = []
    for pattern in CONFIG_GLOBS:
        out.extend(sorted(root.glob(pattern)))
    return out


def load_config(path):
    return yaml.safe_load(Path(path).read_text(encoding="utf-8"))


def _site_ok(site):
    parts = [p for p in site.replace("\\", "/").split("/") if p]
    return ((len(parts) == 4 and parts[0] == "features" and parts[2] == "enablement")
            or (len(parts) == 3 and parts[0] == "narrative" and parts[1] == "enablement"))


def validate(root):
    """(errors, warnings) matching schema.lint_repo's finding shape."""
    root = Path(root)
    errors, warnings = [], []
    for f in find_configs(root):
        rel = f.relative_to(root).as_posix()
        try:
            data = load_config(f)
        except yaml.YAMLError as exc:
            errors.append(f"{rel}: invalid YAML: {exc}")
            continue
        if not isinstance(data, dict):
            errors.append(f"{rel}: must be a YAML mapping")
            continue
        site = str(data.get("site") or "")
        if not site:
            errors.append(f"{rel}: missing 'site'")
        elif not _site_ok(site):
            errors.append(f"{rel}: site must be features/<f>/enablement/<slug>/ "
                          f"or narrative/enablement/<slug>/")
        elif not (root / site.strip("/")).is_dir():
            errors.append(f"{rel}: site does not exist: {site}")
        sources = data.get("sources")
        if not isinstance(sources, dict) or not sources:
            errors.append(f"{rel}: 'sources' must be a non-empty mapping")
            continue
        for stype, val in sources.items():
            if stype not in SOURCE_TYPES:
                errors.append(f"{rel}: unknown source type '{stype}' "
                              f"(known: {', '.join(sorted(SOURCE_TYPES))})")
            elif not val:
                errors.append(f"{rel}: source type '{stype}' is empty")
        for i, doc in enumerate(sources.get("gdocs") or []):
            if not isinstance(doc, dict) or not doc.get("id"):
                errors.append(f"{rel}: gdocs[{i}] needs an 'id'")
        slack = sources.get("slack")
        if slack is not None and (not isinstance(slack, dict)
                                  or not slack.get("channels")):
            errors.append(f"{rel}: slack needs a 'channels' list")
    return errors, warnings
```

In `scripts/hublib/schema.py`: change the import line `from . import frontmatter, jiramap` to `from . import frontmatter, jiramap, refresh`, and in `lint_repo`, after the `jiramap.validate` block, add:

```python
    r_errors, r_warnings = refresh.validate(root)
    errors.extend(r_errors)
    warnings.extend(r_warnings)
```

- [ ] **Step 4: Run the full suite**

Run: `python -m pytest scripts/tests -v` -> all PASS.

- [ ] **Step 5: Commit**

```bash
git add scripts/hublib/refresh.py scripts/hublib/schema.py scripts/tests/test_refresh.py
git commit -m "refresh: hublib refresh-config validator wired into lint (#4)

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

### Task 7: #4 the two site configs

**Files:**
- Create: `features/mcp-gateway/work/refresh-rhcl-hub.yaml`
- Create: `features/mcp-ecosystem/work/refresh-management-hub.yaml`

**Interfaces:**
- Consumes: the Task 6 schema (validated by `hub_lint` on commit).
- Produces: the configs the hub.refresh-site skill (Task 8) and acceptance runs (Tasks 9-10) read.

- [ ] **Step 1: Write the RHCL config**

Create `features/mcp-gateway/work/refresh-rhcl-hub.yaml`:

```yaml
# Source list for hub.refresh-site (see .claude/skills/hub.refresh-site/).
# Tracked and PUBLIC by owner ruling 2026-07-10; scanned by the disclosure
# lint. Seeded from the old repo's update-gateway-hub skill.
site: features/mcp-gateway/enablement/rhcl-hub/
sources:
  gdocs:
  - {id: 14ekB7bfRxvpZNl1SLBoD_MUQ7T4Ot5Tes3xvyftFOW0, title: RHCL Overview Deck}
  - {id: 1asuSND63alcJGIExLH-VvBzevtKleuuWge39lO5Su7Q, title: MCP Gateway Delivery}
  - {id: 1liziAy55qQBd80qRN63WTZjhu5mJRQ4-OlogP_edftQ, title: MCP Gateway on OpenShift}
  - {id: 11JTt4SHZJ1UFG9RWZsVL2t6MZqBFZ4Iuq4niXxtE59g, title: Support Agreement}
  - {id: 1KOLTSMVjdUhb06rQLSx4G5MVSQLXePToGAQ4wNn31m8, title: Data Model Proposal}
  - {id: 1L3yVBHKJLwVJ2SzF5NunzXc8gFJNZKbMU6OWfPyB_fE, title: MCP Catalog}
  - {id: 1Z2rA0fiAC2Zt_AWnond_Ogi3-2cqEzElN-U76M1x740, title: Partners MCP Catalog}
  github:
  - Kuadrant/mcp-gateway
  - kubernetes-sigs/mcp-lifecycle-operator
  - opendatahub-io/ai-gateway-payload-processing
  jira:
    keys: [RHAIRFE-1370, RHAIRFE-1457, RHAIRFE-1456, RHAISTRAT-1937]
  slack:
    channels: [mcp-gateway, mcp-gateway-dev]
    window_days: 14
  local:
  - features/mcp-gateway/knowledge/
  - features/mcp-gateway/research/
```

- [ ] **Step 2: Write the Management config**

Create `features/mcp-ecosystem/work/refresh-management-hub.yaml`:

```yaml
# Source list for hub.refresh-site (see .claude/skills/hub.refresh-site/).
# Tracked and PUBLIC by owner ruling 2026-07-10; scanned by the disclosure
# lint. Seeded from the old repo's update-ecosystem-hub skill.
site: features/mcp-ecosystem/enablement/management-hub/
sources:
  gdocs:
  - {id: 1Hkfrr6hnHJ08Y1DfTNaKTa-BY06lcjejLUwVnDz_w5Y, title: Ecosystem Strategy}
  - {id: 1rFe_OuLw8hPtzHoV9RL8IMDtuL-iEgIfPBIj0FO3vs8, title: Partner Ecosystem}
  - {id: 1vRu8pSLi6VMrX1Cdn64RdQTOhjQZG97BIxTRZadtjVY, title: Operators Deep Dive}
  - {id: 11mJpJ-Py8FxRDYdw41mMWEBvlahENS4rHqnpDNpqa8Y, title: MCPLO Support Agreement}
  - {id: 1L3yVBHKJLwVJ2SzF5NunzXc8gFJNZKbMU6OWfPyB_fE, title: Catalog Integration}
  - {id: 1Z2rA0fiAC2Zt_AWnond_Ogi3-2cqEzElN-U76M1x740, title: Partners MCP Catalog}
  - {id: 1KOLTSMVjdUhb06rQLSx4G5MVSQLXePToGAQ4wNn31m8, title: Gateway Data Model}
  - {id: 11JTt4SHZJ1UFG9RWZsVL2t6MZqBFZ4Iuq4niXxtE59g, title: MCPLO Data Model}
  github:
  - Kuadrant/mcp-gateway
  - kubernetes-sigs/mcp-lifecycle-operator
  jira:
    keys: [RHAISTRAT-1339]
    jql: parent = RHAISTRAT-1339
  slack:
    channels: [forum-ai-asset-management, forum-mcp-lifecycle-operator]
    window_days: 14
  local:
  - features/mcp-ecosystem/knowledge/
  - features/mcp-ecosystem/research/
  - features/mcp-registry/knowledge/
  - features/mcp-catalog/knowledge/
```

- [ ] **Step 3: Validate**

Run: `python scripts/hub_lint.py` -> 0 errors (the validator from Task 6 accepts both; the disclosure patterns pass scans them).
Run: `python -m pytest scripts/tests -v` -> all PASS.

- [ ] **Step 4: Commit**

```bash
git add features/mcp-gateway/work/refresh-rhcl-hub.yaml features/mcp-ecosystem/work/refresh-management-hub.yaml
git commit -m "refresh: rhcl-hub + management-hub source configs (#4)

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

### Task 8: #4 the hub.refresh-site skill + docs + backlog bookkeeping

**Files:**
- Create: `.claude/skills/hub.refresh-site/SKILL.md`
- Modify: `AGENTS.md` (skills table), `docs/skills.md`, `docs/tooling.md`, `docs/publishing.md`, `conventions/publishing.md`, `docs/enhancements.md`

**Interfaces:**
- Consumes: Task 6 globs/validator, Task 7 configs, existing `hublib/jira.py`, google-workspace + slack MCPs, `gh` CLI.
- Produces: the operable skill; updated docs; #34/#8/#4 moved to Done.

- [ ] **Step 1: Create the skill**

Create `.claude/skills/hub.refresh-site/SKILL.md` with exactly:

```markdown
---
name: hub.refresh-site
description: Refresh a published enablement hub site (RHCL hub, Management hub, or any site with a work/refresh-<slug>.yaml config) from its live sources - GDocs, GitHub, Jira, Slack, and local hub entries. Sweeps for changes, proposes page-level diffs through the inline gate, applies surgical edits, bumps data-verified footers, re-runs the disclosure net, and republishes. Use when the user says "refresh the rhcl hub", "update the management hub", "refresh the site", or when data-verified dates look stale.
---

# hub.refresh-site

Config-driven successor to the old repo's update-*-hub skills. One config per
site: `features/<f>/work/refresh-<slug>.yaml` (or `narrative/work/...`),
validated by hub_lint. Never auto-commits. THE DISCLOSURE CONTRACT (step 6)
is what the old skills lacked: they swept customer names IN; this skill
keeps them OUT.

1. TARGET. Resolve the site from the request; if ambiguous, list configs
   (`features/*/work/refresh-*.yaml`, `narrative/work/refresh-*.yaml`) and
   ask. Read the config, the site's artifact.md, and the current pages.
2. STALENESS. Grep `data-verified` across the site's HTML; report per page,
   oldest first. The oldest date is the sweep-since baseline.
3. SWEEP (parallel subagents, one per source type; each returns findings as
   structured notes, never edits):
   - gdocs: google-workspace `get_doc_as_markdown` with `include_comments`
     true, `user_google_email: pedouble@redhat.com`.
   - github: `gh` CLI - releases, commits, README/doc changes since baseline.
   - jira: stored `work/jira-snapshot.yaml` plus live check via
     `python scripts/hub_jira.py` / `hublib/jira.py` (keys and jql from the
     config).
   - slack: channel history over `window_days` via the slack MCP.
   - local: the hub knowledge/research paths listed in the config.
   Any unreachable source (Slack tokens expire; VPN) degrades to a "Fetch
   failures" report section - the run continues.
4. CHANGE REPORT. Categorized: New / Changed / Confirmed-current / Fetch
   failures. Every finding names the page(s) it affects. Live source wins
   over stale page content.
5. GATE. Batch approval: apply all / by number / skip / show diff. Wait for
   the owner. Nothing is written before this.
6. APPLY + DISCLOSURE CONTRACT (non-negotiable):
   - Surgical in-place HTML edits; never rebuild a page. Keep nav.js
     SITE_MAP consistent if a page is added or retitled.
   - NEVER introduce customer or partner names, engagement pricing, or deal
     detail. Use anonymized phrasing ("large enterprise OEM customer",
     "major telecommunications provider").
   - Product naming: full name on first use per page ("RHOAI restricted use
     entitlement for OpenShift"), short form after.
   - No em dashes in newly written content.
   - Bump `data-verified` to today on every page swept-and-updated or
     swept-and-confirmed; leave unswept pages' dates alone.
   - Bump the site's artifact.md `timestamp`.
   - `python scripts/hub_lint.py` must report 0 errors before commit
     (restricted-pattern hits are hard blockers - fix content, never bypass).
7. COMMIT + REPUBLISH. Commit `refresh(<slug>): <summary>` with a bulleted
   body of applied changes; push;
   `gh run watch --repo solaius/rhoai-agentic-hub --exit-status` (publish.yml
   republishes and runs the link gate - CI is the link-check authority;
   local checks false-positive on cross-hub links). Report the live URL.
8. Offer hub.capture for a memory log line summarizing the refresh.
```

- [ ] **Step 2: AGENTS.md skills table row**

In `AGENTS.md`, in the hub skills table (the one listing hub.capture through hub.migrate), add after the `hub.publish` row:

```markdown
| hub.refresh-site | refresh a published hub site from its live sources (gated page diffs, disclosure contract, republish) |
```

Check: `wc -l AGENTS.md` must stay <= 150 (currently 75).

- [ ] **Step 3: docs/skills.md and docs/tooling.md**

In `docs/skills.md`: find the section/list describing the hub.* skills and add a `hub.refresh-site` entry in the same style as its neighbors (one short paragraph or table row): config location (`work/refresh-<slug>.yaml`), gated flow, disclosure contract, CI as link authority.

In `docs/tooling.md`: find the hublib module inventory (list or table naming `schema.py`, `disclosure.py`, `publisher.py`, ...) and add in the same style:

```markdown
`refresh.py` - refresh-site config find/load/validate (work/refresh-<slug>.yaml); findings fold into lint_repo
```

Also update any `disclosure.py` / `publisher.py` descriptions in that inventory that now understate scope (generated-md surfaces; template + snapshot v2) with one-line touch-ups.

- [ ] **Step 4: publishing docs**

In `conventions/publishing.md`, append a short section:

```markdown
## Landing page + snapshot (v2)

The pages-site landing page is rendered from `publish/landing-template.html`
(tracked; self-contained inline CSS): artifacts grouped by area (feature
`title` from features/features.yaml, routing-table order, Narrative last),
one card per artifact, NEW/UPDATED badges for artifacts published or changed
in the last 14 days. Badge state lives in `.publish-snapshot.json` (v2:
`{dest: {source, hash, published, badge}}`); v1 snapshots migrate on the
first run with no false badges.
```

In `docs/publishing.md`, add a matching one-paragraph note wherever the landing page / snapshot is described (same content, guide voice).

- [ ] **Step 5: enhancements.md bookkeeping**

In `docs/enhancements.md`:
- Delete the priority-table rows for #4, #8, and #34.
- Delete the full body sections for **8** (Human-usage) and **4** (Repo functionality) and the **34** row context if any section exists.
- Add to the top of `## Done`:

```markdown
- **#34 + #8 + #4 published-site trust batch** - shipped 2026-07-10:
  heuristic over full entry text + generated views/indexes in the disclosure
  scan surface (#34); full-branded grouped landing page with snapshot-v2
  NEW/UPDATED badges (#8); hub.refresh-site skill + tracked
  refresh-<slug>.yaml configs for the RHCL and Management hubs, with the
  disclosure contract the old update skills lacked (#4). Spec:
  [/docs/specs/2026-07-10-published-site-trust-batch-design.md](/docs/specs/2026-07-10-published-site-trust-batch-design.md).
  Plan: [/docs/plans/2026-07-10-published-site-trust-batch-plan.md](/docs/plans/2026-07-10-published-site-trust-batch-plan.md).
```

- Update the `Last groomed:` date if today differs.

- [ ] **Step 6: Verify and commit**

Run: `python -m pytest scripts/tests -v` -> all PASS.
Run: `python scripts/hub_index.py` (docs/AGENTS edits may not need it, but the pre-commit check must be clean), then `python scripts/hub_lint.py` -> 0 errors.

```bash
git add .claude/skills/hub.refresh-site/ AGENTS.md docs/skills.md docs/tooling.md docs/publishing.md conventions/publishing.md docs/enhancements.md
git commit -m "refresh: hub.refresh-site skill, docs, backlog Done (#34 #8 #4)

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

### Task 9: OWNER-GATED acceptance run: RHCL hub (main session)

Not a subagent task. In the main session, after Tasks 1-8 are merged and pushed (publish.yml green, new landing page live):

- [ ] Invoke `hub.refresh-site` for `rhcl-hub` and follow it end to end: staleness scan, 5-source sweep (expect possible Slack fetch failure; that is a pass if reported correctly), change report, owner gate, surgical edits, data-verified bumps, lint clean, commit, push, `gh run watch` green.
- [ ] Verify live: `curl -sI https://solaius.github.io/rhoai-agentic-hub-pages/mcp-gateway/rhcl/ | head -1` -> 200; landing page shows the UPDATED badge on the RHCL hub card.
- [ ] Record friction in the plan doc (`## Acceptance outcomes` section, create it) and fix small issues before Task 10.

### Task 10: OWNER-GATED acceptance run: Management hub (main session)

- [ ] Same flow for `management-hub` with Task 9 fixes applied. Verify `mcp-ecosystem/hub/` live and badged.
- [ ] Append the outcome note + offer hub.capture for the closing log line (batch shipped).

## Execution notes for the coordinator

- Tasks must run in order 1 -> 8 (2 depends on 1 only for real-repo warning counts; 4-5 depend on 3; 7 depends on 6; 8 depends on 6-7). Run them sequentially with review between tasks.
- Tasks 1 and 2 change what `hub_lint.py` warns about on the REAL repo. Their reports must list the new warnings verbatim so the owner can triage them (precedent: fact-disclosure-warning-triage-2026-07-10).
- Task 5 produces `../landing-preview.html` OUTSIDE the repo for the owner to eyeball; delete it after review.
- Push once after Task 8 review (publish.yml then ships the new landing page), before Task 9.

## Acceptance outcomes

**Task 9 (RHCL hub) - 2026-07-10, commit 03e3d04, publish run 29136086438 green.**
5-source sweep (all succeeded; 2 workarounds), 15 gated change-sets approved
with two owner rulings (Kagenti roadmap removal with OpenShell expansion;
RHCL moved to the AI BU with MaaS-entitlement parity expected, pending
confirmation), 20 pages updated, landing page shows its first UPDATED badge.
Friction found and fixed before Task 10:

- RHCL Overview Deck is a Slides file: `get_doc_as_markdown` 404s; skill now
  documents the `get_presentation` fallback.
- Sweep findings must carry source-table cell values verbatim: the first
  competitive-matrix apply drew on general knowledge and needed a 65-cell
  true-up pass against the source doc; skill now mandates verbatim carry.
- Slack MCP channel-name cache broken (`get_channel_id_by_name` empty,
  `refresh_channel_cache` false); workaround: resolve channel IDs via
  `search_messages`. Candidate hub.doctor probe follow-up.
- `#mcp-gateway-dev` archived 2026-07-02: removed from the RHCL config.
- Upstream drift found mid-apply beyond the sweep findings (MCPServer Kind
  split into MCPServerRegistration/MCPVirtualServer; MCPGatewayExtension
  field set changed): resolved by verify-then-apply against fetched CRD
  yamls; skill now states the verify-before-edit rule for version-sensitive
  claims.

**Task 10 (Management hub) - 2026-07-10/11, commit 0e21278, publish run 29139337802 green.**
6-agent sweep (5 sources + a design/content review framed on the hub's
future umbrella role), 13 gated change-sets + 12 design apply-now items
approved with 5 owner rulings (future hub slugs confirmed; individuals
genericized; partner name anonymized; RHCL reverse links; structural
B-items deferred to the recorded plan). 22 pages + nav.js + styles.css
updated; RHCL hub gained reverse links; umbrella devolution plan recorded
at features/mcp-ecosystem/work/management-hub-umbrella-plan.md; backlog #35
filed. Both hub cards now carry UPDATED badges. Friction fixed in-run:
gdocs token-limit overruns handled by forked persisted-file extraction; the
Slack channel-cache workaround folded into the skill; 4 more inherited
config mislabels corrected against live docs; the verify-before-edit rule
caught a wrong repo attribution in a source doc (kuadrant/mcp-controller
does not exist) and a source-doc CRD shape confirmed against upstream
before rewrite. New CI-visible warning for owner triage:
management-hub govern/entitlement.html:91 (heuristic matches the owner's
own supersession caveat wording; benign by construction).
BOTH ACCEPTANCE RUNS COMPLETE - the published-site trust batch (#34 #8 #4)
is fully accepted.
