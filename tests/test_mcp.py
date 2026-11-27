"""The MCP door: the same tools as the function-calling door, the same argument schemas, identity from the server."""
import asyncio

import pytest
from mcp import Client

from src.mcp_server import mcp
from src.tooling import TOOLS


def run(coro):
    return asyncio.run(coro)


async def _listed():
    async with Client(mcp) as c:
        return {t.name: t for t in (await c.list_tools()).tools}


def strip(schema):
    return {k: {kk: vv for kk, vv in v.items() if kk != "title"} for k, v in schema.get("properties", {}).items()}


def test_same_tools_through_both_doors():
    assert set(run(_listed())) == set(TOOLS)


@pytest.mark.parametrize("name", sorted(TOOLS))
def test_both_doors_describe_the_arguments_identically(name):
    mcp_schema = run(_listed())[name].input_schema
    fc_schema = TOOLS[name].schema()["function"]["parameters"]
    assert strip(mcp_schema) == strip(fc_schema)
    assert set(mcp_schema.get("required", [])) == set(fc_schema.get("required", []))


@pytest.mark.parametrize("name", sorted(TOOLS))
def test_no_identity_field_in_any_contract(name):
    props = set(TOOLS[name].schema()["function"]["parameters"].get("properties", {}))
    assert not props & {"user", "user_id", "owner", "account", "student", "email"}


@pytest.mark.parametrize("name", sorted(TOOLS))
def test_every_contract_forbids_extra_arguments(name):
    assert TOOLS[name].args.model_config.get("extra") == "forbid"


@pytest.mark.parametrize("name", sorted(TOOLS))
def test_annotations_match_the_registry(name):
    ann = run(_listed())[name].annotations
    assert ann is not None and ann.read_only_hint is (not TOOLS[name].writes)
    if TOOLS[name].writes:
        assert ann.destructive_hint is False


@pytest.mark.parametrize("name", sorted(TOOLS))
def test_tool_needs_a_signed_in_user_through_mcp(name, monkeypatch):
    monkeypatch.delenv("OPUSFOCUS_USER", raising=False)
    async def call():
        async with Client(mcp) as c:
            return await c.call_tool(name, {"meeting_id": "mtg-001", **_minimal_args(name)})
    r = run(call())
    assert r.is_error and "Not signed in" in r.content[0].text


def _minimal_args(name):
    """Whatever else each tool requires, so the call gets past the SDK's own validation."""
    props = TOOLS[name].schema()["function"]["parameters"]
    extra = {}
    for field in props.get("required", []):
        if field == "meeting_id":
            continue
        extra[field] = {"query": "room", "timestamp": "00:00:05", "note": "check this"}.get(field, "x")
    return extra
