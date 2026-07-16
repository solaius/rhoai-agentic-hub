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


FEATURES_YAML = ("features:\n- id: mcp-registry\n  title: R\n  description: d\n"
                 "- id: mcp-gateway\n  title: G\n  description: d\n")


def test_known_feature_ids_pass(tmp_path):
    root = make_repo(tmp_path)
    write(root, "features/features.yaml", FEATURES_YAML)
    write(root, "features/mcp-registry/knowledge/fact-a.md",
          ENTRY.format(t="fact", extra="features: [mcp-registry, mcp-gateway]\n"))
    errors, _ = lint_repo(root)
    assert errors == []


def test_unknown_feature_id_is_error(tmp_path):
    root = make_repo(tmp_path)
    write(root, "features/features.yaml", FEATURES_YAML)
    write(root, "features/mcp-registry/knowledge/fact-a.md",
          ENTRY.format(t="fact", extra="features: [mcp-registry, made-up]\n"))
    errors, _ = lint_repo(root)
    assert any("unknown feature id 'made-up'" in e for e in errors)


def test_related_symmetric_passes(tmp_path):
    root = make_repo(tmp_path)
    write(root, "features/features.yaml",
          "features:\n- id: mcp-registry\n  title: R\n  description: d\n"
          "  related: [mcp-gateway]\n"
          "- id: mcp-gateway\n  title: G\n  description: d\n"
          "  related: [mcp-registry]\n")
    errors, warnings = lint_repo(root)
    assert errors == []
    assert not any("related" in w for w in warnings)


def test_related_unknown_id_is_error(tmp_path):
    root = make_repo(tmp_path)
    write(root, "features/features.yaml",
          "features:\n- id: mcp-registry\n  title: R\n  description: d\n"
          "  related: [made-up]\n")
    errors, _ = lint_repo(root)
    assert any("unknown related feature id 'made-up'" in e for e in errors)


def test_related_self_reference_is_error(tmp_path):
    root = make_repo(tmp_path)
    write(root, "features/features.yaml",
          "features:\n- id: mcp-registry\n  title: R\n  description: d\n"
          "  related: [mcp-registry]\n")
    errors, _ = lint_repo(root)
    assert any("must not include the feature itself" in e for e in errors)


def test_related_must_be_a_list(tmp_path):
    root = make_repo(tmp_path)
    write(root, "features/features.yaml",
          "features:\n- id: mcp-registry\n  title: R\n  description: d\n"
          "  related: mcp-gateway\n"
          "- id: mcp-gateway\n  title: G\n  description: d\n")
    errors, _ = lint_repo(root)
    assert any("related must be a list of feature ids" in e for e in errors)


def test_related_asymmetry_is_warning(tmp_path):
    root = make_repo(tmp_path)
    write(root, "features/features.yaml",
          "features:\n- id: mcp-registry\n  title: R\n  description: d\n"
          "  related: [mcp-gateway]\n"
          "- id: mcp-gateway\n  title: G\n  description: d\n")
    errors, warnings = lint_repo(root)
    assert errors == []
    assert any("related is asymmetric" in w for w in warnings)


def test_features_must_be_a_list(tmp_path):
    root = make_repo(tmp_path)
    write(root, "features/features.yaml", FEATURES_YAML)
    write(root, "features/mcp-registry/knowledge/fact-a.md",
          ENTRY.format(t="fact", extra="features: mcp-registry\n"))
    errors, _ = lint_repo(root)
    assert any("features must be a list" in e for e in errors)


def test_features_on_memory_file_is_error(tmp_path):
    root = make_repo(tmp_path)
    write(root, "memory/facts/fact-a.md",
          "---\ntype: fact\ndescription: d\ntimestamp: 2026-07-08\n"
          "features: [mcp-registry]\n---\nb\n")
    errors, _ = lint_repo(root)
    assert any("only allowed on knowledge entries" in e for e in errors)


