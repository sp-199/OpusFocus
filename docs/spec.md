# OpusFocus · product spec v1

**Goal.** People in meetings and lectures keep their attention on the conversation; afterwards they get notes they can trust: a searchable transcript, action items with the line that proves them, and a three-line summary that cites timestamps.

**Users.** Students in group-project meetings and lectures; small teams with weekly syncs. English first; Georgian later (2 to 4 times the tokens).

**Acceptance criteria (product level).**
1. Every action item and every summary line points to a transcript timestamp that exists; anything that does not is shown as unverified. (`hw1/Avto30`, `hw1/KurdGela`)
2. Low-confidence or ownerless action items go to a review list, never to the to-do list. (`hw1/Avto30`)
3. A keyword search returns every matching line with timestamp and speaker, or "0 matches". (`hw1/sp-199`)
4. Every model call is logged with tokens, cost and latency in `logs/usage.jsonl`; median cost per 30-minute meeting under $0.02.
5. Recording starts only after every participant is told; no audio is stored after transcription (planned, Week 6).

**Out of scope until Week 8.** Live audio capture, speaker diarisation, calendar integration, mobile app.
