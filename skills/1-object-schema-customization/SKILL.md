---
name: object-schema-customization
description: Customize DevRev object schemas — create custom object types, add fields to tickets/accounts/issues, define subtypes, add tenant fields, create custom link types, modify stock object schemas with field overrides. Use when you need to extend DevRev's data model to capture domain-specific attributes or define new object types. Covers schema fragments, tenant/subtype fields (tnt__/ctype__ prefixes), custom objects with lifecycle stages, and custom link types for relationships between objects.
---

# Object & schema customization — executable playbook

Customize DevRev's object model: add fields to stock objects (ticket, issue, account, part), create entirely new object types (custom objects), define subtypes, and wire custom relationships between objects. Read the repo root `CLAUDE.md` first for global API rules; use this skill for any schema/object customization request.

## When to use

Trigger when the user wants to:
- Create a custom object type (e.g. Campaign, Asset, Contract)
- Add a field to tickets, accounts, issues, or any stock object
- Define or modify a subtype (e.g. bug subtype of issue)
- Add a tenant field (applies org-wide to all records of a type)
- Create a custom link type to relate objects
- Override a stock field's display name or allowed values
- Modify an object's schema or check the aggregated schema

## When not to use

- Stage/state/lifecycle customization → `skills/2-stage-lifecycle-customization`
- File uploads or bulk data migration or building a fresh org → `skills/3-data-upload-and-org-build`
- Raw API calls with no schema changes → `skills/8-devrev-api`

## Preconditions

1. Token in `.env` (`DEVREV_PAT`). If missing, tell the user exactly what to put in it and stop — never fabricate a token.
2. Verify token works: `POST https://api.devrev.ai/ping` before starting.
3. Required scopes (from `references/Custom_Objects_and_Links_API.md` and `references/Stock_Object_Modification_and_Schemas_API.md`):
   - Custom objects & schema fragments: `custom_type_fragment:write`
   - Custom link types: `custom_link_type:write` (create/update); no scope for get/list
4. For operations referencing parent objects (e.g. linking a custom object to a part), the parent DON ids must exist. Keep a DON scratchpad (see below).

## Playbooks

Every playbook step cites the exact reference file and section. Follow the order, substitute real DON ids, and verify after each change with the matching `*.get`/`*.list` call.

### Playbook 1 — Create a custom object type

**Reference**: `references/Custom_Objects_and_Links_API.md` §1 (Custom objects — end to end).

**Steps**:

1. **Define the schema** — `schemas.custom.set` (scope: `custom_type_fragment:write`) with `is_custom_leaf_type: true` and an `id_prefix` to distinguish it from stock objects.

   ```bash
   curl -X POST 'https://api.devrev.ai/schemas.custom.set' \
   -H 'Authorization: Bearer $DEVREV_TOKEN' \
   -H 'Content-Type: application/json' \
   -d '{
     "type": "tenant_fragment",
     "leaf_type": "campaign",
     "leaf_type_display_name": "Campaign",
     "is_custom_leaf_type": true,
     "id_prefix": "CAMP",
     "fields": [
       { "name": "start_date", "field_type": "date",
         "description": "Start date of the campaign" },
       { "name": "budget", "field_type": "int",
         "description": "Budget allocated" },
       { "name": "target_audience", "field_type": "enum",
         "allowed_values": [ "Professionals", "Students" ] }
     ]
   }'
   ```

2. **Create a record** — `custom-objects.create` (scope: `custom_type_fragment:write`). Pass `unique_key` for idempotency and `custom_schema_spec` (mandatory; without it you get Bad Request).

   ```bash
   curl -X POST 'https://api.devrev.ai/custom-objects.create' \
   -H 'Authorization: Bearer $DEVREV_TOKEN' \
   -d '{
     "leaf_type": "campaign",
     "custom_schema_spec": { "tenant_fragment": true },
     "unique_key": "CAMP-1",
     "custom_fields": { "tnt__budget": 10000 }
   }'
   ```

3. **Verify** — `custom-objects.list` to confirm the record exists; `schemas.custom.list` to confirm the schema.

