"""CLI: regenerate (default) or verify (--check) all generated indexes/views."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from hublib.indexer import check, write_all


def main():
    root = Path(__file__).resolve().parents[1]
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
