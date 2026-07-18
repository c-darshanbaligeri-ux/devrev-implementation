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

**Live-verified 2026-07-19 — CONFIRMED working via two distinct mechanisms**, correcting the
2026-07-18 finding below (which ruled out `stage_diagram_id` and a nested `{"stage_diagram":{...}}`
object, but never tried `stage_diagram` as a bare DON-id **string**, or the leaf-type-level
`is_default` path).

**Mechanism A — leaf-type-level default diagram**, set at `stage-diagrams.create` time with
`is_default: true`. Only works while the leaf type has no existing default diagram (a second
`is_default: true` create for the same leaf type returns `HTTP 409 conflict`), and `is_default`
remains immutable after creation (cannot be added later via `.update`):

```bash
curl -X POST 'https://api.devrev.ai/stage-diagrams.create' \
-H 'Authorization: Bearer $DEVREV_TOKEN' \
-d '{
  "leaf_type": "regression_test_asset",
  "is_custom_leaf_type": true,
  "is_default": true,
  "name": "Asset lifecycle",
  "stages": [ ... ]
}'
```

**Mechanism B — subtype-level diagram**, via `stage_diagram` (the bare DON id **as a string**,
not `stage_diagram_id` and not a nested object) on `schemas.custom.set`:

```bash
curl -X POST 'https://api.devrev.ai/schemas.custom.set' \
-H 'Authorization: Bearer $DEVREV_TOKEN' \
-d '{
  "type": "custom_type_fragment",
  "leaf_type": "issue",
  "subtype": "bug",
  "description": "Bug subtype",
  "stage_diagram": "don:core:dvrv-us-1:devo/xxx:stage_diagram/12",
  "fields": [ ... ]
}'
```

Remember the full-field-replay rule (Field notes) applies here too if the subtype fragment already
exists — replay its complete `fields` array, don't send a partial list.

- For a custom object leaf type (not a subtype), use Mechanism A, or Mechanism B's shape with
  `"type": "tenant_fragment"` and `"is_custom_leaf_type": true` instead of `subtype`.
- **Enforcement differs by object class — important caveat.** On **custom objects**,
  `custom-objects.update` genuinely enforces the attached diagram's transitions: a non-adjacent or
  non-member stage is rejected (`HTTP 400 bad_request`). On **stock-type subtypes**, `works.update`
  showed **no enforcement at all** in testing — setting `stage` to values outside the attached
  diagram (including stages from entirely different lifecycles) still returned `HTTP 200` and
  changed the stage. The attachment itself is real and visible in `schemas.aggregated.get`, but
  treat it as informational/UI-level for stock leaf types until further evidence shows otherwise —
  don't promise a caller that `works.update` will reject invalid stage transitions on a subtype.
- **Verify**: `GET schemas.aggregated.get?leaf_type=<leaf_type>` (add `&is_custom_leaf_type=true` for a custom leaf type) to see the assigned diagram under the `stage_diagram_id` key (the read-side key name is still `stage_diagram_id`, even though the write-side field for Mechanism B is `stage_diagram`). Equivalently, `POST schemas.aggregated.get -d '{"leaf_type":"<leaf_type>"}'` with `custom_schema_spec` omitted also works — only sending `custom_schema_spec: {"tenant_fragment": true}` specifically is rejected (see Field notes). For a subtype specifically, use `custom_schema_spec: {"subtype": "<name>"}`.

<details>
<summary>2026-07-18 finding this section corrects (kept for audit trail, not a live instruction)</summary>

Every write path tried in the 2026-07-18 session for attaching a diagram to a subtype or custom leaf
type was rejected: `schemas.custom.set` with `stage_diagram_id`, `diagram_id`, `stagediagram_id`,
`stage_diagram_ref`, `lifecycle_id`, `workflow_diagram_id`, and a **nested** `{"stage_diagram":{"id":...}}`
object all → `invalid_field`. The root cause of the miss: `stage_diagram` was tried, but only as a
nested object, not as a bare string — the bare-string shape works (Mechanism B above).
</details>

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
- Changing a diagram's transitions — records currently in the old flow may become stuck if the new diagram removes their current stage or valid transitions. Verify with `stage-diagrams.get` and `works.list` filtered by stage before applying.

