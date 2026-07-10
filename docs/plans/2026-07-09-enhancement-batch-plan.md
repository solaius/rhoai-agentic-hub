# Enhancement Batch Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship backlog items #5 (disclosure lint), #7 (pre-commit hook), #10 (recorded small fixes incl. log rotation), #15 (hub_status morning brief), #16 (published-site link checker) as one batch.

**Architecture:** Follow the repo idiom strictly — small `hublib/` modules with thin CLI wrappers and per-module tests. New modules: `disclosure.py`, `status.py`, `logrotate.py`. Extended: `schema.py`, `indexer.py`, `publisher.py`, `doctor.sh`. Spec: `/docs/specs/2026-07-09-enhancement-batch-design.md`.

**Tech Stack:** Python 3.12, pyyaml + pytest only (no new dependencies), bash (doctor), GitHub Actions.

## Global Constraints

- **No new Python dependencies** — stdlib + pyyaml + pytest only.
- **Findings contract:** lint findings are strings `"<relpath>: <message>"`; functions return `(errors, warnings)` tuples, matching `schema.lint_repo`.
- **File writes:** always `encoding="utf-8", newline="\n"`.
- **Public repo:** never use real customer/program names in code, tests, or fixtures — use `acme` / `globex` style placeholders.
- **Never hand-edit generated files** (`views/*`, `*/index.md`, `memory/index.md`) — run `python scripts/hub_index.py` and commit its output.
- **`schema.py` merge discipline:** a concurrent workstream also edits `schema.py`/`test_schema.py` (research-doc lint). Keep edits surgical — touch only the lines named in each task.
- **NEVER run `bash scripts/doctor.sh setup`** in this plan — it writes MCP credentials into the user's Claude config. Verification uses `check` mode and a scratch clone only.
- Tests run from the repo root: `python -m pytest scripts/tests -v` (conftest.py puts `scripts/` on `sys.path`).
- This environment is Windows + Git Bash; in a git **worktree**, `.git` is a file — resolve the hooks dir via `git rev-parse --git-path hooks`, never hardcode `.git/hooks`.

---

### Task 1: Harden the public restricted-content heuristic

**Files:**
- Modify: `scripts/hublib/schema.py:63-65` (the `RESTRICTED_HINTS` constant)
- Test: `scripts/tests/test_schema.py`

**Interfaces:**
- Produces: `schema.RESTRICTED_HINTS` (compiled regex, case-insensitive) additionally matching dollar figures (`\$\d`) and signed-agreement phrasing (`signed[^.\n]{0,40}agreement`). Task 3 imports this constant.

- [ ] **Step 1: Write the failing tests** — append to `scripts/tests/test_schema.py`:

```python
def test_dollar_figure_hint_is_warning(tmp_path):
    root = make_repo(tmp_path)
    write(root, "features/x/knowledge/fact-a.md",
          ENTRY.format(t="fact", extra="") + "Deal size was $2.4M for year one.\n")
    errors, warnings = lint_repo(root)
    assert errors == []
    assert any("restricted-content heuristic" in w for w in warnings)


def test_signed_agreement_hint_is_warning(tmp_path):
    root = make_repo(tmp_path)
    write(root, "features/x/knowledge/fact-a.md",
          ENTRY.format(t="fact", extra="")
          + "They signed a strategic collaboration agreement last week.\n")
    _, warnings = lint_repo(root)
    assert any("restricted-content heuristic" in w for w in warnings)
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python -m pytest scripts/tests/test_schema.py -k "dollar or signed_agreement" -v`
Expected: 2 FAILED (no warning produced).

- [ ] **Step 3: Extend the constant** — in `scripts/hublib/schema.py` replace:

```python
RESTRICTED_HINTS = re.compile(
    r"\bSKU[- ]?\d|\bpricing tier\b|\binternal[- ]only\b|\bdo not share\b|\bNDA\b",
    re.IGNORECASE)
```

with:

```python
RESTRICTED_HINTS = re.compile(
    r"\bSKU[- ]?\d|\bpricing tier\b|\binternal[- ]only\b|\bdo not share\b|\bNDA\b"
    r"|\$\d|signed[^.\n]{0,40}agreement",
    re.IGNORECASE)
```

- [ ] **Step 4: Run the full schema suite**

Run: `python -m pytest scripts/tests/test_schema.py -v`
Expected: all PASS.

- [ ] **Step 5: Commit**

```bash
git add scripts/hublib/schema.py scripts/tests/test_schema.py
git commit -m "feat(lint): RESTRICTED_HINTS learns dollar figures and signed-agreement phrasing (#5)"
```

---

### Task 2: Pillar leading-slash warning

**Files:**
- Modify: `scripts/hublib/schema.py:179-182` (story branch at the end of `lint_entry`)
- Test: `scripts/tests/test_schema.py`

**Interfaces:**
- Consumes: existing `lint_entry` story branch.
- Produces: a warning when a story's `pillar:` value does not start with `/`.

- [ ] **Step 1: Write the failing test** — append to `scripts/tests/test_schema.py`:

```python
def test_story_pillar_without_leading_slash_is_warning(tmp_path):
    root = make_repo(tmp_path)
    write(root, "features/features.yaml", FEATURES_YAML)
    write(root, "narrative/knowledge/pillar-agents.md", ENTRY.format(t="pillar", extra=""))
    write(root, "narrative/knowledge/story-a.md",
          ENTRY.format(t="story", extra="features: [mcp-registry]\n"
                                        "pillar: narrative/knowledge/pillar-agents.md\n"))
    errors, warnings = lint_repo(root)
    assert errors == []
    assert any("leading-slash" in w for w in warnings)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest scripts/tests/test_schema.py::test_story_pillar_without_leading_slash_is_warning -v`
Expected: FAIL (no such warning; the file exists so the dangling check stays quiet).

- [ ] **Step 3: Implement** — in `scripts/hublib/schema.py` replace the story branch:

```python
    if etype == "story" and meta.get("pillar"):
        target = str(meta["pillar"])
        if not (root / target.lstrip("/")).exists():
            warnings.append(f"{rel}: pillar target {target} does not exist (dangling)")
```

with:

```python
    if etype == "story" and meta.get("pillar"):
        target = str(meta["pillar"])
        if not target.startswith("/"):
            warnings.append(f"{rel}: pillar '{target}' should be a leading-slash root "
                            f"path — this story will not attach to its pillar in the "
                            f"narrative map")
        elif not (root / target.lstrip("/")).exists():
            warnings.append(f"{rel}: pillar target {target} does not exist (dangling)")
```

- [ ] **Step 4: Run the schema suite** (`test_story_dangling_pillar_is_warning` must still pass)

Run: `python -m pytest scripts/tests/test_schema.py -v`
Expected: all PASS.

- [ ] **Step 5: Commit**

```bash
git add scripts/hublib/schema.py scripts/tests/test_schema.py
git commit -m "fix(lint): warn on story pillar path missing its leading slash (#10)"
```

---

### Task 3: Disclosure lint module

**Files:**
- Create: `scripts/hublib/disclosure.py`
- Test: `scripts/tests/test_disclosure.py`

