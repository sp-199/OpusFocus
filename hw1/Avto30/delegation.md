# HW1 delegation log · Action-item extractor

**Date:** 2026-10-20 · **Tool:** Claude (agent) · **Rung on the Autonomy Ladder:** 3 (agent drafts spec, code and tests; I review the diff and rerun everything before committing)

**What I delegated.** "Read `Lab-3/MILESTONE-1.md` and the HW1 example. Build an action-item extractor for our note taker: every item with evidence and confidence, low confidence flagged for review. No model call."

**What came back wrong.** (1) The "Name, can you X" rule was anchored to the start of the line, so Nino's "Agreed. Mariam, can you move the action items…" produced no item at all. Caught by running the feature on the sample meeting and seeing Mariam's task missing; the anchor was removed. (2) After that fix, Mariam's reply "I will do that before Thursday" became a second, duplicate item. Caught by golden question 1; left as a documented failure rather than hidden. (3) The first draft had an unused `EmptyTranscript` exception that nothing raised; deleted on diff read. (4) <!-- Avto30: add one thing YOU noticed when you read the diff -->

**How I verified.** Read `src/tests/test_action_items.py` before the code. Ran `pytest hw1/Avto30` (8 passed). Ran the three golden questions and pasted the real output. Checked that no item can exist without an `evidence_line` copied from the transcript.

**What I would change next time.** Put the duplicate case ("Name, can you…" answered by "I will…") in the spec before building. The rule I did not write is the bug I got.
