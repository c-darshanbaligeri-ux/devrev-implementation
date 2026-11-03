# Field transformation reference

Source: <https://developer.devrev.ai/airsync/data-model/transformation-methods>
Scraped: 2026-11-03

## Stock-field transformation methods

| Method                      | Purpose and configuration                                                                                                              |
| --------------------------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| `use_directly`              | Identity transformation when source and target types and collection shape are compatible                                               |
| `use_as_array_value`        | Wrap a compatible scalar input as an array value                                                                                       |
| `use_fixed_value`           | Fixed boolean, enum value or empty choice supported by the target option                                                               |
| `use_devrev_record`         | Use a selected DevRev reference of the compatible type                                                                                 |
| `map_enum`                  | Explicit forward/reverse maps between enum keys; validate unknown-value fallback and collection shape                                  |
| `map_roles`                 | Map external permission roles to DevRev roles; supplies forward role mapping and optional default                                      |
| `use_rich_text`             | Construct rich text while retaining supported mentions                                                                                 |
| `make_custom_stages`        | Build DevRev stages from the external stage diagram and generated stage definitions                                                    |
| `make_custom_links`         | Construct custom link mapping, including reverse stock-link type mappings                                                              |
| `filter_typed_reference`    | Keep typed references only for allowed DevRev leaf types                                                                               |
| `make_struct`               | Map structured values using nested field mappings                                                                                      |
| `use_first_non_null`        | Choose the first non-null result from ordered alternative field mappings                                                               |
| `make_authorization_target` | Specialized authorization target conversion for compatible target fields                                                               |
| `use_raw_jq`                | Custom jq transformation with generated input/output configuration; use when standard compatible methods cannot express the conversion |

The mapping's `forward` and `reverse` flags declare the selected direction. A forward method may not support reverse sync. Test reverse output explicitly before promising reverse sync.

## Custom-field methods

| Method                          | Purpose                                                                             |
| ------------------------------- | ----------------------------------------------------------------------------------- |
| `make_constrained_simple_value` | Preserve simple-field constraints in a DevRev custom field                          |
| `make_enum` / `make_uenum`      | Generate an enum field from external enum metadata                                  |
| `reference_custom_field`        | Generate a compatible reference custom field                                        |
| `use_rich_text`                 | Generate a rich-text custom field                                                   |
| `construct_text_field`          | Construct a text field using the selected input and text configuration              |
| `use_raw_jq`                    | Construct a field using a custom jq expression and explicit output field descriptor |

Custom-field definitions also include descriptors such as data name, display name, type, whether a field is required and allowed values. Use the generated file rather than pasting only a transformation method into IDM.

## Permission transformation methods

| Source EDM type         | Target policy field  | Method                    |
| ----------------------- | -------------------- | ------------------------- |
| `record_type_privilege` | `object_access`      | `make_object_access`      |
| `field_privilege`       | `field_access`       | `make_field_access`       |
| `conditional_privilege` | `conditional_access` | `make_conditional_access` |

These methods preserve policy semantics only for the declared target record types/categories. See the complete [permission contract](permissions.md) and [example](permissions-example.md).

## Field-mapping example

This is a field-level fragment, to be placed inside a generated shard's `stock_field_mappings`. It maps an external text title into a compatible DevRev title and enables both directions:

```json
{
  "title": {
    "forward": true,
    "reverse": true,
    "primary_external_field": "title",
    "transformation_method_for_set": {
      "transformation_method": "use_directly"
    }
  }
}
```

For a field required by DevRev but optional externally, configure a compatible fallback and verify record creation without a source value. Do not build a fallback DON from a display ID.

Related: [Unavailable mappings](mapping-reasons.md).
