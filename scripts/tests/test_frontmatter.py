import pytest
from hublib.frontmatter import parse, FrontmatterError


def test_parse_basic():
    meta, body = parse("---\ntype: fact\ndescription: d\n---\nBody here.\n")
    assert meta == {"type": "fact", "description": "d"}
    assert body == "Body here.\n"


def test_parse_crlf_and_bom():
    meta, body = parse("﻿---\r\ntype: fact\r\n---\r\nB\r\n")
    assert meta["type"] == "fact"
    assert body == "B\n"


def test_parse_empty_frontmatter():
    meta, body = parse("---\n\n---\nB\n")
    assert meta == {}


def test_parse_missing_open():
    with pytest.raises(FrontmatterError):
        parse("no frontmatter\n")


def test_parse_missing_close():
    with pytest.raises(FrontmatterError):
        parse("---\ntype: fact\n")


def test_parse_non_mapping():
    with pytest.raises(FrontmatterError):
        parse("---\n- a\n- b\n---\nB\n")


def test_parse_invalid_yaml():
    with pytest.raises(FrontmatterError):
        parse("---\ntype: [unclosed\n---\nB\n")
