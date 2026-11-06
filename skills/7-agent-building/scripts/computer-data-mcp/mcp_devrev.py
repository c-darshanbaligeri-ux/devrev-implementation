"""An MCP server exposing the DevRev Computer's data-access tools.

WHY THIS EXISTS
---------------
The Computer answers data questions through `mcp__devrev-agent-tools__ExecuteSQL`
and `SearchKGSchema`, injected by the desktop app at runtime. The app cannot be
driven from outside — API-posted messages are not picked up — so to evaluate the
Computer's data-answering path at scale we give the same model the same two
tools, pointed at the same endpoint with the same credentials.

THE ONE RULE THIS FILE EXISTS TO HONOUR
---------------------------------------
This harness must never be the source of a wrong answer. An evaluation whose
tooling quietly fabricates, truncates or swallows an error cannot be trusted in
either direction — a pass might be the harness, and so might a failure.

So every path here fails loud:

  * a query error returns the engine's own message, surfaced as an MCP error.
    It is never an empty result set, which the model would read as "no data".
  * a truncated result says so in the payload, with the cap that applied. A
    silently clipped result is how a SUM becomes wrong without anyone noticing.
  * row and byte caps are stated in the response, not applied invisibly.
  * no retries that could mask a real failure as a transient one.
  * read-only by construction: anything that is not SELECT/WITH is refused here,
    before it reaches the API.

PROTOCOL
--------
MCP over stdio: newline-delimited JSON-RPC 2.0 on stdin/stdout. Only the three
methods Claude Code needs are implemented — `initialize`, `tools/list`,
`tools/call` — plus `notifications/*`, which are acknowledged and ignored.
Anything written to stdout that is not a JSON-RPC response corrupts the channel,
so all diagnostics go to stderr.
"""
from __future__ import annotations

import json
import sys
import traceback
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import devrev_client as dc  # noqa: E402

PROTOCOL_VERSION = "2024-11-05"
ROW_CAP = 2000          # beyond this the payload stops being useful to a model
CHAR_CAP = 120_000      # hard ceiling on a single tool result

TOOLS = [
    {
        "name": "ExecuteSQL",
        "description": (
            "Run a read-only SQL query against the DevRev analytics tables and "
            "return the rows as JSON. Use this to compute any figure from the "
            "data. Only SELECT and WITH statements are accepted. If the query "
            "fails, the engine's own error text is returned — read it and fix "
            "the query rather than guessing. If a result is truncated the "
            "response says so explicitly; treat a truncated result as unsafe to "
            "aggregate."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The SQL to run. SELECT or WITH only.",
                }
            },
            "required": ["query"],
        },
    },
    {
        "name": "SearchKGSchema",
        "description": (
            "List the available tables, optionally filtered by a keyword, and "
            "return each table's columns. Use this BEFORE writing SQL: column "
            "names on the synced Salesforce tables are obfuscated and cannot be "
            "guessed. Passing a table name returns that table's full column "
            "list; passing a keyword returns matching table names."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "keyword": {
                    "type": "string",
                    "description": "Substring to match against table names.",
                },
                "table": {
                    "type": "string",
                    "description": "Exact table name; returns its columns as "
                                   "compact name:type lines.",
                },
                "column_keyword": {
                    "type": "string",
                    "description": "With `table`: return only columns matching "
                                   "this, WITH their descriptions. Use it when "
                                   "you need a column's meaning rather than the "
                                   "whole list.",
                },
            },
        },
    },
]


class ToolError(Exception):
    """Raised so the failure reaches the model as an MCP error, not as data."""


# ── tool implementations ────────────────────────────────────────────────────
def execute_sql(args: dict) -> str:
    query = (args or {}).get("query") or ""
    if not query.strip():
        raise ToolError("No query supplied.")

    flat = " ".join(query.split())
    if not flat.lower().lstrip("( ").startswith(("select", "with")):
        raise ToolError(
            "Refused: this tool is read-only and accepts only SELECT or WITH "
            f"statements. Received: {flat[:120]}")

    try:
        rows = dc.sql(flat)
    except Exception as e:                                        # noqa: BLE001
        # The engine's own text is the actionable part. Surfacing it as an
        # error (not as an empty result) is what stops the model concluding
        # "no rows" when the truth is "the query was malformed".
        raise ToolError(f"Query failed. The engine returned: {e}") from None

    truncated = len(rows) > ROW_CAP
    shown = rows[:ROW_CAP]
    payload = {
        "row_count": len(rows),
        "rows_returned": len(shown),
        "truncated": truncated,
        "rows": shown,
    }
    if truncated:
        payload["warning"] = (
            f"TRUNCATED at {ROW_CAP} rows of {len(rows)}. Do NOT aggregate these "
            "rows — push the aggregation into SQL and re-run.")

    text = json.dumps(payload, default=str)
    if len(text) > CHAR_CAP:
        payload["rows"] = payload["rows"][:200]
        payload["truncated"] = True
        payload["warning"] = (
            f"TRUNCATED: the result exceeded {CHAR_CAP} characters and was cut "
            "to 200 rows. Do NOT aggregate these rows — aggregate in SQL and "
            "re-run.")
        text = json.dumps(payload, default=str)
    return text


