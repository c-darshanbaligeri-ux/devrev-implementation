# Patterns & Recipes: Reusable Designs

Battle-tested building blocks to compose into solutions. Reach here after the decision frameworks tell you *which* primitive — this tells you *how* to shape it. Covers workflow node config, workflow recipes, expression snippets, snap-in patterns, agent patterns, and merge/loop mechanics.

## Table of contents
1. Per-node config quick reference
2. Workflow recipes (full node sequences)
3. Expression language snippets (JSONata + templates)
4. Merge, loop & variable mechanics
5. Snap-in implementation patterns
6. Agent design patterns
7. Workflow-as-agent-skill wiring
8. Documented limits & gotchas

---

## 1. Per-node config quick reference

Covers the shape of the nodes most solutions need: `IF_ELSE`/`ROUTER` (branching), `PICK_USER` (assignment), `ASK_AI`/`CLASSIFY_OBJECT`/`EVALUATE_SENTIMENT`/`SUGGEST_PART`/`OBJECT_SPAM_CHECKER` (AI/intelligence), `SEND_NOTIFICATION`/`ADD_COMMENT`/`SEND_FORM` (communication), `CREATE_*`/`UPDATE_*` object nodes, `TALK_TO_AGENT`/`ASK_AGENT` (agent handoff), `SLEEP_FOR`/`SLEEP_UNTIL`/`WATCH_TICKET_FOR_UPDATES` (blocking), `GET_TIME`, `EXECUTE_CODE`/`RUN_CODE`, `HTTP`, and the `LOOP_OVER_*` batch iterators (sequential, max 1000 items).

→ Exact per-node input/output field schemas (every port, every field, every enum value — field-schema-annotated across 130 ops): `../../6-workflows/operations/schema-index.md` and the individual files it indexes.

---

## 2. Workflow recipes (full node sequences)

1. **Auto-assignment:** `TICKET_CREATED → IF_ELSE(priority) → PICK_USER(group, round-robin) → UPDATE_TICKET(owned_by=$get('pick_user').user) → ADD_COMMENT`
2. **Escalation:** `TICKET_UPDATED / *_SLA_TRACKER_UPDATED → IF_ELSE(SLA breached?) → SEND_NOTIFICATION(team) → UPDATE_TICKET(priority)`
3. **Triage / auto-classify:** `TICKET_CREATED → OBJECT_SPAM_CHECKER → CLASSIFY_OBJECT(categories) → SUGGEST_PART → UPDATE_TICKET(subtype/part) → ROUTER(by category) → PICK_USER`
4. **Sentiment routing:** `CONVERSATION_CREATED → EVALUATE_SENTIMENT → IF_ELSE(frustrated/unhappy?) → SEND_NOTIFICATION / route to senior group`
5. **Approvals (race):** `Trigger → MERGE branches[manager, peer, on_call] var approved_by, timeout 24h → each branch Ask/Talk-to-Agent → SET approved_by → block_callback` (first responder wins); after: `if _timeout → escalate`
6. **Scheduled batch:** `TIMER_TRIGGER(cron "0 9 * * Mon") → LOOP_OVER_TICKETS(filter open>7d) → ADD_COMMENT / UPDATE_TICKET`
7. **Scheduled reminder:** `TICKET_CREATED → SLEEP_FOR(24h) → GET_TICKET → IF_ELSE(still open?) → SEND_NOTIFICATION`
8. **Integration intake:** `API_TRIGGER(web form) → HTTP(enrich) → CREATE_TICKET → SEND_NOTIFICATION`
9. **AI-hybrid routing:** `TICKET_CREATED → ASK_AI(classify intent/tier, structured out) → ROUTER → group`
10. **Deflection / conversational:** `CONVERSATION_CREATED → TALK_TO_AGENT(agent, external, CustomerChat)`
11. **Convert & converge (support→eng):** `CONVERSATION_CREATED → assign rep → (rep) CONVERT_CONVERSATION_TO_TICKET → SUGGEST_PART → CREATE_ISSUE → LINK_TICKET_WITH_ISSUE(is_dependent_on)`
12. **Document chase:** `<obj> enters "Awaiting Docs" → SEND_FORM → SLEEP_FOR(48h) → GET(obj) → IF_ELSE(docs complete?) → loop reminder up to 3× → flag ops`

