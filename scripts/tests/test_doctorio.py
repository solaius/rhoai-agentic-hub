from hublib.doctorio import one_line, say


def test_one_line_collapses_tab_lf_and_crlf_into_spaces():
    assert one_line("a\tb\nc\r\nd") == "a b c d"


def test_one_line_collapses_whitespace_runs_and_strips_ends():
    assert one_line("  a    b\t\tc  ") == "a b c"


def test_one_line_leaves_an_already_clean_message_unchanged():
    assert one_line("a clean message") == "a clean message"


def test_say_emits_exactly_kind_tab_message_with_one_trailing_newline(capsys):
    say("ok", "a clean message")
    captured = capsys.readouterr()
    assert captured.out == "ok\ta clean message\n"


def test_say_with_a_tab_in_the_message_still_produces_one_line_one_tab(capsys):
    say("warn", "line one\tline two\nline three")
    captured = capsys.readouterr()
    assert captured.out.count("\t") == 1
    assert captured.out.count("\n") == 1
