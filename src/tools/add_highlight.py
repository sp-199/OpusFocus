"""add_highlight · owner: KurdGela · adds only.

Saves a highlight (a short note pinned to one transcript line) to the signed-in user's own notes.
It only ever adds: it cannot edit or delete a highlight, and it cannot write to anyone else's notes,
because the user comes from the session and the contract has no user field.
Saving the same highlight twice is safe: the second call returns "already saved".
Highlights are stored in $OPUSFOCUS_STATE_DIR/highlights.json, keyed by a hash of the user id.
"""
import json
import os
from pathlib import Path
from typing import Annotated, Literal

from mcp.server.mcpserver import Resolve
from mcp.types import ToolAnnotations
from pydantic import BaseModel, Field

from ..meetings import NotYourMeeting, meeting_for
from ..tooling import NOT_FOUND, Contract, MeetingId, Timestamp, Tool, ToolFailure, user_key

MAX_PER_MEETING = 50
Note = Annotated[str, Field(pattern=r"^[^<>{}\[\]\\\r\n]{1,200}$",
                            description="The note, one line, 1 to 200 characters, no brackets or backslashes")]


class AddHighlight(Contract):
    """Pin a short note to one line of a meeting the user attended, in the user's own notes. Adds only."""
    meeting_id: MeetingId
    timestamp: Timestamp
    note: Note


class HighlightResult(BaseModel):
    meeting_id: str
    timestamp: str
    line: str
    note: str
    status: Literal["saved", "already saved"]
    total_in_meeting: int


def _state_file() -> Path:
    return Path(os.environ.get("OPUSFOCUS_STATE_DIR", "state")) / "highlights.json"


def _load() -> dict:
    f = _state_file()
    return json.loads(f.read_text(encoding="utf-8")) if f.exists() else {}


def add_highlight(args: AddHighlight, user: str) -> HighlightResult:
    try:
        meeting = meeting_for(args.meeting_id, user)
    except NotYourMeeting:
        raise ToolFailure(NOT_FOUND.format(id=args.meeting_id)) from None
    line = next((l for l in meeting.lines if l.timestamp == args.timestamp), None)
    if line is None:
        raise ToolFailure(f"Meeting {meeting.id} has no line at {args.timestamp}. "
                          "Call search_transcript to find the right timestamp.")
    store = _load()
    mine = store.setdefault(user_key(user), {}).setdefault(meeting.id, [])
    entry = {"timestamp": args.timestamp, "note": args.note.strip()}
    quoted = f"{line.speaker}: {line.text}"
    if entry in mine:                                       # idempotent: asking twice is safe
        return HighlightResult(meeting_id=meeting.id, timestamp=args.timestamp, line=quoted, note=entry["note"],
                               status="already saved", total_in_meeting=len(mine))
    if len(mine) >= MAX_PER_MEETING:
        raise ToolFailure(f"You already have {MAX_PER_MEETING} highlights in {meeting.id}, the limit. "
                          "Tell the user; do not try again.")
    mine.append(entry)
    f = _state_file()
    f.parent.mkdir(parents=True, exist_ok=True)
    tmp = f.with_suffix(".tmp")
    tmp.write_text(json.dumps(store, indent=1, ensure_ascii=False), encoding="utf-8")
    tmp.replace(f)                                          # all or nothing, never half a file
    return HighlightResult(meeting_id=meeting.id, timestamp=args.timestamp, line=quoted, note=entry["note"],
                           status="saved", total_in_meeting=len(mine))


TOOL = Tool("add_highlight", AddHighlight, add_highlight, writes=True)


def register(mcp) -> None:
    from ..mcp_server import run_tool, signed_in_user

    @mcp.tool(name="add_highlight", description=AddHighlight.__doc__,
              annotations=ToolAnnotations(read_only_hint=False, destructive_hint=False, idempotent_hint=True,
                                          open_world_hint=False))
    def _add(meeting_id: MeetingId, timestamp: Timestamp, note: Note,
             user: Annotated[str, Resolve(signed_in_user)]) -> HighlightResult:
        return run_tool(add_highlight, AddHighlight(meeting_id=meeting_id, timestamp=timestamp, note=note), user=user)