4. **Grant access** — custom objects start with **zero access** (even for admins). Grant roles in Settings > Object customization and Settings > User Management > Roles before they appear in the UI.

**Optional enhancements** (same reference §1):
- **Add a stage field** (lifecycle) — create states, stages, and a stage diagram for the custom leaf type (see `skills/2-stage-lifecycle-customization`), then attach the diagram to the schema via `stage_diagram` (a bare DON-id **string** — not `stage_diagram_id`, which is rejected) on `schemas.custom.set`, or via `is_default: true` at `stage-diagrams.create` time. Records can then transition via `custom-objects.update` with `stage` — confirmed live to actually enforce the diagram's allowed transitions for custom objects.
- **Add a tags field** — model it as a custom field (not a native `tags` property). Use `field_type: "array"` with `base_type: "id"` and `id_type: [ "tag" ]` to store references to real DevRev tags created with `tags.create`.
- **Add a part field** (reference a product/capability/feature) — use `field_type: "id"` with `id_type: [ "product", "capability", "feature" ]`. Pass the part DON in `custom_fields`.
- **Add subtypes** (yes, custom leaf types support subtypes, same mechanism as stock objects) — see Playbook 3, and `references/Custom_Objects_and_Links_API.md` §1 Step 5. A subtype on a custom leaf type inherits the tenant fragment's fields and adds its own `ctype__` fields; the only difference from subtyping a stock object is that `leaf_type` refers to your own `is_custom_leaf_type: true` type instead of a built-in one.

### Playbook 2 — Add tenant fields to stock objects & override stock fields

**Reference**: `references/Stock_Object_Modification_and_Schemas_API.md` §4 (Modify a stock object — add fields & overrides).

**Steps**:

1. **Inspect the stock schema** (always read first) — `schemas.stock.get` for the leaf type to see built-in fields.

   ```bash
   curl -X POST 'https://api.devrev.ai/schemas.stock.get' \
   -H 'Authorization: Bearer $DEVREV_TOKEN' \
   -d '{ "leaf_type": "ticket" }'
   ```

2. **Add a tenant field** — applies to every record of the type. Use `schemas.custom.set` with `type: "tenant_fragment"` (scope: `custom_type_fragment:write`). The field is prefixed `tnt__` on records.

   ```bash
   curl -X POST 'https://api.devrev.ai/schemas.custom.set' \
   -H 'Authorization: Bearer $DEVREV_TOKEN' \
   -d '{
     "type": "tenant_fragment",
     "leaf_type": "ticket",
     "fields": [
       { "name": "escalation_reason", "field_type": "rich_text",
         "ui": { "display_name": "Escalation Reason" } }
     ]
   }'
   ```

3. **Override a stock field** (e.g. rename priority, restrict allowed values) — include `stock_field_overrides` in the fragment for the leaf type. This changes display/behavior only; the stock field is preserved.

   ```bash
   curl -X POST 'https://api.devrev.ai/schemas.custom.set' \
   -H 'Authorization: Bearer $DEVREV_TOKEN' \
   -d '{
     "type": "tenant_fragment",
     "leaf_type": "issue",
     "stock_field_overrides": [
       {
         "name": "priority",
         "ui": { "display_name": "Business Priority" }
       }
     ]
   }'
   ```

4. **Verify** — check the merged view with `schemas.aggregated.get`. **Live-verified 2026-07-18: `custom_schema_spec: { "tenant_fragment": true }` is REJECTED** (`HTTP 400 invalid_field field_name: tenant_fragment`) — tenant fields are included by default, so just omit `custom_schema_spec` entirely for this case:

   ```bash
   curl -X POST 'https://api.devrev.ai/schemas.aggregated.get' \
   -H 'Authorization: Bearer $DEVREV_TOKEN' \
   -d '{
     "leaf_type": "ticket"
   }'
   ```

   A `GET` with query params (`?leaf_type=ticket`) also works and is equivalent. `custom_schema_spec: {"subtype": "<name>"}` (no `tenant_fragment` key) DOES work via POST when you need a specific subtype's merged fields — only the `tenant_fragment` key inside `custom_schema_spec` is rejected on this endpoint.

