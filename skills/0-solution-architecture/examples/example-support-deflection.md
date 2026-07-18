# Worked Example — B2B SaaS Support Deflection & Convergence

> Business problem: *"We're a B2B SaaS company. Support volume is growing faster than headcount. Most tickets are repeat 'how-do-I' questions our docs already answer, but customers still open tickets. Real bugs get buried and take too long to reach engineering. We use Zendesk today and Jira for engineering. We want AI to deflect the easy stuff, route the rest correctly, and connect real bugs to engineering without manual copy-paste."*

Grounded in real deployments (FOSSA, ActionIQ, Descope, Sayyam). Comparable builds have hit 40–73% deflection and 40–67% faster resolution.

## 1. Executive summary
Deploy a CX deflection agent on the existing channels that answers doc-covered questions and creates well-formed tickets only when needed; a triage workflow that classifies, prioritizes, and routes what reaches humans; and a convergence link so real bugs become Jira-synced engineering issues automatically. Zendesk history migrates in via AirSync; Jira syncs two-way. Leans on Search + Answer + Action, all grounded in Memory. Comparable deployments: ~40% deflection, ~50% faster ticket resolution.

## 2-5. Requirements (condensed)
- **Functional:** deflect doc-answerable questions; auto-classify + prioritize + route the rest; link bugs to engineering; preserve history from Zendesk; keep Jira as engineering SoR.
- **Non-functional:** no added headcount at 2× volume; permission-aware answers; auditable automation; SLA compliance.
- **Assumptions:** published KB exists (or will be seeded); Zendesk admin available for AirSync; Jira Cloud.

## 6. DevRev capability mapping
| Requirement | Capability | Native-first rationale |
|---|---|---|
| Deflect easy questions | CX Agent on PLuG/email | Language understanding; deterministic can't |
| Classify/prioritize/route | Workflow (CLASSIFY_OBJECT + ASK_AI + ROUTER + PICK_USER) | Mix: AI classify, deterministic route |
| Bug → engineering | CONVERT + CREATE_ISSUE + LINK + Jira AirSync | Native links + connector, no custom code |
| History migration | Zendesk AirSync (bulk import) | Existing connector, ~24-hr setup |
| Jira sync | Jira AirSync 2-way | Native connector |

## 7. Architecture
Customer asks in PLuG/email → conversation created → **Deflection Agent** searches KB, answers or offers a ticket → if a ticket is created, **Triage workflow** classifies (bug/feature/question/billing), sets severity by account tier + sentiment, routes to the right group → if it's a bug, agent/rep **converts** and creates a linked Jira-synced **issue** → leadership watches deflection + SLA dashboards.

## 8. Data model & object design
- **Ticket** subtypes: `question`, `bug`, `feature_request`, `billing`. Custom fields: `deflected` (bool), `product_area` (id→part), `account_tier` (enum, from account). `bug` subtype adds `steps_to_reproduce` (rich_text), `severity` override.
- **Issue** (engineering) — synced 2-way with Jira; `applies_to_part`.
- **Parts** = product areas (product → capability → feature) — the routing + reporting key.
- **Account** carries `tier` (enum) used for prioritization.
- **Link:** ticket → issue via stock `is_dependent_on`.
- Lifecycle: ticket stock stages; `bug` subtype gets `Queued → Awaiting product assist → In engineering → Resolved`.

## 9. Workflow & automation
| Workflow | Trigger | Logic | Outcome |
|---|---|---|---|
| Deflection deploy | Conversation Created (PLuG/email) | `Talk to Agent` (external, CustomerChat, suspend-on-message-from=user) | Agent handles chat, hands off to human cleanly |
| Triage | TICKET_CREATED | `OBJECT_SPAM_CHECKER → CLASSIFY_OBJECT(4 categories) → EVALUATE_SENTIMENT → ASK_AI(severity from tier+sentiment, structured) → UPDATE_TICKET(subtype/severity/part) → ROUTER(by category) → PICK_USER(round-robin in group)` | Every ticket classified, prioritized, routed |
| Convergence | ticket subtype set to `bug` | `SUGGEST_PART → CREATE_ISSUE(applies_to_part) → LINK_TICKET_WITH_ISSUE(is_dependent_on)` | Bug reaches engineering, Jira-synced, linked |
| SLA escalation | TICKET_SLA_TRACKER_UPDATED | `IF_ELSE(breach/warning) → SEND_NOTIFICATION(owner+manager, Slack)` | SLA enforced |

