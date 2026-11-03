# Handle sync-state cleanup events

Source: <https://developer.devrev.ai/airsync/data-attachments-deletion>
Scraped: 2026-11-03

State-deletion events end the connector's stored extraction/loading state lifecycle. The platform owns backend state deletion. With no custom worker override, the SDK acknowledges these events from the main thread. Most connectors require no deletion worker.

These events do not define source record deletion, target record deletion or reverse-sync delete callbacks. Do not interpret deletion of an import's runtime state as authority to remove customer records in the external system.

## Supported deletion events

| Incoming `EventType`                         | Success event                               | Error event                                  |
| -------------------------------------------- | ------------------------------------------- | -------------------------------------------- |
| `START_DELETING_EXTRACTOR_STATE`             | `EXTRACTOR_STATE_DELETION_DONE`             | `EXTRACTOR_STATE_DELETION_ERROR`             |
| `START_DELETING_EXTRACTOR_ATTACHMENTS_STATE` | `EXTRACTOR_ATTACHMENTS_STATE_DELETION_DONE` | `EXTRACTOR_ATTACHMENTS_STATE_DELETION_ERROR` |
| `START_DELETING_LOADER_STATE`                | `LOADER_STATE_DELETION_DONE`                | `LOADER_STATE_DELETION_ERROR`                |
| `START_DELETING_LOADER_ATTACHMENT_STATE`     | `LOADER_ATTACHMENT_STATE_DELETION_DONE`     | `LOADER_ATTACHMENT_STATE_DELETION_ERROR`     |

Use the event constants exported as `EventType.StartDeletingExtractorState`, `StartDeletingExtractorAttachmentsState`, `StartDeletingLoaderState` and `StartDeletingLoaderAttachmentState`. The SDK emits the mapped success event when no override is supplied.

## Optional connector cleanup

A custom worker may clean up connector-created resources such as a registered webhook when that is part of its documented lifecycle. Route it explicitly through `workerPathOverrides`; no default deletion worker path is inferred.

This routing fragment belongs in a `spawn` call from the [runtime entry point](runtime.md):

```typescript
workerPathOverrides: {
  [EventType.StartDeletingExtractorState]: '/workers/cleanup.js',
}
```

Import `EventType` from `@devrev/airsync-sdk`. Include the leading slash: the SDK concatenates the override onto `baseWorkerPath`. The following complete extraction cleanup worker demonstrates acknowledgement; replace its task body with bounded, idempotent cleanup of connector-owned resources only.

```typescript
import { processExtractionTask } from '@devrev/airsync-sdk';

processExtractionTask<Record<string, never>>({
  task: async () => ({ status: 'success' }),
  onTimeout: async () => ({
    status: 'error',
    error: { message: 'Connector cleanup exceeded its time budget' },
  }),
});
```

For loader deletion events, use `processLoadingTask` instead. Deletion phases are stateless and non-resumable: they accept success or error, not progress or delay. Do not rely on persisted connector state being loaded for cleanup, and do not implement a multi-invocation cleanup workflow through these events.

## Failure and verification

A cleanup failure returns error; it must not claim cleanup success before its side effects finish. Keep requests within the runtime budget and handle already-removed resources idempotently. Verify each unoverridden deletion event produces the matching acknowledgement, and that any custom worker leaves source business records intact. Test a missing resource, revoked cleanup permission and a timed-out source request.

Related: [runtime routing and state](runtime.md), [extraction lifecycle](extraction-phases.md), [reverse sync](loading-phases.md).
