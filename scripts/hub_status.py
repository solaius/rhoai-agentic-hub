"""CLI: print the morning brief. Informational — always exits 0. The CI
section lives here (not in hublib.status) so build_brief stays testable
without gh; any gh failure silently skips the section."""
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from hublib.status import build_brief


def _ci_section():
    try:
        out = subprocess.run(
            ["gh", "run", "list", "--branch", "main", "--limit", "1"],
            capture_output=True, encoding="utf-8", errors="replace", timeout=10)
    except (OSError, subprocess.TimeoutExpired):
        return None
    if out.returncode != 0 or not out.stdout.strip():
        return None
    return "## CI (last push)\n" + out.stdout.strip()


def main():
    # Ensure UTF-8 output encoding on Windows
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    root = Path(__file__).resolve().parents[1]
    print(build_brief(root), end="")
    ci = _ci_section()
    if ci:
        print("\n" + ci)
    return 0


if __name__ == "__main__":
    sys.exit(main())
