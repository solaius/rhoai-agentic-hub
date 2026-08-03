"""Extract UXD prototype styles and structure from the RHOAI UXD GitLab repo.

Fetches source files from the UXD prototype repo and refreshes the shared
prototype shell files in conventions/prototype-shell/.

Usage:
    python scripts/extract_uxd_styles.py --branch 3.6
    python scripts/extract_uxd_styles.py --branch 3.7 --verify
"""
import argparse
import re
import subprocess
import sys
import urllib.parse
from datetime import datetime, timezone
from pathlib import Path

# ── Constants ──────────────────────────────────────────────────────────────

GITLAB_HOST = "gitlab.cee.redhat.com"
DEFAULT_PROJECT_ID = "155361"
DEFAULT_BRANCH = "3.6"
DEFAULT_SHELL_DIR = "conventions/prototype-shell"
DEFAULT_DEPLOYED_URL = (
    "https://rhoai-deploy-playground-ux-921ee2.pages.redhat.com"
)

SOURCE_FILES = [
    "src/app/app.css",
    "src/app/AppLayout/AppLayout.tsx",
    "src/app/routes.tsx",
    "src/app/AIHub/MCPServers/MCPCatalog.tsx",
    "src/app/AIHub/MCPServers/MCPCatalogDetails.tsx",
    "src/app/AIHub/MCPServers/DeployMCPServerModal.tsx",
]

REPO_ROOT = Path(__file__).resolve().parents[1]


# ── GitLab fetch ───────────────────────────────────────────────────────────

def fetch_gitlab_file(project_id: str, file_path: str, branch: str) -> str:
    """Fetch a single file from the GitLab repository API via curl.

    Uses ``curl -sk`` to bypass the self-signed certificate on
    gitlab.cee.redhat.com.
    """
    encoded_path = urllib.parse.quote(file_path, safe="")
    url = (
        f"https://{GITLAB_HOST}/api/v4/projects/{project_id}"
        f"/repository/files/{encoded_path}/raw?ref={branch}"
    )
    result = subprocess.run(
        ["curl", "-sk", url],
        capture_output=True,
        timeout=30,
        encoding="utf-8",
        errors="replace",
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"curl failed for {file_path}: {(result.stderr or '').strip()}"
        )
    # GitLab returns a JSON error body for missing files / auth failures.
    body = result.stdout or ""
    if body.lstrip().startswith('{"message"') or body.lstrip().startswith('{"error"'):
        raise RuntimeError(f"GitLab API error for {file_path}: {body.strip()}")
    return body


# ── CSS extraction ─────────────────────────────────────────────────────────

def write_shell_css(css_content: str, shell_dir: Path, branch: str) -> Path:
    """Write app.css content to shell.css with an extraction header."""
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    header = (
        f"/*\n"
        f" * shell.css -- extracted from UXD RHOAI prototype\n"
        f" *\n"
        f" * Source : https://{GITLAB_HOST}/uxd/prototypes/rhoai\n"
        f" * Branch : {branch}\n"
        f" * File   : src/app/app.css\n"
        f" * Date   : {now}\n"
        f" *\n"
        f" * This file is auto-extracted by scripts/extract_uxd_styles.py.\n"
        f" * Manual edits will be overwritten on the next extraction run.\n"
        f" */\n\n"
    )
    out = shell_dir / "shell.css"
    out.write_text(header + css_content, encoding="utf-8")
    return out


# ── Structure analysis ─────────────────────────────────────────────────────

def analyse_app_layout(tsx_content: str) -> None:
    """Print a human-readable summary of AppLayout.tsx component tree."""
    print("\n--- AppLayout.tsx structure analysis ---")

    # Extract component imports
    imports = re.findall(r"import\s+.*?from\s+['\"](.+?)['\"]", tsx_content)
    pf_imports = [i for i in imports if "@patternfly" in i]
    local_imports = [i for i in imports if not i.startswith("@") and not i.startswith("react")]

    if pf_imports:
        print("\nPatternFly components used:")
        for imp in sorted(set(pf_imports)):
            print(f"  - {imp}")

    if local_imports:
        print("\nLocal imports:")
        for imp in sorted(set(local_imports)):
            print(f"  - {imp}")

    # Extract JSX component tags (capitalised tags = React components)
    tags = re.findall(r"<([A-Z][A-Za-z0-9.]+)", tsx_content)
    unique_tags = sorted(set(tags))
    if unique_tags:
        print("\nJSX component tags (unique):")
        for tag in unique_tags:
            print(f"  <{tag}>")

    # Look for key structural elements
    structural = ["Masthead", "Page", "PageSidebar", "Nav", "PageSection"]
    found = [s for s in structural if s in tsx_content]
    if found:
        print("\nKey structural PatternFly components detected:")
        for s in found:
            print(f"  - {s}")

    print("--- end AppLayout analysis ---\n")


