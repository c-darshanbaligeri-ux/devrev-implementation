---
name: implementation-router
description: Master router for all DevRev implementation work in this repo. Use for ANY DevRev request — designing an end-to-end solution for a business problem, customizing objects, fields, schemas, subtypes or custom links ("add a field to accounts"), stages/states/lifecycles ("customize ticket stages"), uploading files or migrating data or building a fresh org, dashboards and widgets ("build me a support dashboard"), custom datasets, workflows and automations ("when a ticket comes in, notify..."), agent-callable skills ("let the agent look up order status"), building/debugging/improving/testing AI agents, snap-ins or AirSync connectors ("build a HubSpot connector"), or raw DevRev REST API calls. Routes to the correct numbered domain skill under skills/.
---

# Implementation Router

Match the request to a domain, then **open that domain's SKILL.md and follow its playbook before
acting**. Never reconstruct API endpoints, payload formats, scopes, or JSON schemas from memory —
every fact must come from the matched skill's reference files.

## Routing table

| The user wants to… | Go to |
| --- | --- |
| Design an end-to-end solution for a business problem, or decide which DevRev capability fits a requirement ("should this be an agent or a workflow", "we're an [industry] company and need to...") | `skills/0-solution-architecture/SKILL.md` |
| Customize objects, fields, schemas, subtypes, custom link types | `skills/1-object-schema-customization/SKILL.md` |
| Customize stages, states, lifecycles, stage diagrams, transitions | `skills/2-stage-lifecycle-customization/SKILL.md` |
| Upload files/artifacts, migrate or bulk-load data, build a fresh org | `skills/3-data-upload-and-org-build/SKILL.md` |
| Create/modify/verify dashboards or widgets | `skills/4-dashboards-and-widgets/SKILL.md` |
| Create/manage custom datasets (Oasis, PaaS, Ponos) | `skills/5-datasets/SKILL.md` |
| Author/manage workflows, automations, agent-callable skills | `skills/6-workflows/SKILL.md` |
| Build, debug, improve, or test AI agents (Agent Studio) | `skills/7-agent-building/SKILL.md` |
| Any raw DevRev REST API call | `skills/8-devrev-api/SKILL.md` |
| Build, plan, update, or test a snap-in or AirSync connector | `skills/9-snapin-development/SKILL.md` |
| "Update the repos" / "pull latest" / "sync to main" | `.claude/skills/update-repos/SKILL.md` |
| Hit an unexpected error/restriction, discovered undocumented API behavior, or was corrected by the user — mid-task, any domain | `.claude/skills/capture-learnings/SKILL.md` (run it immediately, then continue the task) |

## Rules

1. **Read before acting.** Always open the matched SKILL.md first; it names the reference files
   that carry the exact endpoints, scopes, and payload formats.
2. **Preconditions.** A `.env` with `DEVREV_PAT` must exist at repo root. If it's missing, tell
   the user exactly what to put in it (see `.env.example`) and STOP — never fabricate a token.
   Before an API run, confirm the token with `POST https://api.devrev.ai/ping`.
3. **Route by intent, not keyword.** Examples:
   - "add a field to accounts" → 1 (schema customization, not raw API)
   - "tickets should go through a triage step" → 2 (lifecycle)
   - "load these CSVs into DevRev" → 3 (data upload)
   - "chart of open tickets per account" → 4 (dashboards)
   - "a dataset joining tickets and accounts" → 5 (datasets)
   - "when X happens, do Y" → 6 (workflow)
   - "the agent should be able to look up order status" / "create an AI agent skill" / "build a
     workflow tool" / "create an agent workflow" → 6 (agent-callable skill, four-block pattern).
     **Always start from `skills/6-workflows/examples/default-ai-agent-skill-template.json`** — the
     project default scaffold — then customize per `skills/6-workflows/references/ai-agent-skill-pattern.md`.
     Never hand-author the four-block wiring from scratch. In contrast, "make the agent smarter /
     fix the agent's answers / configure the agent" → 7 (agent config).
   - "call works.list" / "hit the API" → 8 (raw REST)
   - "build a connector for X" / "sync X into DevRev" → 9 (snap-in development) — but "build a
     dashboard/widget for X" always stays at 4, even if the user's phrasing echoes skill 9's plugin's
     own dashboard-vertical command names; that vertical is explicitly out of scope (see skill 9)
4. Cross-domain requests (e.g. a fresh org build) start at the lowest-numbered skill involved —
   `skills/3` orchestrates and routes back to 1 and 2 for the customization phases.
5. **Greenfield or genuinely cross-domain requests** ("we're a [industry] company, help us set up
   DevRev", "design a solution for X") start at `skills/0-solution-architecture` for the blueprint
   before any building begins — it hands off to the numbered execution skills section by section
   (see its "Handing off to execution" table). Don't skip straight to building when the ask is this
   broad; a five-minute blueprint prevents building the wrong thing.
