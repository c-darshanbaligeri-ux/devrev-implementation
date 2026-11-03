# Map external records to DevRev objects

Source: <https://developer.devrev.ai/airsync/initial-domain-mapping>
Scraped: 2026-11-03

Initial domain mapping (IDM) defines the default mapping choices offered for your external schema. Package it as `initial_domain_mapping.json`. The choices offered by this file are distinct from the recipe a user selects for a sync unit.

## Mapping inputs and outputs

Mapping authoring requires [external domain metadata](external-domain-metadata.md), representative normalized records and the current DevRev target metadata. Its output is `initial_domain_mapping.json`, checked into the connector project and passed to the SDK entry points.

The public SDK exports this envelope:

```typescript
import type { InitialDomainMapping } from '@devrev/airsync-sdk';

const initialMapping: InitialDomainMapping = {
  additional_mappings: {},
};
```

The empty value demonstrates only the type envelope; it is not a usable mapping. Start from the public [template mapping](https://github.com/devrev/airsync-template/blob/main/code/src/functions/external-system/initial_domain_mapping.json) and edit its record and field options to match your metadata. The SDK's `object` typing does not validate the nested mapping contract.

## Mapping-file structure

| Element                                             | Contract                                                    |
| --------------------------------------------------- | ----------------------------------------------------------- |
| `starting_recipe_blueprint`                         | Optional recipe blueprint to pre-create during installation |
| `additional_mappings.record_type_mappings`          | Options keyed by exact external record-type keys            |
| `additional_mappings.record_type_category_mappings` | Options keyed by external category keys                     |
| `additional_mappings.format_version`                | Mapping format version, retained from generated output      |
| `additional_mappings.devrev_metadata_version`       | Target metadata revision used to produce the options        |

Each record/category mapping declares `default_mapping` and can supply `possible_record_type_mappings` and `mapping_as_custom_object`. A possible record-type mapping includes `devrev_leaf_type`, `forward`, `reverse` and its `shard` configuration. A created shard has `mode: create_shard`, a DevRev leaf-type selector and stock/custom field mappings.

`forward` means external system to DevRev. `reverse` means DevRev to external system. A record mapping's reverse flag and each relevant field's reverse flag must agree with the connector's implemented write capabilities. Turning on a flag does not create a loading worker or grant external API scopes.

A field mapping identifies its external input with `primary_external_field`, direction flags and a transformation method. Method parameters depend on the selected option. Use the [field transformation reference](data-model/transformation-methods.md) and the public template for method-specific shapes. A method name alone is insufficient: input and output types and required parameters must agree.

## Mapping design invariants

Map required target fields and define how missing values and references behave.

* Map every required target field or provide a supported fallback. A fallback can fill a required DevRev field absent from a source record on creation.
* Declare actual reference fields in EDM before mapping them to DevRev references. Text containing an ID is not equivalent to a reference.
* Keep rich text typed as `rich_text` to preserve mentions and article references.
* Mark external read-only fields appropriately and disable unsupported reverse transformations.
* Provide category-level choices for dynamic external record types where possible.
* Use `new_custom_object` when the source model needs a custom DevRev leaf type. Consult [custom objects](../guides/custom-objects.md) and [object customization](../guides/object-customization.md) for its subtype and custom-field behavior.

Users can choose among offered record mappings and filter/configure fields during import. The IDM constrains these choices; it is not the user's final recipe for every sync unit.

## Mapping validation and recovery

Test missing source values, empty collections, enum values, unresolved references and required-field fallbacks. Exercise every offered target mapping and both directions when reverse mapping is enabled. Verify resulting DevRev types, subtype fields, permissions, relationships and external write payloads.

If a mapping option is unavailable, inspect [mapping reasons and transformation methods](data-model/mapping-reasons.md). A changed EDM or target metadata revision may require regenerating options. Test updated mappings with a new test import before shipping a snap-in upgrade; do not assume an existing sync unit's selected recipe changes merely because the bundled IDM changed.

Related contracts: [object mappers](object-mappers.md), [supported object types](supported-object-types.md), [reverse sync](loading-phases.md).

<span id="mapping-authoring-from-the-public-template" />

Related: [Mapping example](mapping-example.md).

<span id="sdk-v2-installation" />

<span id="sdk-installation" />

Mapping installation and upgrades are covered in [Install and update connector mappings](mapping-installation.md).

Next: [Record and field mapping example](mapping-example.md).
