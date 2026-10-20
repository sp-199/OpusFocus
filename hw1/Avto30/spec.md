# HW1 spec · Action-item extractor

*OpusFocus (our Granola-style AI note taker) · individual feature · one page. Run from the repo root: `pip install -r hw1/Avto30/src/requirements.txt && pytest hw1/Avto30` · Try it: `cd hw1/Avto30 && python -m src.action_items src/data/meeting.txt`*

## Goal

From a meeting transcript, list who promised to do what, by when, with the exact line that proves it. An item the extractor is unsure about is flagged for the user to confirm, never shown as a firm commitment.

## Users

Meeting participants who leave a meeting and need the to-do list without rereading the transcript.

## Acceptance criteria

1. Every item has `task`, `owner` (or `null`), `deadline` (or `null`), `evidence_line`, `timestamp`, `confidence` (0 to 1) and `needs_review`.
2. `evidence_line` is copied verbatim from the transcript and starts with `[timestamp]` (grounding: no item without evidence).
3. "I'll / I will X" gives owner = speaker, confidence 0.9; "Name, can you X" gives owner = Name, 0.85; "we need to / we should X" gives owner `null`, 0.5.
4. A hedged line ("maybe", "at some point", "probably", "might") is capped at confidence 0.4. Any item below 0.7 or with no owner has `needs_review: true`.
5. An empty or comment-only transcript returns `[]`. A transcript with no commitments returns `[]`. A missing file prints `{"error": "transcript not found", "field": "path"}` and exits 2.
6. No network, no model call.

## Context the agent needs

- `src/data/meeting.txt`: fictional sample transcript, format `[hh:mm:ss] Speaker: text`.
- Week 3 confidence pattern: value, evidence, confidence; low confidence goes to the user, never prefilled.
- This file and `Lab-3/MILESTONE-1.md`.

## Out of scope

Model-based extraction, merging duplicate items, Georgian phrasing, pushing items to a task app.

## Napkin math

Rules cost zero per meeting. An LLM version would read the whole transcript: about 6k tokens in and 300 out per 30-minute meeting, about $0.006 at Gemini 3.8 Flash slide prices.

## Risks

Rules miss commitments phrased differently ("leave it with me") and can double-count one task said twice. Mitigation: evidence on every item so the user can check it; the duplicate case is a documented golden failure.
