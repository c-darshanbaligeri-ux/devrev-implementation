#!/usr/bin/env python3
"""Import a workflow template into a DevRev org through the API, validate it, and (only when asked) publish it.

    devrev-import-workflow templates/my-workflow.json                       # draft + server-side validate, then STOP
    devrev-import-workflow templates/my-workflow.json --publish             # ... and switch it on / publish it
    devrev-import-workflow new-version.json --version-of workflow-35        # new draft version of an existing workflow
    devrev-import-workflow new-version.json --version-of workflow-35 --override-draft --publish
    devrev-import-workflow t.json --attach-connection "My PAT"              # attach a connection to the Code step
    devrev-import-workflow t.json --dry-run [--json]                        # print every request, send nothing

The flow (all routes live under /internal/, documented in references/manage-workflows-api.md, "Process: importing a
template via the API"): local validator (refuses on errors) -> who/which org (dev-users.self, dev-orgs.self) ->
instantiate (creates a DRAFT) -> find the draft version -> optional keyring attach -> workflows.components.validate
(the Workflows app's Validate button) -> stop. With --publish it then picks the publish route from the workflow's LIVE
state: a draft workflow is switched on with workflows.update-status; an already-active one gets
workflow-versions.publish. It polls workflows.get until the status is active and fails loudly on a timeout.

Safety: nothing is written until the local validator passes; the org and user are printed before the first write;
publishing needs the explicit --publish flag; an existing draft is never overwritten without --override-draft; there
are no interactive prompts (Claude Code's safety hook asks the user to approve every non-dry-run invocation). The token
(DEVREV_PAT, else DEVREV_TOKEN, else the same names in ./.env) is sent only to https://*.devrev.ai (or 127.0.0.1 for
tests) as the bare `Authorization` value, the form the live-tested flow uses, and is never printed.

Exit codes: 0 done | 1 local validation errors | 2 usage, auth or configuration | 3 refused by a safety rule
(existing draft, unknown workflow, inactive workflow) | 4 API error | 5 server-side validation failed | 7 poll timeout.

Response field names are read tolerantly (this script was written from a live run's request bodies and DevRev's own
workflow-skill; it has been exercised against a fake server only). The first real run should use a throwaway template
and stop at the validated draft.
"""
import argparse
import json
import os
import re
import sys
import time
from pathlib import Path
from urllib import error as url_error
from urllib import parse, request

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import validate_template  # noqa: E402

DEFAULT_BASE = "https://api.devrev.ai"
HOST_OK = re.compile(r"^(?:[A-Za-z0-9-]+\.)*devrev\.ai$")
EXIT_LOCAL, EXIT_USAGE, EXIT_REFUSED, EXIT_API, EXIT_INVALID, EXIT_TIMEOUT = 1, 2, 3, 4, 5, 7


class Stop(Exception):
    def __init__(self, code, message):
        super().__init__(message)
        self.code, self.message = code, message


# --------------------------------------------------------------------------- environment
def read_env_file(path):
    out = {}
    try:
        for line in Path(path).read_text(encoding="utf-8").splitlines():
            m = re.match(r"^\s*(?:export\s+)?(DEVREV_PAT|DEVREV_TOKEN|DEVREV_ENDPOINT)\s*=\s*(.*?)\s*$", line)
            if m:
                out[m.group(1)] = m.group(2).strip("'\"")
    except OSError:
        pass
    return out


def get_token():
    env_file = read_env_file(Path.cwd() / ".env")
    for name in ("DEVREV_PAT", "DEVREV_TOKEN"):
        v = os.environ.get(name) or env_file.get(name)
        if v:
            return v
    raise Stop(EXIT_USAGE, "no token: set DEVREV_PAT (DevRev > Settings > Account > Personal Access Token) in the environment or in ./.env")


def get_base(arg):
    base = (arg or os.environ.get("DEVREV_ENDPOINT") or read_env_file(Path.cwd() / ".env").get("DEVREV_ENDPOINT") or DEFAULT_BASE).rstrip("/")
    u = parse.urlparse(base)
    local = u.scheme == "http" and u.hostname in ("127.0.0.1", "localhost")
    if not (local or (u.scheme == "https" and u.hostname and HOST_OK.match(u.hostname))):
        raise Stop(EXIT_USAGE, f"refusing to send a token to {base!r}: the base URL must be https://<something>.devrev.ai")
    return base


