# Custom objects & links — DevRev API

Full lifecycle for net-new object types (e.g. Campaign, Asset) and for
relationships: built-in links, custom link types, and the link instances that
connect work items, parts, identity objects, and custom objects.

| Field | Detail |
| --- | --- |
| Base URL | https://api.devrev.ai |
| Auth | `Authorization: Bearer <TOKEN>` |
| Status | Beta |

---

## 1. Custom objects — end to end

A custom object is a brand-new leaf type you define, then create records of.

### Step 1 — define the schema (`schemas.custom.set`, scope `custom_type_fragment:write`)

Set `is_custom_leaf_type: true` and an `id_prefix` to distinguish it from stock
objects.

```bash
curl -X POST 'https://api.devrev.ai/schemas.custom.set' \
-H 'Authorization: Bearer <TOKEN>' \
-H 'Content-Type: application/json' \
-d '{
  "type": "tenant_fragment",
  "description": "Attributes for Campaign",
  "leaf_type": "campaign",
  "leaf_type_display_name": "Campaign",
  "is_custom_leaf_type": true,
  "id_prefix": "CAMP",
  "fields": [
    { "name": "start_date", "field_type": "date",
      "description": "Start date of the campaign" },
    { "name": "budget", "field_type": "int",
      "description": "Budget allocated for the campaign" },
    { "name": "target_audience", "field_type": "enum",
      "allowed_values": [ "Professionals", "Students" ] }
  ]
}'
```

### Step 2 — create a record (`custom-objects.create`, scope `custom_type_fragment:write`)

```bash
curl -X POST 'https://api.devrev.ai/custom-objects.create' \
-H 'Authorization: Bearer <TOKEN>' \
-d '{
  "leaf_type": "campaign",
  "custom_schema_spec": { "tenant_fragment": true },
  "unique_key": "CAMP-1",
  "custom_fields": { "tnt__budget": 10000 }
}'
```

- `unique_key` gives idempotency — repeating the call with the same key won't
  create a duplicate.
- `custom_schema_spec` must name the schema for every custom field you send;
  omitting it returns a Bad Request. For human-facing surfaces, set
  `tenant_fragment: true` and `validate_required_fields: true`.
- `stage` (optional) sets the custom object's lifecycle stage (see the stages doc).

### Other custom-object operations

| Endpoint | Scope | Purpose |
| --- | --- | --- |
| `custom-objects.create` | `custom_type_fragment:write` | Create a record |
| `custom-objects.update` | `custom_type_fragment:write` | Update fields/stage/description |
| `custom-objects.delete` | `custom_type_fragment:write` | Delete a record — **confirmed live 2026-07-19**: genuinely works (`HTTP 200 {}`, then `.get` 404s), not a stub |
| `custom-objects.get` | none | Fetch one record |
| `custom-objects.list` | none | List records — **live-verified 2026-07-19: `leaf_type` is a required filter**, omitting it returns `HTTP 400 missing_required_field field_name:"leaf_type"` |
| `custom-objects.count` | none | Count records — same required `leaf_type` filter as `.list` |

> Access note: custom objects start with **zero access**, even for admins. Grant
> object- and field-level roles in Settings > Object customization and
> Settings > User Management > Roles before they appear or become editable.
> If list view isn't supported for a custom object, enable search on it.

**`.list`/`.count` filter syntax** — **not independently live-tested in this
repo**, sourced from DevRev's docs (fills a gap the solution-architecture
skill's `api-cookbook.md` §2 previously flagged as undocumented here — that
pointer note is now stale and should be corrected once this is confirmed
live). Filter on a custom field with a 3-element array
`[operator, path, value]`, where the path is prefixed `$custom_fields.`:

```json
{
  "leaf_type": "campaign",
  "filter": [ "eq", "$custom_fields.tnt__target_audience", "Professionals" ]
}
```

If the list view isn't supported for a custom object in the UI, the search
syntax over custom objects requires its own `leaf_type` filter term, and
subtype-specific field filters require a `subtype` term alongside it, e.g.
`leaf_type:campaign subtype:social_media ctype__social_media_platform:Facebook`.

### Step 3 — give the custom object a stage field (lifecycle)

