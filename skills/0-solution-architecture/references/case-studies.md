# Case Studies: Real DevRev Implementations

Grounding evidence from real DevRev deployments — use these to calibrate what's achievable, cite realistic outcome ranges, and borrow proven architecture shapes. Metrics are as documented; distinguish **validated production** numbers from **PoC/projected** ones (flagged).

> Guidance: use these to set expectations and pattern the design, not as guarantees. Every customer differs. When you cite a metric in a blueprint, frame it as "comparable deployments have achieved…", not a promise.

## Support automation & deflection

- **BILL (BILL.com), fintech** — CX agent deployed *inside Salesforce Service Cloud* (SFDC stayed system of record). Problem: 2M+ queries/year at ~$15/case, ~$12M support cost. Architecture: Computer CX Agent + centralized Memory + first-of-its-kind DevRev agent↔Salesforce Live Chat integration; Airdrop to Salesforce; Five9 telephony via SFDC. Outcomes: 73% deflection in PoC, 70% AI resolution validated, **40% of tickets deflected in production**, ~$6M projected annual savings (target $4.5M exceeded), 100% segment deployment in 15 weeks, ~3-month payback.
- **Descope, SaaS auth** — scaling 10M→300M daily sessions without added headcount. Architecture: AirSync lifecycle tracking + conversational AI + Memory + automated workflows. Outcomes: **54% lower avg resolution time**, 5× faster resolution, 100% SLA adherence at scale, 32–40% AI self-service resolution.
- **FOSSA, SaaS** — phased build (one of the clearest reference architectures). Migration: 10,000+ Zendesk tickets via AirSync + 2-way Jira sync + customized ticket forms. Optimization: AI sentiment + severity tagging via Agent Studio + automated workflows/alerts. AI adoption: ticket clustering + root-cause detection + Search Agent. Outcomes: **40% faster resolution, 57% drop in resolution time, backlog cut 100+ tickets**.
- **smallcase, APAC fintech** — 10M+ retail investors; multiple dev orgs = separate PLuG instance/KB/appearance per website section; migrated off Intercom; AI Q&A classification. Outcomes qualitative (anonymized): fewer tickets, faster resolution, higher agent productivity.
- **Velocity Global** — migrated **900,000 tickets + 600 macros** via Airdrop; near-perfect First-Response & Full-Resolution SLA; 30% response-time reduction, 25% CSAT increase, 40% operational efficiency; 350+ users; 1.3M+ monthly workflow runs.
- **Uniphore** — migrated 16K tickets / 72K comments / 17K attachments in **6 hours** via AirDrop; bidirectional Jira sync; 25% resolution-time and 30% bug-fix-time reduction.

## Support ↔ engineering convergence (product+support)

- **ActionIQ, SaaS** — unified engineering incidents with customer tickets; structured workflows + automation + AI insights. Outcomes: **67% reduction in median incident resolution, 50% faster ticket resolution, 60% faster response turnaround, 68% more L1-closed incidents/agent/month**.
- **Skedulo** — reduced ticket overhead 30%→5% (6× improvement); ~15 workflows per ticket lifecycle; Jira integration; migrated off Salesforce.
- **Rexera, real-estate ops** — CX Agent (email + in-app chat + Slack); User Insights; AirSync↔Jira mapping epics→enhancements; approval workflows; **Vista customizations**; **55% deflection for internal agents**.
- **Shipsy, logistics** — Agent Studio workflows auto-create tickets; AI sentiment-based prioritization; comment sync via Airdrop; native Jira issue creation; aging-ticket + SLA-breach automations; users resolved issues 30% faster.

## Product / user insights

- **L&T Financial Services** — session replay + funnel analytics across a native Android app; Memory unifying support/product/eng. Outcomes: improved UX across 3M+ sessions, reduced drop-offs, higher loan-application/account-opening conversion.
- **ICICI Prudential** — resolution time 48hrs→2hrs via session replay + logs + stack traces.

## ITSM / internal IT & HR

- **Camping World** — 1,400 flat-rate technicians; DevRev cut research time from **60→21 min/day**; ITSM + service-technician scope. Pricing model documented: ~$100K platform + $1.50/AI-action.
- **Penumbra** — two-phase: Phase 1 enterprise search across Salesforce/ServiceNow (weeks 1–4); Phase 2 ITSM workflow automation — ticket triage, HR onboarding (weeks 5–10).
- **ManageEngine ServiceDesk Plus integration** — reference architecture: Computer as employee-facing IT interface, ME as ITSM system of record. Inbound = AirSync connector every 5 min (users/requests/solutions). Outbound = agent HTTP skills (`CreateMETicket`, `CheckMETicketStatus`) + KB-grounded deflection agent. 36 story points / 8-week plan.
- Positioning benchmarks (ITSM decks): 60%+ IT tickets resolved without human touch; 25–40% opex reduction; 40–60% less manual triage via intelligent routing.

## Worked configuration examples (borrow these shapes)

- **Sayyam / PayRupik (NBFC), email-to-resolution** — Email snap-in converts inbound email → ticket. An *Ask Computer* workflow fires on ticket creation, calls the *Sayyam Support* agent **once** (classify + KB search + eligibility), atomically sets Category/Sub-Category/Group, posts a KB reply as an external comment; L2 handled by humans. Regulatory emails (RBI/CP-GRAMS/cyber) get **zero automated response** (guardrail). Runs entirely in the DevRev Support App.
- **DevRev-internal reference workflows** — (1) *Service Request Deflection & Assist*: PLuG conversation → keyword auto-assign → Turing answers (deflection) → `/assist` suggests response → rep edits/sends → resolve; metrics = deflection rate, Time@1↔Time@4 first response. (2) *Bug Resolution/Convergence*: PLuG conversation → assign rep → create ticket, assign part, add bug tag, set severity, move stage Queued→Awaiting product assist → notify part owner, review SLA.
- **Razorpay** — custom objects for Change and Problem Management (ITSM); multi-Jira-field → single-DevRev-field mapping; Coralogix integration; Slack→ticket.

## Effort & delivery reference points

- Existing connectors (Salesforce, Zendesk, HubSpot) ≈ 24-hr setup tasks, not builds; proprietary connectors are new builds sized S/M/L.
- Applied AI (AAI) services scope by artifact type (AI Agents, Connectors, Analytics, App Integrations, Automations, Workflows) with T-shirt sizing; ~90% dashboard auto-generation.
- Phased rollout is the norm: migrate + core workflows → agents/skills → AI optimization. BILL hit 100% deployment in 15 weeks; Penumbra ran a 10-week two-phase plan.

## How to use these
- **Calibrate expectations:** deflection 40–73%, resolution-time reductions 25–67%, opex reductions 25–40% are the observed ranges for well-scoped support/ITSM builds.
- **Borrow architecture shapes:** "external system stays system of record + AirSync in + agent HTTP skills out" (BILL, ManageEngine); "migrate → optimize → AI-adopt phases" (FOSSA); "one agent, called once per ticket, sets fields + posts KB reply" (Sayyam).
- **Distinguish measured vs projected:** BILL 70% (PoC-validated), ActionIQ/Descope/FOSSA (measured) vs many ROI slide figures (projected/marketing). Say which when you cite.
- **Under-documented verticals:** internal-HR transformation and production RevOps have thinner public evidence — design them from first principles, flag the lighter precedent.
