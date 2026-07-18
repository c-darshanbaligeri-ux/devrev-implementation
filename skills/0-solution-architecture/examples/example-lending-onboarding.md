# Worked Example — Digital Lending: Loan Application & Support Solution

> Illustrates the full methodology for a non-support domain. The business problem was stated as:
> *"We're a digital consumer-lending fintech. Customers apply for personal loans through our app and website. Today applications live in spreadsheets, our ops team chases documents over email, and support requests come in through a generic inbox with no link to the application. We want one system that runs the application lifecycle, automates document chasing and risk flagging, gives applicants a self-service assistant, and lets leadership see funnel and SLA metrics. Our legacy CRM data is in Salesforce."*

This example shows *how* the reasoning was applied; a real engagement would validate every assumption with the customer.

---

## 1. Business problem
- **Who:** a digital consumer-lending fintech ("the lender"); domain = financial services / lending.
- **What:** run the end-to-end personal-loan application lifecycle, automate document collection and risk flagging, offer applicant self-service, and report funnel + SLA metrics.
- **Why now:** applications live in spreadsheets, document chasing is manual over email, support is disconnected from applications — slow cycle time, poor visibility, compliance risk.
- **Success criteria:** shorter application-to-decision time, lower manual ops effort, higher self-service deflection, and leadership visibility into funnel conversion and review SLA.

## 2. Solution overview
DevRev becomes the system of record for the loan lifecycle. Each application is a **custom object** with a governed stage flow; documents are collected via forms and chased by workflows; a **hybrid** automation flags risk (AI reads free-text/context, deterministic rules decide routing); applicants get a **CX agent** on the app/web PLuG widget grounded in a lending knowledge base with human handoff and hard compliance guardrails; support requests become tickets **linked** to the application; Salesforce legacy data lands via **AirSync**; leadership gets funnel and SLA **dashboards**. It leans on Shared Memory (application ↔ applicant ↔ support all connected), Answer (self-service), and Action (governed automation with HITL on the approval step).

## 3. Domain model (objects & customization)
| Business concept | DevRev object | Reuse / subtype / custom object | Key custom fields | Notes |
|---|---|---|---|---|
| Loan application | Custom object `loan_app` (`id_prefix: LOAN`) | New noun — no built-in fits | `amount_requested` (int), `term_months` (int), `product` (id→part), `risk_score` (double), `risk_band` (enum: low/medium/high), `decision` (enum), `documents_complete` (bool) | New lifecycle-bearing entity; not a distortion of ticket/opportunity. |
| Applicant | `rev_user` | Reuse | `kyc_status` (enum) | External individual. |
| Loan product (Personal / Auto) | `part` (product/capability) | Reuse | — | Routing + reporting key; each app `applies_to_part`. |
| Support request | `ticket` with subtypes | Reuse + subtypes (`document_issue`, `payment_query`, `complaint`) | `related_application` (id→`custom_object.loan_app`) | Inherits stock support automations/dashboards. |
| Applicant conversation | `conversation` | Reuse | — | From PLuG; convertible to ticket. |
| Required document | field on `loan_app` (`[]enum missing_documents`) | Custom field, not a new object | — | Documents are attributes of the application, not their own noun. |

Rationale: the *application* is a true new noun with its own lifecycle and relationships → custom object. Support *is* support → tickets with subtypes. Documents are an *attribute* of the application → a field, not an object.

## 4. Lifecycle (states & stages)
**`loan_app` stage diagram:**
- State **Open:** `Submitted` (start) → `Awaiting Documents`.
- State **In Progress:** `Under Review` → `Risk Assessment` → `Pending Approval`.
- State **Closed:** `Approved`, `Disbursed`, `Rejected`, `Withdrawn` (terminal).

Transitions: Submitted → Awaiting Documents / Under Review; Awaiting Documents → Under Review; Under Review → Risk Assessment; Risk Assessment → Pending Approval / Rejected; Pending Approval → Approved / Rejected; Approved → Disbursed. Use a dependent-field condition to require `custom_fields.decision` before entering a Closed stage.

