"""Run the team golden set against the three HW1 features and commit the result to evals/results/."""
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
FOLDER = {"search": "hw1/sp-199", "action_items": "hw1/Avto30", "summarize": "hw1/KurdGela"}


def run(case: dict, live: bool) -> dict:
    if case.get("live") and not live:
        return {"id": case["id"], "status": "skipped", "reason": "needs --live and OPENROUTER_API_KEY"}
    proc = subprocess.run([sys.executable, "-m", f"src.{case['feature']}", *case["args"]],
                          cwd=ROOT / FOLDER[case["feature"]], capture_output=True, text=True, timeout=120)
    out = proc.stdout + proc.stderr
    missing = [s for s in case.get("must_contain", []) if s not in out]
    reason = f"missing {missing}" if missing else ""
    if "max_firm_items" in case and not missing:
        firm = [i for i in json.loads(proc.stdout) if not i["needs_review"]]
        if len(firm) > case["max_firm_items"]:
            reason = f"{len(firm)} firm items, max {case['max_firm_items']} (duplicate commitment)"
    return {"id": case["id"], "kind": case["kind"], "status": "fail" if reason else "pass",
            "reason": reason, "output": out[:600]}


def main() -> int:
    live = "--live" in sys.argv
    cases = yaml.safe_load((ROOT / "evals/golden.yaml").read_text())
    results = [run(c, live) for c in cases]
    scored = [r for r in results if r["status"] != "skipped"]
    passed = sum(r["status"] == "pass" for r in scored)
    stamp = datetime.now().strftime("%Y-%m-%d-%H%M")
    path = ROOT / f"evals/results/{stamp}-{'live' if live else 'offline'}.json"
    path.write_text(json.dumps({"passed": passed, "scored": len(scored), "results": results}, indent=2))
    for r in results:
        print(f"{r['id']}: {r['status']} {r.get('reason', '')}")
    print(f"{passed}/{len(scored)} passed -> {path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
