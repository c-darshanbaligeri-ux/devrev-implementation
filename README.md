# DevRev Implementation Operating Environment

This is the unified workspace for all DevRev implementation work apart from snap-in development. It's not a buildable software project — it's a plug-and-play operating environment containing skills, reference documentation, cloned toolchains, and an integrated DevRev MCP server. Everything needed to customize DevRev organizations, migrate data, build dashboards and datasets, author workflows, and develop AI agents.

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
| **Repos clone** (`repos/aai-skills`, `repos/dashboard-sync-cli`, `repos/api-specs`) | SessionStart hook clones on first run; status table written to `docs/CLONE_RESULTS.md` |
| **`dashboard-sync` CLI** | SessionStart hook installs via `pipx` on first run (background; logs to `.claude/.auto-setup/install.log`) |
| **Workspace directories** (`dashboards/`, `datasets/`, `plans/`, `logs/`, `templates/`) | SessionStart hook creates synchronously; CLI then runs `dashboard-sync init` once present |
| **`config.yaml`** | The `dashboard-dev` plugin's own hook generates it from `.env` |
| **Plugin marketplace** (`dashboard-dev`, `dataset-builder`) | Committed `.claude/settings.json` registers `devrev-aai-plugins` marketplace; trust prompt activates it |
| **Hosted MCP** (DevRev object access: search, work items, parts, etc.) | `.mcp.json` points to `https://api.devrev.ai/mcp/v1`; token interpolated from `${DEVREV_PAT}` in `.env` |

## Capability map

| Skill | What it does |
| --- | --- |
| **skills/1-object-schema-customization** | Create custom object types, add tenant/subtype fields to stock objects, define custom link types, modify schemas |
| **skills/2-stage-lifecycle-customization** | Customize stages, states, stage diagrams, and lifecycle flows for work items |
| **skills/3-data-upload-and-org-build** | Upload artifacts, bulk-create records, build fresh orgs from scratch (ordered: schemas → parts → Trails → links → work) |
| **skills/4-dashboards-and-widgets** | Router to `dashboard-dev` plugin commands (`/create-dashboard`, `/modify-dashboard`) |
| **skills/5-datasets** | Router to `dataset-builder` plugin commands (`:setup`, `:explore`, `:create`, `:update`, `:delete`, `:test`, `:validate`) |
| **skills/6-workflows** | Author, test, and manage DevRev workflows and agent-callable skills (templates, schemas, examples, trigger script) |
| **skills/7-agent-building** | Build, configure, test, and debug AI agents (configs, guardrails, skills, knowledge sync, annotations, internal API) |
| **skills/8-devrev-api** | Direct DevRev REST API access — complete endpoint catalog + domain guides for all public API groups |

## Plug-and-play acceptance summary

From a fresh machine with git + gh auth + Claude Code installed:

1. Clone this repo.
2. Create `.env` (one line: `DEVREV_PAT=<your_token>`).
3. Start a Claude Code session, accept the trust prompt.
4. Wait ~1 minute for background installs.
5. Start a second session for PATH refresh.

**Fully operational.** Nothing else manual. No npm install, no build, no config files to hand-edit, no CLI to install separately (it auto-installs), no MCP server to run (it's hosted). The workspace auto-configures on every session start after that.

## Troubleshooting

| Symptom | Likely cause | Solution |
| --- | --- | --- |
| `command not found: dashboard-sync` | Install still running, or new session needed for PATH | Check `.claude/.auto-setup/install.log` for progress; if "OK" logged, start a new session to pick up `~/.local/bin` in PATH |
| Plugins missing (`/plugin` doesn't show `dashboard-dev` or `dataset-builder`) | Workspace-trust prompt not accepted, or plugins not loaded | Accept trust prompt; restart Claude Code; or run `/plugin marketplace update devrev-aai-plugins` to force reload. If the GitHub-source marketplace can't authenticate against the private repo, register the local clone once instead: `/plugin marketplace add ./repos/aai-skills` |
| 401 Unauthorized on API calls | Missing or invalid PAT in `.env` | Verify `.env` exists and `DEVREV_PAT` is a valid token; test with `curl -H "Authorization: Bearer $DEVREV_PAT" https://api.devrev.ai/ping` |
| Clone failures for repos | Missing GitHub access to devrev org repos, or `gh` not authenticated | Check `docs/CLONE_RESULTS.md` for error details; run `gh auth status` and ensure the authenticated account has read access to devrev org repos |
| `gcloud` / `bq` / `kubectl` commands fail | Ponos-path prerequisites missing (not auto-installed) | Run `/dataset-builder:setup` to check and configure; these are only needed for Ponos jobs, not PaaS datasets |
