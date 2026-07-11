"""RFE triage: classification, suggestion, transition resolution, gated apply.

Ported from pm-toolkit's scripts/analysis/triage.py, narrowed to the hub's
write surface (spec decision 2: labels, comments, close, approve, no
assignment, no field edits, no issue creation) and re-shaped so transitions
resolve BEFORE the gate rather than during apply (spec decision 3).

Spec: docs/specs/2026-07-11-jira-operating-batch-design.md
"""
import datetime

STALE_THRESHOLD_DAYS = 90
STAKEHOLDER_STALE_DAYS = 270

VALID_STATUSES = {
    "New", "Open", "Draft", "Stakeholder Review", "Pending Approval",
    "Rejection Pending", "Approved", "Closed", "Resolved",
}

# action -> label it adds. roadmap is None: its label is release-dependent
# and comes from the decision row (<release>-candidate).
LABEL_ACTIONS = {
    "roadmap": None,
    "backlog": "pm-backlogged",
    "needs-uxd": "needs-uxd",
    "clarify": "pm-needs-clarification",
}
TRANSITION_ACTIONS = ("close", "approve")
SUPPORTED_ACTIONS = frozenset(
    set(LABEL_ACTIONS) | set(TRANSITION_ACTIONS) | {"comment", "skip"})

# Never written by this hub: <release>-committed is set on the STRAT side.
PROTECTED_LABEL_SUFFIX = "-committed"

DEFAULT_CLOSE_COMMENT = "Closed during PM triage pass. Reopen if still needed."

CLOSE_TRANSITION_NAMES = ("closed", "resolved", "close issue", "done")
APPROVE_TRANSITION_NAMES = ("approved", "approve")

UI_UX_KEYWORDS = ("dashboard", "ui", "ux", "layout", "design", "usability",
                  "wireframe", "screen")


def _date(value):
    """'2026-05-01T10:00:00.000+0000' or '2026-05-01' -> date. None on junk."""
    if not value:
        return None
    try:
        return datetime.date.fromisoformat(str(value)[:10])
    except ValueError:
        return None


def _days_since(value, today):
    d = _date(value)
    return None if d is None else (today - d).days


def issue_to_row(issue):
    """Normalize a Jira issue dict into the flat row the rest of this module
    (and the HTML report, and the log) uses. Dates are truncated to day."""
    f = issue.get("fields", {}) or {}
    links = []
    for link in f.get("issuelinks") or []:
        ltype = link.get("type") or {}
        if link.get("outwardIssue"):
            other, name = link["outwardIssue"], ltype.get("outward", "")
        elif link.get("inwardIssue"):
            other, name = link["inwardIssue"], ltype.get("inward", "")
        else:
            continue
        links.append({
            "type": name,
            "key": other.get("key"),
            "issuetype": ((other.get("fields") or {}).get("issuetype")
                          or {}).get("name"),
        })
    return {
        "key": issue.get("key"),
        "summary": f.get("summary") or "",
        "status": (f.get("status") or {}).get("name") or "",
        "assignee": (f.get("assignee") or {}).get("displayName"),
        "priority": (f.get("priority") or {}).get("name"),
        "labels": list(f.get("labels") or []),
        "components": [c.get("name") for c in f.get("components") or []],
        "updated": str(f.get("updated") or "")[:10],
        "created": str(f.get("created") or "")[:10],
        "links": links,
        "transitions": [],   # filled by fetch_transitions (Task 5)
    }


def flag_staleness(row, today):
    """Objective flags. No judgement, no suggestion: just what is true."""
    flags = []
    age = _days_since(row.get("updated"), today)
    status = row.get("status") or ""

    if status == "Stakeholder Review":
        if age is not None and age >= STAKEHOLDER_STALE_DAYS:
            flags.append(f"stakeholder_review_stale_{age}d")
    elif age is not None and age >= STALE_THRESHOLD_DAYS:
        flags.append(f"no_update_{age}d")

    if not row.get("assignee"):
        flags.append("no_assignee")
    if not row.get("components"):
        flags.append("no_components")
    if status and status not in VALID_STATUSES:
        flags.append(f"invalid_status:{status}")
    return flags


def has_strat_clone(row):
    """True if this RFE is already cloned into a RHAISTRAT feature, which is
    the signal that it has been accepted onto the roadmap."""
    for link in row.get("links") or []:
        ltype = (link.get("type") or "").lower()
        key = link.get("key") or ""
        if any(t in ltype for t in ("clone", "duplicate")) \
                and key.startswith("RHAISTRAT"):
            return True
    return False


def classify_rfe(row, today):
    """roadmapped | backlogged | close_candidate | needs_attention.
    Ordered rules: the first match wins."""
    labels = row.get("labels") or []
    status = row.get("status") or ""

    if any(lbl.endswith("-candidate") or lbl.endswith(PROTECTED_LABEL_SUFFIX)
           for lbl in labels):
        return "roadmapped"
    if has_strat_clone(row):
        return "roadmapped"
    if status in ("Approved", "Closed", "Resolved"):
        return "roadmapped"
    if "pm-backlogged" in labels:
        return "backlogged"

    age = _days_since(row.get("updated"), today)
    if status == "Stakeholder Review":
        if age is not None and age >= STAKEHOLDER_STALE_DAYS:
            return "close_candidate"
    elif age is not None and age >= STALE_THRESHOLD_DAYS * 2:
        return "close_candidate"
    return "needs_attention"


def suggest_action(row, today):
    """A pre-selected action plus the reason shown as a badge in the report.
    Ordered rules: the first match wins. The human overrides freely; this only
    saves keystrokes on the obvious ones."""
    cls = classify_rfe(row, today)
    status = row.get("status") or ""
    age = _days_since(row.get("updated"), today)
    summary = (row.get("summary") or "").lower()

    if cls == "roadmapped":
        return {"action": "", "reason": "already on the roadmap"}
    if cls == "close_candidate":
        return {"action": "close",
                "reason": f"stale for {age}d with no roadmap signal"}
    if status == "Pending Approval":
        return {"action": "approve", "reason": "sitting in Pending Approval"}
    if status == "Rejection Pending":
        return {"action": "close", "reason": "already in Rejection Pending"}
    if any(k in summary for k in UI_UX_KEYWORDS):
        return {"action": "needs-uxd", "reason": "UI or UX language in summary"}
    if not row.get("assignee"):
        return {"action": "clarify", "reason": "no assignee, owner unclear"}
    if cls == "backlogged":
        return {"action": "", "reason": "already backlogged"}
    return {"action": "backlog", "reason": "no roadmap signal yet"}
