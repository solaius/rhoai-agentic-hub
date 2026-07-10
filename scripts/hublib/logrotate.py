"""Yearly rotation of memory/log.md into memory/log-archive/<year>.md
(convention: /conventions/memory.md). Only sections whose '## YYYY-MM-DD'
heading parses AND belongs to a previous year move — rotation never touches
what it cannot date."""
import datetime
import re
from pathlib import Path

HEADING_RE = re.compile(r"^## (\d{4})-\d{2}-\d{2}\s*$")


def rotate_log(root, today=None):
    """Returns {year: sections_moved}; {} means nothing to do."""
    root = Path(root)
    today = today or datetime.date.today()
    log = root / "memory" / "log.md"
    if not log.is_file():
        return {}
    text = log.read_text(encoding="utf-8")
    head, body = "", text
    if text.startswith("---\n"):
        end = text.find("\n---\n", 4)
        if end != -1:
            head, body = text[:end + 5], text[end + 5:]
    kept, moved = [], {}
    move_year = None  # set while inside a section that is being moved
    for line in body.splitlines(keepends=True):
        if line.startswith("## "):
            m = HEADING_RE.match(line.rstrip("\n"))
            year = int(m.group(1)) if m else None
            move_year = year if (year is not None and year < today.year) else None
        if move_year:
            moved.setdefault(move_year, []).append(line)
        else:
            kept.append(line)
    if not moved:
        return {}
    archive = root / "memory" / "log-archive"
    archive.mkdir(parents=True, exist_ok=True)
    counts = {}
    for year, lines in moved.items():
        target = archive / f"{year}.md"
        chunk = "".join(lines).rstrip("\n") + "\n"
        if target.is_file():
            content = target.read_text(encoding="utf-8").rstrip("\n") + "\n\n" + chunk
        else:
            content = f"# memory/log archive — {year}\n\n" + chunk
        target.write_text(content, encoding="utf-8", newline="\n")
        counts[year] = sum(1 for l in lines if l.startswith("## "))
    log.write_text((head + "".join(kept)).rstrip("\n") + "\n",
                   encoding="utf-8", newline="\n")
    return counts
