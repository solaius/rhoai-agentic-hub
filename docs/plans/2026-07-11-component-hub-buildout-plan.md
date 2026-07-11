# Component Hub Build-out Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the Catalog, MCPLO, and Registry knowledge hubs, devolve the
Management hub to a ~12-14 page umbrella, and ship the `audience: internal`
publish target on this repo's gh-pages (spec:
`docs/specs/2026-07-11-component-hub-buildout-design.md`).

**Architecture:** One manifest, two publish targets (public pages repo +
this repo's gh-pages branch, same dest layout). Three new self-contained
HTML hubs under their feature partitions, seeded from both parent hubs in
one pass per component, each launch immediately followed by parent
thinning. `hub.refresh-site` gains JTBD and Strats-Jira-Tracker section
contracts.

**Tech Stack:** Python 3.12 (hublib, pytest), GitHub Actions, static
HTML/CSS/JS (nav.js pattern), `gh` CLI, `hub_jira.py` against
issues.redhat.com.

## Global Constraints

- NO EM DASHES in any new content, code comment, commit message, or HTML
  copy. Use commas, colons, parentheses, or spaced hyphens.
- Anonymization: never introduce customer or partner engagement names,
  pricing, or deal detail into hub HTML ("large enterprise OEM customer"
  style). Everything written is world-readable.
- `python` (not `python3`), Git Bash syntax, repo root
  `C:\Users\peter\code\rh\rhoai-agentic-hub`.
- Before every commit: `git status --short` must show only your files;
  `git diff --cached --stat` reviewed; `python scripts/hub_lint.py` reports
  0 errors (warnings are pre-triaged, do not chase them; NEVER --no-verify).
- After content/entry changes run `python scripts/hub_index.py` and commit
  regenerated indexes with the change.
- Commit messages end with:
  `Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>`
- Every new/edited hub HTML page: footer
  `<footer class="page-footer" data-verified="<TODAY>">` with
  `<span class="staleness-indicator"></span>`, where TODAY is the execution
  date (ISO). Product naming: full name on first use per page.
- Manifest/audience edits in this plan are owner-approved by the spec; do
  not re-ask. Anything beyond them needs a fresh owner gate.
- Publish verification loop (used by several tasks):
  `git push` then
  `gh run list --repo solaius/rhoai-agentic-hub --workflow publish.yml --limit 1 --json databaseId -q '.[0].databaseId'`
  then `gh run watch <id> --repo solaius/rhoai-agentic-hub --exit-status`.
- Internal site root (after Task 3): `https://solaius.github.io/rhoai-agentic-hub/`
  Public site root: `https://solaius.github.io/rhoai-agentic-hub-pages/`

## File Structure (what this plan creates or reshapes)

- `scripts/hublib/publisher.py`: audience-aware `build_plan`/`apply`/
  `generate_landing` + new `check_audience_links`
- `scripts/hub_publish.py`: `--audience` flag
- `publish/landing-template-internal.html`: internal landing template
- `scripts/hublib/refresh.py`: `sections:` config validation
- `scripts/hublib/schema.py`: wires `check_audience_links` into `lint_repo`
- `.github/workflows/publish.yml`: internal target steps
- `.claude/skills/hub.refresh-site/SKILL.md`, `.claude/skills/hub.publish/SKILL.md`: contract updates
- `features/mcp-catalog/enablement/catalog-hub/` (14 pages + nav.js + styles.css + artifact.md)
- `features/mcp-lifecycle-operator/enablement/mcplo-hub/` (16 pages + assets)
- `features/mcp-registry/enablement/registry-hub/` (12 pages + assets)
- `features/{mcp-catalog,mcp-lifecycle-operator,mcp-registry}/work/refresh-*.yaml`
- Thinned pages in `features/mcp-ecosystem/enablement/management-hub/` and
  `features/mcp-gateway/enablement/rhcl-hub/`
- `publish/manifest.yaml`, `features/features.yaml`, `conventions/publishing.md`,
  `docs/enhancements.md` updates

Dependencies: Tasks 1-3 (increment 0) strictly ordered. Task 4 before Task
9. Tasks 5-10 = Catalog, 11-14 = MCPLO, 15-18 = Registry (each hub's tasks
ordered within the hub; hubs ordered Catalog, MCPLO, Registry). Tasks 19-20
= umbrella. Task 21 = network pass. Task 22 = closeout.

---

### Task 1: Audience-aware publisher (TDD)

**Files:**
- Modify: `scripts/hublib/publisher.py`
- Create: `publish/landing-template-internal.html`
- Modify: `scripts/hub_publish.py`
- Test: `scripts/tests/test_publisher.py`

**Interfaces:**
- Produces: `build_plan(root, audience="public")`,
  `apply(root, pages_dir, hub_sha="", audience="public")`,
  `generate_landing(root, plan, hub_sha="", template_name="landing-template.html")`,
  CLI `python scripts/hub_publish.py --audience {public,internal}`.
  Later tasks and publish.yml rely on these exact names.

- [ ] **Step 1: Write failing tests** (append to `scripts/tests/test_publisher.py`; the existing `make_repo` fixture already has an internal manifest entry):

```python
def test_build_plan_internal_audience(tmp_path):
    plan = build_plan(make_repo(tmp_path), audience="internal")
    assert {p["dest"] for p in plan} == {"x/internal"}


def test_apply_internal_target(tmp_path):
    root = make_repo(tmp_path)
    internal = tmp_path / "internal-pages"
    internal.mkdir()
    copied, warnings = apply(root, internal, hub_sha="abc", audience="internal")
    assert copied == ["x/internal"]
    assert (internal / "x/internal/index.html").is_file()
    assert not (internal / "x/site").exists()
    landing = (internal / "index.html").read_text(encoding="utf-8")
    assert "Internal" in landing
    snap = json.loads((internal / SNAPSHOT).read_text())
    assert set(snap) == {"x/internal"}
```

Also update `make_repo` to copy the internal template next to the public one:

```python
    shutil.copy(REPO_ROOT / "publish" / "landing-template-internal.html",
                root / "publish" / "landing-template-internal.html")
```

- [ ] **Step 2: Run and verify failure**

Run: `cd /c/Users/peter/code/rh/rhoai-agentic-hub && python -m pytest scripts/tests/test_publisher.py -v`
Expected: the two new tests FAIL (missing template file / unexpected
keyword `audience`); all pre-existing tests still PASS.

- [ ] **Step 3: Create `publish/landing-template-internal.html`**: copy
  `publish/landing-template.html`, then change exactly: `<title>` to
  `RHOAI Agentic Hub · Internal artifacts`, the hero `<h1>` text to
  `Internal artifacts`, and the tagline paragraph to:
  `Internal-audience artifacts published from the rhoai-agentic-hub manifest. Interim host on this repo's GitHub Pages; moving to protected GitLab Pages later.`
  Keep `{{COUNT}}`, `{{META}}`, `{{SECTIONS}}` placeholders intact.

- [ ] **Step 4: Implement in `scripts/hublib/publisher.py`**:
  - `def build_plan(root, audience="public"):` and change the filter line
    to `if e.get("audience") != audience: continue`
  - `def generate_landing(root, plan, hub_sha="", template_name="landing-template.html"):`
    and read `Path(root) / "publish" / template_name`
  - `def apply(root, pages_dir, hub_sha="", audience="public"):` with
    `plan = build_plan(root, audience)` and

```python
    template_name = ("landing-template.html" if audience == "public"
                     else "landing-template-internal.html")
```

    passed via `generate_landing(root, plan, hub_sha, template_name)`.
    The snapshot filename stays `SNAPSHOT` (each target is its own clone,
    so snapshots are naturally per-target).
  - In `scripts/hub_publish.py`: add
    `ap.add_argument("--audience", choices=["public", "internal"], default="public")`
    and pass `audience=args.audience` to `apply`; final print becomes
    `f"hub_publish[{args.audience}]: {len(copied)} artifact(s), landing regenerated"`.

- [ ] **Step 5: Run full test file, expect all PASS**:
`python -m pytest scripts/tests/test_publisher.py -v`

- [ ] **Step 6: Amend the spec's snapshot naming** (implementation detail
  ruling): in `docs/specs/2026-07-11-component-hub-buildout-design.md`
  replace the sentence naming `.publish-snapshot-internal.json` with:
  `each target clone keeps its own .publish-snapshot.json (targets are separate clones, so snapshots are per-target by construction)`.

- [ ] **Step 7: Commit**

