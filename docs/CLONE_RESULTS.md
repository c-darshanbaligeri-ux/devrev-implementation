# Clone results

Generated: 2026-07-18 (initial build). Clones are shallow (`--depth 1`). This file is the
**curated build-time snapshot**; the bootstrap hook writes its per-machine outcomes to
`docs/CLONE_RESULTS.local.md` (gitignored). Refresh via the `update-repos` skill (explicit request
only).

| Repo | Status | Default branch | Commit SHA | Notes |
|---|---|---|---|---|
| aai-skills | OK | main | 57b8a5f | Plugin marketplace `devrev-aai-plugins`: dashboard-dev + dataset-builder (both auto-enabled) |
| dashboard-sync-cli | OK | main | 451a51d | Python CLI (pipx-installed by bootstrap); dashboard-dev shells out to it |
| api-specs | OK | main | 79cd29e | OpenAPI contracts (`specs/next/openapi-internal.yaml`) for skills/7 grounding |
| devrev-qk-agents | PENDING | main | — | Third-party plugin marketplace `devrev-qk-agents` (source repo `QK-SnapIn/devrev-qk-agents`), powers skills/9's snap-in vertical. Registered in `.claude/settings.json` `extraKnownMarketplaces` but **NOT auto-enabled** — user opts in with `/plugin install devrev@devrev-qk-agents`. Cloned by the bootstrap hook on first session after `.env` is present; the actual SHA on this machine will appear in `CLONE_RESULTS.local.md`. |

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
