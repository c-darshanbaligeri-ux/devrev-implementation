# team fields

Source: <https://developer.devrev.ai/airsync/object-types/team>
Scraped: 2026-11-03

Field reference for the `team` target. Required fields must be mapped or have a supported creation fallback.

Catalog generated July 13, 2026. Validate the mapping in your target organization. Can Load means external → DevRev; Can Extract means DevRev → external. See [field rules](../object-field-contract.md) for required values and references.

**Resource Type:** `team`

**Capabilities:** Can Load

## Fields

| Field            | Type                          | Required | Description                                                                              |
| ---------------- | ----------------------------- | -------- | ---------------------------------------------------------------------------------------- |
| `created_by_id`  | reference → \[#category:user] |          | User ID of the user that created the object.                                             |
| `description`    | text                          |          | The description of the team.                                                             |
| `key`            | text                          | ✔︎       | Key for uniquely identifying the team.                                                   |
| `modified_by_id` | reference → \[#category:user] |          | User ID of the user that last modified the object.                                       |
| `name`           | text                          | ✔︎       | Name of the team. Shall be derived from the group name associated with the team's space. |
| `parent_id`      | reference → \[#record:team]   |          | The parent of the team.                                                                  |
