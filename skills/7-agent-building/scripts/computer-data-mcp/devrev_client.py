#!/usr/bin/env python3
"""
Single transport for every DevRev call this skill makes.

Nothing else in this skill opens a socket. One place to resolve the token, one
place to set headers, one place that knows about rate limits and retries — so a
transport bug is fixed once and a token can never leak from an unreviewed code
path.

WHAT IT KNOWS THAT MATTERS
--------------------------
* Auth header form. `/internal/` endpoints in this org take a BARE
  `Authorization: <token>` header — no `Bearer` prefix. The public root accepts
  both. This client sends the bare form and, on a 401 only, retries once with
  `Bearer` before giving up, because the two conventions are genuinely mixed
  across DevRev surfaces and a hard failure on the wrong guess is a bad
  experience for something this easy to handle.
* Token leakage. Every request is built with urllib, never a shell. That is a
  deliberate choice: a `subprocess.run(..., check=True)` whose argv contains
  `-H "Authorization: ..."` puts the entire PAT into the CalledProcessError
  traceback. This client cannot do that. If a curl fallback is ever added here,
  it must use check=False and must never include r.args or r.stderr in a raised
  message.
* Rate limits. Pacing is read from the live `X-Ratelimit-Remaining` /
  `X-Ratelimit-Limit` headers on every response, never from a hardcoded quota —
  observed limits differ from the published ones by more than an order of
  magnitude and differ per org. On a 429 the `Retry-After` header (or the body's
  `retry_after`) is the only cadence honoured. Five consecutive 429s trip a
  circuit breaker rather than continuing to hammer.
* Error bodies. DevRev's `message` is generic ("Bad Request"); the actionable
  text is in `debug_message`. Errors raised here always surface `debug_message`
  first. 429 bodies use a different, RFC-7807-ish shape where `type` is a URI,
  so no code here branches on `type` being a known enum token.
* Retry classification. 429/503/504 and network errors are retried with capped
  exponential backoff. 400/401/403/404/422 are not — they are deterministic and
  retrying only wastes quota. A bare 500 is NOT retried either: on this API a
  500 has repeatedly meant a malformed request the server failed to validate
  rather than a transient fault, so retrying hides a bug that needs fixing.

TOKEN RESOLUTION
----------------
First hit wins:
    1. env DEVREV_PAT, DEVREV_API_KEY, DEVREV_TOKEN, ORG_PAT   (in that order)
    2. a `.env` file at the skill root (the parent of scripts/), same key order

Note DEVREV_PAT comes first and ORG_PAT last. `tables.query.execute` is served
from `/internal/` but works with an ordinary personal access token — which is
the entire point of this skill. The agent that owns the dashboards runs as a
service account with no data access; the human running this skill has their own
PAT and their own row-level access. Using the user's PAT is what makes the
numbers appear at all, and it means the results respect that user's permissions
rather than escalating past them.

Base URL is `DEVREV_BASE_URL` or `https://api.devrev.ai`.

USE AS A LIBRARY
----------------
    from devrev_client import api, sql, load_token
    resp = api("dashboards.get", {"id": don})       # /internal/ by default
    rows = sql("SELECT COUNT(1) AS n FROM <table> AS x")

USE AS A CLI (handy for probing)
--------------------------------
    python3 devrev_client.py --check                       # verify the token
    python3 devrev_client.py --endpoint dashboards.get --data '{"id":"don:..."}'
    python3 devrev_client.py --sql "SELECT 1 AS n"

Python 3.9+, standard library only.
"""
from __future__ import annotations

import argparse
import base64
import json
import os
import random
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

BASE_URL = os.environ.get("DEVREV_BASE_URL", "https://api.devrev.ai")
SKILL_ROOT = Path(__file__).resolve().parent   # .env sits beside this file here

TOKEN_KEYS = ("DEVREV_PAT", "DEVREV_API_KEY", "DEVREV_TOKEN", "ORG_PAT")

# Quota remaining -> delay before the next call. Pace off live headers, never a
# hardcoded quota figure.
PACING_TABLE = ((0.80, 0.01), (0.50, 0.05), (0.20, 0.20), (0.10, 0.50))
SLOW_DELAY = 1.0

MAX_ATTEMPTS = 4
MAX_BACKOFF = 60.0
MAX_CONSECUTIVE_RATE_LIMITS = 5
CIRCUIT_COOLDOWN = 300.0

RETRY_STATUS = (429, 503, 504)
NO_RETRY_STATUS = (400, 401, 403, 404, 409, 422, 500)

# Result-set cap on tables.query.execute. The API applies it silently: no error,
# no cursor. Any row count exactly equal to this is presumed truncated.
ROW_CAP = 1000

_state = {"delay": 0.01, "consecutive_429": 0, "circuit_open_until": 0.0}


