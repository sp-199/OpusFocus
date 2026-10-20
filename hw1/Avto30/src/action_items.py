"""Rule-based action-item extractor for OpusFocus meeting transcripts. No model call.

Every item carries its evidence (the exact transcript line) and a confidence.
Items below the review threshold are flagged, never silently accepted.

Usage: python -m src.action_items src/data/meeting.txt
"""
import json
import re
import sys
from pathlib import Path

LINE_RE = re.compile(r"^\[(\d{2}:\d{2}:\d{2})\]\s+([^:]+):\s+(.+)$")
REVIEW_THRESHOLD = 0.7

# (pattern, confidence, owner_rule). owner_rule: "speaker" = whoever said it,
# "addressee" = the name addressed at the start of the sentence, None = unknown.
RULES = [
    (re.compile(r"\b(I'll|I will)\b\s+(?P<task>[^.?!]+)", re.I), 0.9, "speaker"),
    (re.compile(r"\b(?P<name>[A-Z][a-z]+),\s+can you\s+(?P<task>[^.?!]+)", re.I), 0.85, "addressee"),
    (re.compile(r"\b(we need to|we should)\b\s+(?P<task>[^.?!]+)", re.I), 0.5, None),
]
HEDGES = re.compile(r"\b(maybe|at some point|probably|might)\b", re.I)
DEADLINE = re.compile(r"\b(today|tomorrow|by \w+day|before \w+day|next week|by \w+ \d{1,2})\b", re.I)


def extract(lines: list[str]) -> list[dict]:
    """Return action items in transcript order: task, owner, deadline, evidence_line, timestamp, confidence, needs_review."""
    content = [l for l in lines if l.strip() and not l.strip().startswith("#")]
    if not content:
        return []
    items = []
    for raw in content:
        m = LINE_RE.match(raw.strip())
        if not m:
            continue
        ts, speaker, text = m.group(1), m.group(2).strip(), m.group(3).strip()
        for pattern, conf, owner_rule in RULES:
            hit = pattern.search(text)
            if not hit:
                continue
            task = hit.group("task").strip()
            owner = speaker if owner_rule == "speaker" else hit.group("name") if owner_rule == "addressee" else None
            if HEDGES.search(text):
                conf = min(conf, 0.4)
            dl = DEADLINE.search(text)
            items.append({
                "task": task,
                "owner": owner,
                "deadline": dl.group(0) if dl else None,
                "evidence_line": raw.strip(),
                "timestamp": ts,
                "confidence": round(conf, 2),
                "needs_review": conf < REVIEW_THRESHOLD or owner is None,
            })
            break  # one item per line
    return items


def main(argv: list[str]) -> int:
    if not argv:
        print("usage: python -m src.action_items <transcript.txt>", file=sys.stderr)
        return 2
    path = Path(argv[0])
    if not path.exists():
        print(json.dumps({"error": "transcript not found", "field": "path"}))
        return 2
    print(json.dumps(extract(path.read_text(encoding="utf-8").splitlines()), indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
