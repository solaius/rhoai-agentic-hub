# Jira Hub Skills Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship the Jira→hub pipeline per the approved spec at `/docs/specs/2026-07-09-jira-hub-skills-design.md` — a `hublib` Jira client (pm-toolkit port), a snapshot/diff module, the `hub_jira.py` CLI, the `hub.jira-sweep` + `hub.jira-sync` skills, an enriched `views/jira-map.md`, and a doctor probe — closing backlog #2.

**Architecture:** All-new files except three surgical touches (`schema.py`, `indexer.py`, `doctor.sh`) and doc edits. The client (`hublib/jira.py`, httpx, async) is read from Jira only; repo writes happen in the skills, gated. Tracked per-feature snapshots (`features/<id>/work/jira-snapshot.yaml`) carry whitelisted fields only, with summaries admitted by the unauthenticated-probe rule; `views/jira-map.md` regenerates deterministically from tracked files, so CI needs no credentials.

**Tech Stack:** Python 3.11+, httpx (NEW dependency, deliberate — spec decision 1), pyyaml, pytest (offline via `httpx.MockTransport`), bash (doctor), markdown skill procedures.

## Global Constraints

- **Precondition — both in-flight plans have landed.** Before Task 1, verify: `test -f scripts/hublib/disclosure.py && test -f .claude/skills/hub.intake/SKILL.md && echo ready` prints `ready`. If not, STOP — the enhancement batch and intake/research plans edit `schema.py`, `indexer.py`, `test_indexer.py`, and `doctor.sh`, and this plan's anchors assume their final state.
- This repo is **PUBLIC**: no customer names, deal context, dollar figures, or agreement language in any tracked file, code, test fixture, or commit message. Test fixtures use `X-1` / `RHOAIENG-…` style keys and neutral summaries.
- `httpx>=0.28` is the ONLY new dependency this plan may add. No pytest-asyncio — async tests wrap coroutines in `asyncio.run()`.
- Findings contract: lint findings are strings `"<relpath>: <message>"`; functions return `(errors, warnings)` tuples, matching `schema.lint_repo`.
- File writes: always `encoding="utf-8", newline="\n"`.
- After every task: `python scripts/hub_lint.py` reports **0 errors** and the warning count has not increased over the pre-task baseline (record the baseline before Task 1); `python scripts/hub_index.py --check` reports 0 stale files.
- Never hand-edit generated files (`views/*`, `*/index.md`, `memory/index.md`) — run `python scripts/hub_index.py` and commit its output with the change that staled it.
- `AGENTS.md` has a hard 150-line CI budget.
- Markdown links use leading-slash repo-root form (`/docs/specs/...`).
- The skills are **read-only against Jira** — nothing in this plan calls the client's write methods.
- Never print `JIRA_TOKEN` (or any secret) in CLI output, logs, tests, or commits.
- Tests run from the repo root: `python -m pytest scripts/tests -v` (conftest.py puts `scripts/` on `sys.path`).
- Run all commands from the repo root: `C:\Users\peter\code\rh\rhoai-agentic-hub` (POSIX `/c/Users/peter/code/rh/rhoai-agentic-hub`). Windows + Git Bash.
- Every commit message ends with `Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>`.

---

### Task 1: The Jira client — `hublib/jira.py` (pm-toolkit port) + httpx

**Files:**
- Modify: `scripts/requirements.txt`
- Create: `scripts/hublib/jira.py` (copied from `C:/Users/peter/code/rh/pm-toolkit/scripts/clients/jira.py`, then edited)
- Test: `scripts/tests/test_jira.py`

**Interfaces:**
- Consumes: nothing (first task).
- Produces: `hublib.jira.JiraClient` (async context manager; `search(jql, fields=None, max_results=200) -> list[dict]`, `get_issue(key, fields=None) -> dict`, `myself() -> dict`, plus ported write methods unused by this plan); `hublib.jira.client_from_env(transport=None) -> JiraClient` (hub env names `JIRA_SERVER`/`JIRA_USER`/`JIRA_TOKEN`); `hublib.jira.probe_public(base_url, keys, max_concurrent=5, transport=None) -> set[str]`; `hublib.jira.adf_to_text(node) -> str`; module constant `RETRY_BASE_DELAY`. Tasks 5 and 7 rely on these exact names.

- [ ] **Step 1: Add the dependency and install it**

In `scripts/requirements.txt` replace:

```
pyyaml>=6.0
pytest>=8.0
```

with:

```
pyyaml>=6.0
pytest>=8.0
httpx>=0.28
```

Run: `pip install -r scripts/requirements.txt`
Expected: httpx installs (or is already satisfied); exit 0.

- [ ] **Step 2: Write the failing tests**

Create `scripts/tests/test_jira.py`:

```python
import asyncio

import httpx
import pytest

from hublib import jira
from hublib.jira import JiraClient, adf_to_text, client_from_env, probe_public


def run(coro):
    return asyncio.run(coro)


def test_client_from_env_requires_server(monkeypatch):
    monkeypatch.delenv("JIRA_SERVER", raising=False)
    with pytest.raises(RuntimeError):
        client_from_env()


def test_client_from_env_basic_auth_when_user_set(monkeypatch):
    monkeypatch.setenv("JIRA_SERVER", "https://jira.example.com")
    monkeypatch.setenv("JIRA_USER", "user@example.com")
    monkeypatch.setenv("JIRA_TOKEN", "tok")
    seen = {}

    def handler(request):
        seen["auth"] = request.headers.get("authorization", "")
        return httpx.Response(200, json={"displayName": "U"})

    async def case():
        async with client_from_env(transport=httpx.MockTransport(handler)) as client:
            await client.myself()

    run(case())
    assert seen["auth"].startswith("Basic ")


def test_client_from_env_bearer_when_no_user(monkeypatch):
    monkeypatch.setenv("JIRA_SERVER", "https://jira.example.com")
    monkeypatch.delenv("JIRA_USER", raising=False)
    monkeypatch.setenv("JIRA_TOKEN", "pat")
    seen = {}

    def handler(request):
        seen["auth"] = request.headers.get("authorization", "")
        return httpx.Response(200, json={})

    async def case():
        async with client_from_env(transport=httpx.MockTransport(handler)) as client:
            await client.myself()

    run(case())
    assert seen["auth"] == "Bearer pat"


def test_search_paginates_with_next_page_token():
    calls = []

    def handler(request):
        calls.append(str(request.url))
        if "nextPageToken=t2" in str(request.url):
            return httpx.Response(200, json={"issues": [{"key": "X-2"}], "isLast": True})
        return httpx.Response(200, json={
            "issues": [{"key": "X-1"}], "isLast": False, "nextPageToken": "t2"})

    async def case():
        async with JiraClient("https://jira.example.com", personal_token="p",
                              transport=httpx.MockTransport(handler)) as client:
            return await client.search("project = X")

    issues = run(case())
    assert [i["key"] for i in issues] == ["X-1", "X-2"]
    assert len(calls) == 2


def test_429_retries_then_succeeds(monkeypatch):
    monkeypatch.setattr(jira, "RETRY_BASE_DELAY", 0.0)
    state = {"n": 0}

    def handler(request):
        state["n"] += 1
        if state["n"] == 1:
            return httpx.Response(429, headers={"Retry-After": "0"})
        return httpx.Response(200, json={"issues": [], "isLast": True})

    async def case():
        async with JiraClient("https://jira.example.com", personal_token="p",
                              transport=httpx.MockTransport(handler)) as client:
            return await client.search("project = X")

    assert run(case()) == []
    assert state["n"] == 2


def test_adf_to_text_nested_doc():
    doc = {"type": "doc", "version": 1, "content": [
        {"type": "heading", "attrs": {"level": 1},
         "content": [{"type": "text", "text": "Title"}]},
        {"type": "paragraph", "content": [{"type": "text", "text": "Body"}]},
        {"type": "bulletList", "content": [
            {"type": "listItem", "content": [
                {"type": "paragraph",
                 "content": [{"type": "text", "text": "item"}]}]}]},
    ]}
    assert adf_to_text(doc) == "Title\nBody\n- item"
    assert adf_to_text("already plain") == "already plain"
    assert adf_to_text(None) == ""


def test_probe_public_fail_closed():
    def handler(request):
        assert "authorization" not in request.headers  # probe must carry no auth
        if "PUB-1" in str(request.url):
            return httpx.Response(200, json={"fields": {"summary": "s"}})
        return httpx.Response(401)

    got = run(probe_public("https://jira.example.com", ["PUB-1", "PRIV-2"],
                           transport=httpx.MockTransport(handler)))
    assert got == {"PUB-1"}
```

- [ ] **Step 3: Run tests to verify they fail**

Run: `python -m pytest scripts/tests/test_jira.py -v`
Expected: collection ERROR — `ModuleNotFoundError: No module named 'hublib.jira'`.

- [ ] **Step 4: Copy the pm-toolkit client**

