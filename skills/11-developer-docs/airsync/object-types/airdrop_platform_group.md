# airdrop_platform_group fields

Source: <https://developer.devrev.ai/airsync/object-types/airdrop_platform_group>
Scraped: 2026-11-03

Field reference for the `airdrop_platform_group` target. Required fields must be mapped or have a supported creation fallback.

Catalog generated July 13, 2026. Validate the mapping in your target organization. Can Load means external → DevRev; Can Extract means DevRev → external. See [field rules](../object-field-contract.md) for required values and references.

AirSync platform group object type is the representation of the default DevRev groups.

**Resource Type:** `airdrop_platform_group`

**Capabilities:** Can Load

## Fields

| Field | Type | Required | Description                         |
| ----- | ---- | -------- | ----------------------------------- |
| `key` | enum | ✔︎       | Key of the platform provided group. |

## Enum values

**key**

| Value       | Name      | Description                                  |
| ----------- | --------- | -------------------------------------------- |
| `dev_users` | Dev users | "Dynamic dev users group created by DevRev". |
| `none`      | No group  | "No group selected".                         |
| `rev_users` | Rev users | "Dynamic rev users group created by DevRev". |
