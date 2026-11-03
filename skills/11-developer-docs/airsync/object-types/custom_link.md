# custom_link fields

Source: <https://developer.devrev.ai/airsync/object-types/custom_link>
Scraped: 2026-11-03

Field reference for the `custom_link` target. Required fields must be mapped or have a supported creation fallback.

Catalog generated July 13, 2026. Validate the mapping in your target organization. Can Load means external → DevRev; Can Extract means DevRev → external. See [field rules](../object-field-contract.md) for required values and references.

**Resource Type:** `link`

**Capabilities:** Can Extract, Can Load

## Fields

| Field            | Type                                                                                                                                                                                                                                                                                            | Required | Description                                        |
| ---------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------- | -------------------------------------------------- |
| `created_by_id`  | reference → \[#category:user]                                                                                                                                                                                                                                                                   |          | User ID of the user that created the object.       |
| `link_type_id`   | enum                                                                                                                                                                                                                                                                                            | ✔︎       | Link Type.                                         |
| `modified_by_id` | reference → \[#category:user]                                                                                                                                                                                                                                                                   |          | User ID of the user that last modified the object. |
| `source_id`      | reference → \[#category:custom\_object #record:account #record:article #record:capability #record:conversation #record:enhancement #record:feature #record:incident #record:issue #record:meeting #record:opportunity #record:product #record:project #record:revu #record:task #record:ticket] | ✔︎       | Source object ID.                                  |
| `target_id`      | reference → \[#category:custom\_object #record:account #record:article #record:capability #record:conversation #record:enhancement #record:feature #record:incident #record:issue #record:meeting #record:opportunity #record:product #record:project #record:revu #record:task #record:ticket] | ✔︎       | Target object ID.                                  |

## Enum values

**link\_type\_id**

| Value             | Name            | Description |
| ----------------- | --------------- | ----------- |
| `is_dependent_on` | Is Dependent On | -           |
| `is_duplicate_of` | Is Duplicate Of | -           |
| `is_parent_of`    | Is Parent Of    | -           |
| `is_related_to`   | Is Related To   | -           |