```bash
cp "C:/Users/peter/code/rh/pm-toolkit/scripts/clients/jira.py" scripts/hublib/jira.py
wc -l scripts/hublib/jira.py
```

Expected: `481 scripts/hublib/jira.py`. (If the sibling repo is unreadable from your sandbox, ask the operator to run the `cp` — do not retype the file.)

- [ ] **Step 5: Apply the port edits**

Five exact edits to `scripts/hublib/jira.py`:

(a) Replace the module docstring:

```python
"""Thin async Jira REST API client for structured data fetching.
```

with:

```python
"""Thin async Jira REST API client (ported 2026-07-09 from pm-toolkit
scripts/clients/jira.py; spec /docs/specs/2026-07-09-jira-hub-skills-design.md).
Write methods are ported for future backlog items (#30, write-back) — the
hub.jira-* skills are read-only against Jira.
```

(b) Drop the pm-toolkit path shim — replace:

```python
import httpx

import scripts._base  # noqa: F401

logger = logging.getLogger(__name__)
```

with:

```python
import httpx

logger = logging.getLogger(__name__)
```

(c) Add the `os` import — replace:

```python
import asyncio
import logging
import re
```

with:

```python
import asyncio
import logging
import os
import re
```

(d) Add transport injection for offline tests — replace:

```python
        max_concurrent: int = 3,
    ) -> None:
```

with:

```python
        max_concurrent: int = 3,
        transport: httpx.AsyncBaseTransport | None = None,
    ) -> None:
```

and replace:

```python
        self._client = httpx.AsyncClient(
            base_url=self.base_url,
            headers=headers,
            auth=self._auth,
            timeout=30.0,
        )
```

with:

```python
        self._client = httpx.AsyncClient(
            base_url=self.base_url,
            headers=headers,
            auth=self._auth,
            timeout=30.0,
            transport=transport,
        )
```

(e) Add `myself()` — replace:

```python
    # -- Lifecycle --

    async def close(self) -> None:
```

with:

```python
    # -- Identity --

    async def myself(self) -> dict:
        """Fetch the authenticated user — the connectivity/auth probe."""
        resp = await self._request("GET", "/rest/api/2/myself")
        resp.raise_for_status()
        return resp.json()

    # -- Lifecycle --

    async def close(self) -> None:
```

Then append at the end of the file:

```python


async def probe_public(
    base_url: str,
    keys: list[str],
    max_concurrent: int = 5,
    transport: httpx.AsyncBaseTransport | None = None,
) -> set[str]:
    """Return the subset of issue keys that are anonymously readable —
    an UNAUTHENTICATED request per key; HTTP 200 means Jira itself serves
    the issue to the world. Fail-closed: any non-200 or network error
    means 'not public'. Gates which summaries may enter tracked files."""
    sem = asyncio.Semaphore(max_concurrent)
    public: set[str] = set()
    async with httpx.AsyncClient(base_url=base_url.rstrip("/"), timeout=15.0,
                                 transport=transport) as client:
        async def one(key: str) -> None:
            async with sem:
                try:
                    resp = await client.get(f"/rest/api/2/issue/{key}",
                                            params={"fields": "summary"})
                except httpx.HTTPError:
                    return
                if resp.status_code == 200:
                    public.add(key)

        await asyncio.gather(*(one(k) for k in keys))
    return public


def client_from_env(
    transport: httpx.AsyncBaseTransport | None = None,
) -> JiraClient:
    """JiraClient from the hub's env names (restricted/.env; doctor section 4).

    JIRA_SERVER + JIRA_USER + JIRA_TOKEN -> Cloud basic auth;
    JIRA_SERVER + JIRA_TOKEN alone -> Data Center bearer.
    """
    url = os.environ.get("JIRA_SERVER", "")
    if not url:
        raise RuntimeError(
            "JIRA_SERVER not set — export restricted/.env into this shell, "
            "or diagnose with: bash scripts/doctor.sh check (section 4)")
    user = os.environ.get("JIRA_USER", "")
    token = os.environ.get("JIRA_TOKEN", "")
    if user:
        return JiraClient(url, username=user, api_token=token,
                          max_concurrent=5, transport=transport)
    return JiraClient(url, personal_token=token, max_concurrent=5,
                      transport=transport)
```

- [ ] **Step 6: Run tests to verify they pass**

Run: `python -m pytest scripts/tests/test_jira.py -v`
Expected: 7 PASS.

- [ ] **Step 7: Full suite + real-repo lint**

Run: `python -m pytest scripts/tests -v && python scripts/hub_lint.py && python scripts/hub_index.py --check`
Expected: all PASS; `0 error(s)` with the baseline warning count; `0 stale file(s)`.

- [ ] **Step 8: Commit**

```bash
git add scripts/requirements.txt scripts/hublib/jira.py scripts/tests/test_jira.py
git commit -m "feat(jira): hublib Jira client — pm-toolkit port + probe_public + hub env mapping (#2)

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

### Task 2: Snapshot contract — `hublib/jiramap.py`

**Files:**
- Create: `scripts/hublib/jiramap.py`
- Test: `scripts/tests/test_jiramap.py`

**Interfaces:**
- Consumes: `hublib.frontmatter.load_file` / `FrontmatterError`.
- Produces (Tasks 3, 4, 5 rely on these exact names): `MARKER: str` (the snapshot's first line), `FIELDS: tuple` (whitelist, in order), `issue_row(issue: dict, public: bool) -> dict`, `build_snapshot(feature_id, jql, rows, swept) -> str` (byte-stable YAML text), `load_all(root) -> list[tuple[str, dict]]`, `validate(root) -> (errors, warnings)`, `diff(old_rows, new_rows) -> dict` (keys `new`/`vanished`/`changed`), `watched_keys(root) -> dict[str, list[str]]`.

- [ ] **Step 1: Write the failing tests**

Create `scripts/tests/test_jiramap.py`:

```python
from pathlib import Path

from hublib.jiramap import (FIELDS, MARKER, build_snapshot, diff, issue_row,
                            load_all, validate, watched_keys)


def write(root: Path, rel: str, text: str):
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8", newline="\n")
    return p


ISSUE_A = {"key": "X-2", "fields": {
    "summary": "Public issue", "issuetype": {"name": "Feature"},
    "status": {"name": "In Progress"}, "resolution": None,
    "fixVersions": [{"name": "RHOAI 3.5"}],
    "updated": "2026-07-08T12:00:00.000+0000"}}
ISSUE_B = {"key": "X-10", "fields": {
    "summary": "Private issue", "issuetype": {"name": "Bug"},
    "status": {"name": "New"}, "resolution": {"name": "Done"},
    "fixVersions": [], "updated": "2026-07-01T09:00:00.000+0000"}}


def test_issue_row_whitelists_and_redacts():
    row = issue_row(ISSUE_A, public=True)
    assert tuple(row) == FIELDS
    assert row["summary"] == "Public issue"
    assert row["fix_versions"] == ["RHOAI 3.5"]
    assert row["updated"] == "2026-07-08"
    assert issue_row(ISSUE_B, public=False)["summary"] is None


def test_build_snapshot_byte_stable_numeric_key_order():
    rows = [issue_row(ISSUE_B, False), issue_row(ISSUE_A, True)]
    one = build_snapshot("x", "project = X", rows, "2026-07-09")
    two = build_snapshot("x", "project = X", list(reversed(rows)), "2026-07-09")
    assert one == two
    assert one.splitlines()[0] == MARKER
    assert one.index("X-2") < one.index("X-10")  # numeric, not lexicographic


def test_validate_ok_and_load_all(tmp_path):
    text = build_snapshot("x", "project = X", [issue_row(ISSUE_A, True)], "2026-07-09")
    write(tmp_path, "features/x/work/jira-snapshot.yaml", text)
    errors, warnings = validate(tmp_path)
    assert errors == [] and warnings == []
    [(fid, data)] = load_all(tmp_path)
    assert fid == "x" and data["issues"][0]["key"] == "X-2"


def test_validate_missing_marker_is_error(tmp_path):
    write(tmp_path, "features/x/work/jira-snapshot.yaml",
          "feature: x\njql: q\nswept: 2026-07-09\nissues: []\n")
    errors, _ = validate(tmp_path)
    assert any("missing generated-file marker" in e for e in errors)


def test_validate_feature_dir_mismatch_is_error(tmp_path):
    text = build_snapshot("y", "project = X", [], "2026-07-09")
    write(tmp_path, "features/x/work/jira-snapshot.yaml", text)
    errors, _ = validate(tmp_path)
    assert any("feature 'y' does not match its directory 'x'" in e for e in errors)


def test_validate_bad_yaml_and_bad_row(tmp_path):
    write(tmp_path, "features/x/work/jira-snapshot.yaml", MARKER + "\n{unclosed\n")
    errors, _ = validate(tmp_path)
    assert any("invalid YAML" in e for e in errors)
    write(tmp_path, "features/x/work/jira-snapshot.yaml",
          MARKER + "\nfeature: x\njql: q\nswept: 2026-07-09\nissues:\n- type: Bug\n")
    errors, _ = validate(tmp_path)
    assert any("issue row 0 missing 'key'" in e for e in errors)


