# HW1 golden questions · Action-item extractor

Run on 20 October 2026 from `hw1/Avto30/` with `python -m src.action_items <file>`. Data files in `src/data/` (fictional).

| # | Question (input) | Expected | Actual | Pass? | How I ran it |
|---|---|---|---|---|---|
| 1 | `src/data/meeting.txt` | 3 firm commitments: Giorgi fixes the WAV upload (by Friday, `00:00:52`); Mariam moves action items above the summary (`00:01:31`); Nino books the room and sends the invite (today, `00:02:50`). The consent-checkbox idea flagged for review. | 4 firm items: the 3 expected **plus a duplicate** Mariam item from `00:01:40` "I will do that before Thursday" (task text "do that before Thursday"). Consent checkbox flagged: confidence 0.4, owner null, `needs_review: true`. | **fail** | command above |
| 2 | `src/data/hedged.txt` (one line: "Maybe we should add a consent checkbox at some point.") | 1 item, owner null, confidence ≤ 0.4, `needs_review: true` | 1 item, owner `null`, confidence 0.4, `needs_review: true`, evidence line verbatim | pass | command above; also `test_hedged_line_is_flagged_not_accepted` |
| 3 | `src/data/empty.txt` (comment only) | `[]`, exit 0 | `[]`, exit 0 | pass | command above; also `test_empty_and_comment_only_transcripts_return_empty_list` |

**Diagnosis of the failure in question 1.** Mariam's "I will do that" is her answer to Nino's request one line earlier. The rules read each line alone, so "that" is not linked back and the same task appears twice. Fix planned: merge an "I will" item into the previous line's "can you" item when the speaker is the addressee and the lines are adjacent. The duplicate is visible to the user because both items carry their evidence line.
