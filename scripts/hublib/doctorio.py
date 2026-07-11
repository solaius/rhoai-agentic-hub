"""Doctor protocol contract: kind<TAB>message lines for scripts/doctor.sh.

doctor.sh parses each CLI's stdout with `while IFS=$'\t' read -r kind msg`.
A message that contains a literal TAB, CR, or LF breaks that parser: the
line is truncated or split into a bogus extra line with a garbage kind.
Messages here can carry externally-controlled strings (Slack API response
fields, raw lines read from a user's shell profile), so every string is
made safe at the point it is emitted, not trusted based on where it came
from. Callers upstream (hublib/slack.py, hublib/shellenv.py) return plain
structured data; sanitizing happens only here, at the emit boundary.
"""
from __future__ import annotations

import re

_WHITESPACE_RUN = re.compile(r"\s+")


def one_line(message: str) -> str:
    """Collapse any literal TAB, CR, or LF (and any other whitespace run)
    into a single space, then strip leading/trailing whitespace. The result
    is always safe as the single message field after doctor.sh's
    kind<TAB> prefix, no matter what the input contained."""
    return _WHITESPACE_RUN.sub(" ", message).strip()


def say(kind: str, message: str) -> None:
    """Print exactly one protocol-safe "kind<TAB>message" line."""
    print(f"{kind}\t{one_line(message)}")
