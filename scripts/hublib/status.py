"""One-page morning brief: where the hub needs attention. Read-only;
sections with nothing to say are omitted entirely."""
import datetime
from pathlib import Path

from . import frontmatter
from .indexer import _home, _load_entries, stale_rows


def _log_body(root):
    log = Path(root) / "memory" / "log.md"
    if not log.is_file():
        return None
    try:
        return frontmatter.load_file(log)[1]
    except frontmatter.FrontmatterError:
        return None


def _previous_years(body, today):
    years = set()
    for raw in (body or "").splitlines():
        if raw.startswith("## "):
            try:
                d = datetime.date.fromisoformat(raw[3:].strip())
            except ValueError:
                continue
            if d.year < today.year:
                years.add(d.year)
    return sorted(years)


def build_brief(root, today=None):
    root = Path(root)
    today = today or datetime.date.today()
    entries = list(_load_entries(root, "*/knowledge/*.md"))
    entries += list(_load_entries(root, "knowledge/*.md", base="narrative"))
    sections = [f"# Hub status — {today.isoformat()}"]

    rows = stale_rows(root, today)
    if rows:
        sections.append(f"## Stale ({len(rows)})\n" + "\n".join(sorted(rows)))

    open_qs = [rp for rp, m, _ in entries
               if m.get("type") == "question" and m.get("status") == "open"]
    if open_qs:
        counts = {}
        for rp in open_qs:
            counts[_home(rp)] = counts.get(_home(rp), 0) + 1
        listing = " · ".join(f"{h}: {n}" for h, n in sorted(counts.items()))
        sections.append(f"## Open questions ({len(open_qs)})\n{listing}")

    open_qa = sorted((rp, m) for rp, m, _ in entries
                     if m.get("type") == "qa" and m.get("status") == "open")
    if open_qa:
        lines = [f"- {_home(rp)} · [{m.get('title') or Path(rp).stem}]({rp})"
                 for rp, m in open_qa]
        sections.append(f"## Unanswered qa ({len(open_qa)})\n" + "\n".join(lines))

    bare = sorted((rp, m) for rp, m, _ in entries if m.get("type") == "jtbd"
                  and not (isinstance(m.get("evidence"), list) and m["evidence"]))
    if bare:
        lines = [f"- {_home(rp)} · [{m.get('title') or Path(rp).stem}]({rp})"
                 for rp, m in bare]
        sections.append(f"## JTBD lacking evidence ({len(bare)})\n" + "\n".join(lines))

    undesc = []
    for pattern in ("features/*/enablement/*", "narrative/enablement/*"):
        for slug in sorted(root.glob(pattern)):
            if slug.is_dir() and not (slug / "artifact.md").is_file():
                undesc.append("/" + slug.relative_to(root).as_posix())
    if undesc:
        sections.append(f"## Enablement dirs missing artifact.md ({len(undesc)})\n"
                        + "\n".join(f"- {p}" for p in undesc))

    body = _log_body(root)
    years = _previous_years(body, today)
    if years:
        sections.append("## Log rotation due\n"
                        f"memory/log.md holds {', '.join(str(y) for y in years)} "
                        "entries — run: python scripts/hub_index.py --rotate-log")

    if body:
        recent, current = [], None
        for raw in body.splitlines():
            if raw.startswith("## "):
                current = raw[3:].strip()
            elif raw.startswith("- ") and current and len(recent) < 5:
                recent.append(f"- {current} — {raw[2:].strip()}")
        if recent:
            sections.append("## Recent log\n" + "\n".join(recent))

    return "\n\n".join(sections) + "\n"