A custom object has no stage until you attach a stage diagram to its leaf type.
Once attached, every record carries a `stage`, and `custom-objects.create/update`
accept a `stage` value that must be a valid stage in that diagram.

1. Create the states, stages, and a stage diagram for the custom leaf type. On
   `stage-diagrams.create`, set `is_custom_leaf_type: true` and `leaf_type` to
   your custom type. (Full detail in `Stages_States_and_StageDiagrams_API.md`.)

   ```bash
   curl -X POST 'https://api.devrev.ai/stage-diagrams.create' \
   -H 'Authorization: Bearer <TOKEN>' \
   -d '{
     "leaf_type": "campaign",
     "is_custom_leaf_type": true,
     "name": "Campaign lifecycle",
     "stages": [
       { "is_start": true, "stage_id": "<PLANNED_STAGE_ID>",
         "transitions": [ { "target_stage_id": "<ACTIVE_STAGE_ID>" } ] },
       { "stage_id": "<ACTIVE_STAGE_ID>",
         "transitions": [ { "target_stage_id": "<CLOSED_STAGE_ID>" } ] },
       { "stage_id": "<CLOSED_STAGE_ID>", "transitions": [] }
     ]
   }'
   ```

2. Attach the diagram. **Live-verified 2026-07-19**: the write field is `stage_diagram` (a bare
   DON-id **string**), not `stage_diagram_id` — that name is rejected (`invalid_field`); a nested
   `{"stage_diagram":{"id":...}}` object is also rejected. Only a bare string succeeds. (For a
   leaf type with no existing default diagram, `is_default: true` at `stage-diagrams.create` time
   is an alternative, leaf-type-scoped path — see `skills/2-stage-lifecycle-customization/references/Stages_States_and_StageDiagrams_API.md` §5.)

   ```bash
   curl -X POST 'https://api.devrev.ai/schemas.custom.set' \
   -H 'Authorization: Bearer <TOKEN>' \
   -d '{
     "type": "tenant_fragment",
     "leaf_type": "campaign",
     "is_custom_leaf_type": true,
     "description": "Attributes for Campaign",
     "stage_diagram": "<STAGE_DIAGRAM_ID>",
     "fields": []
   }'
   ```

   The read-side key (`schemas.aggregated.get`) is still named `stage_diagram_id` — only the
   write-side field on `schemas.custom.set` is `stage_diagram`. If a `tenant_fragment` already
   exists for this leaf type, replay its complete `fields` array (see §5 Common pitfalls) — a
   partial replay 400s.
   **Enforcement note**: this was confirmed to gate `custom-objects.update` correctly (non-adjacent
   stage transitions rejected). The same attachment mechanism on a **stock-type subtype** did
   *not* gate `works.update` in testing — see the stage-lifecycle skill's Field notes.

3. Set the stage on a record:

   ```bash
   curl -X POST 'https://api.devrev.ai/custom-objects.update' \
   -H 'Authorization: Bearer <TOKEN>' \
   -d '{ "id": "<CAMPAIGN_OBJECT_ID>", "stage": "<ACTIVE_STAGE_ID>" }'
   ```

- Use `custom-objects.update` with `stage` to transition; the value must be a
  stage the diagram allows from the current one.
- You can require fields at a given stage with dependent-field `conditions` on the
  fragment (see the stages doc §6).

### Step 3b — give the custom object a tags field

Tags behave differently from other fields, so read this carefully.

- On **stock objects** (works, parts, accounts, contacts) tags are a native
  property — you pass `tags` (an array of `set-tag-with-value`) directly on
  create/update, and no schema change is needed. Example on a ticket:

  ```bash
  curl -X POST 'https://api.devrev.ai/works.update' \
  -H 'Authorization: Bearer <TOKEN>' \
  -d '{ "id": "<TICKET_ID>",
        "tags": [ { "tag": "<TAG_ID>" } ] }'
  ```

