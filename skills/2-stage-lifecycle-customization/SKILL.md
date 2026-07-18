---
name: stage-lifecycle-customization
description: "Customize object lifecycles in DevRev — create custom states (broad categories like open/in_progress/closed), define custom stages (specific steps like \"In Review\" or \"Needs RCA\"), build stage diagrams (allowed transitions), and assign lifecycles to object types or subtypes. Use when you need to model a custom workflow: ticket stages, issue states, custom object lifecycles, or any object's stage-based flow. Covers states.custom.*, stages.custom.*, and stage-diagrams.* endpoints."
---

# Stage & lifecycle customization — executable playbook

Customize the lifecycle of DevRev objects programmatically: define states (broad categories), stages (specific steps within a state), and stage diagrams (allowed transitions). Applies to issue, ticket, custom objects, and any leaf type. Read the repo root `CLAUDE.md` first for global API rules; use this skill for any stage/state/lifecycle customization request.

## When to use

Trigger when the user wants to:
- Customize stages for tickets or issues
- Add a state or stage to an object's lifecycle
- Define a stage diagram (workflow) with allowed transitions
- Model a custom workflow or ticket flow
- Assign a lifecycle to a subtype or custom object
- Add dependent-field conditions tied to stages (e.g. require RCA when a bug reaches a specific stage)

## When not to use

- Object schema customization (fields, subtypes, custom objects) → `skills/1-object-schema-customization`
- File uploads or data migration or building a fresh org → `skills/3-data-upload-and-org-build`
- Raw API calls with no lifecycle changes → `skills/8-devrev-api`

## Preconditions

1. Token in `.env` (`DEVREV_PAT`). If missing, tell the user exactly what to put in it and stop — never fabricate a token.
2. Verify token works: `POST https://api.devrev.ai/ping` before starting.
3. Required scopes (from `references/Stages_States_and_StageDiagrams_API.md` §7):
   - `custom_state:write` for `states.custom.create` / `.update`
   - `custom_stage:write` for `stages.custom.create` / `.update`
   - `stage_diagram:write` for `stage-diagrams.create` / `.update`
   - No scope needed for `*.get` / `*.list` calls
4. Parent objects must exist: if assigning a stage diagram to a subtype, the subtype's schema fragment must exist (see `skills/1-object-schema-customization`). If referencing a part or other object, have its DON id ready.

## Playbook

**Reference**: `references/Stages_States_and_StageDiagrams_API.md` (entire file).

**Ordering matters** (§1): create states first, then stages (each stage needs a valid `state` at creation), then the stage diagram (which references stage DON ids), then optionally assign the diagram to a subtype/leaf type via its schema fragment.

### Step 1 — Create custom states

**Reference**: §2 (Custom states).

A state is a broad category that groups stages (e.g. `open`, `in_progress`, `closed`). DevRev ships three by default; create more if needed. A state can be referenced by any object type.

```bash
curl -X POST 'https://api.devrev.ai/states.custom.create' \
-H 'Authorization: Bearer $DEVREV_TOKEN' \
-H 'Content-Type: application/json' \
-d '{
  "name": "New State",
  "ordinal": 1001
}'
```

- `ordinal` must be **unique within the dev org** and controls ordering.
- Save the returned state DON id (e.g. `don:core:...:custom_state/13`) in your scratchpad.
- **Verify**: `states.custom.list` (no scope required) to see all states.

### Step 2 — Create custom stages

**Reference**: §3 (Custom stages).

A stage is a specific step in the lifecycle (e.g. "Needs RCA", "In Review"). Every stage must belong to a state.

```bash
curl -X POST 'https://api.devrev.ai/stages.custom.create' \
-H 'Authorization: Bearer $DEVREV_TOKEN' \
-H 'Content-Type: application/json' \
-d '{
  "name": "Needs RCA",
  "state": "closed",
  "ordinal": 1000
}'
```

- **Required fields**: `name`, `ordinal` (ordering), `state` (a state ID — either a default state name like `closed` or a custom state DON from Step 1).
- A stage is not bound to one object type — both issue and ticket can reference the same stage.
- Save each returned stage DON id — the stage diagram needs them in Step 3.
- **Verify**: `stages.custom.list` (no scope required) to see all stages.