# --------------------------------------------------------------------------- HTTP
class Client:
    def __init__(self, base, token, say):
        self.base, self.token, self.say = base, token, say

    def call(self, method, name, body=None, params=None, internal=True):
        path = ("/internal/" if internal else "/") + name
        url = self.base + path + ("?" + parse.urlencode(params) if params else "")
        data = json.dumps(body if body is not None else {}).encode() if method == "POST" else None
        req = request.Request(url, data=data, method=method, headers={"Authorization": self.token, "Content-Type": "application/json"})
        try:
            with request.urlopen(req, timeout=60) as resp:
                raw = resp.read().decode("utf-8", "replace")
        except url_error.HTTPError as exc:
            raw = exc.read().decode("utf-8", "replace")
            raise Stop(EXIT_API, f"{method} {path} failed: HTTP {exc.code}\n{raw[:2000]}")
        except (url_error.URLError, TimeoutError, OSError) as exc:
            raise Stop(EXIT_API, f"{method} {path} failed: {getattr(exc, 'reason', exc)}")
        if not raw.strip():
            return {}
        try:
            return json.loads(raw)
        except ValueError:
            raise Stop(EXIT_API, f"{method} {path} returned something that is not JSON: {raw[:300]}")


def first(d, *keys):
    for k in keys:
        if isinstance(d, dict) and d.get(k) not in (None, ""):
            return d[k]
    return None


def find_list(resp, *keys):
    for k in keys:
        if isinstance(resp.get(k), list):
            return resp[k]
    return next((v for v in resp.values() if isinstance(v, list)), []) if isinstance(resp, dict) else []


def wf_status(obj):
    s = str(first(obj if isinstance(obj, dict) else {}, "status", "state") or "").lower()
    if "draft" in s:
        return "draft"
    if "inactive" in s or "disabled" in s:
        return "inactive"
    if "active" in s:
        return "active"
    return s or "unknown"


def ver_is_draft(v):
    return "draft" in str(first(v, "status", "state") or "").lower()


def person(obj, *keys):
    return first(obj, "display_name", "full_name", "name", "email", "id") if isinstance(obj, dict) else None