def test_narrative_story_and_pillar_valid(tmp_path):
    root = make_repo(tmp_path)
    write(root, "features/features.yaml", FEATURES_YAML)
    write(root, "narrative/knowledge/pillar-agents.md", ENTRY.format(t="pillar", extra=""))
    write(root, "narrative/knowledge/story-governed-mcp.md",
          ENTRY.format(t="story",
                       extra="features: [mcp-registry, mcp-gateway]\n"
                             "pillar: /narrative/knowledge/pillar-agents.md\n"))
    errors, warnings = lint_repo(root)
    assert errors == []
    assert not any("pillar target" in w for w in warnings)


def test_story_requires_features(tmp_path):
    root = make_repo(tmp_path)
    write(root, "narrative/knowledge/story-a.md", ENTRY.format(t="story", extra=""))
    errors, _ = lint_repo(root)
    assert any("type 'story' requires field 'features'" in e for e in errors)


def test_story_dangling_pillar_is_warning(tmp_path):
    root = make_repo(tmp_path)
    write(root, "features/features.yaml", FEATURES_YAML)
    write(root, "narrative/knowledge/story-a.md",
          ENTRY.format(t="story", extra="features: [mcp-registry]\n"
                                        "pillar: /narrative/knowledge/pillar-gone.md\n"))
    errors, warnings = lint_repo(root)
    assert errors == []
    assert any("pillar target /narrative/knowledge/pillar-gone.md" in w for w in warnings)


def test_stray_dir_under_narrative_is_error(tmp_path):
    root = make_repo(tmp_path)
    write(root, "narrative/stories/a.md", ENTRY.format(t="fact", extra=""))
    errors, _ = lint_repo(root)
    assert any("not part of the narrative skeleton" in e for e in errors)


def test_stray_file_under_narrative_is_error(tmp_path):
    root = make_repo(tmp_path)
    write(root, "narrative/notes.md", "x\n")
    errors, _ = lint_repo(root)
    assert any("files directly under narrative/" in e for e in errors)


def test_artifact_descriptor_valid(tmp_path):
    root = make_repo(tmp_path)
    write(root, "features/features.yaml", FEATURES_YAML)
    write(root, "features/mcp-registry/enablement/deck/index.html", "<html></html>")
    write(root, "features/mcp-registry/enablement/deck/artifact.md",
          ENTRY.format(t="artifact", extra="features: [mcp-gateway]\n"))
    errors, _ = lint_repo(root)
    assert errors == []


def test_artifact_wrong_type_is_error(tmp_path):
    root = make_repo(tmp_path)
    write(root, "features/mcp-registry/enablement/deck/artifact.md",
          ENTRY.format(t="fact", extra=""))
    errors, _ = lint_repo(root)
    assert any("type 'fact' not in vocabulary ['artifact']" in e for e in errors)


def test_artifact_directly_under_enablement_is_error(tmp_path):
    root = make_repo(tmp_path)
    write(root, "features/mcp-registry/enablement/artifact.md",
          ENTRY.format(t="artifact", extra=""))
    errors, _ = lint_repo(root)
    assert any("must live inside an enablement/<slug>/ directory" in e for e in errors)


def test_artifact_assets_are_not_linted(tmp_path):
    root = make_repo(tmp_path)
    write(root, "features/mcp-registry/enablement/deck/README.md", "no frontmatter here\n")
    errors, _ = lint_repo(root)
    assert errors == []


def test_story_invalid_under_features(tmp_path):
    root = make_repo(tmp_path)
    write(root, "features/x/knowledge/story-a.md", ENTRY.format(t="story", extra=""))
    errors, _ = lint_repo(root)
    assert any("type 'story' not in vocabulary" in e for e in errors)


def test_narrative_artifact_descriptor_valid(tmp_path):
    root = make_repo(tmp_path)
    write(root, "features/features.yaml", FEATURES_YAML)
    write(root, "narrative/enablement/deck/index.html", "<html></html>")
    write(root, "narrative/enablement/deck/artifact.md",
          ENTRY.format(t="artifact", extra="features: [mcp-registry]\n"))
    errors, _ = lint_repo(root)
    assert errors == []


