"""Every test runs offline: no model, no key, no network. Logs and stored highlights go to a temp folder."""
import os
import tempfile

_tmp = tempfile.mkdtemp(prefix="opusfocus-tests-")
os.environ["OPUSFOCUS_TOOL_LOG"] = os.path.join(_tmp, "tools.jsonl")
os.environ.pop("OPUSFOCUS_USER", None)

import pytest  # noqa: E402


@pytest.fixture(autouse=True)
def fresh_state(tmp_path, monkeypatch):
    """Every test starts with no stored highlights."""
    monkeypatch.setenv("OPUSFOCUS_STATE_DIR", str(tmp_path / "state"))