# --------------------------------------------------------------------------- the steps
class Importer:
    def __init__(self, client, say, args):
        self.c, self.say, self.a = client, say, args

    def whoami(self):
        user = self.c.call("POST", "dev-users.self", {}, internal=False)
        org = self.c.call("POST", "dev-orgs.self", {})
        u = person(first(user, "dev_user", "user") or user)
        o = first(org, "dev_org", "org") or org
        self.say(f"Target org: {person(o)}  ({first(o, 'id') or 'id unknown'})   acting as: {u}")
        return {"org": person(o), "org_id": first(o, "id"), "user": u}

    def resolve_workflow(self, ref):
        if ref.startswith("don:"):
            return ref
        m = re.fullmatch(r"(?:workflow-)?(\d+)", ref.strip(), re.I)
        if not m:
            raise Stop(EXIT_USAGE, f"--version-of {ref!r}: use a full workflow DON, workflow-N or N")
        n, cursor = m.group(1), None
        for _ in range(20):
            resp = self.c.call("POST", "workflows.list", {"limit": 100, **({"cursor": cursor} if cursor else {})})
            for w in find_list(resp, "workflows"):
                if str(first(w, "display_id", "")).lower() == f"workflow-{n}" or str(first(w, "id") or "").endswith(f":workflow/{n}"):
                    return first(w, "id")
            cursor = resp.get("next_cursor")
            if not cursor:
                break
        raise Stop(EXIT_REFUSED, f"workflow-{n} was not found in workflows.list; pass its full DON with --version-of")

    def get_workflow(self, don):
        resp = self.c.call("GET", "workflows.get", params={"id": don})
        return first(resp, "workflow") or resp

    def versions(self, don):
        resp = self.c.call("GET", "workflow-versions.list", params={"workflow": don})
        return find_list(resp, "workflow_versions", "versions")

    def run(self, inner, template_version):
        a, out = self.a, {}
        out.update(self.whoami())
        existing = None
        if a.version_of:
            don = self.resolve_workflow(a.version_of)
            existing = self.get_workflow(don)
            out["workflow"], out["workflow_status_before"] = don, wf_status(existing)
            self.say(f"Existing workflow {don}: status {out['workflow_status_before']}")
            drafts = [v for v in self.versions(don) if ver_is_draft(v)]
            if drafts and not a.override_draft:
                raise Stop(EXIT_REFUSED, "this workflow already has a draft version (" + ", ".join(str(first(v, "id")) for v in drafts)
                           + "). Importing would replace it. Review it, then re-run with --override-draft if replacing is intended.")
            if drafts:
                self.say("WARNING: --override-draft replaces the existing draft " + ", ".join(str(first(v, "id")) for v in drafts))
        body = {"template_version": template_version, "workflow_template_v2": inner}
        if a.version_of:
            body.update({"workflow": out["workflow"], "override_draft": True})
        resp = self.c.call("POST", "workflows.templates.instantiate", body)
        wf = first(resp, "workflow") or resp
        don = first(wf, "id") or out.get("workflow")
        if not don:
            raise Stop(EXIT_API, "instantiate returned no workflow id: " + json.dumps(resp)[:500])
        out["workflow"], out["display_id"] = don, first(wf, "display_id")
        self.say(f"Created draft workflow {out.get('display_id') or ''} {don}")
        drafts = [v for v in self.versions(don) if ver_is_draft(v)]
        if not drafts:
            raise Stop(EXIT_API, f"no draft version found for {don} after import (workflow-versions.list)")
        ver = first(drafts[-1], "id")
        out["version"] = ver
        self.say(f"Draft version {ver}")
        if a.attach_connection:
            out["attached"] = self.attach(inner, ver)
        v = self.c.call("POST", "workflows.components.validate",
                        {"components": [{"type": "workflow", "workflow_version_id": ver}]})
        errors, warnings = v.get("errors") or [], v.get("warnings") or []
        out["validation"] = {"valid": bool(v.get("valid")) and not errors, "errors": errors, "warnings": warnings}
        for w in warnings:
            self.say("  validate warning: " + json.dumps(w))
        if not out["validation"]["valid"]:
            for e in errors:
                self.say("  validate ERROR: " + json.dumps(e))
            stop = Stop(EXIT_INVALID, f"server-side validation failed for {ver}; the draft is in the org. Fix the template and re-import "
                        f"with --version-of {out.get('display_id') or don} --override-draft, or delete the draft workflow.")
            stop.result = out
            raise stop
        self.say("Server-side validate: valid")
        out["published"], out["status"] = False, "draft"
        if not a.publish:
            self.say("Stopped at the validated draft. Re-run with --publish (after the user agrees) to put it live.")
            return out
        return self.publish(out, ver)

    def attach(self, inner, ver):
        a = self.a
        code_keys = [s["reference_key"] for s in inner.get("steps", []) if (s.get("operation") or {}).get("slug") == "invoke_code"]
        wanted = a.step or code_keys
        if not wanted:
            raise Stop(EXIT_USAGE, "--attach-connection: the template has no invoke_code step (use --step <reference_key> to name one)")
        if len(code_keys) > 1 and not a.step:
            raise Stop(EXIT_USAGE, f"--attach-connection: several invoke_code steps ({', '.join(code_keys)}); name them with --step")
        rings = find_list(self.c.call("POST", "keyrings.list", {}), "keyrings")
        want = a.attach_connection.strip().lower().replace(" ", "_")
        match = [k for k in rings if str(first(k, "name", "display_name") or "").strip().lower().replace(" ", "_") == want]
        if not match:
            names = ", ".join(str(first(k, "name", "display_name")) for k in rings) or "none"
            raise Stop(EXIT_REFUSED, f"no connection named {a.attach_connection!r}; available: {names}")
        if len(match) > 1:
            raise Stop(EXIT_REFUSED, f"{len(match)} connections are named {a.attach_connection!r}; rename one so the choice is unambiguous")
        keyring_id = first(match[0], "id")
        steps = find_list(self.c.call("GET", "workflow-steps.list", params={"workflow_version": ver}), "workflow_steps", "steps")
        done = []
        for key in wanted:
            hits = [s for s in steps if first(s, "reference_key") == key]
            if len(hits) != 1:
                raise Stop(EXIT_REFUSED, f"--attach-connection: expected exactly one step with reference_key {key!r} in {ver}, found {len(hits)}")
            self.c.call("POST", "workflow-steps.update", {"id": first(hits[0], "id"), "keyrings": [{"name": want, "reference": keyring_id}]})
            done.append(key)
            self.say(f"Attached connection '{want}' to step {key}")
        return done

    def publish(self, out, ver):
        a = self.a
        don = out["workflow"]
        live = wf_status(self.get_workflow(don))  # decide from live state, not from flags
        out["workflow_status_before_publish"] = live
        if live == "draft":
            self.say(f"Workflow is a draft: publishing with workflows.update-status (status active) -- this switches {don} ON")
            self.c.call("POST", "workflows.update-status", {"id": don, "status": "active"})
            final = self.poll(lambda: wf_status(self.get_workflow(don)), lambda s: s == "active", f"{don} to become active")
        elif live == "active":
            self.say("Workflow is already active: publishing the new version with workflow-versions.publish")
            self.c.call("POST", "workflow-versions.publish", {"id": ver, "notes": a.notes})
            final = self.poll(lambda: "draft" if any(ver_is_draft(v) and first(v, "id") == ver for v in self.versions(don)) else "published",
                              lambda s: s != "draft", f"version {ver} to leave draft")
        else:
            raise Stop(EXIT_REFUSED, f"workflow {don} is {live}; not publishing into a workflow that is switched off. "
                       "Turn it on deliberately with workflows.update-status if that is intended.")
        out["published"], out["status"] = True, final
        self.say(f"Published. Status: {final}")
        return out

    def poll(self, fn, done, what):
        deadline, last = time.monotonic() + self.a.poll_timeout, None
        while True:
            last = fn()
            if done(last):
                return last
            if time.monotonic() >= deadline:
                raise Stop(EXIT_TIMEOUT, f"timed out after {self.a.poll_timeout:g}s waiting for {what}; last status: {last}")
            time.sleep(self.a.poll_interval)


