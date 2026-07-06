import datetime
from pathlib import Path

from hublib.indexer import MARKER, build_all, check, write_all


def write(root: Path, rel: str, text: str):
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8", newline="\n")
    return p


TODAY = datetime.date(2026, 7, 5)


def make_repo(tmp_path: Path) -> Path:
    write(tmp_path, "conventions/staleness.yaml",
          "profile_default_days: 30\nfact_default_days: 90\n")
    write(tmp_path, "features/features.yaml",
          "features:\n- id: mcp-registry\n  title: MCP Registry\n  description: Registry MVP\n")
    write(tmp_path, "features/mcp-registry/knowledge/decision-split.md",
          "---\ntype: decision\ntitle: Registry vs catalog\ndescription: the split\n"
          "timestamp: 2026-07-01\ndecided: 2026-07-01\nstatus: current\n---\nb\n")
    write(tmp_path, "features/mcp-registry/knowledge/question-skus.md",
          "---\ntype: question\ntitle: SKU model?\ndescription: open q\n"
          "timestamp: 2026-07-01\nstatus: open\n---\nb\n")
    write(tmp_path, "features/mcp-registry/knowledge/ref-epic.md",
          "---\ntype: reference\ntitle: Main epic\ndescription: epic ref\n"
          "timestamp: 2026-07-01\n"
          "resource: https://redhat.atlassian.net/browse/RHAIRFE-1370\n---\nb\n")
    write(tmp_path, "features/mcp-registry/knowledge/person-jane.md",
          "---\ntype: person\ntitle: Jane Doe\ndescription: PM partner\n"
          "timestamp: 2026-07-01\nrole: PM\norg: Red Hat\n---\nb\n")
    write(tmp_path, "memory/profiles/roadmap.md",
          "---\ntype: profile\ndescription: 3.5 DP dates\ntimestamp: 2026-05-01\n"
          "review_after: 2026-06-01\nstatus: current\n---\nb\n")
    write(tmp_path, "memory/facts/fact-d.md",
          "---\ntype: fact\ndescription: a decision\ntimestamp: 2026-07-01\n"
          "status: current\n---\nb\n")
    write(tmp_path, "memory/log.md",
          "---\ntype: fact\ndescription: log\ntimestamp: 2026-07-05\n---\n"
          "## 2026-07-05\n- **Update** — newest thing.\n"
          "## 2026-07-01\n- **Creation** — older thing.\n")
    return tmp_path


def test_build_all_produces_expected_files(tmp_path):
    built = build_all(make_repo(tmp_path), today=TODAY)
    assert set(built) >= {
        "features/index.md",
        "features/mcp-registry/index.md",
        "features/mcp-registry/knowledge/index.md",
        "memory/index.md",
        "views/decisions.md", "views/open-questions.md",
        "views/stale-facts.md", "views/jira-map.md", "views/people.md",
    }
    for content in built.values():
        assert content.startswith(MARKER)
        assert content.endswith("\n")


def test_views_content(tmp_path):
    built = build_all(make_repo(tmp_path), today=TODAY)
    assert ("[Registry vs catalog](/features/mcp-registry/knowledge/decision-split.md)"
            in built["views/decisions.md"])
    assert "SKU model?" in built["views/open-questions.md"]
    assert "RHAIRFE-1370" in built["views/jira-map.md"]
    assert "Jane Doe" in built["views/people.md"]
    # roadmap profile is past review_after (2026-06-01 < today)
    assert "/memory/profiles/roadmap.md" in built["views/stale-facts.md"]


def test_memory_index_shape(tmp_path):
    built = build_all(make_repo(tmp_path), today=TODAY)
    idx = built["memory/index.md"]
    assert "- [roadmap](/memory/profiles/roadmap.md) — 3.5 DP dates" in idx
    assert "- [fact-d](/memory/facts/fact-d.md) — a decision" in idx
    assert "- 2026-07-05 — **Update** — newest thing." in idx


def test_check_flags_stale_and_write_all_fixes(tmp_path):
    root = make_repo(tmp_path)
    stale = check(root, today=TODAY)
    assert "features/index.md" in stale          # never generated yet
    write_all(root, today=TODAY)
    assert check(root, today=TODAY) == []
    (root / "views" / "decisions.md").write_text("tampered", encoding="utf-8")
    assert check(root, today=TODAY) == ["views/decisions.md"]


def test_feature_index_ignores_untracked_content(tmp_path):
    root = make_repo(tmp_path)
    before = build_all(root, today=TODAY)["features/mcp-registry/index.md"]
    write(root, "features/mcp-registry/work/transcripts/t.md", "x\n")
    after = build_all(root, today=TODAY)["features/mcp-registry/index.md"]
    assert before == after
    assert "file(s)" not in after
