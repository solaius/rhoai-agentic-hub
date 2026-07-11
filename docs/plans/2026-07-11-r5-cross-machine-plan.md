# R5 cross-machine: doctor-owned env wiring + Slack probe - implementation plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship backlog #19 (shell env wiring + Slack connectivity probe) as tested `hublib` code the doctor calls, then execute R5 steps 2-4 on machine B so #14 gets evidence instead of guesswork.

**Architecture:** Logic lives in `hublib` with thin CLIs, mirroring the Jira probe from #2 (`hublib/jira.py` + `scripts/hub_jira.py --check`, called from `doctor.sh`). `doctor.sh` is 476 lines of untested bash, so idempotent profile editing and token probing stay in Python where pytest reaches them. Two existing doctor sections are extended rather than renumbered.

**Tech Stack:** Python 3.11+, `httpx>=0.28` (already in `scripts/requirements.txt`), pytest with `httpx.MockTransport`, bash (Git Bash on Windows).

**Spec:** [/docs/specs/2026-07-11-r5-cross-machine-design.md](/docs/specs/2026-07-11-r5-cross-machine-design.md)

## Global Constraints

- **No em dashes** in any output: code, comments, docs, commit messages. Use commas, colons, parentheses, or spaced hyphens. (`memory/profiles/preferences.md`)
- **No LLM-provider credential handling** anywhere: the doctor neither exports, checks, nor unsets them. Do NOT port the retired block's `unset CLAUDE_CODE_USE_VERTEX ...` line. (Owner ruling 2026-07-08.)
- **Probes WARN, never FAIL.** An offline machine must still reach `0 fail`. Same rule as the existing Jira probe.
- **`python`, not `python3`** (Windows; `~/.bashrc` aliases `python='py'`).
- **Secrets are never printed.** Report key presence and auth identity, never values.
- Verification suite: `python -m pytest scripts/tests -v` · `python scripts/hub_lint.py` · `python scripts/hub_index.py --check`.

## File Structure

| file | responsibility |
|---|---|
| `scripts/hublib/shellenv.py` | CREATE. Pure functions over profile text (render/scan/apply the marked block) plus `load_env()`, the shared `restricted/.env` reader. |
| `scripts/hublib/slack.py` | CREATE. Slack `auth.test` probe, returns `(kind, message)`. |
| `scripts/hub_env.py` | CREATE. CLI: `--check` / `--setup`. Emits `kind<TAB>message` lines for doctor. |
| `scripts/hub_slack.py` | CREATE. CLI: `--check`. Emits one `kind<TAB>message` line. |
| `scripts/hub_jira.py` | MODIFY. `_load_env()` delegates to `shellenv.load_env` (kills the duplicate parser). |
| `scripts/doctor.sh` | MODIFY. Section 4 gains the wiring call; section 9 gains the Slack probe. No renumbering. |
| `scripts/tests/test_shellenv.py` | CREATE. |
| `scripts/tests/test_hub_env.py` | CREATE. |
| `scripts/tests/test_slack.py` | CREATE. |
| `scripts/tests/test_hub_slack.py` | CREATE. |
| `docs/setup.md`, `docs/tooling.md` | MODIFY. Wiring step, new-shell requirement, Bash-tool-only caveat, doctor section reference. |
| `docs/enhancements.md` | MODIFY (Task 7). `## R5 outcome`, #19 to Done, #14 annotated. |

**Deviation from the spec, flagged for review:** the spec said section numbering shifts. It does not. Shell wiring of `restricted/.env` belongs inside section 4 (which already sources that file) and the Slack auth probe belongs inside section 9 (slack runtime). Extending both avoids renumbering ten sections across `doctor.sh` and `docs/tooling.md` for zero functional gain, and keeps related checks together. Section headers are renamed to stay accurate.

---

### Task 1: `hublib/shellenv.py` core

The pure text transforms and the shared env reader. No I/O in the transforms, so they are trivially testable.

**Files:**
- Create: `scripts/hublib/shellenv.py`
- Create: `scripts/tests/test_shellenv.py`
- Modify: `scripts/hub_jira.py:31-48` (delegate `_load_env`)

**Interfaces:**
- Produces:
  - `load_env(root: Path, prefixes: tuple[str, ...] = ()) -> None` - populate `os.environ` from `<root>/restricted/.env`; existing env always wins; empty `prefixes` loads every key.
  - `render_block(env_path: Path) -> str` - the marked `~/.bashrc` block, no trailing newline.
  - `scan(text: str, env_path: Path) -> dict` - keys `hub_block: bool`, `hub_current: bool`, `retired_block: bool`, `retired_unmarked: list[str]`.
  - `apply(text: str, env_path: Path) -> str` - retired block removed, hub block upserted, idempotent.
  - Constants `HUB_BEGIN`, `HUB_END`, `RETIRED_BEGIN`, `RETIRED_END`.

- [ ] **Step 1: Write the failing tests**

Create `scripts/tests/test_shellenv.py`:

