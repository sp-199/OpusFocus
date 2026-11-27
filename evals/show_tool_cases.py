"""Print your tool golden cases with their ACTUAL results, as a markdown table for evidence.md.

    python evals/show_tool_cases.py <your-github-username>

Runs every case in evals/tools/<username>.yaml through call_tool(), exactly like the CI test.
"""
import json
import os
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
os.environ.setdefault("OPUSFOCUS_TOOL_LOG", os.path.join(tempfile.mkdtemp(), "tools.jsonl"))
os.environ["OPUSFOCUS_STATE_DIR"] = tempfile.mkdtemp()

import yaml  # noqa: E402

from src.act import call_tool  # noqa: E402
from src.tooling import tools_for  # noqa: E402


def main(owner: str) -> int:
    cases = yaml.safe_load((ROOT / "evals" / "tools" / f"{owner}.yaml").read_text(encoding="utf-8"))["cases"]
    print("| # | Type | Call | Expected | Actual | Pass? |\n|---|---|---|---|---|---|")
    for c in cases:
        out = call_tool({"name": c["tool"], "arguments": json.dumps(c["arguments"])},
                        tools_for(c.get("caller")), c.get("caller"))
        actual = json.dumps(out["result"], ensure_ascii=False) if out["ok"] else f"refused: {out['error']}"
        if out["ok"]:
            passed = c["expect"] == "ok" and all(out["result"].get(k) == v for k, v in c.get("result_has", {}).items())
        else:
            passed = c["expect"] == "refused" and all(p.lower() in out["error"].lower() for p in c.get("error_has", []))
        expected = c["expect"] + (f" {c['result_has']}" if c.get("result_has") else "") + (f" {c['error_has']}" if c.get("error_has") else "")
        call = f"`{c['tool']}({json.dumps(c['arguments'], ensure_ascii=False)})` as {c.get('caller') or 'visitor'}"
        print(f"| {c['id']} | {c['type']} | {call} | {expected} | {actual[:300]} | {'pass' if passed else 'FAIL'} |")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
