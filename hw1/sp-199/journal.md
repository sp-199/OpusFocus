# Pattern Journal · sp-199 · Weeks 1 to 4

*Copied from `docs/journal/sp-199.md`. One entry per week: the pattern, one place I saw or used it, one thing I would do differently.*

## Week 1 · 2026-09-29 · Delegation and Verification (the Autonomy Ladder)

**Where I used it:** HW1, my transcript keyword search, was built at rung 3: the agent drafted, I read the tests first and reran everything. **What I noticed:** searching "upload" returned 3 hits when I expected 2; the agenda line also says it. At rung 3 the diff is the product; if I do not read it, I have silently moved to rung 4. Context is a budget too: an exact-match search needs no model at all, so this feature costs zero tokens. **Do differently:** write the rung into the first prompt so the agent stops at a plan.

## Week 2 · 2026-10-06 · Spec Before Code

**Where I used it:** my HW1 `spec.md`: every acceptance criterion is something a test or a command decides, with at least one error case. **What I noticed:** the cases I forgot to write down were exactly the ones the code got wrong. **Do differently:** write the error and edge criteria first.

## Week 3 · 2026-10-13 · Uncertainty-Aware UX

**Where I used it:** in OpusFocus, the search has no confidence to show, but a zero-hit result must say "0 matches" clearly instead of an empty screen. **What I noticed:** a confident-looking output with no evidence is the dangerous one, not the one marked unsure. **Do differently:** decide the low-confidence screen in the spec before writing code.

## Week 4 · 2026-10-20 · Grounded Generation

**Where I used it:** every hit carries its timestamp and line number, so the user can jump to the source. **What I noticed:** grounding is cheap to check when the source has stable IDs (timestamps). **Do differently:** build the team golden set from real recorded meetings (with consent) instead of only fictional ones.
