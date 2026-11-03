"""Skill hygiene gates: names, descriptions, size. Run: python3 -m unittest discover -s tests"""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = sorted((ROOT / "skills").glob("*/SKILL.md"))


def frontmatter(p):
    m = re.match(r"\A---\n(.*?)\n---\n", p.read_text(encoding="utf-8"), re.S)
    assert m, f"{p}: no front-matter"
    return m.group(1)


class SkillFrontmatter(unittest.TestCase):
    def test_every_skill_dir_has_a_skill_md(self):
        dirs = {p.name for p in (ROOT / "skills").iterdir() if p.is_dir()}
        have = {p.parent.name for p in SKILLS}
        self.assertEqual(dirs - have, set(), "skill folders without a SKILL.md")

    def test_name_matches_folder_without_its_number(self):
        for p in SKILLS:
            fm = frontmatter(p)
            name = re.search(r"^name: (.+)$", fm, re.M).group(1).strip()
            self.assertEqual(name, re.sub(r"^\d+-", "", p.parent.name), p.parent.name)
            self.assertRegex(name, r"^[a-z0-9-]{1,64}$")

    def test_description_is_one_line_valid_and_short(self):
        for p in SKILLS:
            fm = frontmatter(p)
            self.assertEqual(sorted(re.findall(r"^([A-Za-z_-]+):", fm, re.M)), ["description", "name"], p.parent.name)
            d = re.search(r"^description: (.+)$", fm, re.M).group(1)
            self.assertLessEqual(len(d), 700, f"{p.parent.name}: {len(d)} chars")
            self.assertNotIn(": ", d, f"{p.parent.name}: ': ' breaks a plain YAML value")
            self.assertNotRegex(d, r"[<>]", p.parent.name)
            self.assertIn("Use ", d, f"{p.parent.name}: say when to use it")

    def test_descriptions_say_what_they_are_not_for(self):
        for p in SKILLS:
            if p.parent.name == "devrev-start":
                continue
            d = re.search(r"^description: (.+)$", frontmatter(p), re.M).group(1)
            self.assertRegex(d, r"\bNot for\b|\bNever\b|\bnever\b", f"{p.parent.name}: add a 'Not for ...' clause")


class SkillSize(unittest.TestCase):
    def test_skill_md_files_stay_under_500_lines(self):
        for p in SKILLS:
            n = len(p.read_text(encoding="utf-8").splitlines())
            self.assertLessEqual(n, 500, f"{p.parent.name}: {n} lines; move detail into references/")

    def test_long_references_have_a_current_table_of_contents(self):
        import subprocess
        import sys
        out = subprocess.run([sys.executable, "-I", str(ROOT / "scripts" / "add_toc.py"), "--check"], capture_output=True, text=True)
        self.assertEqual(out.returncode, 0, "run: python3 -I scripts/add_toc.py\n" + out.stdout)

    def test_no_spaces_in_skill_file_names(self):
        bad = [str(p.relative_to(ROOT)) for p in (ROOT / "skills").rglob("*") if p.is_file() and " " in p.name]
        self.assertEqual(bad, [], "shell-unfriendly file names")


if __name__ == "__main__":
    unittest.main()
