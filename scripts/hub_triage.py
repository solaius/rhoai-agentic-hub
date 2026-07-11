"""CLI: the RFE triage pipeline.

  --scan <feature> --out DIR                       fetch + report + rows -> DIR
  --plan <decisions.json> --rows <rows.json>       render the gate table (no network)
  --apply <decisions.json> --rows <rows.json> --feature <f> --out DIR

WRITES TO JIRA (labels, comments, close, approve) in --apply mode only, and
only through the gate in hub.jira-triage. --scan and --plan are read-only.

The CLI never writes into the repo: --out DIR is required, and the gated skill
copies the report into restricted/ and the log into the tracked tree.

Spec: docs/specs/2026-07-11-jira-operating-batch-design.md
"""
import argparse
import asyncio
import datetime
import json
import sys
from pathlib import Path

import httpx
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))

from hublib import triage, triage_html
from hublib.jira import client_from_env
from hublib.shellenv import load_env


def _jira_cfg(root, feature):
    """The feature's jira: block. None = unknown feature, {} = no scope."""
    p = root / "features" / "features.yaml"
    data = yaml.safe_load(p.read_text(encoding="utf-8")) if p.is_file() else {}
    for f in (data or {}).get("features") or []:
        if isinstance(f, dict) and f.get("id") == feature:
            return f.get("jira") or {}
    return None


async def _scan(root, feature, out, today):
    cfg = _jira_cfg(root, feature)
    if cfg is None:
        print(f"ERROR unknown feature '{feature}' (not in features/features.yaml)")
        return 2
    if not cfg.get("jql"):
        print(f"ERROR no stored jira scope for '{feature}' - run hub.jira-sweep "
              f"scope discovery first")
        return 2

    jql = triage.compose_jql(cfg["jql"])
    print(f"scope: {jql}")
    async with client_from_env() as client:
        rows = await triage.scan(client, jql, today)
        base = client.base_url

    out.mkdir(parents=True, exist_ok=True)
    report = out / f"triage-{feature}-{today.isoformat()}.html"
    report.write_text(triage_html.render(feature, jql, rows, today, base),
                      encoding="utf-8", newline="\n")
    rows_path = out / f"rows-{feature}.json"
    rows_path.write_text(json.dumps(rows, indent=2), encoding="utf-8",
                         newline="\n")

    counts = {}
    for row in rows:
        counts[row["classification"]] = counts.get(row["classification"], 0) + 1
    summary = " . ".join(f"{v} {k}" for k, v in sorted(counts.items()))
    print(f"scanned {feature}: {len(rows)} open RFE(s) ({summary})")
    print(f"report: {report}")
    print(f"rows:   {rows_path}")
    print("NOTE the report carries live Jira summaries. It belongs under "
          "restricted/, never in the tracked tree (this repo is PUBLIC).")
    return 0


def _print_gate(plan):
    """The gate table. Transitions first and separate: they are the
    destructive ones (spec decision 3)."""
    if plan["transitions"]:
        print(f"\nTRANSITIONS ({len(plan['transitions'])})")
        for item in plan["transitions"]:
            t = item["transition"]
            line = (f"  {item['key']}: {item['from']} -> "
                    f"{t.get('to') or t.get('name')}")
            if item.get("comment"):
                line += f'  (+comment "{item["comment"][:60]}")'
            print(line)
    if plan["labels"]:
        print(f"\nLABELS ({len(plan['labels'])})")
        for item in plan["labels"]:
            print(f"  {item['key']}: +{item['label']}")
    if plan["comments"]:
        print(f"\nCOMMENTS ({len(plan['comments'])})")
        for item in plan["comments"]:
            print(f'  {item["key"]}: "{item["comment"][:80]}"')
    if plan["skipped"]:
        print(f"\nSKIPPED ({len(plan['skipped'])})")
        for item in plan["skipped"]:
            print(f"  {item['key']}: {item['detail']}")
    if plan["rejected"]:
        print(f"\nREJECTED ({len(plan['rejected'])})")
        for item in plan["rejected"]:
            print(f"  {item['key']}: {item['action']} - {item['detail']}")
    total = len(plan["transitions"]) + len(plan["labels"]) + len(plan["comments"])
    print(f"\n{total} Jira mutation(s) staged. Nothing has been written yet.")


def _load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _coerce_str(value):
    """None stays None; anything else (including a JSON number like 3.6 from
    a hand-edited decisions file) becomes its str() so plan_decisions'
    .strip() calls never see a non-string and blow up with a traceback."""
    return None if value is None else str(value)


def _coerce_current_labels(value):
    """current_labels is ADVISORY ONLY (see triage.plan_decisions): it only
    feeds a "label already present, skip it" check and is never carried into
    a Jira payload, because label writes are atomic adds (JiraClient.add_
    label). So the safe move on anything malformed is to omit it and let the
    freshly-scanned row's labels (the authoritative source) be used instead
    - that can only cause an extra harmless, idempotent write attempt, never
    a wrong one. Returns a list of strings, or None to mean "omit".
    """
    if not isinstance(value, list):
        # int, bool, float, str, dict: not a labels list. Omit rather than
        # guess; plan_decisions falls back to the scanned row's labels.
        return None
    cleaned = []
    for item in value:
        if isinstance(item, str):
            cleaned.append(item)
        elif isinstance(item, (dict, list)) or item is None:
            continue  # not string-coercible sensibly: drop
        else:
            cleaned.append(str(item))
    return cleaned


