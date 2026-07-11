from pathlib import Path

from hublib.refresh import find_configs, validate


def write(root: Path, rel: str, text: str):
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8", newline="\n")
    return p


VALID = """\
site: features/x/enablement/site/
sources:
  gdocs:
  - {id: abc123, title: Overview}
  github:
  - org/repo
  jira:
    keys: [X-1]
  slack:
    channels: [general]
    window_days: 14
  local:
  - features/x/knowledge/
"""


def make_site(root):
    write(root, "features/x/enablement/site/index.html", "<html></html>")


def test_valid_config_passes(tmp_path):
    make_site(tmp_path)
    write(tmp_path, "features/x/work/refresh-site.yaml", VALID)
    assert validate(tmp_path) == ([], [])


def test_find_configs_covers_features_and_narrative(tmp_path):
    write(tmp_path, "features/x/work/refresh-a.yaml", "site: s\n")
    write(tmp_path, "narrative/work/refresh-b.yaml", "site: s\n")
    rels = [p.relative_to(tmp_path).as_posix() for p in find_configs(tmp_path)]
    assert rels == ["features/x/work/refresh-a.yaml", "narrative/work/refresh-b.yaml"]


def test_missing_site_is_error(tmp_path):
    write(tmp_path, "features/x/work/refresh-site.yaml", "sources:\n  github: [a/b]\n")
    errors, _ = validate(tmp_path)
    assert any("missing 'site'" in e for e in errors)


def test_bad_site_shape_is_error(tmp_path):
    write(tmp_path, "features/x/work/refresh-site.yaml",
          "site: features/x/site/\nsources:\n  github: [a/b]\n")
    errors, _ = validate(tmp_path)
    assert any("site must be" in e for e in errors)


def test_nonexistent_site_is_error(tmp_path):
    write(tmp_path, "features/x/work/refresh-site.yaml", VALID)
    errors, _ = validate(tmp_path)
    assert any("site does not exist" in e for e in errors)


def test_unknown_source_type_is_error(tmp_path):
    make_site(tmp_path)
    write(tmp_path, "features/x/work/refresh-site.yaml",
          "site: features/x/enablement/site/\nsources:\n  webscrape: [a]\n")
    errors, _ = validate(tmp_path)
    assert any("unknown source type 'webscrape'" in e for e in errors)


def test_empty_source_type_is_error(tmp_path):
    make_site(tmp_path)
    write(tmp_path, "features/x/work/refresh-site.yaml",
          "site: features/x/enablement/site/\nsources:\n  github: []\n")
    errors, _ = validate(tmp_path)
    assert any("source type 'github' is empty" in e for e in errors)


def test_gdoc_without_id_is_error(tmp_path):
    make_site(tmp_path)
    write(tmp_path, "features/x/work/refresh-site.yaml",
          "site: features/x/enablement/site/\nsources:\n  gdocs:\n"
          "  - {title: No Id}\n")
    errors, _ = validate(tmp_path)
    assert any("gdocs[0] needs an 'id'" in e for e in errors)


def test_slack_without_channels_is_error(tmp_path):
    make_site(tmp_path)
    write(tmp_path, "features/x/work/refresh-site.yaml",
          "site: features/x/enablement/site/\nsources:\n  slack:\n"
          "    window_days: 7\n")
    errors, _ = validate(tmp_path)
    assert any("slack needs a 'channels' list" in e for e in errors)


def test_missing_sources_is_error(tmp_path):
    make_site(tmp_path)
    write(tmp_path, "features/x/work/refresh-site.yaml",
          "site: features/x/enablement/site/\n")
    errors, _ = validate(tmp_path)
    assert any("'sources' must be a non-empty mapping" in e for e in errors)


def test_invalid_yaml_is_error(tmp_path):
    write(tmp_path, "features/x/work/refresh-site.yaml", "site: [unclosed\n")
    errors, _ = validate(tmp_path)
    assert any("invalid YAML" in e for e in errors)


def test_lint_repo_wires_refresh_validation(tmp_path):
    from hublib.schema import lint_repo
    write(tmp_path, "AGENTS.md", "# a\n")
    write(tmp_path, "features/x/work/refresh-site.yaml", "sources:\n  github: [a/b]\n")
    errors, _ = lint_repo(tmp_path)
    assert any("refresh-site.yaml" in e and "missing 'site'" in e for e in errors)


def test_sections_block_valid(tmp_path):
    make_site(tmp_path)
    write(tmp_path, "features/x/work/refresh-site.yaml",
          VALID + "sections:\n  jtbd: true\n  jira_tracker: {project: RHAISTRAT}\n")
    assert validate(tmp_path) == ([], [])


def test_sections_block_invalid(tmp_path):
    make_site(tmp_path)
    write(tmp_path, "features/x/work/refresh-site.yaml",
          VALID + "sections:\n  bogus: 1\n  jtbd: yes please\n  jira_tracker: {}\n")
    errors, _ = validate(tmp_path)
    assert len([e for e in errors if "section" in e]) == 3


def test_sections_errors_survive_missing_sources(tmp_path):
    make_site(tmp_path)
    write(tmp_path, "features/x/work/refresh-site.yaml",
          "site: features/x/enablement/site/\nsections:\n  bogus: 1\n")
    errors, _ = validate(tmp_path)
    assert any("unknown section 'bogus'" in e for e in errors)
    assert any("sources" in e for e in errors)
