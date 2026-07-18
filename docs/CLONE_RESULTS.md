# Clone results

Generated: 2026-07-18 (initial build). Clones are shallow (`--depth 1`). Refresh via the
`update-repos` skill (explicit request only); the bootstrap hook appends rows here if it
performs the initial clone on a fresh machine.

| Repo | Status | Default branch | Commit SHA | Notes |
|---|---|---|---|---|
| aai-skills | OK | main | 57b8a5f | Plugin marketplace `devrev-aai-plugins`: dashboard-dev + dataset-builder |
| dashboard-sync-cli | OK | main | 451a51d | Python CLI (pipx-installed by bootstrap); dashboard-dev shells out to it |
| api-specs | OK | main | 79cd29e | OpenAPI contracts (`specs/next/openapi-internal.yaml`) for skills/7 grounding |

## Deliberate exclusions

- **`https://github.com/devrev/devrev-snap-ins`** — snap-in source is out of scope for this repo.
  The only tangentially related piece is `trigger-dashboard-agent/` (an in-org command to trigger
  the dashboard agent), which is optional, Dev0-only, and not needed for local use. If ever needed,
  add the URL to `repos.txt` and run the update-repos skill.
- **`https://github.com/devrev/mcp-server`** — archived by DevRev. Fully superseded by the hosted
  Remote MCP server (`https://api.devrev.ai/mcp/v1`) wired in this repo's `.mcp.json`.

## On-demand clones

- **`https://github.com/devrev/auto-annotations`** — not in `repos.txt`; auto-cloned on first use
  by `skills/7-agent-building/scripts/check-annotations.sh` (NL2SQL annotation checking).