# --------------------------------------------------------------------------- dry run
def dry_run_plan(args, inner, template_version, base):
    body = {"template_version": template_version, "workflow_template_v2": inner}
    steps = [("POST", "/dev-users.self", {}), ("POST", "/internal/dev-orgs.self", {})]
    if args.version_of:
        wf = args.version_of if args.version_of.startswith("don:") else "<resolved from workflows.list>"
        if not args.version_of.startswith("don:"):
            steps.append(("POST", "/internal/workflows.list", {"limit": 100}))
        steps += [("GET", f"/internal/workflows.get?id={wf}", None), ("GET", f"/internal/workflow-versions.list?workflow={wf}", None)]
        body.update({"workflow": wf, "override_draft": True})
    steps.append(("POST", "/internal/workflows.templates.instantiate", body))
    steps.append(("GET", "/internal/workflow-versions.list?workflow=<new workflow DON>", None))
    if args.attach_connection:
        steps += [("POST", "/internal/keyrings.list", {}), ("GET", "/internal/workflow-steps.list?workflow_version=<draft version DON>", None),
                  ("POST", "/internal/workflow-steps.update", {"id": "<step DON>", "keyrings": [{"name": args.attach_connection.strip().lower().replace(" ", "_"), "reference": "<keyring id>"}]})]
    steps.append(("POST", "/internal/workflows.components.validate",
                  {"components": [{"type": "workflow", "workflow_version_id": "<draft version DON>"}]}))
    if args.publish:
        steps.append(("GET", "/internal/workflows.get?id=<workflow DON>", None))
        steps.append(("POST", "/internal/workflows.update-status", {"id": "<workflow DON>", "status": "active"}))
        steps.append(("POST", "/internal/workflow-versions.publish", {"id": "<draft version DON>", "notes": args.notes}))
        steps.append(("GET", "/internal/workflows.get?id=<workflow DON> (poll until active)", None))
    return [{"method": m, "url": base + p, "body": b} for m, p, b in steps], \
        "(the publish step is chosen at run time from the workflow's live status: a draft gets update-status, an active workflow gets versions.publish)" if args.publish else ""


