"""add_highlight beyond the golden cases: idempotent, stored under a hash, never in someone else's notes."""
import json

from src.act import call_tool
from src.tooling import TOOLS, user_key
from src.tools import add_highlight as ah

CALL = {"name": "add_highlight", "arguments": json.dumps(
    {"meeting_id": "mtg-001", "timestamp": "00:00:52", "note": "Giorgi owns the WAV fix"})}


def test_second_identical_call_is_already_saved_and_stores_once():
    first, second = call_tool(CALL, TOOLS, "u-nino"), call_tool(CALL, TOOLS, "u-nino")
    assert first["result"]["status"] == "saved" and second["result"]["status"] == "already saved"
    assert second["result"]["total_in_meeting"] == 1


def test_stored_under_the_session_user_hash_only():
    call_tool(CALL, TOOLS, "u-nino")
    stored = ah._state_file().read_text(encoding="utf-8")
    assert user_key("u-nino") in stored and "u-nino" not in stored and user_key("u-giorgi") not in stored


def test_non_attendee_cannot_add_to_a_meeting():
    out = call_tool(CALL, TOOLS, "u-ana")
    assert not out["ok"] and "no meeting mtg-001" in out["error"].lower()
    assert not ah._state_file().exists()
