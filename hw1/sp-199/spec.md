# HW1 spec · Transcript keyword search

*OpusFocus (our Granola-style AI note taker) · individual feature · one page. Run from the repo root: `pip install -r hw1/sp-199/src/requirements.txt && pytest hw1/sp-199` · Try it: `cd hw1/sp-199 && python -m src.search src/data/meeting.txt "room"`*

## Goal

After a meeting, a user types a word and gets every transcript line where it was said, with the timestamp and speaker, so they can jump to that moment. Nothing else.

## Users

People who were in a meeting or lecture and remember *that* something was said ("the room", "Friday") but not *when*.

## Acceptance criteria

1. `search(lines, "ROOM")` on `src/data/meeting.txt` returns exactly the lines at `00:02:35` and `00:02:50`, in transcript order (case-insensitive substring match).
2. Each hit has `timestamp` (hh:mm:ss), `speaker`, `text` and `line_no`; none is empty.
3. A query with no match returns an empty list; the CLI prints `0 match(es)` and exits 0.
4. An empty or whitespace-only query raises `EmptyQuery`; the CLI prints `error: query must not be empty` and exits 1. A missing transcript file exits 2.
5. Lines that do not match `[hh:mm:ss] Speaker: text` are skipped and counted, never crash the search; `#` comments and blank lines are not counted as malformed.
6. Optional `speaker=` filter is case-insensitive. No network, no model call.

## Context the agent needs

- `src/data/meeting.txt`: fictional sample transcript, format `[hh:mm:ss] Speaker: text`.
- This file. The HW1 brief `Lab-3/MILESTONE-1.md`.

## Out of scope

Fuzzy or semantic search (embeddings), Georgian stemming, audio playback, a web endpoint, search across several meetings.

## Napkin math

No model call: cost per search is zero. A semantic version would embed every chunk once (about 6k tokens per 30-minute meeting) plus one query embedding per search.

## Risks

Exact substring search misses synonyms and inflections ("booking" vs "book"), especially in Georgian. Mitigation for now: documented as out of scope; semantic search is a later capstone slice.
