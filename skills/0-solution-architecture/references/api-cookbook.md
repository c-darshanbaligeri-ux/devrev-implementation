# API Cookbook: Worked Payloads for Provisioning

Concrete, copy-ready request shapes for the customization surface. Use these when a blueprint's build sequence needs exact API calls — provisioning custom objects, stages, stage diagrams, links, and instances. Base URL `https://api.devrev.ai` (some flows use the `/internal/` variant). All calls need `Authorization: Bearer <TOKEN>`.

> Field-name variance exists across DevRev docs (e.g. stage-diagram transition target is `target_id` in the data-model doc but `target_stage_id` in working payloads — use `target_stage_id`). These payloads reflect the working examples.

## Table of contents
1. Custom object schema
2. Custom object instance
3. States and stages
4. Stage diagram
5. Custom link type and link instance
6. Field descriptor reference
7. Dependent/conditional fields
8. Read/utility endpoints and scopes

---

## 1. Custom object schema — `schemas.custom.set`

Creates (and updates) a custom leaf type. **This is a full replacement** — always `schemas.custom.get`/`list` first and resend existing fields, or dropped fields are removed. Key params: `type: "tenant_fragment"` + `is_custom_leaf_type: true` + `id_prefix` for a new custom object; `type: "custom_type_fragment"` + `subtype` for a subtype on a stock object.

→ Exact payloads (custom object + subtype variants): `../../1-object-schema-customization/references/Stock_Object_Modification_and_Schemas_API.md`.

---

## 2. Custom object instance — `custom-objects.create`

Creates an instance of a custom leaf type; requires `custom_schema_spec`; `unique_key` is an optional idempotency key. Full CRUD: `.get/.list/.update/.delete/.count`.

→ Exact payload, `custom_schema_spec` keys, `.list` filter syntax, response shape (`id`/`display_id`): `../../1-object-schema-customization/references/Custom_Objects_and_Links_API.md`.

---

## 3. States and stages

`states.custom.create` (unique `ordinal` per org); `stages.custom.create` (requires `name`, `ordinal`, `state`). Stages are org-scoped — any object type can reference them.

→ Exact payloads and scopes: `../../2-stage-lifecycle-customization/references/Stages_States_and_StageDiagrams_API.md`.

---

## 4. Stage diagram — `stage-diagrams.create`

Defines stages + transitions for a leaf type. Rules: exactly one `is_start: true` node; a listed stage can't be deleted (mark `is_deprecated: true`); all non-deprecated stages reachable from start; a path to a terminal/closed state must exist; `is_default`/`leaf_type` immutable after creation.

→ Exact payload (note: transition target field is `target_stage_id`, not `target_id`), subtype-linkage mechanics, and the custom-object stage-wiring sequence: `../../2-stage-lifecycle-customization/references/Stages_States_and_StageDiagrams_API.md`.

---

## 5. Custom link type and link instance

`link-types.custom.create` (`name`, `source_types[]`, `target_types[]`, `forward_name`, `backward_name`; max 30 each side; cannot be deleted, only deprecated). `links.create` for instances. Stock `link_type` enum: `is_parent_of, is_dependent_on, is_related_to, is_duplicate_of, is_merged_into, is_follow_up_of, is_part_of, serves, custom_link`.

→ Exact payloads, descriptor options (`leaf_only`, `is_custom_leaf_type`), identity/idempotency rules: `../../1-object-schema-customization/references/Custom_Objects_and_Links_API.md`.

---

## 6. Field descriptor reference

Per-field attributes: `name` (immutable), `field_type`, `id_type`/`devrev_id_type`, `allowed_values`, `is_required`, `is_filterable` (cannot change after creation), `default_value`, `is_pii`, `is_immutable`, `base_type` (arrays), `ui{}` hints. `uenum` is used for stock overrides but **not supported for user-defined custom fields** — use `enum`.

→ Full field-type table, array-form payload, and UI-hint reference: `../../1-object-schema-customization/references/Stock_Object_Modification_and_Schemas_API.md`.

---

## 7. Dependent / conditional fields

A `conditions[]` array on a fragment; each = `expression` (boolean, `== != && ||`) + `effects[]` (`require`/`show`/`allowed_values`). Conditions may only be specified **on** custom fields; effects may target any field. Stages/enums compare by **ID**, never display name.

→ Exact payload (incl. the cascading-enum example): `../../1-object-schema-customization/references/Stock_Object_Modification_and_Schemas_API.md`.

---

## 8. Read/utility endpoints and scopes

Customization endpoints span `schemas.custom.*`, `schemas.stock.*`, `schemas.aggregated.get`, `schemas.subtypes.prepare-update`, `stages.custom.*`, `states.custom.*`, `stage-diagrams.*`, `custom-objects.*`, `link-types.custom.*`.

→ The authoritative, whole-platform endpoint + scope catalog (not just customization): `../../8-devrev-api/references/00_API_Catalog.md`. For the stock-field list per object type, query `schemas.stock.get`/`schemas.aggregated.get` live rather than relying on prose.

### Field namespacing recap
Custom field values live under `custom_fields` with prefixes: tenant `tnt__<name>`, subtype `ctype__<name>`, app `app_<appname>__<name>`, system-protected `sys__`/`ctype_sys__`.
