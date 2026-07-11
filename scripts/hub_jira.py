"""CLI: the deterministic Jira pipeline (read-only against Jira; repo writes
happen in the gated hub.jira-* skills). Spec:
docs/specs/2026-07-09-jira-hub-skills-design.md.

  --check                       connectivity/auth probe (doctor section 4)
  --try-jql '<jql>'             scope discovery: count + sample rows
  --audit <KEY>                 read-only structured dump of one issue, incl.
                                 a best-effort children search (hub.jira-hygiene)
  --sweep <feature> --out DIR   proposed snapshot + ref candidates -> DIR
  --sync [<feature>] --out DIR  diff stored snapshots + watched keys -> report + DIR
"""
import argparse
import asyncio
import datetime
import sys
from pathlib import Path

import httpx
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))

from hublib import jiramap
from hublib.jira import adf_to_text, client_from_env, probe_public
from hublib.shellenv import load_env

SWEEP_FIELDS = ["summary", "status", "issuetype", "resolution",
                "fixVersions", "updated", "description"]
DEFAULT_REF_TYPES = ["Outcome", "Feature"]
MAX_RESULTS = 500


def _load_env(root):
    """restricted/.env fallback so the CLI works in shells that never sourced
    it. Only JIRA_* keys are read; existing env always wins."""
    load_env(root, prefixes=("JIRA_",))


def _jira_cfg(root, feature):
    """The feature's jira: block from features.yaml; None = unknown feature,
    {} = known feature without a stored scope."""
    p = root / "features" / "features.yaml"
    data = yaml.safe_load(p.read_text(encoding="utf-8")) if p.is_file() else {}
    for f in (data or {}).get("features") or []:
        if isinstance(f, dict) and f.get("id") == feature:
            return f.get("jira") or {}
    return None


async def _check():
    async with client_from_env() as client:
        me = await client.myself()
    print(f"jira ok: authenticated as "
          f"{me.get('displayName') or me.get('emailAddress', '?')}")
    return 0


async def _try_jql(jql, sample):
    async with client_from_env() as client:
        issues = await client.search(jql, fields=["summary", "status", "issuetype"],
                                     max_results=MAX_RESULTS)
    if len(issues) == MAX_RESULTS:
        print(f"WARN result set hit the {MAX_RESULTS}-issue cap — counts beyond "
              f"the cap are not shown; narrow the JQL")
    print(f"{len(issues)} issue(s) for: {jql}")
    for issue in issues[:sample]:
        f = issue.get("fields", {})
        print(f"  {issue.get('key')} · {(f.get('issuetype') or {}).get('name', '')}"
              f" · {(f.get('status') or {}).get('name', '')} · {f.get('summary', '')}")
    if len(issues) > sample:
        print(f"  … {len(issues) - sample} more")
    return 0


async def _audit(key, transport=None):
    """Read-only structured dump of one issue for hub.jira-hygiene to judge.

    Prints YAML, not prose. The skill applies the checklists; this only
    supplies the facts. Never writes anything, anywhere. ``transport`` is
    test-only (httpx.MockTransport injection); production callers leave it
    None and client_from_env() picks a real transport.
    """
    fields = [
        "summary", "status", "assignee", "priority", "issuetype", "project",
        "issuelinks", "components", "labels", "created", "updated",
        "fixVersions", "parent", "description",
    ]
    async with client_from_env(transport=transport) as client:
        issue = await client.get_issue_with_links(key, fields=fields)
        base = client.base_url
        children = []
        children_lookup = "ok"
        try:
            child_issues = await client.search(
                f'parent = "{key}"',
                fields=["summary", "status", "issuetype"], max_results=50)
        except httpx.HTTPError as exc:
            children_lookup = f"failed: {exc}"
        else:
            for c in child_issues:
                cf = c.get("fields", {})
                children.append({
                    "key": c.get("key"),
                    "type": (cf.get("issuetype") or {}).get("name"),
                    "status": (cf.get("status") or {}).get("name"),
                    "summary": cf.get("summary", ""),
                })
    f = issue.get("fields", {})
    links = []
    for link in f.get("issuelinks") or []:
        ltype = (link.get("type") or {})
        if link.get("outwardIssue"):
            other, direction = link["outwardIssue"], ltype.get("outward", "")
        elif link.get("inwardIssue"):
            other, direction = link["inwardIssue"], ltype.get("inward", "")
        else:
            continue
        of = other.get("fields", {})
        links.append({
            "direction": direction,
            "key": other.get("key"),
            "type": (of.get("issuetype") or {}).get("name"),
            "status": (of.get("status") or {}).get("name"),
            "summary": of.get("summary"),
        })
    parent_raw = f.get("parent")
    if parent_raw:
        pf = parent_raw.get("fields") or {}
        parent = {
            "key": parent_raw.get("key"),
            "type": (pf.get("issuetype") or {}).get("name"),
            "summary": pf.get("summary"),
        }
    else:
        parent = None
    dump = {
        "key": issue.get("key"),
        "url": f"{base}/browse/{issue.get('key')}",
        "type": (f.get("issuetype") or {}).get("name"),
        "status": (f.get("status") or {}).get("name"),
        "summary": f.get("summary", ""),
        "assignee": (f.get("assignee") or {}).get("displayName"),
        "priority": (f.get("priority") or {}).get("name"),
        "components": [c.get("name") for c in f.get("components") or []],
        "labels": list(f.get("labels") or []),
        "fix_versions": [v.get("name") for v in f.get("fixVersions") or []],
        "parent": parent,
        "links": links,
        "children": children,
        "children_lookup": children_lookup,
        "description": adf_to_text(f.get("description")),
    }
    print(yaml.safe_dump(dump, sort_keys=False, allow_unicode=True))
    return 0


