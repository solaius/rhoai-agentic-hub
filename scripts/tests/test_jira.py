import asyncio

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


def test_probe_public_fail_closed():
    def handler(request):
        assert "authorization" not in request.headers  # probe must carry no auth
        if "PUB-1" in str(request.url):
            return httpx.Response(200, json={"fields": {"summary": "s"}})
        return httpx.Response(401)

    got = run(probe_public("https://jira.example.com", ["PUB-1", "PRIV-2"],
                           transport=httpx.MockTransport(handler)))
    assert got == {"PUB-1"}
