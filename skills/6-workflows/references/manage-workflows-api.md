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
| `workflows.update` | POST | `/internal/workflows.update` | Update workflow-level metadata |
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

## Process: creating a workflow via the API

This is the "build it step by step through API calls" path — as opposed to authoring a full template JSON and importing it in one shot (see `template-json-format.md` and the main SKILL.md's "Author, don't hand-assemble" step, which is almost always the better choice for anything beyond a trivial 1-2 step workflow).

1. `workflows.create` — creates the shell. Store the returned `workflow.id` and `workflow_version.id`.
2. `workflow-steps.create` — one call per step you want in the graph.
3. `workflow-steps.update` — configure each step's `input_values` and `next_steps` connections.
4. `workflow-versions.publish` — publish the version so it goes live.
5. If publish fails because the workflow is still in draft state, tell the user to click **Deploy** in the DevRev Workflows UI (`https://app.devrev.ai/?view=workflows`) — publishing a draft-state workflow isn't reachable purely through the API.

## Process: modifying an existing workflow

1. `workflows.get` — retrieve the current step graph and version.
2. Add steps with `workflow-steps.create`, reconfigure with `workflow-steps.update`, remove with `workflow-steps.delete`.
3. Update connections between steps via each step's `next_steps` field (set through `workflow-steps.update`).
4. Re-publish with `workflow-versions.publish` once satisfied.

## Process: deleting a workflow

1. Call `workflows.delete` with the workflow's DON.
2. An empty `{}` response body means the delete succeeded — don't treat it as a missing/error response.

## Triggering a workflow

For workflows built around a manual or API trigger, use `workflows.trigger`. The workflow must already be **published** — triggering a draft returns 404.

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
| `404` on trigger | Confirm the workflow ID and that it's actually published, not just saved as a draft. |
| `429` | Rate limited — slow down and retry. |

Always report workflow IDs, HTTP status, and the raw API response back to the user clearly — don't paraphrase away the DON strings, since the user will need them for follow-up calls.
