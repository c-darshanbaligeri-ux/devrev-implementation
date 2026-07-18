# DevRev Implementation Operating Environment

This is the unified workspace for all DevRev implementation work, spanning solution design (skill 0) through build (skills 1–9, including snap-in / AirSync connector development via a routed third-party plugin at skill 9). It's not a buildable software project — it's a plug-and-play operating environment containing skills, reference documentation, cloned toolchains, and an integrated DevRev MCP server. Everything needed to design solutions, customize DevRev organizations, migrate data, build dashboards and datasets, author workflows, develop AI agents, and build snap-ins.

## One-time setup

1. **Create `.env` from `.env.example`**:
   ```bash
   cp .env.example .env
   ```
2. **Populate your DevRev PAT** (get one from DevRev → Settings → Account → Personal Access Tokens):
   ```env
   DEVREV_PAT=your_personal_access_token
   DEVREV_ENDPOINT=https://api.devrev.ai
   ```
3. **Start a Claude Code session** in this directory.
4. **Accept the workspace-trust prompt** to activate the plugin marketplace (enables `dashboard-dev` and `dataset-builder` plugins from the committed `.claude/settings.json`).
5. **Wait ~1 minute** for background installs to complete (repos clone + `dashboard-sync` CLI install via pipx). Progress logs to `.claude/.auto-setup/install.log`.
6. **Start a second session** so your shell PATH picks up `~/.local/bin/dashboard-sync` (the hook can't refresh PATH of its own session).

That's it. Everything else auto-configures on session start.

## What self-configures

| Component | How it initializes |
| --- | --- |
| **Repos clone** (6 total: `aai-skills`, `dashboard-sync-cli`, `api-specs`, `devrev-qk-agents`, `aai-custom-computer-capabilities`, `computer-skill`) | SessionStart hook clones on first run; per-machine status table written to `docs/CLONE_RESULTS.local.md` (gitignored). Curated build-time snapshot lives at `docs/CLONE_RESULTS.md`. Refresh on demand via the `update-repos` skill. |
| **`dashboard-sync` CLI** | SessionStart hook installs via `pipx` on first run (background; logs to `.claude/.auto-setup/install.log`) |
| **Workspace directories** (`dashboards/`, `datasets/`, `plans/`, `logs/`, `templates/`) | SessionStart hook creates synchronously; CLI then runs `dashboard-sync init` once present |
| **`config.yaml`** | The `dashboard-dev` plugin's own hook generates it from `.env` |
| **Plugin marketplace** (`dashboard-dev`, `dataset-builder`) | Committed `.claude/settings.json` registers `devrev-aai-plugins` marketplace; trust prompt activates it — these two plugins auto-enable |
| **`devrev-qk-agents` marketplace** (snap-in build pipeline, `skills/9`) | Source registered in `.claude/settings.json`, but **not auto-enabled** — third-party org, manual opt-in: `/plugin install devrev@devrev-qk-agents` |
| **Hosted MCP** (DevRev object access: search, work items, parts, etc.) | `.mcp.json` points to `https://api.devrev.ai/mcp/v1`; `${DEVREV_PAT}` is read from the process environment — export it (or source `.env`) in the shell that launches Claude Code if the MCP shows unauthorized |

## Capability map

| Skill | What it does |
| --- | --- |
| **skills/0-solution-architecture** | Turns a vague business problem into a 20-section DevRev solution blueprint (design phase; no live API calls) — use before skills 1–8 for greenfield/cross-domain requests |
| **skills/1-object-schema-customization** | Create custom object types, add tenant/subtype fields to stock objects, define custom link types, modify schemas |
| **skills/2-stage-lifecycle-customization** | Customize stages, states, stage diagrams, and lifecycle flows for work items |
| **skills/3-data-upload-and-org-build** | Upload artifacts, bulk-create records, build fresh orgs from scratch (ordered: schemas → parts → Trails → links → work) |
| **skills/4-dashboards-and-widgets** | Router to `dashboard-dev` plugin commands (`/create-dashboard`, `/modify-dashboard`) |
| **skills/5-datasets** | Router to `dataset-builder` plugin commands (`:setup`, `:explore`, `:create`, `:update`, `:delete`, `:test`, `:validate`) |
| **skills/6-workflows** | Author, test, and manage DevRev workflows and agent-callable skills (templates, schemas, examples, trigger script) |
| **skills/7-agent-building** | Build, configure, test, and debug AI agents (configs, guardrails, skills, knowledge sync, annotations, internal API) |
| **skills/8-devrev-api** | Direct DevRev REST API access — complete endpoint catalog + domain guides for all public API groups |
| **skills/9-snapin-development** | Router to the `devrev-qk-agents` plugin's snap-in vertical (`/devrev:plan-snapin`, `/devrev:build-snapin`, `/devrev:test-snapin`, `/devrev:update-snapin`) — plugin requires manual install + 2 MCP servers, see the skill's Preconditions |

## Plug-and-play acceptance summary

From a fresh machine with git + gh auth + Claude Code installed:

1. Clone this repo.
2. Create `.env` from `.env.example` (both `DEVREV_PAT=<your_token>` and `DEVREV_ENDPOINT=https://api.devrev.ai` — the dashboard plugin requires both lines).
3. Start a Claude Code session, accept the trust prompt.
4. Wait ~1 minute for background installs.
5. Start a second session for PATH refresh.

**Fully operational for skills 0–8 after these five steps.** No npm install, no build, no config files to hand-edit, no CLI to install separately (it auto-installs), no MCP server to run for the hosted DevRev MCP. The workspace auto-configures on every session start after that.

**Snap-in development (`skills/9`) needs one extra opt-in**, done once per project: `/plugin install devrev@devrev-qk-agents` plus 1–2 third-party MCP server opt-ins (`snapin-builder` for build/update/metadata/search; `airsync` for `/devrev:generate-metadata`). This repo won't auto-activate a non-devrev-org plugin or auto-register non-DevRev MCP endpoints — but the marketplace is already registered, so the `/plugin install` line is all it takes to enable it. See `skills/9-snapin-development/SKILL.md`.

## Troubleshooting

| Symptom | Likely cause | Solution |
| --- | --- | --- |
| `command not found: dashboard-sync` | Install still running, or new session needed for PATH | Check `.claude/.auto-setup/install.log` for progress; if "OK" logged, start a new session to pick up `~/.local/bin` in PATH |
| Plugins missing (`/plugin` doesn't show `dashboard-dev` or `dataset-builder`) | Workspace-trust prompt not accepted, or plugins not loaded | Accept trust prompt; restart Claude Code; or run `/plugin marketplace update devrev-aai-plugins` to force reload. If the GitHub-source marketplace can't authenticate against the private repo, register the local clone once instead: `/plugin marketplace add ./repos/aai-skills` |
| `/devrev:*` snap-in commands don't resolve, or report an MCP server not connected | Plugin never installed (deliberately not auto-enabled), or MCP servers not opted into | Run `/plugin install devrev@devrev-qk-agents`, then `claude mcp add snapin-builder --transport http -s project https://snapin-builder-mcp.onrender.com/mcp` (and `claude mcp add airsync chef-cli mcp initial-mapping` for `/devrev:generate-metadata`) — see `skills/9-snapin-development/SKILL.md` Preconditions |
| 401 Unauthorized on API calls | Missing or invalid PAT in `.env` | Verify `.env` exists and `DEVREV_PAT` is a valid token; test with `curl -H "Authorization: Bearer $DEVREV_PAT" https://api.devrev.ai/ping` |
| Clone failures for repos | Missing GitHub access to devrev org repos, or `gh` not authenticated | Check `docs/CLONE_RESULTS.md` for error details; run `gh auth status` and ensure the authenticated account has read access to devrev org repos |
| `gcloud` / `bq` / `kubectl` commands fail | Ponos-path prerequisites missing (not auto-installed) | Run `/dataset-builder:setup` to check and configure; these are only needed for Ponos jobs, not PaaS datasets |
| `/create-dashboard` doesn't resolve, but `/dashboard-dev:dashboard-create` does | Plugin command's frontmatter uses `dashboard-create`; the namespaced form always resolves | Use `/dashboard-dev:dashboard-create` (same command). Same for `/modify-dashboard` → `/dashboard-dev:modify-dashboard`. |
| `/dashboard-planner` doesn't resolve | It's a plugin **skill**, not a slash command | Invoke it via the Skill mechanism (from `repos/aai-skills/plugins/dashboard-dev/skills/dashboard-planner/`), or just describe the requirement — skill 4 routes correctly. |