```bash
git add scripts/hublib/publisher.py scripts/hub_publish.py publish/landing-template-internal.html scripts/tests/test_publisher.py docs/specs/2026-07-11-component-hub-buildout-design.md
git commit -m "feat(publish): audience-aware targets, internal landing template

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

### Task 2: Public-to-internal link lint (TDD)

**Files:**
- Modify: `scripts/hublib/publisher.py` (new function), `scripts/hublib/schema.py`
- Test: `scripts/tests/test_publisher.py`

**Interfaces:**
- Consumes: `load_manifest`, `LINK_ATTR_RE`, `EXTERNAL_PREFIXES` (publisher.py)
- Produces: `check_audience_links(root) -> list[str]`, wired into
  `schema.lint_repo` as errors.

- [ ] **Step 1: Failing tests** (append to test_publisher.py):

```python
from hublib.publisher import check_audience_links


def test_check_audience_links_flags_public_to_internal(tmp_path):
    root = make_repo(tmp_path)
    write(root, "features/x/enablement/site/index.html",
          '<a href="../internal/">peek</a>')
    errors = check_audience_links(root)
    assert len(errors) == 1
    assert "x/internal" in errors[0]


def test_check_audience_links_clean_and_internal_to_public_ok(tmp_path):
    root = make_repo(tmp_path)
    write(root, "features/x/enablement/internal/index.html",
          '<a href="../site/">fine</a> <a href="https://example.com/x">ext</a>')
    assert check_audience_links(root) == []
```

- [ ] **Step 2: Run, expect ImportError/FAIL**:
`python -m pytest scripts/tests/test_publisher.py -k audience_links -v`

- [ ] **Step 3: Implement** in `scripts/hublib/publisher.py` (add
`import posixpath` at top):

```python
def check_audience_links(root):
    """Public artifacts must not link into internal dests (the #13
    audience boundary): a public page linking to an internal artifact
    would 404 or VPN-block once the internal target moves to GitLab."""
    root = Path(root)
    entries = load_manifest(root)
    internal_dests = [str(e["dest"]).strip("/") for e in entries
                      if e.get("audience") == "internal" and e.get("dest")]
    errors = []
    if not internal_dests:
        return errors
    for e in entries:
        if e.get("audience") != "public" or not e.get("source") or not e.get("dest"):
            continue
        src = root / e["source"]
        dest = str(e["dest"]).strip("/")
        if src.is_dir():
            files = sorted(p for p in src.rglob("*") if p.suffix.lower() in (".html", ".htm", ".js"))
        elif src.suffix.lower() in (".html", ".htm"):
            files = [src]
        else:
            continue
        for f in files:
            base = (posixpath.join(dest, f.relative_to(src).parent.as_posix())
                    if src.is_dir() else posixpath.dirname(dest))
            text = f.read_text(encoding="utf-8", errors="replace")
            for m in LINK_ATTR_RE.finditer(text):
                raw = m.group(1).strip()
                if raw.lower().startswith(EXTERNAL_PREFIXES):
                    continue
                target = unquote(raw.split("#", 1)[0].split("?", 1)[0])
                if not target:
                    continue
                norm = (posixpath.normpath(target.lstrip("/")) if target.startswith("/")
                        else posixpath.normpath(posixpath.join(base, target)))
                for idest in internal_dests:
                    if norm == idest or norm.startswith(idest + "/"):
                        errors.append(f"{f.relative_to(root).as_posix()}: public artifact "
                                      f"links into internal dest '{idest}': {raw}")
    return errors
```

In `scripts/hublib/schema.py`: add `from . import publisher` to the
existing `from . import frontmatter, jiramap, refresh` import, and in
`lint_repo` after `errors.extend(validate_manifest(root))` add
`errors.extend(publisher.check_audience_links(root))`.

- [ ] **Step 4: Run full suite**: `python -m pytest scripts/tests -v` (all PASS).

- [ ] **Step 5: Commit**

```bash
git add scripts/hublib/publisher.py scripts/hublib/schema.py scripts/tests/test_publisher.py
git commit -m "feat(lint): public artifacts must not link into internal dests

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

### Task 3: gh-pages target live, hubs flipped internal

**Files:**
- Modify: `.github/workflows/publish.yml`, `publish/manifest.yaml`,
  `conventions/publishing.md`, `.claude/skills/hub.publish/SKILL.md`,
  `docs/enhancements.md`
- Possibly modify: hub HTML with relative links to public artifacts
  (rewrite to absolute public URLs)

**Interfaces:**
- Consumes: Task 1 CLI (`--audience internal`).
- Produces: live internal site; both hub entries `audience: internal`;
  public site without hubs. Later hub tasks publish against this target.

- [ ] **Step 1: Bootstrap the gh-pages branch** (from a scratch dir, not
the working tree):

```bash
cd "$(mktemp -d)" && git clone --no-checkout https://github.com/solaius/rhoai-agentic-hub.git gh && cd gh
git switch --orphan gh-pages
printf '<!doctype html><title>bootstrap</title>' > index.html
touch .nojekyll
git add -A && git commit -m "bootstrap gh-pages target"
git push origin gh-pages
```

- [ ] **Step 2: Enable Pages on the repo**:
`gh api -X POST repos/solaius/rhoai-agentic-hub/pages -f "source[branch]=gh-pages" -f "source[path]=/"`
A 409 means already enabled (fine). Known gotcha
(fact-hub-build-operational-gotchas): if the first Pages build wedges,
push any empty commit to gh-pages to kick it.

- [ ] **Step 3: Flip the two hub entries** in `publish/manifest.yaml`:
in the `mcp-gateway/rhcl/` and `mcp-ecosystem/hub/` entries change
`audience: public` to `audience: internal`. Touch nothing else.

- [ ] **Step 4: Fix boundary and cross-target links.**
Run `python scripts/hub_lint.py`; fix every
`links into internal dest` ERROR by removing the hyperlink from the public
artifact (keep plain text naming the hub; do not link to the internal URL).
Then handle the reverse direction (internal relative links that escape the
internal target): grep both hubs for cross-artifact relative links,

```bash
grep -rnoE 'href="\.\./\.\./(\.\./)?[a-z-]+/[a-z0-9-]+/[^"]*"' features/mcp-gateway/enablement/rhcl-hub features/mcp-ecosystem/enablement/management-hub | grep -v -E 'mcp-ecosystem/hub|mcp-gateway/rhcl|mcp-catalog/hub|mcp-lifecycle-operator/hub|mcp-registry/hub'
```

and rewrite each hit that points at a PUBLIC dest to the absolute URL form
`https://solaius.github.io/rhoai-agentic-hub-pages/<dest>/`. Hub-to-hub
links stay relative.

- [ ] **Step 5: Rewrite `.github/workflows/publish.yml`** to:

```yaml
name: publish
on:
  push:
    branches: [main]
permissions:
  contents: write
jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/checkout@v4
        with:
          repository: solaius/rhoai-agentic-hub-pages
          token: ${{ secrets.PAGES_PUSH_TOKEN }}
          path: pages-repo
      - uses: actions/checkout@v4
        with:
          ref: gh-pages
          path: internal-pages
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install -r scripts/requirements.txt
      - run: python scripts/hub_publish.py --pages-dir pages-repo --hub-sha "$GITHUB_SHA"
      - run: python scripts/hub_publish.py --check-links --pages-dir pages-repo
      - run: python scripts/hub_publish.py --audience internal --pages-dir internal-pages --hub-sha "$GITHUB_SHA"
      - run: python scripts/hub_publish.py --check-links --pages-dir internal-pages
      - name: Commit and push pages
        run: |
          cd pages-repo
          git config user.name "hub-publish-bot"
          git config user.email "noreply@users.noreply.github.com"
          git add -A
          if git diff --cached --quiet; then echo "no changes"; exit 0; fi
          git commit -m "publish: hub ${GITHUB_SHA}"
          git push
      - name: Commit and push internal pages
        run: |
          cd internal-pages
          git config user.name "hub-publish-bot"
          git config user.email "noreply@users.noreply.github.com"
          git add -A
          if git diff --cached --quiet; then echo "no changes"; exit 0; fi
          git commit -m "publish(internal): hub ${GITHUB_SHA}"
          git push origin HEAD:gh-pages
```

- [ ] **Step 6: Update docs.** `conventions/publishing.md`: replace the
`audience: internal is schema-reserved...` bullet with the two-target
contract (public = pages repo; internal = this repo's gh-pages at
`https://solaius.github.io/rhoai-agentic-hub/`, interim until protected
GitLab; each target clone keeps its own snapshot; public artifacts must
never link into internal dests, lint-enforced; internal-to-public links
use absolute public URLs). Add the internal root under `Live root:`.
`.claude/skills/hub.publish/SKILL.md`: add that the skill now asks
public-vs-internal per entry and both directions of an audience flip are
gated. `docs/enhancements.md`: under #13 add a shipped-interim note
(gh-pages target live, GitLab tail open, date + spec link); priority table
row 13 status to `Shipped (interim)`; under #35 note the audience ruling
(hubs internal-only) and spec link.

