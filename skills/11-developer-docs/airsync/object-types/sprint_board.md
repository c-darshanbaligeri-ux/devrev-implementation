# sprint_board fields

Source: <https://developer.devrev.ai/airsync/object-types/sprint_board>
Scraped: 2026-11-03

Field reference for the `sprint_board` target. Required fields must be mapped or have a supported creation fallback.

Catalog generated July 13, 2026. Validate the mapping in your target organization. Can Load means external → DevRev; Can Extract means DevRev → external. See [field rules](../object-field-contract.md) for required values and references.

**Resource Type:** `vista`

**Capabilities:** Can Load

## Fields

| Field             | Type                          | Required | Description                                                     |
| ----------------- | ----------------------------- | -------- | --------------------------------------------------------------- |
| `cooldown`        | int                           |          | Cooldown period in days between sprints.                        |
| `created_by_id`   | reference → \[#category:user] |          | User ID of the user that created the object.                    |
| `description`     | rich\_text                    |          | Description of the sprint board.                                |
| `duration`        | int                           |          | Duration of the sprints belonging to this sprint board in days. |
| `modified_by_id`  | reference → \[#category:user] |          | User ID of the user that last modified the object.              |
| `name`            | text                          | ✔︎       | Name of the sprint board.                                       |
| `planned_sprints` | int                           |          | Number of planned sprints for the sprint board.                 |
| `team_id`         | reference → \[#record:team]   |          | The team associated with the object.                            |
