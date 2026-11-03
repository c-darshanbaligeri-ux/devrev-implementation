"""devrev-import-workflow against a local FAKE DevRev server (no live calls). Run: python3 -m unittest discover -s tests

The fake mimics the routes the live-tested import flow uses (instantiate, workflow-versions.list, components.validate,
update-status, versions.publish, keyrings, steps, whoami) and records every request, so the tests can assert the exact
order, bodies and headers, and that nothing is sent when it should not be.
"""
import json
import os
import subprocess
import sys
import tempfile
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

ROOT = Path(__file__).resolve().parents[1]
BIN = ROOT / "bin" / "devrev-import-workflow"
EXAMPLES = ROOT / "skills" / "6-workflows" / "examples"
TEMPLATE = EXAMPLES / "working-csat-score-on-ticket-resolved.json"
CODE_TEMPLATE = EXAMPLES / "working-invoke-code-sample.json"
TOKEN = "test-pat-123"
WF = "don:integration:dvrv-us-1:devo/TEST:workflow/35"
VER = WF + ":workflow_version/35.1"
VER2 = WF + ":workflow_version/35.2"
KEYRING = "don:core:dvrv-us-1:devo/TEST:keyring/7"


class Fake:
    """State and request log of the fake server."""

    def __init__(self):
        self.requests = []
        self.workflows = {}  # don -> {"status", "display_id"}
        self.versions = {}  # don -> [{"id", "status"}]
        self.validate_response = {"valid": True}
        self.fail = {}  # route -> HTTP status to return
        self.polls_until_active = 1
        self.pending = {}  # don -> polls left before it turns active
        self.keyrings = [{"id": KEYRING, "name": "My PAT"}]
        self.steps = []

    def names(self):
        return [r["route"] for r in self.requests]


def make_handler(state):
    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *a):
            pass

        def reply(self, obj, status=200):
            data = json.dumps(obj).encode()
            self.send_response(status)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)

        def handle_any(self, method):
            u = urlparse(self.path)
            route = u.path.replace("/internal/", "", 1).lstrip("/")
            query = {k: v[0] for k, v in parse_qs(u.query).items()}
            body = {}
            if method == "POST":
                n = int(self.headers.get("Content-Length") or 0)
                body = json.loads(self.rfile.read(n) or b"{}")
            state.requests.append({"method": method, "route": route, "query": query, "body": body,
                                   "auth": self.headers.get("Authorization"), "internal": u.path.startswith("/internal/")})
            if route in state.fail:
                return self.reply({"type": "bad_request", "message": f"forced failure on {route}"}, state.fail[route])
            getattr(self, "r_" + route.replace(".", "_").replace("-", "_"), self.not_found)(body, query)

        def do_GET(self):
            self.handle_any("GET")

        def do_POST(self):
            self.handle_any("POST")

        def not_found(self, body, query):
            self.reply({"message": "route not found"}, 404)

        def r_dev_users_self(self, body, query):
            self.reply({"dev_user": {"display_name": "Test User", "id": "don:identity:dvrv-us-1:devo/TEST:devu/1"}})

        def r_dev_orgs_self(self, body, query):
            self.reply({"dev_org": {"display_name": "Test Org", "id": "don:identity:dvrv-us-1:devo/TEST"}})

        def r_workflows_list(self, body, query):
            self.reply({"workflows": [{"id": d, "display_id": w["display_id"], "status": w["status"]} for d, w in state.workflows.items()]})

        def r_workflows_get(self, body, query):
            don = query["id"]
            w = state.workflows.get(don)
            if w is None:
                return self.reply({"message": "not found"}, 404)
            if state.pending.get(don) is not None:
                state.pending[don] -= 1
                if state.pending[don] <= 0:
                    w["status"] = "active"
                    del state.pending[don]
            self.reply({"workflow": {"id": don, **w}})

        def r_workflow_versions_list(self, body, query):
            self.reply({"workflow_versions": state.versions.get(query["workflow"], [])})

        def r_workflows_templates_instantiate(self, body, query):
            don = body.get("workflow")
            if don:
                vs = state.versions.setdefault(don, [])
                vs[:] = [v for v in vs if v["status"] != "draft"] + [{"id": VER2, "status": "draft"}]
            else:
                don = WF
                state.workflows[don] = {"status": "draft", "display_id": "workflow-35"}
                state.versions[don] = [{"id": VER, "status": "draft"}]
            self.reply({"workflow": {"id": don, **state.workflows[don]}})

        def r_workflows_components_validate(self, body, query):
            self.reply(state.validate_response)

        def r_workflows_update_status(self, body, query):
            state.pending[body["id"]] = state.polls_until_active
            self.reply({})

        def r_workflow_versions_publish(self, body, query):
            for vs in state.versions.values():
                for v in vs:
                    if v["id"] == body["id"]:
                        v["status"] = "published"
            self.reply({})

        def r_keyrings_list(self, body, query):
            self.reply({"keyrings": state.keyrings})

        def r_workflow_steps_list(self, body, query):
            self.reply({"workflow_steps": state.steps})

        def r_workflow_steps_update(self, body, query):
            self.reply({})

    return Handler


