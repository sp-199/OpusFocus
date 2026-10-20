"""Every model call goes through this file. Every call logs tokens, cost and latency.

Key comes from the environment (OPENROUTER_API_KEY), never from a file in the repo.
Usage lines are appended to logs/usage.jsonl (relative to where you run the command).
"""
import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path

MODEL = os.getenv("OPUSFOCUS_MODEL", "google/gemini-3.8-flash")
PRICE_IN_PER_M = float(os.getenv("PRICE_IN_PER_M", "0.75"))    # course slide price; verify on openrouter.ai
PRICE_OUT_PER_M = float(os.getenv("PRICE_OUT_PER_M", "3.75"))
LOG_PATH = Path(os.getenv("OPUSFOCUS_USAGE_LOG", "logs/usage.jsonl"))

_client = None


def client():
    global _client
    if _client is None:
        from openai import OpenAI  # imported lazily so tests never need the package or a key
        _client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=os.environ["OPENROUTER_API_KEY"])
    return _client


def cost_usd(tokens_in: int, tokens_out: int) -> float:
    return round((tokens_in * PRICE_IN_PER_M + tokens_out * PRICE_OUT_PER_M) / 1_000_000, 6)


def log_usage(usage: dict, path: Path = LOG_PATH) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(usage) + "\n")


def chat(system: str, user: str, max_tokens: int = 400) -> tuple[str, dict]:
    started = time.perf_counter()
    resp = client().chat.completions.create(
        model=MODEL,
        temperature=0.2,
        max_tokens=max_tokens,
        response_format={"type": "json_object"},
        messages=[{"role": "system", "content": system}, {"role": "user", "content": user}],
    )
    u = resp.usage
    usage = {
        "ts": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "feature": "summarize",
        "model": MODEL,
        "tokens_in": u.prompt_tokens,
        "tokens_out": u.completion_tokens,
        "cost_usd": cost_usd(u.prompt_tokens, u.completion_tokens),
        "latency_ms": round((time.perf_counter() - started) * 1000),
    }
    log_usage(usage)
    return resp.choices[0].message.content or "", usage
