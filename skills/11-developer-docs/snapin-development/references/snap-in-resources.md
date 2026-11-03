# Snap-in resources

Source: <https://developer.devrev.ai/snapin-development/references/snap-in-resources>
Scraped: 2026-11-03

Snap-in resources are objects specific to each user for a snap-in. These objects can be

* Keyrings
* Inputs
* Event sources

For a snap-in to access these resources, the user must configure **My Settings** of the snap-in config and enable it.
The snap-in can get these resources using the `snap-ins.resources` [beta API](../../beta/api-reference/snap-ins.md#resources) by specifying the  snap-in ID in the `id` field and the user ID in the `user` field.

> **Note:**
>   This API can only be called by the service account associated with the snap-in.
