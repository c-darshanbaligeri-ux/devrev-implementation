# Discover external sync units

Source: <https://developer.devrev.ai/airsync/external-sync-units-extraction>
Scraped: 2026-11-03

An external sync unit (ESU) is the source container a user selects for an import: a project, repository, workspace or another stable data boundary. Discovery lists containers accessible to the configured source credentials. All later extraction must use the selected `event.payload.event_context.external_sync_unit_id` consistently.

## Discovery input and output

The incoming event is `START_EXTRACTING_EXTERNAL_SYNC_UNITS`; the default worker is `workers/external-sync-units-extraction.js`. Read authentication from the configured [connection/keyring contract](manifest.md), and use the source API to enumerate accessible containers.

Upload records to `AirSyncDefaultItemTypes.EXTERNAL_SYNC_UNITS`. Do not return units inline in `TaskResult`.

| `ExternalSyncUnit` field | Required | Meaning                                                     |
| ------------------------ | -------- | ----------------------------------------------------------- |
| `id: string`             | Yes      | Stable unique external container ID                         |
| `name: string`           | Yes      | Human-readable selectable name                              |
| `description: string`    | Yes      | Container description; use an empty string when unavailable |
| `item_count: number`     | No       | Lightweight source count when available                     |
| `item_type: string`      | No       | Source record-type identifier represented by the count      |

Omit an unavailable count rather than retrieving every record solely to count it. The SDK types permit omission; do not invent a count of zero. Avoid exposing containers that the connection cannot read.

<span id="v2-worker-example" />

## Worker example

This bounded worker uploads one example container. Replace the literal with a paginated, bounded source discovery implementation.

```typescript
import {
  AirSyncDefaultItemTypes,
  ExternalSyncUnit,
  processExtractionTask,
} from '@devrev/airsync-sdk';

processExtractionTask<Record<string, never>>({
  task: async ({ adapter }) => {
    const itemType = AirSyncDefaultItemTypes.EXTERNAL_SYNC_UNITS;
    adapter.initializeRepos([{ itemType }]);
    const repo = adapter.getRepo(itemType);
    if (!repo) throw new Error('External sync unit repo is missing');

    const units: ExternalSyncUnit[] = [{
      id: 'project-123',
      name: 'Example project',
      description: 'A project visible to this connection',
    }];
    await repo.push(units);
    return { status: 'success' };
  },
  onTimeout: async () => ({
    status: 'error',
    error: { message: 'External sync unit discovery exceeded its time budget' },
  }),
});
```

The SDK batches repo output and handles sync-unit upload confirmation automatically. `overriddenOptions: { batchSize: 25_000 }` can change the repo batch size, but the source request still needs bounded pagination and memory use. A larger batch does not extend discovery's runtime budget.

## Failure and verification

This phase is stateless and non-resumable. Return success only after all units are discovered and pushed; return an error when required discovery fails. `progress` and `delay` are invalid results here. Do not present a truncated source listing as complete after a rate limit or timeout.

Test empty accounts, inaccessible containers, duplicate display names, large listings and revoked credentials. A live import should show the same stable IDs and accessible names as the source account. Verify the selected ID is subsequently honored by metadata, data and attachment workers.

Related: [runtime](runtime.md), [metadata extraction](metadata-extraction.md), [public template](https://github.com/devrev/airsync-template/blob/main/code/src/functions/extraction/workers/external-sync-units-extraction.ts).

Next: [Define the external data schema](external-domain-metadata.md).
