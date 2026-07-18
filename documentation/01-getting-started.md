# 01 — Getting Started

## What this repo is (and isn't)

`devrev-implementation` is **not a software project you build** — there is nothing to compile or test.
It is an *operating environment* for Claude Code: domain skills + API reference files + cloned DevRev
toolchains + a hosted DevRev MCP connection. You open a Claude Code session inside it and ask for
DevRev implementation work in plain English; the repo's routing and reference material make the agent
precise, grounded, and safe.

**In scope**: object/schema customization, stage/lifecycle customization, data upload and org builds,
dashboards and widgets, custom datasets, workflows and agent-callable skills, AI agent building
(Agent Studio), and raw DevRev REST API calls.

**Out of scope**: snap-in development (separate discipline, separate repo).

## Prerequisites (fresh machine)

You need exactly three things already working:

1. **Git**
2. **GitHub auth with read access to the `devrev` org** — check with `gh auth status`. The toolchain
   repos (`devrev/aai-skills`, `devrev/dashboard-sync-cli`, `devrev/api-specs`) are private to the org;
   cloning and the CLI install both authenticate through your existing GitHub credentials.
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
| Toolchain clone | Clones every repo in `repos.txt` into `repos/` (aai-skills, dashboard-sync-cli, api-specs) | Background, once; results appended to `docs/CLONE_RESULTS.md` |
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
ls repos/           # expect: aai-skills, dashboard-sync-cli, api-specs
cat docs/CLONE_RESULTS.md

# Plugins loaded? (inside Claude Code)
/plugin             # expect dashboard-dev and dataset-builder from devrev-aai-plugins

# MCP connected? (inside Claude Code)
/mcp                # expect "devrev" (hosted, https://api.devrev.ai/mcp/v1)
```

## One optional extra: the Ponos dataset path

Everything above covers 100% of the repo's capabilities **except** Ponos (cross-org) dataset jobs,
which need `gcloud`/`bq`, the AWS CLI (SSO), and `kubectl`. These require interactive logins, so they
are deliberately **not** auto-installed. If you ever choose the Ponos path, run
`/dataset-builder:setup` — it detects what's missing and walks you through it. PaaS datasets (the
common case) need nothing beyond `.env`.

## Next

- Tour of what's inside: [02 — Repository Tour](02-repository-tour.md)
- Start working: [03 — Using the Skills](03-using-the-skills.md)
