"""Plugin packaging invariants. Run: python3 -m unittest discover -s tests"""
import json
import os
import re
import shutil
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(rel):
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


class Manifests(unittest.TestCase):
    def test_plugin_manifest(self):
        m = load(".claude-plugin/plugin.json")
        self.assertEqual(m["name"], "devrev-operator")
        self.assertRegex(m["name"], r"^[a-z0-9-]+$")
        self.assertNotIn("version", m, "no version: every push must be an update for installers")
        self.assertNotIn("skills", m, "the default skills/ directory is the plugin layout")
        self.assertTrue(m["homepage"].startswith("https://"))

    def test_marketplace_lists_the_plugin_under_the_same_name(self):
        mk = load(".claude-plugin/marketplace.json")
        self.assertEqual(mk["name"], "devrev-implementation")
        self.assertEqual([p["name"] for p in mk["plugins"]], [load(".claude-plugin/plugin.json")["name"]])
        self.assertEqual(mk["plugins"][0]["source"], "./")

    def test_this_repo_does_not_enable_the_plugin_for_itself(self):
        enabled = load(".claude/settings.json")["enabledPlugins"]
        self.assertFalse([k for k in enabled if k.startswith("devrev-operator")], "the plugin must stay opt-in")

    def test_only_first_party_mcp_servers_ship(self):
        servers = load(".mcp.json")["mcpServers"]
        self.assertEqual(list(servers), ["devrev"])
        self.assertRegex(servers["devrev"]["url"], r"^https://([a-z0-9-]+\.)*devrev\.ai/")


class Components(unittest.TestCase):
    def test_hook_is_registered_for_the_plugin_and_exists(self):
        hooks = load("hooks/hooks.json")["hooks"]["PreToolUse"][0]
        self.assertEqual(hooks["matcher"], "Bash")
        cmd = hooks["hooks"][0]["command"]
        self.assertIn("${CLAUDE_PLUGIN_ROOT}/hooks/devrev-safety.py", cmd)
        self.assertTrue((ROOT / "hooks" / "devrev-safety.py").exists())

    def test_the_same_hook_guards_this_repo(self):
        pre = load(".claude/settings.json")["hooks"]["PreToolUse"][0]
        self.assertIn("hooks/devrev-safety.py", pre["hooks"][0]["command"])

    def test_finder_is_executable_so_it_works_from_the_plugin_bin_path(self):
        self.assertTrue(os.access(ROOT / "bin" / "devrev-find", os.X_OK))
        self.assertTrue(os.access(ROOT / "hooks" / "devrev-safety.py", os.X_OK))

    def test_every_bin_command_is_executable_and_has_a_shebang(self):
        commands = sorted(p for p in (ROOT / "bin").iterdir() if p.is_file())
        self.assertIn("devrev-validate-workflow", [p.name for p in commands])
        for p in commands:
            self.assertTrue(os.access(p, os.X_OK), f"{p.name} must be executable (the plugin puts bin/ on PATH)")
            self.assertTrue(p.read_text(encoding="utf-8").startswith("#!"), f"{p.name} needs a shebang")

    def test_finder_reports_its_root(self):
        out = subprocess.run([sys.executable, str(ROOT / "bin" / "devrev-find"), "--root"], capture_output=True, text=True, cwd="/")
        self.assertEqual(Path(out.stdout.strip()).resolve(), ROOT.resolve())

    def test_researcher_agent_is_read_only_by_construction(self):
        text = (ROOT / "agents" / "devrev-api-researcher.md").read_text(encoding="utf-8")
        fm = re.match(r"\A---\n(.*?)\n---\n", text, re.S).group(1)
        self.assertIn("name: devrev-api-researcher", fm)
        tools = re.search(r"^tools: (.+)$", fm, re.M).group(1)
        self.assertNotRegex(tools, r"Edit|Write|NotebookEdit")
        self.assertIn("Never calls the DevRev API", fm)

    def test_skill_paths_are_plugin_ready(self):
        out = subprocess.run([sys.executable, "-I", str(ROOT / "scripts" / "rewrite_plugin_paths.py"), "--check"], capture_output=True, text=True)
        self.assertEqual(out.returncode, 0, out.stdout + "\nrun: python3 -I scripts/rewrite_plugin_paths.py")

    def test_fenced_shell_snippets_never_use_the_unset_plugin_variable(self):
        for p in (ROOT / "skills").glob("*/SKILL.md"):
            fence = False
            for n, line in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
                if line.lstrip().startswith("```"):
                    fence = not fence
                elif fence:
                    self.assertNotIn("${CLAUDE_PLUGIN_ROOT}", line, f"{p.parent.name}:{n} (unset in a plain checkout)")


@unittest.skipUnless(shutil.which("claude"), "claude CLI not installed")
class OfficialValidator(unittest.TestCase):
    def test_claude_plugin_validate_passes(self):
        out = subprocess.run(["claude", "plugin", "validate", str(ROOT)], capture_output=True, text=True, timeout=120)
        self.assertEqual(out.returncode, 0, out.stdout + out.stderr)
        self.assertNotIn("Validation failed", out.stdout)


if __name__ == "__main__":
    unittest.main()
