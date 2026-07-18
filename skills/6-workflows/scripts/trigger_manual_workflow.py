#!/usr/bin/env python3
"""Manually trigger a DevRev workflow that uses an API/manual trigger.

Calls POST https://api.devrev.ai/internal/workflows.trigger.

USAGE
-----
    export DEVREV_PAT='eyJhbGc...'
    python3 scripts/trigger_manual_workflow.py <workflow-id>

    # With a specific manual-trigger step (multiple triggers in one workflow)
    python3 scripts/trigger_manual_workflow.py <workflow-id> --step api_trigger_2

    # With a payload (key=value pairs become payload.value, JSON-typed)
    python3 scripts/trigger_manual_workflow.py <workflow-id> Name=John Phone_number=29

    # Or paste a literal JSON object as the payload
    python3 scripts/trigger_manual_workflow.py <workflow-id> --json '{"Name":"John","Phone":29}'

    # Dry-run: print what would be sent without calling the API
    python3 scripts/trigger_manual_workflow.py <workflow-id> --dry-run

EXAMPLES
--------
    # Fire the Jira sync manual workflow (replace ID with the published workflow ID)
    python3 scripts/trigger_manual_workflow.py workflow-1234

NOTES
-----
- The workflow must be PUBLISHED before it can be triggered.
- $DEVREV_PAT must be set; the script exits non-zero if it isn't.
- Payload keys are case-sensitive and must match the parameter names defined
  on the API trigger node in the workflow.
- This script fires-and-exits — to watch progress, open the run in the DevRev
  Workflows UI.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request


API_URL = "https://api.devrev.ai/internal/workflows.trigger"


def parse_kv_pairs(pairs: list[str]) -> dict:
    """Turn ['Name=John', 'Phone=29'] into {'Name': 'John', 'Phone': 29}.

    Each value is parsed as JSON if possible (so numbers, booleans, and nested
    objects/arrays Just Work) and falls back to the raw string otherwise.
    """
    result = {}
    for pair in pairs:
        if "=" not in pair:
            sys.exit(f"error: payload arg '{pair}' is not in key=value form")
        key, _, raw = pair.partition("=")
        try:
            result[key] = json.loads(raw)
        except json.JSONDecodeError:
            result[key] = raw
    return result


def build_request(workflow_id: str, step_ref: str | None, payload_value: dict) -> dict:
    body = {"id": workflow_id, "payload": {"value": payload_value}}
    if step_ref:
        body["step_reference_key"] = step_ref
    return body


def trigger(pat: str, body: dict) -> tuple[int, str]:
    req = urllib.request.Request(
        API_URL,
        data=json.dumps(body).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {pat}",
            "Accept": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return resp.status, resp.read().decode("utf-8")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8") if e.fp else str(e)


def explain_status(code: int) -> str:
    return {
        200: "OK — workflow triggered",
        201: "Created — workflow run started",
        202: "Accepted — workflow trigger queued",
        400: "Bad Request — check JSON / parameter names (case-sensitive); also returned (with "
             "'is not active' in the response body) when the workflow is still in draft and not "
             "yet published — verified live 2026-07-18, corrects an earlier assumption that this "
             "case 404s",
        401: "Unauthorized — regenerate your PAT in DevRev → Settings → Personal Access Tokens",
        403: "Forbidden — your PAT doesn't have permission to trigger this workflow",
        404: "Not Found — confirm the workflow ID is correct (a draft/unpublished workflow "
             "returns 400, not 404 — see the 400 case above)",
        429: "Rate limited — slow down and retry",
    }.get(code, f"HTTP {code}")


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description="Manually trigger a DevRev workflow.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("workflow_id", help="The published workflow ID, e.g. workflow-1234")
    parser.add_argument("payload", nargs="*", help="Optional key=value pairs sent as payload.value")
    parser.add_argument("--step", dest="step_ref", default=None,
                        help="step_reference_key when the workflow has multiple API triggers")
    parser.add_argument("--json", dest="json_payload", default=None,
                        help="Pass payload.value as a literal JSON object instead of key=value pairs")
    parser.add_argument("--dry-run", action="store_true",
                        help="Print the request body without calling the API")
    args = parser.parse_args(argv)

    if args.json_payload and args.payload:
        sys.exit("error: pass either --json or key=value pairs, not both")

    if args.json_payload:
        try:
            payload_value = json.loads(args.json_payload)
        except json.JSONDecodeError as e:
            sys.exit(f"error: --json is not valid JSON: {e}")
        if not isinstance(payload_value, dict):
            sys.exit("error: --json must be a JSON object")
    else:
        payload_value = parse_kv_pairs(args.payload)

    body = build_request(args.workflow_id, args.step_ref, payload_value)

    if args.dry_run:
        print(f"POST {API_URL}")
        print("Authorization: Bearer <DEVREV_PAT>")
        print("Content-Type: application/json")
        print()
        print(json.dumps(body, indent=2))
        return 0

    pat = os.environ.get("DEVREV_PAT")
    if not pat:
        sys.exit("error: $DEVREV_PAT is not set. Export it first:\n"
                 "  export DEVREV_PAT='eyJhbGc...'\n"
                 "Generate one in DevRev → Settings → Personal Access Tokens.")

    status, body_text = trigger(pat, body)
    print(f"HTTP {status} — {explain_status(status)}")
    if body_text:
        try:
            print(json.dumps(json.loads(body_text), indent=2))
        except json.JSONDecodeError:
            print(body_text)

    return 0 if 200 <= status < 300 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
