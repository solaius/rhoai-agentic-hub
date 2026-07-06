import json
from pathlib import Path

from hublib.publisher import SNAPSHOT, apply, build_plan, generate_landing


def write(root: Path, rel: str, text: str):
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8", newline="\n")
    return p


MANIFEST = """\
- source: features/x/enablement/site/
  dest: x/site/
  audience: public
  title: A <Site>
  description: demo & test
- source: features/x/enablement/one-pager.html
  dest: x/one-pager.html
  audience: public
  title: One pager
  description: single file
- source: features/x/enablement/internal/
  dest: x/internal/
  audience: internal
  title: Internal only
  description: must not publish in v1
"""


def make_repo(tmp_path: Path) -> Path:
    root = tmp_path / "hub"
    write(root, "features/x/enablement/site/index.html", "<html>site</html>")
    write(root, "features/x/enablement/site/style.css", "body{}")
    write(root, "features/x/enablement/one-pager.html", "<html>one</html>")
    write(root, "features/x/enablement/internal/index.html", "<html>secret</html>")
    write(root, "publish/manifest.yaml", MANIFEST)
    return root


def test_build_plan_public_only(tmp_path):
    plan = build_plan(make_repo(tmp_path))
    dests = {p["dest"] for p in plan}
    assert dests == {"x/site", "x/one-pager.html"}
    site = next(p for p in plan if p["dest"] == "x/site")
    assert site["is_dir"] is True and site["href"] == "x/site/"


def test_generate_landing_escapes_and_lists(tmp_path):
    plan = build_plan(make_repo(tmp_path))
    out = generate_landing(plan, hub_sha="abc123")
    assert "A &lt;Site&gt;" in out
    assert 'href="x/site/"' in out
    assert "abc123" in out
    assert "Internal only" not in out


def test_apply_copies_and_snapshots(tmp_path):
    root = make_repo(tmp_path)
    pages = tmp_path / "pages"
    pages.mkdir()
    copied, warnings = apply(root, pages, hub_sha="abc")
    assert sorted(copied) == ["x/one-pager.html", "x/site"]
    assert warnings == []
    assert (pages / "x/site/index.html").is_file()
    assert (pages / "x/site/style.css").is_file()
    assert (pages / "x/one-pager.html").is_file()
    assert not (pages / "x/internal").exists()
    assert (pages / "index.html").is_file()
    snap = json.loads((pages / SNAPSHOT).read_text())
    assert snap == {"x/one-pager.html": "features/x/enablement/one-pager.html",
                    "x/site": "features/x/enablement/site"}


def test_apply_warns_and_removes_on_dropped_dest(tmp_path):
    root = make_repo(tmp_path)
    pages = tmp_path / "pages"
    pages.mkdir()
    apply(root, pages)
    # drop the site entry (its 5 manifest lines) from the manifest
    write(root, "publish/manifest.yaml", "\n".join(MANIFEST.splitlines()[5:]) + "\n")
    copied, warnings = apply(root, pages)
    assert copied == ["x/one-pager.html"]
    assert any("x/site" in w and "no longer in the manifest" in w for w in warnings)
    assert not (pages / "x/site").exists()


def test_manifest_rejects_traversal_dest(tmp_path):
    from hublib.schema import validate_manifest
    root = make_repo(tmp_path)
    write(root, "publish/manifest.yaml",
          "- source: features/x/enablement/one-pager.html\n  dest: ../evil.html\n"
          "  audience: public\n  title: T\n  description: D\n")
    errors = validate_manifest(root)
    assert any("without '..'" in e for e in errors)


def test_apply_handles_dest_type_swap(tmp_path):
    root = make_repo(tmp_path)
    pages = tmp_path / "pages"
    pages.mkdir()
    apply(root, pages)
    # same dest strings, swapped source types: dir dest -> file source, file dest -> dir source
    write(root, "publish/manifest.yaml",
          "- source: features/x/enablement/one-pager.html\n  dest: x/site/\n"
          "  audience: public\n  title: T\n  description: D\n"
          "- source: features/x/enablement/site/\n  dest: x/one-pager.html\n"
          "  audience: public\n  title: T2\n  description: D2\n")
    copied, warnings = apply(root, pages)
    assert (pages / "x/site").is_file()
    assert (pages / "x/one-pager.html").is_dir()
    assert (pages / "x/one-pager.html" / "index.html").is_file()


def test_manifest_rejects_dot_dest(tmp_path):
    from hublib.schema import validate_manifest
    root = make_repo(tmp_path)
    write(root, "publish/manifest.yaml",
          "- source: features/x/enablement/one-pager.html\n  dest: .\n"
          "  audience: public\n  title: T\n  description: D\n")
    errors = validate_manifest(root)
    assert any("must be a relative path" in e for e in errors)
