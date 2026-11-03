# Record and field mapping example

Source: <https://developer.devrev.ai/airsync/mapping-example>
Scraped: 2026-11-03

Inputs: [EDM](external-domain-metadata.md), normalized sample records and the chosen [target type](supported-object-types.md). Output: `initial_domain_mapping.json`.

## Mapping authoring from the public template

Copy the public template's `initial_domain_mapping.json` and edit it alongside your EDM. Keep both files in version control. Start with one record type, verify its import, and expand the options to cover the complete source model. Do not require a separate mapping CLI or agent service to produce this JSON.

This complete example maps the external `users.name` field to DevRev `devu.display_name`. It uses the format and target-metadata revision present in the public template; that revision is a metadata compatibility value, not the SDK version. Include mappings for the remaining record types in your connector and verify the file against your test org's current target options.

```json
{
  "additional_mappings": {
    "record_type_mappings": {
      "users": {
        "default_mapping": { "object_category": "stock", "object_type": "devu" },
        "possible_record_type_mappings": [
          {
            "devrev_leaf_type": "devu",
            "forward": true,
            "reverse": false,
            "shard": {
              "mode": "create_shard",
              "devrev_leaf_type": { "object_category": "stock", "object_type": "devu" },
              "stock_field_mappings": {
                "display_name": {
                  "forward": true,
                  "reverse": false,
                  "primary_external_field": "name",
                  "transformation_method_for_set": { "transformation_method": "use_directly" }
                }
              }
            }
          }
        ]
      }
    },
    "format_version": "v0.2.0",
    "devrev_metadata_version": 13
  }
}
```

The external `users` record type must declare `id` as an identifier and `name` as text in EDM. Creating user-like records in a test org must use the intended user type and the org's supported import behavior. Do not enable user reverse sync solely because a field transformation is reversible.

For task-like objects, use the public template's existing `todos` mapping as the complete example of required work fields, references, stages, constructed custom fields and reverse flags. Rename its external keys to match your EDM and normalization. For additional target types, consult the full [supported-object field reference](supported-object-types.md) and [transformation methods](data-model/transformation-methods.md).

## Method-specific configuration

These field-level fragments belong inside `stock_field_mappings`; they do not replace the file envelope:

```json
{
  "title": {
    "forward": true,
    "reverse": true,
    "primary_external_field": "title",
    "transformation_method_for_set": { "transformation_method": "use_directly" }
  }
}
```

For enum conversion, supply direction maps keyed by the values of that direction's source enum. This illustrative fragment assumes the target enum actually offers `P1` and `P2`:

```json
{
  "priority": {
    "forward": true,
    "reverse": true,
    "primary_external_field": "importance",
    "transformation_method_for_set": {
      "transformation_method": "map_enum",
      "is_array": false,
      "forward": { "high": { "value": "P1" }, "normal": { "value": "P2" } },
      "reverse": { "P1": { "value": "high" }, "P2": { "value": "normal" } }
    }
  }
}
```

Keep array flags consistent with EDM and the target field. For reference mappings, declare the referenced types and use a compatible method rather than a text conversion. For custom fields and jq expressions, retain the full output descriptor from the template and validate the output shape. For policy methods, follow the [authorization example](data-model/permissions-example.md).

## Mapping-stage verification

Deploy the snap-in with its bundled mapping, start a test import and inspect the choices offered during the mapping stage. Select each intended record-type option and check required-field fallbacks and field transformations. An option must be tested with representative data; valid JSON can still be incompatible with the platform metadata.

The user's selections produce the sync unit's recipe. Keep bundled options distinct from those final selections, and validate that record filtering and field filtering produce the intended import. If a required target field has no source value, configure a supported fallback through the import's mapping choices or the template's field configuration before proceeding.

Related: [Initial domain mapping](initial-domain-mapping.md).

Next: [Install and update connector mappings](mapping-installation.md).