class DevRevError(RuntimeError):
    """An API call that failed in a way retrying will not fix."""

    def __init__(self, status, body, endpoint):
        self.status = status
        self.endpoint = endpoint
        self.body = body
        detail = ""
        if isinstance(body, dict):
            detail = body.get("debug_message") or body.get("detail") or body.get("message") or ""
            if body.get("field_name"):
                detail = "%s (field: %s)" % (detail, body["field_name"])
        elif isinstance(body, str):
            detail = body[:400]
        super().__init__("%s -> HTTP %s: %s" % (endpoint, status, detail or "no detail"))


# ---------------------------------------------------------------------------
# Token
# ---------------------------------------------------------------------------

def load_token():
    """Return a PAT. Never logs or returns it as part of an error message."""
    for key in TOKEN_KEYS:
        val = (os.environ.get(key) or "").strip()
        if val:
            return val
    envfile = SKILL_ROOT / ".env"
    if envfile.exists():
        try:
            lines = envfile.read_text().splitlines()
        except OSError:
            lines = []
        for key in TOKEN_KEYS:
            for line in lines:
                line = line.strip()
                if line.startswith(key + "="):
                    val = line.split("=", 1)[1].strip().strip('"').strip("'")
                    if val:
                        return val
    raise SystemExit(
        "No DevRev token found.\n"
        "  Set one of: %s\n"
        "  or put it in %s\n"
        "This skill runs on YOUR personal access token so queries respect your\n"
        "own data access. Create one in DevRev under Settings -> Personal Access Tokens."
        % (", ".join(TOKEN_KEYS), envfile)
    )


# ---------------------------------------------------------------------------
# Pacing
# ---------------------------------------------------------------------------

def _update_pacing(headers):
    try:
        limit = float(headers.get("X-Ratelimit-Limit") or 0)
        remaining = float(headers.get("X-Ratelimit-Remaining") or 0)
    except (TypeError, ValueError):
        return
    if limit <= 0:
        return
    frac = remaining / limit
    delay = SLOW_DELAY
    for threshold, value in PACING_TABLE:
        if frac > threshold:
            delay = value
            break
    _state["delay"] = delay


def _retry_after(headers, body, attempt):
    for src in (body.get("retry_after") if isinstance(body, dict) else None,
                headers.get("Retry-After")):
        try:
            wait = float(src)
            if wait >= 0:
                return min(wait, MAX_BACKOFF)
        except (TypeError, ValueError):
            continue
    # Full jitter, so parallel callers do not resynchronise on the same instant.
    return min(MAX_BACKOFF, (2 ** attempt)) * (0.5 + random.random() / 2.0)


def _check_circuit():
    open_until = _state["circuit_open_until"]
    if open_until and time.time() < open_until:
        raise DevRevError(
            429,
            {"debug_message": "Circuit breaker open after %d consecutive rate limits; "
                              "retry in %d s. Reduce query volume."
                              % (MAX_CONSECUTIVE_RATE_LIMITS, int(open_until - time.time()))},
            "circuit-breaker",
        )
    if open_until:
        _state["circuit_open_until"] = 0.0
        _state["consecutive_429"] = 0


# ---------------------------------------------------------------------------
# Core request
# ---------------------------------------------------------------------------

def api(endpoint, payload=None, internal=True, token=None, timeout=120):
    """POST to a DevRev endpoint and return the decoded JSON body.

    Raises DevRevError for non-retryable failures and after exhausting retries.
    """
    _check_circuit()
    tok = token or load_token()
    url = "%s/%s%s" % (BASE_URL.rstrip("/"), "internal/" if internal else "", endpoint.lstrip("/"))
    body_bytes = json.dumps(payload if payload is not None else {}).encode()

    auth_forms = [tok, "Bearer " + tok] if not tok.lower().startswith("bearer ") else [tok]
    last = None

    for attempt in range(MAX_ATTEMPTS):
        if _state["delay"]:
            time.sleep(_state["delay"])
        for auth in auth_forms:
            req = urllib.request.Request(url, data=body_bytes, method="POST", headers={
                "Authorization": auth,
                "Content-Type": "application/json",
                "Accept": "application/json",
            })
            try:
                with urllib.request.urlopen(req, timeout=timeout) as resp:
                    _update_pacing(resp.headers)
                    _state["consecutive_429"] = 0
                    raw = resp.read()
                    return json.loads(raw) if raw else {}
            except urllib.error.HTTPError as exc:
                raw = b""
                try:
                    raw = exc.read()
                except Exception:
                    pass
                try:
                    parsed = json.loads(raw)
                except Exception:
                    parsed = raw.decode(errors="replace") if raw else ""
                _update_pacing(exc.headers or {})

                # A 401 on the bare header may just be the other convention.
                if exc.code == 401 and auth is auth_forms[0] and len(auth_forms) > 1:
                    continue

                if exc.code == 429:
                    _state["consecutive_429"] += 1
                    if _state["consecutive_429"] >= MAX_CONSECUTIVE_RATE_LIMITS:
                        _state["circuit_open_until"] = time.time() + CIRCUIT_COOLDOWN
                        raise DevRevError(429, {"debug_message":
                            "%d consecutive rate limits; pausing %d s."
                            % (_state["consecutive_429"], int(CIRCUIT_COOLDOWN))}, endpoint)

                if exc.code in NO_RETRY_STATUS:
                    raise DevRevError(exc.code, parsed, endpoint)
                last = DevRevError(exc.code, parsed, endpoint)
                if exc.code in RETRY_STATUS and attempt < MAX_ATTEMPTS - 1:
                    time.sleep(_retry_after(exc.headers or {}, parsed, attempt))
                break
            except (urllib.error.URLError, TimeoutError, OSError) as exc:
                # Deliberately does not include the request object, which holds
                # the Authorization header.
                last = DevRevError(0, {"debug_message": "network error: %s" % exc.__class__.__name__},
                                   endpoint)
                if attempt < MAX_ATTEMPTS - 1:
                    time.sleep(min(MAX_BACKOFF, 2 ** attempt))
                break
        else:
            continue
    raise last or DevRevError(0, {"debug_message": "request failed with no response"}, endpoint)