**Supported field types** (§4): `int`, `double`, `bool`, `tokens`, `text`, `rich_text`, `enum`, `uenum`, `timestamp`, `date`, `id`, plus array/list variants.

**After schema changes**: fragments are versioned. Existing records reference the old version until upgraded. Re-save affected records via their `*.update` with the current `custom_schema_spec` to pick up the latest fragment, OR use `objects.bulk-upgrade` to upgrade all records of a type at once. **Confirmed live 2026-07-18**: `objects.bulk-upgrade` exists ONLY at `/internal/objects.bulk-upgrade` (the public-root path `POST /objects.bulk-upgrade` 404s route-not-found) — `{"type":"<obj_type>"}` (optionally `subtype`) returns HTTP 200 `{"id":"<job_don>"}`; poll `jobs.get?id=<job_don>` for `job_category:"bulk_upgrade"` and `state:"completed"` (a `metadata_list` entry reports the count upgraded). This closes the prior "mentioned but unverified" status. It affects ALL matching records org-wide — confirm before running; for a single record, re-save via `*.update` instead.

### Playbook 3 — Create and manage subtypes

**Reference**: `references/Stock_Object_Modification_and_Schemas_API.md` §5 (Manage subtypes); worked example: `../3-data-upload-and-org-build/references/DevRev_Building_Org_Using_API_v1.md` Phase 1 §1.2 (Add a subtype with custom fields); custom-leaf-type variant: `references/Custom_Objects_and_Links_API.md` §1 Step 5.

This playbook applies equally to stock leaf types (`issue`, `ticket`, ...) and to custom leaf types you defined yourself in Playbook 1 (`is_custom_leaf_type: true`) — a subtype is always a `custom_type_fragment` scoped to a `leaf_type` + `subtype` name, and it inherits every field of that leaf type's tenant fragment regardless of whether the leaf type is stock or custom.

**Steps**:

1. **Define the subtype** — `schemas.custom.set` with `type: "custom_type_fragment"`, `leaf_type`, `subtype`, `subtype_display_name`, and its fields. Subtype fields are prefixed `ctype__` on records.

   ```bash
   curl -X POST 'https://api.devrev.ai/schemas.custom.set' \
   -H 'Authorization: Bearer $DEVREV_TOKEN' \
   -d '{
     "type": "custom_type_fragment",
     "leaf_type": "issue",
     "subtype": "bug",
     "subtype_display_name": "Bug",
     "fields": [
       { "name": "impacted_environments", "field_type": "array",
         "base_type": "enum",
         "allowed_values": [ "Dev", "QA", "Prod" ],
         "ui": { "display_name": "Impacted Environments" } },
       { "name": "rca", "field_type": "rich_text",
         "ui": { "display_name": "RCA" } }
     ]
   }'
   ```

2. **Create a record** with the subtype — pass `custom_schema_spec: { "subtype": "bug" }` and reference fields as `ctype__<name>`:

   ```bash
   curl -X POST 'https://api.devrev.ai/works.create' \
   -H 'Authorization: Bearer $DEVREV_TOKEN' \
   -d '{
     "type": "issue",
     "title": "API failure in Prod",
     "applies_to_part": "<PART_ID>",
     "owned_by": [ "<DEVU_OWNER_ID>" ],
     "custom_schema_spec": { "subtype": "bug" },
     "custom_fields": { "ctype__impacted_environments": [ "Prod" ] }
   }'
   ```

   **On a custom leaf type instead of a stock one** — same shape, just add `is_custom_leaf_type: true` to the `schemas.custom.set` call in step 1 and use `custom-objects.create` (not `works.create`) in this step, since custom-object records are created through their own endpoint:

   ```bash
   curl -X POST 'https://api.devrev.ai/custom-objects.create' \
   -H 'Authorization: Bearer $DEVREV_TOKEN' \
   -d '{
     "leaf_type": "campaign",
     "custom_schema_spec": { "subtype": "social_media", "tenant_fragment": true },
     "custom_fields": {
       "tnt__budget": 10000,
       "ctype__social_media_platform": "Facebook"
     }
   }'
   ```