```python
import os
from pathlib import Path

from hublib import shellenv
from hublib.shellenv import HUB_BEGIN, HUB_END, apply, load_env, render_block, scan

ENV = Path("C:/repo/restricted/.env")

RETIRED = """alias python='py'

# >>> ai-asset-registry env >>>
if [ -f "C:/Users/peter/Code/rh/ai-asset-registry/rhoai-restricted/.env" ]; then
  set -a; . "C:/Users/peter/Code/rh/ai-asset-registry/rhoai-restricted/.env"; set +a
  unset CLAUDE_CODE_USE_VERTEX ANTHROPIC_API_KEY
fi
# <<< ai-asset-registry env <<<
"""


def test_render_block_sources_the_hub_env_and_uses_forward_slashes():
    block = render_block(ENV)
    assert HUB_BEGIN in block and HUB_END in block
    assert 'set -a; . "C:/repo/restricted/.env"; set +a' in block
    assert "\\" not in block


def test_render_block_never_unsets_llm_credentials():
    # Owner ruling 2026-07-08: no LLM-provider credential handling, ever.
    assert "unset" not in render_block(ENV)
    assert "ANTHROPIC" not in render_block(ENV)


def test_apply_removes_the_retired_block_including_its_unset_line():
    out = apply(RETIRED, ENV)
    assert "ai-asset-registry" not in out
    assert "unset" not in out
    assert "alias python='py'" in out          # unrelated lines survive
    assert HUB_BEGIN in out


def test_apply_is_idempotent():
    once = apply(RETIRED, ENV)
    assert apply(once, ENV) == once


def test_apply_repairs_a_moved_repo_path_without_duplicating_the_block():
    stale = apply("", Path("D:/old/restricted/.env"))
    out = apply(stale, ENV)
    assert out.count(HUB_BEGIN) == 1
    assert "D:/old" not in out
    assert "C:/repo/restricted/.env" in out


def test_apply_on_empty_profile():
    out = apply("", ENV)
    assert out.startswith(HUB_BEGIN)
    assert out.endswith("\n")


def test_scan_reports_current_hub_block():
    s = scan(apply("", ENV), ENV)
    assert s["hub_block"] and s["hub_current"]
    assert not s["retired_block"]


def test_scan_reports_stale_hub_block_as_not_current():
    s = scan(apply("", Path("D:/old/restricted/.env")), ENV)
    assert s["hub_block"] and not s["hub_current"]


def test_scan_reports_retired_block():
    s = scan(RETIRED, ENV)
    assert s["retired_block"]
    assert not s["hub_block"]


def test_scan_reports_unmarked_retired_reference():
    text = '. "C:/Users/peter/Code/rh/ai-asset-registry/rhoai-restricted/.env"\n'
    s = scan(text, ENV)
    assert not s["retired_block"]
    assert s["retired_unmarked"] == [
        '. "C:/Users/peter/Code/rh/ai-asset-registry/rhoai-restricted/.env"']


def test_unterminated_marker_is_left_alone_not_truncated():
    text = f"keep me\n{HUB_BEGIN}\nhalf a block\n"
    assert "keep me" in apply(text, ENV)


def test_load_env_populates_prefixed_keys_and_existing_env_wins(tmp_path, monkeypatch):
    (tmp_path / "restricted").mkdir()
    (tmp_path / "restricted" / ".env").write_text(
        '# comment\n'
        'export JIRA_SERVER="https://jira.example.com"\n'
        "JIRA_TOKEN='tok'\n"
        "SLACK_XOXC_TOKEN=xoxc-1\n"
        "GITHUB_TOKEN=ghp-1\n",
        encoding="utf-8")
    monkeypatch.delenv("JIRA_SERVER", raising=False)
    monkeypatch.delenv("SLACK_XOXC_TOKEN", raising=False)
    monkeypatch.setenv("JIRA_TOKEN", "already-set")

    load_env(tmp_path, prefixes=("JIRA_",))
    assert os.environ["JIRA_SERVER"] == "https://jira.example.com"
    assert os.environ["JIRA_TOKEN"] == "already-set"       # existing env wins
    assert "SLACK_XOXC_TOKEN" not in os.environ            # prefix filtered out


def test_load_env_missing_file_is_a_noop(tmp_path):
    load_env(tmp_path, prefixes=("JIRA_",))  # must not raise
```

- [ ] **Step 2: Run the tests, verify they fail**

Run: `python -m pytest scripts/tests/test_shellenv.py -v`
Expected: FAIL, `ModuleNotFoundError: No module named 'hublib.shellenv'`

- [ ] **Step 3: Implement `scripts/hublib/shellenv.py`**

```python
"""Shell-profile wiring for the hub's restricted/.env (doctor section 4).

Hub tooling self-loads restricted/.env via load_env() below. The marketplace
rfe.* skills do NOT: preflight.py, fetch_single.py, dump_jira.py and
rfe.submit read os.environ with no fallback, so JIRA_* must be present in
every shell. This module owns the ~/.bashrc block that puts it there.

Per the 2026-07-08 owner ruling the block never touches LLM-provider
credentials: it neither exports nor unsets them. The retired ai-asset-registry
block did unset them; it is removed wholesale (see apply()).
"""
from __future__ import annotations

import os
from pathlib import Path

HUB_BEGIN = "# >>> rhoai-agentic-hub env >>>"
HUB_END = "# <<< rhoai-agentic-hub env <<<"
RETIRED_BEGIN = "# >>> ai-asset-registry env >>>"
RETIRED_END = "# <<< ai-asset-registry env <<<"
RETIRED_MARKER = "ai-asset-registry"


def load_env(root: Path, prefixes: tuple[str, ...] = ()) -> None:
    """Populate os.environ from <root>/restricted/.env for shells that never
    sourced it. Existing env always wins. Empty prefixes loads every key."""
    env = Path(root) / "restricted" / ".env"
    if not env.is_file():
        return
    for raw in env.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if line.startswith("export "):
            line = line[len("export "):]
        if line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        if prefixes and not key.startswith(prefixes):
            continue
        if key not in os.environ:
            os.environ[key] = value.strip().strip('"').strip("'")


def render_block(env_path: Path) -> str:
    """The marked block. Forward slashes: bash reads this, not Windows."""
    p = str(env_path).replace("\\", "/")
    return "\n".join([
        HUB_BEGIN,
        f'if [ -f "{p}" ]; then',
        f'  set -a; . "{p}"; set +a',
        "fi",
        HUB_END,
    ])


def _has_block(text: str, begin: str, end: str) -> bool:
    lines = [line.strip() for line in text.splitlines()]
    return begin in lines and end in lines


def _strip_block(text: str, begin: str, end: str) -> str:
    """Remove a marker-delimited block. An unterminated marker is left alone:
    truncating the rest of someone's shell profile is never the right call."""
    if not _has_block(text, begin, end):
        return text
    out, skipping = [], False
    for line in text.splitlines():
        stripped = line.strip()
        if stripped == begin:
            skipping = True
            continue
        if skipping:
            if stripped == end:
                skipping = False
            continue
        out.append(line)
    return "\n".join(out)


def scan(text: str, env_path: Path) -> dict:
    """What the profile currently says about hub and retired-repo wiring."""
    normalized = text.replace("\r\n", "\n")
    without_retired = _strip_block(normalized, RETIRED_BEGIN, RETIRED_END)
    unmarked = [
        line.strip() for line in without_retired.splitlines()
        if RETIRED_MARKER in line and not line.strip().startswith("#")
    ]
    return {
        "hub_block": _has_block(normalized, HUB_BEGIN, HUB_END),
        "hub_current": render_block(env_path) in normalized,
        "retired_block": _has_block(normalized, RETIRED_BEGIN, RETIRED_END),
        "retired_unmarked": unmarked,
    }


def apply(text: str, env_path: Path) -> str:
    """Retired block removed, hub block upserted. Idempotent; a moved repo
    path is repaired in place rather than duplicated."""
    body = _strip_block(text.replace("\r\n", "\n"), RETIRED_BEGIN, RETIRED_END)
    body = _strip_block(body, HUB_BEGIN, HUB_END).rstrip("\n")
    block = render_block(env_path)
    return f"{body}\n\n{block}\n" if body else f"{block}\n"
```

