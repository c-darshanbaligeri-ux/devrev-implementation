# unified_authorization_policy fields

Source: <https://developer.devrev.ai/airsync/object-types/unified_authorization_policy>
Scraped: 2026-11-03

Field reference for the `unified_authorization_policy` target. Required fields must be mapped or have a supported creation fallback.

Catalog generated July 13, 2026. Validate the mapping in your target organization. Can Load means external → DevRev; Can Extract means DevRev → external. See [field rules](../object-field-contract.md) for required values and references.

The authorization policy object is the intermediate object type for creating MFZ object types: `role`, `role_set`, and `access_control_entry`.

**Resource Type:** `unified_authorization_policy`

**Capabilities:** Can Load

## Fields

| Field                | Type                                                                                                                                                   | Required | Description                                                                             |
| -------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ | -------- | --------------------------------------------------------------------------------------- |
| `conditional_access` | conditional\_privilege (collection)                                                                                                                    |          | Fields or objects and privileges the role applies to if the defined conditions are met. |
| `field_access`       | field\_privilege (collection)                                                                                                                          |          | Fields and privileges the role applies to.                                              |
| `groups`             | reference (collection) → \[#record:airdrop\_platform\_group #record:group]                                                                             |          | Groups this role applies to.                                                            |
| `name`               | text                                                                                                                                                   |          | The name of the authorization policy instance.                                          |
| `object_access`      | record\_type\_privilege (collection) → \[#category:custom\_object #category:part #category:work #record:article #record:conversation #record:incident] | ✔︎       | Privileges and objects the role applies to.                                             |
| `users`              | reference (collection) → \[#record:devu #record:revu]                                                                                                  |          | Users this role applies to.                                                             |
