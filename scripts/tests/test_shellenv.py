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
