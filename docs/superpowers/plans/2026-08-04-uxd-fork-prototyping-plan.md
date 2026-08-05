# UXD Fork Prototyping Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Retrofit `hub.prototype` to generate React/PF6 pages in the UXD
RHOAI fork (with live GitLab Pages previews) and retire the static HTML
pipeline, per the approved spec.

**Spec:** `docs/superpowers/specs/2026-08-04-uxd-fork-prototyping-design.md`
(owner rulings R1-R6). GitHub issue:
https://github.com/solaius/rhoai-agentic-hub/issues/16

**Architecture:** Two repos, one session. The hub keeps grounding, metadata
(`prototype.yaml` v2), views, and gates; the fork at `F:\code\rh\rhoai`
(origin `pedouble/rhoai`) holds generated React pages on one branch per
prototype, based off `upstream/3.6`, previewed at
`<pages_base_url>/branch-<slug>/`.

**Tech Stack:** Python 3.11 (hublib, pytest), Bash (doctor.sh, Git Bash on
Windows), React 18 + TypeScript + PatternFly 6 + webpack (fork), GitLab
CI/Pages.

## Global Constraints

- This hub repo is PUBLIC. No NDA content in any tracked write.
- No em dashes in written artifacts; use `--` (owner preference).
- Commits: explicit pathspecs only, NEVER `git add -A` (shared checkout).
  End every hub commit message with:
  `Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>`
- GATE steps: show the described summary and wait for the owner's explicit
  OK before running the gated command. Nothing is pushed, no manifest entry
  is removed, and no fork branch is pushed without its gate.
- Never edit the fork's CI/config files (`.gitlab-ci.yml`, `package.json`,
  `package-lock.json`, `webpack.*`, `tsconfig.json`, `.eslintrc.js`).
  `PAGES_URL` is a GitLab CI/CD variable, never a file change.
- Fork network ops (fetch upstream, push, preview URLs, GitLab API) need
  the Red Hat VPN. The probe is silent; only its FAILURE is surfaced:
  "Can't reach gitlab.cee.redhat.com -- make sure you're connected to the
  Red Hat VPN."
- `gitlab.cee.redhat.com` has a self-signed cert: `curl -sk` for API calls;
  `git config http."https://gitlab.cee.redhat.com".sslVerify false` in the
  fork for https fetches.
- Hub verification trio (run from repo root, all must pass):
  `python -m pytest scripts/tests -v`, `python scripts/hub_lint.py`,
  `python scripts/hub_index.py --check`.
- Fork verification pair (run in the fork, non-negotiable per its
  AGENTS.md): `npx eslint <changed files> --no-warn` with 0 errors, then
  `npm run build` passing.
- Fork ESLint gotchas: members inside one `import { ... }` must be
  alphabetical; unused params/vars must be `_`-prefixed; every `.tsx` needs
  `import * as React from 'react'` (classic JSX runtime); unique kebab-case
  page-prefixed `id` attributes on PatternFly components.

---

### Task 1: prototype.yaml v2 schema validation

**Files:**
- Modify: `scripts/hublib/schema.py` (constants at lines 51-52; function
  `_lint_prototypes` at lines 204-243)
- Test: `scripts/tests/test_schema.py` (append after
  `test_narrative_prototype_accepted`, ~line 701)

**Interfaces:**
- Consumes: existing `lint_repo(root)` and test helpers `write(root, rel,
  text)`, `make_repo(tmp_path)` already in `test_schema.py`.
- Produces: dual-schema validation. A `prototype.yaml` WITH a `branch` key
  is validated as v2 (fields: title, description, status, components,
  source_repo, branch, base, preview_url, current, versions; `current` must
  be a key of `versions`; every version entry needs `commit` -- a sha or
  the literal `static`; optional `snapshots` entries need `branch` +
  `preview_url`). A file WITHOUT `branch` keeps today's legacy checks
  (current dir exists, each version dir has index.html). Task 9 writes a
  v2 file; Task 10 may remove the legacy path.

- [ ] **Step 1: Write the failing tests**

Append to `scripts/tests/test_schema.py`:

```python
V2_YAML = (
    "title: Skills Catalog UI\ndescription: Fork prototype\nstatus: active\n"
    "components: [mcp-registry]\n"
    "source_repo: git@gitlab.cee.redhat.com:pedouble/rhoai.git\n"
    "branch: skills-catalog-ui\nbase: upstream/3.6\n"
    "preview_url: https://example.pages.redhat.com/branch-skills-catalog-ui/\n"
    "current: v2\n"
    "versions:\n"
    "  v1: {timestamp: 2026-08-03, commit: static, summary: static era}\n"
    "  v2: {timestamp: 2026-08-05, commit: def5678, summary: fork build}\n")


def test_prototype_v2_accepted_without_version_dirs(tmp_path):
    root = make_repo(tmp_path)
    write(root, "components/x/prototype/skills-catalog-ui/prototype.yaml", V2_YAML)
    write(root, "components/components.yaml",
          "components:\n- id: x\n  title: X\n  description: d\n"
          "- id: mcp-registry\n  title: R\n  description: d\n")
    errors, _ = lint_repo(root)
    assert not any("prototype" in e.lower() for e in errors)


def test_prototype_v2_missing_required_field_is_error(tmp_path):
    root = make_repo(tmp_path)
    write(root, "components/x/prototype/p/prototype.yaml",
          V2_YAML.replace(
              "preview_url: https://example.pages.redhat.com/branch-skills-catalog-ui/\n",
              ""))
    write(root, "components/components.yaml",
          "components:\n- id: x\n  title: X\n  description: d\n"
          "- id: mcp-registry\n  title: R\n  description: d\n")
    errors, _ = lint_repo(root)
    assert any("missing required field 'preview_url'" in e for e in errors)


def test_prototype_v2_current_not_in_versions_is_error(tmp_path):
    root = make_repo(tmp_path)
    write(root, "components/x/prototype/p/prototype.yaml",
          V2_YAML.replace("current: v2", "current: v9"))
    write(root, "components/components.yaml",
          "components:\n- id: x\n  title: X\n  description: d\n"
          "- id: mcp-registry\n  title: R\n  description: d\n")
    errors, _ = lint_repo(root)
    assert any("current 'v9' is not a key of versions" in e for e in errors)


def test_prototype_v2_version_without_commit_is_error(tmp_path):
    root = make_repo(tmp_path)
    write(root, "components/x/prototype/p/prototype.yaml",
          V2_YAML.replace("commit: def5678, ", ""))
    write(root, "components/components.yaml",
          "components:\n- id: x\n  title: X\n  description: d\n"
          "- id: mcp-registry\n  title: R\n  description: d\n")
    errors, _ = lint_repo(root)
    assert any("versions.v2 needs 'commit'" in e for e in errors)


def test_prototype_v2_snapshot_missing_fields_is_error(tmp_path):
    root = make_repo(tmp_path)
    write(root, "components/x/prototype/p/prototype.yaml",
          V2_YAML + "snapshots:\n  v1: {branch: p-v1}\n")
    write(root, "components/components.yaml",
          "components:\n- id: x\n  title: X\n  description: d\n"
          "- id: mcp-registry\n  title: R\n  description: d\n")
    errors, _ = lint_repo(root)
    assert any("snapshots.v1 needs 'branch' and 'preview_url'" in e for e in errors)


def test_prototype_legacy_still_validated(tmp_path):
    # No 'branch' key -> legacy path: current must be an existing dir.
    root = make_repo(tmp_path)
    write(root, "components/x/prototype/registry-ui/prototype.yaml",
          "title: R\ndescription: d\nstatus: active\ncurrent: v1\n"
          "versions:\n  v1:\n    timestamp: 2026-07-09\n    summary: s\n"
          "components: [mcp-registry]\n")
    write(root, "components/components.yaml",
          "components:\n- id: x\n  title: X\n  description: d\n"
          "- id: mcp-registry\n  title: R\n  description: d\n")
    errors, _ = lint_repo(root)
    assert any("does not point to an existing directory" in e for e in errors)
```

- [ ] **Step 2: Run tests to verify the new ones fail**

Run: `python -m pytest scripts/tests/test_schema.py -v -k prototype`
Expected: the 5 new v2 tests FAIL (missing-field messages not produced);
`test_prototype_legacy_still_validated` PASSES already (it exercises
existing behavior); the 8 pre-existing prototype tests PASS.

- [ ] **Step 3: Implement the v2 branch in `_lint_prototypes`**

In `scripts/hublib/schema.py`, add below `PROTOTYPE_REQUIRED` (line 52):

```python
PROTOTYPE_V2_REQUIRED = ("title", "description", "status", "components",
                         "source_repo", "branch", "base", "preview_url",
                         "current", "versions")
```

Replace the body of the per-slug loop in `_lint_prototypes` (keep the
yaml-load and `missing prototype.yaml` handling as-is; after `yrel = ...`
replace the field checks) with:

```python
        if "branch" in data:
            for field in PROTOTYPE_V2_REQUIRED:
                if not data.get(field):
                    errors.append(f"{yrel}: missing required field '{field}'")
            status = data.get("status")
            if status and status not in PROTOTYPE_STATUSES:
                errors.append(f"{yrel}: status must be {'|'.join(PROTOTYPE_STATUSES)}")
            versions = data.get("versions")
            if isinstance(versions, dict):
                current = data.get("current")
                if current and current not in versions:
                    errors.append(f"{yrel}: current '{current}' is not a key of versions")
                for vname, vdata in versions.items():
                    if not isinstance(vdata, dict) or not vdata.get("commit"):
                        errors.append(f"{yrel}: versions.{vname} needs 'commit' "
                                      f"(a sha, or 'static' for migrated static-era entries)")
            snapshots = data.get("snapshots")
            if isinstance(snapshots, dict):
                for sname, sdata in snapshots.items():
                    if (not isinstance(sdata, dict) or not sdata.get("branch")
                            or not sdata.get("preview_url")):
                        errors.append(f"{yrel}: snapshots.{sname} needs 'branch' and 'preview_url'")
        else:
            for field in PROTOTYPE_REQUIRED:
                if not data.get(field):
                    errors.append(f"{yrel}: missing required field '{field}'")
            status = data.get("status")
            if status and status not in PROTOTYPE_STATUSES:
                errors.append(f"{yrel}: status must be {'|'.join(PROTOTYPE_STATUSES)}")
            current = data.get("current")
            if current and not (slug / str(current)).is_dir():
                errors.append(f"{yrel}: current '{current}' does not point to an existing directory")
            versions = data.get("versions")
            if isinstance(versions, dict):
                for vname in versions:
                    vdir = slug / str(vname)
                    if vdir.is_dir() and not (vdir / "index.html").is_file():
                        errors.append(f"{_rel(root, vdir)}: missing index.html")
```

Keep the `components` list check (lines 235-243) after this block -- it
applies to both schemas unchanged.

- [ ] **Step 4: Run the test file, then the full suite**

Run: `python -m pytest scripts/tests/test_schema.py -v`
Expected: ALL PASS.
Run: `python -m pytest scripts/tests -v` and `python scripts/hub_lint.py`
Expected: PASS / 0 errors (the two existing prototype.yaml files are
legacy-schema and still valid).

- [ ] **Step 5: Commit**

```bash
git add scripts/hublib/schema.py scripts/tests/test_schema.py
git commit -m "feat(lint): prototype.yaml v2 schema for fork-based prototypes (#16)

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>" -- scripts/hublib/schema.py scripts/tests/test_schema.py
```

---

### Task 2: Indexer renders fork preview URLs

**Files:**
- Modify: `scripts/hublib/indexer.py` (component-index Prototypes section at
  lines 202-209; `views/prototypes.md` builder at lines 457-481)
- Test: `scripts/tests/test_indexer.py` (append after
  `test_prototypes_view_generated`, ~line 112)

**Interfaces:**
- Consumes: `_load_prototypes(root)` (unchanged) yielding dicts with
  `_slug_rel`/`_home` plus the yaml fields; v2 files carry `preview_url`
  and `branch` (Task 1 semantics).
- Produces: for v2 prototypes both the per-component `index.md` Prototypes
  section and `views/prototypes.md` link `preview_url` and show
  `branch: <branch>`; legacy prototypes keep the
  `/{slug}/{current}/index.html` local link.

- [ ] **Step 1: Write the failing test**

Append to `scripts/tests/test_indexer.py` (its `make_repo(tmp_path)`
already seeds a components.yaml containing `mcp-registry`, and builds run
via `build_all(root, today=TODAY)` -- both already imported/defined in
that file):

```python
def test_prototypes_view_links_preview_url_for_v2(tmp_path):
    root = make_repo(tmp_path)
    write(root, "components/mcp-registry/prototype/skills-ui/prototype.yaml",
          "title: Skills UI\ndescription: Fork prototype\nstatus: active\n"
          "components: [mcp-registry]\n"
          "source_repo: git@gitlab.cee.redhat.com:pedouble/rhoai.git\n"
          "branch: skills-ui\nbase: upstream/3.6\n"
          "preview_url: https://example.pages.redhat.com/branch-skills-ui/\n"
          "current: v1\n"
          "versions:\n  v1: {timestamp: 2026-08-05, commit: abc1234, summary: s}\n")
    built = build_all(root, today=TODAY)
    view = built["views/prototypes.md"]
    assert "https://example.pages.redhat.com/branch-skills-ui/" in view
    assert "branch: skills-ui" in view
    assert "/v1/index.html" not in view
    comp_index = built["components/mcp-registry/index.md"]
    assert "https://example.pages.redhat.com/branch-skills-ui/" in comp_index
```

- [ ] **Step 2: Run it to verify it fails**

Run: `python -m pytest scripts/tests/test_indexer.py -v -k preview`
Expected: FAIL (view still links `/v1/index.html`, no `branch:` text).

- [ ] **Step 3: Implement**

In `scripts/hublib/indexer.py` replace the component-index block
(lines 206-209):

```python
            for sr, d in comp_protos:
                current = d.get("current", "v1")
                href = d.get("preview_url") or f"/{sr}/{current}/index.html"
                lines.append(f"- [{d.get('title', sr)}]({href})"
                             f" — {d.get('description', '')} ({d.get('status', '?')})")
```

And the `views/prototypes.md` loop body (lines 472-479):

```python
            for sr, d in group:
                current = d.get("current", "v1")
                versions = d.get("versions", {})
                ver_list = ", ".join(sorted(versions.keys())) if versions else "—"
                href = d.get("preview_url") or f"/{sr}/{current}/index.html"
                extra = f", branch: {d['branch']}" if d.get("branch") else ""
                lines.append(f"- [{d.get('title', sr)}]({href})"
                             f" — {d.get('description', '')} "
                             f"(status: {d.get('status', '?')}, "
                             f"current: {current}, versions: {ver_list}{extra})")
```

(The `—` characters above are pre-existing generated-view formatting --
keep them byte-identical; the no-em-dash rule is for authored docs.)

- [ ] **Step 4: Run tests**

Run: `python -m pytest scripts/tests/test_indexer.py -v`
Expected: ALL PASS.
Run: `python scripts/hub_index.py && python scripts/hub_index.py --check`
Expected: regenerates cleanly, then 0 stale (legacy prototypes render
exactly as before, so no view content changes yet -- if `--check` reports
stale views, run `python scripts/hub_index.py` once and inspect
`git diff views/` to confirm zero content change, then discard).

- [ ] **Step 5: Commit**

```bash
git add scripts/hublib/indexer.py scripts/tests/test_indexer.py
git commit -m "feat(index): render fork preview URLs for v2 prototypes (#16)

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>" -- scripts/hublib/indexer.py scripts/tests/test_indexer.py
```

---

### Task 3: prototype-fork.yaml + doctor section [12] + setup.md

**Files:**
- Create: `conventions/prototype-fork.yaml`
- Modify: `scripts/doctor.sh` (insert new section AFTER the `[11] git-crypt`
  block ends and BEFORE the `echo "== result: ..."` summary at line 761)
- Modify: `docs/setup.md` (the Optional paragraph, lines 32-38)

**Interfaces:**
- Consumes: doctor helpers `ok`/`warn`/`fail`/`note`, `$MODE`, `$ROOT`,
  `$PYTHON`, and restricted/.env already sourced by section 4 (so
  `$UXD_FORK_DIR` and `$GITLAB_CEE_TOKEN` may be set as env vars).
- Produces: `conventions/prototype-fork.yaml` with `pages_base_url` (filled
  by doctor setup or owner), consumed by the reworked skill (Task 4) and by
  Task 9 to compute `preview_url`. Also the fork clone with an `upstream`
  remote and the fork path granted in `.claude/settings.local.json` under
  `permissions.additionalDirectories`.

- [ ] **Step 1: Create `conventions/prototype-fork.yaml`**

```yaml
# UXD fork prototyping config -- single tracked source of truth for the
# fork-based prototype pipeline (spec:
# /docs/superpowers/specs/2026-08-04-uxd-fork-prototyping-design.md).
# pages_base_url is discovered by `bash scripts/doctor.sh setup` (needs
# GITLAB_CEE_TOKEN) or filled by hand from the fork's GitLab Pages
# settings; commit the change when it lands. The local clone path is
# machine-specific and lives in restricted/.env as UXD_FORK_DIR.
upstream_repo: https://gitlab.cee.redhat.com/uxd/prototypes/rhoai
upstream_project_id: 155361
fork_repo: git@gitlab.cee.redhat.com:pedouble/rhoai.git
fork_project_path: pedouble/rhoai
base_branch: "3.6"
pages_base_url: ""
```

- [ ] **Step 2: Insert doctor section [12]**

In `scripts/doctor.sh`, insert this block between the end of the `[11]`
git-crypt block and the `echo "== result: ..."` line:

