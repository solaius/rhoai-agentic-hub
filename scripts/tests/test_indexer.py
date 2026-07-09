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


def test_check_ignores_time_dependent_stale_view(tmp_path):
    root = make_repo(tmp_path)
    write_all(root, today=TODAY)
    # far future: staleness membership changes, but freshness must stay clean
    assert check(root, today=datetime.date(2027, 1, 1)) == []


def add_narrative(root: Path):
    write(root, "narrative/knowledge/pillar-agents.md",
          "---\ntype: pillar\ntitle: Agents\ndescription: control plane pillar\n"
          "timestamp: 2026-07-01\nstatus: current\n---\nb\n")
    write(root, "narrative/knowledge/story-governed-mcp.md",
          "---\ntype: story\ntitle: Governed MCP\ndescription: registry to gateway\n"
          "timestamp: 2026-07-01\nfeatures: [mcp-registry]\n"
          "pillar: /narrative/knowledge/pillar-agents.md\nstatus: current\n---\nb\n")
    write(root, "narrative/knowledge/decision-narrative-home.md",
          "---\ntype: decision\ntitle: Narrative home\ndescription: top-level layer\n"
          "timestamp: 2026-07-02\ndecided: 2026-07-02\nstatus: current\n---\nb\n")
    write(root, "narrative/knowledge/person-joe.md",
          "---\ntype: person\ntitle: Joe Strategist\ndescription: strategy owner\n"
          "timestamp: 2026-07-01\nrole: VP\norg: Red Hat\n---\nb\n")
    return root


def test_narrative_indexes_generated(tmp_path):
    built = build_all(add_narrative(make_repo(tmp_path)), today=TODAY)
    assert "narrative/index.md" in built
    idx = built["narrative/knowledge/index.md"]
    assert "## pillar" in idx and "## story" in idx
    assert "[Governed MCP](/narrative/knowledge/story-governed-mcp.md)" in idx


def test_narrative_entries_reach_shared_views(tmp_path):
    built = build_all(add_narrative(make_repo(tmp_path)), today=TODAY)
    assert "Narrative home" in built["views/decisions.md"]
    assert "- narrative · [Joe Strategist](/narrative/knowledge/person-joe.md)" \
        in built["views/people.md"]


def test_no_narrative_dir_no_narrative_index(tmp_path):
    built = build_all(make_repo(tmp_path), today=TODAY)
    assert "narrative/index.md" not in built


def test_convergence_with_narrative(tmp_path):
    root = add_narrative(make_repo(tmp_path))
    write_all(root, today=TODAY)
    assert check(root, today=TODAY) == []


def test_feature_connections_section(tmp_path):
    root = add_narrative(make_repo(tmp_path))
    built = build_all(root, today=TODAY)
    idx = built["features/mcp-registry/index.md"]
    assert "## Connections" in idx
    assert "[Governed MCP](/narrative/knowledge/story-governed-mcp.md)" in idx


def test_connections_exclude_own_home_and_absent_when_empty(tmp_path):
    root = make_repo(tmp_path)
    # entry in mcp-registry listing itself must NOT create a self-backlink
    write(root, "features/mcp-registry/knowledge/fact-self.md",
          "---\ntype: fact\ndescription: d\ntimestamp: 2026-07-01\n"
          "features: [mcp-registry]\n---\nb\n")
    idx = build_all(root, today=TODAY)["features/mcp-registry/index.md"]
    assert "## Connections" not in idx


def test_artifact_descriptor_creates_connection(tmp_path):
    root = make_repo(tmp_path)
    write(root, "features/features.yaml",
          "features:\n- id: mcp-registry\n  title: MCP Registry\n  description: d\n"
          "- id: mcp-gateway\n  title: MCP Gateway\n  description: d\n")
    write(root, "features/mcp-gateway/enablement/deck/artifact.md",
          "---\ntype: artifact\ntitle: Big Deck\ndescription: cross deck\n"
          "timestamp: 2026-07-01\nfeatures: [mcp-registry]\n---\nb\n")
    idx = build_all(root, today=TODAY)["features/mcp-registry/index.md"]
    assert "[Big Deck](/features/mcp-gateway/enablement/deck/artifact.md)" in idx


