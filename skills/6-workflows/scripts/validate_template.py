#!/usr/bin/env python3
"""Validate a DevRev workflow template file offline, before it is imported. Standard library only.

    devrev-validate-workflow templates/my-workflow.json [more.json ...]
    options: --json   machine-readable report     --strict   treat warnings as errors
             --ops-index PATH   operations index to check slugs and ports against (default: <toolkit>/index/operations.json)

Accepts the importable wrapper ({"templateVersion": "2.0.0", "data": "<stringified inner JSON>"}) or the bare inner
JSON. Exit status 1 when there is at least one error (or, with --strict, a warning), 2 when a file cannot be read.

It automates the checklist in skills/6-workflows/references/template-json-format.md ("Validation Checklist") plus the
graph checks that file implies (reachability, cycles, port names, references). What it covers: wrapper and header
shape, unique reference keys, operation slugs and namespaces, edges and port names, loop/agent-skill block wiring,
$get / $get_variable references, value type names, the import-breaking field rules (`uenum` without allowed_values,
`array` without base_type, loop and variable ports, invoke_code value types) and the agent-skill shape.
What it does NOT cover: whether DevRev will accept the import. That is decided by the server: after importing, run
`workflows.components.validate` (skills/6-workflows/references/manage-workflows-api.md) and trust its answer over this
script's. The trigger `_filter` structure is not checked.

Rules marked error are import blockers documented in the checklist or structural impossibilities; warnings are
suspicious but not proven wrong. The `default-*`, `working-*` and `ai-agent-skill-*` example templates are the ground
truth: they must produce no errors (tests/test_workflow_validator.py).
"""
import argparse
import difflib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
DEFAULT_OPS = ROOT / "index" / "operations.json"
KEY_RE = re.compile(r"^[a-zA-Z_][a-zA-Z0-9_]*$")
VALUE_TYPES = ("literal", "jsonata_expression", "composite_value", "text_template", "list_value", "composite_value_list")
GET_RE = re.compile(r"""\$get\(\s*(['"])(.*?)\1\s*(?:,\s*(['"])(.*?)\3\s*)?\)""")
GETVAR_RE = re.compile(r"""\$get_variable\(\s*(['"])(.*?)\1""")
EXPR_RE = re.compile(r"\{%\s*expr\b")
BLOCK_SLUGS = {"for_each", "while", "ai_agent_skill"}
TRIGGER_TAIL = re.compile(r"(_created|_updated|_deleted|_trigger|_started)$")
UENUM_KEYS = ("id", "label", "ordinal", "value")
CUSTOM_PREFIXES = ("tnt__", "ctype__", "custom_")  # custom fields a template may set on update_* / create_* steps


def is_loop(slug):
    return slug.startswith("loop_over_")


def is_block(slug):
    return slug in BLOCK_SLUGS or is_loop(slug)


class Report:
    def __init__(self, source):
        self.source = source
        self.issues = []

    def add(self, severity, rule, where, message, fix=""):
        self.issues.append({"severity": severity, "rule": rule, "where": where, "message": message, "fix": fix})

    def error(self, rule, where, message, fix=""):
        self.add("error", rule, where, message, fix)

    def warn(self, rule, where, message, fix=""):
        self.add("warning", rule, where, message, fix)

    @property
    def errors(self):
        return [i for i in self.issues if i["severity"] == "error"]

    @property
    def warnings(self):
        return [i for i in self.issues if i["severity"] == "warning"]


def load_ops(path):
    try:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    return {o["slug"]: o for o in data.get("operations", [])}


