#!/usr/bin/env python3
"""Risk classification for DevRev API calls. Shared by `bin/devrev-find` and `hooks/devrev-safety.py`.

    read         get / list / count / export / ... — never changes anything
    write        creates or updates something
    destructive  deletes, merges, or does something this repo's live notes found irreversible

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
    r"(?:https?://[A-Za-z0-9.\-]*devrev\.ai|\$\{?DEVREV_ENDPOINT\}?)/(?:internal/)?(?:beta/)?(%s)(?=[\s'\"?#\\]|$)" % NAME
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
