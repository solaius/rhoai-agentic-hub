import json
import shutil
from pathlib import Path

from hublib.publisher import SNAPSHOT, apply, build_plan, check_links, generate_landing

REPO_ROOT = Path(__file__).resolve().parents[2]


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

FEATURES_YAML = """\
features:
- id: x
  title: X Feature
- id: y
  title: Y Feature
"""


def make_repo(tmp_path: Path) -> Path:
    root = tmp_path / "hub"
    write(root, "features/x/enablement/site/index.html", "<html>site</html>")
    write(root, "features/x/enablement/site/style.css", "body{}")
    write(root, "features/x/enablement/one-pager.html", "<html>one</html>")
    write(root, "features/x/enablement/internal/index.html", "<html>secret</html>")
    write(root, "publish/manifest.yaml", MANIFEST)
    write(root, "features/features.yaml", FEATURES_YAML)
    (root / "publish").mkdir(parents=True, exist_ok=True)
    shutil.copy(REPO_ROOT / "publish" / "landing-template.html",
                root / "publish" / "landing-template.html")
    return root


def test_build_plan_public_only(tmp_path):
    plan = build_plan(make_repo(tmp_path))
    dests = {p["dest"] for p in plan}
    assert dests == {"x/site", "x/one-pager.html"}
    site = next(p for p in plan if p["dest"] == "x/site")
    assert site["is_dir"] is True and site["href"] == "x/site/"


def test_generate_landing_escapes_and_lists(tmp_path):
    root = make_repo(tmp_path)
    plan = build_plan(root)
    out = generate_landing(root, plan, hub_sha="abc123")
    assert "A &lt;Site&gt;" in out
    assert 'href="x/site/"' in out
    assert "abc123" in out
    assert "Internal only" not in out
    assert "<h2>X Feature</h2>" in out


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
    assert set(snap) == {"x/one-pager.html", "x/site"}
    site = snap["x/site"]
    assert site["source"] == "features/x/enablement/site"
    assert site["badge"] == "new"
    assert site["published"] is not None
    assert len(site["hash"]) == 64


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


def make_pages(tmp_path):
    pages = tmp_path / "pages"
    write(pages, "index.html",
          '<a href="x/site/">site</a> <a href="x/one-pager.html">one</a>')
    write(pages, "x/site/index.html",
          '<link href="style.css"><img src="../one-pager.html">'
          '<a href="https://example.com/x">ext</a> <a href="#top">frag</a>'
          '<a href="mailto:a@b.c">mail</a>')
    write(pages, "x/site/style.css", "body{}")
    write(pages, "x/one-pager.html", "<html></html>")
    return pages


def test_check_links_clean_site(tmp_path):
    assert check_links(make_pages(tmp_path)) == []


def test_check_links_broken_href_and_src(tmp_path):
    pages = make_pages(tmp_path)
    write(pages, "x/broken.html", '<a href="gone.html">g</a><img src="img/gone.png">')
    errors = check_links(pages)
    assert "x/broken.html: broken link gone.html" in errors
    assert "x/broken.html: broken link img/gone.png" in errors


def test_check_links_root_absolute(tmp_path):
    pages = make_pages(tmp_path)
    write(pages, "x/site/abs.html",
          '<a href="/x/one-pager.html">ok</a><a href="/nope.html">bad</a>')
    assert check_links(pages) == ["x/site/abs.html: broken link /nope.html"]


def test_check_links_dir_without_index_is_error(tmp_path):
    pages = make_pages(tmp_path)
    write(pages, "x/noindex/readme.txt", "hi")
    write(pages, "dirlink.html", '<a href="x/noindex/">d</a>')
    assert check_links(pages) == ["dirlink.html: broken link x/noindex/"]


def test_check_links_percent_encoding_and_query(tmp_path):
    pages = make_pages(tmp_path)
    write(pages, "x/my file.html", "<html></html>")
    write(pages, "enc.html",
          '<a href="x/my%20file.html">e</a><a href="x/one-pager.html?v=2">q</a>')
    assert check_links(pages) == []


def test_check_links_all_external_prefixes_skipped(tmp_path):
    pages = make_pages(tmp_path)
    write(pages, "prefixes.html",
          '<a href="http://example.com/x">h</a><a href="//cdn.example.com/x">p</a>'
          '<img src="data:image/png;base64,AAAA"><a href="javascript:void(0)">j</a>')
    assert check_links(pages) == []


def test_check_links_git_dir_skipped(tmp_path):
    pages = make_pages(tmp_path)
    write(pages, ".git/hooks/doc.html", '<a href="gone.html">broken but ignored</a>')
    assert check_links(pages) == []


def test_check_links_fragment_and_query_on_real_path(tmp_path):
    pages = make_pages(tmp_path)
    write(pages, "frag.html",
          '<a href="x/one-pager.html#sec">f</a><a href="x/one-pager.html?v=1#s">q</a>')
    assert check_links(pages) == []


def test_check_links_escaping_link_is_error(tmp_path):
    pages = make_pages(tmp_path)
    write(tmp_path, "outside.html", "<html></html>")
    write(pages, "esc.html", '<a href="../outside.html">e</a>')
    assert check_links(pages) == ["esc.html: broken link ../outside.html"]


def test_check_links_uppercase_scheme_skipped(tmp_path):
    pages = make_pages(tmp_path)
    write(pages, "up.html", '<a href="HTTPS://example.com/x">u</a>')
    assert check_links(pages) == []


