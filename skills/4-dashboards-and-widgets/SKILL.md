---
name: dashboards-and-widgets
description: Use this skill when the user asks to "create a DevRev dashboard", "build a widget", "add a chart", "modify my dashboard", "dashboard layout", "verify the dashboard", or otherwise wants to build or work with analytics dashboards and widgets inside a DevRev org. Routes to the correct dashboard-dev plugin commands rather than duplicating their logic.
---

# DevRev Dashboards & Widgets

This skill routes dashboard and widget requests to the installed `dashboard-dev` Claude Code plugin (marketplace `devrev-aai-plugins`, registered in `.claude/settings.json` with GitHub source `devrev/aai-skills`; the clone at `repos/aai-skills` is the same code, kept for reading/grounding). The actual domain knowledge (widget JSON schema, 12-column grid layout rules, Meerkat aggregations, validation stages) lives in the plugin's own skills at `repos/aai-skills/plugins/dashboard-dev/skills/` — this file only routes.

> **Command-name note** (verified 2026-07-18 against the cloned plugin): the plugin's `commands/` folder contains exactly **two slash commands** — `create-dashboard.md` (frontmatter `name: dashboard-create`) and `modify-dashboard.md`. Their canonical namespaced form is `/dashboard-dev:dashboard-create` and `/dashboard-dev:modify-dashboard`; the unprefixed `/create-dashboard` and `/modify-dashboard` may also resolve depending on how the plugin is loaded. If the unprefixed form doesn't resolve in a session, fall back to the namespaced form (same command). Everything else in the plugin — `dashboard-planner`, `widget-development`, `dashboard-development`, `benchmark-*` — is a **plugin skill** (loaded via the Skill mechanism), not a slash command.

## Routing table

| User wants to... | Do this |
|---|---|
| Create a new dashboard from vague / prose requirements | First invoke the `dashboard-planner` plugin skill (writes `plans/<slug>.md`), then run `/dashboard-dev:dashboard-create plans/<slug>.md`. Or run `/dashboard-dev:dashboard-create <prose>` directly if requirements are already crisp. |
| Modify an existing dashboard | `/dashboard-dev:modify-dashboard` — not `dashboard-create` |
| Fix/debug a single widget, or create one standalone widget outside a dashboard | Load the `widget-development` plugin skill at `repos/aai-skills/plugins/dashboard-dev/skills/widget-development/SKILL.md` |
| Fix dashboard layout/format errors on an existing dashboard | Load the `dashboard-development` plugin skill at `repos/aai-skills/plugins/dashboard-dev/skills/dashboard-development/SKILL.md` |
| Verify an already-deployed dashboard visually | Invoke the `dashboard-verifier` agent |
| Contribute widgets or benchmark the pipeline | Load one of the `benchmark-contributor` / `benchmark-widget` / `benchmark-dashboard` plugin skills |

## HARD RULE: Never bypass the pipeline for new dashboards

**Never invoke `dashboard-development` or `widget-development` directly for a NEW dashboard**, and never hand-write widget JSON for new dashboards. The `/create-dashboard` command's pipeline is the only supported path for new dashboard creation:

1. Parse requirements
2. Scaffold `dashboards/<slug>/widgets/`
3. Parallel `widget-generator` agents create widget JSON
4. PostToolUse hook runs 3-stage validation:
   - Structure validation (schema conformance)
   - Semantic validation (logical consistency)
   - Live API validation (queries run against DevRev)
   - Auto-fix retries on failures
5. `dashboard-generator` assembles `dashboard.json`
6. `dashboard-sync dashboard create` deploys
7. `dashboard-verifier` agent does Playwright visual verification

This pipeline produces reliably valid output; bypassing it skips all validation and retry logic, leading to malformed widgets.

## Preconditions

Check these before routing to any dashboard command:

1. **`.env` with `DEVREV_PAT` + `DEVREV_ENDPOINT`**: Must exist in the workspace root. If missing, tell the user exactly what to put in it (create from `.env.example`) and STOP — never fabricate or guess a token.

2. **`dashboard-sync` CLI on PATH**: The bootstrap hook (`.claude/hooks/bootstrap-workspace.sh`) auto-installs it via pipx once `.env` exists. If `command not found`, the background install may still be running — check `.claude/.auto-setup/install.log`. A fresh session may be needed for PATH to pick up `~/.local/bin/dashboard-sync`.