- [ ] **Step 7: Verify + commit + watch.**
`python -m pytest scripts/tests -v` then `python scripts/hub_lint.py`
(0 errors) then commit everything:

```bash
git add -A && git diff --cached --stat
git commit -m "feat(#13 interim): internal publish target on gh-pages, hubs flipped internal

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
git push
```

Watch the publish run (Global Constraints loop). Then verify: public
landing no longer lists either hub and
`https://solaius.github.io/rhoai-agentic-hub-pages/mcp-gateway/rhcl/` is
gone (404), while `https://solaius.github.io/rhoai-agentic-hub/mcp-gateway/rhcl/`
and `.../mcp-ecosystem/hub/` render (fetch each URL, expect the hub
title in the HTML). Report all four checks.

---

### Task 4: hub.refresh-site sections contract (TDD)

**Files:**
- Modify: `scripts/hublib/refresh.py`, `.claude/skills/hub.refresh-site/SKILL.md`
- Test: `scripts/tests/test_refresh.py`

**Interfaces:**
- Produces: refresh configs may carry
  `sections: {jtbd: true, jira_tracker: {project: RHAISTRAT}}` (validated);
  skill knows how to maintain both page types. Tasks 9/13/17/20/21 rely on
  this schema.

- [ ] **Step 1: Failing tests.** Append to `scripts/tests/test_refresh.py`
(uses its existing `write`, `make_site`, and `VALID` fixtures):

```python
def test_sections_block_valid(tmp_path):
    make_site(tmp_path)
    write(tmp_path, "features/x/work/refresh-site.yaml",
          VALID + "sections:\n  jtbd: true\n  jira_tracker: {project: RHAISTRAT}\n")
    assert validate(tmp_path) == ([], [])


def test_sections_block_invalid(tmp_path):
    make_site(tmp_path)
    write(tmp_path, "features/x/work/refresh-site.yaml",
          VALID + "sections:\n  bogus: 1\n  jtbd: yes please\n  jira_tracker: {}\n")
    errors, _ = validate(tmp_path)
    assert len([e for e in errors if "section" in e]) == 3
```

- [ ] **Step 2: Run, expect FAIL**: `python -m pytest scripts/tests/test_refresh.py -v`

- [ ] **Step 3: Implement** in `scripts/hublib/refresh.py`: add
`import re` and `SECTION_KEYS = {"jtbd", "jira_tracker"}` at module level;
inside `validate()`'s per-config loop (after the sources checks, before
the loop ends) add:

```python
        sections = data.get("sections")
        if sections is not None:
            if not isinstance(sections, dict):
                errors.append(f"{rel}: sections must be a mapping")
            else:
                for key, val in sections.items():
                    if key not in SECTION_KEYS:
                        errors.append(f"{rel}: unknown section '{key}' "
                                      f"(allowed: {', '.join(sorted(SECTION_KEYS))})")
                    elif key == "jtbd" and not isinstance(val, bool):
                        errors.append(f"{rel}: sections.jtbd must be true|false")
                    elif key == "jira_tracker" and (
                            not isinstance(val, dict)
                            or not re.match(r"^[A-Z][A-Z0-9]*$",
                                            str(val.get("project") or ""))):
                        errors.append(f"{rel}: sections.jira_tracker needs "
                                      f"project: <JIRAPROJECT>")
```

- [ ] **Step 4: Run suite green**: `python -m pytest scripts/tests -v`

- [ ] **Step 5: Extend `.claude/skills/hub.refresh-site/SKILL.md`.** Update
the frontmatter description (add: maintains the standard JTBD and Jira
Tracker sections where the config declares them). In the numbered flow:
under step 3 (SWEEP) add two source bullets: `jtbd: when
sections.jtbd is true, re-derive the hub's job set (narrative/knowledge/
jtbd-*.md whose features: list contains the hub's feature id) and diff
against the Jobs to be Done page (new jobs, changed status/evidence,
removals)` and `jira tracker: when sections.jira_tracker is set, re-run
python scripts/hub_jira.py --sweep <feature> (refreshes
work/jira-snapshot.yaml), filter issues to keys of the configured project,
and diff against the tracker page rows`. Under step 6 (APPLY) add: `Tracker
rows show key, type, public summary (render "(summary withheld)" when the
snapshot summary is null: the unauthenticated-probe rule), status, fix
versions, updated date, linked to https://issues.redhat.com/browse/<KEY>.
Jira unreachable = propose no tracker change; the stale data-verified date
is the signal. Never hand-fill tracker cells from memory.`

- [ ] **Step 6: Commit**

```bash
git add scripts/hublib/refresh.py scripts/tests/test_refresh.py .claude/skills/hub.refresh-site/SKILL.md
git commit -m "feat(refresh-site): standard JTBD + Strats jira-tracker section contracts

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

### Task 5: mcp-catalog Jira scope + snapshot

**Files:**
- Modify: `features/features.yaml`
- Create: `features/mcp-catalog/work/jira-snapshot.yaml` (generated)

- [ ] **Step 1:** In `features/features.yaml`, under the `mcp-catalog`
entry (after `description:`), add:

```yaml
  jira:
    jql: '(project = RHAISTRAT AND (summary ~ "\"MCP Catalog\"" OR key in (RHAISTRAT-1339, RHAISTRAT-1084, RHAISTRAT-1306, RHAISTRAT-1149, RHAISTRAT-1859, RHAISTRAT-1994))) OR (project = RHOAIENG AND component = "AI Hub" AND summary ~ "\"MCP Catalog\"")'
    ref_types: [Outcome, Feature]
```

(Seed keys from `features/mcp-catalog/knowledge/ref-mcp-catalog-strat-jiras.md`.)

- [ ] **Step 2:** Validate and sweep (env comes from `restricted/.env` via
the doctor's shell wiring):
`python scripts/hub_jira.py --try-jql "$(python -c "import yaml;print(yaml.safe_load(open('features/features.yaml'))['features'][4]['jira']['jql'])")"`
(sanity: returns issues, no error; index 4 = mcp-catalog, verify first),
then `python scripts/hub_jira.py --sweep mcp-catalog`.
Expected: `features/mcp-catalog/work/jira-snapshot.yaml` created with
RHAISTRAT keys present. If Jira is unreachable, STOP and report (Task 9
needs this snapshot).

- [ ] **Step 3:** `python scripts/hub_index.py && python scripts/hub_lint.py`
(0 errors), then commit:

```bash
git add features/features.yaml features/mcp-catalog/work/jira-snapshot.yaml features/index.md features/mcp-catalog/index.md views/
git commit -m "jira(mcp-catalog): stored scope + first snapshot for the catalog hub tracker

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

### Task 6: Catalog hub scaffold

**Files:**
- Create: `features/mcp-catalog/enablement/catalog-hub/{nav.js,styles.css,index.html,reference.html,artifact.md}`

**Interfaces:**
- Produces: the SITE_MAP page paths below; Tasks 7-9 must create exactly
  these files.

- [ ] **Step 1:** Copy `styles.css` verbatim from
`features/mcp-ecosystem/enablement/management-hub/styles.css`.

- [ ] **Step 2:** Copy `nav.js` from the management hub, then replace:
`SIDEBAR_STATE_KEY = 'catalog-hub-sidebar-state'`; header title block to
`<span class="hub-header__logo">MCP</span> Catalog`; `SITE_MAP` to:

```javascript
const SITE_MAP = [
  { section: 'Understand It', id: 'understand', pages: [
    { title: 'What Is the MCP Catalog?', path: 'understand/what-is-the-catalog.html' },
    { title: 'Jobs to be Done', path: 'understand/jobs-to-be-done.html' },
    { title: 'Upstream & Ecosystem', path: 'understand/upstream-ecosystem.html' },
  ]},
  { section: 'Sell It', id: 'sell', pages: [
    { title: 'Positioning & Trust Tiers', path: 'sell/positioning.html' },
    { title: 'Competitive Landscape', path: 'sell/competitive.html' },
  ]},
  { section: 'Build It', id: 'build', pages: [
    { title: 'Bring Your Own MCP Server', path: 'build/byo-mcp-server.html' },
    { title: 'Enablement & Troubleshooting', path: 'build/enablement-troubleshooting.html' },
  ]},
  { section: 'Govern It', id: 'govern', pages: [
    { title: 'Partner Onboarding Pipeline', path: 'govern/partner-pipeline.html' },
    { title: 'Trust & Policy', path: 'govern/trust-policy.html' },
  ]},
  { section: 'Plan It', id: 'plan', pages: [
    { title: 'Roadmap', path: 'plan/roadmap.html' },
    { title: 'Jira Tracker (Strats)', path: 'plan/jira-tracker.html' },
    { title: 'Gaps & Open Questions', path: 'plan/gaps-open-questions.html' },
  ]},
];
```

