# Write related records in dependency order

Source: <https://developer.devrev.ai/airsync/reverse-sync-ordering>
Scraped: 2026-11-03

## Relationship ordering

`loadItemTypes()` processes supported transformer files in the order of the `itemTypesToLoad` array. Put referenced types before dependents, for example users before tasks and tasks before comments. This ordering is by item type, not a topological sort of records within a file. The SDK does not infer arbitrary external API dependencies.

Resolve DevRev references through `mappers.getByTargetId({ sync_unit, target })`. The returned object contains `sync_mapper_record`; missing records resolve to `null`. A missing mapper is different from an API failure. Validate that the chosen external ID is appropriate when a mapper contains multiple external IDs or labeled `secondary_ids`.

For self-referential records or cycles, design a connector-specific strategy supported by the external API: create without an optional relationship then patch it, or defer the dependent write until the target exists. Do not invent an external parent ID or create an unrelated parent to make a request succeed.

## Failure choices

| Condition                                   | Connector behavior                                                                                                  |
| ------------------------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| External rate limit                         | Return callback `delay` with `delaySeconds`; keep the pending item retryable                                        |
| Invalid record that cannot be written       | Return callback `error`; the SDK records a failed item and advances                                                 |
| Unexpected failure that must stop the batch | Throw a sanitized error or return a task-level `error` from custom orchestration                                    |
| Missing dependency                          | Apply the connector's documented deferral or item-failure strategy; never substitute a DevRev ID for an external ID |
| Write succeeded but mapper failed           | Recover using stable idempotency or external lookup before replay                                                   |

## Bidirectional verification

1. Import an external record and confirm its mapper.
2. Modify the mapped DevRev record and confirm one external update.
3. Extract the external record again using its actual resulting modification timestamp.
4. Confirm that the write does not produce a repeated back-and-forth update.
5. Make a new change directly in the external system; confirm that change still reaches DevRev.
6. Repeat with related records, a rate limit, continuation and a mapper persistence failure.

Test the cases independently. A no-op import is not sufficient evidence that reverse writes, loop prevention and external-originated updates all work.

<span id="loop-prevention" />

<span id="idempotency-across-retries" />

Related:

* [Loop prevention](loop-prevention.md).
* [Write retries and idempotency](write-idempotency.md).

Next: [Upload attachments to the external system](load-attachments.md).