RESEARCH_DOC = ("---\ntitle: T\ndescription: d\ntimestamp: 2026-07-09\n"
                "lens: landscape\nreview_after: 2026-10-09\n---\nbody\n")


def test_valid_research_doc_no_warnings(tmp_path):
    root = make_repo(tmp_path)
    write(root, "features/x/research/01-landscape.md", RESEARCH_DOC)
    errors, warnings = lint_repo(root)
    assert errors == []
    assert not any("research doc" in w for w in warnings)


def test_research_doc_missing_description_is_warning(tmp_path):
    root = make_repo(tmp_path)
    write(root, "features/x/research/01-landscape.md",
          "---\ntitle: T\ntimestamp: 2026-07-09\n---\nbody\n")
    errors, warnings = lint_repo(root)
    assert errors == []
    assert any("research doc missing 'description'" in w for w in warnings)


def test_research_doc_without_frontmatter_is_warning_not_error(tmp_path):
    root = make_repo(tmp_path)
    write(root, "features/x/research/02-notes.md", "# just a heading\nbody\n")
    errors, warnings = lint_repo(root)
    assert errors == []
    assert any("research doc lacks frontmatter" in w for w in warnings)


def test_review_notes_and_index_exempt_from_research_lint(tmp_path):
    root = make_repo(tmp_path)
    write(root, "features/x/research/REVIEW-NOTES.md", "# rulings\n")
    write(root, "features/x/research/index.md", "# idx\n")
    errors, warnings = lint_repo(root)
    assert errors == []
    assert not any("research doc" in w for w in warnings)


def test_narrative_research_doc_missing_timestamp_is_warning(tmp_path):
    root = make_repo(tmp_path)
    write(root, "narrative/research/01-x.md",
          "---\ntitle: T\ndescription: d\n---\nbody\n")
    errors, warnings = lint_repo(root)
    assert errors == []
    assert any("research doc missing 'timestamp'" in w for w in warnings)


def test_dollar_figure_hint_is_warning(tmp_path):
    root = make_repo(tmp_path)
    write(root, "features/x/knowledge/fact-a.md",
          ENTRY.format(t="fact", extra="") + "Deal size was $2.4M for year one.\n")
    errors, warnings = lint_repo(root)
    assert errors == []
    assert any("restricted-content heuristic" in w for w in warnings)


def test_signed_agreement_hint_is_warning(tmp_path):
    root = make_repo(tmp_path)
    write(root, "features/x/knowledge/fact-a.md",
          ENTRY.format(t="fact", extra="")
          + "They signed a strategic collaboration agreement last week.\n")
    _, warnings = lint_repo(root)
    assert any("restricted-content heuristic" in w for w in warnings)


def test_story_pillar_without_leading_slash_is_warning(tmp_path):
    root = make_repo(tmp_path)
    write(root, "features/features.yaml", FEATURES_YAML)
    write(root, "narrative/knowledge/pillar-agents.md", ENTRY.format(t="pillar", extra=""))
    write(root, "narrative/knowledge/story-a.md",
          ENTRY.format(t="story", extra="features: [mcp-registry]\n"
                                        "pillar: narrative/knowledge/pillar-agents.md\n"))
    errors, warnings = lint_repo(root)
    assert errors == []
    assert any("leading-slash" in w for w in warnings)


def test_jtbd_jira_list_of_keys_ok(tmp_path):
    root = make_repo(tmp_path)
    write(root, "features/x/knowledge/jtbd-a.md",
          ENTRY.format(t="jtbd", extra="persona: rhoai-admin\nstatus: candidate\n"
                                       "jira: [RHOAIENG-1234, RHAISTRAT-9]\n"))
    errors, _ = lint_repo(root)
    assert errors == []