and `HUB_NETWORK` to:

```javascript
const HUB_NETWORK = [
  { title: '🏠 MCP Ecosystem Hub', path: '../../mcp-ecosystem/hub/' },
  { title: '🔌 MCP Gateway Hub', path: '../../mcp-gateway/rhcl/' },
  { title: '📦 MCP Catalog Hub', path: '../../mcp-catalog/hub/', self: true },
  { title: '⚙️ MCP Lifecycle Operator Hub', path: '../../mcp-lifecycle-operator/hub/', comingSoon: true },
  { title: '📋 MCP Registry Hub', path: '../../mcp-registry/hub/', comingSoon: true },
];
```

- [ ] **Step 3:** Write `index.html` (landing: hero with one-paragraph
what/why from `features/mcp-catalog/knowledge/fact-mcp-catalog-overview.md`,
section cards linking the five sections, release-train strip DP 3.4 ->
DP 3.5 -> TP 3.6 EA1 -> GA 3.6) and `reference.html` (quick facts table:
upstream repos, release train, key Jiras, glossary of trust tiers). Use
`features/mcp-ecosystem/enablement/management-hub/index.html` and
`reference.html` as the structural reference (same div ids `hub-header`,
`hub-sidebar`, `breadcrumb` div, `page-footer` with `data-verified`).

- [ ] **Step 4:** Write `artifact.md`:

```markdown
---
type: artifact
title: MCP Catalog Knowledge Hub
description: 14-page enablement site for the MCP Catalog (discovery/storefront) across understand/sell/build/govern/plan. Internal audience; customer-engagement detail anonymized.
timestamp: <TODAY>
features: [mcp-catalog]
source: seeded from rhcl-hub govern/catalog.html + management-hub component sections + mcp-catalog partition (spec 2026-07-11)
---
14-page multi-section site sharing styles.css/nav.js; entry point
index.html. Published internal via publish/manifest.yaml (dest
mcp-catalog/hub/).
```

- [ ] **Step 5:** `python scripts/hub_index.py && python scripts/hub_lint.py`
(0 errors; nav links to not-yet-written pages are fine, hub_lint does not
check HTML links), commit `feat(catalog-hub): scaffold (nav, styles, landing, reference)`.

---

### Task 7: Catalog Understand + Sell pages

**Files:**
- Create: `catalog-hub/understand/what-is-the-catalog.html`,
  `understand/jobs-to-be-done.html`, `understand/upstream-ecosystem.html`,
  `sell/positioning.html`, `sell/competitive.html`
  (all under `features/mcp-catalog/enablement/catalog-hub/`)

**Seed map (read these before writing):**
- RHCL `features/mcp-gateway/enablement/rhcl-hub/govern/catalog.html`:
  Purpose, "What Shipped in 3.4 DP" 10-row partner table, partner pipeline
  (goes to govern task, skip here), technical requirements, upstream
  integration, post-Summit plans.
- Management `understand/component-overview.html`: the MCP Catalog card
  (~350 words: status, shipped list, key features incl RHAISTRAT-1859
  admin UI, PM vision, limitation).
- Partition: `fact-mcp-catalog-overview.md` (discover/deploy/connect/consume
  chain), `fact-mcp-upstream-status.md` (official registry >=36K records,
  AAIF, 2026-07-28 stateless spec, subregistry federation),
  `fact-mcp-catalog-competitive-landscape.md` (July 2026 refresh),
  `research/01-upstream-mcp-catalog-registry.md`, `research/02-competitive-mcp-catalogs.md`,
  `question-official-registry-federation.md`, `question-spec-version-policy-ga.md`.
- Management `sell/competitive.html`: the "Catalog & Registry Landscape"
  12-row table; RHCL `sell/competitive.html` has the richer variant (adds
  Databricks Unity Catalog): the RICHER table is the one that moves here.

**Page specs:**
- `what-is-the-catalog.html`: purpose (discovery/browsing/verification/
  trust tiers), the discover->deploy->connect->consume chain, what shipped
  in 3.4 DP (the 10-row table verbatim), key features, current limitation
  (no auto-prereqs), relationship callout (complements Gateway runtime
  enforcement; Registry is system of record).
- `jobs-to-be-done.html`: render every `narrative/knowledge/jtbd-*.md`
  whose `features:` includes `mcp-catalog` (as of the spec:
  jtbd-discover-agentic-assets at minimum; grep to confirm the full set:
  `grep -l "mcp-catalog" narrative/knowledge/jtbd-*.md`). Per job: title,
  persona badge, status badge, the When/I-want/So-I-can block, "How the
  Catalog addresses it" bullets, source link to the GitHub blob URL.
- `upstream-ecosystem.html`: kubeflow/hub = code upstream,
  model-metadata-collection = content upstream, official registry scale +
  immaturity, AAIF governance, subregistry federation expectation, spec
  version churn in the TP->GA window (contradiction item 4 phrasing:
  normalize GA to "RHOAI 3.6 (code freeze Oct 23, 2026)").
- `positioning.html`: storefront story, trust tiers (RH/partner/community/
  BYO), RBAC/approval, admin UI (RHAISTRAT-1859), PM vision (Tool Masking /
  Input Simplification / Output Filtering) clearly labeled VISION not
  shipped.
- `competitive.html`: the full 12+ entry landscape table (RHCL variant,
  cells verbatim) plus the July 2026 refresh findings; label Registry
  governance rows as roadmap, not shipped (contradiction item 1).

- [ ] **Step 1:** Read every seed file above in full.
- [ ] **Step 2:** Write the five pages (skeleton = any management-hub
  section page; footer data-verified = TODAY).
- [ ] **Step 3:** Open each in a quick sanity pass: every page pulls nav
  via `<script src="../nav.js"></script>` and renders standalone.
- [ ] **Step 4:** `python scripts/hub_lint.py` (0 errors), commit
  `content(catalog-hub): understand + sell sections`.

---

### Task 8: Catalog Build + Govern pages

**Files:**
- Create: `catalog-hub/build/byo-mcp-server.html`,
  `build/enablement-troubleshooting.html`, `govern/partner-pipeline.html`,
  `govern/trust-policy.html`

**Seed map:**
- Management `build/configuration-reference.html`: "Bring Your Own MCP
  Server" section (container packaging checklist, restricted-SCC table,
  catalog-yaml metadata spec + kubeflow/hub catalog-yaml-reference.md link)
  and the `mcpCatalog: true` enablement patch in
  `build/operator-installation.html`.
- Management `build/troubleshooting.html` issues #2 (ConfigMap prereqs not
  auto-created) and #3 (server not appearing in catalog deployments).
- RHCL `govern/catalog.html`: partner pipeline 6 steps (Curation ->
  BDM Outreach -> Consent Letter -> Technical Attestation -> Image Build ->
  Catalog Integration), 7-row technical requirements table, STDIO RFEs
  (RHAIRFE-2514/2515/2516 from the component card).
- Partition: `fact-partner-mcp-catalog.md` is in mcp-ecosystem knowledge
  (check `features/mcp-ecosystem/knowledge/fact-partner-mcp-catalog.md`),
  `question-kubeflow-hub-catalog-alignment.md` (ANSWERED: kubeflow/hub IS
  the upstream).

**Page specs:**
- `byo-mcp-server.html`: packaging checklist, SCC compliance table,
  catalog-yaml metadata spec with a fenced YAML example, schema pointer.
- `enablement-troubleshooting.html`: `mcpCatalog: true` dashboard patch
  snippet, the two catalog troubleshooting issues with resolutions,
  prereq limitation + RHAIRFE-2434.
- `partner-pipeline.html`: the 6-step pipeline with per-step detail, the
  technical-requirements table verbatim, consent/attestation notes
  (anonymized: no partner-negotiation specifics beyond the shipped list).
- `trust-policy.html`: trust tiers and what each certifies, RBAC/approval
  flows, federation posture (official registry question open), version
  pinning + health surfacing.

Steps: same rhythm as Task 7 (read seeds, write four pages, lint, commit
`content(catalog-hub): build + govern sections`).

---

### Task 9: Catalog Plan pages

**Files:**
- Create: `catalog-hub/plan/roadmap.html`, `plan/jira-tracker.html`,
  `plan/gaps-open-questions.html`

**Consumes:** `features/mcp-catalog/work/jira-snapshot.yaml` (Task 5),
Task 4's tracker row contract.