## 10. AI components — Deflection Agent (CX)
- **Goal:** "Resolve customer questions using the knowledge base; create a well-formed ticket only when the KB can't resolve it or the customer asks; escalate to a human on frustration or high-severity signals."
- **Knowledge (lean):** Article, Q&A, Ticket, Conversation, Account.
- **Skills:**
  - `search_articles` (tool) — object_types Manual `["article","question_answer"]`; "Use for every question before responding."
  - `create_ticket` (workflow) — Auto-fill title/body/severity/part; owned_by Manual = Tier-1 group; "Use when KB can't resolve or the customer requests a ticket. Do NOT use for doc-answerable questions."
  - `escalate` (tool) — "Use on legal/compliance words, data-loss/security reports, or strong frustration."
- **Guardrails:** never share internal pricing/roadmap; never promise SLA timelines not in docs; PII protection (input+output).
- **HITL:** ticket creation is agent-driven but the triage workflow owns routing; risky field changes suspend for a human.
- **Instructions** follow the standard sections (Role → Core Workflow: search first → Escalation words → Source preferences: official > community, newest > oldest → Out-of-scope handling).

## 11. Analytics
- **Turing/deflection dashboard:** deflection rate, self-serve %, questions vs bugs vs feature requests.
- **Ticket Insights / SLA / Team Performance** (stock): first response (Time@1↔Time@4), median resolution, CSAT, breaches by group.
- Vistas: "Undeflected repeat questions" (candidates for new KB articles), "Bugs awaiting product assist".

## 12. Integration strategy
- **Zendesk AirSync** — bulk import (history) then 1-way ongoing while cutting over: Ticket→Ticket, Organization→Account, End User→Contact, Agent→DevUser, Article→Article. Admin required.
- **Jira AirSync** — 2-way: Issue↔Issue, Comment↔Comment, Status↔Stage, Epic↔Enhancement. Enable "automations for synced items" so synced bugs trigger notifications.

## 13. Security & permissions
- Groups: Tier-1 Support, Tier-2, Engineering (issues). Field ACL hides internal `severity` rationale and eng notes from external roles. External role: customers see own tickets on Portal only.

## 14-15. Plan & sequence
1. Ticket subtypes + fields + bug stage diagram; parts as product areas; account `tier`.
2. Zendesk AirSync bulk import; Jira AirSync 2-way.
3. Triage + SLA + convergence workflows.
4. Deflection Agent + skills + guardrails; deploy workflow.
5. Seed/curate KB articles; enable Q&A generation from resolved conversations.
6. Deflection + SLA dashboards; vistas.
7. Groups, roles, field ACL.
8. Test (Playground + bulk evals + workflow traces); phased rollout; monitor deflection and tune KB.

## 16. Task breakdown (illustrative)
| Task | Complexity | Hours | Dependencies |
|---|---|---|---|
| Ticket subtypes/fields/bug diagram | Medium | 16 | — |
| Zendesk AirSync bulk import | Large | 40 | admin access |
| Jira AirSync 2-way | Medium | 24 | — |
| Triage workflow | Medium | 20 | subtypes exist |
| Convergence workflow | Small | 10 | Jira sync |
| Deflection Agent + 3 skills | Medium | 28 | create_ticket workflow |
| KB seeding + Q&A | Medium | 24 | — |
| Dashboards + vistas | Medium | 16 | data flowing |
Roll-up: Eng ~178h + QA ~50h + UAT ~24h + Docs ~16h + Deploy ~16h + Buffer ~20% ≈ 340h; overall ~8–10 weeks phased.

## 16-20. Risks / alternatives / recommendation
- **Risks:** thin/unpublished KB kills deflection (mitigate: seed articles from top ticket themes first — only published articles are used by AI); Zendesk needs admin; custom Account fields from sync aren't filterable; deflection over-eagerness (mitigate: guardrail + bulk-test with real questions, fix priority Task Success first).
- **Alternatives:** A (fastest) deflection agent only, manual triage — ships in ~3 weeks. B (most scalable) full triage + convergence + 2-way Jira — this design. C (most maintainable) same as B but keep Zendesk as SoR longer via 1-way sync to de-risk cutover. **Recommend B**, cutting over from Zendesk in phases (C's caution folded in).
- **Final:** land the domain model + AirSync + triage first (value without AI risk), then the Deflection Agent once the KB is solid. Open questions: current KB coverage of top themes? SLA targets per tier? keep Zendesk long-term or full cutover?
