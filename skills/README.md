# skills/ — the 10 DevRev implementation domains

Numbered in **implementation-flow order** — the order a fresh org is built in, and the order to
reason in when a request spans domains (start at the lowest number involved; greenfield/cross-domain
requests start at 0):

| # | Skill | Owns | Type |
| --- | --- | --- | --- |
| 0 | `0-solution-architecture` | Turns a vague business problem into a 20-section DevRev solution blueprint (object/lifecycle mapping, workflow/agent capability selection, integrations, estimates, risk, A/B/C alternatives) | Design (references/ inline; never calls the live API) |
| 1 | `1-object-schema-customization` | Custom objects, tenant/subtype fields, field overrides, aggregated schema, custom link types | Knowledge-owner (references/ inline) |
| 2 | `2-stage-lifecycle-customization` | States → stages → stage diagrams, lifecycle assignment, dependent fields | Knowledge-owner |
| 3 | `3-data-upload-and-org-build` | Artifacts/file upload, ordered org builds, idempotent bulk loading | Knowledge-owner |
| 4 | `4-dashboards-and-widgets` | Routes into the `dashboard-dev` plugin (`/create-dashboard`, `/modify-dashboard`) | Router (knowledge lives in `repos/aai-skills`) |
| 5 | `5-datasets` | Routes into the `dataset-builder` plugin; PaaS vs Ponos decision | Router |
| 6 | `6-workflows` | WorkflowTemplateV2 authoring, import debugging, agent-callable skills (four-block pattern), workflow CRUD/trigger | Knowledge-owner (130 op schemas, working examples) |
| 7 | `7-agent-building` | Agent Studio create/debug/improve/test, guardrails, feature flags, NL2SQL annotations | Knowledge-owner (8 commands, 10 KB articles) |
| 8 | `8-devrev-api` | Every public REST endpoint — catalog + per-domain payload docs | Knowledge-owner (horizontal foundation) |
| 9 | `9-snapin-development` | Routes into the third-party `devrev` (`devrev-qk-agents`) plugin's snap-in vertical (PM/Architect/Tester); excludes that plugin's dashboard vertical | Router (knowledge lives in `repos/devrev-qk-agents`; plugin NOT auto-enabled — manual install) |

**Working rules**
- Always open the domain's `SKILL.md` first; it names the reference files that carry the exact
  endpoints, scopes, and payloads. Never reconstruct API facts from memory.
- Skills 1–3 duplicate their reference docs from skill 8 on purpose (self-containment). If a
  learning corrects a reference doc, fix **both** copies (the capture-learnings protocol says how).
- Skill 0's references cross-reference skills 1, 2, 6, 7, 8 for exact API mechanics rather than
  duplicating them — a design-time index over the same knowledge-owner reference files, not a third copy.
- Each SKILL.md ends with a **Field notes** (or domain-specific learning) section — dated facts
  discovered in live use. Read it; it overrides older text above it when they conflict.
