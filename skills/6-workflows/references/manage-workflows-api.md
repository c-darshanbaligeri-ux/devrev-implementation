# DevRev Workflow Lifecycle API

This is the raw API for **managing** workflows as objects — creating the shell, adding/editing/removing steps, publishing, deleting, listing, and triggering. It is a different concern from `template-json-format.md` (which is about the *content* you put inside a workflow) — think of this file as "the CRUD verbs" and that one as "the noun's schema."

The agent cannot manipulate workflows directly through any built-in capability — every action in this reference happens by making an HTTP call to these endpoints. Use whatever HTTP-request capability is available in your session (a `curl` via the shell, an HTTP MCP tool, etc.) — the important part is the request shape below, not which tool sends it.

## Configuration

- **Base URL:** `https://api.devrev.ai`
- **Auth:** Bearer token in the `Authorization` header. Read it from the `DEVREV_TOKEN` (or `DEVREV_PAT` — both names show up across this repo's scripts; check which is set) environment variable. Never hardcode a token in a request or in a file you write.

## Endpoints

| Operation | Method | Path | Purpose |
|---|---|---|---|
| `workflows.list` | POST | `/internal/workflows.list` | List existing workflows |
| `workflows.get` | POST | `/internal/workflows.get` | Fetch one workflow (steps, version, status) |
| `workflows.create` | POST | `/internal/workflows.create` | Create a new workflow shell. **Required body field: `title` (not `name`).** Verified 2026-07-18: an empty body returns HTTP 400 `missing_required_field: title`; a body with `name` or `state` returns HTTP 400 `invalid_field`. Minimum valid body: `{"title": "..."}`. |
| `workflows.update` | POST | `/internal/workflows.update` | Update workflow-level metadata. Verified 2026-07-18: accepts `labels` (array — use `["skill"]` to mark an agent-callable skill after building it via raw CRUD, mirroring the template format's top-level `labels`) and `description` (string); both persist and round-trip through `workflows.get`. Rejects `status`/`state` (`HTTP 400 invalid_field`) — there is no API-level way to move a workflow out of draft. |
| `workflows.delete` | POST | `/internal/workflows.delete` | Delete a workflow |
| `workflows.trigger` | POST | `/internal/workflows.trigger` | Fire a manual/API-triggered workflow |
| `workflow-versions.get` | GET | `/internal/workflow-versions.get` | Fetch a specific version's step graph |
| `workflow-versions.publish` | POST | `/internal/workflow-versions.publish` | Publish a draft version live |
| `workflow-steps.create` | POST | `/internal/workflow-steps.create` | Add a step to a workflow |
| `workflow-steps.update` | POST | `/internal/workflow-steps.update` | Edit a step's config/connections |
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
4. `workflow-versions.publish` — publish the version so it goes live.
5. If publish fails because the workflow is still in draft state, tell the user to click **Deploy** in the DevRev Workflows UI (`https://app.devrev.ai/?view=workflows`) — publishing a draft-state workflow isn't reachable purely through the API. Verified live: `workflow-versions.publish` returns `HTTP 400 bad_request: "workflow ... is in Workflow_StatusEnumDraft state and cannot be published"`; there is no `workflows.deploy`/`workflows.activate`/`workflow-versions.deploy`/`workflows.publish` endpoint (all `404 route not found`), and `workflows.update` rejects both `status` and `state` as top-level fields (`HTTP 400 invalid_field`) — so there is genuinely no API path around the UI Deploy step.

## Process: modifying an existing workflow

1. `workflows.get` — retrieve the current step graph and version.
2. Add steps with `workflow-steps.create`, reconfigure with `workflow-steps.update`, remove with `workflow-steps.delete`.
3. Update connections between steps via each step's `next_steps` field (set through `workflow-steps.update`).
4. Re-publish with `workflow-versions.publish` once satisfied.

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
| Draft publish error | The workflow must be deployed from the DevRev UI before it can be published via the API. |
| Empty response `{}` | Not an error — it means the operation (typically delete) completed successfully. |
| `400 bad_request: "... is not active"` on trigger | **Corrected 2026-07-18** (previously documented as a `404`): triggering a still-draft workflow returns `HTTP 400`, with `debug_message` containing `"is not active"` — not a 404. Confirm the workflow ID and that it's actually published, not just saved as a draft; the workflow's own `.get` response `status` field will say `draft`. |
| `404` / `500` on trigger for an unknown or deleted workflow ID | Observed inconsistently in one live test: a syntactically-valid but nonexistent workflow ID returned `HTTP 500 internal_error` rather than a clean `404` when passed to `workflows.trigger`. Treat any 4xx/5xx on trigger as "check the ID and status," not as a reliable signal of which specifically is wrong. |
| `429` | Rate limited — slow down and retry. |

Always report workflow IDs, HTTP status, and the raw API response back to the user clearly — don't paraphrase away the DON strings, since the user will need them for follow-up calls.
