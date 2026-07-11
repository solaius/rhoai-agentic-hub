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


import asyncio
import json

import httpx
import yaml

from hublib import jira


def run(coro):
    return asyncio.run(coro)


def client_with(handler):
    return jira.JiraClient("https://jira.test", personal_token="t",
                           transport=httpx.MockTransport(handler))


# -- compose_jql --

def test_compose_jql_layers_the_rfe_filter():
    jql = triage.compose_jql('project = RHAIRFE AND component = "AI Hub"')
    assert 'project = RHAIRFE AND component = "AI Hub"' in jql
    assert 'issuetype = "Feature Request"' in jql
    assert "resolution = Unresolved" in jql


# -- resolve_transition (pure) --

TRANSITIONS = [
    {"id": "11", "name": "Start Progress", "to": {"name": "In Progress"}},
    {"id": "31", "name": "Closed", "to": {"name": "Closed"}},
    {"id": "41", "name": "Approved", "to": {"name": "Approved"}},
]


def norm(ts):
    return [{"id": t["id"], "name": t["name"], "to": t["to"]["name"]}
            for t in ts]


def test_resolve_close_transition():
    t, reason = triage.resolve_transition("close", norm(TRANSITIONS))
    assert t["id"] == "31"
    assert reason == ""


def test_resolve_approve_transition():
    t, reason = triage.resolve_transition("approve", norm(TRANSITIONS))
    assert t["id"] == "41"


def test_resolve_is_case_insensitive():
    ts = [{"id": "9", "name": "DONE", "to": "Done"}]
    t, reason = triage.resolve_transition("close", ts)
    assert t["id"] == "9"


def test_resolve_rejects_when_no_transition_matches():
    ts = [{"id": "11", "name": "Start Progress", "to": "In Progress"}]
    t, reason = triage.resolve_transition("close", ts)
    assert t is None
    assert "no matching transition" in reason


def test_resolve_rejects_ambiguous_match_rather_than_guessing():
    ts = [{"id": "31", "name": "Closed", "to": "Closed"},
          {"id": "32", "name": "Resolved", "to": "Resolved"}]
    t, reason = triage.resolve_transition("close", ts)
    assert t is None
    assert "ambiguous" in reason


def test_resolve_of_a_non_transition_action_is_a_programming_error():
    t, reason = triage.resolve_transition("backlog", norm(TRANSITIONS))
    assert t is None
    assert "not a transition action" in reason


# -- scan --

def test_scan_fetches_flags_classifies_and_resolves_transitions():
    def handler(request):
        if "/search/jql" in request.url.path:
            return httpx.Response(200, json={
                "isLast": True,
                "issues": [{
                    "key": "RHAIRFE-1",
                    "fields": {
                        "summary": "Old thing",
                        "status": {"name": "New"},
                        "assignee": None,
                        "priority": {"name": "Normal"},
                        "labels": [],
                        "components": [],
                        "updated": "2025-01-01T00:00:00.000+0000",
                        "created": "2024-01-01T00:00:00.000+0000",
                        "issuelinks": [],
                    },
                }],
            })
        if request.url.path.endswith("/transitions"):
            return httpx.Response(200, json={"transitions": [
                {"id": "31", "name": "Closed", "to": {"name": "Closed"}},
            ]})
        raise AssertionError(f"unexpected request: {request.url}")

    async def go():
        async with client_with(handler) as c:
            return await triage.scan(c, "project = RHAIRFE", TODAY)

    rows = run(go())
    assert len(rows) == 1
    r = rows[0]
    assert r["key"] == "RHAIRFE-1"
    assert "no_assignee" in r["flags"]
    assert r["classification"] == "close_candidate"
    assert r["suggestion"]["action"] == "close"
    assert r["transitions"] == [{"id": "31", "name": "Closed", "to": "Closed"}]


def test_scan_survives_a_transitions_fetch_failure():
    # A 403 on transitions must not sink the run: the row simply carries no
    # transitions, and close/approve will be rejected at the gate for it.
    def handler(request):
        if "/search/jql" in request.url.path:
            return httpx.Response(200, json={
                "isLast": True,
                "issues": [{"key": "RHAIRFE-2", "fields": {
                    "summary": "x", "status": {"name": "New"},
                    "labels": [], "components": [], "issuelinks": [],
                    "updated": "2026-07-10T00:00:00.000+0000",
                    "created": "2026-01-01T00:00:00.000+0000"}}],
            })
        return httpx.Response(403, json={"errorMessages": ["nope"]})

    async def go():
        async with client_with(handler) as c:
            return await triage.scan(c, "project = RHAIRFE", TODAY)

    rows = run(go())
    assert rows[0]["transitions"] == []


