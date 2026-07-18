# Decision Frameworks: Choosing the Right DevRev Capability

This is the connective tissue of the skill. When you know the customer's need, use these frameworks to pick the right platform primitive — and to avoid over-engineering. The overriding principle across all of them: **model the domain natively first, automate deterministically where you can, and add AI only where judgment genuinely adds value.**

---

## 1. The master decision tree

Start at the top for any single requirement and stop at the first match.

```
Is this about STORING/STRUCTURING information (a noun in the business)?
  → Does a built-in object fit (ticket, issue, account, opportunity, part, conversation)?
      YES → reuse it; add a SUBTYPE + CUSTOM FIELDS if it needs extra attributes.
      NO  → is it truly a new kind of thing (campaign, asset, claim, contract)?
              YES → CUSTOM OBJECT (new leaf type + fields + stage diagram).
              NO  → reconsider; you probably want a subtype/custom field.

Is this about a LIFECYCLE / process a record moves through?
  → CUSTOM STATES + STAGES + a STAGE DIAGRAM on the relevant object/subtype.

Is this about REACTING to something happening (deterministic)?
  → Single action, one API call?           → native TOOL / small WORKFLOW.
  → Multi-step / branching / scheduled / long-running? → WORKFLOW.
  → Needs custom code / external OAuth / heavy transform / a new reusable node?
                                            → SNAP-IN (Custom Operation), exposed as a workflow node.

Is this about UNDERSTANDING language / judgment / conversation?
  → AGENT (with skills = tools + workflows + knowledge). Use HITL for risky actions.
  → Mostly-deterministic with a judgment point? → WORKFLOW + Ask AI node (hybrid).

Is this about GETTING EXTERNAL DATA IN?
  → Need history/analytics/2-way sync of records? → AIRSYNC connector.
  → Real-time lookup / action during a chat?      → MCP or HTTP node.
  → New items only, event-driven, no history?      → SNAP-IN event source / webhook.

Is this about a CHANNEL customers use?
  → PLuG / Email / Slack / WhatsApp / Teams / Portal / Telephony snap-in → omnichannel inbox.

Is this about MEASURING / REPORTING?
  → Real-time list → VISTA. Trend/aggregate report → DASHBOARD + WIDGET (SQL). Conversational → NL2SQL.

Is this about WHO CAN SEE / DO WHAT?
  → GROUPS → ROLES → PRIVILEGES (+ caveats + field-level ACL). SSO/SCIM for identity.

Is this about TELLING SOMEONE?
  → SEND_NOTIFICATION / Slack / email / webhook inside a WORKFLOW; white-label customer email.
```

---

## 2. Deterministic vs AI (the single most important call)

| Signal in the requirement | Lean deterministic (workflow/tool) | Lean AI (agent / Ask AI node) |
|---|---|---|
| Inputs are structured fields | ✓ | |
| Inputs are free-text / speech / mixed language | | ✓ |
| Mapping is a fixed table ("if tier=X route to Y") | ✓ | |
| Needs to interpret tone, intent, nuance | | ✓ |
| Path is fully knowable in advance | ✓ | |
| Path depends on reading the situation | | ✓ |
| Auditability/repeatability is paramount | ✓ | |
| Conversational, multi-turn experience | | ✓ |

**The hybrid pattern is usually right for real requirements:** AI extracts/decides at the fuzzy points; a workflow executes the reliable steps. Recommend it whenever a requirement has *both* a "understand what the customer means" part *and* a "then do these exact steps" part.

---

## 3. New object vs subtype vs custom field

- **Custom field** — the thing you're tracking is an *attribute* of an existing record ("contract value" on an account, "affected version" on a ticket).
- **Subtype** — the thing is a *flavor* of an existing record that needs its own fields and/or lifecycle ("Bug" vs "Feature Request" issues; "Escalation" tickets). Subtypes can have their own stage diagram.
- **Custom object** — the thing is a *new noun* with its own identity, lifecycle, and relationships that no built-in object represents (campaign, asset, loan application, insurance claim, vendor, physical shipment).

When unsure, prefer reusing built-ins with subtypes/fields — you keep stock automations, dashboards, and integrations. Reach for a custom object only when reuse would be a distortion.

---

