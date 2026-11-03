# Understand unavailable mappings

Source: <https://developer.devrev.ai/airsync/data-model/mapping-reasons>
Scraped: 2026-11-03

## Why a mapping is unavailable

| Symptom                                    | Check                                                                                        |
| ------------------------------------------ | -------------------------------------------------------------------------------------------- |
| Text cannot map to a rich-text target      | Declare `rich_text` in EDM and normalize rich text correctly                                 |
| ID-like text cannot map to a reference     | Declare a `reference` or `typed_reference` with the correct target types                     |
| Scalar cannot map to a collection directly | Use a supported scalar-to-array method or declare the actual collection                      |
| Struct has few options                     | Inspect compatible structured mapping options; do not flatten it without preserving meaning  |
| Required field remains unresolved          | Supply a mapped source value or a supported fallback                                         |
| Reverse mapping is unavailable             | Check read-only metadata, type support and whether the method supports the reverse direction |
| Permission targets are omitted             | Add their exact record/category keys to the privilege field's EDM `type_keys`                |

Use the [public template mapping](https://github.com/devrev/airsync-template/blob/main/code/src/functions/external-system/initial_domain_mapping.json) as the file-shape reference and verify the offered options in a test import. Method-specific parameters must agree with the exact metadata; a configured transformation does not implement the external API behavior.

## Transformation verification

Test null/missing input, unknown enum values, empty collections, mixed typed references, unresolved identities and limits declared in EDM. For custom jq, verify output type and collection shape, handling of absent fields and whether any reverse expression is valid. A syntactically valid expression can still emit an invalid domain value.

If a transformation fails, retain the failing record-type key, field key, method and sanitized example value. Fix the source declaration or generated mapping and rerun the import. Do not silently change the field type solely to make an option appear.

Related contracts: [EDM](../external-domain-metadata.md), [IDM](../initial-domain-mapping.md), [supported target fields](../supported-object-types.md).

<span id="stock-field-transformation-methods" />

Related:

* [Transformation methods](transformation-methods.md).
