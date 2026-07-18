# examples/ — exact-filename index

All files are importable template JSON (envelope `{"templateVersion": "2.0.0", "data": "<stringified inner JSON>"}`).
`working-*` files are **confirmed to import successfully** — always study the closest one before authoring.
Numbered files are real production templates, not re-validated against current schema rules.
When a new template is confirmed working, add it here AND to the example table in
`../references/template-json-format.md` (the learning loop in SKILL.md).

To read one: `python3 -c "import json; d=json.load(open('<file>')); print(json.dumps(json.loads(d['data']), indent=2))"`

## THE DEFAULT starter for a new agent-callable skill / workflow / tool

**Whenever the user asks to create an "AI agent skill", "agent workflow", "workflow tool", or
"agent-callable skill", start from `default-ai-agent-skill-template.json`** — a minimal, importable
4-step scaffold (trigger → skill block → HTTP → output) that relies on operation defaults instead
of restating every port_schema. Rename `title` and `description`, wire the HTTP step's URL / method /
auth to the target external API, and adjust the output mapping in `set_ai_agent_skill_output_1`.
This is the shortest path from "user asks" to "importable template" — do not hand-author from scratch.

| File (exact) | Pattern |
| --- | --- |
| `default-ai-agent-skill-template.json` | **Default** minimal agent-skill scaffold — use this as the starting point for every new agent skill / workflow tool ask |

## Confirmed working

| File (exact) | Pattern |
| --- | --- |
| `working-ai-agent-skill-koi-booking.json` | Validated **agent-callable skill** (four-block, labels `["skill"]`) — see `../references/ai-agent-skill-pattern.md` |
| `working-csat-score-on-ticket-resolved.json` | HTTP + AI: ticket_updated → if_else → http → ask_ai → add_comment |
| `working-enhancement-replace-agent.json` | Code + update: invoke_code (Python regex) → update_enhancement |
| `working-invoke-code-sample.json` | Minimal invoke_code node pattern |
| `working-loop-variable-sample.json` | loop_over_* + init_variable/set_variable pattern |
| `ai-agent-skill-http-template.json` | Verbose agent-skill scaffold with full port_schemas restated inline — reference only; prefer the `default-*` template above for new work |

## Production references (not re-validated)

| File (exact) | Steps | Pattern |
| --- | --- | --- |
| `3592-Generate rca from pia-template.json` | 8 | Incident trigger → ask_ai → create_article, branching |
| `4392-Async opportunity review agent-template.json` | 2 | Simple trigger → action, labels `["agent_interaction"]` |
| `4441-Ticket escalator from customer message-template.json` | 11 | ask_ai → nested if_else → update + notify |
| `4505-Auto-update issue tcd as end of sprint date-template.json` | 3 | `fields_to_watch` + `_filter`, chained updates |
| `5040-Devrevu - enablement journey - poc emails-template.json` | 8 | Custom-object trigger, HTTP, sleep_for, third-party ops |
| `5158-Devrevu - enablement journey - mailing for non enablement journey users-template.json` | 43 | Long sequential flow: sleep_for + if_else + third-party email |
| `5216-Account segment missing notification-template.json` | 4 | Trigger → get → if_else → comment, `_filter` with stage check |