# --------------------------------------------------------------------------- loading
def parse_template(text, rep):
    """Return the inner workflow dict (or None after reporting why not). Checks the wrapper on the way."""
    try:
        obj = json.loads(text)
    except ValueError as exc:
        rep.error("json", "file", f"not valid JSON: {exc}")
        return None
    if not isinstance(obj, dict):
        rep.error("json", "file", "the top level must be a JSON object")
        return None
    if "data" in obj:
        if obj.get("templateVersion") != "2.0.0":
            rep.error("wrapper", "wrapper", f"templateVersion is {obj.get('templateVersion')!r}, must be \"2.0.0\"",
                      'use {"templateVersion": "2.0.0", "data": "<stringified inner JSON>"}')
        data = obj["data"]
        if isinstance(data, dict):
            rep.error("data_not_string", "wrapper", "`data` is an object; the template file stores it as a stringified JSON string",
                      "JSON.stringify the inner workflow into `data` (the API import script parses it again)")
            return data
        if not isinstance(data, str):
            rep.error("data_not_string", "wrapper", f"`data` must be a string, found {type(data).__name__}")
            return None
        try:
            inner = json.loads(data)
        except ValueError as exc:
            rep.error("data_json", "wrapper", f"`data` does not parse as JSON: {exc}")
            return None
        if not isinstance(inner, dict):
            rep.error("data_json", "wrapper", "`data` must decode to a JSON object")
            return None
        return inner
    if "steps" in obj:
        rep.warn("bare_inner", "wrapper", "this is the bare inner workflow, not the importable wrapper",
                 'wrap it: {"templateVersion": "2.0.0", "data": "<stringified inner JSON>"}')
        return obj
    rep.error("wrapper", "wrapper", "neither a wrapper (`data`) nor an inner workflow (`steps`)")
    return None


