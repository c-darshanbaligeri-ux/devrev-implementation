"""The offline workflow-template validator. Run: python3 -m unittest discover -s tests

Ground truth: the default-/working-/ai-agent-skill example templates import fine, so the validator must report no
error for them. Every rule is then shown to fire on a deliberate mutation of one of those examples.
"""
import copy
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = ROOT / "skills" / "6-workflows" / "examples"
SCRIPT = ROOT / "skills" / "6-workflows" / "scripts" / "validate_template.py"
BIN = ROOT / "bin" / "devrev-validate-workflow"

spec = importlib.util.spec_from_file_location("validate_template", SCRIPT)
vt = importlib.util.module_from_spec(spec)
spec.loader.exec_module(vt)

GROUND_TRUTH = sorted(p.name for p in EXAMPLES.glob("*.json") if p.name.startswith(("default-", "working-", "ai-agent-skill-")))


def inner_of(name):
    return json.loads(json.loads((EXAMPLES / name).read_text(encoding="utf-8"))["data"])


def wrap(inner):
    return json.dumps({"templateVersion": "2.0.0", "data": json.dumps(inner)})


def step(inner, key):
    return next(s for s in inner["steps"] if s["reference_key"] == key)


def descriptors(node):
    return list(vt.walk_field_descriptors(node))


def check(inner_or_text):
    text = inner_or_text if isinstance(inner_or_text, str) else wrap(inner_or_text)
    return vt.validate_text(text, "t.json")[0]


def rules(rep, severity=None):
    return {i["rule"] for i in rep.issues if severity in (None, i["severity"])}


class GroundTruth(unittest.TestCase):
    def test_there_are_examples_to_calibrate_on(self):
        self.assertGreaterEqual(len(GROUND_TRUTH), 7)

    def test_confirmed_examples_have_no_errors_and_no_warnings(self):
        for name in GROUND_TRUTH:
            rep = vt.validate_file(EXAMPLES / name)
            self.assertEqual(rep.issues, [], f"{name}: {vt.render(rep)}")

    def test_production_templates_have_no_errors(self):
        for p in sorted(EXAMPLES.glob("[0-9]*.json")):
            rep = vt.validate_file(p)
            self.assertEqual(rep.errors, [], f"{p.name}: {vt.render(rep)}")


class Wrapper(unittest.TestCase):
    def test_data_as_an_object_is_an_error(self):
        rep = check(json.dumps({"templateVersion": "2.0.0", "data": inner_of("working-csat-score-on-ticket-resolved.json")}))
        self.assertIn("data_not_string", rules(rep, "error"))

    def test_wrong_template_version(self):
        rep = check(json.dumps({"templateVersion": "1.0.0", "data": json.dumps(inner_of("working-csat-score-on-ticket-resolved.json"))}))
        self.assertIn("wrapper", rules(rep, "error"))

    def test_data_that_is_not_json(self):
        self.assertIn("data_json", rules(check(json.dumps({"templateVersion": "2.0.0", "data": "{nope"})), "error"))

    def test_not_json_at_all(self):
        self.assertIn("json", rules(check("{ not json"), "error"))

    def test_bare_inner_json_is_accepted_with_a_warning(self):
        rep = check(json.dumps(inner_of("working-csat-score-on-ticket-resolved.json")))
        self.assertEqual(rep.errors, [])
        self.assertIn("bare_inner", rules(rep, "warning"))


class Header(unittest.TestCase):
    def test_serialization_version(self):
        i = inner_of("working-csat-score-on-ticket-resolved.json")
        i["serialization_version"] = {"major": 1, "minor": 0, "patch": 0}
        self.assertIn("serialization_version", rules(check(i), "error"))

    def test_title_must_be_non_empty(self):
        i = inner_of("working-csat-score-on-ticket-resolved.json")
        i["title"] = ""
        self.assertIn("title", rules(check(i), "error"))

    def test_steps_must_exist(self):
        i = inner_of("working-csat-score-on-ticket-resolved.json")
        i["steps"] = []
        self.assertIn("steps", rules(check(i), "error"))


