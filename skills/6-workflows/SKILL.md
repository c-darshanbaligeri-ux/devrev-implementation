---
name: workflows
description: Manage DevRev workflows end-to-end — create, author, modify, delete, list, inspect, publish, and trigger workflows and AI-agent-callable skills, all through DevRev API calls (the agent has no built-in workflow tool, so every action here is an HTTP request). Use this skill whenever a user wants to create a new workflow or automation, describes an "if this happens, do that" rule in natural language, wants to add/remove/reconnect steps in an existing workflow, wants to build an agent-callable "skill" that wraps an API, needs to debug why a workflow template failed to import, wants to trigger/test a workflow, or asks to list/show/inspect workflows — even if they don't say the word "workflow" explicitly (e.g. "notify someone when a ticket comes in", "let the agent look up order status", "add a step that...", "why won't this template import").
---

# DevRev Workflow Admin

You cannot create, edit, or delete a DevRev workflow directly — there is no built-in tool for it. Every action in this skill happens by calling the DevRev workflow API over HTTP. This skill covers two things that are easy to conflate but serve different purposes, and most real requests need both:

1. **Managing workflow objects** — the CRUD/lifecycle verbs: create a shell, add/edit/delete steps, publish, delete, list, trigger. → `references/manage-workflows-api.md`
2. **Authoring the workflow's content** — the actual JSON graph of steps, triggers, branches, loops, and data mappings that make the workflow do something. → `references/template-json-format.md`

For anything beyond a one-step workflow, **authoring a complete template JSON and importing it is far more reliable** than building the graph step-by-step through the API — DevRev's Workflow Builder UI has an **Import** option that takes a template JSON file directly. Reach for the raw step-by-step CRUD API (`references/manage-workflows-api.md`) mainly for: listing/inspecting existing workflows, triggering a published workflow, deleting one, or making a small targeted edit to one or two fields on an existing step. Reach for full template authoring whenever the user is describing a new workflow or a substantial change to an existing one.

## When not to use

- **Snap-in development** is out of scope for this repo. Snap-in *operations* (third-party namespaces) may still be referenced inside workflow templates by their namespace.
- **AI agent configuration** (creating/modifying agent configs, guardrails, knowledge sync, testing agents) → `skills/7-agent-building`.

## Step 0: Check what's available in your session

Before doing anything, check what tool you have for making HTTP requests (a shell with `curl`, an HTTP-capable MCP tool, etc.) and whether a token is available. Read `DEVREV_PAT` from the repo-root `.env` file (`DEVREV_TOKEN` is accepted as an alias for scripts that expect it). If `.env` is missing or `DEVREV_PAT` is not set, tell the user what's needed and stop — don't guess or fabricate a token.

## Step 1: Figure out which mode the request needs

Ask yourself: is the user describing **new behavior** ("when X happens, do Y", "let the agent fetch Z from this API"), or are they asking to **inspect/manage existing objects** ("show me workflow-130", "delete this workflow", "trigger it with these params")?

- New behavior, or a non-trivial edit → go to **Step 2 (Author)**.
- Inspect, list, trigger, or delete → go straight to `references/manage-workflows-api.md` and use the relevant endpoint. For triggering, prefer the bundled `scripts/trigger_manual_workflow.py` over hand-rolling the HTTP call — it already handles auth, payload shaping, and readable error messages.

Also figure out which **shape** of workflow this is:

- **Event-driven automation** (reacts to something happening in DevRev — a ticket created, a stage change, a timer) → standard template, covered fully in `references/template-json-format.md`.
- **Agent-callable skill** (something an AI agent invokes mid-conversation to fetch data or take an action and get a result back — "let the agent look up...", "give the agent a way to...") → the same template format, but with a specific four-block skeleton. Read `references/ai-agent-skill-pattern.md` **in addition to** `references/template-json-format.md` before building.

## Step 2: Author the template JSON

1. **Parse intent** — identify the trigger event (or, for an agent skill, the input parameters), the sequence of actions, any conditions/branching, and any loops.
2. **Look up operations** — find the correct `{namespace, slug}` and input/output schema for each operation you need:
   - Full lists: `operations/triggers.md` (145), `operations/actions.md` (245), `operations/controls.md` (8), `operations/blockings.md` (2)
   - Detailed field-level schemas for 130 operations: `operations/schemas/<slug>.md`, indexed at `operations/schema-index.md`
3. **Study examples before writing anything** — read the closest-matching file(s) in `examples/`. **Prioritize `working-*.json` files** — these are the ones confirmed to actually import successfully; the numbered files (e.g. `5216-...`) are real production templates but haven't been re-validated against the current schema rules. To read one:
   ```bash
   python3 -c "import json; d=json.load(open('skills/6-workflows/examples/FILE.json')); inner=json.loads(d['data']); print(json.dumps(inner, indent=2))"
   ```
4. **Build the full JSON** following `references/template-json-format.md` — this covers the wrapper envelope, step/port structure, all `input_values` value types, trigger filters, loops and variables, sleep/wait, Ask AI, HTTP, and the Code node, plus a full validation checklist. Read it now if you haven't already; don't try to reconstruct the format from memory or from the examples alone — several field-type rules (`uenum` needing `allowed_values`, `array` needing `base_type`, etc.) are import-breaking if missed and aren't obvious from looking at examples alone.
5. **Write the output** to `templates/<workflow_name>.json` in the user's working directory, and show them a summary of what it does (trigger, steps, branches) — not the raw JSON, unless they ask for it.
6. **Tell the user how to get it live**: import it via **Workflows → Import** in the DevRev app (`https://app.devrev.ai/?view=workflows`), or hand it to `references/manage-workflows-api.md`'s create/publish flow if they specifically want it built up through API calls instead.
7. **After the user confirms it imported/worked**, copy the template into `skills/6-workflows/examples/working-<descriptive-name>.json` and add a row to the table in `references/template-json-format.md`'s example list. This is how the skill gets better over time — every confirmed-working template becomes a pattern the next request can study.

## Debugging a failed import

Import errors are almost always one of a handful of known causes — check `references/template-json-format.md`'s validation checklist first, especially:
- `uenum` fields missing `allowed_values`
- `array` fields missing `base_type`
- `for_each` used where a dedicated `loop_over_*` operation exists (native-object loops need the dedicated op — `for_each`'s dynamic schema is unreliable)
- `invoke_code`'s `code` field using `literal` instead of `text_template`, or its `input_values` using `composite_value` instead of `composite_value_list`

If none of those match, compare the failing template's step structure line-by-line against the closest `working-*.json` example — the difference is usually a port schema or value-type mismatch.

## Reference index

| File | When to read it |
|---|---|
| `references/manage-workflows-api.md` | Any CRUD/lifecycle operation on a workflow object — create shell, list, get, delete, trigger, publish |
| `references/template-json-format.md` | Authoring or debugging the actual step graph inside a template — the bulk of the domain knowledge lives here |
| `references/ai-agent-skill-pattern.md` | The request is for an agent-callable skill rather than an automatic trigger-based workflow |
| `operations/*.md`, `operations/schemas/*.md` | Looking up an operation's slug or exact field names |
| `examples/*.json` | Studying real patterns before writing a new template |
| `scripts/trigger_manual_workflow.py` | Triggering any published workflow with a manual/API trigger step |