# --------------------------------------------------------------------------- the checks
class Checker:
    def __init__(self, inner, ops, rep):
        self.inner, self.ops, self.rep = inner, ops, rep
        self.steps, self.by_key, self.third_party = [], {}, {}

    # -- helpers
    def slug(self, step):
        op = step.get("operation")
        return op.get("slug", "") if isinstance(op, dict) else ""

    def kind(self, step):
        rec = self.ops.get(self.slug(step))
        return rec["kind"] if rec else ""

    def is_trigger(self, step):
        k, s = self.kind(step), self.slug(step)
        return k == "trigger" or (not k and bool(TRIGGER_TAIL.search(s)))

    def out_ports(self, step):
        """Output port names a step may use, or None when we cannot tell (router, unknown third-party operation)."""
        slug = self.slug(step)
        rec = self.ops.get(slug)
        if slug == "router":
            return None
        if rec is None and not is_block(slug) and slug != "if_else":
            return None
        ports = {"output", "error"}
        if slug == "if_else":
            ports |= {"true", "false"}
        if is_block(slug):
            ports.add("block_start")
        if rec:
            ports |= set(rec.get("ports", {}).get("out", {}))
        return ports

    # -- run
    def run(self):
        self.header()
        if not isinstance(self.inner.get("steps"), list) or not self.inner["steps"]:
            self.rep.error("steps", "steps", "`steps` must be a non-empty list")
            return
        self.collect_steps()
        self.operations()
        self.graph()
        self.references_and_values()
        self.port_schemas()
        self.agent_skill()

    def header(self):
        r, inner = self.rep, self.inner
        sv = inner.get("serialization_version")
        if sv != {"major": 2, "minor": 0, "patch": 0}:
            r.error("serialization_version", "header", f"serialization_version is {sv!r}",
                    'must be exactly {"major": 2, "minor": 0, "patch": 0}')
        title = inner.get("title")
        if not isinstance(title, str) or not 1 <= len(title) <= 256:
            r.error("title", "header", "`title` must be a string of 1-256 characters")
        desc = inner.get("description")
        if desc is not None and (not isinstance(desc, str) or len(desc) > 65536):
            r.error("description", "header", "`description` must be a string of at most 65536 characters")
        labels = inner.get("labels")
        if labels is not None and (not isinstance(labels, list) or len(labels) > 16
                                   or any(not isinstance(x, str) or len(x) > 64 for x in labels)):
            r.error("labels", "header", "`labels` must be a list of at most 16 strings of at most 64 characters")

    def collect_steps(self):
        for i, st in enumerate(self.inner["steps"]):
            where = f"steps[{i}]"
            if not isinstance(st, dict):
                self.rep.error("step", where, "a step must be an object")
                continue
            key = st.get("reference_key")
            where = f"step '{key}'" if isinstance(key, str) and key else where
            name = st.get("name")
            if not isinstance(name, str) or not 1 <= len(name) <= 256:
                self.rep.error("step_name", where, "`name` must be a string of 1-256 characters")
            if not isinstance(key, str) or not KEY_RE.match(key):
                self.rep.error("reference_key", where, f"reference_key {key!r} must match ^[a-zA-Z_][a-zA-Z0-9_]*$")
                continue
            if key in self.by_key:
                self.rep.error("duplicate_reference_key", where, f"reference_key '{key}' is used by more than one step",
                               "reference keys must be unique within the workflow")
                continue
            self.by_key[key] = st
            self.steps.append(st)

    def operations(self):
        r = self.rep
        for st in self.steps:
            key, op = st["reference_key"], st.get("operation")
            where = f"step '{key}'"
            if not isinstance(op, dict) or not isinstance(op.get("namespace"), str) or not isinstance(op.get("slug"), str) \
                    or not op["namespace"] or not op["slug"]:
                r.error("operation", where, "`operation` must be {\"namespace\": ..., \"slug\": ...}",
                        "look the slug up with: devrev-find --operation <slug>")
                continue
            if not self.ops:
                continue
            ns, slug = op["namespace"], op["slug"]
            rec = self.ops.get(slug)
            if rec:
                if rec["namespace"] and rec["namespace"] != ns:
                    r.error("wrong_namespace", where, f"operation '{slug}' belongs to namespace '{rec['namespace']}', not '{ns}'",
                            f"use \"namespace\": \"{rec['namespace']}\"")
                continue
            if ns in ("devrev", "custom_object"):
                close = difflib.get_close_matches(slug, self.ops, n=3, cutoff=0.75)
                if close:
                    r.error("unknown_operation", where, f"operation '{slug}' is not in the operations catalog; did you mean {', '.join(close)}?",
                            "check with: devrev-find --operation <slug>")
                else:
                    r.warn("unknown_operation", where, f"operation '{slug}' is not in the operations catalog",
                           "confirm the slug in the Workflows app or with devrev-find; the catalog may lag the product")
            else:
                self.third_party.setdefault(f"{ns}/{slug}", []).append(key)
        for name, keys in sorted(self.third_party.items()):
            r.warn("third_party_operation", f"{len(keys)} step(s): {', '.join(keys[:3])}{' ...' if len(keys) > 3 else ''}",
                   f"operation '{name}' is from a third-party namespace and cannot be checked here")

    def graph(self):
        r, by_key = self.rep, self.by_key
        edges = self.edges = {k: [] for k in by_key}
        for st in self.steps:
            key, where = st["reference_key"], f"step '{st['reference_key']}'"
            ns = st.get("next_steps")
            if ns is None:
                continue
            if not isinstance(ns, list):
                r.error("next_steps", where, "`next_steps` must be a list")
                continue
            allowed = self.out_ports(st)
            for e in ns:
                if not isinstance(e, dict):
                    r.error("next_steps", where, "each next_steps entry must be an object")
                    continue
                target = e.get("next_step_reference_key")
                if target is None:
                    r.error("next_step_shape", where, f"next_steps entry has no `next_step_reference_key` (keys: {sorted(e)})",
                            "templates use next_step_reference_key; `next_step` is only for the raw workflow-steps API")
                    continue
                if target not in by_key:
                    r.error("next_step_missing", where, f"next_steps points at '{target}', which is not a step",
                            "next_step_reference_key must be the reference_key of another step")
                    continue
                port = e.get("port_name")
                if port is None:
                    r.error("port_name", where, "next_steps entry has no `port_name`")
                elif allowed is not None and port not in allowed:
                    r.error("port_name", where, f"'{self.slug(st)}' has no output port '{port}' (use one of {sorted(allowed)})",
                            "if_else: true/false; loops, while, for_each and ai_agent_skill: block_start/output; others: output")
                edges[key].append(target)
        # triggers and reachability
        triggers = [s["reference_key"] for s in self.steps if self.is_trigger(s)]
        if not triggers:
            r.error("no_trigger", "workflow", "no step is a trigger operation", "start the graph with a trigger such as ticket_created")
        seen = set(triggers)
        stack = list(triggers)
        while stack:
            for nxt in edges.get(stack.pop(), []):
                if nxt not in seen:
                    seen.add(nxt)
                    stack.append(nxt)
        if triggers:
            for st in self.steps:
                if st["reference_key"] not in seen:
                    r.warn("unreachable_step", f"step '{st['reference_key']}'", "no path from a trigger reaches this step, so it never runs",
                           "connect it with a next_steps edge or delete it")
        # cycles (a go_back step loops on purpose)
        color = {}
        for root in by_key:
            if color.get(root):
                continue
            path = [(root, iter(edges[root] if self.slug(by_key[root]) != "go_back" else []))]
            color[root] = 1
            while path:
                node, it = path[-1]
                nxt = next(it, None)
                if nxt is None:
                    color[node] = 2
                    path.pop()
                elif color.get(nxt) == 1:
                    r.error("cycle", f"step '{node}'", f"next_steps form a cycle through '{nxt}'",
                            "workflow graphs must be acyclic; use a loop operation (or go_back) to repeat work")
                    color[nxt] = 2
                elif not color.get(nxt):
                    color[nxt] = 1
                    path.append((nxt, iter(edges[nxt] if self.slug(by_key[nxt]) != "go_back" else [])))
        # block wiring
        for st in self.steps:
            key = st["reference_key"]
            parent = st.get("block_step_reference_key")
            if parent is not None:
                if parent not in by_key:
                    r.error("block_parent", f"step '{key}'", f"block_step_reference_key '{parent}' is not a step")
                elif not is_block(self.slug(by_key[parent])):
                    r.warn("block_parent", f"step '{key}'", f"block_step_reference_key points at '{parent}', which is not a loop or block step")
            if is_block(self.slug(st)):
                for e in st.get("next_steps") or []:
                    if isinstance(e, dict) and e.get("port_name") == "block_start":
                        child = by_key.get(e.get("next_step_reference_key"))
                        if child is not None and child.get("block_step_reference_key") != key:
                            r.error("block_child", f"step '{child['reference_key']}'",
                                    f"it is wired to '{key}' block_start but its block_step_reference_key is {child.get('block_step_reference_key')!r}",
                                    f"add \"block_step_reference_key\": \"{key}\"")

    def ancestors(self, key):
        rev = {k: [] for k in self.by_key}
        for a, outs in self.edges.items():
            for b in outs:
                rev[b].append(a)
        seen, stack = set(), [key]
        while stack:
            for p in rev.get(stack.pop(), []):
                if p not in seen:
                    seen.add(p)
                    stack.append(p)
        return seen

    # -- values and references
    def references_and_values(self):
        for st in self.steps:
            key, slug, where = st["reference_key"], self.slug(st), f"step '{st['reference_key']}'"
            ivs = st.get("input_values")
            if ivs is None:
                continue
            if not isinstance(ivs, list):
                self.rep.error("input_values", where, "`input_values` must be a list")
                continue
            for iv in ivs:
                if not isinstance(iv, dict):
                    self.rep.error("input_values", where, "each input_values entry must be an object")
                    continue
                port = iv.get("port_name", "input")
                fields = iv.get("fields") or []
                names = []
                for f in fields:
                    if not isinstance(f, dict) or "name" not in f:
                        self.rep.error("input_values", where, "each field needs a `name` and a `value`")
                        continue
                    names.append(f["name"])
                    self.check_value(st, f["value"] if "value" in f else None, f"{where} field '{f['name']}'", f["name"])
                    if slug == "set_variable" and f["name"] == "variable":
                        self.check_set_variable(st, f.get("value"))
                self.check_field_names(st, port, names)
            if slug == "init_variable":
                self.check_init_variable(st)

    def check_field_names(self, st, port, names):
        slug = self.slug(st)
        rec = self.ops.get(slug)
        if not rec or slug in ("for_each", "invoke_code", "manual_trigger", "ai_agent_skill_trigger", "init_variable", "set_variable"):
            return
        known = {f.split(":", 1)[0] for f in rec.get("ports", {}).get("in", {}).get(port, [])}
        if not known:
            return
        known |= set(rec.get("seen_fields", []))  # fields example templates already use (the schema docs lag the product)
        extra = {"fields_to_watch", "_filter"} if self.is_trigger(st) else set()
        if is_loop(slug):
            extra |= {"block_callback"}
        bad = [n for n in names if n not in known and n not in extra and not n.startswith(CUSTOM_PREFIXES)]
        for n in bad:
            close = difflib.get_close_matches(n, known, n=2, cutoff=0.6)
            self.rep.warn("field_name", f"step '{st['reference_key']}'",
                          f"input field '{n}' is not documented for '{slug}'" + (f" (did you mean {', '.join(close)}?)" if close else ""),
                          f"documented inputs: devrev-find --operation {slug}")

    def check_value(self, st, val, where, field):
        r, slug = self.rep, self.slug(st)
        if not isinstance(val, dict) or "type" not in val:
            r.error("value_type", where, "a value must be an object like {\"type\": \"literal\", \"value\": ...}")
            return
        vt, payload = val.get("type"), val.get("value")
        if vt not in VALUE_TYPES:
            hint = "use the string names, not integer ids" if isinstance(vt, int) else f"allowed: {', '.join(VALUE_TYPES)}"
            r.error("value_type", where, f"unknown value type {vt!r}", hint)
            return
        if slug == "invoke_code":
            if field == "code" and vt != "text_template":
                r.error("invoke_code_value", where, f"invoke_code `code` must be a text_template, found {vt}", "wrap the code as {\"type\": \"text_template\", ...}")
            if vt == "composite_value":
                r.error("invoke_code_value", where, "invoke_code items use composite_value_list, not composite_value")
        if vt == "literal":
            if isinstance(payload, str) and ("$get(" in payload or "$get_variable(" in payload or EXPR_RE.search(payload)):
                r.warn("literal_expression", where, "a literal contains an expression and will be sent as plain text",
                       "use jsonata_expression, or text_template with {% expr ... %}")
        elif vt in ("jsonata_expression", "text_template"):
            if not isinstance(payload, str):
                r.error("value_payload", where, f"{vt} needs a string `value`")
                return
            if vt == "text_template" and payload.count("{%") != payload.count("%}"):
                r.error("template_unbalanced", where, "a text_template has unbalanced {% ... %} markers")
            if vt == "jsonata_expression" and not balanced(payload):
                r.warn("expression_brackets", where, "a jsonata_expression has unbalanced brackets or quotes")
            self.check_references(st, payload, where)
        elif vt == "list_value":
            items = payload.get("items") if isinstance(payload, dict) else None
            if not isinstance(items, list):
                r.error("value_payload", where, "list_value needs {\"items\": [...]}")
                return
            for it in items:
                self.check_value(st, it, where, field)
        elif vt == "composite_value":
            if not isinstance(payload, dict) or not isinstance(payload.get("fields"), list):
                r.error("value_payload", where, "composite_value needs {\"fields\": [{name, value}, ...]}")
                return
            for sub in payload["fields"]:
                if isinstance(sub, dict) and "value" in sub:
                    self.check_value(st, sub["value"], f"{where}.{sub.get('name')}", sub.get("name"))
        elif vt == "composite_value_list":
            if not isinstance(payload, list):
                r.error("value_payload", where, "composite_value_list needs a list of {\"fields\": [...]} objects")
                return
            for entry in payload:
                for sub in (entry.get("fields") or []) if isinstance(entry, dict) else []:
                    if isinstance(sub, dict) and "value" in sub:
                        self.check_value(st, sub["value"], f"{where}.{sub.get('name')}", sub.get("name"))

    def check_references(self, st, text, where):
        r, me = self.rep, st["reference_key"]
        mine = None
        for m in GET_RE.finditer(text):
            ref, port = m.group(2), m.group(4) or "output"
            target = self.by_key.get(ref)
            if target is None:
                r.error("dangling_reference", where, f"$get('{ref}', ...) names a step that does not exist",
                        "use the reference_key of an upstream step")
                continue
            tslug = self.slug(target)
            if tslug in ("init_variable", "set_variable"):
                r.warn("use_get_variable", where, f"'{ref}' is a variable step; read variables with $get_variable",
                       "$get_variable('init_variable_1','name',{'output_port_name':'output'})")
            allowed = self.out_ports(target)
            if allowed is not None and port not in allowed:
                r.warn("reference_port", where, f"$get('{ref}', '{port}') uses a port '{tslug}' does not have (has {sorted(allowed)})")
            if ref == me:
                r.error("self_reference", where, "a step cannot read its own output")
                continue
            if mine is None:
                mine = self.ancestors(me)
            if ref not in mine:
                r.warn("reference_not_upstream", where, f"'{ref}' is not upstream of '{me}', so its output does not exist yet when this step runs")
        for m in GETVAR_RE.finditer(text):
            ref = m.group(2)
            if ref not in self.by_key:
                r.error("dangling_reference", where, f"$get_variable('{ref}', ...) names a step that does not exist")

    def check_set_variable(self, st, val):
        payload = val.get("value") if isinstance(val, dict) and val.get("type") == "literal" else None
        if isinstance(payload, dict) and "step_reference_key" in payload:
            ref = payload["step_reference_key"]
            if ref not in self.by_key:
                self.rep.error("dangling_reference", f"step '{st['reference_key']}'",
                               f"set_variable targets '{ref}', which is not a step", "use the init_variable step's reference_key")
            elif self.slug(self.by_key[ref]) not in ("init_variable",) and not is_block(self.slug(self.by_key[ref])):
                self.rep.warn("set_variable_target", f"step '{st['reference_key']}'", f"set_variable targets '{ref}', which is not an init_variable or loop step")

    def check_init_variable(self, st):
        where = f"step '{st['reference_key']}'"
        out = next((p for p in st.get("output_ports") or [] if isinstance(p, dict) and p.get("name") == "output"), None)
        sv = (out or {}).get("scope_variables")
        if not isinstance(sv, list) or not sv:
            self.rep.error("init_variable_scope", where, "init_variable's `output` port needs a non-empty `scope_variables` list",
                           "one entry per declared variable (see references/template-json-format.md, Variable Management)")
            return
        declared = set()
        for iv in st.get("input_values") or []:
            for f in (iv.get("fields") or []) if isinstance(iv, dict) else []:
                v = f.get("value") if isinstance(f, dict) else None
                if isinstance(f, dict) and f.get("name") == "variables" and isinstance(v, dict) and isinstance(v.get("value"), dict):
                    declared = {x.get("name") for x in v["value"].get("fields", []) if isinstance(x, dict)}
        scoped = {(x.get("field_descriptor") or {}).get("name") for x in sv if isinstance(x, dict)}
        if declared and declared != scoped:
            self.rep.warn("init_variable_scope", where, f"declared variables {sorted(declared)} differ from scope_variables {sorted(x for x in scoped if x)}")

    # -- port schemas
    def port_schemas(self):
        for st in self.steps:
            key, slug, where = st["reference_key"], self.slug(st), f"step '{st['reference_key']}'"
            for side in ("input_ports", "output_ports"):
                for node in walk_field_descriptors(st.get(side)):
                    ft, fname = node.get("field_type"), node.get("name") or node.get("data_name") or "?"
                    if ft == "uenum":
                        av = node.get("allowed_values")
                        if not isinstance(av, list) or not av:
                            self.rep.error("uenum_allowed_values", where, f"{side}: uenum field '{fname}' has no allowed_values",
                                           "add allowed_values as [{id, label, ordinal, value}, ...]")
                        elif any(not isinstance(x, dict) or any(k not in x for k in UENUM_KEYS) for x in av):
                            self.rep.warn("uenum_value_shape", where, f"{side}: uenum field '{fname}' allowed_values entries should be {{id, label, ordinal, value}}")
                    elif ft == "array" and not node.get("base_type"):
                        self.rep.error("array_base_type", where, f"{side}: array field '{fname}' has no base_type",
                                       "base_type is one of id, text, composite, enum, ...")
                    elif ft == "enum" and not isinstance(node.get("allowed_values"), list):
                        self.rep.warn("enum_allowed_values", where, f"{side}: enum field '{fname}' has no allowed_values")
            if is_loop(slug):
                ins = [p.get("name") for p in st.get("input_ports") or [] if isinstance(p, dict)]
                outs = {p.get("name"): p for p in st.get("output_ports") or [] if isinstance(p, dict)}
                if "block_callback" not in ins:
                    self.rep.error("loop_block_callback", where, f"{slug} has no `block_callback` input port",
                                   "copy the input_ports block from a working loop example (working-loop-variable-sample.json)")
                if outs.get("block_start", {}).get("type") != "block_start":
                    self.rep.error("loop_block_start", where, f"{slug} has no `block_start` output port with type \"block_start\"",
                                   "copy the output_ports block from a working loop example")
            if slug == "for_each":
                self.rep.warn("for_each_dynamic", where, "for_each has a dynamic schema that often fails import",
                              "prefer a loop_over_* operation for native objects: devrev-find \"loop over <objects>\"")

    # -- agent skills
    def agent_skill(self):
        r, inner = self.rep, self.inner
        slugs = [self.slug(s) for s in self.steps]
        labels = inner.get("labels") if isinstance(inner.get("labels"), list) else []
        has_skill_trigger = "ai_agent_skill_trigger" in slugs
        if "skill" in labels or has_skill_trigger:
            if "skill" not in labels:
                r.warn("skill_label", "header", "this has an ai_agent_skill_trigger but `labels` lacks \"skill\"",
                       'add "labels": ["skill"] so DevRev lists it as an agent skill')
            if not has_skill_trigger:
                r.error("skill_trigger", "workflow", "`labels` has \"skill\" but there is no ai_agent_skill_trigger step")
            if "set_ai_agent_skill_output" not in slugs and "agent_callback" not in slugs:
                r.error("skill_output", "workflow", "an agent skill must end by returning its result",
                        "add a set_ai_agent_skill_output step (or agent_callback) inside the ai_agent_skill block")
            for st in self.steps:
                if self.slug(st) != "ai_agent_skill_trigger":
                    continue
                for iv in st.get("input_values") or []:
                    names = [f.get("name") for f in (iv.get("fields") or []) if isinstance(f, dict)] if isinstance(iv, dict) else []
                    if "fields_to_watch" in names or "_filter" in names:
                        r.error("skill_trigger_filter", f"step '{st['reference_key']}'",
                                "an ai_agent_skill_trigger takes no fields_to_watch or _filter", "remove them; the trigger only declares the skill's parameters")


