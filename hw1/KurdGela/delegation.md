# HW1 delegation log · Meeting title and three-line summary

**Date:** 2026-10-20 · **Tool:** Claude (agent) · **Rung on the Autonomy Ladder:** 3 (agent drafts spec, code and tests; I review the diff, run the tests and the live golden questions myself)

**What I delegated.** "Read `Lab-3/MILESTONE-1.md` and the course `llm.py`. Build a title + three-line summary for our note taker. One model call through `llm.py` with usage logging; tests use a fake model."

**What came back wrong.** (1) The agent could not run the live golden questions: its workspace has no OpenRouter key and no network route to it. It left `RUN_ME` placeholders instead of inventing outputs, which is correct, but it means questions 2 and 3 still need a live run with a key. (2) Copying the course `llm.py` as-is would import `openai` at the top, so `pytest` fails on a machine without the package even though no test calls a model. The import was moved inside `client()`; confirmed by running `pytest` in an environment where `openai` is not installed (8 passed). (3) I did not run the live golden questions before the deadline, so the model path (prompt, JSON format, timestamp citations from a real model) is still unverified; only the mocked tests prove the checks around it.

**How I verified.** Read `src/tests/test_summarize.py` first: every test passes a fake `chat_fn`. Ran `pytest hw1/KurdGela` with no key set (8 passed). Ran golden question 1 from the command line and pasted the real output into `golden.md`; questions 2 and 3 are marked not run.

**What I would change next time.** Specify what the UI does with an `ungrounded` line before building; the code flags it but the spec only says "unverified".
