# DevRev Integrations, Channels, Analytics, Users & Notifications

Use this reference for the **supporting layers** of a solution: how data gets in (integrations/sync), how customers reach the org (channels), how it's measured (analytics), who can see what (users/permissions), and how people get told (notifications).

## Table of contents
1. Integrations & AirSync
2. Channels
3. Analytics & reporting
4. Search & knowledge
5. Users & permissions
6. Notifications & messaging

---

## 1. Integrations & AirSync

AirSync (formerly Airdrop) is DevRev's bidirectional sync engine — imports/synchronizes data between DevRev and external platforms, preserving context, relationships, and permissions, unifying data into the Knowledge Graph. Near-real-time via periodic sync runs (default hourly). "Event-driven ETL": Extract → Transform → Load, with optional write-back.

**Three sync modes (per connector):**
- One-time import — full migration (source is being discontinued).
- One-way sync — ongoing external → DevRev (coexistence).
- Two-way sync — bidirectional.
- Recipe manager — choose which object types/fields to sync.

An initial import is always a prerequisite to any sync.

**Native connectors vs ADaaS snap-ins:** Jira and Salesforce are native/built-in. Almost all other connectors are snap-ins built on the ADaaS SDK, delivered via the Marketplace. Install the appropriate AirSync snap-in before configuring an import. 50+ connectors (Jira, Salesforce, Zendesk, HubSpot, ServiceNow, Linear, Freshdesk, Intercom, Confluence, Google Drive, OneDrive, Figma, Slack, Gmail, Snowflake, Shopify, Okta, Azure Entra ID, and more).

**When NOT to use Airdrop:** real-time/event updates, enrichment without import, new-items-only (no history), or pure outbound posting — use standard snap-ins, webhooks, events, or APIs instead.

**Domain model:** External system → External sync unit (Jira project / Salesforce org / Linear team) → Sync unit (DevRev-side) → Sync runs. Each imported object gets a **sync mapper record** mapping external ID ↔ DevRev DON; external objects map 1:1 to DevRev objects. **EDM/IDM** define the mapping; the **Chef UI** builds it interactively.

**Representative source → DevRev mappings:**
- Salesforce: Case/Problem/Incident → Ticket (2-way); Account → Account; Contact → Contact; Opportunity → Opportunity (2-way); Knowledge Article → Article; Quote/Order/Asset/custom → Custom Object.
- Zendesk: Ticket → Ticket (2-way); Organization → Account; Agent → Dev User; End User → Contact; Article → Article; Category → State/Stage.
- Jira: Issues → Issues (2-way hourly); Epics → Enhancements. JSM: orgs → accounts, customers → rev users, public/private comments → external/internal messages.
- Gmail: email conversations → DM/Chat. Confluence/Drive/OneDrive/Figma: KB/document import.

**Periodic sync & automations:** the "Enable automations for synced items" toggle controls whether created/updated items trigger events, webhooks, notifications, and snap-ins. First-time imports and manual syncs never trigger events.

**Deletion/persistence:** removing a connection only severs the link (no data deleted); deleting a sync unit is destructive; deleting a source record does NOT delete the DevRev copy (safety). Archive a sync unit to stop syncing while keeping data.