**Interfaces:**
- Consumes: `schema.RESTRICTED_HINTS` (Task 1's extended version, but tests below only rely on pre-existing hint words so this task is order-independent).
- Produces: `disclosure.scan_repo(root) -> (errors, warnings)` and `disclosure.load_patterns(root) -> (patterns, warnings)`. Task 4 wires `scan_repo` into the CLI.

- [ ] **Step 1: Write the failing tests** — create `scripts/tests/test_disclosure.py`:

```python
from pathlib import Path

from hublib.disclosure import load_patterns, scan_repo


def write(root: Path, rel: str, text: str):
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8", newline="\n")
    return p


def test_no_pattern_file_no_errors(tmp_path):
    write(tmp_path, "features/x/enablement/deck/index.html", "<p>Acme Corp content</p>")
    errors, _ = scan_repo(tmp_path)
    assert errors == []


def test_pattern_match_in_html_is_error_with_both_linenos(tmp_path):
    write(tmp_path, "restricted/lint-patterns.txt", "# customer names\nacme\n")
    write(tmp_path, "features/x/enablement/deck/index.html",
          "<html>\n<p>ACME Corp deal</p>\n</html>")
    errors, _ = scan_repo(tmp_path)
    assert errors == ["features/x/enablement/deck/index.html:2: "
                      "matches restricted pattern (lint-patterns.txt:2)"]


def test_pattern_match_in_knowledge_md_including_frontmatter(tmp_path):
    write(tmp_path, "restricted/lint-patterns.txt", "globex\n")
    write(tmp_path, "features/x/knowledge/fact-a.md",
          "---\ntype: fact\ndescription: Globex asked for it\ntimestamp: 2026-07-09\n"
          "---\nbody\n")
    errors, _ = scan_repo(tmp_path)
    assert errors == ["features/x/knowledge/fact-a.md:3: "
                      "matches restricted pattern (lint-patterns.txt:1)"]


def test_narrative_surfaces_scanned(tmp_path):
    write(tmp_path, "restricted/lint-patterns.txt", "acme\n")
    write(tmp_path, "narrative/enablement/deck/index.html", "<p>acme</p>")
    write(tmp_path, "narrative/knowledge/story-a.md", "acme\n")
    errors, _ = scan_repo(tmp_path)
    assert len(errors) == 2


def test_invalid_regex_warns_and_rest_still_applies(tmp_path):
    write(tmp_path, "restricted/lint-patterns.txt", "[unclosed\nacme\n")
    write(tmp_path, "features/x/enablement/deck/index.html", "<p>acme</p>")
    errors, warnings = scan_repo(tmp_path)
    assert any(w.startswith("restricted/lint-patterns.txt:1: invalid regex")
               for w in warnings)
    assert any("(lint-patterns.txt:2)" in e for e in errors)


def test_comments_and_blank_lines_skipped(tmp_path):
    write(tmp_path, "restricted/lint-patterns.txt", "\n# comment\n\nacme\n")
    patterns, warnings = load_patterns(tmp_path)
    assert [n for n, _ in patterns] == [4]
    assert warnings == []


def test_restricted_tree_never_scanned(tmp_path):
    write(tmp_path, "restricted/lint-patterns.txt", "acme\n")
    write(tmp_path, "restricted/features/x/enablement/deck/index.html", "<p>acme</p>")
    write(tmp_path, "restricted/features/x/knowledge/fact-a.md", "acme\n")
    errors, _ = scan_repo(tmp_path)
    assert errors == []


def test_generic_hints_warn_on_enablement_html(tmp_path):
    write(tmp_path, "features/x/enablement/deck/index.html",
          "<html>\n<p>this deck is internal-only, do not share</p>\n</html>")
    errors, warnings = scan_repo(tmp_path)
    assert errors == []
    assert any(w.startswith("features/x/enablement/deck/index.html:2: "
                            "restricted-content heuristic") for w in warnings)


def test_generic_hints_do_not_double_report_knowledge_md(tmp_path):
    # lint_entry (schema.py) already warns on md bodies; disclosure must not repeat it
    write(tmp_path, "features/x/knowledge/fact-a.md",
          "---\ntype: fact\ndescription: d\ntimestamp: 2026-07-09\n---\ninternal-only\n")
    _, warnings = scan_repo(tmp_path)
    assert warnings == []
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python -m pytest scripts/tests/test_disclosure.py -v`
Expected: collection ERROR — `ModuleNotFoundError: No module named 'hublib.disclosure'`.

- [ ] **Step 3: Implement** — create `scripts/hublib/disclosure.py`:

```python
"""Local-first disclosure lint. Two passes over the PUBLIC tree only:
restricted patterns from a gitignored file (errors — CI never has the file),
and the generic public heuristic over enablement HTML (warnings, CI-visible).
Findings are '<relpath>: <message>' strings; (errors, warnings) tuples,
matching schema.lint_repo. Error text references patterns by line NUMBER,
never pattern text — lint output can get pasted into public places."""
import re
from pathlib import Path

from .schema import RESTRICTED_HINTS

PATTERN_FILE = "restricted/lint-patterns.txt"


def load_patterns(root):
    """Read the optional gitignored pattern file: one case-insensitive regex
    per line; '#' comments and blank lines skipped. Invalid regexes are
    skipped with a warning — a typo must never silently disable the net."""
    path = Path(root) / PATTERN_FILE
    patterns, warnings = [], []
    if not path.is_file():
        return patterns, warnings
    for lineno, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        try:
            patterns.append((lineno, re.compile(line, re.IGNORECASE)))
        except re.error as exc:
            warnings.append(f"{PATTERN_FILE}:{lineno}: invalid regex (skipped): {exc}")
    return patterns, warnings


def _scan_files(root):
    """The public scan surface: enablement HTML + knowledge entries."""
    root = Path(root)
    for pattern in ("features/*/enablement/**/*.html",
                    "narrative/enablement/**/*.html",
                    "features/*/knowledge/*.md",
                    "narrative/knowledge/*.md"):
        yield from sorted(root.glob(pattern))


def scan_repo(root):
    root = Path(root)
    patterns, warnings = load_patterns(root)
    errors = []
    for f in _scan_files(root):
        rel = f.relative_to(root).as_posix()
        is_html = f.suffix == ".html"
        for n, line in enumerate(
                f.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            for lineno, pat in patterns:
                if pat.search(line):
                    errors.append(f"{rel}:{n}: matches restricted pattern "
                                  f"(lint-patterns.txt:{lineno})")
            # md bodies already get the heuristic in lint_entry — HTML only here
            if is_html and RESTRICTED_HINTS.search(line):
                warnings.append(f"{rel}:{n}: restricted-content heuristic matched — "
                                f"confirm this belongs in a public repo")
    return errors, warnings
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `python -m pytest scripts/tests/test_disclosure.py -v`
Expected: 9 PASS.

- [ ] **Step 5: Commit**

```bash
git add scripts/hublib/disclosure.py scripts/tests/test_disclosure.py
git commit -m "feat(lint): disclosure module — gitignored restricted patterns + generic HTML heuristic (#5)"
```

---

### Task 4: Wire disclosure into the lint CLI

**Files:**
- Modify: `scripts/hub_lint.py`

**Interfaces:**
- Consumes: `disclosure.scan_repo(root)` (Task 3), `schema.lint_repo(root)`.
- Produces: `python scripts/hub_lint.py` reporting merged findings — every downstream runner (CI, doctor section 6, the Task 8 hook) inherits the net.

- [ ] **Step 1: Modify `scripts/hub_lint.py`** — replace the whole file with:

```python
"""CLI: lint the hub. Exit 1 on errors; warnings never fail the build."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from hublib import disclosure
from hublib.schema import lint_repo


def main():
    root = Path(__file__).resolve().parents[1]
    errors, warnings = lint_repo(root)
    d_errors, d_warnings = disclosure.scan_repo(root)
    errors += d_errors
    warnings += d_warnings
    for w in warnings:
        print(f"WARN  {w}")
    for e in errors:
        print(f"ERROR {e}")
    print(f"hub_lint: {len(errors)} error(s), {len(warnings)} warning(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 2: Integration check on the real repo**

Run: `python scripts/hub_lint.py`
Expected: exit 0 (`0 error(s)`). New warnings from the hardened heuristic over existing enablement HTML are acceptable — **record the warning count in your task report** so the main session can judge noise.

- [ ] **Step 3: Full suite**

Run: `python -m pytest scripts/tests -v`
Expected: all PASS.

- [ ] **Step 4: Commit**

```bash
git add scripts/hub_lint.py
git commit -m "feat(lint): hub_lint runs the disclosure scan alongside lint_repo (#5)"
```

---

### Task 5: Indexer recorded fixes — faq heading + test gaps

**Files:**
- Modify: `scripts/hublib/indexer.py:320` (the `"## All, by feature"` line)
- Test: `scripts/tests/test_indexer.py` (1 assertion update + 3 new tests)
- Regenerate: `views/faq.md` (via `python scripts/hub_index.py`)

**Interfaces:**
- Consumes: existing `build_all`.
- Produces: `views/faq.md` grouping heading reads "All, by home".

- [ ] **Step 1: Update + add tests** — in `scripts/tests/test_indexer.py`, change the last assertion of `test_faq_view` from:

```python
    assert "## All, by feature" in v and "### mcp-registry" in v
```

to:

```python
    assert "## All, by home" in v and "### mcp-registry" in v
```

Then append the three recorded-gap tests:

```python
def test_connections_sorted_multi_item(tmp_path):
    root = make_repo(tmp_path)
    write(root, "features/features.yaml",
          "features:\n- id: mcp-registry\n  title: R\n  description: d\n"
          "- id: mcp-gateway\n  title: G\n  description: d\n")
    write(root, "features/mcp-gateway/knowledge/fact-zeta.md",
          "---\ntype: fact\ntitle: Zeta\ndescription: d\ntimestamp: 2026-07-01\n"
          "features: [mcp-registry]\n---\nb\n")
    write(root, "features/mcp-gateway/knowledge/fact-alpha.md",
          "---\ntype: fact\ntitle: Alpha\ndescription: d\ntimestamp: 2026-07-02\n"
          "features: [mcp-registry]\n---\nb\n")
    idx = build_all(root, today=TODAY)["features/mcp-registry/index.md"]
    assert "## Connections" in idx
    assert idx.index("Alpha") < idx.index("Zeta")  # sorted by rootpath


def test_connections_combine_entries_and_artifacts(tmp_path):
    root = make_repo(tmp_path)
    write(root, "features/features.yaml",
          "features:\n- id: mcp-registry\n  title: R\n  description: d\n"
          "- id: mcp-gateway\n  title: G\n  description: d\n")
    write(root, "features/mcp-gateway/knowledge/fact-conn.md",
          "---\ntype: fact\ntitle: Conn Fact\ndescription: d\ntimestamp: 2026-07-01\n"
          "features: [mcp-registry]\n---\nb\n")
    write(root, "features/mcp-gateway/enablement/deck/artifact.md",
          "---\ntype: artifact\ntitle: Conn Deck\ndescription: d\ntimestamp: 2026-07-01\n"
          "features: [mcp-registry]\n---\nb\n")
    idx = build_all(root, today=TODAY)["features/mcp-registry/index.md"]
    assert "Conn Fact" in idx and "Conn Deck" in idx


def test_empty_narrative_dir_is_safe(tmp_path):
    root = make_repo(tmp_path)
    (root / "narrative").mkdir()
    built = build_all(root, today=TODAY)
    assert "narrative/index.md" in built
    assert "narrative/knowledge/index.md" not in built
```

- [ ] **Step 2: Run to verify the heading test fails and gap tests pass/fail honestly**

Run: `python -m pytest scripts/tests/test_indexer.py -v`
Expected: `test_faq_view` FAILS (heading not renamed yet); the three new tests may already pass (they codify existing behavior — that is the point of recorded gaps).

- [ ] **Step 3: Rename the heading** — in `scripts/hublib/indexer.py` change:

```python
        lines.append("## All, by feature")
```

to:

```python
        lines.append("## All, by home")
```

- [ ] **Step 4: Run the indexer suite**

Run: `python -m pytest scripts/tests/test_indexer.py -v`
Expected: all PASS.

- [ ] **Step 5: Regenerate real indexes and verify freshness**

Run: `python scripts/hub_index.py && python scripts/hub_index.py --check`
Expected: `WROTE …` lines including `views/faq.md`, then `0 stale file(s)`.

- [ ] **Step 6: Commit (include regenerated views)**

```bash
git add scripts/hublib/indexer.py scripts/tests/test_indexer.py views/
git commit -m "fix(index): faq groups by home; codify connections + empty-narrative behavior in tests (#10)"
```

---

### Task 6: stale_rows extraction + status module

**Files:**
- Modify: `scripts/hublib/indexer.py` (extract `stale_rows` from `build_all`)
- Create: `scripts/hublib/status.py`
- Test: `scripts/tests/test_status.py`

**Interfaces:**
- Consumes: `indexer._load_entries`, `indexer._home`, `indexer._staleness_config`, `frontmatter.load_file`.
- Produces: `indexer.stale_rows(root, today=None) -> list[str]` (the exact rows of `views/stale-facts.md`, unsorted); `status.build_brief(root, today=None) -> str`. Task 7's CLI prints `build_brief`.

- [ ] **Step 1: Extract `stale_rows` in `scripts/hublib/indexer.py`.** Add this function above `build_all` (after `_load_artifacts`):

```python
def stale_rows(root, today=None):
    """Overdue rows for views/stale-facts.md — shared with hublib.status so
    the view and the morning brief cannot drift."""
    root = Path(root)
    today = today or datetime.date.today()
    cfg = _staleness_config(root)
    entries = list(_load_entries(root, "*/knowledge/*.md"))
    entries += list(_load_entries(root, "knowledge/*.md", base="narrative"))
    mem = root / "memory"
    rows = []
    mem_files = []
    if (mem / "profiles").is_dir():
        mem_files += [("profile", p) for p in sorted((mem / "profiles").glob("*.md"))]
    if (mem / "facts").is_dir():
        mem_files += [("fact", p) for p in sorted((mem / "facts").glob("*.md"))]
    for kind, p in mem_files:
        meta = _meta_of(p)
        if not meta or meta.get("status") == "superseded":
            continue
        rootpath = "/" + p.relative_to(root).as_posix()
        review = _date(meta.get("review_after"))
        ts = _date(meta.get("timestamp"))
        limit = cfg["profile_default_days"] if kind == "profile" else cfg["fact_default_days"]
        overdue = (review and review < today) or (
            not review and ts and (today - ts).days > limit)
        if overdue:
            age = (today - ts).days if ts else "?"
            rows.append(f"- {rootpath} — {meta.get('description', '')} (age {age}d)")
    for rp, m, _ in entries:
        if m.get("type") == "fact" and m.get("status") != "superseded":
            ts = _date(m.get("timestamp"))
            if ts and (today - ts).days > cfg["fact_default_days"]:
                rows.append(f"- {rp} — {m.get('description', '')} "
                            f"(age {(today - ts).days}d)")
    for rp, m, _ in entries:
        if m.get("type") in ("qa", "jtbd"):
            review = _date(m.get("review_after"))
            if review and review < today:
                rows.append(f"- {rp} — {m.get('description', '')} "
                            f"(review overdue)")
    return rows
```

Then in `build_all`, delete the inline block from `stale_rows = []` / `mem_files = []` down to (but not including) the `built["views/stale-facts.md"]` line, and replace the view assembly with:

```python
    built["views/stale-facts.md"] = \
        "\n".join([MARKER + "# Stale facts & profiles", ""] + sorted(stale_rows(root, today))) + "\n"
```

(The old inline code used local variable name `stale_rows` for its list — the function replaces it entirely; make sure no local variable shadows the function name. Also delete the now-unused `cfg = _staleness_config(root)` line at the top of `build_all`'s `# views/` block — the helper loads its own config.)

- [ ] **Step 2: Verify the refactor is behavior-neutral**

Run: `python -m pytest scripts/tests/test_indexer.py -v && python scripts/hub_index.py --check`
Expected: all PASS and `0 stale file(s)` (identical generated output).

- [ ] **Step 3: Write the failing status tests** — create `scripts/tests/test_status.py`:

```python
import datetime
from pathlib import Path

from hublib.status import build_brief


def write(root: Path, rel: str, text: str):
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8", newline="\n")
    return p


TODAY = datetime.date(2026, 7, 5)


def make_repo(tmp_path: Path) -> Path:
    write(tmp_path, "conventions/staleness.yaml",
          "profile_default_days: 30\nfact_default_days: 90\n")
    write(tmp_path, "features/features.yaml",
          "features:\n- id: mcp-registry\n  title: R\n  description: d\n")
    write(tmp_path, "memory/log.md",
          "---\ntype: fact\ndescription: log\ntimestamp: 2026-07-05\n---\n"
          "## 2026-07-05\n- **Update** — newest thing.\n"
          "## 2026-07-01\n- **Creation** — older thing.\n")
    return tmp_path


def test_minimal_repo_header_only(tmp_path):
    brief = build_brief(make_repo(tmp_path), today=TODAY)
    assert brief.startswith("# Hub status — 2026-07-05")
    assert "## Stale" not in brief          # empty sections omitted
    assert "## Open questions" not in brief
    assert "## Log rotation due" not in brief
    assert "## Recent log" in brief and "newest thing" in brief


def test_open_questions_counted_by_home(tmp_path):
    root = make_repo(tmp_path)
    write(root, "features/mcp-registry/knowledge/question-a.md",
          "---\ntype: question\ntitle: A?\ndescription: d\ntimestamp: 2026-07-01\n"
          "status: open\n---\nb\n")
    write(root, "narrative/knowledge/question-b.md",
          "---\ntype: question\ntitle: B?\ndescription: d\ntimestamp: 2026-07-01\n"
          "status: open\n---\nb\n")
    brief = build_brief(root, today=TODAY)
    assert "## Open questions (2)" in brief
    assert "mcp-registry: 1" in brief and "narrative: 1" in brief


def test_unanswered_qa_and_bare_jtbd_listed(tmp_path):
    root = make_repo(tmp_path)
    write(root, "features/mcp-registry/knowledge/qa-open.md",
          "---\ntype: qa\ntitle: Quotas?\ndescription: d\ntimestamp: 2026-07-02\n"
          "status: open\nasks:\n- date: 2026-07-02\n  by: sales\n---\nb\n")
    write(root, "features/mcp-registry/knowledge/jtbd-bare.md",
          "---\ntype: jtbd\ntitle: Bare job\ndescription: d\ntimestamp: 2026-07-01\n"
          "persona: rhoai-admin\nstatus: validated\n---\nb\n")
    brief = build_brief(root, today=TODAY)
    assert "## Unanswered qa (1)" in brief and "Quotas?" in brief
    assert "## JTBD lacking evidence (1)" in brief and "Bare job" in brief


def test_stale_section_uses_shared_rows(tmp_path):
    root = make_repo(tmp_path)
    write(root, "memory/profiles/roadmap.md",
          "---\ntype: profile\ndescription: dates\ntimestamp: 2026-05-01\n"
          "review_after: 2026-06-01\nstatus: current\n---\nb\n")
    brief = build_brief(root, today=TODAY)
    assert "## Stale (1)" in brief and "/memory/profiles/roadmap.md" in brief


def test_undescriptored_enablement_dir_listed(tmp_path):
    root = make_repo(tmp_path)
    write(root, "features/mcp-registry/enablement/bare/index.html", "<html></html>")
    brief = build_brief(root, today=TODAY)
    assert "## Enablement dirs missing artifact.md (1)" in brief
    assert "/features/mcp-registry/enablement/bare" in brief


def test_rotation_reminder_only_with_old_years(tmp_path):
    root = make_repo(tmp_path)
    assert "## Log rotation due" not in build_brief(root, today=TODAY)
    write(root, "memory/log.md",
          "---\ntype: fact\ndescription: log\ntimestamp: 2026-07-05\n---\n"
          "## 2026-07-05\n- **Update** — new.\n"
          "## 2025-12-01\n- **Creation** — old.\n")
    brief = build_brief(root, today=TODAY)
    assert "## Log rotation due" in brief and "--rotate-log" in brief
```

- [ ] **Step 4: Run tests to verify they fail**

Run: `python -m pytest scripts/tests/test_status.py -v`
Expected: collection ERROR — `No module named 'hublib.status'`.

- [ ] **Step 5: Implement** — create `scripts/hublib/status.py`:

```python
"""One-page morning brief: where the hub needs attention. Read-only;
sections with nothing to say are omitted entirely."""
import datetime
from pathlib import Path

from . import frontmatter
from .indexer import _home, _load_entries, stale_rows


def _log_body(root):
    log = Path(root) / "memory" / "log.md"
    if not log.is_file():
        return None
    try:
        return frontmatter.load_file(log)[1]
    except frontmatter.FrontmatterError:
        return None


def _previous_years(body, today):
    years = set()
    for raw in (body or "").splitlines():
        if raw.startswith("## "):
            try:
                d = datetime.date.fromisoformat(raw[3:].strip())
            except ValueError:
                continue
            if d.year < today.year:
                years.add(d.year)
    return sorted(years)


def build_brief(root, today=None):
    root = Path(root)
    today = today or datetime.date.today()
    entries = list(_load_entries(root, "*/knowledge/*.md"))
    entries += list(_load_entries(root, "knowledge/*.md", base="narrative"))
    sections = [f"# Hub status — {today.isoformat()}"]

    rows = stale_rows(root, today)
    if rows:
        sections.append(f"## Stale ({len(rows)})\n" + "\n".join(sorted(rows)))

    open_qs = [rp for rp, m, _ in entries
               if m.get("type") == "question" and m.get("status") == "open"]
    if open_qs:
        counts = {}
        for rp in open_qs:
            counts[_home(rp)] = counts.get(_home(rp), 0) + 1
        listing = " · ".join(f"{h}: {n}" for h, n in sorted(counts.items()))
        sections.append(f"## Open questions ({len(open_qs)})\n{listing}")

    open_qa = sorted((rp, m) for rp, m, _ in entries
                     if m.get("type") == "qa" and m.get("status") == "open")
    if open_qa:
        lines = [f"- {_home(rp)} · [{m.get('title') or Path(rp).stem}]({rp})"
                 for rp, m in open_qa]
        sections.append(f"## Unanswered qa ({len(open_qa)})\n" + "\n".join(lines))

    bare = sorted((rp, m) for rp, m, _ in entries if m.get("type") == "jtbd"
                  and not (isinstance(m.get("evidence"), list) and m["evidence"]))
    if bare:
        lines = [f"- {_home(rp)} · [{m.get('title') or Path(rp).stem}]({rp})"
                 for rp, m in bare]
        sections.append(f"## JTBD lacking evidence ({len(bare)})\n" + "\n".join(lines))

    undesc = []
    for pattern in ("features/*/enablement/*", "narrative/enablement/*"):
        for slug in sorted(root.glob(pattern)):
            if slug.is_dir() and not (slug / "artifact.md").is_file():
                undesc.append("/" + slug.relative_to(root).as_posix())
    if undesc:
        sections.append(f"## Enablement dirs missing artifact.md ({len(undesc)})\n"
                        + "\n".join(f"- {p}" for p in undesc))

    body = _log_body(root)
    years = _previous_years(body, today)
    if years:
        sections.append("## Log rotation due\n"
                        f"memory/log.md holds {', '.join(str(y) for y in years)} "
                        "entries — run: python scripts/hub_index.py --rotate-log")

    if body:
        recent, current = [], None
        for raw in body.splitlines():
            if raw.startswith("## "):
                current = raw[3:].strip()
            elif raw.startswith("- ") and current and len(recent) < 5:
                recent.append(f"- {current} — {raw[2:].strip()}")
        if recent:
            sections.append("## Recent log\n" + "\n".join(recent))

    return "\n\n".join(sections) + "\n"
```

- [ ] **Step 6: Run tests to verify they pass**

Run: `python -m pytest scripts/tests/test_status.py scripts/tests/test_indexer.py -v`
Expected: all PASS.

- [ ] **Step 7: Commit**

```bash
git add scripts/hublib/indexer.py scripts/hublib/status.py scripts/tests/test_status.py scripts/tests/test_indexer.py
git commit -m "feat(status): morning-brief module; stale rows shared with the stale view (#15)"
```

---

### Task 7: hub_status CLI

**Files:**
- Create: `scripts/hub_status.py`

**Interfaces:**
- Consumes: `status.build_brief` (Task 6).
- Produces: `python scripts/hub_status.py` — prints the brief plus an optional `## CI (last push)` section via `gh`; always exits 0.

- [ ] **Step 1: Create `scripts/hub_status.py`:**

```python
"""CLI: print the morning brief. Informational — always exits 0. The CI
section lives here (not in hublib.status) so build_brief stays testable
without gh; any gh failure silently skips the section."""
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from hublib.status import build_brief


def _ci_section():
    try:
        out = subprocess.run(
            ["gh", "run", "list", "--branch", "main", "--limit", "1"],
            capture_output=True, text=True, timeout=10)
    except (OSError, subprocess.TimeoutExpired):
        return None
    if out.returncode != 0 or not out.stdout.strip():
        return None
    return "## CI (last push)\n" + out.stdout.strip()


def main():
    root = Path(__file__).resolve().parents[1]
    print(build_brief(root), end="")
    ci = _ci_section()
    if ci:
        print("\n" + ci)
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 2: Smoke-run on the real repo**

Run: `python scripts/hub_status.py`
Expected: exit 0; a `# Hub status — <today>` header, plausible sections (Recent log at minimum), no traceback. Paste the output into your task report.

- [ ] **Step 3: Commit**

```bash
git add scripts/hub_status.py
git commit -m "feat(status): hub_status.py CLI — brief + gh CI section with graceful degradation (#15)"
```

---

### Task 8: Log rotation module

**Files:**
- Create: `scripts/hublib/logrotate.py`
- Test: `scripts/tests/test_logrotate.py`

**Interfaces:**
- Produces: `logrotate.rotate_log(root, today=None) -> dict[int, int]` ({year: sections moved}; `{}` = nothing to do). Task 9 wires it into `hub_index.py`.

- [ ] **Step 1: Write the failing tests** — create `scripts/tests/test_logrotate.py`:

```python
import datetime
from pathlib import Path

from hublib.logrotate import rotate_log


def write(root: Path, rel: str, text: str):
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8", newline="\n")
    return p


TODAY = datetime.date(2026, 7, 5)

LOG = ("---\ntype: fact\ndescription: log\ntimestamp: 2026-07-05\n---\n"
       "## 2026-07-05\n- **Update** — new thing.\n"
       "## 2025-12-01\n- **Creation** — old thing.\n"
       "## 2025-06-01\n- **Update** — older thing.\n"
       "## 2024-01-15\n- **Creation** — ancient.\n")


def test_rotates_previous_years_grouped_order_preserved(tmp_path):
    write(tmp_path, "memory/log.md", LOG)
    moved = rotate_log(tmp_path, today=TODAY)
    assert moved == {2025: 2, 2024: 1}
    a2025 = (tmp_path / "memory/log-archive/2025.md").read_text(encoding="utf-8")
    assert "## 2025-12-01" in a2025 and "## 2025-06-01" in a2025
    assert a2025.index("2025-12-01") < a2025.index("2025-06-01")
    assert a2025.startswith("# memory/log archive — 2025")
    a2024 = (tmp_path / "memory/log-archive/2024.md").read_text(encoding="utf-8")
    assert "## 2024-01-15" in a2024 and "ancient" in a2024


def test_frontmatter_and_current_year_untouched(tmp_path):
    write(tmp_path, "memory/log.md", LOG)
    rotate_log(tmp_path, today=TODAY)
    log = (tmp_path / "memory/log.md").read_text(encoding="utf-8")
    assert log.startswith("---\ntype: fact\n")
    assert "## 2026-07-05\n- **Update** — new thing." in log
    assert "2025-12-01" not in log and "2024-01-15" not in log


def test_noop_when_only_current_year(tmp_path):
    write(tmp_path, "memory/log.md",
          "---\ntype: fact\ndescription: log\ntimestamp: 2026-07-05\n---\n"
          "## 2026-07-05\n- **Update** — new.\n")
    before = (tmp_path / "memory/log.md").read_text(encoding="utf-8")
    assert rotate_log(tmp_path, today=TODAY) == {}
    assert (tmp_path / "memory/log.md").read_text(encoding="utf-8") == before
    assert not (tmp_path / "memory/log-archive").exists()


def test_second_run_is_noop(tmp_path):
    write(tmp_path, "memory/log.md", LOG)
    rotate_log(tmp_path, today=TODAY)
    assert rotate_log(tmp_path, today=TODAY) == {}


def test_unparseable_heading_never_moves(tmp_path):
    write(tmp_path, "memory/log.md",
          "---\ntype: fact\ndescription: log\ntimestamp: 2026-07-05\n---\n"
          "## Notes\n- stays.\n## 2025-01-01\n- moves.\n")
    moved = rotate_log(tmp_path, today=TODAY)
    assert moved == {2025: 1}
    log = (tmp_path / "memory/log.md").read_text(encoding="utf-8")
    assert "## Notes" in log and "- stays." in log and "- moves." not in log


def test_missing_log_is_noop(tmp_path):
    assert rotate_log(tmp_path, today=TODAY) == {}
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python -m pytest scripts/tests/test_logrotate.py -v`
Expected: collection ERROR — `No module named 'hublib.logrotate'`.

- [ ] **Step 3: Implement** — create `scripts/hublib/logrotate.py`:

```python
"""Yearly rotation of memory/log.md into memory/log-archive/<year>.md
(convention: /conventions/memory.md). Only sections whose '## YYYY-MM-DD'
heading parses AND belongs to a previous year move — rotation never touches
what it cannot date."""
import datetime
import re
from pathlib import Path

HEADING_RE = re.compile(r"^## (\d{4})-\d{2}-\d{2}\s*$")


def rotate_log(root, today=None):
    """Returns {year: sections_moved}; {} means nothing to do."""
    root = Path(root)
    today = today or datetime.date.today()
    log = root / "memory" / "log.md"
    if not log.is_file():
        return {}
    text = log.read_text(encoding="utf-8")
    head, body = "", text
    if text.startswith("---\n"):
        end = text.find("\n---\n", 4)
        if end != -1:
            head, body = text[:end + 5], text[end + 5:]
    kept, moved = [], {}
    move_year = None  # set while inside a section that is being moved
    for line in body.splitlines(keepends=True):
        if line.startswith("## "):
            m = HEADING_RE.match(line.rstrip("\n"))
            year = int(m.group(1)) if m else None
            move_year = year if (year is not None and year < today.year) else None
        if move_year:
            moved.setdefault(move_year, []).append(line)
        else:
            kept.append(line)
    if not moved:
        return {}
    archive = root / "memory" / "log-archive"
    archive.mkdir(parents=True, exist_ok=True)
    counts = {}
    for year, lines in moved.items():
        target = archive / f"{year}.md"
        chunk = "".join(lines).rstrip("\n") + "\n"
        if target.is_file():
            content = target.read_text(encoding="utf-8").rstrip("\n") + "\n\n" + chunk
        else:
            content = f"# memory/log archive — {year}\n\n" + chunk
        target.write_text(content, encoding="utf-8", newline="\n")
        counts[year] = sum(1 for l in lines if l.startswith("## "))
    log.write_text((head + "".join(kept)).rstrip("\n") + "\n",
                   encoding="utf-8", newline="\n")
    return counts
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `python -m pytest scripts/tests/test_logrotate.py -v`
Expected: 6 PASS.

- [ ] **Step 5: Commit**

```bash
git add scripts/hublib/logrotate.py scripts/tests/test_logrotate.py
git commit -m "feat(memory): yearly log rotation helper — previous-year sections to log-archive/ (#10)"
```

---

### Task 9: `--rotate-log` flag on hub_index

**Files:**
- Modify: `scripts/hub_index.py`

**Interfaces:**
- Consumes: `logrotate.rotate_log` (Task 8), `indexer.write_all`.
- Produces: `python scripts/hub_index.py --rotate-log` — rotate, then full reindex. Incompatible with `--check` (exit 2).

- [ ] **Step 1: Replace `scripts/hub_index.py` with:**

```python
"""CLI: regenerate (default) or verify (--check) all generated indexes/views.
--rotate-log first moves previous-year memory/log.md sections to
memory/log-archive/<year>.md, then reindexes (rotation changes a file the
memory index is generated from)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from hublib.indexer import check, write_all
from hublib.logrotate import rotate_log


def main():
    root = Path(__file__).resolve().parents[1]
    if "--rotate-log" in sys.argv:
        if "--check" in sys.argv:
            print("ERROR --rotate-log is a write operation; incompatible with --check")
            return 2
        moved = rotate_log(root)
        for year in sorted(moved):
            print(f"ROTATED {year}: {moved[year]} section(s) -> "
                  f"memory/log-archive/{year}.md")
        if not moved:
            print("nothing to rotate")
    if "--check" in sys.argv:
        stale = check(root)
        for rel in stale:
            print(f"STALE {rel}")
        print(f"hub_index --check: {len(stale)} stale file(s)")
        return 1 if stale else 0
    for rel in write_all(root):
        print(f"WROTE {rel}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 2: Smoke-run all three modes on the real repo**

Run: `python scripts/hub_index.py --rotate-log` → expect `nothing to rotate` (log.md is all 2026) then `WROTE …` lines, exit 0.
Run: `python scripts/hub_index.py --rotate-log --check` → expect the ERROR line, exit 2 (`echo $?`).
Run: `python scripts/hub_index.py --check` → expect `0 stale file(s)`, exit 0.

- [ ] **Step 3: Full suite**

Run: `python -m pytest scripts/tests -v`
Expected: all PASS.

- [ ] **Step 4: Commit**

```bash
git add scripts/hub_index.py
git commit -m "feat(cli): hub_index --rotate-log — rotate memory log then reindex (#10)"
```

---

### Task 10: Link checker in publisher

**Files:**
- Modify: `scripts/hublib/publisher.py` (add `check_links` + two imports)
- Test: `scripts/tests/test_publisher.py`

**Interfaces:**
- Produces: `publisher.check_links(pages_dir) -> list[str]` (error lines `"<html rel path>: broken link <raw target>"`; empty list = clean). Task 11 wires it into the CLI.

- [ ] **Step 1: Write the failing tests** — append to `scripts/tests/test_publisher.py` (note: it already imports from `hublib.publisher`; extend that import line to include `check_links`):

```python
def make_pages(tmp_path):
    pages = tmp_path / "pages"
    write(pages, "index.html",
          '<a href="x/site/">site</a> <a href="x/one-pager.html">one</a>')
    write(pages, "x/site/index.html",
          '<link href="style.css"><img src="../one-pager.html">'
          '<a href="https://example.com/x">ext</a> <a href="#top">frag</a>'
          '<a href="mailto:a@b.c">mail</a>')
    write(pages, "x/site/style.css", "body{}")
    write(pages, "x/one-pager.html", "<html></html>")
    return pages


def test_check_links_clean_site(tmp_path):
    assert check_links(make_pages(tmp_path)) == []


def test_check_links_broken_href_and_src(tmp_path):
    pages = make_pages(tmp_path)
    write(pages, "x/broken.html", '<a href="gone.html">g</a><img src="img/gone.png">')
    errors = check_links(pages)
    assert "x/broken.html: broken link gone.html" in errors
    assert "x/broken.html: broken link img/gone.png" in errors


def test_check_links_root_absolute(tmp_path):
    pages = make_pages(tmp_path)
    write(pages, "x/site/abs.html",
          '<a href="/x/one-pager.html">ok</a><a href="/nope.html">bad</a>')
    assert check_links(pages) == ["x/site/abs.html: broken link /nope.html"]


def test_check_links_dir_without_index_is_error(tmp_path):
    pages = make_pages(tmp_path)
    write(pages, "x/noindex/readme.txt", "hi")
    write(pages, "dirlink.html", '<a href="x/noindex/">d</a>')
    assert check_links(pages) == ["dirlink.html: broken link x/noindex/"]


def test_check_links_percent_encoding_and_query(tmp_path):
    pages = make_pages(tmp_path)
    write(pages, "x/my file.html", "<html></html>")
    write(pages, "enc.html",
          '<a href="x/my%20file.html">e</a><a href="x/one-pager.html?v=2">q</a>')
    assert check_links(pages) == []
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python -m pytest scripts/tests/test_publisher.py -v`
Expected: ImportError on `check_links`.

- [ ] **Step 3: Implement** — in `scripts/hublib/publisher.py` add to the imports:

```python
import re
from urllib.parse import unquote
```

and add at the end of the file:

```python
LINK_ATTR_RE = re.compile(r"""(?:href|src)\s*=\s*["']([^"']+)["']""", re.IGNORECASE)
EXTERNAL_PREFIXES = ("http://", "https://", "//", "mailto:", "data:", "javascript:", "#")


def check_links(pages_dir):
    """Internal-link integrity of a pages clone: every href/src in every HTML
    file must resolve to a file, or to a directory holding index.html (a bare
    directory link 404s on GitHub Pages without one). External schemes and
    fragment-only links are out of scope."""
    pages = Path(pages_dir)
    errors = []
    for f in sorted(pages.rglob("*.html")):
        if ".git" in f.parts:
            continue
        rel = f.relative_to(pages).as_posix()
        text = f.read_text(encoding="utf-8", errors="replace")
        for m in LINK_ATTR_RE.finditer(text):
            raw = m.group(1).strip()
            if raw.startswith(EXTERNAL_PREFIXES):
                continue
            target = unquote(raw.split("#", 1)[0].split("?", 1)[0])
            if not target:
                continue
            resolved = (pages / target.lstrip("/")) if target.startswith("/") \
                else (f.parent / target)
            if resolved.is_file():
                continue
            if resolved.is_dir() and (resolved / "index.html").is_file():
                continue
            errors.append(f"{rel}: broken link {raw}")
    return errors
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `python -m pytest scripts/tests/test_publisher.py -v`
Expected: all PASS.

- [ ] **Step 5: Commit**

```bash
git add scripts/hublib/publisher.py scripts/tests/test_publisher.py
git commit -m "feat(publish): check_links — internal link integrity for the pages clone (#16)"
```

---

### Task 11: `--check-links` CLI flag + publish workflow step

**Files:**
- Modify: `scripts/hub_publish.py`
- Modify: `.github/workflows/publish.yml`

**Interfaces:**
- Consumes: `publisher.check_links` (Task 10).
- Produces: `hub_publish.py --check-links --pages-dir X` (exit 1 on broken links, 2 on missing --pages-dir); a CI step between apply and push.

- [ ] **Step 1: Modify `scripts/hub_publish.py`** — add the argument and mode. Replace the file with:

```python
"""CLI: validate the publish manifest (--check), verify pages-clone link
integrity (--check-links), or apply the manifest to a pages clone."""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from hublib.publisher import apply, check_links
from hublib.schema import validate_manifest


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pages-dir")
    ap.add_argument("--hub-sha", default="")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--check-links", action="store_true")
    args = ap.parse_args()
    root = Path(__file__).resolve().parents[1]
    errors = validate_manifest(root)
    for e in errors:
        print(f"ERROR {e}")
    if errors:
        return 1
    if args.check:
        print("hub_publish --check: manifest valid")
        return 0
    if args.check_links:
        if not args.pages_dir:
            print("ERROR --pages-dir required with --check-links")
            return 2
        broken = check_links(args.pages_dir)
        for b in broken:
            print(f"ERROR {b}")
        print(f"hub_publish --check-links: {len(broken)} broken link(s)")
        return 1 if broken else 0
    if not args.pages_dir:
        print("ERROR --pages-dir required unless --check")
        return 2
    copied, warnings = apply(root, args.pages_dir, args.hub_sha)
    for w in warnings:
        print(f"WARN  {w}")
    for d in copied:
        print(f"PUBLISHED {d}")
    print(f"hub_publish: {len(copied)} artifact(s), landing regenerated")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 2: Add the CI step** — in `.github/workflows/publish.yml`, between the apply step and the "Commit and push pages" step, insert:

```yaml
      - run: python scripts/hub_publish.py --check-links --pages-dir pages-repo
```

- [ ] **Step 3: Verify locally.** `python scripts/hub_publish.py --check` → `manifest valid`, exit 0. `python scripts/hub_publish.py --check-links` → the `--pages-dir required` ERROR, exit 2. If `../rhoai-agentic-hub-pages` exists (doctor section 5's optional clone), also run `python scripts/hub_publish.py --check-links --pages-dir ../rhoai-agentic-hub-pages` and record the result — 0 broken links expected; report any found, do NOT fix site content in this task.

- [ ] **Step 4: Full suite**

Run: `python -m pytest scripts/tests -v`
Expected: all PASS.

- [ ] **Step 5: Commit**

```bash
git add scripts/hub_publish.py .github/workflows/publish.yml
git commit -m "feat(publish): --check-links CLI + publish.yml gate between apply and push (#16)"
```

---

### Task 12: Doctor section 10 — pre-commit hook

**Files:**
- Modify: `scripts/doctor.sh` (new section between `echo "[9] …"` block's end and the final `echo "== result …"` line)

**Interfaces:**
- Consumes: `hub_lint.py`, `hub_index.py --check` (existing CLIs).
- Produces: doctor check/setup managing the pre-commit hook; marker `# hub-doctor pre-commit v1`.

- [ ] **Step 1: Add section 10** — in `scripts/doctor.sh`, insert before the `echo "== result: …"` line:

```bash
echo "[10] git pre-commit hook"
# Kills the #1 CI failure (edit -> forget reindex -> red) and runs the
# disclosure lint at the earliest possible moment. In a worktree .git is a
# FILE, so resolve the hooks dir via git, never hardcode .git/hooks.
HOOKS_DIR="$(cd "$ROOT" 2>/dev/null && git rev-parse --git-path hooks 2>/dev/null)"
case "$HOOKS_DIR" in
  "") : ;;
  /*|?:*) : ;;
  *) HOOKS_DIR="$ROOT/$HOOKS_DIR" ;;
esac
HOOK="${HOOKS_DIR:+$HOOKS_DIR/pre-commit}"
HOOK_MARKER="# hub-doctor pre-commit v1"
write_hook() {
  mkdir -p "$HOOKS_DIR" && cat > "$HOOK" <<'HOOKEOF' && chmod +x "$HOOK"
#!/bin/sh
# hub-doctor pre-commit v1 — installed by scripts/doctor.sh setup
python scripts/hub_lint.py && python scripts/hub_index.py --check
status=$?
if [ $status -ne 0 ]; then
  echo ""
  echo "pre-commit: hub gate failed."
  echo "  stale indexes     -> python scripts/hub_index.py"
  echo "  deliberate bypass -> git commit --no-verify"
fi
exit $status
HOOKEOF
}
if [ -z "$HOOKS_DIR" ]; then
  warn "not a git repo? could not resolve the hooks dir — skipping hook check"
elif [ -f "$HOOK" ] && grep -qF "$HOOK_MARKER" "$HOOK"; then
  ok "pre-commit hook installed (current version)"
elif [ -f "$HOOK" ] && grep -q "hub-doctor pre-commit" "$HOOK"; then
  if [ "$MODE" = "setup" ]; then
    cp "$HOOK" "$HOOK.bak" && write_hook && ok "pre-commit hook updated (old version -> pre-commit.bak)"
  else
    warn "pre-commit hook is an outdated hub-doctor version — run: bash scripts/doctor.sh setup"
  fi
elif [ -f "$HOOK" ]; then
  if [ "$MODE" = "setup" ]; then
    cp "$HOOK" "$HOOK.bak" && write_hook && ok "pre-commit hook installed (foreign hook -> pre-commit.bak)"
  else
    warn "a non-hub pre-commit hook exists — setup will back it up to pre-commit.bak and replace it"
  fi
else
  if [ "$MODE" = "setup" ]; then
    write_hook && ok "pre-commit hook installed"
  else
    fail "pre-commit hook not installed — run: bash scripts/doctor.sh setup"
  fi
fi
```

- [ ] **Step 2: Verify in a scratch clone (NEVER run `doctor.sh setup` here — see Global Constraints).** Clone the worktree into the scratchpad and exercise every check-mode path plus the hook content itself:

```bash
SCRATCH="<your session scratchpad dir>/hooktest"   # mktemp -d works as a fallback
git clone . "$SCRATCH"
cp scripts/doctor.sh "$SCRATCH/scripts/doctor.sh"   # Step 1's edit is not committed yet
cd "$SCRATCH"
bash scripts/doctor.sh check 2>&1 | grep -A1 '\[10\]'   # expect: FAIL not installed
# hand-install EXACTLY the hook body write_hook writes (this tests the hook content):
mkdir -p .git/hooks && sed -n '/HOOKEOF/,/^HOOKEOF$/p' scripts/doctor.sh | sed '1d;$d' > .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
bash scripts/doctor.sh check 2>&1 | grep -A1 '\[10\]'   # expect: OK current version
# blocked commit: tamper a generated file so hub_index --check fails
echo "tampered" >> views/decisions.md && git add views/decisions.md && git commit -m "should be blocked"
# expect: commit FAILS with "pre-commit: hub gate failed." + remediation lines
python scripts/hub_index.py && git add -A && git commit -m "clean commit passes"
# expect: commit SUCCEEDS
# degraded-marker paths:
sed -i 's/pre-commit v1/pre-commit v0/' .git/hooks/pre-commit
bash scripts/doctor.sh check 2>&1 | grep -A1 '\[10\]'   # expect: WARN outdated
echo '#!/bin/sh' > .git/hooks/pre-commit
bash scripts/doctor.sh check 2>&1 | grep -A1 '\[10\]'   # expect: WARN non-hub hook
cd - && rm -rf "$SCRATCH"
```

Record each observed state in the task report. (The `sed -n` extraction pulls the heredoc body from doctor.sh so the hand-installed hook is byte-identical to what setup writes; if the extraction proves brittle, copy the hook body from Step 1 verbatim instead.)

- [ ] **Step 3: Syntax-check doctor and run check mode in the worktree**

Run: `bash -n scripts/doctor.sh && bash scripts/doctor.sh check; echo "exit=$?"`
Expected: no syntax errors; section 10 reports FAIL (hook not installed in the shared hooks dir yet, or OK if the main clone already has it) — either is fine; sections 1–9 behave as before.

- [ ] **Step 4: Commit**

```bash
git add scripts/doctor.sh
git commit -m "feat(doctor): section 10 installs/verifies the pre-commit gate hook (#7)"
```

---

### Task 13: Skill and doc text edits

**Files:**
- Modify: `.claude/skills/hub.migrate/SKILL.md`
- Modify: `docs/memory.md`
- Modify: `.claude/skills/presentation-create/SKILL.md`
- Modify: `.claude/skills/blog-create/SKILL.md`
- Modify: `.claude/skills/blog-mockup/SKILL.md`

**Interfaces:** text-only; no code consumers.

- [ ] **Step 1: hub.migrate — narrative enumeration.** In `.claude/skills/hub.migrate/SKILL.md` step 2, change `narrative/{knowledge|strategy}/` to `narrative/{knowledge|research|strategy}/`.

- [ ] **Step 2: hub.migrate — link-repoint carve-out.** In the same step 2, after the sentence ending `…and a body note saying what to re-verify.`, append:

```
When re-homing existing hub entries, repoint inbound links across the
   repo — except historical records (docs/specs/, docs/plans/,
   docs/history.md, memory/log.md), which keep the paths that were true
   when written; dangling-link warnings there are acceptable.
```

- [ ] **Step 3: docs/memory.md boundary line.** Change:

```
("how the gateway does authz"), the gate files it as a knowledge entry in
the right feature partition instead.
```

to:

```
("how the gateway does authz"), the gate files it as a knowledge entry in
the right home (feature partition or `narrative/`) instead.
```

- [ ] **Step 4: presentation-create.** In `.claude/skills/presentation-create/SKILL.md`, after the paragraph beginning `Write the HTML file to \`features/<feature>/enablement/<artifact-slug>/index.html\`` (≈line 238), add a new paragraph:

```
If this run created a new `enablement/<artifact-slug>/` directory, also
scaffold an `artifact.md` descriptor alongside the HTML — frontmatter
`type: artifact`, `title`, one-line `description`, `timestamp` (today), and
`features:` listing any other feature partitions the artifact spans.
`views/artifacts.md` flags descriptor-less directories, and `hub.publish`
reads the descriptor when the artifact ships.
```

- [ ] **Step 5: blog-create.** After the `mkdir -p features/<feature>/enablement/blog-<topic-short>/drafts/reviews` step (≈line 89), add:

```
If this created a new `enablement/blog-<topic-short>/` directory, scaffold an
`artifact.md` descriptor in it — frontmatter `type: artifact`, `title` (the
working title), one-line `description`, `timestamp` (today), and `features:`
for any cross-feature spread. `views/artifacts.md` flags descriptor-less
directories.
```

- [ ] **Step 6: blog-mockup.** In the bullet ending `…creating the directory if it doesn't exist yet.` (≈line 39), append to that bullet:

```
 When creating the directory, also scaffold an `artifact.md` descriptor
(`type: artifact`, `title`, one-line `description`, `timestamp`, `features:`
spread) — `views/artifacts.md` flags descriptor-less directories.
```

- [ ] **Step 7: Lint (docs link check rides on it)**

Run: `python scripts/hub_lint.py`
Expected: exit 0.

- [ ] **Step 8: Commit**

```bash
git add .claude/skills/hub.migrate/SKILL.md .claude/skills/presentation-create/SKILL.md .claude/skills/blog-create/SKILL.md .claude/skills/blog-mockup/SKILL.md docs/memory.md
git commit -m "docs(skills): artifact.md scaffolding, migrate repoint carve-out, memory boundary line (#10)"
```

---

### Task 14: docs/tooling.md

**Files:**
- Modify: `docs/tooling.md` (sections: `## The commands`, `## The library — scripts/hublib/`, `## The doctor`; new `## The disclosure lint` section after The library)

**Interfaces:** documentation of Tasks 3–12; text-only.

- [ ] **Step 1: Read `docs/tooling.md`** and make these additions, matching its existing prose/table style exactly:
  - **The commands:** add `python scripts/hub_status.py` (morning brief — stale, open questions, unanswered qa, JTBD without evidence, descriptor-less enablement dirs, rotation reminder, recent log, gh CI state; informational, exit 0); add `python scripts/hub_index.py --rotate-log` (move previous-year memory/log.md sections to memory/log-archive/<year>.md, then reindex; incompatible with --check); add `python scripts/hub_publish.py --check-links --pages-dir <clone>` (internal link integrity of the pages clone; exit 1 on broken links; runs in publish.yml between apply and push).
  - **The library:** add one line each for `disclosure.py` (local-first disclosure lint — see the new section), `status.py` (build_brief), `logrotate.py` (rotate_log).
  - **New section `## The disclosure lint`** after The library:

```markdown
## The disclosure lint

`hub_lint.py` runs `hublib/disclosure.py` alongside the schema lint:

- **Restricted patterns (errors, local-first).** An OPTIONAL, gitignored
  `restricted/lint-patterns.txt` — one case-insensitive regex per line, `#`
  comments allowed — is scanned over `features/*/enablement/**/*.html`,
  `narrative/enablement/**/*.html`, and all public knowledge entries. A match
  is an ERROR naming the file:line and the pattern's line number (never its
  text). CI never sees the pattern file, so this net only exists on machines
  that carry `restricted/` — the pre-commit hook (doctor section 10) is its
  enforcement point. An invalid regex is skipped with a warning; the rest of
  the net still applies.
- **Generic heuristics (warnings, CI-visible).** `schema.RESTRICTED_HINTS`
  (SKU/pricing/NDA phrasing, dollar figures, signed-agreement phrasing) warns
  on knowledge-entry bodies (as before) and now also on enablement HTML.
```

  - **The doctor:** add a section-10 line: `[10] git pre-commit hook — check verifies install state (marker \`# hub-doctor pre-commit v1\`); setup installs a hook running hub_lint + hub_index --check, backing up any foreign hook to pre-commit.bak. Bypass deliberately with git commit --no-verify.`

- [ ] **Step 2: Lint**

Run: `python scripts/hub_lint.py`
Expected: exit 0.

- [ ] **Step 3: Commit**

```bash
git add docs/tooling.md
git commit -m "docs(tooling): document hub_status, --rotate-log, --check-links, disclosure lint, doctor section 10"
```

---

### Task 15: Final gates + backlog bookkeeping (keep as the LAST, separate commit)

**Files:**
- Modify: `docs/enhancements.md`

**Interfaces:** consumes everything; produces the Done record. This commit is deliberately last and self-contained so the concurrent hub.intake workstream can trivially redo it after a rebase (spec §8).

- [ ] **Step 1: Run every gate**

```bash
python -m pytest scripts/tests -v && python scripts/hub_lint.py && python scripts/hub_index.py --check && python scripts/hub_publish.py --check
```

Expected: all green / exit 0.

- [ ] **Step 2: Update `docs/enhancements.md`:**
  - Delete priority-table rows 5, 7, 10, 15, 16.
  - Delete the shipped items' detail write-ups: `**5 · Disclosure lint…**` and `**7 · Pre-commit gate hook.**` (Agent-usage section), `**15 · hub_status.py morning brief.**` (Human-usage section), `**16 · Published-site link checker.**` (Repo functionality section), and the whole `## Recorded small fixes (batch these in one sitting — item 10)` section. All other detail sections stay untouched.
  - Under `## Done`, replace the placeholder line with:

```markdown
- 2026-07-09 — **#5 disclosure lint** — `restricted/lint-patterns.txt`
  (gitignored, errors) over enablement HTML + knowledge entries;
  `RESTRICTED_HINTS` hardened (dollar figures, signed-agreement) and extended
  to enablement HTML (warnings). Shipped in the enhancement batch
  (/docs/specs/2026-07-09-enhancement-batch-design.md).
- 2026-07-09 — **#7 pre-commit gate hook** — doctor section 10 installs
  hub_lint + hub_index --check as `.git/hooks/pre-commit`.
- 2026-07-09 — **#10 recorded small-fix batch** — pillar-path warning, faq
  "by home" heading, indexer test gaps, hub.migrate enumeration + historical
  link-repoint carve-out, docs/memory.md boundary line, artifact.md
  scaffolding in presentation/blog skills, log rotation helper
  (`hub_index.py --rotate-log`).
- 2026-07-09 — **#15 `hub_status.py` morning brief** — stale / open questions
  / unanswered qa / JTBD without evidence / descriptor-less enablement dirs /
  rotation reminder / recent log + gh CI state.
- 2026-07-09 — **#16 published-site link checker** —
  `hub_publish.py --check-links` + publish.yml step between apply and push.
```

  - Update the `Last groomed:` line to `2026-07-09 (post-batch)`.

- [ ] **Step 3: Lint + reindex check once more** (enhancements.md is not generated, but the link added above must resolve)

Run: `python scripts/hub_lint.py && python scripts/hub_index.py --check`
Expected: exit 0 / `0 stale file(s)`.

- [ ] **Step 4: Commit**

```bash
git add docs/enhancements.md
git commit -m "docs(enhancements): move #5 #7 #10 #15 #16 to Done — shipped in the enhancement batch"
```

---

## Post-plan notes (main session, not subagent tasks)

- The `memory/log.md` entry for the batch goes through the **hub.capture gate** with the owner after merge — never a direct write (spec §7).
- Installing the hook on this machine's main clone (`doctor.sh setup`) needs the owner's explicit go-ahead (doctor writes MCP credentials in section 8) — ask at wrap-up.
- Merge coordination with the concurrent hub.intake workstream: expected conflicts only in `docs/enhancements.md` (redo Task 15's edit) and generated files (rerun `python scripts/hub_index.py`). See spec §8.
