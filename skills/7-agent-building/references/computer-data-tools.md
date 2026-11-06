# DevRev Computer data tools (ExecuteSQL, SearchKGSchema) as a local MCP server

Computer answers data questions with two tools that the desktop app injects at runtime as
`mcp__devrev-agent-tools__ExecuteSQL` and `mcp__devrev-agent-tools__SearchKGSchema`. `scripts/computer-data-mcp/`
reproduces them as a stdio MCP server, so any MCP client (Claude Code, Claude Desktop, an eval harness) can ask the
same data questions against the same endpoints and show exactly which queries ran, what came back and what errored.
Use it to evaluate or debug Computer's data-answering path at scale. Python 3.9+, standard library only.

| Tool | What it does | Endpoint |
| --- | --- | --- |
| `SearchKGSchema` | Finds tables by keyword, or returns one table's columns with DevRev's own field documentation | `/internal/tables.schemas.list`, `/internal/tables.schemas.get` |
| `ExecuteSQL` | Runs a read-only SQL query against the DevRev tables | `/internal/tables.query.execute` |

The SQL dialect and the API's silent limits (parenthesized `(t).column` refs, 1,000-row result cap, truncated long
text in snapshot tables) are in `references/toolkit-guide.md` (field notes, confirmed live 2026-09-09).

## Set up

1. **Your own token.** Queries run as you and see only what your account can see; never use someone else's token.
   `export DEVREV_PAT=<token>`, or copy `scripts/computer-data-mcp/.env.example` to `.env` beside `mcp_devrev.py`
   (`.env` is gitignored). The client also accepts `DEVREV_API_KEY`, `DEVREV_TOKEN` or `ORG_PAT`, in that order, and
   `DEVREV_BASE_URL` (default `https://api.devrev.ai`).
2. **Self-test** (makes live read-only calls with your token):
   `python3 skills/7-agent-building/scripts/computer-data-mcp/mcp_devrev.py --selftest`
3. **Register it in your own project**, not in this plugin (this repo's `.mcp.json` ships only DevRev's hosted
   server, by design). A `.mcp.json` with an absolute path:

```json
{"mcpServers": {"devrev-agent-tools": {"command": "python3",
  "args": ["/absolute/path/to/skills/7-agent-building/scripts/computer-data-mcp/mcp_devrev.py"]}}}
```

Then, for example: `claude -p --allowedTools "mcp__devrev-agent-tools__ExecuteSQL,mcp__devrev-agent-tools__SearchKGSchema"`.
Add `--output-format stream-json --verbose` to capture every `tool_use` (the full query) and `tool_result` (what came
back and whether it errored), not just the final answer.

## Design rules the server keeps (and why)

An evaluation whose tooling quietly fabricates, truncates or swallows an error cannot be trusted in either direction,
so every path fails loud:

- **Read-only by construction.** Anything that is not `SELECT` or `WITH` is refused before it reaches DevRev.
- **A query error is an error,** carrying the engine's own message; it is never an empty result, which a model reads
  as "no data".
- **Truncation is announced.** Results over 2,000 rows, or over 120,000 characters (then cut to 200 rows), carry
  `truncated: true` and a warning to aggregate in SQL instead of summing returned rows.
- **Field documentation is passed through whole.** An earlier version cut column descriptions at 200 characters. On
  one customer's data the record-type column says in its first sentence that orders and quota targets share a table,
  and only at the end: "Caution: without this filter order and quota rows mix". The warning fell past the cut, the
  agent summed both kinds and reported company revenue 127% too high, with sound reasoning and a clean query. Never
  truncate schema documentation shown to an agent.

## Transport lessons (from `devrev_client.py`)

- **Auth header.** In one org, `/internal/` endpoints accepted only a bare `Authorization: <token>`; the public root
  accepts both forms. The client sends the bare form and retries once with `Bearer` on a 401. Treat this as
  org-dependent: the repo default is `Bearer` (`skills/devrev-start/references/global-api-rules.md`).
- **Token leakage.** Requests are built with `urllib`, never a shell: a `subprocess.run(..., check=True)` whose argv
  holds `-H "Authorization: ..."` puts the whole PAT into the `CalledProcessError` traceback.
- **Rate limits.** Pace from the live `X-Ratelimit-Remaining` / `X-Ratelimit-Limit` headers, not a hardcoded quota
  (observed limits differ from the published ones by more than an order of magnitude, and per org). On a 429 honour
  `Retry-After` (or the body's `retry_after`); five consecutive 429s trip a circuit breaker.
- **Error bodies.** `message` is generic ("Bad Request"); the actionable text is `debug_message`, so surface it first.
  429 bodies have a different, RFC 7807-like shape where `type` is a URI.
- **Retries.** Retry 429, 503, 504 and network errors with capped backoff; never 400/401/403/404/422. On these data
  endpoints a bare 500 has repeatedly meant a malformed request rather than a transient fault, so it is not retried
  here: fix the request first (the general guidance in `skills/10-api-conventions` still applies elsewhere).
- **Why a personal token works.** `tables.query.execute` is served from `/internal/` but accepts an ordinary PAT, and
  results then respect that user's row-level access. A service account (for example the one that owns dashboards)
  may have no data access at all.
