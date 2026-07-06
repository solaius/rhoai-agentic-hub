"""Markdown + YAML frontmatter parsing for the hub. LF-normalized."""
import yaml


class FrontmatterError(ValueError):
    pass


def parse(text):
    """Split markdown text into (meta: dict, body: str)."""
    text = text.lstrip("﻿").replace("\r\n", "\n")
    if not text.startswith("---\n"):
        raise FrontmatterError("missing frontmatter opening '---'")
    rest = text[4:]
    probe = "\n" + rest
    marker = probe.find("\n---")
    if marker == -1:
        raise FrontmatterError("missing frontmatter closing '---'")
    raw = probe[1:marker + 1]
    after = probe[marker + 4:]
    if after.startswith("\n"):
        after = after[1:]
    elif after != "":
        raise FrontmatterError("missing frontmatter closing '---'")
    try:
        meta = yaml.safe_load(raw)
    except yaml.YAMLError as exc:
        raise FrontmatterError(f"invalid YAML: {exc}") from exc
    if meta is None:
        meta = {}
    if not isinstance(meta, dict):
        raise FrontmatterError("frontmatter is not a mapping")
    return meta, after


def load_file(path):
    return parse(path.read_text(encoding="utf-8"))