- [ ] **Step 4: Run the tests, verify they pass**

Run: `python -m pytest scripts/tests/test_shellenv.py -v`
Expected: PASS, 12 tests.

- [ ] **Step 5: Delegate `hub_jira._load_env` to the shared reader**

In `scripts/hub_jira.py`, change the import line:

```python
from hublib.jira import adf_to_text, client_from_env, probe_public
from hublib.shellenv import load_env
```

and replace the whole `_load_env` function (lines 31-48) with:

```python
def _load_env(root):
    """restricted/.env fallback so the CLI works in shells that never sourced
    it. Only JIRA_* keys are read; existing env always wins."""
    load_env(root, prefixes=("JIRA_",))
```

- [ ] **Step 6: Run the full suite, verify nothing regressed**

Run: `python -m pytest scripts/tests -q`
Expected: PASS, 180 tests (168 existing + 12 new).

- [ ] **Step 7: Commit**

```bash
git add scripts/hublib/shellenv.py scripts/tests/test_shellenv.py scripts/hub_jira.py
git commit -m "feat(shellenv): profile-block transforms + shared restricted/.env reader

Pure functions over ~/.bashrc text: render/scan/apply the hub's marked block,
remove the retired ai-asset-registry block (and with it the LLM-credential
unset machinery the 2026-07-08 ruling banned). hub_jira._load_env now
delegates to the shared reader instead of carrying its own parser.

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

### Task 2: `scripts/hub_env.py` CLI

**Files:**
- Create: `scripts/hub_env.py`
- Create: `scripts/tests/test_hub_env.py`

**Interfaces:**
- Consumes: `hublib.shellenv.{apply, scan, load_env}` from Task 1.
- Produces: `main(argv=None) -> int`. Prints TAB-separated `kind<TAB>message` lines; kinds are `ok`, `warn`, `wrote`. Exit code is always 0 (WARN never FAIL). Flags: `--check`, `--setup`, plus hidden `--root` and `--home` for tests.

The `kind<TAB>message` protocol is the one `doctor.sh` section 8 already reads with `while IFS=$'\t' read -r kind msg`.

- [ ] **Step 1: Write the failing tests**

Create `scripts/tests/test_hub_env.py`:

```python
from pathlib import Path

import pytest

import hub_env
from hublib.shellenv import HUB_BEGIN

RETIRED = """alias python='py'

# >>> ai-asset-registry env >>>
if [ -f "C:/old/ai-asset-registry/rhoai-restricted/.env" ]; then
  set -a; . "C:/old/ai-asset-registry/rhoai-restricted/.env"; set +a
  unset ANTHROPIC_API_KEY
fi
# <<< ai-asset-registry env <<<
"""


def make(tmp_path: Path, profile: str | None = None, env: bool = True):
    root, home = tmp_path / "repo", tmp_path / "home"
    (root / "restricted").mkdir(parents=True)
    home.mkdir()
    if env:
        (root / "restricted" / ".env").write_text("JIRA_SERVER=https://j\n",
                                                  encoding="utf-8")
    if profile is not None:
        (home / ".bashrc").write_text(profile, encoding="utf-8", newline="\n")
    return root, home


def run(root, home, mode, capsys):
    rc = hub_env.main([mode, "--root", str(root), "--home", str(home)])
    lines = [l.split("\t", 1) for l in capsys.readouterr().out.splitlines() if l]
    return rc, lines


def kinds(lines):
    return [k for k, _ in lines]


def msgs(lines):
    return " ".join(m for _, m in lines)


def test_check_never_fails_and_warns_when_unwired(tmp_path, capsys):
    root, home = make(tmp_path, profile="alias python='py'\n")
    rc, lines = run(root, home, "--check", capsys)
    assert rc == 0
    assert "warn" in kinds(lines)
    assert "rfe" in msgs(lines)          # says WHY it matters
    assert "doctor.sh setup" in msgs(lines)   # carries its own remediation


def test_check_reports_ok_when_wired(tmp_path, capsys):
    root, home = make(tmp_path)
    run(root, home, "--setup", capsys)
    rc, lines = run(root, home, "--check", capsys)
    assert rc == 0
    assert kinds(lines).count("warn") == 0 or "JIRA_" in msgs(lines)
    assert any(k == "ok" for k in kinds(lines))


def test_check_warns_about_the_retired_block(tmp_path, capsys):
    root, home = make(tmp_path, profile=RETIRED)
    _, lines = run(root, home, "--check", capsys)
    assert "ai-asset-registry" in msgs(lines)
    assert "warn" in kinds(lines)


def test_setup_writes_the_block_and_removes_the_retired_one(tmp_path, capsys):
    root, home = make(tmp_path, profile=RETIRED)
    rc, lines = run(root, home, "--setup", capsys)
    assert rc == 0
    text = (home / ".bashrc").read_text(encoding="utf-8")
    assert HUB_BEGIN in text
    assert "ai-asset-registry" not in text
    assert "unset" not in text
    assert "alias python='py'" in text
    assert "wrote" in kinds(lines)


def test_setup_backs_up_the_profile_before_writing(tmp_path, capsys):
    root, home = make(tmp_path, profile=RETIRED)
    run(root, home, "--setup", capsys)
    assert (home / ".bashrc.bak").read_text(encoding="utf-8") == RETIRED


