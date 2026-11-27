"""The frame itself: meeting access, the registry and call_tool's first gate."""
import pytest

from src import meetings
from src.act import call_tool
from src.tooling import TOOLS, tools_for


def test_participant_can_read_their_meeting():
    m = meetings.meeting_for("mtg-001", "u-nino")
    assert m.title == "Weekly sync" and m.lines[0].timestamp == "00:00:05"


@pytest.mark.parametrize("mid, user", [("mtg-001", "u-ana"), ("mtg-999", "u-nino")])
def test_not_attended_and_missing_look_the_same(mid, user):
    with pytest.raises(meetings.NotYourMeeting):
        meetings.meeting_for(mid, user)


def test_visitor_is_offered_no_meeting_tools():
    assert all(not t.needs_user for t in tools_for(None).values())
    assert set(tools_for("u-nino")) == set(TOOLS)


def test_unknown_tool_is_refused_not_raised():
    out = call_tool({"name": "delete_everything", "arguments": "{}"}, TOOLS, "u-nino")
    assert not out["ok"] and "no tool named" in out["error"]