3. **Verify** — `schemas.aggregated.get` with `custom_schema_spec: { "subtype": "bug" }` shows the merged field set (the `tenant_fragment: true` key inside `custom_schema_spec` is rejected — see Field notes). `schemas.subtypes.list` lists subtypes **but requires a `leaf_type` filter** — called bare (`{}`) it always returns `{"subtypes":[]}` regardless of what exists; pass `{"leaf_type":"issue"}` to see them.

4. **Attach a stage diagram** (optional) — for lifecycle control, create a stage diagram (see `skills/2-stage-lifecycle-customization`) and reference it from the subtype fragment via `stage_diagram` (bare DON-id **string** — `stage_diagram_id` and a nested object are both rejected) on `schemas.custom.set`. **Caveat**: confirmed to gate `custom-objects.update` transitions on custom objects; NOT confirmed to gate `works.update` transitions on stock-type subtypes (testing showed no enforcement there) — see `skills/2-stage-lifecycle-customization` Field notes.

5. **Prepare a subtype update** (for large changes) — `schemas.subtypes.prepare-update` (scope: `custom_type_fragment:write`) validates and stages the change before you apply it, reporting field conflicts as `ABSENT_IN_NEW` (field dropped) or `INCOMPATIBLE_TYPE` (field kept but `field_type` changed) — **unconfirmed live**, sourced from DevRev's docs, not yet exercised in this repo (the one live probe on record only tried `subtype`/`stage_diagram_id` params and got `invalid_field`; it never tried a same-leaf-type `leaf_type`-only preview payload — see Field notes 2026-07-18 row on this endpoint).

6. **Scope field-level access to a subtype** (optional) — in Settings > User Management > Roles, a role can be scoped to one subtype via `target_subtype`, or applied to every subtype of a leaf type via `include_all_subtypes: true`. This is layered on top of the object-level access grant (Playbook 1 step 4) — **UI-only per this repo's existing findings; not confirmed to have an API equivalent.**

**UI-only alternative for stock-object subtypes** (not applicable to custom leaf types): for `issue`, `ticket`, `opportunity`, `account`, `contact`, and `part`, Settings > Object customization > Subtypes tab lets an admin create a subtype, add its fields, and assign a subtype-specific stage diagram entirely without API calls. `incident` and `meeting` subtypes are API-only — no UI path. This is a genuinely separate path from Playbook 3's `schemas.custom.set` steps above, not just a UI wrapper around the same calls — useful to mention when a user without API access needs a stock-object subtype.

### Playbook 4 — Create custom link types

**Reference**: `references/Custom_Objects_and_Links_API.md` §3 (Custom link types).

Custom link types define relationships not covered by built-in types (`serves`, `is_part_of`, `is_dependent_on`, `is_related_to`). Use when tying a custom object to a ticket, or any non-standard relationship. Allowed between work objects, identity objects (account, rev/dev user, rev org), part objects, and custom leaf types.

**Steps**:

1. **Define the type** — `link-types.custom.create` (scope: `custom_link_type:write`). Specify `source_types` and `target_types` (each with `leaf_type`; add `is_custom_leaf_type: true` for custom objects). Optionally restrict to specific subtypes by adding `subtype`.

   ```bash
   curl -X POST 'https://api.devrev.ai/link-types.custom.create' \
   -H 'Authorization: Bearer $DEVREV_TOKEN' \
   -d '{
     "name": "Link between ticket and campaign",
     "source_types": [ { "leaf_type": "ticket" } ],
     "target_types": [ { "leaf_type": "campaign", "is_custom_leaf_type": true } ],
     "forward_name": "relates to campaign",
     "backward_name": "referenced by ticket"
   }'
   ```

   Save the returned id as `CUSTOM_LINK_TYPE_ID` in your scratchpad.