def short_body(body, full):
    if full or not isinstance(body, dict) or "workflow_template_v2" not in body:
        return body
    t = body["workflow_template_v2"]
    return {**body, "workflow_template_v2": f"<parsed template object: {t.get('title')!r}, {len(t.get('steps', []))} steps; use --json to print it>"}


# --------------------------------------------------------------------------- main
def main(argv=None):
    # allow_abbrev=False: the safety hook matches the exact flag names, so `--pub` must not silently mean `--publish`
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter, allow_abbrev=False)
    ap.add_argument("template", help="template JSON file (the importable wrapper)")
    ap.add_argument("--version-of", metavar="WORKFLOW", help="import as a new version of this workflow (full DON, workflow-N or N)")
    ap.add_argument("--override-draft", action="store_true", help="allow replacing an existing draft of --version-of")
    ap.add_argument("--publish", action="store_true", help="after validation, publish / switch on (the user must have agreed)")
    ap.add_argument("--notes", default="Published by devrev-import-workflow", help="release notes for workflow-versions.publish")
    ap.add_argument("--attach-connection", metavar="NAME", help="attach this connection (keyring) to the invoke_code step")
    ap.add_argument("--step", action="append", metavar="REF_KEY", help="reference_key of the step for --attach-connection (repeatable)")
    ap.add_argument("--dry-run", action="store_true", help="validate locally and print every request; send nothing")
    ap.add_argument("--json", action="store_true", help="print one JSON result on stdout (progress goes to stderr)")
    ap.add_argument("--base-url", default=None, help="API base URL (default $DEVREV_ENDPOINT or https://api.devrev.ai; devrev.ai hosts only)")
    ap.add_argument("--poll-timeout", type=float, default=60.0, help="seconds to wait for the workflow to become active (default 60)")
    ap.add_argument("--poll-interval", type=float, default=2.0)
    a = ap.parse_args(argv)
    say = (lambda m: print(m, file=sys.stderr)) if a.json else print
    result = {}
    try:
        if a.override_draft and not a.version_of:
            raise Stop(EXIT_USAGE, "--override-draft only makes sense with --version-of")
        try:
            text = Path(a.template).read_text(encoding="utf-8")
        except OSError as exc:
            raise Stop(EXIT_USAGE, f"cannot read {a.template}: {exc}")
        report, inner = validate_template.validate_text(text, a.template)
        say(validate_template.render(report))
        if report.errors or inner is None:
            raise Stop(EXIT_LOCAL, "the local validator found errors; fix them before importing (nothing was sent)")
        obj = json.loads(text)
        template_version = obj.get("templateVersion", "2.0.0") if isinstance(obj, dict) and "data" in obj else "2.0.0"
        base = get_base(a.base_url)
        if a.dry_run:
            plan, note = dry_run_plan(a, inner, template_version, base)
            if a.json:
                print(json.dumps({"dry_run": True, "requests": plan, "note": note}, indent=1))
            else:
                print("DRY RUN: nothing is sent. Requests in order:")
                for i, r in enumerate(plan, 1):
                    print(f" {i}. {r['method']} {r['url']}" + (f"\n    body: {json.dumps(short_body(r['body'], False))}" if r["body"] else ""))
                if note:
                    print(note)
            return 0
        result = Importer(Client(base, get_token(), say), say, a).run(inner, template_version)
    except Stop as stop:
        print(f"devrev-import-workflow: {stop.message}", file=sys.stderr)
        if a.json and getattr(stop, "result", None):
            print(json.dumps(stop.result, indent=1))
        return stop.code
    if a.json:
        print(json.dumps(result, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
