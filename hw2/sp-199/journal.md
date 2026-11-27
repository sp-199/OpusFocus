HW2 · Pattern Journal · sp-199

Entries for Weeks 5, 6 and 7, written up on 27 November 2026.

Week 5 · Tool Contract · 2026-11-27

Where I used it: src/tools/search_transcript.py (contract SearchTranscript, meeting_id: MeetingId), product PR #8, red run PR #9.
What I noticed: I expected ../../.env to get through once I removed the ^mtg-\d{3}$ pattern. It didn't, but only because meeting_for() in src/meetings.py checks index.json before it builds the file path. The order of two lines was protecting us, and no rule said so. The bigger surprise was tests/test_mcp.py: weakening one class made the MCP door and the function-calling door describe the tool differently, and the test caught that drift without any case written for it.
Do differently: Put the refusal in the contract, not in the lookup order, and write the adversarial golden case before the tool, so the red run proves something I predicted instead of surprising me.

Week 6 · Session State · 2026-11-27

Where I used it: The user's identity is the session state OpusFocus keeps. Its scope is one server process or one call_tool(..., user) call, and it lasts as long as that process. It's set by OPUSFOCUS_USER through signed_in_user() in src/mcp_server.py, and decision 0003 records it. No tool contract has a user field.
What I noticed: Identity is the only session state we have. The things that sound like session state in our design review, like the consent notice and deleting audio after transcription, are still marked "planned, Week 6" in docs/spec.md and docs/DESIGN-REVIEW.md. They didn't get built.
Do differently: Write down a scope and a lifetime for each new piece of state before building it, the way decision 0003 does for identity, and update the design review when a planned week slips.

Week 7 · Supervised Autonomy Loop · 2026-11-27

Where I used it: I haven't. OpusFocus has no supervised loop yet: nothing in src/ takes a goal and runs tools step by step, and there's no NEEDS_YES list.
What I noticed: We already have a tool that would belong in NEEDS_YES: add_highlight (PR #11) changes a meeting, while search_transcript only reads one. So the split a loop needs is already visible in our contracts.
Do differently: Before we build a loop, mark each tool in src/tooling.py as read-only or needs-a-yes, so the loop can't act without approval on the first day.
