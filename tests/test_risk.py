"""Risk classification: endpoint names and whole shell commands. Run: python3 -m unittest discover -s tests"""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import devrev_risk as r  # noqa: E402


class ClassifyName(unittest.TestCase):
    def test_reads(self):
        for n in ("works.list", "works.get", "accounts.count", "ping", "search.hybrid", "dev-users.self", "schemas.custom.get",
                  "groups.members.list", "artifacts.locate", "accounts.export", "tables.query.execute"):
            self.assertEqual(r.classify(n), "read", n)

    def test_writes(self):
        for n in ("works.create", "works.update", "timeline-entries.create", "artifacts.prepare", "tags.create", "links.create"):
            self.assertEqual(r.classify(n), "write", n)

    def test_destructive(self):
        for n in ("works.delete", "accounts.merge", "webhooks.delete", "objects.bulk-upgrade", "schemas.custom.set",
                  "stages.custom.create", "states.custom.create", "web-crawler-jobs.control", "auth-tokens.self.delete"):
            self.assertEqual(r.classify(n), "destructive", n)

    def test_deprecation_in_body_is_destructive(self):
        self.assertEqual(r.classify("link-types.custom.update", {"deprecated": True}), "destructive")
        self.assertEqual(r.classify("link-types.custom.update", {"deprecated": False}), "write")

    def test_validate_is_read_but_publishing_is_not(self):
        self.assertEqual(r.classify("workflows.components.validate"), "read")
        for n in ("workflows.update-status", "workflow-versions.publish", "workflows.templates.instantiate"):
            self.assertEqual(r.classify(n), "write", n)

    def test_unknown_is_never_read(self):
        self.assertEqual(r.classify("totally.unknown-op"), "write")

    def test_internal_and_beta_prefixes_are_ignored(self):
        self.assertEqual(r.classify("internal/works.delete"), "destructive")
        self.assertEqual(r.classify("/beta/works.list"), "read")


class HighImpact(unittest.TestCase):
    def notes(self, cmd):
        return r.impact_notes(cmd)

    def test_publishing_routes_are_high_impact(self):
        for n in ("workflows.update-status", "workflow-versions.publish"):
            cmd = f"curl -X POST https://api.devrev.ai/internal/{n} -d '{{\"id\":\"x\"}}'"
            self.assertEqual(len(self.notes(cmd)), 1, n)
            self.assertEqual(r.classify_command(cmd)[0], "write", "high impact stays a write: the hook asks")

    def test_replacing_a_draft_on_import_is_high_impact(self):
        cmd = "curl -X POST https://api.devrev.ai/internal/workflows.templates.instantiate -d '{\"override_draft\": true}'"
        self.assertIn("override_draft", self.notes(cmd)[0])
        plain = "curl -X POST https://api.devrev.ai/internal/workflows.templates.instantiate -d '{}'"
        self.assertEqual(self.notes(plain), [])

    def test_ordinary_calls_have_no_notes(self):
        self.assertEqual(self.notes("curl https://api.devrev.ai/works.create -d '{}'"), [])
        self.assertEqual(self.notes("curl https://api.devrev.ai/internal/workflows.components.validate -d '{}'"), [])


class ClassifyCommand(unittest.TestCase):
    def verdict(self, cmd):
        return r.classify_command(cmd)[0]

    def test_read_call(self):
        self.assertEqual(self.verdict("curl -s -X POST 'https://api.devrev.ai/works.list' -H \"Authorization: Bearer $DEVREV_PAT\" -d '{\"limit\":5}'"), "read")

    def test_endpoint_variable_form(self):
        self.assertEqual(self.verdict("curl -X POST \"$DEVREV_ENDPOINT/works.create\" -d '{\"title\":\"x\"}'"), "write")
        self.assertEqual(self.verdict("curl -X POST ${DEVREV_ENDPOINT}/accounts.delete -d '{}'"), "destructive")

    def test_internal_path(self):
        self.assertEqual(self.verdict("curl -X POST https://api.devrev.ai/internal/objects.bulk-upgrade -d '{\"type\":\"ticket\"}'"), "destructive")

    def test_deprecated_body_raises_the_call(self):
        self.assertEqual(self.verdict("curl -X POST https://api.devrev.ai/link-types.custom.update -d '{\"id\":\"don:x\",\"deprecated\":true}'"), "destructive")

    def test_chained_commands_take_the_worst(self):
        self.assertEqual(self.verdict("curl https://api.devrev.ai/accounts.get -d '{}' && curl https://api.devrev.ai/accounts.delete -d '{}'"), "destructive")

    def test_no_opinion_on_other_commands(self):
        for c in ("ls -la", "git push origin main", "curl https://example.com/works.delete", "echo works.delete"):
            self.assertIsNone(self.verdict(c), c)

    def test_lookalike_hosts_are_not_devrev(self):
        for c in ("curl https://evildevrev.ai/works.delete", "curl https://api.devrev.ai.evil.com/works.delete",
                  "curl https://devrev.ai.example.org/works.delete"):
            self.assertIsNone(self.verdict(c), c)
        self.assertEqual(self.verdict("curl https://devrev.ai/works.delete"), "destructive")
        self.assertEqual(self.verdict("curl https://api.devrev.ai/works.delete"), "destructive")


if __name__ == "__main__":
    unittest.main()
