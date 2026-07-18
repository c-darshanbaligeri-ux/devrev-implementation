# Extensibility Surfaces: PLuG, Custom Code, Widgets, Timeline, APIs & Webhooks

Use this reference when a solution needs to go beyond configuration into DevRev's developer/extensibility surfaces. The guiding rule is **native-first, configuration over customization**: reach here only when stock objects, workflows, and agents can't meet the need. See `references/decision-frameworks.md` for when that threshold is crossed.

## Table of contents
1. Native-first ladder
2. PLuG framework
3. TypeScript / JavaScript customizations (snap-in code)
4. Widgets & SQL / analytics
5. Timeline events
6. Custom actions & commands
7. APIs
8. Webhooks & event sources

---

## 1. Native-first ladder

Climb only as high as the requirement forces:
1. **Stock config** — objects, subtypes, custom fields, stages, groups/roles, stock dashboards. (Always try first.)
2. **Workflows** — deterministic orchestration on the no-code canvas.
3. **Agents & skills** — where judgment/conversation is needed.
4. **Snap-in code (TypeScript)** — custom operations, event sources, integrations when 1-3 can't do it.
5. **PLuG / front-end customization** — when the customer-facing widget experience must be tailored.
6. **APIs / webhooks** — for programmatic integration with systems outside DevRev.

Every step up adds build and maintenance cost. Justify each ascent in the blueprint.

---

## 2. PLuG framework

PLuG is DevRev's embeddable engagement widget (web + mobile SDKs) and the primary customer-facing surface for chat, self-service search, and proactive nudges. Configure appearance code-free in Settings > PLuG & Portal; go to code only for deeper needs.

- **Web:** `window.plugSDK.init({ app_id })` + `plug.js`. Identity: anonymous until identified; `identifyUnverifiedUser` / verified identity for authenticated experiences. `disable_plug_chat_window` to run search-only.
- **Mobile SDKs:** iOS, Android, React Native, Flutter, Expo — `DevRev.showSupport()`, `DevRev.createSupportConversation(prefillMessage:)`, device-token registration for push (FCM/APNs).
- **Capabilities delivered through one SDK:** AI chat (agent), live chat, KB semantic search, nudges (proactive outbound), and session replay/observability (recordings, API calls, errors, rage clicks, funnels) linked to tickets.
- **Multiple instances:** different website paths can host separate PLuG instances (each with its own KB/appearance) via multiple dev orgs.
- **When to customize PLuG (code):** bespoke branding beyond the style panel, embedding in a complex SPA, custom identity flows, or driving the widget programmatically (open/prefill/route by app state). Size these Medium-Large.

Design implication: for most solutions PLuG is a *configuration* choice (which channel, which agent, which KB). Treat custom PLuG development as an explicit line item only when the standard widget genuinely can't deliver the experience.

---

## 3. TypeScript / JavaScript customizations (snap-in code)

Custom code lives in **snap-ins** (serverless TypeScript/JS functions running in DevRev infra; see `references/workflows-automation.md` §6). Use it for:
- **Custom Operations** — a reusable workflow node encapsulating logic a native node can't do (complex transforms, external OAuth, multi-call orchestration). Deployed, it appears in the workflow node library.
- **Event-source functions** — react to webhooks, forwarded emails, or `timer-events` cron with arbitrary logic.
- **Code inside workflows** — the `RUN_CODE`/`EXECUTE_CODE` node runs Python/JS for a transform without a full snap-in, for lighter needs.

Prefer a `RUN_CODE` node for a small transform; graduate to a snap-in custom operation when the logic is reusable, needs credentials (keyrings), or is too heavy for an inline node. Snap-ins are version-controlled and CLI-deployed. Sizing: Small (thin function) to Large (multi-operation snap-in with keyrings + event sources).

---

## 4. Widgets & SQL / analytics

Reporting is built from **widgets** (each backed by a SQL query) assembled into **dashboards**; real-time list views are **vistas**. See `references/integrations-channels.md` §3.
- **SQL widgets** — for custom metrics on custom fields/objects: define data source, measures, dimensions, filters, groupings, visualization (metric tile, table, bar, line, donut, pie, stacked, heatmap). Widget Builder 1.5 adds cross-object widgets, pivot tables, drill-through, CSV export.
- **Stock dashboards first** — enable the relevant stock support/product/customer dashboards before building custom ones.
- **NL2SQL** — conversational "talk to your data" over structured data for ad-hoc questions.
- Note: dashboards refresh ~60 min (not real-time); use vistas for live operational lists. Building custom dashboards needs knowledge of the part hierarchy, schema, and custom-field JSON — size Medium-Large.

---

## 5. Timeline events

The timeline is the activity/comment stream on an object. Programmatic timeline entries let a solution write structured or narrative events onto a ticket/issue/conversation/custom object.
- **`ADD_COMMENT`** workflow node writes timeline comments with visibility external / internal / private — the common way to record automation activity or agent notes.
- Snap-ins and the API can create richer timeline entries (e.g. snap-kit cards, structured event bodies) for integration activity ("synced from Salesforce", "risk assessment completed").
- Use timeline events to make automation auditable and human-readable on the record, rather than hiding state changes only in fields.

---

## 6. Custom actions & commands

- **Snap-kit actions** — interactive UI elements (buttons, cards, modals) rendered on surfaces: issue, support/portal, comment rich-text editor, snap-in config, and the PLuG widget. Use for human-triggered actions inside DevRev (e.g. "Create Jira issue", "Escalate") without leaving the record.
- **Commands** — slash commands users invoke (e.g. `/devrev create-issue` in Slack). Use for quick human-initiated operations from chat surfaces.
- **`ASK_OPTIONS` / `SEND_FORM`** nodes — collect a choice or structured input from a user mid-workflow (approval gates, data capture) without building custom UI.

Prefer `ASK_OPTIONS`/`SEND_FORM` for in-flow interaction; use snap-kit actions/commands when the action must live on a surface as a persistent affordance.

---

## 7. APIs

DevRev exposes public REST APIs for essentially every object and operation — programmatic CRUD on works, conversations, accounts, parts, custom objects, schema management (`schemas.custom.set`, `stage-diagrams.create`, `link-types.custom.*`), search (`search.hybrid`), and agent invocation (`internal/ai-agents.events.execute-async`).
- **Auth:** Personal Access Tokens (PAT), Application Access Tokens (AAT), Rev session tokens.
- Use the API for: initial schema/object provisioning at scale, external systems creating/reading DevRev objects, and headless integration. Note the `workflows.create` gap — it builds a shell only; node wiring is manual UI.

---

## 8. Webhooks & event sources

- **Outbound (DevRev → external):** the workflow `HTTP` node posts to external endpoints; snap-in webhook event sources and DevRev webhooks push events out. Webhooks act as event-driven "reverse APIs".
- **Inbound (external → DevRev):** snap-in event sources (`flow-custom-webhook`/`flow-generic-events` with policy logic) or workflow `API_TRIGGER` receive external events and start automation.
- **Choosing:** for pulling records with history/analytics use AirSync; for real-time single-event reactions use webhooks/event sources; for a lookup or action mid-conversation use MCP or the HTTP node.

Design implication: name the exact mechanism per integration in the blueprint (AirSync connector vs snap-in event source vs HTTP node vs MCP vs API) — "integrate with X" is not a design; the mechanism and direction are.