**Page specs:**
- `roadmap.html`: version table DP 3.4 (shipped, code freeze Apr 10) ->
  DP continues 3.5 -> TP 3.6 EA1 -> GA RHOAI 3.6 (code freeze Oct 23,
  2026). Source callout: owner re-plan 2026-07-10/11. Seed: Management
  `plan/roadmap.html` MCP Catalog sub-table.
- `jira-tracker.html`: table of snapshot issues whose key starts
  `RHAISTRAT-`; columns Key (linked to
  `https://issues.redhat.com/browse/<KEY>`), Type, Summary (`(summary
  withheld)` when null), Status, Fix versions (joined, `-` if empty),
  Updated. Intro sentence: tracked scope + swept date from the snapshot.
- `gaps-open-questions.html`: prereq automation (RHAIRFE-2434), STDIO
  transport (RHAIRFE-2514/2515/2516), spec-version policy at GA, official
  registry federation posture, community-vs-partner positioning, partner
  pipeline mechanics Qs (from Management `plan/open-questions.html` Q7,
  Q11-Q16 catalog items + partition question- files).

Steps: read seeds, write three pages, lint, commit
`content(catalog-hub): plan section (roadmap, strats tracker, gaps)`.

---

### Task 10: Catalog launch: publish + parent thinning

**Files:**
- Modify: `publish/manifest.yaml`, management-hub `nav.js`, `index.html`,
  `understand/component-overview.html`, `reference.html`,
  `build/configuration-reference.html`, `build/troubleshooting.html`,
  `plan/gaps.html`, `plan/open-questions.html`, `plan/roadmap.html`,
  `sell/competitive.html`; RHCL `govern/catalog.html`,
  RHCL `sell/competitive.html`
- Create: `features/mcp-catalog/work/refresh-catalog-hub.yaml`

- [ ] **Step 1: Manifest entry** (append to `publish/manifest.yaml`):

```yaml
- source: features/mcp-catalog/enablement/catalog-hub/
  dest: mcp-catalog/hub/
  audience: internal
  title: MCP Catalog Knowledge Hub
  description: 14-page enablement site for the MCP Catalog (discovery/storefront) across understand/sell/build/govern/plan.
```

- [ ] **Step 2: Refresh config** `features/mcp-catalog/work/refresh-catalog-hub.yaml`:

```yaml
# Source list for hub.refresh-site. Tracked and PUBLIC.
site: features/mcp-catalog/enablement/catalog-hub/
sources:
  gdocs:
  - {id: 1L3yVBHKJLwVJ2SzF5NunzXc8gFJNZKbMU6OWfPyB_fE, title: MCP Catalog}
  - {id: 1Z2rA0fiAC2Zt_AWnond_Ogi3-2cqEzElN-U76M1x740, title: Partners MCP Catalog}
  github:
  - kubeflow/hub
  - opendatahub-io/model-metadata-collection
  jira:
    jql: project = RHAISTRAT AND summary ~ "\"MCP Catalog\""
  slack:
    channels: [forum-ai-asset-management]
    window_days: 14
  local:
  - features/mcp-catalog/knowledge/
  - features/mcp-catalog/research/
sections:
  jtbd: true
  jira_tracker: {project: RHAISTRAT}
```

(Verify the model-metadata-collection org/repo against
`features/mcp-ecosystem/knowledge/ref-model-metadata-collection-repo.md`
before writing.)

- [ ] **Step 3: Management hub launch conversion.**
  - `nav.js`: Catalog HUB_NETWORK entry loses `comingSoon: true`.
  - `index.html` + `reference.html`: convert Catalog coming-soon badges to
    live links (`grep -rn "coming soon" features/mcp-ecosystem/enablement/management-hub -i`
    and fix the Catalog ones only).
  - `understand/component-overview.html`: Catalog card shrinks to ~80
    words (purpose, status line) + prominent `Full depth: MCP Catalog
    Knowledge Hub` link to `../../../mcp-catalog/hub/`.
  - `build/configuration-reference.html`: remove the BYO-MCP packaging/
    catalog-yaml block, keep seam artifacts (dashboard patches,
    gen-ai-aa-mcp-servers ConfigMap, namespace label, ownership table),
    add link to the catalog hub BYO page.
  - `build/troubleshooting.html`: issues #2/#3 collapse to one-line
    pointers to `catalog-hub` enablement-troubleshooting.
  - `plan/gaps.html` + `plan/open-questions.html`: catalog cards/questions
    collapse to pointers.
  - `plan/roadmap.html`: Catalog sub-table collapses to one matrix row +
    link.
  - `sell/competitive.html`: replace the Catalog & Registry landscape
    table with a two-sentence summary + link to catalog-hub competitive.
- [ ] **Step 4: RHCL hub thinning.** `govern/catalog.html`: reduce to
  gateway-vantage content only (the relationship callout, planned-scope
  gap callout, one-paragraph summary) + link to the catalog hub;
  `sell/competitive.html`: same table replacement as Management. Bump both
  pages' data-verified to TODAY.
- [ ] **Step 5: Verify + ship.**
  `python scripts/hub_index.py && python scripts/hub_lint.py` (0 errors),
  `python -m pytest scripts/tests -v`, commit
  `launch(catalog-hub): publish internal + management/rhcl thinning`, push,
  watch publish.yml green, then fetch
  `https://solaius.github.io/rhoai-agentic-hub/mcp-catalog/hub/` (expect
  the hub title) and the management hub sidebar (expect Catalog as a live
  link, MCPLO/Registry still coming soon). Report results.

---

### Task 11: MCPLO hub scaffold

Mirror of Task 6 under
`features/mcp-lifecycle-operator/enablement/mcplo-hub/`:
`SIDEBAR_STATE_KEY = 'mcplo-hub-sidebar-state'`, header
`<span class="hub-header__logo">MCP</span> Lifecycle Operator`,
HUB_NETWORK self = MCPLO entry, Catalog entry now LIVE (no comingSoon),
Registry still comingSoon. SITE_MAP:

```javascript
const SITE_MAP = [
  { section: 'Understand It', id: 'understand', pages: [
    { title: 'What Is the MCP Lifecycle Operator?', path: 'understand/what-is-mcplo.html' },
    { title: 'Architecture', path: 'understand/architecture.html' },
    { title: 'Jobs to be Done', path: 'understand/jobs-to-be-done.html' },
    { title: 'Upstream', path: 'understand/upstream.html' },
  ]},
  { section: 'Sell It', id: 'sell', pages: [
    { title: 'Positioning & Competitive', path: 'sell/positioning-competitive.html' },
  ]},
  { section: 'Build It', id: 'build', pages: [
    { title: 'Installation', path: 'build/installation.html' },
    { title: 'MCPServer CRD Reference', path: 'build/mcpserver-crd.html' },
    { title: 'Supported Servers & Troubleshooting', path: 'build/supported-servers-troubleshooting.html' },
  ]},
  { section: 'Govern It', id: 'govern', pages: [
    { title: 'Distribution & Entitlement', path: 'govern/distribution-entitlement.html' },
    { title: 'Qualification & Security', path: 'govern/qualification-security.html' },
    { title: 'Gateway Integration', path: 'govern/gateway-integration.html' },
  ]},
  { section: 'Plan It', id: 'plan', pages: [
    { title: 'Roadmap', path: 'plan/roadmap.html' },
    { title: 'Jira Tracker (Strats)', path: 'plan/jira-tracker.html' },
    { title: 'Gaps & Open Questions', path: 'plan/gaps-open-questions.html' },
  ]},
];
```

index.html hero from `fact-mcp-lifecycle-operator-overview.md`;
reference.html quick facts (repos, CRD group `mcp.x-k8s.io/v1alpha1`,
release train, key Jiras). artifact.md: 16-page site, features
`[mcp-lifecycle-operator]`, internal audience. Lint + commit
`feat(mcplo-hub): scaffold`.

---

### Task 12: MCPLO Understand + Sell pages

**Files:** `understand/what-is-mcplo.html`, `understand/architecture.html`,
`understand/jobs-to-be-done.html`, `understand/upstream.html`,
`sell/positioning-competitive.html` under mcplo-hub.

**Seed map:** RHCL `govern/lifecycle-operator.html` (purpose: deployment
primitive NOT governance; component flow; independence-from-gateway
callout); Management MCPLO card in `understand/component-overview.html`;
partition `fact-mcp-lifecycle-operator-overview.md`,
`fact-mcplo-three-repo-architecture.md`, `fact-mcpserver-crd.md`,
`fact-mcp-spec-stateless-shift.md`, `fact-mcplo-key-decisions-from-slack.md`;
research `01-upstream.md` (RH 83% commits, 5/8 approvers, NVIDIA release
manager, v0.1->v0.2 in 10 weeks), `02-architecture.md` (DSC module,
Catalog->MCPLO->Gateway->Studio flow, TLS gap), `03-competitive.md` (10
competitors, 3-tier market, ToolHive/Stacklok closest), `05-landscape.md`
(stateless shift, AAIF, NSA/OWASP/CSA, 97M SDK downloads/month).

