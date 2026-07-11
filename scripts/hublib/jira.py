"""Thin async Jira REST API client (ported 2026-07-09 from pm-toolkit
scripts/clients/jira.py; spec /docs/specs/2026-07-09-jira-hub-skills-design.md).
Write methods are ported for future backlog items (#30, write-back) — the
hub.jira-* skills are read-only against Jira.
"""

from __future__ import annotations

import asyncio
import logging
import os
import re

import httpx

logger = logging.getLogger(__name__)

MAX_RETRIES = 3
RETRY_BASE_DELAY = 2.0


# ---------------------------------------------------------------------------
# Markdown → ADF conversion
# ---------------------------------------------------------------------------

def _adf_text(text: str, marks: list[dict] | None = None) -> dict:
    node: dict = {"type": "text", "text": text}
    if marks:
        node["marks"] = marks
    return node


def _parse_inline(text: str) -> list[dict]:
    """Parse **bold**, *italic*, ~~strike~~, `code`, [text](url)."""
    nodes: list[dict] = []
    pattern = re.compile(
        r'(\*\*(?P<bold>.+?)\*\*)'
        r'|(\*(?P<italic>.+?)\*)'
        r'|(~~(?P<strike>.+?)~~)'
        r'|(`(?P<code>[^`]+)`)'
        r'|(\[(?P<lt>[^\]]*)\]\((?P<lu>[^)]+)\))'
    )
    pos = 0
    for m in pattern.finditer(text):
        if m.start() > pos:
            nodes.append(_adf_text(text[pos:m.start()]))
        if m.group("bold") is not None:
            nodes.append(_adf_text(m.group("bold"), [{"type": "strong"}]))
        elif m.group("italic") is not None:
            nodes.append(_adf_text(m.group("italic"), [{"type": "em"}]))
        elif m.group("strike") is not None:
            nodes.append(_adf_text(m.group("strike"), [{"type": "strike"}]))
        elif m.group("code") is not None:
            nodes.append(_adf_text(m.group("code"), [{"type": "code"}]))
        elif m.group("lt") is not None:
            nodes.append(_adf_text(
                m.group("lt"),
                [{"type": "link", "attrs": {"href": m.group("lu")}}],
            ))
        pos = m.end()
    if pos < len(text):
        nodes.append(_adf_text(text[pos:]))
    return nodes if nodes else [_adf_text(text)]


def markdown_to_adf(markdown: str) -> dict:
    """Convert markdown to Atlassian Document Format (ADF).

    Handles headings, paragraphs, bullet/ordered lists, bold, italic,
    strikethrough, code spans, fenced code blocks, blockquotes, tables,
    horizontal rules, and links.
    """
    lines = markdown.split("\n")
    content: list[dict] = []
    i = 0

    while i < len(lines):
        line = lines[i]

        # Fenced code block
        if line.startswith("```"):
            lang = line[3:].strip()
            code_lines: list[str] = []
            i += 1
            while i < len(lines) and not lines[i].startswith("```"):
                code_lines.append(lines[i])
                i += 1
            i += 1
            node: dict = {"type": "codeBlock",
                          "content": [_adf_text("\n".join(code_lines))]}
            if lang:
                node["attrs"] = {"language": lang}
            content.append(node)
            continue

        # Heading
        hm = re.match(r'^(#{1,6})\s+(.*)', line)
        if hm:
            level = len(hm.group(1))
            txt = hm.group(2).strip()
            content.append({"type": "heading", "attrs": {"level": level},
                            "content": _parse_inline(txt) if txt else [_adf_text("")]})
            i += 1
            continue

        # Horizontal rule
        if re.match(r'^---+\s*$', line):
            content.append({"type": "rule"})
            i += 1
            continue

        # Bullet list
        if re.match(r'^[-*]\s', line):
            items: list[list[dict]] = []
            while i < len(lines) and re.match(r'^[-*]\s', lines[i]):
                items.append(_parse_inline(re.sub(r'^[-*]\s+', '', lines[i])))
                i += 1
            content.append({"type": "bulletList", "content": [
                {"type": "listItem", "content": [
                    {"type": "paragraph", "content": nodes}
                ]} for nodes in items
            ]})
            continue

        # Ordered list
        if re.match(r'^\d+\.\s', line):
            items = []
            while i < len(lines) and re.match(r'^\d+\.\s', lines[i]):
                items.append(_parse_inline(re.sub(r'^\d+\.\s+', '', lines[i])))
                i += 1
            content.append({"type": "orderedList", "content": [
                {"type": "listItem", "content": [
                    {"type": "paragraph", "content": nodes}
                ]} for nodes in items
            ]})
            continue

        # Table
        if re.match(r'^\|.+\|', line):
            table_rows: list[list[str]] = []
            while i < len(lines) and re.match(r'^\|.+\|', lines[i]):
                row_text = lines[i].strip()
                if re.match(r'^\|[\s\-:|]+\|$', row_text):
                    i += 1
                    continue
                cells = row_text.split("|")
                table_rows.append([c for c in cells[1:-1]])
                i += 1
            if table_rows:
                adf_rows: list[dict] = []
                for ri, cells in enumerate(table_rows):
                    cell_type = "tableHeader" if ri == 0 else "tableCell"
                    adf_rows.append({"type": "tableRow", "content": [
                        {"type": cell_type, "content": [
                            {"type": "paragraph", "content": _parse_inline(c.strip())}
                        ]} for c in cells
                    ]})
                content.append({"type": "table", "content": adf_rows})
            continue

        # Empty line
        if not line.strip():
            i += 1
            continue

        # Paragraph
        para_lines: list[str] = []
        while (i < len(lines) and lines[i].strip()
               and not lines[i].startswith("#")
               and not lines[i].startswith("```")
               and not re.match(r'^[-*]\s', lines[i])
               and not re.match(r'^\d+\.\s', lines[i])
               and not re.match(r'^---+\s*$', lines[i])
               and not re.match(r'^\|.+\|', lines[i])):
            para_lines.append(lines[i])
            i += 1
        if para_lines:
            content.append({"type": "paragraph",
                            "content": _parse_inline(" ".join(para_lines))})
        else:
            content.append({"type": "paragraph",
                            "content": _parse_inline(line)})
            i += 1

    if not content:
        content = [{"type": "paragraph", "content": [_adf_text("")]}]
    return {"type": "doc", "version": 1, "content": content}


