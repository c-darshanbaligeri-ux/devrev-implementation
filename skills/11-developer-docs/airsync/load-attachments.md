# Upload attachments to the external system

Source: <https://developer.devrev.ai/airsync/load-attachments>
Scraped: 2026-11-03

Attachment loading uploads DevRev attachments to the external system. Use it when the external API accepts files and the connector declares loadable attachments on the relevant record types. Data loading must establish any parent records needed by the external API before the upload.

## Attachment loading inputs

Call `adapter.loadAttachments({ create })`. The callback receives `ExternalSystemItemLoadingParams` with the attachment, mapper client and event:

| Attachment field                      | Meaning                                                 |
| ------------------------------------- | ------------------------------------------------------- |
| `reference_id`                        | DevRev attachment identity used in the resulting mapper |
| `parent_reference_id`                 | DevRev identity of its parent                           |
| `parent_type`                         | Parent record type                                      |
| `parent_id`, `grand_parent_id`        | Optional resolved external parent identities            |
| `file_name`, `file_type`, `file_size` | File metadata; size is in bytes                         |
| `url`, `valid_until`                  | Download URL and its expiry                             |
| `created_by_id`, `modified_by_id`     | Actor identifiers                                       |
| `created_date`, `modified_date`       | Attachment timestamps                                   |

Use `parent_id` when it matches the external API's required parent identity. If it is absent, resolve `parent_reference_id` through [object mappers](object-mappers.md). Do not send a DevRev DON to an endpoint that requires an external record ID.

Fetch the content using the supplied download URL while it is valid. The external API may require multipart upload, a stream or a separate upload-session workflow; the connector owns that implementation. Do not buffer unbounded files or log signed URLs. Handle file-size and content-type restrictions explicitly.

<span id="v2-attachment-worker" />

## Attachment worker

The template helper paths below define the connector's HTTP client and denormalization boundary. Replace their placeholders with a real external upload implementation.

```typescript
import {
  ExternalSystemAttachment,
  ExternalSystemItemLoadingParams,
  ExternalSystemItemLoadingResponse,
  processLoadingTask,
} from '@devrev/airsync-sdk';
import { HttpClient } from '../../external-system/http-client';
import { denormalizeAttachment } from '../../external-system/data-denormalization';
import type { LoaderState } from '../index';

async function createAttachment({ item, mappers, event }: ExternalSystemItemLoadingParams<ExternalSystemAttachment>): Promise<ExternalSystemItemLoadingResponse> {
  const lookup = item.parent_id ? null : await mappers.getByTargetId({
    sync_unit: event.payload.event_context.sync_unit,
    target: item.parent_reference_id,
  });
  const parentId = item.parent_id ?? lookup?.sync_mapper_record.external_ids[0];
  if (!parentId) {
    return { status: 'error', error: { message: 'External attachment parent is missing.' } };
  }
  const client = new HttpClient(event);
  return client.createAttachment({
    ...denormalizeAttachment(item),
    parent_id: parentId,
  });
}

processLoadingTask<LoaderState>({
  task: async ({ adapter }) => adapter.loadAttachments({ create: createAttachment }),
});
```

See the public [template worker](https://github.com/devrev/airsync-template/blob/main/code/src/functions/loading/workers/load-attachments.ts), [denormalization module](https://github.com/devrev/airsync-template/blob/main/code/src/functions/external-system/data-denormalization.ts) and [HTTP client](https://github.com/devrev/airsync-template/blob/main/code/src/functions/external-system/http-client.ts). The external upload callback must return the uploaded file's external identity, not the parent ID.

## Outcomes and recovery

The callback result uses the same `success`, `delay` and `error` union as [data loading](load-data.md#loading-callback-results). `delaySeconds` is in seconds. A callback error records a failed attachment and advances; a delay leaves the attachment pending. A thrown exception or mapper persistence failure fails the phase.

On success the SDK creates a mapper from the returned external ID to `reference_id`. Attachment mapper creation does not persist the callback's optional `modifiedDate` as an external version. Do not assume the data-record loop-prevention behavior applies to attachment writes.

The SDK tracks file and line continuation and emits reports. Return `loadAttachments()`'s `TaskResult`; no manual emit or timeout payload is needed. External upload and mapper creation are separate operations, so retries must handle a successful upload followed by a mapper failure. Prefer a stable external idempotency key or an external lookup before repeating an upload.

## Verification

Test an upload to an existing parent and to a parent created during data loading. Verify bytes, filename, content type, parent relationship and mapper identity. Test an expired URL, missing parent, external size rejection, rate limiting and continuation. Confirm rejected attachments appear in failed reports and are not silently treated as successful uploads.

Related contracts: [reverse sync lifecycle](loading-phases.md), [relationship ordering](reverse-sync-ordering.md), [attachment extraction](extract-attachments.md).

Next: [Prevent repeated updates between systems](loop-prevention.md).