def test_diff_changed_new_vanished():
    old = [issue_row(ISSUE_A, True), issue_row(ISSUE_B, False)]
    changed_a = dict(issue_row(ISSUE_A, True), status="Closed")
    new_c = dict(issue_row(ISSUE_A, True), key="X-30")
    d = diff(old, [changed_a, new_c])
    assert [r["key"] for r in d["new"]] == ["X-30"]
    assert [r["key"] for r in d["vanished"]] == ["X-10"]
    assert d["changed"] == [{"key": "X-2",
                             "changes": {"status": ("In Progress", "Closed")}}]


def test_watched_keys_refs_and_jtbd(tmp_path):
    write(tmp_path, "features/x/knowledge/ref-a.md",
          "---\ntype: reference\ndescription: d\ntimestamp: 2026-07-09\n"
          "resource: https://redhat.atlassian.net/browse/RHAISTRAT-1345\n---\nb\n")
    write(tmp_path, "narrative/knowledge/jtbd-b.md",
          "---\ntype: jtbd\ndescription: d\ntimestamp: 2026-07-09\n"
          "persona: rhoai-admin\nstatus: candidate\n"
          "jira: [RHOAIENG-7, RHAISTRAT-1345]\n---\nb\n")
    watched = watched_keys(tmp_path)
    assert set(watched) == {"RHAISTRAT-1345", "RHOAIENG-7"}
    assert len(watched["RHAISTRAT-1345"]) == 2
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python -m pytest scripts/tests/test_jiramap.py -v`
Expected: collection ERROR — `No module named 'hublib.jiramap'`.

- [ ] **Step 3: Implement** — create `scripts/hublib/jiramap.py`:

```python
"""The Jira snapshot contract (spec /docs/specs/2026-07-09-jira-hub-skills-design.md):
whitelisted rows, byte-stable YAML, lint validation, sync diffing, and the
ref-/jtbd watched-key scan. Snapshots are machine-written by hub.jira-sweep
into features/<id>/work/jira-snapshot.yaml — tracked, public, never
hand-edited. Only FIELDS ever enter a snapshot; summaries only when the
unauthenticated probe proved the issue world-readable."""
import re
from pathlib import Path

import yaml

from . import frontmatter

MARKER = "# generated by hub.jira-sweep (scripts/hub_jira.py) — do not hand-edit"
SNAPSHOT_GLOB = "features/*/work/jira-snapshot.yaml"
FIELDS = ("key", "type", "status", "resolution", "fix_versions", "updated", "summary")
JIRA_BROWSE_RE = re.compile(
    r"^https://redhat\.atlassian\.net/browse/([A-Z][A-Z0-9]*-\d+)$")


def _key_sort(key):
    proj, _, num = str(key).rpartition("-")
    return (proj, int(num) if num.isdigit() else 0)


def issue_row(issue, public):
    """Whitelist one raw API issue into a snapshot row. `public` comes from
    jira.probe_public — a redacted summary is None, never elided."""
    f = issue.get("fields", {})
    return {
        "key": issue.get("key", ""),
        "type": (f.get("issuetype") or {}).get("name", ""),
        "status": (f.get("status") or {}).get("name", ""),
        "resolution": (f.get("resolution") or {}).get("name"),
        "fix_versions": [v.get("name", "") for v in (f.get("fixVersions") or [])],
        "updated": str(f.get("updated") or "")[:10] or None,
        "summary": (f.get("summary") or "") if public else None,
    }


def build_snapshot(feature_id, jql, rows, swept):
    """Byte-stable snapshot text: same rows -> identical bytes, so diffs are
    reviewable and the jira-map view regenerates deterministically."""
    data = {
        "feature": feature_id,
        "jql": jql,
        "swept": swept,
        "issues": sorted(rows, key=lambda r: _key_sort(r.get("key", ""))),
    }
    return MARKER + "\n" + yaml.safe_dump(
        data, sort_keys=False, allow_unicode=True, default_flow_style=False)


def load_all(root):
    """[(feature_id, data)] for every parseable snapshot, sorted by path.
    Permissive — lint (validate) is where breakage is reported."""
    out = []
    for snap in sorted(Path(root).glob(SNAPSHOT_GLOB)):
        try:
            data = yaml.safe_load(snap.read_text(encoding="utf-8"))
        except yaml.YAMLError:
            continue
        if isinstance(data, dict) and isinstance(data.get("issues"), list):
            out.append((snap.parent.parent.name, data))
    return out


def validate(root):
    """Lint every tracked snapshot. Structural problems are errors — a broken
    snapshot means a broken sweep or a hand edit, and both must fail CI."""
    root = Path(root)
    errors, warnings = [], []
    for snap in sorted(root.glob(SNAPSHOT_GLOB)):
        rel = snap.relative_to(root).as_posix()
        text = snap.read_text(encoding="utf-8")
        if (text.splitlines() or [""])[0] != MARKER:
            errors.append(f"{rel}: missing generated-file marker (snapshots are "
                          f"machine-written by hub.jira-sweep — never by hand)")
        try:
            data = yaml.safe_load(text)
        except yaml.YAMLError as exc:
            errors.append(f"{rel}: invalid YAML: {exc}")
            continue
        if not isinstance(data, dict):
            errors.append(f"{rel}: snapshot must be a mapping")
            continue
        fid = snap.parent.parent.name
        if data.get("feature") != fid:
            errors.append(f"{rel}: feature '{data.get('feature')}' does not match "
                          f"its directory '{fid}'")
        for field in ("jql", "swept"):
            if not data.get(field):
                errors.append(f"{rel}: missing '{field}'")
        issues = data.get("issues")
        if not isinstance(issues, list):
            errors.append(f"{rel}: 'issues' must be a list")
            continue
        for i, row in enumerate(issues):
            if not isinstance(row, dict):
                errors.append(f"{rel}: issue row {i} must be a mapping")
                continue
            for field in ("key", "type", "status"):
                if not row.get(field):
                    errors.append(f"{rel}: issue row {i} missing '{field}'")
    return errors, warnings


def diff(old_rows, new_rows):
    """Pure set/field comparison between two row lists. Returns
    {'new': [rows], 'vanished': [rows], 'changed': [{'key', 'changes'}]}
    where changes maps field -> (old, new)."""
    old = {r["key"]: r for r in old_rows if r.get("key")}
    new = {r["key"]: r for r in new_rows if r.get("key")}
    changed = []
    for key in sorted(old.keys() & new.keys(), key=_key_sort):
        deltas = {f: (old[key].get(f), new[key].get(f))
                  for f in FIELDS if f != "key" and old[key].get(f) != new[key].get(f)}
        if deltas:
            changed.append({"key": key, "changes": deltas})
    return {
        "new": [new[k] for k in sorted(new.keys() - old.keys(), key=_key_sort)],
        "vanished": [old[k] for k in sorted(old.keys() - new.keys(), key=_key_sort)],
        "changed": changed,
    }


def watched_keys(root):
    """Jira keys referenced by tracked entries — ref- resource: URLs and jtbd
    jira: lists — mapped to the rootpaths that reference them. hub.jira-sync
    watches these even outside every stored JQL scope, so refs never
    silently rot."""
    root = Path(root)
    watched = {}

    def scan(glob, base):
        basedir = root / base
        if not basedir.is_dir():
            return
        for entry in sorted(basedir.glob(glob)):
            if not entry.is_file():
                continue
            try:
                meta, _ = frontmatter.load_file(entry)
            except frontmatter.FrontmatterError:
                continue
            rp = "/" + entry.relative_to(root).as_posix()
            keys = []
            m = JIRA_BROWSE_RE.match(str(meta.get("resource", "")))
            if m:
                keys.append(m.group(1))
            if meta.get("type") == "jtbd" and isinstance(meta.get("jira"), list):
                keys.extend(k for k in meta["jira"] if isinstance(k, str))
            for k in keys:
                watched.setdefault(k, []).append(rp)

    scan("*/knowledge/*.md", "features")
    scan("knowledge/*.md", "narrative")
    return watched
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `python -m pytest scripts/tests/test_jiramap.py -v`
Expected: 8 PASS.

- [ ] **Step 5: Commit**