**Ticket** uses stock support stages; the `complaint` subtype gets a stricter stage diagram with a mandatory `Regulatory Review` stage.

## 5. Relationships
- Ticket → `loan_app` via a **custom link type** "concerns application" (forward) / "has support request" (backward).
- `loan_app` → product **part** via `applies_to_part`.
- Conversation ↔ ticket via convert/link when a chat needs tracked follow-up.

## 6. Data ingestion & integrations
- **Salesforce → DevRev via AirSync** (one-time import + one-way ongoing): Accounts → Account, Contacts → Contact, legacy Cases → Ticket, custom Loan records → `loan_app` custom object (mapped through the Chef UI / IDM). Enable "automations for synced items" so imported in-flight applications trigger the document-chasing workflow.
- **Core banking / disbursement system** — no history needed, real-time action at disbursement → **HTTP node** call from the disbursement workflow (or a snap-in Integrate module if OAuth/token management is required).

## 7. Channels
- **PLuG widget** on the app + website → applicant conversations (self-service assistant, application status, document upload prompts).
- **Email** (Email snap-in) → ticket creation for applicants who email support.
- **Customer Portal** → authenticated applicants track application status and submit documents.
- Conversations map to `conversation`; tracked follow-ups become `ticket`.

## 8. Automation (workflows & automations)
| Workflow | Trigger | Logic (nodes) | Outcome |
|---|---|---|---|
| Document chase | `loan_app` enters `Awaiting Documents` (`*_UPDATED` + If/Else on stage) | `SEND_FORM` (request docs) → `SLEEP_FOR` 48h → check `documents_complete` → `SEND_NOTIFICATION` reminder; loop up to 3× then flag ops | Documents collected without manual chasing. |
| Risk flagging (hybrid) | `loan_app` enters `Risk Assessment` | `ASK_AI` (Reasoning mode: assess free-text employment/notes → structured `risk_band`) → `UPDATE` `loan_app` → `IF_ELSE` on band → route: low = auto-advance, medium/high = assign senior underwriter via `PICK_USER` | AI reads nuance; deterministic rules route. |
| Approval gate | `loan_app` enters `Pending Approval` | HITL approval (`ASK_OPTIONS` / Wait-for-Approval) to authorized approver group → `IF_ELSE` → set `decision`, advance to Approved/Rejected | Governed, auditable human decision. |
| Disbursement | `loan_app` enters `Approved` | `HTTP` POST to core-banking → on success advance to `Disbursed`, `SEND_NOTIFICATION` to applicant | Money moves only after approval + successful API call. |
| Support triage | `TICKET_CREATED` | `CLASSIFY_OBJECT` (subtype) → `SUGGEST_PART` → `PICK_USER` (round-robin within support group) | Tickets routed without manual triage. |
| SLA escalation | `TICKET_SLA_TRACKER_UPDATED` / `loan_app` review SLA | `IF_ELSE` (breach/warning) → `SEND_NOTIFICATION` to owner + manager | Review-time SLA enforced. |

Assignment: `PICK_USER` round-robin within underwriter and support groups. SLA: metric trackers on review time and first response; escalation workflows above.

## 9. Intelligence (agents & skills)
**Applicant Assistant (CX agent)** — deployed to PLuG + Portal via a Conversation-Created → Talk-to-Agent workflow.
- **Goal/persona:** helpful, plain-spoken lending assistant; explains process, checks application status, guides document upload, answers product/eligibility questions.
- **Knowledge sources (lean):** Article, Q&A, `loan_app` (status lookup), Conversation.
- **Skills (each with when/what/exclusion):**
  - `get_application_status` (tool) — "Use when an authenticated applicant asks about their application. Fetches status/next step. Do NOT expose internal risk fields."
  - `request_document_upload` (workflow) — "Use when documents are missing. Triggers the upload form. Do NOT use if `documents_complete`."
  - `create_support_ticket` (workflow) — "Use when the issue can't be resolved from the KB or the applicant asks for a human. Creates a ticket linked to the application. Do NOT use for questions answerable from articles."
