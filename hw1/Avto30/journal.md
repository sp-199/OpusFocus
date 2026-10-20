# Pattern Journal · Avto30 · Weeks 1 to 4

*Copied from `docs/journal/Avto30.md`. One entry per week: the pattern, one place I saw or used it, one thing I would do differently.*

## Week 1 · 2026-09-29 · Delegation and Verification (the Autonomy Ladder)

**Where I used it:** HW1, my action-item extractor, was built at rung 3: the agent drafted, I read the tests first and reran everything. **What I noticed:** the "Name, can you…" rule was anchored to the start of the line and missed Mariam's task until I ran the feature. At rung 3 the diff is the product; if I do not read it, I have silently moved to rung 4. Context is a budget too: rules instead of a model keep the cost at zero and make every result explainable. **Do differently:** write the rung into the first prompt so the agent stops at a plan.

## Week 2 · 2026-10-06 · Spec Before Code

**Where I used it:** my HW1 `spec.md`: every acceptance criterion is something a test or a command decides, with at least one error case. **What I noticed:** the cases I forgot to write down were exactly the ones the code got wrong. **Do differently:** write the error and edge criteria first.

## Week 3 · 2026-10-13 · Uncertainty-Aware UX

**Where I used it:** in OpusFocus, hedged lines ("maybe… at some point") are capped at 0.4 confidence and go to review instead of the to-do list. **What I noticed:** a confident-looking output with no evidence is the dangerous one, not the one marked unsure. **Do differently:** decide the low-confidence screen in the spec before writing code.

## Week 4 · 2026-10-20 · Grounded Generation

**Where I used it:** an item cannot exist without its verbatim evidence line; golden question 1 shows a duplicate the evidence makes visible. **What I noticed:** grounding is cheap to check when the source has stable IDs (timestamps). **Do differently:** build the team golden set from real recorded meetings (with consent) instead of only fictional ones.
