# comment fields

Source: <https://developer.devrev.ai/airsync/object-types/comment>
Scraped: 2026-11-03

Field reference for the `comment` target. Required fields must be mapped or have a supported creation fallback.

Catalog generated July 13, 2026. Validate the mapping in your target organization. Can Load means external → DevRev; Can Extract means DevRev → external. See [field rules](../object-field-contract.md) for required values and references.

**Resource Type:** `comment`

**Capabilities:** Can Extract, Can Load

## Fields

| Field                     | Type                                                                                                                                                                                    | Required | Description                                        |
| ------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------- | -------------------------------------------------- |
| `body`                    | rich\_text                                                                                                                                                                              | ✔︎       | Comment body.                                      |
| `created_by_id`           | reference → \[#category:user]                                                                                                                                                           | ✔︎       | User ID of the user that created the object.       |
| `creator_display_name`    | text                                                                                                                                                                                    |          | Creator display name.                              |
| `grandparent_object_id`   | reference → \[#category:chat #category:custom\_object #category:part #category:work #record:account #record:conversation #record:incident #record:meeting #record:revu]                 |          | The object this relates to.                        |
| `grandparent_object_type` | text                                                                                                                                                                                    |          | The object type this relates to.                   |
| `item_url_field`          | text                                                                                                                                                                                    |          | Link to the item in the origin system.             |
| `modified_by_id`          | reference → \[#category:user]                                                                                                                                                           | ✔︎       | User ID of the user that last modified the object. |
| `parent_object_id`        | reference → \[#category:chat #category:custom\_object #category:part #category:work #record:account #record:comment #record:conversation #record:incident #record:meeting #record:revu] | ✔︎       | The object this relates to.                        |
| `parent_object_type`      | text                                                                                                                                                                                    |          | The object type this relates to.                   |
| `visibility`              | enum                                                                                                                                                                                    |          | Visibility of the comment.                         |

## Enum values

**visibility**

| Value                 | Name                 | Description |
| --------------------- | -------------------- | ----------- |
| `Visibility_EXTERNAL` | Visibility\_EXTERNAL | -           |
| `Visibility_INTERNAL` | Visibility\_INTERNAL | -           |
| `Visibility_PRIVATE`  | Visibility\_PRIVATE  | -           |
| `Visibility_PUBLIC`   | Visibility\_PUBLIC   | -           |