class ImportTest(unittest.TestCase):
    def setUp(self):
        self.fake = Fake()
        self.server = ThreadingHTTPServer(("127.0.0.1", 0), make_handler(self.fake))
        self.url = f"http://127.0.0.1:{self.server.server_address[1]}"
        threading.Thread(target=self.server.serve_forever, daemon=True).start()
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.addCleanup(self.server.server_close)
        self.addCleanup(self.server.shutdown)

    def run_cli(self, *args, token=TOKEN, template=TEMPLATE):
        env = {k: v for k, v in os.environ.items() if not k.startswith("DEVREV")}
        if token:
            env["DEVREV_PAT"] = token
        cmd = [sys.executable, str(BIN), str(template), "--base-url", self.url, "--poll-interval", "0.05", *map(str, args)]
        return subprocess.run(cmd, capture_output=True, text=True, cwd=self.tmp.name, env=env, timeout=60)

    def posted(self, route):
        return [r for r in self.fake.requests if r["route"] == route]

    def existing(self, status="active", drafts=False):
        self.fake.workflows[WF] = {"status": status, "display_id": "workflow-35"}
        self.fake.versions[WF] = [{"id": WF + ":workflow_version/35.0", "status": "published"}] + ([{"id": VER, "status": "draft"}] if drafts else [])


class NewWorkflow(ImportTest):
    def test_default_run_creates_a_draft_validates_and_stops(self):
        p = self.run_cli()
        self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
        self.assertEqual(self.fake.names(), ["dev-users.self", "dev-orgs.self", "workflows.templates.instantiate",
                                             "workflow-versions.list", "workflows.components.validate"])
        self.assertIn("Stopped at the validated draft", p.stdout)
        self.assertNotIn("workflows.update-status", self.fake.names())

    def test_org_and_user_are_printed_before_the_first_write(self):
        p = self.run_cli()
        self.assertIn("Target org: Test Org", p.stdout)
        self.assertIn("acting as: Test User", p.stdout)
        self.assertLess(p.stdout.index("Target org"), p.stdout.index("Created draft workflow"))

    def test_instantiate_gets_the_parsed_template_object_not_the_string(self):
        self.run_cli()
        body = self.posted("workflows.templates.instantiate")[0]["body"]
        self.assertEqual(set(body), {"template_version", "workflow_template_v2"})
        self.assertEqual(body["template_version"], "2.0.0")
        self.assertIsInstance(body["workflow_template_v2"], dict)
        self.assertEqual(body["workflow_template_v2"]["title"], "CSAT Score on Ticket Resolved")
        self.assertIsInstance(body["workflow_template_v2"]["steps"], list)

    def test_token_is_sent_bare_and_only_to_the_chosen_host(self):
        self.run_cli()
        self.assertTrue(self.fake.requests)
        for r in self.fake.requests:
            self.assertEqual(r["auth"], TOKEN)
        self.assertNotIn(TOKEN, self.run_cli().stdout + self.run_cli().stderr)

    def test_internal_routes_use_internal_and_whoami_uses_the_public_path(self):
        self.run_cli()
        for r in self.fake.requests:
            self.assertEqual(r["internal"], r["route"] != "dev-users.self", r["route"])

    def test_validate_gets_the_draft_version_id(self):
        self.run_cli()
        self.assertEqual(self.posted("workflows.components.validate")[0]["body"],
                         {"components": [{"type": "workflow", "workflow_version_id": VER}]})
        self.assertEqual(self.posted("workflow-versions.list")[0]["query"], {"workflow": WF})

    def test_publish_switches_a_draft_workflow_on_and_polls_until_active(self):
        self.fake.polls_until_active = 3
        p = self.run_cli("--publish", "--json")
        self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
        names = self.fake.names()
        self.assertEqual(names[-1], "workflows.get")
        self.assertIn("workflows.update-status", names)
        self.assertNotIn("workflow-versions.publish", names)
        self.assertEqual(self.posted("workflows.update-status")[0]["body"], {"id": WF, "status": "active"})
        self.assertGreaterEqual(len([n for n in names if n == "workflows.get"]), 4)  # one to decide + polls until active
        result = json.loads(p.stdout)
        self.assertEqual((result["published"], result["status"]), (True, "active"))
        self.assertLess(names.index("workflows.components.validate"), names.index("workflows.update-status"))

    def test_poll_timeout_fails_loudly(self):
        self.fake.polls_until_active = 10_000
        p = self.run_cli("--publish", "--poll-timeout", "0.4")
        self.assertEqual(p.returncode, 7)
        self.assertIn("timed out", p.stderr)
        self.assertIn("last status", p.stderr)

    def test_server_side_validation_failure_stops_before_publishing(self):
        self.fake.validate_response = {"valid": False, "errors": [{"message": "step x has no trigger"}], "warnings": [{"message": "w"}]}
        p = self.run_cli("--publish")
        self.assertEqual(p.returncode, 5)
        self.assertIn("step x has no trigger", p.stdout)
        self.assertNotIn("workflows.update-status", self.fake.names())
        self.assertIn("draft is in the org", p.stderr)

    def test_warnings_from_the_server_are_printed_but_do_not_block(self):
        self.fake.validate_response = {"valid": True, "warnings": [{"message": "unused variable"}]}
        p = self.run_cli()
        self.assertEqual(p.returncode, 0)
        self.assertIn("unused variable", p.stdout)


