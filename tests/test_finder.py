"""The index and the devrev-find CLI. Run: python3 -m unittest discover -s tests"""
import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIND = str(ROOT / "bin" / "devrev-find")


def find(*args):
    return subprocess.run([sys.executable, FIND, *args], capture_output=True, text=True, cwd="/")


class Index(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.eps = json.loads((ROOT / "index" / "endpoints.json").read_text(encoding="utf-8"))["endpoints"]
        cls.by = {e["name"]: e for e in cls.eps}

    def test_is_fresh(self):
        out = subprocess.run([sys.executable, "-I", str(ROOT / "scripts" / "build_index.py"), "--check"], capture_output=True, text=True)
        self.assertEqual(out.returncode, 0, out.stdout + out.stderr)

    def test_every_endpoint_has_a_risk(self):
        self.assertTrue(all(e["risk"] in ("read", "write", "destructive") for e in self.eps))

    def test_every_doc_pointer_exists(self):
        for e in self.eps:
            for key in ("doc", "beta_doc"):
                if e.get(key):
                    path, _, anchor = e[key].partition("#")
                    f = ROOT / path
                    self.assertTrue(f.exists(), f"{e['name']}: {path} missing")
                    if anchor:
                        self.assertIn(f'<a id="{anchor}"></a>', f.read_text(encoding="utf-8"), f"{e['name']}: anchor {anchor}")

    def test_known_endpoints_carry_scopes_and_required_fields(self):
        self.assertIn("account:write", self.by["accounts.create"]["scopes"])
        self.assertEqual(self.by["accounts.create"]["required"], ["display_name"])
        self.assertIn("title", self.by["works.create"]["required"])  # field tables under oneOf variants are captured

    def test_catalog_rows_are_linked(self):
        self.assertIsNotNone(self.by["accounts.list"]["catalog"])  # catalog writes this as `.list` shorthand


class Cli(unittest.TestCase):
    def test_runs_from_any_directory_and_prints_absolute_paths(self):
        out = find("create a support ticket for a customer", "-n", "3")
        self.assertEqual(out.returncode, 0, out.stderr)
        self.assertIn("works.create", out.stdout)
        self.assertIn(str(ROOT / "skills"), out.stdout)

    def test_endpoint_brief(self):
        out = find("--endpoint", "works.create")
        self.assertEqual(out.returncode, 0, out.stderr)
        for needle in ("RISK:", "MIRROR SECTION", "Required scopes", "required:"):
            self.assertIn(needle, out.stdout)

    def test_unknown_endpoint_suggests_siblings(self):
        out = find("--endpoint", "works.frobnicate")
        self.assertEqual(out.returncode, 1)
        self.assertIn("works.", out.stdout)

    def test_risk_flag(self):
        self.assertEqual(find("--risk", "works.delete").stdout.strip(), "destructive")
        self.assertEqual(find("--risk", "works.list").stdout.strip(), "read")

    def test_json_output_parses(self):
        d = json.loads(find("list all open tickets", "--json").stdout)
        self.assertEqual(d["endpoints"][0][1]["name"], "works.list")

    def test_destructive_goal_is_flagged(self):
        d = json.loads(find("delete a webhook", "--json").stdout)
        top = d["endpoints"][0][1]
        self.assertEqual((top["name"], top["risk"]), ("webhooks.delete", "destructive"))


class Eval(unittest.TestCase):
    def test_finder_accuracy_gate(self):
        out = subprocess.run([sys.executable, "-I", str(ROOT / "scripts" / "eval_finder.py"), "--min-hit3", "0.9"], capture_output=True, text=True)
        self.assertEqual(out.returncode, 0, out.stdout + out.stderr)


class Paths(unittest.TestCase):
    def test_no_dangling_repo_paths(self):
        out = subprocess.run([sys.executable, "-I", str(ROOT / "scripts" / "check_paths.py")], capture_output=True, text=True)
        self.assertEqual(out.returncode, 0, out.stdout + out.stderr)


if __name__ == "__main__":
    unittest.main()
