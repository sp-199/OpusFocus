# HW1 golden questions · Transcript keyword search

Run on 20 October 2026 from `hw1/sp-199/` with `python -m src.search src/data/meeting.txt <query>`. Data: `src/data/meeting.txt` (fictional).

| # | Question (input) | Expected | Actual | Pass? | How I ran it |
|---|---|---|---|---|---|
| 1 | `"room"` | 2 hits: `[00:02:35] Mariam: The demo is next Tuesday at 18:00 in room B204.` and `[00:02:50] Nino: I'll book the room and send the invite today.`, exit 0 | exactly those two lines (lines 11 and 12), `2 match(es); 0 malformed line(s) skipped`, exit 0 | pass | command above; also `test_case_insensitive_and_in_order` |
| 2 | `"kubernetes"` (never said) | no hits, `0 match(es)`, exit 0 | `0 match(es); 0 malformed line(s) skipped`, exit 0 | pass | command above; also `test_no_match_returns_empty_list` |
| 3 | `""` (empty query) | `error: query must not be empty`, exit 1 | `error: query must not be empty`, exit 1 | pass | command above; also `test_empty_query_raises` |

What I learned from running them: searching `"upload"` returned 3 hits, not the 2 I expected, because the agenda line at `00:00:05` also says "upload". The search was right and my expectation was wrong, so I fixed the CLI test instead of the code.