def test_jtbd_jira_not_a_list_is_error(tmp_path):
    root = make_repo(tmp_path)
    write(root, "features/x/knowledge/jtbd-a.md",
          ENTRY.format(t="jtbd", extra="persona: rhoai-admin\nstatus: candidate\n"
                                       "jira: RHOAIENG-1234\n"))
    errors, _ = lint_repo(root)
    assert any("jira must be a list of issue keys" in e for e in errors)


def test_jtbd_jira_malformed_key_is_error(tmp_path):
    root = make_repo(tmp_path)
    write(root, "features/x/knowledge/jtbd-a.md",
          ENTRY.format(t="jtbd", extra="persona: rhoai-admin\nstatus: candidate\n"
                                       "jira: [not-a-key]\n"))
    errors, _ = lint_repo(root)
    assert any("jira must be a list of issue keys" in e for e in errors)


def test_snapshot_lint_wired_into_lint_repo(tmp_path):
    root = make_repo(tmp_path)
    write(root, "features/x/work/jira-snapshot.yaml", "feature: x\nissues: []\n")
    errors, _ = lint_repo(root)
    assert any("missing generated-file marker" in e for e in errors)


def test_restricted_hint_in_frontmatter_only_is_warning(tmp_path):
    root = make_repo(tmp_path)
    write(root, "features/x/knowledge/fact-a.md",
          "---\ntype: fact\ndescription: internal-only pricing detail\n"
          "timestamp: 2026-07-05\n---\nclean body\n")
    _, warnings = lint_repo(root)
    assert any("fact-a.md" in w and "restricted-content heuristic" in w
               for w in warnings)


def test_restricted_hint_in_frontmatter_skipped_under_restricted(tmp_path):
    root = make_repo(tmp_path)
    write(root, "restricted/features/x/knowledge/fact-a.md",
          "---\ntype: fact\ndescription: internal-only pricing detail\n"
          "timestamp: 2026-07-05\n---\nclean body\n")
    _, warnings = lint_repo(root)
    assert not any("restricted-content heuristic" in w for w in warnings)


def test_restricted_tree_skipped_when_encrypted(tmp_path):
    """git-crypt locked files start with \\x00GITCRYPT -- linter must skip."""
    root = make_repo(tmp_path)
    know = tmp_path / "restricted" / "features" / "x" / "knowledge"
    know.mkdir(parents=True)
    # Simulate a git-crypt encrypted blob: starts with \x00GITCRYPT header
    (know / "fact-a.md").write_bytes(b"\x00GITCRYPT\x00\x00\x02\x00" + b"\xff" * 50)
    errors, warnings = lint_repo(root)
    assert errors == []
    assert not any("restricted" in w for w in warnings)


def test_restricted_tree_handles_mixed_plaintext_leftover_and_encrypted_blob(tmp_path):
    """Regression (#14 follow-up): a locked checkout can have a stray
    UNTRACKED plaintext file sitting right next to TRACKED git-crypt
    ciphertext (e.g. left behind from before the tree was encrypted). Locked
    state is per-file, not "read the first .md found" -- the linter must not
    crash on the ciphertext file, and must still lint the plaintext file
    that sits beside it."""
    root = make_repo(tmp_path)
    know = tmp_path / "restricted" / "features" / "x" / "knowledge"
    know.mkdir(parents=True)
    # Sorts before "fact-b.md" so a first-file-found heuristic would have
    # inspected this encrypted file first and (correctly) called it locked --
    # the bug was the opposite ordering, covered by fact-b existing at all.
    (know / "fact-a.md").write_bytes(b"\x00GITCRYPT\x00\x00\x02\x00" + b"\xff" * 50)
    write(root, "restricted/features/x/knowledge/fact-b.md",
          "---\ndescription: d\ntimestamp: 2026-07-05\n---\nbody\n")
    errors, warnings = lint_repo(root)
    # The encrypted file produced nothing; the plaintext file was actually
    # linted and its real problem (missing 'type') surfaced normally.
    assert any("fact-b.md" in e and "missing required field 'type'" in e
                for e in errors)
    assert not any("fact-a.md" in e for e in errors)