def test_setup_is_idempotent_and_says_so(tmp_path, capsys):
    root, home = make(tmp_path, profile=RETIRED)
    run(root, home, "--setup", capsys)
    first = (home / ".bashrc").read_text(encoding="utf-8")
    _, lines = run(root, home, "--setup", capsys)
    assert (home / ".bashrc").read_text(encoding="utf-8") == first
    assert "wrote" not in kinds(lines)
    assert "ok" in kinds(lines)


def test_setup_creates_the_profile_when_absent(tmp_path, capsys):
    root, home = make(tmp_path, profile=None)
    run(root, home, "--setup", capsys)
    assert HUB_BEGIN in (home / ".bashrc").read_text(encoding="utf-8")


def test_setup_refuses_to_wire_a_missing_env(tmp_path, capsys):
    root, home = make(tmp_path, profile=None, env=False)
    rc, lines = run(root, home, "--setup", capsys)
    assert rc == 0
    assert not (home / ".bashrc").exists()
    assert "warn" in kinds(lines)
    assert "restricted/.env" in msgs(lines)


def test_exactly_one_mode_required(tmp_path):
    with pytest.raises(SystemExit):
        hub_env.main([])
    with pytest.raises(SystemExit):
        hub_env.main(["--check", "--setup"])
```

- [ ] **Step 2: Run the tests, verify they fail**

Run: `python -m pytest scripts/tests/test_hub_env.py -v`
Expected: FAIL, `ModuleNotFoundError: No module named 'hub_env'`

- [ ] **Step 3: Implement `scripts/hub_env.py`**

```python
"""CLI: shell-profile wiring for restricted/.env (doctor section 4).

  --check   report whether the profile sources the hub's restricted/.env and
            whether JIRA_* actually reach this shell
  --setup   back up ~/.bashrc, remove the retired ai-asset-registry block,
            write or repair the hub block (idempotent)

Why this exists: hub tooling self-loads restricted/.env, but the marketplace
rfe.* skills read os.environ with no fallback, so JIRA_* must be in the shell.

Emits TAB-separated "<kind>\\t<message>" lines for doctor.sh (kinds: ok, warn,
wrote), the protocol section 8 already reads. Exit code is always 0: missing
wiring is a WARN, never a FAIL.
"""
import argparse
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from hublib.shellenv import apply, scan

JIRA_KEYS = ("JIRA_SERVER", "JIRA_USER", "JIRA_TOKEN")


def _say(kind, message):
    print(f"{kind}\t{message}")


def _report_shell(env):
    missing = [k for k in JIRA_KEYS if not env.get(k)]
    if missing:
        _say("warn", f"{', '.join(missing)} not set in this shell "
                     f"(open a new shell after setup, or the rfe.* skills "
                     f"will prompt you to export them by hand)")
    else:
        _say("ok", "JIRA_* present in this shell")


def _report_profile(state, wired_msg):
    if state["hub_current"]:
        _say("ok", wired_msg)
    elif state["hub_block"]:
        _say("warn", "~/.bashrc sources a different repo path (moved clone?); "
                     "repair with: bash scripts/doctor.sh setup")
    else:
        _say("warn", "~/.bashrc does not source restricted/.env; the "
                     "marketplace rfe.* skills need JIRA_* in the shell. "
                     "Fix with: bash scripts/doctor.sh setup")
    if state["retired_block"]:
        _say("warn", "~/.bashrc still sources the RETIRED ai-asset-registry "
                     ".env; setup removes it (the hub's .env supersedes it)")
    for line in state["retired_unmarked"]:
        _say("warn", f"~/.bashrc references the retired ai-asset-registry repo "
                     f"outside a marked block, remove it by hand: {line}")


def _check(env_file, profile, env):
    text = profile.read_text(encoding="utf-8") if profile.is_file() else ""
    _report_profile(scan(text, env_file),
                    "~/.bashrc sources the hub's restricted/.env")
    _report_shell(env)
    return 0


def _setup(env_file, profile, env):
    text = profile.read_text(encoding="utf-8") if profile.is_file() else ""
    state = scan(text, env_file)
    updated = apply(text, env_file)
    if updated == text:
        _say("ok", "~/.bashrc already wired to restricted/.env (no change)")
        _report_shell(env)
        return 0
    if profile.is_file():
        backup = profile.with_suffix(profile.suffix + ".bak")
        backup.write_text(text, encoding="utf-8", newline="\n")
        _say("ok", f"backed up {profile.name} to {backup.name}")
    profile.write_text(updated, encoding="utf-8", newline="\n")
    if state["retired_block"]:
        _say("wrote", "removed the retired ai-asset-registry block from ~/.bashrc")
    _say("wrote", "~/.bashrc now sources the hub's restricted/.env")
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--setup", action="store_true")
    ap.add_argument("--root", help=argparse.SUPPRESS)   # tests only
    ap.add_argument("--home", help=argparse.SUPPRESS)   # tests only
    args = ap.parse_args(argv)
    if args.check == args.setup:
        ap.error("pick exactly one mode: --check | --setup")

    root = Path(args.root) if args.root else Path(__file__).resolve().parents[1]
    home = Path(args.home) if args.home else Path.home()
    env_file = root / "restricted" / ".env"
    profile = home / ".bashrc"

    if not env_file.is_file():
        _say("warn", "restricted/.env not found, nothing to wire "
                     "(copy it from your other machine, then re-run setup)")
        return 0
    if args.check:
        return _check(env_file, profile, os.environ)
    return _setup(env_file, profile, os.environ)


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 4: Run the tests, verify they pass**

Run: `python -m pytest scripts/tests/test_hub_env.py -v`
Expected: PASS, 9 tests.

- [ ] **Step 5: Commit**

