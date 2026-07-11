import json
from pathlib import Path

import pytest

import hub_triage


def write(root: Path, rel: str, text: str):
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8", newline="\n")
    return p


def make_repo(tmp_path: Path) -> Path:
    write(tmp_path, "features/features.yaml",
          "features:\n"
          "- id: mcp-registry\n  title: R\n  description: d\n"
          "  jira:\n    jql: 'project = RHAIRFE'\n"
          "- id: bare\n  title: B\n  description: d\n")
    return tmp_path


def test_exactly_one_mode_required():
    with pytest.raises(SystemExit):
        hub_triage.main([])
    with pytest.raises(SystemExit):
        hub_triage.main(["--scan", "x", "--apply", "y"])


def test_scan_requires_out_dir(tmp_path):
    with pytest.raises(SystemExit):
        hub_triage.main(["--scan", "mcp-registry",
                         "--root", str(make_repo(tmp_path))])


def test_scan_unknown_feature_exits_2(tmp_path, capsys):
    rc = hub_triage.main(["--scan", "nope", "--out", str(tmp_path / "o"),
                          "--root", str(make_repo(tmp_path))])
    assert rc == 2
    assert "unknown feature" in capsys.readouterr().out


def test_scan_without_stored_scope_exits_2(tmp_path, capsys):
    rc = hub_triage.main(["--scan", "bare", "--out", str(tmp_path / "o"),
                          "--root", str(make_repo(tmp_path))])
    assert rc == 2
    assert "no stored jira scope" in capsys.readouterr().out


def test_plan_mode_prints_the_gate_table_and_touches_no_network(tmp_path, capsys):
    rows = [{
        "key": "A-1", "summary": "s", "status": "New", "assignee": None,
        "priority": None, "labels": [], "components": [], "updated": "2026-07-01",
        "created": "2026-01-01", "links": [], "transitions": [],
        "flags": [], "classification": "needs_attention",
        "suggestion": {"action": "backlog", "reason": "r"},
    }]
    rows_p = tmp_path / "rows.json"
    rows_p.write_text(json.dumps(rows), encoding="utf-8")
    dec_p = tmp_path / "d.json"
    dec_p.write_text(json.dumps({
        "feature": "mcp-registry",
        "decisions": {"A-1": {"action": "backlog", "current_labels": []},
                      "A-2": {"action": "assign"}},
    }), encoding="utf-8")

    rc = hub_triage.main(["--plan", str(dec_p), "--rows", str(rows_p)])
    out = capsys.readouterr().out
    assert rc == 0
    assert "LABELS (1)" in out
    assert "+pm-backlogged" in out
    assert "REJECTED (1)" in out
    assert "not in the scan" in out


def test_apply_requires_rows_and_feature(tmp_path):
    with pytest.raises(SystemExit):
        hub_triage.main(["--apply", str(tmp_path / "d.json")])


def test_plan_coerces_a_numeric_release_to_a_string(tmp_path, capsys):
    # A hand-edited decisions file can carry "release": 3.6 as a JSON number
    # rather than a string. plan_decisions() calls .strip() on release, so an
    # unnormalized number would raise AttributeError. The CLI must coerce it
    # to "3.6" before handing it to plan_decisions, and plan it successfully.
    rows = [{
        "key": "A-1", "summary": "s", "status": "New", "assignee": None,
        "priority": None, "labels": [], "components": [], "updated": "2026-07-01",
        "created": "2026-01-01", "links": [], "transitions": [],
        "flags": [], "classification": "needs_attention",
        "suggestion": {"action": "backlog", "reason": "r"},
    }]
    rows_p = tmp_path / "rows.json"
    rows_p.write_text(json.dumps(rows), encoding="utf-8")
    dec_p = tmp_path / "d.json"
    dec_p.write_text(json.dumps({
        "feature": "mcp-registry",
        "decisions": {"A-1": {"action": "roadmap", "release": 3.6}},
    }), encoding="utf-8")

    rc = hub_triage.main(["--plan", str(dec_p), "--rows", str(rows_p)])
    out = capsys.readouterr().out
    assert rc == 0
    assert "LABELS (1)" in out
    assert "+3.6-candidate" in out


def test_plan_rejects_a_malformed_decisions_payload_without_a_traceback(
        tmp_path, capsys):
    rows_p = tmp_path / "rows.json"
    rows_p.write_text(json.dumps([]), encoding="utf-8")
    dec_p = tmp_path / "d.json"
    dec_p.write_text(json.dumps(["not", "a", "dict"]), encoding="utf-8")

    rc = hub_triage.main(["--plan", str(dec_p), "--rows", str(rows_p)])
    out = capsys.readouterr().out
    assert rc == 2
    assert "ERROR" in out
