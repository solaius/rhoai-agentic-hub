"""Shell-profile wiring for the hub's restricted/.env (doctor section 4).

Hub tooling self-loads restricted/.env via load_env() below. The marketplace
rfe.* skills do NOT: preflight.py, fetch_single.py, dump_jira.py and
rfe.submit read os.environ with no fallback, so JIRA_* must be present in
every shell. This module owns the ~/.bashrc block that puts it there.

Per the 2026-07-08 owner ruling the block never touches LLM-provider
credentials: it neither exports nor unsets them. The retired ai-asset-registry
block did unset them; it is removed wholesale (see apply()).
"""
from __future__ import annotations

import os
from pathlib import Path

from . import gitcrypt

HUB_BEGIN = "# >>> rhoai-agentic-hub env >>>"
HUB_END = "# <<< rhoai-agentic-hub env <<<"
RETIRED_BEGIN = "# >>> ai-asset-registry env >>>"
RETIRED_END = "# <<< ai-asset-registry env <<<"
RETIRED_MARKER = "ai-asset-registry"


def load_env(root: Path, prefixes: tuple[str, ...] = ()) -> None:
    """Populate os.environ from <root>/restricted/.env for shells that never
    sourced it. Existing env always wins. Empty prefixes loads every key.

    A git-crypt encrypted .env (locked checkout, no key configured on this
    machine) is skipped silently, same as a missing file -- never a crash."""
    env = Path(root) / "restricted" / ".env"
    if not env.is_file() or gitcrypt.is_git_crypt_blob(env):
        return
    for raw in env.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if line.startswith("export "):
            line = line[len("export "):]
        if line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        if prefixes and not key.startswith(prefixes):
            continue
        if key not in os.environ:
            os.environ[key] = value.strip().strip('"').strip("'")


def render_block(env_path: Path) -> str:
    """The marked block. Forward slashes: bash reads this, not Windows."""
    p = str(env_path).replace("\\", "/")
    return "\n".join([
        HUB_BEGIN,
        f'if [ -f "{p}" ]; then',
        f'  set -a; . "{p}"; set +a',
        "fi",
        HUB_END,
    ])


class MalformedProfile(ValueError):
    """Raised when the shell profile has an unbalanced hub marker block:
    an orphan HUB_BEGIN with no matching HUB_END, or vice versa. This
    happens when a previous write crashed mid-block or someone hand-edited
    the profile. Guessing at a repair here risks silently deleting real
    shell-profile content between the markers, so apply() refuses to touch
    the file at all. A human needs to open ~/.bashrc and fix it by hand.
    """


def malformed_reason(text: str) -> str | None:
    """None if the profile is safe for apply() to edit, else a human-
    readable reason it is not. Unsafe means the hub markers are out of
    sequence: an END before its BEGIN, a nested BEGIN, or an unterminated
    BEGIN. Two well-formed hub blocks (BEGIN, END, BEGIN, END) are balanced,
    not malformed: _strip_block already removes both cleanly, and apply()
    then writes back a single block, which is the desired repair."""
    lines = [line.strip() for line in text.splitlines()]
    open_block = False

    for line in lines:
        if line == HUB_BEGIN:
            if open_block:
                return (
                    f"malformed rhoai-agentic-hub markers in the shell profile: "
                    f"nested or duplicate \"{HUB_BEGIN}\" line detected. "
                    "Fix ~/.bashrc by hand before rerunning."
                )
            open_block = True
        elif line == HUB_END:
            if not open_block:
                return (
                    f"malformed rhoai-agentic-hub markers in the shell profile: "
                    f"\"{HUB_END}\" appears before \"{HUB_BEGIN}\". "
                    "Fix ~/.bashrc by hand before rerunning."
                )
            open_block = False

    if open_block:
        return (
            f"malformed rhoai-agentic-hub markers in the shell profile: "
            f"unterminated \"{HUB_BEGIN}\" (no matching \"{HUB_END}\"). "
            "Fix ~/.bashrc by hand before rerunning."
        )

    return None


def _has_block(text: str, begin: str, end: str) -> bool:
    lines = [line.strip() for line in text.splitlines()]
    return begin in lines and end in lines


def _strip_block(text: str, begin: str, end: str) -> str:
    """Remove a marker-delimited block. An unterminated marker is left alone:
    truncating the rest of someone's shell profile is never the right call."""
    if not _has_block(text, begin, end):
        return text
    out, skipping = [], False
    for line in text.splitlines():
        stripped = line.strip()
        if stripped == begin:
            skipping = True
            continue
        if skipping:
            if stripped == end:
                skipping = False
            continue
        out.append(line)
    return "\n".join(out)


def scan(text: str, env_path: Path) -> dict:
    """What the profile currently says about hub and retired-repo wiring."""
    normalized = text.replace("\r\n", "\n")
    without_retired = _strip_block(normalized, RETIRED_BEGIN, RETIRED_END)
    unmarked = [
        line.strip() for line in without_retired.splitlines()
        if RETIRED_MARKER in line and not line.strip().startswith("#")
    ]
    return {
        "hub_block": _has_block(normalized, HUB_BEGIN, HUB_END),
        "hub_current": render_block(env_path) in normalized,
        "retired_block": _has_block(normalized, RETIRED_BEGIN, RETIRED_END),
        "retired_unmarked": unmarked,
    }


def apply(text: str, env_path: Path) -> str:
    """Retired block removed, hub block upserted. Idempotent; a moved repo
    path is repaired in place rather than duplicated.

    Raises MalformedProfile, before touching anything, if the hub markers
    are unbalanced: an unterminated block cannot be safely repaired by
    guessing, so we refuse rather than risk deleting real content."""
    reason = malformed_reason(text)
    if reason is not None:
        raise MalformedProfile(reason)
    body = _strip_block(text.replace("\r\n", "\n"), RETIRED_BEGIN, RETIRED_END)
    body = _strip_block(body, HUB_BEGIN, HUB_END).rstrip("\n")
    block = render_block(env_path)
    return f"{body}\n\n{block}\n" if body else f"{block}\n"
