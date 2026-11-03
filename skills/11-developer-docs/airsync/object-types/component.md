# component fields

Source: <https://developer.devrev.ai/airsync/object-types/component>
Scraped: 2026-11-03

Field reference for the `component` target. Required fields must be mapped or have a supported creation fallback.

Catalog generated July 13, 2026. Validate the mapping in your target organization. Can Load means external → DevRev; Can Extract means DevRev → external. See [field rules](../object-field-contract.md) for required values and references.

**Resource Type:** `part`, `component`

**Capabilities:** Can Extract, Can Load, Can Subtype

## Fields

| Field                  | Type                                       | Required | Description                                                                                |
| ---------------------- | ------------------------------------------ | -------- | ------------------------------------------------------------------------------------------ |
| `airsync_shared_with`  | permission (collection)                    |          | List of users and groups who have explicit access to the item and the corresponding roles. |
| `created_by_id`        | reference → \[#category:user]              |          | User ID of the user that created the object.                                               |
| `delivered_as`         | enum (collection)                          |          | Methods the product can be delivered as.                                                   |
| `description`          | rich\_text                                 |          | Description of the part.                                                                   |
| `development_owner_id` | reference → \[#category:user]              |          | User ID of the development owner of the part.                                              |
| `docs`                 | struct (collection)                        |          | Docs associated with the part.                                                             |
| `item_url_field`       | text                                       |          | Link to the item in the origin system.                                                     |
| `modified_by_id`       | reference → \[#category:user]              |          | User ID of the user that last modified the object.                                         |
| `name`                 | text                                       | ✔︎       | Name of the part.                                                                          |
| `owned_by_ids`         | reference (collection) → \[#category:user] | ✔︎       | User IDs of the users that own the part.                                                   |
| `parent_part`          | reference → \[#category:part]              |          | Parent of this part.                                                                       |
| `parent_part_ids`      | reference (collection) → \[#category:part] |          | Parent Part Ids of the Part.                                                               |
| `pm_owner_id`          | reference → \[#category:user]              |          | User ID of the PM owner of the part.                                                       |
| `qa_owner_id`          | reference → \[#category:user]              |          | User ID of the QA owner of the part.                                                       |
| `ref_url`              | text                                       |          | URL to the part details (git url, website, etc.).                                          |
| `tags`                 | reference (collection) → \[#record:tag]    |          | Tags associated with the object.                                                           |

## Enum values

**delivered\_as**

| Value      | Name     | Description |
| ---------- | -------- | ----------- |
| `goods`    | goods    | -           |
| `service`  | service  | -           |
| `software` | software | -           |

### Structs

#### doc\_field

| Field      | Type   | Required | Description           |
| ---------- | ------ | -------- | --------------------- |
| `doc_type` | enum   |          | Type of doc.          |
| `url_info` | struct | ✔︎       | URL Info for the doc. |

#### url\_field

| Field   | Type | Required | Description             |
| ------- | ---- | -------- | ----------------------- |
| `title` | text |          | Title text for the url. |
| `url`   | text | ✔︎       | URL for the field.      |
