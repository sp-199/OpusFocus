# Pattern Journal · KurdGela · Weeks 5 to 7

### Week 5 · Tool Contract · 2026-11-27
**Where I used it:** `src/tools/add_highlight.py` (PR #11) and red run PR #12. **What I noticed:** with `extra="ignore"` the extra `user: u-giorgi` argument was dropped silently and the tool still answered "saved" — no one else's notes changed, but the model would have been told something untrue. **Do differently:** write the adversarial case before the code, so I know which lock I am relying on.

### Week 6 · Session State · 2026-11-27
**Where I used it:** the only thing OpusFocus keeps between sessions is highlights in `state/highlights.json`, keyed by a hash of the user id, with no expiry. **What I noticed:** we never decided how long highlights live or how a user deletes them; there is no delete tool on purpose, but there is no delete button either. **Do differently:** decide scope and lifetime (per user, until the meeting is deleted) before storing anything.

### Week 7 · Supervised Autonomy Loop · 2026-11-27
**Where I used it:** OpusFocus has no agent loop yet. The action that would need a human "yes" first is sending notes or action items to other participants, because it reaches people outside the user's own notes. **What I noticed:** my tool only writes to the caller's own data, which is why it can run without a confirmation. **Do differently:** list which future tools write to other people and put those behind confirmation from the start.

*Drafted with Claude from my HW2 work tonight; I checked it against my PRs.*
