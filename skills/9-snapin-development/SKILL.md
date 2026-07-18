---
name: snapin-development
description: Use this skill when the user asks to build, plan, update, or test a DevRev snap-in, AirSync connector, or integration — e.g. "build a HubSpot connector", "I need to sync Asana into DevRev", "plan an AirSync integration for X", "add pagination to the Trello connector", "test this snap-in end-to-end", "generate the metadata JSON for Y". Routes to the `devrev` (devrev-qk-agents) plugin's snap-in vertical (PM → Architect → Tester) rather than duplicating its logic; the plugin requires a one-time manual install (never auto-enabled — third-party org). Does NOT cover this plugin's own "Implementation" (dashboard) vertical — that conflicts with `skills/4-dashboards-and-widgets`'s hard rule and is explicitly excluded; see below.
---

# DevRev Snap-in Development

This skill covers snap-in and AirSync connector development end-to-end. It routes to the `devrev` Claude Code plugin (source repo `QK-SnapIn/devrev-qk-agents`, a third-party org, distinct from `devrev/aai-skills`). The actual domain knowledge (PRD/TDD templates, ADaaS SDK patterns, manifest structure, CLI workflow) lives in the plugin's own skills — this file only routes and states the hard rules. It's the one skill in this repo whose plugin isn't auto-activated: `.claude/settings.json` registers the marketplace but deliberately excludes the plugin from `enabledPlugins` (third-party org, manual trust boundary).

**Install is manual, one-time, and not auto-enabled** (unlike `dashboard-dev`/`dataset-builder`, which activate automatically): the marketplace source is registered in `.claude/settings.json`'s `extraKnownMarketplaces`, but `enabledPlugins` deliberately does not include it — auto-activating a third-party org's code on every session is a real trust boundary this repo doesn't cross silently. Before using any `/devrev:*` command below, the user runs:

```bash
/plugin install devrev@devrev-qk-agents
```

The repo also clones the source at `repos/devrev-qk-agents` (via `repos.txt`, same mechanism as `aai-skills`) purely for reading/grounding — never edit it in place; refresh only via the `update-repos` skill.

## Routing table

| User wants to... | Do this |
|---|---|
| Plan a snap-in or AirSync connector (gather requirements, PRD, TDD) | `/devrev:plan-snapin` |
| Build the deployable code (manifest, functions, extraction/loading workers) | `/devrev:build-snapin` |
| Test it (unit tests + UI automation) | `/devrev:test-snapin` |
| Modify an existing snap-in — 7 supported update types: add entity, add pagination, switch auth, add bidirectional loading, add attachments, add rate limiting, add nested children | `/devrev:update-snapin` |
| Generate `external_domain_metadata.json` / `initial_domain_mapping.json` standalone | `/devrev:generate-metadata` |
| Quick pattern/decision lookup (auth, pagination, rate limiting) without a full build | `/devrev:search-guide` |
| Report a mistake the plugin's agents made so it doesn't repeat | `/devrev:improve-skill` — see "Self-learning is plugin-scoped" below |
| Update the plugin itself to the latest version | `/devrev:update` |

## HARD RULE: Never bypass the PM → Architect → Tester pipeline

**Never hand-write snap-in code or a manifest directly, and never skip straight to `/devrev:build-snapin` for a new connector without a plan.** The pipeline exists because the Architect's 15 documented engineering decisions and mandatory API research (never hallucinated) are what make the generated code correct:

1. `/devrev:plan-snapin` — PM gathers requirements across 4 discovery rounds → feasibility check (does a native connector already exist?) → PRD → TDD with sequence/data-mapping diagrams → explicit user approval gate → structured handoff brief
2. `/devrev:build-snapin` — Architect consumes the handoff, web-researches the real external API (8 research areas: auth, endpoints, rate limits, pagination, errors, incremental sync, permissions, attachments), documents 15 technical decisions, and generates the complete project. **For AirSync connectors**, the Architect is required to clone the production Asana template and rewrite it (a hard rule, not an optimization — it exists because generating 20+ files from a blank scaffold produced unreliable output in the plugin's build history)
3. `/devrev:test-snapin` — Tester writes Jest unit tests (normalization, mapping, error handling, state, pagination; target 70%+ coverage), then drives a real UI automation pass (install → configure mapping → run sync → verify imported data field-by-field → test incremental sync)

Bugs flow back upstream, not sideways: code bugs → Architect, requirements bugs → PM, systematic/repeated agent errors → `/devrev:improve-skill`.

## Precondition: three MCP servers (manual opt-in — NOT auto-registered)

Snap-in commands (`build-snapin`, `update-snapin`, `generate-metadata`, `search-guide`) require MCP servers this repo does **not** wire into `.mcp.json` and the bootstrap hook does **not** auto-install — per this repo's guardrail against unattended network installs beyond the confirmed bootstrap (repos clone + `dashboard-sync` pipx install). The user must opt in explicitly, once, per project:

```bash
# Required for all snap-in build/update/metadata/search commands
claude mcp add snapin-builder --transport http -s project https://snapin-builder-mcp.onrender.com/mcp

# Required only for /devrev:generate-metadata (AirSync mapping validation)
claude mcp add airsync chef-cli mcp initial-mapping
```

A third MCP reference — "devrev-sdk MCP" (for checking `@devrev/ts-adaas` breaking changes after cloning the Asana template) — is named throughout the plugin's Architect skill/agent but its setup command is not documented anywhere in the plugin itself; treat it as **NOT VERIFIED** and tell the user to ask the plugin's maintainers rather than guessing a `claude mcp add` invocation for it.

The `airsync` MCP above is one specific mode of `chef-cli` (the DevRev AirSync mapping tool). The plugin's `build-snapin` command also references a separate mode — `chef-cli mcp` at `https://developer.devrev.ai/airsync/mcp` — for constructing `initial_domain_mapping.json`. Both are provided by the same `chef-cli` binary; if the user hits `chef-cli: command not found`, they need to install the AirSync tooling per DevRev's developer docs before the mapping/metadata commands work.

If a snap-in command reports the MCP server isn't connected, tell the user exactly which command above to run and STOP — never proceed without it (the commands themselves also self-check and refuse).

## Excluded: this plugin's "Implementation" (dashboard) vertical

The `devrev` plugin also ships a second vertical — Implementation PM/Architect/Tester — for building DevRev dashboards and widgets. **Do not route to it.** It has the Architect agent generate widget JSON directly by hand, which is exactly what `skills/4-dashboards-and-widgets`'s HARD RULE forbids in this repo (that skill's pipeline — parallel widget-generator agents → 3-stage validation with auto-fix retries → assemble → deploy → Playwright-verify — is the only supported path here, precisely because hand-authored widget JSON produces unreliable output). If a user's request sounds like dashboard/widget work, route to `skills/4-dashboards-and-widgets` instead, even if they phrase it using this plugin's command names (`/devrev:plan-implementation`, `/devrev:build-implementation`, `/devrev:test-implementation`). Those three commands and their three agents/skills exist in the cloned plugin but are out of scope for this repo — never invoke them.

## A native alternative already exists in this repo's other marketplace

`repos/aai-skills` (the `devrev-aai-plugins` marketplace, already registered for `skills/4` and `skills/5`) declares two more plugins relevant here: **`snap-in-dev`** (reference-only skill covering manifest/functions/event-source structure — no build pipeline, no PM/Architect/Tester agents) and **`connector-dev`** (declared in `repos/aai-skills/.claude-plugin/marketplace.json` as an AirSync connector-development plugin using the same `@devrev/ts-adaas` framework — but its source directory `plugins/connector-dev` is **missing from the actual clone** as of the SHA pinned in `docs/CLONE_RESULTS.md`; this is an upstream drift in `devrev/aai-skills` itself, not a fault in this repo). Until `connector-dev` actually exists in that clone, `skills/9-snapin-development` (this skill, routing to the separate `devrev-qk-agents` plugin) is the only working snap-in build pipeline in this repo. If `connector-dev` appears in a future `aai-skills` update, compare it against this skill's pipeline before recommending one over the other — don't assume superiority in either direction without reading both.

## Preconditions

1. **Plugin installed** (manual, one-time — see "Install is manual" above): `/plugin install devrev@devrev-qk-agents`. **Verified live 2026-07-18: this fails as written** — the upstream repo has no `.claude-plugin/marketplace.json` (see Field notes below), so the marketplace itself cannot be added, by any of `/plugin marketplace add QK-SnapIn/devrev-qk-agents`, `./repos/devrev-qk-agents`, or `./repos/devrev-qk-agents/devrev-agents`. A working install requires hand-authoring a local shim `marketplace.json` (with a relative, not absolute, `source` path) outside `repos/` and pointing it at `repos/devrev-qk-agents/devrev-agents`, plus fixing `plugin.json`'s `skills` array (each entry must be the skill's directory, not its `SKILL.md` file) in the shim copy. See Field notes for the exact workaround. After installing, **start a new Claude Code session** before expecting any `/devrev:*` command, agent, or skill to actually resolve — mid-session installs did not become invocable in the same session in this test pass.
2. **MCP servers connected** (see above) — required before any `build-snapin`/`update-snapin`/`generate-metadata`/`search-guide` call; not required for `plan-snapin` (pure requirements-gathering, no MCP tools called).
3. **DevRev CLI authenticated** (only needed at deploy time, not build time): `devrev profiles authenticate -o <org-slug> -u <user-email> --expiry 7`. This is separate from this repo's `.env`/`DEVREV_PAT` — the plugin's CLI workflow uses its own session-based auth, not the repo's REST API token.

If any precondition is unmet, surface it to the user rather than proceeding — snap-in commands fail loudly (explicit MCP-not-connected messages) rather than silently degrading.

## Self-learning is plugin-scoped, not this-repo-scoped

