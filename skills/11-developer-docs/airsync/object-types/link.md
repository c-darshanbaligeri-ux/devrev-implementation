# link fields

Source: <https://developer.devrev.ai/airsync/object-types/link>
Scraped: 2026-11-03

Field reference for the `link` target. Required fields must be mapped or have a supported creation fallback.

Catalog generated July 13, 2026. Validate the mapping in your target organization. Can Load means external → DevRev; Can Extract means DevRev → external. See [field rules](../object-field-contract.md) for required values and references.

**Resource Type:** `link`

**Capabilities:** Can Extract, Can Load

## Fields

| Field                 | Type                                           | Required | Description                                        |
| --------------------- | ---------------------------------------------- | -------- | -------------------------------------------------- |
| `created_by_id`       | reference → \[#category:user]                  |          | User ID of the user that created the object.       |
| `link_type`           | enum                                           | ✔︎       | Type of link used to define the relationship.      |
| `modified_by_id`      | reference → \[#category:user]                  |          | User ID of the user that last modified the object. |
| `source_id`           | reference → \[#category:work #record:incident] | ✔︎       | Source object ID.                                  |
| `source_object_type`  | enum                                           |          | Source object type.                                |
| `target_id`           | reference → \[#category:work #record:incident] | ✔︎       | Target object ID.                                  |
| `target_object_type`  | enum                                           |          | Target object type.                                |
| `transformed_from_id` | text                                           |          |                                                    |

## Enum values

**link\_type**

| Value             | Name            | Description |
| ----------------- | --------------- | ----------- |
| `is_dependent_on` | Is Dependent On | -           |
| `is_duplicate_of` | Is Duplicate Of | -           |
| `is_parent_of`    | Is Parent Of    | -           |
| `is_related_to`   | Is Related To   | -           |

**source\_object\_type**

| Value          | Name | Description |
| -------------- | ---- | ----------- |
| `conversation` | -    | -           |
| `incident`     | -    | -           |
| `work`         | -    | -           |

**target\_object\_type**

| Value          | Name | Description |
| -------------- | ---- | ----------- |
| `conversation` | -    | -           |
| `incident`     | -    | -           |
| `work`         | -    | -           |
