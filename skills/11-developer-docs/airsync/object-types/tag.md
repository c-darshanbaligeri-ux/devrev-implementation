# tag fields

Source: <https://developer.devrev.ai/airsync/object-types/tag>
Scraped: 2026-11-03

Field reference for the `tag` target. Required fields must be mapped or have a supported creation fallback.

Catalog generated July 13, 2026. Validate the mapping in your target organization. Can Load means external → DevRev; Can Extract means DevRev → external. See [field rules](../object-field-contract.md) for required values and references.

**Resource Type:** `tag`

**Capabilities:** Can Load

## Fields

| Field            | Type                          | Required | Description                                        |
| ---------------- | ----------------------------- | -------- | -------------------------------------------------- |
| `access_level`   | enum                          |          | Access level for the tag.                          |
| `created_by_id`  | reference → \[#category:user] |          | User ID of the user that created the object.       |
| `description`    | rich\_text                    |          | Description of the tag.                            |
| `modified_by_id` | reference → \[#category:user] |          | User ID of the user that last modified the object. |
| `name`           | text                          | ✔︎       | Name of the tag.                                   |
| `style`          | text                          |          | hex color of in the format #RRGGBB.                |

## Enum values

**access\_level**

| Value        | Name       | Description |
| ------------ | ---------- | ----------- |
| `internal`   | internal   | -           |
| `private`    | private    | -           |
| `public`     | public     | -           |
| `restricted` | restricted | -           |
