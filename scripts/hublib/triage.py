"""RFE triage: classification, suggestion, transition resolution, gated apply.

Ported from pm-toolkit's scripts/analysis/triage.py, narrowed to the hub's
write surface (spec decision 2: labels, comments, close, approve, no
assignment, no field edits, no issue creation) and re-shaped so transitions
resolve BEFORE the gate rather than during apply (spec decision 3).

Spec: docs/specs/2026-07-11-jira-operating-batch-design.md
"""
import asyncio
import datetime

import httpx
import yaml

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


RFE_FILTER = 'issuetype = "Feature Request" AND resolution = Unresolved'

SCAN_FIELDS = ["summary", "status", "assignee", "priority", "labels",
               "components", "updated", "created", "issuelinks"]

MAX_RESULTS = 500
TRANSITION_CONCURRENCY = 5


def compose_jql(feature_jql):
    """The feature's stored scope, narrowed to open RFEs (spec decision 5).
    ORDER BY is stripped from the stored scope: it would be illegal mid-query.
    """
    base = feature_jql.strip()
    order = ""
    lowered = base.lower()
    if " order by " in lowered:
        cut = lowered.rindex(" order by ")
        base, order = base[:cut].strip(), base[cut:].strip()
    return f"({base}) AND {RFE_FILTER} " + (order or "ORDER BY updated ASC")


def resolve_transition(action, transitions):
    """(transition, "") on success, (None, reason) on failure. PURE.

    Resolved during the scan so the gate can name the transition that will
    fire. pm-toolkit resolved this during apply, AFTER posting the close
    comment, so a workflow with no matching transition left a "Closed during
    PM triage pass" comment on an issue that stayed open. That half-apply is
    the bug this function exists to prevent.
    """
    if action == "close":
        wanted = CLOSE_TRANSITION_NAMES
    elif action == "approve":
        wanted = APPROVE_TRANSITION_NAMES
    else:
        return None, f"'{action}' is not a transition action"

    matches = [t for t in transitions
               if (t.get("name") or "").strip().lower() in wanted]
    if not matches:
        available = ", ".join(t.get("name", "?") for t in transitions) or "none"
        return None, (f"no matching transition for '{action}' in this workflow "
                      f"(available: {available})")
    if len(matches) > 1:
        names = ", ".join(t.get("name", "?") for t in matches)
        return None, (f"ambiguous transition for '{action}': {names}. "
                      f"Resolve it in Jira, not here.")
    return matches[0], ""


async def fetch_transitions(client, rows):
    """Fill row["transitions"] for every row, concurrently. A failure on one
    issue leaves that row with an empty list: close/approve will then be
    rejected at the gate for it, which is the correct fail-closed behavior.
    """
    sem = asyncio.Semaphore(TRANSITION_CONCURRENCY)

    async def one(row):
        async with sem:
            try:
                raw = await client.get_transitions(row["key"])
            except httpx.HTTPError:
                return
        row["transitions"] = [
            {"id": t.get("id"), "name": t.get("name"),
             "to": (t.get("to") or {}).get("name")}
            for t in raw
        ]

    await asyncio.gather(*(one(r) for r in rows))


async def scan(client, jql, today):
    """Fetch, normalize, flag, classify, suggest, and resolve transitions.
    Everything the report and the gate need, in one pass. Read-only."""
    issues = await client.search(jql, fields=SCAN_FIELDS,
                                 max_results=MAX_RESULTS)
    rows = [issue_to_row(i) for i in issues]
    await fetch_transitions(client, rows)
    for row in rows:
        row["flags"] = flag_staleness(row, today)
        row["classification"] = classify_rfe(row, today)
        row["suggestion"] = suggest_action(row, today)
    return rows


def plan_decisions(decisions, rows):
    """Turn the browser's exported decisions into an explicit, inspectable
    plan. PURE: this is what the gate renders, and nothing here touches Jira.

    Every rejection carries its reason. Nothing is ever silently dropped
    (spec decision 2).
    """
    by_key = {r["key"]: r for r in rows}
    plan = {"labels": [], "comments": [], "transitions": [],
            "rejected": [], "skipped": []}

    for key, decision in decisions.items():
        action = (decision or {}).get("action") or "skip"
        row = by_key.get(key)

        if row is None:
            plan["rejected"].append({
                "key": key, "action": action,
                "detail": "not in the scan (stale decisions file?)"})
            continue
        if action not in SUPPORTED_ACTIONS:
            plan["rejected"].append({
                "key": key, "action": action,
                "detail": f"'{action}' is not a supported action. This hub "
                          f"writes labels, comments, close and approve only."})
            continue
        if action == "skip":
            plan["skipped"].append({"key": key, "action": "skip",
                                    "detail": "skipped"})
            continue

        # current_labels round-trips through the report so label writes stay
        # read-modify-write. Fall back to the scanned row if it is absent.
        current = list(decision.get("current_labels") or row.get("labels") or [])

        if action in LABEL_ACTIONS:
            label = LABEL_ACTIONS[action]
            if action == "roadmap":
                release = (decision.get("release") or "").strip()
                if not release:
                    plan["rejected"].append({
                        "key": key, "action": action,
                        "detail": "roadmap needs a release (for example 3.6)"})
                    continue
                if release.endswith(PROTECTED_LABEL_SUFFIX) \
                        or PROTECTED_LABEL_SUFFIX in release:
                    plan["rejected"].append({
                        "key": key, "action": action,
                        "detail": f"'{release}' would write a committed label. "
                                  f"That is set on the STRAT side, never here."})
                    continue
                label = f"{release}-candidate"
            if label in current:
                plan["skipped"].append({
                    "key": key, "action": action,
                    "detail": f"label {label} already present"})
                continue
            plan["labels"].append({"key": key, "action": action, "label": label,
                                   "current_labels": current})
            continue

        if action == "comment":
            body = (decision.get("comment") or "").strip()
            if not body:
                plan["rejected"].append({
                    "key": key, "action": action,
                    "detail": "comment action with no comment text"})
                continue
            plan["comments"].append({"key": key, "action": "comment",
                                     "comment": body})
            continue

        # close | approve: resolve the transition NOW, before the gate.
        transition, reason = resolve_transition(action, row.get("transitions") or [])
        if transition is None:
            plan["rejected"].append({"key": key, "action": action,
                                     "detail": reason})
            continue
        entry = {"key": key, "action": action, "transition": transition,
                 "from": row.get("status") or "?", "comment": None}
        if action == "close":
            # The comment and the transition are a UNIT. If we could not
            # resolve the transition we rejected above, so no comment is
            # posted on an issue that stays open (the pm-toolkit bug).
            entry["comment"] = ((decision.get("comment") or "").strip()
                                or DEFAULT_CLOSE_COMMENT)
        plan["transitions"].append(entry)

    return plan


