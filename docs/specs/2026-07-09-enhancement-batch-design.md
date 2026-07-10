# Enhancement batch design — disclosure lint, pre-commit hook, small fixes, status brief, link checker

- **Date:** 2026-07-09
- **Status:** approved (owner rulings inline)
- **Backlog items:** [/docs/enhancements.md](/docs/enhancements.md) #5, #7, #10, #15, #16
- **Structure ruling:** follow the repo idiom strictly — new `hublib/` modules with
  thin CLI wrappers and per-module tests, matching the existing
  `schema.py`/`hub_lint.py`, `indexer.py`/`hub_index.py`,
  `publisher.py`/`hub_publish.py` pattern.

## Overview

One-sitting batch of five backlog items, all pure local Python/bash tooling
against the `scripts/` surface plus a handful of doc/skill text edits. No new
dependencies (stays pyyaml + pytest), no MCP servers, no schema changes to
content entries, nothing that alters the publish disclosure gates.

Owner rulings recorded during brainstorm:

1. Log rotation (#10 sub-item): build the **full rotation helper**, not just a
   reminder.
2. `views/faq.md` heading fix (#10 sub-item): apply **now**, without waiting
   for the first narrative-homed qa entry.
3. Disclosure lint (#5): a match on a `restricted/lint-patterns.txt` pattern in
   a public file is a **blocking error** (the pre-commit hook fails the
   commit). Generic heuristics stay warnings.

## 1 · Disclosure lint (#5) — `scripts/hublib/disclosure.py`

The scrub episode showed the leaks that matter live in enablement HTML, and
literal customer/program name lists cannot be committed to a public repo. The
first net becomes mechanical and local-first.

### Pattern file

- Path: `restricted/lint-patterns.txt` — inside the gitignored `restricted/`
  tree, so it never reaches git or CI. Optional: absent file means the
  restricted-pattern scan is silently skipped (CI, fresh clones).
- Format: one Python regex per line. Blank lines and lines starting `#` are
  skipped. Each pattern is compiled with `re.IGNORECASE`.
- An invalid regex produces a lint **warning** naming the line number
  (`restricted/lint-patterns.txt:3: invalid regex (skipped): <re.error>`) and
  the remaining patterns still apply — a typo in the net must never disable
  the net silently.

### Module API

```python
# scripts/hublib/disclosure.py
load_patterns(root)  # -> (list[(lineno, compiled_pattern)], warnings)
scan_repo(root)      # -> (errors, warnings) — same contract as schema.lint_repo
```

`scan_repo` performs two passes over the **public tree only** (`restricted/`
is never scanned — that is where such content is supposed to live):

1. **Restricted-pattern pass** (errors; only when the pattern file exists).
   Scan surface:
   - `features/*/enablement/**/*.html` and `narrative/enablement/**/*.html`
   - knowledge entries: `features/*/knowledge/*.md` and
     `narrative/knowledge/*.md` (raw file text, so frontmatter is covered too)

   Error format references the pattern by **line number, not text** — lint
   output can get pasted into public places (CI logs, issues), the pattern
   text must not travel:
   `ERROR features/x/enablement/deck/index.html:212: matches restricted pattern (lint-patterns.txt:3)`

2. **Generic-heuristic pass** (warnings; always runs, CI-visible). Applies
   `schema.RESTRICTED_HINTS` to the same enablement HTML surface — today the
   heuristic only sees knowledge-entry bodies via `lint_entry`. Same
   `file:line` format, existing wording ("restricted-content heuristic
   matched — confirm this belongs in a public repo").

### Public heuristic hardening (`schema.py`)

`RESTRICTED_HINTS` gains the two generic patterns learned in the scrub
episode, as alternates in the existing regex:

- dollar figures: `\$\d`
- signed-agreement phrasing: `signed[^.\n]{0,40}agreement`
  (covers "signed a strategic collaboration agreement" etc.)

These stay **warnings** everywhere (false-positive prone: `$1` in embedded
JS, invoice examples, etc.). Known cost accepted at design time.

### Wiring

`schema.py` must not import `disclosure` (that would be circular —
`disclosure` imports `RESTRICTED_HINTS` from `schema`). Instead
`scripts/hub_lint.py` calls both and merges:

```python
errors, warnings = lint_repo(root)
d_err, d_warn = disclosure.scan_repo(root)
errors += d_err; warnings += d_warn
```

Everything downstream (doctor section 6, CI `validate.yml`, the new
pre-commit hook) already runs `hub_lint.py`, so they inherit the net with no
further changes.

## 2 · Pre-commit gate hook (#7) — `doctor.sh` section 10

Kills the #1 CI failure (edit → forget reindex → red) and moves the
disclosure net to the earliest possible moment.

### Hook body (exact content, written by setup)

```sh
#!/bin/sh
# hub-doctor pre-commit v1 — installed by scripts/doctor.sh setup
python scripts/hub_lint.py && python scripts/hub_index.py --check
status=$?
if [ $status -ne 0 ]; then
  echo ""
  echo "pre-commit: hub gate failed."
  echo "  stale indexes  -> python scripts/hub_index.py"
  echo "  deliberate bypass -> git commit --no-verify"
fi
exit $status
```

- No pytest in the hook — too slow for every commit; CI keeps the full suite.
- Git runs pre-commit hooks from the top of the working tree, so the relative
  script paths are safe.
- The `# hub-doctor pre-commit v1` marker line is the idempotency/versioning
  key: a future hook change bumps `v1` and doctor setup rewrites on mismatch.

### Doctor semantics (new section `[10] git pre-commit hook`)

| state of `.git/hooks/pre-commit` | check mode | setup mode |
|---|---|---|
| present, marker current version | OK | OK (no-op) |
| present, marker older version | WARN (outdated) | rewrite (backup first) |
| present, no marker (foreign hook) | WARN — check never touches it | backup to `pre-commit.bak`, then write ours |
| absent | FAIL with remediation (`run: bash scripts/doctor.sh setup`) | write hook + `chmod +x`, report OK |

Backups follow the section 7/8 discipline: `pre-commit` → `pre-commit.bak`
before any rewrite doctor performs.

## 3 · Published-site link checker (#16) — `publisher.check_links`

Automates the click-through verification the HTML migration did manually, and
catches cross-artifact rewrite regressions when the hub sites get refreshed
(backlog #4).

### Function

```python
# scripts/hublib/publisher.py
check_links(pages_dir)  # -> list[str] of error lines; empty = clean
```

- Walk every `*.html` under `pages_dir` (skip `.git/`).
- Extract link targets with a regex — no new dependency:
  `(?:href|src)\s*=\s*["']([^"']+)["']` (case-insensitive).
- **Skip** targets starting `http://`, `https://`, `//`, `mailto:`, `data:`,
  `javascript:`, or `#` (fragment-only). External links are out of scope —
  this checker owns the site's internal integrity only.
- Normalize: strip fragment and query, `urllib.parse.unquote` percent-escapes
  (`%20` → space). Empty after stripping → skip.
- Resolve: leading `/` → relative to `pages_dir` root; otherwise relative to
  the HTML file's own directory.
- **Exists** means: a file at the resolved path, or a directory containing
  `index.html` (a bare directory link 404s on GitHub Pages without one — that
  is an error).
- Error line format: `<html file rel to pages_dir>: broken link <target>`.

### CLI and CI

- `hub_publish.py --check-links --pages-dir X` — runs manifest validation
  (as today) then `check_links`; prints `ERROR` lines; exit 1 on any. It only
  checks — it never applies the manifest.
- `.github/workflows/publish.yml` gains one step **between** apply and the
  commit/push step: a publish that would go live with broken internal links
  fails before it ships.

```yaml
- run: python scripts/hub_publish.py --check-links --pages-dir pages-repo
```

## 4 · Morning brief (#15) — `scripts/hublib/status.py` + `scripts/hub_status.py`

The daily-loop "where was I": one command, one page.

### Module

```python
# scripts/hublib/status.py
build_brief(root, today=None)  # -> str (plain markdown)
```

Sections, in order — a section with nothing to say is omitted entirely:

1. `## Stale (N)` — the same rows as `views/stale-facts.md`. The stale-row
   computation currently lives inline in `indexer.build_all`; it is
   **extracted** into a shared `indexer.stale_rows(root, today)` helper used
   by both `build_all` and `status`, so the brief and the view cannot drift.
2. `## Open questions (N)` — counts grouped by home
   (`mcp-gateway: 3 · narrative: 1`), derived from entries with
   `type: question, status: open`.
3. `## Unanswered qa (N)` — title + home per `type: qa, status: open` entry.
4. `## JTBD lacking evidence (N)` — `type: jtbd` entries whose `evidence`
   list is missing or empty.
5. `## Enablement dirs missing artifact.md (N)` — same detection as
   `views/artifacts.md` ("no descriptor yet" rows).
6. `## Log rotation due` — present only when `memory/log.md` contains
   `## YYYY-MM-DD` sections from a previous year; names the fix
   (`python scripts/hub_index.py --rotate-log`).
7. `## Recent log` — last 5 log entries (same parsing as the memory index).

### CLI

`scripts/hub_status.py` prints the brief and always exits 0 (informational —
it is not a gate). It appends one extra section the module deliberately does
not own:

- `## CI (last push)` — via `gh run list --branch main --limit 1`
  (subprocess, 10s timeout). Any failure — `gh` missing, not authenticated,
  timeout, non-zero exit — silently skips the section. Keeping this in the
  CLI keeps `build_brief` fully testable without `gh`.

## 5 · Log rotation (#10 sub-item, full helper) — `scripts/hublib/logrotate.py`

```python
rotate_log(root, today=None)  # -> {year: sections_moved}; {} = nothing to do
```

- Parse `memory/log.md`: preserve frontmatter untouched; split the body on
  `## ` headings; a section belongs to the year in its `## YYYY-MM-DD`
  heading.
- Sections dated in a **previous year** move to
  `memory/log-archive/<year>.md`, grouped by year, preserving their log.md
  order (newest-first). Archive files are created on first use with a plain
  `# memory/log archive — <year>` heading — no frontmatter; the linter
  already skips `log-archive/`.
- Sections with an unparseable heading date are **never moved** — rotation
  only touches what it can date.
- Idempotent: a log.md with only current-year sections is a no-op.

CLI: `hub_index.py --rotate-log` — calls `rotate_log`, prints
`ROTATED <year>: N section(s) -> memory/log-archive/<year>.md` (or
`nothing to rotate`), then **falls through to the normal full reindex** —
rotation changes a file the memory index is generated from. `--rotate-log`
is a write operation and therefore incompatible with `--check`; passing both
is an error (exit 2).

## 6 · Recorded small fixes (#10, remaining sub-items)

All carried verbatim from [/docs/enhancements.md](/docs/enhancements.md)
§Recorded small fixes:

1. **`schema.py` — pillar leading-slash warning.** In the story branch of
   `lint_entry`: a `pillar:` value not starting with `/` gets a warning
   ("pillar should be a leading-slash root path — this story will not attach
   to its pillar in the narrative map"). The existing dangling-target check
   stays.
2. **`indexer.py` — faq heading.** `views/faq.md` section heading
   "All, by feature" → "All, by home" (owner ruling: now). `_home()` already
   returns `narrative` for narrative-homed entries; only the label was wrong.
3. **Test gaps** (test_indexer.py): multi-item Connections list is sorted;
   a knowledge entry and an artifact descriptor for the same feature id
   combine into one Connections list; `narrative/` directory existing but
   empty (no `knowledge/`) generates indexes without error.
4. **`hub.migrate` SKILL.md:** narrative routing enumeration gains
   `research` — `narrative/{knowledge|research|strategy}/` — matching
   working-here; and the link-repoint instruction is added with the
   historical-docs carve-out codified: *when re-homing existing hub content,
   repoint inbound links across the repo — except historical records
   (`docs/specs/`, `docs/plans/`, `docs/history.md`, `memory/log.md`), which
   keep the paths that were true when written; the linter reports those as
   dangling-link warnings, which is acceptable.*
5. **`docs/memory.md`:** the memory-vs-knowledge boundary line becomes "…the
   gate files it as a knowledge entry in the right home (feature partition or
   `narrative/`) instead."
6. **`presentation-create`, `blog-create`, `blog-mockup` SKILL.mds:** each
   gains the instruction to scaffold an `artifact.md` descriptor
   (`type: artifact`, `title`, `description`, `timestamp`, `features:`
   spread) when creating a new `enablement/<slug>/` directory — today only
   `hub.migrate` instructs this, and `views/artifacts.md` flags the gap as
   "no artifact.md descriptor yet".

## 7 · Docs, bookkeeping, out of scope

- `docs/tooling.md`: document `hub_status.py`, `hub_index.py --rotate-log`,
  `hub_publish.py --check-links`, doctor section 10, and the disclosure lint
  (pattern file location + format + severity model).
- `docs/enhancements.md`: items 5, 7, 10, 15, 16 move to **Done** with date +
  commit; the priority table rows are removed.
- `memory/log.md` line goes through the normal gate (hub.capture) at the end
  of the batch — never a direct write.
- **Out of scope, recorded deliberately:** #8 landing-page upgrade (its own
  item); extending the restricted-pattern scan to `memory/**/*.md` (noted as
  a possible follow-up in the backlog if wanted); external-URL checking in
  `check_links`; pytest in the pre-commit hook.

## 8 · Concurrent work — hub.intake/hub.research (running in parallel)

The hub.intake + hub.research implementation
([/docs/superpowers/specs/2026-07-09-hub-intake-research-design.md](/docs/superpowers/specs/2026-07-09-hub-intake-research-design.md))
is being built concurrently in a separate environment. Assessed compatible;
three merge-time contact points, none during implementation:

1. **`scripts/hublib/schema.py` + `test_schema.py`** — the only file both
   workstreams modify (they: warnings-only `research/*.md` frontmatter check;
   us: `RESTRICTED_HINTS` extension + pillar warning). Different regions;
   expected to auto-merge. No semantic overlap in scan surfaces.
2. **`docs/enhancements.md`** — both move backlog items to Done. Mitigation:
   the bookkeeping edit is this batch's **final, separate commit**, so the
   second workstream to land can redo it in seconds after rebasing.
3. **Generated indexes/views + `memory/log.md`** — resolved mechanically:
   rerun `python scripts/hub_index.py` after merge; log.md is an append-merge.

Synergy note: the intake spec's discipline line ("dollar figures and
agreement language … trip the lint heuristics by design") is delivered BY
this batch (§1's `RESTRICTED_HINTS` hardening) — it does not exist before
this lands. This batch is implemented on its own branch; whichever workstream
finishes second rebases.

## 9 · Testing and verification

New test files follow the existing per-module pattern (direct imports via
`conftest.py`, `tmp_path` fixtures):

- **`test_disclosure.py`** — no pattern file → no errors; a matching pattern
  in enablement HTML → error with `file:line` and `lint-patterns.txt:<n>`
  reference; case-insensitive matching; invalid regex → warning, remaining
  patterns still applied; comments/blank lines skipped; `restricted/` tree
  never scanned; knowledge `.md` scanned including frontmatter; generic
  hints over enablement HTML → warnings.
- **`test_schema.py` additions** — pillar-missing-leading-slash warning;
  `\$\d` and `signed…agreement` fire `RESTRICTED_HINTS` as warnings.
- **`test_publisher.py` additions** — `check_links`: clean site passes;
  broken `href` and broken `src` caught; external/mailto/fragment-only
  skipped; root-absolute and relative resolution; directory link without
  `index.html` is an error; percent-encoded targets resolved.
- **`test_status.py`** — sections appear with content and are omitted when
  empty; open-question counts grouped by home; rotation reminder appears only
  with previous-year log entries; brief never raises on a minimal repo.
- **`test_logrotate.py`** — previous-year sections move grouped by year,
  order preserved; current-year sections and frontmatter untouched;
  unparseable headings left in place; second run is a no-op; archive file
  created on first use.
- **`test_indexer.py` additions** — the three recorded gaps (§6.3) plus the
  "All, by home" heading.

Gates that must stay green: `python -m pytest scripts/tests -v` ·
`python scripts/hub_lint.py` · `python scripts/hub_index.py --check` ·
`python scripts/hub_publish.py --check`.

Live verification (not automatable in CI): doctor section 10 installs the
hook; a commit with deliberately stale indexes is blocked with the
remediation message; a clean commit passes; `hub_status.py` runs on this
repo and prints a sane brief.