# ---------------------------------------------------------------------------
# SQL
# ---------------------------------------------------------------------------

def sql(query, token=None, timeout=180):
    """Run SQL through tables.query.execute and return a list of row dicts.

    The endpoint returns its payload base64-encoded under `data`, holding a JSON
    array. Both layers are unwrapped here so callers deal in plain rows.
    """
    resp = api("tables.query.execute", {"query": query}, token=token, timeout=timeout)
    blob = resp.get("data")
    if blob is None:
        return []
    try:
        text = base64.b64decode(blob).decode("utf-8", errors="replace")
    except Exception:
        text = blob if isinstance(blob, str) else ""
    text = text.strip()
    if not text:
        return []
    try:
        rows = json.loads(text)
    except ValueError:
        # Not JSON after all — hand the raw text back rather than inventing rows.
        return [{"_raw": text}]
    return rows if isinstance(rows, list) else [rows]


def sql_checked(query, token=None):
    """sql() plus the truncation warning. Returns (rows, warnings)."""
    rows = sql(query, token=token)
    warnings = []
    if len(rows) >= ROW_CAP:
        warnings.append(
            "Returned exactly %d rows, the silent server-side cap. The result is "
            "almost certainly truncated - aggregate in SQL or narrow the filters "
            "instead of paging, because this endpoint returns no cursor." % ROW_CAP)
    return rows, warnings


# ---------------------------------------------------------------------------
# Catalog helpers
# ---------------------------------------------------------------------------

def list_tables(token=None, max_pages=60):
    """Every table name the caller's token can see, via cursor paging."""
    out, cursor = [], None
    for _ in range(max_pages):
        body = {"limit": 100}
        if cursor:
            body["cursor"] = cursor
        resp = api("tables.schemas.list", body, token=token)
        page = resp.get("table_schemas") or []
        out.extend(page)
        cursor = resp.get("next_cursor")
        if not cursor or not page:
            break
    return out


def table_schema(table_id, token=None):
    """Field list for one table. The response key is `table_schema`, not `schema`."""
    resp = api("tables.schemas.get", {"id": table_id}, token=token)
    schema = resp.get("table_schema") or resp.get("schema") or resp
    return schema.get("fields") or schema.get("columns") or []


def current_user(token=None):
    try:
        return api("dev-users.self", {}, internal=False, token=token)
    except DevRevError:
        return {}


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(description="DevRev transport for the imperative-care skill.")
    ap.add_argument("--check", action="store_true", help="verify the token resolves and works")
    ap.add_argument("--endpoint", help="endpoint name, e.g. dashboards.get")
    ap.add_argument("--data", default="{}", help="JSON request body")
    ap.add_argument("--public", action="store_true", help="use the public root, not /internal/")
    ap.add_argument("--sql", help="run a SQL query and print rows")
    ap.add_argument("--list-tables", action="store_true", help="print every visible table name")
    args = ap.parse_args()

    try:
        if args.check:
            tok = load_token()
            rows = sql("SELECT 1 AS ok")
            who = current_user()
            user = (who.get("dev_user") or {}).get("display_name") or "(name unavailable)"
            print(json.dumps({"ok": bool(rows), "token_length": len(tok),
                              "token_source": "env or .env (value not shown)",
                              "user": user, "base_url": BASE_URL}, indent=1))
            return 0
        if args.list_tables:
            names = sorted(t.get("name", "") for t in list_tables())
            print(json.dumps({"count": len(names), "tables": names}, indent=1))
            return 0
        if args.sql:
            rows, warns = sql_checked(args.sql)
            print(json.dumps({"ok": True, "row_count": len(rows), "rows": rows,
                              "warnings": warns}, indent=1, default=str))
            return 0
        if args.endpoint:
            print(json.dumps(api(args.endpoint, json.loads(args.data), internal=not args.public),
                             indent=1, default=str))
            return 0
    except DevRevError as exc:
        print(json.dumps({"ok": False, "status": exc.status, "endpoint": exc.endpoint,
                          "error": str(exc)}, indent=1))
        return 1
    except ValueError as exc:
        print(json.dumps({"ok": False, "error": "bad --data JSON: %s" % exc}))
        return 1
    ap.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
