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
