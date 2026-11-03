# Verify a live data import

Source: <https://developer.devrev.ai/airsync/live-extraction-testing>
Scraped: 2026-11-03

## Live initial and incremental sync

Use a test DevRev organization and external workspace with known fixtures. Connect through [deployment](deploy-to-organization.md) or the [live development server](local-development.md#receive-live-platform-events).

| Scenario                      | Observable pass condition                                                                          |
| ----------------------------- | -------------------------------------------------------------------------------------------------- |
| Connection                    | Valid credential succeeds; invalid/revoked credential is rejected or yields an actionable failure  |
| Sync-unit discovery           | Only accessible units are offered; IDs remain stable                                               |
| Metadata and default mapping  | Offered fields/types match extraction; required DevRev fields resolve                              |
| Initial sync                  | Expected objects, references, rich text and attachment contents appear once                        |
| Incremental sync              | One known external change updates the existing target object; unrelated records are not duplicated |
| Empty incremental window      | Run completes without creating or modifying unrelated objects                                      |
| Interrupted/rate-limited sync | Run resumes from durable progress and eventually completes without omissions                       |
| Selective extraction          | Excluded types stay excluded; included types still have valid required references                  |
| Permissions and teams         | Imported access and memberships match intended source visibility, where implemented                |
| Time-scoped/historical sync   | Objects outside the requested window stay excluded; completion behavior is correct                 |

Check expected values in DevRev, not only summary counts. Compare normalized artifacts with the metadata and final objects to distinguish extraction bugs from mapping bugs.

Related: [Validation checklist](validation.md).

Next: [Verify live reverse sync](live-loading-testing.md).