**Page specs:** what-is (purpose, component flow diagram text, what it is
NOT, independence from Gateway); architecture (three-repo model:
kubernetes-sigs upstream / opendatahub-io module / opendatahub-operator
parent, two-tier image, DSC integration, CRD->controller->Deployment+
Service+NetworkPolicy, stateless spec shift impact on scaling); JTBD (grep
`narrative/knowledge/jtbd-*.md` for `mcp-lifecycle-operator`; if zero jobs
match, the page states that no narrative jobs are mapped yet and lists the
two nearest ecosystem jobs by hand: manage-agent-fleet,
govern-agent-tool-access, each marked "related, mapped at the ecosystem
level"); upstream (governance, commit share, release velocity, since-v0.2.0
changes: NetworkPolicy reconciliation, TLS profile, RBAC verbs, Go 1.26.5);
positioning-competitive (3-tier market, ToolHive coopetition, why
in-platform operator wins for RHOAI customers; no customer stories exist:
frame via field QA the partition holds, anonymized).

Steps: read seeds, write 5 pages, lint, commit
`content(mcplo-hub): understand + sell sections`.

---

### Task 13: MCPLO Build + Govern pages

**Files:** `build/installation.html`, `build/mcpserver-crd.html`,
`build/supported-servers-troubleshooting.html`,
`govern/distribution-entitlement.html`, `govern/qualification-security.html`,
`govern/gateway-integration.html` under mcplo-hub.

**Seed map:** Management `build/operator-installation.html` (Tier 2
MCPLO install: manual `oc apply` of install.yaml v0.2.0, kubernetes-sigs
vs openshift fork note, validated-versions matrix row);
`build/configuration-reference.html` (the MCPServer CRD YAML example,
verified 2026-07-10); `build/troubleshooting.html` issue #9 (crashloop /
CRD order); RHCL `govern/lifecycle-operator.html` (supported servers
table, distribution & entitlement tables, update delivery, qualification
split, RHAIRFE-1456 productization); partition `qa-mcplo-*.md` (3 field
QA files), `question-disconnected-catalog-delivery.md`,
`question-ols-mcplo-transition.md`, `ref-ocpmcp-347-gateway-integration.md`,
`ref-gateway-integration-proposal.md`, research `04-requirements.md` (P0
gaps, capability levels); roadmap profile `memory/profiles/roadmap.md`.

**MANDATORY corrections (spec checklist items 7-9):**
- Entitlement: MCPLO ships with OCP entitlement (base OCP customers get
  MCPLO); RHOAI adds Registry, Authorino, Limitador. Do NOT carry forward
  "RHOAI restricted-use entitlement required".
- TP dates: OCP-side TP mid-July 2026 (OCPSTRAT-3263, functional
  qualification) vs RHOAI TP mid-Aug 2026 (RHAISTRAT-1773, deployment/
  integration qualification). Both stated, distinctly.
- Gateway integration is GA scope, not TP (Slack decision May 2026,
  OCPMCP-347).

**Page specs:** installation (two-tier install model, oc apply + DSC
paths, validated versions, cluster-admin requirement flagged); CRD
reference (full MCPServer YAML example verbatim from
configuration-reference, field table: source/config/runtime, status
conditions, discovery URL, K8s v1.28+); supported-servers-troubleshooting
(supported table incl WIP rows, crashloop issue, field QA:
dependencies/defaults); distribution-entitlement (corrected entitlement
story, not-in-OperatorHub/OLM, update delivery connected/disconnected,
disconnected catalog question, OCP 5.0 RHOAI Limited install flow);
qualification-security (OCP-functional vs RHOAI-deployment split, TLS 1.3
ML-KEM note + upstream TLS gap, NSA/OWASP framing, stateless spec shift);
gateway-integration (OCPMCP-347 proposal summary, GA scope, manual today,
`update_mode: SYSTEM_MANAGED` handoff to Registry).

Steps: read seeds, write 6 pages, lint, commit
`content(mcplo-hub): build + govern sections`.

---

### Task 14: MCPLO Plan pages + launch

**Files:** `plan/roadmap.html`, `plan/jira-tracker.html`,
`plan/gaps-open-questions.html`; then the Task-10 launch pattern for MCPLO.

- [ ] **Step 1:** Refresh the snapshot:
  `python scripts/hub_jira.py --sweep mcp-lifecycle-operator`.
- [ ] **Step 2:** Write the three plan pages. Roadmap: v0.2.0 DP (June 17)
  -> OCP TP mid-July (OCPSTRAT-3263) -> RHOAI TP mid-Aug (RHAISTRAT-1773,
  on-risk OCPMCP-298) -> GA RHOAI 3.6 (RHAISTRAT-1995, OCPSTRAT-2879) ->
  OCP 5.0 (RHOAI Limited); OpenShift/K8s MCP server tracked separately
  (OCPSTRAT-2739/3337). Tracker: Task 9 format, RHAISTRAT keys from the
  fresh snapshot. Gaps: P0 (observability, disconnected, OLS transition,
  Helm), maturity Level 1-2 -> 3-4, cluster-admin, OLM 1.0 removal in OCP
  5.0, plus open questions (RHOAI-exclusive vs standalone).
- [ ] **Step 3: Launch conversion** (Task 10 pattern, MCPLO edition):
  manifest entry (dest `mcp-lifecycle-operator/hub/`, audience internal,
  16-page description); `refresh-mcplo-hub.yaml`:

```yaml
site: features/mcp-lifecycle-operator/enablement/mcplo-hub/
sources:
  gdocs:
  - {id: 1vRu8pSLi6VMrX1Cdn64RdQTOhjQZG97BIxTRZadtjVY, title: MCPLO Weekly Meeting Notes}
  github:
  - kubernetes-sigs/mcp-lifecycle-operator
  jira:
    keys: [RHAISTRAT-1339]
    jql: project = RHAISTRAT AND (summary ~ "\"MCP Lifecycle Operator\"" OR summary ~ "MCPLO")
  slack:
    channels: [forum-mcp-lifecycle-operator]
    window_days: 14
  local:
  - features/mcp-lifecycle-operator/knowledge/
  - features/mcp-lifecycle-operator/research/
sections:
  jtbd: true
  jira_tracker: {project: RHAISTRAT}
```

  (Add the opendatahub module repo to `github:` after verifying its
  org/name in `fact-mcplo-three-repo-architecture.md`.)
  Management conversion: MCPLO comingSoon off in BOTH management nav.js
  AND catalog-hub nav.js; badges to links; MCPLO card to summary+link;
  operator-installation MCPLO section out (two-tier model + version
  matrix stay) + link; configuration-reference MCPServer CRD out (seam
  artifacts stay) + link; troubleshooting #9 pointer; gaps/questions
  pointers; roadmap sub-table to row. RHCL `govern/lifecycle-operator.html`
  to gateway-vantage summary (independence callout + corrected entitlement
  sentence + link). Security-model MCPLO TLS bullet gets a hub link.
- [ ] **Step 4:** index+lint+pytest, commit
  `launch(mcplo-hub): plan section + publish internal + parent thinning`,
  push, watch green, fetch
  `https://solaius.github.io/rhoai-agentic-hub/mcp-lifecycle-operator/hub/`.

---

### Task 15: Registry hub scaffold

Mirror of Task 6 under `features/mcp-registry/enablement/registry-hub/`:
`SIDEBAR_STATE_KEY = 'registry-hub-sidebar-state'`, header
`<span class="hub-header__logo">MCP</span> Registry`, HUB_NETWORK self =
Registry, Catalog and MCPLO now live, none comingSoon. SITE_MAP:

```javascript
const SITE_MAP = [
  { section: 'Understand It', id: 'understand', pages: [
    { title: 'What Is the MCP Registry?', path: 'understand/what-is-the-registry.html' },
    { title: 'Data Model', path: 'understand/data-model.html' },
    { title: 'Jobs to be Done', path: 'understand/jobs-to-be-done.html' },
  ]},
  { section: 'Sell It', id: 'sell', pages: [
    { title: 'The Governance Story', path: 'sell/governance-story.html' },
  ]},
  { section: 'Build It', id: 'build', pages: [
    { title: 'MVP Scope & Prototype', path: 'build/mvp-scope-prototype.html' },
  ]},
  { section: 'Govern It', id: 'govern', pages: [
    { title: 'Lifecycle & Governance', path: 'govern/lifecycle-governance.html' },
    { title: 'Integrations', path: 'govern/integrations.html' },
  ]},
  { section: 'Plan It', id: 'plan', pages: [
    { title: 'Roadmap', path: 'plan/roadmap.html' },
    { title: 'Jira Tracker (Strats)', path: 'plan/jira-tracker.html' },
    { title: 'Gaps & Open Questions', path: 'plan/gaps-open-questions.html' },
  ]},
];
```