async def _fetch_rows(client, jql):
    issues = await client.search(jql, fields=SWEEP_FIELDS, max_results=MAX_RESULTS)
    keys = [i.get("key", "") for i in issues if i.get("key")]
    public = await probe_public(client.base_url, keys)
    rows = [jiramap.issue_row(i, i.get("key") in public) for i in issues]
    return issues, rows


async def _sweep(root, feature, jql_override, out, today):
    cfg = _jira_cfg(root, feature)
    if cfg is None:
        print(f"ERROR unknown feature '{feature}' (not in features/features.yaml)")
        return 2
    jql = jql_override or cfg.get("jql")
    if not jql:
        print(f"ERROR no stored jira scope for '{feature}' — pass --jql, or run "
              f"hub.jira-sweep scope discovery first")
        return 2
    ref_types = cfg.get("ref_types") or DEFAULT_REF_TYPES
    async with client_from_env() as client:
        base = client.base_url
        issues, rows = await _fetch_rows(client, jql)
    if len(rows) == MAX_RESULTS:
        print(f"WARN result set hit the {MAX_RESULTS}-issue cap — the snapshot "
              f"may be truncated; narrow the JQL")
    old = root / "features" / feature / "work" / "jira-snapshot.yaml"
    if old.is_file():
        old_rows = (yaml.safe_load(old.read_text(encoding="utf-8")) or {}).get("issues") or []
        if old_rows and (not rows or len(rows) < len(old_rows) / 2
                         or len(rows) > len(old_rows) * 2):
            print(f"WARN result count {len(rows)} vs {len(old_rows)} in the last "
                  f"snapshot — scope may have drifted; review the JQL before the gate")
    out.mkdir(parents=True, exist_ok=True)
    snap_path = out / f"jira-snapshot-{feature}.yaml"
    snap_path.write_text(jiramap.build_snapshot(feature, jql, rows, today),
                         encoding="utf-8", newline="\n")
    redacted_keys = {r["key"] for r in rows if r.get("summary") is None}
    candidates = []
    for issue in issues:
        f = issue.get("fields", {})
        if (f.get("issuetype") or {}).get("name") in ref_types:
            candidates.append({
                "key": issue.get("key"),
                "public": issue.get("key") not in redacted_keys,
                "type": (f.get("issuetype") or {}).get("name"),
                "status": (f.get("status") or {}).get("name"),
                "summary": f.get("summary", ""),
                "url": f"{base}/browse/{issue.get('key')}",
                "description": adf_to_text(f.get("description"))[:2000],
            })
    cand_path = out / f"candidates-{feature}.yaml"
    cand_path.write_text(yaml.safe_dump(candidates, sort_keys=False, allow_unicode=True),
                         encoding="utf-8", newline="\n")
    redacted = sum(1 for r in rows if r.get("summary") is None)
    print(f"swept {feature}: {len(rows)} issue(s), {redacted} summary(ies) withheld "
          f"(not anonymously readable), {len(candidates)} ref candidate(s)")
    print(f"proposed snapshot: {snap_path}")
    print(f"ref candidates:    {cand_path}")
    return 0


