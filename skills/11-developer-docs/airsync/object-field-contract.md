# Read target field requirements

Source: <https://developer.devrev.ai/airsync/object-field-contract>
Scraped: 2026-11-03

## Field contract and verification

The field tables give type, whether a field is required and reference targets. Required target fields must be mapped or have a supported creation fallback. `collection` means an array of the listed type. Reference labels such as `#record:article` and `#category:user` identify compatible targets, not literal values to send as object IDs.

Test actual required values, enums, empty collections and unresolved references. Verify subtypes and custom fields when supported. For reverse-enabled objects, confirm the external write receives the denormalized values your API accepts. For permissions and teams, test enforcement and relationships in addition to field presence.

Related contracts: [transformation methods](data-model/transformation-methods.md), [permissions](data-model/permissions.md), [teams](data-model/team-import.md), [rich text](data-model/rich-text-fields.md), [reverse sync](loading-phases.md).

Related: [supported types](supported-object-types.md), [mapping rules](initial-domain-mapping.md#mapping-design-invariants).
