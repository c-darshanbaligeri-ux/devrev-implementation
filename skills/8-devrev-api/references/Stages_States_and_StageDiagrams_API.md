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

**Live-verified 2026-07-19 — CONFIRMED working, via two distinct mechanisms.** This corrects the
2026-07-18 finding below the fold, which ruled out `stage_diagram_id` and a **nested**
`{"stage_diagram":{"id":...}}` object, but never tried `stage_diagram` as a **bare string** — that
turned out to be the actual working field name.

**Mechanism A — leaf-type-level default diagram**, via `is_default: true` at `stage-diagrams.create`
time. Works only while the leaf type has no existing default diagram — a second `is_default: true`
create for the same leaf type returns `HTTP 409 conflict`. `is_default` is immutable after creation
(cannot be added retroactively via `.update`), so this is a one-shot, create-time-only path.

**Mechanism B — subtype-level diagram**, via `stage_diagram` (bare DON-id string) on
`schemas.custom.set`:

```bash
curl -X POST 'https://api.devrev.ai/schemas.custom.set' \
-H 'Authorization: Bearer <TOKEN>' \
-d '{
  "type": "custom_type_fragment",
  "leaf_type": "issue",
  "subtype": "bug",
  "description": "Bug subtype",
  "stage_diagram": "don:core:dvrv-us-1:devo/xxx:stage_diagram/12",
  "fields": [...]
}'
```

Verified: `schemas.custom.get` on the resulting fragment shows `"stage_diagram":{"id":"...stage_diagram/12","name":"..."}` persisted, and `schemas.aggregated.get` with
`custom_schema_spec:{"subtype":"bug"}` shows `stage_diagram_id` populated for that subtype. If the
subtype fragment already exists, the full-field-replay rule (§4a) applies — replay every existing
field, don't send a partial list.

For a custom object leaf type (not a subtype), use Mechanism A, or Mechanism B's shape with
`"type": "tenant_fragment"` and `"is_custom_leaf_type": true` in place of `subtype`.

**Enforcement differs by object class — read before promising this gates anything.** On **custom
objects**, `custom-objects.update` genuinely enforces the diagram: setting `stage` to a non-member
or non-adjacent stage returns `HTTP 400 bad_request`; valid transitions return `200`. On **stock-type
subtypes**, `works.update` showed **no enforcement** in testing — after attaching a diagram that only
allowed `triage → completed` on an `issue`/`bug` subtype record, `works.update` still accepted
`stage` values from entirely unrelated lifecycles (an opportunity-only stage, an incident-only
stage) with `HTTP 200`, changing the stage every time. The only rejection producible was a
syntactically invalid stage DON. Treat subtype-level diagram attachment as real/persisted (visible
in `schemas.aggregated.get`) but **not confirmed to gate `works.update`** — don't tell a caller it
will reject invalid stage transitions on a stock leaf type's subtype.

By default a bug subtype inherits transitions from its parent type (Issue); once you assign a
dedicated diagram via Mechanism B, it takes effect immediately — no separate publish step was
needed in testing.

<details>
<summary>2026-07-18 finding this section corrects (kept for audit trail)</summary>

Every write path tried in the 2026-07-18 session was rejected:
- `schemas.custom.set` with `stage_diagram_id` (also `diagram_id`, `stagediagram_id`,
  `stage_diagram_ref`, `lifecycle_id`, `workflow_diagram_id`, and a **nested**
  `{"stage_diagram":{"id":"..."}}`) → always `invalid_field`. `stage_diagram` as a bare string was
  never tried — that gap is the actual root cause of this now-superseded finding.
- `stage-diagrams.create` with a top-level `subtype` field → `invalid_field field_name:"subtype"`.
  Diagrams remain `leaf_type`-scoped only; subtype-scoping happens via the fragment, not the
  diagram itself.
- `schemas.subtypes.prepare-update` with `subtype`/`stage_diagram_id` → `invalid_field`; it only
  accepts `leaf_type` and previews a bulk-upgrade (`{"added_fields":[...]}`), not an attachment tool.
</details>

**Separately, live-verified 2026-07-18, still accurate:** `schemas.aggregated.get` via POST works
fine in general — the specific shape `{"leaf_type":"ticket","custom_schema_spec":{"tenant_fragment":true}}`
returns `invalid_field field_name:"tenant_fragment"` because tenant/custom fields are included by
default. Omitting `custom_schema_spec` entirely (`POST {"leaf_type":"ticket"}`, or the equivalent
`GET schemas.aggregated.get?leaf_type=<type>`, add `&is_custom_leaf_type=true` for custom leaf
types) returns `HTTP 200` with the full merged set. `custom_schema_spec: {"subtype": "<name>"}` (no
`tenant_fragment` key) also works via POST. Response wrapper is `{"schema": {...}}`. Note: a bare
`GET ?leaf_type=<custom_leaf_type>` **without** `&is_custom_leaf_type=true` returns `HTTP 200` with
a silently **empty** schema rather than an error — easy to mistake for "no custom fields exist."

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

**Live-verified 2026-07-19 nuance**: the requirement is enforced only when the conditioned field is
**explicitly included** in an update payload, not as a standing invariant checked on every write or
re-checked on stage entry. A record can sit indefinitely in the stage named by the condition with the
field empty, as long as no update ever tries to explicitly clear that field again; moving the record
into the stage while the field is already empty succeeds, and updating unrelated fields while parked
in that stage also succeeds without re-validating the conditioned field.

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
  diagram via `stage_diagram` (bare DON string) or `is_default: true` — see §5 for
  both confirmed-working mechanisms and the enforcement caveat (custom objects
  enforce transitions on `custom-objects.update`; stock-type subtypes did not on
  `works.update` in testing).
- Deleting a stage that's referenced by a diagram — there's no delete endpoint
  anyway. `is_deprecated` was intended as the retirement path but **is rejected
  live** (`HTTP 400 bad_request` on both create and update, live-verified
  2026-07-18 — see §4). Treat every stage added to a diagram as permanent.
