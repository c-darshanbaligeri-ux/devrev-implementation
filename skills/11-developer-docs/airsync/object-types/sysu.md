# sysu fields

Source: <https://developer.devrev.ai/airsync/object-types/sysu>
Scraped: 2026-11-03

Field reference for the `sysu` target. Required fields must be mapped or have a supported creation fallback.

Catalog generated July 13, 2026. Validate the mapping in your target organization. Can Load means external → DevRev; Can Extract means DevRev → external. See [field rules](../object-field-contract.md) for required values and references.

**Resource Type:** `sys_user`

**Capabilities:** Can Load

## Fields

| Field          | Type | Required | Description                                                  |
| -------------- | ---- | -------- | ------------------------------------------------------------ |
| `display_name` | text | ✔︎       | The user's display name. The name is non-unique and mutable. |
| `full_name`    | text |          | Full name of the user.                                       |
