"""Slack connectivity probe (doctor section 9).

The Slack MCP server authenticates with xoxc/xoxd browser session tokens (see
docs/mcp-servers.md). Doctor already checks that the server is REGISTERED;
registration is not validity. These tokens are per-login, so a copy carried
over from another machine can be silently dead, which is exactly the failure
R5 predicted for machine B.

WARN only, never FAIL: an offline machine must still reach 0 fail.
"""
from __future__ import annotations

import os

import httpx

AUTH_TEST_URL = "https://slack.com/api/auth.test"
TIMEOUT = 10.0
AUTH_ERRORS = ("invalid_auth", "not_authed", "token_revoked", "token_expired",
               "account_inactive")


def tokens_from_env() -> tuple[str, str]:
    return (os.environ.get("SLACK_XOXC_TOKEN", ""),
            os.environ.get("SLACK_XOXD_TOKEN", ""))


async def auth_test(
    xoxc: str,
    xoxd: str,
    transport: httpx.AsyncBaseTransport | None = None,
) -> dict:
    """Raw auth.test response. Slack answers HTTP 200 with ok:false on bad
    tokens, so the body is the signal, not the status code."""
    cookie = xoxd if xoxd.startswith("d=") else f"d={xoxd}"
    async with httpx.AsyncClient(timeout=TIMEOUT, transport=transport) as client:
        resp = await client.post(
            AUTH_TEST_URL,
            headers={"Authorization": f"Bearer {xoxc}", "Cookie": cookie},
        )
        resp.raise_for_status()
        return resp.json()


async def probe(transport: httpx.AsyncBaseTransport | None = None) -> tuple[str, str]:
    """(kind, message) for doctor. Token values are never included."""
    xoxc, xoxd = tokens_from_env()
    missing = [name for name, value in
               (("SLACK_XOXC_TOKEN", xoxc), ("SLACK_XOXD_TOKEN", xoxd)) if not value]
    if missing:
        return ("warn", f"{', '.join(missing)} missing in restricted/.env, so the "
                        f"slack MCP will not authenticate (see docs/mcp-servers.md)")
    try:
        data = await auth_test(xoxc, xoxd, transport=transport)
    except httpx.HTTPError as exc:
        return ("warn", f"slack unreachable ({exc.__class__.__name__}), offline? "
                        f"re-run: python scripts/hub_slack.py --check")
    except ValueError:
        # resp.json() raises json.JSONDecodeError (a ValueError subclass) on
        # a non-JSON body. A captive portal or corporate proxy answering
        # HTTP 200 with an HTML page is the realistic cause on a VPN.
        return ("warn", "slack auth.test response was not valid Slack JSON "
                        "(body did not parse as JSON), likely a captive "
                        "portal or corporate proxy on this network: retry "
                        "off that network, or check the proxy settings")
    if not isinstance(data, dict):
        # Valid JSON (a list, null, a number, ...) that is not the object
        # shape Slack always returns, same likely cause as above.
        return ("warn", "slack auth.test response was not valid Slack JSON "
                        "(body was not a JSON object), likely a captive "
                        "portal or corporate proxy on this network: retry "
                        "off that network, or check the proxy settings")
    if data.get("ok"):
        return ("ok", f"slack auth ok: {data.get('user', '?')} "
                      f"@ {data.get('team', '?')}")
    error = data.get("error", "unknown")
    if error in AUTH_ERRORS:
        return ("warn", f"slack auth failed ({error}). xoxc/xoxd are per-login "
                        f"session tokens and do not travel between machines: "
                        f"re-extract them on THIS machine per docs/mcp-servers.md")
    return ("warn", f"slack auth.test returned an error: {error}")
