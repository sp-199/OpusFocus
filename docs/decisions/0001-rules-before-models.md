# 0001 · Rules and string matching before a model, where they are enough

**Date:** 2026-10-20 · **Status:** accepted · **Deciders:** sp-199, Avto30, KurdGela

**Context.** Three first features: transcript search, action items, title + summary. A model call costs tokens and latency and can invent things.

**Decision.** Search (`hw1/sp-199`) and action items (`hw1/Avto30`) use no model. Only the summary (`hw1/KurdGela`) calls a model, through `llm.py` with usage logging.

**Consequences.** Two of three features cost zero and are fully deterministic, so their golden questions run offline. Rules miss unusual phrasing and can duplicate items (golden g3 fails for that reason). We revisit model-based action items once the golden set has 10 questions (Week 11).
