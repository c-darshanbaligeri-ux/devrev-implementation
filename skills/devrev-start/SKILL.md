---
name: devrev-start
description: Entry point for any task in a DevRev organization. Use first when the user asks to create, find, update, delete, analyze, configure, import, automate or integrate anything in DevRev — tickets, issues, accounts, customers, parts, articles, SLAs, custom fields and objects, stages, workflows, AI agents, dashboards, datasets, snap-ins or connectors — even if they name no API. Finds the right playbook and API endpoint with `devrev-find`, then reads only those files. Not for general coding unrelated to DevRev.
---

# DevRev operator — start here

You act on a live DevRev organization. Every endpoint, field, scope and id must come from this toolkit's files or from a real API response, never from memory. `devrev-find` searches the toolkit: it is on PATH when this plugin is installed; in a checkout of the repo run `./bin/devrev-find`.

## Procedure

**0. Preflight (once per task).**
- Token: `DEVREV_PAT` from the environment, else from `.env` in the working directory (`set -a; source .env; set +a`). If neither exists, tell the user to create a personal access token (DevRev Settings > Account > Personal Access Token), set `DEVREV_PAT`, and **stop**. Never fabricate one.
- Base URL `https://api.devrev.ai` (or `DEVREV_ENDPOINT` if set). Confirm the token: `curl -s -X POST https://api.devrev.ai/ping -H "Authorization: Bearer $DEVREV_PAT" -H "Content-Type: application/json" -d '{}'`.
- On 401/403 read `references/troubleshooting.md`; do not retry blindly.

**1. Find.** `devrev-find "<the goal in a few plain words>"`
- A **playbook** hit (a numbered skill) → open that skill's `SKILL.md` and follow it; it holds the procedure and the live-verified Field notes.
- **Endpoint** hits only → a plain API operation; go to step 2.
- Nothing relevant → `grep -rIil '<keyword>'` over the toolkit's `skills/`. If still nothing, say what you could not find. Do not invent.
- A goal that spans several skills (greenfield, "set up DevRev for X") → start at `skills/0-solution-architecture`.

**2. Brief.** `devrev-find --endpoint <name>` for each endpoint you will call. It prints scopes, required fields, the risk class, the vendor-doc section to read, and the repo notes and learnings that apply. Read only the files it lists.

**3. Resolve conflicts** in this order: learnings (`docs/LEARNINGS.md`) and a skill's Field notes, then that skill's reference docs, then the vendor mirror (`skills/11-developer-docs`). The mirror records what the docs *say*; this toolkit's notes record what was *verified live*.

**4. Act.**
- Use full DON ids (`don:core:dvrv-us-1:devo/<ORG_ID>:ticket/456`), never display ids like `TKT-456`.
- Send `-H "Authorization: Bearer $DEVREV_PAT" -H "Content-Type: application/json"`; prefer POST with a JSON body.
- The risk class decides what you do. **read**: run it. **write**: say what will change, then run it (a hook asks the user to confirm). **destructive**: stop, get explicit confirmation in this session, snapshot the ids it will affect, then run it. Details in `references/safety.md`.
- Run dependent steps one at a time and keep a scratchpad of returned ids.

**5. Verify.** Re-read with the matching `.get` / `.list` straight away and report the ids of what you created or changed.

**6. If reality differs from the docs or notes:** in a checkout of this repo run `.claude/skills/capture-learnings`; in an installed plugin tell the user exactly what differed (do not edit the plugin's files).

## Hard rules

1. Never fabricate an endpoint, field, scope, enum value, DON id or file path. If you cannot find it, say so.
2. Never print or log a token, and never paste one into a website (jwt.io included).
3. Destructive calls (`*.delete`, `*.merge`, `objects.bulk-upgrade`, `schemas.custom.set`, creating custom stages or states, `web-crawler-jobs.control`) need explicit confirmation in this session.
4. Do not hand-write dashboard or widget JSON, or snap-in code. Use skill 4's and skill 9's pipelines.
5. Beta endpoints can change without notice. Use them only when the user asks or no public endpoint exists.
6. Ask the user only when a required value cannot be found or the action is destructive; otherwise proceed.
7. A custom-field write with the wrong prefix fails silently. See `references/global-api-rules.md`.

## Toolkit map

| Need | Open |
| --- | --- |
| The 12 playbooks | `skills/<N>-…/SKILL.md`: 0 design, 1 objects/fields, 2 stages, 3 data load, 4 dashboards, 5 datasets, 6 workflows, 7 agents, 8 REST API, 9 snap-ins/AirSync, 10 API conventions, 11 official docs |
| Rules that apply to every call | `references/global-api-rules.md` |
| Destructive-call list and confirmations | `references/safety.md` |
| Common goals and where to start | `references/goal-map.md` |
| Setup problems and error fixes | `references/troubleshooting.md` |
| Verified corrections to the docs | `docs/LEARNINGS.md` (the finder surfaces the relevant rows) |
