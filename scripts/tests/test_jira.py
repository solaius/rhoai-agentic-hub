import asyncio
import json

import httpx
import pytest

from hublib import jira
from hublib.jira import JiraClient, adf_to_text, client_from_env, probe_public


def run(coro):
    return asyncio.run(coro)


def test_client_from_env_requires_server(monkeypatch):
    monkeypatch.delenv("JIRA_SERVER", raising=False)
    with pytest.raises(RuntimeError):
        client_from_env()


def test_client_from_env_basic_auth_when_user_set(monkeypatch):
    monkeypatch.setenv("JIRA_SERVER", "https://jira.example.com")
    monkeypatch.setenv("JIRA_USER", "user@example.com")
    monkeypatch.setenv("JIRA_TOKEN", "tok")
    seen = {}

    def handler(request):
        seen["auth"] = request.headers.get("authorization", "")
        return httpx.Response(200, json={"displayName": "U"})

    async def case():
        async with client_from_env(transport=httpx.MockTransport(handler)) as client:
            await client.myself()

    run(case())
    assert seen["auth"].startswith("Basic ")


def test_client_from_env_bearer_when_no_user(monkeypatch):
    monkeypatch.setenv("JIRA_SERVER", "https://jira.example.com")
    monkeypatch.delenv("JIRA_USER", raising=False)
    monkeypatch.setenv("JIRA_TOKEN", "pat")
    seen = {}

    def handler(request):
        seen["auth"] = request.headers.get("authorization", "")
        return httpx.Response(200, json={})

    async def case():
        async with client_from_env(transport=httpx.MockTransport(handler)) as client:
            await client.myself()

    run(case())
    assert seen["auth"] == "Bearer pat"


def test_search_paginates_with_next_page_token():
    calls = []

    def handler(request):
        calls.append(str(request.url))
        if "nextPageToken=t2" in str(request.url):
            return httpx.Response(200, json={"issues": [{"key": "X-2"}], "isLast": True})
        return httpx.Response(200, json={
            "issues": [{"key": "X-1"}], "isLast": False, "nextPageToken": "t2"})

    async def case():
        async with JiraClient("https://jira.example.com", personal_token="p",
                              transport=httpx.MockTransport(handler)) as client:
            return await client.search("project = X")

    issues = run(case())
    assert [i["key"] for i in issues] == ["X-1", "X-2"]
    assert len(calls) == 2


def test_429_retries_then_succeeds(monkeypatch):
    monkeypatch.setattr(jira, "RETRY_BASE_DELAY", 0.0)
    state = {"n": 0}

    def handler(request):
        state["n"] += 1
        if state["n"] == 1:
            return httpx.Response(429, headers={"Retry-After": "0"})
        return httpx.Response(200, json={"issues": [], "isLast": True})

    async def case():
        async with JiraClient("https://jira.example.com", personal_token="p",
                              transport=httpx.MockTransport(handler)) as client:
            return await client.search("project = X")

    assert run(case()) == []
    assert state["n"] == 2


def test_adf_to_text_nested_doc():
    doc = {"type": "doc", "version": 1, "content": [
        {"type": "heading", "attrs": {"level": 1},
         "content": [{"type": "text", "text": "Title"}]},
        {"type": "paragraph", "content": [{"type": "text", "text": "Body"}]},
        {"type": "bulletList", "content": [
            {"type": "listItem", "content": [
                {"type": "paragraph",
                 "content": [{"type": "text", "text": "item"}]}]}]},
    ]}
    assert adf_to_text(doc) == "Title\nBody\n- item"
    assert adf_to_text("already plain") == "already plain"
    assert adf_to_text(None) == ""


def test_add_label_is_an_atomic_add_never_a_field_replace():
    seen = {}

    def handler(request):
        seen["method"] = request.method
        seen["path"] = request.url.path
        seen["body"] = json.loads(request.content or b"{}")
        return httpx.Response(204)

    async def case():
        async with JiraClient("https://jira.example.com", personal_token="p",
                              transport=httpx.MockTransport(handler)) as client:
            await client.add_label("A-1", "x")

    run(case())
    assert seen["method"] == "PUT"
    assert seen["path"] == "/rest/api/3/issue/A-1"
    assert seen["body"] == {"update": {"labels": [{"add": "x"}]}}
    assert "fields" not in seen["body"]      # a replace would delete labels


def test_add_comment_tolerates_a_200_with_a_non_json_body():
    # A 2xx on the comment POST means Jira ACCEPTED AND CREATED the comment.
    # Some deployments (DC behind SSO) then answer with an HTML login page.
    # Failing to decode the response is NOT failing to write: raising here
    # would tell the caller the comment never posted while it sits on the
    # issue, which is how a close comment gets orphaned on an open issue.
    def handler(request):
        return httpx.Response(200, content=b"<html>not json</html>")

    async def case():
        async with JiraClient("https://jira.example.com", personal_token="p",
                              transport=httpx.MockTransport(handler)) as client:
            return await client.add_comment("A-1", "hello")

    assert run(case()) == {}          # no raise, and no pretend payload


def test_add_comment_still_raises_on_a_real_http_failure():
    # Tolerating a junk body must not tolerate a rejected write.
    def handler(request):
        return httpx.Response(403, content=b"<html>denied</html>")

    async def case():
        async with JiraClient("https://jira.example.com", personal_token="p",
                              transport=httpx.MockTransport(handler)) as client:
            await client.add_comment("A-1", "hello")

    with pytest.raises(httpx.HTTPStatusError):
        run(case())


def test_probe_public_fail_closed():
    def handler(request):
        assert "authorization" not in request.headers  # probe must carry no auth
        if "PUB-1" in str(request.url):
            return httpx.Response(200, json={"fields": {"summary": "s"}})
        return httpx.Response(401)

    got = run(probe_public("https://jira.example.com", ["PUB-1", "PRIV-2"],
                           transport=httpx.MockTransport(handler)))
    assert got == {"PUB-1"}
