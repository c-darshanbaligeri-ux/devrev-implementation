# Define object and field privileges

Source: <https://developer.devrev.ai/airsync/data-model/privileges>
Scraped: 2026-11-03

## Object-level privileges

Each object-access entry supplies `record_types` and `privileges`. Supported privilege names are `create`, `read`, `update` and `delete`:

```json
{
  "record_types": ["tasks", "documents"],
  "privileges": ["read", "update"]
}
```

## Field-level privileges

A field-access entry supplies `record_type` and read/write selectors:

```json
{
  "record_type": "tasks",
  "read_fields": ["title", "body", "owner"],
  "write_fields": ["title", "body"]
}
```

Use `read_all_fields` or `write_all_fields` to express all-field access instead of enumerating keys. Writable fields also require read access. Keep explicit write fields within the intended readable set rather than relying on a conversion to mask a mismatched source policy.

## Conditional privileges

A conditional-access entry supplies `record_type` and either `object_privileges` or `field_privileges`, plus at least one non-empty condition:

| Condition            | Meaning                                                             |
| -------------------- | ------------------------------------------------------------------- |
| `scope_to_users_in`  | The principal must occur in each listed user-reference field        |
| `scope_to_groups_in` | A principal's group must occur in each listed group-reference field |
| `field_caveats`      | All specified field comparisons must match                          |

User and group scope conditions can be combined. They are mutually exclusive with `field_caveats`. Conditions within an array are conjunctive.

Each caveat contains `field`, `operator` and `value`. Supported operators are `eq`, `not_eq`, `in` and `intersects`. `intersects` applies to collections; `eq`, `not_eq` and `in` apply to scalar fields, and boolean fields permit only `eq` and `not_eq`. Supported fields include int, text, bool, rich text, enum, reference, typed reference and collections of these types. The value must match the field type; `in` supplies an array of matching scalar values.

```json
{
  "record_type": "tasks",
  "object_privileges": ["read"],
  "field_caveats": [
    { "field": "status", "operator": "in", "value": ["open", "done"] }
  ]
}
```

Related: [Permissions](permissions.md).

Next: [Access-rule import example](permissions-example.md).
