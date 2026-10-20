# 0002 · OpenRouter gateway, `google/gemini-3.8-flash` as default model

**Date:** 2026-10-20 · **Status:** accepted · **Deciders:** sp-199, Avto30, KurdGela

**Context.** The course uses OpenRouter; a 30-minute meeting is about 6k tokens in. We need cheap, fast, JSON-capable summaries.

**Decision.** All model calls go through OpenRouter via one `llm.py` per feature, model set by `OPUSFOCUS_MODEL` (default `google/gemini-3.8-flash`), key from `OPENROUTER_API_KEY`, every call appended to `logs/usage.jsonl`.

**Consequences.** Switching model is one environment variable. Prices in `llm.py` come from the course slides and must be checked on openrouter.ai. One gateway is a single point of failure; a fallback model is planned for Week 10.
