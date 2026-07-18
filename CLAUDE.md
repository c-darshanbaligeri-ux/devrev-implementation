# DevRev Implementation Operating Environment

## Identity

This is the unified operating environment for all DevRev implementation work apart from snap-in development. It is not a buildable software project — it's a workspace containing skills + references + cloned toolchains (`repos/`) + a hosted DevRev MCP. Everything needed to design a solution, customize DevRev organizations, upload data, build dashboards, create datasets, author workflows, and develop AI agents lives here in a plug-and-play configuration, spanning design (skill 0) through build (skills 1–8).

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
| "Update the repos" / "pull latest" / "sync repos to main" / "refresh the cloned repos" (explicit request only — never automatically) | `.claude/skills/update-repos` |

**Rule**: open the matched SKILL.md file and follow its playbook. Do not reconstruct API endpoint formats, payload structures, scope names, or JSON schemas from training data — every API fact must come from the skill's reference files.

## Plug and play

This repo requires **one manual step** to activate: create `.env` from `.env.example` and populate `DEVREV_PAT` + `DEVREV_ENDPOINT`. Once `.env` exists, a `SessionStart` hook (`.claude/hooks/bootstrap-workspace.sh`) auto-configures the environment on session start:

1. **Workspace directories**: creates `dashboards/`, `datasets/`, `plans/`, `logs/`, `templates/` synchronously.
2. **Toolchain repos clone** (background, once): if `repos/aai-skills/.git` doesn't exist, loops over non-comment lines in `repos.txt` and clones each to `repos/<name>`. Clone status logs to `.claude/.auto-setup/install.log` and appends a result table to `docs/CLONE_RESULTS.md`.
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
- **Fragment versioning**: fragments are versioned. After any schema change (adding a field, modifying overrides, changing subtypes), **re-save affected records** via their `*.update` endpoint so they pick up the latest fragment version. (`objects.bulk-upgrade` is mentioned in older material but is NOT in the public API catalog — verify its availability before use.)
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
- Deprecating objects (custom link types via `deprecated: true`; stages within a diagram via `is_deprecated` on the stage node — the references document no whole-diagram or state deprecation)
- `objects.bulk-upgrade` (if available — verify scope first; affects all records of a type)
- `web-crawler-jobs.control` with `stop` or `reset` actions
- Dataset or PaaS/Ponos job deletion (destructive via `/dataset-builder:delete`)
- Workflow deletion (destructive via workflows skill)

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
3. **Append one row to `docs/LEARNINGS.md`** (the append-only journal) and `git commit` the change
   (`learn: <summary>`).

Never edit files under `repos/` (upstream clones) — learnings about their tools go in our skill
files. Never record secrets or real customer DON ids.

## Guardrails

- **Dashboard validation loop**: never bypass the `/create-dashboard` pipeline for new dashboards. That pipeline (generate widgets in parallel → 3-stage validation: structure → semantic → live API, with auto-fix retries → assemble dashboard → deploy via `dashboard-sync` → Playwright verify) is the only supported path to reliably valid output. Never hand-write widget JSON — it skips all validation.
- **No unattended network installs** beyond the confirmed bootstrap (`pipx` CLI install + `repos/` clone) which the user has pre-approved as part of this workspace model. Don't extend auto-config to other unattended network installs.
- **Never fabricate**: if an API field name, DON id format, scope name, JSON structure, or file path doesn't appear in a reference file or tool result, look it up or stop. Do not reconstruct from memory.
- **Determinism first**: model reasoning produces plans; deterministic scripts, templates, and validators execute them. Same input → same output. Re-runs are safe. Failures are loud (non-zero exit, clear error message).
- **Capture learnings**: reality beats documentation — when they disagree, fix the documentation via the self-learning protocol above, in the same task where you discovered it.
