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
  `transitions` (list of allowed `target_stage_id`), and `is_deprecated` to
  retire a stage without breaking the diagram.
- A stage with no outgoing transitions is effectively terminal (e.g. Resolved).

### Update — `stage-diagrams.update`

Update transitions, deprecate stages, or rename. Note: `is_default` and
`leaf_type` cannot be changed after creation.

### Read
- `stage-diagrams.get` — fetch one diagram.
- `stage-diagrams.list` — list diagrams; filter by `leaf_type`, `name`, or
  `is_custom_leaf_type` (no scope required).

---

## 5. Assigning a stage diagram to a subtype

A stage diagram is applied to a subtype through the subtype's schema fragment.
When you define or update the subtype with `schemas.custom.set`, reference the
stage diagram via `stage_diagram_id`. This lets different subtypes of the same
object (e.g. a Bug vs. a Feature Request issue) follow different lifecycles.

By default a bug subtype inherits transitions from its parent type (Issue); once
you assign a dedicated diagram, publish the change to activate it.

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
  `stage_diagram_id` and the change is published.
- Deleting a stage that's referenced by a diagram — deprecate it (`is_deprecated`)
  instead so existing records aren't orphaned.
