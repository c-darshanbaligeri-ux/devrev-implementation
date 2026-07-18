# Estimation, Risk & Delivery

Use this reference when the solution needs an implementation plan: effort estimates, complexity sizing, risk analysis, alternative designs, and a rollout/monitoring/maintenance plan. Base numbers on realistic enterprise implementation experience, not optimistic assumptions.

## Table of contents
1. Complexity sizing
2. Effort estimation model
3. Task breakdown format
4. Risk analysis
5. Alternative designs (A/B/C)
6. Deployment, testing, rollout, monitoring, maintenance

---

## 1. Complexity sizing

Classify each build unit (an object, a workflow, an agent, an integration) into a tier. The tier drives the hour estimate.

| Tier | What it looks like | Typical effort feel |
|---|---|---|
| Very Small | One config change: a custom field, a subtype, a single stock dashboard enablement, a one-node notification. | Hours. |
| Small | A simple object with a few fields; a 2-4 node workflow; a native tool as an agent skill; enabling a standard AirSync connector. | ~1 day. |
| Medium | A custom object with a stage diagram; a branching/looping workflow; an agent with 3-5 skills + guardrails; a hybrid AI+workflow; a custom dashboard with several widgets. | A few days. |
| Large | Multi-object domain model with links + field-level ACL; a multi-agent orchestration; a snap-in with custom operations; a bespoke AirSync mapping (custom object, EDM/IDM via Chef UI); a PLuG customization. | 1-2+ weeks. |
| Enterprise | End-to-end program: full domain model + integrations + agents + dashboards + permissions + change management across teams/regions. | Multiple weeks to months, phased. |

Sizing signals that push a unit up a tier: custom code, external OAuth/token management, data migration, deep branching (>3-4 levels), field-level security, multi-region/multi-tenant, regulatory/compliance requirements, and net-new connectors (vs. existing ones like Salesforce/Zendesk/HubSpot, which are ~24-hr setups, not builds).

---

## 2. Effort estimation model

For each task give **Estimated Hours** and **Dependencies**, and explain *why* the estimate was chosen (the driver — e.g. "Large because it needs a custom AirSync mapping + field-ACL"). Then roll up the program:

- **Total Engineering Hours** — build/config/custom dev.
- **QA Hours** — typically 25-40% of engineering.
- **UAT Hours** — customer acceptance support.
- **Documentation Hours** — runbooks, admin docs, handover.
- **Deployment Hours** — publish, canary, cutover.
- **Buffer** — 15-25% for clarification, debugging, rework (higher when requirements are ambiguous or many net-new integrations exist).
- **Overall Timeline** — calendar time given parallelism and dependencies, not just summed hours.

Account for the full lifecycle in estimates: requirement clarification, solution design, configuration, custom development, snap-ins, PLuG development, workflow creation, testing, debugging, documentation, deployment, UAT support, and production rollout.

Reference points from DevRev delivery: existing connectors ≈ 24-hr setup tasks; proprietary connectors are new builds sized S/M/L; agents are sized S/M/L by skill count and reasoning complexity.

---

## 3. Task breakdown format

Present the plan as a table, ordered by dependency:

| Task | Complexity | Estimated Hours | Dependencies |
|---|---|---|---|
| Create loan_app custom object + stage diagram | Medium | 16 | States/stages defined |
| Salesforce AirSync mapping to loan_app | Large | 40 | Custom object exists |
| Document-chase workflow | Small | 8 | loan_app stages |
| Applicant Assistant agent + 3 skills | Medium | 24 | Workflows exist as skills |
| ... | ... | ... | ... |

Follow the table with the roll-up (Total Eng / QA / UAT / Docs / Deployment / Buffer / Overall Timeline) and one line per non-obvious estimate explaining its driver.

---

## 4. Risk analysis

Identify and give a mitigation for each relevant risk category:
- **Technical risks** — approach unproven, complex branching, custom code fragility.
- **Product/DevRev limitations** — e.g. `workflows.create` builds a shell only (node wiring is manual UI); custom-object fields default to no access and need explicit ACL; `uenum` unsupported for user-defined custom fields; `composite`/`struct` have limited UI/Airdrop mapping; Teams channel less documented than Slack/Email/WhatsApp; scheduled report distribution and proactive multichannel outbound may be roadmap. State the limitation plainly and route around it (e.g. use a `timer-events` snap-in for code-defined scheduling).
- **Performance bottlenecks** — large loops (`While` caps at 1000), high-volume workflow triggers, dashboard refresh (~60 min, not real-time), AirSync frequency.
- **Security concerns** — field-level exposure, external-role scoping, agent Execute-as-User vs system-level.
- **Scalability risks** — event volume, connector limits, agent token cost (Reflection ~2×).
- **Migration risks** — 1:1 external↔DevRev mapping, staged-record data-model violations, no deletion sync, initial-import-required-before-sync.

Each risk: likelihood/impact in a word, then the mitigation.

---

## 5. Alternative designs (A/B/C)

When a requirement has materially different viable approaches, offer up to three and compare trade-offs:
- **Option A — Fastest implementation.** Most native/config-only, least custom code. Ships soonest; may trade flexibility.
- **Option B — Most scalable.** Handles the highest volume/complexity; more upfront build.
- **Option C — Most maintainable.** Cleanest to operate and evolve; favors fewer, broader components and native features.

Give a short trade-off table (effort, scalability, maintainability, risk) and a clear recommendation with the reason. Don't manufacture three options when the choice is obvious — say so and move on.

---

## 6. Deployment, testing, rollout, monitoring, maintenance

- **Deployment plan** — order of publishing (schema → integrations → workflows → agents → dashboards → permissions); use versioning; canary/staged where supported.
- **Testing strategy** — workflow run traces; agent Playground (10-15 inputs) + Traces + bulk evals with evaluators (answer relevance, groundedness, deflection, CSAT); validate stage-diagram transitions and field-ACL before go-live; fix priority Task Success first, then Accuracy.
- **Rollout strategy** — phased (Phase 1 objects+automation → Phase 2 agents/skills → Phase 3 optimization); change management for affected teams.
- **Monitoring** — workflow analytics (run counts, error hotspots), agent observability (session tracing, token usage, guardrail triggers), SLA/CSAT dashboards, log streaming to SIEM/Datadog.
- **Maintenance plan** — owner for each component, versioning/rollback discipline, KB/Q&A tuning cadence, connector health checks, periodic review of deprecated stages/fragments.
