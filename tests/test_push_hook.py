"""Scenario tests for .claude/hooks/push-learnings.sh against a throwaway bare 'origin' (never the real remote).
Run: python3 -m unittest discover -s tests"""
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

HOOK = str(Path(__file__).resolve().parents[1] / ".claude" / "hooks" / "push-learnings.sh")
ENV = {**os.environ, "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t", "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t"}


def git(cwd, *args, check=True):
    return subprocess.run(["git", *args], cwd=cwd, env=ENV, capture_output=True, text=True, check=check)


class PushHook(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.origin = self.tmp / "origin.git"
        self.work = self.tmp / "work"
        subprocess.run(["git", "init", "-q", "--bare", "-b", "main", str(self.origin)], check=True)
        subprocess.run(["git", "clone", "-q", str(self.origin), str(self.work)], check=True, capture_output=True)
        git(self.work, "checkout", "-q", "-B", "main")
        (self.work / "README.md").write_text("init\n")
        (self.work / ".gitignore").write_text(".claude/.auto-setup/\n")  # the hook's marker files, as in the real repo
        git(self.work, "add", "-A")
        git(self.work, "commit", "-q", "-m", "init")
        git(self.work, "push", "-q", "-u", "origin", "main")

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def commit(self, subject, rel, text="x\n"):
        f = self.work / rel
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(text)
        git(self.work, "add", "-A")
        git(self.work, "commit", "-q", "-m", subject)

    def fire(self):
        return subprocess.run(["bash", HOOK], input="{}", env={**ENV, "CLAUDE_PROJECT_DIR": str(self.work)}, capture_output=True, text=True, cwd=str(self.work))

    def remote(self):
        return subprocess.run(["git", "--git-dir", str(self.origin), "rev-parse", "main"], capture_output=True, text=True).stdout.strip()

    def local(self):
        return git(self.work, "rev-parse", "HEAD").stdout.strip()

    def test_a_clean_learn_commit_is_pushed(self):
        self.commit("learn: a fact", "skills/x/SKILL.md")
        out = self.fire()
        self.assertEqual(out.returncode, 0)
        self.assertEqual(self.remote(), self.local(), out.stderr)

    def test_index_and_skill_scoped_claude_paths_are_allowed(self):
        self.commit("learn: index", "index/endpoints.json", "{}\n")
        self.fire()
        self.assertEqual(self.remote(), self.local())
        self.commit("learn: claude skill", ".claude/skills/y/SKILL.md")
        self.fire()
        self.assertEqual(self.remote(), self.local())

    def test_a_non_learn_commit_must_not_ride_along(self):
        before = self.remote()
        self.commit("feat: something unreviewed", "skills/x/a.md")
        self.commit("learn: a fact", "skills/x/b.md")
        out = self.fire()
        self.assertEqual(self.remote(), before, "pushed an unreviewed commit")
        self.assertIn("not learn:", out.stderr)

    def test_the_guard_itself_is_not_auto_pushable(self):
        before = self.remote()
        self.commit("learn: tweak the hook", ".claude/hooks/push-learnings.sh", "#!/bin/bash\n")
        out = self.fire()
        self.assertEqual(self.remote(), before)
        self.assertIn("outside the knowledge-base surface", out.stderr)

    def test_scripts_and_hooks_directories_need_review(self):
        before = self.remote()
        self.commit("learn: edit a script", "scripts/build_index.py", "print(1)\n")
        self.fire()
        self.assertEqual(self.remote(), before)

    def test_secret_shaped_strings_block_the_push(self):
        before = self.remote()
        self.commit("learn: oops", "skills/x/leak.md", "token ghp_" + "a" * 36 + "\n")
        out = self.fire()
        self.assertEqual(self.remote(), before)
        self.assertIn("secret-shaped", out.stderr)

    def test_only_acts_on_main(self):
        before = self.remote()
        git(self.work, "checkout", "-q", "-b", "feature")
        self.commit("learn: on a branch", "skills/x/c.md")
        out = self.fire()
        self.assertEqual(out.returncode, 0)
        self.assertEqual(self.remote(), before)

    def test_diverged_origin_is_never_force_pushed(self):
        other = self.tmp / "other"
        subprocess.run(["git", "clone", "-q", str(self.origin), str(other)], check=True, capture_output=True)
        (other / "elsewhere.md").write_text("y\n")
        git(other, "add", "-A")
        git(other, "commit", "-q", "-m", "someone else")
        git(other, "push", "-q", "origin", "main")
        theirs = self.remote()
        self.commit("learn: mine", "skills/x/d.md")
        out = self.fire()
        self.assertEqual(self.remote(), theirs)
        self.assertIn("diverged", out.stderr)

    def test_non_learn_head_is_ignored(self):
        before = self.remote()
        self.commit("docs: not a learning", "skills/x/e.md")
        self.assertEqual(self.fire().returncode, 0)
        self.assertEqual(self.remote(), before)


if __name__ == "__main__":
    unittest.main()
