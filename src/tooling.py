"""The tool frame: contract base class, shared argument types, the Tool record and the registry.

Every tool lives in its own file in src/tools/ and defines three things:
  * a contract class (subclass of Contract): what the model may send, checked by pydantic
  * a function that takes the validated contract and the signed-in user, and returns a pydantic result
  * TOOL = Tool(...) for the registry, and register(mcp) for the MCP server
The registry finds every module in src/tools/ by itself, so adding a tool never edits a shared file.

Rules for every contract (Week 5, the seven locks):
  * extra="forbid": an argument we did not ask for is an error, never ignored
  * every string has a pattern or a fixed set of values; every number has bounds
  * no user, account or owner field: identity comes from the session, never from the model
"""
from __future__ import annotations

import hashlib
import importlib
import pkgutil
from dataclasses import dataclass
from typing import Annotated, Callable

from pydantic import BaseModel, ConfigDict, Field

from . import tools as tools_pkg

MeetingId = Annotated[str, Field(pattern=r"^mtg-\d{3}$", description="Meeting id, like mtg-001")]
Timestamp = Annotated[str, Field(pattern=r"^\d{2}:[0-5]\d:[0-5]\d$", description="Transcript time, hh:mm:ss")]

NOT_FOUND = "There is no meeting {id} among your meetings. Ask the user which meeting they mean."


class Contract(BaseModel):
    model_config = ConfigDict(extra="forbid")


class ToolFailure(Exception):
    """An expected failure. The message goes back to the model, so it says what to do next."""


def user_key(user: str) -> str:
    """We store and log a hash of the user id, not the id itself."""
    return hashlib.sha256(user.encode()).hexdigest()[:12]


@dataclass(frozen=True)
class Tool:
    name: str
    args: type[Contract]
    run: Callable[..., BaseModel]
    writes: bool = False          # True: changes stored data
    needs_user: bool = True       # True: only offered to a signed-in user; meetings are private

    def schema(self) -> dict:
        """What the model sees through function calling: all of it comes from the contract."""
        return {"type": "function", "function": {
            "name": self.name, "description": self.args.__doc__.strip(),
            "parameters": self.args.model_json_schema()}}


def _discover() -> dict[str, Tool]:
    found = {}
    for info in pkgutil.iter_modules(tools_pkg.__path__):
        module = importlib.import_module(f"{tools_pkg.__name__}.{info.name}")
        tool = getattr(module, "TOOL", None)
        if isinstance(tool, Tool):
            found[tool.name] = tool
    return dict(sorted(found.items()))


TOOLS: dict[str, Tool] = _discover()


def tools_for(user: str | None) -> dict[str, Tool]:
    """Least privilege by construction: a caller who is not signed in is offered no meeting tool."""
    return {n: t for n, t in TOOLS.items() if user or not t.needs_user}


def tool_modules():
    for info in pkgutil.iter_modules(tools_pkg.__path__):
        yield importlib.import_module(f"{tools_pkg.__name__}.{info.name}")