def _normalize_decisions(payload):
    """Validate and coerce the untrusted, human/browser-generated decisions
    payload before it reaches triage.plan_decisions. Returns
    (decisions_dict, error_message). error_message is None on success.

    The decisions file is exported by the report's JS or hand-edited by a
    human, so it is untrusted input. plan_decisions() calls .strip() on
    "release" and "comment"; a JSON number there (a hand-edited "release":
    3.6) raises AttributeError and aborts with a traceback. Planning happens
    before any Jira write, so that already fails closed - zero writes - but
    a traceback is a bad experience and a bad error path. Fix it here, once,
    for every caller of _plan_from.
    """
    if not isinstance(payload, dict):
        return None, "decisions file must be a JSON object with a 'decisions' key"
    decisions = payload.get("decisions")
    if not isinstance(decisions, dict):
        return None, "decisions file must have a top-level 'decisions' object"

    normalized = {}
    for key, decision in decisions.items():
        if not isinstance(decision, dict):
            normalized[key] = {}
            continue
        clean = {}
        for field in ("action", "release", "comment"):
            if field in decision:
                clean[field] = _coerce_str(decision[field])
        if "current_labels" in decision:
            labels = _coerce_current_labels(decision["current_labels"])
            if labels is not None:
                clean["current_labels"] = labels
        normalized[key] = clean
    return normalized, None


def _plan_from(decisions_path, rows_path):
    payload = _load(decisions_path)
    decisions, error = _normalize_decisions(payload)
    if error is not None:
        return None, None, error
    rows = _load(rows_path)
    return triage.plan_decisions(decisions, rows), rows, None


async def _apply(decisions_path, rows_path, feature, out, today):
    plan, rows, error = _plan_from(decisions_path, rows_path)
    if error is not None:
        print(f"ERROR {error}")
        return 2
    _print_gate(plan)

    async with client_from_env() as client:
        result = await triage.apply_decisions(client, plan)

    cfg_jql = _load(decisions_path).get("jql", "")
    out.mkdir(parents=True, exist_ok=True)
    log_path = out / f"triage-log-{feature}.yaml"
    log_path.write_text(
        triage.build_triage_log(feature, cfg_jql, rows, plan, result, today),
        encoding="utf-8", newline="\n")

    print(f"\napplied {len(result['applied'])} . skipped {len(result['skipped'])}"
          f" . rejected {len(result['rejected'])} . errors {len(result['errors'])}")
    # A transition is the destructive action, so counts alone are not enough:
    # every transition that actually fired is named explicitly, not folded
    # anonymously into "applied N".
    for item in result["applied"]:
        tag = "TRANSITION" if item["action"] in triage.TRANSITION_ACTIONS else "OK"
        print(f"  {tag:<10} {item['key']}: {item['detail']}")
    for item in result["errors"]:
        print(f"  ERROR      {item['key']}: {item['detail']}")
    print(f"proposed log: {log_path}")
    return 1 if result["errors"] else 0


def main(argv=None):
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--scan", metavar="FEATURE")
    ap.add_argument("--plan", metavar="DECISIONS_JSON")
    ap.add_argument("--apply", metavar="DECISIONS_JSON")
    ap.add_argument("--rows", metavar="ROWS_JSON")
    ap.add_argument("--feature", metavar="FEATURE")
    ap.add_argument("--out", metavar="DIR")
    ap.add_argument("--root", help=argparse.SUPPRESS)  # tests only
    args = ap.parse_args(argv)

    modes = [args.scan is not None, args.plan is not None, args.apply is not None]
    if sum(modes) != 1:
        ap.error("pick exactly one mode: --scan | --plan | --apply")
    if args.scan is not None and not args.out:
        ap.error("--out DIR is required with --scan "
                 "(proposals are written there, never into the repo)")
    if args.plan is not None and not args.rows:
        ap.error("--rows ROWS_JSON is required with --plan")
    if args.apply is not None and not (args.rows and args.feature and args.out):
        ap.error("--apply needs --rows ROWS_JSON, --feature FEATURE and --out DIR")

    root = Path(args.root) if args.root else Path(__file__).resolve().parents[1]
    today = datetime.date.today()
    load_env(root, prefixes=("JIRA_",))

    try:
        if args.scan is not None:
            return asyncio.run(_scan(root, args.scan, Path(args.out), today))
        if args.plan is not None:
            plan, _, error = _plan_from(args.plan, args.rows)
            if error is not None:
                print(f"ERROR {error}")
                return 2
            _print_gate(plan)
            return 0
        return asyncio.run(_apply(args.apply, args.rows, args.feature,
                                  Path(args.out), today))
    except RuntimeError as exc:
        print(f"ERROR {exc}")
        return 1
    except httpx.HTTPStatusError as exc:
        code = exc.response.status_code
        if code in (401, 403):
            print(f"ERROR jira auth failed ({code}) - JIRA_TOKEN expired? "
                  f"Generate a new API token at https://id.atlassian.com/"
                  f"manage-profile/security/api-tokens, update JIRA_TOKEN in "
                  f"restricted/.env, re-run. (Token values are never printed.)")
        else:
            print(f"ERROR jira request failed: {code} on {exc.request.url}")
        return 1
    except httpx.HTTPError as exc:
        print(f"ERROR network failure talking to Jira: {exc}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