```bash
git add scripts/hublib/jiramap.py scripts/tests/test_jiramap.py
git commit -m "feat(jira): jiramap — snapshot whitelist/build/validate/diff + watched keys (#2)

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

### Task 3: Lint wiring — snapshot validation + jtbd `jira:` shape

**Files:**
- Modify: `scripts/hublib/schema.py` (import line; jtbd block inside `lint_entry`; `lint_repo`)
- Test: `scripts/tests/test_schema.py` (append)

**Interfaces:**
- Consumes: `jiramap.validate(root) -> (errors, warnings)` (Task 2).
- Produces: `lint_repo` findings covering snapshots and jtbd `jira:` lists — Task 8's docs describe them; CI enforces them.

- [ ] **Step 1: Write the failing tests** — append to `scripts/tests/test_schema.py`:

```python
def test_jtbd_jira_list_of_keys_ok(tmp_path):
    root = make_repo(tmp_path)
    write(root, "features/x/knowledge/jtbd-a.md",
          ENTRY.format(t="jtbd", extra="persona: rhoai-admin\nstatus: candidate\n"
                                       "jira: [RHOAIENG-1234, RHAISTRAT-9]\n"))
    errors, _ = lint_repo(root)
    assert errors == []


def test_jtbd_jira_not_a_list_is_error(tmp_path):
    root = make_repo(tmp_path)
    write(root, "features/x/knowledge/jtbd-a.md",
          ENTRY.format(t="jtbd", extra="persona: rhoai-admin\nstatus: candidate\n"
                                       "jira: RHOAIENG-1234\n"))
    errors, _ = lint_repo(root)
    assert any("jira must be a list of issue keys" in e for e in errors)


def test_jtbd_jira_malformed_key_is_error(tmp_path):
    root = make_repo(tmp_path)
    write(root, "features/x/knowledge/jtbd-a.md",
          ENTRY.format(t="jtbd", extra="persona: rhoai-admin\nstatus: candidate\n"
                                       "jira: [not-a-key]\n"))
    errors, _ = lint_repo(root)
    assert any("jira must be a list of issue keys" in e for e in errors)


def test_snapshot_lint_wired_into_lint_repo(tmp_path):
    root = make_repo(tmp_path)
    write(root, "features/x/work/jira-snapshot.yaml", "feature: x\nissues: []\n")
    errors, _ = lint_repo(root)
    assert any("missing generated-file marker" in e for e in errors)
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python -m pytest scripts/tests/test_schema.py -v -k "jtbd_jira or snapshot_lint"`
Expected: `test_jtbd_jira_not_a_list_is_error`, `test_jtbd_jira_malformed_key_is_error`, and `test_snapshot_lint_wired_into_lint_repo` FAIL (no such findings yet); `test_jtbd_jira_list_of_keys_ok` passes vacuously.

- [ ] **Step 3: Implement** — three exact edits to `scripts/hublib/schema.py`:

(a) Replace the import line:

```python
from . import frontmatter
```

with:

```python
from . import frontmatter, jiramap
```

(`jiramap` imports only stdlib, yaml, and `frontmatter` — no cycle.)

(b) In `lint_entry`, directly after the persona block:

```python
    if etype == "jtbd" and meta.get("persona") is not None:
        if str(meta["persona"]) not in PERSONAS:
            errors.append(f"{rel}: persona must be one of {'|'.join(PERSONAS)}")
```

insert:

```python
    if etype == "jtbd" and meta.get("jira") is not None:
        keys = meta["jira"]
        if not isinstance(keys, list) or not all(
                isinstance(k, str) and re.match(r"^[A-Z][A-Z0-9]*-\d+$", k)
                for k in keys):
            errors.append(f"{rel}: jira must be a list of issue keys "
                          f"(e.g. [RHOAIENG-1234]) — watched by hub.jira-sync")
```

(c) In `lint_repo`, replace:

```python
    _lint_budgets(root, errors)
```

with:

```python
    snap_errors, snap_warnings = jiramap.validate(root)
    errors.extend(snap_errors)
    warnings.extend(snap_warnings)
    _lint_budgets(root, errors)
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `python -m pytest scripts/tests/test_schema.py -v`
Expected: all PASS (including every pre-existing test).

- [ ] **Step 5: Full suite + real-repo lint**

Run: `python -m pytest scripts/tests -v && python scripts/hub_lint.py`
Expected: all PASS; `0 error(s)`, warning count unchanged (the repo has no snapshots or jtbd `jira:` lists yet).

- [ ] **Step 6: Commit**

```bash
git add scripts/hublib/schema.py scripts/tests/test_schema.py
git commit -m "feat(lint): snapshot validation + jtbd jira: key-list shape (#2)

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

### Task 4: The enriched `views/jira-map.md`

**Files:**
- Modify: `scripts/hublib/indexer.py` (import line; the jira-map block inside `build_all`)
- Test: `scripts/tests/test_indexer.py` (append)
- Regenerate: `views/jira-map.md` (via `python scripts/hub_index.py`)

**Interfaces:**
- Consumes: `jiramap.load_all(root)` (Task 2).
- Produces: the two-part view — per-feature snapshot sections plus a `## Referenced elsewhere` section preserving today's behavior for refs without snapshot coverage.

- [ ] **Step 1: Write the failing tests** — append to `scripts/tests/test_indexer.py`:

```python
SNAP = """# generated by hub.jira-sweep (scripts/hub_jira.py) — do not hand-edit
feature: mcp-registry
jql: project = X
swept: 2026-07-05
issues:
- key: RHAIRFE-1370
  type: Feature
  status: In Progress
  resolution: null
  fix_versions: [RHOAI 3.5]
  updated: 2026-07-01
  summary: Epic summary
- key: RHAIRFE-2000
  type: Feature
  status: New
  resolution: null
  fix_versions: []
  updated: 2026-07-02
  summary: null
"""


def test_jira_map_merges_snapshot_and_refs(tmp_path):
    root = make_repo(tmp_path)
    write(root, "features/mcp-registry/work/jira-snapshot.yaml", SNAP)
    view = build_all(root, today=TODAY)["views/jira-map.md"]
    assert "## mcp-registry" in view
    # make_repo already files ref-epic.md for RHAIRFE-1370 — row links to it
    assert "RHAIRFE-1370 · Feature · In Progress · RHOAI 3.5 — Epic summary" in view
    assert "→ [Main epic](" in view
    assert "(/features/mcp-registry/knowledge/ref-epic.md)" in view
    assert "withheld" in view                      # redacted-summary row
    assert "## Referenced elsewhere" not in view   # the only ref is covered


def test_jira_map_refs_without_snapshots_keep_working(tmp_path):
    view = build_all(make_repo(tmp_path), today=TODAY)["views/jira-map.md"]
    assert "## Referenced elsewhere" in view
    assert "RHAIRFE-1370" in view
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python -m pytest scripts/tests/test_indexer.py -v -k jira_map`
Expected: both FAIL (old flat-list view has neither `## mcp-registry` nor `## Referenced elsewhere`). The pre-existing `test_views_content` assertion on `RHAIRFE-1370` still passes.

- [ ] **Step 3: Implement** — two exact edits to `scripts/hublib/indexer.py`:

(a) Replace the import line:

```python
from . import frontmatter
```

with:

```python
from . import frontmatter, jiramap
```

(b) Replace the jira-map block inside `build_all`:

```python
    jira = URI_PATTERNS["redhat.atlassian.net"]
    rows = []
    for rp, m, _ in entries:
        res = str(m.get("resource", ""))
        if jira.match(res):
            rows.append(f"- {res.rsplit('/', 1)[-1]} → [{_title(m, rp)}]({rp})")
    built["views/jira-map.md"] = "\n".join([MARKER + "# Jira map", ""] + sorted(rows)) + "\n"
```

with:

```python
    jira_pat = URI_PATTERNS["redhat.atlassian.net"]
    ref_by_key = {}
    for rp, m, _ in entries:
        res = str(m.get("resource", ""))
        if jira_pat.match(res):
            ref_by_key[res.rsplit("/", 1)[-1]] = (rp, m)
    lines = [MARKER + "# Jira map", ""]
    covered = set()
    for fid, snap in jiramap.load_all(root):
        lines.append(f"## {fid}")
        lines.append(f"_swept {snap.get('swept', '?')} · `{snap.get('jql', '')}`_")
        lines.append("")
        for row in snap.get("issues", []):
            key = str(row.get("key", "?"))
            covered.add(key)
            fixes = ", ".join(row.get("fix_versions") or []) or "—"
            summary = row.get("summary") or "_(summary withheld — not anonymously readable)_"
            line = (f"- {key} · {row.get('type', '')} · {row.get('status', '')} · "
                    f"{fixes} — {summary}")
            if key in ref_by_key:
                rp, m = ref_by_key[key]
                line += f" → [{_title(m, rp)}]({rp})"
            lines.append(line)
        lines.append("")
    extras = sorted(f"- {key} → [{_title(m, rp)}]({rp})"
                    for key, (rp, m) in ref_by_key.items() if key not in covered)
    if extras:
        lines.append("## Referenced elsewhere")
        lines.extend(extras)
    built["views/jira-map.md"] = "\n".join(lines).rstrip() + "\n"
```

- [ ] **Step 4: Run the indexer suite**

Run: `python -m pytest scripts/tests/test_indexer.py -v`
Expected: all PASS (the new tests and every pre-existing one).

- [ ] **Step 5: Regenerate real views and verify**

