"""Manifest-driven publishing: copy allowlisted public artifacts into the
pages repo clone and regenerate its landing index.html + snapshot."""
import hashlib
import html
import json
import re
import shutil
from datetime import date
from pathlib import Path
from urllib.parse import unquote

import yaml

SNAPSHOT = ".publish-snapshot.json"
BADGE_WINDOW_DAYS = 14


def _hash_source(src):
    """sha256 over artifact content. Directories hash a deterministic walk of
    relative POSIX paths + bytes so a rename counts as a change."""
    h = hashlib.sha256()
    src = Path(src)
    if src.is_dir():
        for f in sorted(p for p in src.rglob("*") if p.is_file()):
            h.update(f.relative_to(src).as_posix().encode("utf-8"))
            h.update(b"\0")
            h.update(f.read_bytes())
    else:
        h.update(src.read_bytes())
    return h.hexdigest()


def _snapshot_entry(old, dest):
    """Old snapshot row as a dict. v1 rows (plain source string) migrate to
    unknown hash + no published date so the first v2 run shows no false
    badges; hashes populate on that run."""
    e = old.get(dest)
    if isinstance(e, str):
        return {"source": e, "hash": None, "published": None, "badge": None}
    return e


def load_manifest(root):
    mpath = Path(root) / "publish" / "manifest.yaml"
    if not mpath.is_file():
        return []
    data = yaml.safe_load(mpath.read_text(encoding="utf-8")) or []
    return [e for e in data if isinstance(e, dict)]


def _feature_titles(root):
    """id -> display title from features/features.yaml, preserving the
    routing-table order (drives landing-page section order)."""
    p = Path(root) / "features" / "features.yaml"
    if not p.is_file():
        return {}
    try:
        data = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError:
        return {}
    return {f["id"]: (f.get("title") or f["id"])
            for f in (data.get("features") or [])
            if isinstance(f, dict) and f.get("id")}


def build_plan(root):
    root = Path(root)
    titles = _feature_titles(root)
    order = list(titles)
    plan = []
    for e in load_manifest(root):
        if e.get("audience") != "public":
            continue
        src = root / e["source"]
        dest = e["dest"].strip("/")
        is_dir = src.is_dir()
        parts = [p for p in str(e["source"]).replace("\\", "/").split("/") if p]
        if parts and parts[0] == "features" and len(parts) > 1:
            fid = parts[1]
            group = titles.get(fid, fid)
            group_key = (0, order.index(fid)) if fid in order else (1, fid)
        elif parts and parts[0] == "narrative":
            group, group_key = "Narrative", (2, "")
        else:
            group, group_key = (parts[0] if parts else "Other",
                                (1, parts[0] if parts else ""))
        plan.append({
            "src": src,
            "dest": dest,
            "is_dir": is_dir,
            "title": e["title"],
            "description": e["description"],
            "href": dest + "/" if is_dir else dest,
            "group": group,
            "group_key": group_key,
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
    today = date.today()
    for p in plan:
        prev = _snapshot_entry(old, p["dest"])
        digest = _hash_source(p["src"])
        if prev is None:
            published, badge = today.isoformat(), "new"
        elif prev.get("hash") and prev["hash"] != digest:
            published, badge = today.isoformat(), "updated"
        else:
            published, badge = prev.get("published"), prev.get("badge")
        p["hash"], p["published"], p["badge"] = digest, published, badge
        active = (published is not None and
                  (today - date.fromisoformat(published)).days <= BADGE_WINDOW_DAYS)
        p["show_badge"] = badge if active else None
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
        json.dumps({p["dest"]: {"source": p["src"].relative_to(root).as_posix(),
                                "hash": p["hash"],
                                "published": p["published"],
                                "badge": p["badge"]}
                    for p in plan},
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
