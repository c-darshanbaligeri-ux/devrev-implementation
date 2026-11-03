# enhancement fields

Source: <https://developer.devrev.ai/airsync/object-types/enhancement>
Scraped: 2026-11-03

Field reference for the `enhancement` target. Required fields must be mapped or have a supported creation fallback.

Catalog generated July 13, 2026. Validate the mapping in your target organization. Can Load means external → DevRev; Can Extract means DevRev → external. See [field rules](../object-field-contract.md) for required values and references.

**Resource Type:** `part`, `enhancement`

**Capabilities:** Can Extract, Can Load, Can Subtype

## Fields

| Field                 | Type                                        | Required | Description                                                                                |
| --------------------- | ------------------------------------------- | -------- | ------------------------------------------------------------------------------------------ |
| `account_ids`         | reference (collection) → \[#record:account] |          | Accounts associated to enhancement.                                                        |
| `airsync_shared_with` | permission (collection)                     |          | List of users and groups who have explicit access to the item and the corresponding roles. |
| `created_by_id`       | reference → \[#category:user]               |          | User ID of the user that created the object.                                               |
| `delivered_as`        | enum (collection)                           |          | Methods the product can be delivered as.                                                   |
| `description`         | rich\_text                                  |          | Description of the part.                                                                   |
| `docs`                | struct (collection)                         |          | Docs associated with the part.                                                             |
| `health`              | enum                                        |          | Health status tracking for enhancement.                                                    |
| `item_url_field`      | text                                        |          | Link to the item in the origin system.                                                     |
| `modified_by_id`      | reference → \[#category:user]               |          | User ID of the user that last modified the object.                                         |
| `name`                | text                                        | ✔︎       | Name of the part.                                                                          |
| `opportunity_ids`     | reference (collection) → \[#category:work]  |          | Opportunities from the enhancement.                                                        |
| `owned_by_ids`        | reference (collection) → \[#category:user]  | ✔︎       | User IDs of the users that own the part.                                                   |
| `parent_part`         | reference → \[#category:part]               | ✔︎       | Parent of this part.                                                                       |
| `parent_part_ids`     | reference (collection) → \[#category:part]  |          | Parent Part Ids of the Part.                                                               |
| `potential_revenue`   | float                                       |          | Potential revenue from the enhancement.                                                    |
| `ref_url`             | text                                        |          | URL to the part details (git url, website, etc.).                                          |
| `release_notes`       | text                                        |          | Release notes of the enhancement.                                                          |
| `rev_score`           | float                                       |          | Rev Score of the enhancement.                                                              |
| `rev_score_tier`      | enum                                        |          | Rev Score tier of the enhancement.                                                         |
| `stage`               | enum                                        | ✔︎       | Stage of the part.                                                                         |
| `status_update`       | text                                        |          | Status update for enhancement.                                                             |
| `tags`                | reference (collection) → \[#record:tag]     |          | Tags associated with the object.                                                           |
| `target_close_date`   | timestamp                                   |          | Target close date for the object.                                                          |
| `target_start_date`   | timestamp                                   |          | Target start date for the object.                                                          |
| `team_id`             | reference → \[#record:team]                 |          | The team associated with the object.                                                       |
| `ticket_ids`          | reference (collection) → \[#category:work]  |          | Tickets associated with the enhancement.                                                   |

## Enum values

**delivered\_as**

| Value      | Name     | Description |
| ---------- | -------- | ----------- |
| `goods`    | goods    | -           |
| `service`  | service  | -           |
| `software` | software | -           |

**health**

| Value | Name           | Description |
| ----- | -------------- | ----------- |
| `1`   | On Track       | -           |
| `2`   | At Risk        | -           |
| `3`   | Off Track      | -           |
| `4`   | Not Applicable | -           |

**rev\_score\_tier**

| Value    | Name   | Description |
| -------- | ------ | ----------- |
| `high`   | high   | -           |
| `low`    | low    | -           |
| `medium` | medium | -           |

**stage**

| Value                  | Name                 | Description |
| ---------------------- | -------------------- | ----------- |
| `deprecated`           | Deprecated           | -           |
| `deprioritized`        | Deprioritized        | -           |
| `general_availability` | General Availability | -           |
| `ideation`             | Ideation             | -           |
| `in_development`       | In Development       | -           |
| `in_testing`           | In testing           | -           |
| `limited_availability` | Limited Availability | -           |
| `prioritized`          | Prioritized          | -           |
| `ux_design`            | UX Design            | -           |
| `wont_do`              | Won't do             | -           |

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