Run: `python scripts/hub_index.py && python scripts/hub_index.py --check && python scripts/hub_lint.py`
Expected: `WROTE views/jira-map.md` (RHAISTRAT-1345 now sits under `## Referenced elsewhere` — no snapshots exist yet); `0 stale file(s)`; `0 error(s)`.

- [ ] **Step 6: Commit (include the regenerated view)**

```bash
git add scripts/hublib/indexer.py scripts/tests/test_indexer.py views/jira-map.md
git commit -m "feat(views): jira-map — per-feature snapshot sections + referenced-elsewhere refs (#2)

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

### Task 5: The CLI — `scripts/hub_jira.py`

**Files:**
- Create: `scripts/hub_jira.py`
- Test: `scripts/tests/test_hub_jira.py`

**Interfaces:**
- Consumes: `hublib.jira.client_from_env/probe_public/adf_to_text` (Task 1), `hublib.jiramap` (Task 2), the optional `jira:` block on `features/features.yaml` entries (`{jql: str, ref_types: [str]}`).
- Produces: the four modes the skills (Task 6) and doctor (Task 7) invoke: `--check` · `--try-jql '<jql>' [--sample N]` · `--sweep <feature> [--jql '<jql>'] --out DIR` · `--sync [<feature>] --out DIR`. `main(argv=None) -> int`. Proposal files land ONLY in `--out` (scratch) — the CLI never writes into the repo.

- [ ] **Step 1: Write the failing tests**

Create `scripts/tests/test_hub_jira.py`:

```python
from pathlib import Path

import pytest

import hub_jira


def write(root: Path, rel: str, text: str):
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8", newline="\n")
    return p


def make_repo(tmp_path: Path) -> Path:
    write(tmp_path, "features/features.yaml",
          "features:\n- id: mcp-registry\n  title: R\n  description: d\n")
    return tmp_path


def test_exactly_one_mode_required(tmp_path):
    with pytest.raises(SystemExit):
        hub_jira.main(["--check", "--sync"])
    with pytest.raises(SystemExit):
        hub_jira.main([])


def test_out_required_for_sweep(tmp_path):
    with pytest.raises(SystemExit):
        hub_jira.main(["--sweep", "mcp-registry", "--root", str(make_repo(tmp_path))])


def test_sweep_unknown_feature_exits_2(tmp_path, capsys):
    rc = hub_jira.main(["--sweep", "nope", "--out", str(tmp_path / "o"),
                        "--root", str(make_repo(tmp_path))])
    assert rc == 2
    assert "unknown feature" in capsys.readouterr().out


def test_sweep_without_stored_scope_exits_2(tmp_path, capsys):
    rc = hub_jira.main(["--sweep", "mcp-registry", "--out", str(tmp_path / "o"),
                        "--root", str(make_repo(tmp_path))])
    assert rc == 2
    assert "no stored jira scope" in capsys.readouterr().out


def test_sync_with_no_scoped_features_is_quiet(tmp_path, capsys):
    rc = hub_jira.main(["--sync", "--out", str(tmp_path / "o"),
                        "--root", str(make_repo(tmp_path))])
    assert rc == 0
    assert "nothing to sync" in capsys.readouterr().out
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python -m pytest scripts/tests/test_hub_jira.py -v`
Expected: collection ERROR — `No module named 'hub_jira'`.

- [ ] **Step 3: Implement** — create `scripts/hub_jira.py`:

```python
"""CLI: the deterministic Jira pipeline (read-only against Jira; repo writes
happen in the gated hub.jira-* skills). Spec:
docs/specs/2026-07-09-jira-hub-skills-design.md.

  --check                       connectivity/auth probe (doctor section 4)
  --try-jql '<jql>'             scope discovery: count + sample rows
  --sweep <feature> --out DIR   proposed snapshot + ref candidates -> DIR
  --sync [<feature>] --out DIR  diff stored snapshots + watched keys -> report + DIR
"""
import argparse
import asyncio
import datetime
import os
import sys
from pathlib import Path

import httpx
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))

from hublib import jiramap
from hublib.jira import adf_to_text, client_from_env, probe_public

SWEEP_FIELDS = ["summary", "status", "issuetype", "resolution",
                "fixVersions", "updated", "description"]
DEFAULT_REF_TYPES = ["Outcome", "Feature"]
MAX_RESULTS = 500


def _load_env(root):
    """restricted/.env fallback so the CLI works in shells that never sourced
    it. Only JIRA_* keys are read; existing env always wins."""
    if os.environ.get("JIRA_SERVER"):
        return
    env = root / "restricted" / ".env"
    if not env.is_file():
        return
    for raw in env.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if line.startswith("export "):
            line = line[len("export "):]
        if line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        k = k.strip()
        if k.startswith("JIRA_") and k not in os.environ:
            os.environ[k] = v.strip().strip('"').strip("'")


def _jira_cfg(root, feature):
    """The feature's jira: block from features.yaml; None = unknown feature,
    {} = known feature without a stored scope."""
    p = root / "features" / "features.yaml"
    data = yaml.safe_load(p.read_text(encoding="utf-8")) if p.is_file() else {}
    for f in (data or {}).get("features") or []:
        if isinstance(f, dict) and f.get("id") == feature:
            return f.get("jira") or {}
    return None


async def _check():
    async with client_from_env() as client:
        me = await client.myself()
    print(f"jira ok: authenticated as "
          f"{me.get('displayName') or me.get('emailAddress', '?')}")
    return 0


async def _try_jql(jql, sample):
    async with client_from_env() as client:
        issues = await client.search(jql, fields=["summary", "status", "issuetype"],
                                     max_results=MAX_RESULTS)
    print(f"{len(issues)} issue(s) for: {jql}")
    for issue in issues[:sample]:
        f = issue.get("fields", {})
        print(f"  {issue.get('key')} · {(f.get('issuetype') or {}).get('name', '')}"
              f" · {(f.get('status') or {}).get('name', '')} · {f.get('summary', '')}")
    if len(issues) > sample:
        print(f"  … {len(issues) - sample} more")
    return 0


async def _fetch_rows(client, jql):
    issues = await client.search(jql, fields=SWEEP_FIELDS, max_results=MAX_RESULTS)
    keys = [i.get("key", "") for i in issues if i.get("key")]
    public = await probe_public(client.base_url, keys)
    rows = [jiramap.issue_row(i, i.get("key") in public) for i in issues]
    return issues, rows


async def _sweep(root, feature, jql_override, out, today):
    cfg = _jira_cfg(root, feature)
    if cfg is None:
        print(f"ERROR unknown feature '{feature}' (not in features/features.yaml)")
        return 2
    jql = jql_override or cfg.get("jql")
    if not jql:
        print(f"ERROR no stored jira scope for '{feature}' — pass --jql, or run "
              f"hub.jira-sweep scope discovery first")
        return 2
    ref_types = cfg.get("ref_types") or DEFAULT_REF_TYPES
    async with client_from_env() as client:
        base = client.base_url
        issues, rows = await _fetch_rows(client, jql)
    old = root / "features" / feature / "work" / "jira-snapshot.yaml"
    if old.is_file():
        old_rows = (yaml.safe_load(old.read_text(encoding="utf-8")) or {}).get("issues") or []
        if old_rows and (not rows or len(rows) < len(old_rows) / 2
                         or len(rows) > len(old_rows) * 2):
            print(f"WARN result count {len(rows)} vs {len(old_rows)} in the last "
                  f"snapshot — scope may have drifted; review the JQL before the gate")
    out.mkdir(parents=True, exist_ok=True)
    snap_path = out / f"jira-snapshot-{feature}.yaml"
    snap_path.write_text(jiramap.build_snapshot(feature, jql, rows, today),
                         encoding="utf-8", newline="\n")
    candidates = []
    for issue in issues:
        f = issue.get("fields", {})
        if (f.get("issuetype") or {}).get("name") in ref_types:
            candidates.append({
                "key": issue.get("key"),
                "type": (f.get("issuetype") or {}).get("name"),
                "status": (f.get("status") or {}).get("name"),
                "summary": f.get("summary", ""),
                "url": f"{base}/browse/{issue.get('key')}",
                "description": adf_to_text(f.get("description"))[:2000],
            })
    cand_path = out / f"candidates-{feature}.yaml"
    cand_path.write_text(yaml.safe_dump(candidates, sort_keys=False, allow_unicode=True),
                         encoding="utf-8", newline="\n")
    redacted = sum(1 for r in rows if r.get("summary") is None)
    print(f"swept {feature}: {len(rows)} issue(s), {redacted} summary(ies) withheld "
          f"(not anonymously readable), {len(candidates)} ref candidate(s)")
    print(f"proposed snapshot: {snap_path}")
    print(f"ref candidates:    {cand_path}")
    return 0