def analyse_routes(tsx_content: str) -> None:
    """Print the navigation item tree from routes.tsx."""
    print("\n--- routes.tsx navigation analysis ---")

    # Look for route definitions -- common patterns:
    #   { path: '/foo', label: 'Foo', ... }
    #   <NavItem to="/foo">Foo</NavItem>
    paths = re.findall(
        r"""(?:path|to)\s*[:=]\s*['"]([^'"]+)['"]""",
        tsx_content,
    )
    labels = re.findall(
        r"""(?:label|title|navLabel)\s*[:=]\s*['"]([^'"]+)['"]""",
        tsx_content,
    )
    nav_items = re.findall(
        r"<NavItem[^>]*>([^<]+)</NavItem>",
        tsx_content,
    )

    if paths:
        print("\nRoute paths:")
        for p in paths:
            print(f"  {p}")

    if labels:
        print("\nRoute labels:")
        for lab in labels:
            print(f"  {lab}")

    if nav_items:
        print("\nNavItem text:")
        for ni in nav_items:
            print(f"  {ni.strip()}")

    # Try to detect nav groups / sections
    groups = re.findall(
        r"""(?:NavExpandable|NavGroup)[^>]*title\s*=\s*['"]([^'"]+)['"]""",
        tsx_content,
    )
    if groups:
        print("\nNav groups/expandable sections:")
        for g in groups:
            print(f"  [{g}]")

    print("--- end routes analysis ---\n")


# ── Metadata ───────────────────────────────────────────────────────────────

def write_metadata(
    shell_dir: Path,
    branch: str,
    project_id: str,
    deployed_url: str,
    fetched_files: list[str],
    failed_files: list[str],
) -> Path:
    """Write extraction-metadata.yaml (plain text, no yaml dependency)."""
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    source_url = f"https://{GITLAB_HOST}/uxd/prototypes/rhoai"

    lines = [
        f'branch: "{branch}"',
        f"project_id: {project_id}",
        f'extracted_at: "{now}"',
        f'source_url: "{source_url}"',
        f'deployed_url: "{deployed_url}"',
        "files_fetched:",
    ]
    for f in fetched_files:
        lines.append(f"  - {f}")

    if failed_files:
        lines.append("files_failed:")
        for f in failed_files:
            lines.append(f"  - {f}")

    lines.append(
        'notes: "CSS extracted directly from app.css. '
        "Shell HTML and nav maintained manually from AppLayout.tsx "
        'and routes.tsx analysis."'
    )
    lines.append("")  # trailing newline

    out = shell_dir / "extraction-metadata.yaml"
    out.write_text("\n".join(lines), encoding="utf-8")
    return out


# ── Verification instructions ──────────────────────────────────────────────

def print_verify_instructions(deployed_url: str) -> None:
    """Print manual verification instructions (Playwright MCP is interactive)."""
    print("\n--- Verification instructions ---")
    print(
        "The --verify flag is set. Playwright-based verification is done\n"
        "interactively via the Playwright MCP plugin in Claude Code, not\n"
        "by this Python script.\n"
    )
    print("To verify extracted styles against the deployed site:")
    print(f"  1. Open {deployed_url} in the browser")
    print("  2. Compare computed styles against shell.css values")
    print("  3. Check:")
    print("     - Masthead background color")
    print("     - Sidebar background color")
    print("     - Content area border-radius")
    print("     - Card border styles")
    print("     - Nav link active/hover styles")
    print("     - Overall layout dimensions (masthead height, sidebar width)")
    print("--- end verification ---\n")


# ── Main ───────────────────────────────────────────────────────────────────