3. **Plugins loaded**: Workspace trust must be accepted (activates the committed plugin marketplace in `.claude/settings.json`). If `/plugin` doesn't show `dashboard-dev` as installed, restart Claude Code or run `/plugin marketplace update devrev-aai-plugins`.

If any precondition is unmet, surface it to the user rather than proceeding — dashboard commands fail loudly (401s, `command not found`) rather than silently degrading.

## Why this indirection

The actual domain knowledge lives in `repos/aai-skills/plugins/dashboard-dev/skills/`. This file intentionally does not duplicate that content — it only routes and states the hard rules. Read the target skill's `SKILL.md` for the real implementation details.

## Background references (local)

| File | When to read it |
| --- | --- |
| `references/plugin-and-toolchain-overview.md` | Background on how the dashboard-dev toolchain works: plugin structure, the 7-step end-to-end flow, the local DuckDB/Parquet widget validator, federated skill architecture, manual preview surfaces |
| `references/widget-api-and-dashboard-json.md` | The raw `widgets.create`/`widgets.get` API shapes and dashboard JSON skeleton — for understanding what the pipeline produces (NOT for hand-writing widget JSON; the HARD RULE above still applies) |

## Field notes (live-learned; see docs/LEARNINGS.md)

Dated facts discovered while operating this domain — errors hit, restrictions found, behaviors that
differ from the references. Add entries via the `capture-learnings` protocol
(`.claude/skills/capture-learnings/SKILL.md`): one dated bullet per fact, with evidence. If a fact
*corrects* a reference doc, fix the doc in place too — this section is for knowledge that has no
better home or needs domain-level visibility.

- **2026-07-18 · Full `/create-dashboard` pipeline verified live end-to-end for the first time** — plan file → `widget-generator` agent → `dashboard-generator` agent → `dashboard-sync widget create` → `dashboard-sync dashboard create <file>` → confirmed via raw `POST /internal/dashboards.get?id=<DON>`. A single-widget metric dashboard passed structure/semantic/API validation on the first attempt, no fix iterations needed.
- **2026-07-18 · `dashboard-sync dashboard validate` takes a slug; `dashboard-sync dashboard create` takes a file path.** These sibling subcommands have inconsistent argument shapes — `validate <dashboards/slug-dir-name>` vs `create <path/to/dashboard.json>`. Passing a file path to `validate` or a slug to `create` fails with a clear but easy-to-miss usage error.
- **2026-07-18 · The command doc's documented `create` → `pull` sequence (create-dashboard.md Phase 7) does not work for a freshly-created dashboard.** `dashboard-sync dashboard pull <slug>` fails with "Dashboard '<slug>' not found locally" immediately after `dashboard create` — `pull` only works on a dashboard already known locally. The correct sequence is `dashboard-sync dashboard create <file>` → `dashboard-sync dashboard download <full-DON-id>` (not `pull`) to establish the local `meta.json`/`manifest.json` and pick up the platform-assigned ids.
- **2026-07-18 · `POST /internal/dashboards.get?id=<DON>` is a real, working raw-API read endpoint** for dashboard state (title, layout, widget references, timestamps) — useful as a lightweight verification alternative when Playwright/Chrome-remote-debugging isn't available. Not previously documented in `references/widget-api-and-dashboard-json.md`.
- **2026-07-18 · `dashboard-sync dataset list` takes ~6 minutes on first run (no cache), validating ~142 datasets sequentially at ~1.8s each with zero network stalls** — it's genuinely working, not hung, but easily exceeds a 120s timeout and looks stuck. A cache is written to `.cache/dataset_availability.json`; subsequent runs complete in ~2 seconds. Anyone scripting or agent-driving this command should budget for a long first call (5+ minutes) or pre-warm the cache once per workspace.
- **2026-07-18 · Playwright visual verification (Phase 8) requires Chrome already running with `--remote-debugging-port=9222` and a logged-in DevRev session** — this is an interactive-login precondition this repo cannot auto-satisfy in an unattended/headless test pass. Confirmed the pipeline's own documented fallback ("skip verification, recommend manual check") is the correct behavior when port 9222 has nothing listening — this is expected, not a bug.
- **2026-07-18 · The `dashboard-dev` plugin's own `SessionStart` hook (`check-workspace-config.sh`, which runs `dashboard-sync config init`) depends on the session's cwd being the workspace root at session start.** If a session starts elsewhere and later `cd`s into the workspace, `config.yaml` may never get generated automatically even though `.env` and the CLI are both present — running `dashboard-sync config init` manually from the workspace root fixes it immediately. Worth knowing before assuming the plugin's auto-config is broken.
