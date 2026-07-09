from pathlib import Path

from hublib.schema import lint_repo, validate_manifest


def write(root: Path, rel: str, text: str):
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8", newline="\n")
    return p


ENTRY = "---\ntype: {t}\ndescription: d\ntimestamp: 2026-07-05\n{extra}---\nbody\n"


def make_repo(tmp_path: Path) -> Path:
    write(tmp_path, "AGENTS.md", "# a\n")
    write(tmp_path, "memory/index.md", "# m\n")
    write(tmp_path, "memory/log.md",
          "---\ntype: fact\ndescription: log\ntimestamp: 2026-07-05\n---\n"
          "## 2026-07-05\n- **Creation** — seed.\n")
    return tmp_path


def test_valid_entry_passes(tmp_path):
    root = make_repo(tmp_path)
    write(root, "features/mcp-registry/knowledge/fact-scope.md", ENTRY.format(t="fact", extra=""))
    errors, warnings = lint_repo(root)
    assert errors == []


def test_missing_type_is_error(tmp_path):
    root = make_repo(tmp_path)
    write(root, "features/x/knowledge/fact-a.md",
          "---\ndescription: d\ntimestamp: 2026-07-05\n---\nb\n")
    errors, _ = lint_repo(root)
    assert any("missing required field 'type'" in e for e in errors)


def test_prefix_type_mismatch_is_error(tmp_path):
    root = make_repo(tmp_path)
    write(root, "features/x/knowledge/ref-a.md", ENTRY.format(t="fact", extra=""))
    errors, _ = lint_repo(root)
    assert any("prefix 'ref-' implies type 'reference'" in e for e in errors)


def test_reference_requires_canonical_resource(tmp_path):
    root = make_repo(tmp_path)
    write(root, "features/x/knowledge/ref-a.md",
          ENTRY.format(t="reference",
                       extra="resource: https://docs.google.com/document/d/abc/edit?tab=t.0\n"))
    errors, _ = lint_repo(root)
    assert any("non-canonical resource" in e for e in errors)


def test_unknown_resource_domain_is_warning(tmp_path):
    root = make_repo(tmp_path)
    write(root, "features/x/knowledge/ref-a.md",
          ENTRY.format(t="reference", extra="resource: https://arxiv.org/abs/2501.13956\n"))
    errors, warnings = lint_repo(root)
    assert errors == []
    assert any("unknown resource domain" in w for w in warnings)


def test_stray_dir_in_feature_is_error(tmp_path):
    root = make_repo(tmp_path)
    write(root, "features/x/notes/a.md", ENTRY.format(t="fact", extra=""))
    errors, _ = lint_repo(root)
    assert any("not part of the feature skeleton" in e for e in errors)


def test_agents_budget_enforced(tmp_path):
    root = make_repo(tmp_path)
    write(root, "AGENTS.md", "line\n" * 151)
    errors, _ = lint_repo(root)
    assert any("AGENTS.md exceeds 150 lines" in e for e in errors)


def test_broken_root_link_is_warning(tmp_path):
    root = make_repo(tmp_path)
    write(root, "features/x/knowledge/fact-a.md",
          ENTRY.format(t="fact", extra="") + "see [gone](/features/x/knowledge/missing.md)\n")
    errors, warnings = lint_repo(root)
    assert errors == []
    assert any("broken link" in w for w in warnings)


def test_superseded_without_pointer_is_warning(tmp_path):
    root = make_repo(tmp_path)
    write(root, "memory/facts/fact-old.md",
          "---\ntype: fact\ndescription: d\ntimestamp: 2026-01-01\nstatus: superseded\n---\nb\n")
    _, warnings = lint_repo(root)
    assert any("superseded without superseded_by" in w for w in warnings)


def test_restricted_hint_in_public_dir_is_warning(tmp_path):
    root = make_repo(tmp_path)
    write(root, "features/x/knowledge/fact-a.md",
          ENTRY.format(t="fact", extra="") + "This is internal-only pricing.\n")
    _, warnings = lint_repo(root)
    assert any("restricted-content heuristic" in w for w in warnings)


