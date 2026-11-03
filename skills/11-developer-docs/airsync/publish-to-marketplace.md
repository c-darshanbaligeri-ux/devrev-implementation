# Publish to the marketplace

Source: <https://developer.devrev.ai/airsync/publish-to-marketplace>
Scraped: 2026-11-03

Marketplace publication distributes a deployed snap-in to other organizations. A listing must describe the connector's implemented behavior, required permissions and limits accurately. Deploy and [validate](validation.md) the exact version you intend to submit first.

## Prepare the listing

Have the snap-in package/version IDs, display name, summary, description and listing assets ready. State the external prerequisites, supported record types, initial/incremental behavior, attachments, reverse-sync support, permission behavior and important external API limits. Explain how users establish the connection and select a sync unit. Do not advertise a feature merely because the SDK or another connector supports it.

Complete an installation test with a user who has the documented permissions. Verify that OAuth credentials or developer keyrings are managed by the publisher as required; users should not need access to the publisher's source repository or development environment.

## Submission lifecycle

The [public DevRev CLI](../snapin-development/references/cli-install.md) provides interactive wizards for these operations:

```bash
devrev marketplace_submissions create
devrev marketplace_submissions transition
```

Creation produces a **Draft** submission. Transition the completed draft to **Waiting for review**. Marketplace administrators review it in **In review** and move it to **Approved** or **Rejected**. Submissions in **In review** or **Approved** cannot be modified. A rejected submission can return to **Draft** for corrections and another review.

An approved submission can be published:

```bash
devrev marketplace_items publish
devrev marketplace_items show YOUR_MARKETPLACE_ITEM_ID
```

Select the approved submission/item in the wizard and record the resulting item ID. Verify the item's published state and actual listing content. Approval and publication are separate operations.

## Updates and access

For an existing listing, create a new submission for that listing rather than a second independent listing. At most one item in a listing is published. Automatic upgrades are supported when the new version does not require user input/action, new global variables or new connections. Test existing syncs against the upgrade, especially persisted state and mapper compatibility.

Listings are public by default. Restricted listings can be shared with selected organizations using marketplace invitation controls. Changing a restricted listing to public is supported; changing a public listing back to restricted is not. Choose the intended access level before submission.

## Publication verification

Install the published item in a separate test organization using only the public instructions. Check connection creation, sync-unit discovery, default mappings, initial sync and incremental updates. Exercise attachments and reverse sync if advertised. Confirm installation does not depend on local test servers or development-only secrets.

Record the tested item/version, SDK version and observed results. See [marketplace listing reference](../snapin-development/marketplace-listings.md) for listing properties and sharing commands, and [deployment](deploy-to-organization.md) for version readiness and logs.