index.html hero states plainly: the Registry is in design phase, this hub
is the design-decision record growing toward TP 3.6 EA1. artifact.md:
12-page site, features `[mcp-registry]`, internal. Lint + commit
`feat(registry-hub): scaffold`.

---

### Task 16: Registry Understand + Sell + Build pages

**Files:** `understand/what-is-the-registry.html`, `understand/data-model.html`,
`understand/jobs-to-be-done.html`, `sell/governance-story.html`,
`build/mvp-scope-prototype.html` under registry-hub.

**Seed map:** RHCL `govern/registry.html` (freshest, data-verified
2026-07-11: purpose, data model flow, two-enum governance tables, observed
tool metadata, MLflow/Databricks RFC, MVP scope 7 bullets, reviewer
questions); Management Registry card (~550 words, data model + enums
tables); partition `fact-mcp-registry.md`,
`fact-mcp-registry-data-model-proposal.md` (the FOUR-TRACK PROPOSAL:
label as proposal), `fact-mcp-flow-34-to-35.md`,
`fact-mcp-server-lifecycle-stages.md`, `ref-mcp-registry-mvp-requirements.md`,
`ref-mlflow-mcp-registry-data-model-proposal.md`; existing public
enablement `registry-ui-prototype` (link via absolute public URL
`https://solaius.github.io/rhoai-agentic-hub-pages/mcp-registry/ui-prototype/`).

**MANDATORY corrections (spec checklist items 1-3):** current model =
MCPServerStatus (Active->Deprecated->Retired) + MCPPublishState
(Draft->Published->Deprecated->Retired) + MCPUpdateMode; four-track
(Lifecycle/Approval/Verification/Certification) is a deferred PROPOSAL.
Registry is NOT built; nothing ships in 3.5 stable; no early-access-in-3.5
claims anywhere.

**Page specs:** what-is (system of record: identity, version, lifecycle
state, certification context, policy-aware visibility; what it solves,
3.4-fragmented vs registry-governed flow); data-model (entity flow
MCPServer -> MCPServerVersion, MCPObservedTool/Snapshot, the two-enum
tables verbatim, then a clearly-bounded "Proposed: four-track model"
section from the proposal fact, invariants); JTBD (grep jtbd files for
`mcp-registry`: jtbd-discover-agentic-assets and any others; same render
format as Task 7); governance-story ("governance: the missing layer"
framing rebuilt honestly: what is VISION vs what is CURRENT DESIGN,
anonymized field signals: "a major telecommunications provider asked for
early access", no 3.5 dates); mvp-scope-prototype (MVP scope bullets, API/
entity sketch from the data model, UI prototype link + screenshots
description, MLflow upstream collaboration status, reviewer open items).

Steps: read seeds, write 5 pages, lint, commit
`content(registry-hub): understand + sell + build sections`.

---

### Task 17: Registry Govern pages

**Files:** `govern/lifecycle-governance.html`, `govern/integrations.html`.

**Seed map:** Management `govern/lifecycle-flow.html` (near-total move:
full lifecycle stages, Today-3.4 vs Target tables, governance tracks
tables, invariants, post-MVP phasing callout); Management
`govern/component-integration.html` Registry flows (Registry->Gateway
Flow 3, Catalog->Registry Flow 4 = RHAISTRAT-2027 3.6 EA1, MCPLO->Registry
`update_mode: SYSTEM_MANAGED`); RHCL `govern/registry.html` integration
gap callout (Registry->Gateway auto-config = GA); partition
`question-mcp-registry-state-propagation.md`,
`question-mlflow-upstream-registry-scope.md`.

**Page specs:** lifecycle-governance (7-stage lifecycle flow, stage
tables, enums + invariants, phasing: current vs post-MVP, explicitly
Registry-owned vs Catalog-surfaced state); integrations (per-component
integration map + the three flows with their Jira keys and timing, MLflow
upstream split question).

Steps: read seeds, write 2 pages, lint, commit
`content(registry-hub): govern section`.

---

### Task 18: Registry Plan pages + launch

Task-14 pattern for Registry:

- [ ] **Step 1:** `python scripts/hub_jira.py --sweep mcp-registry`.
- [ ] **Step 2:** Plan pages. Roadmap: design/DP (NOT in 3.5 stable,
  owner 2026-07-11) -> TP 3.6 EA1 (with Catalog TP + RHAISTRAT-2027
  integration) -> GA RHOAI 3.6 (RHAISTRAT-1993); replan source callout.
  Tracker: RHAISTRAT rows from the snapshot (Task 9 format). Gaps &
  open questions: registry-not-built, registry->gateway auto-config
  missing, Q1-Q4/Q9 block + resolved-questions callouts (keep the
  retarget-in-progress annotations, verify fixversions against the fresh
  snapshot: spec checklist item 5), MVP data-model gaps (6 decisions).
- [ ] **Step 3: Launch conversion**: manifest entry (dest
  `mcp-registry/hub/`, audience internal); `refresh-registry-hub.yaml`:

```yaml
site: features/mcp-registry/enablement/registry-hub/
sources:
  gdocs:
  - {id: 11mJpJ-Py8FxRDYdw41mMWEBvlahENS4rHqnpDNpqa8Y, title: MCP Registry MVP Requirements}
  - {id: 1KOLTSMVjdUhb06rQLSx4G5MVSQLXePToGAQ4wNn31m8, title: MCP Registry Data Model Proposal}
  jira:
    jql: (project = RHOAIENG AND component = "AI Hub" AND (summary ~ "\"MCP Registry\"" OR summary ~ "mcp-registry")) OR (project = RHAISTRAT AND summary ~ "\"MCP Registry\"")
  slack:
    channels: [forum-ai-asset-management]
    window_days: 14
  local:
  - features/mcp-registry/knowledge/
sections:
  jtbd: true
  jira_tracker: {project: RHAISTRAT}
```

  Registry comingSoon off in management, catalog-hub AND mcplo-hub nav.js;
  badges to links; Registry card to summary+link; `govern/lifecycle-flow.html`
  keeps the 7-stage cross-component flow, governance tables collapse to
  pointer; Registry gaps/questions to pointers; roadmap sub-table to row;
  fix "3.5 early access" residue in `sell/customer-stories.html` +
  `sell/summit-feedback.html` (say "early access" without a release
  number, note the 3.6 EA1 target); verify competitive pages carry no
  four-track-as-shipped claims (fixed in Task 10, re-check). RHCL
  `govern/registry.html` to gateway-vantage summary (integration-gap
  callout + update_mode note + link).
- [ ] **Step 4:** index+lint+pytest, commit
  `launch(registry-hub): plan section + publish internal + parent thinning`,
  push, watch green, fetch
  `https://solaius.github.io/rhoai-agentic-hub/mcp-registry/hub/`.

---

### Task 19: Umbrella restructure: IA, directory, merged architecture

**Files:** management-hub `nav.js`, `index.html`,
`understand/component-overview.html` -> becomes
`understand/component-directory.html`, `understand/ecosystem-architecture.html`
(absorbs `govern/component-integration.html`), plus a new
`understand/decision-guide.html`; deletions per below.

- [ ] **Step 1: New SITE_MAP** (target ~13 content pages + home +
reference):

```javascript
const SITE_MAP = [
  { section: 'Ecosystem', id: 'ecosystem', pages: [
    { title: 'What Is MCP Management?', path: 'understand/what-is-mcp-management.html' },
    { title: 'Umbrella Architecture', path: 'understand/ecosystem-architecture.html' },
    { title: 'Personas', path: 'understand/personas.html' },
  ]},
  { section: 'Components', id: 'components', pages: [
    { title: 'Component Directory', path: 'understand/component-directory.html' },
    { title: 'Which Component Do I Need?', path: 'understand/decision-guide.html' },
  ]},
  { section: 'Choose & Integrate', id: 'integrate', pages: [
    { title: 'Integration Scenarios', path: 'build/end-to-end-setup.html' },
    { title: 'Lifecycle Flow', path: 'govern/lifecycle-flow.html' },
    { title: 'Entitlement', path: 'govern/entitlement.html' },
  ]},
  { section: 'Sell It', id: 'sell', pages: [
    { title: 'Value Proposition', path: 'sell/value-prop.html' },
    { title: 'Field Evidence', path: 'sell/customer-stories.html' },
    { title: 'Competitive Landscape', path: 'sell/competitive.html' },
  ]},
  { section: 'Plan & Govern', id: 'plan', pages: [
    { title: 'Roadmap', path: 'plan/roadmap.html' },
    { title: 'Jira Tracker (Strats Rollup)', path: 'plan/jira-tracker.html' },
    { title: 'Security Model', path: 'govern/security-model.html' },
    { title: 'Gaps & Open Questions', path: 'plan/gaps.html' },
  ]},
];
```