class Graph(unittest.TestCase):
    def setUp(self):
        self.base = inner_of("working-csat-score-on-ticket-resolved.json")
        self.keys = [s["reference_key"] for s in self.base["steps"]]

    def test_duplicate_reference_key(self):
        i = copy.deepcopy(self.base)
        i["steps"][1]["reference_key"] = i["steps"][0]["reference_key"]
        self.assertIn("duplicate_reference_key", rules(check(i), "error"))

    def test_bad_reference_key_characters(self):
        i = copy.deepcopy(self.base)
        i["steps"][1]["reference_key"] = "1-bad key"
        self.assertIn("reference_key", rules(check(i), "error"))

    def test_next_step_points_nowhere(self):
        i = copy.deepcopy(self.base)
        i["steps"][0]["next_steps"][0]["next_step_reference_key"] = "ghost_step"
        self.assertIn("next_step_missing", rules(check(i), "error"))

    def test_raw_api_edge_key_is_called_out(self):
        i = copy.deepcopy(self.base)
        e = i["steps"][0]["next_steps"][0]
        e["next_step"] = e.pop("next_step_reference_key")
        self.assertIn("next_step_shape", rules(check(i), "error"))

    def test_if_else_ports_must_be_true_and_false(self):
        i = copy.deepcopy(self.base)
        cond = next(s for s in i["steps"] if s["operation"]["slug"] == "if_else")
        for e in cond["next_steps"]:
            if e["port_name"] == "true":
                e["port_name"] = "yes"
        self.assertIn("port_name", rules(check(i), "error"))

    def test_cycle(self):
        i = copy.deepcopy(self.base)
        last = i["steps"][-1]
        last["next_steps"] = [{"port_name": "output", "next_step_reference_key": i["steps"][1]["reference_key"], "next_port_name": "input"}]
        self.assertIn("cycle", rules(check(i), "error"))

    def test_no_trigger(self):
        i = copy.deepcopy(self.base)
        trigger = next(s for s in i["steps"] if s["operation"]["slug"] == "ticket_updated")
        trigger["operation"]["slug"] = "add_comment"
        self.assertIn("no_trigger", rules(check(i), "error"))

    def test_unreachable_step_is_a_warning(self):
        i = copy.deepcopy(self.base)
        orphan = copy.deepcopy(i["steps"][-1])
        orphan["reference_key"] = "orphan_1"
        orphan["next_steps"] = []
        i["steps"].append(orphan)
        rep = check(i)
        self.assertIn("unreachable_step", rules(rep, "warning"))
        self.assertEqual(rep.errors, [])


class Operations(unittest.TestCase):
    def setUp(self):
        self.base = inner_of("working-csat-score-on-ticket-resolved.json")

    def test_typo_in_a_catalog_slug(self):
        i = copy.deepcopy(self.base)
        step(i, "ticket_updated_1")["operation"]["slug"] = "ticket_updatd"
        rep = check(i)
        self.assertIn("unknown_operation", rules(rep, "error"))
        self.assertIn("ticket_updated", " ".join(x["message"] for x in rep.issues))

    def test_wrong_namespace(self):
        i = copy.deepcopy(self.base)
        step(i, "ticket_updated_1")["operation"]["namespace"] = "custom_object"
        self.assertIn("wrong_namespace", rules(check(i), "error"))

    def test_third_party_namespace_is_only_a_warning(self):
        i = copy.deepcopy(self.base)
        step(i, "ask_ai_1")["operation"] = {"namespace": "send-emails", "slug": "send_emails"}
        rep = check(i)
        self.assertEqual(rep.errors, [])
        self.assertIn("third_party_operation", rules(rep, "warning"))

    def test_undocumented_input_field_warns_with_a_suggestion(self):
        i = copy.deepcopy(self.base)
        add = next(s for s in i["steps"] if s["operation"]["slug"] == "add_comment")
        add["input_values"][0]["fields"][0]["name"] = "bodyy"
        rep = check(i)
        self.assertIn("field_name", rules(rep, "warning"))
        self.assertIn("body", " ".join(x["message"] for x in rep.issues if x["rule"] == "field_name"))

    def test_custom_fields_are_not_flagged(self):
        i = copy.deepcopy(self.base)
        add = next(s for s in i["steps"] if s["operation"]["slug"] == "add_comment")
        add["input_values"][0]["fields"].append({"name": "tnt__anything", "value": {"type": "literal", "value": 1}})
        self.assertNotIn("field_name", rules(check(i)))