async def apply_decisions(client, plan):
    """Execute an approved plan. Labels, then comments, then transitions:
    a workflow surprise on the sharpest action cannot strand the cheap ones.

    Per-item try/except. One failure never sinks the batch.
    """
    result = {"applied": [], "skipped": list(plan["skipped"]),
              "rejected": list(plan["rejected"]), "errors": []}

    for item in plan["labels"]:
        labels = list(item["current_labels"]) + [item["label"]]
        try:
            await client.update_issue(item["key"], {"labels": labels})
        except httpx.HTTPError as exc:
            result["errors"].append({"key": item["key"], "action": item["action"],
                                     "detail": f"label write failed: {exc}"})
            continue
        result["applied"].append({"key": item["key"], "action": item["action"],
                                  "detail": f"+label {item['label']}"})

    for item in plan["comments"]:
        try:
            await client.add_comment(item["key"], item["comment"])
        except httpx.HTTPError as exc:
            result["errors"].append({"key": item["key"], "action": "comment",
                                     "detail": f"comment failed: {exc}"})
            continue
        result["applied"].append({"key": item["key"], "action": "comment",
                                  "detail": "comment posted"})

    for item in plan["transitions"]:
        key, action, transition = item["key"], item["action"], item["transition"]
        if item.get("comment"):
            try:
                await client.add_comment(key, item["comment"])
            except httpx.HTTPError as exc:
                result["errors"].append({
                    "key": key, "action": action,
                    "detail": f"close comment failed, transition NOT attempted: {exc}"})
                continue
        try:
            await client.transition_issue(key, transition["id"])
        except httpx.HTTPError as exc:
            detail = f"transition to {transition['name']} failed: {exc}"
            if item.get("comment"):
                detail += (" (the close comment HAS already posted; the issue "
                           "is still open. Resolve it in Jira.)")
            result["errors"].append({"key": key, "action": action,
                                     "detail": detail})
            continue
        result["applied"].append({
            "key": key, "action": action,
            "detail": f"{item['from']} -> {transition['to'] or transition['name']}"})

    return result


def build_triage_log(feature, jql, rows, plan, result, today):
    """The tracked record: keys, flags, decisions, outcomes. NO Jira prose
    (no summaries, no comment bodies, no assignee names) so it needs no
    redaction in a PUBLIC repo (spec decision 4).
    """
    outcome_by_key = {}
    labels_by_key = {}
    transition_by_key = {}
    for bucket, name in (("applied", "applied"), ("skipped", "skipped"),
                         ("rejected", "rejected"), ("errors", "error")):
        for item in result[bucket]:
            outcome_by_key.setdefault(item["key"], name)
    for item in plan["labels"]:
        labels_by_key.setdefault(item["key"], []).append(item["label"])
    for item in plan["transitions"]:
        t = item["transition"]
        transition_by_key[item["key"]] = \
            f"{item['from']} -> {t.get('to') or t.get('name')}"

    entries = []
    for row in sorted(rows, key=lambda r: r["key"]):
        key = row["key"]
        if key not in outcome_by_key:
            continue          # not decided this pass: not our business to log
        entries.append({
            "key": key,
            "flags": list(row.get("flags") or []),
            "suggestion": (row.get("suggestion") or {}).get("action") or "",
            "decision": _decision_of(key, plan),
            "outcome": outcome_by_key[key],
            "labels_added": labels_by_key.get(key, []),
            "transition": transition_by_key.get(key),
        })

    doc = {"feature": feature, "jql": jql, "triaged": today.isoformat(),
           "issues": entries}
    header = ("# generated by hub.jira-triage (scripts/hub_triage.py) - "
              "do not hand-edit\n")
    return header + yaml.safe_dump(doc, sort_keys=False, allow_unicode=True)


def _decision_of(key, plan):
    for bucket in ("labels", "comments", "transitions", "rejected", "skipped"):
        for item in plan[bucket]:
            if item["key"] == key:
                return item["action"]
    return ""