- On a **custom object**, the create/update payload does not expose that native
  `tags` property. To get a "tags field" on a custom object, model it as a custom
  field in the schema. Two options:

  1. A field of `field_type: "id"` (or an array of ids) restricted to the tag
     type — stores references to real DevRev tags:

     ```bash
     curl -X POST 'https://api.devrev.ai/schemas.custom.set' \
     -H 'Authorization: Bearer <TOKEN>' \
     -d '{
       "type": "tenant_fragment",
       "leaf_type": "campaign",
       "is_custom_leaf_type": true,
       "fields": [
         {
           "name": "labels",
           "field_type": "array",
           "base_type": "id",
           "id_type": [ "tag" ],
           "ui": { "display_name": "Tags" }
         }
       ]
     }'
     ```

     Create the tags first with `tags.create`, then set them on a record:

     ```bash
     curl -X POST 'https://api.devrev.ai/custom-objects.update' \
     -H 'Authorization: Bearer <TOKEN>' \
     -d '{
       "id": "<CAMPAIGN_OBJECT_ID>",
       "custom_schema_spec": { "tenant_fragment": true },
       "custom_fields": { "tnt__labels": [ "<TAG_ID_1>", "<TAG_ID_2>" ] }
     }'
     ```

  2. If you only need free-form labels (not links to managed tag objects), use an
     `enum`/`array of enum` field with `allowed_values`, or a `tokens` field.

- Note the array-field shape: use `field_type: "array"` with `base_type` set to
  the element type (`id`, `enum`, etc.), matching DevRev's documented pattern for
  multi-value fields (e.g. `id_type: [ "custom_object.campaign" ]` when
  referencing custom objects, `[ "tag" ]` for tags).

### Step 4 — give the custom object a part field (reference a part)

To store a product/capability/feature (a part) on a custom object, add a custom
field of type `id` restricted to part leaf types. The field then holds a part DON.

```bash
curl -X POST 'https://api.devrev.ai/schemas.custom.set' \
-H 'Authorization: Bearer <TOKEN>' \
-d '{
  "type": "tenant_fragment",
  "leaf_type": "campaign",
  "is_custom_leaf_type": true,
  "fields": [
    {
      "name": "related_product",
      "field_type": "id",
      "id_type": [ "product", "capability", "feature" ],
      "ui": { "display_name": "Related Product" }
    }
  ]
}'
```

Set it on a record by passing the part DON in `custom_fields`:

```bash
curl -X POST 'https://api.devrev.ai/custom-objects.update' \
-H 'Authorization: Bearer <TOKEN>' \
-d '{
  "id": "<CAMPAIGN_OBJECT_ID>",
  "custom_schema_spec": { "tenant_fragment": true },
  "custom_fields": { "tnt__related_product": "<PART_ID>" }
}'
```

- `field_type: "id"` with `id_type` limits which object types the field accepts;
  list the part types you want (`product`, `capability`, `feature`, `enhancement`).
- For multiple parts on one record, use the array shape:
  `"field_type": "array", "base_type": "id", "id_type": [ "product", ... ]`, and
  pass an array of part DONs in `custom_fields`.
- The stored value is a DON — never a display ID like `PROD-12`.
- Alternative to a field: create a **link** between the custom object and the part
  (built-in `is_related_to`/`serves` or a custom link type — see §2 and §3).
  Use a field when the part is a first-class attribute of the record; use a link
  when it's a looser relationship you want to traverse on the Trail.

### Step 5 — give the custom object subtypes

**Yes — custom leaf types support subtypes exactly the same way stock leaf
types do.** A subtype is a `custom_type_fragment` scoped to a `leaf_type` +
`subtype` name; it works identically whether that `leaf_type` is a stock object
(`issue`, `ticket`) or one you defined yourself with `is_custom_leaf_type: true`
in Step 1. The subtype **inherits every field of the parent leaf type** (its
tenant fragment) and adds its own fields on top, prefixed `ctype__` on records.

Continuing the campaign example: define a `social_media` subtype and an
`email_marketing` subtype, each with fields specific to that flavor of campaign.

```bash
curl -X POST 'https://api.devrev.ai/schemas.custom.set' \
-H 'Authorization: Bearer <TOKEN>' \
-d '{
  "type": "custom_type_fragment",
  "description": "Attributes for social media campaigns",
  "leaf_type": "campaign",
  "subtype": "social_media",
  "subtype_display_name": "Social Media",
  "is_custom_leaf_type": true,
  "fields": [
    {
      "name": "social_media_platform",
      "field_type": "enum",
      "allowed_values": [ "Facebook", "Instagram", "LinkedIn", "X" ],
      "is_filterable": true,
      "ui": { "display_name": "Platform" }
    },
    { "name": "post_id", "field_type": "text", "ui": { "display_name": "Post ID" } }
  ]
}'
```

