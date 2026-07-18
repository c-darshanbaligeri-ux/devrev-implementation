# DevRev AI Agents & AI Capabilities

Use this reference when the solution needs conversational understanding, judgment, natural-language input, or an "answer + act" experience. If the task is deterministic, prefer a workflow (see `workflows-automation.md`).

## Table of contents
1. What DevRev agents are
2. Agent types
3. How agents are built (Agent Studio)
4. Skills and tools
5. Knowledge, grounding, and RAG
6. Multi-agent pipelines & orchestration
7. Agent triggers
8. Guardrails, instructions, personas, HITL
9. Deployment contexts & channels

---

## 1. What DevRev agents are

An AI agent is an intelligent entity that helps humans accomplish work or augments their capabilities — it perceives its environment, decides, and takes actions with autonomy. **Not a chatbot** (chatbots follow rigid scripts; agents are goal-driven).

Composition — the parts of an agent:
- **Agent** — orchestrator and user-facing entry point; holds context/config.
- **Instructions / prompts** — plain-language system prompts defining role, behavior, tone, boundaries.
- **Skills** — executable capability units combining instructions + tool access + context awareness.
- **Tools** — fine-grained actions (API calls, workflow execution). Knowledge acts as a native tool.
- **Knowledge** — the permission-filtered information-access layer.
- **Memory / sessions** — isolated session state; context persists across handoffs.
- **An LLM** — the reasoning engine.

**Core design tenets:** fewer but broader agents (avoid narrow-agent proliferation — build department-level agents); integration flexibility (MCP/A2A, no lock-in); maintainability first; reuse platform primitives (permissions, groups, roles, spaces); simple by default, powerful when needed.

---

## 2. Agent types

**By audience (primary split):**
- **CX / customer-facing agents** — support, self-service, deflection; deployed to PLuG, email, Slack, WhatsApp via External Spaces / RevSpaces.
- **Internal / employee-facing agents** — extensions of Computer across sales, engineering, operations; deployed within organizational Spaces/teams.

**By function (out-of-the-box catalog / personas):**
- Support: Chat/Auto-Resolution, Incident Management, Ticket Triage, Tier-1 Deflection, Technical Troubleshooting.
- CX: Churn Reduction, Feedback Routing, NPS Follow-up, Proactive Engagement.
- Sales (Revenue Agent): Customer Research, Sales Performance, Lead Gen, SDR Meeting, Renewal, Upsell.
- Product/Build: Bug Triage, Feature Prioritization, Release QA, PRD, Enhancement Request.
- Search: enterprise "Ask me anything" across silos.

Treat the functional "agents" as **personas/skill-sets layered on the same framework**, not distinct engines. DevRev effectively provides two super-agents that orchestrate — Computer (employees) and Computer for Your Customers (CX) — plus website apps.

---

## 3. How agents are built (Agent Studio)

**Agent Studio** is the interface for building, testing, and monitoring agents. Access: Settings → Agent Studio. Three-phase loop:
1. **Build** — define identity, configure knowledge, attach skills, set guardrails, write instructions.
2. **Test** — validate against scenarios (Playground + bulk evaluation) before shipping.
3. **Observe** — monitor live performance, track versions, identify drift, feed back into Build.

Build walkthrough:
1. Create agent (starts with default name/goal + Default Guardrail on).
2. Set Name + Goal (overall direction).
3. Add Knowledge sources (object types the agent may search — Article, Ticket, Q&A, Conversation, etc.).
4. Attach Skills (tabs: All / Operations = built-in DevRev actions / Workflows = your custom automations). Per operation set: name, description, input field modes (Auto-fill vs Manual), Execute-as-User toggle, Connections/keyrings.
5. Review Guardrails (Default always-on; add custom).
6. Write Instructions (rich-text playbook; `@`/`/` to reference tools/skills/knowledge).
7. Test in Playground (View Trace shows skills/knowledge/guardrails invoked).
8. Publish (Draft → Live; one live version at a time; version history + restore).

No-code by default (describe in plain English; agents auto-understand business context via Computer Memory); low/high-code extension where needed.

---

## 4. Skills and tools

- **Tool** — a single atomic operation (one API step).
- **Skill** — a package of instructions + tool access + logic for a type of task. Analogy: an agent is a person; a skill is a playbook. You don't create a new agent per task — you give the same agent a new skill.
- Terminology caveat: DevRev Agent-Studio "skills" are AI Agent Plans (`ai-agent-plans` API). These are NOT filesystem `SKILL.md` skills — a different system.

