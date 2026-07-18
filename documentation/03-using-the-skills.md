# 03 — Using the Skills (daily work)

You don't invoke skills by name — **you describe what you want in plain English** and the repo's
router (top-level `CLAUDE.md` + the `implementation-router` skill) maps your intent to the right
domain. The agent then opens that domain's `SKILL.md` and follows its playbook, taking every
endpoint, scope, and payload format from the domain's reference files — never from memory.

Routing is by **intent, not keyword**:

| You say… | Routed to |
| --- | --- |
| "design a solution for [business problem]", "how should I build X in DevRev", "we're a fintech and need to..." | 0 — solution architecture (blueprint) |
| "add a field to accounts", "create a custom object", "define a subtype" | 1 — object & schema customization |
| "tickets should go through a triage step", "customize stages", "add a state" | 2 — stage & lifecycle |
| "load these CSVs", "attach this file", "build an org from scratch" | 3 — data upload & org build |
| "build me a support dashboard", "add a chart of open tickets per account" | 4 — dashboards & widgets |
| "a dataset joining tickets and accounts", "Ponos job", "Oasis dataset" | 5 — datasets |
| "when a ticket comes in, notify the owner", "why won't this template import" | 6 — workflows |
| "let the agent look up order status" | 6 — agent-callable skill (four-block pattern) |
| "make the agent smarter", "debug the agent", "test the agent's guardrails" | 7 — agent building |
| "call works.list", "hit the API", any raw endpoint | 8 — raw REST API |
| "build a HubSpot connector", "sync Asana into DevRev", "add pagination to the Trello snap-in" | 9 — snap-in / AirSync development (routed to third-party plugin) |
| "update the repos", "pull latest" | update-repos (maintenance) |
| "remember this so we don't hit it again", any correction / undocumented behavior | capture-learnings (self-improves the repo mid-task) |

Below: what each domain does, example prompts, and what happens under the hood.

---

## 0 — Solution architecture (design phase)

**Covers**: turning a vague business problem — support, sales, ITSM, fintech, insurance, healthcare,
internal ops, anything — into a **20-section solution blueprint** that maps the domain onto the full
DevRev platform. Never calls the live API; the blueprint hands off section-by-section to skills 1–8.

**Example prompts**
- "We're a fintech doing digital lending — design an end-to-end solution."
- "How should we build support deflection + support↔engineering convergence for a B2B SaaS?"
- "We use ManageEngine as our IT ticketing system-of-record — how do we bring DevRev on top?"
- "Should this be an agent or a workflow?"
- "Native-first analysis: where does this need custom code vs. configuration?"

**Under the hood**: 6-step design arc — (1) analyze the domain, (2) map customer nouns onto the
DevRev graph (data model + lifecycle first), (3) select capability per requirement (deterministic vs
intelligent, usually hybrid), (4) walk the 13-layer completeness checklist, (5) estimate effort + risk
+ A/B/C alternatives, (6) sequence the build. Outputs the blueprint template, which then routes each
build step to the right execution skill (1–8). The design principle throughout: **native-first /
configuration over customization** — model the domain natively, automate deterministically where
possible, add AI or custom code only where they genuinely add value. Also flags two known gaps where
DevRev design must go outside this repo: AirSync connector setup (unless skill 9 covers it) and
Security/Permissions/RBAC (no execution-skill counterpart yet).

## 1 — Object & schema customization

**Covers**: custom object types, custom fields on stock objects (tenant `tnt__` fields), subtypes
(`ctype__` fields), stock field overrides, aggregated schema checks, custom link types.

**Example prompts**
- "Create a custom object type for purchase orders with a status enum and an amount field."
- "Add a `region` dropdown to accounts."
- "Create a subtype 'bug' on issues with a severity field."
- "Create a custom link type 'blocks' between issues."

**Under the hood**: schemas are set via `schemas.custom.set`; records reference them with a mandatory
`custom_schema_spec`; custom-object creates use `unique_key` so re-runs don't duplicate. The skill
knows the sharp edges: a wrong `tnt__`/`ctype__` prefix **fails silently**; after any schema change,
affected records must be re-saved to pick up the new fragment version; custom link types can only be
**deprecated, never deleted**; new custom objects start with zero access until roles are granted.

## 2 — Stage & lifecycle customization

**Covers**: custom states, stages, stage diagrams, transitions, assigning lifecycles to subtypes,
dependent-field conditions.