Create a record of that subtype by naming it in `custom_schema_spec` and mixing
`tnt__` (inherited) and `ctype__` (subtype-only) fields in one payload:

```bash
curl -X POST 'https://api.devrev.ai/custom-objects.create' \
-H 'Authorization: Bearer <TOKEN>' \
-d '{
  "leaf_type": "campaign",
  "custom_schema_spec": { "subtype": "social_media", "tenant_fragment": true },
  "custom_fields": {
    "tnt__budget": 10000,
    "ctype__social_media_platform": "Facebook",
    "ctype__post_id": "1234567890"
  }
}'
```

Repeat the `schemas.custom.set` call with a different `subtype` (e.g.
`email_marketing`) and its own `fields` to add another flavor of the same
custom leaf type. Verify a subtype landed with `schemas.aggregated.get` and
`custom_schema_spec: { "subtype": "<name>" }` — see the Field notes above on
`schemas.subtypes.list` requiring a `leaf_type` filter to show anything.

**Field namespace nuance**: the `ctype__`/`tnt__` prefixes only apply to field
*values* on an instantiated record (`custom_fields` in create/update payloads
and in `schemas.aggregated.get`'s merged view). Inside a schema *definition*
(the `fields` array passed to `schemas.custom.set` itself), field `name`s are
bare — never write `"name": "ctype__post_id"` there, just `"name": "post_id"`.

**Subtype-scoped access roles**: object access is granted per Step 4's access
note, but field-level roles (Settings > User Management > Roles) can further be
scoped to one subtype via `target_subtype`, or applied uniformly with
`include_all_subtypes: true` — useful when different campaign subtypes should
be editable by different teams.

**Changing which subtype a record uses**: `schemas.subtypes.prepare-update`
(Playbook 3 step 5 in SKILL.md) previews the effect of a subtype schema change
before you apply it, reporting field-compatibility conflicts as
`ABSENT_IN_NEW` (a field the old subtype had that the new one drops) or
`INCOMPATIBLE_TYPE` (a field kept but with a changed `field_type`).

**Retiring an unwanted subtype (confirmed live 2026-07-26)**: there is no hard
delete for a `custom_type_fragment`, but you can deprecate it — replay the
fragment's complete existing payload (`type`, `leaf_type`, `subtype`,
`subtype_display_name`, full `fields` array) through `schemas.custom.set` with
**`deprecated: true`** added at the top level. **The field name is `deprecated`,
not `is_deprecated`** — sending `is_deprecated: true` returns HTTP 400
`bad_request` with no diagnostic. A successful call bumps `object_version` and
a follow-up `schemas.custom.get` echoes the field back as `is_deprecated: true`
(output name differs from input name). Effect verified: `schemas.subtypes.list
{"leaf_type":"<leaf_type>"}` stops listing a deprecated subtype, while an
active, non-deprecated subtype on the same call still appears — so this is a
real suppression, not just cosmetic. Not confirmed: whether `custom-objects.create`
/`works.create` using the deprecated subtype's `custom_schema_spec` is actually
rejected, since `schemas.aggregated.get` still resolves its fields when the
subtype is named explicitly.

> Sourced from DevRev's object-customization and custom-objects guides
> (developer.devrev.ai) — not independently live-tested in this repo yet.
> Where it overlaps with facts already live-verified here, the live-verified
> version wins: e.g. that source material's stage-diagram-attachment example
> uses `stage_diagram_id` on the subtype fragment, but this repo confirmed live
> (2026-07-19, Field notes above) that `stage_diagram_id` is **rejected** —
> the working write-side field is `stage_diagram` (a bare DON-id string), as
> already documented in Step 3 above. Likewise, that source claims custom link
> types can restrict by `subtype` **and** `leaf_only` — only the `subtype`
> restriction is confirmed to exist in this API; a live pass on 2026-07-19
> (see `skills/0-solution-architecture/references/api-cookbook.md` §5) found
> no `leaf_only` field anywhere in this domain. Treat `leaf_only` as unconfirmed
> until someone hits a live response that actually contains it.

