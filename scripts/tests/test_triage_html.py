import datetime
import html
import json
import re

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
    html_out = triage_html.render("mcp-registry", "project = X", [scan_row()],
                                  TODAY, "https://jira.test")
    assert 'data-feature="mcp-registry"' in html_out
    # the em-dash title split that pm-toolkit used must not reappear
    assert "document.title.split" not in html_out
    # the no-em-dashes rule governs what WE author (chrome: CSS, JS, static
    # labels/headers, option values) - not third-party Jira text we display.
    # Pin the authored chrome directly, plus a full render whose row data
    # contains no em dash (so the pinned string covers real markup too).
    assert "—" not in triage_html.CSS
    assert "—" not in triage_html.JS
    assert "—" not in html_out


def test_a_jira_summary_may_contain_an_em_dash_and_is_rendered_verbatim():
    # Third-party Jira text is data, not agent-authored prose: it may
    # legitimately contain an em dash, and we must display it verbatim.
    summary = "Support A2A — agent to agent"
    rows = [scan_row(summary=summary)]
    html_out = triage_html.render("f", "jql", rows, TODAY, "https://jira.test")
    assert html.escape(summary, quote=True) in html_out
    assert "—" in html_out


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
    rows = [
        scan_row(key="A-1", labels=["mcp", "3.6-candidate"]),
        scan_row(key="A-2", labels=["other"]),
    ]
    html_out = triage_html.render("f", "jql", rows, TODAY, "https://jira.test")
    assert "labels-data" in html_out
    # Find the specific row by data-key and pull its labels-data span's text,
    # rather than substring-checking the whole page (which would pass even if
    # the cell were malformed or attached to the wrong row).
    row_match = re.search(
        r'<tr data-key="A-1"[^>]*>.*?</tr>', html_out, re.DOTALL)
    assert row_match is not None
    cell_match = re.search(
        r'<span class="labels-data" hidden>(.*?)</span>', row_match.group(0))
    assert cell_match is not None
    # The cell content is html-escaped; a browser unescapes it via textContent.
    labels = json.loads(html.unescape(cell_match.group(1)))
    assert labels == ["mcp", "3.6-candidate"]


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