# -- plan_decisions (pure) --

def scan_row(**kw):
    r = row(**kw)
    r["flags"] = []
    r["classification"] = "needs_attention"
    r["suggestion"] = {"action": "", "reason": ""}
    return r


CLOSABLE = [{"id": "31", "name": "Closed", "to": "Closed"}]


def test_plan_sorts_actions_into_buckets():
    rows = [scan_row(key="A-1", labels=["old"]),
            scan_row(key="A-2", transitions=CLOSABLE),
            scan_row(key="A-3")]
    decisions = {
        "A-1": {"action": "backlog", "current_labels": ["old"]},
        "A-2": {"action": "close"},
        "A-3": {"action": "skip"},
    }
    plan = triage.plan_decisions(decisions, rows)
    assert plan["labels"] == [
        {"key": "A-1", "action": "backlog", "label": "pm-backlogged",
         "current_labels": ["old"]}]
    assert plan["transitions"][0]["key"] == "A-2"
    assert plan["transitions"][0]["transition"]["id"] == "31"
    assert plan["skipped"] == [{"key": "A-3", "action": "skip",
                                "detail": "skipped"}]
    assert plan["rejected"] == []


def test_plan_rejects_unsupported_actions():
    rows = [scan_row(key="A-1")]
    plan = triage.plan_decisions({"A-1": {"action": "assign"}}, rows)
    assert plan["rejected"][0]["key"] == "A-1"
    assert "not a supported action" in plan["rejected"][0]["detail"]
    assert plan["labels"] == []


def test_plan_rejects_a_close_with_no_matching_transition():
    # The half-apply guard, for real: an unresolvable close must produce NO
    # transition entry, and apply must then issue ZERO requests for that
    # issue. The pm-toolkit bug posted the close comment first and only then
    # discovered the workflow had no close, stranding an open issue under a
    # "Closed during PM triage pass" comment.
    rows = [scan_row(key="A-1", transitions=[])]
    plan = triage.plan_decisions(
        {"A-1": {"action": "close", "comment": "please close"}}, rows)
    assert plan["transitions"] == []
    assert plan["comments"] == []
    assert "no matching transition" in plan["rejected"][0]["detail"]

    seen = []

    def handler(request):
        seen.append((request.method, request.url.path))
        return httpx.Response(200, json={})

    async def go():
        async with client_with(handler) as c:
            return await triage.apply_decisions(c, plan)

    result = run(go())
    assert seen == []                                    # zero HTTP requests
    assert not any(p.endswith("/comment") for _, p in seen)
    assert result["applied"] == []


def test_plan_rejects_a_decision_for_an_issue_not_in_the_scan():
    plan = triage.plan_decisions({"GHOST-9": {"action": "backlog"}},
                                 [scan_row(key="A-1")])
    assert "not in the scan" in plan["rejected"][0]["detail"]


def test_plan_skips_a_label_already_present():
    rows = [scan_row(key="A-1", labels=["pm-backlogged"])]
    plan = triage.plan_decisions(
        {"A-1": {"action": "backlog", "current_labels": ["pm-backlogged"]}}, rows)
    assert plan["labels"] == []
    assert plan["skipped"][0]["detail"] == "label pm-backlogged already present"


def test_plan_roadmap_requires_a_release():
    rows = [scan_row(key="A-1")]
    plan = triage.plan_decisions({"A-1": {"action": "roadmap"}}, rows)
    assert "needs a release" in plan["rejected"][0]["detail"]

    plan = triage.plan_decisions(
        {"A-1": {"action": "roadmap", "release": "3.6"}}, rows)
    assert plan["labels"][0]["label"] == "3.6-candidate"


def test_plan_never_writes_a_committed_label():
    rows = [scan_row(key="A-1")]
    plan = triage.plan_decisions(
        {"A-1": {"action": "roadmap", "release": "3.6-committed"}}, rows)
    assert plan["labels"] == []
    assert "committed" in plan["rejected"][0]["detail"]


def test_plan_committed_guard_is_case_insensitive():
    rows = [scan_row(key="A-1")]
    plan = triage.plan_decisions(
        {"A-1": {"action": "roadmap", "release": "3.6-COMMITTED"}}, rows)
    assert plan["labels"] == []
    assert "committed" in plan["rejected"][0]["detail"].lower()


def test_plan_close_carries_the_default_comment():
    rows = [scan_row(key="A-1", transitions=CLOSABLE)]
    plan = triage.plan_decisions({"A-1": {"action": "close"}}, rows)
    assert plan["transitions"][0]["comment"] == triage.DEFAULT_CLOSE_COMMENT


