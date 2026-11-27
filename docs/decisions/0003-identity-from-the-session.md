# 0003 · The user comes from the session, never from the model

**Date:** 2026-11-27 · **Status:** accepted · **Deciders:** sp-199, Avto30, KurdGela

**Context.** Meeting transcripts are private, and `add_highlight` writes to a user's notes. If a tool took a `user` argument, a confused model or a sentence spoken in a meeting could make it read or write someone else's data.

**Decision.** No contract has a user, owner or account field, and every contract forbids extra arguments. `call_tool(call, allowed, user)` receives the user from our code; the MCP server takes it from `OPUSFOCUS_USER`, set by whoever starts the server. Every meeting read goes through `meeting_for(meeting_id, user)`, which answers "no such meeting" both for a missing meeting and for one the user did not attend.

**Consequences.** `tests/test_mcp.py` checks that no contract has an identity field; each owner's adversarial golden case tries one. A visitor who is not signed in is offered no meeting tools (`tools_for`). Real sign-in replaces the environment variable when the web app exists.