```bash
echo "[12] UXD fork prototyping (hub.prototype)"
# Silent VPN probe -- gitlab.cee.redhat.com is VPN-only. Failure is the
# ONLY thing surfaced; success prints nothing extra (owner ruling
# 2026-08-04: automatic, never a question).
GITLAB_CEE="https://gitlab.cee.redhat.com"
HTTP=$(curl -sk --connect-timeout 5 -o /dev/null -w '%{http_code}' \
  "$GITLAB_CEE/api/v4/projects/155361" 2>/dev/null || echo 000)
if [ "$HTTP" != "200" ]; then
  warn "cannot reach gitlab.cee.redhat.com — connect to the Red Hat VPN (fork checks skipped: VPN)"
else
  # 12a. clone. UXD_FORK_DIR (restricted/.env) overrides; default probe.
  FORK=""
  for CAND in "${UXD_FORK_DIR:-}" "/f/code/rh/rhoai" "$HOME/code/rh/rhoai"; do
    [ -n "$CAND" ] && [ -d "$CAND/.git" ] && FORK="$CAND" && break
  done
  if [ -z "$FORK" ]; then
    if [ "$MODE" = "setup" ]; then
      FORK="${UXD_FORK_DIR:-/f/code/rh/rhoai}"
      if git clone git@gitlab.cee.redhat.com:pedouble/rhoai.git "$FORK" 2>/dev/null; then
        ok "fork cloned to $FORK"
      else
        fail "could not clone the fork — check SSH access to gitlab.cee.redhat.com"
        FORK=""
      fi
    else
      fail "fork clone not found — set UXD_FORK_DIR in restricted/.env or run: bash scripts/doctor.sh setup"
    fi
  else
    ok "fork clone at $FORK"
  fi
  if [ -n "$FORK" ]; then
    # 12b. remotes: origin must be the personal fork; upstream must exist.
    ORIGIN_URL=$(git -C "$FORK" remote get-url origin 2>/dev/null || echo "")
    case "$ORIGIN_URL" in
      *pedouble/rhoai*) ok "origin -> pedouble/rhoai" ;;
      *) warn "origin is '$ORIGIN_URL' (expected pedouble/rhoai)" ;;
    esac
    if git -C "$FORK" remote get-url upstream >/dev/null 2>&1; then
      ok "upstream remote configured"
    elif [ "$MODE" = "setup" ]; then
      git -C "$FORK" remote add upstream "$GITLAB_CEE/uxd/prototypes/rhoai.git" \
        && git -C "$FORK" config http."$GITLAB_CEE".sslVerify false \
        && ok "upstream remote added (uxd/prototypes/rhoai, sslVerify off for cee)" \
        || fail "could not add upstream remote"
    else
      fail "no 'upstream' remote — run: bash scripts/doctor.sh setup"
    fi
    if git -C "$FORK" remote get-url upstream >/dev/null 2>&1; then
      if git -C "$FORK" fetch upstream --quiet 2>/dev/null; then
        ok "upstream fetch works"
      else
        warn "upstream fetch failed — check VPN/certs (git config http.$GITLAB_CEE.sslVerify false)"
      fi
    fi
    # 12c. toolchain: node >= 18, npm, node_modules.
    if command -v node >/dev/null 2>&1 && node -e 'process.exit(parseInt(process.versions.node)>=18?0:1)'; then
      ok "node $(node --version)"
    else
      fail "node >= 18 required for the fork build — install Node.js"
    fi
    if [ -d "$FORK/node_modules" ]; then
      ok "fork node_modules installed"
    elif [ "$MODE" = "setup" ]; then
      note "running npm install in the fork (takes a few minutes)..."
      (cd "$FORK" && npm install --no-audit --no-fund >/dev/null 2>&1) \
        && ok "npm install done (submodules init via postinstall)" \
        || fail "npm install failed — run it manually in $FORK"
    else
      fail "fork node_modules missing — run: bash scripts/doctor.sh setup"
    fi
    # 12d. session wiring: the fork as an additional working directory so
    # hub sessions can write there (same local-settings pattern as
    # autoMemoryDirectory in section 3).
    AD_RESULT=$(FORK="$FORK" "$PYTHON" - "$ROOT/.claude/settings.local.json" "$MODE" <<'PY'
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
    case "$AD_RESULT" in
      ok) ok "fork granted as additional working directory" ;;
      written) ok "fork added to additionalDirectories (restart Claude Code to take effect)" ;;
      *) fail "fork not in .claude/settings.local.json additionalDirectories — run: bash scripts/doctor.sh setup" ;;
    esac
    # 12e. Pages + PAGES_URL CI variable. With GITLAB_CEE_TOKEN (api scope,
    # restricted/.env): discover the fork's Pages URL and set the variable
    # via the API. NEVER edit .gitlab-ci.yml (mr-scope-check exists to
    # catch exactly that). Without the token: manual instructions.
    PROJ="$GITLAB_CEE/api/v4/projects/pedouble%2Frhoai"
    if [ -n "${GITLAB_CEE_TOKEN:-}" ]; then
      PAGES_JSON=$(curl -sk -H "PRIVATE-TOKEN: $GITLAB_CEE_TOKEN" "$PROJ/pages" 2>/dev/null || echo "")
      PAGES_LIVE=$(printf '%s' "$PAGES_JSON" | "$PYTHON" -c 'import json,sys
try: print(json.load(sys.stdin).get("url",""))
except Exception: print("")')
      if [ -n "$PAGES_LIVE" ]; then
        ok "fork Pages enabled: $PAGES_LIVE"
        VAR_CODE=$(curl -sk -o /dev/null -w '%{http_code}' -H "PRIVATE-TOKEN: $GITLAB_CEE_TOKEN" "$PROJ/variables/PAGES_URL")
        if [ "$VAR_CODE" = "200" ]; then
          ok "PAGES_URL CI variable set"
        elif [ "$MODE" = "setup" ]; then
          curl -sk -o /dev/null -X POST -H "PRIVATE-TOKEN: $GITLAB_CEE_TOKEN" \
            "$PROJ/variables" --data-urlencode "key=PAGES_URL" --data-urlencode "value=$PAGES_LIVE" \
            && ok "PAGES_URL CI variable created ($PAGES_LIVE)" \
            || fail "could not create PAGES_URL variable (token needs api scope + Maintainer)"
        else
          warn "PAGES_URL CI variable not set — run: bash scripts/doctor.sh setup"
        fi
        # keep conventions/prototype-fork.yaml in sync (tracked -- commit it).
        SYNC=$(PAGES_LIVE="$PAGES_LIVE" "$PYTHON" - "$ROOT/conventions/prototype-fork.yaml" "$MODE" <<'PY'
import os, re, sys
path, mode = sys.argv[1], sys.argv[2]
url = os.environ["PAGES_LIVE"].rstrip("/")
text = open(path, encoding="utf-8").read()
m = re.search(r'(?m)^pages_base_url:\s*"?([^"\n]*)"?\s*$', text)
cur = m.group(1) if m else None
if cur == url:
    print("ok")
elif mode == "setup" and m:
    open(path, "w", encoding="utf-8").write(
        text[:m.start()] + f'pages_base_url: "{url}"' + text[m.end():])
    print("written")
else:
    print("stale")
PY
)
        case "$SYNC" in
          ok) ok "prototype-fork.yaml pages_base_url in sync" ;;
          written) ok "prototype-fork.yaml pages_base_url written — commit the change" ;;
          *) warn "prototype-fork.yaml pages_base_url is stale/empty — run: bash scripts/doctor.sh setup" ;;
        esac
      else
        warn "fork Pages not reachable via API — check token scope, or enable Pages by pushing a branch once"
      fi
    else
      PB=$(grep -E '^pages_base_url:' "$ROOT/conventions/prototype-fork.yaml" 2>/dev/null | sed 's/pages_base_url:[[:space:]]*"\{0,1\}\([^"]*\)"\{0,1\}/\1/')
      if [ -n "$PB" ]; then
        ok "pages_base_url configured: $PB (no GITLAB_CEE_TOKEN — API checks skipped)"
      else
        warn "no GITLAB_CEE_TOKEN in restricted/.env — set PAGES_URL by hand: fork Settings > CI/CD > Variables (key PAGES_URL, value from Deploy > Pages), then put the same URL in conventions/prototype-fork.yaml pages_base_url"
      fi
      note "optional: GITLAB_API_TOKEN as a fork CI variable enables MR-comment previews (fork CI feature)"
    fi
  fi
fi
```

- [ ] **Step 3: Syntax-check and run doctor**