class NewVersion(ImportTest):
    def test_version_of_a_don_sends_workflow_and_override_draft(self):
        self.existing("active")
        p = self.run_cli("--version-of", WF)
        self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
        body = self.posted("workflows.templates.instantiate")[0]["body"]
        self.assertEqual(body["workflow"], WF)
        self.assertIs(body["override_draft"], True)
        self.assertIsInstance(body["workflow_template_v2"], dict)

    def test_workflow_n_is_resolved_through_workflows_list(self):
        self.existing("active")
        p = self.run_cli("--version-of", "workflow-35")
        self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
        self.assertIn("workflows.list", self.fake.names())
        self.assertEqual(self.posted("workflows.templates.instantiate")[0]["body"]["workflow"], WF)

    def test_unknown_workflow_number_is_refused_before_any_write(self):
        self.existing("active")
        p = self.run_cli("--version-of", "99")
        self.assertEqual(p.returncode, 3)
        self.assertNotIn("workflows.templates.instantiate", self.fake.names())

    def test_active_workflow_is_published_with_versions_publish_not_update_status(self):
        self.existing("active")
        p = self.run_cli("--version-of", WF, "--publish", "--notes", "v2 notes")
        self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
        self.assertEqual(self.posted("workflow-versions.publish")[0]["body"], {"id": VER2, "notes": "v2 notes"})
        self.assertNotIn("workflows.update-status", self.fake.names())

    def test_route_follows_live_state_even_when_version_of_is_given(self):
        self.existing("draft")  # never published: versions.publish would 400, so update-status must be used
        p = self.run_cli("--version-of", WF, "--publish")
        self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
        self.assertIn("workflows.update-status", self.fake.names())
        self.assertNotIn("workflow-versions.publish", self.fake.names())

    def test_inactive_workflow_is_never_published_into(self):
        self.existing("inactive")
        p = self.run_cli("--version-of", WF, "--publish")
        self.assertEqual(p.returncode, 3)
        self.assertNotIn("workflows.update-status", self.fake.names())
        self.assertNotIn("workflow-versions.publish", self.fake.names())

    def test_an_existing_draft_is_not_overwritten_without_the_flag(self):
        self.existing("active", drafts=True)
        p = self.run_cli("--version-of", WF)
        self.assertEqual(p.returncode, 3)
        self.assertIn("--override-draft", p.stderr)
        self.assertIn(VER, p.stderr)
        self.assertNotIn("workflows.templates.instantiate", self.fake.names())

    def test_override_draft_replaces_the_draft_when_asked(self):
        self.existing("active", drafts=True)
        p = self.run_cli("--version-of", WF, "--override-draft")
        self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
        self.assertIn("WARNING: --override-draft replaces the existing draft", p.stdout)
        self.assertEqual(len(self.posted("workflows.templates.instantiate")), 1)

    def test_override_draft_alone_is_a_usage_error(self):
        p = self.run_cli("--override-draft")
        self.assertEqual(p.returncode, 2)
        self.assertEqual(self.fake.requests, [])