async def _sync(root, feature, out, today):
    p = root / "features" / "features.yaml"
    data = yaml.safe_load(p.read_text(encoding="utf-8")) if p.is_file() else {}
    feats = [f for f in (data or {}).get("features") or []
             if isinstance(f, dict) and f.get("jira")]
    if feature:
        feats = [f for f in feats if f.get("id") == feature]
        if not feats:
            print(f"ERROR '{feature}' has no jira: block in features/features.yaml "
                  f"— run hub.jira-sweep first")
            return 2
    if not feats:
        print("nothing to sync — no feature has a jira: block yet "
              "(run hub.jira-sweep first)")
        return 0
    watched = jiramap.watched_keys(root)
    any_changes = False
    out.mkdir(parents=True, exist_ok=True)
    async with client_from_env() as client:
        snap_keys = set()
        for f in feats:
            fid, jql = f["id"], (f.get("jira") or {}).get("jql", "")
            snap = root / "features" / fid / "work" / "jira-snapshot.yaml"
            if not snap.is_file():
                print(f"NOTE {fid}: no committed snapshot yet — run hub.jira-sweep "
                      f"first; skipping")
                continue
            old_rows = (yaml.safe_load(snap.read_text(encoding="utf-8")) or {}).get("issues") or []
            issues, rows = await _fetch_rows(client, jql)
            snap_keys |= {r.get("key") for r in rows} | {r.get("key") for r in old_rows}
            d = jiramap.diff(old_rows, rows)
            if not (d["new"] or d["vanished"] or d["changed"]):
                print(f"{fid}: no changes")
                continue
            any_changes = True
            print(f"{fid}: {len(d['new'])} new · {len(d['changed'])} changed · "
                  f"{len(d['vanished'])} vanished")
            for row in d["new"]:
                print(f"  NEW      {row['key']} · {row.get('type', '')} · "
                      f"{row.get('status', '')}")
            for ch in d["changed"]:
                deltas = "; ".join(f"{k}: {a!r} -> {b!r}"
                                   for k, (a, b) in ch["changes"].items())
                print(f"  CHANGED  {ch['key']} · {deltas}")
            for row in d["vanished"]:
                print(f"  VANISHED {row['key']} (left the JQL scope or was deleted)")
            path = out / f"jira-snapshot-{fid}.yaml"
            path.write_text(jiramap.build_snapshot(fid, jql, rows, today),
                            encoding="utf-8", newline="\n")
            print(f"  refreshed snapshot proposal: {path}")
        for key in sorted(k for k in watched if k not in snap_keys):
            try:
                issue = await client.get_issue(
                    key, fields=["summary", "status", "resolution"])
            except httpx.HTTPError:
                any_changes = True
                print(f"  WATCHED  {key} unreachable (deleted? moved? permission?) "
                      f"— referenced by {', '.join(watched[key])}")
                continue
            fx = issue.get("fields", {})
            status = (fx.get("status") or {}).get("name", "?")
            res = (fx.get("resolution") or {}).get("name")
            print(f"  WATCHED  {key} · {status}" + (f" ({res})" if res else "")
                  + f" — referenced by {', '.join(watched[key])}")
    print("sync: changes found — gate them via hub.jira-sync"
          if any_changes else "sync: all quiet")
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--try-jql", metavar="JQL")
    ap.add_argument("--sample", type=int, default=15)
    ap.add_argument("--sweep", metavar="FEATURE")
    ap.add_argument("--jql", metavar="JQL")
    ap.add_argument("--sync", nargs="?", const="", metavar="FEATURE")
    ap.add_argument("--out", metavar="DIR")
    ap.add_argument("--root", help=argparse.SUPPRESS)  # tests only
    args = ap.parse_args(argv)
    modes = [bool(args.check), args.try_jql is not None,
             args.sweep is not None, args.sync is not None]
    if sum(modes) != 1:
        ap.error("pick exactly one mode: --check | --try-jql | --sweep | --sync")
    if (args.sweep is not None or args.sync is not None) and not args.out:
        ap.error("--out DIR is required with --sweep/--sync "
                 "(proposals are written there, never into the repo)")
    root = Path(args.root) if args.root else Path(__file__).resolve().parents[1]
    today = datetime.date.today().isoformat()
    _load_env(root)
    try:
        if args.check:
            return asyncio.run(_check())
        if args.try_jql is not None:
            return asyncio.run(_try_jql(args.try_jql, args.sample))
        out = Path(args.out)
        if args.sweep is not None:
            return asyncio.run(_sweep(root, args.sweep, args.jql, out, today))
        return asyncio.run(_sync(root, args.sync or None, out, today))
    except RuntimeError as exc:
        print(f"ERROR {exc}")
        return 1
    except httpx.HTTPStatusError as exc:
        code = exc.response.status_code
        if code in (401, 403):
            print(f"ERROR jira auth failed ({code}) — JIRA_TOKEN expired? Generate "
                  f"a new API token at https://id.atlassian.com/manage-profile/"
                  f"security/api-tokens, update JIRA_TOKEN in restricted/.env, "
                  f"re-run. (Token values are never printed.)")
        else:
            print(f"ERROR jira request failed: {code} on {exc.request.url}")
        return 1
    except httpx.HTTPError as exc:
        print(f"ERROR network failure talking to Jira: {exc}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `python -m pytest scripts/tests/test_hub_jira.py -v`
Expected: 5 PASS. (These paths return before any network call — offline-safe.)

- [ ] **Step 5: Live smoke — connectivity probe (this machine has creds)**

Run: `python scripts/hub_jira.py --check`
Expected: `jira ok: authenticated as <display name>`, exit 0. Paste the output line (it contains no secrets) into your task report. If it fails with the 401 remediation, report that instead — do not debug credentials yourself.

- [ ] **Step 6: Full suite + lint**

Run: `python -m pytest scripts/tests -v && python scripts/hub_lint.py && python scripts/hub_index.py --check`
Expected: all PASS; `0 error(s)`; `0 stale file(s)`.

- [ ] **Step 7: Commit**

```bash
git add scripts/hub_jira.py scripts/tests/test_hub_jira.py
git commit -m "feat(cli): hub_jira — check/try-jql/sweep/sync, proposals to --out only (#2)

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

### Task 6: The skills — `hub.jira-sweep` + `hub.jira-sync`

**Files:**
- Create: `.claude/skills/hub.jira-sweep/SKILL.md`
- Create: `.claude/skills/hub.jira-sync/SKILL.md`

**Interfaces:**
- Consumes: the CLI modes from Task 5 (exact invocations below).
- Produces: the skills Task 8's docs describe. `.claude/` is not linted — no counts change.

- [ ] **Step 1: Write the sweep skill**

Create `.claude/skills/hub.jira-sweep/SKILL.md` with exactly this content:

```markdown
---
name: hub.jira-sweep
description: Sweep Jira into the hub for one feature — conversational scope discovery (JQL stored in features.yaml), a curated public snapshot under <feature>/work/, and gated ref- entries for strategic issues (default Outcome/Feature types). Use when the user says "sweep jira for <feature>", "pull the jiras for <feature>", "set up jira tracking for <feature>", or when filed Jira links deserve field ingestion. Read-only against Jira; every repo write is gated.
---

# hub.jira-sweep

Input: a feature id (features/features.yaml) + optional JQL/scope hints.
Spec: /docs/specs/2026-07-09-jira-hub-skills-design.md. Read-only against
Jira — never comment, transition, or edit issues.

1. PRE-FLIGHT: `python scripts/hub_jira.py --check`. Failure → stop and
   point at `bash scripts/doctor.sh check` (section 4) — no retry loops.
2. SCOPE: a `jira:` block on the feature in features/features.yaml → use
   it. None → scope discovery: ask ONCE for hints (project? component?
   labels? a known issue key?), then iterate
   `python scripts/hub_jira.py --try-jql '<candidate>'` showing counts +
   sample rows until the user approves the JQL. The approved block
   (`jql:` + optional `ref_types:`, default [Outcome, Feature]) becomes a
   features.yaml edit proposed AT THE GATE (step 5) — nothing is written
   now. Component↔label mapping is messy by nature; JQL is the one stored
   scope language.
3. FETCH: `python scripts/hub_jira.py --sweep <feature> [--jql '<jql>']
   --out <scratchpad>/jira`. The CLI writes the proposed snapshot
   (summaries already redacted by the unauthenticated-probe rule) and
   candidates-<feature>.yaml (the strategic tier). Heed its WARN on
   result-count swings — a drifted scope needs the user's eyes on the JQL
   before anything is gated.
4. DRAFT (scratch only, no repo writes): one ref- entry per candidate the
   feature does not already track (match on resource: URL) — filename
   `ref-<key-lower>-<slug>.md`, `type: reference`, canonical `resource:`
   (/conventions/uris.md), one-line description written for a reader
   deciding whether to open it, body 2–4 sentences (what it is, status,
   why it matters to this feature). An existing ref- for a candidate →
   propose an update only if the issue materially changed. NEVER copy a
   probe-redacted summary into any tracked file — a withheld summary
   means Jira itself does not serve that text anonymously.
5. GATE: one batch table — every proposed write, one line:
   `path: description [new|update]` — the snapshot
   (features/<id>/work/jira-snapshot.yaml, redacted count called out),
   each ref-, and the features.yaml scope edit when new/changed. Full
   content on request. Approve/edit/reject per line; nothing touches the
   repo before OK.
6. On OK: write the approved files, `python scripts/hub_index.py`, then
   `python scripts/hub_lint.py` (0 errors — fix the written content,
   never the scripts). Commit:
   `git add -A && git commit -m "jira(<feature>): sweep — <n> issues, <m> refs"`
   && `git push`.
7. Offer follow-ups, never auto-run: a `hub.jira-sync` cadence, or ref-
   entries for non-strategic issues the user names (hub.capture path).
```

- [ ] **Step 2: Write the sync skill**

Create `.claude/skills/hub.jira-sync/SKILL.md` with exactly this content:

```markdown
---
name: hub.jira-sync
description: Refresh the hub against live Jira — re-run every stored feature scope, diff against the committed snapshots, watch each ref-'d and jtbd-linked issue key, and propose the consequences (snapshot refresh, ref- updates, jtbd status nudges) through the gate. Use when the user says "sync jira", "refresh the jira map", "what changed in jira", or periodically once sweeps exist. Read-only against Jira.
---

# hub.jira-sync

Input: optional feature id — default is every feature with a `jira:` block
in features/features.yaml. Spec:
/docs/specs/2026-07-09-jira-hub-skills-design.md.

1. PRE-FLIGHT: `python scripts/hub_jira.py --check`. Failure → stop and
   point at `bash scripts/doctor.sh check` (section 4).
2. DIFF: `python scripts/hub_jira.py --sync [<feature>] --out
   <scratchpad>/jira`. It reads committed snapshots, re-runs stored JQLs,
   and reports NEW / CHANGED / VANISHED per feature, plus WATCHED lines
   for every Jira key referenced by ref- resource: URLs or jtbd jira:
   lists outside the swept scopes — refs never silently rot. "sync: all
   quiet" → report that and stop; zero ceremony.
3. INTERPRET the diff into proposals (scratch only):
   - the refreshed snapshot per changed feature (the CLI already wrote
     the proposed file to --out);
   - ref- updates only where the change matters to the entry's prose or
     validity: resolved / closed / won't-fix → a status note in the body
     + a `review_after` bump. Routine status churn is snapshot-only —
     do not rewrite refs for it;
   - jtbd nudges: every key in a jtbd's `jira:` list resolved → propose
     `status: delivered` (the user rules; never automatic);
   - NEW arrivals whose type is in the feature's `ref_types` → ref-
     candidates drafted per hub.jira-sweep step 4;
   - VANISHED or unreachable WATCHED keys → flag the referencing entries
     for the user's ruling (deleted, moved, or permission change).
4. GATE: one batch table — `path: description [new|update]`;
   approve/edit/reject per line; nothing touches the repo before OK.
5. On OK: write, `python scripts/hub_index.py`, `python
   scripts/hub_lint.py` (0 errors), commit
   `git add -A && git commit -m "jira(sync): <features> — <summary>"` &&
   `git push`.
```

- [ ] **Step 3: Verify lint/index untouched**

Run: `python scripts/hub_lint.py && python scripts/hub_index.py --check`
Expected: `0 error(s)` (baseline warnings), `0 stale file(s)` — `.claude/` is not linted.

- [ ] **Step 4: Commit**

```bash
git add .claude/skills/hub.jira-sweep .claude/skills/hub.jira-sync
git commit -m "skills: hub.jira-sweep + hub.jira-sync — gated Jira pipeline (#2)

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

### Task 7: Doctor — httpx in deps check + live Jira probe

**Files:**
- Modify: `scripts/doctor.sh` (section 1 import line; section 4 after the `JIRA_*` presence loop)

**Interfaces:**
- Consumes: `hub_jira.py --check` (Task 5).
- Produces: the doctor lines Task 8's tooling.md rows describe. Delivers the Jira slice of backlog #19.

- [ ] **Step 1: Section 1 — add httpx to the import check.** Replace:

```bash
if python -c "import yaml, pytest" 2>/dev/null; then
  ok "python + pyyaml + pytest"
```

with:

```bash
if python -c "import yaml, pytest, httpx" 2>/dev/null; then
  ok "python + pyyaml + pytest + httpx"
```

- [ ] **Step 2: Section 4 — live probe after the presence loop.** Replace:

```bash
  for k in JIRA_SERVER JIRA_USER JIRA_TOKEN; do
    if [ -n "${!k:-}" ]; then ok "$k present"; else warn "$k missing in restricted/.env"; fi
  done
```

with:

```bash
  for k in JIRA_SERVER JIRA_USER JIRA_TOKEN; do
    if [ -n "${!k:-}" ]; then ok "$k present"; else warn "$k missing in restricted/.env"; fi
  done
  # Live probe (backlog #19's Jira slice): presence is not validity. WARN,
  # not FAIL — offline machines must still pass the doctor.
  if [ -n "${JIRA_SERVER:-}" ] && [ -n "${JIRA_TOKEN:-}" ]; then
    if python "$ROOT/scripts/hub_jira.py" --check >/dev/null 2>&1; then
      ok "jira reachable (hub_jira --check)"
    else
      warn "jira unreachable or auth failed — run: python scripts/hub_jira.py --check (expired JIRA_TOKEN? offline?)"
    fi
  fi
```

- [ ] **Step 3: Smoke-run check mode (read-only — NEVER run setup)**

Run: `bash scripts/doctor.sh check`
Expected: section 1 prints `OK python + pyyaml + pytest + httpx`; section 4 prints the three presence lines plus `OK jira reachable (hub_jira --check)`; overall `0 fail`. Paste the section 1 and 4 lines into your task report.

- [ ] **Step 4: Commit**

```bash
git add scripts/doctor.sh
git commit -m "feat(doctor): httpx dep check + live Jira probe via hub_jira --check (#2, #19 slice)

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

### Task 8: Docs, conventions, backlog, and log

**Files:**
- Modify: `AGENTS.md`, `docs/skills.md`, `docs/tooling.md`, `conventions/type-vocabulary.md`, `conventions/layout.md`, `docs/enhancements.md`, `memory/log.md`, `.claude/skills/hub.intake/SKILL.md`
- Regenerate: whatever `hub_index.py` touches

**Interfaces:**
- Consumes: skill names/behaviors (Task 6), CLI modes (Task 5), doctor lines (Task 7), and Task 6's commit hash for the Done entry (`git log --format=%h --grep="hub.jira-sweep" -1`).
- Produces: shipping paperwork only.

- [ ] **Step 1: AGENTS.md — two skill rows.** In the `## Skills` table, directly after the `| hub.research | ... |` row, insert:

```markdown
| hub.jira-sweep | sweep Jira into a feature — scope discovery, public snapshot, gated refs |
| hub.jira-sync | diff stored Jira scopes + watched keys; propose updates via the gate |
```

Then run: `wc -l AGENTS.md` — Expected: ≤ 150 (hard CI budget; currently well under).

- [ ] **Step 2: conventions/type-vocabulary.md — formalize jtbd `jira:`.** Replace the jtbd row:

```markdown
| `jtbd`      | `jtbd-`     | a job to be done ("When …, I want …, so I can …"); execution status stays in Jira (`jira:` field) | `persona` (locked list), `status: candidate\|validated\|delivered\|retired` |
```

with:

```markdown
| `jtbd`      | `jtbd-`     | a job to be done ("When …, I want …, so I can …"); execution status stays in Jira — optional `jira: [KEYS]` list is watched by hub.jira-sync | `persona` (locked list), `status: candidate\|validated\|delivered\|retired` |
```

- [ ] **Step 3: conventions/layout.md — snapshot in the work/ row.** Replace:

```markdown
| `work/`      | active drafts, RFE pipeline artifacts, `transcripts/` (gitignored) |
```

with:

```markdown
| `work/`      | active drafts, RFE pipeline artifacts, `transcripts/` (gitignored), `jira-snapshot.yaml` (machine-written by hub.jira-sweep; tracked) |
```

- [ ] **Step 4: docs/skills.md — chains, quick reference, in-depth.**

(a) In `## The common chains`, directly after the `- **Research:** ...` bullet, add:

```markdown
- **Jira:** `hub.jira-sweep <feature>` (scope discovery → tracked snapshot +
  gated refs) then `hub.jira-sync` on demand — diff-driven refresh; the map
  lives in [/views/jira-map.md](/views/jira-map.md).
```

(b) In the `## Quick reference` table, directly after the `hub.research` row, add:

```markdown
| `hub.jira-sweep` | sweep Jira for one feature (snapshot + strategic refs) | scope confirm + batch write gate | features.yaml scope, work/jira-snapshot.yaml, ref- entries, reindex + commit |
| `hub.jira-sync` | refresh swept scopes + watched keys against live Jira | batch write gate | snapshot refreshes, ref-/jtbd updates, reindex + commit |
```

(c) In `## The hub.* skills in more depth`, directly after the `**hub.research**` paragraph, add:

```markdown
**`hub.jira-sweep`** — the Jira intake path for one feature. First run does
conversational scope discovery (`--try-jql` iterations until the JQL looks
right; the approved scope is stored as a `jira:` block in
`features/features.yaml`). Every run fetches the scope, builds a
whitelisted public snapshot (`work/jira-snapshot.yaml` — summaries admitted
only when an unauthenticated probe proves the issue world-readable), picks
strategic-tier issues (`ref_types`, default Outcome/Feature) as gated ref-
candidates, and batches everything through one table. Read-only against
Jira.

**`hub.jira-sync`** — the refresh half: re-runs every stored scope, diffs
against committed snapshots (NEW / CHANGED / VANISHED), and watches every
Jira key referenced by ref- `resource:` URLs or jtbd `jira:` lists even
outside the scopes. Consequences (snapshot refresh, ref- status notes,
jtbd `delivered` nudges, new ref- candidates) are proposed through the
gate; an all-quiet run is a one-line report.
```

- [ ] **Step 5: docs/tooling.md — commands, library, doctor rows.**

(a) In the `## The commands` table, directly after the `hub_publish.py --pages-dir` row, add:

```markdown
| `python scripts/hub_jira.py --check` | Jira connectivity/auth probe (doctor section 4 runs it) | setup; auth debugging |
| `python scripts/hub_jira.py --try-jql '<jql>'` | scope discovery: result count + sample rows | hub.jira-sweep step 2 |
| `python scripts/hub_jira.py --sweep <feature> --out <dir>` | proposed snapshot + ref candidates into `<dir>` (repo untouched) | driven by hub.jira-sweep |
| `python scripts/hub_jira.py --sync --out <dir>` | diff stored scopes + watched keys against live Jira | driven by hub.jira-sync |
```

(b) In the `## The library — scripts/hublib/` table, after the `publisher.py` row, add:

```markdown
| `jira.py` | async Jira REST client (pm-toolkit port): Cloud basic / DC bearer auth from `JIRA_*` env, JQL search with pagination, 429 retry, ADF→text, unauthenticated `probe_public`; write methods ported but unused by the hub.jira-* skills |
| `jiramap.py` | the snapshot contract: whitelisted `issue_row`, byte-stable `build_snapshot`, `validate` (lint), `diff` (sync), `watched_keys` (ref-/jtbd backlinks) |
```

(c) In the `## The doctor` sections table, replace row 1:

```markdown
| 1 | python + pyyaml + pytest importable | `pip install -r scripts/requirements.txt` |
```

with:

```markdown
| 1 | python + pyyaml + pytest + httpx importable | `pip install -r scripts/requirements.txt` |
```

and replace row 4:

```markdown
| 4 | `restricted/.env` exists with required keys (`JIRA_*`); sources it so later sections see the `CTRACK_*` overrides and MCP secrets | — (secrets are copied between machines by hand, never generated) |
```

with:

```markdown
| 4 | `restricted/.env` exists with required keys (`JIRA_*`) + live Jira reachability (`hub_jira.py --check`, WARN when offline); sources it so later sections see the `CTRACK_*` overrides and MCP secrets | — (secrets are copied between machines by hand, never generated) |
```

- [ ] **Step 6: docs/enhancements.md — close #2, trim #19, unblock #27.**

(a) Priority table: **delete** the row starting `| 2 | Jira hub skills — sweep, track, and sync |`.

(b) Priority table: **replace** the row starting `| 19 |` with:

```markdown
| 19 | Doctor: `~/.bashrc` env wiring + Slack connectivity probe (the Jira probe shipped 2026-07-09 with #2) | Low–Medium — remaining slice is env wiring + Slack | Small | With R5 |
```

(c) Priority table: in the row starting `| 27 |`, replace the final cell `After #2` with `Next — #2 shipped 2026-07-09`.

(d) Prose: **delete** the entire `**2 · Jira hub skills — sweep, track, and sync.**` paragraph (it moves to Done).

(e) Prose: Read the `**19 ·**` paragraph and append this exact sentence at its end:

```markdown
The Jira connectivity probe shipped 2026-07-09 with #2 (doctor section 4
runs `hub_jira.py --check`); the remaining scope is the env wiring and a
Slack probe.
```

(f) Prose: Read the `**30 · Jira hygiene auditor.**` paragraph and append this exact sentence at its end:

```markdown
The client layer it needs now exists (`scripts/hublib/jira.py`, including
the write methods hygiene fixes would use behind a gate).
```

(g) In `## Done`, add (substitute `<hash>` from `git log --format=%h --grep="hub.jira-sweep" -1`):

```markdown
- **#2 Jira hub skills** — shipped 2026-07-09 (`<hash>`): `hublib/jira.py`
  (pm-toolkit client port, httpx), `hublib/jiramap.py` + `hub_jira.py`
  (check/try-jql/sweep/sync CLI), `hub.jira-sweep` + `hub.jira-sync`
  skills, tracked public `work/jira-snapshot.yaml` per feature with the
  unauthenticated-probe summary rule, enriched `views/jira-map.md`, and
  the doctor Jira probe (#19's Jira slice). Spec:
  [/docs/specs/2026-07-09-jira-hub-skills-design.md](/docs/specs/2026-07-09-jira-hub-skills-design.md).
  Plan: [/docs/plans/2026-07-09-jira-hub-skills-plan.md](/docs/plans/2026-07-09-jira-hub-skills-plan.md).
```

- [ ] **Step 7: memory/log.md — ship line.** Under the `## 2026-07-09` heading (create it directly after the frontmatter if absent), add:

```markdown
- **Creation** — Jira hub skills shipped (backlog #2): hublib Jira client
  (httpx port from pm-toolkit), hub.jira-sweep/hub.jira-sync, tracked
  public snapshots with probe-gated summaries, enriched jira-map view,
  doctor Jira probe (#19 slice). #27(b) jira-gap unblocked.
```

- [ ] **Step 8: hub.intake — upgrade the deferred-Jira note.** In `.claude/skills/hub.intake/SKILL.md` step 2, replace:

```markdown
(field ingestion arrives with the Jira hub skills, backlog #2)
```

with:

```markdown
(offer a hub.jira-sweep run afterwards for field ingestion + the
   feature snapshot)
```

- [ ] **Step 9: Reindex, lint, verify**

Run: `python scripts/hub_index.py && python scripts/hub_lint.py && python scripts/hub_index.py --check`
Expected: `0 error(s)` (broken-link warnings must not increase); `0 stale file(s)`.

- [ ] **Step 10: Commit**

```bash
git add AGENTS.md docs/skills.md docs/tooling.md conventions/type-vocabulary.md conventions/layout.md docs/enhancements.md memory/log.md memory/index.md .claude/skills/hub.intake/SKILL.md
git commit -m "docs: ship Jira hub skills — backlog #2 done, #19 trimmed, #27 unblocked

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

(If `hub_index.py` regenerated other `views/*` or `index.md` files, `git add -A` instead — generated files ship with the edit that staled them.)

---

### Task 9: Full verification + push

**Files:** none (verification only).

**Interfaces:**
- Consumes: everything above.
- Produces: a green `validate.yml` run on `main`.

- [ ] **Step 1: Full local verification**

Run: `python -m pytest scripts/tests -v && python scripts/hub_lint.py && python scripts/hub_index.py --check && python scripts/hub_publish.py --check`
Expected: all tests PASS; `0 error(s)`; `0 stale file(s)`; manifest valid.

- [ ] **Step 2: Push and watch CI**

```bash
git push
gh run watch --exit-status $(gh run list --workflow=validate.yml --limit 1 --json databaseId --jq '.[0].databaseId')
```

Expected: success. Note: CI installs `scripts/requirements.txt`, so httpx is present there; all Jira tests are offline (MockTransport). If CI fails, read `gh run view --log-failed`, fix the offending file (never by weakening linter/tests), commit, re-push.

---

## Acceptance runs (owner-in-the-loop — NOT subagent tasks)

Live sessions with Peter at the gates and real Jira access, after the plan
lands. Findings become skill/CLI edits (normal commits), not plan changes.

- [ ] 1. First sweep with scope discovery on a real feature (mcp-registry:
  component/labels archaeology → stored JQL → snapshot + refs through the
  gate; verify the probe redacts non-public summaries; CI green after push).
- [ ] 2. `views/jira-map.md` reads well on the real data — adjust rendering
  by taste (skill edit, not plan change).
- [ ] 3. A `hub.jira-sync` run a few days later: diff report, gated snapshot
  refresh, WATCHED line for RHAISTRAT-1345.
- [ ] 4. `bash scripts/doctor.sh check` on this machine: section 4 shows the
  live probe OK.
- [ ] 5. A jtbd entry gains a `jira:` list; the next sync watches it.