```bash
git add scripts/hub_env.py scripts/tests/test_hub_env.py
git commit -m "feat(hub_env): --check/--setup CLI for the shell-profile wiring

Backs up ~/.bashrc, removes the retired ai-asset-registry block, upserts the
hub block. Idempotent, refuses to write when restricted/.env is absent, and
always exits 0 (missing wiring is a WARN, never a FAIL).

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

### Task 3: `hublib/slack.py` connectivity probe

**Files:**
- Create: `scripts/hublib/slack.py`
- Create: `scripts/tests/test_slack.py`

**Interfaces:**
- Produces:
  - `tokens_from_env() -> tuple[str, str]` - `(SLACK_XOXC_TOKEN, SLACK_XOXD_TOKEN)`.
  - `async auth_test(xoxc: str, xoxd: str, transport: httpx.AsyncBaseTransport | None = None) -> dict` - raw `auth.test` JSON.
  - `async probe(transport=None) -> tuple[str, str]` - `(kind, message)`; kind is `"ok"` or `"warn"`, never `"fail"`.
  - `AUTH_TEST_URL`.

Slack's `auth.test` returns HTTP 200 with `{"ok": false, "error": "invalid_auth"}` on bad tokens, so the JSON body is the signal, not the status code.

- [ ] **Step 1: Write the failing tests**

Create `scripts/tests/test_slack.py`:

```python
import asyncio

import httpx
import pytest

from hublib.slack import AUTH_TEST_URL, auth_test, probe, tokens_from_env


def run(coro):
    return asyncio.run(coro)


@pytest.fixture(autouse=True)
def clean_env(monkeypatch):
    monkeypatch.setenv("SLACK_XOXC_TOKEN", "xoxc-abc")
    monkeypatch.setenv("SLACK_XOXD_TOKEN", "xoxd-def")


def transport(handler):
    return httpx.MockTransport(handler)


def test_auth_test_sends_bearer_token_and_d_cookie():
    seen = {}

    def handler(request):
        seen["url"] = str(request.url)
        seen["auth"] = request.headers.get("authorization", "")
        seen["cookie"] = request.headers.get("cookie", "")
        return httpx.Response(200, json={"ok": True, "user": "peter", "team": "RH"})

    run(auth_test("xoxc-abc", "xoxd-def", transport=transport(handler)))
    assert seen["url"] == AUTH_TEST_URL
    assert seen["auth"] == "Bearer xoxc-abc"
    assert seen["cookie"] == "d=xoxd-def"


def test_auth_test_does_not_double_prefix_a_cookie_that_already_has_d():
    seen = {}

    def handler(request):
        seen["cookie"] = request.headers.get("cookie", "")
        return httpx.Response(200, json={"ok": True})

    run(auth_test("xoxc-abc", "d=xoxd-def", transport=transport(handler)))
    assert seen["cookie"] == "d=xoxd-def"


def test_probe_ok_reports_user_and_team():
    def handler(request):
        return httpx.Response(200, json={"ok": True, "user": "peter", "team": "RH"})

    kind, msg = run(probe(transport=transport(handler)))
    assert kind == "ok"
    assert "peter" in msg and "RH" in msg


def test_probe_invalid_auth_warns_and_explains_per_machine_tokens():
    def handler(request):
        return httpx.Response(200, json={"ok": False, "error": "invalid_auth"})

    kind, msg = run(probe(transport=transport(handler)))
    assert kind == "warn"
    assert "invalid_auth" in msg
    assert "docs/mcp-servers.md" in msg
    assert "machine" in msg          # says tokens do not travel between machines


def test_probe_network_error_warns_never_fails():
    def handler(request):
        raise httpx.ConnectError("offline")

    kind, msg = run(probe(transport=transport(handler)))
    assert kind == "warn"
    assert "offline" in msg.lower() or "unreachable" in msg.lower()


def test_probe_missing_tokens_warns(monkeypatch):
    monkeypatch.delenv("SLACK_XOXC_TOKEN", raising=False)
    kind, msg = run(probe())
    assert kind == "warn"
    assert "SLACK_XOXC_TOKEN" in msg


def test_probe_never_returns_fail():
    for payload in ({"ok": True}, {"ok": False, "error": "invalid_auth"},
                    {"ok": False, "error": "ratelimited"}):
        def handler(request, p=payload):
            return httpx.Response(200, json=p)
        kind, _ = run(probe(transport=transport(handler)))
        assert kind in ("ok", "warn")


def test_probe_never_prints_the_token_values():
    def handler(request):
        return httpx.Response(200, json={"ok": False, "error": "invalid_auth"})

    _, msg = run(probe(transport=transport(handler)))
    assert "xoxc-abc" not in msg and "xoxd-def" not in msg


def test_tokens_from_env():
    assert tokens_from_env() == ("xoxc-abc", "xoxd-def")
```

- [ ] **Step 2: Run the tests, verify they fail**

Run: `python -m pytest scripts/tests/test_slack.py -v`
Expected: FAIL, `ModuleNotFoundError: No module named 'hublib.slack'`

- [ ] **Step 3: Implement `scripts/hublib/slack.py`**

```python
"""Slack connectivity probe (doctor section 9).

The Slack MCP server authenticates with xoxc/xoxd browser session tokens (see
docs/mcp-servers.md). Doctor already checks that the server is REGISTERED;
registration is not validity. These tokens are per-login, so a copy carried
over from another machine can be silently dead, which is exactly the failure
R5 predicted for machine B.

WARN only, never FAIL: an offline machine must still reach 0 fail.
"""
from __future__ import annotations

import os

import httpx

AUTH_TEST_URL = "https://slack.com/api/auth.test"
TIMEOUT = 10.0
AUTH_ERRORS = ("invalid_auth", "not_authed", "token_revoked", "token_expired",
               "account_inactive")


def tokens_from_env() -> tuple[str, str]:
    return (os.environ.get("SLACK_XOXC_TOKEN", ""),
            os.environ.get("SLACK_XOXD_TOKEN", ""))


async def auth_test(
    xoxc: str,
    xoxd: str,
    transport: httpx.AsyncBaseTransport | None = None,
) -> dict:
    """Raw auth.test response. Slack answers HTTP 200 with ok:false on bad
    tokens, so the body is the signal, not the status code."""
    cookie = xoxd if xoxd.startswith("d=") else f"d={xoxd}"
    async with httpx.AsyncClient(timeout=TIMEOUT, transport=transport) as client:
        resp = await client.post(
            AUTH_TEST_URL,
            headers={"Authorization": f"Bearer {xoxc}", "Cookie": cookie},
        )
        resp.raise_for_status()
        return resp.json()


