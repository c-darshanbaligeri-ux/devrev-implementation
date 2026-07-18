# Worked Example — Internal ITSM & Employee Support

> Business problem: *"Our internal IT team drowns in repetitive requests — password resets, access requests, laptop issues, software installs — filed over email and Slack with no structure. Employees don't know where to ask. We already run ManageEngine ServiceDesk Plus for IT tickets and don't want to rip it out. We want an employee-facing assistant in Slack that answers policy questions, creates properly-categorized tickets, and checks status — while ManageEngine stays the system of record."*

Grounded in the ManageEngine reference architecture and Camping World / Penumbra ITSM deployments. Comparable builds resolve 60%+ of IT requests without human touch and cut research time substantially.

## 1. Executive summary
DevRev Computer becomes the employee-facing IT interface in Slack; ManageEngine ServiceDesk Plus stays the ITSM system of record. Inbound ME data (users, requests, solutions) syncs into DevRev via an AirSync connector every 5 minutes for grounding; the agent takes real-time actions (create ticket, check status) via HTTP skills against the ME REST API. The agent deflects policy/how-to questions from a knowledge base, creates well-formed requests through a guided intake flow, and reports status conversationally. Pattern: "external system stays SoR + AirSync in + agent HTTP skills out."

## 2-5. Requirements (condensed)
- **Functional:** Slack assistant that answers IT/HR policy questions, creates categorized ME requests via conversational intake, checks ticket status, deflects repetitive requests; ME remains SoR.
- **Non-functional:** real-time outbound actions; permission-aware (employee identity); auditable; ME as source of truth (no data divergence).
- **Assumptions:** ME ServiceDesk Plus with REST API + API key; Slack workspace; policy content available to seed a KB.

## 6. DevRev capability mapping
| Requirement | Capability | Rationale |
|---|---|---|
| Slack assistant | Internal agent + Slack channel | Conversational, employee-facing |
| Policy Q&A / deflection | Agent + Article knowledge (RAG) | Language understanding |
| Read ME data for grounding | AirSync connector (5-min delta) | Bulk/periodic import, native pattern |
| Create/check ME tickets in real time | Agent HTTP skills → ME REST API | Real-time single actions; AirSync can't (no webhooks, near-real-time only) |
| Guided intake | Workflow with SEND_FORM / ASK_OPTIONS | Deterministic data capture |

Note the deliberate split: **AirSync inbound** (history/grounding, tolerates 5-min lag) vs **HTTP skills outbound** (must be real-time).

## 7. Architecture
Employee messages the IT assistant in Slack → agent classifies intent → policy/how-to → answer from KB (deflect); access/reset/hardware request → guided intake flow → `CreateMETicket` HTTP skill posts to ME → confirms with ticket ID; "what's the status of my ticket" → `CheckMETicketStatus` HTTP skill → conversational status. ME requests/solutions/users sync into DevRev every 5 min so the agent has context and the KB stays current.

## 8. Data model & object design
- Employees = **dev users / contacts** (synced from ME users).
- IT requests = **issues** (from ME requests via AirSync; ME status → DevRev stage mapping) — used for grounding/reporting; ME holds the master.
- Services = **parts** (service variant): IT, HR, Facilities → capabilities (Access, Hardware, Software, Onboarding).
- Change/Problem management (if in scope) = **custom objects** (as Razorpay modeled them).
- KB = **articles** (from ME solutions via AirSync + authored policy docs), scope internal.

## 9. Workflow & automation
| Workflow | Trigger | Logic | Outcome |
|---|---|---|---|
| Assistant deploy | Slack conversation created | `Talk to Agent` (internal, suspend-on-message-from=user) | Agent handles employee chat |
| Guided intake | agent invokes intake skill | `SEND_FORM(per request type: access/reset/hardware) → completeness check → CreateMETicket` | Well-formed ME request |
| Aging-request nudge | TIMER_TRIGGER (daily) | `LOOP_OVER_ISSUES(open > SLA) → SEND_NOTIFICATION(assignee, Slack)` | SLA hygiene |

