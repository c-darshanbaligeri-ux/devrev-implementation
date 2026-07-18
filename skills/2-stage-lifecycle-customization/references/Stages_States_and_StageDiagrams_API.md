# Stages, states, and stage diagrams — DevRev API

How to customize an object's lifecycle programmatically: states (broad
categories), stages (steps within a state), and stage diagrams (allowed
transitions). Applies to issue, ticket, custom objects, and any leaf type.

| Field | Detail |
| --- | --- |
| Base URL | https://api.devrev.ai |
| Auth | `Authorization: Bearer <TOKEN>` (PAT or Service Account Token) |
| Status | Beta |

---

## 1. Concepts

- State — a broad category that groups stages. DevRev ships three by default:
  `open`, `in_progress`, `closed`. A state can be referenced by any object type.
- Stage — a specific step in the lifecycle (e.g. "In Review", "Needs RCA").
  Every stage must belong to a state.
- Stage diagram — defines the allowed transitions between stages for a leaf type
  or subtype (e.g. Backlog -> In development is allowed; the reverse is not).
- Ordering matters: **create states first, then stages, then the stage diagram**,
  because each stage needs a valid `state` (state ID) at creation time.
- A stage is not bound to one object type — both issue and ticket can reference
  the same `in_development` stage.

---

## 2. Custom states

### Create — `states.custom.create` (scope: `custom_state:write`)

```bash
curl -X POST 'https://api.devrev.ai/states.custom.create' \
-H 'Authorization: Bearer <TOKEN>' \
-H 'Content-Type: application/json' \
-d '{
  "name": "New State",
  "ordinal": 1001
}'
```

- `ordinal` must be unique within the dev org and controls ordering.
- Save the returned state DON id (e.g. `don:core:...:custom_state/13`).

### Update — `states.custom.update`

```bash
curl -X POST 'https://api.devrev.ai/states.custom.update' \
-H 'Authorization: Bearer <TOKEN>' \
-d '{
  "id": "don:core:dvrv-us-1:devo/xxx:custom_state/13",
  "name": "New State Name",
  "ordinal": 1003
}'
```

### Read
- `states.custom.get` — fetch one state.
- `states.custom.list` — list states (no scope required).

---

## 3. Custom stages

### Create — `stages.custom.create` (scope: `custom_stage:write`)

```bash
curl -X POST 'https://api.devrev.ai/stages.custom.create' \
-H 'Authorization: Bearer <TOKEN>' \
-H 'Content-Type: application/json' \
-d '{
  "name": "Needs RCA",
  "state": "closed",
  "ordinal": 1000
}'
```

- Required fields: `name`, `ordinal` (ordering), `state` (a state ID — a default
  state name like `closed` or a custom state DON).
- Optional: `marketplace_ref` (reference to an imported marketplace item).
- Save each returned stage DON id — the stage diagram needs them.

### Update — `stages.custom.update`

```bash
curl -X POST 'https://api.devrev.ai/stages.custom.update' \
-H 'Authorization: Bearer <TOKEN>' \
-d '{
  "id": "don:core:dvrv-us-1:devo/xxx:custom_stage/8",
  "name": "In Review",
  "ordinal": 1005,
  "state_id": "don:core:dvrv-us-1:devo/xxx:custom_state/13"
}'
```

### Read
- `stages.custom.get` — fetch one stage.
- `stages.custom.list` — list stages (no scope required).

---

## 4. Stage diagrams

A stage diagram wires stages together into a workflow: a start stage, allowed
transitions, and terminal stages.

### Create — `stage-diagrams.create` (scope: `stage_diagram:write`)

Required: `leaf_type` (e.g. `issue`, `ticket`, or a custom leaf type), `name`,
and a `stages` array. Optional: `is_custom_leaf_type`, `is_default`.

```bash
curl -X POST 'https://api.devrev.ai/stage-diagrams.create' \
-H 'Authorization: Bearer <TOKEN>' \
-H 'Content-Type: application/json' \
-d '{
  "leaf_type": "issue",
  "name": "RCA Workflow",
  "stages": [
    {
      "is_start": true,
      "stage_id": "don:core:dvrv-us-1:devo/xxx:custom_stage/1",
      "transitions": [
        { "target_stage_id": "don:core:dvrv-us-1:devo/xxx:custom_stage/8" }
      ]
    },
    {
      "stage_id": "don:core:dvrv-us-1:devo/xxx:custom_stage/8",
      "transitions": [
        { "target_stage_id": "don:core:dvrv-us-1:devo/xxx:custom_stage/1" },
        { "target_stage_id": "don:core:dvrv-us-1:devo/xxx:custom_stage/9" }
      ]
    },
    {
      "stage_id": "don:core:dvrv-us-1:devo/xxx:custom_stage/9",
      "transitions": [
        { "target_stage_id": "don:core:dvrv-us-1:devo/xxx:custom_stage/1" }
      ]
    }
  ]
}'
```

- Each stage node: `stage_id` (required), `is_start` (marks the entry stage),
  `transitions` (list of allowed `target_stage_id`).
- A stage with no outgoing transitions is effectively terminal (e.g. Resolved).
- **Live-verified 2026-07-18: `is_deprecated: true` on a stage node is REJECTED** at both
  create and update time (`HTTP 400 {"type":"bad_request"}`), tried on the start stage, a
  middle stage, and a terminal stage, and on a brand-new diagram never touched by `.update`.
  The identical payload with `is_deprecated` omitted succeeds; `is_deprecated: false` is
  accepted as a no-op. There is currently **no known working mechanism** to retire a stage
  inside a diagram via the public API — treat every stage added to a diagram as permanent.

