# Tool contracts · OpusFocus

Every tool is one file in `src/tools/`: a contract class (what the model may send), the function, `TOOL = Tool(...)` for the registry, and `register(mcp)` for the MCP server. `src/tooling.py` finds the files by itself, so adding a tool never edits a shared file. Two doors use the same contract: function calling (`src/act.py`, `call_tool`) and MCP (`src/mcp_server.py`, started by `serve.py`). `tests/test_mcp.py` fails if the doors differ.

**Rules for every contract:** `extra="forbid"`; a pattern or fixed set on every string; bounds on every number; no user, owner or account field. The user comes from the session (`OPUSFOCUS_USER` for MCP, the `user` argument of `call_tool` for function calling), never from the model ([0003](decisions/0003-identity-from-the-session.md)). Meetings are private: every tool reads them through `meeting_for(meeting_id, user)` in `src/meetings.py`, which treats "not your meeting" and "no such meeting" the same.

**Golden cases:** `evals/tools/<github-username>.yaml`, five per owner (3 normal, 1 bad-input, 1 adversarial), run by `tests/test_tool_golden.py` in the CI job `test`, which the branch rule on `main` requires.

## Owners (HW2)

| Tool | Owner | Effect | File | Golden cases |
|---|---|---|---|---|
| `search_transcript` | sp-199 | reads | `src/tools/search_transcript.py` | `evals/tools/sp-199.yaml` |
| `list_action_items` | Avto30 | reads | `src/tools/list_action_items.py` | `evals/tools/Avto30.yaml` |
| `add_highlight` | KurdGela | adds only, to the caller's own notes | `src/tools/add_highlight.py` | `evals/tools/KurdGela.yaml` |
