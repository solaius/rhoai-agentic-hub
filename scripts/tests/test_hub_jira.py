import asyncio
from pathlib import Path

import httpx
import pytest
import yaml

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


def test_audit_is_a_mode(tmp_path):
    # --audit combined with another mode is rejected
    with pytest.raises(SystemExit):
        hub_jira.main(["--audit", "RHAIRFE-1", "--check"])


def test_audit_needs_no_out_dir(tmp_path, monkeypatch):
    # --audit is read-only and prints to stdout, so unlike --sweep/--sync
    # it must NOT require --out. Argparse must not reject it.
    calls = {}

    def fake_run(coro):
        coro.close()
        calls["ran"] = True
        return 0

    monkeypatch.setattr(hub_jira.asyncio, "run", fake_run)
    rc = hub_jira.main(["--audit", "RHAIRFE-1",
                        "--root", str(make_repo(tmp_path))])
    assert rc == 0
    assert calls["ran"] is True


def _issue_response(with_parent=True):
    parent = None
    if with_parent:
        parent = {
            "key": "RHAISTRAT-1",
            "fields": {
                "summary": "Outcome summary",
                "issuetype": {"name": "Outcome"},
            },
        }
    return {
        "key": "RHAISTRAT-100",
        "fields": {
            "summary": "[Feat] Example feature",
            "status": {"name": "In Progress"},
            "assignee": {"displayName": "A Person"},
            "priority": {"name": "High"},
            "issuetype": {"name": "Feature"},
            "components": [],
            "labels": [],
            "fixVersions": [],
            "parent": parent,
            "description": None,
            "issuelinks": [
                {
                    "type": {"outward": "documents", "inward": "is documented by"},
                    "outwardIssue": {
                        "key": "CCS-1",
                        "fields": {
                            "summary": "[ccs] doc task",
                            "issuetype": {"name": "Task"},
                            "status": {"name": "Open"},
                        },
                    },
                }
            ],
        },
    }


def _run_audit(monkeypatch, key, handler):
    monkeypatch.setenv("JIRA_SERVER", "https://jira.example.com")
    monkeypatch.setenv("JIRA_USER", "user@example.com")
    monkeypatch.setenv("JIRA_TOKEN", "tok")
    transport = httpx.MockTransport(handler)

    async def case():
        return await hub_jira._audit(key, transport=transport)

    return asyncio.run(case())


def test_audit_parent_carries_key_and_type(tmp_path, capsys, monkeypatch):
    def handler(request):
        if "/issue/RHAISTRAT-100" in str(request.url):
            return httpx.Response(200, json=_issue_response())
        if "/search/jql" in str(request.url):
            return httpx.Response(200, json={"issues": [], "isLast": True})
        raise AssertionError(f"unexpected request: {request.url}")

    rc = _run_audit(monkeypatch, "RHAISTRAT-100", handler)
    assert rc == 0
    dump = yaml.safe_load(capsys.readouterr().out)
    assert dump["parent"]["key"] == "RHAISTRAT-1"
    assert dump["parent"]["type"] == "Outcome"
    assert dump["parent"]["summary"] == "Outcome summary"


def test_audit_link_records_carry_summary(tmp_path, capsys, monkeypatch):
    def handler(request):
        if "/issue/RHAISTRAT-100" in str(request.url):
            return httpx.Response(200, json=_issue_response())
        if "/search/jql" in str(request.url):
            return httpx.Response(200, json={"issues": [], "isLast": True})
        raise AssertionError(f"unexpected request: {request.url}")

    rc = _run_audit(monkeypatch, "RHAISTRAT-100", handler)
    assert rc == 0
    dump = yaml.safe_load(capsys.readouterr().out)
    assert dump["links"][0]["summary"] == "[ccs] doc task"


def test_audit_children_populated_on_success(tmp_path, capsys, monkeypatch):
    def handler(request):
        if "/issue/RHAISTRAT-100" in str(request.url):
            return httpx.Response(200, json=_issue_response())
        if "/search/jql" in str(request.url):
            return httpx.Response(200, json={
                "issues": [{
                    "key": "RHAIENG-1",
                    "fields": {
                        "summary": "Epic 1",
                        "status": {"name": "Open"},
                        "issuetype": {"name": "Epic"},
                    },
                }],
                "isLast": True,
            })
        raise AssertionError(f"unexpected request: {request.url}")

    rc = _run_audit(monkeypatch, "RHAISTRAT-100", handler)
    assert rc == 0
    dump = yaml.safe_load(capsys.readouterr().out)
    assert dump["children_lookup"] == "ok"
    assert dump["children"] == [{
        "key": "RHAIENG-1", "type": "Epic", "status": "Open", "summary": "Epic 1",
    }]


def test_audit_failing_children_lookup_degrades_gracefully(tmp_path, capsys, monkeypatch):
    def handler(request):
        if "/issue/RHAISTRAT-100" in str(request.url):
            return httpx.Response(200, json=_issue_response())
        if "/search/jql" in str(request.url):
            return httpx.Response(500)
        raise AssertionError(f"unexpected request: {request.url}")

    rc = _run_audit(monkeypatch, "RHAISTRAT-100", handler)
    assert rc == 0
    dump = yaml.safe_load(capsys.readouterr().out)
    assert dump["children"] == []
    assert dump["children_lookup"].startswith("failed:")
