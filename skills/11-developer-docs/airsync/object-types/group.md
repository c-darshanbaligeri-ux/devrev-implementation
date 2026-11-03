# group fields

Source: <https://developer.devrev.ai/airsync/object-types/group>
Scraped: 2026-11-03

Field reference for the `group` target. Required fields must be mapped or have a supported creation fallback.

Catalog generated July 13, 2026. Validate the mapping in your target organization. Can Load means external → DevRev; Can Extract means DevRev → external. See [field rules](../object-field-contract.md) for required values and references.

**Resource Type:** `group`

**Capabilities:** Can Load

## Fields

| Field            | Type                                      | Required | Description                                        |
| ---------------- | ----------------------------------------- | -------- | -------------------------------------------------- |
| `created_by_id`  | reference → \[#category:user]             |          | User ID of the user that created the object.       |
| `description`    | rich\_text                                | ✔︎       | Description of the group.                          |
| `includes`       | reference (collection) → \[#record:group] |          | IDs of the group(s) that the group includes.       |
| `item_url_field` | text                                      |          | Link to the item in the origin system.             |
| `member_type`    | enum                                      |          | Type of the members in the group.                  |
| `modified_by_id` | reference → \[#category:user]             |          | User ID of the user that last modified the object. |
| `name`           | text                                      | ✔︎       | Name of the group.                                 |
| `owner`          | reference → \[#record:devu]               |          | Owner of the group.                                |
| `type`           | enum                                      |          | Type of the group.                                 |

## Enum values

**member\_type**

| Value      | Name      | Description |
| ---------- | --------- | ----------- |
| `dev_user` | dev\_user | -           |
| `rev_user` | rev\_user | -           |
| `svc_acc`  | svc\_acc  | -           |

**type**

| Value     | Name    | Description |
| --------- | ------- | ----------- |
| `dynamic` | dynamic | -           |
| `static`  | static  | -           |
