# repos/ — cloned upstream toolchains

Everything in this directory except this file and `.gitkeep` is a **shallow clone of an upstream repo**, listed in `../repos.txt` and cloned by the bootstrap hook on first session. The contents are gitignored.

| Clone | Why it is here |
| --- | --- |
| `aai-skills/` | Plugin marketplace `devrev-aai-plugins`: source of the `dashboard-dev` and `dataset-builder` plugins (skills 4 and 5 route into it) |
| `dashboard-sync-cli/` | The Python CLI the dashboard plugin shells out to (installed with pipx by the bootstrap) |
| `api-specs/` | DevRev OpenAPI contracts (`specs/next/openapi-internal.yaml`), used to ground skill 7's internal API calls |
| `devrev-qk-agents/` | Third-party snap-in plugin that skill 9 routes into (read-only here; installing it is a manual step) |
| `aai-custom-computer-capabilities/` | Source the agent-building skill (7) was derived from; kept so later updates can be diffed against it (private, needs devrev org read access). Its `3-computer-capabilities-nxt/workflow-skill` (MIT) is the cross-check for skill 6's import, validate and publish API calls |
| `computer-skill/` | Community Computer skill, kept as grounding for skill 0 blueprints; no skill routes to it. Its `create-workflow-template` is already inlined in skill 6 (identical or a subset, checked 2026-11-03), and it has no licence file: copy nothing from it |
| `agent-evals/` | DevRev's agent evaluation harness (datasets, direct and DM run modes, metrics, benchmarks including Computer); skill 7's `commands/agent-test.md` routes to it for test sets at scale. Private (needs devrev org read access) and unlicensed: copy nothing from it |

**Rules**
- **Never edit these clones.** They are not the source of truth for this repo. Local edits block the updater (it skips dirty repos). Learnings about these tools go in this repo's own skill files (`.claude/skills/capture-learnings/SKILL.md`).
- Refresh **only on an explicit user request**, through `.claude/skills/update-repos/`.
- Per-machine clone status is written to `../docs/CLONE_RESULTS.local.md` (gitignored). Deliberately excluded repos (`devrev-snap-ins`, the archived `mcp-server`) and why are noted in `../repos.txt`.
