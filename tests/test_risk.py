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

    def test_unknown_is_never_read(self):
        self.assertEqual(r.classify("totally.unknown-op"), "write")

    def test_internal_and_beta_prefixes_are_ignored(self):
        self.assertEqual(r.classify("internal/works.delete"), "destructive")
        self.assertEqual(r.classify("/beta/works.list"), "read")


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


if __name__ == "__main__":
    unittest.main()