### Update — `stage-diagrams.update`

Update transitions or rename. Note: `is_default` and
`leaf_type` cannot be changed after creation (live-verified: both return
`{"message":"Bad Request","type":"invalid_field"}` if included in the update body).
Stage deprecation via `is_deprecated` does **not** work — see the verified note above.

### Read
- `stage-diagrams.get` — fetch one diagram.
- `stage-diagrams.list` — list diagrams; filter by `leaf_type`, `name`, or
  `is_custom_leaf_type` (no scope required). **Live-verified 2026-07-18**: for a
  custom leaf type, `leaf_type=<custom_leaf_type>` alone returns `{"result":[]}` —
  you must also pass `is_custom_leaf_type=true` in the same query to get matches.
  `name` filters correctly on its own (exact match; no match returns `[]`).

---

## 5. Assigning a stage diagram to a subtype

**Live-verified 2026-07-18 — this section is UNCONFIRMED / likely wrong; do not rely on it
without re-checking the live API first.** The mechanism below is what older material and this
doc previously described, but every write path tried this session was rejected:
- `schemas.custom.set` with `stage_diagram_id` (also tried `stage_diagram`, `diagram_id`,
  `stagediagram_id`, `stage_diagram_ref`, `lifecycle_id`, `workflow_diagram_id`, and a nested
  `{"stage_diagram":{"id":"..."}}`) → always `{"message":"Bad Request","type":"invalid_field","field_name":"stage_diagram_id"}` (or the tried field name). Tried on both a `tenant_fragment`
  (custom leaf type) and a `custom_type_fragment` (subtype of `issue`).
- `stage-diagrams.create` with a top-level `subtype` field → `{"message":"Bad Request","type":"invalid_field","field_name":"subtype"}`. Diagrams appear to be `leaf_type`-scoped only.
- `schemas.subtypes.prepare-update` with `subtype` or `stage_diagram_id` in the body → both
  rejected as `invalid_field`; it only accepts `leaf_type` and returns
  `{"added_fields":[...]}` (fields a bulk-upgrade would add), so it's a preview/dry-run tool,
  not the attachment mechanism.
- Counter-evidence the field exists somewhere in the data model: `schemas.aggregated.get`
  returns a **read-only** `stage_diagram_id` key for stock leaf types that already have a
  diagram, e.g. `ticket` → `"stage_diagram_id":{"id":"don:core:...:stage_diagram/6","name":"ticket_transitions"}`. So the association exists server-side — only the public
  write path to set it on a subtype/custom leaf type remains unconfirmed.
  **Also note (live-verified 2026-07-18, corrected same day):** `schemas.aggregated.get` works fine
  via POST — the specific shape `{"leaf_type":"ticket","custom_schema_spec":{"tenant_fragment":true}}`
  (the example this skill and skill 1 previously documented) returns
  `{"message":"Bad Request","type":"invalid_field","field_name":"tenant_fragment"}`, but that's
  because tenant/custom fields are included by default — omitting `custom_schema_spec` entirely
  (`POST` with just `{"leaf_type":"ticket"}`, or the equivalent `GET schemas.aggregated.get?leaf_type=<type>`,
  add `&is_custom_leaf_type=true` for custom leaf types) returns `HTTP 200` with the full merged set.
  `custom_schema_spec: {"subtype": "<name>"}` (no `tenant_fragment` key) also works via POST when you
  need a specific subtype's fields. Response wrapper is `{"schema": {...}}`.

By default a bug subtype inherits transitions from its parent type (Issue); once
you assign a dedicated diagram, publish the change to activate it — **write path unconfirmed,
see above.**

---

## 6. Dependent-field conditions on stages

You can enforce rules tied to a stage — for example, require an RCA field when a
bug reaches a specific stage. Add `conditions` to the subtype fragment:

```json
"conditions": [{
  "expression": "stage == 'don:core:dvrv-us-1:devo/0:stage/5'",
  "effects": [{ "fields": [ "custom_fields.rca" ], "require": true }]
}]
```

Effects can `require`, `show`, or constrain `allowed_values` for fields.

---

## 7. Quick reference

| Endpoint | Scope | Purpose |
| --- | --- | --- |
| `states.custom.create` | `custom_state:write` | Create a state |
| `states.custom.update` | `custom_state:write` | Update a state |
| `states.custom.get` / `.list` | none | Read states |
| `stages.custom.create` | `custom_stage:write` | Create a stage |
| `stages.custom.update` | `custom_stage:write` | Update a stage |
| `stages.custom.get` / `.list` | none | Read stages |
| `stage-diagrams.create` | `stage_diagram:write` | Create a diagram |
| `stage-diagrams.update` | `stage_diagram:write` | Update a diagram |
| `stage-diagrams.get` / `.list` | none | Read diagrams |

---

## 8. Common pitfalls

- Creating a stage before its state exists — fails, because `state` must resolve.
- Duplicate `ordinal` for states — must be unique within the dev org.
- Forgetting to assign the diagram to the subtype — stages exist but the object
  still uses the inherited/default lifecycle until the subtype references the
  `stage_diagram_id` and the change is published. **Live-verified 2026-07-18: the
  write path for this is itself unconfirmed** — see §5 for every field-name
  variant tried and rejected.
- Deleting a stage that's referenced by a diagram — there's no delete endpoint
  anyway. `is_deprecated` was intended as the retirement path but **is rejected
  live** (`HTTP 400 bad_request` on both create and update, live-verified
  2026-07-18 — see §4). Treat every stage added to a diagram as permanent.