Run: `bash -n scripts/doctor.sh`
Expected: no output (clean parse).
Run: `bash scripts/doctor.sh check`
Expected: section `[12]` appears; on this machine (VPN up, fork present,
node 22, node_modules installed) expect `ok` for clone/node/node_modules,
`fail` for the missing upstream remote and additionalDirectories (setup
not yet run), and the no-token `warn` unless GITLAB_CEE_TOKEN is set.
The pre-existing sections must be unaffected (same PASS/WARN/FAIL as
before this task, plus the new section's lines).

- [ ] **Step 4: Update `docs/setup.md`**

In the Optional paragraph (lines 32-38), after the existing
`Optional (hub.prototype): Node.js for the PatternFly MCP server ...`
sentence, add (matching the established `Optional (<who>): <dep> -- <how>`
shape):

```markdown
Optional (hub.prototype): the UXD RHOAI fork clone + Red Hat VPN --
`bash scripts/doctor.sh setup` (section 12) clones it, wires the
`upstream` remote, installs deps, and grants it as a working directory;
set `UXD_FORK_DIR` in `restricted/.env` if the clone lives somewhere
custom, and `GITLAB_CEE_TOKEN` (GitLab CEE personal token, api scope)
to let setup verify Pages and set the fork's `PAGES_URL` CI variable.
```

- [ ] **Step 5: Commit**

```bash
git add conventions/prototype-fork.yaml scripts/doctor.sh docs/setup.md
git commit -m "feat(doctor): UXD fork prototyping section + prototype-fork.yaml (#16)

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>" -- conventions/prototype-fork.yaml scripts/doctor.sh docs/setup.md
```

- [ ] **Step 6: GATE — owner runs setup**

Show the owner the `bash scripts/doctor.sh check` output for section [12]
and ask them to approve running `bash scripts/doctor.sh setup` (adds the
upstream remote, writes settings.local.json, and -- with a token --
creates PAGES_URL and fills pages_base_url). If no GITLAB_CEE_TOKEN is
available, ask the owner to set PAGES_URL by hand per the warn message and
paste the Pages URL so `pages_base_url` can be filled and committed. Tasks
7-9 need the upstream remote and pages_base_url; do not start Task 7
until this gate clears. Commit any resulting `conventions/prototype-fork.yaml`
change:

```bash
git add conventions/prototype-fork.yaml
git commit -m "chore(doctor): record fork pages_base_url (#16)

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>" -- conventions/prototype-fork.yaml
```

---

### Task 4: Rewrite hub.prototype SKILL.md

**Files:**
- Modify: `.claude/skills/hub.prototype/SKILL.md` (full replacement)

**Interfaces:**
- Consumes: `conventions/prototype-fork.yaml` (Task 3), prototype.yaml v2
  semantics (Task 1).
- Produces: the operative skill instructions Tasks 7-10 and all future
  prototype sessions follow.

- [ ] **Step 1: Replace the entire file with:**

````markdown
---
name: hub.prototype
description: Create, version, or list UI prototypes for a component or across components. Generates React + PatternFly 6 pages in the UXD RHOAI fork (branch per prototype, live GitLab Pages preview), grounded in the component's real architecture, knowledge, and upstream repos. Use when the user says "prototype", "mockup", "UI prototype", "create a prototype for <component>", "new version of the prototype", "list prototypes", or "prototype the <feature>".
---

# hub.prototype

Input: a subcommand (`create`, `version`, `list`) plus a component id
and/or slug. Default subcommand: `create`.

Spec: /docs/superpowers/specs/2026-08-04-uxd-fork-prototyping-design.md
(owner rulings R1-R6). Fork config: /conventions/prototype-fork.yaml.
Structure: /conventions/layout.md (prototype/ leg, prototype.yaml v2).

Prototypes are internal-only (fork GitLab Pages, Red Hat network). There
is no publish mode: the preview URL is the shareable artifact. The fork's
manual whole-app public deploy exists but is owner-only and NEVER fired
by this skill (ruling R4).

## Step 0: Prerequisites (CREATE and VERSION)

1. **VPN probe (automatic, silent).** Run
   `curl -sk --connect-timeout 5 -o /dev/null -w '%{http_code}' https://gitlab.cee.redhat.com/api/v4/projects/155361`.
   On `200`, proceed silently -- no output, no question. Otherwise STOP:
   > Can't reach gitlab.cee.redhat.com -- make sure you're connected to
   > the Red Hat VPN.
2. **PatternFly MCP.** Call `searchPatternFlyDocs` with
   `searchQuery: "button"`, `version: "v6"`. On failure STOP and point at
   `bash scripts/doctor.sh setup` + /docs/mcp-servers.md.
3. **Fork ready.** Read `conventions/prototype-fork.yaml`. Resolve the
   clone dir (UXD_FORK_DIR from restricted/.env, else `F:/code/rh/rhoai`,
   else `~/code/rh/rhoai`). Verify: clone exists, `git -C <fork> remote
   get-url upstream` works, `node_modules/` present, `pages_base_url`
   non-empty. On any miss STOP and point at
   `bash scripts/doctor.sh setup` (section 12).

Skip Step 0 for LIST.

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

Unchanged from the original skill: resolve the component id against
`components/components.yaml` (offer `hub.intake` and stop if unknown),
then deep-read, skipping what does not exist:

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
   components; open their preview URLs for continuity).
h. Restricted context (if `restricted/` exists locally -- informs design,
   NEVER surfaces in output; the fork branch is internal but the hub repo
   is PUBLIC).
i. Fork design context: the fork's `.design/features/` for the closest
   feature area, plus `.agents/rules/design-guidelines.md`.

### Step 2: Scope

Summarize the most design-relevant findings (2-5 sentences), then ask
what to prototype. Accept a description, a Jira key, a knowledge entry
reference, a Figma link/screenshot, or "the whole thing".

### Step 3: Slug

Derive a kebab-case slug (e.g. `registry-ui`). It becomes BOTH the hub
metadata dir (`components/<id>/prototype/<slug>/`) and the fork branch
name. If a branch of that name already exists in the fork, prefix the
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

### Step 7: Generate (in the fork)

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

### Step 8: Verify (non-negotiable)

a. `npx eslint <changed files> --no-warn` -- 0 errors (use
   `--fix` first for import sorting).
b. `npm run build` -- passes.
c. Optional: `npm run start:dev` (port 9000) + Playwright/browser visual
   check; the fork's `check-patternfly-compliance` and `review-design`
   skills as extra review passes.

### Step 9: Metadata (in the hub)

Write `components/<id>/prototype/<slug>/prototype.yaml`:

```yaml
title: <title>
description: <one line>
status: active
components: [<id>]
source_repo: git@gitlab.cee.redhat.com:pedouble/rhoai.git
branch: <slug>
base: upstream/3.6
preview_url: <pages_base_url>/branch-<slug>/
current: v1
versions:
  v1: {timestamp: <today>, commit: <sha after the fork commit>, summary: <one line>}
```

`preview_url` = `pages_base_url` from conventions/prototype-fork.yaml +
`/branch-<branch>/`.

### Step 10: Gate (two-part, one confirm)

Show: fork branch name, files created/changed, eslint/build results, the
prototype.yaml content, and the computed preview URL. On OK:
a. Fork: `git -C <fork> add <files>` then commit with a descriptive
   message, then `git -C <fork> push -u origin <slug>`.
b. Hub: fill `commit:` with the fork sha, then stage the prototype dir +
   regenerated indexes (Step 11) and commit with pathspecs
   (`proto(<id>): <slug> v1`).
On reject: discard both sides, ask what to change.

### Step 11: Reindex

`python scripts/hub_index.py` then `python scripts/hub_lint.py` (0
errors). Stage `components/<id>/prototype/<slug>/`, the component
`index.md`, `components/index.md`, `views/prototypes.md` -- never
`git add -A`.

### Step 12: Report

Print the preview URL and note it goes live when the fork pipeline
finishes (watch: `<fork web url>/-/pipelines`). VPN required to view.
No publish offer -- there is nothing to publish.

## VERSION

Input: `<component>/<slug>`.

1. Read `components/<id>/prototype/<slug>/prototype.yaml` (error +
   suggest `create` if missing).
2. Context: re-run the deltas of CREATE step 1 (what changed in
   knowledge/strategy/Jira since the last version) plus the user's
   feedback. Show a brief; user confirms.
3. In the fork: `git -C <fork> checkout <branch>`; iterate; re-verify
   (CREATE step 8).
4. Snapshot on request: if the user wants the CURRENT state kept
   viewable side by side, first `git -C <fork> branch <slug>-v<N>` (the
   old version) and push it; record under `snapshots:` with its own
   `/branch-<slug>-v<N>/` preview URL.
5. Gate (same two-part shape): fork commit+push; hub prototype.yaml gets
   a new `versions:` entry (sha, date, summary), `current:` bumped.
6. Reindex + report preview URL (redeploys automatically on push).

## Upstreaming (manual, opportunistic -- ruling R5)

Not a subcommand. When a design earns a place in the canonical UXD
prototype, run the fork's own `prepare-merge-request` skill from the fork
(branches base off upstream/3.6, so fork-local divergences never ride
along), then record the MR URL in prototype.yaml `mr_url:` through the
normal gate.

## Key principles

1. **Grounded, not invented.** The context load exists so the prototype
   reflects reality -- real entity names, states, navigation.
2. **PatternFly accuracy is mandatory.** Step 6 queries the MCP for every
   component; the fork's design rules are law.
3. **Real app, real chrome.** The fork provides the actual RHOAI shell,
   nav, and components -- never hand-approximate them.
4. **Branch per prototype, off upstream/3.6.** Keeps previews isolated
   and upstream MRs clean by construction.
5. **Internal-only.** Preview URLs are the artifact; no public mirror
   from this skill, ever.
6. **The gate is sacred.** Nothing is committed or pushed -- in either
   repo -- before the user approves.
````

- [ ] **Step 2: Verify**

Run: `grep -n "prototype-shell\|build_prototype\|extract_uxd_styles\|PUBLISH" .claude/skills/hub.prototype/SKILL.md`
Expected: no matches.
Run: `python scripts/hub_lint.py`
Expected: 0 errors.

- [ ] **Step 3: Commit**

```bash
git add .claude/skills/hub.prototype/SKILL.md
git commit -m "feat(skills): rewrite hub.prototype for UXD-fork generation (#16)

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>" -- .claude/skills/hub.prototype/SKILL.md
```

---

### Task 5: Retire the static pipeline

**Files:**
- Delete: `conventions/prototype-shell/` (entire dir),
  `scripts/build_prototype.py`, `scripts/extract_uxd_styles.py`
- Modify: `docs/specs/2026-08-02-prototype-system-design.md` (supersede
  note), `docs/superpowers/specs/2026-08-03-prototype-template-system-design.md`
  (supersede note)

