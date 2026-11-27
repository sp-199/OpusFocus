# HW2 · Evidence · `list_action_items` · Avto30

**Where the cases live:** `evals/tools/Avto30.yaml`, run by `tests/test_tool_golden.py` in the CI job `test`, which the branch rule on `main` requires.

## The five golden cases

Results of `python evals/show_tool_cases.py Avto30`, the same calls CI made on PR #14:

| # | Type | Call | Expected | Actual | Pass? |
|---|---|---|---|---|---|
| a1 | normal | `list_action_items({"meeting_id": "mtg-001"})` as u-mariam | ok {'count': 4, 'hidden_for_review': 1} | {"meeting_id": "mtg-001", "count": 4, "hidden_for_review": 1, "items": [{"task": "fix the WAV upload by Friday", "owner": "Giorgi", "deadline": "by Friday", "timestamp": "00:00:52", "evidence": "[00:00:52] Giorgi: Ours. We read the whole file into memory. I'll fix the WAV upload by Friday.", "confid | pass |
| a2 | normal | `list_action_items({"meeting_id": "mtg-002", "include_review": true, "limit": 5})` as u-ana | ok {'count': 1, 'hidden_for_review': 0} | {"meeting_id": "mtg-002", "count": 1, "hidden_for_review": 0, "items": [{"task": "cut it to one sentence by Thursday", "owner": "Ana", "deadline": "by Thursday", "timestamp": "00:00:44", "evidence": "[00:00:44] Ana: I'll cut it to one sentence by Thursday.", "confidence": 0.9, "needs_review": false} | pass |
| a3 | normal | `list_action_items({"meeting_id": "mtg-001"})` as u-ana | refused ['no meeting mtg-001', 'ask the user'] | refused: There is no meeting mtg-001 among your meetings. Ask the user which meeting they mean. | pass |
| a4 | bad-input | `list_action_items({"meeting_id": "mtg-001", "limit": 0})` as u-nino | refused ['invalid arguments', 'limit'] | refused: invalid arguments: limit: Input should be greater than or equal to 1 | pass |
| a5 | adversarial | `list_action_items({"meeting_id": "mtg-001", "user": "u-nino"})` as u-ana | refused ['invalid arguments', 'user'] | refused: invalid arguments: user: Extra inputs are not permitted | pass |

**The adversarial case (a5):** u-ana did not attend mtg-001, so a model acting for her adds `user: u-nino` to the arguments to read Nino's meeting as if it were Nino.

## The red run

Not done before the deadline. My tool PR (#14) was opened at 23:38 and merged at about 23:40, which left no time for the throwaway branch. What I would weaken: add `model_config = {"extra": "ignore"}` to `class ListActionItems`. My teammates' red runs (#9 and #12) on the same frame show the gate blocks such a change: `ci / test` is a required check and the merge button stays disabled. For my tool, the tests that would fail are `test_every_contract_forbids_extra_arguments[list_action_items]` and my adversarial case `Avto30:a5`, because a5's refusal would no longer say "invalid arguments: user" once the extra argument is silently dropped.

## The green run

Product pull request #14 · checks: https://github.com/sp-199/OpusFocus/pull/14/checks · the pytest step shows a row of dots ending `[100%]` with no `F` (CI runs pytest quiet twice, so it prints no summary line).

## Through the MCP door

Not run through a desktop MCP host before the deadline. The MCP door is exercised in CI by `tests/test_mcp.py` with the SDK's in-memory client: `list_action_items` is listed with the same argument schema as the function-calling door, annotated read-only, and without `OPUSFOCUS_USER` the call returns `Not signed in: this server was started without OPUSFOCUS_USER.`
