# HW1 delegation log · Transcript keyword search

**Date:** 2026-10-20 · **Tool:** Claude (agent) · **Rung on the Autonomy Ladder:** 3 (agent drafts spec, code and tests; I review the diff and rerun everything before committing)

**What I delegated.** "Read `Lab-3/MILESTONE-1.md` and the example in `Lab-3/examples/hw1-example/`. Build a transcript keyword search for our note taker: spec, `src/`, tests, golden questions. No model call."

**What came back wrong.** (1) The first CLI test asserted `2 match(es)` for `"upload"`; running it failed because the agenda line also contains "upload" (3 hits). The test, not the code, was wrong. (2) <!-- sp-199: add one thing YOU noticed when you read the diff, e.g. something you would name differently -->

**How I verified.** Read `src/tests/test_search.py` before `src/search.py`. Ran `pytest hw1/sp-199` (8 passed). Ran the three golden questions from the command line and pasted the real output into `golden.md`. Checked the diff for network imports: none.

**What I would change next time.** Say in the spec exactly which characters count as a word boundary; "room" also matches "bedroom", and the spec does not say whether that is wanted.
