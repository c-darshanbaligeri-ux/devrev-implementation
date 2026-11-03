# DevRev Workflow Lifecycle API

## Contents
<!-- toc -->
- [Configuration](#configuration)
- [Endpoints](#endpoints)
- [DON ID formats](#don-id-formats)
- [Process: importing a template via the API](#process-importing-a-template-via-the-api)
- [Process: creating a workflow via the API](#process-creating-a-workflow-via-the-api)
- [Process: modifying an existing workflow](#process-modifying-an-existing-workflow)
- [Process: deleting a workflow](#process-deleting-a-workflow)
- [Triggering a workflow](#triggering-a-workflow)
- [Error handling](#error-handling)
<!-- /toc -->

This is the raw API for **managing** workflows as objects — creating the shell, adding/editing/removing steps, publishing, deleting, listing, and triggering. It is a different concern from `template-json-format.md` (which is about the *content* you put inside a workflow) — think of this file as "the CRUD verbs" and that one as "the noun's schema."

The agent cannot manipulate workflows directly through any built-in capability — every action in this reference happens by making an HTTP call to these endpoints. Use whatever HTTP-request capability is available in your session (a `curl` via the shell, an HTTP MCP tool, etc.) — the important part is the request shape below, not which tool sends it.

## Configuration

- **Base URL:** `https://api.devrev.ai`
- **Auth:** the PAT in the `Authorization` header. Two forms are in use and both reach `/internal/` workflow routes: `Authorization: Bearer <PAT>` (what `scripts/trigger_manual_workflow.py` sends, verified live 2026-07) and the bare `Authorization: <PAT>` (what the 2026-11-03 live import test and DevRev's own `workflow-skill` script send). Read the token from the `DEVREV_TOKEN` (or `DEVREV_PAT` — both names show up across this repo's scripts; check which is set) environment variable. Never hardcode a token in a request or in a file you write.

## Endpoints

| Operation | Method | Path | Purpose |
|---|---|---|---|
| `workflows.list` | POST | `/internal/workflows.list` | List existing workflows |
| `workflows.get` | POST | `/internal/workflows.get` | Fetch one workflow (steps, version, status) |
| `workflows.create` | POST | `/internal/workflows.create` | Create a new workflow shell. **Required body field: `title` (not `name`).** Verified 2026-07-18: an empty body returns HTTP 400 `missing_required_field: title`; a body with `name` or `state` returns HTTP 400 `invalid_field`. Minimum valid body: `{"title": "..."}`. |
| `workflows.update` | POST | `/internal/workflows.update` | Update workflow-level metadata. Verified 2026-07-18: accepts `labels` (array — use `["skill"]` to mark an agent-callable skill after building it via raw CRUD, mirroring the template format's top-level `labels`) and `description` (string); both persist and round-trip through `workflows.get`. Rejects `status`/`state` (`HTTP 400 invalid_field`) — status is changed through the separate `workflows.update-status` route below, not here. |
| `workflows.templates.instantiate` | POST | `/internal/workflows.templates.instantiate` | Create a workflow (or a new draft version of one) from a template. Body `{"template_version": "2.0.0", "workflow_template_v2": {…parsed inner template…}}`; add `"workflow": "<workflow DON>"` and `"override_draft": true` to import as a new version of an existing workflow. The result is a **draft**. See "Process: importing a template via the API". Scope `workflow:write`. |
| `workflows.components.validate` | POST | `/internal/workflows.components.validate` | The Workflows app's **Validate** button. Body `{"components":[{"type":"workflow","workflow_version_id":"<version DON>"}]}`. Returns `{"valid": true}`, or `errors` and `warnings` lists. Read-only. |
| `workflows.update-status` | POST | `/internal/workflows.update-status` | The app's **Deploy** for a brand-new (draft) workflow. Body `{"id":"<workflow DON>","status":"active"}` publishes the draft **and switches the workflow on**; `"inactive"` switches it off. |
| `workflow-versions.list` | POST | `/internal/workflow-versions.list` | List a workflow's versions (body `{"workflow":["<workflow DON>"]}`; the 2026-11-03 live test used a GET with `workflow=` as a query parameter). The draft shows `"status": "draft"`. |
| `workflow-steps.list` | GET | `/internal/workflow-steps.list` | List the steps of a version (`workflow_version=<version DON>` as a query parameter in the live test; DevRev's own script POSTs the same field in a body). Use it to find a step's DON before `workflow-steps.update`. |
| `keyrings.list` | POST | `/internal/keyrings.list` | List the org's connections (keyrings) with `{}`. Use a keyring's `id` as `reference` when attaching a connection to a step. |
| `dev-orgs.self` / `dev-users.self` | POST | `/internal/dev-orgs.self`, `/dev-users.self` | Read-only: which org (name) and which user the token acts as. Check these before writing. |
| `workflows.delete` | POST | `/internal/workflows.delete` | Delete a workflow |
| `workflows.trigger` | POST | `/internal/workflows.trigger` | Fire a manual/API-triggered workflow |
| `workflow-versions.get` | GET | `/internal/workflow-versions.get` | Fetch a version's metadata/`triggers` — **live-verified 2026-07-19: does NOT return the inline step graph**, despite the name suggesting it does. To verify step wiring (`next_steps`, `block_step`, etc.) after building via raw CRUD, call `workflow-steps.get` on each step individually and inspect its `next_steps`/`block_step` fields — that's the only way to confirm the graph, not this endpoint. |
| `workflow-versions.publish` | POST | `/internal/workflow-versions.publish` | Publish a draft version live — **live-verified 2026-07-19: rejected while the workflow is in `Workflow_StatusEnumDraft`** (`HTTP 400 bad_request`, `debug_message` states the enum by name); 8 other plausible names (`workflows.deploy`/`.activate`/`.publish`/`.enable`/`.status.update`, `workflow-versions.deploy`/`.activate`/`.set-active`) all 404. **This route is only for a workflow that is already published** (a new version of a live workflow; body `{"id":"<version id>","notes":"…"}`). A brand-new draft workflow is published with `workflows.update-status` (the 2026-07-19 probe never tried that name). |
| `workflow-steps.create` | POST | `/internal/workflow-steps.create` | Add a step to a workflow |
| `workflow-steps.update` | POST | `/internal/workflow-steps.update` | Edit a step's config/connections. To attach a connection (for example a PAT connection on a Code step) send `{"id":"<step DON>","keyrings":[{"name":"<connection name, lowercase, spaces as _>","reference":"<keyring id>"}]}`. |
| `workflow-steps.get` | GET | `/internal/workflow-steps.get` | Fetch a single step |
| `workflow-steps.delete` | POST | `/internal/workflow-steps.delete` | Remove a step |

## DON ID formats

DevRev object names (DONs) for workflow objects follow this pattern:

```
don:integration:dvrv-in-1:devo/21ATptZyZt:workflow/<NUM>
don:integration:dvrv-in-1:devo/21ATptZyZt:workflow/<NUM>:workflow_version/<NUM>.1
don:integration:dvrv-in-1:devo/21ATptZyZt:workflow/<NUM>:workflow_step/<NUM>.<VERSION>.<STEP_NUM>
```

Operation DONs (used when referencing an operation slug, e.g. inside a step's `operation` field at the raw API level rather than the `{namespace, slug}` shorthand used in template JSON) follow:

```
don:integration:dvrv-in-1:operation/devrev.<slug>
```

**Verified 2026-07-18**: the `dvrv-in-1` shard shown above is just this doc's original example org's shard — it is NOT universal. On a `dvrv-us-1` org, an operation DON built with `dvrv-in-1` returns `HTTP 400 id_not_found: object not found`. Always substitute the actual target org's shard (visible in any object's own `id`, e.g. the `workflow.id` just returned by `workflows.create`).

## Process: importing a template via the API

Live-tested 2026-11-03 (user-reported run that created, validated and published a workflow from a template file; the same endpoints and bodies appear in DevRev's own `workflow-skill` `api.py`). This is the API equivalent of Workflows → Import, Validate and Deploy. Replace `devo/<ORG_ID>` with the target org's own id.

1. **Build the body.** The template file stores the inner template as a *string* in `data`; the API wants it as a parsed object:
   ```bash
   jq '{template_version: .templateVersion, workflow_template_v2: (.data | fromjson)}' template.json > body.json
   ```
2. **Instantiate.** `POST /internal/workflows.templates.instantiate` with `-d @body.json`. The response holds the new workflow (for example `don:integration:dvrv-us-1:devo/<ORG_ID>:workflow/35`) in **draft**. To import as a new version of an existing workflow instead, add `"workflow": "<workflow DON>"` and `"override_draft": true`. Note that `override_draft` replaces any draft the workflow already has.
3. **Find the draft version.** `workflow-versions.list` for that workflow returns the version (for example `…:workflow/35:workflow_version/35.1`) with `"status": "draft"`.
4. **Validate.** `POST /internal/workflows.components.validate` with `{"components":[{"type":"workflow","workflow_version_id":"<version DON>"}]}`. `{"valid": true}` means ready; otherwise read the `errors` and `warnings` lists, fix the template and instantiate again.
5. **Publish.**
   - *Brand-new workflow:* `POST /internal/workflows.update-status` with `{"id":"<workflow DON>","status":"active"}`. This publishes the draft **and switches it on**. Then poll `workflows.get` until `status` is `active`.
   - *New version of an already-published workflow:* `POST /internal/workflow-versions.publish` with `{"id":"<version id>","notes":"…"}`. Calling this on a brand-new workflow fails with `400 "is in Draft state and cannot be published"`.
6. **Optional: attach a connection to a Code step** (for example a PAT connection). Get the connection's id from `POST /internal/keyrings.list` with `{}`, the Code step's id from `GET /internal/workflow-steps.list?workflow_version=<version DON>`, then call `workflow-steps.update` as shown in the endpoint table.
7. **Read-only helpers:** `dev-users.self` (who the token is), `internal/dev-orgs.self` (org name), `internal/workflows.list` (find the `workflow-N` id for a new version).

Publishing switches live automation on, so get the user's explicit yes in the session before step 5.

**Scripted version of this process:** `devrev-import-workflow <template.json>` (`./bin/devrev-import-workflow` in a checkout; `--help` lists the flags). It runs `devrev-validate-workflow` first, prints the target org and user, imports the draft, validates it server-side and stops. `--publish` then picks the route from the workflow's live status (a draft gets `workflows.update-status`, an active workflow gets `workflow-versions.publish`) and polls until it is active; `--version-of <workflow>` imports a new version (and refuses to replace an existing draft without `--override-draft`); `--attach-connection "<name>"` does step 6; `--dry-run` prints every request and sends nothing. It was tested against a fake server only, so the first real run should use a throwaway template and stop at the validated draft.

## Process: creating a workflow via the API

This is the "build it step by step through API calls" path — as opposed to authoring a full template JSON and importing it in one shot (see `template-json-format.md` and the main SKILL.md's "Author, don't hand-assemble" step, which is almost always the better choice for anything beyond a trivial 1-2 step workflow).

**Verified live 2026-07-18 — the raw CRUD API uses different field shapes than the template-JSON wrapper format for three things that are easy to get wrong by analogy with `template-json-format.md`:**

| Concept | Template JSON (`template-json-format.md`) | Raw CRUD API (`workflow-steps.create`/`.update`) |
|---|---|---|
| Which operation a step runs | `"operation": {"namespace": "devrev", "slug": "enhancement_updated"}` | `"operation": "don:integration:<shard>:operation/devrev.enhancement_updated"` (a DON **string**; sending the `{namespace,slug}` object returns `HTTP 400 unexpected_json_type`) |
| Connecting one step's output to the next step's input | `"next_steps": [{"port_name": "output", "next_step_reference_key": "if_else_1", "next_port_name": "input"}]` | `"next_steps": [{"port_name": "output", "next_step": "<full step DON>", "next_port_name": "input"}]` (key is `next_step`, not `next_step_reference_key` — the latter, plus `next_step_id`/`step_reference_key`/bare `reference_key`, all return `HTTP 400 invalid_field`) |
| Nesting a step inside an `ai_agent_skill` block | `"block_step_reference_key": "ai_agent_skill_1"` | `"block_step": "<block step's full DON>"` (a DON, not a reference_key string; `block_step_reference_key` returns `HTTP 400 invalid_field` at this layer) |

The operation DON's shard segment must match the **target org's own shard** (e.g. `dvrv-us-1`), not necessarily `dvrv-in-1` — copy it from any existing object's `id` in that org (or from `workflows.create`'s own response) rather than assuming the shard shown in this doc's examples.

1. `workflows.create` — creates the shell. Store the returned `workflow.id` and `workflow_version.id`.
2. `workflow-steps.create` — one call per step you want in the graph. Required fields, in the order the API demands them if missing: `workflow`, `name`, `operation` (DON string, see table above), `reference_key`.
3. `workflow-steps.update` — configure each step's `input_values` and `next_steps` connections (see table above for the correct key names). For `invoke_code` specifically: do **not** send `input_ports`/`output_ports` on `.update` — the operation auto-populates its own default static schema for them; sending them explicitly returns `HTTP 400` (`invalid_field: type` or `dynamic input ports are not supported` depending on shape). Sending only `input_values` + `next_steps` is sufficient and the resulting step already has correct `input_ports`/`output_ports`.
4. Publish. A brand-new workflow is still a draft, so use `workflows.update-status` with `{"id":"<workflow DON>","status":"active"}` (it switches the workflow on). `workflow-versions.publish` is for already-published workflows: on a draft it returns `HTTP 400 bad_request: "workflow ... is in Workflow_StatusEnumDraft state and cannot be published"` (verified live 2026-07-19). The UI's Deploy button does the same job as `update-status`.
5. Corrected 2026-11-03: the earlier note here said no API path leaves the draft state. That came from probing names such as `workflows.deploy`/`.activate`/`.publish` (all `404 route not found`) and from `workflows.update` rejecting `status`/`state`; the route that works is `workflows.update-status`, which that probe never tried. Verify with `workflows.get` until `status` is `active`.

## Process: modifying an existing workflow

1. `workflows.get` — retrieve the current step graph and version.
2. Add steps with `workflow-steps.create`, reconfigure with `workflow-steps.update`, remove with `workflow-steps.delete`.
3. Update connections between steps via each step's `next_steps` field (set through `workflow-steps.update`).
4. Re-publish with `workflow-versions.publish` once satisfied (the workflow is already published, so this route applies). To replace the whole graph from a template instead, use the import process above with `workflow` and `override_draft`.

## Process: deleting a workflow

1. Call `workflows.delete` with the workflow's DON.
2. An empty `{}` response body means the delete succeeded — don't treat it as a missing/error response.

## Triggering a workflow

For workflows built around a manual or API trigger, use `workflows.trigger`. The workflow must already be **published** — triggering a draft returns **`HTTP 400` with `debug_message` containing `"is not active"`** (corrected 2026-07-18; previously documented here as a 404 — see the error table below for the verified live response).

This repo bundles a ready-to-run script for this exact call: `scripts/trigger_manual_workflow.py`. It handles auth (`DEVREV_PAT` env var), payload construction (key=value pairs or raw `--json`), multi-trigger workflows (`--step <ref_key>`), and gives human-readable explanations of the common HTTP status codes. Prefer it over hand-rolling the HTTP call:

```bash
export DEVREV_PAT='eyJhbGc...'
python3 scripts/trigger_manual_workflow.py <workflow-id> Name=John Phone_number=29
python3 scripts/trigger_manual_workflow.py <workflow-id> --json '{"Name":"John"}'
python3 scripts/trigger_manual_workflow.py <workflow-id> --dry-run   # inspect the request without sending it
```

Payload keys are case-sensitive and must match the parameter names on the workflow's trigger step exactly.

## Error handling

| Error | Meaning / response |
|---|---|
| `401` | Token expired — ask the user to refresh authentication (regenerate the PAT in DevRev → Settings → Personal Access Tokens). |
| Invalid field error | Double-check the operation DON, field names, and field types against `operations/schemas/<slug>.md`. |
| `400 "... is in Draft state and cannot be published"` on `workflow-versions.publish` | The workflow is a brand-new draft. Publish it with `workflows.update-status` `{"id":"<workflow DON>","status":"active"}` (or the UI's Deploy); `workflow-versions.publish` is only for workflows that are already published. |
| Empty response `{}` | Not an error — it means the operation (typically delete) completed successfully. |
| `400 bad_request: "... is not active"` on trigger | **Corrected 2026-07-18** (previously documented as a `404`): triggering a still-draft workflow returns `HTTP 400`, with `debug_message` containing `"is not active"` — not a 404. Confirm the workflow ID and that it's actually published, not just saved as a draft; the workflow's own `.get` response `status` field will say `draft`. |
| `404` / `500` on trigger for an unknown or deleted workflow ID | Observed inconsistently in one live test: a syntactically-valid but nonexistent workflow ID returned `HTTP 500 internal_error` rather than a clean `404` when passed to `workflows.trigger`. Treat any 4xx/5xx on trigger as "check the ID and status," not as a reliable signal of which specifically is wrong. |
| `429` | Rate limited — slow down and retry. |

Always report workflow IDs, HTTP status, and the raw API response back to the user clearly — don't paraphrase away the DON strings, since the user will need them for follow-up calls.