### Connector-specific detail (for the build)
- **Salesforce** — modes: bulk / 1-way / 2-way. Case/Problem/Incident→Ticket (2-way), Account→Account, Contact→Contact, Opportunity→Opportunity (2-way), Product→Product, Knowledge Article→Article, Quote/Order/Asset/Task/Event/custom→Custom Object; **Lead does NOT sync**. Requires an edition with API access (Enterprise/Unlimited/Developer/Performance) and (post-2025) "Use Any API client" permission. To flag a DevRev ticket for sync-back, set subtype `SalesforceService / cases` at creation. Custom Account/Contact fields arrive as **app-fragment fields** — not filterable and no field-level permissions.
- **Zendesk** — connecting user **must be an admin** (incremental endpoints require it). Ticket→Ticket (2-way), Comment→Comment (2-way), Organization→Account, Agent→DevUser, End User→Contact, Article→Article, Category/Status→State/Stage. Chat/SLA/Macro/Custom Object do **not** sync.
- **Jira** — 2-way (Cloud OAuth; Data Center v10.3+ PAT). Issue↔Issue/Ticket, Epic↔Enhancement, Comment↔Comment, Label↔Tag, Link↔Link, Attachment↔Attachment, Status↔State/Stage, Workflow→stage diagram (Cloud only). Sprints not imported (land as a text field). Sub-tasks need a synced parent. Reverse-sync link types limited to is_dependent_on/is_duplicate_of/is_parent_of/is_related_to. **JSM** is a separate 1-way connector (issues→tickets; orgs→accounts; public/private comments→external/internal).
- **DevRev↔DevRev** — org migration/cloning; imports most objects but **not Tasks or Attachments**.
- **Confirmed connectors, partial mapping detail:** HubSpot (admin required), ServiceNow (bidirectional ITSM/CSM), Freshdesk, Intercom (conversations/contacts/companies/tickets/articles), Slack (1-way, Enterprise Grid), Gmail (→DM/Chat), Google Drive, Notion (hierarchy flattens), Confluence (**PAT required, no OAuth**), Azure Boards (bidirectional), GitHub Issues (bidirectional; no attachments), Airtable (PAT), SAP SuccessFactors (read-only). **No AirSync connector articles found for Shopify, Okta, or Azure Entra** — do not assume they exist as native connectors.

### Generic AirSync limits (all connectors)
Attachments >250 MB skipped; parent/child link depth >3 dropped; a contact can't belong to multiple accounts; **deletions do not sync**; only current state syncs (no change history). Dedup: users by email (no email → "Unassigned", no match → "Shadow" user). Each imported object gets a **sync mapper record** (external ID ↔ DON). **Pending Records** (custom objects prefixed `C-PEND-`) hold records that failed to sync in, with the failing payload, for admin re-sync. Sync statuses: Succeeded / Modified / Staged (constraint violated — resolve) / Failed.

