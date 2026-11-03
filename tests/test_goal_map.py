"""goal-map.md and the entry skill may only name endpoints and files that exist. Run: python3 -m unittest discover -s tests"""
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
START = ROOT / "skills" / "devrev-start"
NAME = re.compile(r"`([a-z][a-z0-9-]*(?:\.[a-z0-9-]+)+|ping)`")


class GoalMap(unittest.TestCase):
    def test_every_endpoint_named_exists_in_the_index(self):
        known = {e["name"] for e in json.loads((ROOT / "index" / "endpoints.json").read_text(encoding="utf-8"))["endpoints"]}
        text = (START / "references" / "goal-map.md").read_text(encoding="utf-8")
        named = {m.group(1) for m in NAME.finditer(text)}
        self.assertGreaterEqual(len(named), 20, "goal-map should name a useful number of endpoints")
        missing = sorted(n for n in named if n not in known)
        self.assertEqual(missing, [], f"goal-map.md names endpoints that are not in the index: {missing}")

    def test_entry_skill_is_small_and_has_valid_frontmatter(self):
        text = (START / "SKILL.md").read_text(encoding="utf-8")
        self.assertLessEqual(len(text.splitlines()), 120)
        m = re.match(r"---\nname: ([a-z0-9-]+)\ndescription: (.+)\n---\n", text)
        self.assertIsNotNone(m, "front-matter must be name + one-line description")
        self.assertEqual(m.group(1), "devrev-start")
        self.assertLessEqual(len(m.group(2)), 1024)

    def test_references_linked_from_the_entry_skill_exist(self):
        text = (START / "SKILL.md").read_text(encoding="utf-8")
        for ref in re.findall(r"`(references/[a-z\-]+\.md)`", text):
            self.assertTrue((START / ref).exists(), ref)


if __name__ == "__main__":
    unittest.main()