async def probe(transport: httpx.AsyncBaseTransport | None = None) -> tuple[str, str]:
    """(kind, message) for doctor. Token values are never included."""
    xoxc, xoxd = tokens_from_env()
    missing = [name for name, value in
               (("SLACK_XOXC_TOKEN", xoxc), ("SLACK_XOXD_TOKEN", xoxd)) if not value]
    if missing:
        return ("warn", f"{', '.join(missing)} missing in restricted/.env, so the "
                        f"slack MCP will not authenticate (see docs/mcp-servers.md)")
    try:
        data = await auth_test(xoxc, xoxd, transport=transport)
    except httpx.HTTPError as exc:
        return ("warn", f"slack unreachable ({exc.__class__.__name__}), offline? "
                        f"re-run: python scripts/hub_slack.py --check")
    if data.get("ok"):
        return ("ok", f"slack auth ok: {data.get('user', '?')} "
                      f"@ {data.get('team', '?')}")
    error = data.get("error", "unknown")
    if error in AUTH_ERRORS:
        return ("warn", f"slack auth failed ({error}). xoxc/xoxd are per-login "
                        f"session tokens and do not travel between machines: "
                        f"re-extract them on THIS machine per docs/mcp-servers.md")
    return ("warn", f"slack auth.test returned an error: {error}")
```

- [ ] **Step 4: Run the tests, verify they pass**

Run: `python -m pytest scripts/tests/test_slack.py -v`
Expected: PASS, 9 tests.

- [ ] **Step 5: Commit**

```bash
git add scripts/hublib/slack.py scripts/tests/test_slack.py
git commit -m "feat(slack): auth.test connectivity probe (WARN, never FAIL)

Doctor checks the slack MCP is registered; registration is not validity.
xoxc/xoxd are per-login session tokens that do not travel between machines,
which is the failure R5 predicted for machine B. The probe names it in one
line. Token values are never printed.

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

### Task 4: `scripts/hub_slack.py` CLI

**Files:**
- Create: `scripts/hub_slack.py`
- Create: `scripts/tests/test_hub_slack.py`

**Interfaces:**
- Consumes: `hublib.slack.probe` (Task 3), `hublib.shellenv.load_env` (Task 1).
- Produces: `main(argv=None) -> int`. Prints one `kind<TAB>message` line. Always exits 0.

- [ ] **Step 1: Write the failing tests**

Create `scripts/tests/test_hub_slack.py`:

```python
from pathlib import Path

import pytest

import hub_slack


def make_repo(tmp_path: Path, env_line: str = "SLACK_XOXC_TOKEN=xoxc-from-file\n"):
    (tmp_path / "restricted").mkdir(parents=True)
    (tmp_path / "restricted" / ".env").write_text(
        env_line + "SLACK_XOXD_TOKEN=xoxd-from-file\n", encoding="utf-8")
    return tmp_path


def test_check_prints_one_tab_separated_line(tmp_path, capsys, monkeypatch):
    async def fake_probe(transport=None):
        return ("ok", "slack auth ok: peter @ RH")

    monkeypatch.setattr(hub_slack, "probe", fake_probe)
    rc = hub_slack.main(["--check", "--root", str(make_repo(tmp_path))])
    out = capsys.readouterr().out.strip()
    assert rc == 0
    assert out == "ok\tslack auth ok: peter @ RH"


def test_check_exits_zero_even_when_the_probe_warns(tmp_path, capsys, monkeypatch):
    async def fake_probe(transport=None):
        return ("warn", "slack auth failed (invalid_auth)")

    monkeypatch.setattr(hub_slack, "probe", fake_probe)
    rc = hub_slack.main(["--check", "--root", str(make_repo(tmp_path))])
    assert rc == 0
    assert capsys.readouterr().out.startswith("warn\t")


def test_check_loads_slack_tokens_from_restricted_env(tmp_path, capsys, monkeypatch):
    monkeypatch.delenv("SLACK_XOXC_TOKEN", raising=False)
    monkeypatch.delenv("SLACK_XOXD_TOKEN", raising=False)
    seen = {}

    async def fake_probe(transport=None):
        import os
        seen["xoxc"] = os.environ.get("SLACK_XOXC_TOKEN")
        return ("ok", "fine")

    monkeypatch.setattr(hub_slack, "probe", fake_probe)
    hub_slack.main(["--check", "--root", str(make_repo(tmp_path))])
    assert seen["xoxc"] == "xoxc-from-file"


def test_check_is_required(tmp_path):
    with pytest.raises(SystemExit):
        hub_slack.main([])
```

- [ ] **Step 2: Run the tests, verify they fail**

Run: `python -m pytest scripts/tests/test_hub_slack.py -v`
Expected: FAIL, `ModuleNotFoundError: No module named 'hub_slack'`

- [ ] **Step 3: Implement `scripts/hub_slack.py`**

```python
"""CLI: Slack connectivity probe (doctor section 9). Read-only against Slack.

  --check   authenticate the xoxc/xoxd tokens from restricted/.env against
            slack.com/api/auth.test

Emits one TAB-separated "<kind>\\t<message>" line (kinds: ok, warn). Exit code
is always 0: a failed probe is a WARN, never a FAIL, so an offline machine
still reaches 0 fail.
"""
import argparse
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from hublib.shellenv import load_env
from hublib.slack import probe


def main(argv=None):
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true", required=True)
    ap.add_argument("--root", help=argparse.SUPPRESS)   # tests only
    args = ap.parse_args(argv)

    root = Path(args.root) if args.root else Path(__file__).resolve().parents[1]
    load_env(root, prefixes=("SLACK_",))
    kind, message = asyncio.run(probe())
    print(f"{kind}\t{message}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 4: Run the tests, verify they pass**

Run: `python -m pytest scripts/tests/test_hub_slack.py -v`
Expected: PASS, 4 tests.

- [ ] **Step 5: Run the full suite**

Run: `python -m pytest scripts/tests -q`
Expected: PASS, 193 tests (168 + 12 + 9 + 9 + 4 = 202; confirm the actual count and use it).

- [ ] **Step 6: Commit**

```bash
git add scripts/hub_slack.py scripts/tests/test_hub_slack.py
git commit -m "feat(hub_slack): --check CLI for the slack auth probe

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

