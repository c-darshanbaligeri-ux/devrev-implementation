# repos/ — cloned upstream toolchains

Everything in this directory (except this file and `.gitkeep`) is a **shallow clone of an upstream
DevRev repo**, listed in `../repos.txt` and cloned automatically by the bootstrap hook on first
session. Contents are gitignored.

| Clone | Why it's here |
| --- | --- |
| `aai-skills/` | Plugin marketplace `devrev-aai-plugins` — source of the `dashboard-dev` and `dataset-builder` plugins (skills 4 and 5 route into it) |
| `dashboard-sync-cli/` | The Python CLI the dashboard plugin shells out to (pipx-installed by the bootstrap) |
| `api-specs/` | DevRev OpenAPI contracts (`specs/next/openapi-internal.yaml`) — grounding for skill 7's internal API calls |

**Rules**
- **Never edit these clones.** They are not source of truth for this repo; local edits block the
  updater (it skips dirty repos) and are lost context. Learnings about these tools belong in OUR
  skill files (see `.claude/skills/capture-learnings/SKILL.md`).
- Refresh **only on explicit user request** via `.claude/skills/update-repos/`.
- Clone status/SHAs live in `../docs/CLONE_RESULTS.md`, including the deliberately excluded repos
  (`devrev-snap-ins`, archived `mcp-server`) and why.
