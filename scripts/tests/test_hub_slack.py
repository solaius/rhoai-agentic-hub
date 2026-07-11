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


def test_check_protects_the_protocol_when_the_probe_message_has_a_tab_and_newline(
        tmp_path, capsys, monkeypatch):
    async def fake_probe(transport=None):
        return ("warn", "slack said\tsomething odd\nacross two lines")

    monkeypatch.setattr(hub_slack, "probe", fake_probe)
    rc = hub_slack.main(["--check", "--root", str(make_repo(tmp_path))])
    out = capsys.readouterr().out
    assert rc == 0
    assert out.count("\t") == 1
    assert out.count("\n") == 1