2. **Create a link instance** — `links.create` with `link_type: "custom_link"` and `custom_link_type` set to the id from step 1. Requires `link:write` or `link:all`, plus read access to both objects.

   ```bash
   curl -X POST 'https://api.devrev.ai/links.create' \
   -H 'Authorization: Bearer $DEVREV_TOKEN' \
   -d '{
     "link_type": "custom_link",
     "custom_link_type": "<CUSTOM_LINK_TYPE_ID>",
     "source": "<TICKET_ID>",
     "target": "<CAMPAIGN_OBJECT_ID>"
   }'
   ```

3. **Verify** — `links.list` on either object to see the link; `link-types.custom.list` to see the type definition.

**Important**: Custom link types **cannot be deleted, only deprecated** (no public `link-types.custom.delete` — reference §3). To retire one, set `deprecated: true` via `link-types.custom.update`. This preserves referential integrity for existing links and old objects. Name them carefully.

## Reference index

Open these files as needed:

| File | When to read it |
| --- | --- |
| `references/Custom_Objects_and_Links_API.md` | Defining custom object types (§1); creating custom link types (§3); linking work items and custom objects (§4); custom object stage/tags/part/subtype fields (§1 Steps 3-5) |
| `references/Stock_Object_Modification_and_Schemas_API.md` | Adding fields to stock objects (§4); inspecting stock schemas (§2); viewing the aggregated schema (§3); managing subtypes (§5); field overrides (§4b); upgrading records after schema changes (§7) |

## DON id scratchpad

Keep track of returned DON ids for dependent calls:

```
CUSTOM_OBJECT_ID=       CUSTOM_LINK_TYPE_ID=       PART_ID=
TAG_ID=                 ACCOUNT_ID=                DEVU_OWNER_ID=
TICKET_ID=              WORK_ID=
```

## Safety

Confirm before these destructive/irreversible operations:
- Any `*.delete` on custom objects or custom link instances
- Deprecating a custom link type (`deprecated: true` is permanent; there is no `link-types.custom.delete`)
- `objects.bulk-upgrade` — confirmed live at `/internal/objects.bulk-upgrade` (see Playbook 2 note); affects ALL records of a type org-wide, so confirm before running; for a single record, prefer re-saving via `*.update`

After any schema change:
- Verify with `schemas.aggregated.get` to see the merged field set
- Re-save affected records via their `*.update` with the current `custom_schema_spec` so they pick up the latest fragment version
- For custom objects, confirm access was granted (Settings > Object customization and Roles) before expecting UI visibility

## Common pitfalls (from the references)

- **Wrong prefix silently fails**: `tnt__` for tenant fields, `ctype__` for subtype fields. A mismatched prefix fails to match with no error.
- **Missing `custom_schema_spec`**: sending custom fields without naming the schema returns Bad Request. Always include `custom_schema_spec` on create/update.
- **Custom objects invisible**: they start with zero access by default (even for admins). Grant roles explicitly.
- **Using display IDs in links**: always pass the full DON id (`don:core:...:ticket/456`), never a display ID like `TKT-456`.
- **Duplicate records**: pass a stable `unique_key` on `custom-objects.create` for idempotency.
- **Setting `stage` without a diagram**: attach a stage diagram to the leaf type first (Playbook 1 optional), or the stage value is rejected.
- **Trying to delete a custom link type**: no public delete endpoint — deprecate via `link-types.custom.update` with `deprecated: true`.
- **Old field values persisting**: records reference the old fragment version until upgraded — re-save them via `*.update` with the current `custom_schema_spec`.

## Field notes (live-learned; see docs/LEARNINGS.md)

Dated facts discovered while operating this domain — errors hit, restrictions found, behaviors that
differ from the references. Add entries via the `capture-learnings` protocol
(`.claude/skills/capture-learnings/SKILL.md`): one dated bullet per fact, with evidence. If a fact
*corrects* a reference doc, fix the doc in place too — this section is for knowledge that has no
better home or needs domain-level visibility.