**Important**: `ordinal` for stages controls ordering within the list. The reference (§7) documents the uniqueness requirement only for **states** (unique within the dev org); keep stage ordinals unique anyway for predictable ordering.

### Step 3 — Create a stage diagram

**Reference**: §4 (Stage diagrams).

A stage diagram wires stages together into a workflow: a start stage, allowed transitions, and terminal stages.

```bash
curl -X POST 'https://api.devrev.ai/stage-diagrams.create' \
-H 'Authorization: Bearer $DEVREV_TOKEN' \
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
      "transitions": []
    }
  ]
}'
```

- **Required**: `leaf_type` (e.g. `issue`, `ticket`, or a custom leaf type), `name`, and a `stages` array.
- **Optional**: `is_custom_leaf_type: true` if applying to a custom object; `is_default: true` to make this the default diagram for the leaf type.
- Each stage node: `stage_id` (required), `is_start` (marks the entry stage — exactly one stage must have this), `transitions` (array of allowed `target_stage_id`), and optionally `is_deprecated` to retire a stage without breaking the diagram.
- A stage with no outgoing transitions is effectively terminal (e.g. Resolved).
- Save the returned `STAGE_DIAGRAM_ID` in your scratchpad.
- **Verify**: `stage-diagrams.list` filtered by `leaf_type` or `name` (no scope required).

**Important** (§4): `is_default` and `leaf_type` **cannot be changed after creation**. Choose them carefully.

### Step 4 — Assign the stage diagram to a subtype or leaf type

**Reference**: §5 (Assigning a stage diagram to a subtype).

A stage diagram is applied to a subtype through the subtype's schema fragment. When you define or update the subtype with `schemas.custom.set`, reference the stage diagram via `stage_diagram_id`. This lets different subtypes of the same object (e.g. Bug vs. Feature Request) follow different lifecycles.

```bash
curl -X POST 'https://api.devrev.ai/schemas.custom.set' \
-H 'Authorization: Bearer $DEVREV_TOKEN' \
-d '{
  "type": "custom_type_fragment",
  "leaf_type": "issue",
  "subtype": "bug",
  "stage_diagram_id": "<STAGE_DIAGRAM_ID>",
  "fields": []
}'
```

- For a custom object, use `"type": "tenant_fragment"`, `"is_custom_leaf_type": true`, and `"leaf_type"` = your custom object name.
- By default a subtype inherits transitions from its parent type; once you assign a dedicated diagram, publish the change to activate it.
- **Verify**: `schemas.aggregated.get` with `custom_schema_spec: { "subtype": "bug" }` to see the assigned diagram.

### Step 5 (optional) — Add dependent-field conditions on stages

**Reference**: §6 (Dependent-field conditions on stages).

Enforce rules tied to a stage — for example, require an RCA field when a bug reaches a specific stage. Add `conditions` to the subtype fragment:

```json
"conditions": [{
  "expression": "stage == 'don:core:dvrv-us-1:devo/0:stage/5'",
  "effects": [{ "fields": [ "custom_fields.rca" ], "require": true }]
}]
```

Effects can `require`, `show`, or constrain `allowed_values` for fields. Include this in the `schemas.custom.set` call for the subtype.

### Updating stages and diagrams

- **Update a state**: `states.custom.update` with `id`, `name`, and/or `ordinal` (§2).
- **Update a stage**: `stages.custom.update` with `id`, `name`, `ordinal`, and/or `state_id` (§3).
- **Update a diagram**: `stage-diagrams.update` to change transitions, deprecate stages, or rename (§4). Note: `is_default` and `leaf_type` are immutable after creation.

**Verify after each tier** (§2–4): always run the matching `*.list` call after creating each tier (states, then stages, then diagram) before building the next, to catch errors early.

## Reference index

| File | When to read it |
| --- | --- |
| `references/Stages_States_and_StageDiagrams_API.md` | Entire file — concepts (§1), creating states (§2), creating stages (§3), creating stage diagrams (§4), assigning diagrams to subtypes (§5), dependent-field conditions (§6), quick reference table (§7), common pitfalls (§8) |