---

## 3. Expression language snippets

**JSONata** (single value):
```
$get('step_ref')                         // default output port
$get('step_ref','port').field            // specific port
$get_variable('var_step_ref','name')     // workflow variable
$get('http_call').response.data.title    // nested
$get('trigger').a & '-' & $get('trigger').b   // concat
$get('step').items[0]                    // array index
$get('for_each','block_start').item      // current loop item
$get('create_issue','error').message     // error port
$distinct($append($get('t','custom_fields').rocks, $get('t','custom_fields').pebbles))  // merge arrays
```

**Text templates** (interpolated string):
```
"Ticket #{% expr $get('ticket').display_id %} - {% expr $get('ticket').title %}"
"Value: {% expr $get_variable('init_variable','counter') %}"
"Error: {% expr $get('action','error').message %} ({% expr $get('action','error').type %})"
```
UI: type `{{` or click **Insert variable** to pick `Node > output > field`.

---

## 4. Merge, loop & variable mechanics

**Merge** convergence is **first-wins ("any of")** — the first branch's callback completes the merge and abandons the rest; **"all of" is NOT supported**. Branch names must be unique and identifier-safe; shared variables need defaults (losing branches leave defaults). **FOR_EACH/Loop Over/WHILE** all cap at **1000 items**, run sequentially. Variables: use step outputs by default; use a variable to collect across iterations, carry a value past a merge, count/increment, or build a string.

→ Exact field names (`branches[]`, `timeout`→`_timeout`/`_timeout_at`, `$get('<merge>','<branch>').<var>` read syntax) and variable init/mutate mechanics: `../../6-workflows/references/template-json-format.md`.

---

## 5. Snap-in implementation patterns

Eight canonical patterns (distilled from 400+ production snap-ins):
1. **Integration** — bidirectional sync with an external system (event source + functions + keyrings).
2. **Automation** — event-driven action inside DevRev (`devrev-webhook` + automation + function).
3. **3P Node** — a reusable workflow node (`operations` in the manifest); surfaces in the workflow builder once deployed.
4. **Notification** — push updates to an external channel (Slack/email/webhook).
5. **Survey/Feedback** — collect and record responses (e.g. CSAT).
6. **Timer/Scheduler** — `timer-events` cron for periodic jobs (the go-to for fully code-defined scheduling; the workflow API only creates a shell).
7. **Multi-Platform** — one snap-in fanning out to several systems.
8. **Custom-object storage** — persist function results in custom objects/fields the snap-in defines.

Manifest v2 sections: `service_account` (identity + scopes), `inputs` (org/user config), `keyrings` (org/user/developer), `event_sources`, `functions`, `automations` (source+event_types→function), `operations` (3P nodes), `commands` (slash), `hooks` (activate/update/deactivate/validate), `snap_kit_actions` (UI), `tags`, `imports` (ADaaS only).

Event source types: `devrev-webhook` (DevRev events + JQ filter), `flow-custom-webhook` (external + Rego validation), `flow-events` (self-dispatched/deferred), `timer-events` (cron/interval → `timer.tick`), `email-forward` (`email.receive`). Cron examples: `*/5 * * * *`, `0 * * * *`, `0 9 * * 1-5`, `0 0 1 * *`.

Keyrings: organization (shared), user (per-user, always optional), developer (hidden, cross-install). Referenced in functions via `event.input_data.keyrings['name'].secret` (or `.access_token` for OAuth); service-account token at `event.context.secrets.service_account_token`.

Named marketplace snap-ins to reuse rather than build: Auto-reply, CSAT (conversation/ticket), Spam Shield, Smart issue creator, Sentiment evaluator, SLA change notifier, Operational SLA Metrics, Ticket email notifier (SendGrid), Auto-assignment, Convergence (support automations), Account deduplication, Search Node, Workflow Generator, Search Agent, Slack/WhatsApp/Twilio/Datadog/PagerDuty/GitHub/Jira/Harness integrations.