**Example prompts**
- "Give tickets a triage → investigating → resolved flow."
- "Add an 'awaiting customer' stage to the support lifecycle."
- "Require the root-cause field once an incident reaches 'closed'."

**Under the hood**: strict build order — **states first, then stages, then the stage diagram**, each
tier verified with a `*.list` before the next. Diagrams attach to subtypes via `stage_diagram_id`.
Some properties (`is_default`, `leaf_type`) are immutable after creation, so the skill gets them
right the first time.

## 3 — Data upload & org build

**Covers**: file/artifact uploads, bulk record loading, migrations, and full fresh-org builds.

**Example prompts**
- "Upload this PDF and attach it to ticket don:core:…:ticket/456."
- "Load these 200 accounts with their rev-orgs and users."
- "Build a demo org: product catalog, 3 accounts, 20 tickets."

**Under the hood**: artifacts use the two-step `artifacts.prepare` → upload-bytes-to-URL flow. Org
builds follow the ordered sequence: auth/ping → customization (routes back to skills 1–2) → parts
(product → capability → feature) → Trail (via `parent_part` + `serves` links) → custom links → work
items → verify. Customer data goes top-down: account → rev-org → rev-user, saving each returned DON
id in a scratchpad for the dependent calls. **Honesty note**: DevRev has no public bulk-create
endpoint — "bulk" means deterministic scripted loops that are idempotent (`unique_key` or
check-before-create), safe to re-run, and loud on failure.

## 4 — Dashboards & widgets

**Covers**: creating, modifying, and verifying dashboards and widgets (via the `dashboard-dev` plugin).

**Example prompts**
- "Build a support dashboard: ticket counts by state, priority distribution, weekly trend."
- "/dashboard-planner" (optional, for vague requirements — writes `plans/<slug>.md` first)
- "/create-dashboard plans/support-overview.md"
- "/modify-dashboard — add an SLA-breach widget to the ops dashboard."

**Under the hood — the only supported path**: `/create-dashboard` parses requirements → scaffolds
`dashboards/<slug>/widgets/` → parallel widget-generator agents → each widget passes **3-stage
validation (structure → semantic → live API)** with auto-fix retries → dashboard assembly → deploy
via `dashboard-sync dashboard create` → visual verification pass. Modifications go through
`/modify-dashboard` (download → delta → push). **Hard rule**: never hand-write widget JSON and never
use the low-level widget skills for a *new* dashboard — that bypasses all validation. The agent will
refuse to shortcut this.

## 5 — Datasets

**Covers**: custom analytics datasets (via the `dataset-builder` plugin).

**Example prompts**
- "/dataset-builder:setup" then "/dataset-builder:explore" (always check what already exists first)
- "Create a dataset of ticket resolution times joined with account tier."

**Under the hood — PaaS vs Ponos**:

| Aspect | PaaS (default) | Ponos |
| --- | --- | --- |
| Scope | Org-specific | Cross-org (all orgs) |
| Setup | Pure API calls | YAML + PR into the internal ponos repo |
| Use case | Custom org analytics | Stock/shared datasets |
| Extra tools | None (just `.env`) | gcloud/bq, AWS CLI, kubectl |

Rule of thumb: **PaaS for almost everything**; Ponos only for stock datasets shared across orgs.
Known gotchas the skill enforces: dataset `title` is required, partition columns must be
`TIMESTAMP`-typed, and no `dim_`/`fact_` name prefixes.

## 6 — Workflows & agent-callable skills

**Covers**: event-driven automations, manual workflows, and agent-callable skills — plus workflow
CRUD (list/inspect/trigger/publish/delete) via DevRev's internal workflows API.

**Example prompts**
- "When a ticket is created with priority P0, post an internal comment and notify the owner."
- "Let the agent look up a customer's order status." (→ agent-callable skill)
- "List my workflows." / "Trigger workflow don:integration:…:workflow/123 with order_id=42."
- "This template won't import — here's the error."

**Under the hood**: for anything beyond one step, the skill **authors a complete template JSON**
(validated against the 130 operation schemas in `operations/schemas/`) and you import it via
**Workflows → Import** in the DevRev UI — far more reliable than building graphs step-by-step through
the API. Agent-callable skills use a fixed four-block skeleton (trigger with input schema → skill
block → action steps → output block, labeled `"skill"`). Confirmed-working patterns live in
`examples/working-*.json`, and there's a debugging checklist for the handful of causes behind almost
every import failure. Manual triggering uses the bundled `scripts/trigger_manual_workflow.py`
(supports `--dry-run`; the workflow must be published first).