Four building-block primitives:
| Primitive | What it is | Execution | Authoring |
|---|---|---|---|
| Tool | Atomic single-step API call | Agent runtime, permission-inherited | Select/configure in Agent Studio |
| Workflow | Multi-step rule-based DAG | Server-side engine; deterministic; not in agent context window | No-code visual builder |
| Custom Operation | TypeScript serverless function | Snap-in runtime; a workflow node or API call | High-code; packaged in a snap-in |
| Skill (AI Agent Plan) | A tool or workflow attached with a description defining *when to invoke* | Agent reads description → decides → invokes | Configured in Agent Studio |

Skill config fields:
- **Name** — `^[a-zA-Z0-9_]+$`.
- **Description** — decides everything; the agent uses ONLY this to choose. Formula: **[When to use] + [What it does] + [Exclusions]**. Good: "Use when a customer reports an issue KB articles don't resolve, or explicitly requests a ticket. Do NOT use for general questions answerable from docs." Bad: "Creates a ticket."
- **Input field modes:** Auto-fill (agent derives from context) vs Manual (fixed value).
- **Execute as User** — default ON (runs with the invoking user's permissions). Turn OFF only for system-level ops.
- **Connections (keyrings)** — required for external systems.
- **Limits:** max 5–8 skills per agent; one skill = one job; always include exclusions.

How skills attach:
- Single-use-case agent → attach tools/workflows **directly**; put orchestration in the system prompt.
- Multi-use-case agent → wrap in skills with descriptions; keep the system prompt thin (routing only).

Custom skills can be built for industry terms/brand voice; reusable across agents. Agent Studio has a curated **skill marketplace** — installing a skill auto-attaches the tools it depends on.

**MCP tools:** DevRev as MCP client (native MCP node connects to any remote MCP server, EXECUTE/FETCH); DevRev as MCP server (exposes DevRev objects to Claude/Cursor via OAuth). Agents are MCP- and Bedrock-compatible.

---

## 5. Knowledge, grounding, and RAG

Knowledge is a **native tool** — the permission-filtered information layer:
- Structured knowledge: database entities, relationships, profiles.
- Unstructured knowledge: documents, conversations, articles, code.
- Permission-aware: filtered at the field level, validated in real time.

Configured as object types the agent may search. **Fewer sources = less noise = better.** Recommended source sets:
| Agent type | Knowledge sources |
|---|---|
| Customer Support | Article, Q&A, Ticket, Conversation, Account, Rev User, Rev Org |
| Ticket Routing | Ticket, Conversation, Account, Product/Feature/Capability |
| Knowledge Q&A | Article, Q&A only |
| RevOps | Account, Rev Org, Rev User, Opportunity, Dataset |

The grounding stack:
- **Knowledge Graph ("Shared Memory")** — patented AI-native graph mapping relationships. Agents navigate pre-built relationships, not just retrieve documents. Powers the "Search, Answer, Action" framework.
- **Airdrop / AirSync** — bidirectional sync (50+ connectors) injecting real-time live data for accurate personalized responses.

Retrieval priority (reliability decreases going down):
1. FetchObjectContext (have an ID? fetch directly).
2. Deterministic skill (common query? pre-build it).
3. HybridSearch (need to discover? narrow scope).
4. NL2SQL (need aggregates/counts/trends?).
5. Generic knowledge (last resort).

Anti-hallucination: constrain sources ("only use knowledge base results"); reduce KB scope; make instructions specific.

---

## 6. Multi-agent pipelines & orchestration

Agents coordinate behind the scenes:
- **Delegation** — hand off complex requests to specialized agents, preserving context.
- **Skill-level invocation** — a skill can call another agent.
- **Routing intelligence** — the Computer agent routes queries to the most appropriate specialist.
- **Context preservation** — full history transfers between agents.

Orchestration nodes:
- **Talk to Agent** — one-way handoff to a named agent (does not return to the workflow).
- **Ask Agent** — two-way: workflow calls an agent mid-flow, gets a response, continues. Ideal for complex routing.
- Bidirectional agent↔workflow: workflows invoke agents as decision points; agents invoke workflows as packaged skills.

Multi-agent design patterns (start simple; escalate only when needed):
| Pattern | Flow | Constraint |
|---|---|---|
| Tool Use (default) | Input → Select Skill → Execute → Respond | 5–8 skills max |
| ReAct | Think → Act → Observe → Repeat | max_steps 3–5, timeout 30–60s |
| Plan-Execute | Plan → Execute (parallel where possible) | Planner + Executor agents via Talk-to-Agent |
| Reflection | Output → Validate → Refine | Max 2 iterations; ~2× cost |
| Multi-Agent Routing | Router → Specialists | Router classifies only; always define a default route |

When to create a new agent vs add a skill:
- **New agent** only for: different user audiences (customer vs internal), security boundaries (different permission models), or conflicting workflows.
- **Add a skill** to extend capabilities for the same user group, build on existing context, or maintain centralized governance. Mental model: create skills to up-skill an agent; create agents to establish distinct "departments."

---

## 7. Agent triggers

Agents can be invoked by:
1. **Manually by users** — via Agent Studio / chat surfaces.
2. **Event-based via workflows** (primary production mechanism) — a workflow listens to an event and calls the agent via Talk to Agent / Ask Agent. Skills only run when the agent explicitly calls them — not just because they're attached.
3. **Programmatically via API** — `POST internal/ai-agents.events.execute-async` with `agent`, `event.input_message.message`, `session_object` (state key), and `webhook_target`.

Conversation/ticket trigger config: set trigger to Conversation created or Ticket created (fires on Portal/PLuG/Slack/WhatsApp/email), then add Talk to Agent. Key params: `agent`, `object`, `visibility` (internal/external), `panel`, `quick_replies`, `respond_to_user_types`, `suspend_on_message_from` (pauses the agent when a human replies — the human-handoff lever), `additional_context`.

Trigger node types include event triggers on essentially every object, plus `MANUAL_TRIGGER`, `API_TRIGGER`, `TIMER_TRIGGER` (interval/cron → scheduled), and `AI_AGENT_SKILL_TRIGGER`.

---

## 8. Guardrails, instructions, personas, HITL

**Instructions vs Guardrails:**
- Use **Instructions** for preferences, tone, formatting, orchestration/routing, escalation. Structure: Role & Persona → Scope (handles X, not Y) → Core Workflow (step-by-step) → When to Use Skills → Escalation Rules → Tone & Style.
- Use **Guardrails** for hard never/always rules, compliance, safety. Max 16 guardrails; a Default Guardrail is always on. Example: "Never share internal pricing information with customers."

Prompt best practices: clear, affirmative language; define role/tasks/skills/boundaries; test edge cases. Personas set via goal + instructions and can adapt by customer traits (tier, language, industry) in RevSpaces.

**Human-in-the-loop (HITL):** requires human approval before an agent executes specific tools/actions — grant broad permissions while keeping oversight on high-stakes/irreversible decisions. Many write-action nodes are flagged `NeedsApproval=true`.

**Security & governance:** permission inheritance (agents operate under the user's identity; least privilege), fine-grained RBAC (user/team/org scope), auditable execution (every tool call/skill path/output logged; SIEM streaming), data-boundary enforcement (internal vs external agents), versioned config with rollback and canary deployments, SOC2 + GDPR.

**Observability:** session tracing, the reasoning "thinking stack," token usage per turn, guardrail-trigger visibility, latency breakdown, built-in evaluators (answer relevance, groundedness, deflection rate, CSAT). Testing layers: Playground (10–15 inputs), Traces (Observe → Sessions), Bulk tests (datasets + evaluators). Fix priority: Task Success first, then Accuracy.

---

## 9. Deployment contexts & channels

- **Internal Spaces** — agents within org teams, inheriting space permissions/knowledge boundaries.
- **External Spaces / RevSpaces** — customer-facing; combine channel + user traits + brand; a single RevSpace can host multiple agent configs for different segments; trait-based behavior.
- **Channels** — CX agents deploy to PLuG, email, Slack, WhatsApp with one-click deploy. Deploying to a channel is workflow-driven: the channel must be active and creating Conversation objects; a Conversation Created trigger fires a Talk to Agent node.
- **Sessions** — isolated session state; context persists across handoffs and failures; configurable memory-retention.

---

### Implementation guidance
- Phased rollout: Phase 1 Agent & Tools → Phase 2 Introduce Skills → Phase 3 Customize Agents.
- Sizing: agents sized S/M/L by skill count and reasoning complexity; existing connectors (Salesforce, Zendesk, HubSpot) are ~24-hr setups; proprietary connectors are new builds.

### One-line positioning
Agent Studio is enterprise agent **lifecycle** infrastructure — build, test, deploy, and manage agents grounded in DevRev's unified Knowledge Graph, so teams **Search accurately, Answer correctly, and Act safely** with production governance and observability.

---

## 10. Build detail (for real configs)

**The five configuration elements:** Goal (1-2 sentences, the north star) · Knowledge (object types it can search) · Skills (Tools / Workflows / NL Skills) · Guardrails (safety, override everything) · Instructions (the playbook). Agents are created in **Draft**; Internal vs CX types (CX = stricter guardrails).

**Goal structure:** `[Role] + [what it handles] + [boundary/escalation]`. Good: "Help customers troubleshoot product issues by searching the knowledge base, and escalate to a human when it can't be resolved." Bad: "Be a helpful assistant."

**Instructions recommended sections:** `## Role & Persona` · `## Scope of Responsibilities` · `## Core Workflow` (numbered steps) · `## When to Use Skills` (`@`-mention each) · `## Escalation Rules` · `## Response Format` · `## Source Preferences` · `## Tone & Style` · `## Out-of-Scope Handling`. Use `@` mentions to bind a specific tool/skill. Real production agents encode explicit priority rules (P1–P4 severity matrix by account tier + impact), escalation trigger words ("legal", "lawsuit", "refund > $500", "third time"), and source-conflict tie-breakers (official > community; newest > oldest).

**Skill (Tool) config fields:** Name (`^[a-zA-Z0-9_]+$`); Description (the ONLY thing the agent uses to choose — `[when to use] + [what it does] + [exclusions]`); Input fields each **Auto-fill** (agent derives) or **Manual** (fixed constant, e.g. a group ID); **Execute as User** (default ON); **Needs Approval** (HITL, default off); Connections (keyrings). Good desc: "Use when the customer reports a new issue KB articles can't resolve, or explicitly requests a ticket, or troubleshooting failed after 2 attempts. Do NOT use for general questions answerable from docs." Bad: "Creates a ticket."

**Guardrails:** one type today — `topic_boundary`. Fields: Topic Name, Description (what the model evaluates against), Applies To (`["input"]` / `["output"]` / both), Default Message, Enabled. A **Default Guardrail** is always on and can't be deleted. **Hard max 16 guardrails.** Example: {PII Protection, input+output, "Never disclose internal employee personal info to external users"}.

→ The GET-vs-write shape is **asymmetric** (flat array on create, `{"set":[...]}` wrapper on update; `topic_boundary` fields nest on GET but must be flattened on write) — full OpenAPI schema names, endpoint-by-endpoint payload shapes, and a GET→write conversion helper (empirically verified against the live internal API, dated 2026-06-01): `../../7-agent-building/references/guardrails-api.md`.

**NL Skills (sub-agents, API-only):** three layers — Skill Description (**≤1024 chars**, always in context) + Plan Guidance (full prompt, loads on activation) + Tools (workflows/operations). Configured via `ai-agents-plans.create/.update` then `ai-agents.update`; `skills.set` **replaces all** — include existing ones. Sub-agents are stateless (return results to the main agent).

→ **Live-verified correction**: `ai-agents.plans.get`/`ai-agents.plans.list` **do not exist** as endpoints — confirmed by empirical testing against the internal API. Do not assume they're available for reading back NL-skill plans. Full create-vs-update payload templates, pre-flight checklists, and an error→fix table: `../../7-agent-building/references/api-contracts.md`.

**Testing:** Playground (Start New Chat + View Trace) → traces show Thought/Reasoning, Input, Output per skill, Knowledge retrieval, Guardrail Check, Response Time, Tokens → Bulk tests over a CSV Dataset (Input / Expected Output / Remarks) with evaluators. **Documented evaluators are Correctness and Completeness only** — deflection/CSAT/groundedness are business metrics/roadmap, not built-in evaluators. Fix priority: Task Success → Accuracy → latency/cost.

**Deploy to channel:** Publish (Draft→Live, prior Live→Archived; every save versions; restore creates a new Draft). Build a workflow: `Conversation Created` trigger → `Talk to Agent` node with Agent / Object=Conversation / Visibility=External / Panel=Customer Chat / Respond-to-user-types=customer / **Suspend on Message From = user** (human handoff) / Quick Replies / Additional Context. Talk to Agent = one-way + agent-to-agent routing; Ask Agent = two-way mid-flow. Async API: `POST /internal/ai-agents.events.execute-async` with `agent`, `event.input_message.message`, `session_object` (conversation id — same value = same context), `webhook_target`.

**Agent identity at runtime:** each agent has its own IAM identity; effective privileges = INTERSECTION(agent's own, triggering user's) via `act_as` — never exceeds the user. Permissions checked at **tool-execution time** (object + field level), enforced before data reaches the LLM; every tool call is an immutable audit record. This is why Execute-as-User defaults ON.

**Documented hard limits:** 16 guardrails/agent; NL-skill description 1024 chars. 5–8 skills is **guidance, not a hard cap** (progressive context loading means each skill costs ~100 tokens at session start; schemas load on invoke). Knowledge-source count, max steps, timeouts, and token budgets are **not documented** — don't assume numbers. Canary deployment is claimed in marketing; only publish/archive/restore + suspend-on-message handoff are documented mechanics.
