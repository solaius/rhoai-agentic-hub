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


def _one_row_no_labels():
    # labels: [] so plan_decisions falls through to decision.get(
    # "current_labels") - the exact path a malformed current_labels blows up
    # in if the CLI does not normalize it first.
    return [{
        "key": "A-1", "summary": "s", "status": "New", "assignee": None,
        "priority": None, "labels": [], "components": [], "updated": "2026-07-01",
        "created": "2026-01-01", "links": [], "transitions": [],
        "flags": [], "classification": "needs_attention",
        "suggestion": {"action": "backlog", "reason": "r"},
    }]


@pytest.mark.parametrize("bad_current_labels", [5, True, "mcp", 3.6, {"a": 1}])
def test_plan_ignores_a_non_list_current_labels_without_a_traceback(
        tmp_path, capsys, bad_current_labels):
    # A hand-edited decisions file can carry a type-confused current_labels
    # (int, bool, str, float, dict) instead of a list. plan_decisions() does
    # list(row.get("labels") or decision.get("current_labels") or []), so an
    # un-normalized non-iterable raises TypeError. The CLI must omit it -
    # current_labels is advisory only - and plan successfully instead.
    rows_p = tmp_path / "rows.json"
    rows_p.write_text(json.dumps(_one_row_no_labels()), encoding="utf-8")
    dec_p = tmp_path / "d.json"
    dec_p.write_text(json.dumps({
        "feature": "mcp-registry",
        "decisions": {"A-1": {"action": "backlog",
                              "current_labels": bad_current_labels}},
    }), encoding="utf-8")

    rc = hub_triage.main(["--plan", str(dec_p), "--rows", str(rows_p)])
    out = capsys.readouterr().out
    assert rc == 0
    assert "LABELS (1)" in out
    assert "+pm-backlogged" in out


def test_plan_drops_junk_entries_from_a_current_labels_list(tmp_path, capsys):
    # A list current_labels can still carry junk entries (a stray dict, a
    # null). Those must not crash and must not corrupt the "label already
    # present" skip check - the row's own (empty) labels list is what
    # actually governs skip-vs-plan here.
    rows_p = tmp_path / "rows.json"
    rows_p.write_text(json.dumps(_one_row_no_labels()), encoding="utf-8")
    dec_p = tmp_path / "d.json"
    dec_p.write_text(json.dumps({
        "feature": "mcp-registry",
        "decisions": {"A-1": {"action": "backlog",
                              "current_labels": ["mcp", 3, None]}},
    }), encoding="utf-8")

    rc = hub_triage.main(["--plan", str(dec_p), "--rows", str(rows_p)])
    out = capsys.readouterr().out
    assert rc == 0
    assert "LABELS (1)" in out
    assert "+pm-backlogged" in out


@pytest.mark.parametrize("bad_decision", ["backlog", None, 5, ["backlog"]])
def test_plan_handles_a_non_dict_decision_value_without_a_traceback(
        tmp_path, capsys, bad_decision):
    # A decision entry whose VALUE is not a dict at all (e.g. {"A-1":
    # "backlog"} or {"A-1": null}) must not crash. _normalize_decisions
    # already replaces it with {}, which plan_decisions treats as an
    # implicit "skip".
    rows_p = tmp_path / "rows.json"
    rows_p.write_text(json.dumps(_one_row_no_labels()), encoding="utf-8")
    dec_p = tmp_path / "d.json"
    dec_p.write_text(json.dumps({
        "feature": "mcp-registry",
        "decisions": {"A-1": bad_decision},
    }), encoding="utf-8")

    rc = hub_triage.main(["--plan", str(dec_p), "--rows", str(rows_p)])
    out = capsys.readouterr().out
    assert rc == 0
    assert "SKIPPED (1)" in out
