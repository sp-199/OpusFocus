# HW2 · Evidence · `search_transcript` · sp-199

**Where the cases live:** `evals/tools/sp-199.yaml`, run by `tests/test_tool_golden.py` in the CI job `test`, which the branch rule on `main` requires (status check `test`, no bypassing).

## The five golden cases

Actual results from `python evals/show_tool_cases.py sp-199` on my machine, 27 November 2026 (the same cases ran green in CI on PR #8):

| # | Type | Call | Expected | Actual | Pass? |
|---|---|---|---|---|---|
| s1 | normal | `search_transcript({"meeting_id": "mtg-001", "query": "ROOM"})` as u-nino | ok {'meeting_id': 'mtg-001', 'count': 2} | {"meeting_id": "mtg-001", "count": 2, "truncated": false, "hits": [{"timestamp": "00:02:35", "speaker": "Mariam", "text": "The demo is next Tuesday at 18:00 in room B204."}, {"timestamp": "00:02:50", "speaker": "Nino", "text": "I'll book the room and send the invite today."}]} | pass |
| s2 | normal | `search_transcript({"meeting_id": "mtg-001", "query": "kubernetes", "speaker": "Giorgi"})` as u-giorgi | ok {'count': 0, 'hits': []} | {"meeting_id": "mtg-001", "count": 0, "truncated": false, "hits": []} | pass |
| s3 | normal | `search_transcript({"meeting_id": "mtg-999", "query": "room"})` as u-nino | refused ['no meeting mtg-999', 'ask the user'] | refused: There is no meeting mtg-999 among your meetings. Ask the user which meeting they mean. | pass |
| s4 | bad-input | `search_transcript({"meeting_id": "mtg-001", "query": "r"})` as u-nino | refused ['invalid arguments', 'query'] | refused: invalid arguments: query: String should match pattern '^[\w' -]{2,40}$' | pass |
| s5 | adversarial | `search_transcript({"meeting_id": "../../.env", "query": "KEY"})` as u-nino | refused ['invalid arguments', 'meeting_id'] | refused: invalid arguments: meeting_id: String should match pattern '^mtg-\d{3}$' | pass |

**The adversarial case (s5):** a model or an attacker passes a relative path, `../../.env`, as the meeting id, to make the tool read a file outside `data/meetings/`, such as the repo's secrets file.

## The red run

- Branch `hw2-sp-199-red` · one-line diff in `src/tools/search_transcript.py`: `meeting_id: MeetingId` → `meeting_id: str`
- Pull request #9 (closed, not merged) · run: https://github.com/sp-199/OpusFocus/actions/runs/46052517071/job/140687062972?pr=9
- Failed (same two locally before pushing: `2 failed, 15 passed`):
  - `tests/test_mcp.py::test_both_doors_describe_the_arguments_identically[search_transcript]`
  - `tests/test_tool_golden.py::test_tool_golden_case[sp-199:s5]`
- s5's error changed from `invalid arguments: meeting_id: String should match pattern '^mtg-\d{3}$'` to `There is no meeting ../../.env among your meetings. Ask the user which meeting they mean.`
- Merge box: "All checks have failed · 1 failing check · ci / test (pull_request) Failing after 12s · Required", with the Merge pull request button disabled.

**What the red run taught me.** I expected s5 to start passing the path through once the pattern was gone. It didn't: it was still refused, just by a different line. `meeting_for()` checks `index.json` before it builds `DATA / f"{meeting_id}.txt"`, so the path never reached the file system, but only because of the order of two lines that nobody wrote down as a rule. One refactor that reads the file first and the string goes straight into a path. The test failed because the message lost "invalid arguments", and that is the right reason to fail: the contract should refuse it, not the lookup. The second failure surprised me more: the MCP door still had the pattern (its `register()` uses `MeetingId`), so weakening one class made the two doors describe the tool differently, and `test_mcp.py` caught the drift on its own.

## The green run

Product pull request #8 (merged by KurdGela) · run: https://github.com/sp-199/OpusFocus/actions/runs/46051056175/job/140682169657?pr=8 · last pytest line: `................. [100%]` (17 dots = 17 passed; CI runs pytest quiet twice, `-q` in the workflow plus `addopts = -q`, so it prints no summary line).

## Through the MCP door

Not run through a desktop MCP host before the deadline. The MCP door is exercised in CI by `tests/test_mcp.py` with the SDK's in-memory client: `search_transcript` is listed with the same argument schema as the function-calling door, and without `OPUSFOCUS_USER` the call returns `Not signed in: this server was started without OPUSFOCUS_USER.`