def adf_to_text(node: dict | str | None) -> str:
    """Extract plain text from an ADF document.

    Handles the nested ADF structure returned by Jira Cloud v3 endpoints.
    If the input is already a string (v2 API), returns it unchanged.
    """
    if node is None:
        return ""
    if isinstance(node, str):
        return node
    if not isinstance(node, dict):
        return str(node)

    if node.get("type") == "text":
        return node.get("text", "")

    parts: list[str] = []
    for child in node.get("content", []):
        child_type = child.get("type", "")
        child_text = adf_to_text(child)

        if child_type == "heading":
            parts.append(child_text + "\n")
        elif child_type == "paragraph":
            parts.append(child_text + "\n")
        elif child_type == "bulletList":
            parts.append(child_text)
        elif child_type == "orderedList":
            parts.append(child_text)
        elif child_type == "listItem":
            parts.append("- " + child_text + "\n")
        elif child_type == "codeBlock":
            parts.append(child_text + "\n")
        elif child_type == "hardBreak":
            parts.append("\n")
        elif child_type == "rule":
            parts.append("---\n")
        elif child_type in ("table", "tableRow"):
            parts.append(child_text + "\n")
        elif child_type in ("tableHeader", "tableCell"):
            parts.append(child_text + " | ")
        else:
            parts.append(child_text)

    return "".join(parts).rstrip("\n")


def _ensure_adf(text: str | dict) -> dict:
    """Convert a string to ADF if needed; pass through dicts unchanged."""
    if isinstance(text, dict):
        return text
    return markdown_to_adf(text)