class References(unittest.TestCase):
    def setUp(self):
        self.base = inner_of("working-csat-score-on-ticket-resolved.json")

    def _expr_step(self, i):
        return next(s for s in i["steps"] if any(f["value"]["type"] == "jsonata_expression"
                                                  for iv in s.get("input_values") or [] for f in iv.get("fields", [])))

    def test_dangling_get(self):
        i = copy.deepcopy(self.base)
        add = next(s for s in i["steps"] if s["operation"]["slug"] == "add_comment")
        add["input_values"][0]["fields"].append({"name": "body", "value": {"type": "jsonata_expression", "value": "$get('ghost_1', 'output').id"}})
        self.assertIn("dangling_reference", rules(check(i), "error"))

    def test_dangling_get_inside_a_text_template(self):
        i = copy.deepcopy(self.base)
        add = next(s for s in i["steps"] if s["operation"]["slug"] == "add_comment")
        add["input_values"][0]["fields"].append({"name": "body", "value": {"type": "text_template", "value": "Hi {% expr $get('ghost_1', 'output').id %}"}})
        self.assertIn("dangling_reference", rules(check(i), "error"))

    def test_reading_a_step_that_runs_later_warns(self):
        i = copy.deepcopy(self.base)
        trig = step(i, "ticket_updated_1")
        last = i["steps"][-1]["reference_key"]
        trig["input_values"][0]["fields"].append({"name": "fields_to_watch", "value": {"type": "jsonata_expression", "value": f"$get('{last}', 'output').id"}})
        self.assertIn("reference_not_upstream", rules(check(i), "warning"))

    def test_integer_value_type(self):
        i = copy.deepcopy(self.base)
        add = next(s for s in i["steps"] if s["operation"]["slug"] == "add_comment")
        add["input_values"][0]["fields"][0]["value"]["type"] = 1
        self.assertIn("value_type", rules(check(i), "error"))

    def test_unknown_value_type_name(self):
        i = copy.deepcopy(self.base)
        add = next(s for s in i["steps"] if s["operation"]["slug"] == "add_comment")
        add["input_values"][0]["fields"][0]["value"]["type"] = "string"
        self.assertIn("value_type", rules(check(i), "error"))

    def test_unbalanced_template_marker(self):
        i = copy.deepcopy(self.base)
        add = next(s for s in i["steps"] if s["operation"]["slug"] == "add_comment")
        add["input_values"][0]["fields"].append({"name": "body", "value": {"type": "text_template", "value": "x {% expr $get('ticket_updated_1').id "}})
        self.assertIn("template_unbalanced", rules(check(i), "error"))

    def test_expression_inside_a_literal_warns(self):
        i = copy.deepcopy(self.base)
        add = next(s for s in i["steps"] if s["operation"]["slug"] == "add_comment")
        add["input_values"][0]["fields"].append({"name": "body", "value": {"type": "literal", "value": "$get('ticket_updated_1').id"}})
        self.assertIn("literal_expression", rules(check(i), "warning"))


class LoopsAndVariables(unittest.TestCase):
    def setUp(self):
        self.base = inner_of("working-loop-variable-sample.json")

    def test_uenum_without_allowed_values(self):
        i = copy.deepcopy(self.base)
        node = next(d for d in descriptors(step(i, "set_variable_1")["input_ports"]) if d["field_type"] == "uenum")
        del node["allowed_values"]
        self.assertIn("uenum_allowed_values", rules(check(i), "error"))

    def test_array_without_base_type(self):
        i = copy.deepcopy(self.base)
        node = next(d for s in i["steps"] for d in descriptors(s.get("input_ports")) + descriptors(s.get("output_ports")) if d["field_type"] == "array")
        del node["base_type"]
        self.assertIn("array_base_type", rules(check(i), "error"))

    def test_loop_without_block_callback(self):
        i = copy.deepcopy(self.base)
        loop = step(i, "loop_over_issues_1")
        loop["input_ports"] = [p for p in loop["input_ports"] if p["name"] != "block_callback"]
        self.assertIn("loop_block_callback", rules(check(i), "error"))

    def test_loop_without_block_start_port(self):
        i = copy.deepcopy(self.base)
        loop = step(i, "loop_over_issues_1")
        for p in loop["output_ports"]:
            if p["name"] == "block_start":
                p["type"] = "default"
        self.assertIn("loop_block_start", rules(check(i), "error"))

    def test_loop_child_without_block_step_reference_key(self):
        i = copy.deepcopy(self.base)
        del step(i, "http_1")["block_step_reference_key"]
        self.assertIn("block_child", rules(check(i), "error"))

    def test_init_variable_without_scope_variables(self):
        i = copy.deepcopy(self.base)
        for p in step(i, "init_variable_1")["output_ports"]:
            p.pop("scope_variables", None)
        self.assertIn("init_variable_scope", rules(check(i), "error"))

    def test_set_variable_targeting_a_missing_step(self):
        i = copy.deepcopy(self.base)
        fields = step(i, "set_variable_1")["input_values"][0]["fields"]
        var = next(f for f in fields if f["name"] == "variable")
        var["value"]["value"]["step_reference_key"] = "init_variable_9"
        self.assertIn("dangling_reference", rules(check(i), "error"))

    def test_reading_a_variable_with_get_warns(self):
        i = copy.deepcopy(self.base)
        ask = step(i, "ask_ai_1")
        ask["input_values"][0]["fields"].append({"name": "ai_input", "value": {"type": "jsonata_expression", "value": "$get('init_variable_1', 'output').summary"}})
        self.assertIn("use_get_variable", rules(check(i), "warning"))

    def test_for_each_warns(self):
        i = copy.deepcopy(self.base)
        step(i, "loop_over_issues_1")["operation"]["slug"] = "for_each"
        self.assertIn("for_each_dynamic", rules(check(i), "warning"))


