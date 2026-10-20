from pathlib import Path

import pytest

from src import search as s

DATA = Path(__file__).resolve().parent.parent / "data" / "meeting.txt"
LINES = DATA.read_text(encoding="utf-8").splitlines()


def test_case_insensitive_and_in_order():
    hits = s.search(LINES, "ROOM")
    assert [h.timestamp for h in hits] == ["00:02:35", "00:02:50"]


def test_hit_fields_are_filled():
    for h in s.search(LINES, "upload"):
        assert h.timestamp and h.speaker and h.text and h.line_no > 0


def test_no_match_returns_empty_list():
    assert s.search(LINES, "kubernetes") == []


@pytest.mark.parametrize("q", ["", "   "])
def test_empty_query_raises(q):
    with pytest.raises(s.EmptyQuery):
        s.search(LINES, q)


def test_malformed_lines_skipped_and_counted():
    lines = ["[00:00:01] Nino: hello upload", "garbage line", "[0:1] bad: stamp", "# comment", ""]
    parsed, skipped = s.parse(lines)
    assert len(parsed) == 1 and skipped == 2


def test_speaker_filter():
    hits = s.search(LINES, "I'll", speaker="nino")
    assert [h.timestamp for h in hits] == ["00:02:50"]


def test_cli_exit_codes(capsys):
    assert s.main([str(DATA), "upload"]) == 0
    assert "3 match(es)" in capsys.readouterr().out
    assert s.main([str(DATA), "  "]) == 1
    assert s.main(["missing.txt", "x"]) == 2
