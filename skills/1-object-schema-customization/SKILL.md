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
- **Add a stage field** (lifecycle) — create states, stages, and a stage diagram for the custom leaf type (see `skills/2-stage-lifecycle-customization`), then attach the diagram to the schema via `stage_diagram_id` on `schemas.custom.set`. Records can then transition via `custom-objects.update` with `stage`.
- **Add a tags field** — model it as a custom field (not a native `tags` property). Use `field_type: "array"` with `base_type: "id"` and `id_type: [ "tag" ]` to store references to real DevRev tags created with `tags.create`.
- **Add a part field** (reference a product/capability/feature) — use `field_type: "id"` with `id_type: [ "product", "capability", "feature" ]`. Pass the part DON in `custom_fields`.

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

4. **Verify** — check the merged view with `schemas.aggregated.get`:

   ```bash
   curl -X POST 'https://api.devrev.ai/schemas.aggregated.get' \
   -H 'Authorization: Bearer $DEVREV_TOKEN' \
   -d '{
     "leaf_type": "ticket",
     "custom_schema_spec": { "tenant_fragment": true }
   }'
   ```

**Supported field types** (§4): `int`, `double`, `bool`, `tokens`, `text`, `rich_text`, `enum`, `uenum`, `timestamp`, `date`, `id`, plus array/list variants.

**After schema changes**: fragments are versioned. Existing records reference the old version until upgraded. Re-save affected records via their `*.update` with the current `custom_schema_spec` to pick up the latest fragment. (`objects.bulk-upgrade` exists but is not in the public API-to-scope reference — verify before using; prefer re-saving via `*.update`.)

### Playbook 3 — Create and manage subtypes

**Reference**: `references/Stock_Object_Modification_and_Schemas_API.md` §5 (Manage subtypes); worked example: `../3-data-upload-and-org-build/references/DevRev_Building_Org_Using_API_v1.md` Phase 1 §1.2 (Add a subtype with custom fields).

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

3. **Verify** — `schemas.aggregated.get` with `custom_schema_spec: { "tenant_fragment": true, "subtype": "bug" }` shows the merged field set; `schemas.subtypes.list` lists all subtypes.

4. **Attach a stage diagram** (optional) — for lifecycle control, create a stage diagram (see `skills/2-stage-lifecycle-customization`) and reference it from the subtype fragment via `stage_diagram_id` on `schemas.custom.set`.

5. **Prepare a subtype update** (for large changes) — `schemas.subtypes.prepare-update` (scope: `custom_type_fragment:write`) validates and stages the change before you apply it.

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
| `references/Custom_Objects_and_Links_API.md` | Defining custom object types (§1); creating custom link types (§3); linking work items and custom objects (§4); custom object stage/tags/part fields (§1 optional enhancements) |
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
- `objects.bulk-upgrade` (if confirmed available — see §7 caveat; prefer re-saving via `*.update`)

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
- **2026-07-18 · `custom-objects.create` returns HTTP 403 Forbidden immediately after schema creation.** No role has been granted to the new leaf type by default. This matches the CLAUDE.md rule "Custom objects: start with zero access by default. Grant roles explicitly after creation." — verified live. If a user hits this, the fix is to grant a role in DevRev Settings; don't retry the API call.
- **2026-07-18 · `schemas.custom.delete` does not exist (route 404).** Custom fragments cannot be hard-deleted via the public API. Combined with the versioned-create behavior above, this makes accidental fragment proliferation the primary risk of running `.set` blindly.
