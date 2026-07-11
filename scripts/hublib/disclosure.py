"""Local-first disclosure lint. Two passes over the PUBLIC tree only:
restricted patterns from a gitignored file (errors — CI never has the file),
and the generic public heuristic over enablement HTML and generated markdown
(warnings, CI-visible). Findings are '<relpath>: <message>' strings; (errors,
warnings) tuples, matching schema.lint_repo. Error text references patterns by
line NUMBER, never pattern text — lint output can get pasted into public places."""
import re
from pathlib import Path

from .schema import RESTRICTED_HINTS

PATTERN_FILE = "restricted/lint-patterns.txt"


def load_patterns(root):
    """Read the optional gitignored pattern file: one case-insensitive regex
    per line; '#' comments and blank lines skipped. Invalid regexes are
    skipped with a warning — a typo must never silently disable the net."""
    path = Path(root) / PATTERN_FILE
    patterns, warnings = [], []
    if not path.is_file():
        return patterns, warnings
    for lineno, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        try:
            patterns.append((lineno, re.compile(line, re.IGNORECASE)))
        except re.error as exc:
            pos = getattr(exc, "pos", None)
            where = f" at position {pos}" if pos is not None else ""
            warnings.append(f"{PATTERN_FILE}:{lineno}: invalid regex (skipped{where})")
    return patterns, warnings


def _scan_files(root):
    """The public scan surface as (path, heuristic) pairs. Every file gets the
    restricted-patterns pass (errors); heuristic=True adds the generic
    RESTRICTED_HINTS pass (warnings): enablement HTML plus the generated
    markdown that entry descriptions propagate into (#34). Markdown ENTRIES
    stay heuristic=False here: lint_entry (schema.py) already scans their
    full text. YAML surfaces get the patterns pass only."""
    root = Path(root)
    surfaces = (
        ("features/*/enablement/**/*.html", True),
        ("narrative/enablement/**/*.html", True),
        ("features/*/knowledge/*.md", False),
        ("narrative/knowledge/*.md", False),
        ("features/*/work/jira-snapshot.yaml", False),
        ("features/*/work/triage-log.yaml", False),
        ("features/*/work/refresh-*.yaml", False),
        ("artifacts/**/*.md", False),
        ("narrative/work/refresh-*.yaml", False),
        ("views/*.md", True),
        ("memory/index.md", True),
        ("features/index.md", True),
        ("features/*/index.md", True),
        ("narrative/index.md", True),
    )
    for pattern, heuristic in surfaces:
        for f in sorted(root.glob(pattern)):
            yield f, heuristic


def scan_repo(root):
    root = Path(root)
    patterns, warnings = load_patterns(root)
    errors = []
    for f, heuristic in _scan_files(root):
        rel = f.relative_to(root).as_posix()
        for n, line in enumerate(
                f.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            for lineno, pat in patterns:
                if pat.search(line):
                    errors.append(f"{rel}:{n}: matches restricted pattern "
                                  f"(lint-patterns.txt:{lineno})")
            if heuristic and RESTRICTED_HINTS.search(line):
                warnings.append(f"{rel}:{n}: restricted-content heuristic matched — "
                                f"confirm this belongs in a public repo")
    return errors, warnings