class JiraClient:
    """Async Jira REST client supporting Bearer PAT (Data Center) or Basic auth (Cloud).

    Usage::

        async with JiraClient(url, personal_token="...") as client:
            issues = await client.search('project = MYPROJ ORDER BY created ASC')
    """

    def __init__(
        self,
        url: str,
        *,
        personal_token: str = "",
        username: str = "",
        api_token: str = "",
        max_concurrent: int = 3,
        transport: httpx.AsyncBaseTransport | None = None,
    ) -> None:
        self.base_url = url.rstrip("/")
        self._semaphore = asyncio.Semaphore(max_concurrent)
        headers: dict[str, str] = {"Accept": "application/json"}

        if personal_token:
            headers["Authorization"] = f"Bearer {personal_token}"
            self._auth = None
        else:
            self._auth = httpx.BasicAuth(username, api_token)

        self._client = httpx.AsyncClient(
            base_url=self.base_url,
            headers=headers,
            auth=self._auth,
            timeout=30.0,
            transport=transport,
        )

    async def _request(self, method: str, url: str, **kwargs: object) -> httpx.Response:
        """Make an HTTP request with rate-limit retry and concurrency control."""
        async with self._semaphore:
            for attempt in range(MAX_RETRIES):
                resp = await self._client.request(method, url, **kwargs)
                if resp.status_code != 429:
                    return resp
                delay = RETRY_BASE_DELAY * (2 ** attempt)
                retry_after = resp.headers.get("Retry-After")
                if retry_after and retry_after.isdigit():
                    delay = max(delay, int(retry_after))
                logger.warning(
                    "429 rate limited on %s, retrying in %.1fs (attempt %d/%d)",
                    url, delay, attempt + 1, MAX_RETRIES,
                )
                await asyncio.sleep(delay)
            return resp  # return last response even if still 429

    # -- Search --

    async def search(
        self,
        jql: str,
        fields: list[str] | None = None,
        max_results: int = 200,
    ) -> list[dict]:
        """Run a JQL search with token-based pagination (Jira Cloud v3 endpoint).

        Returns a flat list of issue dicts (NOT ``{"issues": [...]}``)::

            issues = await client.search('project = RHAIRFE', fields=['summary', 'status', 'labels'])
            for issue in issues:
                print(issue['key'], issue['fields']['summary'])

        ``fields`` must be a **list** of strings, not a comma-separated string.
        If omitted, a sensible default set is used.
        """
        all_issues: list[dict] = []
        page_size = min(max_results, 100)

        default_fields = [
            "summary", "status", "assignee", "priority", "labels",
            "created", "updated", "comment", "components", "issuetype",
        ]

        next_page_token: str | None = None
        while True:
            params: dict[str, str | int] = {
                "jql": jql,
                "maxResults": page_size,
                "fields": ",".join(fields or default_fields),
            }
            if next_page_token:
                params["nextPageToken"] = next_page_token

            resp = await self._request("GET", "/rest/api/3/search/jql", params=params)
            resp.raise_for_status()
            data = resp.json()

            issues = data.get("issues", [])
            all_issues.extend(issues)

            if data.get("isLast", True) or len(all_issues) >= max_results or not issues:
                break
            next_page_token = data.get("nextPageToken")
            if not next_page_token:
                break

        return all_issues[:max_results]

    # -- Single issue --

    async def get_issue(self, issue_key: str, fields: list[str] | None = None) -> dict:
        """Fetch a single issue by key."""
        params = {}
        if fields:
            params["fields"] = ",".join(fields)
        resp = await self._request("GET", f"/rest/api/2/issue/{issue_key}", params=params)
        resp.raise_for_status()
        return resp.json()

    @staticmethod
    def get_description(issue: dict) -> str:
        """Extract description as plain text from an issue dict.

        Works with both v2 (wiki markup string) and v3 (ADF object) responses.
        """
        desc = issue.get("fields", {}).get("description")
        return adf_to_text(desc)

    async def get_issue_with_links(
        self, issue_key: str, fields: list[str] | None = None,
    ) -> dict:
        """Fetch an issue with issuelinks and common fields expanded."""
        default = [
            "summary", "status", "assignee", "priority", "issuetype",
            "project", "issuelinks", "components", "labels",
            "created", "updated", "comment",
        ]
        return await self.get_issue(issue_key, fields=fields or default)

    # -- Changelog --

    async def get_changelog(self, issue_key: str) -> list[dict]:
        """Fetch the full changelog for an issue (paginated)."""
        all_histories: list[dict] = []
        start_at = 0
        while True:
            resp = await self._request(
                "GET", f"/rest/api/2/issue/{issue_key}/changelog",
                params={"startAt": start_at, "maxResults": 100},
            )
            resp.raise_for_status()
            data = resp.json()
            histories = data.get("values", [])
            all_histories.extend(histories)
            if data.get("isLast", True) or not histories:
                break
            start_at += len(histories)
        return all_histories

    # -- Comments --

    async def add_comment(self, issue_key: str, body: str | dict) -> dict:
        """Post a comment on a Jira issue. Returns the created comment, or
        ``{}`` if the response body could not be decoded.

        ``body`` can be a markdown string (auto-converted to ADF) or a
        pre-built ADF dict.
        """
        resp = await self._request(
            "POST", f"/rest/api/3/issue/{issue_key}/comment",
            json={"body": _ensure_adf(body)},
        )
        resp.raise_for_status()
        try:
            return resp.json()
        except ValueError:
            # The POST succeeded, so the comment WAS created. Some Jira
            # deployments return a 200 with a non-JSON body (an SSO login
            # page). Losing the response payload is not losing the write,
            # and a caller told "this failed" would strand the comment.
            logger.warning(
                "comment on %s posted but the response body was not JSON",
                issue_key,
            )
            return {}

    # -- Transitions --

    async def get_transitions(self, issue_key: str) -> list[dict]:
        """Get available status transitions for an issue."""
        resp = await self._request("GET", f"/rest/api/2/issue/{issue_key}/transitions")
        resp.raise_for_status()
        return resp.json().get("transitions", [])

    async def transition_issue(self, issue_key: str, transition_id: str) -> None:
        """Transition an issue to a new status."""
        resp = await self._request(
            "POST", f"/rest/api/2/issue/{issue_key}/transitions",
            json={"transition": {"id": transition_id}},
        )
        resp.raise_for_status()

    # -- Update --

    async def update_issue(self, issue_key: str, fields: dict) -> None:
        """Update fields on a Jira issue.

        If ``fields["description"]`` is a markdown string, it is
        auto-converted to ADF before posting.
        """
        if "description" in fields and isinstance(fields["description"], str):
            fields = {**fields, "description": _ensure_adf(fields["description"])}
        resp = await self._request(
            "PUT", f"/rest/api/3/issue/{issue_key}",
            json={"fields": fields},
        )
        resp.raise_for_status()

    async def add_label(self, issue_key: str, label: str) -> None:
        """Atomically ADD one label. Cannot remove existing labels.

        Uses Jira's `update` verb rather than a `fields` replace: a
        read-modify-write on `labels` would destroy any label added between
        the scan and the write. Additive by construction.
        """
        resp = await self._request(
            "PUT", f"/rest/api/3/issue/{issue_key}",
            json={"update": {"labels": [{"add": label}]}},
        )
        resp.raise_for_status()

    # -- Create --

    async def create_issue(self, fields: dict) -> dict:
        """Create a new Jira issue. Returns the created issue (with key, id, self).

        If ``fields["description"]`` is a markdown string, it is
        auto-converted to ADF before posting.
        """
        if "description" in fields and isinstance(fields["description"], str):
            fields = {**fields, "description": _ensure_adf(fields["description"])}
        resp = await self._request("POST", "/rest/api/3/issue", json={"fields": fields})
        resp.raise_for_status()
        return resp.json()

    # -- Fields --

    async def get_fields(self) -> list[dict]:
        """Fetch all field definitions (for custom field ID discovery)."""
        resp = await self._request("GET", "/rest/api/2/field")
        resp.raise_for_status()
        return resp.json()

    # -- Identity --

    async def myself(self) -> dict:
        """Fetch the authenticated user — the connectivity/auth probe."""
        resp = await self._request("GET", "/rest/api/2/myself")
        resp.raise_for_status()
        return resp.json()

    # -- Lifecycle --

    async def close(self) -> None:
        await self._client.aclose()

    async def __aenter__(self) -> JiraClient:
        return self

    async def __aexit__(self, *args: object) -> None:
        await self.close()