## DON id scratchpad

Keep track of returned DON ids for dependent calls:

```
STATE_ID=         STAGE_ID_1=       STAGE_ID_2=       STAGE_ID_3=
STAGE_DIAGRAM_ID= SUBTYPE_NAME=     CUSTOM_OBJECT_TYPE=
```

## Safety

Confirm before these operations:
- Deprecating a stage (`is_deprecated: true` in a stage-diagrams.update) — existing records referencing that stage are not orphaned, but the stage is hidden from new transitions.
- Changing a diagram's transitions — records currently in the old flow may become stuck if the new diagram removes their current stage or valid transitions. Verify with `stage-diagrams.get` and `works.list` filtered by stage before applying.

**Stages within a diagram deprecate via `is_deprecated`** (§4, §8): to retire a stage without breaking the diagram or orphaning records, set `is_deprecated: true` on that stage's node inside the diagram via `stage-diagrams.update`. Do not delete stages that are referenced by a diagram. (The references document `is_deprecated` only on stage nodes within a diagram — not on the diagram object itself; whole-diagram retirement is not covered, so verify against the live API before attempting it.)

After any lifecycle change:
- Verify each tier with the matching `*.list` call before building the next.
- Test a record transition: create a test work item (or custom object), set its `stage`, and update it via `works.update` or `custom-objects.update` to confirm the allowed transitions work as expected.

## Common pitfalls (from the reference §8)

- **Creating a stage before its state exists**: fails, because `state` must resolve to a valid state ID. Always create states first (Step 1), then stages (Step 2).
- **Duplicate `ordinal` for states**: must be unique within the dev org (§2). For stages the reference states no uniqueness rule — keep them unique anyway for predictable ordering.
- **Forgetting to assign the diagram to the subtype**: stages and the diagram exist, but the object still uses the inherited/default lifecycle until the subtype references the `stage_diagram_id` (Step 4) and the change is published.
- **Deleting a stage that's referenced by a diagram**: do not delete — deprecate it (`is_deprecated: true`) instead so existing records aren't orphaned.
- **Immutable fields**: `is_default` and `leaf_type` on a stage diagram cannot be changed after creation (§4, §8). Choose them carefully at creation time.

## Field notes (live-learned; see docs/LEARNINGS.md)

Dated facts discovered while operating this domain — errors hit, restrictions found, behaviors that
differ from the references. Add entries via the `capture-learnings` protocol
(`.claude/skills/capture-learnings/SKILL.md`): one dated bullet per fact, with evidence. If a fact
*corrects* a reference doc, fix the doc in place too — this section is for knowledge that has no
better home or needs domain-level visibility.

- **2026-07-18 · Standalone custom stages and states are PERMANENT once created.** `stages.custom.delete` and `states.custom.delete` both return HTTP 404 "route not found". `stages.custom.update` accepts `name` and `ordinal` but rejects every deprecation-shaped field tried (`is_deprecated`, `deprecated`, `archived`, `active`, `is_active`, `enabled`, `is_enabled`, `status`) with HTTP 400. The `is_deprecated` flag documented in this skill's reference lives on a stage node **inside a stage diagram** — not on the standalone stage/state object.
- **2026-07-18 · Warning to add before creating**: because there is no cleanup path, treat every `states.custom.create` / `stages.custom.create` as durable. Test in a dev tenant where clutter is acceptable, or use existing state/stage IDs by list-first instead of create.
- **2026-07-18 · Response wrapper is `custom_state` / `custom_stage` (not `state` / `stage`).** `.create` returns `{"custom_state": {"id": "..."}}`; `.list` returns `{"result": [...], "cursor": "..."}`. Parsers assuming the shorter name silently return null IDs.
- **2026-07-18 · Regression orphans**: `custom_stage/44` and `custom_state/6` in `devo/1139FmGETi` were created by regression testing and renamed to `zzz_ORPHAN_REGRESSION_DELETE_ME` — they'll appear at the bottom of the stages/states list in DevRev Settings until manually purged from the UI. Manual UI delete works even when the API doesn't.
