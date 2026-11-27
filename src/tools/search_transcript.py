"""search_transcript · owner: sp-199 · reads only.

Keyword search inside one meeting the signed-in user attended. Plain substring matching, no model
(decision 0001). Returns at most 20 lines, each with its timestamp so the model can cite it.
"""
from typing import Annotated

from mcp.server.mcpserver import Resolve
from mcp.types import ToolAnnotations
from pydantic import BaseModel, Field

from ..meetings import NotYourMeeting, meeting_for
from ..tooling import NOT_FOUND, Contract, MeetingId, Tool, ToolFailure

MAX_HITS = 20
Query = Annotated[str, Field(pattern=r"^[\w' -]{2,40}$",
                             description="Words to find, 2 to 40 letters, digits, spaces, hyphens or apostrophes")]
Speaker = Annotated[str, Field(pattern=r"^[A-Za-z][A-Za-z-]{0,29}$", description="Only lines said by this first name")]


class SearchTranscript(Contract):
    """Find the lines in one of the user's meetings that contain some words, with timestamps. Reads only."""
    meeting_id: MeetingId
    query: Query
    speaker: Speaker | None = None


class Hit(BaseModel):
    timestamp: str
    speaker: str
    text: str


class SearchResult(BaseModel):
    meeting_id: str
    count: int
    truncated: bool
    hits: list[Hit]


def search_transcript(args: SearchTranscript, user: str) -> SearchResult:
    try:
        meeting = meeting_for(args.meeting_id, user)
    except NotYourMeeting:
        raise ToolFailure(NOT_FOUND.format(id=args.meeting_id)) from None
    q = args.query.strip().casefold()
    hits = [Hit(timestamp=l.timestamp, speaker=l.speaker, text=l.text) for l in meeting.lines
            if q in l.text.casefold() and (args.speaker is None or l.speaker.casefold() == args.speaker.casefold())]
    return SearchResult(meeting_id=meeting.id, count=len(hits), truncated=len(hits) > MAX_HITS, hits=hits[:MAX_HITS])


TOOL = Tool("search_transcript", SearchTranscript, search_transcript)


def register(mcp) -> None:
    from ..mcp_server import run_tool, signed_in_user

    @mcp.tool(name="search_transcript", description=SearchTranscript.__doc__,
              annotations=ToolAnnotations(read_only_hint=True, open_world_hint=False))
    def _search(meeting_id: MeetingId, query: Query, user: Annotated[str, Resolve(signed_in_user)],
                speaker: Speaker | None = None) -> SearchResult:
        return run_tool(search_transcript, SearchTranscript(meeting_id=meeting_id, query=query, speaker=speaker),
                        user=user)
