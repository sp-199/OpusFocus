# HW2 · Contract · `add_highlight` · KurdGela

**Tool:** `add_highlight` · **Owner:** KurdGela · **Team repo:** https://github.com/sp-199/OpusFocus
**Code on `main`:** contract class `AddHighlight` in [`src/tools/add_highlight.py`](https://github.com/sp-199/OpusFocus/blob/main/src/tools/add_highlight.py#L26) line 26 · function line 51 · registry entry `TOOL` line 80 (`writes=True`) · MCP registration `register()` line 83 · extra tests `tests/test_add_highlight.py`
**Product pull request:** #11 (closes #10) · tool commit `e54867d` · merged as `bfaa03d`

**In one sentence, for the model:** Pin a short note to one line of a meeting the user attended, in the user's own notes. Adds only.

| | |
|---|---|
| **Effect** | adds: one highlight `{timestamp, note}` to the caller's own list in `highlights.json` |
| **Undo** | there is no delete tool on purpose; a person removes the entry from `state/highlights.json` (a delete button belongs in the notes screen, not in a tool the model can call) |
| **Idempotent?** | yes: the second identical call returns `"status": "already saved"` with `total_in_meeting` unchanged (`test_second_identical_call_is_already_saved_and_stores_once`) |
| **Offered to** | signed-in users only: `needs_user=True`, filtered by `tools_for()` in `src/tooling.py` |
| **Identity from** | the session: `call_tool(..., user)` in `src/act.py`; `OPUSFOCUS_USER` via `signed_in_user()` in `src/mcp_server.py`. Stored under `user_key(user)`, a hash |
| **Touches** | reads `data/meetings/` through `meeting_for()`; writes only `$OPUSFOCUS_STATE_DIR/highlights.json` |
| **Must never** | write to another user's notes, edit or delete a highlight, or add to a meeting the user did not attend |

**Inputs**

| Argument | Type | Constraint (as written in code) | Description the model reads |
|---|---|---|---|
| `meeting_id` | str | `^mtg-\d{3}$` | Meeting id, like mtg-001 |
| `timestamp` | str | `^\d{2}:[0-5]\d:[0-5]\d$`, and must be a line in that meeting | Transcript time, hh:mm:ss |
| `note` | str | `^[^<>{}\[\]\\\r\n]{1,200}$` | The note, one line, 1 to 200 characters, no brackets or backslashes |
| *(any other)* | | forbidden: `extra="forbid"` on `Contract` | |

At most 50 highlights per user per meeting (`MAX_PER_MEETING`).

**Expected failures**

| When | Message the model reads |
|---|---|
| meeting missing, or not attended by the user | `There is no meeting mtg-001 among your meetings. Ask the user which meeting they mean.` |
| no line at that timestamp | `Meeting mtg-001 has no line at 00:09:59. Call search_transcript to find the right timestamp.` |
| 50 highlights already | `You already have 50 highlights in mtg-001, the limit. Tell the user; do not try again.` |
| an argument the contract does not have | `invalid arguments: user: Extra inputs are not permitted` |
| not signed in (MCP door) | `Not signed in: this server was started without OPUSFOCUS_USER.` |

**The decision I had to make.** The tempting version of this tool takes a `user` argument, so a model could save a highlight "for Giorgi", and treats arguments it doesn't know as harmless. I removed both. The user comes only from the session (`call_tool(..., user)`, `OPUSFOCUS_USER` in `src/mcp_server.py`), and `extra="forbid"` refuses a `user` argument instead of dropping it. My red run (#12) showed why the second part matters: with `extra="ignore"`, case h5 asked to write into u-giorgi's notes, the argument was silently dropped, the note was saved into u-nino's own notes, and the tool answered `"status": "saved"`. Nobody else's data changed, but the model was told its request succeeded when it did not do what it asked. The tool also has no edit or delete: removing a highlight belongs to the user in the notes screen, not to the model.

*Drafted with Claude from my own runs; I checked every number and message against my terminal and GitHub.*