**The learning loop**: when you confirm a template imported and works, the agent promotes it into
`examples/working-<name>.json` — every success becomes a proven pattern for the next request.

## 7 — Agent building (Agent Studio)

**Covers**: creating, debugging, improving, and testing DevRev AI agents; guardrails; feature flags;
NL2SQL annotations; multi-agent routing patterns.

**Example prompts**
- "Design a support agent that answers from our KB and can look up ticket status."
- "The agent keeps picking the wrong skill — debug it." (agent ID/slug + `ORG_PAT` needed)
- "Write a test set for the billing agent."
- "Configure a topic-boundary guardrail so the agent won't discuss pricing."

**Under the hood**: eight command playbooks (`commands/agent-create.md`, `agent-debug`, `agent-improve`,
`agent-test`, `agent-ask`, `agent-sync`, `feature-flags`, `guardrails-api`) plus ten Agent Studio
knowledge-base articles (prompting, retrieval strategy — FetchObjectContext vs HybridSearch vs NL2SQL,
design patterns including multi-agent routing, testing, full examples). API payloads are grounded in
the live-verified `references/api-contracts.md` and the cloned `repos/api-specs`. **Auth**: reads and
public-API work need only `DEVREV_PAT`; mutating agent configs via the internal API needs the
optional `ORG_PAT` in `.env` — and the agent always asks before any mutating internal call.

## 8 — Raw REST API

**Covers**: any DevRev public REST endpoint — work items, timelines, tags, links, accounts/users,
conversations, articles, surveys, meetings, SLAs, artifacts, webhooks, schedules, vistas, and all
customization endpoints.

**Example prompts**
- "List the 5 most recent tickets."
- "Create an issue linked to that ticket."
- "Set up an SLA: first response 30 minutes for enterprise accounts."

**Under the hood — the execution flow every call follows**:
1. Find the endpoint + required scope in `references/00_API_Catalog.md`
2. Open the domain doc for the exact payload
3. Substitute real DON ids (never display IDs like `TKT-456`)
4. Run with standard headers
5. **Verify** with the matching `*.get`/`*.list`
6. Keep a scratchpad of returned DON ids for dependent calls
7. `ping` first when token validity is uncertain

## 9 — Snap-in / AirSync connector development

**Covers**: planning, building, updating, and testing DevRev snap-ins and AirSync connectors (any
external system → DevRev integration). Routes to the `devrev` plugin from `QK-SnapIn/devrev-qk-agents`
(third-party — **plugin is not auto-enabled**; the user runs `/plugin install devrev@devrev-qk-agents`
once before first use).

**Example prompts**
- "Plan an AirSync connector for HubSpot."
- "Build the snap-in code from the approved TDD."
- "Add pagination to the Trello connector."
- "Test this snap-in end-to-end (unit + UI automation)."
- "/devrev:plan-snapin" → "/devrev:build-snapin" → "/devrev:test-snapin"

**Under the hood**: PM → Architect → Tester pipeline. PM gathers requirements across 4 discovery
rounds → feasibility check (does a native connector already exist?) → PRD → TDD → explicit user
approval gate. Architect web-researches the real external API across 8 areas (auth, endpoints, rate
limits, pagination, errors, incremental sync, permissions, attachments), documents 15 engineering
decisions, and generates the full project (AirSync connectors clone-and-rewrite a production Asana
template rather than starting from a blank scaffold). Tester writes Jest unit tests (≥70% coverage)
then drives real UI automation (install → configure → sync → verify field-by-field → test
incremental).

**Precondition**: 1–2 MCP servers must be added manually — see [01 — Getting Started, "Optional:
snap-in development"](01-getting-started.md). This skill also **explicitly excludes** the same
plugin's Implementation (dashboard) vertical — that vertical hand-writes widget JSON and violates
skill 4's hard rule; dashboards always go through skill 4.

## The hosted MCP (always on)

Alongside the skills, the hosted DevRev MCP server (`.mcp.json`) gives the agent direct
search/read/create/update access to work items, accounts, parts, and users, plus analytical queries —
useful for quick lookups without hand-building REST calls. It authenticates with the same
`DEVREV_PAT` from `.env`.
