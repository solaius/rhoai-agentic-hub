from pathlib import Path

from hublib.gitcrypt import is_git_crypt_blob


def test_git_crypt_blob_is_detected(tmp_path):
    p = tmp_path / "fact-a.md"
    p.write_bytes(b"\x00GITCRYPT\x00\x00\x02\x00" + b"\xff" * 50)
    assert is_git_crypt_blob(p) is True


def test_plaintext_file_is_not_a_blob(tmp_path):
    p = tmp_path / "fact-a.md"
    p.write_text("---\ntype: fact\ndescription: d\ntimestamp: 2026-07-05\n---\nbody\n",
                 encoding="utf-8")
    assert is_git_crypt_blob(p) is False


def test_missing_file_is_not_a_blob(tmp_path):
    assert is_git_crypt_blob(tmp_path / "does-not-exist.md") is False


def test_short_file_is_not_a_blob(tmp_path):
    # Shorter than the magic header entirely -- must not raise, must not
    # false-positive.
    p = tmp_path / "tiny.md"
    p.write_bytes(b"\x00GIT")
    assert is_git_crypt_blob(p) is False


def test_accepts_a_string_path(tmp_path):
    p = tmp_path / "fact-a.md"
    p.write_bytes(b"\x00GITCRYPT\x00" + b"\xff" * 20)
    assert is_git_crypt_blob(str(p)) is True
