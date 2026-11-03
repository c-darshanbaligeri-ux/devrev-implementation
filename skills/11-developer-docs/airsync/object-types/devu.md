# devu fields

Source: <https://developer.devrev.ai/airsync/object-types/devu>
Scraped: 2026-11-03

Field reference for the `devu` target. Required fields must be mapped or have a supported creation fallback.

Catalog generated July 13, 2026. Validate the mapping in your target organization. Can Load means external → DevRev; Can Extract means DevRev → external. See [field rules](../object-field-contract.md) for required values and references.

**Resource Type:** `dev_user`

**Capabilities:** Can Load

## Fields

| Field          | Type | Required | Description                                                  |
| -------------- | ---- | -------- | ------------------------------------------------------------ |
| `display_name` | text | ✔︎       | The user's display name. The name is non-unique and mutable. |
| `email`        | text |          | Email address of the user.                                   |
| `full_name`    | text |          | Full name of the user.                                       |

### Structs

#### external\_identity

| Field          | Type | Required | Description                                      |
| -------------- | ---- | -------- | ------------------------------------------------ |
| `display_name` | text |          | Display name of the user in the external source. |
| `id`           | text | ✔︎       | Unique ID of the user in the external source.    |
| `issuer`       | text | ✔︎       | Issuer of the external identity of the user.     |
| `state`        | enum | ✔︎       | State of the user in the external source.        |