**Interfaces:**
- Consumes: Task 4 (SKILL.md no longer references these paths).
- Produces: the retired state Tasks 6 and 11 verify against.

- [ ] **Step 1: Delete the pipeline**

```bash
git rm -r conventions/prototype-shell
git rm scripts/build_prototype.py scripts/extract_uxd_styles.py
```

(No tests exist for either script -- verified; nothing to delete in
`scripts/tests/`.)

- [ ] **Step 2: Add supersede notes**

At the top of `docs/specs/2026-08-02-prototype-system-design.md`, directly
under the title line, insert:

```markdown
> **Superseded (2026-08-04):** principles P1/P3/P8 (static HTML, on-disk
> version dirs, static-over-React) are replaced by the UXD fork pipeline --
> see /docs/superpowers/specs/2026-08-04-uxd-fork-prototyping-design.md.
> The prototype/ skeleton leg, grounding flow, and gate discipline remain.
```

At the top of
`docs/superpowers/specs/2026-08-03-prototype-template-system-design.md`,
directly under the `**Status:** Implemented 2026-08-03` line, insert:

```markdown
> **Superseded (2026-08-04):** the entire template system (shell,
> patterns, extract/build scripts) is retired -- prototypes now build as
> React pages in the UXD fork itself. See
> /docs/superpowers/specs/2026-08-04-uxd-fork-prototyping-design.md.
```

- [ ] **Step 3: Verify the reference surface**

Run: `grep -rln "build_prototype\|extract_uxd_styles\|prototype-shell" --include="*.md" --include="*.py" --include="*.sh" --include="*.yaml" . | grep -v ".git/\|node_modules\|.scratch"`
Expected remaining (all intentional at this point): the two superseded
specs, `docs/superpowers/plans/2026-08-03-prototype-template-system-plan.md`
(historical plan), `docs/enhancements-complete.md` (history),
`docs/superpowers/specs/2026-08-04-uxd-fork-prototyping-design.md` (names
them as retired), this plan file, `docs/tooling.md` +
`docs/architecture.md` (cleared in Task 6), and
`components/skills-catalog/prototype/skills-catalog-ui/prototype.yaml`
(rewritten in Task 9).
Run: `python -m pytest scripts/tests -v && python scripts/hub_lint.py`
Expected: PASS / 0 errors.

- [ ] **Step 4: Commit**

```bash
git add -u conventions/prototype-shell scripts/build_prototype.py scripts/extract_uxd_styles.py
git add docs/specs/2026-08-02-prototype-system-design.md "docs/superpowers/specs/2026-08-03-prototype-template-system-design.md"
git commit -m "chore(prototype): retire static prototype pipeline (#16)

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>" -- conventions/prototype-shell scripts/build_prototype.py scripts/extract_uxd_styles.py docs/specs/2026-08-02-prototype-system-design.md docs/superpowers/specs/2026-08-03-prototype-template-system-design.md
```

---

### Task 6: Documentation sweep

**Files:**
- Modify: `docs/capabilities.md`, `docs/skills.md`, `docs/tooling.md`,
  `docs/architecture.md`, `docs/working-here.md`, `conventions/layout.md`,
  `AGENTS.md`, `docs/publishing.md`, `docs/mcp-servers.md`

**Interfaces:**
- Consumes: the new pipeline shape (Tasks 1-5).
- Produces: docs consistent with fork-based prototyping; verified by grep
  + lint in this task and Task 11.

All line numbers below are pre-edit anchors -- locate by the quoted
heading/text, not blindly by number.

- [ ] **Step 1: `docs/capabilities.md`**

  - L28 (table row in "Problems this solves"): change the answer for "UI
    prototypes look nothing like the real product" to say prototypes are
    now real React/PF6 pages built in the UXD team's RHOAI prototype fork
    with live internal previews.
  - L43 ("A day in the life" bullet): rewrite the hub.prototype bullet:
    it loads architecture/upstream/strategy, queries the PatternFly MCP,
    generates a React page in the UXD fork, and pushes a branch whose
    GitLab Pages preview URL lands in `views/prototypes.md`.
  - L63: no change needed (`prototype/` stays in the skeleton list).
  - L112 (Content Creation paragraph): replace the hub.prototype
    paragraph with:

```markdown
- **`hub.prototype`** -- UI prototypes as real React + PatternFly 6 pages
  in the UXD RHOAI fork (`pedouble/rhoai`, based off `upstream/3.6`, one
  branch per prototype). The skill deep-reads the component's knowledge,
  research, strategy, related components, Jira scope, and upstream repos,
  runs mandatory PatternFly MCP component planning, generates the page(s)
  + route + nav wiring in the fork, and verifies with the fork's own
  eslint + build. Pushing the branch yields a live internal preview at
  `<pages>/branch-<slug>/`; the hub records metadata in
  `prototype/<slug>/prototype.yaml` (branch, preview_url, versions as
  commits) and links the preview from `views/prototypes.md`. Versions are
  commits; side-by-side comparison via frozen `<slug>-vN` snapshot
  branches. Internal-only -- the preview URL is the artifact; nothing
  publishes through the pages site.
```

- [ ] **Step 2: `docs/skills.md`** (lines 40-45, the Prototype chain):
  replace with:

```markdown
- **Prototype:** `hub.prototype create <component>` -> context load
  (knowledge + research + strategy + related + Jira + upstream repos) ->
  architecture grounding brief -> component planning (PatternFly MCP
  query per component, fork idiom reuse) -> generate React/PF6 page(s) on
  a fork branch off `upstream/3.6` -> `eslint` + `npm run build` -> gate
  -> push + hub metadata -> reindex -> live preview URL. Then
  `hub.prototype version <component>/<slug>` iterates on the same branch
  (preview redeploys on push).
```

- [ ] **Step 3: `docs/tooling.md`**

  - Delete the two command-table rows for `build_prototype.py` and
    `extract_uxd_styles.py` (L32-33).
  - `schema.py` row (L47): replace the prototype clause with: validates
    `prototype/` dirs -- v2 files (with `branch:`) need source_repo,
    base, preview_url, current in versions, and a `commit` per version;
    legacy files (no `branch:`) keep the version-dir/index.html checks.
  - `indexer.py` row (L48): append: v2 prototypes link their live
    `preview_url` in `views/prototypes.md` and component indexes.

- [ ] **Step 4: `docs/architecture.md`**

  - Delete the `conventions/prototype-shell/` row from the top-level
    anatomy table (L61).
  - Skeleton table row for `prototype/` (L101): change to "prototype
    metadata (`prototype.yaml` v2: fork branch, preview URL, versions as
    commits) -- the pages themselves live in the UXD fork".
  - Views table row (L132): change `views/prototypes.md` description to
    "all prototypes with live preview links, grouped by component, with
    branch, version and status".

- [ ] **Step 5: `docs/working-here.md`** (L30 filing row): change the
  "UI mockup for a component" row's location to
  `components/<f>/prototype/<slug>/prototype.yaml` (metadata; the React
  page lives on a branch of the UXD fork), cross-component ->
  `narrative/prototype/<slug>/`.

- [ ] **Step 6: `conventions/layout.md`**

  - Skeleton table row (L36): `prototype/` = "one subdirectory per
    prototype holding `prototype.yaml` (v2: fork branch + preview URL);
    generated pages live in the UXD fork, not this repo".
  - Replace the `### Prototype structure` section (L43-56) with:

```markdown
### Prototype structure

Each `prototype/<slug>/` holds exactly one file, `prototype.yaml`:

- required: `title`, `description`, `status` (active | superseded |
  archived), `components` (list of component ids), `source_repo`,
  `branch` (fork branch, usually = slug), `base` (e.g. `upstream/3.6`),
  `preview_url` (`<pages_base_url>/branch-<branch>/`), `current` (a key
  of `versions`), `versions` (map `vN -> {timestamp, commit, summary}`;
  `commit` is a fork sha, or `static` on migrated static-era entries)
- optional: `snapshots` (map `vN -> {branch, preview_url}` for frozen
  side-by-side branches), `mr_url` (set when upstreamed)

The React pages themselves live in the UXD fork
(`conventions/prototype-fork.yaml` points at it), one branch per
prototype based off `upstream/3.6`. Cross-component prototypes keep their
metadata in `narrative/prototype/<slug>/`.
```

- [ ] **Step 7: `AGENTS.md`** (skills table row, L61): replace with:

```markdown
| hub.prototype | create/version/list prototypes — React/PF6 pages in the UXD fork with live previews, grounded in component knowledge, PatternFly MCP, and upstream repos |
```

(This row keeps the table's existing em-dash separator style -- match the
neighboring rows byte-for-byte in separator usage.)

- [ ] **Step 8: `docs/publishing.md`** (replace the `### Prototypes`
  section, L71-88, YAML examples included) with:

```markdown
### Prototypes

Prototypes do not publish through the manifest. They are React pages in
the UXD RHOAI fork; the shareable artifact is the branch's GitLab Pages
preview URL (internal, VPN), recorded in each `prototype.yaml` and
rendered in [/views/prototypes.md](/views/prototypes.md). See
/docs/superpowers/specs/2026-08-04-uxd-fork-prototyping-design.md
(ruling R4).
```

