"""Transcript keyword search for OpusFocus. No model call: plain string matching.

Usage: python -m src.search src/data/meeting.txt "upload"
"""
import re
import sys
from dataclasses import dataclass, asdict
from pathlib import Path

LINE_RE = re.compile(r"^\[(\d{2}:\d{2}:\d{2})\]\s+([^:]+):\s+(.+)$")


class EmptyQuery(ValueError):
    """Raised when the search query is empty or only whitespace."""


@dataclass
class Hit:
    timestamp: str
    speaker: str
    text: str
    line_no: int


def parse(lines: list[str]) -> tuple[list[Hit], int]:
    """Return parsed transcript lines and the number of malformed (skipped) lines.

    Blank lines and lines starting with '#' are comments, not malformed.
    """
    parsed, skipped = [], 0
    for i, raw in enumerate(lines, start=1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        m = LINE_RE.match(line)
        if not m:
            skipped += 1
            continue
        parsed.append(Hit(m.group(1), m.group(2).strip(), m.group(3).strip(), i))
    return parsed, skipped


def search(lines: list[str], query: str, speaker: str | None = None) -> list[Hit]:
    """Case-insensitive substring search over the spoken text, in transcript order."""
    if not query or not query.strip():
        raise EmptyQuery("query must not be empty")
    q = query.strip().casefold()
    parsed, _ = parse(lines)
    hits = [h for h in parsed if q in h.text.casefold()]
    if speaker:
        hits = [h for h in hits if h.speaker.casefold() == speaker.strip().casefold()]
    return hits


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("usage: python -m src.search <transcript.txt> <query> [--speaker NAME]", file=sys.stderr)
        return 2
    path, query = Path(argv[0]), argv[1]
    speaker = argv[argv.index("--speaker") + 1] if "--speaker" in argv else None
    if not path.exists():
        print(f"error: transcript not found: {path}", file=sys.stderr)
        return 2
    lines = path.read_text(encoding="utf-8").splitlines()
    try:
        hits = search(lines, query, speaker)
    except EmptyQuery as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
    _, skipped = parse(lines)
    for h in hits:
        print(f"[{h.timestamp}] {h.speaker}: {h.text}  (line {h.line_no})")
    print(f"{len(hits)} match(es); {skipped} malformed line(s) skipped")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
