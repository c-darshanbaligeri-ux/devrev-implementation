# Import external teams

Source: <https://developer.devrev.ai/airsync/data-model/external-teams>
Scraped: 2026-11-03

## Mapped external teams

Declare an ordinary external team record type and map it to DevRev `team`. Map the required `key` and `name`, optional `description`, and any external parent reference to target `parent_id`. The source field name can differ; its EDM declaration and field mapping must agree.

If a parent is mapped, that hierarchy is honored. Without a mapped parent, a sync-unit team becomes the fallback parent when one is defined. Without either, the team is created at the org level. Mapped team keys have the same stability and format constraints as a sync-unit team's key.

Records supporting a team reference can be scoped to mapped teams through the offered `team_id` field. Check the actual target's [supported field list](../supported-object-types.md); subtype scope remains separate from the record's team assignment.

For a mapped team's membership, map the record to `object_member` and set its required `target_object_type` mapping to the fixed enum value `team`. Use the external team identity in the normalized source data:

```json
{
  "object_id": "external-team-1",
  "add_member_ids": ["external-user-1", "external-user-2"]
}
```

Use membership removals when the source exposes them. An incremental member-addition record does not mean all other members should be removed.

## Team configuration choices

| Configuration                    | Resulting hierarchy                                                            |
| -------------------------------- | ------------------------------------------------------------------------------ |
| Sync-unit team only              | One container for the sync unit; no external team records are imported         |
| Sync-unit team plus mapped teams | Mapped teams use their explicit parent or fall back to the sync-unit team      |
| Mapped teams only                | Explicit external hierarchy is preserved; teams without a parent are org-level |

Issue/enhancement subtypes remain scoped to the sync-unit team, or Global when no sync-unit team exists. Record team assignment can follow a mapped team when supported by the target.

## Limits and failure behavior

* Team keys are immutable and must contain three to five uppercase letters.
* Keys must be unique across the org. On a collision with a team from another source, AirSync can alter the imported key; do not assume the visible key remains the source value.
* Teams are archived rather than deleted; archiving does not free a key for reuse.
* After defining `team_data`, continue providing it on later metadata runs. Omitting it can cause warnings and inconsistent expectations about team scope.
* References to missing or filtered users/teams must be tested; a valid membership JSON value does not prove the relationship was applied.

Do not generate random team keys on each metadata run or derive them from a display name that can change. Validate the key before submitting metadata.

Related: [Sync-unit teams](team-import.md).

Next: [Import and export rich text](rich-text-fields.md).