class InvokeCode(unittest.TestCase):
    def setUp(self):
        self.base = inner_of("working-enhancement-replace-agent.json")

    def test_code_must_be_a_text_template(self):
        i = copy.deepcopy(self.base)
        code = next(s for s in i["steps"] if s["operation"]["slug"] == "invoke_code")
        field = next(f for f in code["input_values"][0]["fields"] if f["name"] == "code")
        field["value"]["type"] = "literal"
        self.assertIn("invoke_code_value", rules(check(i), "error"))

    def test_items_must_be_composite_value_list(self):
        i = copy.deepcopy(self.base)
        code = next(s for s in i["steps"] if s["operation"]["slug"] == "invoke_code")
        field = next(f for f in code["input_values"][0]["fields"] if f["name"] == "input_values")
        field["value"]["value"]["items"][0]["type"] = "composite_value"
        self.assertIn("invoke_code_value", rules(check(i), "error"))


class AgentSkill(unittest.TestCase):
    def setUp(self):
        self.base = inner_of("default-ai-agent-skill-template.json")

    def test_skill_without_output_step(self):
        i = copy.deepcopy(self.base)
        i["steps"] = [s for s in i["steps"] if s["operation"]["slug"] != "set_ai_agent_skill_output"]
        for s in i["steps"]:
            s["next_steps"] = [e for e in s.get("next_steps", []) if e["next_step_reference_key"] != "set_ai_agent_skill_output_1"]
        self.assertIn("skill_output", rules(check(i), "error"))

    def test_skill_label_missing(self):
        i = copy.deepcopy(self.base)
        i["labels"] = []
        self.assertIn("skill_label", rules(check(i), "warning"))

    def test_skill_label_without_skill_trigger(self):
        i = inner_of("working-csat-score-on-ticket-resolved.json")
        i["labels"] = ["skill"]
        self.assertIn("skill_trigger", rules(check(i), "error"))

    def test_skill_trigger_takes_no_filter(self):
        i = copy.deepcopy(self.base)
        trig = step(i, "ai_agent_skill_trigger_1")
        trig["input_values"][0]["fields"] = [{"name": "fields_to_watch", "value": {"type": "literal", "value": ["stage"]}}]
        self.assertIn("skill_trigger_filter", rules(check(i), "error"))


class CommandLine(unittest.TestCase):
    def run_cli(self, *args, launcher=BIN):
        return subprocess.run([sys.executable, str(launcher), *map(str, args)], capture_output=True, text=True, cwd="/")

    def test_exit_codes(self):
        ok = self.run_cli(EXAMPLES / "default-ai-agent-skill-template.json")
        self.assertEqual(ok.returncode, 0, ok.stdout + ok.stderr)
        with tempfile.TemporaryDirectory() as d:
            bad = Path(d) / "bad.json"
            bad.write_text("{ nope")
            self.assertEqual(self.run_cli(bad).returncode, 1)
        self.assertEqual(self.run_cli("/no/such/template.json").returncode, 2)

    def test_strict_fails_on_warnings(self):
        p = EXAMPLES / "5040-devrevu-enablement-journey-poc-emails-template.json"
        self.assertEqual(self.run_cli(p).returncode, 0)
        self.assertEqual(self.run_cli(p, "--strict").returncode, 1)

    def test_json_report_is_machine_readable(self):
        out = self.run_cli(EXAMPLES / "default-ai-agent-skill-template.json", "--json")
        data = json.loads(out.stdout)
        self.assertEqual(data[0]["errors"], 0)

    def test_script_and_launcher_agree(self):
        a = self.run_cli(EXAMPLES / "working-loop-variable-sample.json")
        b = self.run_cli(EXAMPLES / "working-loop-variable-sample.json", launcher=SCRIPT)
        self.assertEqual((a.returncode, a.stdout), (b.returncode, b.stdout))


if __name__ == "__main__":
    unittest.main()
