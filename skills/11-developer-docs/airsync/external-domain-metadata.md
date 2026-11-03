# Define the external data schema

Source: <https://developer.devrev.ai/airsync/external-domain-metadata>
Scraped: 2026-11-03

External domain metadata (EDM) is the schema for the records your connector emits. Define it before writing the metadata worker. Its record-type and field keys must match your normalized data.

## Top-level EDM contract

The public SDK exports `ExternalDomainMetadata` and its component types:

| Field                    | Required | Meaning                                                                                                 |
| ------------------------ | -------- | ------------------------------------------------------------------------------------------------------- |
| `record_types`           | Yes      | Map of external record-type keys to record definitions                                                  |
| `schema_version`         | No       | EDM format version; use `v0.2.0` for the documented format                                              |
| `record_type_categories` | No       | Named categories grouping related record types                                                          |
| `struct_types`           | No       | Reusable structured field definitions                                                                   |
| `team_data`              | No       | Platform schema extension naming the sync-unit team; see [team import](data-model/team-import.md) |

The format version is separate from the SDK version and from DevRev metadata revisions. Do not set `schema_version` to the SDK package version. The platform EDM schema includes `team_data`; the SDK's current `ExternalDomainMetadata` interface does not declare that extension. If you use it in TypeScript, model the extension explicitly rather than suppressing checks with `any`.

## Verification

Type-check metadata against the public SDK types and compare it with the [template metadata definition](https://github.com/devrev/airsync-template/tree/main/code/src/functions/external-system). Validate it in a test import too: TypeScript checks alone do not prove normalized values or platform schema extensions match the declarations.

Check every normalized record type and field against EDM, verify all references resolve, and test custom fields, stages and permissions in an import. Add a dynamic record type to a declared category and confirm the intended mapping remains available. Never substitute an empty schema after an external metadata failure; fail or resume the metadata task as appropriate.

Related contracts: [initial domain mapping](initial-domain-mapping.md), [mapping methods](data-model/mapping-reasons.md), [supported targets](supported-object-types.md).

## Record-type definition

A record type defines a group of external records and the capabilities available for them.

| Property              | Meaning                                                                         |
| --------------------- | ------------------------------------------------------------------------------- |
| `fields`              | Required map of field keys to definitions                                       |
| `name`, `description` | Human-readable labels and explanation                                           |
| `category`            | Key in `record_type_categories`                                                 |
| `is_loadable`         | Connector supports creating the record type in the external system              |
| `is_snapshot`         | This type represents a complete current-state snapshot when it is emitted       |
| `no_identifier`       | Record type has no identifier field, primarily for authorization-policy records |
| `scope`               | `metadata_is_system_scoped` or `data_is_system_scoped` when applicable          |
| `conditions`          | Conditional field requirements or visibility rules                              |
| `stage_diagram`       | External stage/state definitions and transitions                                |
| `link_naming_data`    | Link type field and forward/backward names                                      |
| `attachments`         | `is_extractable` and/or `is_loadable` attachment capabilities                   |

Do not mark a type loadable until its mapping and create/update callbacks are implemented. Snapshot semantics are especially important for [authorization policies](data-model/permissions.md): a partial changed-record set cannot represent the current policy state.

<span id="complete-edm-example" />

Related: [Metadata example](metadata-example.md).

<span id="categories-conditions-and-stages" />

For dynamic types and workflows, see [Categories, conditions and stages](metadata-advanced.md).

<span id="field-definition" />

Related:

* [Metadata fields and references](metadata-fields.md).

Next: [Define schema fields and references](metadata-fields.md).
