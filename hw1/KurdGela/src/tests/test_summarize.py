"""Every test uses a fake model. No test needs a key or the network."""
import json
from pathlib import Path

from src import llm
from src import summarize as s

DATA = (Path(__file__).resolve().parent.parent / "data" / "meeting.txt").read_text(encoding="utf-8")
USAGE = {"tokens_in": 500, "tokens_out": 80, "cost_usd": 0.000675, "latency_ms": 900}


def fake(payload):
    calls = []

    def chat(system, user):
        calls.append((system, user))
        return (payload if isinstance(payload, str) else json.dumps(payload)), USAGE
    chat.calls = calls
    return chat


GOOD = {"title": "Weekly sync: upload bug, summary layout, demo",
        "summary": ["WAV uploads over ten minutes fail; Giorgi fixes by Friday [00:00:52]",
                    "Action items move above the summary [00:01:31]",
                    "Demo next Tuesday 18:00 in B204 [00:02:35]"]}


def test_good_output_is_grounded():
    out = s.summarize(DATA, fake(GOOD))
    assert out["title"] == GOOD["title"] and len(out["summary"]) == 3
    assert out["ungrounded"] == [] and out["usage"]["tokens_in"] == 500


def test_invented_timestamp_is_flagged():
    bad = dict(GOOD, summary=GOOD["summary"][:2] + ["Budget approved [00:09:99]"])
    assert s.summarize(DATA, fake(bad))["ungrounded"] == [2]


def test_line_without_citation_is_flagged():
    bad = dict(GOOD, summary=["No citation here"] + GOOD["summary"][1:])
    assert s.summarize(DATA, fake(bad))["ungrounded"] == [0]


def test_empty_transcript_returns_error_without_calling_model():
    chat = fake(GOOD)
    assert s.summarize("   ", chat) == {"error": "transcript has no timestamped lines", "field": "transcript"}
    assert chat.calls == []


def test_malformed_model_json():
    assert s.summarize(DATA, fake("not json"))["field"] == "model_output"


def test_wrong_number_of_lines():
    out = s.summarize(DATA, fake(dict(GOOD, summary=GOOD["summary"][:2])))
    assert out["field"] == "summary"


def test_long_title_truncated():
    out = s.summarize(DATA, fake(dict(GOOD, title="x" * 200)))
    assert len(out["title"]) == 60


def test_cost_formula_and_log(tmp_path):
    assert llm.cost_usd(1_000_000, 0) == llm.PRICE_IN_PER_M
    log = tmp_path / "usage.jsonl"
    llm.log_usage({"tokens_in": 1}, log)
    assert json.loads(log.read_text().strip()) == {"tokens_in": 1}
