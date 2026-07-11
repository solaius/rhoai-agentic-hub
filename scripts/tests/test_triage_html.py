import datetime

from hublib import triage, triage_html

TODAY = datetime.date(2026, 7, 11)


def scan_row(**kw):
    base = {
        "key": "RHAIRFE-1", "summary": "A thing", "status": "New",
        "assignee": None, "priority": "Normal", "labels": [],
        "components": [], "updated": "2026-07-10", "created": "2026-01-01",
        "links": [], "transitions": [], "flags": [],
        "classification": "needs_attention",
        "suggestion": {"action": "backlog", "reason": "no roadmap signal yet"},
    }
    base.update(kw)
    return base


def test_report_is_self_contained():
    html = triage_html.render("mcp-registry", "project = X", [scan_row()],
                              TODAY, "https://jira.test")
    assert html.startswith("<!doctype html>")
    assert "<style>" in html and "<script>" in html
    # no external anything: a CSP-hostile report is a broken report
    assert "http-equiv" not in html
    assert 'src="http' not in html
    assert 'href="http' not in html or 'href="https://jira.test/browse' in html


def test_feature_is_a_data_attribute_not_a_title_scrape():
    html = triage_html.render("mcp-registry", "project = X", [scan_row()],
                              TODAY, "https://jira.test")
    assert 'data-feature="mcp-registry"' in html
    # the em-dash title split that pm-toolkit used must not reappear
    assert "document.title.split" not in html
    assert "—" not in html          # no em dashes anywhere, ever


def test_rows_are_grouped_into_the_three_sections():
    rows = [
        scan_row(key="A-1", classification="needs_attention"),
        scan_row(key="A-2", classification="backlogged"),
        scan_row(key="A-3", status="Stakeholder Review",
                 classification="needs_attention"),
    ]
    html = triage_html.render("f", "jql", rows, TODAY, "https://jira.test")
    assert "Untriaged" in html
    assert "Waiting on Input" in html
    assert "Backlogged" in html
    for key in ("A-1", "A-2", "A-3"):
        assert key in html


def test_current_labels_round_trip_through_a_hidden_cell():
    rows = [scan_row(labels=["mcp", "3.6-candidate"])]
    html = triage_html.render("f", "jql", rows, TODAY, "https://jira.test")
    assert "labels-data" in html
    assert "3.6-candidate" in html


def test_close_and_approve_are_offered_only_when_the_workflow_allows_it():
    closable = scan_row(key="A-1",
                        transitions=[{"id": "31", "name": "Closed",
                                      "to": "Closed"}])
    stuck = scan_row(key="A-2", transitions=[])
    html = triage_html.render("f", "jql", [closable, stuck], TODAY,
                              "https://jira.test")
    # the closable row offers close; the stuck one says why it cannot
    assert 'value="close"' in html
    assert "no matching transition" in html


def test_suggestion_and_reason_are_rendered():
    html = triage_html.render("f", "jql", [scan_row()], TODAY,
                              "https://jira.test")
    assert "no roadmap signal yet" in html
    assert 'data-suggestion="backlog"' in html


def test_summaries_are_html_escaped():
    rows = [scan_row(summary='<script>alert("x")</script> & more')]
    html = triage_html.render("f", "jql", rows, TODAY, "https://jira.test")
    assert "<script>alert" not in html
    assert "&lt;script&gt;" in html
