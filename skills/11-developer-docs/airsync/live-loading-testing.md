# Verify live reverse sync

Source: <https://developer.devrev.ai/airsync/live-loading-testing>
Scraped: 2026-11-03

## Live reverse-sync validation

For a connector declaring loading, create a DevRev record and confirm exactly one corresponding external object. Update a mapped field and verify the correct external object changes. Test a reference to an already mapped object and one whose mapper is missing. Verify ordering for parents, children and attachments.

After the external write, run extraction again. It must preserve identity and converge without repeated create/update loops. Test rejected writes and rate limits: failures must be observable and resumable according to the loading contract. Validate attachment bytes and destination association when attachment loading is implemented.

Related: [Validation checklist](validation.md).

Next: [Connector implementation checklist](connector-checklist.md).
