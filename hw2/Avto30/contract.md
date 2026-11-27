# HW2 · Contract · `list_action_items` · Avto30

**Tool:** `list_action_items` · **Owner:** Avto30 · **Team repo:** https://github.com/sp-199/OpusFocus
**Code on `main`:** contract class `ListActionItems` in [`src/tools/list_action_items.py`](https://github.com/sp-199/OpusFocus/blob/main/src/tools/list_action_items.py#L29) line 29 · function line 71 (rules in `extract()` line 53, ported from `hw1/Avto30`) · registry entry `TOOL` line 82 · MCP registration `register()` line 85
**Product pull request:** #14 · commit `410a6e6` by Avto30 (through GitHub's upload page) · merged as `0d08394`

**In one sentence, for the model:** List the action items in one of the user's meetings: task, owner, deadline, evidence line, confidence. Reads only.

| | |
|---|---|
| **Effect** | reads: one meeting transcript in `data/meetings/` |
| **Undo** | nothing to undo, it changes nothing |
| **Idempotent?** | yes: the second identical call returns the same items; rules, no model, nothing stored |
| **Offered to** | signed-in users only: `needs_user=True`, filtered by `tools_for()` in `src/tooling.py` |
| **Identity from** | the session: `call_tool(..., user)` in `src/act.py`; `OPUSFOCUS_USER` via `signed_in_user()` in `src/mcp_server.py` |
| **Touches** | `data/meetings/index.json` and `data/meetings/<meeting_id>.txt`, only through `meeting_for()` in `src/meetings.py` |
| **Must never** | present a hedged or ownerless item as a firm commitment, or read a meeting the user did not attend |

**Inputs**

| Argument | Type | Constraint (as written in code) | Description the model reads |
|---|---|---|---|
| `meeting_id` | str | `^mtg-\d{3}$` | Meeting id, like mtg-001 |
| `include_review` | bool | true or false, default false | *(no description)* |
| `limit` | int | `ge=1, le=20`, default 10 | At most this many items, 1 to 20 |
| *(any other)* | | forbidden: `extra="forbid"` on `Contract` | |

Every item has `evidence` (the verbatim transcript line) and `confidence`; below 0.7 or with no owner it is `needs_review` and hidden unless `include_review` is true. `hidden_for_review` says how many were held back.

**Expected failures**

| When | Message the model reads |
|---|---|
| meeting missing, or not attended by the user | `There is no meeting mtg-001 among your meetings. Ask the user which meeting they mean.` |
| argument breaks the contract | `invalid arguments: limit: Input should be greater than or equal to 1` |
| an argument the contract does not have | `invalid arguments: user: Extra inputs are not permitted` |
| not signed in (MCP door) | `Not signed in: this server was started without OPUSFOCUS_USER.` |

**The decision I had to make.** My HW1 extractor returned every match it found, firm or not, for whatever transcript it was given. As a tool a model can call, two things had to go. It no longer reads any transcript: it reads one meeting, only for a user who attended it, through `meeting_for()`, and a meeting you did not attend gets the same answer as one that does not exist. And it no longer hands everything back: hedged or ownerless items are `needs_review` and hidden unless the model asks with `include_review`, with `hidden_for_review` saying how many, and `limit` is bounded to 1 to 20. A model that reads "Maybe we should add a consent checkbox" as a commitment would tell the team something nobody promised.

*Drafted with Claude from my own runs; I checked every number and message against GitHub.*
