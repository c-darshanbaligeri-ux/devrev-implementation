---
name: snapin-development
description: Use this skill when the user asks to build, plan, update, or test a DevRev snap-in, AirSync connector, or integration — e.g. "build a HubSpot connector", "I need to sync Asana into DevRev", "plan an AirSync integration for X", "add pagination to the Trello connector", "test this snap-in end-to-end", "generate the metadata JSON for Y". Routes to the `devrev` (devrev-qk-agents) plugin's snap-in vertical (PM → Architect → Tester) rather than duplicating its logic; the plugin requires a one-time manual install (never auto-enabled — third-party org). Does NOT cover this plugin's own "Implementation" (dashboard) vertical — that conflicts with `skills/4-dashboards-and-widgets`'s hard rule and is explicitly excluded; see below.
---

# DevRev Snap-in Development

This skill fills the one gap `CLAUDE.md`'s Identity line names explicitly: "all DevRev implementation work **apart from snap-in development**." It routes to the `devrev` Claude Code plugin (source repo `QK-SnapIn/devrev-qk-agents`, a third-party org, distinct from `devrev/aai-skills`). The actual domain knowledge (PRD/TDD templates, ADaaS SDK patterns, manifest structure, CLI workflow) lives in the plugin's own skills — this file only routes and states the hard rules.

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
| Modify an existing snap-in (add entity, fix pagination, switch auth, add attachments) | `/devrev:update-snapin` |
| Generate `external_domain_metadata.json` / `initial_domain_mapping.json` standalone | `/devrev:generate-metadata` |
| Quick pattern/decision lookup (auth, pagination, rate limiting) without a full build | `/devrev:search-guide` |
| Report a mistake the plugin's agents made so it doesn't repeat | `/devrev:improve-skill` — see "Self-learning is plugin-scoped" below |
| Update the plugin itself to the latest version | `/devrev:update` |

## HARD RULE: Never bypass the PM → Architect → Tester pipeline

**Never hand-write snap-in code or a manifest directly, and never skip straight to `/devrev:build-snapin` for a new connector without a plan.** The pipeline exists because the Architect's 15 documented engineering decisions and mandatory API research (never hallucinated) are what make the generated code correct:

1. `/devrev:plan-snapin` — PM gathers requirements across 4 discovery rounds → feasibility check (does a native connector already exist?) → PRD → TDD with sequence/data-mapping diagrams → explicit user approval gate → structured handoff brief
2. `/devrev:build-snapin` — Architect consumes the handoff, web-researches the real external API (8 research areas: auth, endpoints, rate limits, pagination, errors, incremental sync, permissions, attachments), documents 15 technical decisions, generates the complete project (for AirSync: clones and rewrites the production Asana template rather than starting from a blank scaffold)
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

If a snap-in command reports the MCP server isn't connected, tell the user exactly which command above to run and STOP — never proceed without it (the commands themselves also self-check and refuse).

## Excluded: this plugin's "Implementation" (dashboard) vertical

The `devrev` plugin also ships a second vertical — Implementation PM/Architect/Tester — for building DevRev dashboards and widgets. **Do not route to it.** It has the Architect agent generate widget JSON directly by hand, which is exactly what `skills/4-dashboards-and-widgets`'s HARD RULE forbids in this repo (that skill's pipeline — parallel widget-generator agents → 3-stage validation with auto-fix retries → assemble → deploy → Playwright-verify — is the only supported path here, precisely because hand-authored widget JSON produces unreliable output). If a user's request sounds like dashboard/widget work, route to `skills/4-dashboards-and-widgets` instead, even if they phrase it using this plugin's command names (`/devrev:plan-implementation`, `/devrev:build-implementation`, `/devrev:test-implementation`). Those three commands and their three agents/skills exist in the cloned plugin but are out of scope for this repo — never invoke them.

## A native alternative already exists in this repo's other marketplace

`repos/aai-skills` (the `devrev-aai-plugins` marketplace, already registered for `skills/4` and `skills/5`) declares two more plugins relevant here: **`snap-in-dev`** (reference-only skill covering manifest/functions/event-source structure — no build pipeline, no PM/Architect/Tester agents) and **`connector-dev`** (declared in `repos/aai-skills/.claude-plugin/marketplace.json` as an AirSync connector-development plugin using the same `@devrev/ts-adaas` framework — but its source directory `plugins/connector-dev` is **missing from the actual clone** as of the SHA pinned in `docs/CLONE_RESULTS.md`; this is an upstream drift in `devrev/aai-skills` itself, not a fault in this repo). Until `connector-dev` actually exists in that clone, `skills/9-snapin-development` (this skill, routing to the separate `devrev-qk-agents` plugin) is the only working snap-in build pipeline in this repo. If `connector-dev` appears in a future `aai-skills` update, compare it against this skill's pipeline before recommending one over the other — don't assume superiority in either direction without reading both.

## Preconditions

1. **Plugin installed** (manual, one-time — see "Install is manual" above): `/plugin install devrev@devrev-qk-agents`. If `/devrev:*` commands don't resolve, check `/plugin` shows `devrev` installed; if the marketplace itself won't resolve, run `/plugin marketplace update devrev-qk-agents` or register the local clone once instead: `/plugin marketplace add ./repos/devrev-qk-agents`.
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

- _(none yet)_
