"""hooks/devrev-safety.py: allow only whole-command read-only DevRev calls; ask for writes and destructive calls;
no opinion on everything else. Run: python3 -m unittest discover -s tests"""
import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HOOK = str(ROOT / "hooks" / "devrev-safety.py")
U = "https://api.devrev.ai"


def run(cmd, tool="Bash", raw=None):
    stdin = raw if raw is not None else json.dumps({"tool_name": tool, "tool_input": {"command": cmd}})
    p = subprocess.run([sys.executable, HOOK], input=stdin, capture_output=True, text=True)
    out = p.stdout.strip()
    decision = json.loads(out)["hookSpecificOutput"] if out else None
    return decision, p.returncode


class Allow(unittest.TestCase):
    CASES = [
        f"curl -s -X POST '{U}/works.list' -H \"Authorization: Bearer $DEVREV_PAT\" -H 'Content-Type: application/json' -d '{{\"limit\":5}}'",
        f"curl -s -X POST {U}/works.list -d '{{}}' | jq '.works[].id'",
        f"set -a; source .env; set +a; curl -s {U}/accounts.get -d '{{}}'",
        f"curl -s {U}/works.list -d '{{}}' && echo done",
        f"curl -s {U}/works.list 2>/dev/null | head -c 200",
        f"ACCT=$(curl -s -X POST {U}/accounts.list -d '{{}}' | jq -r '.accounts[0].id')",
        "curl -s -X POST \"$DEVREV_ENDPOINT/works.list\" \\\n  -H \"Authorization: Bearer $DEVREV_PAT\" \\\n  -d '{\n    \"limit\": 5\n  }'",
    ]

    def test_pure_read_calls_are_allowed(self):
        for c in self.CASES:
            d, rc = run(c)
            self.assertEqual(rc, 0)
            self.assertIsNotNone(d, c)
            self.assertEqual(d["permissionDecision"], "allow", c)


class NoDecision(unittest.TestCase):
    CASES = [
        f"curl -s {U}/works.list; rm -rf ~",
        f"curl -s {U}/works.list > out.json",
        f"curl -s -o out.json {U}/works.list",
        f"curl -sO {U}/works.list",
        f"curl -s {U}/works.list | sh",
        f"curl -s {U}/works.list | tee out.txt",
        f"X=$(curl -s {U}/works.list) && rm -rf /tmp/x",
        f"python3 - <<'EOF'\nimport requests; requests.post('{U}/works.list')\nEOF",
        f"echo `curl -s {U}/works.list`",
        "curl https://example.com/works.delete",
        "curl https://evildevrev.ai/works.list",
        "curl https://api.devrev.ai.evil.com/works.delete",
        "ls -la", "git push origin main", "rm -rf node_modules",
    ]

    def test_everything_else_falls_through_to_the_normal_prompt(self):
        for c in self.CASES:
            d, rc = run(c)
            self.assertEqual(rc, 0)
            self.assertIsNone(d, c)


class Ask(unittest.TestCase):
    WRITES = [
        f"curl -s -X POST {U}/works.create -d '{{\"title\":\"t\"}}'",
        f"curl -s -X POST {U}/works.update -d '{{\"id\":\"don:x\"}}'",
    ]
    DESTRUCTIVE = [
        f"curl -s -X POST {U}/works.delete -d '{{\"id\":\"don:x\"}}'",
        f"curl -s -X POST {U}/internal/objects.bulk-upgrade -d '{{\"type\":\"ticket\"}}'",
        f"curl -s -X POST {U}/link-types.custom.update -d '{{\"id\":\"don:x\",\"deprecated\":true}}'",
        f"source .env && curl -s -X POST {U}/accounts.merge -d '{{}}'",
        f"curl -s {U}/works.list -d '{{}}' ; curl -s -X POST {U}/works.delete -d '{{}}'",
        "curl -s -X POST \"$DEVREV_ENDPOINT/works.delete\" -d '{}'",
    ]

    def test_writes_ask(self):
        for c in self.WRITES:
            d, _ = run(c)
            self.assertEqual(d["permissionDecision"], "ask", c)
            self.assertIn("write", d["permissionDecisionReason"])

    def test_destructive_calls_ask_loudly(self):
        for c in self.DESTRUCTIVE:
            d, _ = run(c)
            self.assertEqual(d["permissionDecision"], "ask", c)
            self.assertIn("DESTRUCTIVE", d["permissionDecisionReason"], c)


class Robustness(unittest.TestCase):
    def test_other_tools_are_ignored(self):
        self.assertEqual(run(f"curl {U}/works.delete", tool="Edit"), (None, 0))

    def test_invalid_input_never_blocks(self):
        self.assertEqual(run("", raw="not json"), (None, 0))
        self.assertEqual(run("", raw="{}"), (None, 0))
        self.assertEqual(run("", raw='{"tool_name":"Bash","tool_input":{}}'), (None, 0))

    def test_output_has_the_documented_shape(self):
        d, _ = run(f"curl -s -X POST {U}/works.list -d '{{}}'")
        self.assertEqual(d["hookEventName"], "PreToolUse")
        self.assertIn(d["permissionDecision"], {"allow", "ask", "deny"})


if __name__ == "__main__":
    unittest.main()
