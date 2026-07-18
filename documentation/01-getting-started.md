# 01 — Getting Started

## What this repo is (and isn't)

`devrev-implementation` is **not a software project you build** — there is nothing to compile or test.
It is an *operating environment* for Claude Code: domain skills + API reference files + cloned DevRev
toolchains + a hosted DevRev MCP connection. You open a Claude Code session inside it and ask for
DevRev implementation work in plain English; the repo's routing and reference material make the agent
precise, grounded, and safe.

**In scope**: end-to-end solution design (blueprint for a business problem), object/schema
customization, stage/lifecycle customization, data upload and org builds, dashboards and widgets,
custom datasets, workflows and agent-callable skills, AI agent building (Agent Studio), raw DevRev
REST API calls, **and snap-in / AirSync connector development** (via a routed third-party plugin,
manual one-time install, see the "Optional: snap-in development" section below).

## Prerequisites (fresh machine)

You need exactly three things already working:

1. **Git**
2. **GitHub auth with read access to the `devrev` org** — check with `gh auth status`. The toolchain
   repos (`devrev/aai-skills`, `devrev/dashboard-sync-cli`, `devrev/api-specs`) are private to the org;
   cloning and the CLI install both authenticate through your existing GitHub credentials. The fourth
   toolchain repo (`QK-SnapIn/devrev-qk-agents`) is a public third-party clone used by skill 9.
3. **Claude Code**

Homebrew is used to install `pipx` automatically if it's missing (macOS). Nothing else is assumed.

## Setup — the one manual step

```bash
git clone https://github.com/c-darshanbaligeri-ux/devrev-implementation.git
cd devrev-implementation
cp .env.example .env
```

Edit `.env` and paste your token:

```env
DEVREV_PAT=<your personal access token>
DEVREV_ENDPOINT=https://api.devrev.ai

# Optional — only needed for AI-agent building against DevRev's internal API (skills/7):
# ORG_PAT=<your org PAT>
```

Get a PAT from **DevRev → Settings → Account → Personal Access Tokens**.

Notes on token names (you don't need to do anything about these — just so you know):
- `DEVREV_PAT` is the canonical name. `DEVREV_API_KEY` is a synonym used by some plugins.
- Older scripts inherited from the source projects expect `DEVREV_TOKEN`; the agent aliases it
  automatically when running API calls (`export DEVREV_TOKEN="$DEVREV_PAT"`).
- `.env` is gitignored. It is the **only** place a real token ever lives.

## First session — what happens automatically

Start a Claude Code session in the repo folder. Two things happen:

**1. You get one trust prompt.** Accept the *workspace-trust* prompt. This activates the plugin
marketplace committed in `.claude/settings.json` (`devrev-aai-plugins`, sourced from
`devrev/aai-skills` on GitHub), which provides the `dashboard-dev` and `dataset-builder` plugins
and their slash commands.

**2. The bootstrap hook runs** (`.claude/hooks/bootstrap-workspace.sh`, wired as a SessionStart hook).
With `.env` present it:

| Step | What | How |
| --- | --- | --- |
| Workspace dirs | Creates `dashboards/`, `datasets/`, `plans/`, `logs/`, `templates/` | Instant, synchronous |
| Toolchain clone | Clones every repo in `repos.txt` into `repos/` (aai-skills, dashboard-sync-cli, api-specs, devrev-qk-agents) | Background, once; results appended to `docs/CLONE_RESULTS.local.md` (per-machine) — the curated `docs/CLONE_RESULTS.md` is the build-time snapshot |
| CLI install | Installs `pipx` (via Homebrew if missing), then `dashboard-sync` from `devrev/dashboard-sync-cli` | Background, once |
| CLI init | Runs `dashboard-sync init` once the CLI is on PATH | Next session start |
| Dashboard config | The `dashboard-dev` plugin's own hook generates `config.yaml` from `.env` | Automatic |

Everything backgrounds and logs to **`.claude/.auto-setup/install.log`** — session start is never blocked.
If `.env` is missing, the hook prints a one-line reminder and does nothing at all.

## Second session — why you need it

The CLI installs into `~/.local/bin`, and a running session can't refresh its own PATH. So after the
first session (give the background install a minute — watch `.claude/.auto-setup/install.log`),
**start a new session**. The hook then runs `dashboard-sync init` and from that point every session
start is an instant no-op. You're fully operational.

## Verifying the setup

Run these (or just ask the agent to verify):

```bash
# Token works?
curl -s -X POST 'https://api.devrev.ai/ping' -H "Authorization: Bearer $DEVREV_PAT" -d '{}'

# CLI installed?
dashboard-sync --version

# Toolchain repos cloned?
ls repos/           # expect: aai-skills, dashboard-sync-cli, api-specs, devrev-qk-agents
cat docs/CLONE_RESULTS.md          # curated build-time snapshot
cat docs/CLONE_RESULTS.local.md    # per-machine bootstrap output (if the hook has cloned anything on this machine)

# Plugins loaded? (inside Claude Code)
/plugin             # expect dashboard-dev and dataset-builder from devrev-aai-plugins

# MCP connected? (inside Claude Code)
/mcp                # expect "devrev" (hosted, https://api.devrev.ai/mcp/v1)
```

## Optional: the Ponos dataset path

Everything above covers 100% of skills 0–8 **except** Ponos (cross-org) dataset jobs, which need
`gcloud`/`bq`, the AWS CLI (SSO), and `kubectl`. These require interactive logins, so they are
deliberately **not** auto-installed. If you ever choose the Ponos path, run `/dataset-builder:setup`
— it detects what's missing and walks you through it. PaaS datasets (the common case) need nothing
beyond `.env`.

## Optional: snap-in development (skill 9)

Snap-in / AirSync connector development is fully in scope, but it lives behind a **manual one-time
opt-in** because it routes to a third-party plugin (`QK-SnapIn/devrev-qk-agents`, not `devrev/aai-skills`)
and needs 1–2 MCP servers this repo won't auto-install:

```bash
# 1. Install the plugin (marketplace already registered in .claude/settings.json — just not auto-enabled)
/plugin install devrev@devrev-qk-agents

# 2. MCP server required for all build/update/metadata/search commands
claude mcp add snapin-builder --transport http -s project https://snapin-builder-mcp.onrender.com/mcp

# 3. MCP server required only for /devrev:generate-metadata (AirSync mapping validation)
claude mcp add airsync chef-cli mcp initial-mapping
```

Then use `/devrev:plan-snapin` → `/devrev:build-snapin` → `/devrev:test-snapin`. See
`skills/9-snapin-development/SKILL.md` for the full pipeline. **Do not** use this plugin's own
`/devrev:plan-implementation`, `build-implementation`, `test-implementation` — they hand-write widget
JSON and are explicitly out of scope; dashboard work must go through skill 4.

## Next

- Tour of what's inside: [02 — Repository Tour](02-repository-tour.md)
- Start working: [03 — Using the Skills](03-using-the-skills.md)
