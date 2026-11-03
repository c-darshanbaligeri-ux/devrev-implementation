#!/usr/bin/env python3
"""Score `bin/devrev-find` on evals/finder-cases.json (hit@1 and hit@3). Standard library only.

    python3 -I scripts/eval_finder.py [--min-hit3 0.9] [--verbose]

Each case lists acceptable endpoints and/or playbooks; a hit means one of them is in the finder's top 1 / top 3 for
that kind. Exit status 1 when hit@3 is below the threshold (so it can gate commits and tests).
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIND = ROOT / "bin" / "devrev-find"


def run(prompt):
    out = subprocess.run([sys.executable, str(FIND), prompt, "-n", "5", "--json"], capture_output=True, text=True, cwd="/")
    if out.returncode not in (0, 1):
        raise SystemExit(f"devrev-find failed for {prompt!r}: {out.stderr.strip()[:300]}")
    return json.loads(out.stdout) if out.stdout.strip().startswith("{") else {}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--min-hit3", type=float, default=0.9)
    ap.add_argument("--verbose", action="store_true")
    a = ap.parse_args()
    cases = json.loads((ROOT / "evals" / "finder-cases.json").read_text(encoding="utf-8"))["cases"]
    known = {e["name"] for e in json.loads((ROOT / "index" / "endpoints.json").read_text(encoding="utf-8"))["endpoints"]}
    skills = {p["id"] for p in json.loads((ROOT / "index" / "playbooks.json").read_text(encoding="utf-8"))["playbooks"]}
    total = hit1 = hit3 = 0
    misses = []
    for c in cases:
        for e in c.get("expect_endpoints", []):
            if e not in known:
                raise SystemExit(f"case {c['id']}: expected endpoint {e!r} is not in the index")
        for s in c.get("expect_playbooks", []):
            if s not in skills:
                raise SystemExit(f"case {c['id']}: expected playbook {s!r} is not in the index")
        res = run(c["prompt"])
        for kind, key, got_key in (("endpoint", "expect_endpoints", "endpoints"), ("playbook", "expect_playbooks", "playbooks")):
            want = set(c.get(key, []))
            if not want:
                continue
            ranked = [(x[1]["name"] if kind == "endpoint" else x[1]["id"]) for x in res.get(got_key, [])]
            total += 1
            h1 = bool(ranked[:1] and ranked[0] in want)
            h3 = any(r in want for r in ranked[:3])
            hit1 += h1
            hit3 += h3
            if a.verbose or not h3:
                print(f"{'ok  ' if h3 else 'MISS'} {c['id']:20} {kind:8} want {sorted(want)} got {ranked[:3]}")
            if not h3:
                misses.append(c["id"])
    print(f"cases={len(cases)} checks={total}  hit@1={hit1}/{total} ({hit1 / total:.0%})  hit@3={hit3}/{total} ({hit3 / total:.0%})")
    return 0 if hit3 / total >= a.min_hit3 else 1


if __name__ == "__main__":
    sys.exit(main())
