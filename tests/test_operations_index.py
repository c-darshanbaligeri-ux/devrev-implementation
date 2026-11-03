"""The workflow-operations index and the finder's operation search. Run: python3 -m unittest discover -s tests"""
import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIND = str(ROOT / "bin" / "devrev-find")
OPS_DIR = ROOT / "skills" / "6-workflows" / "operations"


def find(*args):
    return subprocess.run([sys.executable, FIND, *args], capture_output=True, text=True, cwd="/")


class OperationsIndex(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.doc = json.loads((ROOT / "index" / "operations.json").read_text(encoding="utf-8"))
        cls.ops = cls.doc["operations"]
        cls.by = {o["slug"]: o for o in cls.ops}

    def test_counts_match_the_catalog_headings(self):
        kinds = self.doc["meta"]["kinds"]
        self.assertEqual({k: kinds[k] for k in ("trigger", "action", "control", "blocking")},
                         {"trigger": 145, "action": 245, "control": 8, "blocking": 2})
        self.assertEqual(self.doc["meta"]["with_schema"], len(list((OPS_DIR / "schemas").glob("*.md"))))
        self.assertEqual(self.doc["meta"]["count"], len(self.ops))

    def test_slugs_are_unique_and_namespaced(self):
        self.assertEqual(len(self.by), len(self.ops))
        for o in self.ops:
            self.assertTrue(o["slug"], o)
            if o["kind"] != "other":
                self.assertIn(o["namespace"], ("devrev", "custom_object"), o["slug"])

    def test_every_schema_file_is_attached_to_a_record(self):
        for p in (OPS_DIR / "schemas").glob("*.md"):
            self.assertEqual(self.by[p.stem]["schema"], p.relative_to(ROOT).as_posix(), p.stem)

    def test_pointers_exist(self):
        for o in self.ops:
            self.assertTrue((ROOT / o["doc"].split("#")[0]).exists(), o["slug"])
            if o["schema"]:
                self.assertTrue((ROOT / o["schema"]).exists(), o["slug"])
            for ex in o["examples"]:
                self.assertTrue((ROOT / "skills" / "6-workflows" / "examples" / ex).exists(), (o["slug"], ex))

    def test_ports_come_from_the_schema_files_with_required_marks(self):
        ports = self.by["add_comment"]["ports"]["in"]["input"]
        self.assertIn("object:id*", ports)
        self.assertIn("body:text*", ports)
        self.assertIn("visibility:enum", ports)
        self.assertEqual(self.by["add_comment"]["ports_source"], "schema")

    def test_example_usage_is_decoded_from_the_template_files(self):
        self.assertIn("working-loop-variable-sample.json", self.by["loop_over_issues"]["examples"])
        self.assertIn("working-invoke-code-sample.json", self.by["invoke_code"]["examples"])

    def test_operations_named_in_the_evals_exist(self):
        cases = json.loads((ROOT / "evals" / "finder-cases.json").read_text(encoding="utf-8"))["cases"]
        named = {o for c in cases for o in c.get("expect_operations", [])}
        self.assertGreaterEqual(len(named), 8)
        self.assertEqual(sorted(named - set(self.by)), [])


class InternalWorkflowEndpoints(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        eps = json.loads((ROOT / "index" / "endpoints.json").read_text(encoding="utf-8"))["endpoints"]
        cls.by = {e["name"]: e for e in eps}

    def test_import_validate_publish_routes_are_indexed(self):
        for name in ("workflows.templates.instantiate", "workflows.components.validate", "workflows.update-status",
                     "workflow-versions.list", "workflow-versions.publish", "workflow-steps.list", "workflow-steps.update",
                     "keyrings.list", "dev-orgs.self", "workflows.get", "workflows.list"):
            self.assertIn(name, self.by, name)
            self.assertIn("internal", self.by[name]["channels"], name)
            self.assertTrue(self.by[name]["internal_path"].startswith("/internal/"), name)

    def test_publishing_routes_say_what_they_do(self):
        self.assertIn("switches the workflow on", self.by["workflows.update-status"]["purpose"])
        self.assertIn("already published", self.by["workflow-versions.publish"]["purpose"])

    def test_public_names_keep_their_public_record(self):
        self.assertIn("public", self.by["dev-users.self"]["channels"])


class FinderOperations(unittest.TestCase):
    def test_operation_brief(self):
        out = find("--operation", "add_comment")
        self.assertEqual(out.returncode, 0, out.stderr)
        self.assertIn('"slug": "add_comment"', out.stdout)
        self.assertIn("object:id*", out.stdout)
        self.assertIn("visibility: external, internal, private", out.stdout)
        self.assertIn("/skills/6-workflows/operations/schemas/add_comment.md", out.stdout)

    def test_operation_lookup_accepts_namespace_prefixes_and_titles(self):
        for name in ("devrev.add_comment", "operation-devrev.add_comment", "Add Comment"):
            self.assertEqual(find("--operation", name).returncode, 0, name)

    def test_unknown_operation_fails_loudly_with_suggestions(self):
        out = find("--operation", "ticket")
        self.assertEqual(out.returncode, 1)
        self.assertIn("Did you mean", out.stdout)
        self.assertNotEqual(find("--operation", "zzz_no_such_step").returncode, 0)

    def test_operation_json(self):
        data = json.loads(find("--operation", "if_else", "--json").stdout)
        self.assertEqual(data["operation"]["kind"], "control")

    def test_automation_goals_list_triggers_and_steps(self):
        out = find("when a ticket is created, wait a day, then send a notification to the team")
        self.assertIn("WORKFLOW OPERATIONS", out.stdout)
        for slug in ("ticket_created", "sleep_for", "send_notification"):
            self.assertIn(slug, out.stdout)

    def test_plain_api_goals_do_not_list_operations(self):
        self.assertNotIn("WORKFLOW OPERATIONS", find("show me all open tickets").stdout)

    def test_json_search_carries_operations(self):
        data = json.loads(find("when a ticket is created notify the team", "--json").stdout)
        self.assertTrue(data["operations"])
        triggers = [o["slug"] for _, o in data["operations"] if o["kind"] == "trigger"]
        self.assertIn("ticket_created", triggers)


if __name__ == "__main__":
    unittest.main()
