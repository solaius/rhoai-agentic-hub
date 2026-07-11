import datetime

from hublib import triage

TODAY = datetime.date(2026, 7, 11)


def row(**kw):
    base = {
        "key": "RHAIRFE-1",
        "summary": "A thing",
        "status": "New",
        "assignee": None,
        "priority": "Normal",
        "labels": [],
        "components": ["AI Hub"],
        "updated": "2026-07-10",
        "created": "2026-01-01",
        "links": [],
        "transitions": [],
    }
    base.update(kw)
    return base


# -- issue_to_row --

def test_issue_to_row_normalizes_jira_shape():
    issue = {
        "key": "RHAIRFE-9",
        "fields": {
            "summary": "Add a dashboard",
            "status": {"name": "Stakeholder Review"},
            "assignee": {"displayName": "Peter"},
            "priority": {"name": "Major"},
            "labels": ["mcp"],
            "components": [{"name": "AI Hub"}],
            "updated": "2026-05-01T10:00:00.000+0000",
            "created": "2026-01-01T10:00:00.000+0000",
            "issuelinks": [
                {"type": {"outward": "clones"},
                 "outwardIssue": {"key": "RHAISTRAT-5",
                                  "fields": {"issuetype": {"name": "Feature"}}}},
            ],
        },
    }
    r = triage.issue_to_row(issue)
    assert r["key"] == "RHAIRFE-9"
    assert r["status"] == "Stakeholder Review"
    assert r["assignee"] == "Peter"
    assert r["labels"] == ["mcp"]
    assert r["components"] == ["AI Hub"]
    assert r["updated"] == "2026-05-01"          # date only, no time
    assert r["links"] == [{"type": "clones", "key": "RHAISTRAT-5",
                           "issuetype": "Feature"}]


# -- flag_staleness --

def test_fresh_issue_has_no_staleness_flags():
    assert triage.flag_staleness(row(assignee="Peter"), TODAY) == []


def test_no_update_flag_fires_past_90_days():
    flags = triage.flag_staleness(
        row(updated="2026-01-01", assignee="Peter"), TODAY)
    assert "no_update_191d" in flags


def test_no_update_flag_does_not_fire_at_89_days():
    updated = (TODAY - datetime.timedelta(days=89)).isoformat()
    flags = triage.flag_staleness(row(updated=updated, assignee="Peter"), TODAY)
    assert not any(f.startswith("no_update_") for f in flags)


def test_stakeholder_review_stale_needs_270_days():
    updated = (TODAY - datetime.timedelta(days=280)).isoformat()
    flags = triage.flag_staleness(
        row(status="Stakeholder Review", updated=updated, assignee="Peter"),
        TODAY)
    assert "stakeholder_review_stale_280d" in flags


def test_missing_assignee_and_components_flag():
    flags = triage.flag_staleness(row(assignee=None, components=[]), TODAY)
    assert "no_assignee" in flags
    assert "no_components" in flags


def test_invalid_status_flag():
    flags = triage.flag_staleness(row(status="Marinating"), TODAY)
    assert "invalid_status:Marinating" in flags


# -- has_strat_clone --

def test_strat_clone_detected():
    r = row(links=[{"type": "clones", "key": "RHAISTRAT-5",
                    "issuetype": "Feature"}])
    assert triage.has_strat_clone(r) is True


def test_non_strat_clone_is_not_a_strat_clone():
    r = row(links=[{"type": "clones", "key": "RHOAIENG-5",
                    "issuetype": "Epic"}])
    assert triage.has_strat_clone(r) is False


def test_strat_link_of_wrong_type_is_not_a_clone():
    r = row(links=[{"type": "blocks", "key": "RHAISTRAT-5",
                    "issuetype": "Feature"}])
    assert triage.has_strat_clone(r) is False


# -- classify_rfe --

def test_roadmapped_when_release_candidate_label_present():
    assert triage.classify_rfe(row(labels=["3.6-candidate"]), TODAY) == "roadmapped"


def test_roadmapped_when_strat_clone_exists():
    r = row(links=[{"type": "clones", "key": "RHAISTRAT-5",
                    "issuetype": "Feature"}])
    assert triage.classify_rfe(r, TODAY) == "roadmapped"


def test_backlogged_when_pm_backlogged_label_present():
    assert triage.classify_rfe(row(labels=["pm-backlogged"]), TODAY) == "backlogged"


def test_close_candidate_when_very_stale():
    r = row(updated="2025-01-01", assignee="Peter")
    assert triage.classify_rfe(r, TODAY) == "close_candidate"


def test_needs_attention_is_the_default():
    assert triage.classify_rfe(row(assignee="Peter"), TODAY) == "needs_attention"


# -- suggest_action --

def test_suggests_close_for_a_close_candidate():
    s = triage.suggest_action(row(updated="2025-01-01", assignee="Peter"), TODAY)
    assert s["action"] == "close"
    assert "stale" in s["reason"].lower()


def test_suggests_approve_when_pending_approval():
    s = triage.suggest_action(row(status="Pending Approval", assignee="Peter"),
                              TODAY)
    assert s["action"] == "approve"


def test_suggests_needs_uxd_on_ui_keywords():
    s = triage.suggest_action(
        row(summary="Improve the dashboard UI layout", assignee="Peter"), TODAY)
    assert s["action"] == "needs-uxd"


def test_suggests_clarify_when_no_assignee():
    s = triage.suggest_action(row(assignee=None), TODAY)
    assert s["action"] == "clarify"


def test_roadmapped_issue_gets_no_suggestion():
    s = triage.suggest_action(row(labels=["3.6-candidate"], assignee="Peter"),
                              TODAY)
    assert s["action"] == ""
