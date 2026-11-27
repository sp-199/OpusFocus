# HW2 · Evidence · `add_highlight` · KurdGela

**Where the cases live:** `evals/tools/KurdGela.yaml`, run by `tests/test_tool_golden.py` in the CI job `test`, which the branch rule on `main` requires. Extra tests: `tests/test_add_highlight.py` (idempotent second call, stored under a hash, non-attendee refused).

## The five golden cases

Actual results from `python evals/show_tool_cases.py KurdGela` on my machine, 27 November 2026 (the same cases ran green in CI on PR #11):

| # | Type | Call | Expected | Actual | Pass? |
|---|---|---|---|---|---|
| h1 | normal | `add_highlight({"meeting_id": "mtg-001", "timestamp": "00:02:35", "note": "demo time and room"})` as u-nino | ok {'status': 'saved', 'total_in_meeting': 1, 'line': 'Mariam: The demo is next Tuesday at 18:00 in room B204.'} | {"meeting_id": "mtg-001", "timestamp": "00:02:35", "line": "Mariam: The demo is next Tuesday at 18:00 in room B204.", "note": "demo time and room", "status": "saved", "total_in_meeting": 1} | pass |
| h2 | normal | `add_highlight({"meeting_id": "mtg-002", "timestamp": "00:00:44", "note": "Ana shortens the hero text"})` as u-levan | ok {'status': 'saved', 'timestamp': '00:00:44'} | {"meeting_id": "mtg-002", "timestamp": "00:00:44", "line": "Ana: I'll cut it to one sentence by Thursday.", "note": "Ana shortens the hero text", "status": "saved", "total_in_meeting": 1} | pass |
| h3 | normal | `add_highlight({"meeting_id": "mtg-001", "timestamp": "00:09:59", "note": "no such line"})` as u-nino | refused ['no line at 00:09:59', 'search_transcript'] | refused: Meeting mtg-001 has no line at 00:09:59. Call search_transcript to find the right timestamp. | pass |
| h4 | bad-input | `add_highlight({"meeting_id": "mtg-001", "timestamp": "00:00:52", "note": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"})` as u-nino | refused ['invalid arguments', 'note'] | refused: invalid arguments: note: String should match pattern '^[^<>{}\[\]\\\r\n]{1,200}$' | pass |
| h5 | adversarial | `add_highlight({"meeting_id": "mtg-001", "timestamp": "00:00:52", "note": "Giorgi owns the WAV fix", "user": "u-giorgi"})` as u-nino | refused ['invalid arguments', 'user'] | refused: invalid arguments: user: Extra inputs are not permitted | pass |

**The adversarial case (h5):** a confused model, or an instruction spoken in a meeting, tries to write a note into another user's notes by adding `user: u-giorgi` to the arguments, while u-nino is the one signed in.

## The red run

- Branch `hw2-KurdGela-red` · one-line diff in `src/tools/add_highlight.py`, inside `class AddHighlight`: added `model_config = {"extra": "ignore"}`
- Pull request #12 (closed, not merged), commit `4a6ef69` · run: https://github.com/sp-199/OpusFocus/actions/runs/46055568255/job/140697096712?pr=12
- Failed (same two locally before pushing: `2 failed, 28 passed`):
  - `tests/test_mcp.py::test_every_contract_forbids_extra_arguments[add_highlight]`
  - `tests/test_tool_golden.py::test_tool_golden_case[KurdGela:h5]`, with `KurdGela:h5 should be refused but ran: {'meeting_id': 'mtg-001', 'timestamp': '00:00:52', ... 'note': 'Giorgi owns the WAV fix', 'status': 'saved', 'total_in_meeting': 1}`
- Merge box: "All checks have failed · 1 failing check · ci / test (pull_request) Failing after 13s · Required", with the Merge pull request button disabled.

**What the red run taught me.** I thought the danger of dropping `extra="forbid"` would be that the tool writes into Giorgi's notes. It didn't: identity comes from the session, so the note went into u-nino's own notes and nobody else's data changed. The real failure was quieter. The `user: u-giorgi` argument was silently thrown away, the tool answered `"status": "saved"`, and a model reading that would tell the user "saved to Giorgi's notes" when it wasn't. So `extra="forbid"` is not only a security lock; it is what makes the tool tell the model the truth about what it did. Identity from the session protected the data; the strict contract protects the answer.

## The green run

Product pull request #11 (merged by sp-199) · run: https://github.com/sp-199/OpusFocus/actions/runs/46054548241/job/140693745563?pr=11 · last pytest line: a row of dots ending `[100%]`, no `F` (CI runs pytest quiet twice, `-q` in the workflow plus `addopts = -q`, so it prints no summary line; locally the same suite printed `30 passed`).

## Through the MCP door

Not run through a desktop MCP host before the deadline. The MCP door is exercised in CI by `tests/test_mcp.py` with the SDK's in-memory client: `add_highlight` is listed with the same argument schema as the function-calling door, annotated not read-only and not destructive, and without `OPUSFOCUS_USER` the call returns `Not signed in: this server was started without OPUSFOCUS_USER.`
