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

**Two distinct shapes live in this skill — decide which one first**:

- **Generic workflow** — event-driven (e.g. `ticket_created` → notify) or manual/API-triggered
  automation that runs independently, no calling agent. No default scaffold; pick the closest
  `working-*.json` in `examples/` for the pattern (loop, HTTP + AI, invoke_code, etc.). Continue
  with the general steps below.
- **AI agent skill workflow** — the four-block shape (`ai_agent_skill_trigger` → `ai_agent_skill`
  block → action(s) → `set_ai_agent_skill_output`, `labels: ["skill"]`) that an AI agent invokes
  mid-conversation to fetch data or take an action, then gets a structured result back. **Always
  start from `examples/default-ai-agent-skill-template.json`** — a minimal importable scaffold —
  and customize per `references/ai-agent-skill-pattern.md` § "Default starter — use this every
  time". Never hand-author the four-block wiring from scratch: too easy to miss
  `block_step_reference_key`, the `$get('ai_agent_skill_trigger_1', 'output').<field>` reference
  shape, or `labels: ["skill"]`.

If the phrasing is ambiguous ("build a workflow that..."), ask once which shape the user means —
the two shapes have nothing in common structurally.

General steps (apply to both shapes, except that agent-skill authoring always begins by copying
the default template rather than composing from operation lookups):

1. **Parse intent** — identify the trigger event (or, for an agent skill, the input parameters), the sequence of actions, any conditions/branching, and any loops.
2. **Look up operations** — find the correct `{namespace, slug}` and input/output schema for each operation you need:
   - Full lists: `operations/triggers.md` (145), `operations/actions.md` (245), `operations/controls.md` (8), `operations/blockings.md` (2)
   - Detailed field-level schemas for 130 operations: `operations/schemas/<slug>.md`, indexed at `operations/schema-index.md`
3. **Study examples before writing anything** — for agent skills, read `default-ai-agent-skill-template.json` first, then a closer `working-ai-agent-skill-*.json` if one matches. For event workflows, prioritize `working-*.json` files — these are confirmed to import successfully; the numbered files (e.g. `5216-...`) are real production templates but haven't been re-validated against the current schema rules. To read one:
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

## Capturing new learnings

This skill already has two built-in learning channels — use them, plus the journal:

- **New import-failure cause** (not in the checklist above): add it to "Debugging a failed import"
  here AND to the validation checklist in `references/template-json-format.md`.
- **Confirmed-working template**: promote to `examples/working-<name>.json` + a row in
  `references/template-json-format.md`'s example table.
- **Operation schema surprise** (field the schema doc missed/got wrong): fix
  `operations/schemas/<slug>.md` in place.

In all cases also append a row to `docs/LEARNINGS.md` and commit — full protocol:
`.claude/skills/capture-learnings/SKILL.md`.

## Field notes (live-learned; see docs/LEARNINGS.md)

- **2026-07-18 — Step-by-step CRUD build works end-to-end, confirmed live.** Built and deleted two
  full workflows via raw API only (no import): a 4-step generic workflow
  (`enhancement_updated`→`if_else`→`invoke_code`→`update_enhancement`, mirroring
  `working-enhancement-replace-agent.json`) and a 4-block AI agent skill (from
  `default-ai-agent-skill-template.json`). `workflows.create`→`workflow-steps.create`(×N)→
  `workflow-steps.update`(×N to wire `input_values`/`next_steps`)→`workflows.get`/
  `workflow-versions.get` to verify→`workflows.delete`→`workflows.get` 404 to confirm gone. All
  worked as expected except the specific field-name corrections below.

- **`workflow-steps.create`'s `operation` field is a DON string, NOT `{namespace, slug}`.**
  Passing `{"namespace":"devrev","slug":"enhancement_updated"}` fails: `HTTP 400
  unexpected_json_type — expected: 'STRING', actual: 'OBJECT'`. The correct value is the full
  operation DON: `"don:integration:<shard>:operation/devrev.<slug>"`. This is a different rule
  from the *template JSON* format (`references/template-json-format.md`), where `{namespace,
  slug}` is correct — that shorthand is a template-authoring convenience, not what the raw CRUD
  API accepts. **Owning file**: this note + `references/manage-workflows-api.md` (fixed in
  place, see below).

- **The operation-DON shard must match the target org's shard, not the doc's example
  `dvrv-in-1`.** `references/manage-workflows-api.md` showed `don:integration:dvrv-in-1:...` as
  the pattern; on a `dvrv-us-1` org, using `dvrv-in-1` in the operation DON returns `HTTP 400
  id_not_found: object not found`. Discover the correct shard from the org's own DON prefix
  (visible in any existing object's `id`, or in `workflows.create`'s own response) and substitute
  it — don't copy the doc's example shard literally.

- **`workflow-steps.create` requires, in order: `workflow` → `name` → `operation` →
  `reference_key`.** Omitting any one gives a `missing_required_field` error naming exactly the
  next missing field, so build the body iteratively if unsure.