class AttachConnection(ImportTest):
    def setUp(self):
        super().setUp()
        self.fake.steps = [{"id": "don:integration:dvrv-us-1:devo/TEST:workflow_step/35.1.3", "reference_key": "invoke_code_1"}]

    def code_key(self):
        inner = json.loads(json.loads(CODE_TEMPLATE.read_text())["data"])
        return next(s["reference_key"] for s in inner["steps"] if s["operation"]["slug"] == "invoke_code")

    def test_connection_is_attached_with_a_normalized_name_before_validation(self):
        self.fake.steps[0]["reference_key"] = self.code_key()
        p = self.run_cli("--attach-connection", "My PAT", template=CODE_TEMPLATE)
        self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
        body = self.posted("workflow-steps.update")[0]["body"]
        self.assertEqual(body, {"id": self.fake.steps[0]["id"], "keyrings": [{"name": "my_pat", "reference": KEYRING}]})
        names = self.fake.names()
        self.assertLess(names.index("workflow-steps.update"), names.index("workflows.components.validate"))
        self.assertEqual(self.posted("workflow-steps.list")[0]["query"], {"workflow_version": VER})

    def test_unknown_connection_lists_the_available_ones(self):
        p = self.run_cli("--attach-connection", "Nope", template=CODE_TEMPLATE)
        self.assertEqual(p.returncode, 3)
        self.assertIn("My PAT", p.stderr)
        self.assertNotIn("workflow-steps.update", self.fake.names())

    def test_ambiguous_connection_name_is_refused(self):
        self.fake.keyrings.append({"id": KEYRING + "b", "name": "my pat"})
        p = self.run_cli("--attach-connection", "My PAT", template=CODE_TEMPLATE)
        self.assertEqual(p.returncode, 3)
        self.assertNotIn("workflow-steps.update", self.fake.names())

    def test_template_without_a_code_step_is_a_usage_error(self):
        p = self.run_cli("--attach-connection", "My PAT")
        self.assertEqual(p.returncode, 2)
        self.assertNotIn("workflow-steps.update", self.fake.names())


class SafetyRails(ImportTest):
    def test_local_validation_errors_stop_everything(self):
        bad = Path(self.tmp.name) / "bad.json"
        bad.write_text(json.dumps({"templateVersion": "2.0.0", "data": "{\"title\": \"x\", \"steps\": []}"}))
        p = self.run_cli(template=bad)
        self.assertEqual(p.returncode, 1)
        self.assertEqual(self.fake.requests, [])

    def test_dry_run_sends_nothing_and_needs_no_token(self):
        p = self.run_cli("--dry-run", "--publish", "--version-of", WF, "--override-draft", token=None)
        self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
        self.assertEqual(self.fake.requests, [])
        self.assertIn("DRY RUN", p.stdout)
        self.assertIn("workflows.update-status", p.stdout)

    def test_dry_run_json_shows_the_parsed_body(self):
        p = self.run_cli("--dry-run", "--json", token=None)
        data = json.loads(p.stdout)
        inst = next(r for r in data["requests"] if r["url"].endswith("/internal/workflows.templates.instantiate"))
        self.assertIsInstance(inst["body"]["workflow_template_v2"], dict)
        self.assertEqual(inst["body"]["template_version"], "2.0.0")
        self.assertEqual(self.fake.requests, [])

    def test_missing_token_is_a_usage_error(self):
        p = self.run_cli(token=None)
        self.assertEqual(p.returncode, 2)
        self.assertIn("DEVREV_PAT", p.stderr)
        self.assertEqual(self.fake.requests, [])

    def test_token_is_never_sent_to_a_foreign_host(self):
        for base in ("https://evil.example.com", "http://api.devrev.ai", "https://devrev.ai.evil.com", "https://evildevrev.ai"):
            env = {**os.environ, "DEVREV_PAT": TOKEN}
            p = subprocess.run([sys.executable, str(BIN), str(TEMPLATE), "--base-url", base], capture_output=True, text=True,
                               cwd=self.tmp.name, env=env, timeout=30)
            self.assertEqual(p.returncode, 2, base)
            self.assertIn("refusing to send a token", p.stderr)

    def test_flag_abbreviations_are_rejected_so_the_hook_sees_exact_names(self):
        p = self.run_cli("--pub")
        self.assertNotEqual(p.returncode, 0)
        self.assertEqual(self.fake.requests, [])

    def test_api_errors_are_loud_and_carry_the_server_message(self):
        self.fake.fail["workflows.templates.instantiate"] = 400
        p = self.run_cli()
        self.assertEqual(p.returncode, 4)
        self.assertIn("HTTP 400", p.stderr)
        self.assertIn("forced failure", p.stderr)

    def test_unreadable_template(self):
        p = self.run_cli(template=Path(self.tmp.name) / "missing.json")
        self.assertEqual(p.returncode, 2)

    def test_token_can_come_from_a_dotenv_in_the_working_directory(self):
        (Path(self.tmp.name) / ".env").write_text("DEVREV_PAT=from-dotenv\n")
        p = self.run_cli(token=None)
        self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
        self.assertTrue(all(r["auth"] == "from-dotenv" for r in self.fake.requests))


if __name__ == "__main__":
    unittest.main()
