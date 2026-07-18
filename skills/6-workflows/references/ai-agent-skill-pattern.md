# AI Agent Skill Pattern (Agent-Callable Workflows)

Most templates covered in `template-json-format.md` are **event-driven workflows** — they start from a trigger like `ticket_created` and run automatically. This reference covers a different, narrower shape: a workflow that packages up an **agent-callable skill** — the thing an AI agent (e.g. a DevRev support agent) invokes mid-conversation to fetch data or take an action, then gets a structured result back from.

Use this pattern when the user's request sounds like "give the agent a way to look up X" or "let the agent call this API" rather than "when X happens, do Y automatically."

## The four-block skeleton

Every agent skill workflow has exactly this shape:

```
ai_agent_skill_trigger_1  (trigger — defines the skill's input schema)
        |
        v
ai_agent_skill_1           (block step — the skill's body/scope)
        |  block_start
        v
   [action step(s)]        (block_step_reference_key: ai_agent_skill_1)
        |
        v
set_ai_agent_skill_output_1  (block_step_reference_key: ai_agent_skill_1 — returns data to the agent)
```

1. **`ai_agent_skill_trigger`** (namespace `devrev`) — the entry point. Its `input_values.schema` (a `literal` composite) defines every parameter the agent can pass in — this is what shows up as the skill's argument list to the calling agent. Each field needs `description`, `field_type`, and UI metadata; mark truly required fields with `is_required: true`.

2. **`ai_agent_skill`** — a block/container step (like a loop body owner). It has a `block_start` output port and an `error` output port. All the real work steps set `block_step_reference_key` pointing at this step's `reference_key`. Its own `input_values` just pass through `agent_session_id`, `skill_call_id`, `skill_name` from the trigger's `agent_metadata`.

3. **One or more action steps inside the block** — typically an `http` call to an external API, or native DevRev actions (`get_ticket`, `create_ticket`, etc.). Each must set `"block_step_reference_key": "ai_agent_skill_1"` (or whatever the block step's ref key is). Reference the trigger's fields via `$get('ai_agent_skill_trigger_1', 'output').<field_name>`.

4. **`set_ai_agent_skill_output`** — also inside the block (`block_step_reference_key` set the same way). Its `outputs` field is a `list_value` of `composite_value_list` items, each `{key, value}` pair — this is the data structure the calling agent receives back. Reference upstream step outputs the normal way, e.g. `$get('http_1', 'output').body`.

## Key differences from event-driven templates

- **`labels` must include `"skill"`** at the top level (`inner.labels = ["skill"]`) — this is what makes DevRev list it as an agent skill rather than an automation.
- **The trigger has no `fields_to_watch` or `_filter`** — those are for event triggers reacting to object changes. Agent skill triggers just declare a parameter schema.
- **Everything after the block step nests under it** via `block_step_reference_key`, the same mechanical pattern used for loop bodies (see "Loops and Iteration" in `template-json-format.md`) — an agent skill is structurally a block, not a linear chain.
- **Description matters more here than in ordinary workflows.** The top-level `description` field is what an orchestrating agent reads to decide *when* to call this skill and *what* arguments to pass — write it like a tool description: identification modes, required vs optional params, edge cases, error conditions. See the worked example below for the level of detail that's actually useful.

## Building the URL/body dynamically from agent inputs

When the skill wraps an HTTP API, build the `url` (and `body`, if needed) as a single `jsonata_expression` that conditionally appends query params — don't hardcode a fixed query string, since not every param the agent could pass is always present:

```
'https://api.example.com/resource?type=' & $get('ai_agent_skill_trigger_1', 'output').type
  & ($get('ai_agent_skill_trigger_1', 'output').id ? '&id=' & $get('ai_agent_skill_trigger_1', 'output').id : '')
```

This keeps optional fields out of the query string entirely when the agent didn't supply them, instead of sending `&id=` empty.

## Worked examples

- `examples/working-ai-agent-skill-koi-booking.json` — a real, validated skill (`ride_details_skill_v3`) that wraps a booking-lookup REST API with five use-case modes. Study its top-level `description` field closely — it documents identification modes, case-sensitivity rules, and per-field defaults inline, which is exactly the density an orchestrating agent needs to call it correctly on the first try.
- `examples/ai-agent-skill-http-template.json` — a minimal generic skeleton: trigger -> block -> `http` -> output. Start here when scaffolding a brand-new agent skill before filling in the specifics.

To read either: `python3 -c "import json; d=json.load(open('skills/6-workflows/examples/FILENAME.json')); inner=json.loads(d['data']); print(json.dumps(inner, indent=2))"`

## Checklist (in addition to the general validation checklist)

1. Top-level `labels` includes `"skill"`.
2. Trigger's `input_values.schema` literal lists every parameter the agent can pass, each with a clear `description` and `tooltip` — these surface to the calling agent.
3. Every step after the block step sets `block_step_reference_key` to the block step's `reference_key`.
4. `set_ai_agent_skill_output` is present and its `outputs` list covers everything downstream logic (or the calling agent) will need.
5. The workflow's top-level `description` is written as a tool description for an LLM caller, not as internal documentation — be explicit about required/optional params, valid enum values, and what happens on error.
