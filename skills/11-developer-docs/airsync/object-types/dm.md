# dm fields

Source: <https://developer.devrev.ai/airsync/object-types/dm>
Scraped: 2026-11-03

Field reference for the `dm` target. Required fields must be mapped or have a supported creation fallback.

Catalog generated July 13, 2026. Validate the mapping in your target organization. Can Load means external → DevRev; Can Extract means DevRev → external. See [field rules](../object-field-contract.md) for required values and references.

**Resource Type:** `chat`, `dm`

**Capabilities:** Can Load

## Fields

| Field               | Type                                                     | Required | Description                                                                                                                                                                                                 |
| ------------------- | -------------------------------------------------------- | -------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `created_by_id`     | reference → \[#category:user]                            |          | User ID of the user that created the object.                                                                                                                                                                |
| `is_default`        | bool                                                     |          | Whether this is the default DM for messaging the constituent users. If true, then this DM is always returned when opening a DM for the users. Note only one DM may be the default for a given set of users. |
| `item_url_field`    | text                                                     |          | Link to the item in the origin system.                                                                                                                                                                      |
| `last_comment_date` | timestamp                                                |          | Timestamp of the last comment in the chat.                                                                                                                                                                  |
| `modified_by_id`    | reference → \[#category:user]                            |          | User ID of the user that last modified the object.                                                                                                                                                          |
| `record_ids`        | text (collection)                                        |          | The associated records for this DM.                                                                                                                                                                         |
| `shared_with`       | permission (collection)                                  |          | Members that this object is shared with.                                                                                                                                                                    |
| `title`             | text                                                     |          | The title given to the chat.                                                                                                                                                                                |
| `user_ids`          | reference (collection) → \[#category:user #record:group] | ✔︎       | The users in the direct message. Only these users have access the chat's history and can send new messages (either users or groups).                                                                        |
