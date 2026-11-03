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
| aai-custom-computer-capabilities | PENDING | main | — | Original source of `skills/7-agent-building/` (agent-building toolkit) and the Computer snap-ins routed via skills/9. **Private** repo — requires GitHub read access to the `devrev` org, same as api-specs. Content was copied and adapted at build time; the live clone here is grounding for future re-diff/re-inline (see `docs/SUMMARY.md` § "Fixups Applied"). |
| computer-skill | PENDING | main | — | Community fork `shashankcube/computer-skill`: 10 sales-oriented Claude Code skills (MEDDPICC deal review, sales call planning, account research, workflow-template generation, etc.). Public. Reference material only — not routed to by any skill in this repo. Note: name collides with any future `devrev/computer-skill` clone — if that ever enters `repos.txt`, resolve the collision (e.g. rename this entry's clone dir manually or fork-suffix the name in `repos.txt`). |

## Non-git references (documented for provenance, not cloned)

- **Google Doc "Agent Skills Marketplace"** — `https://docs.google.com/document/d/16NFkXnoY4c4xASkmoBfkG2uP32MInqlxzA2HOmUye2o/` — requires Google auth; design/marketplace notes that informed some of the skill routing. Not automatable. If the doc is updated meaningfully, mirror any relevant facts into `docs/LEARNINGS.md` via the capture-learnings protocol.

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
