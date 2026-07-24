# DevRev Implementation Operating Environment

## Identity

This is the unified operating environment for all DevRev implementation work, including snap-in development (via a routed third-party plugin, `skills/9` — the one area not covered by this repo's own native skills). It is not a buildable software project — it's a workspace containing skills + references + cloned toolchains (`repos/`) + a hosted DevRev MCP. Everything needed to design a solution, customize DevRev organizations, upload data, build dashboards, create datasets, author workflows, develop AI agents, and build snap-ins/AirSync connectors lives here in a plug-and-play configuration, spanning design (skill 0) through build (skills 1–9).

## Routing table

When the user asks to work with DevRev, match the request to a skill and **read that skill's SKILL.md before acting**. Never reconstruct API formats or JSON structures from memory.

| The user wants to… | Route to |
| --- | --- |
| Design an end-to-end solution for a business problem ("how would I build X in DevRev", "we're a fintech and need to...", "should this be an agent or a workflow") — before any building starts | `skills/0-solution-architecture` |
| Customize objects, fields, schemas, subtypes, or custom link types ("add a field to accounts", "create a custom object", "define a subtype") | `skills/1-object-schema-customization` |
| Customize stages, states, or lifecycles ("customize ticket stages", "add a state", "define transitions") | `skills/2-stage-lifecycle-customization` |
| Upload files, attach artifacts, migrate data, build a fresh org, bulk-create records ("load these CSVs", "import data", "build an org from scratch") | `skills/3-data-upload-and-org-build` |
| Create or modify dashboards or widgets ("build me a support dashboard", "add a chart", "verify the dashboard") | `skills/4-dashboards-and-widgets` |
| Create custom datasets ("Oasis dataset", "Ponos job", "PaaS job", "dataset schema") | `skills/5-datasets` |
| Work with workflows, automations, or agent-callable skills ("when a ticket comes in, notify…", "the agent should be able to look up order status") | `skills/6-workflows` |
| Build, debug, improve, or test AI agents ("configure the agent", "add a skill to the agent", "test the agent's guardrails") | `skills/7-agent-building` |
| Make any raw DevRev REST API call ("call works.list", "get account details", "create a ticket via API") | `skills/8-devrev-api` |
| Build, plan, update, or test a snap-in or AirSync connector ("build a HubSpot connector", "sync Asana into DevRev", "add pagination to the Trello connector") | `skills/9-snapin-development` (routes to a third-party plugin, manual install required — never `skills/4`'s dashboard vertical) |
| "Update the repos" / "pull latest" / "sync repos to main" / "refresh the cloned repos" (explicit request only — never automatically) | `.claude/skills/update-repos` |
| "Remember this so we don't hit it again", any correction, any undocumented restriction/behavior discovered mid-task | `.claude/skills/capture-learnings` (routes the fix to the specific owning file + `docs/LEARNINGS.md`) |
| Route unclear or genuinely spanning multiple skills | `.claude/skills/implementation-router` (uses this same routing table to pick a skill, or picks the lowest-numbered one for cross-domain requests) |

**Rule**: open the matched SKILL.md file and follow its playbook. Do not reconstruct API endpoint formats, payload structures, scope names, or JSON schemas from training data — every API fact must come from the skill's reference files.

## Plug and play

This repo requires **one manual step** to activate: create `.env` from `.env.example` and populate `DEVREV_PAT` + `DEVREV_ENDPOINT`. Once `.env` exists, a `SessionStart` hook (`.claude/hooks/bootstrap-workspace.sh`) auto-configures the environment on session start:

1. **Workspace directories**: creates `dashboards/`, `datasets/`, `plans/`, `logs/`, `templates/` synchronously.
2. **Toolchain repos clone** (background, once): if any repo in `repos.txt` is missing, loops over the non-comment lines and clones each to `repos/<name>`. Clone status logs to `.claude/.auto-setup/install.log` and appends a per-machine result table to `docs/CLONE_RESULTS.local.md` (gitignored). The curated `docs/CLONE_RESULTS.md` is the build-time snapshot and is not touched by the hook.
3. **`dashboard-sync` CLI install** (background, once): if `dashboard-sync` is not on PATH and no install is already running, installs `pipx` via Homebrew (if missing) and then `pipx install git+https://github.com/devrev/dashboard-sync-cli.git`. Logs to `.claude/.auto-setup/install.log`.
4. **Dashboard workspace init**: once the CLI is present, runs `dashboard-sync init` once (tracked by the `.claude/.auto-setup/init.done` marker, since this repo pre-creates `dashboards/` itself).
5. **Plugin hook**: the `dashboard-dev` plugin's own `SessionStart` hook generates `config.yaml` from `.env`.

**First session after adding `.env`**: accept the workspace-trust prompt to activate the committed plugin marketplace (`devrev-aai-plugins` from `.claude/settings.json`). The CLI install runs in the background — give it a minute, then **start a new session** so PATH picks up `~/.local/bin/dashboard-sync` (a hook can't refresh the shell PATH of its own already-running session).

**If `.env` is missing**: the repo stays inert; the bootstrap hook prints a message telling you to create `.env` and exits. The agent must tell the user exactly what to put in `.env` and stop — never fabricate a token.

**Ponos-only tools** (`gcloud`/`bq`, AWS CLI with SSO, `kubectl`) are NOT auto-installed — they require interactive login. `/dataset-builder:setup` detects and prompts for them only when the user chooses the Ponos path for dataset creation.

## Global API rules

All DevRev REST API calls must follow these rules:

- **Base URL**: `https://api.devrev.ai`
- **Headers** (every request):
  - `Authorization: Bearer <TOKEN>`
  - `Content-Type: application/json`
  - `Accept: application/json`
- **Token**: read from `.env`. Canonical name is `DEVREV_PAT`. Synonyms: `DEVREV_API_KEY` ≡ `DEVREV_PAT`. Scripts inherited from older repos may expect `DEVREV_TOKEN` — alias it:
  ```bash
  set -a; source .env; set +a
  export DEVREV_TOKEN="$DEVREV_PAT" DEVREV_API_KEY="$DEVREV_PAT"
  ```
- **Method**: prefer POST for non-trivial bodies; GET with query params works for most endpoints.
- **Object references**: always use full DON ids (`don:core:dvrv-us-1:devo/0:ticket/456`), never display IDs like `TKT-456`.
- **Scopes**: check `skills/8-devrev-api/references/00_API_Catalog.md` for every endpoint. Scope ranges like `x:read,x:write,x:all` mean "any one grants access"; a bare `x:all` is required for destructive operations (delete, merge). Work items: the scope tracks the type — `works.create` of a ticket needs `ticket:write`, of an issue `issue:write`. Timeline entries have no separate scope — they inherit from the parent object's read/write scope.
- **Custom field prefixes**: `tnt__` (tenant fragment) and `ctype__` (subtype fragment). A wrong prefix **fails silently** — the server accepts the request but ignores the field.
- **`custom_schema_spec`**: must be sent with any payload that includes custom fields (fragments).
- **Fragment versioning**: fragments are versioned. After any schema change (adding a field, modifying overrides, changing subtypes), **re-save affected records** via their `*.update` endpoint so they pick up the latest fragment version, or use `objects.bulk-upgrade` to upgrade all matching records at once. **Confirmed live 2026-07-18**: `objects.bulk-upgrade` exists ONLY at `/internal/objects.bulk-upgrade` (the public-root path 404s) — `{"type":"<obj_type>"}` returns HTTP 200 `{"id":"<job_don>"}`; poll `jobs.get` for `job_category:"bulk_upgrade"`/`state:"completed"`. This closes a long-open "is it real" question — it is, just internal-only, same pattern as `ai-agents.*`.
- **Custom objects**: start with zero access by default. Grant roles explicitly after creation.
- **Custom link types**: can only be **deprecated, not deleted**. There is no `link-types.custom.delete`. Set `deprecated: true` via `link-types.custom.update`. Write scope is `custom_link_type:write`.
- **`links.replace`**: atomic only for part-to-part default (non-custom) link types. For custom types or non-part objects, it's a non-atomic delete+create sequence; must keep the same type across the replacement.

## Execution flow

1. **Locate endpoint + scope**: start with `skills/8-devrev-api/references/00_API_Catalog.md` to find the endpoint name, HTTP method, and required scope.
2. **Read the domain doc**: open the matching reference file for exact payload format, field constraints, and examples.
3. **Substitute real DON ids**: replace placeholders with actual ids from previous calls or user input.
4. **Run the call**: execute via `curl` or equivalent, with proper headers.
5. **Verify**: immediately follow with the matching `*.get` or `*.list` call to confirm the change landed.
6. **Keep a DON scratchpad**: persist returned ids for dependent calls (e.g., schema id for records, part id for work items, artifact id for attachments).
7. **Ping first** if you need to confirm the token works: `POST https://api.devrev.ai/ping` (scope: none).

## Safety

The following operations are **destructive or irreversible**. State the impact clearly and get explicit user confirmation before running:

- Any `*.delete` (objects, parts, works, accounts, etc.)
- `*.merge` (accounts, works)
- Deprecating objects (custom link types via `deprecated: true`; stages within a diagram via `is_deprecated` on the stage node). **Verified live 2026-07-18**: standalone custom stages and states have **no deprecation and no delete endpoint** — `stages.custom.delete`/`states.custom.delete` return 404, and no top-level `deprecated` variant is accepted on `.update`. Treat every `states.custom.create` and `stages.custom.create` as permanent; manual UI cleanup is the only fix. **Further verified live 2026-07-18**: `is_deprecated: true` on a stage node *inside* a diagram — the mechanism this bullet used to point to as the supported alternative — is ALSO rejected outright at both `stage-diagrams.create` and `.update` (`HTTP 400 bad_request`), on the start stage, a middle stage, and a terminal stage alike. There is currently **no known working mechanism to retire any stage, anywhere in a diagram, via the public API** — every stage added to a diagram is effectively permanent for that diagram's lifetime too.
- Custom-object schema creation via `schemas.custom.set` (**verified live 2026-07-18**): this is a *versioned create*, not an update. Two calls with the same `leaf_type` produce two fragments (`tenant_fragment/N` and `tenant_fragment/N+1`), and there is no `schemas.custom.delete`. Always `schemas.custom.list` first — if a fragment for that `leaf_type` exists, do NOT call `.set` again. Also: `id_prefix` must match `^[A-Z]{2,10}$` and `leaf_type` must be `[a-z_]+` (no digits) or `.set` returns HTTP 400. **Additionally verified 2026-07-18**: if a `tenant_fragment` already exists for that `leaf_type` (i.e. adding to an already-customized stock object), `.set` requires the request's `fields` array to replay the COMPLETE existing field list plus the new field(s) — a partial replay 400s with no diagnostic `field_name`. Always `schemas.custom.get` the current fragment first and replay it in full.
- `objects.bulk-upgrade` — confirmed live at `/internal/objects.bulk-upgrade` (see the Fragment versioning bullet above); affects ALL records of a type org-wide, so confirm before running.
- Workflow deletion (`workflows.delete`) — **confirmed live 2026-07-18**: this genuinely works (`HTTP 200 {}`, and a follow-up `.get` 404s), unlike most `.delete` endpoints elsewhere in this list. Still destructive/irreversible — confirm before running, same as any other delete.
- `works.delete` and `custom-objects.delete` — **confirmed live 2026-07-19**: both genuinely work (`HTTP 200 {}`, then `.get` 404s), same tier as `workflows.delete`/`tags.delete`/`links.delete` above. Don't assume work items or custom-object records are permanent by default — they're deletable, so treat every delete on them as a real, confirm-first destructive action rather than a no-op to skip past.
- `web-crawler-jobs.control` with `stop` or `reset` actions
- Dataset or PaaS/Ponos job deletion (destructive via `/dataset-builder:delete`)
- Workflow deletion (destructive via workflows skill)
- `devrev snap_in_version delete-one` (required before creating a new version — only one non-published version per package — but destroys the deleted version's state)

After any change, **verify with the matching read endpoint** (`*.get`, `*.list`, or `schemas.aggregated.get`). If the change involves custom fields or fragments, re-read an affected record to confirm the fields appear.

**Never commit `.env`** — it's gitignored. Never write a real PAT anywhere except `.env`. If you need to reference a token in documentation or logs, redact it to `<REDACTED_PAT>`.

## Keeping repos current

The `repos/` directory is cloned once on first session and **never updated automatically**. To refresh the cloned repos to their latest default branch, the user must explicitly request it ("update the repos", "pull latest", "sync repos to main"). Then invoke the `update-repos` skill:

```bash
bash .claude/skills/update-repos/update_repos.sh
```

The script clones anything missing, fast-forwards clean repos to their upstream default branch, and **skips** (reports, never discards) any repo with uncommitted local changes.

**After updating `repos/aai-skills`** (the plugin marketplace source): restart Claude Code or run `/plugin marketplace update devrev-aai-plugins` so new commands and skills load.

## Self-learning — MANDATORY, not optional

This repo must improve itself every time it's used. Whenever you hit an **error the references
didn't predict**, a **restriction** (scope/permission/feature-flag/immutability), an **undocumented
endpoint/field/enum/limit**, a **new workflow-import failure cause**, a **plugin/CLI quirk**, or a
**user correction** about DevRev behavior — follow the protocol in
`.claude/skills/capture-learnings/SKILL.md` **immediately, as part of the same task**:

1. **Verify** the fact (real request/response, reproduced behavior, or explicit user statement — never a guess).
2. **Update the SPECIFIC owning file** — the routing table in capture-learnings maps every kind of
   learning to its exact target (a domain SKILL.md "Field notes" section, an API reference doc's
   wrong passage fixed in place, the workflow import-debugging checklist, an operation schema file,
   `api-contracts.md`, the README troubleshooting table, a router trigger phrase…). Updating only
   this CLAUDE.md is wrong unless the learning is a truly global API rule.
3. **Append one permanent row to `docs/LEARNINGS.md`** (append-only — never rewrite or delete an
   old row; rows with no single owning file go in the "Standing notes" section at the top instead)
   and `git commit` the change with a `learn:`-prefixed subject (`learn: <summary>`).

**The commit auto-pushes to `origin/main` — you don't need to push it yourself.** A `PostToolUse`
hook on `Bash` (`.claude/hooks/push-learnings.sh`) fires right after any commit whose subject starts
with `learn:`, runs three guardrails against its diff (no secret-shaped strings; every changed file
inside the known knowledge-base surface — `skills/`, `docs/`, `.claude/`, `plans/`, `CLAUDE.md`,
`README.md`, `rate limits.md`, `documentation/`; `origin/main` hasn't diverged), and pushes only if
all three pass. If a guardrail fails, the commit stays local and the hook says why — fix and commit
again rather than pushing around it. See `.claude/skills/capture-learnings/SKILL.md` for the full
guardrail detail and the (brief, since-reverted) staging/reconciliation model this replaced.

Never edit files under `repos/` (upstream clones) — learnings about their tools go in our skill
files. Never record secrets or real customer DON ids.

## Guardrails

- **Dashboard validation loop**: never bypass the `/create-dashboard` pipeline for new dashboards. That pipeline (generate widgets in parallel → 3-stage validation: structure → semantic → live API, with auto-fix retries → assemble dashboard → deploy via `dashboard-sync` → Playwright verify) is the only supported path to reliably valid output. Never hand-write widget JSON — it skips all validation. This also means: never route to `skills/9-snapin-development`'s plugin's own "Implementation" vertical (`/devrev:plan-implementation` etc.) — it hand-writes widget JSON directly, violating this same rule.
- **AI agent skill default template (agent-skills ONLY — not generic workflows)**: DevRev has two structurally distinct things authored inside skill 6, and this rule applies to *only one* of them:
  - **Generic workflow** — event-driven or manual/API-triggered automation (`ticket_created` → notify, timer → job, etc.). Runs independently, has no calling agent. **No default template here** — pick the closest `working-*.json` in `skills/6-workflows/examples/`.
  - **AI agent skill workflow** — the four-block shape (`ai_agent_skill_trigger` → `ai_agent_skill` block → action(s) → `set_ai_agent_skill_output`, `labels: ["skill"]`) that an AI agent invokes mid-conversation to fetch data or take an action, then gets a structured result back. **This is the case the default template covers.**
  - When (and only when) the ask matches the second shape — phrasings like "create an AI agent skill", "let the agent look up X", "agent-callable skill", "a skill for the agent to call" — **always start from `skills/6-workflows/examples/default-ai-agent-skill-template.json`** rather than hand-authoring the four-block wiring (too many failure modes: missing `block_step_reference_key`, wrong `$get` reference format, missing `labels: ["skill"]`). Customize per `skills/6-workflows/references/ai-agent-skill-pattern.md` § "Default starter".
  - If the phrasing is ambiguous (e.g. bare "workflow" without saying whether an agent invokes it), ASK ONCE which shape the user means before scaffolding.
- **No unattended network installs** beyond the confirmed bootstrap (`pipx` CLI install + `repos/` clone) which the user has pre-approved as part of this workspace model. Don't extend auto-config to other unattended network installs.
- **Never fabricate**: if an API field name, DON id format, scope name, JSON structure, or file path doesn't appear in a reference file or tool result, look it up or stop. Do not reconstruct from memory.
- **Determinism first**: model reasoning produces plans; deterministic scripts, templates, and validators execute them. Same input → same output. Re-runs are safe. Failures are loud (non-zero exit, clear error message).
- **Capture learnings**: reality beats documentation — when they disagree, fix the documentation via the self-learning protocol above, in the same task where you discovered it.
