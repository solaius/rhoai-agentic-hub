"""Manifest-driven publishing: copy allowlisted public artifacts into the
pages repo clone and regenerate its landing index.html + snapshot."""
import html
import json
import re
import shutil
from pathlib import Path
from urllib.parse import unquote

import yaml

SNAPSHOT = ".publish-snapshot.json"


def load_manifest(root):
    mpath = Path(root) / "publish" / "manifest.yaml"
    if not mpath.is_file():
        return []
    data = yaml.safe_load(mpath.read_text(encoding="utf-8")) or []
    return [e for e in data if isinstance(e, dict)]


def build_plan(root):
    root = Path(root)
    plan = []
    for e in load_manifest(root):
        if e.get("audience") != "public":
            continue
        src = root / e["source"]
        dest = e["dest"].strip("/")
        is_dir = src.is_dir()
        plan.append({
            "src": src,
            "dest": dest,
            "is_dir": is_dir,
            "title": e["title"],
            "description": e["description"],
            "href": dest + "/" if is_dir else dest,
        })
    return plan


def generate_landing(plan, hub_sha=""):
    items = "\n".join(
        f'      <li><a href="{html.escape(p["href"])}">{html.escape(p["title"])}</a>'
        f' — {html.escape(p["description"])}</li>'
        for p in sorted(plan, key=lambda p: p["dest"]))
    if not items:
        items = "      <li>No published artifacts yet.</li>"
    sha_line = (f'\n    <p class="meta">hub commit: {html.escape(hub_sha)}</p>'
                if hub_sha else "")
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>rhoai-agentic-hub — published artifacts</title>
  <style>
    body {{ font-family: system-ui, sans-serif; max-width: 720px;
           margin: 3rem auto; padding: 0 1rem; }}
    .meta {{ color: #666; font-size: .85rem; }}
  </style>
</head>
<body>
  <h1>rhoai-agentic-hub — published artifacts</h1>
  <ul>
{items}
  </ul>{sha_line}
  <p class="meta">Generated from publish/manifest.yaml — do not edit by hand.</p>
</body>
</html>
"""


def apply(root, pages_dir, hub_sha=""):
    root, pages = Path(root), Path(pages_dir)
    plan = build_plan(root)
    warnings = []
    snap_path = pages / SNAPSHOT
    old = json.loads(snap_path.read_text(encoding="utf-8")) if snap_path.is_file() else {}
    new_dests = {p["dest"] for p in plan}
    pages_root = pages.resolve()
    for dest in sorted(set(old) - new_dests):
        warnings.append(f"dest '{dest}' was published before and is no longer in the "
                        f"manifest — its files will be removed (dest slugs are contracts)")
        target = pages / dest
        if not target.resolve().is_relative_to(pages_root):
            warnings.append(f"snapshot dest escapes pages dir, skipped: {dest}")
            continue
        if target.is_dir():
            shutil.rmtree(target)
        elif target.is_file():
            target.unlink()
    copied = []
    for p in plan:
        target = pages / p["dest"]
        if not target.resolve().is_relative_to(pages_root):
            raise ValueError(f"dest escapes pages dir: {p['dest']}")
        if target.is_dir():
            shutil.rmtree(target)
        elif target.exists():
            target.unlink()
        if p["is_dir"]:
            shutil.copytree(p["src"], target)
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(p["src"], target)
        copied.append(p["dest"])
    (pages / "index.html").write_text(generate_landing(plan, hub_sha),
                                      encoding="utf-8", newline="\n")
    snap_path.write_text(
        json.dumps({p["dest"]: p["src"].relative_to(root).as_posix() for p in plan},
                   indent=2, sort_keys=True) + "\n",
        encoding="utf-8", newline="\n")
    return copied, warnings


LINK_ATTR_RE = re.compile(r"""(?<![-\w:])(?:href|src)\s*=\s*["']([^"']+)["']""",
                          re.IGNORECASE)
EXTERNAL_PREFIXES = ("http://", "https://", "//", "mailto:", "data:", "javascript:", "#")


def check_links(pages_dir):
    """Internal-link integrity of a pages clone: every href/src in every HTML
    file must resolve to a file, or to a directory holding index.html (a bare
    directory link 404s on GitHub Pages without one). External schemes and
    fragment-only links are out of scope."""
    pages = Path(pages_dir)
    pages_root = pages.resolve()
    errors = []
    for f in sorted(pages.rglob("*.html")):
        if ".git" in f.parts:
            continue
        rel = f.relative_to(pages).as_posix()
        text = f.read_text(encoding="utf-8", errors="replace")
        for m in LINK_ATTR_RE.finditer(text):
            raw = m.group(1).strip()
            if raw.lower().startswith(EXTERNAL_PREFIXES):
                continue
            target = unquote(raw.split("#", 1)[0].split("?", 1)[0])
            if not target:
                continue
            resolved = (pages / target.lstrip("/")) if target.startswith("/") \
                else (f.parent / target)
            try:
                contained = resolved.resolve().is_relative_to(pages_root)
            except OSError:
                contained = False
            if not contained:
                errors.append(f"{rel}: broken link {raw}")
                continue
            if resolved.is_file():
                continue
            if resolved.is_dir() and (resolved / "index.html").is_file():
                continue
            errors.append(f"{rel}: broken link {raw}")
    return errors