def test_manifest_duplicate_dest_is_error(tmp_path):
    root = make_repo(tmp_path)
    write(root, "features/x/enablement/deck/index.html", "<html></html>")
    write(root, "publish/manifest.yaml",
          "- source: features/x/enablement/deck/\n  dest: a/\n  audience: public\n"
          "  title: T\n  description: D\n"
          "- source: features/x/enablement/deck/\n  dest: a/\n  audience: public\n"
          "  title: T2\n  description: D2\n")
    errors = validate_manifest(root)
    assert any("duplicate dest" in e for e in errors)


def test_manifest_missing_source_is_error(tmp_path):
    root = make_repo(tmp_path)
    write(root, "publish/manifest.yaml",
          "- source: features/x/enablement/nope/\n  dest: a/\n  audience: public\n"
          "  title: T\n  description: D\n")
    errors = validate_manifest(root)
    assert any("source does not exist" in e for e in errors)


def test_unknown_status_is_error(tmp_path):
    root = make_repo(tmp_path)
    write(root, "memory/facts/fact-typo.md",
          "---\ntype: fact\ndescription: d\ntimestamp: 2026-07-05\nstatus: superceded\n---\nb\n")
    errors, _ = lint_repo(root)
    assert any("status must be current|superseded" in e for e in errors)


QA = ("---\ntype: qa\ndescription: d\ntimestamp: 2026-07-08\nstatus: answered\n"
      "asks:\n- date: 2026-07-08\n  by: customer\n---\n## Question\nq\n## Answer\na\n")


def test_qa_entry_valid(tmp_path):
    root = make_repo(tmp_path)
    write(root, "features/x/knowledge/qa-airgap.md", QA)
    errors, _ = lint_repo(root)
    assert errors == []


def test_qa_missing_asks_is_error(tmp_path):
    root = make_repo(tmp_path)
    write(root, "features/x/knowledge/qa-airgap.md",
          "---\ntype: qa\ndescription: d\ntimestamp: 2026-07-08\nstatus: answered\n---\nb\n")
    errors, _ = lint_repo(root)
    assert any("requires field 'asks'" in e for e in errors)


def test_qa_bad_ask_by_is_error(tmp_path):
    root = make_repo(tmp_path)
    write(root, "features/x/knowledge/qa-airgap.md",
          "---\ntype: qa\ndescription: d\ntimestamp: 2026-07-08\nstatus: answered\n"
          "asks:\n- date: 2026-07-08\n  by: random-person\n---\nb\n")
    errors, _ = lint_repo(root)
    assert any("asks[0].by must be" in e for e in errors)


def test_qa_status_uses_question_enum(tmp_path):
    root = make_repo(tmp_path)
    write(root, "features/x/knowledge/qa-airgap.md",
          "---\ntype: qa\ndescription: d\ntimestamp: 2026-07-08\nstatus: current\n"
          "asks:\n- date: 2026-07-08\n  by: sales\n---\nb\n")
    errors, _ = lint_repo(root)
    assert any("status must be open|answered" in e for e in errors)


def test_jtbd_entry_valid(tmp_path):
    root = make_repo(tmp_path)
    write(root, "features/x/knowledge/jtbd-find-approved-servers.md",
          "---\ntype: jtbd\ndescription: d\ntimestamp: 2026-07-08\n"
          "persona: ai-engineer\nstatus: candidate\n---\n## Job\nWhen …\n")
    errors, _ = lint_repo(root)
    assert errors == []


def test_jtbd_bad_persona_is_error(tmp_path):
    root = make_repo(tmp_path)
    write(root, "features/x/knowledge/jtbd-a.md",
          "---\ntype: jtbd\ndescription: d\ntimestamp: 2026-07-08\n"
          "persona: wizard\nstatus: candidate\n---\nb\n")
    errors, _ = lint_repo(root)
    assert any("persona must be one of" in e for e in errors)


def test_jtbd_status_enum(tmp_path):
    root = make_repo(tmp_path)
    write(root, "features/x/knowledge/jtbd-a.md",
          "---\ntype: jtbd\ndescription: d\ntimestamp: 2026-07-08\n"
          "persona: data-scientist\nstatus: open\n---\nb\n")
    errors, _ = lint_repo(root)
    assert any("status must be candidate|validated|delivered|retired" in e for e in errors)


def test_pillar_and_story_invalid_under_features(tmp_path):
    root = make_repo(tmp_path)
    write(root, "features/x/knowledge/pillar-agents.md", ENTRY.format(t="pillar", extra=""))
    errors, _ = lint_repo(root)
    assert any("type 'pillar' not in vocabulary" in e for e in errors)
