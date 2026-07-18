# DevRev Workflows, Automation & Snap-ins

Use this reference for the **automation layer** of a solution — anything that reacts to events, runs on a schedule, orchestrates multi-step logic, or extends the platform with custom code. Mental model: **workflows are the recipe (deterministic); agents are the chef (probabilistic).** Master workflows before reaching for agents.

## Table of contents
1. What workflows are
2. Node types (the four operation types)
3. Trigger types
4. Data flow, variables, expressions
5. Automations / rules vs full workflows
6. Snap-ins & the snap-in framework
7. Integration boundaries (workflow / MCP / AirSync)
8. Decision guide + common patterns

---

## 1. What workflows are

A workflow is a series of triggers, actions, and conditions depicted as a flowchart: "if this happens → check that → then do this." Built at **Settings > Workflows** on a no-code drag-and-drop canvas with **160+ native nodes**.

Characteristics:
- Event-driven; reacts to DevRev events in real time.
- Deterministic logic + AI decisions in one canvas (via the Ask AI node).
- Long-running / durable — can pause for days/weeks/months (approvals, renewal dates); runs resume from checkpoints.
- No middleware — the engine is native to the system of record.
- Scalable (millions of executions/day).
- Natural-language generation — describe an automation in plain English and get a workflow.

Object model:
| Concept | Analogy | What it is |
|---|---|---|
| Operation | Class / blueprint | Reusable definition: input/output schema + logic. |
| Workflow | Program | Composition of steps with control + data flow (the canvas). |
| Step | Object instance | An operation placed with specific config. |
| Run | Process | A single execution from one event. |

Steps have typed **input/output ports**; data travels along connections (edges). Lifecycle: Draft → Active. Version control with rollback; in-flight runs stay on their old version during publish. Observability: per-run step trace (Runs tab), analytics page (run counts, error hotspots), log streaming to Datadog/OTLP. `While` loops cap at 1000 iterations.

---

## 2. Node types (the four operation types)

Four categories: trigger nodes (object-event, SLA/metric, feedback, sync, and control triggers like `TIMER_TRIGGER`/`API_TRIGGER`/`MANUAL_TRIGGER`/`AI_AGENT_SKILL_TRIGGER`), action nodes (create/update/delete objects, get/list, linking, communication, AI/intelligence, external/code, data/analytics, knowledge store, SLA/metrics, assignment/utility, loop-over batch), control nodes (`IF_ELSE`, `ROUTER`+Merge, `FOR_EACH`/`WHILE`, `GO_BACK`, variables), and blocking nodes (`SLEEP_FOR`/`SLEEP_UNTIL`/`WATCH_TICKET_FOR_UPDATES`). The **Ask AI node** embeds LLM reasoning as a step (Prompt + Mode Normal/Reasoning + Output Format) — use only where the outcome is non-deterministic; never for tasks a Code/Regex/If-Else node can do (the "AI overage" anti-pattern).

→ The full, field-schema-annotated catalog (145 triggers + 245 actions + 130 ops with resolved I/O schemas — strictly larger and more precise than any curated node list, including exact input/output ports per node): `../../6-workflows/operations/{triggers.md,actions.md,schema-index.md}`.

---

## 3. Trigger types

- **Object events** — created/updated/linked; stage changes surface via `*_UPDATED` (filter in trigger config or a following If/Else). Filter which events fire by group/part/priority.
- **Timers/schedules** — `TIMER_TRIGGER` interval + cron for periodic reports, maintenance, batch processing.
- **API triggers** — start via authenticated HTTP POST with typed input params; require a PAT/connection. One workflow can trigger another via the HTTP node → target's API trigger (modular sub-workflows).
- **HTTP node** — outbound REST; provide a sample response to auto-generate a downstream schema.
- **Forms & interactive** — `SEND_FORM`, `NUDGE_BUTTONS_CLICKED`, `ASK_OPTIONS`.

**Known gap:** `workflows.create` API produces a workflow shell only — node wiring is still a manual UI step. For fully code-defined scheduled automation with zero UI, use a snap-in `timer-events` cron path instead.

---

## 4. Data flow, variables, expressions

Port-based architecture: output of a step connects to the input of the next; you can reference only upstream data. Expression language is JSONata (`$get('step_ref').field`) plus text templates. Use step outputs by default; use a variable when you must collect across loop iterations, carry a value past a merge, count/increment, or build a string.