# -- apply_decisions --

def test_apply_writes_labels_comments_and_transitions_in_order():
    seen = []

    def handler(request):
        seen.append((request.method, request.url.path,
                     json.loads(request.content or b"{}")))
        return httpx.Response(204 if request.method == "PUT" else 200, json={})

    rows = [scan_row(key="A-1", labels=["old"]),
            scan_row(key="A-2", transitions=CLOSABLE)]
    plan = triage.plan_decisions({
        "A-1": {"action": "backlog", "current_labels": ["old"]},
        "A-2": {"action": "close"},
    }, rows)

    async def go():
        async with client_with(handler) as c:
            return await triage.apply_decisions(c, plan)

    result = run(go())
    assert len(result["applied"]) == 2
    assert result["errors"] == []

    # the label write is an atomic ADD: no array, so nothing can be deleted
    put = [s for s in seen if s[0] == "PUT"][0]
    assert put[2] == {"update": {"labels": [{"add": "pm-backlogged"}]}}
    assert "fields" not in put[2]

    # transitions go last, and the close comment precedes its transition
    kinds = [(m, p.rsplit("/", 1)[-1]) for m, p, _ in seen]
    assert kinds.index(("POST", "comment")) < kinds.index(("POST", "transitions"))
    assert kinds[-1] == ("POST", "transitions")


def test_apply_never_touches_jira_for_a_rejected_decision():
    seen = []

    def handler(request):
        seen.append(request.url.path)
        return httpx.Response(200, json={})

    rows = [scan_row(key="A-1", transitions=[])]        # cannot close
    plan = triage.plan_decisions({"A-1": {"action": "close"}}, rows)

    async def go():
        async with client_with(handler) as c:
            return await triage.apply_decisions(c, plan)

    result = run(go())
    assert seen == []                                   # zero requests
    assert result["applied"] == []
    assert len(result["rejected"]) == 1


def test_apply_partial_failure_still_applies_the_rest():
    def handler(request):
        if request.url.path.endswith("/A-2/transitions") \
                and request.method == "POST":
            return httpx.Response(400, json={"errorMessages": ["workflow moved"]})
        return httpx.Response(204 if request.method == "PUT" else 200, json={})

    rows = [scan_row(key="A-1", labels=[]),
            scan_row(key="A-2", transitions=CLOSABLE)]
    plan = triage.plan_decisions({
        "A-1": {"action": "backlog", "current_labels": []},
        "A-2": {"action": "close"},
    }, rows)

    async def go():
        async with client_with(handler) as c:
            return await triage.apply_decisions(c, plan)

    result = run(go())
    applied_keys = [a["key"] for a in result["applied"]]
    assert "A-1" in applied_keys                        # label still landed
    assert any(e["key"] == "A-2" for e in result["errors"])


# -- build_triage_log --

def test_triage_log_is_yaml_and_carries_no_jira_prose():
    rows = [scan_row(key="A-1", summary="Secret internal roadmap detail",
                     labels=[], transitions=CLOSABLE)]
    plan = triage.plan_decisions({"A-1": {"action": "close"}}, rows)

    async def go():
        async with client_with(
                lambda r: httpx.Response(200, json={})) as c:
            return await triage.apply_decisions(c, plan)

    result = run(go())
    text = triage.build_triage_log("mcp-registry", "project = X", rows, plan,
                                   result, TODAY)
    assert "do not hand-edit" in text
    assert "feature: mcp-registry" in text
    assert "Secret internal roadmap detail" not in text   # NO Jira prose
    assert "transition: Open -> Closed" in text or "Closed" in text


# -- the reviewer's attack: a stale decisions file must not delete labels --

def test_a_stale_current_labels_cannot_delete_labels():
    # The scanned row carries three labels. The decisions file, exported from
    # a browser tab that has gone stale (or hand-edited), claims there is only
    # one. Under the old read-modify-write this PUT replaced the whole array
    # and destroyed customer-escalation and security. It must now be an
    # atomic add that CANNOT remove anything.
    seen = []

    def handler(request):
        seen.append((request.method, request.url.path,
                     json.loads(request.content or b"{}")))
        return httpx.Response(204)

    rows = [scan_row(key="A-1",
                     labels=["mcp", "customer-escalation", "security"])]
    plan = triage.plan_decisions(
        {"A-1": {"action": "backlog", "current_labels": ["mcp"]}}, rows)

    async def go():
        async with client_with(handler) as c:
            return await triage.apply_decisions(c, plan)

    result = run(go())
    assert len(result["applied"]) == 1
    assert len(seen) == 1

    method, path, body = seen[0]
    assert (method, path) == ("PUT", "/rest/api/3/issue/A-1")
    # Structurally additive: no "fields", no labels array, one add op.
    assert body == {"update": {"labels": [{"add": "pm-backlogged"}]}}
    assert "fields" not in body
    blob = json.dumps(body)
    for survivor in ("customer-escalation", "security", "mcp"):
        assert survivor not in blob        # the write cannot even name them
    assert "remove" not in blob


