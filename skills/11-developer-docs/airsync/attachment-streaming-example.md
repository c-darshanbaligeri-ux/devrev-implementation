# Attachment import worker example

Source: <https://developer.devrev.ai/airsync/attachment-streaming-example>
Scraped: 2026-11-03

Use this with the [attachment descriptor contract](extract-attachments.md). The [runtime](runtime.md) routes extraction events to this worker.

<span id="bounded-v2-streaming-example" />

## Bounded streaming example

This complete worker uses the public Axios package for Node streams. Its source example serves stable HTTPS URLs; add the authentication required by your actual source, and never log signed URLs or credential headers.

```typescript
import axios from 'axios';
import {
  ExternalSystemAttachmentStreamingFunction,
  processExtractionTask,
} from '@devrev/airsync-sdk';

const getFileStream: ExternalSystemAttachmentStreamingFunction = async ({ item }) => {
  try {
    const response = await axios.get(item.url, {
      responseType: 'stream',
      timeout: 30_000,
      headers: { 'Accept-Encoding': 'identity' },
    });
    return { status: 'success', httpStream: response };
  } catch (error) {
    if (axios.isAxiosError(error) && error.response?.status === 429) {
      const value = Number(error.response.headers['retry-after']);
      return {
        status: 'delay',
        delaySeconds: Number.isFinite(value) && value > 0 ? value : 30,
      };
    }
    return {
      status: 'error',
      error: { message: 'Unable to fetch source attachment content' },
    };
  }
};

processExtractionTask<Record<string, never>>({
  task: async ({ adapter }) => adapter.streamAttachments({
    stream: getFileStream,
    batchSize: 4,
  }),
});
```

The `stream` function receives `{ item: NormalizedAttachment, event: AirSyncEvent }`. Return `{ status: 'success', httpStream: { data, headers } }`, a delay with `delaySeconds`, or an error. `data` must be a consumable Node-readable stream. Preserve `content-type` and trustworthy `content-length`; use identity encoding so the reported length corresponds to streamed bytes. The example parses numeric `Retry-After`; implement HTTP dates when your source uses them.

Related: [Attachment extraction](extract-attachments.md).

Optional capabilities: [Import access rules](data-model/permissions.md).

If these optional capabilities are outside your connector's scope, continue to [Run connector events locally](local-development.md).