def walk_field_descriptors(node):
    """Every dict that has a `field_type`, anywhere inside a port definition."""
    if isinstance(node, dict):
        if "field_type" in node:
            yield node
        for v in node.values():
            yield from walk_field_descriptors(v)
    elif isinstance(node, list):
        for v in node:
            yield from walk_field_descriptors(v)


def balanced(expr):
    stack, quote = [], None
    pairs = {")": "(", "]": "[", "}": "{"}
    i = 0
    while i < len(expr):
        c = expr[i]
        if quote:
            if c == "\\":
                i += 1
            elif c == quote:
                quote = None
        elif c in "'\"`":
            quote = c
        elif c in "([{":
            stack.append(c)
        elif c in pairs:
            if not stack or stack.pop() != pairs[c]:
                return False
        i += 1
    return not stack and quote is None


# --------------------------------------------------------------------------- API
def validate_text(text, source="<template>", ops_index=None):
    """Validate template text. Returns (Report, inner workflow dict or None)."""
    rep = Report(source)
    inner = parse_template(text, rep)
    if inner is not None:
        Checker(inner, load_ops(ops_index or DEFAULT_OPS), rep).run()
        if not load_ops(ops_index or DEFAULT_OPS):
            rep.warn("no_operations_index", "workflow", "index/operations.json was not found, so operation slugs and ports were not checked",
                     "run: python3 -I scripts/build_index.py in the toolkit")
    return rep, inner


