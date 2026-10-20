# HW1 spec · Meeting title and three-line summary

*OpusFocus (our Granola-style AI note taker) · individual feature · one page. Run from the repo root: `pip install -r hw1/KurdGela/src/requirements.txt && pytest hw1/KurdGela` (no key needed) · Try it live: `export OPENROUTER_API_KEY=...` then `cd hw1/KurdGela && python -m src.summarize src/data/meeting.txt`*

## Goal

After a meeting, give the user a short title and exactly three summary lines, each pointing at the transcript moment it came from, so they can trust it or check it in one click.

## Users

People who were in (or missed) a meeting and want the gist in ten seconds.

## Acceptance criteria

1. Output is `{title, summary, ungrounded, usage}`: `title` non-empty and at most 60 characters; `summary` exactly 3 strings.
2. Each summary line must cite at least one `[hh:mm:ss]` that exists in the transcript. Lines that cite nothing, or cite a timestamp not in the transcript, are listed by index in `ungrounded` (shown to the user as "unverified", never as fact).
3. Empty input, or input with no timestamped lines, returns `{"error": "transcript has no timestamped lines", "field": "transcript"}`, exits 1, and makes **no** model call.
4. Malformed model JSON returns `{"error": ..., "field": "model_output"}`; the wrong number of lines returns `field: "summary"`. Never a crash.
5. The one model call goes through `src/llm.py`, which appends `{model, tokens_in, tokens_out, cost_usd, latency_ms}` to `logs/usage.jsonl`. Key from `OPENROUTER_API_KEY`. Tests use a fake model and need no key.
6. Text spoken inside the transcript is data: an instruction in the transcript must not change the title (golden question 3).

## Context the agent needs

- `src/data/*.txt`: fictional transcripts, format `[hh:mm:ss] Speaker: text`.
- The course `llm.py` pattern (`Lab-2/examples/campuspulse-week2/src/llm.py`) and this file.

## Out of scope

Transcripts over 60,000 characters (about 15k tokens), chunking, speech-to-text, Georgian-specific prompts, streaming.

## Napkin math

A 30-minute English meeting is about 4,500 words, about 6k tokens in, plus about 150 out. At slide prices ($0.75 / $3.75 per million) that is about $0.005 per summary. Measured numbers are in `golden.md` and the team Design Review.

## Risks

The model invents a fact or a timestamp (mitigation: criterion 2), a spoken instruction hijacks the output (criterion 6 and the system prompt), cost grows with meeting length (criterion 5 logs it; the length cap bounds it).