- **Guardrails (hard):** never disclose internal risk score/band or decision rationale; never give financial/eligibility guarantees; never collect card/full bank credentials in chat.
- **HITL:** ticket creation and any status change beyond informational are agent-suggested, human-confirmed for edge cases.
- **Triggers & handoff:** Conversation Created on PLuG/Portal; `suspend_on_message_from` = human agent so a person can take over seamlessly.
- **Orchestration:** single broad agent with three skills — no multi-agent needed (one audience, one security boundary).

Internal ops keep the deterministic workflows; no separate internal agent is warranted yet (fewer, broader agents).

## 10. Knowledge & self-service
- Author/import articles: application process, required documents, product eligibility, FAQ; **external** scope for applicant-facing, **internal** for ops runbooks.
- Auto-generate Q&A pairs from resolved conversations to raise deflection over time.

## 11. Notifications
- Applicant: document requests + reminders (email/portal), decision + disbursement (email, Important).
- Ops/underwriters: new assignment, SLA warning/breach (in-app + Slack via notifier).
- Approvers: pending-approval HITL request.

## 12. Analytics & reporting
- **Funnel dashboard** (custom): `loan_app` count by stage → conversion Submitted → Disbursed; drop-off by stage; median time-in-stage.
- **SLA dashboard:** review-time compliance, breaches, by underwriter/product.
- **Support dashboards:** stock Ticket Insights / SLA / Team Performance; CSAT.
- Vistas for ops: "Applications awaiting documents", "High-risk pending approval".

## 13. Identity & permissions
- Groups: `Underwriters`, `Senior Underwriters`, `Approvers`, `Support`, plus customer group `Applicants`.
- Roles: field-level ACL hides `risk_score`/`risk_band`/`decision` from Support and all external roles; only Underwriters+ read risk fields; only Approvers write `decision`.
- External role for applicants on Portal/Plug: read own application status only.
- SSO (SAML) + SCIM (Okta) for staff provisioning.

## 14. Governance & rollout
- Guardrails + HITL on approval and disbursement (money-movement is never fully automated).
- Versioned workflows/agent with rollback; audit log streamed for compliance.
- **Phased rollout:** Phase 1 — `loan_app` object + stages + Salesforce import + core workflows (document chase, triage, SLA). Phase 2 — Applicant Assistant agent + knowledge base + PLuG. Phase 3 — dashboards, optimization, Q&A deflection tuning.
- Testing: Playground + bulk evals for the agent; run traces for each workflow; validate stage-diagram transitions and field-ACL before go-live.

## 15. Build sequence
1. Create states + stages + `loan_app` custom object schema (fields, id_prefix) and its stage diagram.
2. Add ticket subtypes + custom fields + the `complaint` stage diagram; create the custom link type.
3. Set up AirSync Salesforce connector; run initial import; map Loan records → `loan_app`.
4. Build deterministic workflows (document chase, triage, SLA, disbursement HTTP).
5. Build the hybrid risk-flagging workflow (Ask AI + routing).
6. Configure the Applicant Assistant agent, its three skills, guardrails; wire the Conversation-Created → Talk-to-Agent deploy workflow.
7. Author/import knowledge base; enable Q&A generation.
8. Build funnel + SLA dashboards and ops vistas.
9. Configure groups, roles, field-level ACL, SSO/SCIM.
10. Test (traces + evals), phased rollout with canary, monitor and tune.

## 16. Assumptions, risks & open questions
- **Assumptions:** consumer (not commercial) lending; single region; Salesforce holds legacy applications; disbursement system exposes a REST API.
- **Risks / verify:** `workflows.create` builds a shell only (node wiring is manual UI) — plan build effort accordingly, or use `timer-events` snap-in if any step must be fully code-defined; confirm which Salesforce edition (API access required for AirSync); field-level ACL on custom-object fields must be configured explicitly (custom objects default to no access).
- **Open questions:** regulatory retention/audit requirements? Multiple loan products or just personal? Does risk scoring already exist in an external model (then AI just summarizes, and the score comes via API)? Required decision SLA?