async def _sync(root, feature, out, today):
    p = root / "features" / "features.yaml"
    data = yaml.safe_load(p.read_text(encoding="utf-8")) if p.is_file() else {}
    feats = [f for f in (data or {}).get("features") or []
             if isinstance(f, dict) and f.get("jira")]
    if feature:
        feats = [f for f in feats if f.get("id") == feature]
        if not feats:
            print(f"ERROR '{feature}' has no jira: block in features/features.yaml "
                  f"— run hub.jira-sweep first")
            return 2
    if not feats:
        print("nothing to sync — no feature has a jira: block yet "
              "(run hub.jira-sweep first)")
        return 0
    watched = jiramap.watched_keys(root)
    any_changes = False
    out.mkdir(parents=True, exist_ok=True)
    async with client_from_env() as client:
        snap_keys = set()
        for f in feats:
            fid, jql = f["id"], (f.get("jira") or {}).get("jql", "")
            snap = root / "features" / fid / "work" / "jira-snapshot.yaml"
            if not snap.is_file():
                print(f"NOTE {fid}: no committed snapshot yet — run hub.jira-sweep "
                      f"first; skipping")
                continue
            old_rows = (yaml.safe_load(snap.read_text(encoding="utf-8")) or {}).get("issues") or []
            issues, rows = await _fetch_rows(client, jql)
            snap_keys |= {r.get("key") for r in rows} | {r.get("key") for r in old_rows}
            d = jiramap.diff(old_rows, rows)
            if not (d["new"] or d["vanished"] or d["changed"]):
                print(f"{fid}: no changes")
                continue
            any_changes = True
            print(f"{fid}: {len(d['new'])} new · {len(d['changed'])} changed · "
                  f"{len(d['vanished'])} vanished")
            for row in d["new"]:
                print(f"  NEW      {row['key']} · {row.get('type', '')} · "
                      f"{row.get('status', '')}")
            for ch in d["changed"]:
                deltas = "; ".join(f"{k}: {a!r} -> {b!r}"
                                   for k, (a, b) in ch["changes"].items())
                print(f"  CHANGED  {ch['key']} · {deltas}")
            for row in d["vanished"]:
                print(f"  VANISHED {row['key']} (left the JQL scope or was deleted)")
            path = out / f"jira-snapshot-{fid}.yaml"
            path.write_text(jiramap.build_snapshot(fid, jql, rows, today),
                            encoding="utf-8", newline="\n")
            print(f"  refreshed snapshot proposal: {path}")
        for key in sorted(k for k in watched if k not in snap_keys):
            try:
                issue = await client.get_issue(
                    key, fields=["summary", "status", "resolution"])
            except httpx.HTTPError:
                any_changes = True
                print(f"  WATCHED  {key} unreachable (deleted? moved? permission?) "
                      f"— referenced by {', '.join(watched[key])}")
                continue
            fx = issue.get("fields", {})
            status = (fx.get("status") or {}).get("name", "?")
            res = (fx.get("resolution") or {}).get("name")
            print(f"  WATCHED  {key} · {status}" + (f" ({res})" if res else "")
                  + f" — referenced by {', '.join(watched[key])}")
    print("sync: changes found — gate them via hub.jira-sync"
          if any_changes else "sync: all quiet")
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--try-jql", metavar="JQL")
    ap.add_argument("--sample", type=int, default=15)
    ap.add_argument("--audit", metavar="KEY")
    ap.add_argument("--sweep", metavar="FEATURE")
    ap.add_argument("--jql", metavar="JQL")
    ap.add_argument("--sync", nargs="?", const="", metavar="FEATURE")
    ap.add_argument("--out", metavar="DIR")
    ap.add_argument("--root", help=argparse.SUPPRESS)  # tests only
    args = ap.parse_args(argv)
    modes = [bool(args.check), args.try_jql is not None, args.audit is not None,
             args.sweep is not None, args.sync is not None]
    if sum(modes) != 1:
        ap.error("pick exactly one mode: --check | --try-jql | --audit | "
                 "--sweep | --sync")
    if (args.sweep is not None or args.sync is not None) and not args.out:
        ap.error("--out DIR is required with --sweep/--sync "
                 "(proposals are written there, never into the repo)")
    root = Path(args.root) if args.root else Path(__file__).resolve().parents[1]
    today = datetime.date.today().isoformat()
    _load_env(root)
    try:
        if args.check:
            return asyncio.run(_check())
        if args.try_jql is not None:
            return asyncio.run(_try_jql(args.try_jql, args.sample))
        if args.audit is not None:
            return asyncio.run(_audit(args.audit))
        out = Path(args.out)
        if args.sweep is not None:
            return asyncio.run(_sweep(root, args.sweep, args.jql, out, today))
        return asyncio.run(_sync(root, args.sync or None, out, today))
    except RuntimeError as exc:
        print(f"ERROR {exc}")
        return 1
    except httpx.HTTPStatusError as exc:
        code = exc.response.status_code
        if code in (401, 403):
            print(f"ERROR jira auth failed ({code}) — JIRA_TOKEN expired? Generate "
                  f"a new API token at https://id.atlassian.com/manage-profile/"
                  f"security/api-tokens, update JIRA_TOKEN in restricted/.env, "
                  f"re-run. (Token values are never printed.)")
        else:
            print(f"ERROR jira request failed: {code} on {exc.request.url}")
        return 1
    except httpx.HTTPError as exc:
        print(f"ERROR network failure talking to Jira: {exc}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
