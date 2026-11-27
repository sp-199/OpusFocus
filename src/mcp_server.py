"""OpusFocus as an MCP server: every tool in src/tools/, usable by any MCP host.

Run over stdio (Claude Desktop, Claude Code, Cursor, MCP Inspector launch it this way):
    OPUSFOCUS_USER=u-nino python serve.py
Each tool module registers itself with register(mcp). Its argument types come from the same
contract class the function-calling door uses; tests/test_mcp.py fails if the two doors differ.
"""
from __future__ import annotations

import os

from mcp.server import MCPServer
from mcp.server.mcpserver.exceptions import ToolError

from .tooling import ToolFailure, tool_modules

mcp = MCPServer("opusfocus", instructions="OpusFocus meeting notes: search transcripts, action items, highlights.")


def signed_in_user() -> str:
    """Who is calling. Set by whoever launches the server, never by the model."""
    user = os.environ.get("OPUSFOCUS_USER")
    if not user:
        raise ToolError("Not signed in: this server was started without OPUSFOCUS_USER.")
    return user


def run_tool(fn, *args, **kwargs):
    """Expected failures reach the model as readable errors, never as stack traces."""
    try:
        return fn(*args, **kwargs)
    except ToolFailure as e:
        raise ToolError(str(e)) from e


for _module in tool_modules():
    if hasattr(_module, "register"):
        _module.register(mcp)


if __name__ == "__main__":
    mcp.run()
