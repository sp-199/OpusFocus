from pathlib import Path

from src import action_items as ai

DATA = Path(__file__).resolve().parent.parent / "data" / "meeting.txt"
LINES = DATA.read_text(encoding="utf-8").splitlines()


def test_accepted_items_in_transcript_order():
    items = [i for i in ai.extract(LINES) if not i["needs_review"]]
    assert [(i["owner"], i["timestamp"]) for i in items] == [
        ("Giorgi", "00:00:52"), ("Mariam", "00:01:31"), ("Mariam", "00:01:40"), ("Nino", "00:02:50")]


def test_every_item_has_verbatim_evidence():
    for i in ai.extract(LINES):
        assert i["evidence_line"] in LINES
        assert i["evidence_line"].startswith(f"[{i['timestamp']}]")


def test_hedged_line_is_flagged_not_accepted():
    hedged = [i for i in ai.extract(LINES) if i["timestamp"] == "00:02:18"]
    assert len(hedged) == 1
    assert hedged[0]["confidence"] <= 0.4 and hedged[0]["needs_review"]


def test_unknown_owner_goes_to_review():
    items = ai.extract(["[00:00:01] Nino: We need to write the privacy note."])
    assert items[0]["owner"] is None and items[0]["needs_review"]


def test_deadline_extracted():
    giorgi = ai.extract(LINES)[0]
    assert giorgi["deadline"] == "by Friday"


def test_empty_and_comment_only_transcripts_return_empty_list():
    assert ai.extract([]) == []
    assert ai.extract(["", "# just a header", "   "]) == []


def test_no_action_items_returns_empty_list():
    assert ai.extract(["[00:00:01] Nino: The weather is nice today."]) == []


def test_cli_missing_file(capsys):
    assert ai.main(["nope.txt"]) == 2
    assert '"field": "path"' in capsys.readouterr().out
