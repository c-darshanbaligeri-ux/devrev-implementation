# How reverse sync works

Source: <https://developer.devrev.ai/airsync/loading-phases>
Scraped: 2026-11-03

## Reverse sync prerequisites

* Set `is_loadable: true` on the relevant external record types in [external domain metadata](external-domain-metadata.md).
* Enable reverse mapping on the record type and the writable fields in [initial domain mapping](initial-domain-mapping.md).
* Configure the manifest's loading function and event routing; see [manifest](manifest.md).
* Give the external connection the scopes needed to create and update the supported records. Read-only extraction credentials may be insufficient.
* Implement denormalization and HTTP writes for every item type the connector advertises as loadable.

The platform transforms DevRev changes into the external domain model before invoking a loading worker. Your worker then converts those transformed fields into the external API's request shape. This final conversion is **denormalization**; it is distinct from field mapping in the platform.

## Loading event contracts

| Capability                      | Incoming start / continuation                                | Default worker file        | Successful outcome                      |
| ------------------------------- | ------------------------------------------------------------ | -------------------------- | --------------------------------------- |
| Data writes                     | `START_LOADING_DATA` / `CONTINUE_LOADING_DATA`               | `workers/load-data`        | `DATA_LOADING_DONE`                     |
| Attachment writes               | `START_LOADING_ATTACHMENTS` / `CONTINUE_LOADING_ATTACHMENTS` | `workers/load-attachments` | `ATTACHMENT_LOADING_DONE`               |
| Data loader state cleanup       | `START_DELETING_LOADER_STATE`                                | SDK-managed                | `LOADER_STATE_DELETION_DONE`            |
| Attachment loader state cleanup | `START_DELETING_LOADER_ATTACHMENT_STATE`                     | SDK-managed                | `LOADER_ATTACHMENT_STATE_DELETION_DONE` |

Workers return a `TaskResult`. The SDK emits the phase-appropriate done, progress, delayed or error event exactly once. Connector code must not emit a second event. State cleanup removes synchronization state; it does not delete records in the external system.

## Loading entry point

This is a complete loading entry point for a template project with `resolveJsonModule` enabled and compiled worker files alongside the entry point:

```typescript
import { AirSyncEvent, spawn } from '@devrev/airsync-sdk';
import initialDomainMapping from '../external-system/initial_domain_mapping.json';

export type LoaderState = Record<string, never>;

export default async function run(events: AirSyncEvent[]): Promise<void> {
  for (const event of events) {
    await spawn<LoaderState>({
      event,
      initialState: {},
      initialDomainMapping,
      baseWorkerPath: __dirname,
    });
  }
}
```

The SDK resolves default worker paths from the incoming event. The public [template loading entry point](https://github.com/devrev/airsync-template/blob/main/code/src/functions/loading/index.ts) demonstrates this layout. Change worker routing only when the compiled layout differs.

## What starts reverse sync

Changes to records participating in a sync unit can initiate loading. When testing a new DevRev record, select the subtype established by the import and provide its required fields. The subtype identifies the external record type and recipe; creating an unrelated stock record is not a sufficient test.

## Verification

Verify both a new record and an update to an existing mapped record. Confirm external IDs are recorded, required fields and references survive transformation, and continuation does not duplicate writes. Test each claimed capability with the [data loading](load-data.md), [attachment loading](load-attachments.md) and [ordering and loop prevention](reverse-sync-ordering.md) contracts.

## Loading state and continuation

The SDK tracks loading progress. Return its result and preserve connector-owned state needed by your external writes.

Extractor and loader state are separate. `adapter.state` contains connector-owned state; the SDK owns its file positions, completion flags and reports. Do not construct or modify SDK state directly.

`adapter.loadItemTypes()` and `adapter.loadAttachments()` return `TaskResult` and resume from SDK-managed file positions. Return their result unchanged. A delay keeps the current item pending; a progress outcome schedules continuation in a new invocation. The SDK's soft timeout is capped at ten minutes. Do not rely on older documentation's thirteen-minute worker budget.

External writes and mapper persistence are separate operations. If an external write succeeds but persisting its mapper fails, the phase fails and the same write can be attempted again. Use the external API's idempotency mechanism where available, with a stable key derived from sync-unit and DevRev object identity.

Next: [Create and update external records](load-data.md).
