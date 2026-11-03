# Define schema fields and references

Source: <https://developer.devrev.ai/airsync/metadata-fields>
Scraped: 2026-11-03

Fields belong to a [record type](external-domain-metadata.md#record-type-definition). Their keys must match the normalized data.

## Field definition

Every field has a `type`. Optional shared properties are `name`, `description`, `is_required`, `is_read_only`, `is_write_only`, `is_indexed`, `is_identifier`, `default_value` and `collection`.

`is_required` describes the external domain's requirement; DevRev target fields may have different requirements and need mapping fallbacks. `is_read_only` fields must not be sent on external create/update calls. Set `is_identifier` on fields that uniquely identify an external record.

The presence of `collection: {}` makes a field a collection of its declared type. Collection bounds are `min_length` and `max_length`.

| Field type              | Type-specific definition or data contract                                                     |
| ----------------------- | --------------------------------------------------------------------------------------------- |
| `bool`                  | Boolean value                                                                                 |
| `int`                   | Integer; optional `int.min`, `int.max`                                                        |
| `float`                 | Number; optional `float.min`, `float.max`                                                     |
| `text`                  | String; optional `text.min_length`, `text.max_length`                                         |
| `rich_text`             | Structured strings and mention objects; see [rich text](data-model/rich-text-fields.md) |
| `date`                  | Calendar date                                                                                 |
| `timestamp`             | Timestamp; keep formatting consistent with normalized record timestamps                       |
| `enum`                  | `enum.values`, each containing `key` and optional `name`, `description`, `is_deprecated`      |
| `reference`             | `reference.refers_to`; targets declared record types, optionally by a named field             |
| `typed_reference`       | `typed_reference.refers_to`; preserves target type with the identity                          |
| `struct`                | `struct.key` refers to a reusable `struct_types` definition                                   |
| `permission`            | `permission.member_id` reference definition and `permission.role` enum                        |
| `record_type_privilege` | `record_type_privilege.type_keys` declares target records/categories                          |
| `field_privilege`       | `field_privilege.type_keys` declares target records/categories                                |
| `conditional_privilege` | `conditional_privilege.type_keys` declares target records/categories                          |
| `participation`         | `participation.refers_to` declares participating record types                                 |

The exported `Field` type also has `type_key` and `field_reference` definition properties. Their presence does not add new values to the SDK's `FieldType` union. Use the documented target-field contract for specialized platform fields rather than inventing a new type name.

## Reference identity

A plain reference value uses the external identity as a string. A typed-reference value must include the referenced record type as well as its identity; use it when that type varies per record. Collections contain arrays of the corresponding value shape.

Declare referenced record types with `#record:<record-type-key>`. Reference definitions can set `by_field` to identify a non-primary lookup field and `reference_type` to `parent` or `child`. A parent reference describes special ownership, not just an arbitrary link.

Normalized values must use the external identity expected by that declaration. They must not contain pre-guessed DevRev IDs. Import referenced entities or provide a valid pre-existing identity mapping. `typed_reference` is appropriate when the value can reference more than one external record type and the target type must be preserved.

## Field types and references

Use the supported field types and define reference targets explicitly.

The public `FieldType` supports `bool`, `int`, `float`, `text`, `rich_text`, `reference`, `typed_reference`, `enum`, `date`, `timestamp`, `struct`, `permission`, `record_type_privilege`, `field_privilege`, `conditional_privilege` and `participation`.

| Field configuration       | Contract                                                                         |
| ------------------------- | -------------------------------------------------------------------------------- |
| `is_required`             | Normalized records must provide a valid value when required                      |
| `collection`              | Values are arrays, optionally bounded in length                                  |
| `reference.refers_to`     | Declare target `#record:<key>` or `#category:<key>` entries                      |
| `typed_reference`         | Declare allowed targets; emitted values include explicit target type             |
| `enum`                    | Declare accepted external keys and display values                                |
| `struct`                  | Declare the nested structure                                                     |
| Type-specific constraints | Apply the schema's text lengths, numeric bounds and other supported restrictions |

Use case-sensitive field keys. A numeric source ID must become a string before use as a reference. Plain references and typed references have different value shapes; see the [mapping contract](initial-domain-mapping.md). Permission and privilege fields must use the [permissions schema](data-model/permissions.md), and formatted content must use [rich text](data-model/rich-text-fields.md).

Related: [Metadata extraction](metadata-extraction.md).

Next: [External schema example](metadata-example.md).
