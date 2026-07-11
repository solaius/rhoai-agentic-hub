"""CLI: shell-profile wiring for restricted/.env (doctor section 4).

  --check   report whether the profile sources the hub's restricted/.env and
            whether JIRA_* actually reach this shell
  --setup   back up ~/.bashrc, remove the retired ai-asset-registry block,
            write or repair the hub block (idempotent)

Why this exists: hub tooling self-loads restricted/.env, but the marketplace
rfe.* skills read os.environ with no fallback, so JIRA_* must be in the shell.

Emits TAB-separated "<kind>\\t<message>" lines for doctor.sh (kinds: ok, warn,
wrote), the protocol section 8 already reads. Exit code is always 0: missing
wiring is a WARN, never a FAIL.
"""
import argparse
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from hublib import doctorio
from hublib.shellenv import MalformedProfile, apply, malformed_reason, scan

JIRA_KEYS = ("JIRA_SERVER", "JIRA_USER", "JIRA_TOKEN")


def _report_shell(env):
    missing = [k for k in JIRA_KEYS if not env.get(k)]
    if missing:
        doctorio.say("warn", f"{', '.join(missing)} not set in this shell "
                     f"(open a new shell after setup, or the rfe.* skills "
                     f"will prompt you to export them by hand)")
    else:
        doctorio.say("ok", "JIRA_* present in this shell")


def _report_profile(state, wired_msg):
    if state["hub_current"]:
        doctorio.say("ok", wired_msg)
    elif state["hub_block"]:
        doctorio.say("warn", "~/.bashrc sources a different repo path (moved clone?); "
                     "repair with: bash scripts/doctor.sh setup")
    else:
        doctorio.say("warn", "~/.bashrc does not source restricted/.env; the "
                     "marketplace rfe.* skills need JIRA_* in the shell. "
                     "Fix with: bash scripts/doctor.sh setup")
    if state["retired_block"]:
        doctorio.say("warn", "~/.bashrc still sources the RETIRED ai-asset-registry "
                     ".env; setup removes it (the hub's .env supersedes it)")
    for line in state["retired_unmarked"]:
        doctorio.say("warn", f"~/.bashrc references the retired ai-asset-registry repo "
                     f"outside a marked block, remove it by hand: {line}")


def _check(env_file, profile, env):
    text = profile.read_text(encoding="utf-8") if profile.is_file() else ""
    reason = malformed_reason(text)
    if reason is not None:
        doctorio.say("warn", reason)
    else:
        _report_profile(scan(text, env_file),
                        "~/.bashrc sources the hub's restricted/.env")
    _report_shell(env)
    return 0


def _setup(env_file, profile, env):
    text = profile.read_text(encoding="utf-8") if profile.is_file() else ""
    try:
        state = scan(text, env_file)
        updated = apply(text, env_file)
    except MalformedProfile as exc:
        doctorio.say("warn", str(exc))
        return 0
    if updated == text:
        doctorio.say("ok", "~/.bashrc already wired to restricted/.env (no change)")
        _report_shell(env)
        return 0
    if profile.is_file():
        backup = profile.with_suffix(profile.suffix + ".bak")
        backup.write_text(text, encoding="utf-8", newline="\n")
        doctorio.say("ok", f"backed up {profile.name} to {backup.name}")
    profile.write_text(updated, encoding="utf-8", newline="\n")
    if state["retired_block"]:
        doctorio.say("wrote", "removed the retired ai-asset-registry block from ~/.bashrc")
    doctorio.say("wrote", "~/.bashrc now sources the hub's restricted/.env")
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--setup", action="store_true")
    ap.add_argument("--root", help=argparse.SUPPRESS)   # tests only
    ap.add_argument("--home", help=argparse.SUPPRESS)   # tests only
    args = ap.parse_args(argv)
    if args.check == args.setup:
        ap.error("pick exactly one mode: --check | --setup")

    root = Path(args.root) if args.root else Path(__file__).resolve().parents[1]
    home = Path(args.home) if args.home else Path.home()
    env_file = root / "restricted" / ".env"
    profile = home / ".bashrc"

    if not env_file.is_file():
        doctorio.say("warn", "restricted/.env not found, nothing to wire "
                     "(copy it from your other machine, then re-run setup)")
        return 0
    if args.check:
        return _check(env_file, profile, os.environ)
    return _setup(env_file, profile, os.environ)


if __name__ == "__main__":
    raise SystemExit(main())