## 4. Agent vs workflow vs snap-in (capability selection)

| Need | Primitive | Why |
|---|---|---|
| One deterministic API action | Native tool | No orchestration required |
| Fixed multi-step, branching, scheduled, or long-running logic | Workflow | Visual, durable, versioned, no-code |
| Custom code, external OAuth, heavy transforms, a new reusable node, code-defined cron | Snap-in (Custom Operation / timer-events) | The extensibility layer; feeds the node library |
| Conversational understanding, dynamic routing, "answer + act" | Agent | Goal-driven reasoning grounded in the graph |
| Mostly-deterministic flow with one judgment point | Workflow + Ask AI node | Reliability with a sprinkle of AI |

New agent vs new skill: create a **new agent** only for a different audience, a security boundary, or genuinely conflicting workflows. Otherwise **add a skill** to an existing agent (fewer, broader agents).

---

## 5. Solution completeness checklist

A good end-to-end DevRev solution touches most of these layers. When designing, walk the list and either use the layer or consciously note it's out of scope:

1. **Domain model** — objects, subtypes, custom objects, custom fields.
2. **Lifecycle** — states, stages, stage diagrams per object/subtype.
3. **Relationships** — links, part associations, references.
4. **Ingestion** — AirSync connectors / snap-in event sources / API for external data.
5. **Channels** — how humans/customers interact (PLuG, email, Slack, portal, API).
6. **Automation** — workflows and automations for deterministic reactions.
7. **Intelligence** — agents + skills where judgment/conversation is needed; HITL on risky actions.
8. **Knowledge** — articles/collections/Q&A for grounding and self-service.
9. **Assignment & routing** — PICK_USER, groups, round-robin, SLA policies.
10. **Notifications** — who gets told, on which channel, at what priority.
11. **Analytics** — vistas, dashboards, widgets, the KPIs the customer cares about.
12. **Identity & permissions** — groups, roles, field-level ACL, SSO/SCIM, internal vs external.
13. **Governance** — guardrails, audit, versioning, rollout/canary plan.

---

## 6. Common anti-patterns to steer away from

- Using AI for a deterministic task (route by explicit field, timestamp math, regex). Use a workflow/code node.
- Building a snap-in for simple CRUD when a native tool exists.
- A "skill" that just calls one tool with no logic — attach the tool directly.
- A fat agent system prompt full of business logic — move logic into skills/workflows.
- Many narrow agents for related tasks — one agent, multiple skills.
- Too many agent knowledge sources — fewer = less noise = better.
- Vague skill descriptions ("creates a ticket") — always include when/what/exclusions.
- Modeling a genuinely new noun as a pile of custom fields on tickets — use a custom object.
- Using AirSync for real-time/event/enrichment/outbound-only needs — use snap-ins/webhooks/APIs.

---

## 7. Domain quick-starts (illustrative, not exhaustive)

These are starting mappings for common verticals. Always validate against the customer's actual process.

- **Financial services / lending:** loan application = custom object (states: Submitted → Under Review → Approved/Rejected → Disbursed); applicant = rev user; product = part; document collection via SEND_FORM; risk-flag via Ask AI; SLA on review time; portal + PLuG channel; approval gate via HITL.
- **Insurance claims:** claim = custom object with subtypes (auto/home/health); policyholder = account/rev user; adjuster assignment via PICK_USER; sentiment routing for escalations; fraud check via Ask AI; Zendesk/Salesforce sync for legacy data.
- **IT service management (ITSM):** incident = incident object; service = part (service variant); request = ticket subtypes; change = custom object; SLA metrics + escalation workflows; Slack/portal channels; asset = custom object; CMDB via AirSync.
- **E-commerce support:** order = custom object (AirSync from Shopify); return/refund = ticket subtypes; account = shopper; deflection agent on PLuG; sentiment routing; CSAT dashboards.
- **B2B SaaS support + product:** ticket (customer) ↔ issue (engineering) linked via "is dependent on"; parts = product areas; feedback → enhancement; auto-triage agent; Jira 2-way sync; ticket/SLA dashboards.
- **Sales / RevOps:** opportunity pipeline via custom stages; account/contact from Salesforce sync; renewal reminder workflows (SLEEP_UNTIL); meeting notes → next steps agent; forecast dashboards.