def validate_file(path, ops_index=None):
    return validate_text(Path(path).read_text(encoding="utf-8"), str(path), ops_index)[0]


def render(rep):
    lines = [f"{rep.source}: {len(rep.errors)} error(s), {len(rep.warnings)} warning(s)"]
    for i in sorted(rep.issues, key=lambda x: (x["severity"] != "error", x["where"])):
        lines.append(f"  {i['severity'].upper():7} [{i['rule']}] {i['where']}: {i['message']}")
        if i["fix"]:
            lines.append(f"          fix: {i['fix']}")
    if not rep.issues:
        lines.append("  no issues found (the server-side validate is still the authority)")
    return "\n".join(lines)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("files", nargs="+", help="template JSON file(s)")
    ap.add_argument("--json", action="store_true", help="machine-readable report")
    ap.add_argument("--strict", action="store_true", help="warnings also fail the run")
    ap.add_argument("--ops-index", default=None, help="operations index (default: <toolkit>/index/operations.json)")
    a = ap.parse_args(argv)
    reports, unreadable = [], False
    for f in a.files:
        try:
            reports.append(validate_file(f, a.ops_index))
        except OSError as exc:
            print(f"validate_template: cannot read {f}: {exc}", file=sys.stderr)
            unreadable = True
    if a.json:
        print(json.dumps([{"file": r.source, "errors": len(r.errors), "warnings": len(r.warnings), "issues": r.issues} for r in reports], indent=1))
    elif reports:
        print("\n".join(render(r) for r in reports))
    if unreadable:
        return 2
    return 1 if any(r.errors or (a.strict and r.warnings) for r in reports) else 0


if __name__ == "__main__":
    sys.exit(main())
