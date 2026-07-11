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

MALFORMED = f"keep me\n{HUB_BEGIN}\nhalf a block\n"


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


def test_check_reports_ok_when_wired(tmp_path, capsys, monkeypatch):
    root, home = make(tmp_path)
    run(root, home, "--setup", capsys)
    monkeypatch.delenv("JIRA_SERVER", raising=False)
    monkeypatch.delenv("JIRA_USER", raising=False)
    monkeypatch.delenv("JIRA_TOKEN", raising=False)
    rc, lines = run(root, home, "--check", capsys)
    assert rc == 0
    assert ("ok", "~/.bashrc sources the hub's restricted/.env") in [
        (k, m) for k, m in lines]


def test_check_warns_about_the_retired_block(tmp_path, capsys):
    root, home = make(tmp_path, profile=RETIRED)
    _, lines = run(root, home, "--check", capsys)
    assert "ai-asset-registry" in msgs(lines)
    assert "warn" in kinds(lines)


def test_setup_warns_about_an_unmarked_retired_line_and_still_writes(tmp_path, capsys):
    # An unmarked bare line survives --setup on purpose (setup only removes
    # the MARKED retired block); it must not survive SILENTLY. --setup has
    # to say what it left behind, on both the "wrote" path and the
    # "already wired, no change" path.
    unmarked_line = "still using ai-asset-registry directly, not through the hub"
    profile = f"alias python='py'\n{unmarked_line}\n"
    root, home = make(tmp_path, profile=profile)
    rc, lines = run(root, home, "--setup", capsys)
    assert rc == 0
    assert unmarked_line in msgs(lines)
    assert "warn" in kinds(lines)
    text = (home / ".bashrc").read_text(encoding="utf-8")
    assert HUB_BEGIN in text
    assert "wrote" in kinds(lines)


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


def test_check_warns_unwired_when_env_present_and_no_profile_at_all(tmp_path, capsys):
    # Machine B: restricted/.env was copied over, but this machine has never
    # had a ~/.bashrc at all (not just unwired). --check must still warn
    # about the missing wiring (not crash, not silently say nothing) and
    # stay read-only (return 0, no file written).
    root, home = make(tmp_path, profile=None)
    rc, lines = run(root, home, "--check", capsys)
    assert rc == 0
    assert "warn" in kinds(lines)
    assert "doctor.sh setup" in msgs(lines)
    assert not (home / ".bashrc").exists()


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


def test_setup_against_malformed_profile_does_not_write_and_warns(tmp_path, capsys):
    root, home = make(tmp_path, profile=MALFORMED)
    rc, lines = run(root, home, "--setup", capsys)
    assert rc == 0
    assert (home / ".bashrc").read_text(encoding="utf-8") == MALFORMED
    assert "warn" in kinds(lines)
    assert not (home / ".bashrc.bak").exists()


def test_check_against_malformed_profile_warns_to_fix_by_hand(tmp_path, capsys):
    root, home = make(tmp_path, profile=MALFORMED)
    rc, lines = run(root, home, "--check", capsys)
    assert rc == 0
    assert "warn" in kinds(lines)
    assert "fix" in msgs(lines).lower() and "hand" in msgs(lines).lower()


def test_check_protects_the_protocol_when_a_retired_reference_line_has_a_tab(
        tmp_path, capsys):
    tab_line = "\tstill using ai-asset-registry\tclone directly, not through the hub"
    root, home = make(tmp_path, profile=f"keep me\n{tab_line}\n")
    rc = hub_env.main(["--check", "--root", str(root), "--home", str(home)])
    out = capsys.readouterr().out
    lines = out.splitlines()
    assert rc == 0
    matching = [l for l in lines if "still using ai-asset-registry" in l]
    assert len(matching) == 1
    assert matching[0].count("\t") == 1