def test_plan_prefers_the_scanned_row_over_the_decisions_file():
    # The row is never the staler source, so it wins.
    rows = [scan_row(key="A-1", labels=["pm-backlogged"])]
    plan = triage.plan_decisions(
        {"A-1": {"action": "backlog", "current_labels": []}}, rows)
    assert plan["labels"] == []            # the row already has it: skip
    assert plan["skipped"][0]["detail"] == "label pm-backlogged already present"


# -- audit-trail completeness --

def test_triage_log_records_a_rejected_key_that_was_never_scanned():
    rows = [scan_row(key="A-1", labels=[])]
    plan = triage.plan_decisions({
        "A-1": {"action": "backlog"},
        "GHOST-9": {"action": "close"},     # not in the scan
    }, rows)

    async def go():
        async with client_with(
                lambda r: httpx.Response(204)) as c:
            return await triage.apply_decisions(c, plan)

    result = run(go())
    text = triage.build_triage_log("f", "project = X", rows, plan, result, TODAY)
    doc = yaml.safe_load(text)
    by_key = {i["key"]: i for i in doc["issues"]}
    assert set(by_key) == {"A-1", "GHOST-9"}
    ghost = by_key["GHOST-9"]
    assert ghost["outcome"] == "rejected"
    assert ghost["decision"] == "close"
    assert ghost["flags"] == []
    assert ghost["labels_added"] == []
    assert ghost["transition"] is None


def test_triage_log_carries_error_detail_but_no_jira_prose():
    def handler(request):
        if request.url.path.endswith("/A-1/transitions") \
                and request.method == "POST":
            return httpx.Response(500, json={"errorMessages": ["boom"]})
        return httpx.Response(200, json={})

    rows = [scan_row(key="A-1", summary="Secret internal roadmap detail",
                     transitions=CLOSABLE)]
    plan = triage.plan_decisions(
        {"A-1": {"action": "close",
                 "comment": "Confidential customer name said close it"}}, rows)

    async def go():
        async with client_with(handler) as c:
            return await triage.apply_decisions(c, plan)

    result = run(go())
    text = triage.build_triage_log("f", "project = X", rows, plan, result, TODAY)
    doc = yaml.safe_load(text)
    entry = doc["issues"][0]
    assert entry["outcome"] == "error"
    # The distinction the audit trail exists for: the comment posted, the
    # transition did not, the issue is still open.
    assert "transition to Closed failed" in entry["detail"]
    assert "still open" in entry["detail"]
    # PUBLIC repo: no summary, no comment body, anywhere in the log.
    assert "Secret internal roadmap detail" not in text
    assert "Confidential customer name" not in text
    assert triage.DEFAULT_CLOSE_COMMENT not in text


def test_triage_log_omits_detail_when_there_is_no_error():
    rows = [scan_row(key="A-1", labels=[])]
    plan = triage.plan_decisions({"A-1": {"action": "backlog"}}, rows)

    async def go():
        async with client_with(lambda r: httpx.Response(204)) as c:
            return await triage.apply_decisions(c, plan)

    result = run(go())
    doc = yaml.safe_load(
        triage.build_triage_log("f", "project = X", rows, plan, result, TODAY))
    assert doc["issues"][0]["outcome"] == "applied"
    assert "detail" not in doc["issues"][0]


def test_apply_survives_a_200_with_a_non_json_body():
    # add_comment decodes JSON after raise_for_status. A 200 carrying junk
    # raises ValueError, which must be an item-level error, not a batch abort.
    def handler(request):
        if request.url.path.endswith("/comment"):
            return httpx.Response(200, text="<html>not json</html>")
        return httpx.Response(204)

    rows = [scan_row(key="A-1", labels=[]),
            scan_row(key="A-2", transitions=CLOSABLE)]
    plan = triage.plan_decisions({
        "A-1": {"action": "backlog"},
        "A-2": {"action": "close"},
    }, rows)

    async def go():
        async with client_with(handler) as c:
            return await triage.apply_decisions(c, plan)

    result = run(go())
    assert [a["key"] for a in result["applied"]] == ["A-1"]   # label landed
    assert result["errors"][0]["key"] == "A-2"
    assert "close comment failed" in result["errors"][0]["detail"]
