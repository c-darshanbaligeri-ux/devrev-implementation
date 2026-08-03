# Stock object modification & schema management — DevRev API

How to inspect and safely modify DevRev's built-in ("stock") objects — issue,
ticket, account, contact, opportunity, part — and manage schema fragments,
subtypes, field overrides, and record upgrades.

| Field | Detail |
| --- | --- |
| Base URL | https://api.devrev.ai |
| Auth | `Authorization: Bearer <TOKEN>` |
| Status | Beta |

---

## 1. The additive model

DevRev customization is additive: you never mutate a stock field's underlying
definition. Instead you layer fragments on top:

- Stock schema — DevRev's built-in fields for a leaf type. Read-only structure;
  inspect it but don't redefine it.
- Tenant fragment (`tnt__` prefix) — custom fields added to every record of a
  leaf type, org-wide.
- Custom-type fragment (`ctype__` prefix) — fields specific to a subtype.
- Field override — a controlled change to how a stock field behaves/appears
  (e.g. renaming the display name of `priority`/`severity`, restricting allowed
  values) without altering the stock field itself.
- Aggregated schema — the merged view of stock + tenant + subtype fragments as
  applied to a record.

---

## 2. Inspect stock schemas (read-only)

Always read the stock schema before overriding a field, so you know the exact
field name and type.

```bash
# Get the stock schema fragment for a leaf type
curl -X POST 'https://api.devrev.ai/schemas.stock.get' \
-H 'Authorization: Bearer <TOKEN>' \
-H 'Content-Type: application/json' \
-d '{ "leaf_type": "ticket" }'

# List all stock schema fragments
curl -X POST 'https://api.devrev.ai/schemas.stock.list' \
-H 'Authorization: Bearer <TOKEN>' \
-d '{}'
```

Both require no scope.

---

## 3. See the merged (aggregated) schema

`schemas.aggregated.get` returns the full field set that actually applies to a
record — stock plus every custom fragment. Use it to verify your customization
landed.

```bash
curl -X POST 'https://api.devrev.ai/schemas.aggregated.get' \
-H 'Authorization: Bearer <TOKEN>' \
-d '{
  "leaf_type": "ticket",
  "custom_schema_spec": { "tenant_fragment": true, "subtype": "bug" }
}'
```

No scope required.

---

## 4. Modify a stock object — add fields & overrides

All modifications go through `schemas.custom.set` (scope:
`custom_type_fragment:write`). It creates or updates a fragment.

### 4a. Add a tenant field to every record of a stock type

```bash
curl -X POST 'https://api.devrev.ai/schemas.custom.set' \
-H 'Authorization: Bearer <TOKEN>' \
-d '{
  "type": "tenant_fragment",
  "leaf_type": "ticket",
  "fields": [
    { "name": "escalation_reason", "field_type": "rich_text",
      "ui": { "display_name": "Escalation Reason" } }
  ]
}'
```

The field is referenced as `tnt__escalation_reason` on records.

### 4b. Override a stock field (e.g. rename priority/severity, restrict values)

Stock field overrides let you tailor a built-in field's presentation and
constraints. Include the override in the fragment for the leaf type/subtype:

```bash
curl -X POST 'https://api.devrev.ai/schemas.custom.set' \
-H 'Authorization: Bearer <TOKEN>' \
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

Overrides change display/behaviour only; the stock field itself is preserved so
platform features that depend on it keep working.

### Supported field types
`int`, `double`, `bool`, `tokens`, `text`, `rich_text`, `enum`,
`uenum` (advanced enum with stable numeric IDs), `timestamp`, `date`, `id`,
plus array/list variants of each.

`uenum` stores a numeric `id` + `ordinal` per option instead of a bare string,
so you can relabel or reorder options later without touching stored data. Each
option: `{ id, label, ordinal, deprecated? }`; `default_value` references an
option's `id`, not its label. Use `uenum[]` for multi-select. **Open
discrepancy, not yet resolved**: `skills/0-solution-architecture/references/api-cookbook.md`
§6 claims `uenum` is "used for stock overrides but not supported for
user-defined custom fields — use `enum`", which contradicts this file's own
Playbook 3 worked example and SKILL.md's field-type list, both of which show
`uenum` as a plain supported custom field type. Neither claim has been
live-tested against `schemas.custom.set`; try a real `uenum` custom field
before trusting either statement.

### Removing fields
Fragments are immutable and auto-versioned. To drop a field, send the full field
list and name the removals in `deleted_fields`.

### UI hints per field (`ui` object)

Set under a field's `ui` object in `schemas.custom.set` — **not independently
live-tested in this repo**, sourced from DevRev's docs:

| Hint | Purpose |
| --- | --- |
| `display_name` | Label shown in the UI (used throughout this doc's examples) |
| `is_hidden` | Hide the field from the UI |
| `placeholder` | Placeholder text |
| `is_sortable` | Allow sorting (requires the field's top-level `is_filterable: true`) |
| `is_groupable` | Allow grouping (requires `is_filterable: true`) |
| `order` | Field order in the side panel |
| `is_read_only` | Not editable in UI after creation (the API can still write it) |
| `group_name` | Group fields under a titled section |
| `unit` | Display unit (e.g. days, kg) |

`is_filterable` itself is a top-level field property (sibling of `field_type`), not nested under `ui`.

---

## 5. Manage subtypes

- Add a subtype: `schemas.custom.set` with `type: custom_type_fragment`,
  `leaf_type`, `subtype`, `subtype_display_name`, and its `ctype__` fields.
- Prepare a subtype update: `schemas.subtypes.prepare-update` (scope:
  `custom_type_fragment:write`) validates and stages a subtype change before you
  apply it — useful for large field/stage remaps.
- List subtypes: `schemas.subtypes.list`.

---

## 6. Read & manage custom fragments

| Endpoint | Scope | Purpose |
| --- | --- | --- |
| `schemas.custom.set` | `custom_type_fragment:write` | Create/update a fragment, subtype, tenant field, override |
| `schemas.custom.get` | none | Get a custom fragment |
| `schemas.custom.list` | none | List custom fragments. **Pass `is_custom_leaf_type: true` to see custom-leaf-type fragments** — a bare `{}` call returns stock-object fragments ONLY, and a `leaf_type` filter *alone* returns 0 rows (verified live 2026-08-04). There is no `type` filter (`{"type":"tenant_fragment"}` → 400 `invalid_field`). |
| `schemas.stock.get` / `.list` | none | Inspect stock fields |
| `schemas.aggregated.get` | none | Merged stock + custom view. Fields come back under **`custom_fields`** and **`stock_fields`** — there is **no `fields` key**, so reading `fields` silently reports zero fields (verified live 2026-08-04). |
| `schemas.subtypes.prepare-update` | `custom_type_fragment:write` | Stage a subtype change |

---

## 7. Upgrade existing records after a schema change

When you evolve a fragment, records created under the old version don't
automatically reflect the change; they keep referencing the older fragment until
upgraded.

> Accuracy note: a bulk-upgrade operation exists in DevRev's tooling, but
> `objects.bulk-upgrade` is **not listed in the public API-to-scope reference**.
> Treat it as unverified for public use — confirm the current endpoint name and
> availability in the official API reference before relying on it. In many cases
> re-saving the record (via the object's own `*.update`) with the current
> `custom_schema_spec` is the supported path to pick up the latest fragment.

```bash
# Unverified for public use — confirm before running:
curl -X POST 'https://api.devrev.ai/objects.bulk-upgrade' \
-H 'Authorization: Bearer <TOKEN>' \
-d '{ "leaf_type": "ticket" }'
```

---

## 8. Common pitfalls

- Redefining a stock field instead of overriding it — use
  `stock_field_overrides`, never try to recreate the built-in field.
- Wrong namespace prefix — `tnt__` for tenant fields, `ctype__` for subtype
  fields. A mismatched prefix silently fails to match, with no error.
- Old values persisting after a change — records still point at the old fragment;
  re-save them via the object's `*.update` with the current `custom_schema_spec`
  (or a bulk-upgrade operation if confirmed available — see §7 caveat).
- Assuming aggregated == stock — always check `schemas.aggregated.get` to see
  what truly applies to a record before debugging a "missing" field.
