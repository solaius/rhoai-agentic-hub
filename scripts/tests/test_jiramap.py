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