- [ ] **Step 9: `docs/mcp-servers.md`** (PatternFly section survives --
  the fork work still requires it):

  - L11 table row: keep, wording "needed by `hub.prototype`" stays true.
  - In the `## PatternFly MCP` section (232-270): replace the sentence
    containing "before generating any HTML" with: "`hub.prototype`
    queries it during component planning -- before generating any React
    -- to ensure correct component selection, props, composition, and
    design token usage."
  - Troubleshooting bullets naming hub.prototype: adjust any "HTML"
    wording to "React page generation"; doctor section reference stays.

- [ ] **Step 10: Verify + commit**

Run: `grep -rn "build_prototype\|extract_uxd_styles\|prototype-shell" docs/ conventions/ AGENTS.md README.md | grep -v "superpowers/\|specs/2026-08-02\|enhancements"`
Expected: no matches.
Run: `python scripts/hub_lint.py`
Expected: 0 errors, no NEW warnings versus the pre-task baseline.

```bash
git add docs/capabilities.md docs/skills.md docs/tooling.md docs/architecture.md docs/working-here.md conventions/layout.md AGENTS.md docs/publishing.md docs/mcp-servers.md
git commit -m "docs: sweep static-prototype references for fork-based prototyping (#16)

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>" -- docs/capabilities.md docs/skills.md docs/tooling.md docs/architecture.md docs/working-here.md conventions/layout.md AGENTS.md docs/publishing.md docs/mcp-servers.md
```

---

### Task 7: Pilot part A — Skills data + catalog page in the fork

All fork paths are relative to the fork clone (default `F:/code/rh/rhoai`;
honor `UXD_FORK_DIR`). Precondition (from Task 3 gate): `git -C <fork>
remote get-url upstream` succeeds and `conventions/prototype-fork.yaml`
has a non-empty `pages_base_url`.

**Files (fork):**
- Create: `src/app/AIHub/Skills/skillsCatalogData.ts`
- Create: `src/app/AIHub/Skills/SkillsCatalog.tsx`
- Create: `src/app/AIHub/Skills/index.ts`
- Modify: `src/app/routes.tsx` (import + AI hub group entries + barrel
  export line at the bottom)
- Modify: `src/app/AppLayout/AppLayout.tsx` (`filterAIHubRoutes`,
  lines ~692-747)

**Interfaces:**
- Consumes: the static prototype source of truth in the HUB repo:
  `components/skills-catalog/prototype/skills-catalog-ui/v1/content/app.js`
  (arrays `SKILLS` 63 entries, `PACKS` 7, `SOURCES` 3).
- Produces: `export interface SkillEntry`, `export interface SkillPack`,
  `export interface SkillSource`, `export const SKILLS: SkillEntry[]`,
  `export const PACKS: SkillPack[]`, `export const SOURCES:
  SkillSource[]`, and `export const SkillsCatalog:
  React.FunctionComponent<{ isTabContent?: boolean }>` -- Task 8 imports
  all of these.

- [ ] **Step 1: Branch off upstream**

```bash
git -C <fork> fetch upstream
git -C <fork> checkout -b skills-catalog-ui upstream/3.6
```

- [ ] **Step 2: Port the data module**

Create `src/app/AIHub/Skills/skillsCatalogData.ts`. Read the hub file
`components/skills-catalog/prototype/skills-catalog-ui/v1/content/app.js`
and mechanically convert `var SKILLS = [...]` (63 entries), `var PACKS`
(7), `var SOURCES` (3) to typed TS. Interfaces:

```ts
export interface SkillEntry {
  name: string;
  slug: string;
  pack: string;
  persona: string;
  invocation: string;
  trustTier: string;
  signing: 'signed' | 'pending' | 'unsigned';
  description: string;
  version: string;
  category: string;
  apis: string[];
  frameworks: string[];
  status: 'active' | 'pending';
  evalScore: number;
}

export interface SkillPack {
  name: string;
  persona: string;
  count: number;
  maturity: 'GREEN' | 'ORANGE';
  repo: string;
  status: string;
}

export interface SkillSource {
  name: string;
  type: string;
  repo: string;
  skills: number;
  status: 'active' | 'pending';
  description: string;
}
```

Known data defects to FIX during the port: set each `SkillPack.count` to
the real number of SKILLS entries with that `pack` (the static data
claims 68 total; reality is 63 -- rh-ai-engineer is 6, not 11). Do not
hardcode facet lists anywhere -- derive personas/categories/packs from
`SKILLS` at runtime. If the source entries carry a field the interface
above lacks, EXTEND the interface -- never drop data during the port.

Verify the port: `node -e` a quick count is not possible on TS; instead
assert in Step 5's build that TypeScript compiles, and manually check
`grep -c "slug:" src/app/AIHub/Skills/skillsCatalogData.ts` prints `63`
(sources have no slug field, packs neither).

- [ ] **Step 3: Build the catalog page**

Create `src/app/AIHub/Skills/SkillsCatalog.tsx`, modeled on
`src/app/AIHub/Agents/AgentCatalog.tsx` (the clean 661-line template) and
`MCPCatalog.tsx`'s Sidebar filter rail. Requirements (from the static
prototype, defects fixed):

- Signature: `const SkillsCatalog: React.FunctionComponent<{ isTabContent?: boolean }>`
  with the standard dual-mode ending:
  `if (isTabContent) { return content; } return <PageSection ...>{content}</PageSection>;`
- Header (standalone mode only): Title "Skills" + description "Discover
  curated AI agent skills provided by Red Hat, partners, and your
  organization." Tabs `Catalog` / `Registry` with Registry `isDisabled`
  (design intent from the static prototype, where it was decorative).
- Left `SidebarPanel` (fixed ~240px) with three multi-select checkbox
  facets, options DERIVED from SKILLS: Persona (7, display the long
  labels: General->General Red Hat Users, SRE->Site Reliability
  Engineers, Developer->Application Developers, Virt Admin->
  Virtualization Admins, OCP Admin->OpenShift Administrators,
  AI/ML Engineer->AI/ML Engineers, Automation Lead->Automation Leads),
  Category (34, first 5 visible -- Security, Diagnostics, Operations,
  Serving, CI/CD -- rest behind a Show more/less toggle), Pack (7).
- Toolbar: `SearchInput` (placeholder "Search by name, keyword, or
  description...", matches name+description, case-insensitive) and a
  4-button single-select `ToggleGroup`: All skills | Red Hat skills |
  Partner skills | Enterprise skills (trustTier '' / 'Red Hat' /
  'Partner' / 'Organization'). Non-empty tier shows a section header
  "{Red Hat provided|Partner verified|Enterprise approved} skills" with
  a live count.
- Active-filter `LabelGroup` chips (Pack:/Persona:/Category:/Search:"..")
  each removable, plus "Clear all filters".
- Live item count derived from the filtered array (fixes the static
  "73 skills" defect).
- Card gallery: PF `Gallery` (`minWidths={{ default: '360px' }}`), one
  `Card` per skill -- header: name + colored trustTier label (check icon
  for Red Hat); body: description truncated at 120 chars; meta row: pack
  outline label, persona blue outline label, signing badge, evalScore
  badge (`NN% pass`: >=90 green, >=80 blue, else orange); footer:
  invocation in monospace. Whole card clickable -> navigate to the
  detail route (Task 8): `navigate(\`/ai-hub/skills/${skill.slug}\`)`.
- Filtering: one `React.useMemo` over SKILLS with AND semantics (search
  AND tier AND (pack empty-or-member) AND (persona ...) AND
  (category ...)) -- derived array, not DOM show/hide.
- Empty state: SearchIcon, "No skills found", "No skills match the
  current filters. Try adjusting your search or filter criteria."
- Unique kebab-case ids on PF components, prefixed `skills-catalog-`
  (e.g. `id="skills-catalog-gallery"`,
  `id={\`skills-catalog-card-${skill.slug}\`}`).

- [ ] **Step 4: Wire route + nav**

- `src/app/AIHub/Skills/index.ts`:

```ts
export { SkillsCatalog } from './SkillsCatalog';
export * from './skillsCatalogData';
```

- `src/app/routes.tsx`: add the import near the other AIHub imports:

```tsx
import { SkillsCatalog } from '@app/AIHub/Skills';
```

  and inside the `label: 'AI hub'` group's `routes:` array (after the
  'MCP servers' sub-group), add:

```tsx
    {
      element: <SkillsCatalog />,
      exact: true,
      label: 'Skills',
      path: '/ai-hub/skills',
      title: 'RHOAI Prototype | AI Hub - Skills',
    },
```

  and append `SkillsCatalog` to the bottom export line
  (`export { AppRoutes, routes, ..., SkillsCatalog };`).
- `src/app/AppLayout/AppLayout.tsx`: `filterAIHubRoutes` (lines
  ~692-747) rebuilds the AI hub nav and DISCARDS the routes.tsx list, so
  also push the item there. Import `SkillsCatalog` from `@app/routes`
  (extend the existing import at line ~42), and inside the rebuilt
  `routes` array add after the Models entry:

```tsx
    {
      element: <SkillsCatalog />,
      exact: true,
      label: 'Skills',
      path: '/ai-hub/skills',
      title: 'RHOAI Prototype | AI Hub - Skills',
    } as IAppRoute,
```

  (unconditional -- no feature flag; this branch is the prototype).

- [ ] **Step 5: Verify**

```bash
cd <fork>
npx eslint src/app/AIHub/Skills/ src/app/routes.tsx src/app/AppLayout/AppLayout.tsx --no-warn
npm run build
```