def test_narrative_map_view(tmp_path):
    root = add_narrative(make_repo(tmp_path))
    write(root, "narrative/knowledge/story-orphan.md",
          "---\ntype: story\ntitle: Orphan\ndescription: no pillar yet\n"
          "timestamp: 2026-07-01\nfeatures: [mcp-registry]\nstatus: current\n---\nb\n")
    v = build_all(root, today=TODAY)["views/narrative-map.md"]
    assert "## [Agents](/narrative/knowledge/pillar-agents.md)" in v
    assert "[Governed MCP](/narrative/knowledge/story-governed-mcp.md)" in v
    assert "connects: [mcp-registry](/features/mcp-registry/index.md)" in v
    assert "## Stories without a pillar" in v and "Orphan" in v


def test_faq_view(tmp_path):
    root = make_repo(tmp_path)
    write(root, "features/mcp-registry/knowledge/qa-airgap.md",
          "---\ntype: qa\ntitle: Airgap?\ndescription: does it airgap\n"
          "timestamp: 2026-07-01\nstatus: answered\n"
          "asks:\n- date: 2026-07-01\n  by: customer\n- date: 2026-07-03\n  by: ssa\n"
          "---\nb\n")
    write(root, "features/mcp-registry/knowledge/qa-open.md",
          "---\ntype: qa\ntitle: Quotas?\ndescription: open one\n"
          "timestamp: 2026-07-02\nstatus: open\n"
          "asks:\n- date: 2026-07-02\n  by: sales\n---\nb\n")
    v = build_all(root, today=TODAY)["views/faq.md"]
    assert "## Unanswered" in v and "Quotas?" in v
    assert "## Most asked" in v and "2x · [Airgap?]" in v
    assert "## All, by feature" in v and "### mcp-registry" in v


def test_stale_view_includes_overdue_qa(tmp_path):
    root = make_repo(tmp_path)
    write(root, "features/mcp-registry/knowledge/qa-old.md",
          "---\ntype: qa\ntitle: Old\ndescription: aging answer\n"
          "timestamp: 2026-01-01\nstatus: answered\nreview_after: 2026-06-01\n"
          "asks:\n- date: 2026-01-01\n  by: pm\n---\nb\n")
    v = build_all(root, today=TODAY)["views/stale-facts.md"]
    assert "/features/mcp-registry/knowledge/qa-old.md" in v


def test_jtbd_view(tmp_path):
    root = make_repo(tmp_path)
    write(root, "features/mcp-registry/knowledge/jtbd-find.md",
          "---\ntype: jtbd\ntitle: Find approved\ndescription: find servers\n"
          "timestamp: 2026-07-01\npersona: ai-engineer\nstatus: candidate\n"
          "evidence:\n- /features/mcp-registry/knowledge/qa-airgap.md\n---\nb\n")
    write(root, "features/mcp-registry/knowledge/jtbd-bare.md",
          "---\ntype: jtbd\ntitle: Bare job\ndescription: no proof\n"
          "timestamp: 2026-07-01\npersona: rhoai-admin\nstatus: validated\n---\nb\n")
    v = build_all(root, today=TODAY)["views/jtbd.md"]
    assert "## candidate" in v and "persona: ai-engineer · 1 evidence" in v
    assert "## validated" in v and "NO EVIDENCE" in v


def test_artifacts_view(tmp_path):
    root = make_repo(tmp_path)
    write(root, "features/mcp-registry/enablement/deck/index.html", "<html></html>")
    write(root, "features/mcp-registry/enablement/deck/artifact.md",
          "---\ntype: artifact\ntitle: Catalog Deck\ndescription: the deck\n"
          "timestamp: 2026-07-01\nfeatures: [mcp-registry]\n---\nb\n")
    write(root, "features/mcp-registry/enablement/bare/index.html", "<html></html>")
    write(root, "publish/manifest.yaml",
          "- source: features/mcp-registry/enablement/deck/\n  dest: mcp-registry/deck/\n"
          "  audience: public\n  title: T\n  description: D\n")
    v = build_all(root, today=TODAY)["views/artifacts.md"]
    assert "[Catalog Deck](/features/mcp-registry/enablement/deck/)" in v
    assert "published → mcp-registry/deck/" in v
    assert "connects: mcp-registry" in v
    assert "_no artifact.md descriptor yet_" in v and "(unpublished)" in v
