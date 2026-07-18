# Overview — dashboard & widget creation tooling in DevRev

Background for the task in `START_HERE.md`. Sourced from DevRev's internal docs
(Agent Skills Marketplace, Building Dashboards Tech Talk, Widget Validator, the
architecture critique, and the Trigger Dashboard Agent guide). Use this to
understand what the repos should contain; verify against the cloned files.

---

## 1. dashboard-dev (the primary tool)

A Claude Code **plugin** that lets an AI agent build dashboards and widgets on
its own in a DevRev org. It lives in the **Agent Skills Marketplace** repo and is
installed via Claude Code's plugin system:

```
/plugin marketplace add devrev/aai-skills
/plugin install dashboard-dev@devrev-aai-plugins
```

After install, you provide DevRev credentials in a `.env`:

```
DEVREV_PAT=your_personal_access_token
DEVREV_ENDPOINT=https://api.devrev.ai
```

Then prompt in plain English, e.g.:

```
Create a dashboard that displays issues, grouped by account, and filtered by sprint.
```

### Plugin structure (standard across the marketplace)

```
plugin-name/
  .claude-plugin/plugin.json   # manifest
  commands/                    # slash commands
  agents/                      # sub-agents
  skills/                      # reusable Agent Skills
  scripts/                     # executable logic and validation
  hooks/                       # event hooks
  README.md
  CLAUDE.md
```

The marketplace repo (`devrev/aai-skills`) hosts several plugins; **dashboard-dev**
is the relevant one. Others: `snap-in-dev`, `dataset-builder`, `connector-review`.

### How it creates a dashboard (end-to-end flow)

1. **Planner skill** reads plain-English requirements (or a DOCX/PDF/XLSX/MD doc),
   fetches datasets and samples the data via CLI, caches them in the workspace,
   analyzes the data against the requirements, and writes a structured plan.
2. **create-dashboard command** reads that plan (a well-tested reusable prompt).
3. **Widget Generator agent** + **Widget Development skill** produce valid widget
   JSON per spec.
4. **Dashboard Generator agent** + **Dashboard Development skill** assemble the
   widgets into dashboard JSON.
5. **Hooks + validators**: a PreToolUse hook blocks bad writes; PostToolUse
   validates after. Structural checks catch syntax errors; semantic checks catch
   SQL and type issues.
6. **Dashboard Sync CLI** sends validate-then-create calls to the platform.
7. Result: a live dashboard persisted with real DON IDs, ready to render.

The generator agents are used for context isolation + an extra system prompt to
improve reliability. The flow can also run with just the skills (no sub-agents).

### Widget Validator (the reliability engine)

- Replicates DevRev's DuckDB validation pipeline **locally**.
- Generates SQL from the widget JSON, executes it via Node + DuckDB against
  cached **Parquet** files (real data), and emulates applying group-by and
  filters (e.g. "last 7 days") so the query is robust to dynamic WHERE clauses.
- Outputs `results.json`, the generated SQL, and any compiler errors; errors are
  fed back to the agent to self-correct — no human copy-paste loop.
- Guarantees: always-valid JSON (compiles with no SQL/binder/type errors),
  correct values, and filter/group-by robustness.

### Architecture note (federation)

The plugin uses a four-layer architecture — Commands (orchestration), Agents
(execution), Skills (knowledge, via progressive disclosure of `SKILL.md` +
`references/` + `examples/`), and Scripts (Python/Bash utilities). A proposed
"Federated Skill Architecture" moves shared logic (e.g. the SQL Generator) into a
`common/` core that is hydrated (copied at build time) into each plugin, because
Claude Code's install cache only copies the plugin dir containing `plugin.json`
(so runtime symlinks/`../shared` references break). Confirm the actual layout in
the cloned repo — it may or may not have adopted this yet.

---

## 2. trigger-dashboard-agent (in-org snap-in)

A DevRev **snap-in** that exposes the dashboard agent as a command runnable from
any object's internal discussion:

```
/trigger_dashboard_agent [connection-name] prompt
```

- Currently available in the **Dev0** org only.
- You configure it with a user-scoped connection storing a **PAT** that allows
  deploying into a target org (Dev0 or a customer org); up to 5 connections, with
  optional aliases. You must click "Enable for me" for connections to work.
- Snap-in settings: app.devrev.ai/devrev/settings/snap-ins/trigger-dashboard-agent

This snap-in is part of the DevRev snap-ins family (repo `devrev/devrev-snap-ins`).
After cloning that repo, search for the actual snap-in directory; note the real
path (or that it isn't in the public repo).

---

## 3. Manual builder surfaces (no agent)

For reference, dashboards/widgets can also be built by hand:

- Widget preview: `https://app.devrev.ai/<org-slug>/widget-preview`
- Dashboard preview: `https://app.devrev.ai/<org-slug>/dashboard-preview`
  (all widgets must exist in the org before assembling the dashboard here)

Both surfaces are a JSON editor + a live preview. See `API_AND_JSON.md` for the
JSON structure and the platform API endpoints the tooling ultimately calls.

---

## Source articles (DevRev knowledge base, for provenance)

- Agent Skills Marketplace — ART-32157
- Building Dashboards in DevRev, Tech Talk — ART-32402
- Widget Validator — ART-32597
- Architecture critique (federated skills) — ART-32578
- How to Trigger Dashboard Agent — ART-30956
- Product Mastery Structure (dashboard/widget JSON, preview URLs) — ART-18387
- Create Widget API — ART-33145
- MELTS dashboard recommendations for Claude Code plugins — ART-32218
