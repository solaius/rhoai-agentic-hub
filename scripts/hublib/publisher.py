"""Manifest-driven publishing: copy allowlisted public artifacts into the
pages repo clone and regenerate its landing index.html + snapshot."""
import html
import json
import shutil
from pathlib import Path

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
    for dest in sorted(set(old) - new_dests):
        warnings.append(f"dest '{dest}' was published before and is no longer in the "
                        f"manifest — its files will be removed (dest slugs are contracts)")
        target = pages / dest
        if target.is_dir():
            shutil.rmtree(target)
        elif target.is_file():
            target.unlink()
    copied = []
    for p in plan:
        target = pages / p["dest"]
        if p["is_dir"]:
            if target.exists():
                shutil.rmtree(target)
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
