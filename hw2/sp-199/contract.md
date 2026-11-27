# HW2 · Contract · `search_transcript` · sp-199

**Tool:** `search_transcript` · **Owner:** sp-199 · **Team repo:** https://github.com/sp-199/OpusFocus
**Code on `main`:** contract class `SearchTranscript` in [`src/tools/search_transcript.py`](https://github.com/sp-199/OpusFocus/blob/main/src/tools/search_transcript.py#L21) line 21 · function line 41 · registry entry `TOOL` line 52 · MCP registration `register()` line 55 · served by `serve.py` → `src/mcp_server.py`
**Product pull request:** #8 · tool commit `ea9ceab` · merged as `7b3f406` (frame: #6)

**In one sentence, for the model:** Find the lines in one of the user's meetings that contain some words, with timestamps. Reads only.

| | |
|---|---|
| **Effect** | reads: one meeting transcript in `data/meetings/` |
| **Undo** | nothing to undo, it changes nothing |
| **Idempotent?** | yes: the second identical call returns the same hits; nothing is stored |
| **Offered to** | signed-in users only: `needs_user=True` (default in `Tool`), filtered by `tools_for()` in `src/tooling.py` |
| **Identity from** | the session: `call_tool(..., user)` in `src/act.py`; `OPUSFOCUS_USER` via `signed_in_user()` in `src/mcp_server.py` |
| **Touches** | `data/meetings/index.json` (who attended) and `data/meetings/<meeting_id>.txt`, only through `meeting_for()` in `src/meetings.py` |
| **Must never** | return lines from a meeting the user did not attend, or say that such a meeting exists |

**Inputs**

| Argument | Type | Constraint (as written in code) | Description the model reads |
|---|---|---|---|
| `meeting_id` | str | `^mtg-\d{3}$` | Meeting id, like mtg-001 |
| `query` | str | `^[\w' -]{2,40}$` | Words to find, 2 to 40 letters, digits, spaces, hyphens or apostrophes |
| `speaker` | str, optional | `^[A-Za-z][A-Za-z-]{0,29}$` | Only lines said by this first name |
| *(any other)* | | forbidden: `extra="forbid"` on `Contract` | |

Results are capped at 20 hits (`MAX_HITS`); `truncated` says when more matched.

**Expected failures**

| When | Message the model reads |
|---|---|
| meeting missing, or not attended by the user | `There is no meeting mtg-999 among your meetings. Ask the user which meeting they mean.` |
| argument breaks the contract | `invalid arguments: query: String should match pattern '^[\w' -]{2,40}$'` |
| not signed in (MCP door) | `Not signed in: this server was started without OPUSFOCUS_USER.` |

**The decision I had to make.** The easy version of this tool takes `meeting_id` as any string and looks it up; that is what my red run (#9) put back. With a plain string, `../../.env` passed the contract and reached `meeting_for()`, and it was refused only because `index.json` is checked before a file path is built: the order of two lines in `src/meetings.py`, not a rule. So the id has a pattern, `^mtg-\d{3}$` (`MeetingId` in `src/tooling.py`), and the tool has no user field and no "search all meetings" option: it searches one meeting, for the signed-in user, and a meeting they did not attend gets the same answer as one that does not exist.

*Drafted with Claude from my own runs; I checked every number and message against my terminal and GitHub.*