### Task 5: Wire both into `doctor.sh` and update the docs

**Files:**
- Modify: `scripts/doctor.sh` (section 4 header + body; section 9 header + tail)
- Modify: `docs/setup.md`
- Modify: `docs/tooling.md`

**Interfaces:**
- Consumes: `scripts/hub_env.py --check|--setup` (Task 2), `scripts/hub_slack.py --check` (Task 4). Both emit `kind<TAB>message`.

No renumbering: section 4 already owns `restricted/.env`, section 9 already owns the Slack runtime.

- [ ] **Step 1: Rename the section 4 header**

In `scripts/doctor.sh`, change line 124:

```bash
echo "[4] restricted/.env + shell wiring"
```

- [ ] **Step 2: Add the wiring call at the end of section 4's then-branch**

In `scripts/doctor.sh`, immediately after the Jira probe's closing `fi` (the block ending `warn "jira unreachable or auth failed ..."`) and BEFORE the `else` that handles a missing `.env`, insert:

```bash
  # Shell wiring (backlog #19). Hub tooling self-loads restricted/.env, but the
  # marketplace rfe.* scripts read os.environ with no fallback, so JIRA_* must
  # reach every shell. hub_env.py owns the ~/.bashrc block and removes the
  # retired ai-asset-registry one. Logic lives in python because it is tested;
  # idempotent profile editing is where bash quietly gets it wrong.
  if [ "$MODE" = "setup" ]; then ENV_MODE="--setup"; else ENV_MODE="--check"; fi
  while IFS=$'\t' read -r kind msg; do
    case "$kind" in
      ok)    ok "$msg" ;;
      wrote) ok "$msg (open a new shell for it to take effect)" ;;
      warn)  warn "$msg" ;;
    esac
  done < <(python "$ROOT/scripts/hub_env.py" $ENV_MODE 2>/dev/null)
```

- [ ] **Step 3: Rename the section 9 header and append the auth probe**

In `scripts/doctor.sh`, change line 324:

```bash
echo "[9] slack MCP runtime (podman) + auth probe"
```

Then append at the very end of section 9 (after its final `fi`, before `echo "[10] git pre-commit hook"`):

```bash
# Auth probe (backlog #19). Section 8 proves the server is REGISTERED;
# registration is not validity. xoxc/xoxd are per-login session tokens that do
# not travel between machines, the exact gap R5 predicted for machine B.
# WARN only, so an offline machine still reaches 0 fail.
while IFS=$'\t' read -r kind msg; do
  case "$kind" in
    ok)   ok "$msg" ;;
    warn) warn "$msg" ;;
  esac
done < <(python "$ROOT/scripts/hub_slack.py" --check 2>/dev/null)
```

- [ ] **Step 4: Verify the doctor runs clean on machine A**

Run: `bash scripts/doctor.sh check`
Expected: `0 fail`. Section 4 now WARNs that `~/.bashrc` sources the retired `ai-asset-registry` `.env` (that is the live bug, still unfixed at this point). Section 9 prints a slack auth line.

- [ ] **Step 5: Update `docs/setup.md`**

Replace step 7 and step 8 with:

```markdown
7. Re-run `bash scripts/doctor.sh setup` - with `.env` in place it also
   writes the Slack + Google Workspace MCP servers into your Claude config,
   prepares the Slack podman runtime (traps and manual steps, e.g. the podman
   engine install: [/docs/mcp-servers.md](/docs/mcp-servers.md)), and wires
   `restricted/.env` into `~/.bashrc` so `JIRA_*` reaches every shell (the
   marketplace `rfe.*` skills read the environment directly and have no
   fallback). Then **open a new shell** and restart Claude Code once more.
8. Verify: `bash scripts/doctor.sh check` -> `0 fail`. You're done.

Note: the `~/.bashrc` wiring reaches Claude Code's Bash tool, not its
PowerShell tool. If a skill runs Jira scripts through PowerShell it will not
see `JIRA_*`; hub scripts self-load `restricted/.env` and are unaffected.
```

- [ ] **Step 6: Update `docs/tooling.md`**

Find the doctor section-by-section reference and update the two entries:

- Section 4: now `restricted/.env + shell wiring`. Add: presence of `JIRA_*`, the live Jira probe (`hub_jira.py --check`), and the `~/.bashrc` block (`hub_env.py`), which `setup` writes and which removes the retired `ai-asset-registry` block. Note `setup` backs up to `~/.bashrc.bak`.
- Section 9: now `slack MCP runtime (podman) + auth probe`. Add: `hub_slack.py --check` calls `auth.test`; WARN on failure because xoxc/xoxd are per-login tokens that do not travel between machines.

- [ ] **Step 7: Run the full verification suite**

Run: `python -m pytest scripts/tests -q && python scripts/hub_lint.py && python scripts/hub_index.py --check`
Expected: all tests pass, `0 error(s)`, `0 stale file(s)`.

- [ ] **Step 8: Commit**

```bash
git add scripts/doctor.sh docs/setup.md docs/tooling.md
git commit -m "feat(doctor): shell wiring in section 4, slack auth probe in section 9

Closes backlog #19. Sections are extended, not renumbered: section 4 already
owns restricted/.env and section 9 already owns the slack runtime.

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

### Task 6: Fix machine A, then push

The latent bug from the spec: A's `~/.bashrc` sources the retired repo's `.env`. This task is where the tooling built above actually repairs it.

**Files:** none in the repo. This mutates `~/.bashrc` on machine A.

- [ ] **Step 1: Record the before-state**

Run: `cat ~/.bashrc`
Expected: the `# >>> ai-asset-registry env >>>` block is present, pointing at `C:/Users/peter/Code/rh/ai-asset-registry/rhoai-restricted/.env`, and includes the `unset CLAUDE_CODE_USE_VERTEX ...` line.

- [ ] **Step 2: Run the doctor in setup mode**

Run: `bash scripts/doctor.sh setup`
Expected: section 4 reports a backup, the removal of the retired block, and the new hub block.

