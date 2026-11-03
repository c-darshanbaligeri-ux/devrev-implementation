# sprint fields

Source: <https://developer.devrev.ai/airsync/object-types/sprint>
Scraped: 2026-11-03

Field reference for the `sprint` target. Required fields must be mapped or have a supported creation fallback.

Catalog generated July 13, 2026. Validate the mapping in your target organization. Can Load means external → DevRev; Can Extract means DevRev → external. See [field rules](../object-field-contract.md) for required values and references.

**Resource Type:** `vista_group_item`

**Capabilities:** Can Load

## Fields

| Field            | Type                                 | Required | Description                                        |
| ---------------- | ------------------------------------ | -------- | -------------------------------------------------- |
| `created_by_id`  | reference → \[#category:user]        |          | User ID of the user that created the object.       |
| `end_date`       | timestamp                            | ✔︎       | Timestamp when the sprint ends.                    |
| `goals`          | text                                 |          | Goals of the sprint.                               |
| `modified_by_id` | reference → \[#category:user]        |          | User ID of the user that last modified the object. |
| `name`           | text                                 | ✔︎       | Name of the sprint.                                |
| `parent_id`      | reference → \[#record:sprint\_board] | ✔︎       | Parent sprint board of the sprint.                 |
| `start_date`     | timestamp                            | ✔︎       | Timestamp when the sprint starts.                  |
