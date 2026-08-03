#!/usr/bin/env python3
"""Assemble a self-contained prototype index.html from shell + pattern + content fragments.

Usage:
    python scripts/build_prototype.py \\
        --pattern catalog \\
        --content components/skills-catalog/prototype/skills-catalog-ui/v1/content/ \\
        --output components/skills-catalog/prototype/skills-catalog-ui/v1/index.html \\
        --component "Skills Catalog" \\
        --version v1
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

# Repo root -- this script lives in scripts/, one level below root.
REPO_ROOT = Path(__file__).resolve().parent.parent

# Placeholder regex -- matches {{SOME_NAME}}
PLACEHOLDER_RE = re.compile(r"\{\{[A-Z][A-Z0-9_]*\}\}")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def read_file(path: Path, label: str) -> str:
    """Read a file and return its contents, or exit with a helpful message."""
    if not path.exists():
        print(f"Error: {label} not found: {path}", file=sys.stderr)
        sys.exit(1)
    return path.read_text(encoding="utf-8")


def fragment_name_to_placeholder(filename: str) -> str:
    """Convert a content fragment filename to its placeholder token.

    Examples:
        cards.html           -> {{CARDS}}
        filter_sections.html -> {{FILTER_SECTIONS}}
        content-scripts.js   -> {{CONTENT_SCRIPTS}}
        page_title.html      -> {{PAGE_TITLE}}
        scripts.js           -> {{CONTENT_SCRIPTS}}  (special case)
    """
    stem = Path(filename).stem  # strip extension
    normalised = stem.replace("-", "_").upper()

    # Special case: "scripts.js" maps to {{CONTENT_SCRIPTS}} to avoid
    # colliding with the shell-level {{SCRIPTS}} placeholder.
    if normalised == "SCRIPTS" and Path(filename).suffix.lower() == ".js":
        normalised = "CONTENT_SCRIPTS"

    return "{{" + normalised + "}}"


def wrap_script(content: str) -> str:
    """Wrap content in <script> tags."""
    return f"<script>\n{content}\n</script>"


def list_patterns(shell_dir: Path) -> list[str]:
    """Return available pattern names from the patterns directory."""
    patterns_dir = shell_dir / "patterns"
    if not patterns_dir.is_dir():
        return []
    return sorted(p.stem for p in patterns_dir.glob("*.html"))


# ---------------------------------------------------------------------------
# Assembly
# ---------------------------------------------------------------------------

def assemble(args: argparse.Namespace) -> None:
    shell_dir = REPO_ROOT / args.shell_dir
    content_dir = REPO_ROOT / args.content
    output_path = REPO_ROOT / args.output

    # ------------------------------------------------------------------
    # 1. Read shell.html
    # ------------------------------------------------------------------
    shell_path = shell_dir / "shell.html"
    if not shell_path.exists():
        print(
            f"Error: shell.html not found at {shell_path}\n"
            "  Hint: run  python scripts/extract_uxd_styles.py  to create the shell.",
            file=sys.stderr,
        )
        sys.exit(1)
    html = read_file(shell_path, "shell.html")

    # ------------------------------------------------------------------
    # 2. Inject nav
    # ------------------------------------------------------------------
    nav_path = shell_dir / "nav" / "nav.html"
    nav_html = read_file(nav_path, "nav/nav.html") if nav_path.exists() else ""
    html = html.replace("{{NAV}}", nav_html)

    # ------------------------------------------------------------------
    # 3. Replace component name and version
    # ------------------------------------------------------------------
    html = html.replace("{{COMPONENT_NAME}}", args.component)
    html = html.replace("{{VERSION}}", args.version)

    # ------------------------------------------------------------------
    # 4. Read the pattern file
    # ------------------------------------------------------------------
    pattern_path = shell_dir / "patterns" / f"{args.pattern}.html"
    if not pattern_path.exists():
        available = list_patterns(shell_dir)
        print(
            f"Error: pattern '{args.pattern}' not found at {pattern_path}\n"
            f"  Available patterns: {', '.join(available) if available else '(none)'}",
            file=sys.stderr,
        )
        sys.exit(1)
    pattern_html = read_file(pattern_path, f"pattern:{args.pattern}")

    # ------------------------------------------------------------------
    # 5. Append extra patterns (e.g. modal)
    # ------------------------------------------------------------------
    if args.extra_patterns:
        for extra in args.extra_patterns:
            extra_path = shell_dir / "patterns" / f"{extra}.html"
            if not extra_path.exists():
                available = list_patterns(shell_dir)
                print(
                    f"Error: extra pattern '{extra}' not found at {extra_path}\n"
                    f"  Available patterns: {', '.join(available) if available else '(none)'}",
                    file=sys.stderr,
                )
                sys.exit(1)
            pattern_html += "\n" + read_file(extra_path, f"pattern:{extra}")

    # ------------------------------------------------------------------
    # 6. Read content fragments and replace placeholders in the pattern
    # ------------------------------------------------------------------
    replaced_placeholders: list[str] = []
    content_scripts: list[str] = []  # collect JS fragments separately

    if not content_dir.exists():
        print(f"Error: content directory not found: {content_dir}", file=sys.stderr)
        sys.exit(1)

    # Sort for deterministic assembly
    content_files = sorted(content_dir.iterdir()) if content_dir.is_dir() else []

    for fpath in content_files:
        if not fpath.is_file():
            continue
        fragment = fpath.read_text(encoding="utf-8")
        placeholder = fragment_name_to_placeholder(fpath.name)

        # JS files get wrapped in <script> tags
        if fpath.suffix.lower() == ".js":
            content_scripts.append(fragment)
            # Also replace the placeholder directly if it appears in the pattern
            if placeholder in pattern_html:
                pattern_html = pattern_html.replace(placeholder, wrap_script(fragment))
                replaced_placeholders.append(placeholder)
        else:
            if placeholder in pattern_html:
                pattern_html = pattern_html.replace(placeholder, fragment)
                replaced_placeholders.append(placeholder)

    # ------------------------------------------------------------------
    # 7. Inject the assembled pattern into the shell's {{CONTENT}}
    # ------------------------------------------------------------------
    html = html.replace("{{CONTENT}}", pattern_html)

    # ------------------------------------------------------------------
    # 8. Inline shell.css (replace the <link> tag with an inline <style>)
    # ------------------------------------------------------------------
    css_path = shell_dir / "shell.css"
    if css_path.exists():
        css_content = css_path.read_text(encoding="utf-8")
        style_block = f"<style>\n{css_content}\n</style>"
        # Replace the link tag that references shell.css
        html = re.sub(
            r'<link\s+rel="stylesheet"\s+href="shell\.css"\s*/?>',
            style_block,
            html,
        )
    # PatternFly CDN link stays as-is (external)

    # ------------------------------------------------------------------
    # 9. Build the {{SCRIPTS}} block: nav.js + content scripts
    # ------------------------------------------------------------------
    scripts_parts: list[str] = []
    nav_js_path = shell_dir / "nav" / "nav.js"
    if nav_js_path.exists():
        scripts_parts.append(nav_js_path.read_text(encoding="utf-8"))

    # Any JS content fragments that were NOT already injected via a
    # {{CONTENT_SCRIPTS}} placeholder go here as well.
    for fpath in content_files:
        if not fpath.is_file() or fpath.suffix.lower() != ".js":
            continue
        placeholder = fragment_name_to_placeholder(fpath.name)
        # Only append if it was NOT already replaced inline
        if placeholder not in replaced_placeholders:
            scripts_parts.append(fpath.read_text(encoding="utf-8"))

    scripts_block = wrap_script("\n".join(scripts_parts)) if scripts_parts else ""
    html = html.replace("{{SCRIPTS}}", scripts_block)

    # ------------------------------------------------------------------
    # 10. Write output
    # ------------------------------------------------------------------
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html, encoding="utf-8")

    # ------------------------------------------------------------------
    # 11. Summary
    # ------------------------------------------------------------------
    size_kb = output_path.stat().st_size / 1024
    remaining = set(PLACEHOLDER_RE.findall(html))
    # Filter out false positives inside JS string literals that legitimately
    # contain template-like tokens (e.g. innerHTML = '{{FOO}}' used as
    # placeholder text inside prototype JavaScript).
    # We only warn about placeholders that look like missed build tokens.

    print(f"  Output:       {output_path}")
    print(f"  Size:         {size_kb:.1f} KB")
    print(f"  Replaced:     {len(replaced_placeholders)} content placeholders")

    if remaining:
        print(
            f"  Unreplaced:   {len(remaining)} placeholder(s) remaining:",
            file=sys.stderr,
        )
        for p in sorted(remaining):
            print(f"                  {p}", file=sys.stderr)
        print(
            "  (These may be expected if the pattern defines placeholders\n"
            "   that are populated at runtime or by optional content.)",
            file=sys.stderr,
        )
    else:
        print("  Unreplaced:   0 (all placeholders filled)")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Assemble a self-contained prototype index.html from "
                    "shell + pattern + content fragments.",
    )
    parser.add_argument(
        "--pattern",
        required=True,
        help="Pattern name (catalog, detail, admin-table, modal, empty). "
             "Maps to conventions/prototype-shell/patterns/<name>.html.",
    )
    parser.add_argument(
        "--content",
        required=True,
        help="Directory containing content fragment files.",
    )
    parser.add_argument(
        "--output",
        required=True,
        help="Output path for the assembled index.html.",
    )
    parser.add_argument(
        "--component",
        required=True,
        help="Component display name for the PM Hub banner.",
    )
    parser.add_argument(
        "--version",
        default="v1",
        help="Version string for the PM Hub banner (default: v1).",
    )
    parser.add_argument(
        "--shell-dir",
        default="conventions/prototype-shell",
        help="Path to the shell directory, relative to repo root "
             "(default: conventions/prototype-shell).",
    )
    parser.add_argument(
        "--extra-patterns",
        action="append",
        default=[],
        metavar="PATTERN",
        help="Additional pattern files to append (e.g. modal). "
             "Can be specified multiple times.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv)
    assemble(args)


if __name__ == "__main__":
    main()