- [ ] **Step 3: Verify the repair**

Run: `cat ~/.bashrc && echo "--- backup:" && cat ~/.bashrc.bak`
Expected: `~/.bashrc` contains the `# >>> rhoai-agentic-hub env >>>` block pointing at `C:/Users/peter/code/rh/rhoai-agentic-hub/restricted/.env`, no `ai-asset-registry` reference, no `unset` line, and `alias python='py'` still on line 1. The `.bak` holds the original.

- [ ] **Step 4: Verify the wiring works in a fresh shell**

Run: `bash -lc 'echo "JIRA_SERVER=${JIRA_SERVER:-UNSET}"'`
Expected: `JIRA_SERVER=https://redhat.atlassian.net`

- [ ] **Step 5: Confirm the retired repo is no longer load-bearing**

Run: `bash -lc 'python scripts/hub_jira.py --check'`
Expected: `jira ok: authenticated as ...`, now sourced from the hub's own `.env`.

- [ ] **Step 6: Full check, then push**

Run: `bash scripts/doctor.sh check`
Expected: `0 fail`, section 4 all OK, section 9 prints the slack auth result (OK, or a WARN naming the real token state on A).

```bash
git push origin main
```

- [ ] **Step 7: Capture the finding**

Fire the `hub.capture` skill with the A-bashrc finding: the `rfe.*` skills depended on the retired `ai-asset-registry` clone surviving on disk, the doctor now owns the wiring, and the dependency is severed. This is a durable machine fact, so it belongs in the tracked store rather than in this plan.

---

### Task 7: R5 steps 2-4 on machine B

Executed ON MACHINE B, in a Claude Code session opened on the hub there. This is the measurement half: it produces the evidence #14 has been waiting for. B is a machine where the wiring genuinely does not exist, so it is a real test of Tasks 1-5, not a simulation.

**Files:**
- Modify: `docs/enhancements.md` (`## R5 outcome`, #19 to Done, #14 annotated)
- Modify: `memory/log.md` (via `hub.capture` or `hub.consolidate`, never by hand)

- [ ] **Step 1: Pull and run the doctor cold on B**

Run on B: `git pull && bash scripts/doctor.sh check`
Record verbatim: every WARN and FAIL. Expected new signal, and the whole point of the exercise:
- section 4 WARNs that `~/.bashrc` does not source `restricted/.env` (B never had it)
- section 9 WARNs `invalid_auth` if A's Slack tokens do not travel, or reports OK if they do. **Either answer is a result.** This is the first time that question has ever been answered.

- [ ] **Step 2: Run setup on B and confirm it converges**

Run on B: `bash scripts/doctor.sh setup`, open a new shell, then `bash scripts/doctor.sh check`
Expected: `0 fail`. Record anything that needed a human hand (podman engine install, token re-extraction, restart). Every such step is either a doctor gap or a `docs/setup.md` gap, so file it.

- [ ] **Step 3: R5 step 2, the round trip**

On B: run one real `hub.capture` (gated, committed, pushed).
On A: `git pull && python scripts/hub_index.py --check`
Expected: `0 stale file(s)`.
Then reverse the direction: capture on A, pull on B, check.
Record: did anything drift, did indexes stay clean both ways.

- [ ] **Step 4: R5 step 3, the restricted-tier reality check (this is the #14 evidence)**

Answer these three questions with specifics, not impressions:
1. Which `restricted/` files did B actually need day to day? (`.env` alone, or the `features/` and `memory/` trees too?)
2. How far had A's and B's copies drifted? Compare file lists and modification times, never contents into a tracked file.
3. Was manual copying tolerable, or did it fail in practice?

- [ ] **Step 5: R5 step 4, the push race**

Deliberately commit on both A and B, push both, and resolve the resulting race by following only what the docs say. Record whether the documented rebase discipline was sufficient for a human with no extra context.

- [ ] **Step 6: Write the outcome**

Append a `## R5 outcome` subsection to the R5 section of `docs/enhancements.md` covering: what broke, what was fixed, what is now parked. It MUST state the two non-goals plainly, so nobody later reads R5 as proving more than it did:
- step 1 (cold path) was not executed, because B was warm; machine C will verify itself through `doctor.sh check`
- no cross-OS signal, because B is Windows and Git Bash like A

Then in the priority table: move #19 to Done, and annotate #14 with the evidence from Step 4 (a recommendation, not yet a ruling).

- [ ] **Step 7: Log it**

Fire `hub.capture` (or `hub.consolidate` if the session produced scratch) for the R5 log line and any durable facts the run surfaced. Never hand-edit `memory/log.md`.

---

## Self-Review

**Spec coverage.** Every spec section maps to a task: `shellenv` (Task 1), `hub_env` CLI (Task 2), `slack.py` (Task 3), `hub_slack` CLI (Task 4), doctor sections and docs (Task 5), the A-machine repair the spec's Problem section identified (Task 6), sequencing steps 1-5 and the R5 measurement (Task 7). The spec's "Testing" section is satisfied by the named cases in Tasks 1-4 (retired-line removal, no-op re-run, moved-path repair, backup, `ok:true`, `invalid_auth`, missing tokens, network error, WARN-never-FAIL). Non-goals are carried into Task 7 Step 6 so the outcome note cannot overclaim.

**Deviation.** The spec said doctor section numbering shifts; this plan extends sections 4 and 9 instead. Flagged in File Structure with rationale. If you want the renumber, say so and Task 5 changes.

**Type consistency.** `load_env(root, prefixes)` is defined in Task 1 and consumed with the same signature in Tasks 2 and 4. `scan()` returns exactly the four keys Task 2 reads (`hub_block`, `hub_current`, `retired_block`, `retired_unmarked`). `probe()` returns `(kind, message)` in Task 3 and is consumed as such in Task 4. The `kind<TAB>message` protocol is identical across `hub_env.py`, `hub_slack.py`, and the two `doctor.sh` `while IFS=$'\t'` loops, and matches the one section 8 already uses.

**Test count.** Task 4 Step 5 says "confirm the actual count": 168 existing + 12 + 9 + 9 + 4 = 202 expected.