Expected: 0 eslint errors (run `npx eslint ... --fix` first if import
sorting complains), build passes. Optional visual check:
`npm run start:dev` then open http://localhost:9000/ai-hub/skills --
sidebar shows "Skills" under AI hub; 63 cards; facets filter; count is
live.

- [ ] **Step 6: Commit (fork, local only -- push happens in Task 9's gate)**

```bash
git -C <fork> add src/app/AIHub/Skills src/app/routes.tsx src/app/AppLayout/AppLayout.tsx
git -C <fork> commit -m "Add Skills catalog page (browse) - hub skills-catalog prototype"
```

---

### Task 8: Pilot part B — detail, register modal, admin screens

**Files (fork):**
- Create: `src/app/AIHub/Skills/SkillDetail.tsx`
- Create: `src/app/AIHub/Skills/RegisterSkillModal.tsx`
- Create: `src/app/AIHub/Skills/SkillsAdmin.tsx`
- Modify: `src/app/AIHub/Skills/index.ts`, `src/app/routes.tsx`
- Create: `.design/features/skills-catalog/design-history.md` (or extend
  the area `.design/feature-mapping.md` points at, if one already maps)

**Interfaces:**
- Consumes: `SkillEntry`, `SKILLS`, `SOURCES`, `SkillsCatalog` from
  Task 7.
- Produces: routes `/ai-hub/skills/:slug` (detail) and
  `/settings/skill-resources` (admin); components `SkillDetail`,
  `SkillsAdmin`, `RegisterSkillModal`.

- [ ] **Step 1: SkillDetail** (`src/app/AIHub/Skills/SkillDetail.tsx`)

Resolves the skill via `useParams()` slug against SKILLS (unknown slug ->
PF EmptyState with a back-to-catalog button). Layout per the static
prototype: Breadcrumb (`Skills Catalog` -> name, catalog crumb links back
to `/ai-hub/skills`); header row (icon + h1 name + badges for
`{tier} provided`, signing, eval) with a primary **Register** button
opening `RegisterSkillModal`; two columns -- main (Description card;
Install card with one copyable command per entry in `skill.frameworks`
using templates Claude Code -> `claude mcp add-skill {invocation}`,
Cursor -> `cursor-ext install rh-skill:{slug}`, OpenCode ->
`opencode plugin install {slug}`, Dev Spaces -> `devspaces skill add
{slug}`, via PF `ClipboardCopy`; Compatibility card over the fixed list
Claude Code, Cursor, OpenCode, Dev Spaces, Goose, Hermes, Antigravity
showing Tested/Not tested per membership in `skill.frameworks`; README
card generated from the skill fields -- name, description, pack/persona,
prerequisites from `apis` + frameworks, installation, usage, API
connections table, eval table, License Apache 2.0) and a right sidebar
card "Skill details" (Pack chip, Persona, Category, Trust tier chip,
Signing badge, Version, Invocation `<code>`, Eval pass rate, Live APIs
chips when non-empty, Source `RHEcosystemAppEng/agentic-collections`,
License Apache 2.0). Ids prefixed `skill-detail-`.

- [ ] **Step 2: RegisterSkillModal** (`src/app/AIHub/Skills/RegisterSkillModal.tsx`)

PF `Modal` titled "Register skill", props `{ skill: SkillEntry | null,
isOpen: boolean, onClose: () => void }`. Fields per the static prototype:
Skill name (TextInput readonly), Registry namespace (Select: default
preselected, production, staging, development; popover "The MLflow
registry namespace where this skill will be registered"), Version
(readonly), Pack (readonly), Tags (read-only Label chips: pack, persona,
category, trustTier, signing, plus each API slugified), Description
(TextArea readonly). Footer: Register (primary -> PF Alert/inline
success "Skill X registered to namespace Y", then close), Close (link),
Reset (secondary -> namespace back to default). Ids prefixed
`register-skill-`.

- [ ] **Step 3: SkillsAdmin** (`src/app/AIHub/Skills/SkillsAdmin.tsx`)

Two in-component views switched by local state (matches the static
prototype):
- **Sources list**: title "Skill catalog sources", subtitle "Add and
  manage skill catalog sources. Each source is a YAML catalog file that
  can contain multiple skills for users in your organization." Primary
  button "+ Add a source" (no-op with a PF Tooltip "Prototype: not
  implemented"). PF `Table` over SOURCES: Name | Skill visibility (header
  tooltip) | Source type ("YAML file") | Enable (PF `Switch`, checked
  when status==='active') | Validation status (Ready/Pending label) |
  kebab (`ActionsColumn`: Manage source -> manage view, View in catalog
  -> navigate `/ai-hub/skills`).
- **Manage source**: breadcrumb back to sources; read-only Name and
  derived "{name}-catalog.yaml"; skills count line; expandable "Skill
  visibility" section with Included skills / Excluded skills textareas
  (placeholders from the static: `Example: CVE Explainer, Cluster Health
  Check, rh-sre*` / `Example: *preview*`); preview card with 2 tabs
  (Skills included / Skills excluded) rendering check/X rows; Save
  (returns to list with a success alert) / Cancel. Ids prefixed
  `skills-admin-`.

- [ ] **Step 4: Wire routes**

`index.ts` add: `export { SkillDetail } from './SkillDetail';`
`export { SkillsAdmin } from './SkillsAdmin';`
`export { RegisterSkillModal } from './RegisterSkillModal';`
`routes.tsx`: extend the Skills import, and add two entries -- detail
(NO label -> hidden from nav) after the Skills entry in the AI hub group:

```tsx
    {
      element: <SkillDetail />,
      exact: true,
      path: '/ai-hub/skills/:slug',
      title: 'RHOAI Prototype | AI Hub - Skill Details',
    },
```

and, in the `Settings` group's routes array, alongside its existing
items:

```tsx
    {
      element: <SkillsAdmin />,
      exact: true,
      label: 'Skill resources',
      path: '/settings/skill-resources',
      title: 'RHOAI Prototype | Settings - Skill resources',
    },
```

(The Settings nav is NOT rebuilt by `filterAIHubRoutes` -- only the AI
hub group is -- so no AppLayout edit is needed for the Settings entry.
The detail route has no label, so it needs no AppLayout edit either.)

- [ ] **Step 5: Design history (fork convention)**

Check `.design/feature-mapping.md` for a skills area. If none maps,
create `.design/features/skills-catalog/design-history.md`:

```markdown
# Skills Catalog — design history

## 2026-08-05 — Initial Skills catalog prototype (hub-grounded)

Added AI Hub > Skills: catalog browse (facets: persona/category/pack,
trust-tier toggle, search, 63 skills from the RH agentic-collections
packs), skill detail (install commands per harness, compatibility,
generated README, register-to-MLflow modal), and Settings > Skill
resources (source management with include/exclude visibility).
Migrated from the rhoai-agentic-hub static prototype
(skills-catalog/skills-catalog-ui v1); grounded in the hub's
skills-catalog knowledge and Jira scope (RHAISTRAT-1940/-1339,
RHAIRFE-2207). Owner: Peter Double (PM).
```

- [ ] **Step 6: Verify + commit (fork, local)**

```bash
cd <fork>
npx eslint src/app/AIHub/Skills/ src/app/routes.tsx --no-warn
npm run build
```

Expected: 0 errors, build passes. Optional: dev-server check of
`/ai-hub/skills/cve-explainer` and `/settings/skill-resources`.

```bash
git -C <fork> add src/app/AIHub/Skills src/app/routes.tsx .design/features/skills-catalog
git -C <fork> commit -m "Add Skills detail, register modal, and Settings > Skill resources"
```

---

### Task 9: Pilot landing — push, preview, hub metadata, unpublish (GATED)

**Files (hub):**
- Rewrite: `components/skills-catalog/prototype/skills-catalog-ui/prototype.yaml`
- Delete: `components/skills-catalog/prototype/skills-catalog-ui/v1/` (dir)
- Modify: `publish/manifest.yaml` (remove the skills-catalog ui-prototype
  entry, lines 104-108)
- Regenerate: `views/prototypes.md`, `components/skills-catalog/index.md`,
  `components/index.md`

**Interfaces:**
- Consumes: fork branch `skills-catalog-ui` (Tasks 7-8), `pages_base_url`
  from `conventions/prototype-fork.yaml`, v2 schema (Task 1), indexer
  (Task 2).
- Produces: the migrated pilot -- issue #16's core acceptance evidence.

- [ ] **Step 1: GATE — push the fork branch**

Show the owner: branch name, `git -C <fork> log --oneline upstream/3.6..skills-catalog-ui`,
`git -C <fork> diff --stat upstream/3.6...skills-catalog-ui`, eslint/build
results, and the computed preview URL
(`<pages_base_url>/branch-skills-catalog-ui/`). On OK:

```bash
git -C <fork> push -u origin skills-catalog-ui
```

- [ ] **Step 2: Wait for CI, confirm the preview**

Tell the owner to watch
`https://gitlab.cee.redhat.com/pedouble/rhoai/-/pipelines` (VPN). When
green, owner opens `<pages_base_url>/branch-skills-catalog-ui/` and
confirms it loads with the Skills page reachable. Record the fork commit
sha: `git -C <fork> rev-parse --short HEAD`. If the pipeline fails, fix
in the fork (eslint/build locally first), commit, push again -- the same
gate does not need to be re-asked for fix-up pushes to the same branch
within this task.

- [ ] **Step 3: Rewrite the hub prototype.yaml (v2)**

Replace `components/skills-catalog/prototype/skills-catalog-ui/prototype.yaml`
with (fill `<sha>` from Step 2, `<pages>` from prototype-fork.yaml,
today's date):

```yaml
title: Skills Catalog UI
description: Full skills catalog prototype -- browse (card grid with persona/category/pack facets and trust-tier toggle), skill detail (install commands, compatibility, README, register modal), and catalog source admin -- 63 EX public library skills across 7 packs, as React/PF6 pages in the UXD fork.
status: active
components: [skills-catalog]
source_repo: git@gitlab.cee.redhat.com:pedouble/rhoai.git
branch: skills-catalog-ui
base: upstream/3.6
preview_url: <pages>/branch-skills-catalog-ui/
current: v2
versions:
  v1: {timestamp: 2026-08-03, commit: static, summary: Static-era template-system build (retired 2026-08-05)}
  v2: {timestamp: <today>, commit: <sha>, summary: Migrated to the UXD fork -- React/PF6 browse + detail + admin with live preview}
```

- [ ] **Step 4: Delete the static version dir**

```bash
git rm -r components/skills-catalog/prototype/skills-catalog-ui/v1
```

- [ ] **Step 5: GATE — remove the manifest entry (unpublish)**

Per ruling R4 this is a disclosure decision through the hub.publish gate
pattern. Show the owner the entry being removed (publish/manifest.yaml
lines 104-108):

```yaml
- source: components/skills-catalog/prototype/skills-catalog-ui/v1/
  dest: skills-catalog/ui-prototype/
  audience: internal
  title: Skills Catalog UI Prototype
  description: Interactive skills catalog prototype — browse (card grid), skill detail (full page with tabs), and catalog admin (skills table, packs table, source configs) — populated with 68 EX public library skills across 7 packs.
```

plus the check `grep -rn "skills-catalog/ui-prototype" --include="*.md" --include="*.html" . | grep -v ".git/"`
(expected: only the manifest itself). On OK, delete those 5 lines. The
publish CI prunes the dest on the next run.

- [ ] **Step 6: Reindex, lint, commit (hub)**

```bash
python scripts/hub_index.py
python scripts/hub_lint.py
```

Expected: lint 0 errors; `views/prototypes.md` now links the live preview
URL with `branch: skills-catalog-ui`.

```bash
git add components/skills-catalog/prototype/skills-catalog-ui publish/manifest.yaml components/skills-catalog/index.md components/index.md views/prototypes.md
git commit -m "proto(skills-catalog): migrate skills-catalog-ui to the UXD fork (#16)

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>" -- components/skills-catalog/prototype/skills-catalog-ui publish/manifest.yaml components/skills-catalog/index.md components/index.md views/prototypes.md
```

(If `git status` shows other regenerated views changed, include exactly
those view files in the same commit -- still by explicit path.)

---

### Task 10: registry-ui ruling (GATED decision)

**Files:** depends on the ruling; listed per option below.

**Interfaces:**
- Consumes: the working pilot (Task 9), the reworked skill (Task 4).
- Produces: either the second migration or a recorded deferral; possibly
  the removal of the legacy schema path.

- [ ] **Step 1: GATE — present the decision**

Ask the owner (spec: "port vs. fresh rebuild decided at migration time"):

- **Option A — migrate now (fresh rebuild):** run the NEW hub.prototype
  CREATE flow for `mcp-registry` in this session (dogfooding Task 4's
  skill end to end: grounding -> planning -> fork branch `registry-ui`
  off upstream/3.6 -> verify -> gate -> push -> v2 metadata). The old
  static prototype is an MLflow-style mockup; a fresh grounded rebuild is
  the spec's lean. Then Steps 2-4 below.
- **Option B — defer:** registry-ui stays static and its PUBLIC manifest
  entry stays frozen (ruling R4 takes it down only when it migrates).
  Record the deferral: add a `## History` line to the skills-catalog
  migration summary in the Task 11 wrap-up and a comment on issue #16.
  The legacy schema path in `_lint_prototypes` and the indexer's local
  fallback REMAIN until it migrates. Skip Steps 2-4.

- [ ] **Step 2 (Option A only): public entry takedown**

Before removing, check inbound links:
`grep -rn "mcp-registry/ui-prototype" --include="*.md" --include="*.html" . | grep -v ".git/"`
Expected: only `publish/manifest.yaml`. If a published deck links it,
STOP and surface to the owner before proceeding. Then GATE: show the
manifest entry (lines 44-48, `dest: mcp-registry/ui-prototype/`,
audience public) and on OK delete it -- this takes down a PUBLIC URL.
Replace `components/mcp-registry/prototype/registry-ui/prototype.yaml`
with (fill `<sha>` from the fork commit, `<pages>` from
prototype-fork.yaml, `<today>`):

```yaml
title: MCP Registry UI Prototype
description: Registry list/detail/version UI with lifecycle governance -- rebuilt as React/PF6 pages in the UXD fork, grounded in current registry strategy (MLflow governance direction).
status: active
components: [mcp-registry]
source_repo: git@gitlab.cee.redhat.com:pedouble/rhoai.git
branch: registry-ui
base: upstream/3.6
preview_url: <pages>/branch-registry-ui/
current: v3
versions:
  v1: {timestamp: 2026-07-09, commit: static, summary: Static-era list/detail layout (retired)}
  v2: {timestamp: 2026-07-09, commit: static, summary: Static-era version comparison + policy badges (retired)}
  v3: {timestamp: <today>, commit: <sha>, summary: Fresh grounded rebuild in the UXD fork}
```

Then `git rm -r components/mcp-registry/prototype/registry-ui/v1
components/mcp-registry/prototype/registry-ui/v2`.

- [ ] **Step 3 (Option A only): remove the legacy schema path**

In `scripts/hublib/schema.py` `_lint_prototypes`: delete the `else:`
legacy branch (keep v2 as the only path; a missing `branch` key becomes
`missing required field 'branch'` via `PROTOTYPE_V2_REQUIRED`). In
`scripts/tests/test_schema.py`: delete
`test_prototype_legacy_still_validated` and update the 8 static-era
prototype tests to v2 fixtures (reuse `V2_YAML`). In
`scripts/hublib/indexer.py`: the `or f"/{sr}/{current}/index.html"`
fallbacks may remain (harmless) or be simplified -- if simplified, update
`test_prototypes_view_generated` to a v2 fixture too.

Run: `python -m pytest scripts/tests -v && python scripts/hub_lint.py`
Expected: PASS / 0 errors.

- [ ] **Step 4 (Option A only): reindex + commit**

```bash
python scripts/hub_index.py
git add components/mcp-registry/prototype/registry-ui publish/manifest.yaml scripts/hublib/schema.py scripts/hublib/indexer.py scripts/tests/test_schema.py scripts/tests/test_indexer.py components/mcp-registry/index.md components/index.md views/prototypes.md
git commit -m "proto(mcp-registry): migrate registry-ui to the UXD fork; retire legacy prototype schema (#16)

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>" -- components/mcp-registry/prototype/registry-ui publish/manifest.yaml scripts/hublib/schema.py scripts/hublib/indexer.py scripts/tests/test_schema.py scripts/tests/test_indexer.py components/mcp-registry/index.md components/index.md views/prototypes.md
```

---

### Task 11: Final verification + wrap-up

**Files:** none new -- verification and handoff.

- [ ] **Step 1: Hub verification trio**

```bash
python -m pytest scripts/tests -v
python scripts/hub_lint.py
python scripts/hub_index.py --check
```

Expected: all pass, 0 lint errors, 0 stale files.

- [ ] **Step 2: Reference sweep (final state)**

Run: `grep -rln "build_prototype\|extract_uxd_styles\|prototype-shell" --include="*.md" --include="*.py" --include="*.sh" --include="*.yaml" . | grep -v ".git/\|node_modules\|.scratch"`
Expected ONLY: the two superseded specs, the 2026-08-03 template plan,
`docs/enhancements-complete.md`, the 2026-08-04 spec, and this plan --
i.e. historical/spec documents. Nothing operative.

- [ ] **Step 3: Fork branch green**

Confirm with the owner: the `skills-catalog-ui` pipeline is green and the
preview URL loads (VPN). `views/prototypes.md` links it.

- [ ] **Step 4: Walk issue #16 acceptance criteria**

Check each against evidence and report to the owner:
spec with owner rulings (the 2026-08-04 spec, R1-R6) · repeatable fork
setup (doctor section 12 + setup.md) · hub.prototype produces a React/PF6
page passing lint+build (Tasks 7-8) · pushed branch yields a preview URL
recorded in prototype.yaml and views/prototypes.md (Task 9) · one static
prototype migrated end to end (Task 9) · disclosure boundary explicit
(spec R4 + docs/publishing.md) · static generation retired with no
dangling references (Tasks 5-6, Step 2 above).

- [ ] **Step 5: Hand back for the completion ceremony**

Do NOT run it autonomously: suggest the owner runs
`/hub.enhance complete 16` (moves the enhancements.md entry to
enhancements-complete.md, closes the issue, runs the docs-impact
checklist -- capabilities/skills/conventions were already updated in
Task 6; doctor/setup in Task 3).