**Stage deprecation via `is_deprecated` does NOT work (live-verified 2026-07-18) — do not tell a user this is available.** `is_deprecated: true` on a stage node is rejected with HTTP 400 `bad_request` at both `stage-diagrams.create` and `stage-diagrams.update`, tried on the start stage, a middle stage, and a terminal stage with no dependents. `is_deprecated: false` is accepted as a no-op, and omitting the field entirely succeeds — only the `true` value is rejected. There is currently no known working mechanism to retire a stage inside a diagram via the public API; every stage added to a diagram must be treated as permanent for the diagram's lifetime. See Field notes for full evidence.

After any lifecycle change:
- Verify each tier with the matching `*.list` call before building the next.
- Test a record transition: create a test work item (or custom object), set its `stage`, and update it via `works.update` or `custom-objects.update` to confirm the allowed transitions work as expected.

## Common pitfalls (from the reference §8)

- **Creating a stage before its state exists**: fails, because `state` must resolve to a valid state ID. Always create states first (Step 1), then stages (Step 2).
- **Duplicate `ordinal` for states**: must be unique within the dev org (§2). For stages the reference states no uniqueness rule — keep them unique anyway for predictable ordering.
- **Forgetting to assign the diagram to the subtype**: stages and the diagram exist, but the object still uses the inherited/default lifecycle until the subtype references the diagram (Step 4) via `stage_diagram` (bare DON string, on the subtype fragment) or `is_default: true` (leaf-type level, at diagram-create time). See Step 4 for the two confirmed-working mechanisms, and its enforcement caveat (custom objects enforce transitions; stock-type subtypes did not in testing).
- **Deleting a stage that's referenced by a diagram**: do not delete — there is no delete endpoint anyway. Deprecating it instead (`is_deprecated: true`) is the documented fallback but **does not work live** (HTTP 400 `bad_request` — see Field notes); as of this session there is no working retirement mechanism, so choose stages conservatively since they're effectively permanent once added to a diagram.
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
- **2026-07-18 · E2E pass: `stage_diagram_id` on `schemas.custom.set` is REJECTED — the documented subtype/custom-leaf-type diagram-attachment mechanism does not work via the public API.** `POST schemas.custom.set` with `{"type":"tenant_fragment","leaf_type":"regression_test_asset","is_custom_leaf_type":true,"stage_diagram_id":"don:core:dvrv-us-1:devo/1139FmGETi:stage_diagram/9",...}` → `{"message":"Bad Request","type":"invalid_field","field_name":"stage_diagram_id"}`. Also tried field-name variants `stage_diagram`, `diagram_id`, `stagediagram_id`, `stage_diagram_ref`, `lifecycle_id`, `workflow_diagram_id`, and a nested `{"stage_diagram":{"id":"..."}}` shape — all rejected identically (`invalid_field`). Repeated on a subtype fragment (`type: custom_type_fragment`, `leaf_type: issue`, `subtype: regression_test_bug`) with the same `stage_diagram_id` rejection. `schemas.subtypes.prepare-update` also rejects both `subtype` and `stage_diagram_id` as `invalid_field` — it only accepts `leaf_type` (returns `{"added_fields":[...]}` showing fields that would be added by upgrading records). By contrast, `schemas.aggregated.get` DOES expose a **read-only** `stage_diagram_id` key for stock leaf types that already have a diagram (e.g. `ticket` → `"stage_diagram_id":{"id":"don:core:...:stage_diagram/6","name":"ticket_transitions"}`), proving the field exists in the data model — but no working write path was found this session. Skill 1's `references/Custom_Objects_and_Links_API.md` (§ custom-object stage wiring) and its skill 8 mirror document this same unverified mechanism and need the same correction.
- **2026-07-18 · CORRECTED 2026-07-18 (later same day): the `custom_schema_spec: {"tenant_fragment": true}` shape specifically is rejected — POST itself is fine.** The original finding here overgeneralized from one test. Precise, re-verified behavior: `POST schemas.aggregated.get -d '{"leaf_type":"ticket","custom_schema_spec":{"tenant_fragment":true}}'` → `HTTP 400 invalid_field field_name: tenant_fragment` (reproduced on both `ticket` and a custom leaf type) — tenant/custom fields are included by default, so the fix is to **omit `custom_schema_spec` entirely** for that case, not necessarily to switch to GET. `POST schemas.aggregated.get -d '{"leaf_type":"issue"}'` (no `custom_schema_spec`) returns `HTTP 200` with the full merged field set under `{"schema": {...}}`, and `POST ... -d '{"leaf_type":"issue","custom_schema_spec":{"subtype":"<name>"}}'` also works via POST — only the `tenant_fragment` key inside `custom_schema_spec` is the problem, not the POST method or `custom_schema_spec` itself. A bare `GET schemas.aggregated.get?leaf_type=<type>` also works and is equivalent when no subtype filtering is needed. This affects skill 1's docs too (same example shape appears there) — corrected in both places.
- **2026-07-18 · E2E pass: `is_deprecated: true` on a stage node is REJECTED outright, at both create and update time — the documented stage-retirement mechanism does not work.** Isolated tests on `stage-diagrams.update`: setting `is_deprecated: true` on the start stage → `{"message":"Bad Request","type":"bad_request"}`; on a middle stage (not start, has dependents) → same `bad_request`; on a terminal stage with no outgoing transitions and no incoming transitions left pointing at it → same `bad_request`. Also tested at `stage-diagrams.create` time on a brand-new diagram never touched by `.update` (so not a stale-diagram artifact) — same `bad_request`, HTTP 400. The identical payload with `is_deprecated` simply omitted succeeds (`stage-diagrams.create` → HTTP 201; `stage-diagrams.update` → HTTP 200). Setting `is_deprecated: false` explicitly is accepted as a no-op, confirming the field is parsed but `true` specifically is rejected. This directly contradicts this SKILL.md's Safety section, its Common pitfalls section, and reference §4/§8, which all describe `is_deprecated: true` as the supported way to retire a stage without breaking a diagram. **As of this session there is no known working mechanism to retire/deprecate a stage inside a diagram via the public API** — treat every stage added to a diagram as permanent for as long as that diagram exists.
- **2026-07-18 · E2E pass: `stage-diagrams.list?leaf_type=<custom_leaf_type>` alone returns empty for custom leaf types — `is_custom_leaf_type=true` must be passed alongside it.** Two diagrams created for the custom leaf type `regression_test_asset` were confirmed to exist via `stage-diagrams.get?id=...` and appeared in `stage-diagrams.list?is_custom_leaf_type=true` (unfiltered by leaf_type) — but `stage-diagrams.list?leaf_type=regression_test_asset` alone returned `{"result":[]}`. Adding `&is_custom_leaf_type=true` to the same query returned both diagrams correctly. Reference §4 "Read" bullet lists `leaf_type`, `name`, `is_custom_leaf_type` as if independently optional filters; for custom leaf types they are not independent — `is_custom_leaf_type=true` is required alongside `leaf_type` to get a match.
- **2026-07-18 · E2E pass: `stage-diagrams.create` rejects a top-level `subtype` field.** `{"leaf_type":"issue","subtype":"regression_test_bug","name":"...","stages":[...]}` → `{"message":"Bad Request","type":"invalid_field","field_name":"subtype"}`. Diagrams are `leaf_type`-scoped only, with no direct subtype-scoped creation path — consistent with the `stage_diagram_id` finding above: subtype-specific lifecycles currently have **no confirmed working attachment path** via the public API (neither via the diagram nor via the schema fragment).
- **2026-07-18 · E2E pass: dependent-field stage conditions (§6) CONFIRMED WORKING end-to-end — no doc fix needed.** Added `"conditions":[{"expression":"stage == '<completed-stage-DON>'","effects":[{"fields":["custom_fields.impacted_environments"],"require":true}]}]` to an existing subtype fragment (`issue`/`regression_test_bug`) via `schemas.custom.set` (created a new versioned fragment, per the already-known versioned-create behavior). Verified live: with the test record in the `completed` stage, clearing the required field via `works.update` returned `{"message":"Bad Request","type":"customization_validation_error","reason":"required field ctype__impacted_environments cannot be set to an empty array","subtype":"field_required"}` (HTTP 400). Moving the same record to the `triage` stage (not named in the condition) and clearing the same field then succeeded (HTTP 200) — confirming the requirement is correctly stage-scoped rather than global.
- **2026-07-18 · E2E pass: immutability and filter behaviors confirmed exactly as documented (no fix needed).** `stage-diagrams.update` with `is_default: true` → `invalid_field`; with `leaf_type` set to a different value than at creation → `invalid_field`. `stage-diagrams.list?name=<exact match>` returns the matching diagram; `?name=<no match>` returns `{"result":[]}` — the `name` filter works as documented.
- **2026-07-18 · E2E pass: new permanent test artifacts created (no delete path exists for any of these — see the PERMANENT finding above).** `stage_diagram/9` (leaf_type `regression_test_asset`, renamed to `zzz_E2E_TEST_asset_lifecycle_renamed`), `stage_diagram/10` (`zzz_E2E_TEST_deprecation_probe2`, same leaf_type), `custom_type_fragment/3` (supersedes `custom_type_fragment/2` for the `regression_test_bug` subtype, adds the `conditions` block above), and `custom_object/regression_test_asset/1` (test record, display id `C-RTASSET-1`). All in `devo/1139FmGETi`. Also notable: `custom-objects.create` for `regression_test_asset` succeeded this session (HTTP 201) — access must have been granted sometime after the 403 recorded in skill 1's Field notes for the same leaf type.
- **2026-07-19 · CORRECTS the 2026-07-18 row above — stage-diagram attachment to a subtype/custom leaf type DOES work.** Root cause of the prior miss: `stage_diagram` (bare DON-id **string**) was never tried — only `stage_diagram_id` and a **nested** `{"stage_diagram":{"id":...}}` object were, and both are genuinely rejected. The bare string works: `POST schemas.custom.set {"type":"custom_type_fragment","leaf_type":"issue","subtype":"regression_test_bug","stage_diagram":"don:core:...:stage_diagram/12","fields":[...]}` → `HTTP 201`, and `schemas.custom.get`/`schemas.aggregated.get` both confirm it persisted. Separately, `stage-diagrams.create` with `is_default: true` at create time also attaches a diagram at the **leaf-type** level (not subtype-level) — confirmed via `schemas.aggregated.get` showing `stage_diagram_id` populated; a second `is_default:true` create for the same leaf type correctly `409 conflict`s, and `is_default` remains immutable via `.update`. New artifacts: `stage_diagram/11` (`e2er2s2_default_diagram_attach_test`, leaf_type `regression_test_asset`, `is_default:true`), `stage_diagram/12` (`e2er2s2_issue_subtype_diagram_probe`, leaf_type `issue`), `custom_type_fragment/5` (new version of the `regression_test_bug` subtype fragment, adds `stage_diagram` pointing at `stage_diagram/12`; supersedes `/3`, which still exists per versioned-create behavior). See Step 4 and reference §5 for the full corrected mechanism and an important enforcement caveat below.
- **2026-07-19 · Stage-diagram enforcement differs by object class — custom objects enforce, stock-type subtypes did not in testing.** After attaching `stage_diagram/12` (only `triage → completed` allowed) to `issue`'s `regression_test_bug` subtype, `works.update` on a record of that subtype accepted `stage` values from unrelated lifecycles (`in_review`, an opportunity-only `negotiation` stage, an incident-only `mitigated` stage, an enhancement-only `general_availability` stage) — all `HTTP 200`, all actually changed the stage. The only rejection reproducible was a syntactically invalid stage DON. By contrast, the same diagram attached to `regression_test_asset` (a custom object) via `custom-objects.update` correctly rejected non-member/non-adjacent stages with `HTTP 400 bad_request`. Conclusion: don't promise a caller that attaching a diagram to a stock-type subtype will gate `works.update` transitions — it may be advisory/UI-only for stock leaf types, unlike custom objects where it's a real guardrail.
- **2026-07-19 · Dependent-field stage conditions (§6) are enforced only on explicit field-touch, not as a standing invariant.** A record can sit in the conditioned stage indefinitely with the required field empty, as long as no update explicitly tries to clear that field again — moving into the stage with the field already empty succeeds, and updating unrelated fields while parked there doesn't retroactively validate the conditioned field. Only an update that explicitly sets the field to empty while in that stage gets rejected.
- **2026-07-19 · `schemas.aggregated.get` via `GET` on a custom leaf type silently returns an empty schema (not an error) if `is_custom_leaf_type=true` is omitted.** `GET ?leaf_type=regression_test_asset` (no flag) → `HTTP 200 {"custom_fields":[],...}` — easy to misread as "no custom fields exist" rather than "wrong query." Always pass `&is_custom_leaf_type=true` for custom leaf types.