def test_check_links_data_and_namespaced_attrs_not_scanned(tmp_path):
    pages = make_pages(tmp_path)
    write(pages, "attrs.html", '<a data-href="gone.html">d</a><use xlink:href="gone.svg"/>')
    assert check_links(pages) == []


def test_build_plan_groups_by_source_area(tmp_path):
    root = make_repo(tmp_path)
    write(root, "narrative/enablement/story/index.html", "<html></html>")
    write(root, "publish/manifest.yaml", MANIFEST +
          "- source: narrative/enablement/story/\n  dest: narrative/story/\n"
          "  audience: public\n  title: Story\n  description: narr\n")
    plan = build_plan(root)
    by_dest = {p["dest"]: p for p in plan}
    assert by_dest["x/site"]["group"] == "X Feature"
    assert by_dest["x/site"]["group_key"] == (0, 0)
    assert by_dest["narrative/story"]["group"] == "Narrative"
    assert by_dest["narrative/story"]["group_key"] == (2, "")


def test_build_plan_unknown_feature_id_falls_back(tmp_path):
    root = make_repo(tmp_path)
    write(root, "features/zed/enablement/deck/index.html", "<html></html>")
    write(root, "publish/manifest.yaml",
          "- source: features/zed/enablement/deck/\n  dest: zed/deck/\n"
          "  audience: public\n  title: Z\n  description: D\n")
    plan = build_plan(root)
    assert plan[0]["group"] == "zed"
    assert plan[0]["group_key"] == (1, "zed")


def test_apply_badge_lifecycle(tmp_path):
    root = make_repo(tmp_path)
    pages = tmp_path / "pages"
    pages.mkdir()
    apply(root, pages)
    snap1 = json.loads((pages / SNAPSHOT).read_text())
    assert snap1["x/site"]["badge"] == "new"
    apply(root, pages)  # unchanged: carried forward verbatim
    snap2 = json.loads((pages / SNAPSHOT).read_text())
    assert snap2["x/site"] == snap1["x/site"]
    write(root, "features/x/enablement/site/index.html", "<html>site v2</html>")
    apply(root, pages)  # content change: flips to updated
    snap3 = json.loads((pages / SNAPSHOT).read_text())
    assert snap3["x/site"]["badge"] == "updated"
    assert snap3["x/site"]["hash"] != snap1["x/site"]["hash"]
    out = (pages / "index.html").read_text(encoding="utf-8")
    assert "badge--updated" in out
    assert ">Updated " in out


def test_apply_migrates_v1_snapshot_without_false_badges(tmp_path):
    root = make_repo(tmp_path)
    pages = tmp_path / "pages"
    pages.mkdir()
    (pages / SNAPSHOT).write_text(json.dumps(
        {"x/one-pager.html": "features/x/enablement/one-pager.html",
         "x/site": "features/x/enablement/site"}), encoding="utf-8")
    apply(root, pages)
    snap = json.loads((pages / SNAPSHOT).read_text())
    assert snap["x/site"]["badge"] is None
    assert snap["x/site"]["published"] is None
    assert len(snap["x/site"]["hash"]) == 64


def test_hash_source_dir_is_deterministic_and_content_sensitive(tmp_path):
    from hublib.publisher import _hash_source
    root = make_repo(tmp_path)
    src = root / "features/x/enablement/site"
    h1 = _hash_source(src)
    assert h1 == _hash_source(src)
    write(root, "features/x/enablement/site/style.css", "body{color:red}")
    assert _hash_source(src) != h1


def test_generate_landing_group_order(tmp_path):
    root = make_repo(tmp_path)
    write(root, "narrative/enablement/story/index.html", "<html></html>")
    write(root, "features/zed/enablement/deck/index.html", "<html></html>")
    write(root, "publish/manifest.yaml", MANIFEST +
          "- source: narrative/enablement/story/\n  dest: narrative/story/\n"
          "  audience: public\n  title: Story\n  description: narr\n"
          "- source: features/zed/enablement/deck/\n  dest: zed/deck/\n"
          "  audience: public\n  title: Zed\n  description: unknown feature\n")
    out = generate_landing(root, build_plan(root), "")
    assert (out.index("<h2>X Feature</h2>") < out.index("<h2>zed</h2>")
            < out.index("<h2>Narrative</h2>"))


def test_generate_landing_empty_plan(tmp_path):
    root = make_repo(tmp_path)
    out = generate_landing(root, [], "")
    assert "No published artifacts yet." in out


def test_apply_landing_shows_new_badge(tmp_path):
    root = make_repo(tmp_path)
    pages = tmp_path / "pages"
    pages.mkdir()
    apply(root, pages)
    out = (pages / "index.html").read_text(encoding="utf-8")
    assert "badge--new" in out and ">NEW</span>" in out


def test_badge_ages_out_after_window(tmp_path):
    from hublib.publisher import _hash_source
    root = make_repo(tmp_path)
    write(root, "publish/manifest.yaml",
          "- source: features/x/enablement/site/\n  dest: x/site/\n"
          "  audience: public\n  title: Old Site\n  description: D\n")
    pages = tmp_path / "pages"
    pages.mkdir()
    digest = _hash_source(root / "features/x/enablement/site")
    (pages / SNAPSHOT).write_text(json.dumps(
        {"x/site": {"source": "features/x/enablement/site", "hash": digest,
                    "published": "2020-01-01", "badge": "new"}}),
        encoding="utf-8")
    apply(root, pages)
    out = (pages / "index.html").read_text(encoding="utf-8")
    # Not "badge--new" not in out: that class name is also present in the
    # template's static <style> block regardless of any card rendering it.
    assert ">NEW</span>" not in out
