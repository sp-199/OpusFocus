"""Meeting data: transcripts in data/meetings/, who attended each one in data/meetings/index.json.

Every tool reads meetings through this file, and only through `meeting_for(meeting_id, user)`,
which returns a meeting only if `user` attended it. A meeting that does not exist and a meeting
the user did not attend give the same answer, so a tool never reveals that someone else's meeting exists.
"""
from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass
from pathlib import Path

DATA = Path(os.environ.get("OPUSFOCUS_MEETINGS", Path(__file__).resolve().parents[1] / "data" / "meetings"))
LINE_RE = re.compile(r"^\[(\d{2}:\d{2}:\d{2})\]\s+([^:]+):\s+(.+)$")


@dataclass(frozen=True)
class Line:
    timestamp: str
    speaker: str
    text: str


@dataclass(frozen=True)
class Meeting:
    id: str
    title: str
    date: str
    lines: list[Line]


class NotYourMeeting(LookupError):
    """Raised for a meeting that does not exist or that the user did not attend."""


def _index() -> dict:
    return json.loads((DATA / "index.json").read_text(encoding="utf-8"))


def parse(text: str) -> list[Line]:
    return [Line(*m.groups()) for raw in text.splitlines() if (m := LINE_RE.match(raw.strip()))]


def meeting_for(meeting_id: str, user: str) -> Meeting:
    entry = _index().get(meeting_id)
    if entry is None or user not in entry["participants"]:
        raise NotYourMeeting(meeting_id)
    text = (DATA / f"{meeting_id}.txt").read_text(encoding="utf-8")
    return Meeting(meeting_id, entry["title"], entry["date"], parse(text))