- **2026-07-18 · `id_prefix` regex is `^[A-Z]{2,10}$`.** `schemas.custom.set` rejects a `id_prefix` with any digit or lowercase letter, or one shorter than 2 or longer than 10, with HTTP 400 `value_not_permitted`. Evidence: rejected `RGT639`, accepted `RGTEST`. Reference examples like `LOAN` are compliant but never named the pattern.
- **2026-07-18 · `leaf_type` for a NEW custom leaf must be `[a-z_]+`.** `schemas.custom.set` rejected `regression_test_1784390513` (digits) with HTTP 400 `bad_request`; accepted `regression_test`. Digits in `leaf_type` fail — no error field names the constraint, so you have to try/see. Do not append a timestamp to your test leaf_type.
- **2026-07-18 · `.get`/`.list`/`.set` response wrappers differ per op.** `schemas.custom.get` → `{"fragment": {...}}`. `schemas.custom.list` → `{"result": [...], "cursor": "..."}` (paginated). `schemas.custom.set` → `{"id": "..."}` only. Parsers that assume `{"schema": ...}` will silently return nulls.
- **2026-07-18 · `schemas.custom.set` behaves like versioned create, not full-replacement update.** Calling `.set` twice with the same `leaf_type` produces TWO fragments (`tenant_fragment/N`, `tenant_fragment/N+1`). The prior version doesn't get replaced; there is no way to delete or deprecate the previous version from the public API. Test carefully — every `.set` call is an additive commit. Reference doc's "full replacement" language means fields *within* a single fragment, not "supersede the previous fragment".
- **2026-07-23 · Unresolved conflict, needs a live test**: DevRev's own docs (not yet independently verified here) describe each new fragment version as chained to the old one via `old_fragment_ref`/`new_fragment_ref` keys, and describe `"is_deprecated": true` on a `.set` payload as the way to deprecate a fragment version. This directly conflicts with the row above, which found live (2026-07-18) that there is NO way to delete or deprecate a prior fragment version via the public API. Do not tell a user fragment deprecation works until someone actually tries `is_deprecated: true` on a `custom_type_fragment`/`tenant_fragment` payload and checks whether `schemas.custom.list` then excludes it — the two claims cannot both be right as stated.
- **2026-07-18 · `custom-objects.create` returns HTTP 403 Forbidden immediately after schema creation.** First call right after `schemas.custom.set` for `regression_test_asset` → HTTP 403 Forbidden (matches the CLAUDE.md rule "zero access by default"). A retry ~20-35 minutes later succeeded with no UI action taken in between.
- **2026-07-19 · CORRECTS the row above — the "~20-35 min auto-resolve" timing is NOT reliably reproducible; treat resolution as inconsistent, not a fixed window.** A fresh leaf type (`eersone_widget`) created and retried at +6min, +16min, +20min, and +22min was **still 403 every time** — the timing that worked for `regression_test_asset` did not generalize. Separately, retrying `custom-objects.create` on `regression_test_asset` itself (the exact leaf type from the original finding) *did* succeed this session, confirming that whatever granted access to it earlier is durable — but a brand-new leaf type does not automatically get the same treatment on the same schedule. Advice: if a user hits this 403, "wait and retry" is still worth trying before jumping to the UI, but don't promise a specific window — root cause (propagation delay vs. some other unidentified factor) remains unconfirmed.
- **2026-07-19 · `custom-objects.delete` confirmed live and genuinely working — not a documentation-only claim.** `POST custom-objects.delete {"id":"...custom_object/regression_test_asset/3"}` → `HTTP 200 {}`; follow-up `.get` → `HTTP 404`. Use it to clean up custom-object test records instead of leaving them permanent.
- **2026-07-19 · `custom-objects.list`/`.count` require `leaf_type`.** Omitting it returns `HTTP 400 missing_required_field field_name:"leaf_type"`. Not previously documented — SKILL.md/reference examples never showed this as mandatory.
- **2026-07-19 · `schemas.custom.get` requires `id`; `leaf_type` alone is rejected.** `POST schemas.custom.get {"leaf_type":"..."}` → `HTTP 400 invalid_field field_name:"leaf_type"`. Always fetch by the fragment's own `id`.
- **2026-07-19 · `id_prefix` appears globally unique per org, not just per leaf type.** Reusing the same `id_prefix` (e.g. `EERSONE`) on a second, distinct `leaf_type` returned `HTTP 400 bad_request`. Pick a fresh prefix per custom leaf type.
- **2026-07-19 · CORRECTS the `schemas.subtypes.list` row below — it DOES reflect new subtypes immediately, but only when called with a `leaf_type` filter.** `POST schemas.subtypes.list {"leaf_type":"ticket"}` showed a subtype created 11 seconds earlier, with zero measurable delay. `POST schemas.subtypes.list {}` (no filter) always returns `{"subtypes":[]}` regardless of what exists — that bare-call behavior is almost certainly what the original 2026-07-18 finding actually hit. Always pass `leaf_type` when calling this endpoint.
- **2026-07-19 · The full-field-replay requirement on `schemas.custom.set` also applies to subtype (`custom_type_fragment`) fragments, not just stock `tenant_fragment`s.** A partial replay (new field only, omitting an existing field) on an already-customized subtype fragment 400s the same way stock tenant fragments do; a full replay (all existing fields + new field) succeeds. Broaden the "already-customized stock leaf type" framing below to "any already-customized fragment, tenant or subtype."
- **2026-07-19 · `deleted_fields` on `schemas.custom.set` confirmed working live** (previously documented but never live-tested). Sending `fields` (the remaining field list) plus `deleted_fields:["<name>"]` → `HTTP 201`, and `schemas.aggregated.get` immediately shows the field gone.
- **2026-07-19 · `link-types.custom.update` accepts both `deprecated` and `is_deprecated` as input field aliases.** Both were tested independently (toggled true→false→unset-by-default) and both work; the response always echoes the field back as `is_deprecated` regardless of which alias was sent. Not a documentation bug — either works as input.
- **2026-07-19 · `link-types.custom.list` did not reflect 2 freshly created custom link types even 15+ minutes later, while `link-types.custom.get` by id resolved them correctly every time.** A pre-existing link type (created earlier by a system snap-in) does appear in `.list`. This is a genuine list-vs-get staleness gap, distinct from (but structurally similar to) the `schemas.subtypes.list` filter-requirement finding above. Verify a newly created custom link type via `.get` by id, not `.list`. `.list` (and the equivalent `GET` with query params) also returns an undocumented extra `reverse_result` key alongside `result`.
- **2026-07-19 · `works.update` custom-field validation error has a specific shape worth citing verbatim.** Sending `custom_fields` without `custom_schema_spec` returns `HTTP 400 {"type":"customization_validation_error","reason":"field <name> is not in selected schemas","subtype":"field_not_in_schema"}` — more specific than a generic Bad Request; useful for error-matching in scripts.
- **2026-07-19 · Stage-diagram attachment to a subtype/custom leaf type — see `skills/2-stage-lifecycle-customization` Field notes for the full correction.** It DOES work (`stage_diagram` as a bare string on `schemas.custom.set`, or `is_default:true` at leaf-type level) — this repo's Custom_Objects_and_Links_API.md §1 Step 3 is now corrected to match. Enforcement is confirmed real for custom objects, unconfirmed (tested and found absent) for stock-type subtypes.
- **2026-07-18 · `schemas.custom.delete` does not exist (route 404).** Custom fragments cannot be hard-deleted via the public API. Combined with the versioned-create behavior above, this makes accidental fragment proliferation the primary risk of running `.set` blindly.
- **2026-07-18 · `schemas.custom.set` auto-creates a workflow.** Creating a custom leaf type triggers DevRev to auto-generate a `Custom Object Reporting for <leaf_type>` workflow (verified: `workflow/11` appeared immediately after creating `regression_test`). Any regression/cleanup routine that lists workflows after schema changes must be aware — that workflow is deletable via `POST /internal/workflows.delete` and is safe to remove if the parent leaf type is gone.
- **2026-07-18 · `objects.bulk-upgrade` CONFIRMED to exist — closes prior open question.** It lives ONLY at `/internal/objects.bulk-upgrade`; the public-root path `POST /objects.bulk-upgrade` returns HTTP 404 route-not-found (which is almost certainly why earlier passes flagged it "not in the public API catalog" — they were likely checking the root path). Verified: `POST /internal/objects.bulk-upgrade` with `{"type":"ticket"}` → HTTP 200 `{"id":"don:core:...:job/3"}`. Then `GET /jobs.get?id=<job_don>` shows `job_category:"bulk_upgrade"`, `state:"completed"`, `progress:100`, `title:"Bulk Upgrade"`, and a `metadata_list` entry `{"key":"Count","value":"<N>"}` with the count of records upgraded. Affects ALL records of the given `type` (and optional `subtype`) org-wide — treat as destructive/confirm-first, same as before, but it is real and works.
- **2026-07-18 · `schemas.custom.set` on a leaf type that already has a `tenant_fragment` requires the COMPLETE existing field list to be replayed, not just the new field(s).** Verified live against stock `ticket`/`issue`: sending only the new field (or the new field plus one existing field, i.e. a partial replay) returns generic HTTP 400 `bad_request` with no `field_name` — no diagnostic. Only a `fields` array containing every existing field verbatim plus the new one succeeded. By contrast, a leaf type with NO prior tenant_fragment (e.g. stock `account`, never customized) accepted a minimal `fields` array with just the new field. Always `schemas.custom.get` the current fragment first and replay its `fields` array in full when adding to an already-customized stock type. Separately: `schemas.custom.set` also requires a top-level `description` string — omitting it returns `missing_required_field: description` even though some reference examples don't show it.
- **2026-07-18 · `schemas.subtypes.list` does not reflect a subtype just created via `schemas.custom.set` (`type: "custom_type_fragment"` + `subtype` field).** Returned `{"subtypes":[]}` immediately after a subtype (`regression_test_bug` on `issue`) was successfully created and confirmed via `schemas.aggregated.get` (which correctly showed the merged `ctype__impacted_environments` field) and via a real `works.create` using that subtype. Root cause not identified — possibly a different creation path or indexing delay. Use `schemas.aggregated.get` with `custom_schema_spec: {"subtype": "<name>"}`, not `schemas.subtypes.list`, to confirm a subtype landed.
- **2026-07-23 · Confirmed (from DevRev's own object-customization/custom-objects guides, not yet independently live-tested in this repo): custom leaf types support subtypes via the exact same `custom_type_fragment` mechanism as stock leaf types.** Add `is_custom_leaf_type: true` to the subtype fragment (matching the parent leaf type's definition) and the subtype inherits every tenant field, adding its own `ctype__` fields on top — see Playbook 3 step 2 and `references/Custom_Objects_and_Links_API.md` §1 Step 5. Two claims from that same source material conflict with facts already live-verified in this repo and should NOT be trusted over the live findings: (1) it shows attaching a stage diagram to a subtype via `stage_diagram_id` — this repo confirmed live (2026-07-19 row below) that `stage_diagram_id` is rejected and the working field is `stage_diagram` (bare string). (2) it claims custom link types can restrict by `subtype` **and** `leaf_only` — only `subtype` is confirmed to exist here (`skills/0-solution-architecture/references/api-cookbook.md` §5 already flags `leaf_only` as unconfirmed/likely nonexistent). Also net-new, not yet live-tested: `schemas.subtypes.prepare-update` reportedly returns `ABSENT_IN_NEW`/`INCOMPATIBLE_TYPE` conflict codes when previewing a subtype field change, and subtype-scoped field access uses `target_subtype`/`include_all_subtypes` role options (UI-only, Settings > Roles).
- **2026-07-18 · Playbook 1 (new custom object) cannot be fully exercised via the public API alone.** `schemas.custom.set` (schema creation) succeeds, but the immediately-following `custom-objects.create` reliably 403s (zero-access-by-default, per the finding above) and there is no API-level role-grant endpoint anywhere in this skill's or skill 8's reference docs — the grant is UI-only (Settings > Object customization + Settings > User Management > Roles). Any live regression test of this playbook should stop after schema creation/verification and pivot to Playbook 3 (subtypes) or Playbook 4 (custom link types) to exercise create+verify+cleanup flows, since those aren't blocked by the zero-access restriction.