_TABLE_CACHE: list[dict] = []


def _tables() -> list[dict]:
    """Table name, id and description. The descriptions are what make dataset
    selection possible — they state grain, record-type splits and what each
    table is NOT for, which is exactly what a model otherwise has to guess."""
    global _TABLE_CACHE
    if not _TABLE_CACHE:
        try:
            _TABLE_CACHE = [
                {"name": t.get("name", ""), "id": t.get("id", ""),
                 "description": (t.get("description") or "")}
                for t in dc.list_tables() if t.get("name")
            ]
            _TABLE_CACHE.sort(key=lambda t: t["name"])
        except Exception as e:                                    # noqa: BLE001
            raise ToolError(f"Could not list tables: {e}") from None
    return _TABLE_CACHE


def _columns(table: str) -> list[dict]:
    """Columns for one table, read from the schema API.

    SELECT * is blocked by this engine, so the schema endpoint is the only
    route. The payload nests as table_schema.fields — getting that path wrong
    returns nothing, which the model reads as 'this table has no columns' and
    then guesses column names from the Salesforce originals. That is precisely
    the failure this tool exists to prevent, so a miss raises rather than
    returning empty.
    """
    tid = next((t["id"] for t in _tables() if t["name"] == table), None)
    if not tid:
        raise ToolError(
            f"No table named '{table}'. Search by keyword first; do not guess "
            "table names.")
    try:
        resp = dc.api("tables.schemas.get", {"id": tid})
    except Exception as e:                                        # noqa: BLE001
        raise ToolError(f"Could not read the schema of {table}: {e}") from None
    fields = ((resp or {}).get("table_schema") or {}).get("fields") or []
    if not fields:
        raise ToolError(
            f"The schema API returned no fields for '{table}'. Do not guess "
            "column names — report that the schema is unavailable.")
    out = []
    for f in fields:
        if not isinstance(f, dict):
            out.append({"name": str(f)})
            continue
        enum = (f.get("enum") or {}).get("enum_list") or []
        out.append({k: v for k, v in (
            ("name", f.get("name")),
            ("type", f.get("type") or f.get("field_type")),
            ("display_name", f.get("display_name")),
            # The allowed values matter as much as the type. 'Order' vs 'Quota'
            # on one column is the difference between revenue and target.
            ("allowed_values", [e.get("value") for e in enum if e.get("value")]),
            ("description", (f.get("description") or "")),
        ) if v})
    return out


def search_schema(args: dict) -> str:
    """Tables by keyword, or one table's columns with their descriptions.

    A leaner payload was tried and measured: columns as bare name:type cut each
    result 4.8x but pushed tool calls from 10 to 16, because the model simply
    asked again for what had been removed. Total cost was identical and the run
    took ~40% longer. The richer payload is kept for that reason, not by
    default — fewer, better-informed calls beat more, thinner ones.
    """
    args = args or {}
    table = (args.get("table") or "").strip()
    keyword = (args.get("keyword") or "").strip()
    col_kw = (args.get("column_keyword") or "").strip().lower()

    if table:
        cols = _columns(table)
        meta = next((t for t in _tables() if t["name"] == table), {})
        if col_kw:
            cols = [c for c in cols
                    if col_kw in c.get("name", "").lower()
                    or col_kw in c.get("description", "").lower()]
        return json.dumps({
            "table": table,
            "description": (meta.get("description") or ""),
            "column_count": len(cols),
            # Descriptions are passed through WHOLE. They were truncated to
            # 200 characters, and the field documentation puts the usable part
            # last: the record-type column explains the Order/Quota split in
            # its first sentence but says "Caution: without this filter order
            # and quota rows mix" at the end. The agent read the first half,
            # summed across both kinds, and reported company revenue 127% too
            # high. The warning was fetched, then thrown away before it was
            # shown. Nothing here is truncated again without a measured reason.
            "columns": [{k: v for k, v in (
                ("name", c.get("name")),
                ("type", c.get("type")),
                ("allowed_values", c.get("allowed_values")),
                ("description", c.get("description") or ""),
            ) if v} for c in cols],
        }, default=str)

    matches = _tables()
    if keyword:
        k = keyword.lower()
        matches = [t for t in matches
                   if k in t["name"].lower() or k in t["description"].lower()]
    return json.dumps({
        "match_count": len(matches),
        "tables": [{"name": t["name"], "description": t["description"]}
                   for t in matches[:120]],
        "note": ("Pass an exact table name as `table` for its columns. Column "
                 "names on synced Salesforce tables are obfuscated and must be "
                 "read, not guessed."),
    }, default=str)