async def probe_public(
    base_url: str,
    keys: list[str],
    max_concurrent: int = 5,
    transport: httpx.AsyncBaseTransport | None = None,
) -> set[str]:
    """Return the subset of issue keys that are anonymously readable —
    an UNAUTHENTICATED request per key; HTTP 200 means Jira itself serves
    the issue to the world. Fail-closed: any non-200 or network error
    means 'not public'. Gates which summaries may enter tracked files."""
    sem = asyncio.Semaphore(max_concurrent)
    public: set[str] = set()
    async with httpx.AsyncClient(base_url=base_url.rstrip("/"), timeout=15.0,
                                 transport=transport) as client:
        async def one(key: str) -> None:
            async with sem:
                try:
                    resp = await client.get(f"/rest/api/2/issue/{key}",
                                            params={"fields": "summary"})
                except httpx.HTTPError:
                    return
                if resp.status_code == 200:
                    public.add(key)

        await asyncio.gather(*(one(k) for k in keys))
    return public


def client_from_env(
    transport: httpx.AsyncBaseTransport | None = None,
) -> JiraClient:
    """JiraClient from the hub's env names (restricted/.env; doctor section 4).

    JIRA_SERVER + JIRA_USER + JIRA_TOKEN -> Cloud basic auth;
    JIRA_SERVER + JIRA_TOKEN alone -> Data Center bearer.
    """
    url = os.environ.get("JIRA_SERVER", "")
    if not url:
        raise RuntimeError(
            "JIRA_SERVER not set — export restricted/.env into this shell, "
            "or diagnose with: bash scripts/doctor.sh check (section 4)")
    user = os.environ.get("JIRA_USER", "")
    token = os.environ.get("JIRA_TOKEN", "")
    if user:
        return JiraClient(url, username=user, api_token=token,
                          max_concurrent=5, transport=transport)
    return JiraClient(url, personal_token=token, max_concurrent=5,
                      transport=transport)
