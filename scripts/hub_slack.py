"""CLI: Slack connectivity probe (doctor section 9). Read-only against Slack.

  --check   authenticate the xoxc/xoxd tokens from restricted/.env against
            slack.com/api/auth.test

Emits one TAB-separated "<kind>\t<message>" line (kinds: ok, warn). Exit code
is always 0: a failed probe is a WARN, never a FAIL, so an offline machine
still reaches 0 fail.
"""
import argparse
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from hublib.shellenv import load_env
from hublib.slack import probe


def main(argv=None):
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true", required=True)
    ap.add_argument("--root", help=argparse.SUPPRESS)   # tests only
    args = ap.parse_args(argv)

    root = Path(args.root) if args.root else Path(__file__).resolve().parents[1]
    load_env(root, prefixes=("SLACK_",))
    kind, message = asyncio.run(probe())
    print(f"{kind}\t{message}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
