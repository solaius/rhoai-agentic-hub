import asyncio

import httpx
import pytest

from hublib.slack import AUTH_TEST_URL, auth_test, probe, tokens_from_env


def run(coro):
    return asyncio.run(coro)


@pytest.fixture(autouse=True)
def clean_env(monkeypatch):
    monkeypatch.setenv("SLACK_XOXC_TOKEN", "xoxc-abc")
    monkeypatch.setenv("SLACK_XOXD_TOKEN", "xoxd-def")


def transport(handler):
    return httpx.MockTransport(handler)


def test_auth_test_sends_bearer_token_and_d_cookie():
    seen = {}

    def handler(request):
        seen["url"] = str(request.url)
        seen["auth"] = request.headers.get("authorization", "")
        seen["cookie"] = request.headers.get("cookie", "")
        return httpx.Response(200, json={"ok": True, "user": "peter", "team": "RH"})

    run(auth_test("xoxc-abc", "xoxd-def", transport=transport(handler)))
    assert seen["url"] == AUTH_TEST_URL
    assert seen["auth"] == "Bearer xoxc-abc"
    assert seen["cookie"] == "d=xoxd-def"


def test_auth_test_does_not_double_prefix_a_cookie_that_already_has_d():
    seen = {}

    def handler(request):
        seen["cookie"] = request.headers.get("cookie", "")
        return httpx.Response(200, json={"ok": True})

    run(auth_test("xoxc-abc", "d=xoxd-def", transport=transport(handler)))
    assert seen["cookie"] == "d=xoxd-def"


def test_probe_ok_reports_user_and_team():
    def handler(request):
        return httpx.Response(200, json={"ok": True, "user": "peter", "team": "RH"})

    kind, msg = run(probe(transport=transport(handler)))
    assert kind == "ok"
    assert "peter" in msg and "RH" in msg


def test_probe_invalid_auth_warns_and_explains_per_machine_tokens():
    def handler(request):
        return httpx.Response(200, json={"ok": False, "error": "invalid_auth"})

    kind, msg = run(probe(transport=transport(handler)))
    assert kind == "warn"
    assert "invalid_auth" in msg
    assert "docs/mcp-servers.md" in msg
    assert "machine" in msg          # says tokens do not travel between machines


def test_probe_network_error_warns_never_fails():
    def handler(request):
        raise httpx.ConnectError("offline")

    kind, msg = run(probe(transport=transport(handler)))
    assert kind == "warn"
    assert "offline" in msg.lower() or "unreachable" in msg.lower()


def test_probe_missing_tokens_warns(monkeypatch):
    monkeypatch.delenv("SLACK_XOXC_TOKEN", raising=False)
    kind, msg = run(probe())
    assert kind == "warn"
    assert "SLACK_XOXC_TOKEN" in msg


def test_probe_html_body_warns_and_never_raises():
    def handler(request):
        return httpx.Response(200, text="<html><body>captive portal</body></html>")

    kind, msg = run(probe(transport=transport(handler)))
    assert kind == "warn"
    assert "not valid Slack JSON" in msg


def test_probe_json_list_body_warns_and_never_raises():
    def handler(request):
        return httpx.Response(200, json=["not", "a", "dict"])

    kind, msg = run(probe(transport=transport(handler)))
    assert kind == "warn"
    assert "not valid Slack JSON" in msg


def test_probe_never_returns_fail():
    for payload in ({"ok": True}, {"ok": False, "error": "invalid_auth"},
                    {"ok": False, "error": "ratelimited"}):
        def handler(request, p=payload):
            return httpx.Response(200, json=p)
        kind, _ = run(probe(transport=transport(handler)))
        assert kind in ("ok", "warn")


def test_probe_never_prints_the_token_values():
    def handler(request):
        return httpx.Response(200, json={"ok": False, "error": "invalid_auth"})

    _, msg = run(probe(transport=transport(handler)))
    assert "xoxc-abc" not in msg and "xoxd-def" not in msg


def test_tokens_from_env():
    assert tokens_from_env() == ("xoxc-abc", "xoxd-def")