def main() -> int:
    ap = argparse.ArgumentParser(
        description="Extract UXD prototype styles from the RHOAI GitLab repo.",
    )
    ap.add_argument(
        "--branch",
        default=DEFAULT_BRANCH,
        help=f"GitLab branch to fetch from (default: {DEFAULT_BRANCH})",
    )
    ap.add_argument(
        "--shell-dir",
        default=DEFAULT_SHELL_DIR,
        help=f"Output directory relative to repo root (default: {DEFAULT_SHELL_DIR})",
    )
    ap.add_argument(
        "--project-id",
        default=DEFAULT_PROJECT_ID,
        help=f"GitLab project ID (default: {DEFAULT_PROJECT_ID})",
    )
    ap.add_argument(
        "--verify",
        action="store_true",
        help="Print verification instructions for the deployed site",
    )
    ap.add_argument(
        "--deployed-url",
        default=DEFAULT_DEPLOYED_URL,
        help="URL of the deployed UXD prototype site",
    )
    args = ap.parse_args()

    shell_dir = REPO_ROOT / args.shell_dir
    if not shell_dir.is_dir():
        print(f"ERROR: shell directory does not exist: {shell_dir}")
        return 1

    print(f"Extracting UXD styles from branch '{args.branch}'")
    print(f"  Project : {args.project_id}")
    print(f"  Host    : {GITLAB_HOST}")
    print(f"  Output  : {shell_dir}")
    print()

    # ── Fetch all source files ────────────────────────────────────────────
    fetched: dict[str, str] = {}
    failed: list[str] = []

    for file_path in SOURCE_FILES:
        print(f"  Fetching {file_path} ... ", end="", flush=True)
        try:
            content = fetch_gitlab_file(args.project_id, file_path, args.branch)
            fetched[file_path] = content
            size = len(content)
            print(f"OK ({size:,} bytes)")
        except Exception as exc:
            print(f"FAILED ({exc})")
            failed.append(file_path)

    print()
    print(f"Fetched {len(fetched)}/{len(SOURCE_FILES)} files "
          f"({len(failed)} failed)")

    if not fetched:
        print("ERROR: no files fetched, aborting")
        return 1

    # ── Extract CSS ───────────────────────────────────────────────────────
    css_path = "src/app/app.css"
    if css_path in fetched:
        out = write_shell_css(fetched[css_path], shell_dir, args.branch)
        print(f"\nWrote {out.relative_to(REPO_ROOT)}")
    else:
        print(f"\nWARNING: {css_path} was not fetched; shell.css not updated")

    # ── Structural analysis ───────────────────────────────────────────────
    layout_path = "src/app/AppLayout/AppLayout.tsx"
    if layout_path in fetched:
        analyse_app_layout(fetched[layout_path])
    else:
        print(f"WARNING: {layout_path} not fetched; skipping layout analysis")

    routes_path = "src/app/routes.tsx"
    if routes_path in fetched:
        analyse_routes(fetched[routes_path])
    else:
        print(f"WARNING: {routes_path} not fetched; skipping routes analysis")

    # ── Log reference files ───────────────────────────────────────────────
    ref_files = [
        "src/app/AIHub/MCPServers/MCPCatalog.tsx",
        "src/app/AIHub/MCPServers/MCPCatalogDetails.tsx",
        "src/app/AIHub/MCPServers/DeployMCPServerModal.tsx",
    ]
    fetched_refs = [f for f in ref_files if f in fetched]
    if fetched_refs:
        print(f"Reference files fetched ({len(fetched_refs)}):")
        for f in fetched_refs:
            lines = fetched[f].count("\n") + 1
            print(f"  {f} ({lines} lines)")

    # ── Write metadata ────────────────────────────────────────────────────
    meta_path = write_metadata(
        shell_dir,
        args.branch,
        args.project_id,
        args.deployed_url,
        list(fetched.keys()),
        failed,
    )
    print(f"\nWrote {meta_path.relative_to(REPO_ROOT)}")

    # ── Verification ──────────────────────────────────────────────────────
    if args.verify:
        print_verify_instructions(args.deployed_url)

    # ── Summary ───────────────────────────────────────────────────────────
    print("Done. To update shell.html or nav/nav.html, review the")
    print("structural analysis above and edit manually.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
