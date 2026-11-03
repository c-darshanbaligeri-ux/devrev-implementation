# directory fields

Source: <https://developer.devrev.ai/airsync/object-types/directory>
Scraped: 2026-11-03

Field reference for the `directory` target. Required fields must be mapped or have a supported creation fallback.

Catalog generated July 13, 2026. Validate the mapping in your target organization. Can Load means external → DevRev; Can Extract means DevRev → external. See [field rules](../object-field-contract.md) for required values and references.

**Resource Type:** `directory`

**Capabilities:** Can Load

## Fields

| Field                        | Type                                    | Required | Description                                                                             |
| ---------------------------- | --------------------------------------- | -------- | --------------------------------------------------------------------------------------- |
| `created_by_id`              | reference → \[#category:user]           |          | User ID of the user that created the object.                                            |
| `description`                | text                                    |          | Description of the directory.                                                           |
| `external_translation_group` | text                                    |          | The translation group the directory belongs to.                                         |
| `icon`                       | text                                    |          | Icon of the directory.                                                                  |
| `language`                   | text                                    |          | Language of the directory.                                                              |
| `modified_by_id`             | reference → \[#category:user]           |          | User ID of the user that last modified the object.                                      |
| `parent`                     | reference → \[#record:directory]        |          | Parent directory.                                                                       |
| `published`                  | bool                                    | ✔︎       | Whether the directory is published.                                                     |
| `shared_with`                | permission (collection)                 |          | The list of users and groups the directory is shared with and the  corresponding roles. |
| `tags`                       | reference (collection) → \[#record:tag] |          | Tags associated with the directory.                                                     |
| `title`                      | text                                    | ✔︎       | Title of the directory.                                                                 |