### Snap-in framework quick facts (for integration design)
Manifest v2 sections: `service_account` (identity + `<object>:<op>` scopes; new required scopes can't be added on upgrade), `inputs` (org/user config), `keyrings` (org / user [always optional] / developer [hidden, cross-install]), `event_sources`, `functions`, `automations` (source+event_types→function), `operations` (3P workflow nodes), `commands` (slash), `hooks` (activate/update/deactivate/validate), `snap_kit_actions` (UI), `tags`, `imports` (ADaaS only).
Event source types: `devrev-webhook` (+ JQ filter), `flow-custom-webhook` (+ Rego validation, HMAC verify), `flow-events` (self-dispatched/deferred), `timer-events` (cron/interval → `timer.tick`), `email-forward` (`email.receive`). In functions: keyrings at `event.input_data.keyrings['name'].secret` (or `.access_token`); service-account token at `event.context.secrets.service_account_token`; endpoint at `event.execution_metadata.devrev_endpoint`.

---

## 2. Channels

All inbound customer communication lands in a single **omnichannel Support Inbox**; every channel maps to Conversation and/or Ticket objects. A Conversation is a real-time thread (SLA = time to response); a Ticket is a tracked follow-up request. An AI layer (Turing / CX Agent) attempts resolution from KB/FAQ/Q&A before a human is involved.

- **PLuG widget** (web/in-app/mobile) — DevRev's engagement center, embedded via SDK. One SDK powers AI chat, live chat, KB semantic search, and **nudges** (proactive outbound). Web: `window.plugSDK.init({app_id})`. Mobile SDKs (iOS/Android/RN/Flutter/Expo). Styled code-free in Settings > PLuG & Portal. Also carries session replay/observability. Multiple PLuG instances possible via multiple dev orgs.
- **Email** — Email snap-in; customers email a support address (auto-creates ticket/conversation) or use the portal. Reply routing depends on the ticket's Channel field.
- **Slack** — Slack snap-in; sync Slack conversations into the inbox, create tickets/issues from Slack (`/devrev create-issue`), notifications to channels, two-way commands. 5-min notification cooldown; threads not synced.
- **WhatsApp** — WhatsApp snap-in; routes into the omnichannel inbox.
- **Microsoft Teams** — supported/available channel; less documented than Slack/Email/WhatsApp.
- **API / Webform / Portal** — programmatic conversation/ticket creation; Customer Portal / Help Center with searchable KB, form submission, threaded conversations.
- **Telephony** — native Twilio integration auto-creates a ticket per call with transcript/recording.

**Agent deployment to a channel is workflow-driven** (not a toggle): the channel must be active + creating Conversations; a Conversation Created trigger fires a Talk to Agent node. Node fields: Agent, Object, Visibility, Panel, Respond-to-user-types, Suspend-on-message-from (human handoff), Quick replies, Additional context. Talk to Agent = one-way handoff; Ask Agent = two-way skill.

---

## 3. Analytics & reporting

Analytics runs on an in-browser DuckDB layer over summary tables — sub-second queries over millions of records; backed by a multi-tenant warehouse with full change history.

- **Vistas** — customizable real-time list views/queries across objects. The primary tabular working object.
- **Dashboards** — collections of **widgets**; refresh ~every 60 minutes (not real-time). Local-timezone display; CSV export.
- **Vista Reports** — dashboard-based reports scoped to a vista; powered by dashboards (widget containers) + datasets (SQL tables). Access via Explore.
- **Widget Builder** — each widget has a backing SQL query; define data source, measures, dimensions, filters, groupings, visualization (metric tile, table, bar, line, donut, pie, stacked, heatmap). Widget Builder 1.5 adds cross-object widgets, pivot tables, drill-through, auto-refresh, CSV export.
- **Stock dashboards** ship ready to use; **custom dashboards** use custom fields/objects.

Stock support dashboards: Conversation Insights / SLA / Team Performance; Ticket Insights / SLA / Team Performance; Article Analytics; Turing Analytics; Search Agent Analytics; Session Analytics / Session 360; Airdrop Analytics; Sprint Insights (burndown); Dev360, People360, Product360, Customer360.

What can be measured: **CSAT** (automations for conversations/tickets; widgets; negative-CSAT notifier), **SLA** (compliance, breaches, resolution time by team/priority), **resolution & response time** (median recommended, exclude cancelled), **agent/team performance**, **volumetrics by channel/type**, **session/product analytics** (DAU/WAU/MAU, adoption, funnels, error timelines).

Distribution: CSV/Excel export (50k-row cap); scheduled/automated report distribution via the workflow engine + email; NL2SQL conversational analytics ("talk to your data").

---

## 4. Search & knowledge

- **Global search (Cmd+K)** across tickets, issues, articles, customers, feedback, conversations, comments; filter by type/creator/date.
- **Semantic search** (vector embeddings; permission-aware) powers RAG. **Hybrid search** = keyword + vector (`search.hybrid`).
- **Enterprise Search** — AI search over structured + unstructured data (desktop app, browser extension, Slack bot); indexes DevRev objects plus external sources brought in via AirSync; in-line citations; permission-aware.
- **Knowledge base / Articles** — grouped into **collections**; content blocks (rich text), versioned, `applies_to_parts`. Scope: `internal` vs `external` (published to Portal/Plug). Permissions via `shared_with`. Ingest from Google Drive, Notion, PDF/HTML/Markdown, or connect external KBs via URL/sitemap. Only published articles are used by AI. Auto-generate articles from resolved tickets; **Q&A pairs** from resolved conversations improve deflection.
- **Customer Portal / Help Center** — self-service portal with searchable KB, ticket submission (auth + unauth), threaded conversations, multi-workspace, localization, JIT contact provisioning, custom domain/branding, email-OTP auth.

---

## 5. Users & permissions

Three **actor** types: Organization members (Dev Users), Customers (Rev Users/Contacts, managed via customer groups), Service Accounts (Sys Users).

Access-control model (MFZ): **Groups → grant Roles → grant Privileges (Create/Read/Update/Delete/List) → allow actions.** Layers:
- **RBAC** — roles via groups.
- **ABAC / caveats** — roles conditioned on object attributes (e.g. only if `priority == p0`).
- **Field-level ACL (FieldACL)** — read/write per field, per subtype.
- **ReBAC / Object Members** — connect users/groups to objects for per-object role assignment (sharing).
- Roles are **additive** (union of highest applicable privileges).
- **Internal vs external roles** — internal govern org members; external govern customers on Portal/Plug (Settings > Customer Management > Roles).

**Groups:** user groups (internal defaults: Admins, All Users [dynamic], Platform Users, Support, Agent and Automations Admin — only Support gets Plug-inbox updates); customer groups (Customers, Customer Admins, Verified Customers). Static (manual) vs dynamic (rule-derived) groups.

**Teams & Spaces:** teams are collections of users + groups with a Space admin; team-scoped display IDs (e.g. `ENG-12`). Group hierarchy is a prerequisite for Space hierarchy.

**Identity:** SSO via SAML (JIT provisioning); SCIM 2.0 with Okta and Microsoft Entra ID (SCIM users created in Shadow state until first login; requires SSO). Tokens: PAT, AAT, Rev session tokens. Audit logging; SOC 2 Type II / ISO 27001.

**Rev-user access on tickets:** Reported By (may have edit access), Subscribers (always access + notified), email_members/slack_members (channel participants, always access).

---

## 6. Notifications & messaging

- **Updates page** (in-app notification center) — priority tabs: Important, Others, Muted. Bell-icon subscription per record; filters by record type / notification type / notified-by.
- **Priority routing:** Important → all channels (in-app, email, push, integrations) + badge/sound/toast; Others → in-app only; Email → after a 5-min delay if unread; Push → immediate.
- **Personalization** — toggle Reminders, Assignments, Group Mentions, Mentions, Comments, Attribute updates.
- **Push (mobile SDK)** — for new PLuG chat messages; register FCM/APNs device token.
- **Customer email (white-label)** — default sender `notifications@devrev.ai`; override to org's support address with branding; customer replies append to the ticket/conversation.
- **Slack notifications** — configurable channel IDs for ticket/conversation/incident; state-update notifications; marketplace notifier snap-ins (SLA Status Change, SLA Breach, Blockers, negative CSAT).
- **Workflow-driven notifications** — on any event via email/in-app/Slack/webhook with custom content/recipients.

---

## Solution-architecture cheat sheet (supporting layers)
- **Integration layer:** install per-source AirSync snap-in → initial import → choose 1-time/1-way/2-way → recipe & field mappings → periodic sync (hourly) with "automations for synced items" if downstream workflows should fire. Native = Jira/Salesforce; else ADaaS snap-ins. Use standard snap-ins/webhooks/APIs (not Airdrop) for real-time/event/enrichment/outbound-only.
- **Channel layer:** PLuG, Email, Slack, WhatsApp, Teams, API, Portal, Telephony → omnichannel inbox → Conversation/Ticket. Deploy agents to channels via workflow (Conversation Created → Talk to Agent).
- **Reporting layer:** Vistas (real-time) → Vista Reports/Dashboards (~60-min, widget + dataset). Stock dashboards for support; custom via Widget Builder (SQL/DuckDB). CSAT/SLA/resolution/agent-perf measurable; export CSV; schedule via workflows.
- **Identity layer:** Dev/Rev/Service users; Groups (static/dynamic, user vs customer) → Roles (internal/external) → CRUD + caveats + field-level ACL, additive. SSO (SAML), SCIM (Okta/Entra), tokens, audit.
- **Notifications layer:** Updates page; in-app + email (5-min) + push + Slack/webhook; white-label customer emails; workflow-driven event notifications.
