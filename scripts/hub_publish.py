"""CLI: validate the publish manifest (--check) or apply it to a pages clone."""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from hublib.publisher import apply
from hublib.schema import validate_manifest


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pages-dir")
    ap.add_argument("--hub-sha", default="")
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    root = Path(__file__).resolve().parents[1]
    errors = validate_manifest(root)
    for e in errors:
        print(f"ERROR {e}")
    if errors:
        return 1
    if args.check:
        print("hub_publish --check: manifest valid")
        return 0
    if not args.pages_dir:
        print("ERROR --pages-dir required unless --check")
        return 2
    copied, warnings = apply(root, args.pages_dir, args.hub_sha)
    for w in warnings:
        print(f"WARN  {w}")
    for d in copied:
        print(f"PUBLISHED {d}")
    print(f"hub_publish: {len(copied)} artifact(s), landing regenerated")
    return 0


if __name__ == "__main__":
    sys.exit(main())
