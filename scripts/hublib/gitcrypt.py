"""Git-crypt blob detection.

git-crypt encrypts each file independently and rewrites it in place with a
fixed 10-byte header: b"\\x00GITCRYPT\\x00" followed by ciphertext. A checkout
without the repo's git-crypt key configured sees this ciphertext verbatim for
every tracked encrypted file.

Locked state is a PER-FILE property, not a directory-wide one: a stray
untracked plaintext file can sit right next to tracked ciphertext (left over
from before the tree was encrypted, or copied in from an unlocked machine).
Checking only the first file found under a tree misreports "unlocked"
whenever that plaintext file happens to sort first, and everything
downstream that then assumes plaintext crashes on the real ciphertext files.
Always check the file you are about to read, not a sibling.
"""
from pathlib import Path

GIT_CRYPT_MAGIC = b"\x00GITCRYPT\x00"


def is_git_crypt_blob(path: Path) -> bool:
    """True if `path` is a git-crypt encrypted blob (starts with the fixed
    magic header). Missing or unreadable files are not blobs (False) --
    callers that care about a missing file check that separately."""
    try:
        with open(path, "rb") as fh:
            head = fh.read(len(GIT_CRYPT_MAGIC))
    except OSError:
        return False
    return head == GIT_CRYPT_MAGIC
