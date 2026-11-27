"""list_action_items · owner: Avto30 · reads only.

The action items in one meeting the signed-in user attended, found by the rules from HW1
(hw1/Avto30), with no model (decision 0001). Every item carries its verbatim evidence line and a
confidence; items below 0.7 or without an owner are marked needs_review and are left out unless asked for.
"""
import re
from typing import Annotated

from mcp.server.mcpserver import Resolve
from mcp.types import ToolAnnotations
from pydantic import BaseModel, Field

from ..meetings import Line, NotYourMeeting, meeting_for
from ..tooling import NOT_FOUND, Contract, MeetingId, Tool, ToolFailure

REVIEW_THRESHOLD = 0.7
RULES = [  # (pattern, confidence, owner rule): "speaker" = who said it, "addressee" = the name addressed
    (re.compile(r"\b(I'll|I will)\b\s+(?P<task>[^.?!]+)", re.I), 0.9, "speaker"),
    (re.compile(r"\b(?P<name>[A-Z][a-z]+),\s+can you\s+(?P<task>[^.?!]+)", re.I), 0.85, "addressee"),
    (re.compile(r"\b(we need to|we should)\b\s+(?P<task>[^.?!]+)", re.I), 0.5, None),
]
HEDGES = re.compile(r"\b(maybe|at some point|probably|might)\b", re.I)
DEADLINE = re.compile(r"\b(today|tomorrow|by \w+day|before \w+day|next week)\b", re.I)

Limit = Annotated[int, Field(ge=1, le=20, description="At most this many items, 1 to 20")]


class ListActionItems(Contract):
    """List the action items in one of the user's meetings: task, owner, deadline, evidence line, confidence. Reads only."""
    meeting_id: MeetingId
    include_review: bool = False
    limit: Limit = 10


class ActionItem(BaseModel):
    task: str
    owner: str | None
    deadline: str | None
    timestamp: str
    evidence: str
    confidence: float
    needs_review: bool


class ActionItemList(BaseModel):
    meeting_id: str
    count: int
    hidden_for_review: int
    items: list[ActionItem]


def extract(lines: list[Line]) -> list[ActionItem]:
    items = []
    for line in lines:
        for pattern, conf, owner_rule in RULES:
            hit = pattern.search(line.text)
            if not hit:
                continue
            owner = line.speaker if owner_rule == "speaker" else hit.group("name") if owner_rule == "addressee" else None
            if HEDGES.search(line.text):
                conf = min(conf, 0.4)
            dl = DEADLINE.search(line.text)
            items.append(ActionItem(task=hit.group("task").strip(), owner=owner, deadline=dl.group(0) if dl else None,
                                    timestamp=line.timestamp, evidence=f"[{line.timestamp}] {line.speaker}: {line.text}",
                                    confidence=conf, needs_review=conf < REVIEW_THRESHOLD or owner is None))
            break
    return items


def list_action_items(args: ListActionItems, user: str) -> ActionItemList:
    try:
        meeting = meeting_for(args.meeting_id, user)
    except NotYourMeeting:
        raise ToolFailure(NOT_FOUND.format(id=args.meeting_id)) from None
    every = extract(meeting.lines)
    shown = every if args.include_review else [i for i in every if not i.needs_review]
    return ActionItemList(meeting_id=meeting.id, count=len(shown[:args.limit]),
                          hidden_for_review=len(every) - len(shown), items=shown[:args.limit])


TOOL = Tool("list_action_items", ListActionItems, list_action_items)


def register(mcp) -> None:
    from ..mcp_server import run_tool, signed_in_user

    @mcp.tool(name="list_action_items", description=ListActionItems.__doc__,
              annotations=ToolAnnotations(read_only_hint=True, open_world_hint=False))
    def _list(meeting_id: MeetingId, user: Annotated[str, Resolve(signed_in_user)],
              include_review: bool = False, limit: Limit = 10) -> ActionItemList:
        return run_tool(list_action_items,
                        ListActionItems(meeting_id=meeting_id, include_review=include_review, limit=limit), user=user)
