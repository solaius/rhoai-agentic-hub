"""CLI: lint the hub. Exit 1 on errors; warnings never fail the build."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from hublib.schema import lint_repo


def main():
    root = Path(__file__).resolve().parents[1]
    errors, warnings = lint_repo(root)
    for w in warnings:
        print(f"WARN  {w}")
    for e in errors:
        print(f"ERROR {e}")
    print(f"hub_lint: {len(errors)} error(s), {len(warnings)} warning(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