## 10. AI components — IT Assistant (Internal agent)
- **Goal:** "Help employees resolve IT and HR requests: answer policy/how-to questions from the knowledge base, create properly categorized ServiceDesk requests through a guided flow, and report ticket status. Escalate to the IT team when you can't resolve or the request is urgent/security-related."
- **Knowledge (lean):** Article, Q&A, Issue (status lookup), Product/Capability (services), Dev User.
- **Skills:**
  - `search_it_kb` (tool) — object_types Manual `["article","question_answer"]`; "Use for every policy/how-to question before responding."
  - `CreateMETicket` (workflow with HTTP) — intent-classified (password_reset / access_request / hardware); "Use when the employee needs a new IT request and intake is complete. Confirm the ticket ID back."
  - `CheckMETicketStatus` (workflow with HTTP) — "Use when the employee asks about an existing ticket; resolve 'my last ticket' from context."
  - `escalate_to_it` (tool) — "Use for security incidents, urgent outages, or anything unresolved after intake."
- **Guardrails:** never grant access or reset credentials directly (only file the request); never share another employee's data; scope to IT/HR/Facilities topics only.
- **HITL:** access-request and any privileged action file a ticket for human approval in ME — the agent never provisions access itself.
- **Deployment:** internal agent surfaced in Slack; suspend-on-message-from=user for handoff to a live IT agent.

## 11. Analytics
- Deflection rate; requests by category/service; median time-to-resolution (from synced issues); top deflected topics (KB gap finder). Stock dashboards + custom vistas ("Open access requests", "Aging hardware tickets").

## 12. Integration strategy
- **Inbound — ManageEngine AirSync connector, 5-min delta:** `GET /api/v3/users` → dev users/contacts; `GET /api/v3/requests` → issues (status→stage map, comments synced); `GET /api/v3/solutions` → articles (KB for RAG). Delta via `last_modified >= {last_sync}`; API-key auth; pagination + rate limiting.
- **Outbound — agent HTTP skills, real-time:** `CreateMETicket` → `POST /api/v3/requests` (requester/category/template); `CheckMETicketStatus` → `GET /api/v3/requests/{id}`.
- Rationale: import tolerates 5-min lag (grounding); actions must be immediate → direct API, not an AirSync round-trip.

## 13. Security & permissions
- Employees interact under their own identity (agent Execute-as-User ON); the agent can never exceed the employee's permissions. Access requests always route to human approval in ME. Internal-only KB scope.

## 14-15. Plan & sequence
1. Parts (IT/HR/Facilities services + capabilities); issue status→stage mapping; any Change/Problem custom objects.
2. Build the ManageEngine AirSync connector (3 extractors); initial import; verify status mapping.
3. Author/seed IT & HR policy articles (+ synced ME solutions).
4. Build intake + aging-nudge workflows; build `CreateMETicket` / `CheckMETicketStatus` HTTP skills.
5. Configure the IT Assistant agent, skills, guardrails; deploy to Slack.
6. Dashboards + vistas; groups/roles.
7. Test (Playground + bulk evals + workflow traces); pilot with one department; expand.

## 16. Task breakdown (illustrative)
| Task | Complexity | Hours | Dependencies |
|---|---|---|---|
| Services parts + issue status mapping | Small | 10 | — |
| ManageEngine AirSync connector (custom, 3 extractors) | Large | 48 | ME API access |
| CreateMETicket / CheckMETicketStatus HTTP skills | Medium | 24 | ME API |
| Guided intake workflow | Medium | 16 | HTTP skills |
| IT Assistant agent + 4 skills + guardrails | Medium | 28 | intake + skills |
| KB seeding | Medium | 20 | — |
| Dashboards/vistas + rollout | Medium | 16 | data flowing |
Roll-up: Eng ~162h + QA ~45h + UAT ~24h + Docs ~16h + Deploy ~16h + Buffer ~20% ≈ 315h; overall ~8 weeks (matches the ManageEngine 36-story-point / 8-week reference).

## 16-20. Risks / alternatives / recommendation
- **Risks:** ME connector is a **new build** (Large), not an existing connector — main effort driver; ME API rate limits (mitigate: 5-min delta + pagination + backoff); status-mapping drift if ME workflows change; keeping ME as SoR means no create-in-DevRev of authoritative IT tickets (by design).
- **Alternatives:** A (fastest) Slack agent + KB deflection only, no ME writes — ships in ~3 weeks, no connector. B (most scalable/complete) inbound sync + outbound HTTP skills — this design. C (most maintainable) if migrating off ME eventually, model IT requests natively in DevRev and retire ME — larger change-management. **Recommend B** now; revisit C only if the org decides to consolidate onto DevRev as SoR.
- **Final:** start with A's deflection value while building B's connector in parallel, then layer in ticket create/status. Open questions: ME edition/API limits? which request types are in scope for automation? access-request approval policy?