- [ ] **Step 2: Page work.**
  - `component-directory.html` (rename of component-overview): one card
    per component (Gateway, Catalog, MCPLO, Registry, plus AI Gateway
    pointer), each ~80 words + status line + hub link; delete the old
    deep content (already thinned in Tasks 10/14/18).
  - `ecosystem-architecture.html`: merge in the still-relevant
    cross-component seams from `govern/component-integration.html`
    (integration map, the numbered flows in summary form with links to
    component-hub depth), then DELETE `govern/component-integration.html`.
  - `decision-guide.html` (new): "which component do I need?" decision
    table: rows = needs ("deploy an MCP server", "govern tool access at
    runtime", "discover approved servers", "prove provenance/audit"),
    columns = component, what it gives you, hub link.
  - `sell/customer-stories.html` absorbs `sell/summit-feedback.html`
    (retitled Field Evidence, anonymized as-is), DELETE summit-feedback.
    `plan/gaps.html` absorbs `plan/open-questions.html` (one page, two
    sections), DELETE open-questions. `build/end-to-end-setup.html`
    reframed: integration scenarios with mechanics thinned to
    component-hub links. `build/operator-installation.html`,
    `build/configuration-reference.html`, `build/troubleshooting.html`:
    fold their remaining seam content into `end-to-end-setup.html` (version
    matrix, seam artifacts, cross-component issues) and DELETE all three.
- [ ] **Step 3:** Update every deleted page's inbound links
  (`grep -rn "component-integration.html\|summit-feedback.html\|open-questions.html\|operator-installation.html\|configuration-reference.html\|troubleshooting.html" features/ --include=*.html`)
  to their new homes, including from the three component hubs and RHCL.
- [ ] **Step 4:** index+lint, commit
  `restructure(management-hub): umbrella IA, component directory, merged architecture, decision guide`.
  (Publish rides the next task's push.)

---

### Task 20: Umbrella rollup tracker + gateway scope + refresh rebalance

**Files:** `features/features.yaml` (mcp-gateway jira block),
management-hub `plan/jira-tracker.html`,
`features/mcp-ecosystem/work/refresh-management-hub.yaml`,
`features/mcp-gateway/work/jira-snapshot.yaml` (generated)

- [ ] **Step 1: Gateway Jira scope.** Derive candidate RHAISTRAT keys:
  `grep -rn "RHAISTRAT-[0-9]*" features/mcp-gateway/knowledge/ | grep -oE "RHAISTRAT-[0-9]+" | sort -u`.
  Add to features.yaml under mcp-gateway:

```yaml
  jira:
    jql: 'project = RHAISTRAT AND (summary ~ "\"MCP Gateway\"" OR key in (<the keys found>))'
    ref_types: [Outcome, Feature]
```

  Validate with `--try-jql`, then `python scripts/hub_jira.py --sweep mcp-gateway`.
  FLAG in the final report: this scope is provisional, owner may refine.
- [ ] **Step 2: Rollup tracker.** Rewrite management `plan/jira-tracker.html`
  as the cross-component RHAISTRAT rollup: one section per component
  (Gateway, Catalog, MCPLO, Registry), rows from each feature's
  `work/jira-snapshot.yaml` filtered to RHAISTRAT (Task 9 row format),
  intro = swept dates per feature. Outcome rows (type Outcome) listed
  first per section.
- [ ] **Step 3: Rebalance** `refresh-management-hub.yaml`: drop
  `features/mcp-registry/knowledge/` and `features/mcp-catalog/knowledge/`
  from `local:` (their hubs own them now; keep mcp-ecosystem paths); add

```yaml
sections:
  jtbd: true
  jira_tracker: {project: RHAISTRAT}
```

- [ ] **Step 4:** index+lint+pytest, commit
  `feat(management-hub): strats rollup tracker, gateway jira scope, refresh rebalance`,
  push, watch publish green, fetch the management hub URL and confirm the
  new IA renders (sidebar shows the five new sections).

---

### Task 21: Network pass

**Files:** RHCL `nav.js` + new `understand/jobs-to-be-done.html` + new
`plan/jira-tracker.html` + `plan/skus.html` check; management
`understand/jobs-to-be-done.html` (new); all five hubs' nav.js; touched
pages across the network.

- [ ] **Step 1: RHCL HUB_NETWORK.** Add to RHCL `nav.js` the same
  HUB_NETWORK block (self = Gateway entry, all five live) AND the
  sidebar-rendering code for it: port the `Hub Network` section block from
  management nav.js `buildSidebar()` verbatim (RHCL nav.js lacks it; diff
  the two files first and port only the HUB_NETWORK rendering).
- [ ] **Step 2: RHCL retrofits.** `understand/jobs-to-be-done.html`: jobs
  whose `features:` includes `mcp-gateway` (grep to enumerate), Task 7
  render format; add to RHCL SITE_MAP under Understand. `plan/jira-tracker.html`:
  RHAISTRAT rows from `features/mcp-gateway/work/jira-snapshot.yaml`
  (Task 20), add to SITE_MAP under Plan. Refresh `plan/skus.html` stub's
  pointer (entitlement page moved? verify path still resolves).
  Add `sections: {jtbd: true, jira_tracker: {project: RHAISTRAT}}` to
  `features/mcp-gateway/work/refresh-rhcl-hub.yaml`.
- [ ] **Step 3: Management JTBD.** New
  `understand/jobs-to-be-done.html`: aggregate jobs tagged with ANY of
  mcp-ecosystem, mcp-gateway, mcp-catalog, mcp-lifecycle-operator,
  mcp-registry, grouped by component, each linking to the component hub's
  JTBD page; add to management SITE_MAP (Ecosystem section).
- [ ] **Step 4: Reciprocal sweep.** For each of the five hubs: HUB_NETWORK
  identical (five entries, correct self, zero comingSoon); every
  cross-hub content link resolves (run the grep from Task 3 Step 4 across
  all five hub dirs; fix stragglers); every page footer data-verified is
  TODAY for touched pages.
- [ ] **Step 5: Contradiction checklist verification.** Grep the network
  for each spec-checklist item and confirm resolved:
  `grep -rn "four-track\|Draft → Candidate\|early access" features/*/enablement/*hub* --include=*.html -i`
  (no shipped-four-track claims, no 3.5-early-access), `grep -rn "restricted-use entitlement" features/mcp-lifecycle-operator features/mcp-gateway/enablement/rhcl-hub/govern/lifecycle-operator.html` (corrected), TP-date and GA-phrasing spot checks. Fix anything found.
- [ ] **Step 6:** index+lint+pytest, commit
  `network(hubs): reciprocal links, RHCL hub-network + retrofits, management jtbd, checklist sweep`,
  push, watch green, fetch all five internal hub URLs (200 + title each).

---

### Task 22: Closeout

**Files:** `docs/enhancements.md`,
`features/mcp-ecosystem/work/management-hub-umbrella-plan.md`,
`memory/` via hub.capture

- [ ] **Step 1:** `docs/enhancements.md`: move #35 to Done (shipped date,
  spec + plan links, one-paragraph summary: 3 hubs + devolution + internal
  target; note the provisional gateway Jira scope for owner review).
  Priority-table rows for 35 and 13 updated.
- [ ] **Step 2:** `management-hub-umbrella-plan.md`: status note at top:
  executed via the spec/plan (links), devolution map retained as the
  historical record.
- [ ] **Step 3:** Run the full gate one last time:
  `python -m pytest scripts/tests -v && python scripts/hub_lint.py && python scripts/hub_index.py --check`.
- [ ] **Step 4:** Commit `backlog(#35): shipped, umbrella plan executed`,
  push, watch publish green.
- [ ] **Step 5:** Fire hub.capture for the durable decisions: (a) hubs are
  internal-audience on this repo's gh-pages, GitLab later (#13 interim
  shipped); (b) hub.refresh-site now owns JTBD + Strats-tracker sections;
  (c) the provisional mcp-gateway Jira scope awaiting owner refinement.
  Then report: live URLs (internal landing + five hubs), public landing
  state, page counts per hub, checklist confirmation, anything flagged.
