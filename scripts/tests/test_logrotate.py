import datetime
from pathlib import Path

from hublib.logrotate import rotate_log


def write(root: Path, rel: str, text: str):
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8", newline="\n")
    return p


TODAY = datetime.date(2026, 7, 5)

LOG = ("---\ntype: fact\ndescription: log\ntimestamp: 2026-07-05\n---\n"
       "## 2026-07-05\n- **Update** — new thing.\n"
       "## 2025-12-01\n- **Creation** — old thing.\n"
       "## 2025-06-01\n- **Update** — older thing.\n"
       "## 2024-01-15\n- **Creation** — ancient.\n")


def test_rotates_previous_years_grouped_order_preserved(tmp_path):
    write(tmp_path, "memory/log.md", LOG)
    moved = rotate_log(tmp_path, today=TODAY)
    assert moved == {2025: 2, 2024: 1}
    a2025 = (tmp_path / "memory/log-archive/2025.md").read_text(encoding="utf-8")
    assert "## 2025-12-01" in a2025 and "## 2025-06-01" in a2025
    assert a2025.index("2025-12-01") < a2025.index("2025-06-01")
    assert a2025.startswith("# memory/log archive — 2025")
    a2024 = (tmp_path / "memory/log-archive/2024.md").read_text(encoding="utf-8")
    assert "## 2024-01-15" in a2024 and "ancient" in a2024


def test_frontmatter_and_current_year_untouched(tmp_path):
    write(tmp_path, "memory/log.md", LOG)
    rotate_log(tmp_path, today=TODAY)
    log = (tmp_path / "memory/log.md").read_text(encoding="utf-8")
    assert log.startswith("---\ntype: fact\n")
    assert "## 2026-07-05\n- **Update** — new thing." in log
    assert "2025-12-01" not in log and "2024-01-15" not in log


def test_noop_when_only_current_year(tmp_path):
    write(tmp_path, "memory/log.md",
          "---\ntype: fact\ndescription: log\ntimestamp: 2026-07-05\n---\n"
          "## 2026-07-05\n- **Update** — new.\n")
    before = (tmp_path / "memory/log.md").read_text(encoding="utf-8")
    assert rotate_log(tmp_path, today=TODAY) == {}
    assert (tmp_path / "memory/log.md").read_text(encoding="utf-8") == before
    assert not (tmp_path / "memory/log-archive").exists()


def test_second_run_is_noop(tmp_path):
    write(tmp_path, "memory/log.md", LOG)
    rotate_log(tmp_path, today=TODAY)
    assert rotate_log(tmp_path, today=TODAY) == {}


def test_unparseable_heading_never_moves(tmp_path):
    write(tmp_path, "memory/log.md",
          "---\ntype: fact\ndescription: log\ntimestamp: 2026-07-05\n---\n"
          "## Notes\n- stays.\n## 2025-01-01\n- moves.\n")
    moved = rotate_log(tmp_path, today=TODAY)
    assert moved == {2025: 1}
    log = (tmp_path / "memory/log.md").read_text(encoding="utf-8")
    assert "## Notes" in log and "- stays." in log and "- moves." not in log


def test_unparseable_heading_after_moved_section_stays(tmp_path):
    write(tmp_path, "memory/log.md",
          "---\ntype: fact\ndescription: log\ntimestamp: 2026-07-05\n---\n"
          "## 2025-01-01\n- moves.\n## Notes\n- stays.\n")
    moved = rotate_log(tmp_path, today=TODAY)
    assert moved == {2025: 1}
    log = (tmp_path / "memory/log.md").read_text(encoding="utf-8")
    assert "## Notes" in log and "- stays." in log and "- moves." not in log
    a = (tmp_path / "memory/log-archive/2025.md").read_text(encoding="utf-8")
    assert "- moves." in a and "Notes" not in a


def test_missing_log_is_noop(tmp_path):
    assert rotate_log(tmp_path, today=TODAY) == {}


def test_appends_to_existing_archive(tmp_path):
    write(tmp_path, "memory/log-archive/2025.md",
          "# memory/log archive — 2025\n\n## 2025-03-01\n- **Update** — already archived.\n")
    write(tmp_path, "memory/log.md",
          "---\ntype: fact\ndescription: log\ntimestamp: 2026-07-05\n---\n"
          "## 2026-07-05\n- **Update** — new.\n"
          "## 2025-12-01\n- **Creation** — late addition.\n")
    moved = rotate_log(tmp_path, today=TODAY)
    assert moved == {2025: 1}
    a = (tmp_path / "memory/log-archive/2025.md").read_text(encoding="utf-8")
    assert a.count("# memory/log archive — 2025") == 1
    assert "already archived" in a and "late addition" in a
    assert a.index("already archived") < a.index("late addition")
