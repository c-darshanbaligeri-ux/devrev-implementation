#!/usr/bin/env python3
"""Risk classification for DevRev API calls. Shared by `bin/devrev-find` and `hooks/devrev-safety.py`.

    read         get / list / count / export / ... — never changes anything
    write        creates or updates something
    destructive  deletes, merges, or does something this repo's live notes found irreversible

Some writes are also HIGH IMPACT (`impact_notes`): they change what a live automation does, for example publishing a
workflow switches it on. They stay in the write class (the hook always asks) but say so in the prompt.

The rules mirror the Safety list in the repo's notes (`skills/devrev-start/references/safety.md` once Phase C
lands): `*.delete`, `*.merge`, `objects.bulk-upgrade`, `schemas.custom.set` (a versioned create that cannot be
undone), standalone custom stages/states (permanent once created), `web-crawler-jobs.control`, and any update that
sets `deprecated` / `is_deprecated` to true. Anything unrecognised is `write` (so it prompts), never `read`.

Standard library only. Importable (`import devrev_risk`) and runnable (`python3 devrev_risk.py works.delete`).
"""
import json
import re
import shlex
import sys

READ_SUFFIXES = {"get", "list", "count", "export", "locate", "download", "self", "info", "query", "aggregate"}
READ_NAMES = {
    "ping",
    "search.core", "search.hybrid",
    "tables.query.execute",  # the SQL query tool: a query engine, not a mutation endpoint
    "workflows.components.validate",  # the Workflows app's Validate button: checks a draft, changes nothing
}
HIGH_IMPACT = {
    "workflows.update-status": "switches a workflow on (status active) or off; a new workflow goes live",
    "workflow-versions.publish": "publishes a new version of an already-live workflow",
}
DESTRUCTIVE_SUFFIXES = {"delete", "merge", "revoke", "purge"}
DESTRUCTIVE_NAMES = {
    "objects.bulk-upgrade",       # affects every record of a type, org-wide
    "schemas.custom.set",         # versioned create; no schemas.custom.delete exists
    "stages.custom.create",       # permanent once created
    "states.custom.create",       # permanent once created
    "web-crawler-jobs.control",   # stop / reset actions
}
NAME = r"[a-z][a-z0-9-]*(?:\.[a-z0-9-]+)+|ping"
# A DevRev API URL: a real host, or the $DEVREV_ENDPOINT variable the skills use, then an optional /internal/.
URL_RE = re.compile(
    # host must be devrev.ai or a subdomain of it (api.devrev.ai); lookalikes such as evildevrev.ai or
    # api.devrev.ai.evil.com do not match
    r"(?:https?://(?:[A-Za-z0-9\-]+\.)*devrev\.ai|\$\{?DEVREV_ENDPOINT\}?)/(?:internal/)?(?:beta/)?(%s)(?=[\s'\"?#\\]|$)" % NAME
)


def normalize(name: str) -> str:
    n = name.strip().lower().lstrip("/")
    for prefix in ("internal/", "beta/"):
        if n.startswith(prefix):
            n = n[len(prefix):]
    return n


def classify(name: str, body=None) -> str:
    """Return 'read', 'write' or 'destructive' for an endpoint name (and optionally its JSON body)."""
    n = normalize(name)
    last = n.rsplit(".", 1)[-1]
    if n in DESTRUCTIVE_NAMES or last in DESTRUCTIVE_SUFFIXES:
        return "destructive"
    if isinstance(body, dict) and (body.get("deprecated") is True or body.get("is_deprecated") is True):
        return "destructive"
    if n in READ_NAMES or last in READ_SUFFIXES:
        return "read"
    return "write"


def impact_notes(command: str):
    """Why a command is HIGH IMPACT (empty list when it is not): publishing routes, and import that replaces a draft."""
    notes = []
    for name in endpoints_in_command(command):
        if name in HIGH_IMPACT:
            notes.append(f"{name} {HIGH_IMPACT[name]}")
    if "workflows.templates.instantiate" in endpoints_in_command(command):
        if any(b.get("override_draft") is True for b in json_bodies(command)):
            notes.append("workflows.templates.instantiate with override_draft replaces the workflow's existing draft")
    return notes


def endpoints_in_command(command: str):
    """Endpoint names a shell command calls (in order, de-duplicated). Empty if it calls none."""
    seen, out = set(), []
    for m in URL_RE.finditer(command):
        n = normalize(m.group(1))
        if n not in seen:
            seen.add(n)
            out.append(n)
    return out


def json_bodies(command: str):
    """JSON objects passed with -d / --data / --data-raw / --data-binary (best effort; ignores non-JSON)."""
    try:
        tokens = shlex.split(command, posix=True)
    except ValueError:
        return []
    bodies = []
    for i, tok in enumerate(tokens[:-1]):
        if tok in ("-d", "--data", "--data-raw", "--data-binary", "--json"):
            try:
                val = json.loads(tokens[i + 1])
            except ValueError:
                continue
            if isinstance(val, dict):
                bodies.append(val)
    return bodies


def classify_command(command: str):
    """Overall verdict for a shell command: (risk or None, [(endpoint, risk), ...]).

    None means the command calls no DevRev API endpoint we can identify (so no opinion). If it calls several, the
    most severe risk wins (destructive > write > read). A body that sets `deprecated: true` raises that call to
    destructive.
    """
    names = endpoints_in_command(command)
    if not names:
        return None, []
    bodies = json_bodies(command)
    body = {}
    for b in bodies:
        body.update({k: v for k, v in b.items() if k in ("deprecated", "is_deprecated")})
    per = [(n, classify(n, body or None)) for n in names]
    order = {"read": 0, "write": 1, "destructive": 2}
    return max((r for _, r in per), key=order.__getitem__), per


if __name__ == "__main__":
    for arg in sys.argv[1:]:
        print(f"{arg}: {classify(arg)}")