---

## 2. Built-in links

Links connect two objects. Built-in link types cover the common relationships:
`serves`, `is_part_of`, `is_dependent_on`, `is_related_to`.

```bash
curl -X POST 'https://api.devrev.ai/links.create' \
-H 'Authorization: Bearer <TOKEN>' \
-d '{
  "link_type": "serves",
  "source": "<RUNNABLE_ID>",
  "target": "<FEATURE_ID>"
}'
```

- `links.list` — list an object's links.
- `links.replace` — swap a link. Atomic only for **part-to-part default (non-custom)
  link types**; for custom link types or non-part endpoints it runs as a
  non-atomic delete-then-create, and the new link must keep the same link type
  and share at least one endpoint. Use this to re-parent a part so it's
  never briefly orphaned; don't delete-then-create).
- `links.delete` — remove a link instance.
- Scope: `link:write` or `link:all`, plus read access to both linked objects.
- The API verifies both objects exist, so you can't create a dangling link.

---

## 3. Custom link types

When no built-in type fits — e.g. tying a custom object to a ticket — define a
custom link type once, then create many link instances from it. Allowed between
work objects, identity objects (account, rev/dev user, rev org), part objects,
and any custom leaf type.

### Step 1 — define the type (`link-types.custom.create`)

```bash
curl -X POST 'https://api.devrev.ai/link-types.custom.create' \
-H 'Authorization: Bearer <TOKEN>' \
-d '{
  "name": "Link between ticket and campaign",
  "source_types": [ { "leaf_type": "ticket" } ],
  "target_types": [ { "leaf_type": "campaign", "is_custom_leaf_type": true } ],
  "forward_name": "relates to campaign",
  "backward_name": "referenced by ticket"
}'
```

Save the returned id as `CUSTOM_LINK_TYPE_ID`. You can restrict to specific
subtypes by adding `subtype` inside a source/target descriptor.

### Step 2 — create a link instance (`links.create` with `custom_link`)

```bash
curl -X POST 'https://api.devrev.ai/links.create' \
-H 'Authorization: Bearer <TOKEN>' \
-d '{
  "link_type": "custom_link",
  "custom_link_type": "<CUSTOM_LINK_TYPE_ID>",
  "source": "<TICKET_ID>",
  "target": "<CAMPAIGN_OBJECT_ID>"
}'
```

### Manage custom link types

| Endpoint | Purpose |
| --- | --- |
| `link-types.custom.create` | Define a new custom link type |
| `link-types.custom.update` | Update a custom link type (also used to deprecate) |
| `link-types.custom.get` / `.list` | Read custom link types |

Scope: `link-types.custom.create` / `.update` require `custom_link_type:write`;
`.get` / `.list` require no scope.

> Custom link types **cannot be deleted, only deprecated** — there is no public
> `link-types.custom.delete`. To retire one, set `deprecated: true` via
> `link-types.custom.update`. This preserves referential integrity so existing
> links and old objects don't become corrupt. Name them carefully.

---

## 4. Linking work items, tickets, and issues

- Ticket <-> issue, issue <-> issue, and ticket <-> custom object are all created
  with `links.create` (built-in type where one fits, otherwise a custom link).
- Attach work to a part with `applies_to_part` on `works.create` so it surfaces
  on the part's Trail.
- Always reference objects by full DON id, never a display ID (e.g. use
  `don:core:...:ticket/456`, not `TKT-456`), in `source`, `target`, and
  `parent_part`.

---

## 5. Common pitfalls

- Sending custom fields without `custom_schema_spec` — Bad Request. Always name
  the schema for each field.
- Expecting a custom object to be visible immediately — grant roles first; also
  try refreshing / re-login for UI indexing delays.
- Using a display ID in a link — always pass the DON, or you get "object not found".
- Trying to delete a custom link type in use — deprecate instead.
- Duplicate records — pass a stable `unique_key` on `custom-objects.create`.
- Setting `stage` on a custom object that has no stage diagram — attach a diagram
  to the leaf type first (Step 3), or the stage value is rejected.
- Storing a part as text — use a `field_type: "id"` field with `id_type` limited
  to part types (Step 4), and pass the part DON, not `PROD-12`.
