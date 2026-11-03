# new_custom_object fields

Source: <https://developer.devrev.ai/airsync/object-types/new_custom_object>
Scraped: 2026-11-03

Field reference for the `new_custom_object` target. Required fields must be mapped or have a supported creation fallback.

Catalog generated July 13, 2026. Validate the mapping in your target organization. Can Load means external → DevRev; Can Extract means DevRev → external. See [field rules](../object-field-contract.md) for required values and references.

New custom object is an example of how custom objects look in the context of AirSync mapping.

**Resource Type:** `custom_object`

**Capabilities:** Can Extract, Can Load, Can Subtype

## Fields

| Field                 | Type                          | Required | Description                                                                                |
| --------------------- | ----------------------------- | -------- | ------------------------------------------------------------------------------------------ |
| `airsync_shared_with` | permission (collection)       |          | List of users and groups who have explicit access to the item and the corresponding roles. |
| `created_by_id`       | reference → \[#category:user] |          | User ID of the user that created the object.                                               |
| `description`         | rich\_text                    |          | Description of the object.                                                                 |
| `item_url_field`      | text                          |          | Link to the item in the origin system.                                                     |
| `modified_by_id`      | reference → \[#category:user] |          | User ID of the user that last modified the object.                                         |
| `title`               | text                          |          | Title of the object.                                                                       |
