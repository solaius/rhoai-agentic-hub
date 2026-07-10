import datetime
from pathlib import Path

from hublib.status import build_brief


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
          "features:\n- id: mcp-registry\n  title: R\n  description: d\n")
    write(tmp_path, "memory/log.md",
          "---\ntype: fact\ndescription: log\ntimestamp: 2026-07-05\n---\n"
          "## 2026-07-05\n- **Update** — newest thing.\n"
          "## 2026-07-01\n- **Creation** — older thing.\n")
    return tmp_path


def test_minimal_repo_header_only(tmp_path):
    brief = build_brief(make_repo(tmp_path), today=TODAY)
    assert brief.startswith("# Hub status — 2026-07-05")
    assert "## Stale" not in brief          # empty sections omitted
    assert "## Open questions" not in brief
    assert "## Log rotation due" not in brief
    assert "## Recent log" in brief and "newest thing" in brief


def test_open_questions_counted_by_home(tmp_path):
    root = make_repo(tmp_path)
    write(root, "features/mcp-registry/knowledge/question-a.md",
          "---\ntype: question\ntitle: A?\ndescription: d\ntimestamp: 2026-07-01\n"
          "status: open\n---\nb\n")
    write(root, "narrative/knowledge/question-b.md",
          "---\ntype: question\ntitle: B?\ndescription: d\ntimestamp: 2026-07-01\n"
          "status: open\n---\nb\n")
    brief = build_brief(root, today=TODAY)
    assert "## Open questions (2)" in brief
    assert "mcp-registry: 1" in brief and "narrative: 1" in brief


def test_unanswered_qa_and_bare_jtbd_listed(tmp_path):
    root = make_repo(tmp_path)
    write(root, "features/mcp-registry/knowledge/qa-open.md",
          "---\ntype: qa\ntitle: Quotas?\ndescription: d\ntimestamp: 2026-07-02\n"
          "status: open\nasks:\n- date: 2026-07-02\n  by: sales\n---\nb\n")
    write(root, "features/mcp-registry/knowledge/jtbd-bare.md",
          "---\ntype: jtbd\ntitle: Bare job\ndescription: d\ntimestamp: 2026-07-01\n"
          "persona: rhoai-admin\nstatus: validated\n---\nb\n")
    brief = build_brief(root, today=TODAY)
    assert "## Unanswered qa (1)" in brief and "Quotas?" in brief
    assert "## JTBD lacking evidence (1)" in brief and "Bare job" in brief


def test_stale_section_uses_shared_rows(tmp_path):
    root = make_repo(tmp_path)
    write(root, "memory/profiles/roadmap.md",
          "---\ntype: profile\ndescription: dates\ntimestamp: 2026-05-01\n"
          "review_after: 2026-06-01\nstatus: current\n---\nb\n")
    brief = build_brief(root, today=TODAY)
    assert "## Stale (1)" in brief and "/memory/profiles/roadmap.md" in brief


def test_undescriptored_enablement_dir_listed(tmp_path):
    root = make_repo(tmp_path)
    write(root, "features/mcp-registry/enablement/bare/index.html", "<html></html>")
    brief = build_brief(root, today=TODAY)
    assert "## Enablement dirs missing artifact.md (1)" in brief
    assert "/features/mcp-registry/enablement/bare" in brief


def test_rotation_reminder_only_with_old_years(tmp_path):
    root = make_repo(tmp_path)
    assert "## Log rotation due" not in build_brief(root, today=TODAY)
    write(root, "memory/log.md",
          "---\ntype: fact\ndescription: log\ntimestamp: 2026-07-05\n---\n"
          "## 2026-07-05\n- **Update** — new.\n"
          "## 2025-12-01\n- **Creation** — old.\n")
    brief = build_brief(root, today=TODAY)
    assert "## Log rotation due" in brief and "--rotate-log" in brief
