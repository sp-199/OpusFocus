"""The function-calling door: the model asks for a tool, our code decides whether it runs.

call_tool() never raises. Whatever happens becomes a dict the model can read, and one line in
logs/tools.jsonl (who, as a hash; which tool; ok or the error; latency).
Gates, in order: 1 offered to this caller? 2 arguments pass the contract? 3 run, with identity from us.
"""
from __future__ import annotations

import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path

from pydantic import ValidationError

from .tooling import Tool, ToolFailure, user_key

TOOL_LOG = Path(os.environ.get("OPUSFOCUS_TOOL_LOG", "logs/tools.jsonl"))


def brief(e: ValidationError) -> str:
    """A validation error the model can act on: which field, what was wrong. No stack trace."""
    return "; ".join(f"{'.'.join(map(str, x['loc'])) or 'arguments'}: {x['msg']}" for x in e.errors())


def call_tool(call: dict, allowed: dict[str, Tool], user: str | None) -> dict:
    t0 = time.perf_counter()
    tool = allowed.get(call["name"])
    if tool is None:                                                     # 1 · not offered to this caller
        return _log(call, user, t0, error=f"no tool named {call['name']!r} is available")
    try:
        args = tool.args.model_validate_json(call["arguments"] or "{}")  # 2 · the contract, checked
    except ValidationError as e:
        return _log(call, user, t0, error=f"invalid arguments: {brief(e)}")
    try:
        out = tool.run(args, user=user) if tool.needs_user else tool.run(args)   # 3 · identity from us
    except ToolFailure as e:
        return _log(call, user, t0, error=str(e))
    return _log(call, user, t0, result=out.model_dump(mode="json"))


def _log(call: dict, user: str | None, t0: float, result: dict | None = None, error: str | None = None) -> dict:
    line = {"ts": datetime.now(timezone.utc).isoformat(timespec="seconds"), "tool": call["name"],
            "arguments": call["arguments"], "ok": error is None, "error": error,
            "user": user_key(user) if user else None,
            "latency_ms": round((time.perf_counter() - t0) * 1000, 2)}
    TOOL_LOG.parent.mkdir(parents=True, exist_ok=True)
    with TOOL_LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps(line) + "\n")
    return {**line, "result": result}