HANDLERS = {"ExecuteSQL": execute_sql, "SearchKGSchema": search_schema}


# ── JSON-RPC plumbing ───────────────────────────────────────────────────────
def reply(msg: dict) -> None:
    sys.stdout.write(json.dumps(msg) + "\n")
    sys.stdout.flush()


def handle(req: dict) -> dict | None:
    rid, method = req.get("id"), req.get("method", "")

    if method == "initialize":
        return {"jsonrpc": "2.0", "id": rid, "result": {
            "protocolVersion": PROTOCOL_VERSION,
            "capabilities": {"tools": {}},
            "serverInfo": {"name": "devrev-agent-tools", "version": "1.0.0"},
        }}

    if method == "tools/list":
        return {"jsonrpc": "2.0", "id": rid, "result": {"tools": TOOLS}}

    if method == "tools/call":
        params = req.get("params") or {}
        name = params.get("name", "")
        fn = HANDLERS.get(name)
        if not fn:
            return {"jsonrpc": "2.0", "id": rid,
                    "error": {"code": -32601, "message": f"No such tool: {name}"}}
        try:
            text = fn(params.get("arguments") or {})
            return {"jsonrpc": "2.0", "id": rid, "result": {
                "content": [{"type": "text", "text": text}], "isError": False}}
        except ToolError as e:
            # isError=True so the model sees a failure, never an empty success.
            return {"jsonrpc": "2.0", "id": rid, "result": {
                "content": [{"type": "text", "text": str(e)}], "isError": True}}
        except Exception as e:                                    # noqa: BLE001
            print(traceback.format_exc(), file=sys.stderr)
            return {"jsonrpc": "2.0", "id": rid, "result": {
                "content": [{"type": "text",
                             "text": f"Tool crashed: {type(e).__name__}: {e}"}],
                "isError": True}}

    if method.startswith("notifications/"):
        return None

    if rid is None:
        return None
    return {"jsonrpc": "2.0", "id": rid,
            "error": {"code": -32601, "message": f"Unsupported method: {method}"}}


def selftest() -> int:
    """Check the token, the connection and both tools, and say what is wrong.

    Written for someone setting this up for the first time: every failure names
    the thing to fix rather than raising a stack trace at them.
    """
    print("DevRev Computer MCP — self test\n")
    try:
        tok = dc.load_token()
        print(f"  [ok]   token found ({len(tok)} chars, not shown)")
    except SystemExit as e:
        print(f"  [FAIL] {e}")
        return 1
    try:
        tables = _tables()
        print(f"  [ok]   connected — {len(tables)} tables visible to your account")
    except Exception as e:                                        # noqa: BLE001
        print(f"  [FAIL] could not reach DevRev: {str(e)[:200]}")
        print("         check the token is valid and not expired.")
        return 1
    if not tables:
        print("  [FAIL] connected, but your account can see no tables.")
        return 1
    try:
        r = json.loads(execute_sql({"query": "SELECT 1 AS ok"}))
        assert r["rows"][0]["ok"] == 1
        print("  [ok]   ExecuteSQL works")
    except Exception as e:                                        # noqa: BLE001
        print(f"  [FAIL] ExecuteSQL: {str(e)[:200]}")
        return 1
    try:
        name = tables[0]["name"]
        cols = json.loads(search_schema({"table": name}))
        n = cols["column_count"]
        documented = sum(1 for c in cols["columns"]
                         if len(c.get("description") or "") > 200)
        print(f"  [ok]   SearchKGSchema works — {name} has {n} columns, "
              f"{documented} with detailed documentation")
    except Exception as e:                                        # noqa: BLE001
        print(f"  [FAIL] SearchKGSchema: {str(e)[:200]}")
        return 1
    print("\n  All good. Point your MCP client at this folder.")
    return 0


def main() -> None:
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
        except ValueError:
            continue
        try:
            out = handle(req)
        except Exception:                                         # noqa: BLE001
            print(traceback.format_exc(), file=sys.stderr)
            continue
        if out is not None:
            reply(out)


if __name__ == "__main__":
    main()