→ Full JSONata/template syntax, variable init/mutate mechanics, and deployment-tested gotchas (e.g. `uenum` missing `allowed_values`, array missing `base_type`, `for_each` vs. `loop_over_*` choice, `invoke_code`'s template-vs-literal requirement) that break imports if missed: `../../6-workflows/references/template-json-format.md`.

---

## 5. Automations / rules vs full workflows

DevRev has no separate legacy "rules engine" — the workflow engine IS the automation/rules engine. Simpler rule-style automations are expressed as workflows or as **Automate snap-ins** (packaged code-defined rules: auto-reply, CSAT survey, spam detection, SLA breach alert, auto-assignment, escalation).

- **SLAs** are modeled as metric trackers. Workflows react to `*_SLA_TRACKER_UPDATED` and manage state with `EXECUTE_METRIC_ACTION`. "Operational SLA Metrics" and "SLA change notifier" snap-ins package common SLA automations.
- **Assignment / round-robin** — the `PICK_USER` node picks from a group by strategy; triggered by `*_CREATED` + `UPDATE_*` to assign. Round-robin state tracked as objects.

Rule of thumb: a single "if event then one action" need can be a small workflow or an Automate snap-in; anything multi-step, branching, long-running, or cross-system is a full workflow.

---

## 6. Snap-ins & the snap-in framework

Snap-ins are collections of DevRev objects that extend the platform at arm's length — serverless, event-driven TypeScript modules running inside DevRev infrastructure. Deployed via the DevRev CLI; version-controlled; publishable to the Marketplace.

Three categories:
- **Automate** — tasks inside DevRev on events (auto-reply, CSAT, spam, SLA alerts, escalation).
- **Integrate** — connect DevRev with external tools two-way (Slack, Datadog, GitHub, Jira, PagerDuty).
- **AirSync** — import & synchronize external data into the Knowledge Graph.

Core object model:
- **Package** → declarative blueprint. **Package version** → the definition/source. **Installed snap-in** → an active instance with configured inputs + keyrings + a service account.
- **Manifest** (`manifest.yaml`) declares: `service_account`, `inputs`, `keyrings`, `event_sources`, `functions`, `automations`, `operations`, `commands`, `hooks`, `snap_kit_actions`, `tags`.

Key sub-components:
- **Automation** — links an event source to a function.
- **Event sources** — `devrev-webhook` (DevRev events), `flow-custom-webhook`/`flow-generic-events` (external webhooks with policy logic), `timer-events` (cron — the go-to for code-defined scheduled jobs), `email-forward`.
- **Keyrings (Connections)** — secure credential storage; scopes: organization / user / developer. OAuth tokens auto-refresh.
- **Functions** — JS/TS code; receive `payload`, `context` (service account token, secrets), `input_data` (keyrings, event sources).
- **Operations / 3P nodes** — single-purpose reusable **workflow nodes** contributed by a snap-in. Once deployed, they surface as nodes in the workflow builder — the primary way to extend the node library.
- **Commands** (slash commands), **Hooks** (install lifecycle), **Snap-kit actions** (interactive UI on issue/portal/comments/plug).

Relationship: **Snap-ins → Workflow Nodes → Agent Skills** (complementary, not competing).

---

## 7. Integration boundaries

- **HTTP node / webhooks** — outbound REST from workflows; inbound via snap-in event sources or API triggers.
- **MCP** — best for quick federated search and real-time actions during a conversation. NOT for deep research, complex structured queries, or analytics. DevRev provides an extensible MCP gateway (native + custom tools; whitelisted external MCP servers).
- **AirSync** — patented bidirectional sync that copies external data (with permissions) into DevRev for deep research, analytics, joins, and history. Periodic + real-time; can trigger workflows on synced data. See `integrations-channels.md`.

---

## 8. Decision guide + common patterns

Core principle: **if it can be done deterministically without tradeoff, make it a workflow (callable skill). Use AI only where it adds value.**

Three-way rule of thumb:
- Single deterministic API call, no payload reasoning → **Tool** (native).
- Fixed multi-step sequence, deterministic → **Workflow**.
- Complex code / external OAuth / data transform / deep branching (>3–4 levels) → **Custom Operation (snap-in)**, ideally as a workflow node.
- Needs judgment about when/how, routing, contextual awareness → wrap as a **Skill** on an **Agent**.

AI vs deterministic examples:
| Scenario | Approach | Why |
|---|---|---|
| Route ticket to team by product area | Workflow | Clear mapping rules |
| Classify ticket bug vs feature request | AI | NL nuance |
| Send notification on SLA breach | Workflow | Fixed trigger/action |
| Determine if a customer is frustrated | AI | Tone/context interpretation |
| Create ticket from fields in a conversation | Hybrid | AI extracts → workflow creates |
| Escalate by account tier + severity | Workflow | Explicit rules |
| Summarize a long thread | AI | Language understanding |

The **hybrid pattern** (most common & effective): AI extracts + deterministic workflow executes. The AI owns understanding/extraction; the workflow owns reliable execution.

Common workflow patterns:
1. Auto-assignment: `TICKET_CREATED → IF_ELSE(priority) → PICK_USER → UPDATE_TICKET`
2. Escalation: `TICKET_UPDATED → IF_ELSE(SLA) → SEND_NOTIFICATION → UPDATE_TICKET`
3. Batch: `TIMER_TRIGGER → LOOP_OVER_TICKETS → UPDATE_TICKET`
4. Approval: `ISSUE_CREATED → TALK_TO_AGENT → IF_ELSE(approved?) → UPDATE_ISSUE`
5. Integration: `API_TRIGGER → HTTP → CREATE_TICKET`
6. AI classification: `TICKET_CREATED → CLASSIFY_OBJECT → UPDATE_TICKET(category)`
7. Sentiment routing: `CONVERSATION_CREATED → EVALUATE_SENTIMENT → IF_ELSE → SEND_NOTIFICATION`
8. Scheduled reminder: `TICKET_CREATED → SLEEP_FOR(24h) → GET_TICKET → IF_ELSE(still open?) → SEND_NOTIFICATION`
9. KB index: `ARTICLE_CREATED → KNOWLEDGE_STORE_INDEX → SEND_NOTIFICATION`
10. Multi-path: `TICKET_CREATED → ROUTER → [parallel paths] → Merge`

Anti-patterns to avoid: AI for deterministic tasks; a snap-in for simple CRUD (use a native tool); a skill that just calls one tool with no logic (attach the tool directly); fat system prompts with business logic (move to skills); too many knowledge sources.
