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

Creates a custom leaf type. **`.set` is a versioned create, not an update** — verified live 2026-07-18: calling `.set` twice with the same `leaf_type` produces two fragments (`tenant_fragment/N`, `tenant_fragment/N+1`), the older one is NOT superseded, and there is no delete endpoint. "Full replacement" means fields *within a single fragment*, not "supersede the previous fragment". List first to check if the leaf type exists before calling `.set` at all. Key params: `type: "tenant_fragment"` + `is_custom_leaf_type: true` + `id_prefix` (uppercase letters only, 2–10 chars) + `leaf_type` (lowercase letters + underscores, no digits) for a new custom object; `type: "custom_type_fragment"` + `subtype` for a subtype on a stock object.

→ Exact payloads (custom object + subtype variants): `../../1-object-schema-customization/references/Stock_Object_Modification_and_Schemas_API.md`.

---

## 2. Custom object instance — `custom-objects.create`

Creates an instance of a custom leaf type; requires `custom_schema_spec`; `unique_key` is an optional idempotency key. Full CRUD: `.get/.list/.update/.delete/.count`. **Live-verified 2026-07-19**: `.list`/`.count` require a `leaf_type` filter — omitting it 400s `missing_required_field`. `.delete` is confirmed genuinely working (`HTTP 200 {}`, then `.get` 404s), not a documentation-only claim.

→ Exact create/update payload and `custom_schema_spec` keys: `../../1-object-schema-customization/references/Custom_Objects_and_Links_API.md`. (That file does not document a `.list` filter-syntax table or an `id`/`display_id` response-shape breakdown beyond what's shown inline in its examples — don't expect more detail there than the create/update flow.)

---

## 3. States and stages

`states.custom.create` (unique `ordinal` per org); `stages.custom.create` (requires `name`, `ordinal`, `state`). Stages are org-scoped — any object type can reference them.

→ Exact payloads and scopes: `../../2-stage-lifecycle-customization/references/Stages_States_and_StageDiagrams_API.md`.

---

## 4. Stage diagram — `stage-diagrams.create`

Defines stages + transitions for a leaf type. Rules: exactly one `is_start: true` node; all stages reachable from start; a path to a terminal/closed state must exist; `is_default`/`leaf_type` immutable after creation. **Live-verified 2026-07-18, still accurate: a listed stage cannot be deleted or deprecated at all** — `is_deprecated: true` on a stage node is rejected (`HTTP 400`) at both create and update, on start/middle/terminal stages alike; there is no known working retirement mechanism anywhere in a diagram via the public API. Design stage diagrams conservatively — every stage added is effectively permanent for that diagram's lifetime. **Subtype/custom-leaf-type attachment, live-verified 2026-07-19**: DOES work — via `stage_diagram` (a bare DON-id string, on `schemas.custom.set`) for subtype-level, or `is_default: true` (at `stage-diagrams.create` time) for leaf-type-level. Enforcement differs by object class: confirmed real for custom objects (`custom-objects.update` rejects invalid transitions); NOT confirmed for stock-type subtypes (`works.update` showed no enforcement in testing) — don't promise a caller a subtype's diagram will gate `works.update`.

→ Exact payload (note: transition target field is `target_stage_id`, not `target_id`), subtype-linkage mechanics, and the custom-object stage-wiring sequence: `../../2-stage-lifecycle-customization/references/Stages_States_and_StageDiagrams_API.md`.

---

## 5. Custom link type and link instance

`link-types.custom.create` (`name`, `source_types[]`, `target_types[]`, `forward_name`, `backward_name`; max 30 each side; cannot be deleted, only deprecated — **live-verified 2026-07-19: `link-types.custom.update` accepts either `deprecated` or `is_deprecated` as the input field**, both work, response always echoes `is_deprecated`). `links.create` for instances. Stock `link_type` enum: `is_parent_of, is_dependent_on, is_related_to, is_duplicate_of, is_merged_into, is_follow_up_of, is_part_of, serves, custom_link`.

→ Exact payloads and the `is_custom_leaf_type` descriptor option: `../../1-object-schema-customization/references/Custom_Objects_and_Links_API.md`. (That file does not document a `leaf_only` descriptor option — no such field exists there; don't expect it.) **Also live-verified 2026-07-19**: `link-types.custom.list` did not reflect 2 freshly created link types even 15+ minutes later — verify a new one via `.get` by id, not `.list`.

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
