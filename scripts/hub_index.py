"""CLI: regenerate (default) or verify (--check) all generated indexes/views.
--rotate-log first moves previous-year memory/log.md sections to
memory/log-archive/<year>.md, then reindexes (rotation changes a file the
memory index is generated from)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from hublib.indexer import check, write_all
from hublib.logrotate import rotate_log


def main():
    root = Path(__file__).resolve().parents[1]
    if "--rotate-log" in sys.argv:
        if "--check" in sys.argv:
            print("ERROR --rotate-log is a write operation; incompatible with --check")
            return 2
        moved = rotate_log(root)
        for year in sorted(moved):
            print(f"ROTATED {year}: {moved[year]} section(s) -> "
                  f"memory/log-archive/{year}.md")
        if not moved:
            print("nothing to rotate")
    if "--check" in sys.argv:
        stale = check(root)
        for rel in stale:
            print(f"STALE {rel}")
        print(f"hub_index --check: {len(stale)} stale file(s)")
        return 1 if stale else 0
    for rel in write_all(root):
        print(f"WROTE {rel}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