---

## 6. Agent design patterns

Five patterns — start simple, escalate only when the simpler one demonstrably fails:
| Pattern | Flow | Constraint |
|---|---|---|
| Tool Use (default) | Input → select skill → execute → respond | 5–8 skills |
| ReAct | Think → Act → Observe → repeat | max_steps 3–5, timeout 30–60s, fallback = escalate |
| Plan-Execute | Plan → execute steps (parallel where possible) | Planner + Executor via Talk-to-Agent, or a single NL sub-agent |
| Reflection | Output → validate → refine | 1–2 iterations, ~2× cost |
| Multi-Agent Routing | Router classifies → specialists | Router classifies only; always define a default route |

**Strong guidance:** Tool-Use / ReAct / Plan-Execute / Reflection can all be realized *inside a single agent via an NL sub-agent skill*. Reserve true multi-agent only for distinct domains needing different permissions, knowledge, or guardrails. A simple Tool-Use agent (lean prompt, one well-scoped search tool) often beats a complex multi-tool pipeline — the usual bottleneck is retrieval scoping, not the pattern.

NL sub-agent (API-only) three-layer model: **Skill Description** (≤1024 chars, always in context) + **Plan Guidance** (full prompt, loads on activation) + **Tools** (workflows/operations the plan calls). Sub-agents are stateless — they return results to the main agent.

---

## 7. Workflow-as-agent-skill wiring

A workflow becomes a skill by shaping it as: `Trigger (MANUAL_TRIGGER or AI_AGENT_SKILL_TRIGGER) → [action/control/AI nodes] → Agent Callback / Set Skill Output`.

- The **manual-trigger output-port schema defines the skill's input contract** (e.g. `agent_session_id`, `skill_call_id`, `skill_name`, plus your domain fields like `sql_query`).
- The **Agent Callback** node maps results back: session/call/skill ids from the trigger + `output` = the result step (`$get('step','output')`).
- In Agent Studio, **Configure** auto-builds the deployment workflow (`Conversation Created → Talk to Agent` on Plug); manual build gives full control.
- Skill registration overwrites all skills — always include existing ones.

→ The full four-block skeleton with worked examples and a build checklist: `../../6-workflows/references/ai-agent-skill-pattern.md`.

---

## 8. Documented limits & gotchas

- Per-node timeout ~30s (TALK_TO_AGENT 90s; Get Complete Enhancement Details 120s). Long external calls fail — split or optimize.
- Rate limit (429) → add a delay node or reduce trigger frequency.
- Error ports: branch off `error{message,type}`; GO_BACK enables retry loops. No global retry/backoff knobs — handle via error-port + GO_BACK.
- WHILE and Loop caps: 1000. Loops are sequential.
- Merge: "all of" unsupported; unique, identifier-safe branch names; shared variables need defaults.
- Deploy validations (block on error): no trigger, no step, disconnected step, if-else missing condition (warning), max depth 100 / circular reference, type mismatch, operation deleted (snap-in removed), missing required field.
- Conditions are case-sensitive/exact. Custom field must exist in the workspace or the node skips silently. Imported workflows lose snap-in nodes until the snap-in is installed.
- `workflows.create` API builds a **shell only** — node wiring is manual UI. For fully code-defined scheduling, use a `timer-events` snap-in.
- Agent hard limits: **16 guardrails**, NL-skill description **1024 chars**. 5–8 skills is guidance, not a hard cap. Knowledge-source count, max steps, timeouts, token budgets are **not documented** — don't assume numbers.
- Documented agent evaluators are **Correctness** and **Completeness** only; deflection/CSAT/groundedness are business metrics/roadmap, not built-in bulk-test evaluators. Canary deployment is claimed in marketing; only publish/archive/restore + suspend-on-message handoff are documented mechanics.
