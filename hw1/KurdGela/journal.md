# Pattern Journal · KurdGela · Weeks 1 to 4

*Copied from `docs/journal/KurdGela.md`. One entry per week: the pattern, one place I saw or used it, one thing I would do differently.*

## Week 1 · 2026-09-29 · Delegation and Verification (the Autonomy Ladder)

**Where I used it:** HW1, my meeting title and three-line summary, was built at rung 3: the agent drafted, I read the tests first and reran everything. **What I noticed:** the agent could not run the live golden questions and left RUN_ME instead of inventing results. At rung 3 the diff is the product; if I do not read it, I have silently moved to rung 4. Context is a budget too: a 30-minute meeting is about 6k tokens in; I log every call so the budget comes from real numbers. **Do differently:** write the rung into the first prompt so the agent stops at a plan.

## Week 2 · 2026-10-06 · Spec Before Code

**Where I used it:** my HW1 `spec.md`: every acceptance criterion is something a test or a command decides, with at least one error case. **What I noticed:** the cases I forgot to write down were exactly the ones the code got wrong. **Do differently:** write the error and edge criteria first.

## Week 3 · 2026-10-13 · Uncertainty-Aware UX

**Where I used it:** in OpusFocus, summary lines citing a timestamp that is not in the transcript are flagged as unverified, not shown as fact. **What I noticed:** a confident-looking output with no evidence is the dangerous one, not the one marked unsure. **Do differently:** decide the low-confidence screen in the spec before writing code.

## Week 4 · 2026-10-20 · Grounded Generation

**Where I used it:** every summary line must cite a real [hh:mm:ss]; the injection transcript tests that spoken text stays data. **What I noticed:** grounding is cheap to check when the source has stable IDs (timestamps). **Do differently:** build the team golden set from real recorded meetings (with consent) instead of only fictional ones.