- **Wiring one step to the next uses `next_steps: [{port_name, next_step, next_port_name}]` on
  the *upstream* step via `workflow-steps.update` — the key is `next_step` (a full step DON
  string), NOT `next_step_reference_key`.** `next_step_reference_key` (used in the template-JSON
  wrapper format) returns `HTTP 400 invalid_field` at the raw API level; so do `next_step_id`,
  `step_reference_key`, and bare `reference_key`. Verified by elimination against a live
  `workflow-steps.update` call.

- **The AI-agent-skill block nesting field at the raw CRUD API level is `block_step` (a step
  DON), NOT `block_step_reference_key`.** The template-JSON wrapper format's
  `block_step_reference_key` (a `reference_key` string) is template-authoring shorthand only;
  passing it to `workflow-steps.create` at the raw API returns `HTTP 400 invalid_field`. Use
  `"block_step": "<block-step's-full-DON>"` instead. Confirmed live: building the four-block
  agent-skill shape (`ai_agent_skill_trigger`→`ai_agent_skill`→`http`→
  `set_ai_agent_skill_output`) step-by-step through the CRUD API required this substitution for
  both the `http` and `set_ai_agent_skill_output` steps, and the resulting
  `workflow-steps.get`/`workflow-versions.get` response confirms the nesting rendered correctly
  (`block_step` populated on both, absent on the trigger/block steps).

- **`invoke_code`'s `input_ports`/`output_ports` do NOT need to be sent on `workflow-steps.update`
  — the operation auto-populates a default static schema for them.** Sending `input_ports`
  explicitly (even copying the exact structure from `operations/schemas/invoke_code.md`) returns
  `HTTP 400 invalid_field: type` (the nested port `"type": "default"` field is rejected at this
  layer) or, with the type field stripped, `HTTP 400 bad_request: dynamic input ports are not
  supported`. Sending only `input_values` (code / input_values / output_schema) plus `next_steps`
  succeeds (`200`) and the resulting step already has fully-populated `input_ports`/`output_ports`
  matching the schema doc's shape. This only concerns the raw `workflow-steps.update` API — the
  template-JSON import path (`references/template-json-format.md`) that explicitly restates
  `input_ports`/`output_ports` is unaffected and still the documented approach for that path.

- **`workflows.update` accepts `labels` (array) and `description` (string) at the top level** —
  both persisted correctly on a live workflow (`labels: ["skill"]`, description text), confirming
  these are valid post-create fields for marking a workflow as an agent-callable skill without
  reconstructing the whole object.

- **Publishing correction, more precise than the existing note**: `workflow-versions.publish`
  fails with `HTTP 400 bad_request: "workflow ... is in Workflow_StatusEnumDraft state and cannot
  be published"` — this is the *workflow's* status (`draft`), not just the version's. No
  `workflows.deploy`/`workflows.activate`/`workflow-versions.deploy`/`workflows.publish` endpoint
  exists (all 404 `route not found`), and `workflows.update` rejects both `status` and `state` as
  top-level fields (`HTTP 400 invalid_field`). Confirms there is genuinely no API path to move a
  workflow out of draft — the DevRev UI's Deploy action is the only route, exactly as the existing
  doc says, but now with the exact error strings for both the publish attempt and the blocked
  update attempts.

- **Triggering a still-draft workflow returns `HTTP 400`, not `HTTP 404` as previously
  documented.** Built a minimal single-step `manual_trigger` workflow specifically to test this
  precisely (then deleted it — see below): `workflows.trigger` on a draft workflow (either an
  `enhancement_updated` event-trigger shape or a bare `manual_trigger` shape) returns `HTTP 400
  bad_request: "workflow ... is not active"`. The existing doc/CLAUDE.md claim of "404 on
  trigger" for an undeployed workflow does not match live behavior in this org — **correcting**,
  not just confirming, the prior finding. (A 404 does occur for `workflows.trigger` against a
  workflow ID that was already deleted — but that path returned `HTTP 500 internal_error` in this
  test, not a clean 404, which is a separate minor drift worth noting if hit again.)

- **`workflows.delete` → `workflows.get` cycle is clean and immediate.** `workflows.delete`
  returns `HTTP 200 {}` for both a full 4-step workflow and a single-step probe workflow; the
  immediately-following `workflows.get` on the same ID returns `HTTP 404 not_found` with a
  `debug_message` naming the deleted workflow's own DON. No propagation delay observed.

- **Operation-schema spot-check results**: `enhancement_updated`, `update_enhancement`, `if_else`,
  and `invoke_code`'s documented input/output field shapes in `operations/schemas/*.md` all
  matched what the live API actually returned/accepted for those operations (field names, types,
  required flags) — no drift found in the schema *content* itself. The drift found in this test
  round was entirely in `references/manage-workflows-api.md`'s CRUD-level field-naming
  assumptions (operation DON vs. `{namespace,slug}`, `next_step` vs. `next_step_reference_key`,
  `block_step` vs. `block_step_reference_key`), not in the 130 op schema files.