`/devrev:improve-skill` patches files **inside the cloned plugin** (`repos/devrev-qk-agents/...`), which this repo's own rule says never to edit (`repos/` is a read-only clone target). This is a genuine conflict between the plugin's own self-improvement design and this repo's "never edit `repos/`" convention. Resolve it this way: if `/devrev:improve-skill` proposes a patch, apply it to the **local working copy** at `repos/devrev-qk-agents/` (that copy is disposable — `update-repos` will overwrite it on refresh) and separately record the same learning as a dated bullet in this file's Field notes below, so the fix survives an `update-repos` refresh even though the plugin's own patch doesn't. If the fix looks durable and broadly useful, tell the user it's worth upstreaming as a PR to `QK-SnapIn/devrev-qk-agents` directly (see the plugin's own `CONTRIBUTING.md`).

## Why this indirection

The actual domain knowledge (PRD/TDD templates, discovery question banks, ADaaS SDK patterns, manifest structure, CLI/chef-cli workflow, Jest/UI-automation test patterns) lives in `repos/devrev-qk-agents/devrev-agents/skills/`. This file intentionally does not duplicate that content — it only routes, states the hard rules, and flags the two exclusions (dashboard vertical, unverified third MCP server) that a naive full-adoption would miss.

## Field notes (live-learned; see docs/LEARNINGS.md)

Dated facts discovered while operating this domain — errors hit, restrictions found, behaviors that
differ from the plugin's own docs, or `/devrev:improve-skill` patches applied to the local
`repos/devrev-qk-agents/` copy (see "Self-learning is plugin-scoped" above — record here too so the
fix survives an `update-repos` refresh). Add entries via the `capture-learnings` protocol
(`.claude/skills/capture-learnings/SKILL.md`): one dated bullet per fact, with evidence.

- **2026-07-18 · The upstream `QK-SnapIn/devrev-qk-agents` repo is missing `.claude-plugin/marketplace.json` entirely** (confirmed on `main`, all branches — `git ls-tree -r HEAD --name-only | grep -i marketplace` returns nothing). This means the documented install command in this file (`/plugin install devrev@devrev-qk-agents`) **cannot work as written** — `claude plugin marketplace add QK-SnapIn/devrev-qk-agents` fails with "Marketplace file not found," and `claude plugin install QK-SnapIn/devrev-qk-agents` (bypassing the marketplace) fails with "not found in any configured marketplace." Only `.claude-plugin/plugin.json` exists (both at repo root and under `devrev-agents/`). Worked around by hand-authoring a local shim marketplace.json (outside `repos/`, since `repos/` is never edited) with `source: "./devrev-agents"` (a relative path — an absolute path source triggers "source type your Claude Code version does not support"), then `claude plugin marketplace add <shim-dir>` + `claude plugin install devrev@<shim-marketplace-name>`. This is a real upstream gap, not something fixable in this repo without either (a) maintaining the shim indefinitely and re-pointing it after every `update-repos` refresh, or (b) upstreaming a `marketplace.json` PR to `QK-SnapIn/devrev-qk-agents`.
- **2026-07-18 · The upstream plugin's own `plugin.json` has a second bug**: its `skills` array lists paths straight to each `SKILL.md` file (e.g. `./skills/devrev-imp-architect/SKILL.md`) instead of the parent directory. Claude Code's plugin loader rejects this with `skills load failed ... path is a file; skills entries must be directories`. All 7 skills failed to load until each path was manually stripped of its trailing `/SKILL.md` segment in the local shim copy. `claude plugin list` still reported the plugin as `✔ enabled` even while every skill failed to load — check `claude plugin list`'s per-plugin error lines, not just the enabled/disabled status, to catch this class of failure.
- **2026-07-18 · After fixing both bugs above, `claude plugin details devrev@devrev-qk-agents` shows `Skills (7)` listed by name but `Agents (0)` and no commands**, even though `plugin.json` declares 7 agent files and 11 command files. Neither the Agent tool's subagent_type list nor the Skill tool's available-skills list exposed ANY of this plugin's 7 skills, 7 agents, or 11 commands in the session where the plugin was installed — `Agent({subagent_type: "devrev-imp-pm"})` returned "Agent type not found," and `Skill({skill: "devrev-imp-pm"})` returned "Unknown skill." **Root cause not fully confirmed but strongly suspected to be session-timing**: this repo's own docs already document an identical pattern for the `dashboard-sync` CLI ("a hook can't refresh the shell PATH of its own already-running session... start a new session") — plugin components installed/enabled mid-session likely require a fresh Claude Code session to actually load into the running process, the same way `enabledPlugins` changes normally take effect at session start. **This was not independently re-verified with an actual fresh session in this test pass** (the testing agent cannot restart its own session) — a future test pass should confirm by installing the plugin, then genuinely starting a new session before probing `/devrev:*` commands or the 7 skills/agents.
- **2026-07-18 · Net effect for now**: the `devrev`/`devrev-qk-agents` plugin's PM → Architect → Tester pipeline described in this file's "HARD RULE" section remains **unverified live** in this repo. Two real upstream packaging bugs were found and worked around locally (not fixable in `repos/`), and the plugin loaded cleanly per `claude plugin list`/`details`, but no command, agent, or skill from it was actually invocable within the same session it was installed in. If a user hits "command not found" or "unknown skill" for any `/devrev:*` surface right after installing, the fix is almost certainly the same as the dashboard-sync CLI case: **start a new session**.
